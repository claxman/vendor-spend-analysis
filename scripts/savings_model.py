#!/usr/bin/env python3
"""The savings model (step 4, prompt 17): the register, the lever assignment, the figures and the roll-ups.

Shared by scripts/03_savings.py, which writes outputs/analysis/savings.csv and savings.md, and by qa/check_outputs.py,
whose self-test renders a synthetic report with the same functions. No spend figure is hard-coded: every percentage
comes from docs/savings_assumptions.md and every dollar from outputs/vendors_classified.csv.

The lever of a row is decided in this order (docs/savings_assumptions.md, "How the figures are computed"):
  1. the M&A, customer-mandated, statutory and student-labour clusters take their own levers;
  2. a row the register names under a lever takes it (VENDOR_LEVERS, guarded by a fragment of the vendor name);
  3. any other row with is_recurring FALSE takes "One-off spend that falls away", except in the two clusters where
     the category recurs even when the payee does not;
  4. every remaining row takes the lever of its cluster (CLUSTER_LEVER).
"""
from __future__ import annotations

import math
from collections import defaultdict

from vsa_common import ROOT, money, pct, section_rows, strip_accents, table

REGISTER = ROOT / "docs" / "savings_assumptions.md"
OPPORTUNITIES = ["Salesforce platform agreement", "Office exit", "Back office into group shared services",
                 "Second wave", "Excluded"]
# The people-linked lines the review does not count beyond the small savings it models on them: they move only with the
# workforce plan (step 10, prompt 23).
PEOPLE_LINKED_LEVERS = ["Employee health and life insurance", "Statutory cover and benefit schemes",
                        "Employer-of-record providers", "Student labour"]
PCT_COLUMNS = ["pct_low", "pct_base", "pct_high", "pct_without_decision"]
SAVING_COLUMNS = ["saving_low", "saving_base", "saving_high", "saving_without_decision", "saving_year1"]
SAVINGS_COLUMNS = ["vendor_id", "vendor_name_clean", "spend_12m", "cost_cluster", "lever", "opportunity",
                   *PCT_COLUMNS, "year1_factor", "depends_on", *SAVING_COLUMNS]
