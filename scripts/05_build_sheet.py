#!/usr/bin/env python3
"""Step 6 (prompt 19): the sheet workbook.

Copies the raw workbook to outputs/sheet/Vendor Analysis Assessment - Chaitanya Laxman.xlsx, never touching the raw
file (it is opened from a binary handle, read-only, and saved under the new name), keeps the Department dropdown, and
fills:
  Vendor Analysis Assessment  rows 2 to 387 in the original order: B department, D description, E recommendation,
                              and new headed columns F Rationale, G Key risk, H Estimated annual saving (USD, base
                              case), I Savings opportunity, J Verified online (Yes or No), K Source
  Top 3 Opportunities         titles in B, explanations in C, D headed "Estimated annual savings (USD)"
  Methodology                 the lines of outputs/methodology.md from row 2 down, one per row
  CEOCFO Recommendations      row 2 "Memo (Google Doc): [link to be added]", then the memo text, one line per row,
                              with the memo's table laid out across columns A to D

verify(path) reads the workbook back and confirms every cell against the source files, the row order against the raw
file, that every department is in the Config list, that the dropdown is still there, and that column H sums to the
base saving. qa/check_outputs.py runs it as check W1.

Usage:
    python scripts/05_build_sheet.py            build and verify
    python scripts/05_build_sheet.py --verify   verify only
"""
from __future__ import annotations

import copy
import csv
import math
import re
import sys
from pathlib import Path

from openpyxl.styles import Alignment
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vsa_common import CONFIG_SHEET, MAIN_SHEET, RAW_PATH, open_workbook, rel  # noqa: E402

OUT = ROOT / "outputs" / "sheet" / "Vendor Analysis Assessment - Chaitanya Laxman.xlsx"
CLASSIFIED = ROOT / "outputs" / "vendors_classified.csv"
SAVINGS = ROOT / "outputs" / "analysis" / "savings.csv"
TOP3 = ROOT / "outputs" / "top3_opportunities.md"
METHODOLOGY = ROOT / "outputs" / "methodology.md"
MEMO = ROOT / "outputs" / "memo.md"
TOP3_SHEET, METHOD_SHEET, MEMO_SHEET = "Top 3 Opportunities", "Methodology", "CEOCFO Recommendations"
NEW_HEADERS = {"F": "Rationale", "G": "Key risk", "H": "Estimated annual saving (USD, base case)",
               "I": "Savings opportunity", "J": "Verified online (Yes or No)", "K": "Source"}
WIDTHS = {"F": 60, "G": 45, "H": 18, "I": 32, "J": 14, "K": 50}
TOP3_HEADER = "Estimated annual savings (USD)"
MEMO_LINK = "Memo (Google Doc): [link to be added]"
FIRST_ROW, LAST_ROW = 2, 387


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def top3_entries(text: str) -> list[tuple[str, str, int]]:
    """(title, explanation, base saving in dollars) for each '## n. Title' section of top3_opportunities.md."""
    entries = []
    sections = re.split(r"^## \d+\. ", text, flags=re.M)[1:]
    for s in sections:
        lines = s.strip().splitlines()
        title = lines[0].strip()
        body = "\n".join(lines[1:]).strip()
        m = re.search(r"Estimated annual saving \(USD, base case\): \$([\d,]+)", body)
        if not m:
            raise SystemExit(f"no saving line in the Top 3 section {title!r}")
        explanation = body[:m.start()].strip().replace("\n", " ")
        entries.append((title, explanation, int(m.group(1).replace(",", ""))))
    if len(entries) != 3:
        raise SystemExit(f"the Top 3 file has {len(entries)} sections, not 3")
    return entries


def sheet_lines(text: str) -> list[str]:
    """A markdown document as one line per spreadsheet row: headings without their marks, list items without the
    bullet, blank lines dropped."""
    out = []
    for line in text.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        line = re.sub(r"^#+\s*", "", line)
        line = re.sub(r"^[-*]\s+", "", line)
        line = line.replace("**", "")
        out.append(line)
    return out


def memo_rows(text: str) -> list[list[str]]:
    """The memo as rows: a table line becomes its cells, any other line one cell."""
    rows = []
    for line in sheet_lines(text):
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells):
                continue
            rows.append(cells)
        else:
            rows.append([line])
    return rows


