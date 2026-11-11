#!/usr/bin/env python3
"""QA checks for the classification deliverable, outputs/vendors_classified.csv.

Where each rule comes from:
  CLAUDE.md                     one-line descriptions without the banned phrases, departments from the
                                taxonomy, three recommendations with a one-sentence rationale, no em dashes
  docs/taxonomy.md, clusters.md the allowed departments and cost clusters
  docs/savings_assumptions.md   the acquirer decisions and the depends_on tag of every savings assumption
                                (steps 2e and 2f), checked by S6
  docs/decisions.md             per-row deliverable (step 2c), group recommendation rule (step 2d), the
                                outcomes fixed for named rows (steps 2b to 2e), the columns of the
                                classification spec and the risk-note check (step 2d-fix), the verification
                                exceptions (step 2d-fix2), names matched by vendor_id with the rows in the
                                original sheet order (step 2d-fix3), the hardware rule and the advisers
                                kept in the recurring base (step 2e), the platform reclassification with the
                                one Optimize row allowed a risk note (step 3b), and the SaaS department
                                reading (step 3c)
  scripts/vsa_common.py         the merge and link groups, their recommendation scope and the names a
                                rationale may use for each group

Structural checks run now. The classification checks run once outputs/vendors_classified.csv exists;
until then they are reported as pending. C17 reads only the "Verification exceptions" heading of
qa/validation_report.md, which scripts/merge_validate.py writes from qa/verification_exceptions.csv; this
script never writes it. scripts/merge_validate.py runs these checks through run(), with full details.
The savings checks V1 to V8 (step 4) run once outputs/analysis/savings.csv exists: they read it against
the classification, the register docs/savings_assumptions.md and the roll-up tables of savings.md.

Usage:
    python qa/check_outputs.py              check the real files
    python qa/check_outputs.py --self-test  run the classification checks on a synthetic classification and
                                            validation report, first clean and then with planted errors, to
                                            show that each check catches what it should
Exit code 1 if any check fails.
"""
from __future__ import annotations

import copy
import csv
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from savings_model import (  # noqa: E402
    MNA_CLUSTER, MONEY_COLUMNS, ROLLUP_HEADINGS, SAVING_COLUMNS, SAVINGS_COLUMNS, format_row, load_register,
    render_rollup_sections, rollup, saving_row, to_float, totals as savings_totals,
)
from vsa_common import (  # noqa: E402
    EM_DASH, EN_DASH, LINK_GROUPS, MERGE_GROUPS, money, names_group, rel, section_rows, strip_accents,
)

CLASSIFIED = ROOT / "outputs" / "vendors_classified.csv"
SAVINGS_CSV = ROOT / "outputs" / "analysis" / "savings.csv"
SAVINGS_MD = ROOT / "outputs" / "analysis" / "savings.md"
CLEAN = ROOT / "outputs" / "vendors_clean.csv"
GROUPS = ROOT / "qa" / "vendor_groups.csv"
TAXONOMY = ROOT / "docs" / "taxonomy.md"
CLUSTERS = ROOT / "docs" / "clusters.md"
VALIDATION_REPORT = ROOT / "qa" / "validation_report.md"
EXCEPTIONS_HEADING = "Verification exceptions"
SAVINGS_ASSUMPTIONS = ROOT / "docs" / "savings_assumptions.md"
# The levers that are purely vendor actions: their assumptions carry depends_on none. Step 2f named the Salesforce
# licence audit, AWS savings plans, Navan policy and the insurance re-broke; step 4 restated the licence audit as the
# platform agreement and folded the re-broke into the without-decision case of the commercial insurance lever.
VENDOR_ACTION_LEVERS = ["Salesforce platform agreement", "AWS", "Navan"]

# The columns of the classification spec, in its order (docs/decisions.md, step 2d-fix).
REQUIRED_COLUMNS = ["vendor_id", "vendor_name_original", "vendor_name_clean", "spend_12m", "department",
                    "sub_function", "description", "recommendation", "rationale", "risk_note", "cost_cluster",
                    "is_addressable", "is_recurring", "confidence", "verified", "source_url"]
BOOLEAN_COLUMNS = ["is_addressable", "is_recurring", "verified"]
RECOMMENDATIONS = {"Terminate", "Consolidate", "Optimize"}
NEEDS_RISK_NOTE = {"Terminate", "Consolidate"}
CONFIDENCE = {"high", "medium", "low"}
BOOLEANS = {"TRUE", "FALSE"}
BANNED_PHRASES = ["business services", "software company", "service provider", "solutions", "various services",
                  "technology company"]
# When a row's own name already contains its group's name, the rationale must also show the grouping.
GROUP_CUES = ["group", "both", "two", "three", "four", "entities", "entity", "together", "linked", "alongside",
              "across", "other"]
ABBREVIATIONS = ["j.d.o.o.", "d.o.o.", "d.d.", "s.r.o.", "inc.", "ltd.", "co.", "s.l.", "p.c.", "p.p.", "dr.", "pte.",
                 "pty.", "e.g.", "i.e.", "vs.", "no.", "vl.", "mr.", "ms.", "st.", "u.s.", "u.k."]
PER_ROW_LINKS = {"Amazon", "Microsoft"}  # docs/decisions.md, step 2d; Sodexo and Pluxee became a merge in step 3
VENDOR_ID = re.compile(r"\bV\d{4}\b")
# Step 2e: employee hardware (the four Apple entities, Magazin Računalni Sistemi, Sniper Systems, HP, E-Disti,
# Currys) is Consolidate into group IT procurement; BDO, Bisley Law and Grant Thornton stay in the recurring base.
HARDWARE_IDS = ["V0066", "V0123", "V0131", "V0167", "V0172", "V0175", "V0229", "V0260", "V0378"]
RECURRING_ADVISER_IDS = ["V0004", "V0018", "V0029"]
# Optimize rows carry no risk note, except where a recorded decision allows one (step 3b).
OPTIMIZE_RISK_NOTE_EXCEPTIONS = {
    "V0002": "step 3b: the product depends on the Salesforce platform, so the lever is commercial terms, never exit",
}
# True lists every item in a check's detail instead of the first few; scripts/merge_validate.py sets it so that
# qa/validation_report.md shows every failure in full.
FULL_DETAIL = False

