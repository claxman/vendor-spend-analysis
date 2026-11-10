#!/usr/bin/env python3
"""QA checks for the classification deliverable, outputs/vendors_classified.csv.

Where each rule comes from:
  CLAUDE.md                     one-line descriptions without the banned phrases, departments from the
                                taxonomy, three recommendations with a one-sentence rationale, no em dashes
  docs/taxonomy.md, clusters.md the allowed departments and cost clusters
  docs/decisions.md             per-row deliverable (step 2c), group recommendation rule (step 2d), the
                                outcomes fixed for named rows (steps 2b to 2d), the columns of the
                                classification spec and the risk-note check (step 2d-fix), the verification
                                exceptions and the name check (step 2d-fix2)
  scripts/vsa_common.py         the merge and link groups, their recommendation scope and the names a
                                rationale may use for each group

Structural checks run now. The classification checks run once outputs/vendors_classified.csv exists;
until then they are reported as pending. C17 reads only the "Verification exceptions" heading of
qa/validation_report.md, which the verification step writes; this script never writes it.

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
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vsa_common import (  # noqa: E402
    EM_DASH, EN_DASH, LINK_GROUPS, MERGE_GROUPS, names_group, rel, section_rows, strip_accents,
)

CLASSIFIED = ROOT / "outputs" / "vendors_classified.csv"
CLEAN = ROOT / "outputs" / "vendors_clean.csv"
GROUPS = ROOT / "qa" / "vendor_groups.csv"
TAXONOMY = ROOT / "docs" / "taxonomy.md"
CLUSTERS = ROOT / "docs" / "clusters.md"
VALIDATION_REPORT = ROOT / "qa" / "validation_report.md"
EXCEPTIONS_HEADING = "Verification exceptions"

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
PER_ROW_LINKS = {"Amazon", "Microsoft", "Sodexo and Pluxee"}  # docs/decisions.md, step 2d
VENDOR_ID = re.compile(r"\bV\d{4}\b")

# Outcomes fixed by recorded decisions: (vendor_ids, column, expected value, source).
DECISION_EXPECTATIONS = [
    (["V0014", "V0103"], "recommendation", "Optimize", "step 2d: AWS is Optimize"),
    (["V0203", "V0291"], "recommendation", "Terminate", "step 2d: Amazon marketplaces, consumer retail through AP"),
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
    (["V0034"], "cost_cluster", "Salesforce platform", "step 2b: Mason Frank"),
    (["V0173"], "department", "SaaS", "step 2b: Slack"),
    (["V0173"], "cost_cluster", "Salesforce platform", "step 2b: Slack"),
]
# Phrases a rationale must contain: (vendor_ids, phrases, source).
RATIONALE_EXPECTATIONS = [
    (["V0015", "V0093"], ["rebate", "revenue"], "step 2b: Telefónica rebates would belong against revenue"),
    (["V0030", "V0086", "V0186"], ["hiring plan"], "step 2b: student labour rationale"),
]
# Each fixed row's clean name must contain this, so a mistyped id cannot test the wrong vendor.
EXPECTED_NAMES = {"V0014": "Amazon Web Services", "V0103": "Amazon Web Services", "V0203": "Amazon",
                  "V0291": "Amazon", "V0081": "Microsoft", "V0026": "LinkedIn", "V0125": "npm",
                  "V0015": "Telefonica", "V0093": "Telefonica", "V0030": "Studentski Centar",
                  "V0086": "Studentski Centar", "V0186": "Studentski Centar", "V0034": "Mason Frank",
                  "V0173": "Slack"}


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
    return "; ".join(str(x) for x in items[:k]) + (f" (and {len(items) - k} more)" if len(items) > k else "")


# ---------------------------------------------------------------- structural checks (run now)

def structural_checks(res: Results, clean: list[dict]) -> None:
    ids = {r["vendor_id"] for r in clean}
    clean_names = {r["vendor_id"]: r["vendor_name_clean"] for r in clean}
    gs = groups()

    scopes_ok = all(g["status"] in ("shared", "per row") for g in gs if g["kind"] == "link")
    per_row = {g["name"] for g in gs if g["kind"] == "link" and not g["shared"]}
    res.add("S1", "Link groups are marked shared or per row; per row exactly for Amazon, Microsoft, Sodexo and Pluxee",
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
    for vids, phrases, source in RATIONALE_EXPECTATIONS:
        for vid in vids:
            if vid in by_id and not all(p in plain(by_id[vid]["rationale"]) for p in phrases):
                bad.append(f"{vid} lacks {' and '.join(phrases)} ({source})")
    res.add("C14", "Rationale wording fixed by recorded decisions", not bad, f"bad: {sample(bad, 2) or 'none'}")

    bad = [r["vendor_id"] for r in rows if r["is_addressable"] == "FALSE"
           and not ("non-discretionary" in plain(r["rationale"]) and "savings base" in plain(r["rationale"]))]
    res.add("C15", "Rows outside the savings base say \"non-discretionary, excluded from the savings base\"", not bad,
            f"bad: {sample(bad) or 'none'}")

    bad = [r["vendor_id"] for r in rows if r["recommendation"] in NEEDS_RISK_NOTE and not r["risk_note"].strip()]
    res.add("C16", "Every Terminate and Consolidate row has a risk_note", not bad, f"missing: {sample(bad) or 'none'}")

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

    mismatched = []
    for line, (r, c) in enumerate(zip(rows, clean), start=1):
        if (r["vendor_id"], r["vendor_name_original"], r["vendor_name_clean"]) != (
                c["vendor_id"], c["vendor_name_raw"], c["vendor_name_clean"]):
            mismatched.append(f"row {line}: {r['vendor_id']}")
    if len(rows) != len(clean):
        mismatched.append(f"{len(rows)} rows against {len(clean)}")
    res.add("C18", f"vendor_name_original and vendor_name_clean match {rel(CLEAN)} row for row", not mismatched,
            f"mismatches: {sample(mismatched) or 'none'}")


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
    for r in rows:
        if r["recommendation"] in NEEDS_RISK_NOTE:
            r["risk_note"] = "Synthetic risk note for the QA self-test"
    for vid in SYNTHETIC_UNVERIFIED:
        by_id[vid]["verified"] = "FALSE"
        by_id[vid]["source_url"] = ""
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
    ("Proposed 4i merge split", set_field("V0072", "recommendation", "Terminate"), "C11"),
    ("Rationale does not name its group", set_field("V0071", "rationale", "Synthetic rationale for one insurer."), "C12"),
    ("Group named only through the row's own name", set_field("V0047", "rationale", "Bupa keeps the policy."), "C12"),
    ("Per-row link rationale does not name its group",
     set_field("V0026", "rationale", "Synthetic rationale for recruiter seats."), "C12"),
    ("Amazon marketplace row not Terminate", set_field("V0203", "recommendation", "Optimize"), "C13"),
    ("Microsoft 365 not Consolidate", set_field("V0081", "recommendation", "Optimize"), "C13"),
    ("npm outside Engineering", set_field("V0125", "department", "SaaS"), "C13"),
    ("Telefónica rationale without the revenue note",
     set_field("V0015", "rationale", "Synthetic rationale, part of the Telefónica group: non-discretionary, "
                                     "excluded from the savings base."), "C14"),
    ("Non-addressable row without the savings-base wording",
     set_field("V0093", "rationale", "Synthetic rationale, part of the Telefónica group, where rebates would "
                                     "belong against revenue."), "C15"),
    ("Banned phrase in a description", set_field("V0002", "description", "CRM solutions for the sales team"), "C7"),
    ("Em dash in a description", set_field("V0005", "description", "Flexible offices — London"), "C9"),
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
    # C18: names row for row
    ("vendor_name_original repaired instead of verbatim",
     set_field("V0030", "vendor_name_original", "Sveučilište U Zagrebu, Studentski Centar"), "C18"),
    ("vendor_name_clean edited", set_field("V0004", "vendor_name_clean", "BDO"), "C18"),
    ("Rows out of the source order", swap_rows(0, 1), "C18"),
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
    for title, mutate, expected in MUTATIONS:
        rows, report = mutate(copy.deepcopy(base_rows), base_report)
        res = Results()
        classification_checks(res, rows, clean, report)
        caught = expected in res.failed()
        all_ok &= caught
        print(f"{'PASS' if caught else 'FAIL'}    planted error caught by {expected}: {title}"
              f" (checks failing: {', '.join(res.failed()) or 'none'})")
    print(f"self-test {'passed' if all_ok else 'FAILED'}: clean run plus {len(MUTATIONS)} planted errors")
    return all_ok


# ---------------------------------------------------------------- main

def main(argv: list[str]) -> int:
    clean = read_csv(CLEAN)
    if "--self-test" in argv:
        return 0 if self_test(clean) else 1
    res = Results()
    structural_checks(res, clean)
    if CLASSIFIED.exists():
        validation_text = VALIDATION_REPORT.read_text(encoding="utf-8") if VALIDATION_REPORT.exists() else None
        classification_checks(res, read_csv(CLASSIFIED), clean, validation_text)
    else:
        res.add("C*", "Classification checks C1 to C18", None, f"{rel(CLASSIFIED)} not produced yet")
    res.show()
    failed = res.failed()
    print(f"{len(failed)} failed" + (f": {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