REGISTER_COLUMNS = ["Lever", "Opportunity", "Applies to", *PCT_COLUMNS, "year1_factor", "depends_on", "Reasoning"]
MNA_CLUSTER = "M&A and transaction costs"
# Clusters whose rows take the cluster's own lever whatever else is true of the row.
OWN_LEVER_CLUSTERS = {
    MNA_CLUSTER: "M&A and transaction costs",
    "Customer-mandated platform fees": "Customer-mandated platform fees",
    "Statutory and government": "Statutory and government",
    "Student labour": "Student labour",
}
# The category recurs even when the payee does not, so a non-recurring row keeps its cluster's lever.
CATEGORY_RECURS = {"Travel and entertainment", "Team events, perks and wellness"}
ONE_OFF_LEVER = "One-off spend that falls away"
CLUSTER_LEVER = {
    "Office footprint": "Office footprint",
    "Office running costs": "Office running costs",
    "Travel and entertainment": "Other travel, hotels, restaurants and food through AP",
    "Team events, perks and wellness": "Team events, perks and wellness",
    "Audit, tax, accounting and corporate services": "Audit, tax and accounting firms",
    "Legal": "Law firms and legal resourcing",
    "Insurance and benefits": "Employee health and life insurance",
    "Recruiting and HR outsourcing": "Recruitment agencies and job boards",
    "Cloud, telecom and IT": "Other cloud and IT",
    "Outsourced engineering and contractors": "Outsourced engineering and contractors",
    "Software subscriptions (non-Salesforce)": "Other software subscriptions",
    "Marketing agencies, media and memberships": "Other marketing, media and events",
    "Unidentified and individual payees": "Unidentified and individual payees",
}
SLACK_YOXEL = "Slack and Yoxel inside the Salesforce renewal"
AUDIT = "Audit, tax and accounting firms"
SECRETARIAL = "Corporate secretarial, registered agent and share registry"
EMPLOYMENT = "Employment-law settlement advice"
TRAINING = "External training and coaching"
EOR = "Employer-of-record providers"
PAYROLL = "Payroll processing providers"
BROKERS = "Commercial insurance through brokers"
HEALTH = "Employee health and life insurance"
STATUTORY_COVER = "Statutory cover and benefit schemes"
SYSTEMS = "HR and finance systems"
TELECOM = "Telecom and internet providers"
OTHER_IT = "Other cloud and IT"
HARDWARE = "Employee hardware"
COURIERS = "Couriers and postage"
AGENCIES = "Marketing agencies"
OTHER_MARKETING = "Other marketing, media and events"
UNIDENTIFIED = "Unidentified and individual payees"
FEES = "Bank, payment and certification fees"
# Rows the register names under a lever: vendor_id -> (a fragment of the clean name, the lever). The fragment stops a
# mistyped id from selecting the wrong row.
VENDOR_LEVERS = {
    "V0002": ("Salesforce", "Salesforce platform agreement"),
    "V0006": ("Cloudcrossing", "PDF Butler OEM pricing"),
    "V0027": ("Kimble", "Kimble PSA licences"),
    "V0170": ("Yoxel", SLACK_YOXEL), "V0173": ("Slack", SLACK_YOXEL),
    "V0351": ("Mithras", AUDIT),
    "V0088": ("Intertrust", SECRETARIAL), "V0099": ("Acclime", SECRETARIAL), "V0105": ("Acclime", SECRETARIAL),
    "V0334": ("Capitol", SECRETARIAL), "V0305": ("Bigshare", SECRETARIAL),
    "V0068": ("GrantTree", "R&D tax credit adviser (contingent fee)"),
    "V0230": ("Kalra", EMPLOYMENT), "V0231": ("Kilgannon", EMPLOYMENT), "V0241": ("Landu", EMPLOYMENT),
    "V0076": ("Visalogic", "Law firms and legal resourcing"),
    "V0026": ("LinkedIn", "LinkedIn"),
    "V0020": ("Big Frontier", TRAINING), "V0075": ("Ramiro", TRAINING), "V0079": ("Emerge", TRAINING),
    "V0127": ("Calm Achiever", TRAINING),
    "V0016": ("HR Solution", EOR), "V0090": ("Hrsolution", EOR), "V0179": ("Radius", EOR),
    "V0111": ("Australian Payroll", PAYROLL), "V0058": ("Smart Group", PAYROLL),
    "V0010": ("Jensten", BROKERS), "V0078": ("Shoff Darby", BROKERS),
    "V0098": ("Mercer", HEALTH), "V0273": ("Doctor Anywhere", HEALTH),
    "V0094": ("Allianz", STATUTORY_COVER), "V0201": ("icare", STATUTORY_COVER), "V0212": ("Allianz", STATUTORY_COVER),
    "V0300": ("Nastavni Zavod", STATUTORY_COVER), "V0328": ("Ustanova", STATUTORY_COVER),
    "V0382": ("Specijalisticka", STATUTORY_COVER), "V0383": ("Specijalisticka", STATUTORY_COVER),
    "V0384": ("Ustanova", STATUTORY_COVER), "V0100": ("Green Commute", STATUTORY_COVER),
    "V0195": ("Inside Edge", STATUTORY_COVER), "V0054": ("Sodexo", STATUTORY_COVER), "V0128": ("Pluxee", STATUTORY_COVER),
    "V0057": ("Benefit Systems", STATUTORY_COVER),
    "V0066": ("Racunalni Sistemi", HARDWARE), "V0123": ("Apple", HARDWARE), "V0131": ("Sniper Systems", HARDWARE),
    "V0167": ("HP", HARDWARE), "V0172": ("Apple", HARDWARE), "V0175": ("Apple", HARDWARE), "V0229": ("Apple", HARDWARE),
    "V0260": ("E-Disti", HARDWARE), "V0378": ("Currys", HARDWARE), "V0048": ("Shree Info System", HARDWARE),
    "V0196": ("Rhea", COURIERS), "V0232": ("UK Postbox", COURIERS), "V0240": ("Trans-Agram", COURIERS),
    "V0303": ("DHL", COURIERS), "V0316": ("Parcelforce", COURIERS), "V0336": ("DHL", COURIERS),
    "V0368": ("Gophr", COURIERS), "V0371": ("FedEx", COURIERS), "V0377": ("Post Office", COURIERS),
    "V0211": ("Caboodle", "Other software subscriptions"),
    "V0028": ("Sage", SYSTEMS), "V0039": ("Planful", SYSTEMS), "V0055": ("Peakon", SYSTEMS),
    "V0080": ("Performancepro", SYSTEMS),
    "V0037": ("HubSpot", "HubSpot"),
    "V0003": ("Navan", "Navan"), "V0024": ("Navan", "Navan"),
    "V0014": ("Amazon Web Services", "AWS"), "V0103": ("Amazon Web Services", "AWS"),
    "V0046": ("New Star Networks", TELECOM), "V0053": ("Hrvatski Telekom", TELECOM), "V0083": ("Omonia", TELECOM),
    "V0104": ("Telemach", TELECOM), "V0135": ("Vodafone", TELECOM), "V0140": ("T-Mobile", TELECOM),
    "V0141": ("Akton", TELECOM), "V0163": ("StarHub", TELECOM), "V0188": ("British Telecommunications", TELECOM),
    "V0306": ("Zettanet", TELECOM), "V0356": ("Inet Telecoms", TELECOM),
    "V0309": ("Avoxi", OTHER_IT), "V0363": ("Click Send", OTHER_IT),
    "V0050": ("MightyHive", AGENCIES), "V0056": ("Plus Your Business", AGENCIES), "V0184": ("Carrington", AGENCIES),
    "V0168": ("Cision", OTHER_MARKETING),
    "V0025": ("Tmforum", "TM Forum"), "V0249": ("TM Forum", "TM Forum"),
    "V0074": ("Bijeli Pijesak", UNIDENTIFIED), "V0137": ("Orcola", UNIDENTIFIED),
    "V0216": ("Raiffeisenbank", FEES), "V0198": ("FastSpring", FEES), "V0142": ("Bureau Veritas", FEES),
    "V0203": ("Amazon.co.uk", "Office running costs"), "V0291": ("Amazon (Aus)", "Office running costs"),
}
# Rows whose lever is an analyst call rather than a rule (docs/savings_assumptions.md, "Lever assignment").
ANALYST_CALLS = {
    "V0351": "actuarial valuations are an accounting requirement of the Indian entity, so they follow the group auditor",
    "V0211": "a benefits platform fee, not pay or cover, so it is software rather than a benefit scheme",
    "V0098": "benefits consulting is the broking and scheme-terms work that the lever describes",
    "V0273": "a health benefit for Singapore staff",
    "V0057": "the MultiSport card is the gym scheme the assumption names; it stays as an employee benefit at the hub (step 4b), and Gym4You consolidates into it on the Team events lever",
    "V0058": "HR outsourcing, unconfirmed; the closest lever by sub_function, and its rationale already waits for group payroll",
    "V0179": "global payroll and expansion services are employer-of-record work",
    "V0020": "a lever added in step 4, because the assumptions list has no line for training",
    "V0075": "a lever added in step 4, because the assumptions list has no line for training",
    "V0079": "a lever added in step 4, because the assumptions list has no line for training",
    "V0074": "Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of its cluster",
    "V0127": "productivity training identified in step 5, so the training lever rather than the recruitment lever of its cluster",
    "V0137": "Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of its cluster",
    "V0309": "telephony numbers that do not end with the offices, so not the telecom lever",
    "V0363": "an SMS API that does not end with the offices, so not the telecom lever",
    "V0168": "a press release wire, not an agency",
    "V0076": "immigration work follows the legal cluster into the panel",
    "V0216": "a lever added in step 4 at 0%, because the assumptions list has no line for bank fees",
    "V0198": "a lever added in step 4 at 0%, because the assumptions list has no line for payment processing",
    "V0142": "a lever added in step 4 at 0%, because the assumptions list has no line for certification audits",
    "V0203": "follows its cluster as office consumables (confirmed in step 4b), although the card policy that removes it does not depend on the office decision",
    "V0291": "follows its cluster as office consumables (confirmed in step 4b), although the card policy that removes it does not depend on the office decision",
}
# Vendors that must not be cut (insights section 3 and the presentation figures): (label, vendor_ids).
MUST_NOT_CUT = [
    ("Customer-mandated platform fees (Telefónica, Ariba)", ["V0015", "V0093", "V0191"]),
    ("Software escrow for customer contracts", ["V0144"]),
    ("ISO certification audits", ["V0142"]),
    ("Statutory workers' compensation and occupational health",
     ["V0094", "V0201", "V0212", "V0300", "V0328", "V0382", "V0383", "V0384"]),
    ("Taxes, government fees, regulators and the depository", ["V0073", "V0139", "V0284", "V0333", "V0353", "V0361"]),
    ("Salary-sacrifice schemes (cycle to work, novated leasing)", ["V0100", "V0195"]),
    ("Meal and benefit cards", ["V0054", "V0128"]),
    ("The contingent-fee R&D tax credit adviser", ["V0068"]),
]
# Levers whose spend falls away without action (the presentation figures).
FALLS_AWAY_LEVERS = ["M&A and transaction costs", ONE_OFF_LEVER]
ROLLUP_HEADINGS = {"opportunity": "Savings by opportunity", "cost_cluster": "Savings by cost cluster",
                   "lever": "Savings by lever"}


