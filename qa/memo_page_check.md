# Memo page check

Written by `qa/memo_page_check.py` for `outputs/memo.docx`, rendered to `outputs/memo.pdf`.

How it was checked: Microsoft Word on this machine refuses the AppleScript save-as command (error -1708 for every format), so Pages, driven by AppleScript through osascript, opened the Word file and exported it as PDF (the PDF embeds Calibri and Calibri Bold). macOS PDFKit, through osascript's JavaScript, then read the PDF back: the page size, the page count, the position of every character (hence the number of text lines and the lowest line), and whether the header line and each table row sit on one line. The lines to spare are the space between the lowest line and the bottom margin, divided by the height of a body line. The page objects in the PDF were counted again from the file.

| Measure | Result |
|---|---|
| Page size | 8.5 by 11.0 in (US Letter) |
| Pages (PDFKit) | 1 |
| Pages (objects in the PDF) | 1 |
| Text lines on the page | 36 |
| Bottom of the lowest line, from the bottom of the page | 193.6 pt |
| Bottom margin | 54 pt |
| Space left below the last line | 139.6 pt, 1.94 in |
| Lines to spare at 10.5 pt with 2 pt after (14.8 pt a line) | 9.4 (at least 8 required) |
| Header line (To, From, Date) on one line | yes |
| Table row pitch, amount to next amount (pt) | 17.4, 17.4, 17.4, 17.4 |
| Every table row on one line (pitch under 20 pt, last cell level with the amount) | yes |

Result: PASS: the memo is 1 page with 9.4 lines to spare.
