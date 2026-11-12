#!/usr/bin/env python3
"""Step 4 (prompt 17): the savings model.

Inputs
  outputs/vendors_classified.csv   the classification (step 3c), one row per vendor
  docs/savings_assumptions.md      the register: ten acquirer decisions and one row per lever with its percentages,
                                   year-1 factor, depends_on tag and reasoning
Outputs
  outputs/analysis/savings.csv     one row per vendor: vendor_id, name, spend, cluster, lever, opportunity, the four
                                   percentages, year1_factor, depends_on, and the run-rate savings low, base and
                                   high, the saving without the decision and the year-1 saving, at full precision
  outputs/analysis/savings.md      the totals, the excluded spend by reason, the savings by opportunity, cluster and
                                   lever, the acquirer decisions and their value, the 15 largest vendor savings, the
                                   savings on non-recurring rows, the reconciliation and the analyst calls, in
                                   whole dollars

No spend figure is hard-coded: the dollars come from the classification and the percentages from the register
(scripts/savings_model.py). After writing, the savings checks V1 to V11 of qa/check_outputs.py run on the files
just written. Exit code 1 if the register does not load, a row has no lever, or a check fails.

Usage:
    python scripts/03_savings.py
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "qa"))
import check_outputs  # noqa: E402
from savings_model import (  # noqa: E402
    ANALYST_CALLS, FALLS_AWAY_LEVERS, MONEY_COLUMNS, MUST_NOT_CUT, OPPORTUNITIES, PCT_COLUMNS, PEOPLE_LINKED_LEVERS,
    REGISTER, SAVING_COLUMNS, SAVINGS_COLUMNS, build, decision_values, dollars, money_k, reconciliation,
    render_rollup_sections, rollup, thousands, to_float, totals,
)
from vsa_common import money, pct, rel, table, write_text  # noqa: E402

CLASSIFIED = check_outputs.CLASSIFIED
SAVINGS_CSV = ROOT / "outputs" / "analysis" / "savings.csv"
SAVINGS_MD = ROOT / "outputs" / "analysis" / "savings.md"
SUMMARY_MD = ROOT / "outputs" / "analysis" / "savings_summary.md"
REVIEW_CSV = ROOT / "qa" / "second_pass_review.csv"
TOP_N = 15
LARGEST_VENDOR = "V0002"


def whole_pct(part: float, whole: float) -> str:
    return f"{round(100 * part / whole):d}%" if whole else "n/a"


NAMED_LINES = 3   # an opportunity with more lines than NAMED_LINES + 1 names its largest three and groups the rest


def calculation_table(srows: list[dict], opp: str) -> list[str]:
    """Step 9 (prompt 22): the calculation behind one opportunity in whole dollars, so that the Top 3 can state it and
    a reader can reproduce it. One row per saving line: its spend to the dollar, its base rate, and spend times rate
    rounded to the dollar; the three largest lines and the rest as one row where there are more than four; a Total
    that is the sum of the rounded rows; and the figure rounded to the nearest $1,000, as the Opportunities table
    shows it. qa/check_outputs.py (D5) recomputes every calculation the Top 3 states from savings.csv."""
    per: dict[str, dict] = {}
    for s in srows:
        if s["opportunity"] != opp:
            continue
        d = per.setdefault(s["lever"], {"spend": 0.0, "base": 0.0, "pct": int(float(s["pct_base"]))})
        d["spend"] += to_float(s["spend_12m"])
        d["base"] += to_float(s["saving_base"])
    ordered = sorted(per.items(), key=lambda kv: (-kv[1]["base"], kv[0]))
    named, rest = (ordered, []) if len(ordered) <= NAMED_LINES + 1 else (ordered[:NAMED_LINES], ordered[NAMED_LINES:])
    body = [[name, dollars(d["spend"]), f"{d['pct']}%", dollars(d["spend"] * d["pct"] / 100)] for name, d in named]
    if rest:
        rates = sorted({d["pct"] for _, d in rest})
        body.append([f"The other {len(rest)} lines together", dollars(math.fsum(d["spend"] for _, d in rest)),
                     f"{rates[0]}% to {rates[-1]}%", dollars(math.fsum(d["base"] for _, d in rest))])
    exact = math.fsum(d["base"] for _, d in ordered)
    out = [[n, money(sp), r, money(sv)] for n, sp, r, sv in body]
    out.append(["Total", money(sum(b[1] for b in body)), "", money(sum(b[3] for b in body))])
    return [f"### {opp}", "", *table(["Saving line", "Spend", "Rate", "Saving"], out), "",
            f"Rounded to the nearest $1,000: {money(thousands(exact))}."]


def people_linked_table(srows: list[dict]) -> list[str]:
    """Step 10 (prompt 23): the people-linked lines (PEOPLE_LINKED_LEVERS), each with its rows, spend, the saving the
    model counts on it and the rest, in whole dollars; a Total that is the sum of the rows; and the rest rounded to the
    nearest $1,000, the figure the Top 3 and the insights quote."""
    body = []
    for lever in PEOPLE_LINKED_LEVERS:
        sel = [s for s in srows if s["lever"] == lever]
        spend = dollars(math.fsum(to_float(s["spend_12m"]) for s in sel))
        counted = dollars(math.fsum(to_float(s["saving_base"]) for s in sel))
        body.append([lever, len(sel), spend, counted, spend - counted])
    tot = [sum(b[i] for b in body) for i in (1, 2, 3, 4)]
    out = [[n, str(r), money(sp), money(c), money(nc)] for n, r, sp, c, nc in body]
    out.append(["Total", str(tot[0]), money(tot[1]), money(tot[2]), money(tot[3])])
    return [*table(["Saving line", "Rows", "Spend", "Saving counted", "Not counted"], out), "",
            f"Rounded to the nearest $1,000: {money(thousands(tot[3]))} not counted, after {money(thousands(tot[2]))} of "
            f"savings counted on these lines."]


ZAGREB_LEASE = ("V0007", "Zagrebtower")   # the Zagreb lease row and a fragment of its name, as VENDOR_LEVERS guards ids
OFFICE_LEVER = "Office footprint"


def outside_platform_rows(opp_lines: list[tuple[str, dict]], tot: dict) -> list[list[str]]:
    """Step 11 (prompt 24): the spend and the base saving outside the Salesforce platform line (total less that line, both
    from the rounded figures above), and the saving as a share of that spend: the memo's saving rate outside the platform."""
    sf = next((k for n, k in opp_lines if n == OPPORTUNITIES[0]), None)
    if sf is None:
        return []
    spend, base = tot["spend"] - sf["spend"], tot["saving_base"] - sf["saving_base"]
    return [["Spend outside the Salesforce platform (total less the Salesforce platform agreement line)", money(spend)],
            ["Base saving outside the Salesforce platform (base less that line's base)", money(base)],
            ["Base saving outside the platform as a share of the spend outside it (the saving rate outside the platform)",
             whole_pct(base, spend)]]


