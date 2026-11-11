#!/usr/bin/env python3
"""Merge the classification batches into outputs/vendors_classified.csv, run the QA checks and write
qa/validation_report.md.

Inputs
  outputs/batches/batch_NN.csv     one CSV per batch of 40 vendors, numbered from 01 without gaps, with exactly
                                   the 16 columns of the classification spec, in its order (docs/decisions.md,
                                   step 2e). Batches may hold any vendors, and rows may come in any order.
  qa/verification_exceptions.csv   columns vendor_id and reason: a one-line reason for every row whose verified
                                   is FALSE. The verification step keeps it, because the batches have no column
                                   for the reason and the report is rebuilt on every run.
Outputs
  outputs/vendors_classified.csv   every batch row in the 16 columns, sorted by vendor_id, which is the original
                                   sheet order (step 2d-fix3), whatever order the batches came in
  qa/validation_report.md          counts; distributions by department, recommendation, cost cluster and
                                   confidence; the low-confidence vendors sorted by spend; the "Verification
                                   exceptions" section; every check, and every failure with its full detail

Order of work. The merge checks M1 to M7 run on the batches and the reasons file. The merged file is written
whatever they find, so that one run reports every failure. The report is written first with its "Verification
exceptions" section, because check C17 reads that section; qa/check_outputs.py then runs on both files, and the
report is written again with the results. The section is the same text both times.

Usage:
    python scripts/merge_validate.py              merge the real batches and validate them
    python scripts/merge_validate.py --self-test  merge synthetic batches in a temporary directory, first clean
                                                  and then with planted errors, to show each check catches its error
Exit code 1 if any check fails, or if there is no batch file (then nothing is written).
"""
from __future__ import annotations

import copy
import csv
import io
import math
import random
import re
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "qa"))
import check_outputs  # noqa: E402
from vsa_common import EM_DASH, EN_DASH, money, pct, rel, section_rows, table, write_text  # noqa: E402

BATCH_DIR = ROOT / "outputs" / "batches"
REASONS = ROOT / "qa" / "verification_exceptions.csv"
COLUMNS = check_outputs.REQUIRED_COLUMNS
VENDOR_ID = check_outputs.VENDOR_ID
BATCH_SIZE = 40
BATCH_NAME = re.compile(r"batch_(\d{2})\.csv")
REASON_COLUMNS = ["vendor_id", "reason"]
RECOMMENDATION_ORDER = ["Terminate", "Consolidate", "Optimize"]
CONFIDENCE_ORDER = ["high", "medium", "low"]
REPORT_SECTIONS = ["Counts", "Distribution by department", "Distribution by recommendation",
                   "Distribution by cost cluster", "Distribution by confidence", "Low-confidence vendors",
                   check_outputs.EXCEPTIONS_HEADING, "Checks", "Failures"]

MERGE_CHECKS = {
    "M1": "Batch files are named batch_NN.csv and numbered from 01 without gaps",
    "M2": f"Every batch has exactly the {len(COLUMNS)} columns of the classification spec, in its order",
    "M3": f"Every batch holds at most {BATCH_SIZE} vendors, and every batch but the last exactly {BATCH_SIZE}",
    "M4": "Every row has as many fields as its batch's header",
    "M5": "No vendor_id appears more than once across the batches",
    "M6": "spend_12m is a finite number in every row",
    "M7": "The verification reasons file has the columns vendor_id and reason, lists each vendor_id once, and each "
          "reason is one line without em or en dashes",
}


# ---------------------------------------------------------------- reading and merging

def parse_spend(text) -> float | None:
    try:
        x = float(text)
    except (TypeError, ValueError):
        return None
    return x if math.isfinite(x) else None


def spend(row: dict) -> float:
    return parse_spend(row["spend_12m"]) or 0.0


def id_key(vid: str) -> tuple:
    """Sort key: well-formed vendor_ids by number, which is the sheet order; anything else after them."""
    return (0, int(vid[1:]), "") if VENDOR_ID.fullmatch(vid) else (1, 0, vid)