# Outcomes fixed by recorded decisions: (vendor_ids, column, expected value, source).
DECISION_EXPECTATIONS = [
    (["V0014", "V0103"], "recommendation", "Optimize", "step 2d: AWS is Optimize"),
    (["V0203", "V0291"], "recommendation", "Terminate",
     "steps 2d and 2e: Amazon marketplaces, marketplace purchases through AP"),
    (["V0081"], "recommendation", "Consolidate", "step 2d: Microsoft 365, two productivity suites"),
    (["V0026"], "recommendation", "Optimize", "step 2d: LinkedIn, seat review"),
    (["V0125"], "department", "Engineering", "step 2d: npm follows the developer-tool rule (taxonomy rule 9)"),
    (["V0125"], "cost_cluster", "Software subscriptions (non-Salesforce)",
     "step 2d: npm follows the developer-tool rule (clusters C10)"),
    (["V0015", "V0093"], "department", "Sales", "step 2b: Telefónica"),
    (["V0015", "V0093"], "recommendation", "Optimize", "step 2b: Telefónica"),
    (["V0015", "V0093"], "is_addressable", "FALSE", "step 2b: Telefónica"),
    (["V0030", "V0086", "V0186"], "recommendation", "Optimize", "steps 2b and 2c: student labour"),
    (["V0030", "V0086", "V0186"], "is_addressable", "TRUE", "step 2b: student labour"),
    (["V0030", "V0086", "V0186"], "cost_cluster", "Student labour", "step 2b: student labour"),
    (["V0034"], "department", "G&A", "step 2b: Mason Frank"),
    (["V0034"], "cost_cluster", "Recruiting and HR outsourcing",
     "step 3b: Mason Frank, whose lever is ending the agency, not the Salesforce contract"),
    (["V0173"], "department", "G&A", "step 3c: Slack is corporate IT, company-wide messaging"),
    (["V0173"], "cost_cluster", "Salesforce platform", "step 2b: Slack"),
    (HARDWARE_IDS, "recommendation", "Consolidate", "step 2e: employee hardware, into group IT procurement"),
    (RECURRING_ADVISER_IDS, "is_recurring", "TRUE",
     "step 2e: advisers whose spend may include sale-related work stay in the recurring base"),
    (["V0002"], "department", "SaaS", "step 3c: Salesforce is the platform the hosted product runs on"),
    (["V0002", "V0006"], "recommendation", "Optimize", "step 3b: commercial terms for the platform and PDF Butler"),
    (["V0002", "V0006"], "cost_cluster", "Salesforce platform", "step 3b: Salesforce platform"),
    (["V0006"], "department", "SaaS", "step 3c: PDF Butler, a component delivered with the product"),
    (["V0014", "V0103", "V0130", "V0214", "V0278", "V0311", "V0350"], "department", "SaaS",
     "step 3c: hosting, logging, domains, DNS and monitoring run the hosted product"),
    (["V0023", "V0081"], "department", "G&A", "step 3c: the two productivity suites are corporate IT"),
    (["V0009"], "department", "Engineering", "step 3b: Weking, outsourced engineering"),
    (["V0009"], "cost_cluster", "Outsourced engineering and contractors", "step 3b: Weking"),
    (["V0009", "V0018"], "recommendation", "Consolidate",
     "step 3b: Weking into the group's engineering sourcing model; Bisley Law stays Consolidate"),
    (["V0009"], "confidence", "low", "step 3b: Weking stays low confidence"),
    (["V0284"], "is_addressable", "FALSE", "step 3b: NSDL, as in the forensic exclusion"),
    (["V0284"], "cost_cluster", "Statutory and government", "step 3b: NSDL"),
]
# Phrases a field must contain: (vendor_ids, column, phrases, source).
WORDING_EXPECTATIONS = [
    (["V0015", "V0093"], "rationale", ["rebate", "revenue"], "step 2b: Telefónica rebates would belong against revenue"),
    (["V0030", "V0086", "V0186"], "rationale", ["hiring plan"], "step 2b: student labour rationale"),
    (HARDWARE_IDS, "rationale", ["group it procurement"], "step 2e: hardware rationale names group IT procurement"),
    (["V0002"], "rationale", ["change of control"], "step 3b: renegotiate the platform agreement at change of control"),
    (["V0002"], "risk_note", ["never exit"], "step 3b: the product depends on the platform"),
    (["V0006"], "rationale", ["oem"], "step 3b: PDF Butler, OEM or volume pricing"),
    (["V0006"], "description", ["confirm oem terms with finance"], "step 3b: PDF Butler, OEM terms"),
    (["V0009"], "rationale", ["engineering sourcing model"], "step 3b: Weking, the group's engineering sourcing model"),
    (["V0009"], "risk_note", ["product knowledge"], "step 3b: Weking, product knowledge transferred first"),
    (["V0009"], "description", ["confirm with finance"], "step 3b: Weking keeps \"confirm with Finance\""),
    (["V0018"], "risk_note", ["companies house", "non-trading"], "step 3b: Bisley Law control finding"),
    (["V0023", "V0081", "V0173"], "sub_function", ["corporate it"],
     "step 3c: company-wide software carries a sub_function that starts Corporate IT"),
]
# Each fixed row's clean name must contain this, so a mistyped id cannot test the wrong vendor.
EXPECTED_NAMES = {"V0014": "Amazon Web Services", "V0103": "Amazon Web Services", "V0203": "Amazon",
                  "V0291": "Amazon", "V0081": "Microsoft", "V0026": "LinkedIn", "V0125": "npm",
                  "V0015": "Telefonica", "V0093": "Telefonica", "V0030": "Studentski Centar",
                  "V0086": "Studentski Centar", "V0186": "Studentski Centar", "V0034": "Mason Frank",
                  "V0173": "Slack", "V0066": "Racunalni Sistemi", "V0123": "Apple", "V0131": "Sniper Systems",
                  "V0167": "HP", "V0172": "Apple", "V0175": "Apple", "V0229": "Apple", "V0260": "E-Disti",
                  "V0378": "Currys", "V0004": "BDO", "V0018": "Bisley Law", "V0029": "Grant Thornton",
                  "V0002": "Salesforce", "V0006": "Cloudcrossing", "V0009": "Weking",
                  "V0284": "National Securities Depository", "V0023": "Cloud Technology", "V0130": "Papertrail",
                  "V0214": "GoDaddy", "V0278": "DNSimple", "V0311": "SolarWinds", "V0350": "Uptime Robot"}


# ---------------------------------------------------------------- helpers

def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def plain(s: str) -> str:
    return strip_accents(s).lower()


def groups() -> list[dict]:
    out = [{"kind": "merge", "name": g["canonical"], "ids": [f"V{r:04d}" for r in g["rows"]], "shared": True,
            "names": g["names"], "status": g["status"]} for g in MERGE_GROUPS]
    out += [{"kind": "link", "name": g["label"], "ids": [f"V{r:04d}" for r in g["rows"]],
             "shared": g["recommendation"] == "shared", "names": g["names"], "status": g["recommendation"]}
            for g in LINK_GROUPS]
    return out


def name_text(entry) -> str:
    return " and ".join(entry) if isinstance(entry, list) else entry


def sentence_count(text: str) -> int:
    t = text
    for abbr in ABBREVIATIONS:
        t = re.sub(re.escape(abbr), abbr.replace(".", ""), t, flags=re.IGNORECASE)
    return len(re.findall(r"[.!?]\s+(?=[A-Z0-9\"'(])", t)) + 1


def verification_exceptions(text: str | None) -> tuple[dict[str, str], list[str]]:
    """Rows listed under the heading "Verification exceptions": ({vendor_id: reason}, problems).

    Only lines under a heading whose text is exactly "Verification exceptions" count, up to the next heading
    of the same or a higher level. A line that carries a vendor_id lists that row; it must carry exactly one
    vendor_id and a reason on the same line. Lines without a vendor_id are ignored, as is the rest of the file.
    """
    listed: dict[str, str] = {}
    problems: list[str] = []
    if text is None:
        return listed, problems
    lines = text.splitlines()
    for i, line in enumerate(lines):
        m = re.match(r"^(#{1,6})\s+(.*?)\s*#*\s*$", line)
        if not m or m.group(2) != EXCEPTIONS_HEADING:
            continue
        level = len(m.group(1))
        for nxt in lines[i + 1:]:
            h = re.match(r"^(#{1,6})\s", nxt)
            if h and len(h.group(1)) <= level:
                break
            ids = list(dict.fromkeys(VENDOR_ID.findall(nxt)))
            if not ids:
                continue
            if len(ids) > 1:
                problems.append(f"one line lists several ids ({', '.join(ids)})")
                continue
            reason = re.sub(r"^\s*(?:\d+[.)]|[-*+>])\s*", "", nxt)   # list marker
            reason = VENDOR_ID.sub("", reason)
            reason = reason.strip(" \t|:`.-")
            if not re.search(r"[A-Za-z]", reason):
                problems.append(f"{ids[0]} has no reason")
                continue
            listed[ids[0]] = reason
    return listed, problems