def thousands(x: float) -> int:
    """A dollar figure rounded to the nearest $1,000, as an integer number of dollars."""
    return int(round(x / 1000.0)) * 1000


def dollars(x: float) -> int:
    """A dollar figure rounded to the nearest dollar, half up, as an integer: the rounding the documents use when a
    calculation is written out in full (step 9)."""
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def money_k(x: float) -> str:
    return money(thousands(x))
ROLLUP_LABELS = {"opportunity": "Opportunity", "cost_cluster": "Cost cluster", "lever": "Lever"}
# Report column -> savings column, for the roll-up tables and the check that reads them back.
MONEY_COLUMNS = {"Spend": "spend", "Low": "saving_low", "Base": "saving_base", "High": "saving_high",
                 "Without decision": "saving_without_decision", "Year 1": "saving_year1"}


# ---------------------------------------------------------------- the register

def to_float(s) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return float("nan")


def load_register(text: str) -> tuple[list[str], dict[str, dict], list[str]]:
    """(decision names, {lever: fields}, problems) from the text of docs/savings_assumptions.md.

    Fields: opportunity, applies_to, reasoning, the four percentages and year1_factor as floats, depends_on as a
    list of tags. A lever whose numbers do not parse is kept with what parsed, and the problem is reported.
    """
    problems: list[str] = []
    decisions = [r[0].strip("`") for r in section_rows(text, "Acquirer decisions")[1:]]
    rows = section_rows(text, "Assumptions")
    header = rows[0] if rows else []
    missing = [c for c in REGISTER_COLUMNS if c not in header]
    if missing:
        return decisions, {}, [f"the Assumptions table lacks the columns {', '.join(missing)}"]
    idx = {c: header.index(c) for c in REGISTER_COLUMNS}
    levers: dict[str, dict] = {}
    for r in rows[1:]:
        name = r[0]
        if len(r) != len(header):
            problems.append(f"{name}: {len(r)} cells for {len(header)} columns")
            continue
        if name in levers:
            problems.append(f"{name}: listed twice")
        d = {"opportunity": r[idx["Opportunity"]], "applies_to": r[idx["Applies to"]], "reasoning": r[idx["Reasoning"]],
             "depends_on": [t.strip().strip("`").strip() for t in r[idx["depends_on"]].split(",") if t.strip()]}
        numbers_ok = True
        for c in PCT_COLUMNS + ["year1_factor"]:
            d[c] = to_float(r[idx[c]])
            if math.isnan(d[c]):
                problems.append(f"{name}: {c} is {r[idx[c]]!r}")
                numbers_ok = False
        levers[name] = d
        if d["opportunity"] not in OPPORTUNITIES:
            problems.append(f"{name}: opportunity {d['opportunity']!r} is not one of the five")
        if not d["depends_on"]:
            problems.append(f"{name}: no depends_on tag")
        elif "none" in d["depends_on"] and len(d["depends_on"]) > 1:
            problems.append(f"{name}: none together with a decision name")
        else:
            problems += [f"{name}: {t} is not a registered decision" for t in d["depends_on"]
                         if t != "none" and t not in decisions]
        if not numbers_ok:
            continue
        if not 0 <= d["pct_low"] <= d["pct_base"] <= d["pct_high"] <= 100:
            problems.append(f"{name}: low, base and high are {d['pct_low']:g}, {d['pct_base']:g}, {d['pct_high']:g}")
        if not 0 <= d["pct_without_decision"] <= d["pct_base"]:
            problems.append(f"{name}: pct_without_decision {d['pct_without_decision']:g} is outside 0 to the base")
        if d["depends_on"] == ["none"] and d["pct_without_decision"] != d["pct_base"]:
            problems.append(f"{name}: untagged, but pct_without_decision differs from pct_base")
        if not 0 <= d["year1_factor"] <= 1:
            problems.append(f"{name}: year1_factor {d['year1_factor']:g} is outside 0 to 1")
    if not levers:
        problems.append("the Assumptions table has no levers")
    return decisions, levers, problems