def show(path: Path) -> str:
    """A path as the report shows it: relative to the repository, or just the name outside it."""
    shown = rel(path)
    return path.name if Path(shown).is_absolute() else shown


def read_records(path: Path) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """The header and the non-blank records of a CSV, each with the line it ends on."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.reader(fh)
        header = next(reader, [])
        records = [(reader.line_num, rec) for rec in reader if any(cell.strip() for cell in rec)]
    return header, records


def read_reasons(path: Path, problems: list[str]) -> list[tuple[str, str]] | None:
    """(vendor_id, reason) in vendor_id order, or None when the file does not exist."""
    if not path.exists():
        return None
    header, records = read_records(path)
    if header != REASON_COLUMNS:
        problems.append(f"{show(path)}: the columns are {', '.join(header) or 'missing'}; expected vendor_id, reason")
    entries, seen = [], defaultdict(int)
    for line, rec in records:
        vid = rec[0].strip() if rec else ""
        reason = rec[1] if len(rec) > 1 else ""
        label = vid or f"line {line}"
        if len(rec) != len(REASON_COLUMNS):
            problems.append(f"line {line}: {len(rec)} fields for {len(REASON_COLUMNS)} columns")
        if not VENDOR_ID.fullmatch(vid):
            problems.append(f"line {line}: {vid!r} is not a vendor_id")
        if "\n" in reason or "\r" in reason:
            problems.append(f"{label}: the reason runs over more than one line")
        if EM_DASH in reason or EN_DASH in reason:
            problems.append(f"{label}: the reason contains an em or en dash")
        seen[vid] += 1
        entries.append((vid, " ".join(reason.split())))
    problems.extend(f"{vid}: listed {n} times" for vid, n in seen.items() if vid and n > 1)
    return sorted(entries, key=lambda e: id_key(e[0]))


def merge(batch_dir: Path, reasons_path: Path) -> dict:
    problems: dict[str, list[str]] = {cid: [] for cid in MERGE_CHECKS}
    numbered = []
    for path in sorted(batch_dir.glob("*.csv")):
        m = BATCH_NAME.fullmatch(path.name)
        if m and int(m.group(1)) >= 1:
            numbered.append((int(m.group(1)), path))
        else:
            problems["M1"].append(f"{path.name} is not named batch_NN.csv with NN from 01, so it was not merged")
    numbered.sort()
    numbers = {n for n, _ in numbered}
    gaps = [f"batch_{n:02d}.csv" for n in range(1, max(numbers, default=0) + 1) if n not in numbers]
    if gaps:
        problems["M1"].append(f"missing: {', '.join(gaps)}")

    rows, sizes = [], []
    places = defaultdict(list)
    for k, (_, path) in enumerate(numbered):
        header, records = read_records(path)
        if header != COLUMNS:
            missing = [c for c in COLUMNS if c not in header]
            extra = [c for c in header if c not in COLUMNS]
            repeated = sorted({c for c in header if header.count(c) > 1})
            what = ([f"missing {', '.join(missing)}"] if missing else []) \
                + ([f"unexpected {', '.join(extra)}"] if extra else []) \
                + ([f"repeated {', '.join(repeated)}"] if repeated else [])
            problems["M2"].append(f"{path.name}: {'; '.join(what) or 'the columns are in another order'}")
        batch_ids = []
        for line, rec in records:
            if len(rec) != len(header):
                problems["M4"].append(f"{path.name} line {line}: {len(rec)} fields for {len(header)} columns")
            fields = dict(zip(header, rec))       # by column name, so a column order slip cannot shift values
            row = {c: fields.get(c, "") for c in COLUMNS}
            places[row["vendor_id"]].append(f"{path.name} line {line}")
            if parse_spend(row["spend_12m"]) is None:
                problems["M6"].append(f"{row['vendor_id'] or path.name + ' line ' + str(line)}: {row['spend_12m']!r}")
            batch_ids.append(row["vendor_id"])
            rows.append(row)
        sizes.append((path.name, len(records), batch_ids))
        if len(records) > BATCH_SIZE or not records or (k < len(numbered) - 1 and len(records) != BATCH_SIZE):
            problems["M3"].append(f"{path.name}: {len(records)} vendors")
    problems["M5"] = [f"{vid or '(blank vendor_id)'} in {' and '.join(where)}"
                      for vid, where in places.items() if len(where) > 1]
    rows.sort(key=lambda r: id_key(r["vendor_id"]))   # stable: a duplicated id keeps its batch order
    reasons = read_reasons(reasons_path, problems["M7"])
    return {"batches": [path for _, path in numbered], "sizes": sizes, "rows": rows, "reasons": reasons,
            "reasons_path": reasons_path, "problems": problems}


def write_csv(path: Path, rows: list[dict]) -> None:
    """The rows in the columns of the spec. Written even when a field breaks a rule (an em dash, say), so that the
    QA checks report it; refusing to write would hide every other failure."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n", extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(buf.getvalue(), encoding="utf-8")