def tag_problems(text: str) -> tuple[int, int, list[str]]:
    """The depends_on tags of docs/savings_assumptions.md: (assumptions, decisions, problems).

    Every row of the "Assumptions" table carries `none` or one or more names from the "Acquirer decisions"
    table, never both; the levers named as vendor actions carry `none`.
    """
    names = [r[0].strip("`") for r in section_rows(text, "Acquirer decisions")[1:]]   # row 0 is the header
    table_rows = section_rows(text, "Assumptions")
    if not table_rows or "depends_on" not in table_rows[0]:
        return 0, len(names), ["the Assumptions table has no depends_on column"]
    col = table_rows[0].index("depends_on")
    rows = table_rows[1:]
    problems = [f"decision {n} is registered twice" for n in sorted({n for n in names if names.count(n) > 1})]
    tags: dict[str, list[str]] = {}
    for r in rows:
        cell = r[col] if len(r) > col else ""
        found = [t.strip().strip("`").strip() for t in cell.split(",")]
        found = [t for t in found if t]
        tags[r[0]] = found
        if not found:
            problems.append(f"{r[0]}: no depends_on tag")
        elif "none" in found and len(found) > 1:
            problems.append(f"{r[0]}: none together with a decision name")
        else:
            problems += [f"{r[0]}: {t} is not a registered decision" for t in found if t != "none" and t not in names]
    for lever in VENDOR_ACTION_LEVERS:
        if lever not in tags:
            problems.append(f"{lever}: no row")
        elif tags[lever] != ["none"]:
            problems.append(f"{lever}: tagged {', '.join(tags[lever]) or 'nothing'}, expected none (step 2f)")
    return len(rows), len(names), problems


class Results:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, str, str]] = []

    def add(self, cid: str, title: str, ok: bool | None, detail: str) -> None:
        status = "PENDING" if ok is None else ("PASS" if ok else "FAIL")
        self.items.append((cid, status, title, detail))

    def failed(self) -> list[str]:
        return [cid for cid, status, _, _ in self.items if status == "FAIL"]

    def show(self) -> None:
        for cid, status, title, detail in self.items:
            print(f"{status:7s} {cid:4s} {title} | {detail}")


def sample(items: list, k: int = 3) -> str:
    if FULL_DETAIL:
        k = len(items)
    return "; ".join(str(x) for x in items[:k]) + (f" (and {len(items) - k} more)" if len(items) > k else "")


# ---------------------------------------------------------------- structural checks (run now)

def structural_checks(res: Results, clean: list[dict]) -> None:
    ids = {r["vendor_id"] for r in clean}
    clean_names = {r["vendor_id"]: r["vendor_name_clean"] for r in clean}
    gs = groups()

    scopes_ok = all(g["status"] in ("shared", "per row") for g in gs if g["kind"] == "link")
    per_row = {g["name"] for g in gs if g["kind"] == "link" and not g["shared"]}
    res.add("S1", "Link groups are marked shared or per row; per row exactly for Amazon and Microsoft",
            scopes_ok and per_row == PER_ROW_LINKS, f"per row: {', '.join(sorted(per_row))}")

    unknown = [i for g in gs for i in g["ids"] if i not in ids]
    nameless = [g["name"] for g in gs if not g["names"]]
    res.add("S2", "Every group's rows exist and every group has names a rationale can use",
            not unknown and not nameless,
            f"{len(gs)} groups; unknown ids: {sample(unknown) or 'none'}; groups without names: {sample(nameless) or 'none'}")

    vg = {r["vendor_id"]: r for r in read_csv(GROUPS)}
    link_of = {i: g for g in gs if g["kind"] == "link" for i in g["ids"]}
    merge_of = {i: g for g in gs if g["kind"] == "merge" for i in g["ids"]}
    mismatches = []
    for vid, r in vg.items():
        want_link = link_of[vid]["status"] if vid in link_of else ""
        want_decision = merge_of[vid]["status"] if vid in merge_of else "keep"
        if r.get("link_recommendation", None) != want_link or r["decision"] != want_decision:
            mismatches.append(vid)
    res.add("S3", f"{rel(GROUPS)} agrees with the group definitions (decision, link recommendation)",
            not mismatches and len(vg) == len(ids), f"{len(vg)} rows; mismatches: {sample(mismatches) or 'none'}")

    wrong = [f"{vid} is {clean_names.get(vid)}" for vid, name in EXPECTED_NAMES.items()
             if plain(name) not in plain(clean_names.get(vid, ""))]
    res.add("S4", "Rows fixed by decisions are the vendors the decisions name", not wrong,
            f"{len(EXPECTED_NAMES)} rows; wrong: {sample(wrong) or 'none'}")

    deps = [r[1] for r in section_rows(TAXONOMY.read_text(encoding="utf-8"), "Departments")]
    clus = [r[1] for r in section_rows(CLUSTERS.read_text(encoding="utf-8"), "Clusters")]
    res.add("S5", "Taxonomy and cluster lists load (12 departments, 18 clusters)", len(deps) == 12 and len(clus) == 18,
            f"{len(deps)} departments, {len(clus)} clusters")

    n_rows, n_names, problems = tag_problems(SAVINGS_ASSUMPTIONS.read_text(encoding="utf-8"))
    res.add("S6", f"Every savings assumption in {rel(SAVINGS_ASSUMPTIONS)} carries depends_on: none, or decision names "
                  "registered there; the levers named as vendor actions carry none",
            not problems and n_rows > 0, f"{n_rows} assumptions, {n_names} decisions; problems: {sample(problems) or 'none'}")


# ---------------------------------------------------------------- classification checks