def office_check_table(srows: list[dict]) -> list[str]:
    """Step 11 (prompt 24): a check of the office assumption from the rows. The Office footprint line's spend, the Zagreb
    lease, and every other site, adviser and charge on the line (what closing every site except Zagreb would save),
    in whole dollars, against the share the base case takes; the line is the lease plus the rest."""
    sel = [s for s in srows if s["lever"] == OFFICE_LEVER]
    zagreb = [s for s in sel if s["vendor_id"] == ZAGREB_LEASE[0]]
    if len(zagreb) != 1 or ZAGREB_LEASE[1].lower() not in zagreb[0]["vendor_name_clean"].lower():
        raise SystemExit(f"{ZAGREB_LEASE[0]} is not the {ZAGREB_LEASE[1]} row on the {OFFICE_LEVER} line")
    exact = math.fsum(to_float(s["spend_12m"]) for s in sel)
    line, lease = dollars(exact), dollars(to_float(zagreb[0]["spend_12m"]))
    others = line - lease
    pct_base = int(float(zagreb[0]["pct_base"]))
    base = dollars(exact * pct_base / 100)
    body = [[f"Leases and coworking, the {OFFICE_LEVER} line", str(len(sel)), money(line), "100%"],
            [f"The Zagreb lease (`{ZAGREB_LEASE[0]}` {zagreb[0]['vendor_name_clean']})", "1", money(lease), whole_pct(lease, line)],
            ["Every other site, adviser and charge on the line: what closing every site except Zagreb, with its lease "
             "untouched, would save",
             str(len(sel) - 1), money(others), whole_pct(others, line)],
            [f"The base case, {pct_base}% of the line", "", money(base), f"{pct_base}%"],
            ["Difference between the cross-check and the base case", "", money(others - base),
             whole_pct(others - base, line)]]
    return [*table(["Measure", "Rows", "Figure", "Share of the line"], body), "",
            f"Rounded to the nearest $1,000: as a cross-check, closing every site except Zagreb with its lease untouched would "
            f"save {money(thousands(others))} ({whole_pct(others, line)} of the leases), against {money(thousands(base))} at the "
            f"{pct_base}% applied evenly to every lease row, so the {pct_base}% sits just below that."]