# ---------------------------------------------------------------- the lever of a row

def lever_for(row: dict) -> str:
    cluster = row["cost_cluster"]
    if cluster in OWN_LEVER_CLUSTERS:
        return OWN_LEVER_CLUSTERS[cluster]
    vid = row["vendor_id"]
    if vid in VENDOR_LEVERS:
        fragment, lever = VENDOR_LEVERS[vid]
        if strip_accents(fragment).lower() not in strip_accents(row["vendor_name_clean"]).lower():
            raise ValueError(f"{vid} is {row['vendor_name_clean']!r}, not the {fragment!r} row the lever map expects")
        return lever
    if row["is_recurring"] == "FALSE" and cluster not in CATEGORY_RECURS:
        return ONE_OFF_LEVER
    if cluster not in CLUSTER_LEVER:
        raise ValueError(f"{vid}: no lever for cluster {cluster!r}")
    return CLUSTER_LEVER[cluster]


def saving_row(row: dict, lever: str, fields: dict) -> dict:
    """One savings row with float figures: the row's spend times each percentage, and year 1 from the base."""
    spend = to_float(row["spend_12m"])
    out = {"vendor_id": row["vendor_id"], "vendor_name_clean": row["vendor_name_clean"], "spend_12m": row["spend_12m"],
           "cost_cluster": row["cost_cluster"], "lever": lever, "opportunity": fields["opportunity"],
           "year1_factor": fields["year1_factor"], "depends_on": ", ".join(fields["depends_on"])}
    for c in PCT_COLUMNS:
        out[c] = fields[c]
    for saving, p in zip(SAVING_COLUMNS[:4], PCT_COLUMNS):
        out[saving] = spend * fields[p] / 100
    out["saving_year1"] = out["saving_base"] * fields["year1_factor"]
    return out