def classification_checks(res: Results, rows: list[dict], clean: list[dict], validation_text: str | None) -> None:
    deps = {r[1] for r in section_rows(TAXONOMY.read_text(encoding="utf-8"), "Departments")}
    clus = {r[1] for r in section_rows(CLUSTERS.read_text(encoding="utf-8"), "Clusters")}
    cols = set(rows[0].keys()) if rows else set()
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in cols]
    res.add("C1", "The columns of the classification spec are present", not missing_cols,
            f"{len(REQUIRED_COLUMNS)} required; missing: {', '.join(missing_cols) or 'none'}")
    if missing_cols:
        return

    by_id = {r["vendor_id"]: r for r in rows}
    want = [r["vendor_id"] for r in clean]
    seen: dict[str, int] = defaultdict(int)
    for r in rows:
        seen[r["vendor_id"]] += 1
    dupes = sorted(i for i, n in seen.items() if n > 1)
    missing = [i for i in want if i not in by_id]
    extra = [i for i in by_id if i not in set(want)]
    res.add("C2", f"One row per source row ({len(want)}), no duplicates, no extras",
            len(rows) == len(want) and not dupes and not missing and not extra,
            f"{len(rows)} rows; missing: {sample(missing) or 'none'}; extra: {sample(extra) or 'none'}; "
            f"duplicated: {sample(dupes) or 'none'}")

    bad = [f"{r['vendor_id']}: {r['department']}" for r in rows if r["department"] not in deps]
    res.add("C3", "Departments come from docs/taxonomy.md", not bad, f"bad: {sample(bad) or 'none'}")
    bad = [f"{r['vendor_id']}: {r['cost_cluster']}" for r in rows if r["cost_cluster"] not in clus]
    res.add("C4", "Cost clusters come from docs/clusters.md", not bad, f"bad: {sample(bad) or 'none'}")
    bad = [f"{r['vendor_id']}: {r['recommendation']}" for r in rows if r["recommendation"] not in RECOMMENDATIONS]
    res.add("C5", "Recommendations are Terminate, Consolidate or Optimize", not bad, f"bad: {sample(bad) or 'none'}")
    bad = [f"{r['vendor_id']}: {col}={r[col]!r}" for r in rows for col in BOOLEAN_COLUMNS if r[col] not in BOOLEANS]
    bad += [f"{r['vendor_id']}: confidence={r['confidence']!r}" for r in rows if r["confidence"] not in CONFIDENCE]
    res.add("C6", "is_addressable, is_recurring and verified are TRUE or FALSE; confidence is high, medium or low",
            not bad, f"bad: {sample(bad) or 'none'}")

    bad = []
    for r in rows:
        d = r["description"]
        hits = [p for p in BANNED_PHRASES if p in d.lower()]
        if not d.strip() or "\n" in d or hits:
            bad.append(f"{r['vendor_id']}: {', '.join(hits) or 'empty or multi-line'}")
    res.add("C7", "Descriptions are one non-empty line without the banned phrases", not bad, f"bad: {sample(bad) or 'none'}")

    bad = [r["vendor_id"] for r in rows
           if not r["rationale"].strip() or not r["rationale"].rstrip().endswith(".") or sentence_count(r["rationale"]) != 1]
    res.add("C8", "Rationales are one sentence ending in a full stop", not bad, f"bad: {sample(bad) or 'none'}")

    bad = [r["vendor_id"] for r in rows if any(EM_DASH in str(v) or EN_DASH in str(v) for v in r.values())]
    res.add("C9", "No em or en dash in any field", not bad, f"bad: {sample(bad) or 'none'}")

    try:
        total = math.fsum(float(r["spend_12m"]) for r in rows)
    except ValueError:
        total = float("nan")
    want_total = math.fsum(float(r["cost_usd"]) for r in clean)
    res.add("C10", "Total spend_12m equals the clean file's total exactly", total == want_total,
            f"${total:,.2f} against ${want_total:,.2f}")

    clean_names = {r["vendor_id"]: r["vendor_name_clean"] for r in clean}
    split, unnamed = [], []
    for g in groups():
        present = [by_id[i] for i in g["ids"] if i in by_id]
        if g["shared"] and len({r["recommendation"] for r in present}) > 1:
            split.append(f"{g['name']} ({', '.join(r['vendor_id'] + ' ' + r['recommendation'] for r in present)})")
        for r in present:
            rationale = r["rationale"]
            if not names_group(rationale, g["names"]):
                unnamed.append(f"{r['vendor_id']} does not name {g['name']}")
            elif names_group(clean_names.get(r["vendor_id"], ""), g["names"]) and not names_group(rationale, GROUP_CUES):
                unnamed.append(f"{r['vendor_id']} names {g['name']} only as its own name")
    res.add("C11", "Rows of each merge group and each shared link group carry one recommendation", not split,
            f"split: {sample(split) or 'none'}")
    res.add("C12", "Every grouped row's rationale names its group (per-row links included)", not unnamed,
            f"bad: {sample(unnamed) or 'none'}")

    bad = []
    for vids, col, expected, source in DECISION_EXPECTATIONS:
        for vid in vids:
            if vid in by_id and by_id[vid][col] != expected:
                bad.append(f"{vid} {col} is {by_id[vid][col]}, expected {expected} ({source})")
    res.add("C13", "Outcomes fixed by recorded decisions", not bad, f"bad: {sample(bad, 2) or 'none'}")

    bad = []
    for vids, col, phrases, source in WORDING_EXPECTATIONS:
        for vid in vids:
            if vid in by_id and not all(p in plain(by_id[vid][col]) for p in phrases):
                bad.append(f"{vid} {col} lacks {' and '.join(phrases)} ({source})")
    res.add("C14", "Rationale, risk-note and description wording fixed by recorded decisions", not bad,
            f"bad: {sample(bad, 2) or 'none'}")

    bad = [r["vendor_id"] for r in rows if r["is_addressable"] == "FALSE"
           and not ("non-discretionary" in plain(r["rationale"]) and "savings base" in plain(r["rationale"]))]
    res.add("C15", "Rows outside the savings base say \"non-discretionary, excluded from the savings base\"", not bad,
            f"bad: {sample(bad) or 'none'}")

    bad = [r["vendor_id"] for r in rows if r["recommendation"] in NEEDS_RISK_NOTE and not r["risk_note"].strip()]
    extra = [r["vendor_id"] for r in rows if r["recommendation"] == "Optimize" and r["risk_note"].strip()
             and r["vendor_id"] not in OPTIMIZE_RISK_NOTE_EXCEPTIONS]
    res.add("C16", "Every Terminate and Consolidate row has a risk_note; Optimize rows have none, except "
                   f"{', '.join(sorted(OPTIMIZE_RISK_NOTE_EXCEPTIONS))} (step 3b)", not bad and not extra,
            f"missing: {sample(bad) or 'none'}; on Optimize rows: {sample(extra) or 'none'}")

    listed, problems = verification_exceptions(validation_text)
    false_rows = {r["vendor_id"] for r in rows if r["verified"] == "FALSE"}
    unlisted = [r["vendor_id"] for r in rows if r["verified"] != "TRUE" and r["vendor_id"] not in listed]
    wrongly_listed = [i for i in listed if i not in false_rows]
    res.add("C17", f"Every row is verified TRUE, or FALSE and listed with a reason under \"{EXCEPTIONS_HEADING}\" in "
                   f"{rel(VALIDATION_REPORT)}; every listed id is FALSE in the file",
            not unlisted and not wrongly_listed and not problems,
            f"{len(false_rows)} rows FALSE; {len(listed)} listed"
            + ("" if validation_text is not None else f" ({rel(VALIDATION_REPORT)} not found)")
            + f"; not verified and not listed: {sample(unlisted) or 'none'}; listed but not FALSE in the file: "
              f"{sample(wrongly_listed) or 'none'}; format problems: {sample(problems) or 'none'}")

    # Names are matched by vendor_id (unknown ids are C2's job). The order must be the original sheet order,
    # vendor_id ascending, because the sheet columns are pasted straight from this file.
    clean_by_id = {c["vendor_id"]: c for c in clean}
    name_bad = [r["vendor_id"] for r in rows if r["vendor_id"] in clean_by_id
                and (r["vendor_name_original"], r["vendor_name_clean"])
                != (clean_by_id[r["vendor_id"]]["vendor_name_raw"], clean_by_id[r["vendor_id"]]["vendor_name_clean"])]
    order_bad = []
    for line in range(1, len(rows)):
        prev, cur = rows[line - 1]["vendor_id"], rows[line]["vendor_id"]
        if not (VENDOR_ID.fullmatch(prev) and VENDOR_ID.fullmatch(cur) and int(cur[1:]) > int(prev[1:])):
            order_bad.append(f"data row {line + 1} holds {cur} after {prev}")
    res.add("C18", f"vendor_name_original and vendor_name_clean match {rel(CLEAN)} by vendor_id, and the rows are in "
                   "the original sheet order (vendor_id ascending)", not name_bad and not order_bad,
            f"name mismatches: {sample(name_bad) or 'none'}; out of order at {len(order_bad)} positions"
            + (f", first: {order_bad[0]}" if order_bad else ""))


# ---------------------------------------------------------------- self-test