def sources() -> dict:
    rows = read_csv(CLASSIFIED)
    savings = {s["vendor_id"]: s for s in read_csv(SAVINGS)}
    if len(rows) != LAST_ROW - FIRST_ROW + 1:
        raise SystemExit(f"{rel(CLASSIFIED)} has {len(rows)} rows, expected {LAST_ROW - FIRST_ROW + 1}")
    return {"rows": rows, "savings": savings, "top3": top3_entries(TOP3.read_text(encoding="utf-8")),
            "method": sheet_lines(METHODOLOGY.read_text(encoding="utf-8")),
            "memo": memo_rows(MEMO.read_text(encoding="utf-8"))}


def vendor_cells(r: dict, s: dict) -> dict[str, object]:
    return {"B": r["department"], "D": r["description"], "E": r["recommendation"], "F": r["rationale"],
            "G": r["risk_note"], "H": float(s["saving_base"]), "I": s["opportunity"],
            "J": "Yes" if r["verified"] == "TRUE" else "No", "K": r["source_url"]}


def build(out: Path = OUT) -> Path:
    src = sources()
    wb = open_workbook(RAW_PATH)
    ws = wb[MAIN_SHEET]
    header_font, header_fill, header_align = copy.copy(ws["A1"].font), copy.copy(ws["A1"].fill), copy.copy(ws["A1"].alignment)
    for col, title in NEW_HEADERS.items():
        c = ws[f"{col}1"]
        c.value = title
        c.font, c.fill, c.alignment = copy.copy(header_font), copy.copy(header_fill), copy.copy(header_align)
        ws.column_dimensions[col].width = WIDTHS[col]
    for r in src["rows"]:
        n = int(r["vendor_id"][1:])
        if ws[f"A{n}"].value != r["vendor_name_original"]:
            raise SystemExit(f"row {n}: the raw name {ws[f'A{n}'].value!r} is not {r['vendor_name_original']!r}")
        for col, value in vendor_cells(r, src["savings"][r["vendor_id"]]).items():
            cell = ws[f"{col}{n}"]
            cell.value = value
            if col == "H":
                cell.number_format = "#,##0.00"
            elif col in ("D", "F", "G"):
                cell.alignment = Alignment(wrap_text=True, vertical="top")

    t = wb[TOP3_SHEET]
    t["D1"].value = TOP3_HEADER
    t["D1"].font, t["D1"].fill, t["D1"].alignment = copy.copy(t["B1"].font), copy.copy(t["B1"].fill), copy.copy(t["B1"].alignment)
    for i, (title, explanation, saving) in enumerate(src["top3"], start=2):
        t[f"B{i}"].value = title
        t[f"C{i}"].value = explanation
        t[f"C{i}"].alignment = Alignment(wrap_text=True, vertical="top")
        t[f"D{i}"].value = saving
        t[f"D{i}"].number_format = "#,##0"
    t.column_dimensions["B"].width = 55
    t.column_dimensions["C"].width = 110
    t.column_dimensions["D"].width = 24

    m = wb[METHOD_SHEET]
    for i, line in enumerate(src["method"], start=2):
        m[f"A{i}"].value = line
    m.column_dimensions["A"].width = 120

    c = wb[MEMO_SHEET]
    c["A2"].value = MEMO_LINK
    for i, cells in enumerate(src["memo"], start=3):
        for j, value in enumerate(cells, start=1):
            if value != "":
                c.cell(row=i, column=j).value = value
    c.column_dimensions["A"].width = 110
    for col in ("B", "C", "D"):
        c.column_dimensions[col].width = 22

    out.parent.mkdir(parents=True, exist_ok=True)
    wb.save(out)
    return out


