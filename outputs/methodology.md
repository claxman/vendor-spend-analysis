# Methodology

## Approach
Profiled the raw workbook: 386 rows, $7,887,000, one 12-month total per vendor.
Ran a forensic pass: identical amounts, precision, first digits, duplicates, payee types.
Cleaned names, merged five double entries, and wrote the taxonomy, rules, cost groups and notes.
Classified all 386 rows in groups of 40, a web search and source per vendor.
Reread Salesforce as the product platform and SaaS as the function running it.
Built the savings model: 41 saving lines, low to high, each tagged with its decision.
Reviewed every row again offline, then 142 rows with fresh web checks.
Rewrote the text for readers; wrote the Top 3, memo, README and workbook.

## Tools that produced the outputs
Claude Code CLI, one session: Claude Opus 5.5 to the classification, Claude Fable 5.1 after.
Research agents did the web verification and the second pass.
Python 3.11 with openpyxl and python-docx; CSV via the standard library.
Web search and page fetch; git and GitHub, one commit per step.

## Prompts
Nineteen prompts, logged verbatim in prompts/log.md before any work on them.
Prompt 6: taxonomy, recommendation rules, cost groups, 79 analyst notes.
Prompt 9: which merged and linked rows share one recommendation.
Prompt 15: classify all rows with a web search and a lookup log per vendor.
Prompt 16: Salesforce as the product platform; URLs naming individuals withheld.
Prompt 17: the SaaS department reread; the savings assumptions, line by line.
Prompt 18: the open assumptions decided; the second-pass review; reader-facing text.
Research brief: prompts/research_brief.md.

## Validation and evidence
47 automated checks per build: merge, rule documents, classification, savings, documents, workbook.
They test values, rationales, banned phrases, risk notes, recorded decisions, American English, savings ranges, roll-ups to the cent, quoted figures and table totals.
Planted-error self-tests: 79 errors in the QA script and 16 in the merge script, each caught.
Web verification: 319 of 386 rows, 99% of spend; 67 unconfirmed rows listed with reasons.
Second pass: 386 rows read, 142 (95% of spend) re-verified, 96% agreement, 25 rows changed.
Evidence: qa/validation_report.md, qa/verification_log.csv, qa/verification_exceptions.csv, qa/research/, qa/second_pass_review.csv, qa/second_pass_report.md, outputs/analysis/, docs/decisions.md, prompts/log.md.

## Limits
One 12-month total per vendor: no dates, invoices, entities, cost centers or contracts.
Names and costs were modified by the data provider; an unconfirmed name is a question, not a finding.
No contract register, renewal dates or headcount; year-1 figures rest on stated timing assumptions.
67 rows, $96,000, remain unconfirmed and are marked so in the sheet.