SYNTHETIC_VALIDATION_REPORT = "\n".join([
    "# Validation report (synthetic, for the QA self-test)",
    "",
    "An introduction that mentions V0002 Salesforce UK Ltd outside the heading; it does not count.",
    "",
    "## Verification exceptions",
    "",
    "Rows that could not be verified, one per line:",
    "",
    "- V0009: Croatian company whose function no public source confirms.",
    "- V0160: individual payee; there is no public record to check against.",
    "- V0325: the source has no vendor name.",
    "",
    "## Other notes",
    "",
    "- V0004 BDO LLP is mentioned here, outside the heading, and does not count.",
])
SYNTHETIC_UNVERIFIED = ["V0009", "V0160", "V0325"]
SYNTHETIC_MNA = ["V0013", "V0031", "V0035", "V0036"]   # the M&A rows, so that the savings checks meet that cluster


def synthetic(clean: list[dict]) -> list[dict]:
    """A classification that satisfies every rule, built only to exercise the checks."""
    member: dict[str, list[dict]] = {}
    for g in groups():
        for i in g["ids"]:
            member.setdefault(i, []).append(g)
    rows = []
    for c in clean:
        gs = member.get(c["vendor_id"], [])
        rationale = ("Synthetic rationale, part of the "
                     + " and of the ".join(f"{name_text(g['names'][0])} group" for g in gs) + "."
                     if gs else "Synthetic rationale for the QA self-test.")
        rows.append({"vendor_id": c["vendor_id"], "vendor_name_original": c["vendor_name_raw"],
                     "vendor_name_clean": c["vendor_name_clean"], "spend_12m": c["cost_usd"], "department": "G&A",
                     "sub_function": "Synthetic sub-function", "description": "Synthetic description for the QA self-test",
                     "recommendation": "Optimize", "rationale": rationale, "risk_note": "",
                     "cost_cluster": "Unidentified and individual payees", "is_addressable": "TRUE",
                     "is_recurring": "TRUE", "confidence": "low", "verified": "TRUE",
                     "source_url": "https://example.com/synthetic-evidence"})
    by_id = {r["vendor_id"]: r for r in rows}
    for vids, col, expected, _ in DECISION_EXPECTATIONS:
        for vid in vids:
            by_id[vid][col] = expected
    for vid in ("V0015", "V0093"):
        by_id[vid]["rationale"] = ("Synthetic rationale, part of the Telefónica group: non-discretionary, excluded "
                                   "from the savings base, and rebates would belong against revenue.")
    for vid in ("V0030", "V0086", "V0186"):
        by_id[vid]["rationale"] = "Synthetic rationale: workforce cost, set by the hiring plan, not a vendor action."
    for vid in HARDWARE_IDS:
        by_id[vid]["rationale"] = by_id[vid]["rationale"][:-1] + ", consolidated into group IT procurement."
    for r in rows:
        if r["recommendation"] in NEEDS_RISK_NOTE:
            r["risk_note"] = "Synthetic risk note for the QA self-test"
    for vids, col, phrases, _ in WORDING_EXPECTATIONS:
        for vid in vids:
            text = by_id[vid][col]
            if not all(p in plain(text) for p in phrases):
                added = ", ".join(phrases)
                by_id[vid][col] = text.rstrip(".") + f", with {added}." if col == "rationale" else f"{text} {added}".strip()
    for r in rows:
        if r["is_addressable"] == "FALSE" and "non-discretionary" not in plain(r["rationale"]):
            r["rationale"] = r["rationale"].rstrip(".") + ": non-discretionary, excluded from the savings base."
    for vid in SYNTHETIC_UNVERIFIED:
        by_id[vid]["verified"] = "FALSE"
        by_id[vid]["source_url"] = ""
    for vid in SYNTHETIC_MNA:
        by_id[vid]["cost_cluster"] = MNA_CLUSTER
    return rows


def set_field(vid: str, col: str, value: str):
    def mutate(rows: list[dict], report: str | None):
        for r in rows:
            if r["vendor_id"] == vid:
                r[col] = value
        return rows, report
    return mutate


def drop_row(vid: str):
    def mutate(rows, report):
        return [r for r in rows if r["vendor_id"] != vid], report
    return mutate


def swap_rows(a: int, b: int):
    def mutate(rows, report):
        rows[a], rows[b] = rows[b], rows[a]
        return rows, report
    return mutate


def shuffle_rows(seed: int):
    def mutate(rows, report):
        random.Random(seed).shuffle(rows)
        return rows, report
    return mutate


def rename_column(old: str, new: str):
    def mutate(rows, report):
        return [{(new if k == old else k): v for k, v in r.items()} for r in rows], report
    return mutate


def edit_report(old: str, new: str):
    def mutate(rows, report):
        assert report is not None and report.count(old) == 1, f"self-test edit not applicable: {old!r}"
        return rows, report.replace(old, new)
    return mutate


def then(*steps):
    def mutate(rows, report):
        for step in steps:
            rows, report = step(rows, report)
        return rows, report
    return mutate


