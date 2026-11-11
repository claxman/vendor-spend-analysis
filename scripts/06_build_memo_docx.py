#!/usr/bin/env python3
"""Step 6 (prompt 19): outputs/memo.docx from outputs/memo.md, the same text in a Word file.

US Letter, 0.75 inch margins, 10.5 point text, the memo's table as a real table. Prints the word count outside the
table, which the memo keeps at or under 430.

Usage:
    python scripts/06_build_memo_docx.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Inches, Pt

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vsa_common import rel  # noqa: E402

MEMO_MD = ROOT / "outputs" / "memo.md"
MEMO_DOCX = ROOT / "outputs" / "memo.docx"
WORD_LIMIT = 430


def words_outside_table(text: str) -> int:
    body = "\n".join(line for line in text.splitlines() if not line.startswith("|"))
    body = body.replace("**", "").replace("#", "")
    return len(body.split())


def add_runs(paragraph, text: str) -> None:
    """Markdown bold (**...**) as bold runs."""
    for i, part in enumerate(re.split(r"(\*\*[^*]+\*\*)", text)):
        if not part:
            continue
        run = paragraph.add_run(part[2:-2] if part.startswith("**") else part)
        run.bold = part.startswith("**")
        run.font.size = Pt(10.5)


def build() -> int:
    text = MEMO_MD.read_text(encoding="utf-8")
    doc = Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(section, side, Inches(0.75))
    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = "Calibri", Pt(10.5)
    normal.paragraph_format.space_after = Pt(4)

    lines = text.splitlines()
    i = 0
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
            table = doc.add_table(rows=len(table_lines), cols=len(table_lines[0]))
            table.style = "Table Grid"
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            for r, cells in enumerate(table_lines):
                for c, value in enumerate(cells):
                    cell = table.cell(r, c)
                    cell.text = ""
                    p = cell.paragraphs[0]
                    run = p.add_run(value.replace("**", ""))
                    run.font.size = Pt(9.5)
                    run.bold = r == 0 or cells[0].lower() == "total"
            doc.add_paragraph()
            continue
        if line.startswith("#"):
            p = doc.add_paragraph()
            run = p.add_run(line.lstrip("#").strip())
            run.bold, run.font.size = True, Pt(12 if line.startswith("# ") else 10.5)
        elif line.startswith("- "):
            p = doc.add_paragraph(style="List Bullet")
            add_runs(p, line[2:])
        else:
            p = doc.add_paragraph()
            add_runs(p, line)
        i += 1
    doc.save(MEMO_DOCX)
    n = words_outside_table(text)
    print(f"Wrote {rel(MEMO_DOCX)} from {rel(MEMO_MD)}: {n} words outside the table (limit {WORD_LIMIT}).")
    return 0 if n <= WORD_LIMIT else 1


if __name__ == "__main__":
    sys.exit(build())