def verify(path: Path = OUT) -> list[str]:
    """Problems found reading the workbook back against its sources; an empty list means it matches."""
    problems: list[str] = []
    if not path.exists():
        return [f"{rel(path)} does not exist"]
    src = sources()
    wb = open_workbook(path)
    raw = open_workbook(RAW_PATH)
    ws, raw_ws = wb[MAIN_SHEET], raw[MAIN_SHEET]
    config = {raw[CONFIG_SHEET][f"A{i}"].value for i in range(2, raw[CONFIG_SHEET].max_row + 1)} - {None}
    for col, title in NEW_HEADERS.items():
        if ws[f"{col}1"].value != title:
            problems.append(f"header {col}1 is {ws[f'{col}1'].value!r}")
    for col in "ABCDE":
        if ws[f"{col}1"].value != raw_ws[f"{col}1"].value:
            problems.append(f"header {col}1 changed")
    total_h = []
    for r in src["rows"]:
        n = int(r["vendor_id"][1:])
        cost, raw_cost = ws[f"C{n}"].value, raw_ws[f"C{n}"].value
        if ws[f"A{n}"].value != raw_ws[f"A{n}"].value or cost is None or raw_cost is None \
                or not math.isclose(float(cost), float(raw_cost), rel_tol=1e-12, abs_tol=1e-6):
            problems.append(f"row {n}: name or cost differs from the raw file")
        want = vendor_cells(r, src["savings"][r["vendor_id"]])
        for col, value in want.items():
            got = ws[f"{col}{n}"].value
            if col == "H":
                total_h.append(float(got) if got is not None else float("nan"))
                if got is None or abs(float(got) - value) > 0.005:
                    problems.append(f"row {n}: H is {got!r}, expected {value!r}")
            elif (got if got is not None else "") != value:
                problems.append(f"row {n}: {col} is {got!r}, expected {value!r}")
        if ws[f"B{n}"].value not in config:
            problems.append(f"row {n}: department {ws[f'B{n}'].value!r} is not in Config")
    for n in range(LAST_ROW + 1, raw_ws.max_row + 1):
        if any(ws[f"{col}{n}"].value is not None for col in "ABCDEFGHIJK"):
            problems.append(f"row {n}: a value below the last vendor row")
    base = math.fsum(float(s["saving_base"]) for s in src["savings"].values())
    if abs(math.fsum(total_h) - base) > 0.01:
        problems.append(f"column H sums to {math.fsum(total_h):,.2f}, not the base saving {base:,.2f}")
    dvs = [(str(dv.sqref), dv.formula1) for dv in ws.data_validations.dataValidation]
    if ("B2:B387", f"{CONFIG_SHEET}!$A$2:$A814") not in dvs:
        problems.append(f"the Department dropdown is missing: {dvs}")

    t = wb[TOP3_SHEET]
    if t["D1"].value != TOP3_HEADER:
        problems.append(f"Top 3 D1 is {t['D1'].value!r}")
    for i, (title, explanation, saving) in enumerate(src["top3"], start=2):
        if t[f"B{i}"].value != title or t[f"C{i}"].value != explanation or t[f"D{i}"].value != saving:
            problems.append(f"Top 3 row {i} differs from {rel(TOP3)}")
    m = wb[METHOD_SHEET]
    for i, line in enumerate(src["method"], start=2):
        if m[f"A{i}"].value != line:
            problems.append(f"Methodology row {i} differs from {rel(METHODOLOGY)}")
    if m[f"A{len(src['method']) + 2}"].value is not None:
        problems.append("Methodology has a row beyond the file's lines")
    c = wb[MEMO_SHEET]
    if c["A2"].value != MEMO_LINK:
        problems.append(f"CEOCFO A2 is {c['A2'].value!r}")
    for i, cells in enumerate(src["memo"], start=3):
        got = [c.cell(row=i, column=j).value or "" for j in range(1, len(cells) + 1)]
        if got != cells:
            problems.append(f"CEOCFO row {i} differs from {rel(MEMO)}")
    if c[f"A{len(src['memo']) + 3}"].value is not None:
        problems.append("CEOCFO has a row beyond the memo's lines")
    return problems


def main(argv: list[str]) -> int:
    if "--verify" not in argv:
        out = build()
        print(f"Wrote {rel(out)} from {rel(RAW_PATH)}: vendor rows {FIRST_ROW} to {LAST_ROW} filled in columns B, D to K; "
              f"Top 3, Methodology and CEOCFO Recommendations tabs filled.")
    problems = verify()
    if problems:
        print(f"VERIFY FAILED: {len(problems)} problems")
        for p in problems[:20]:
            print(f"  {p}")
        return 1
    print(f"Verified {rel(OUT)}: every cell matches its source, the raw order and the Config list hold, the dropdown is "
          "kept, and column H sums to the base saving.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
