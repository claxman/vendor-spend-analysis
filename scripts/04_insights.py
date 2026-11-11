#!/usr/bin/env python3
"""Step 4 (prompt 17): outputs/analysis/insights.md, built only from files in the repository.

Inputs
  outputs/vendors_classified.csv        the classification (step 3c)
  outputs/analysis/savings.csv          the savings model (scripts/03_savings.py)
  docs/savings_assumptions.md           the register, for the year-1 factors
  qa/vendor_groups.csv                  the merge map, for the vendor count after merging
  outputs/analysis/01_forensic_flags.csv the forensic flags (scripts/01_forensics.py)
  qa/verification_exceptions.csv        the rows the web verification could not establish
  docs/decisions.md                     the open questions for Finance
Output
  outputs/analysis/insights.md          ten short sections, each with figures and vendor_ids

Every figure is computed here from those files; the prose names the rows it rests on. Where a section needs a
fact about a row that the files state in words (a country, say), the script checks that the row's sub_function
or description carries that word before using it, and stops if it does not.

Usage:
    python scripts/04_insights.py
"""
from __future__ import annotations

import csv
import datetime as dt
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from savings_model import MUST_NOT_CUT, PEOPLE_LINKED_LEVERS, REGISTER, load_register, thousands, to_float  # noqa: E402
from vsa_common import money, pct, rel, section_rows, table, write_text  # noqa: E402

CLASSIFIED = ROOT / "outputs" / "vendors_classified.csv"
SAVINGS = ROOT / "outputs" / "analysis" / "savings.csv"
GROUPS = ROOT / "qa" / "vendor_groups.csv"
FLAGS = ROOT / "outputs" / "analysis" / "01_forensic_flags.csv"
EXCEPTIONS = ROOT / "qa" / "verification_exceptions.csv"
DECISIONS = ROOT / "docs" / "decisions.md"
OUT = ROOT / "outputs" / "analysis" / "insights.md"

# Employee hardware (step 2e): retail-flagged rows that a card policy would not remove, because they are equipment.
HARDWARE_IDS = ["V0066", "V0123", "V0131", "V0167", "V0172", "V0175", "V0229", "V0260", "V0378"]
# The country and legal-entity footprint: (country, the word the row must carry, [(vendor_id, kind)]).
COUNTRY_EVIDENCE = [
    ("United Kingdom", r"\bUK\b|United Kingdom|London|England|Kingston",
     [("V0353", "statutory"), ("V0010", "insurance"), ("V0047", "insurance"), ("V0100", "benefits"),
      ("V0211", "benefits"), ("V0004", "audit"), ("V0070", "audit"), ("V0108", "audit"), ("V0068", "audit")]),
    ("Croatia", r"Croatia|Croatian|Zagreb|Split",
     [("V0073", "statutory"), ("V0139", "statutory"), ("V0300", "statutory"), ("V0328", "statutory"),
      ("V0382", "statutory"), ("V0383", "statutory"), ("V0384", "statutory"), ("V0042", "insurance"),
      ("V0067", "audit"), ("V0114", "audit"), ("V0176", "audit"), ("V0216", "bank")]),
    ("India", r"India|Indian|Bengaluru|Bangalore|Mumbai|Gurgaon",
     [("V0284", "statutory"), ("V0305", "secretarial"), ("V0045", "insurance"), ("V0095", "insurance"),
      ("V0143", "insurance"), ("V0054", "benefits"), ("V0128", "benefits"), ("V0017", "audit"), ("V0072", "audit"),
      ("V0164", "audit"), ("V0351", "audit")]),
    ("Australia", r"Australia|Australian|NSW|New South Wales|Victoria|Western Australia",
     [("V0333", "statutory"), ("V0201", "statutory"), ("V0094", "statutory"), ("V0212", "statutory"),
      ("V0071", "insurance"), ("V0111", "payroll"), ("V0195", "benefits"), ("V0153", "audit")]),
    ("Singapore", r"Singapore",
     [("V0088", "secretarial"), ("V0069", "insurance"), ("V0109", "audit"), ("V0273", "benefits")]),
    ("United States", r"\bUS\b|United States|Connecticut|Austin|San Francisco|New York",
     [("V0105", "secretarial"), ("V0334", "secretarial"), ("V0078", "insurance"), ("V0064", "audit")]),
    ("Germany and Switzerland", r"Germany|DACH|Swiss|Switzerland", [("V0016", "payroll"), ("V0090", "payroll")]),
    ("Greece", r"Greece|Athens", [("V0052", "audit")]),
    ("Cayman Islands", r"Cayman", [("V0361", "statutory")]),
]
KINDS = ["statutory", "payroll", "secretarial", "insurance", "benefits", "audit", "bank"]
KIND_LABELS = {"statutory": "Statutory", "payroll": "Payroll and employer of record", "secretarial": "Corporate secretarial and registry",
               "insurance": "Insurance", "benefits": "Benefit schemes", "audit": "Audit, tax and accounting", "bank": "Bank"}
