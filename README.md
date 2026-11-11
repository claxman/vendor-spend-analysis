# Vendor spend analysis

## What this is

A review of the acquired business's third-party vendor spend for an acquisition due diligence: 386 vendor rows and $7,887,000 of spend over 12 months, each row classified, verified online and given a recommendation, with a savings model, a second-pass review, and the documents for the CEO and CFO of the group. The outputs were produced in one Claude Code session, prompt by prompt, with the prompts that directed the analysis logged, every step committed and every figure computed by a script from the data.

Deliverables: the Google Sheet, https://docs.google.com/spreadsheets/d/1LBowVBvWB4T5Ii1-9YZGiAOpO9L_ngidNbsS86yXrgQ, and the memo, https://docs.google.com/document/d/1ZVG70hx3l9UNfTCQIN2medwAudMVrYi-nsck-Ck9fN0.

## Results in five lines

- Base-case run-rate saving of $2,229,000 a year, 28% of spend, in a range of $1,566,000 to $3,097,000; $1,209,000 lands in year 1.
- Three moves carry most of it: the office exit under a remote operating model ($669,000), back-office services to the group's shared functions ($653,000) and the Salesforce platform agreement renegotiated at change of control ($515,000).
- $1,264,000 of the base is vendor action the acquired business can take alone; the rest is the value of decisions only the group can take.
- 319 of 386 rows (99% of spend) were verified from the vendor's own site or a reliable directory; a second pass re-verified 142 rows (95% of spend) fresh and agreed with the first pass on 96% of them.
- $274,000 of deal and one-off costs fall away without action and are not counted; $171,000 of mandated, statutory and contingent payees must not be cut.

## How the work was done

| Step | Prompt | Commit | What was done |
|---|---|---|---|
| 0 | 1 to 3 | `a070c13`, `94b915a` | Repository, CLAUDE.md, folders, the raw workbook committed unchanged |
| 1 | 4 | `47f9ba4` | Profile of the raw workbook: structure, hidden content, totals (`outputs/analysis/00_data_profile.md`) |
| 1b | 5 | `d6a0926` | Forensic pass: identical amounts, precision, first digits, duplicate names, payee types (`01_forensics.md`) |
| 2 | 6 | `94e24af` | Taxonomy, recommendation rules, analyst notes, cost groups, name cleaning and the merge map (`02_cleaning_report.md`) |
| 2b to 2d | 7 to 12 | `c49d9d2` to `be8fb00` | Rule decisions, merge policy, the group recommendation rule, the QA script and its fixes |
| 2e, 2f | 13, 14 | `dfdb321`, `3391ec9` | Decision tags on every savings assumption, the hardware rule, the merge script |
| 3 | 15 | `41f0bb6` to `9da68c0` | Classification of all 386 rows in ten groups of 40, with web verification and a log of every lookup |
| 3b | 16 | `61dc5c5` | Salesforce reread as the product platform; URLs naming private individuals withheld |
| 3c | 17 | `f40a2d5` | SaaS reread as the function that runs the hosted product |
| 4 | 17 | `620f2ce` | Savings model (41 saving lines, low, base and high, decision tags) and the insights |
| 4b | 18 | `876b70c` | The open assumptions decided (hardware and courier lines, MultiSport kept, Bisley Law reworded) |
| 5 | 18 | `13e3708` | Second-pass review (all rows, then 142 fresh web checks), the working files kept, reader-facing text |
| 6 | 19 | `2c3abf2` | Presentation figures, the Top 3, the memo, this README, the methodology and the sheet workbook |
| 7 | 20 | `6db69ff` | Final corrections: the memo on one page, decision-led rationales, the workbook's saving columns, the manual review |
| 8 | 21 | `07ab5fb` | Wording corrections: the memo's subject line, how the classification lines were written, the manual review as done, the prompt count |
| 9 | 22 | this commit | Calculations that reproduce: each Top 3 calculation written out in whole dollars and recomputed by a check, the memo's Scale line, the department rule in the methodology, the deliverable links |

The decisions behind each step are in `docs/decisions.md`; the prompts are in `prompts/log.md`, in the order given.

## Repository map

