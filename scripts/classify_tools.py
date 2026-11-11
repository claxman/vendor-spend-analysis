"""Classification tooling for step 3: the batch builder, kept as it ran (copied into the repository in step 5 with its
paths pointed at the working files under qa/, prompts/ and scripts/).

It reflects the step 3 rules; rules added later (the risk note on large Optimize rows, the reader-facing wording,
the savings checks) live in qa/check_outputs.py, which is the authority.

  python scripts/classify_tools.py sheet NN   print the worksheet for batch NN: hints, groups, fixed decisions, research findings
  python scripts/classify_tools.py build NN   build outputs/batches/batch_NN.csv from qa/classification_lines/batch_NN.txt,
                                              validate, and update qa/verification_exceptions.csv
  python scripts/classify_tools.py log        assemble qa/verification_log.csv from the research logs in qa/research/logs

qa/classification_lines/batch_NN.txt holds one vendor per line, fields separated by " | ":
  vendor_id | department | sub_function | description | recommendation | rationale | risk_note | cluster number |
  is_addressable T/F | is_recurring T/F | confidence | verified T/F | source_url | exception reason (FALSE rows only)
"""
import csv
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FINDINGS_DIR = REPO / "qa" / "research" / "findings"
LOGS_DIR = REPO / "qa" / "research" / "logs"
LINES_DIR = REPO / "qa" / "classification_lines"
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO / "qa"))
import check_outputs as qa  # noqa: E402
from vsa_common import EM_DASH, EN_DASH, LINK_GROUPS, MERGE_GROUPS, names_group, section_rows  # noqa: E402

CLEAN = {r["vendor_id"]: r for r in csv.DictReader(open(REPO / "outputs/vendors_clean.csv", encoding="utf-8"))}
IDS = list(CLEAN)
DEPTS = [r[1] for r in section_rows((REPO / "docs/taxonomy.md").read_text(encoding="utf-8"), "Departments")]
CLUSTERS = [r[1] for r in section_rows((REPO / "docs/clusters.md").read_text(encoding="utf-8"), "Clusters")]
BANNED = qa.BANNED_PHRASES
EXCEPTIONS = REPO / "qa/verification_exceptions.csv"
LOG = REPO / "qa/verification_log.csv"


def batch_ids(nn: int) -> list[str]:
    return IDS[(nn - 1) * 40:nn * 40]


def hints() -> dict:
    out = {}
    text = (REPO / "docs/vendor_hints.md").read_text(encoding="utf-8").split("## Notes")[0]
    for line in text.splitlines():
        m = re.match(r"^\| (\d+) \| (.*?) \| (.*) \|$", line)
        if m:
            for vid in re.findall(r"`(V\d{4})`", m.group(3)):
                out.setdefault(vid, []).append(f"[{m.group(1)}] {m.group(2)}")
    return out


def groups_of(vid: str) -> list[str]:
    row = int(vid[1:])
    out = []
    for g in MERGE_GROUPS:
        if row in g["rows"]:
            out.append(f"MERGE {g['canonical']} rows {g['rows']} names {g['names']} (one recommendation)")
    for g in LINK_GROUPS:
        if row in g["rows"]:
            out.append(f"LINK {g['label']} rows {g['rows']} names {g['names']} ({g['recommendation']})")
    return out


def needs_cue(vid: str) -> bool:
    row = int(vid[1:])
    for g in MERGE_GROUPS + LINK_GROUPS:
        if row in g["rows"] and names_group(CLEAN[vid]["vendor_name_clean"], g["names"]):
            return True
    return False


