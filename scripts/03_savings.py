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
(scripts/savings_model.py). After writing, the savings checks V1 to V8 of qa/check_outputs.py run on the files
just written. Exit code 1 if the register does not load, a row has no lever, or a check fails.

Usage:
    python scripts/03_savings.py
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "qa"))
import check_outputs  # noqa: E402
from savings_model import (  # noqa: E402
    ANALYST_CALLS, MONEY_COLUMNS, OPPORTUNITIES, PCT_COLUMNS, REGISTER, SAVING_COLUMNS, SAVINGS_COLUMNS, build,
    decision_values, reconciliation, render_rollup_sections, rollup, to_float, totals,
)
from vsa_common import money, pct, rel, table, write_text  # noqa: E402

CLASSIFIED = check_outputs.CLASSIFIED
SAVINGS_CSV = ROOT / "outputs" / "analysis" / "savings.csv"
SAVINGS_MD = ROOT / "outputs" / "analysis" / "savings.md"
TOP_N = 15


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
    tot = totals(srows)
    print(f"Wrote {rel(SAVINGS_CSV)} ({len(srows)} rows) and {rel(SAVINGS_MD)}: spend {money(tot['spend'])}, "
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