MUTATIONS = [
    ("AWS merge rows split between two recommendations", set_field("V0103", "recommendation", "Consolidate"), "C11"),
    ("Bupa link rows disagree", set_field("V0071", "recommendation", "Consolidate"), "C11"),
    ("4i merge split", set_field("V0072", "recommendation", "Terminate"), "C11"),
    ("Pluxee merge split (Sodexo SVC India renamed)", set_field("V0054", "recommendation", "Terminate"), "C11"),
    ("Rationale does not name its group", set_field("V0071", "rationale", "Synthetic rationale for one insurer."), "C12"),
    ("Group named only through the row's own name", set_field("V0047", "rationale", "Bupa keeps the policy."), "C12"),
    ("Per-row link rationale does not name its group",
     set_field("V0026", "rationale", "Synthetic rationale for recruiter seats."), "C12"),
    ("Amazon marketplace row not Terminate", set_field("V0203", "recommendation", "Optimize"), "C13"),
    ("Microsoft 365 not Consolidate", set_field("V0081", "recommendation", "Optimize"), "C13"),
    ("npm outside Engineering", set_field("V0125", "department", "SaaS"), "C13"),
    ("Employee hardware Terminated as retail", set_field("V0378", "recommendation", "Terminate"), "C13"),
    ("Hardware rationale without group IT procurement",
     set_field("V0167", "rationale", "Synthetic rationale for one hardware vendor."), "C14"),
    ("Adviser taken out of the recurring base", set_field("V0018", "is_recurring", "FALSE"), "C13"),
    ("Telefónica rationale without the revenue note",
     set_field("V0015", "rationale", "Synthetic rationale, part of the Telefónica group: non-discretionary, "
                                     "excluded from the savings base."), "C14"),
    ("Non-addressable row without the savings-base wording",
     set_field("V0093", "rationale", "Synthetic rationale, part of the Telefónica group, where rebates would "
                                     "belong against revenue."), "C15"),
    ("Banned phrase in a description", set_field("V0002", "description", "CRM solutions for the sales team"), "C7"),
    ("Em dash in a description", set_field("V0005", "description", f"Flexible offices {EM_DASH} London"), "C9"),
    ("Two-sentence rationale", set_field("V0004", "rationale", "First sentence. Second sentence."), "C8"),
    ("Department outside the taxonomy", set_field("V0006", "department", "IT"), "C3"),
    ("Cluster outside the fixed list", set_field("V0007", "cost_cluster", "Facilities"), "C4"),
    ("Label outside the three recommendations", set_field("V0008", "recommendation", "Renegotiate"), "C5"),
    ("verified neither TRUE nor FALSE", set_field("V0010", "verified", "yes"), "C6"),
    ("is_recurring neither TRUE nor FALSE", set_field("V0011", "is_recurring", ""), "C6"),
    ("A source row missing", drop_row("V0387"), "C2"),
    ("Spend column under the old name cost_usd", rename_column("spend_12m", "cost_usd"), "C1"),
    ("Terminate row without a risk_note", set_field("V0203", "risk_note", ""), "C16"),
    ("Consolidate row without a risk_note", set_field("V0081", "risk_note", " "), "C16"),
    ("Optimize row with a risk note and no recorded exception",
     set_field("V0005", "risk_note", "Synthetic risk note on an Optimize row"), "C16"),
    # Step 3b: the platform reclassification
    ("Salesforce back in Sales as the sales team's CRM", set_field("V0002", "department", "Sales"), "C13"),
    ("Mason Frank back in the Salesforce platform cluster", set_field("V0034", "cost_cluster", "Salesforce platform"),
     "C13"),
    ("NSDL back in the savings base", set_field("V0284", "is_addressable", "TRUE"), "C13"),
    ("Bisley Law risk note without the control finding",
     set_field("V0018", "risk_note", "open legal matters must move first"), "C14"),
    ("Weking description without confirm with Finance",
     set_field("V0009", "description", "Zagreb Salesforce consultancy supplying developers"), "C14"),
    # Step 3c: the SaaS department reading
    ("AWS back in Engineering", set_field("V0014", "department", "Engineering"), "C13"),
    ("Slack back in SaaS as a cross-functional subscription", set_field("V0173", "department", "SaaS"), "C13"),
    ("Microsoft 365 without the Corporate IT sub_function", set_field("V0081", "sub_function", "Productivity suite"),
     "C14"),
    # C17: verification exceptions
    ("Unverified row not listed", set_field("V0010", "verified", "FALSE"), "C17"),
    ("Listed row is TRUE in the file", set_field("V0009", "verified", "TRUE"), "C17"),
    ("Listed id not in the file",
     edit_report("- V0325: the source has no vendor name.",
                 "- V0325: the source has no vendor name.\n- V0999: an id that is not in the file."), "C17"),
    ("Listing without a reason", edit_report("- V0160: individual payee; there is no public record to check against.",
                                             "- V0160"), "C17"),
    ("Unverified row named only outside the heading", set_field("V0004", "verified", "FALSE"), "C17"),
    ("Unverified row listed by name, not by vendor_id",
     then(set_field("V0002", "verified", "FALSE"),
          edit_report("- V0325: the source has no vendor name.",
                      "- V0325: the source has no vendor name.\n- Salesforce UK Ltd: listed by name only.")), "C17"),
    ("Heading worded differently", edit_report("## Verification exceptions", "## Verification Exceptions"), "C17"),
    ("Two ids on one line",
     edit_report("- V0009: Croatian company whose function no public source confirms.",
                 "- V0009 and V0160: Croatian company whose function no public source confirms."), "C17"),
    ("Validation report missing while rows are FALSE", lambda rows, report: (rows, None), "C17"),
    # C18: names matched by vendor_id; rows in the original sheet order. An optional fourth element is text
    # the expected check's detail must contain: here it proves the names still match by vendor_id.
    ("vendor_name_original repaired instead of verbatim",
     set_field("V0030", "vendor_name_original", "Sveučilište U Zagrebu, Studentski Centar"), "C18"),
    ("vendor_name_clean edited", set_field("V0004", "vendor_name_clean", "BDO"), "C18"),
    ("Two rows swapped", swap_rows(0, 1), "C18", "name mismatches: none"),
    ("Shuffled file, every name still right for its vendor_id", shuffle_rows(2026), "C18", "name mismatches: none"),
]


def retag(lever: str, tag: str):
    """Edit docs/savings_assumptions.md text: give the lever's row this depends_on cell."""
    def mutate(text: str) -> str:
        lines = text.splitlines()
        col = None
        for i, line in enumerate(lines):
            if line.startswith("| Lever |"):
                col = [c.strip() for c in line.strip().strip("|").split("|")].index("depends_on")
            elif col is not None and line.startswith(f"| {lever} |"):
                cells = line.strip().strip("|").split("|")
                cells[col] = f" {tag} "
                lines[i] = "|" + "|".join(cells) + "|"
                return "\n".join(lines) + "\n"
        raise AssertionError(f"self-test lever not found: {lever}")
    return mutate


# Planted errors in the real docs/savings_assumptions.md text, each to be caught by S6.
DOC_MUTATIONS = [
    ("Assumption without a depends_on tag", retag("Law firms and legal resourcing", "")),
    ("Tag that is not a registered decision", retag("Commercial insurance through brokers", "`group_finance`")),
    ("none together with a decision name", retag("Unidentified and individual payees", "`none`, `group_systems`")),
    ("Lever named as a vendor action tagged with a decision", retag("Navan", "`remote_operating_model`")),
]


# ---------------------------------------------------------------- savings checks (step 4)