def merge_items(m: dict) -> list[tuple[str, str, str, str]]:
    """The merge checks in the same form as the QA results: (id, status, rule, detail)."""
    reasons = m["reasons"]
    passed = {
        "M1": f"{len(m['batches'])} batch files",
        "M2": "every header matches",
        "M3": "sizes " + ", ".join(str(n) for _, n, _ in m["sizes"]),
        "M4": "every row matches its header",
        "M5": f"{len(m['rows'])} rows, each vendor_id once",
        "M6": "every spend_12m is a number",
        "M7": (f"{show(m['reasons_path'])} does not exist, so no row is listed" if reasons is None
               else f"{len(reasons)} reasons in {show(m['reasons_path'])}"),
    }
    out = []
    for cid, rule in MERGE_CHECKS.items():
        found = m["problems"][cid]
        out.append((cid, "FAIL" if found else "PASS", rule, "; ".join(found) if found else passed[cid]))
    return out


# ---------------------------------------------------------------- report

def distribution(rows: list[dict], col: str, allowed: list[str], total: float, label: str) -> list[str]:
    by_value = defaultdict(list)
    for r in rows:
        by_value[r[col]].append(r)
    body = []
    for value in list(allowed) + sorted(v for v in by_value if v not in allowed):
        sel = by_value.get(value, [])
        s = math.fsum(spend(r) for r in sel)
        name = value if value in allowed else f"{value or '(blank)'} (not an allowed value)"
        body.append([name, len(sel), pct(len(sel) / len(rows)) if rows else "n/a", money(s),
                     pct(s / total) if total else "n/a"])
    body.append(["Total", len(rows), pct(1) if rows else "n/a", money(total), pct(1) if total else "n/a"])
    return table([label, "Vendors", "Share of vendors", "Spend", "Share of spend"], body)


