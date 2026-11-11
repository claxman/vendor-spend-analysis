#!/usr/bin/env python3
"""Step 6 (prompt 19), tightened in step 7 (prompt 20): outputs/memo.docx from outputs/memo.md, the same text in a Word
file that fits one US Letter page.

US Letter, 0.75 inch margins, Calibri 10.5 point, single spacing with 2 points after each paragraph and no blank
lines; To, From and Date on one line and the Subject on the next (as in memo.md); the memo's table as a real table
with fixed column widths of 3.4, 1.0, 1.0 and 1.6 inches, set in the table grid and in every cell, 9.5-point cells,
so that every row fits on one line. Prints the word count outside the table, which the memo keeps at or under 360
(exit code 1 above it). qa/memo_page_check.py renders the file to PDF and confirms the page count.

Usage:
    python scripts/06_build_memo_docx.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vsa_common import rel  # noqa: E402

MEMO_MD = ROOT / "outputs" / "memo.md"
MEMO_DOCX = ROOT / "outputs" / "memo.docx"
WORD_LIMIT = 360
PAGE_WIDTH, PAGE_HEIGHT, MARGIN = Inches(8.5), Inches(11), Inches(0.75)
COLUMN_WIDTHS = [Inches(3.4), Inches(1.0), Inches(1.0), Inches(1.6)]   # 7.0 inches, the text width
BODY_PT, TABLE_PT, TITLE_PT = 10.5, 9.5, 12
SPACE_AFTER = Pt(2)
FONT = "Calibri"


def words_outside_table(text: str) -> int:
    body = "\n".join(line for line in text.splitlines() if not line.startswith("|"))
    body = body.replace("**", "").replace("#", "")
    return len(body.split())


def tight(paragraph, space_before=Pt(0)) -> None:
    """Single spacing, 2 points after, nothing before (the rule of step 7)."""
    pf = paragraph.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = space_before, SPACE_AFTER, 1.0


def add_runs(paragraph, text: str, size: float = BODY_PT) -> None:
    """Markdown bold (**...**) as bold runs."""
    for part in re.split(r"(\*\*[^*]+\*\*)", text):
        if not part:
            continue
        run = paragraph.add_run(part[2:-2] if part.startswith("**") else part)
        run.bold = part.startswith("**")
        run.font.name, run.font.size = FONT, Pt(size)


def fixed_widths(table) -> None:
    """The column widths in the table grid (w:gridCol), in every cell (w:tcW) and as a fixed layout, so that Word
    keeps them."""
    table.autofit = False
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    table._tbl.tblPr.append(layout)
    for col, width in zip(table.columns, COLUMN_WIDTHS):
        col.width = width
    for row in table.rows:
        for cell, width in zip(row.cells, COLUMN_WIDTHS):
            cell.width = width


def add_table(doc, table_lines: list[list[str]]) -> None:
    table = doc.add_table(rows=len(table_lines), cols=len(table_lines[0]))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r, cells in enumerate(table_lines):
        for c, value in enumerate(cells):
            cell = table.cell(r, c)
            cell.text = ""
            p = cell.paragraphs[0]
            tight(p)
            run = p.add_run(value.replace("**", ""))
            run.font.name, run.font.size = FONT, Pt(TABLE_PT)
            run.bold = r == 0 or cells[0].lower() == "total"
    fixed_widths(table)


def build() -> int:
    text = MEMO_MD.read_text(encoding="utf-8")
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = PAGE_WIDTH, PAGE_HEIGHT
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, MARGIN)
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = FONT, Pt(BODY_PT)
    tight(normal)

    lines = text.splitlines()
    i, after_table = 0, False
    while i < len(lines):
        line = lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    table_lines.append(cells)
                i += 1
            add_table(doc, table_lines)
            after_table = True
            continue
        if line.startswith("#"):
            p = doc.add_paragraph()
            run = p.add_run(line.lstrip("#").strip())
            run.bold, run.font.name, run.font.size = True, FONT, Pt(TITLE_PT if line.startswith("# ") else BODY_PT)
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, line[2:])
        else:
            p = doc.add_paragraph()
            add_runs(p, line)
        tight(p, SPACE_AFTER if after_table else Pt(0))   # a little air under the table, no blank line
        after_table = False
        i += 1
    doc.save(MEMO_DOCX)
    n = words_outside_table(text)
    print(f"Wrote {rel(MEMO_DOCX)} from {rel(MEMO_MD)}: {n} words outside the table (limit {WORD_LIMIT}); US Letter, "
          f"0.75 inch margins, {BODY_PT} point, columns of 3.4, 1.0, 1.0 and 1.6 inches.")
    return 0 if n <= WORD_LIMIT else 1


if __name__ == "__main__":
    sys.exit(build())