# Software bought for the same job by more than one vendor: (what, [vendor_ids]).
OVERLAPS = [
    ("Two productivity suites", ["V0023", "V0081"]),
    ("Three work-management tools and an Atlassian partner", ["V0091", "V0145", "V0297", "V0032"]),
    ("Two integration and automation platforms", ["V0060", "V0310"]),
    ("Three contact and intent data tools", ["V0040", "V0156", "V0352"]),
    ("Three monitoring and logging tools", ["V0130", "V0311", "V0350"]),
    ("Two meeting and messaging tools", ["V0173", "V0089"]),
    ("Three document and e-signature tools", ["V0194", "V0281", "V0117"]),
    ("Two learning platforms", ["V0221", "V0276"]),
    ("Marketing automation (HubSpot) alongside the Salesforce platform's own marketing", ["V0037"]),
]
LEAVER_SIGNS = [
    ("three one-off payments to UK employment-law firms, of the size of an employer's contribution to a departing "
     "employee's settlement-agreement advice", ["V0230", "V0231", "V0241"]),
    ("a laptop and monitor return service for employers with remote staff", ["V0345"]),
    ("two office moves and a self-storage unit for office equipment or archives", ["V0161", "V0269", "V0282"]),
    ("a virtual UK address and mail scanning", ["V0232"]),
]
SEAT_ROWS = ["V0002", "V0023", "V0081", "V0173", "V0026", "V0027"]
HUB_PERKS = ["V0057", "V0121", "V0038", "V0096"]
HUB_CONTRACTORS = ["V0009", "V0065", "V0074", "V0137"]
HUB_OFFICE = ["V0007", "V0224", "V0134", "V0147"]
STUDENT = ["V0030", "V0086", "V0186"]
CROATIA = re.compile(r"Croatia|Croatian|Zagreb|\bSplit\b|Podstrana|Istria")   # case-sensitive: Split is the city


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def spend_of(rows: list[dict]) -> float:
    return math.fsum(to_float(r["spend_12m"]) for r in rows)


def ids(rows: list[dict]) -> str:
    return ", ".join(f"`{r['vendor_id']}`" for r in rows)