def findings(nn: int) -> dict:
    out = {}
    for p in sorted(FINDINGS_DIR.glob(f"batch_{nn:02d}*_findings.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            vid = r["vendor_id"].strip()
            if vid not in out or r.get("verified", "").strip() == "TRUE":
                out[vid] = r
    return out


def sheet(nn: int) -> None:
    h, f = hints(), findings(nn)
    fixed = {}
    for vids, col, val, src in qa.DECISION_EXPECTATIONS:
        for v in vids:
            fixed.setdefault(v, []).append(f"{col}={val}")
    for vids, col, phrases, src in qa.WORDING_EXPECTATIONS:
        for v in vids:
            fixed.setdefault(v, []).append(f"{col} has " + " + ".join(phrases))
    for vid in batch_ids(nn):
        c = CLEAN[vid]
        print(f"== {vid} {c['vendor_name_clean']} | ${float(c['cost_usd']):,.0f}")
        for x in h.get(vid, []):
            print("   hint", x[:240])
        for x in groups_of(vid):
            print("   group", x, "| cue word needed" if needs_cue(vid) else "")
        if vid in fixed:
            print("   fixed", "; ".join(fixed[vid]))
        r = f.get(vid)
        if r:
            print(f"   web {r['verified']} {r['identity_confidence']} | {r['what_it_does']} | {r['country']} | {r['source_url']}")
            if r["hint_check"] not in ("agrees", "no hint"):
                print("   hint_check", r["hint_check"])
            if r["notes"]:
                print("   notes", r["notes"][:300])
        else:
            print("   web: no finding yet")


def words(s: str) -> int:
    return len(s.split())


def seen_urls() -> set:
    urls = set()
    for p in list(FINDINGS_DIR.glob("*.csv")) + list(LOGS_DIR.glob("*.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            for k in ("url_found", "source_url"):
                if r.get(k):
                    urls.add(r[k].strip())
    return urls


def build(nn: int) -> int:
    src = LINES_DIR / f"batch_{nn:02d}.txt"
    want = batch_ids(nn)
    rows, problems, reasons = [], [], {}
    seen = set()
    found, urls = findings(nn), seen_urls()
    for i, line in enumerate(src.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        f = [x.strip() for x in line.split(" | ")]
        if len(f) not in (13, 14):
            problems.append(f"line {i}: {len(f)} fields")
            continue
        vid, dept, sub, desc, rec, why, risk, clu, addr, recur, conf, ver, url = f[:13]
        reason = f[13] if len(f) == 14 else ""
        p = lambda msg: problems.append(f"{vid}: {msg}")  # noqa: E731
        if vid not in want:
            p("not in this batch")
            continue
        if vid in seen:
            p("twice")
        seen.add(vid)
        if dept not in DEPTS:
            p(f"department {dept!r}")
        if not clu.isdigit() or not 1 <= int(clu) <= 18:
            p(f"cluster {clu!r}")
            clu = "18"
        if rec not in ("Terminate", "Consolidate", "Optimize"):
            p(f"recommendation {rec!r}")
        if conf not in ("high", "medium", "low"):
            p(f"confidence {conf!r}")
        for name, v in (("addressable", addr), ("recurring", recur), ("verified", ver)):
            if v not in ("T", "F"):
                p(f"{name} {v!r}")
        if not 5 <= words(desc) <= 25:
            p(f"description has {words(desc)} words")
        for field, text in (("description", desc), ("rationale", why), ("sub_function", sub), ("risk_note", risk)):
            hits = [b for b in BANNED if b in text.lower()]
            if hits:
                p(f"{field} has banned phrase {hits}")
        if any(EM_DASH in x or EN_DASH in x for x in f):
            p("dash")
        if not why.endswith(".") or qa.sentence_count(why) != 1:
            p("rationale not one sentence ending in a full stop")
        if rec == "Optimize" and risk:
            p("risk_note must be empty for Optimize")
        if rec in ("Terminate", "Consolidate") and not risk:
            p("risk_note missing")
        if risk.endswith("."):
            p("risk_note should be a clause without a full stop")
        if url == "@":
            url = (found.get(vid) or {}).get("source_url", "").strip()
        if ver == "T" and not url.startswith("http"):
            p("verified without a URL")
        if ver == "T" and url not in urls:
            p(f"URL not seen in any lookup: {url}")
        if ver == "F":
            if url:
                p("unverified row with a URL")
            if not reason:
                p("unverified row without an exception reason")
            if not desc.rstrip(".").endswith("confirm with Finance"):
                p("unverified description must end with 'confirm with Finance'")
            if conf != "low":
                p("unverified row must be confidence low")
            reasons[vid] = reason
        if addr == "F" and not ("non-discretionary" in why and "savings base" in why):
            p("non-addressable rationale wording")
        if needs_cue(vid) and not names_group(why, qa.GROUP_CUES):
            p("grouped row whose name holds the group name needs a cue word")
        for g in MERGE_GROUPS + LINK_GROUPS:
            if int(vid[1:]) in g["rows"] and not names_group(why, g["names"]):
                p(f"rationale does not name group {g.get('canonical') or g.get('label')}")
        c = CLEAN[vid]
        rows.append({"vendor_id": vid, "vendor_name_original": c["vendor_name_raw"],
                     "vendor_name_clean": c["vendor_name_clean"], "spend_12m": c["cost_usd"], "department": dept,
                     "sub_function": sub, "description": desc, "recommendation": rec, "rationale": why,
                     "risk_note": risk, "cost_cluster": CLUSTERS[int(clu) - 1],
                     "is_addressable": "TRUE" if addr == "T" else "FALSE",
                     "is_recurring": "TRUE" if recur == "T" else "FALSE", "confidence": conf,
                     "verified": "TRUE" if ver == "T" else "FALSE", "source_url": url if ver == "T" else ""})
    missing = [v for v in want if v not in seen]
    if missing:
        problems.append("missing: " + ", ".join(missing))
    if problems:
        print("NOT WRITTEN. Problems:")
        for x in problems:
            print("  ", x)
        return 1
    rows.sort(key=lambda r: r["vendor_id"])
    out = REPO / "outputs/batches" / f"batch_{nn:02d}.csv"
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=qa.REQUIRED_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    existing = {}
    if EXCEPTIONS.exists():
        for r in csv.DictReader(open(EXCEPTIONS, encoding="utf-8")):
            existing[r["vendor_id"]] = r["reason"]
    for v in want:
        existing.pop(v, None)
    existing.update(reasons)
    with open(EXCEPTIONS, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["vendor_id", "reason"])
        for v in sorted(existing):
            w.writerow([v, existing[v]])
    from collections import Counter
    rc = Counter(r["recommendation"] for r in rows)
    print(f"wrote {out.name}: {len(rows)} rows; {sum(r['verified'] == 'TRUE' for r in rows)} verified, "
          f"{len(reasons)} exceptions; " + ", ".join(f"{k} {v}" for k, v in sorted(rc.items())))
    return 0


def assemble_log() -> int:
    rows = []
    for p in sorted(LOGS_DIR.glob("*_log.csv")):
        for r in csv.DictReader(open(p, encoding="utf-8")):
            rows.append({k: " ".join((r.get(k) or "").replace(EM_DASH, ", ").replace(EN_DASH, ", ").split())
                         for k in ("vendor_id", "query", "url_found", "established")})
    rows = [r for r in rows if re.fullmatch(r"V\d{4}", r["vendor_id"])]
    # A search the session limit refused never ran, so it is not a lookup; a failed fetch did run and stays.
    never_ran = re.compile(r"search not (run|performed)|no lookup (run|made)|no search run|\(not searched\)", re.I)
    rows = [r for r in rows if not never_ran.search(r["established"] + " " + r["query"])]
    rows.sort(key=lambda r: r["vendor_id"])          # stable: each vendor's lookups keep their order
    with open(LOG, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["vendor_id", "query", "url_found", "established"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{LOG.name}: {len(rows)} lookups for {len({r['vendor_id'] for r in rows})} vendors")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "sheet":
        sheet(int(sys.argv[2]))
    elif cmd == "build":
        sys.exit(build(int(sys.argv[2])))
    elif cmd == "log":
        sys.exit(assemble_log())