def render(m: dict, clean: list[dict], paths: dict, items: list | None) -> str:
    """The validation report. `items` is None for the first write, before the QA checks have run."""
    rows = m["rows"]
    total = math.fsum(spend(r) for r in rows)
    clean_total = math.fsum(float(c["cost_usd"]) for c in clean)
    ids = {r["vendor_id"] for r in rows}

    def share(sel: list[dict]) -> str:
        s = math.fsum(spend(r) for r in sel)
        return f"{len(sel)} vendors, {money(s)}" + (f" ({pct(s / total)} of spend)" if total else "")

    def where(col: str, value: str) -> str:
        return share([r for r in rows if r[col] == value])

    batches, reasons_file = m["batches"], show(paths["reasons"])
    lines = [
        "# Validation report",
        "",
        f"Written by `scripts/merge_validate.py`, which merged the batch files in `{show(paths['batches'])}/` into "
        f"`{show(paths['out'])}`, sorted by `vendor_id` (the original sheet order), and ran `qa/check_outputs.py` on "
        "it. The report is rebuilt on every run and is not edited by hand: the reason for a row with `verified` "
        f"FALSE goes in `{reasons_file}`.",
        "",
    ]
    if items is None:
        lines += ["QA checks not run yet.", ""]
    else:
        failed = [i[0] for i in items if i[1] == "FAIL"]
        lines += [f"**Result: FAIL.** {len(failed)} of {len(items)} checks failed: {', '.join(failed)}." if failed
                  else f"**Result: PASS.** All {len(items)} checks passed.", ""]

    counts = [
        ["Batch files merged", f"{len(batches)}" + (f" ({batches[0].name} to {batches[-1].name})" if batches else "")],
        ["Rows in the batches", len(rows)],
        ["Distinct vendor_ids", len(ids)],
        [f"Source rows in `{show(check_outputs.CLEAN)}`", len(clean)],
        ["Source rows in no batch", sum(1 for c in clean if c["vendor_id"] not in ids)],
        ["Total `spend_12m`", f"{money(total)} (source total {money(clean_total)})"],
        ["`verified` TRUE", where("verified", "TRUE")],
        ["`verified` FALSE", where("verified", "FALSE")],
        ["`is_addressable` TRUE", where("is_addressable", "TRUE")],
        ["`is_recurring` TRUE", where("is_recurring", "TRUE")],
        ["Confidence low", where("confidence", "low")],
    ]
    per_batch = []
    for name, n, batch_ids in m["sizes"]:
        ordered = sorted(batch_ids, key=id_key)
        per_batch.append([name, n, ordered[0] if ordered else "", ordered[-1] if ordered else ""])
    lines += ["## Counts", "", *table(["Measure", "Value"], counts), "", "Rows per batch:", "",
              *table(["Batch", "Rows", "Lowest vendor_id", "Highest vendor_id"], per_batch), ""]

    departments = [r[1] for r in section_rows(check_outputs.TAXONOMY.read_text(encoding="utf-8"), "Departments")]
    clusters = [r[1] for r in section_rows(check_outputs.CLUSTERS.read_text(encoding="utf-8"), "Clusters")]
    for heading, col, allowed in [("department", "department", departments),
                                  ("recommendation", "recommendation", RECOMMENDATION_ORDER),
                                  ("cost cluster", "cost_cluster", clusters),
                                  ("confidence", "confidence", CONFIDENCE_ORDER)]:
        lines += [f"## Distribution by {heading}", "",
                  *distribution(rows, col, allowed, total, heading[0].upper() + heading[1:]), ""]

    low = sorted((r for r in rows if r["confidence"] == "low"), key=lambda r: (-spend(r), id_key(r["vendor_id"])))
    lines += ["## Low-confidence vendors", ""]
    if low:
        lines += [f"{share(low)}, sorted by spend, largest first.", "",
                  *table(["vendor_id", "Vendor", "Spend", "Department", "Recommendation", "Description"],
                         [[r["vendor_id"], r["vendor_name_clean"], money(spend(r)), r["department"],
                           r["recommendation"], r["description"]] for r in low]), ""]
    else:
        lines += ["No vendor has low confidence.", ""]

    # C17 reads only this section: a line in it that carries a vendor_id lists that row. Nothing else here may
    # carry one, and the next section starts at the same heading level.
    lines += [f"## {check_outputs.EXCEPTIONS_HEADING}", "",
              f"Every row with `verified` FALSE, by `vendor_id`, with a one-line reason, as kept in `{reasons_file}`. "
              "Check C17 compares this list with the `verified` column, both ways.", ""]
    if m["reasons"] is None:
        lines += [f"No row is listed: `{reasons_file}` does not exist.", ""]
    elif not m["reasons"]:
        lines += [f"No row is listed: `{reasons_file}` has no entries.", ""]
    else:
        lines += [f"- {vid}: {reason}" for vid, reason in m["reasons"]] + [""]

    lines += ["## Checks", ""]
    if items is None:
        lines += ["Not run yet.", ""]
    else:
        lines += ["The merge checks M1 to M7 on the batches, then `qa/check_outputs.py` on the merged file: structural "
                  "checks S1 to S6, classification checks C1 to C18 and, once `outputs/analysis/savings.csv` exists, "
                  "the savings checks V1 to V8 on it (step 4).", "",
                  *table(["Check", "Result", "Rule"], [[cid, status, rule] for cid, status, rule, _ in items]), ""]
    lines += ["## Failures", ""]
    if items is None:
        lines += ["Not run yet.", ""]
    else:
        failed_items = [i for i in items if i[1] == "FAIL"]
        if not failed_items:
            lines += [f"None: all {len(items)} checks passed.", ""]
        for cid, _, rule, detail in failed_items:
            lines += [f"### {cid}: {rule}", ""]
            lines += ([f"- {p}" for p in m["problems"][cid]] if cid in m["problems"] else [detail]) + [""]
    text = "\n".join(lines).rstrip("\n") + "\n"
    # A batch may carry a dash (C9 reports it); the report itself never does.
    return text.replace(EM_DASH, "[em dash]").replace(EN_DASH, "[en dash]")


