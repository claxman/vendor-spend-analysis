#!/usr/bin/env python3
"""Step 2 cleaning: stable vendor ids, repaired and correctly cased display
names, matching keys and the entity merge map. Also checks the Step 2 docs.

Nothing is classified here. The raw workbook is opened read-only and its
SHA-256 is checked before and after the run.

Inputs:  data/raw/vendor_analysis_assessment.xlsx, docs/*.md, and the merge
         decisions in scripts/vsa_common.py (MERGE_GROUPS, PARENT_LINKS).
Outputs: outputs/vendors_clean.csv            one row per source row; original and clean names, exact cost
         qa/vendor_groups.csv                 the entity merge map, one row per source row
         qa/name_changes.csv                  every change from original to clean name, step by step
         outputs/analysis/02_cleaning_report.md  reconciliation, repair table, merges, doc checks

Usage: python scripts/02_clean.py
"""
from __future__ import annotations

import csv
import io
import math
import re
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vsa_common import (  # noqa: E402
    CONFIG_SHEET, DISTINCT_VERDICTS, MERGE_GROUPS, PARENT_LINKS, RAW_PATH, ROOT, assert_no_dashes,
    load_vendor_records, md_escape, money, normalize_name, open_workbook, pct, rel, repair_mojibake,
    sha256, table, write_text,
)

OUT_CLEAN = ROOT / "outputs" / "vendors_clean.csv"
OUT_GROUPS = ROOT / "qa" / "vendor_groups.csv"
OUT_CHANGES = ROOT / "qa" / "name_changes.csv"
OUT_REPORT = ROOT / "outputs" / "analysis" / "02_cleaning_report.md"
DOCS = ROOT / "docs"
PROMPT_LOG = ROOT / "prompts" / "log.md"

# The fixed list from prompt 6, in order.
EXPECTED_CLUSTERS = [
    "Salesforce platform", "Office footprint", "Office running costs", "Travel and entertainment",
    "Team events, perks and wellness", "Audit, tax, accounting and corporate services", "M&A and transaction costs",
    "Legal", "Insurance and benefits", "Recruiting and HR outsourcing", "Cloud, telecom and IT",
    "Outsourced engineering and contractors", "Software subscriptions (non-Salesforce)",
    "Marketing agencies, media and memberships", "Customer-mandated platform fees", "Statutory and government",
    "Student labour", "Unidentified and individual payees",
]
RECOMMENDATIONS = ["Terminate", "Consolidate", "Optimize"]

# ---------------------------------------------------------------- name cleaning rules
# Each rule: (pattern, replacement, reason). Applied in order; every change is logged.