def savings_checks(res: Results, srows: list[dict], rows: list[dict], register_text: str,
                   savings_text: str | None) -> None:
    """V1 to V8 on outputs/analysis/savings.csv, read against the classification, the register and savings.md."""
    decisions, levers, register_problems = load_register(register_text)
    cols = set(srows[0].keys()) if srows else set()
    missing_cols = [c for c in SAVINGS_COLUMNS if c not in cols]
    if missing_cols or not srows:
        for cid in ("V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8"):
            res.add(cid, "Savings check", False, f"savings file unusable; missing columns: {', '.join(missing_cols) or 'none'}"
                    + ("; no rows" if not srows else ""))
        return
    by_id = {r["vendor_id"]: r for r in rows}
    tol = 1e-6

    bad = [f"{s['vendor_id']}: {s['pct_low']} / {s['pct_base']} / {s['pct_high']}" for s in srows
           if not (0 <= to_float(s["pct_low"]) <= to_float(s["pct_base"]) <= to_float(s["pct_high"]) <= 100)]
    res.add("V1", "pct_low <= pct_base <= pct_high on every row, all within 0 and 100", not bad,
            f"bad: {sample(bad) or 'none'}")

    bad = [f"{s['vendor_id']}: without {s['pct_without_decision']} against base {s['pct_base']}" for s in srows
           if not (0 <= to_float(s["pct_without_decision"]) <= to_float(s["pct_base"]))
           or (s["depends_on"].strip() == "none" and to_float(s["pct_without_decision"]) != to_float(s["pct_base"]))]
    res.add("V2", "pct_without_decision <= pct_base on every row, and equal to it on untagged rows", not bad,
            f"bad: {sample(bad) or 'none'}")

    bad = [f"{s['vendor_id']}: year 1 {s['saving_year1']} against base {s['saving_base']} at factor {s['year1_factor']}"
           for s in srows
           if not (0 <= to_float(s["year1_factor"]) <= 1) or to_float(s["saving_year1"]) > to_float(s["saving_base"]) + tol
           or abs(to_float(s["saving_year1"]) - to_float(s["saving_base"]) * to_float(s["year1_factor"])) > tol]
    res.add("V3", "The year-1 saving is the base saving times a factor between 0 and 1, so never above the base", not bad,
            f"bad: {sample(bad) or 'none'}")

    bad = []
    for s in srows:
        c = by_id.get(s["vendor_id"])
        if c and (c["is_addressable"] == "FALSE" or c["cost_cluster"] == MNA_CLUSTER) \
                and any(to_float(s[col]) != 0 for col in SAVING_COLUMNS):
            bad.append(f"{s['vendor_id']} ({'not addressable' if c['is_addressable'] == 'FALSE' else 'M&A'}): "
                       f"base {s['saving_base']}")
    res.add("V4", "No saving on a row that is not addressable or in the M&A cluster", not bad, f"bad: {sample(bad) or 'none'}")

    bad = [f"{s['vendor_id']}: spend {s['spend_12m']}, high {s['saving_high']}" for s in srows
           if to_float(s["spend_12m"]) < 0 or math.isnan(to_float(s["spend_12m"]))
           or any(to_float(s[col]) > to_float(s["spend_12m"]) + tol for col in SAVING_COLUMNS)]
    res.add("V5", "No saving above the row's spend, and spend is a non-negative number", not bad,
            f"bad: {sample(bad) or 'none'}")

    unregistered = [f"{s['vendor_id']}: {s['lever']}" for s in srows if s["lever"] not in levers]
    inconsistent = []
    for s in srows:
        f = levers.get(s["lever"])
        if f is None:
            continue
        spend = to_float(s["spend_12m"])
        wrong = [c for c in ("pct_low", "pct_base", "pct_high", "pct_without_decision", "year1_factor")
                 if abs(to_float(s[c]) - f[c]) > tol]
        wrong += [c for c, p in zip(SAVING_COLUMNS[:4], ("pct_low", "pct_base", "pct_high", "pct_without_decision"))
                  if abs(to_float(s[c]) - spend * f[p] / 100) > tol]
        if s["opportunity"] != f["opportunity"]:
            wrong.append("opportunity")
        if s["depends_on"] != ", ".join(f["depends_on"]):
            wrong.append("depends_on")
        if wrong:
            inconsistent.append(f"{s['vendor_id']}: {', '.join(wrong)} differ from the register")
    unused = sorted(set(levers) - {s["lever"] for s in srows})
    seen: dict[str, int] = defaultdict(int)
    for s in srows:
        seen[s["vendor_id"]] += 1
    dupes = sorted(v for v, n in seen.items() if n > 1)
    missing = [v for v in by_id if v not in seen]
    extra = [v for v in seen if v not in by_id]
    mismatched = [f"{s['vendor_id']}: {', '.join(c for c in ('spend_12m', 'cost_cluster', 'vendor_name_clean') if s[c] != by_id[s['vendor_id']][c])}"
                  for s in srows if s["vendor_id"] in by_id
                  and any(s[c] != by_id[s["vendor_id"]][c] for c in ("spend_12m", "cost_cluster", "vendor_name_clean"))]
    other_register = [p for p in register_problems if "decision" not in p]
    ok6 = not (unregistered or inconsistent or unused or dupes or missing or extra or mismatched or other_register)
    res.add("V6", "Every row has one registered lever with the register's values, every lever is used, and the rows "
                  "are the classification's rows with their spend, cluster and name", ok6,
            f"{len(levers)} levers, {len(srows)} rows; unregistered: {sample(unregistered) or 'none'}; differing from the "
            f"register: {sample(inconsistent) or 'none'}; unused levers: {sample(unused) or 'none'}; duplicated: "
            f"{sample(dupes) or 'none'}; missing: {sample(missing) or 'none'}; extra: {sample(extra) or 'none'}; "
            f"spend, cluster or name mismatches: {sample(mismatched) or 'none'}; register problems: "
            f"{sample(other_register) or 'none'}")

    bad = []
    for s in srows:
        tags = [t.strip().strip("`") for t in s["depends_on"].split(",") if t.strip()]
        if not tags or ("none" in tags and len(tags) > 1) or any(t != "none" and t not in decisions for t in tags):
            bad.append(f"{s['vendor_id']}: {s['depends_on']!r}")
    bad += [f"register: {p}" for p in register_problems if "decision" in p]
    res.add("V7", "Every depends_on tag, on the rows and in the register, is none or a registered decision", not bad,
            f"{len(decisions)} decisions; bad: {sample(bad) or 'none'}")

    bad = []
    if savings_text is None:
        bad.append(f"{rel(SAVINGS_MD)} not found")
    else:
        tot = savings_totals(srows)
        for key, heading in ROLLUP_HEADINGS.items():
            try:
                rows_md = section_rows(savings_text, heading)
            except SystemExit:
                bad.append(f"no section {heading!r}")
                continue
            if not rows_md:
                bad.append(f"{heading}: no table")
                continue
            header = rows_md[0]
            if any(c not in header for c in MONEY_COLUMNS):
                bad.append(f"{heading}: columns missing")
                continue
            idx = {c: header.index(c) for c in MONEY_COLUMNS}
            expected = rollup(srows, key)
            listed = {}
            for r in rows_md[1:]:
                if len(r) != len(header):
                    bad.append(f"{heading}: a row with {len(r)} cells")
                    continue
                listed[r[0]] = {c: r[i] for c, i in idx.items()}
            for name, sums in expected.items():
                if name not in listed:
                    bad.append(f"{heading}: {name} missing")
                    continue
                wrong = [c for c, col in MONEY_COLUMNS.items() if listed[name][c] != money(sums[col])]
                if wrong:
                    bad.append(f"{heading}: {name} differs on {', '.join(wrong)}")
            for name in listed:
                if name not in expected and name != "Total":
                    bad.append(f"{heading}: {name} is not a group in the file")
            if "Total" not in listed:
                bad.append(f"{heading}: no Total row")
            elif any(listed["Total"][c] != money(tot[col]) for c, col in MONEY_COLUMNS.items()):
                bad.append(f"{heading}: the Total row differs from the vendor rows")
    res.add("V8", f"The roll-ups by opportunity, cluster and lever in {rel(SAVINGS_MD)} equal the sums of the vendor rows, "
                  "and their totals equal the file's total", not bad, f"bad: {sample(bad) or 'none'}")


def synthetic_savings(rows: list[dict], levers: dict[str, dict]) -> list[dict]:
    """Savings rows for the synthetic classification that satisfy every savings check: rows outside the savings
    base and in the M&A cluster take 0% levers, every other row cycles through the whole register."""
    names = list(levers)
    zero = [n for n in names if levers[n]["pct_high"] == 0]
    out = []
    for k, r in enumerate(rows):
        if r["is_addressable"] == "FALSE" or r["cost_cluster"] == MNA_CLUSTER:
            name = zero[k % len(zero)]
        else:
            name = names[k % len(names)]
        out.append(format_row(saving_row(r, name, levers[name])))
    return out


def set_saving(vid: str, col: str, value):
    def mutate(srows, rows, text):
        for s in srows:
            if s["vendor_id"] == vid:
                s[col] = str(value(s) if callable(value) else value)
        return srows, rows, text
    return mutate


def reassign(vid: str, lever_name: str, levers: dict[str, dict], cluster: str | None = None):
    """Give the row this lever with values consistent with the register (and this cluster, in both files)."""
    def mutate(srows, rows, text):
        for r in rows:
            if r["vendor_id"] == vid and cluster:
                r["cost_cluster"] = cluster
        for i, s in enumerate(srows):
            if s["vendor_id"] == vid:
                r = next(r for r in rows if r["vendor_id"] == vid)
                srows[i] = format_row(saving_row(r, lever_name, levers[lever_name]))
        return srows, rows, text
    return mutate


def move_lever(old: str, new: str, levers: dict[str, dict]):
    def mutate(srows, rows, text):
        by_id = {r["vendor_id"]: r for r in rows}
        for i, s in enumerate(srows):
            if s["lever"] == old:
                srows[i] = format_row(saving_row(by_id[s["vendor_id"]], new, levers[new]))
        return srows, rows, text
    return mutate


def drop_saving_row(vid: str):
    def mutate(srows, rows, text):
        return [s for s in srows if s["vendor_id"] != vid], rows, text
    return mutate


def edit_rollup(line_start: str, heading: str, change):
    """Edit the first table line under `heading` in savings.md that starts with `line_start`."""
    def mutate(srows, rows, text):
        assert text is not None
        head, sep, tail = text.partition(f"## {heading}\n")
        assert sep, f"self-test section not found: {heading}"
        lines = tail.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("## "):
                break
            if line.startswith(line_start):
                lines[i] = change(line)
                return srows, rows, head + sep + "\n".join(lines)
        raise AssertionError(f"self-test row not found: {line_start}")
    return mutate