def render_summary(srows: list[dict], rows: list[dict], decisions: list[str], levers: dict[str, dict]) -> str:
    """The figures the documents may quote: rounded to the nearest $1,000, every total the sum of the rounded lines it
    shows, so that parts always add to totals."""
    by_id = {r["vendor_id"]: r for r in rows}
    by_opp = rollup(srows, "opportunity")
    by_lever = rollup(srows, "lever")
    cols = ["spend", "saving_low", "saving_base", "saving_high", "saving_year1", "saving_without_decision"]
    opp_lines = []
    for name in OPPORTUNITIES:
        g = by_opp.get(name)
        if not g:
            continue
        k = {c: thousands(g[c]) for c in cols}
        k["value"] = k["saving_base"] - k["saving_without_decision"]
        opp_lines.append((name, k))
    tot = {c: sum(k[c] for _, k in opp_lines) for c in cols + ["value"]}
    spend_total = tot["spend"]

    def row(name, k):
        return [name, money(k["spend"]), money(k["saving_low"]), money(k["saving_base"]), money(k["saving_high"]),
                money(k["saving_year1"]), money(k["saving_without_decision"]), money(k["value"])]

    largest = thousands(to_float(by_id[LARGEST_VENDOR]["spend_12m"]))
    lines = [
        "# Presentation figures",
        "",
        f"Written by `scripts/03_savings.py` with `{rel(SAVINGS_MD)}`. These are the figures the Top 3, the memo, the "
        "methodology and the README may quote. Every dollar figure is rounded to the nearest $1,000 and every total is the "
        "sum of the rounded lines above it, so that parts always add to totals; percentages are whole numbers of the "
        "rounded total spend. The exact figures are in `savings.md` and `savings.csv`.",
        "",
        "## Spend and savings",
        "",
        *table(["Measure", "Figure"], [
            ["Total spend, 12 months (the sum of the opportunity lines below)", money(spend_total)],
            ["Largest vendor, Salesforce UK, and its share of spend", f"{money(largest)} ({whole_pct(largest, spend_total)})"],
            ["Run-rate saving, low", money(tot["saving_low"])],
            ["Run-rate saving, base", money(tot["saving_base"])],
            ["Run-rate saving, high", money(tot["saving_high"])],
            ["Base saving as a share of spend", whole_pct(tot["saving_base"], spend_total)],
            ["High saving as a share of spend", whole_pct(tot["saving_high"], spend_total)],
            ["Year-1 saving", money(tot["saving_year1"])],
            ["Year-1 saving as a share of spend", whole_pct(tot["saving_year1"], spend_total)],
            ["Saving from vendor action alone, with no group decision", money(tot["saving_without_decision"])],
            ["Vendor action alone as a share of spend", whole_pct(tot["saving_without_decision"], spend_total)],
            ["Value of the group decisions together (base minus vendor action alone)", money(tot["value"])],
            *outside_platform_rows(opp_lines, tot),
        ]),
        "",
        "## Opportunities",
        "",
        "Base is the run-rate saving the documents quote. Year 1 is the share of the base live in the first 12 months. "
        "\"Without the decision\" is what vendor action alone achieves; the value of the decision is the difference.",
        "",
        *table(["Opportunity", "Spend", "Low", "Base", "High", "Year 1", "Without the decision", "Value of the decision"],
               [row(name, k) for name, k in opp_lines] + [row("Total", tot)]),
        "",
        "## Decisions for the group",
        "",
        "For each decision only the group can take: the base saving of the moves that depend on it, what vendor action "
        "alone achieves without it, and the difference as the value of the decision.",
        "",
    ]
    values = decision_values(srows, decisions, levers)
    dec_lines = [(v["decision"], thousands(v["spend"]), thousands(v["with"]), thousands(v["without"]),
                  thousands(v["with"]) - thousands(v["without"]), thousands(v["year1"])) for v in values]
    lines += table(["Decision", "Spend", "With the decision", "Without it", "Value of the decision", "Year 1"],
                   [[f"`{d}`", money(s), money(w), money(wo), money(val), money(y)] for d, s, w, wo, val, y in dec_lines]
                   + [["Total", money(sum(x[1] for x in dec_lines)), money(sum(x[2] for x in dec_lines)),
                       money(sum(x[3] for x in dec_lines)), money(sum(x[4] for x in dec_lines)),
                       money(sum(x[5] for x in dec_lines))]])
    office = next((k for n, k in opp_lines if n == "Office exit"), None)
    back = next((k for n, k in opp_lines if n == "Back office into group shared services"), None)
    if office and back:
        two = office["value"] + back["value"]
        lines += ["", "## Cost of delay", "",
                  "The two decisions the memo asks for, valued as in the Opportunities table (base minus without the "
                  "decision), and what each month of delay costs: one twelfth of their value together.", "",
                  *table(["Measure", "Figure"], [
                      ["Value of the remote operating model (the Office exit line)", money(office["value"])],
                      ["Value of the group shared functions (the Back office line)", money(back["value"])],
                      ["The two decisions together", money(two)],
                      ["Cost of each month of delay, one twelfth of the two together", money(thousands(two / 12))],
                  ])]
    lines += ["", "## Calculations that reproduce", "",
              "For the three opportunities the Top 3 presents: each saving line's spend to the dollar, its base rate, and "
              "its saving as spend times rate rounded to the dollar, so that the Top 3 can state every calculation and a "
              "reader can reproduce it. An opportunity with more than four lines names its three largest and groups the "
              "rest in one row. Each Total is the sum of the rounded rows above it, and the rounded figure is the one the "
              "Opportunities table shows.", ""]
    for n, opp in enumerate(OPPORTUNITIES[:3]):
        lines += ([""] if n else []) + calculation_table(srows, opp)
    lines += ["", "## Office exit check", "",
              "A cross-check of the office assumption from the rows (steps 11 and 12): what closing every site except "
              "Zagreb, with its lease untouched, would save on the Office footprint line, against the 75% the base case "
              "applies evenly to every lease row while keeping the Zagreb hub space, right-sized at the next break.", "",
              *office_check_table(srows)]
    lines += ["", "## People-linked spend not counted", "",
              "Vendor spend that moves only with the workforce plan, which this review does not count: health and life "
              "cover, statutory cover and benefit schemes, employer-of-record pay and student labor. Each line's rows, spend, "
              "the small saving the model does count on it (the insurers' rate, the employer-of-record fee) and the rest, in "
              "whole dollars; the Total is the sum of the rows, and the rounded figure is the one the Top 3 and the insights "
              "quote.", "",
              *people_linked_table(srows)]
    falls = [(name, thousands(by_lever[name]["spend"]), by_lever[name]["rows"]) for name in FALLS_AWAY_LEVERS if name in by_lever]
    lines += ["", "## Spend that falls away without action", "",
              "Deal and one-off costs that end on their own; they carry no saving in the model.", "",
              *table(["Spend", "Rows", "Figure"], [[n, r, money(s)] for n, s, r in falls]
                     + [["Total", sum(r for _, _, r in falls), money(sum(s for _, s, _ in falls))]])]
    keep = []
    for label, vids in MUST_NOT_CUT:
        sel = [by_id[v] for v in vids]
        keep.append((label, len(sel), thousands(math.fsum(to_float(r["spend_12m"]) for r in sel))))
    lines += ["", "## Spend that must not be cut", "",
              "Payees that customers, regulators or employment terms require, or whose fee is contingent on cash recovered.", "",
              *table(["Spend", "Rows", "Figure"], [[n, r, money(s)] for n, r, s in keep]
                     + [["Total", sum(r for _, r, _ in keep), money(sum(s for _, _, s in keep))]])]
    verified = [r for r in rows if r["verified"] == "TRUE"]
    unverified = [r for r in rows if r["verified"] != "TRUE"]
    v_spend = thousands(math.fsum(to_float(r["spend_12m"]) for r in verified))
    u_spend = thousands(math.fsum(to_float(r["spend_12m"]) for r in unverified))
    lines += ["", "## Verification", "",
              *table(["Measure", "Figure"], [
                  ["Rows verified online, from the vendor's own site or a reliable directory", f"{len(verified)} of {len(rows)}"],
                  ["Spend verified online", f"{money(v_spend)} ({whole_pct(v_spend, spend_total)})"],
                  ["Rows left unconfirmed", f"{len(unverified)} ({money(u_spend)})"],
              ])]
    if REVIEW_CSV.exists():
        review = check_outputs.read_csv(REVIEW_CSV)
        stage1 = {r["vendor_id"] for r in review if r["stage"] == "1"}
        stage2 = {r["vendor_id"] for r in review if r["stage"] == "2"}
        changed = {r["vendor_id"] for r in review if r["verdict"] == "changed"}
        disagreed = {r["vendor_id"] for r in review if r["stage"] == "2" and r["verdict"] == "changed"
                     and r["field"] in ("department", "cost_cluster", "recommendation", "sub_function")}
        s2_spend = thousands(math.fsum(to_float(by_id[v]["spend_12m"]) for v in stage2 if v in by_id))
        agreement = whole_pct(len(stage2) - len(disagreed), len(stage2)) if stage2 else "n/a"
        lines += ["", "## Second-pass review", "",
                  "Stage 1: an independent read of every row against its research finding and the rules, without the web. "
                  "Stage 2: fresh web verification, with neither the hint nor the first-pass row, of every flagged row, "
                  "every row at or above $10,000 and a random sample.", "",
                  *table(["Measure", "Figure"], [
                      ["Stage 1 rows reviewed", f"{len(rows)} of {len(rows)}"],
                      ["Stage 1 rows flagged", f"{len(stage1)}"],
                      ["Stage 2 rows verified fresh", f"{len(stage2)} of {len(rows)}"],
                      ["Stage 2 spend covered", f"{money(s2_spend)} ({whole_pct(s2_spend, spend_total)})"],
                      ["Stage 2 rows whose reading changed (department, function, group or recommendation)", f"{len(disagreed)}"],
                      ["Stage 2 agreement with the first pass", agreement],
                      ["Rows changed by the review, any field", f"{len(changed)}"],
                  ])]
    return "\n".join(lines).rstrip("\n") + "\n"