- `CLAUDE.md`: the brief and the rules the session worked to.
- `README.md`: this file. `requirements.txt`: the two Python packages the scripts need.
- `data/raw/vendor_analysis_assessment.xlsx`: the input workbook, never modified (its SHA-256 is recorded in every analysis file).
- `outputs/vendors_clean.csv`: the 386 rows with repaired names, ids and the merge map columns.
- `outputs/vendors_classified.csv`: the deliverable, 16 columns per row: department, description, recommendation, rationale, risk note, cost group, flags, confidence, verification and source.
- `outputs/batches/batch_01.csv` to `batch_10.csv`: the classification in groups of 40, merged into the file above.
- `outputs/analysis/00_data_profile.md`, `01_forensics.md`, `01_forensic_flags.csv`, `02_cleaning_report.md`: the profile, the forensic pass and the cleaning report.
- `outputs/analysis/savings.csv`, `savings.md`, `savings_summary.md`: the savings model per vendor, its report, and the rounded figures the documents quote.
- `outputs/analysis/insights.md`: ten short findings with figures and vendor ids.
- `outputs/top3_opportunities.md`, `outputs/memo.md`, `outputs/memo.docx`, `outputs/memo.pdf`, `outputs/methodology.md`: the documents; the PDF is the Word file as Pages rendered it on this machine (`qa/memo_page_check.md`).
- `outputs/sheet/Vendor Analysis Assessment - Chaitanya Laxman.xlsx`: the filled copy of the workbook.
- `scripts/vsa_common.py`: shared helpers (workbook access, name repair, the merge and link groups, the no-dash guard).
- `scripts/00_data_profile.py`, `01_forensics.py`, `02_clean.py`: the profile, the forensic pass, the cleaning.
- `scripts/research_inputs.py`, `build_hints.py`, `classify_tools.py`: the research inputs, the analyst-notes document and the batch builder, as they ran in steps 2 and 3.
- `scripts/merge_validate.py`: merges the batches, runs every check, writes `qa/validation_report.md`.
- `scripts/savings_model.py`, `03_savings.py`: the savings model and its outputs. `04_insights.py`: the insights.
- `scripts/05_build_sheet.py`: the workbook and its read-back check. `06_build_memo_docx.py`: the memo as a Word file.
- `qa/check_outputs.py`: the checks (M1 to M7, S1 to S6, C1 to C20, V1 to V11, D1 to D5, W1) and the planted-error self-test. `qa/memo_page_check.py`: renders the memo to PDF with Pages, reads it back with macOS PDFKit and confirms the page count and the lines to spare (`qa/memo_page_check.md`).
- `qa/validation_report.md`: the result of every check, the distributions and the cross-tab of recommendation by saving line.
- `qa/verification_log.csv`, `qa/verification_exceptions.csv`: every web lookup, and the reason for each unconfirmed row.
- `qa/vendor_groups.csv`, `qa/name_changes.csv`: the merge map and the name repairs.
- `qa/second_pass_review.csv`, `qa/second_pass_report.md`: the second-pass review, row by row and as a report.
- `qa/manual_review.md`: the VP Operations' own check of the 25 largest rows (13 against their source links, 12 well-known vendors against the reviewer's own knowledge), and of the Top 3 and the memo, before submission.
- `qa/research/`: the research inputs, findings, logs and failed attempts of step 3, with a README; `qa/classification_lines/`: the per-batch classification lines the builder read.
- `docs/taxonomy.md`, `clusters.md`, `recommendation_rules.md`, `vendor_hints.md`, `savings_assumptions.md`: the rules the classification and the model follow. `docs/decisions.md`: every decision, newest first, with the open questions for Finance.
- `prompts/log.md`: the 22 prompts, in the order given (one housekeeping omission is marked in place). `prompts/research_brief.md`: the brief the research agents worked from.

## How to re-run

From the repository root, with Python 3.11:

```
python -m venv .venv && .venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/00_data_profile.py
.venv/bin/python scripts/01_forensics.py
.venv/bin/python scripts/02_clean.py
.venv/bin/python scripts/merge_validate.py
.venv/bin/python scripts/03_savings.py
.venv/bin/python scripts/04_insights.py
.venv/bin/python scripts/06_build_memo_docx.py
.venv/bin/python scripts/05_build_sheet.py
.venv/bin/python qa/check_outputs.py
.venv/bin/python qa/check_outputs.py --self-test
.venv/bin/python scripts/merge_validate.py --self-test
.venv/bin/python qa/memo_page_check.py
```

The classification lines in `qa/classification_lines/` were written by Claude Code in the session, vendor by vendor, from the research findings and the rules: not typed by a person and not generated by a script. `scripts/classify_tools.py build NN` built each batch file from them, and re-running the scripts above rebuilds every output from those lines and the raw workbook without touching the raw file. The last line needs a Mac with Pages; without it the page check says so and changes nothing.

## Quality checks and evidence

- Every build runs 50 checks: the merge (M1 to M7), the rule documents (S1 to S6), the classification (C1 to C20: allowed values, one-sentence rationales, banned phrases, risk notes, every recorded decision, no project workings in the reader-facing text, American English), the savings model (V1 to V11: ranges, tags, one saving line per row, roll-ups to the cent, recommendation against saving rate, the group function first in every rationale that rests on a group decision, a reason on every Terminate row that saves under half its spend), the documents (D1 to D5: every figure traceable, every table adds up, no project vocabulary, American English, every calculation in the Top 3 recomputed from the savings file) and the workbook (W1). Results: `qa/validation_report.md`.
- Planted-error self-tests show that each check catches what it should (`qa/check_outputs.py --self-test`, `scripts/merge_validate.py --self-test`).
- Web verification: `qa/verification_log.csv` (every lookup), `qa/verification_exceptions.csv` (the 67 unconfirmed rows), `qa/research/` (the agents' findings).
- Second-pass review: `qa/second_pass_review.csv` and `qa/second_pass_report.md`.
- The savings figures reconcile to the cent across vendors, saving lines, cost groups and opportunities (`outputs/analysis/savings.md`, "Reconciliation").
- Manual review before submission: of the 25 largest rows (78.5% of spend), 13 checked against their source links and 12 well-known vendors read against the VP Operations' own knowledge; the Top 3 and the memo read line by line; no changes (`qa/manual_review.md`).
- The memo renders to one US Letter page with lines to spare (`qa/memo_page_check.md`: Pages renders it, PDFKit measures it).

## Assumptions and limits

- The data is one 12-month total per vendor: no dates, invoices, paying entities, cost centers, contracts or headcount. The year-1 figures rest on stated timing assumptions (`docs/savings_assumptions.md`).
- Every savings assumption is written next to the figure it produces, as a low, base and high case; a saving that needs a group decision is tagged with that decision and presented as the value of the decision, never as a fact about the group.
- 67 rows ($96,000) could not be verified online and are marked as unconfirmed; the recommendations on them are provisional.
- The vendor names and costs were modified by the provider of the data. A name the web does not confirm is therefore a question for Finance, not evidence of a problem with the payee, and the amounts are the file's modified values.