def format_row(d: dict) -> dict:
    """The row as the CSV holds it: spend verbatim from the classification, percentages as written in the
    register, savings at full precision."""
    out = dict(d)
    for c in PCT_COLUMNS + ["year1_factor"]:
        out[c] = f"{d[c]:g}"
    for c in SAVING_COLUMNS:
        out[c] = repr(float(d[c]))
    return out


def build(rows: list[dict], levers: dict[str, dict]) -> list[dict]:
    """The savings rows, formatted for the CSV, in the order of the classification."""
    out = []
    for r in rows:
        lever = lever_for(r)
        if lever not in levers:
            raise ValueError(f"{r['vendor_id']}: lever {lever!r} is not in the register")
        out.append(format_row(saving_row(r, lever, levers[lever])))
    return out


# ---------------------------------------------------------------- roll-ups

def _sums(group: list[dict]) -> dict:
    return {"rows": len(group), "spend": math.fsum(to_float(s["spend_12m"]) for s in group),
            **{c: math.fsum(to_float(s[c]) for s in group) for c in SAVING_COLUMNS}}


def rollup(srows: list[dict], key: str) -> dict[str, dict]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for s in srows:
        groups[s[key]].append(s)
    return {name: _sums(group) for name, group in groups.items()}


def totals(srows: list[dict]) -> dict:
    return _sums(srows)