def csv_text(srows: list[dict]) -> str:
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=SAVINGS_COLUMNS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(srows)
    return buf.getvalue()


def render(srows: list[dict], rows: list[dict], decisions: list[str], levers: dict[str, dict]) -> str:
    by_id = {r["vendor_id"]: r for r in rows}
    tot = totals(srows)
    by_lever = rollup(srows, "lever")
    recurring = [s for s in srows if by_id[s["vendor_id"]]["is_recurring"] == "TRUE"]
    non_recurring = [s for s in srows if by_id[s["vendor_id"]]["is_recurring"] == "FALSE"]
    addressable = [s for s in srows if by_id[s["vendor_id"]]["is_addressable"] == "TRUE"]
    modelled = [s for s in srows if levers[s["lever"]]["pct_base"] > 0]
    rec, nonrec, addr, mod = totals(recurring), totals(non_recurring), totals(addressable), totals(modelled)

    def share(x: float) -> str:
        return pct(x / tot["spend"]) if tot["spend"] else "n/a"

    lines = [
        "# Savings model",
        "",
        f"Written {dt.date.today().isoformat()} by `scripts/03_savings.py` from `{rel(CLASSIFIED)}` ({len(srows)} rows) and "
        f"the register `{rel(REGISTER)}` ({len(levers)} levers, {len(decisions)} acquirer decisions). Every figure is "
        "the row's 12-month spend times a percentage from the register; no spend figure is typed into the script. "
        f"Whole dollars here, full precision in `{rel(SAVINGS_CSV)}`. The costs are the file's modified values "
        "(`outputs/analysis/01_forensics.md`, section 3). A saving tagged with a decision is the value of that "
        "decision, not a fact about the parent (`docs/savings_assumptions.md`).",
        "",
        "## Totals",
        "",
        *table(["Measure", "Value"], [
            ["Vendor rows", f"{tot['rows']} ({len(by_lever)} levers in use)"],
            ["Total spend, 12 months", money(tot["spend"])],
            ["Recurring base (`is_recurring` TRUE)", f"{rec['rows']} rows, {money(rec['spend'])} ({share(rec['spend'])})"],
            ["Non-recurring spend (`is_recurring` FALSE)",
             f"{nonrec['rows']} rows, {money(nonrec['spend'])} ({share(nonrec['spend'])})"],
            ["Addressable spend (`is_addressable` TRUE)",
             f"{addr['rows']} rows, {money(addr['spend'])} ({share(addr['spend'])})"],
            ["Spend on levers with a base above 0%", f"{mod['rows']} rows, {money(mod['spend'])} ({share(mod['spend'])})"],
            ["Run-rate saving, low / base / high",
             f"{money(tot['saving_low'])} / {money(tot['saving_base'])} / {money(tot['saving_high'])}"],
            ["Base saving as a share of total spend", share(tot["saving_base"])],
            ["Saving without any acquirer decision (vendor action alone)",
             f"{money(tot['saving_without_decision'])} ({share(tot['saving_without_decision'])})"],
            ["Year-1 saving (base times each lever's year-1 factor)",
             f"{money(tot['saving_year1'])} ({share(tot['saving_year1'])})"],
        ]),
        "",
        "## Excluded spend by reason",
        "",
        "Every lever with a 0% base case, one line each. The spend stays in the file's total and out of the savings.",
        "",
    ]
    excluded = [(n, f) for n, f in levers.items() if f["pct_base"] == 0 and n in by_lever]
    lines += table(["Reason (lever)", "Opportunity", "Rows", "Spend", "Share of spend", "High case", "Why"],
                   [[n, f["opportunity"], by_lever[n]["rows"], money(by_lever[n]["spend"]), share(by_lever[n]["spend"]),
                     money(by_lever[n]["saving_high"]), f["reasoning"]] for n, f in excluded]
                   + [["Total", "", sum(by_lever[n]["rows"] for n, _ in excluded),
                       money(sum(by_lever[n]["spend"] for n, _ in excluded)),
                       share(sum(by_lever[n]["spend"] for n, _ in excluded)),
                       money(sum(by_lever[n]["saving_high"] for n, _ in excluded)), ""]])
    lines += ["", render_rollup_sections(srows, levers).rstrip("\n"), ""]

    lines += ["## Assumptions behind each lever", "",
              "The register, repeated next to the figures it produces. Percentages are of each row's 12-month spend; "
              "the year-1 factor is the share of the first 12 months in which the saving is live.", "",
              *table(["Lever", "Applies to", "Low / base / high", "Without decision", "Year-1 factor", "depends_on",
                      "Reasoning"],
                     [[n, f["applies_to"], f"{f['pct_low']:g}% / {f['pct_base']:g}% / {f['pct_high']:g}%",
                       f"{f['pct_without_decision']:g}%", f"{f['year1_factor']:g}", ", ".join(f["depends_on"]),
                       f["reasoning"]] for n, f in levers.items()]), ""]

    values = decision_values(srows, decisions, levers)
    lines += ["## Acquirer decisions", "",
              "For each decision: the base saving of the levers that depend on it, what vendor action alone achieves "
              "without it, and the difference as the value of the decision. A lever with no tag is in none of these rows.",
              "",
              *table(["Decision", "Levers", "Rows", "Spend", "Saving with the decision (base)", "Saving without it",
                      "Value of the decision", "Year 1 with the decision"],
                     [[f"`{v['decision']}`", "; ".join(v["levers"]) or "no lever", v["rows"], money(v["spend"]),
                       money(v["with"]), money(v["without"]), money(v["value"]), money(v["year1"])] for v in values]
                     + [["Total", "", sum(v["rows"] for v in values), money(sum(v["spend"] for v in values)),
                         money(sum(v["with"] for v in values)), money(sum(v["without"] for v in values)),
                         money(sum(v["value"] for v in values)), money(sum(v["year1"] for v in values))]]), ""]

    largest = sorted(srows, key=lambda s: (-to_float(s["saving_base"]), s["vendor_id"]))[:TOP_N]
    lines += [f"## Largest vendor savings", "", f"The {TOP_N} rows with the largest base saving.", "",
              *table(["vendor_id", "Vendor", "Cost cluster", "Lever", "Spend", "Low", "Base", "High", "Without decision",
                      "Year 1", "depends_on"],
                     [[s["vendor_id"], s["vendor_name_clean"], s["cost_cluster"], s["lever"], money(to_float(s["spend_12m"])),
                       *(money(to_float(s[c])) for c in SAVING_COLUMNS), s["depends_on"]] for s in largest]), ""]

    nr_by_lever = rollup(non_recurring, "lever")
    nr_names = sorted(nr_by_lever, key=lambda n: (-nr_by_lever[n]["saving_base"], n))
    nr_top = sorted((s for s in non_recurring if to_float(s["saving_base"]) > 0),
                    key=lambda s: (-to_float(s["saving_base"]), s["vendor_id"]))[:10]
    lines += ["## Savings on non-recurring rows", "",
              f"{nonrec['rows']} rows have `is_recurring` FALSE ({money(nonrec['spend'])}). A saving sits on them only in "
              "Travel and entertainment and Team events, perks and wellness, where the category recurs even when the "
              "payee does not; every other non-recurring row is in \"One-off spend that falls away\" at 0%.", "",
              *table(["Lever", "Non-recurring rows", "Spend", "Base saving", "Year 1"],
                     [[n, nr_by_lever[n]["rows"], money(nr_by_lever[n]["spend"]), money(nr_by_lever[n]["saving_base"]),
                       money(nr_by_lever[n]["saving_year1"])] for n in nr_names]
                     + [["Total", nonrec["rows"], money(nonrec["spend"]), money(nonrec["saving_base"]),
                         money(nonrec["saving_year1"])]]), ""]
    if nr_top:
        lines += ["The ten largest:", "",
                  *table(["vendor_id", "Vendor", "Lever", "Spend", "Base saving"],
                         [[s["vendor_id"], s["vendor_name_clean"], s["lever"], money(to_float(s["spend_12m"])),
                           money(to_float(s["saving_base"]))] for s in nr_top]), ""]

    recon, worst = reconciliation(srows)
    lines += ["## Reconciliation", "",
              f"The vendor rows sum to the levers, the clusters and the opportunities. Largest difference: ${worst:,.2f}.",
              "", *recon, ""]

    calls = [s for s in srows if s["vendor_id"] in ANALYST_CALLS]
    lines += ["## Lever assignments decided in this step", "",
              "Rows whose lever is an analyst call rather than a cluster rule or a row the register names "
              "(`docs/savings_assumptions.md`, \"Lever assignment\").", "",
              *table(["vendor_id", "Vendor", "Lever", "Why"],
                     [[s["vendor_id"], s["vendor_name_clean"], s["lever"], ANALYST_CALLS[s["vendor_id"]]] for s in calls]),
              ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def main() -> int:
    rows = check_outputs.read_csv(CLASSIFIED)
    register_text = REGISTER.read_text(encoding="utf-8")
    decisions, levers, problems = check_outputs.load_register(register_text)
    if problems:
        print(f"{rel(REGISTER)} does not load:")
        for p in problems:
            print(f"  {p}")
        return 1
    try:
        srows = build(rows, levers)
    except ValueError as e:
        print(f"no lever: {e}")
        return 1
    SAVINGS_CSV.parent.mkdir(parents=True, exist_ok=True)
    SAVINGS_CSV.write_text(csv_text(srows), encoding="utf-8")
    text = render(srows, rows, decisions, levers)
    write_text(SAVINGS_MD, text)
    write_text(SUMMARY_MD, render_summary(srows, rows, decisions, levers))
    tot = totals(srows)
    print(f"Wrote {rel(SUMMARY_MD)} and {rel(SAVINGS_CSV)} ({len(srows)} rows) and {rel(SAVINGS_MD)}: spend {money(tot['spend'])}, "
          f"run-rate saving {money(tot['saving_low'])} / {money(tot['saving_base'])} / {money(tot['saving_high'])}, "
          f"without decisions {money(tot['saving_without_decision'])}, year 1 {money(tot['saving_year1'])}.")
    res = check_outputs.Results()
    check_outputs.savings_checks(res, check_outputs.read_csv(SAVINGS_CSV), rows, register_text,
                                 SAVINGS_MD.read_text(encoding="utf-8"))
    res.show()
    failed = res.failed()
    print(f"{len(failed)} of {len(res.items)} savings checks failed" + (f": {', '.join(failed)}" if failed else ""))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