MANUAL_FIXES = [
    (r"\bRaunalni\b", "Računalni",
     "the letter č was dropped; računalni (computer) is the only Croatian word that fits, and the analyst hint spells it so"),
]
PUNCTUATION = [
    ("’", "'", "typographic apostrophe made plain"),
]
SPACING = [
    (r"(?<=[A-Za-z0-9])\(", " (", "space added before an opening bracket"),
]
TAGS = [
    (r"- Supplier$", "", "Supplier tag removed; the source system appears to hold a second record for this company"),
    (r" \(Supplier\)$", "", "Supplier tag removed; the source system appears to hold a second record for this company"),
    (r"(?<=\bLtd)-Uk$", "", "country tag -Uk removed"),
    (r"(?<=\bLtd)-Greec$", "", "country tag -Greec (Greece, cut short in the source) removed"),
    (r",\.\.$", "", "name cut short in the source; trailing ,.. removed"),
]
CASING = [
    # whole-name or compound forms first, so the token rules below cannot half-apply to them
    (r"^Amazon\.Co\.Uk$", "Amazon.co.uk", "brand casing"),
    (r"\bGodaddy\.Com\b", "GoDaddy.com", "brand casing"),
    (r"^Ico$", "ICO", "acronym"),
    (r"\bJ\.D\.O\.O\.", "j.d.o.o.", "Croatian legal form written in lower case"),
    (r"\bD\.O\.O\.", "d.o.o.", "Croatian legal form written in lower case"),
    (r"\bD\.D\.", "d.d.", "Croatian legal form written in lower case"),
    (r"\bS\.R\.O\.", "s.r.o.", "Czech and Slovak legal form written in lower case"),
    (r"\bLlp\b", "LLP", "legal form"), (r"\bLlc\b", "LLC", "legal form"), (r"\bLp\b", "LP", "legal form"),
    (r"\bPlc\b", "PLC", "legal form"), (r"\bGmbh\b", "GmbH", "legal form"), (r"\bBvba\b", "BVBA", "legal form"),
    (r"\bAps\b", "ApS", "legal form"), (r"\bAg\b", "AG", "legal form or acronym"),
    # the acronyms named in prompt 6 that appear as tokens (AWS, JLL and PwC do not; see CANONICAL_OVERRIDES)
    (r"\bBdo\b", "BDO", "acronym"), (r"\bDhl\b", "DHL", "acronym"), (r"\bHp\b", "HP", "acronym"),
    (r"\bSs&C\b", "SS&C", "acronym"), (r"\bTog\b", "TOG", "acronym"), (r"\bGpt\b", "GPT", "acronym"),
    (r"\bCbre\b", "CBRE", "acronym"), (r"\bNcc\b", "NCC", "acronym"), (r"\bHep\b", "HEP", "acronym"),
    (r"\bPricewaterhousecoopers\b", "PricewaterhouseCoopers", "brand casing"),
    (r"\bLasalle\b", "LaSalle", "brand casing"),
    # other acronyms present in the names
    (r"\bUk\b", "UK", "acronym"), (r"\bUsa\b", "USA", "acronym"), (r"\bNsw\b", "NSW", "acronym"),
    (r"\bSg\b", "SG", "acronym"), (r"\bWa\b", "WA", "acronym"), (r"\bAmer\b", "AMER", "acronym"),
    (r"\bCbd\b", "CBD", "acronym"), (r"\bRsm\b", "RSM", "acronym"), (r"\bAto\b", "ATO", "acronym"),
    (r"\bNsdl\b", "NSDL", "acronym"), (r"\bNsn\b", "NSN", "acronym"), (r"\bCsc\b", "CSC", "acronym"),
    (r"\bKlg\b", "KLG", "acronym"), (r"\bGrt\b", "GRT", "acronym"), (r"\bIcici\b", "ICICI", "acronym"),
    (r"\bGic\b", "GIC", "acronym"), (r"\bSvc\b", "SVC", "acronym"), (r"\bPmi\b", "PMI", "acronym"),
    (r"\bPr\b", "PR", "acronym"), (r"\bHr\b", "HR", "acronym"), (r"\bIt\b(?= Recruitment)", "IT", "acronym"),
    (r"\bIp\b", "IP", "acronym"), (r"\bCa$", "CA", "acronym"), (r"\bBb\b", "BB", "acronym"),
    (r"\bDsv\b", "DSV", "acronym"), (r"\bEtm\b", "ETM", "acronym"), (r"\bTm\b", "TM", "acronym"),
    (r"\bTeb\b", "TEB", "acronym"), (r"\bIkea\b", "IKEA", "acronym"), (r"\bPc\b", "PC", "acronym"),
    (r"\bDjs\b", "DJs", "acronym"), (r"\bTp\b", "TP", "acronym"),
    # brands whose own casing is not Title Case
    (r"\bHubspot\b", "HubSpot", "brand casing"), (r"\bLinkedin\b", "LinkedIn", "brand casing"),
    (r"\bDocusign\b", "DocuSign", "brand casing"), (r"\bFastspring\b", "FastSpring", "brand casing"),
    (r"\bJetbrains\b", "JetBrains", "brand casing"), (r"\bLastpass\b", "LastPass", "brand casing"),
    (r"\bSolarwinds\b", "SolarWinds", "brand casing"), (r"\bMightyhive\b", "MightyHive", "brand casing"),
    (r"\bTripactions\b", "TripActions", "brand casing"), (r"\bGoto\b", "GoTo", "brand casing"),
    (r"\bGitkraken\b", "GitKraken", "brand casing"), (r"\bDnsimple\b", "DNSimple", "brand casing"),
    (r"\bStarhub\b", "StarHub", "brand casing"), (r"\bWework\b", "WeWork", "brand casing"),
    (r"\bFormswift\b", "FormSwift", "brand casing"), (r"\bNpm\b", "npm", "brand casing"),
    (r"\b6Sense\b", "6sense", "brand casing"), (r"\b4I\b", "4i", "brand casing"),
    (r"\bIcare\b", "icare", "brand casing"), (r"\bFedex\b", "FedEx", "brand casing"),
    (r"\bGranttree\b", "GrantTree", "brand casing"), (r"\bMpillay\b", "MPillay", "brand casing"),
    (r"(?<=\w)'S\b", "'s", "possessive"),
    (r"\bMc([a-z])", lambda m: "Mc" + m.group(1).upper(), "Mc prefix"),
]
# Canonical names for two single-entity vendors best known by an acronym that
# does not appear in their legal name (prompt 6 lists JLL and PwC). AWS is a
# merged group and gets its canonical name from MERGE_GROUPS.
CANONICAL_OVERRIDES = {
    "PricewaterhouseCoopers LLP": "PwC",
    "Jones Lang LaSalle (NSW) Pty Ltd": "JLL",
}
# Notes about a name that is kept as in the source.
NAME_NOTES = {
    143: "spelled Cici in the source; the analyst hint identifies it as ICICI Prudential",
    153: "Charted (sic) kept as in the source",
    318: "Nezavisnici as in the source; the analyst hint spells it Nezavisni",
    325: "placeholder: the source has no vendor name",
    370: "card-statement descriptor, suggesting a card transaction",
}