def first_row_base_above_zero(srows: list[dict]) -> dict:
    return next(s for s in srows if to_float(s["saving_base"]) > 0)


# (title, change, the check that must fail, whether savings.md is rendered again after the change)
def savings_mutations(levers: dict[str, dict]) -> list[tuple]:
    names = list(levers)
    nonzero = next(n for n in names if levers[n]["pct_base"] > 0)
    return [
        ("pct_low above pct_base", set_saving("V0005", "pct_low", "99"), "V1", True),
        ("pct_without_decision above pct_base", set_saving("V0005", "pct_without_decision", "99"), "V2", True),
        ("Year-1 saving above the base saving",
         set_saving(None, "saving_year1", None), "V3", True),   # filled in below
        ("A saving on a row outside the savings base", set_saving("V0015", "saving_base", "1"), "V4", True),
        ("A saving on an M&A row", reassign("V0013", nonzero, levers), "V4", True),
        ("A saving above the row's spend", set_saving("V0005", "saving_high", lambda s: to_float(s["spend_12m"]) * 2),
         "V5", True),
        ("A lever that is not in the register", set_saving("V0005", "lever", "Synthetic lever"), "V6", True),
        ("A registered lever left unused", move_lever(names[0], names[1], levers), "V6", True),
        ("A vendor row missing from the savings file", drop_saving_row("V0387"), "V6", True),
        ("spend_12m that differs from the classification", set_saving("V0005", "spend_12m", "1"), "V6", True),
        ("A depends_on tag that is not a registered decision", set_saving("V0005", "depends_on", "group_finance"), "V7",
         True),
        ("A roll-up figure edited in the lever table",
         edit_rollup(f"| {names[0]} |", ROLLUP_HEADINGS["lever"], lambda line: line.replace("$", "$9", 1)), "V8", False),
        ("An opportunity row removed from its roll-up",
         edit_rollup("| Office exit |", ROLLUP_HEADINGS["opportunity"], lambda line: ""), "V8", False),
    ]


def self_test(clean: list[dict]) -> bool:
    base_rows = synthetic(clean)
    base_report = SYNTHETIC_VALIDATION_REPORT
    res = Results()
    classification_checks(res, copy.deepcopy(base_rows), clean, base_report)
    listed, problems = verification_exceptions(base_report)
    clean_ok = not res.failed() and not any(status == "PENDING" for _, status, _, _ in res.items)
    print(f"{'PASS' if clean_ok else 'FAIL'}    synthetic classification that follows every rule passes all "
          f"{len(res.items)} checks; the synthetic report lists {', '.join(sorted(listed))} as verification exceptions"
          + ("" if clean_ok else f" (failed: {', '.join(res.failed())})"))
    if not clean_ok:
        res.show()
    all_ok = clean_ok and sorted(listed) == SYNTHETIC_UNVERIFIED and not problems
    for title, mutate, expected, *must in MUTATIONS:
        rows, report = mutate(copy.deepcopy(base_rows), base_report)
        res = Results()
        classification_checks(res, rows, clean, report)
        detail = next((d for cid, _, _, d in res.items if cid == expected), "")
        caught = expected in res.failed() and all(m in detail for m in must)
        all_ok &= caught
        print(f"{'PASS' if caught else 'FAIL'}    planted error caught by {expected}: {title}"
              f" (checks failing: {', '.join(res.failed()) or 'none'}"
              + "".join(f"; {expected} reports {m!r}" for m in must) + ")")
    doc = SAVINGS_ASSUMPTIONS.read_text(encoding="utf-8")
    n_rows, n_names, problems = tag_problems(doc)
    doc_ok = not problems and n_rows > 0
    all_ok &= doc_ok
    print(f"{'PASS' if doc_ok else 'FAIL'}    {rel(SAVINGS_ASSUMPTIONS)} as it stands passes S6: {n_rows} assumptions, "
          f"{n_names} decisions" + (f" (problems: {'; '.join(problems)})" if problems else ""))
    for title, mutate in DOC_MUTATIONS:
        _, _, problems = tag_problems(mutate(doc))
        all_ok &= bool(problems)
        print(f"{'PASS' if problems else 'FAIL'}    planted error caught by S6: {title} ({'; '.join(problems) or 'none'})")

    # The savings checks, on savings rows built from the synthetic classification and the real register.
    decisions, levers, register_problems = load_register(doc)
    base_savings = synthetic_savings(base_rows, levers)
    base_text = render_rollup_sections(base_savings, levers)
    res = Results()
    savings_checks(res, copy.deepcopy(base_savings), copy.deepcopy(base_rows), doc, base_text)
    clean_ok = not res.failed() and not register_problems
    all_ok &= clean_ok
    print(f"{'PASS' if clean_ok else 'FAIL'}    synthetic savings rows that follow the register pass all {len(res.items)} "
          f"savings checks ({len(levers)} levers, {len(decisions)} decisions)"
          + ("" if clean_ok else f" (failed: {', '.join(res.failed())}; register: {'; '.join(register_problems)})"))
    if not clean_ok:
        res.show()
    mutations = savings_mutations(levers)
    year1_row = first_row_base_above_zero(base_savings)
    mutations[2] = ("Year-1 saving above the base saving",
                    set_saving(year1_row["vendor_id"], "saving_year1", lambda s: to_float(s["saving_base"]) * 2), "V3",
                    True)
    for title, mutate, expected, rerender in mutations:
        srows, rows, text = mutate(copy.deepcopy(base_savings), copy.deepcopy(base_rows), base_text)
        if rerender:
            text = render_rollup_sections(srows, levers)
        res = Results()
        savings_checks(res, srows, rows, doc, text)
        caught = expected in res.failed()
        all_ok &= caught
        print(f"{'PASS' if caught else 'FAIL'}    planted error caught by {expected}: {title}"
              f" (checks failing: {', '.join(res.failed()) or 'none'})")
    print(f"self-test {'passed' if all_ok else 'FAILED'}: clean run plus "
          f"{len(MUTATIONS) + len(DOC_MUTATIONS) + len(mutations)} planted errors")
    return all_ok


# ---------------------------------------------------------------- main

def run(classified: Path = CLASSIFIED, report: Path = VALIDATION_REPORT, savings: Path = SAVINGS_CSV,
        savings_report: Path = SAVINGS_MD) -> Results:
    """The structural checks, then the classification checks once `classified` exists, then the savings checks once
    `savings` exists. main() calls it on the real files; scripts/merge_validate.py calls it on the files it has just
    written, and scripts/03_savings.py runs the savings checks on its own output."""
    clean = read_csv(CLEAN)
    res = Results()
    structural_checks(res, clean)
    if classified.exists():
        validation_text = report.read_text(encoding="utf-8") if report.exists() else None
        rows = read_csv(classified)
        classification_checks(res, rows, clean, validation_text)
        if savings.exists():
            savings_text = savings_report.read_text(encoding="utf-8") if savings_report.exists() else None
            savings_checks(res, read_csv(savings), rows, SAVINGS_ASSUMPTIONS.read_text(encoding="utf-8"), savings_text)
        else:
            res.add("V*", "Savings checks V1 to V8", None, f"{rel(savings)} not produced yet")
    else:
        res.add("C*", "Classification checks C1 to C18", None, f"{rel(classified)} not produced yet")
    return res


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return 0 if self_test(read_csv(CLEAN)) else 1
    res = run()
    res.show()
    failed = res.failed()
    print(f"{len(failed)} failed" + (f": {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