# ---------------------------------------------------------------- run

def merge_and_validate(paths: dict, quiet: bool = False) -> tuple[int, list]:
    say = (lambda *args: None) if quiet else print
    m = merge(paths["batches"], paths["reasons"])
    if not m["batches"]:
        say(f"No batch files in {show(paths['batches'])}: nothing merged, nothing written.")
        for problem in m["problems"]["M1"]:
            say(f"  {problem}")
        return 1, []
    write_csv(paths["out"], m["rows"])
    clean = check_outputs.read_csv(check_outputs.CLEAN)
    write_text(paths["report"], render(m, clean, paths, None))   # the section C17 reads
    check_outputs.FULL_DETAIL = True
    try:
        res = check_outputs.run(paths["out"], paths["report"], paths["savings"], paths["savings_report"])
    finally:
        check_outputs.FULL_DETAIL = False
    items = merge_items(m) + res.items
    write_text(paths["report"], render(m, clean, paths, items))
    failed = [cid for cid, status, _, _ in items if status == "FAIL"]
    say(f"Merged {len(m['batches'])} batch files ({len(m['rows'])} rows) into {show(paths['out'])}, sorted by vendor_id.")
    for cid, status, rule, _ in items:
        say(f"{status:7s} {cid:4s} {rule}")
    say(f"{len(failed)} of {len(items)} checks failed" + (f": {', '.join(failed)}" if failed else "")
        + f". Full details in {show(paths['report'])}.")
    return (1 if failed else 0), items


# ---------------------------------------------------------------- self-test

def case_paths(case: Path) -> dict:
    return {"batches": case / "batches", "reasons": case / "verification_exceptions.csv",
            "out": case / "vendors_classified.csv", "report": case / "validation_report.md",
            "savings": case / "savings.csv", "savings_report": case / "savings.md"}


def write_rows(path: Path, rows: list[list[str]]) -> None:
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerows(rows)
    path.write_text(buf.getvalue(), encoding="utf-8")


def write_batches(batch_dir: Path, rows: list[dict], seed: int) -> None:
    """Batches of 40 from the rows in shuffled order, so the merge has to sort."""
    shuffled = copy.deepcopy(rows)
    random.Random(seed).shuffle(shuffled)
    batch_dir.mkdir(parents=True)
    for k in range(0, len(shuffled), BATCH_SIZE):
        write_csv(batch_dir / f"batch_{k // BATCH_SIZE + 1:02d}.csv", shuffled[k:k + BATCH_SIZE])


def edit_batches(paths: dict, change) -> None:
    """Load every batch file as lists of fields, let `change` edit, add, rename or drop files, write them back."""
    files = {}
    for path in sorted(paths["batches"].glob("*.csv")):
        with open(path, encoding="utf-8", newline="") as fh:
            files[path.name] = list(csv.reader(fh))
        path.unlink()
    change(files)
    for name, data in files.items():
        write_rows(paths["batches"] / name, data)