def clean_name(raw: str, vid: str) -> tuple[str, list[dict], list[str]]:
    changes, notes = [], []
    name = raw

    def log(step: str, before: str, after: str, reason: str) -> None:
        changes.append({"vendor_id": vid, "step": step, "before": before, "after": after, "reason": reason})

    fixed, changed = repair_mojibake(name)
    if changed:
        log("mojibake", name, fixed, "UTF-8 text had been read as Windows-1252 and then Title Cased; restored")
        notes.append("mojibake repaired")
        name = fixed
    for step, rules in (("manual fix", MANUAL_FIXES), ("punctuation", PUNCTUATION), ("spacing", SPACING),
                        ("tag", TAGS), ("casing", CASING)):
        for pattern, repl, reason in rules:
            new = name.replace(pattern, repl) if step == "punctuation" else re.sub(pattern, repl, name)
            if new != name:
                log(step, name, new, reason)
                if step in ("manual fix", "tag"):
                    notes.append(reason)
                name = new
    squeezed = " ".join(name.split())
    if squeezed != name:
        log("spacing", name, squeezed, "extra spaces removed")
        name = squeezed
    return name, changes, notes


# ---------------------------------------------------------------- doc checks

def section_rows(text: str, heading: str) -> list[list[str]]:
    """Cells of the markdown table under a '## heading' (up to the next '## ')."""
    m = re.search(rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit(f"heading '## {heading}' not found")
    rows = []
    for line in m.group(1).splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line) and not re.match(r"^\|\s*#\s*\|", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows


def check_docs(recs_by_id: dict, config_departments: list[str]) -> tuple[list[tuple[str, str, bool]], list[str]]:
    checks = []
    tax = (DOCS / "taxonomy.md").read_text(encoding="utf-8")
    deps = [r[1] for r in section_rows(tax, "Departments")]
    checks.append(("docs/taxonomy.md departments equal Config A2:A13, same spelling and order",
                   f"{len(deps)} listed: {', '.join(deps)}", deps == config_departments))

    clu = (DOCS / "clusters.md").read_text(encoding="utf-8")
    clusters = [r[1] for r in section_rows(clu, "Clusters")]
    checks.append(("docs/clusters.md holds exactly the 18 clusters of prompt 6, in order",
                   f"{len(clusters)} listed", clusters == EXPECTED_CLUSTERS))

    rules = (DOCS / "recommendation_rules.md").read_text(encoding="utf-8")
    heads = [h for h in RECOMMENDATIONS if re.search(rf"^## {h}$", rules, re.M)]
    checks.append(("docs/recommendation_rules.md has a section for each of Terminate, Consolidate, Optimize",
                   ", ".join(heads), heads == RECOMMENDATIONS))

    hints = (DOCS / "vendor_hints.md").read_text(encoding="utf-8")
    log_text = PROMPT_LOG.read_text(encoding="utf-8")
    table_lines = [ln for ln in hints.split("## Notes")[0].splitlines()
                   if re.match(r"^\| \d+ \|", ln)]
    bad_ids, bad_names, not_verbatim, covered = [], [], [], []
    for ln in table_lines:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        hint_text = cells[1].replace("\\|", "|")
        if hint_text not in log_text:
            not_verbatim.append(cells[0])
        for vid, name in re.findall(r"`(V\d{4})` ([^;]+)", cells[2]):
            name = name.strip()
            covered.append(vid)
            if vid not in recs_by_id:
                bad_ids.append(vid)
            elif recs_by_id[vid]["name_fixed"] != name:
                bad_names.append(f"{vid}: {name} vs {recs_by_id[vid]['name_fixed']}")
    checks.append(("docs/vendor_hints.md: every hint is verbatim from prompt 6",
                   f"{len(table_lines)} hints; {len(not_verbatim)} not verbatim", not not_verbatim))
    checks.append(("docs/vendor_hints.md: every vendor_id exists and its name matches the file",
                   f"{len(covered)} ids ({len(set(covered))} distinct); {len(bad_ids)} unknown ids; {len(bad_names)} "
                   "name mismatches" + (": " + "; ".join(bad_names[:3]) if bad_names else ""),
                   not bad_ids and not bad_names and len(covered) == len(set(covered))))
    for doc in ("taxonomy.md", "recommendation_rules.md", "vendor_hints.md", "clusters.md"):
        text = (DOCS / doc).read_text(encoding="utf-8")
        ok = "—" not in text and "–" not in text
        checks.append((f"docs/{doc} has no em or en dash", "clean" if ok else "dash found", ok))
    return checks, sorted(set(covered))


# ---------------------------------------------------------------- outputs

def to_csv(header: list[str], rows: list[list]) -> str:
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    return buf.getvalue()


def main() -> int:
    before = sha256(RAW_PATH)
    recs = load_vendor_records(RAW_PATH)
    wb = open_workbook(RAW_PATH)
    config_departments = [str(c.value).strip() for c in wb[CONFIG_SHEET]["A"][1:] if c.value is not None]
    by_row = {r["row"]: r for r in recs}
    by_id = {r["vendor_id"]: r for r in recs}

    # names
    all_changes, used_overrides = [], set()
    for r in recs:
        clean, changes, notes = clean_name(r["name"], r["vendor_id"])
        r["clean"] = clean
        r["key"] = normalize_name(clean)
        r["notes"] = notes + ([NAME_NOTES[r["row"]]] if r["row"] in NAME_NOTES else [])
        all_changes += changes

    # merge map
    group_of, parent_of, distinct_of = {}, {}, {}
    for canonical, rows, relationship, confidence, reason in MERGE_GROUPS:
        lead = max(rows, key=lambda x: by_row[x]["cost"])
        for x in rows:
            if x in group_of:
                raise SystemExit(f"row {x} is in two merge groups")
            group_of[x] = (canonical, f"V{lead:04d}", relationship, confidence, reason)
    for parent, rows, reason in PARENT_LINKS:
        for x in rows:
            parent_of[x] = (parent, reason)
    for rows, verdict, reason in DISTINCT_VERDICTS:
        for x in rows:
            distinct_of.setdefault(x, (verdict, reason))
    for r in recs:
        x = r["row"]
        if x in group_of:
            canonical, gid, relationship, confidence, reason = group_of[x]
            r.update(group_id=gid, canonical=canonical, decision="merge", relationship=relationship,
                     confidence=confidence, reason=reason)
        else:
            canonical = CANONICAL_OVERRIDES.get(r["clean"], r["clean"])
            if canonical != r["clean"]:
                used_overrides.add(r["clean"])
            if x in parent_of:
                relationship, reason = "separate vendor, shared parent", parent_of[x][1]
            elif x in distinct_of:
                relationship, reason = distinct_of[x]
            else:
                relationship, reason = "single entity", ""
            r.update(group_id=r["vendor_id"], canonical=canonical, decision="keep", relationship=relationship,
                     confidence="", reason=reason)
        r["parent"] = parent_of.get(x, ("", ""))[0]
    missing_overrides = set(CANONICAL_OVERRIDES) - used_overrides
    if missing_overrides:
        raise SystemExit(f"canonical overrides matched no clean name: {missing_overrides}")

    # write outputs
    clean_csv = to_csv(
        ["vendor_id", "source_row", "vendor_name_raw", "vendor_name_clean", "match_key", "group_id",
         "canonical_vendor", "parent_company", "cost_usd", "name_notes"],
        [[r["vendor_id"], r["row"], r["name"], r["clean"], r["key"], r["group_id"], r["canonical"], r["parent"],
          repr(float(r["cost"])), "; ".join(r["notes"])] for r in recs])
    groups_csv = to_csv(
        ["vendor_id", "source_row", "vendor_name_raw", "vendor_name_clean", "match_key", "group_id",
         "canonical_vendor", "decision", "relationship", "merge_confidence", "parent_company", "reason"],
        [[r["vendor_id"], r["row"], r["name"], r["clean"], r["key"], r["group_id"], r["canonical"], r["decision"],
          r["relationship"], r["confidence"], r["parent"], r["reason"]] for r in recs])
    changes_csv = to_csv(["vendor_id", "step", "before", "after", "reason"],
                         [[c["vendor_id"], c["step"], c["before"], c["after"], c["reason"]] for c in all_changes])
    write_text(OUT_CLEAN, clean_csv)
    write_text(OUT_GROUPS, groups_csv)
    write_text(OUT_CHANGES, changes_csv)

    # reconciliation, from the files just written
    with open(OUT_CLEAN, encoding="utf-8", newline="") as fh:
        back = list(csv.DictReader(fh))
    with open(OUT_GROUPS, encoding="utf-8", newline="") as fh:
        back_groups = list(csv.DictReader(fh))
    raw_total = math.fsum(float(r["cost"]) for r in recs)
    back_total = math.fsum(float(r["cost_usd"]) for r in back)
    after = sha256(RAW_PATH)
    canon_spend = defaultdict(float)
    canon_rows = defaultdict(list)
    for r in recs:
        canon_spend[(r["group_id"], r["canonical"])] += float(r["cost"])
        canon_rows[(r["group_id"], r["canonical"])].append(r["vendor_id"])
    checks, hinted = check_docs(by_id, config_departments)
    recon = [
        ("Rows in the raw sheet equal rows in outputs/vendors_clean.csv and qa/vendor_groups.csv",
         f"{len(recs)} = {len(back)} = {len(back_groups)}", len(recs) == len(back) == len(back_groups)),
        ("vendor_id is unique and equals V plus the source row",
         f"{len({r['vendor_id'] for r in back})} distinct",
         len({r["vendor_id"] for r in back}) == len(back) and all(r["vendor_id"] == f"V{int(r['source_row']):04d}" for r in back)),
        ("Original names kept verbatim in vendor_name_raw",
         "all rows", all(b["vendor_name_raw"] == r["name"] for b, r in zip(back, recs))),
        ("Total cost after cleaning equals the raw total exactly",
         f"${raw_total:,.2f} = ${back_total:,.2f}", raw_total == back_total),
        ("Every cost value round-trips unchanged",
         "all rows", all(float(b["cost_usd"]) == float(r["cost"]) for b, r in zip(back, recs))),
        ("Raw workbook unchanged by the run", f"SHA-256 {after[:16]}...", before == after),
    ]
    all_checks = recon + checks
    failed = [c for c in all_checks if not c[2]]

    # report
    steps = Counter(c["step"] for c in all_changes)
    rows_by_step = {s: len({c["vendor_id"] for c in all_changes if c["step"] == s}) for s in steps}
    changed_rows = len({c["vendor_id"] for c in all_changes})
    merge_rows = sum(len(rows) for _, rows, *_ in MERGE_GROUPS)
    n_vendors = len(canon_spend)
    lines = [
        "# Cleaning report",
        "",
        f"Generated {date.today().isoformat()} by `scripts/02_clean.py`. The raw workbook was opened read-only; SHA-256 "
        f"`{before}` before and after. Nothing is classified here.",
        "",
        "Outputs:",
        "",
        f"- `{rel(OUT_CLEAN)}`: one row per source row with `vendor_id`, the original name (`vendor_name_raw`), the "
        "clean name (`vendor_name_clean`), the matching key, the merge group, the canonical vendor, the parent company, "
        "the exact cost as stored, and notes on the name.",
        f"- `{rel(OUT_GROUPS)}`: the entity merge map, one row per source row, with decision, relationship, confidence "
        "and reason.",
        f"- `{rel(OUT_CHANGES)}`: every change from original to clean name, one line per step.",
        "",
        "## 1. Checks",
        "",
    ]
    lines += table(["Check", "Result", "Pass"], [[c[0], c[1], "yes" if c[2] else "NO"] for c in all_checks])
    lines += [
        "",
        "## 2. What the cleaning does",
        "",
        "1. **Stable ids.** `vendor_id` is `V` plus the source row number (`V0002` to "
        f"`V{max(r['row'] for r in recs):04d}`), so every later number traces to one row of the raw sheet.",
        "2. **Original names kept.** `vendor_name_raw` is the cell text exactly; all repairs go to `vendor_name_clean`.",
        "3. **Mojibake repaired**, then one dropped letter restored (table below).",
        "4. **Tags and truncation marks** moved out of the display name and into `name_notes`.",
        "5. **Casing.** The source Title Cased every name, so acronyms, legal forms and brands are restored: the acronyms "
        "named in prompt 6 (BDO, DHL, HP, SS&C, TOG, GPT, CBRE, NCC, HEP, plus PricewaterhouseCoopers and LaSalle), other "
        "acronyms in the names, legal forms (LLP, LLC, GmbH; d.o.o. and d.d. in lower case as written in Croatia), brand "
        "casing (HubSpot, LinkedIn, DocuSign) and possessives (Kat's). AWS is the canonical name of the merged Amazon Web "
        "Services group; PwC and JLL are the canonical names of PricewaterhouseCoopers LLP and Jones Lang LaSalle.",
        "6. **Matching key** (`match_key`): the clean name with accents, legal forms, geography, stop words and the "
        "Supplier tag removed. It is used for matching only and never displayed.",
        f"7. **Entity merge map.** {len(MERGE_GROUPS)} groups covering {merge_rows} rows; every other row is its own group. "
        "`group_id` is the vendor_id of the group's largest row.",
        "",
        "## 3. Name changes",
        "",
        f"{len(all_changes)} changes on {changed_rows} of {len(recs)} rows:",
        "",
    ]
    lines += table(["Step", "Changes", "Rows"], [[s, steps[s], rows_by_step[s]] for s in
                                                ("mojibake", "manual fix", "punctuation", "spacing", "tag", "casing") if s in steps])
    lines += ["", "### Mojibake repair table", ""]
    moj = [c for c in all_changes if c["step"] in ("mojibake", "manual fix")]
    lines += table(["vendor_id", "As stored", "Repaired", "How", "Final clean name"],
                   [[c["vendor_id"], c["before"], c["after"], c["step"], by_id[c["vendor_id"]]["clean"]] for c in moj])
    lines += ["", "### Tags and truncation", ""]
    lines += table(["vendor_id", "Before", "After", "Reason"],
                   [[c["vendor_id"], c["before"], c["after"], c["reason"]] for c in all_changes if c["step"] == "tag"])
    lines += ["", "### Names kept as in the source, with a note", ""]
    lines += table(["vendor_id", "Clean name", "Note"],
                   [[f"V{x:04d}", by_row[x]["clean"], note] for x, note in sorted(NAME_NOTES.items())])
    casing_by_row: dict[str, list[dict]] = defaultdict(list)
    for c in all_changes:
        if c["step"] == "casing":
            casing_by_row[c["vendor_id"]].append(c)
    lines += ["", f"Casing changes ({steps.get('casing', 0)} rule applications on {len(casing_by_row)} rows) are listed in "
              f"full in `{rel(OUT_CHANGES)}`. The first rows affected, before and after casing:", ""]
    lines += table(["vendor_id", "Before casing", "After casing", "Rules"],
                   [[vid, cs[0]["before"], cs[-1]["after"], ", ".join(dict.fromkeys(c["reason"] for c in cs))]
                    for vid, cs in list(casing_by_row.items())[:15]])
    lines += ["", "## 4. Entity merge map", "",
              f"{len(recs)} rows become {n_vendors} vendors. Merge groups:", ""]
    grows = []
    for canonical, rows, relationship, confidence, reason in sorted(
            MERGE_GROUPS, key=lambda g: -sum(by_row[x]["cost"] for x in g[1])):
        grows.append([canonical, group_of[rows[0]][1], ", ".join(f"V{x:04d}" for x in rows),
                      money(sum(by_row[x]["cost"] for x in rows)), relationship, confidence, reason])
    lines += table(["Canonical vendor", "group_id", "Rows", "12-month cost", "Relationship", "Confidence", "Reason"], grows)
    lines += ["", "Kept separate, with a shared parent recorded in `parent_company`:", ""]
    lines += table(["Parent", "Rows", "Why it matters"],
                   [[p, "; ".join(f"V{x:04d} {by_row[x]['clean']}" for x in rows), reason] for p, rows, reason in PARENT_LINKS])
    lines += ["", "Reviewed and kept as different vendors (from the near-duplicate search in `01_forensics.md`):", ""]
    lines += table(["Rows", "Verdict", "Reason"],
                   [["; ".join(f"V{x:04d} {by_row[x]['clean']}" for x in rows), verdict, reason]
                    for rows, verdict, reason in DISTINCT_VERDICTS if not set(rows) <= set(group_of)])
    top = sorted(canon_spend.items(), key=lambda kv: -kv[1])[:15]
    cum = 0.0
    trows = []
    for i, ((gid, canonical), spend) in enumerate(top, start=1):
        cum += spend
        trows.append([i, canonical, gid, len(canon_rows[(gid, canonical)]), money(spend), pct(spend / raw_total), pct(cum / raw_total)])
    lines += ["", "## 5. Largest vendors after merging", ""]
    lines += table(["Rank", "Canonical vendor", "group_id", "Rows", "12-month cost", "Share", "Cumulative"], trows)
    lines += ["", f"Total: {money(raw_total)} across {n_vendors} vendors ({len(recs)} rows).", "",
              "## 6. Analyst hint coverage", "",
              f"`docs/vendor_hints.md` maps its hints to {len(hinted)} rows; the other {len(recs) - len(hinted)} rows have "
              "no hint and are classified from their names and general knowledge.", ""]
    text = "\n".join(lines)
    assert_no_dashes(text, "cleaning report")
    write_text(OUT_REPORT, text)
    print(f"wrote {rel(OUT_CLEAN)}, {rel(OUT_GROUPS)}, {rel(OUT_CHANGES)} ({len(all_changes)} changes), {rel(OUT_REPORT)}")
    print(f"rows {len(recs)}; vendors after merging {n_vendors}; total {money(raw_total)}; hinted rows {len(hinted)}")
    for c in all_checks:
        print(("PASS " if c[2] else "FAIL ") + c[0] + " | " + c[1])
    if failed:
        raise SystemExit(f"{len(failed)} checks failed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