def main() -> int:
    rows = read_csv(CLASSIFIED)
    by_id = {r["vendor_id"]: r for r in rows}
    srows = {s["vendor_id"]: s for s in read_csv(SAVINGS)}
    groups = read_csv(GROUPS)
    flags = read_csv(FLAGS)
    exceptions = read_csv(EXCEPTIONS)
    decisions_text = DECISIONS.read_text(encoding="utf-8")
    _, levers, problems = load_register(REGISTER.read_text(encoding="utf-8"))
    if problems:
        raise SystemExit("register problems: " + "; ".join(problems))
    total = spend_of(rows)

    def share(x: float) -> str:
        return pct(x / total)

    def pick(vids: list[str]) -> list[dict]:
        missing = [v for v in vids if v not in by_id]
        if missing:
            raise SystemExit(f"ids not in the classification: {', '.join(missing)}")
        return [by_id[v] for v in vids]

    def saving(vids: list[str], col: str = "saving_base") -> float:
        return math.fsum(to_float(srows[v][col]) for v in vids)

    # 1. concentration, on the merged view
    canonical: dict[str, list[dict]] = defaultdict(list)
    for g in groups:
        canonical[g["group_id"]].append(by_id[g["vendor_id"]])
    ranked = sorted(canonical.items(), key=lambda kv: -spend_of(kv[1]))
    top = lambda n: math.fsum(spend_of(v) for _, v in ranked[:n])  # noqa: E731
    platform = [r for r in rows if r["cost_cluster"] == "Salesforce platform"]
    sf_labour = pick(["V0009", "V0034"])
    sf = by_id["V0002"]

    # 2. what falls away, the recurring base, the advisers
    recurring = [r for r in rows if r["is_recurring"] == "TRUE"]
    non_recurring = [r for r in rows if r["is_recurring"] == "FALSE"]
    mna = [r for r in rows if r["cost_cluster"] == "M&A and transaction costs"]
    one_off = [r for r in rows if srows[r["vendor_id"]]["lever"] == "One-off spend that falls away"]
    nr_with_saving = [r for r in non_recurring if to_float(srows[r["vendor_id"]]["saving_base"]) > 0]
    advisers = pick(["V0004", "V0018", "V0029"])

    # 3. must not cut
    must = [(label, pick(vids)) for label, vids in MUST_NOT_CUT]
    not_addressable = [r for r in rows if r["is_addressable"] == "FALSE"]

    # 4. control findings
    merges = [(gid, v) for gid, v in canonical.items() if len(v) > 1]
    supplier_tag = [by_id[f["vendor_id"]] for f in flags if f["subgroup"] == "Supplier tag in the name"]
    individuals = [by_id[f["vendor_id"]] for f in flags if f["subgroup"] == "Bare personal name"]
    surname_like = [by_id[f["vendor_id"]] for f in flags if f["subgroup"] == "Single surname-like word"]
    unnamed = pick(["V0325"])
    bisley = by_id["V0018"]
    obrt = sorted((by_id[f["vendor_id"]] for f in flags if f["subgroup"] == "Croatian sole trader (obrt)"),
                  key=lambda r: -to_float(r["spend_12m"]))
    obrt_scale = [r for r in obrt if to_float(r["spend_12m"]) >= 5000]
    hinted_unknown = [by_id[f["vendor_id"]] for f in flags
                      if f["subgroup"] == "Croatian companies the analyst hints list as unknown"]
    retail_flagged = {f["vendor_id"] for f in flags if f["category"] == "Consumer or retail purchases"}
    retail = [by_id[v] for v in sorted(retail_flagged) if v not in HARDWARE_IDS]
    retail_hardware = [by_id[v] for v in sorted(retail_flagged) if v in HARDWARE_IDS]
    removed_groups = {gid for gid, v in canonical.items() if all(r["vendor_id"] in {x["vendor_id"] for x in retail} for r in v)}
    vendors_after = len(canonical) - len(removed_groups)

    # 5. footprint
    footprint = []
    for country, pattern, evidence in COUNTRY_EVIDENCE:
        cells = defaultdict(list)
        country_rows = []
        for vid, kind in evidence:
            r = by_id[vid]
            if not re.search(pattern, r["sub_function"] + " " + r["description"]):
                raise SystemExit(f"{vid} does not name {country} in its sub_function or description")
            cells[kind].append(vid)
            country_rows.append(r)
        footprint.append((country, cells, country_rows))
    follow_levers = ["Audit, tax and accounting firms", "Employer-of-record providers", "Payroll processing providers",
                     "Corporate secretarial, registered agent and share registry"]
    follow_rows = [r for r in rows if srows[r["vendor_id"]]["lever"] in follow_levers]

    # 6. software overlap
    software = [r for r in rows if r["cost_cluster"] in ("Software subscriptions (non-Salesforce)", "Salesforce platform")]
    per_dept: dict[str, list[dict]] = defaultdict(list)
    for r in software:
        per_dept[r["department"]].append(r)
    corporate_it = [r for r in rows if r["sub_function"].startswith("Corporate IT")]
    overlaps = [(what, pick(vids)) for what, vids in OVERLAPS]

    # 7. leavers
    leaver_rows = [(what, pick(vids)) for what, vids in LEAVER_SIGNS]
    seats = pick(SEAT_ROWS)
    coworking = [r for r in rows if r["cost_cluster"] == "Office footprint"]

    # 8. the engineering hub
    croatia_rows = [r for r in rows if CROATIA.search(r["sub_function"] + " " + r["description"])]
    hub_perks, hub_contractors, hub_office, students = pick(HUB_PERKS), pick(HUB_CONTRACTORS), pick(HUB_OFFICE), pick(STUDENT)
    weking = by_id["V0009"]

    # 9. timing
    by_factor: dict[float, list[str]] = defaultdict(list)
    for name, f in levers.items():
        if f["pct_base"] > 0:
            by_factor[f["year1_factor"]].append(name)
    year1_total = math.fsum(to_float(s["saving_year1"]) for s in srows.values())
    base_total = math.fsum(to_float(s["saving_base"]) for s in srows.values())

    # 10. data limits
    unverified = [r for r in rows if r["verified"] == "FALSE"]
    unidentified = [by_id[f["vendor_id"]] for f in flags if f["category"] == "Function not evident from the name"]
    finance_questions = section_rows(decisions_text, "Open questions for Finance")
    low_conf = [r for r in rows if r["confidence"] == "low"]

    def rows_line(label: str, sel: list[dict]) -> str:
        n = f"{len(sel)} row" + ("s" if len(sel) != 1 else "")
        return f"{label}: {n}, {money(spend_of(sel))} ({share(spend_of(sel))}); {ids(sel)}"

    for vid, word in (("V0012", "Bermuda"), ("V0099", "Asia")):
        if word not in by_id[vid]["description"]:
            raise SystemExit(f"{vid} does not name {word} in its description")

    # 11. people-linked spend the review does not count (step 10)
    people_rows = [r for r in rows if srows[r["vendor_id"]]["lever"] in PEOPLE_LINKED_LEVERS]
    people_spend = spend_of(people_rows)
    people_counted = saving([r["vendor_id"] for r in people_rows])
    people_rest = people_spend - people_counted

    L = [
        "# Insights",
        "",
        f"Written {dt.date.today().isoformat()} by `scripts/04_insights.py` from `{rel(CLASSIFIED)}`, `{rel(SAVINGS)}`, "
        f"`{rel(GROUPS)}`, `{rel(FLAGS)}`, `{rel(EXCEPTIONS)}`, `{rel(REGISTER)}` and `{rel(DECISIONS)}`. Every figure is "
        "computed from those files and every finding names its rows. Total spend in the file: "
        f"{money(total)} across {len(rows)} rows and {len(canonical)} vendors after the {len(merges)} merges. Whole dollars; "
        "the costs are the file's modified values.",
        "",
        "## 1. Platform dependency and concentration",
        "",
        f"- The product runs on Salesforce. `V0002` {sf['vendor_name_clean']} is {money(to_float(sf['spend_12m']))}, "
        f"{share(to_float(sf['spend_12m']))} of all spend, and the Salesforce platform cluster (the platform, PDF Butler, "
        f"Kimble, Yoxel and Slack: {ids(platform)}) is {money(spend_of(platform))}, {share(spend_of(platform))}. "
        f"Salesforce-specialist labour adds {money(spend_of(sf_labour))} ({ids(sf_labour)}).",
        f"- Concentration on the merged view: the top vendor is {share(top(1))} of spend, the top 10 are {share(top(10))}, "
        f"the top 50 are {share(top(50))}; the other {len(canonical) - 50} vendors share {share(total - top(50))}.",
        f"- The platform agreement is the largest single lever in the model, {money(saving(['V0002']))} base run-rate "
        f"({money(saving(['V0002'], 'saving_low'))} to {money(saving(['V0002'], 'saving_high'))}), and the largest "
        "dependency: the lever is commercial terms at change of control, never exit, and the figure is the value of a "
        "negotiation that starts when the contract and usage data arrive (Finance question 2).",
        "",
        "## 2. What falls away without action, the recurring base, and the sale-related share",
        "",
        f"- Non-recurring spend: {len(non_recurring)} rows, {money(spend_of(non_recurring))} ({share(spend_of(non_recurring))}). "
        f"Of it, M&A and transaction costs ({ids(mna)}) are {money(spend_of(mna))} and fall away with the sale; another "
        f"{len(one_off)} one-off rows ({money(spend_of(one_off))}) fall away without action and carry no saving in the model; "
        f"{len(nr_with_saving)} rows ({money(spend_of(nr_with_saving))}) in travel and team events carry a saving because the "
        "category recurs even when the payee does not.",
        f"- The recurring base is {len(recurring)} rows, {money(spend_of(recurring))} ({share(spend_of(recurring))}).",
        f"- It still holds {money(spend_of(advisers))} of adviser spend that plausibly includes sale-related work: "
        f"{ids(advisers)} (BDO, Bisley Law, Grant Thornton; step 2e). The recurring figure is therefore likely lower than "
        "shown; Finance question 6 asks for the sale-related share.",
        "",
        "## 3. Vendors that must not be cut",
        "",
        *[f"- {rows_line(label, sel)}" for label, sel in must],
        f"- Together {money(math.fsum(spend_of(sel) for _, sel in must))}. The {len(not_addressable)} rows outside the savings "
        f"base ({money(spend_of(not_addressable))}) are among them; the rest stay addressable but carry a 0% assumption or a "
        "keep-and-review rationale in the classification.",
        "",
        "## 4. Control findings",
        "",
        f"- Duplicate vendor records: {len(merges)} vendors appear under two names each ("
        + "; ".join(f"{v[0]['vendor_name_clean']} and {v[1]['vendor_name_clean']}, {ids(v)}" for _, v in merges)
        + f"), {money(math.fsum(spend_of(v) for _, v in merges))} in all; two more names carry a Supplier tag that suggests a "
        f"second record of the same company ({ids(supplier_tag)}). A vendor master with duplicate records calls for a "
        "duplicate-payment review, which needs invoice-level data: this file holds 12-month totals, and its identical "
        "amounts are explained by the cost modification (`outputs/analysis/01_forensics.md`, section 2).",
        f"- Individual and unnamed payees: {len(individuals)} individuals paid through AP ({money(spend_of(individuals))}; "
        f"{ids(individuals)}), {len(surname_like)} single-word names that may be people ({ids(surname_like)}) and one payment "
        f"with no vendor name ({ids(unnamed)}, {money(spend_of(unnamed))}). Each is a contractor-status or reimbursement "
        "question before it is a saving.",
        f"- A law firm paid under a name that no longer trades: `V0018` {bisley['vendor_name_clean']}, "
        f"{money(to_float(bisley['spend_12m']))}. The firm merged into Gordons Partnership in January 2024 and its company is "
        "now registered as non-trading, so the question for Finance is which entity invoices now (question 7). The provider "
        "of this data also modified vendor names, so an unmatched name is a question, not evidence of a problem. The spend is "
        "legal work and follows the law-firms lever whoever the payee proves to be; the payee check is a control action.",
        f"- Sole traders paid at contractor scale: {len(obrt_scale)} Croatian obrt rows of $5,000 or more, "
        f"{money(spend_of(obrt_scale))} ({ids(obrt_scale)}), and {len(hinted_unknown)} Croatian companies of unknown function "
        f"({money(spend_of(hinted_unknown))}, led by `V0009` Weking at {money(to_float(weking['spend_12m']))}, whose "
        f"{money(to_float(srows['V0009']['saving_base']))} base saving is provisional until Finance confirms the work it supplies). "
        "One-person businesses supplying labour carry an employment-status question as well as an identification one; "
        "with modified vendor names, an unidentified name is a question for Finance, not a finding against the payee.",
        f"- Retail merchants in the vendor master: the forensic pass flags {len(retail_flagged)} consumer or retail payees, "
        f"{money(math.fsum(to_float(by_id[v]['spend_12m']) for v in retail_flagged))}; {len(retail_hardware)} of them are "
        f"employee hardware that stays ({ids(retail_hardware)}), the other {len(retail)} ({money(spend_of(retail))}) are "
        f"food, groceries, gifts, gyms and marketplaces that a purchasing-card and expense policy removes from the vendor "
        f"master. The vendor count falls from {len(canonical)} to {vendors_after} once they go.",
        "",
        "## 5. Country and legal-entity footprint",
        "",
        "Where the statutory, payroll, secretarial, insurance and audit payees place the company's entities and staff. "
        "Each id is a row whose sub_function or description names the country.",
        "",
        *table(["Country", *(KIND_LABELS[k] for k in KINDS), "Spend of these rows"],
               [[country, *(", ".join(f"`{v}`" for v in cells.get(k, [])) or "" for k in KINDS), money(spend_of(crows))]
                for country, cells, crows in footprint]),
        "",
        f"- Nine jurisdictions show, with Aetna (`V0012`, {money(to_float(by_id['V0012']['spend_12m']))}) writing expatriate "
        f"cover from Bermuda and Acclime (`V0099`) serving an Asian entity the file does not name. The Cayman Islands fee "
        "(`V0361`) implies an entity the legal-entity map should confirm (Finance question 5).",
        f"- The cost that follows the footprint: the audit, tax and accounting firms, the employer-of-record and payroll "
        f"providers and the corporate secretarial and registry providers are {len(follow_rows)} rows, "
        f"{money(spend_of(follow_rows))} ({share(spend_of(follow_rows))}), with a base saving of "
        f"{money(math.fsum(to_float(srows[r['vendor_id']]['saving_base']) for r in follow_rows))} that depends on "
        "`group_auditor` and `group_payroll`. Every entity kept keeps an auditor, a payroll and a company secretary.",
        "",
        "## 6. Software overlap",
        "",
        f"Software rows (the Salesforce platform and the non-Salesforce subscriptions): {len(software)} rows, "
        f"{money(spend_of(software))}. Tools per function after the step 3c reading:",
        "",
        *table(["Department", "Tools", "Spend", "Rows"],
               [[d, len(v), money(spend_of(v)), ids(v)] for d, v in sorted(per_dept.items(), key=lambda kv: -spend_of(kv[1]))]),
        "",
        f"- G&A holds {len(corporate_it)} company-wide tools under Corporate IT ({money(spend_of(corporate_it))}). The overlaps "
        "the classification names, each a Consolidate or Terminate case:",
        *[f"  - {what}: {money(spend_of(sel))} ({ids(sel)})" for what, sel in overlaps],
        "",
        "## 7. Signs of leavers in the last 12 months",
        "",
        "The file has no headcount, but some rows are the kind of spend that leavers and a shrinking footprint produce:",
        *[f"- {what}: {money(spend_of(sel))} ({ids(sel)})" for what, sel in leaver_rows],
        f"- What it implies: seat counts and space should be sized on current headcount, not on the 12 months of spend. The "
        f"seat-based rows ({ids(seats)}) are {money(spend_of(seats))}, and the coworking and office rows ({len(coworking)} "
        f"rows) are {money(spend_of(coworking))}; both are priced for the peak if staff have left. Headcount by site and "
        "entity, now and 12 months ago, is the data request in section 10.",
        "",
        "## 8. Retention risk at the engineering hub",
        "",
        f"- {len(croatia_rows)} rows name Croatia, Zagreb or Split in their sub_function or description, "
        f"{money(spend_of(croatia_rows))} ({share(spend_of(croatia_rows))}): the hub's office and parking "
        f"({money(spend_of(hub_office))}; {ids(hub_office)}), student labour ({money(spend_of(students))}; {ids(students)}), "
        f"the Salesforce consultancy and the unidentified contractors ({money(spend_of(hub_contractors))}; "
        f"{ids(hub_contractors)}) and the perks and events ({money(spend_of(hub_perks))}; {ids(hub_perks)}).",
        f"- The model cuts the hub from several sides at once: 60% off team events, 30% off the consultancies, the end of the "
        "agency hiring, and the office exit keeps only a touchdown space. The MultiSport card and the gym are at 0% in the "
        "model but Terminate in the classification. Product knowledge sits with the consultancy's developers (`V0009` risk "
        "note), so the sequence matters: transfer the knowledge and settle the sourcing model before the perks and the "
        "space change, and keep the per-head culture budget the team-events assumption leaves.",
        "",
        "## 9. Timing constraints",
        "",
        f"The year-1 saving is {money(year1_total)} against a base run-rate of {money(base_total)}, because the levers wait "
        "for dates the file does not show:",
        "",
        *table(["Year-1 factor", "What it waits for", "Levers"],
               [[f"{f:g}",
                 {0.25: "a system migration", 0.4: "the financial year-end, when an auditor changes",
                  0.5: "a renewal or notice date the file does not show",
                  0.6: "renewals spread through the year", 0.75: "a policy change within 90 days",
                  0.9: "open mandates closing"}.get(f, ""), "; ".join(names)]
                for f, names in sorted(by_factor.items())]),
        "",
        "- Insurance renewals: the broker and the insurers (`V0010`, `V0012`, `V0042`, `V0045`, `V0047`, `V0069`, `V0071`, "
        "`V0095`, `V0143`) move at renewal, and the file does not show when that is.",
        "- Audit year-end: the group auditor takes over at the year-end of each entity (`V0004`, `V0017`, `V0029`, `V0114` and "
        "the other firms in section 5).",
        "- Lease notice: the office footprint (`V0005`, `V0007`, `V0008`, `V0011`, `V0022` and the smaller rows) follows "
        "notice periods that are not in the file.",
        "- System migration: Sage, Planful, Peakon, Performancepro and HubSpot (`V0028`, `V0039`, `V0055`, `V0080`, `V0037`) "
        "save only after the migration to the parent's systems, so they carry a 0.25 factor.",
        "",
        "## 10. Data limits and the requests that follow",
        "",
        f"- The file is one 12-month total per vendor: no dates, invoices, entities, cost centres or approvers, and the "
        f"costs were modified by the data owner. {len(unverified)} rows ({money(spend_of(unverified))}) could not be verified on "
        f"the web and {len(low_conf)} rows ({money(spend_of(low_conf))}) carry low confidence; {len(unidentified)} payees "
        f"({money(spend_of(unidentified))}) have names that do not show their function. The provider of this data modified "
        "vendor names, so a name that matches no trading firm, or that the web does not confirm, is a question for Finance "
        f"and never evidence of a problem with the payee. The Salesforce contract, {share(to_float(sf['spend_12m']))} of "
        f"spend, is not visible. {len(finance_questions)} questions for Finance are open in `docs/decisions.md`.",
        "- Requests, in the order they unlock the figures:",
        "  1. The monthly AP ledger for the 12 months, with invoice number, date, paying entity, cost centre and approver: "
        "it settles the duplicate-payment review, the one-off against recurring split, the leavers question and the "
        "identification of the payees in section 4.",
        "  2. The contract register with renewal and notice dates for insurance, the leases and coworking, the Salesforce "
        "agreement, the HR and finance systems and the telecom lines: it turns the year-1 factors in section 9 from "
        "conventions into dates.",
        "  3. The Salesforce contract and usage: licence counts by product, the split between platform and ISV fees and "
        "internal CRM seats, the OEM terms for PDF Butler, and any change-of-control clause.",
        "  4. Headcount by site and entity, now and 12 months ago: it sizes the seats, the space, the payroll and the "
        "insurance cover, and it tests the leavers reading in section 7.",
        "",
        "## 11. People-linked spend the review does not count",
        "",
        f"- {money(people_rest)} of people-linked vendor spend is not counted ({money(thousands(people_rest))} rounded): health "
        f"and life cover, statutory cover and benefit schemes, employer-of-record pay and student labor, {money(people_spend)} "
        f"across {len(people_rows)} rows less the {money(people_counted)} of savings the model counts on those lines (the "
        "insurers' rate and the employer-of-record fee). It moves only with the workforce plan, not with a vendor action: "
        f"{ids(people_rows)}.",
    ]
    write_text(OUT, "\n".join(L).rstrip("\n") + "\n")
    print(f"Wrote {rel(OUT)}: {len(L)} lines; top 1 {share(top(1))}, top 10 {share(top(10))}, top 50 {share(top(50))}; "
          f"recurring base {money(spend_of(recurring))}; {len(croatia_rows)} Croatian rows; vendors after a card policy "
          f"{vendors_after}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