def decision_values(srows: list[dict], decisions: list[str], levers: dict[str, dict]) -> list[dict]:
    """Per decision: the levers tagged with it, their spend, the base saving with the decision, the saving without
    it, and the difference as the value of the decision."""
    out = []
    for d in decisions:
        tagged = [n for n, f in levers.items() if d in f["depends_on"]]
        group = [s for s in srows if s["lever"] in tagged]
        sums = _sums(group)
        out.append({"decision": d, "levers": tagged, "rows": sums["rows"], "spend": sums["spend"],
                    "with": sums["saving_base"], "without": sums["saving_without_decision"],
                    "value": sums["saving_base"] - sums["saving_without_decision"], "year1": sums["saving_year1"]})
    return out


def rollup_table(srows: list[dict], key: str, order: list[str] | None = None, extra=None,
                 extra_headers: list[str] | None = None) -> list[str]:
    """A markdown table of the roll-up by `key`, one row per group and a Total row. `order` fixes the row order
    for the groups it names; the rest follow by spend. `extra(name)` adds cells after the name."""
    groups = rollup(srows, key)
    order = [n for n in (order or []) if n in groups]
    names = order + sorted((n for n in groups if n not in order), key=lambda n: (-groups[n]["spend"], n))
    tot = totals(srows)

    def cells(name: str, g: dict) -> list:
        share = pct(g["saving_base"] / g["spend"]) if g["spend"] else "n/a"
        return [name, *(extra(name) if extra else []), g["rows"], *(money(g[c]) for c in MONEY_COLUMNS.values()), share]

    body = [cells(n, groups[n]) for n in names] + [cells("Total", tot)]
    if extra:
        body[-1] = ["Total", *([""] * len(extra_headers or [])), tot["rows"],
                    *(money(tot[c]) for c in MONEY_COLUMNS.values()),
                    pct(tot["saving_base"] / tot["spend"]) if tot["spend"] else "n/a"]
    headers = [ROLLUP_LABELS[key], *(extra_headers or []), "Rows", *MONEY_COLUMNS, "Base share of spend"]
    return table(headers, body)


def render_rollup_sections(srows: list[dict], levers: dict[str, dict]) -> str:
    """The three roll-up sections that qa/check_outputs.py reads back (V8)."""
    lines = ["## " + ROLLUP_HEADINGS["opportunity"], "", *rollup_table(srows, "opportunity", OPPORTUNITIES), "",
             "## " + ROLLUP_HEADINGS["cost_cluster"], "", *rollup_table(srows, "cost_cluster"), "",
             "## " + ROLLUP_HEADINGS["lever"], "",
             *rollup_table(srows, "lever", list(levers),
                           extra=lambda n: [levers[n]["opportunity"], ", ".join(levers[n]["depends_on"])]
                           if n in levers else ["", ""],
                           extra_headers=["Opportunity", "depends_on"]), ""]
    return "\n".join(lines) + "\n"


def reconciliation(srows: list[dict]) -> tuple[list[str], float]:
    """A table showing that the vendor rows sum to the levers, clusters and opportunities, and the largest
    difference found, in dollars."""
    tot = totals(srows)
    sums = {key: rollup(srows, key) for key in ROLLUP_HEADINGS}
    body, worst = [], 0.0
    for label, col in [("Rows", "rows"), *MONEY_COLUMNS.items()]:
        parts = {key: (sum(g[col] for g in groups.values()) if col == "rows"
                       else math.fsum(g[col] for g in groups.values())) for key, groups in sums.items()}
        diff = max(abs(parts[k] - tot[col]) for k in parts)
        worst = max(worst, diff)
        fmt = (lambda x: f"{x:,}") if col == "rows" else (lambda x: f"${x:,.2f}")
        body.append([label, fmt(tot[col]), fmt(parts["lever"]), fmt(parts["cost_cluster"]), fmt(parts["opportunity"]),
                     f"${diff:,.2f}" if col != "rows" else f"{diff:,.0f}"])
    return table(["Measure", "Vendor rows", "Sum of levers", "Sum of clusters", "Sum of opportunities",
                  "Largest difference"], body), worst
