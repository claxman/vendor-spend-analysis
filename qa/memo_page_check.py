#!/usr/bin/env python3
"""Step 7 (prompt 20): render outputs/memo.docx to outputs/memo.pdf and confirm that it fits one US Letter page with
lines to spare.

This machine has no LibreOffice, pandoc or PDF library, and its Microsoft Word refuses the AppleScript "save as"
command (error -1708 for every format), so the check uses what does work here:
  1. The open command (Launch Services) puts the Word file in Pages, starting Pages if needed, and AppleScript through
     osascript has Pages export the document as PDF. The PDF embeds Calibri and Calibri Bold, the memo's fonts.
     (Pages' own AppleScript open command worked in step 7 but not in step 8: it answered "can't be opened right now,
     Pages couldn't read the file", one alert per try, and every later event timed out behind the alerts.)
  2. macOS PDFKit, through osascript's JavaScript, reads the PDF back: the page count, the position of every
     character, hence the number of text lines and the lowest line on the page, and whether the header line and
     each table row sit on one line. The lines to spare are the space between the lowest line and the bottom
     margin, divided by the height of a body line.
The page count is also counted a second time from the PDF's own page objects. The result goes to
qa/memo_page_check.md.

Exit codes: 0 when the memo is one page with at least eight lines to spare and every measured line is one line;
1 otherwise; 2 when nothing on this machine can render it (the check then says so and changes nothing).

Usage:
    python qa/memo_page_check.py [path/to/memo.docx]
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from vsa_common import rel  # noqa: E402

MEMO_DOCX = ROOT / "outputs" / "memo.docx"
MEMO_PDF = ROOT / "outputs" / "memo.pdf"
REPORT = ROOT / "qa" / "memo_page_check.md"
PAGES_APP = Path("/Applications/Pages.app")
LINES_REQUIRED = 8
PAGE_HEIGHT_PT, PAGE_WIDTH_PT = 11 * 72, 8.5 * 72
BOTTOM_MARGIN_PT = 0.75 * 72
BODY_LINE_PT = 10.5 * 1.22 + 2   # a Calibri 10.5-point line with the memo's 2 points after
# The header line is one line when both its ends sit at the same height.
HEADER_TEXTS = ["To: group CEO and CFO", "Date: November 11, 2026"]
# The table rows are anchored on their amounts, which are unique and free of the ligatures PDFKit returns for "ti"
# and "ffi" in the labels. Consecutive rows less than ROW_PITCH_MAX_PT apart are one line each (a wrapped row pushes
# the next row down by a full extra line), and each row's last cell must start at the height of its amount; the cell
# texts are prefixes that stop before any ligature.
TABLE_ROWS = [("$669,000", "Your decision; no"), ("$653,000", "Your decisions; handovers"),
              ("$515,000", "Contract and usage data"), ("$392,000", "Our own vendor ac")]
TABLE_END = "Total"
ROW_PITCH_MAX_PT = 20

CLOSE_SCRIPT = '''on run argv
  set docName to item 1 of argv
  tell application "Pages"
    with timeout of 30 seconds
      if exists document docName then close document docName saving no
    end timeout
  end tell
  return "ok"
end run
'''

RENDER_SCRIPT = '''on run argv
  set docName to item 1 of argv
  set outPath to item 2 of argv
  tell application "Pages"
    with timeout of 120 seconds
      repeat 60 times
        if exists document docName then exit repeat
        delay 1
      end repeat
      if not (exists document docName) then error "Pages has not opened " & docName
      export document docName to (POSIX file outPath) as PDF
      close document docName saving no
    end timeout
  end tell
  return "ok"
end run
'''

MEASURE_SCRIPT = r'''ObjC.import('Quartz');
function run(argv) {
  var pdf = $.PDFDocument.alloc.initWithURL($.NSURL.fileURLWithPath(argv[0]));
  var out = {pages: pdf.pageCount, lines: 0, minY: null, width: null, height: null, texts: {}};
  var page = pdf.pageAtIndex(0);
  var box = page.boundsForBox($.kPDFDisplayBoxMediaBox);
  out.width = box.size.width; out.height = box.size.height;
  var text = ObjC.unwrap(page.string);
  var count = page.numberOfCharacters;
  var ys = [], lines = {}, minY = 1e9;
  for (var i = 0; i < count; i++) {
    var sel = page.selectionForRange($.NSMakeRange(i, 1));
    var y = null;
    if (sel && !sel.isNil()) { y = sel.boundsForPage(page).origin.y; }
    ys.push(y);
    if (y !== null && text.charAt(i).trim() !== '') { lines[Math.round(y)] = 1; if (y < minY) minY = y; }
  }
  out.lines = Object.keys(lines).length;
  out.minY = minY;
  for (var k = 1; k < argv.length; k++) {
    var s = argv[k], idx = text.indexOf(s);
    out.texts[s] = idx < 0 ? null : [ys[idx], ys[idx + s.length - 1]];
  }
  return JSON.stringify(out);
}
'''


def pages_running() -> bool:
    return subprocess.run(["pgrep", "-x", "Pages"], capture_output=True).returncode == 0


def render(docx: Path, pdf: Path, scripts: dict[str, Path]) -> None:
    """The open command puts the Word file in Pages, starting Pages if needed; AppleScript waits for the document,
    exports it as PDF and closes it. A document of the same name left open by an earlier run is closed first, so that
    Pages reads the file afresh. Three tries, because Pages sometimes answers late while busy."""
    name = docx.stem   # Pages names the document after the file, without its extension
    if pages_running():
        subprocess.run(["osascript", str(scripts["close"]), name], capture_output=True, text=True, timeout=60)
    subprocess.run(["open", "-g", "-a", str(PAGES_APP), str(docx)], check=True, timeout=60)
    for attempt in range(1, 4):
        out = subprocess.run(["osascript", str(scripts["render"]), name, str(pdf)], capture_output=True, text=True,
                             timeout=240)
        if out.returncode == 0 and pdf.exists():
            return
        time.sleep(5 * attempt)
    raise RuntimeError(f"Pages could not render {docx.name}: {out.stderr.strip() or out.stdout.strip()}")


def measure(pdf: Path, script: Path, texts: list[str]) -> dict:
    out = subprocess.run(["osascript", "-l", "JavaScript", str(script), str(pdf), *texts], capture_output=True,
                         text=True, timeout=240)
    if out.returncode != 0:
        raise RuntimeError(f"PDFKit could not read {pdf.name}: {out.stderr.strip()}")
    return json.loads(out.stdout.strip())


def pdf_page_count(pdf: Path) -> int:
    """The page objects in the PDF itself, a count independent of PDFKit."""
    return len(re.findall(rb"/Type\s*/Page(?![s/a-zA-Z])", pdf.read_bytes()))


def main(argv: list[str]) -> int:
    docx = Path(argv[1]).resolve() if len(argv) > 1 else MEMO_DOCX
    if not docx.exists():
        print(f"{rel(docx)} does not exist; build it with scripts/06_build_memo_docx.py first")
        return 2
    if sys.platform != "darwin" or not shutil.which("osascript") or not PAGES_APP.exists():
        print("Nothing on this machine can render the memo to PDF: the check needs macOS with Pages (osascript "
              "drives it and PDFKit reads the result). Not checked.")
        return 2
    texts = HEADER_TEXTS + [a for a, _ in TABLE_ROWS] + [c for _, c in TABLE_ROWS] + [TABLE_END]
    with tempfile.TemporaryDirectory() as tmp:
        scripts = {"close": Path(tmp) / "close.applescript", "render": Path(tmp) / "render.applescript"}
        scripts["close"].write_text(CLOSE_SCRIPT, encoding="utf-8")
        scripts["render"].write_text(RENDER_SCRIPT, encoding="utf-8")
        measure_script = Path(tmp) / "measure.js"
        measure_script.write_text(MEASURE_SCRIPT, encoding="utf-8")
        MEMO_PDF.parent.mkdir(parents=True, exist_ok=True)
        if MEMO_PDF.exists():
            MEMO_PDF.unlink()
        render(docx, MEMO_PDF, scripts)
        memo = measure(MEMO_PDF, measure_script, texts)
    memo["pages"] = int(memo["pages"])   # PDFKit's page count arrives as text through the JavaScript bridge
    pdf_pages = pdf_page_count(MEMO_PDF)
    spare_pt = memo["minY"] - BOTTOM_MARGIN_PT
    spare_lines = spare_pt / BODY_LINE_PT
    def y_of(t: str):
        v = memo["texts"].get(t)
        return v[0] if v else None

    header_ys = [y for t in HEADER_TEXTS for y in (memo["texts"].get(t) or [])]
    header_ok = len(header_ys) == 2 * len(HEADER_TEXTS) and max(header_ys) - min(header_ys) < 1.5
    anchors = [y_of(a) for a, _ in TABLE_ROWS] + [y_of(TABLE_END)]
    pitches = ([anchors[i] - anchors[i + 1] for i in range(len(anchors) - 1)]
               if all(a is not None for a in anchors) else [])
    cells_ok = all(y_of(c) is not None and abs(y_of(c) - y_of(a)) < 1.5 for a, c in TABLE_ROWS)
    rows_ok = bool(pitches) and all(0 < p < ROW_PITCH_MAX_PT for p in pitches) and cells_ok
    letter = abs(memo["width"] - PAGE_WIDTH_PT) < 1 and abs(memo["height"] - PAGE_HEIGHT_PT) < 1
    ok = memo["pages"] == 1 and pdf_pages == 1 and letter and spare_lines >= LINES_REQUIRED and header_ok and rows_ok

    lines = [
        "# Memo page check",
        "",
        f"Written by `qa/memo_page_check.py` for `{rel(docx)}`, rendered to `{rel(MEMO_PDF)}`.",
        "",
        "How it was checked: Microsoft Word on this machine refuses the AppleScript save-as command (error -1708 for "
        "every format), so the open command put the Word file in Pages and AppleScript through osascript had Pages "
        "export it as PDF (the PDF embeds Calibri and Calibri Bold). macOS PDFKit, through osascript's JavaScript, then "
        "read the PDF "
        "back: the page size, the page count, the position of every character (hence the number of text lines and the "
        "lowest line), and whether the header line and each table row sit on one line. The lines to spare are the space "
        "between the lowest line and the bottom margin, divided by the height of a body line. The page objects in the "
        "PDF were counted again from the file.",
        "",
        "| Measure | Result |",
        "|---|---|",
        f"| Page size | {memo['width'] / 72:.1f} by {memo['height'] / 72:.1f} in ({'US Letter' if letter else 'not US Letter'}) |",
        f"| Pages (PDFKit) | {memo['pages']} |",
        f"| Pages (objects in the PDF) | {pdf_pages} |",
        f"| Text lines on the page | {memo['lines']} |",
        f"| Bottom of the lowest line, from the bottom of the page | {memo['minY']:.1f} pt |",
        f"| Bottom margin | {BOTTOM_MARGIN_PT:.0f} pt |",
        f"| Space left below the last line | {spare_pt:.1f} pt, {spare_pt / 72:.2f} in |",
        f"| Lines to spare at 10.5 pt with 2 pt after ({BODY_LINE_PT:.1f} pt a line) | {spare_lines:.1f} (at least {LINES_REQUIRED} required) |",
        f"| Header line (To, From, Date) on one line | {'yes' if header_ok else 'NO'} |",
        f"| Table row pitch, amount to next amount (pt) | {', '.join(f'{p:.1f}' for p in pitches) or 'not found'} |",
        f"| Every table row on one line (pitch under {ROW_PITCH_MAX_PT} pt, last cell level with the amount) | "
        f"{'yes' if rows_ok else 'NO'} |",
        "",
        f"Result: {'PASS' if ok else 'FAIL'}: the memo is {memo['pages']} page{'s' if memo['pages'] != 1 else ''} with "
        f"{spare_lines:.1f} lines to spare.",
        "",
    ]
    REPORT.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[6:]))
    print(f"Wrote {rel(REPORT)} and {rel(MEMO_PDF)}.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