def self_test() -> bool:
    clean = check_outputs.read_csv(check_outputs.CLEAN)
    base = check_outputs.synthetic(clean)          # follows every rule; three rows are verified FALSE
    unverified = check_outputs.SYNTHETIC_UNVERIFIED
    reasons = [(vid, "Synthetic reason: no public source confirms what this payee supplies.") for vid in unverified]
    col = COLUMNS.index
    all_ok = True

    def verdict(ok: bool, text: str) -> None:
        nonlocal all_ok
        all_ok &= ok
        print(f"{'PASS' if ok else 'FAIL'}    {text}")

    def rename_column(f):
        f["batch_03.csv"][0][col("spend_12m")] = "cost_usd"

    def swap_columns(f):
        for rec in f["batch_02.csv"]:
            rec[col("department")], rec[col("description")] = rec[col("description")], rec[col("department")]

    def move_row(f):
        f["batch_01.csv"].append(f["batch_10.csv"].pop(1))

    def drop_row(f):
        f["batch_04.csv"].pop(1)

    def copy_row(f):
        f["batch_10.csv"].append(list(f["batch_02.csv"][1]))

    def leave_gap(f):
        f["batch_11.csv"] = f.pop("batch_05.csv")

    def misname(f):
        f["batch_4.csv"] = f.pop("batch_04.csv")

    def extra_field(f):
        f["batch_06.csv"][3].append("an extra field")

    def bad_spend(f):
        f["batch_07.csv"][2][col("spend_12m")] = "n/a"

    def dash_in_description(f):
        f["batch_08.csv"][1][col("description")] = "Flexible offices " + EM_DASH + " London"

    def reason_for(vid: str, text: str) -> list[tuple[str, str]]:
        return [(v, text if v == vid else r) for v, r in reasons]

    # (title, change to the batch files, reasons file entries or None for no file, checks that must fail,
    #  True when no other check may fail)
    cases = [
        ("Column renamed in one batch (cost_usd for spend_12m)", rename_column, reasons, {"M2"}, False),
        ("Two columns swapped in one batch, header and values alike", swap_columns, reasons, {"M2"}, True),
        ("41 vendors in one batch", move_row, reasons, {"M3"}, True),
        ("A batch of 39 that is not the last", drop_row, reasons, {"M3"}, False),
        ("One vendor in two batches", copy_row, reasons, {"M5"}, False),
        ("Gap in the batch numbers", leave_gap, reasons, {"M1"}, False),
        ("Batch file not named batch_NN.csv", misname, reasons, {"M1"}, False),
        ("A row with one field too many", extra_field, reasons, {"M4"}, True),
        ("spend_12m that is not a number", bad_spend, reasons, {"M6"}, False),
        ("Em dash in a description", dash_in_description, reasons, {"C9"}, True),
        ("Unverified row with no reason in the reasons file", None, [e for e in reasons if e[0] != unverified[1]],
         {"C17"}, True),
        ("Reason given for a row that is verified", None,
         reasons + [("V0002", "Synthetic reason for a row that is verified.")], {"C17"}, True),
        ("Reasons file missing while rows are FALSE", None, None, {"C17"}, True),
        ("One vendor_id twice in the reasons file", None, reasons + [reasons[0]], {"M7"}, True),
        ("Reason over two lines", None, reason_for(unverified[2], "First line\nsecond line"), {"M7"}, True),
        ("Em dash in a reason", None, reason_for(unverified[2], "No source " + EM_DASH + " none found"), {"M7"}, True),
    ]

    with tempfile.TemporaryDirectory(prefix="merge_validate_") as tmp:
        tmp = Path(tmp)
        p = case_paths(tmp / "clean")
        write_batches(p["batches"], base, seed=1)
        write_rows(p["reasons"], [REASON_COLUMNS] + [list(e) for e in reasons])
        code, items = merge_and_validate(p, quiet=True)
        failed = [cid for cid, status, _, _ in items if status == "FAIL"]
        verdict(code == 0 and not failed, f"synthetic batches that follow every rule, shuffled: all {len(items)} "
                f"checks pass" + (f" (failing: {', '.join(failed)})" if failed else ""))
        merged_ids = [r["vendor_id"] for r in check_outputs.read_csv(p["out"])]
        verdict(merged_ids == [c["vendor_id"] for c in clean],
                f"the merged file holds the {len(clean)} rows in vendor_id order, the original sheet order")
        text = p["report"].read_text(encoding="utf-8")
        missing = [s for s in REPORT_SECTIONS if f"\n## {s}\n" not in text]
        verdict(not missing, f"the report has its {len(REPORT_SECTIONS)} sections"
                + (f" (missing: {', '.join(missing)})" if missing else ""))
        listed, problems = check_outputs.verification_exceptions(text)
        verdict(sorted(listed) == unverified and not problems,
                f"the report lists {', '.join(unverified)} under \"{check_outputs.EXCEPTIONS_HEADING}\", each with "
                "its reason")
        section = text.split("\n## Low-confidence vendors\n")[1].split("\n## ")[0]
        low_ids = [ln.split("|")[1].strip() for ln in section.splitlines() if ln.startswith("| V")]
        want_low = sorted((r for r in base if r["confidence"] == "low"),
                          key=lambda r: (-float(r["spend_12m"]), id_key(r["vendor_id"])))
        verdict(low_ids == [r["vendor_id"] for r in want_low],
                f"the low-confidence list holds the {len(want_low)} low-confidence rows, largest spend first")
        rerun = check_outputs.run(p["out"], p["report"], p["savings"], p["savings_report"])
        verdict([i[:2] for i in rerun.items] == [i[:2] for i in items if not i[0].startswith("M")],
                "qa/check_outputs.py run again on the files as written gives the same results")
        first = (p["out"].read_bytes(), p["report"].read_bytes())
        code, _ = merge_and_validate(p, quiet=True)
        verdict(code == 0 and (p["out"].read_bytes(), p["report"].read_bytes()) == first,
                "a second run on the same batches gives byte-identical files")
        shutil.rmtree(p["batches"])
        write_batches(p["batches"], base, seed=2)
        code, _ = merge_and_validate(p, quiet=True)
        verdict(code == 0 and p["out"].read_bytes() == first[0],
                "the same rows shuffled into other batches give a byte-identical merged file")

        p = case_paths(tmp / "empty")
        p["batches"].mkdir(parents=True)
        code, _ = merge_and_validate(p, quiet=True)
        verdict(code == 1 and not p["out"].exists() and not p["report"].exists(),
                "no batch files: nothing is written, and the exit code is 1")

        for n, (title, change, case_reasons, must_fail, alone) in enumerate(cases, 1):
            p = case_paths(tmp / f"case{n:02d}")
            write_batches(p["batches"], base, seed=n)
            if case_reasons is not None:
                write_rows(p["reasons"], [REASON_COLUMNS] + [list(e) for e in case_reasons])
            if change:
                edit_batches(p, change)
            code, items = merge_and_validate(p, quiet=True)
            failed = [cid for cid, status, _, _ in items if status == "FAIL"]
            text = p["report"].read_text(encoding="utf-8") if p["report"].exists() else ""
            caught = (code == 1 and must_fail <= set(failed) and (not alone or set(failed) == must_fail)
                      and bool(text) and EM_DASH not in text and EN_DASH not in text)
            all_ok &= caught
            print(f"{'PASS' if caught else 'FAIL'}    planted error caught by {', '.join(sorted(must_fail))}"
                  f"{' alone' if alone else ''}: {title} (checks failing: {', '.join(failed) or 'none'})")
    print(f"self-test {'passed' if all_ok else 'FAILED'}: clean run plus {len(cases)} planted errors")
    return all_ok


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return 0 if self_test() else 1
    code, _ = merge_and_validate({"batches": BATCH_DIR, "reasons": REASONS, "out": check_outputs.CLASSIFIED,
                                  "report": check_outputs.VALIDATION_REPORT, "savings": check_outputs.SAVINGS_CSV,
                                  "savings_report": check_outputs.SAVINGS_MD})
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv))
