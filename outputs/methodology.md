Repository: https://github.com/claxman/vendor-spend-analysis

# Methodology

## Approach
Profiled the raw workbook: 386 rows, $7,887,000 over 12 months.
Ran a forensic pass: identical amounts, precision, first digits, duplicates, payee types.
Cleaned names, merged five double entries; wrote taxonomy, rules, cost groups and notes.
The Config list names company functions, so SaaS is read as the function that runs the hosted product (platform, hosting, monitoring); company-wide software sits in G&A as corporate IT and function-specific software with its function.
Config has no HR or IT department, so HR, recruiting, travel, benefits, insurance and corporate IT sit in G&A, which is why it holds the most rows.
Classified all 386 rows in groups of 40, a web search and source each.
Reread Salesforce as the product platform.
Built the savings model: 41 saving lines, low to high, each tagged with its decision.
Reviewed every row again offline, then 142 with fresh web checks.
Rewrote the text for readers; wrote the Top 3, memo, README, workbook.

## Tools that produced the outputs
Claude Code CLI, one session: Claude Fable 5.1 for the scaffold and profile, Claude Opus 5.5 from the forensic pass to the platform reread, Claude Fable 5.1 after.
Research agents did the web verification and second pass.
Python 3.11, openpyxl, python-docx; Pages rendered the memo to PDF.
Web search, page fetch; git and GitHub, a commit per step.

## Prompts
Twenty-five prompts directed the analysis, logged in prompts/log.md in the order given.
Prompt 6: taxonomy, recommendation rules, cost groups, 79 analyst notes.
Prompt 15: classify all rows, a web search and lookup log each.
Prompt 16: Salesforce as the product platform; URLs naming individuals withheld.
Prompt 17: the savings assumptions, line by line.
Prompt 18: the second-pass review; reader-facing text.
Prompts 19 to 25: documents, workbook, manual review, corrections, calculations, platform bill, cross-checks.
Research brief: prompts/research_brief.md.

## Validation and evidence
50 automated checks per build: merge, rule documents, classification, savings, documents, workbook.
Planted-error self-tests: 89 errors in the QA script, 16 in the merge script, each caught.
Web verification: 319 of 386 rows, 99% of spend; 67 unconfirmed, with reasons.
Second pass: 386 rows read, 142 (95% of spend) re-verified, 96% agreement, 25 changed.
Manual review: 25 largest rows (78.5% of spend), 13 checked against source links, 12 well-known vendors read against the reviewer's own knowledge; Top 3 and memo read line by line; no changes.
Evidence: qa/ (validation report, verification log, research, reviews, page check), outputs/analysis/, docs/decisions.md.

## Limits
One 12-month total per vendor: no dates, invoices, entities, cost centers, contracts, renewal dates or headcount; year-1 figures rest on stated timing assumptions.
The data provider modified names and costs; an unconfirmed name is a question, not a finding.
67 rows, $96,000, remain unconfirmed, marked in the sheet.
