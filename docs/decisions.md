# Decisions

Decisions taken during the analysis, newest first. Each records what was decided and where it is implemented. The prompts that carried them are in `prompts/log.md`.

## 2026-11-12: office cross-check and platform wording (prompt 25, step 12)

- The office sentence of step 11 ("the 75% equals keeping the Zagreb lease whole") was not exact and contradicted row `V0007`, which keeps Zagreb as the hub and right-sizes it. The Top 3 now says that the model keeps one hub space in Zagreb, right-sized at the next break, that the 75% is applied evenly to every lease row, and, as a cross-check, that closing every site except Zagreb with its lease untouched would save $653,000 (78% of the leases), so the 75% sits just below that. The register's Office footprint reasoning and the closing sentence of "Office exit check" in `savings_summary.md` (written by `scripts/03_savings.py`, whose row "Kept at the base case beyond the Zagreb lease" is now "Difference between the cross-check and the base case") say the same; "equals" and "whole" are gone from all three. The office explanation runs to 140 words (limit 140).
- The Salesforce explanation is rewritten in plain sentences, no semicolons, 170 words (limit 170). The base is stated as what it is: until the contract shows which reading applies, it takes the middle of the 5% to 25% range modeled on the platform agreement; the register says the same in the lever's reasoning and in "The Salesforce platform bill" ("placeholder" is gone). The explanation states the published rates from the lookups logged against `V0002`: 15% of net revenue as the standard share, 25% for embedded apps, 25% until May 2017, and that these are what the best rate and the older rate mean; the register's two readings carry the same figures in brackets. The two readings, every calculation in whole dollars, the range, year 1 and the main risk are kept, and D5 still reproduces the calculation.
- The session records (`~/.claude/projects/<this folder>/`, Claude Code 2.1.321) hold one session file with one session id, cwd this folder, from 2026-11-09 21:39 to 2026-11-12 UTC, so "one Claude Code session" stands. The `model` field of the main thread's assistant messages switches three times: Claude Opus 5.5 for the opening message (21:39 UTC on November 9), Claude Fable 5.1 from 21:40 through the scaffold and the profile (steps 0 and 1, commits at 21:43 and 22:06), Claude Opus 5.5 from 22:52 on November 9 through the forensic pass, the cleaning, the decision tags, the classification, the platform reread and the housekeeping commit (steps 1b to 3b, last Opus message 05:44 UTC on November 11, the housekeeping commit at 05:43), and Claude Fable 5.1 from 05:48 on November 11 (step 3c at 06:04) to the end. The 40 research subagents ran on the main model of their time: 27 on Opus 5.5 for the step 3 verification on November 10, 13 on Fable 5.1 for the second pass on November 11. The records also carry an `advisorModel` field naming claude-opus-5-5 on every Opus message and claude-fable-5-2 on 427 of the 928 Fable messages; the records do not say what the field does, so the methodology states the `model` field only. The tools line therefore reads "Claude Fable 5.1 for the scaffold and profile, Claude Opus 5.5 from the forensic pass to the platform reread, Claude Fable 5.1 after" in place of "Claude Opus 5.5 through the classification step, Claude Fable 5.1 after it", which the records do not support as written.
- Methodology at 449 words (limit 450) after small trims ("each" for "per vendor", "research" for "research files" and the like); twenty-five prompts. README: step 12 in the table, step 11's commit, the prompt count 25. The memo, the vendor rows and every figure are untouched: `outputs/analysis/savings.csv` has the same SHA-256 before and after this step (f931278bb31f4beb66ade7321854662fc343f6c5f3b1612ee63ac7198aa6a7f0), 50 checks pass, the self-tests catch 89 and 16 planted errors, and the memo is 380 words on one page with 8.5 lines to spare.

## 2026-11-11: what the platform bill is (prompt 24, step 11)

- What the Salesforce bill most likely is: a product that runs on the Salesforce platform normally pays Salesforce a share of its product revenue under a partner distribution agreement, plus the seats the company uses itself, not a per-seat subscription. The programme terms were verified on Salesforce's own pages and logged against `V0002` in `qa/verification_log.csv` and `qa/research/logs/claude_log.csv` (six lookups): 15% of net revenue for an ISVforce app sold to existing Salesforce customers (the help article "Partner Program FAQ: AgentExchange ISV"; the March 2018 programme guide, which also gives 20% for Premier partners; Trailhead); 25% for an embedded (OEM) app (the same FAQ and guide; the program year 2019 policies); 25% as the standard rate until the press release of May 2, 2017 lowered it to 15% for new partners; and marginal rates by annual order value on the Partner Community page (FY22 policies): ISVforce 15% down to 10% above $20 million, OEM 25% down to 15%, with a reduction only above $1 million. `docs/savings_assumptions.md` records them in a new section, "The Salesforce platform bill", next to the lever's reasoning.
- The lever on `V0002` is restated as two readings in the register, the Top 3 and the row's rationale: a partner revenue share moves with revenue and seat counts do not reduce it, so the levers are the rate tier, what counts as net revenue and the company's own seats (a small saving if the agreement is already on the best tier, a large one on an older rate); licences would mean a seat true-down and the renewal terms, where co-terming with any Salesforce agreement the group holds and a multi-year commitment now sit and nowhere else. The first question for the contract is which reading applies and which rate tier the agreement is on. The Top 3's Salesforce explanation runs to 140 words (limit 140); its calculation sentence is unchanged, so D5 still reproduces it.
- The low case on `V0002` is 5% (internal seats only, with the revenue share already on the best tier); the base 15% and the high 25% are unchanged, and the register says the base is a placeholder between the two readings until the contract is read. Re-run: the run-rate low falls from $1,565,930 to $1,410,068 ($1,410,000 rounded, $1,566,000 before), the Salesforce platform agreement line's low from $335,000 to $179,000, and the Top 3 range reads $179,000 to $850,000; the base, high, year-1 and without-decision figures are unchanged. The README's range follows.
- `V0002`'s description (24 words): "Platform fees for the company's Salesforce-native product, most likely a partner revenue share on product sales, plus internal CRM seats; the largest single cost". C14 now expects "revenue share" and "rate tier" in the rationale; one planted error added (89 in all). `qa/manual_review.md` notes the change to row 2 after the review, at the reviewer's instruction; Finance question 2 is reworded for the two readings and the rate tier; `scripts/04_insights.py` adds the reading to finding 1 and to request 3.
- Office opportunity: the Top 3 says the 75% equals keeping the Zagreb lease whole, because closing every other site saves the $653,000 the rows give on leases alone. `scripts/03_savings.py` writes the check to `savings_summary.md` ("Office exit check"): the Office footprint line $837,043 on 10 rows, the Zagreb lease (`V0007`) $183,754, every other site, adviser and charge $653,289 (78%), the base case $627,782 (75%), $25,507 kept beyond the Zagreb lease for registered addresses. The office explanation runs to 119 words (limit 120): the touchdown-space clause, the "in a range of" wording and "not yet known" gave way to the check sentence. The register's Office footprint reasoning says the same.
- Memo, the Scale line: "$2,229,000 a year is 28% of this business's third-party spend and falls straight to operating profit; the saving rate outside the Salesforce platform is 38%, and the same review repeats on every acquisition." The 38% is the base saving outside the Salesforce platform line ($2,229,000 less $515,000, $1,714,000) over the spend outside it ($7,887,000 less $3,383,000, $4,504,000), both written by `03_savings.py` into the "Spend and savings" table; the whole base saving over the spend outside the platform (49%) would count the platform's own saving against spend that excludes it, so it is not the figure used. To keep 380 words: the bottom line no longer repeats "28% of spend" (the Scale line carries it), the Context line reads "Salesforce is $3,117,000, 40% of spend", the Salesforce decision bullet "the contract, usage data and group procurement", and the 0-to-30-day line "collect contracts, notice dates, Salesforce usage data; Finance confirms the 67 vendors not verified online". 380 words outside the table, one page with 8.5 lines to spare (37 lines; the Scale line still takes two).
- Methodology: twenty-four prompts, "Prompts 19 to 24: ... calculations, the platform bill", 89 planted errors; to stay at 450 words, "142 rows" became "142" and "research files" became "research". README: step 11 in the table, step 10's commit, the prompt count 24, the range $1,410,000 to $3,097,000.

## 2026-11-11: spelling and what is not counted (prompt 23, step 10)

- `V0174`'s risk note reads "notarization". The British-forms check (C20 on descriptions, rationales and risk notes; D4 on the four documents) now also flags every -ise, -ises, -ised, -ising, -isation or -isations word whose base American English does not spell -ise as well; `AMERICAN_ISE` in `qa/check_outputs.py` lists the bases it does (advertise, advise, enterprise, exercise, expertise, franchise, merchandise, premise, promise, supervise and the rest), and -wise words are left alone. The rescan of every reader-facing text found nothing else: the forms the texts contain (advertising, advising, merchandise, franchise, enterprises, premises) are American spellings, and "organisation" appears only inside four source URLs, which the check does not read. Two planted errors added to the self-test (88 in all): "notarisation" in a risk note, "categorisation" in a document.
- People-linked spend the review does not count: the four saving lines in `PEOPLE_LINKED_LEVERS` (`scripts/savings_model.py`), health and life cover, statutory cover and benefit schemes, employer-of-record pay and student labor, are $434,781 of spend on 29 rows, of which the model counts $37,143 (the insurers' rate and the employer-of-record fee); the rest, $397,638, $398,000 rounded, moves only with the workforce plan. `scripts/03_savings.py` writes it to `savings_summary.md` ("People-linked spend not counted"); the Top 3 closes with the rounded figure and the reason; the memo's "Not counted" line names it without a figure; `scripts/04_insights.py` gives the figure with its vendor ids as finding 11. The longer "Not counted" line wraps, which left 7.7 lines to spare against the eight that prompt 20 requires, so the retention risk now opens "Retention of the Zagreb engineers" instead of "Retention at the Zagreb engineering hub" (one word fewer, the bullet back on one line): 379 words outside the table against the limit of 380, one page with 8.5 lines to spare.
- README: step 10 in the table, the prompt count 23, eleven findings in the insights; methodology: twenty-three prompts, 88 planted errors.

## 2026-11-11: calculations that reproduce (prompt 22, step 9)

- Top 3: each explanation states its calculation with its own base and rate, in whole dollars, so that a reader who multiplies gets the figure shown. Offices: 75% of the $837,043 of leases and coworking ($627,782) and 70% of the $59,297 of running costs ($41,508), $669,290 a year, $669,000 rounded. Salesforce: 15% off the $3,117,226 platform agreement ($467,584), 20% off the $208,675 document app ($41,735) and 10% off the $52,825 PSA tool ($5,283), $514,602, $515,000 rounded. Back office: 35% of the $553,641 of audit, tax and accounting ($193,774), 100% of the $149,179 of recruiters ($149,179), 80% of the $101,762 of HR and finance systems ($81,410) and the other twelve lines ($229,093), $653,456, $653,000 rounded. The spends are the saving lines' spends to the dollar, each product is spend times rate rounded half up to the dollar, and each total is the sum of the products as shown, which rounds to the opportunity's figure; the model's exact totals differ by at most a dollar of rounding ($514,601.44 and $653,456.57). The explanations run to 117, 120 and 119 words against a limit of 120.
- `scripts/03_savings.py` writes a "Calculations that reproduce" section into `savings_summary.md` with the same figures (every line of the office and Salesforce opportunities; the three largest back-office lines and the other twelve as one row), so that D1 traces them. `dollars()` in `scripts/savings_model.py` is the half-up rounding the summary and the check share.
- New check D5 in `qa/check_outputs.py` (50 checks): every "R% of $spend ... ($product)" statement in the Top 3 must name exactly one saving line of the section's opportunity in `savings.csv` (the same rate, the same spend to the dollar); its product must be spend times rate to the dollar; lines left out must appear as "the other N lines ($rest)" with their base saving unless they save nothing; the parts must add to the stated "$total a year, $rounded rounded"; and the rounded figure must be the section's base saving. Four planted errors in the self-test (86 in all): a wrong product, a spend no line carries, parts that do not add up, a line left out.
- Memo: the Scale line reads "$2,229,000 a year is 28% of this business's third-party spend; it falls straight to operating profit, and the same review repeats on every acquisition." The memo is 370 words outside the table against the new limit of 380, and the page check passes.
- Methodology: two lines under Approach give the department rule (the Config list names company functions, so SaaS is read as the function that runs the hosted product; company-wide software sits in G&A as corporate IT, function-specific software with its function) and why G&A holds the most rows (Config has no HR or IT department). The tools line reads "Claude Opus 5.5 through the classification step, Claude Fable 5.1 after it"; the prompt count is twenty-two; 450 words against the new limit of 450. To make room: the profile line no longer repeats "one 12-month total per vendor", the Salesforce reread line no longer repeats the SaaS reading, which the department rule now states, and two Limits lines were merged.
- README: the deliverable links (the Google Sheet and the memo) under "What this is"; step 9 in the table; the prompt count 22; the check count 50 and D1 to D5.

## 2026-11-11: wording corrections (prompt 21, step 8)

- The memo's subject line is "Vendor review: $2,229,000 a year in savings, $1,209,000 of it in year 1" in `outputs/memo.md`, in `outputs/memo.docx` and in the workbook's CEOCFO Recommendations tab, which `scripts/05_build_sheet.py` copies from memo.md. The four extra words took the memo to 362, so the high-case sentence was tightened by two words ("The high case, $3,097,000, needs every decision and negotiation at the top of its range."): 360 words outside the table, the limit of prompt 20. `qa/memo_page_check.py` re-run on the rebuilt file (`qa/memo_page_check.md`).
- README: the re-run section no longer says the classification "was written by hand". It says the classification lines in `qa/classification_lines/` were written by Claude Code in the session, vendor by vendor, from the research findings and the rules, not typed by a person and not generated by a script, and that `scripts/classify_tools.py build NN` built each batch file from them. "What this is" says the outputs were produced in one Claude Code session, prompt by prompt, with the prompts that directed the analysis logged. The step table gains step 8 and the prompt count is 21.
- Methodology: the heading is "Tools that produced the outputs", as prompt 19 named it (step 6 had shortened it); the prompts line says twenty-one; the manual-review line says what was done. To keep the tab at 400 words, six other lines lost a word or two without losing a fact (the cleaning, research-agent, prompt 15, web-verification, second-pass and data-provider lines; the evidence line no longer repeats prompts/log.md, which the Prompts section names).
- Manual review: of the 25 largest rows (78.5% of spend), 13 were checked against their source links and 12 are well-known vendors read against the reviewer's own knowledge; the Top 3 and the memo were read line by line; no changes. Recorded in `qa/manual_review.md`, the README and the methodology. Which rows fall in each group is not recorded.
- `qa/memo_page_check.py` no longer asks Pages to open the file through AppleScript. In this step Pages was not running, AppleScript's launch command failed with error -600, and once Pages was started its AppleScript open command answered "memo.docx can't be opened right now; Pages couldn't read the file" (one alert per try, five in all) while every later event timed out behind the alerts (-1712); the file itself was sound (python-docx and unzip read it). The check now puts the file in Pages with the open command (Launch Services, which also starts Pages), waits for the document, exports it as PDF by AppleScript and closes it; a document of the same name left open by an earlier run is closed first. The rebuilt memo renders to one page with 9.4 lines to spare, the same geometry as step 7.
- No batch, savings or check script changed; the rebuild re-ran every check and both self-tests on the same 386 rows. The step 7 entry's count of Terminate rows saving under half their spend is corrected from 57 to 53: four rows sit a cent under half through rounding and the check's tolerance leaves them out.

## 2026-11-11: final corrections (prompt 20, step 7)

### 1. The memo fits one page

- `outputs/memo.md` is rewritten to 358 words outside the table (limit 360): To, From and Date on one line, the Subject on the next; the decision values tie to the table (the remote operating model is worth the Office exit line's base minus its fallback, $448,000, not the $466,000 of the decision table, which also carries the telecom lines; the shared functions $455,000 as before, with the bracketed breakdown dropped); one date for both decisions, December 15, 2026, and the cost of each month of delay, $75,000, one twelfth of the two values together, written by `scripts/03_savings.py` in a new "Cost of delay" section of `savings_summary.md`; the Salesforce bullet names the contract, the usage data and group procurement; the 30-to-90-day line puts the travel and expense policy in place instead of stopping perks and card spend; the retention risk says benefits and a hub space stay; the words around every figure were checked against what the figure contains (the 67 are the rows not verified online, the $171,000 names every kind of payee in it, the high case is every decision and negotiation at the top of its range).
- `scripts/06_build_memo_docx.py` sets single spacing with 2 points after each paragraph and no blank lines, the table columns at 3.4, 1.0, 1.0 and 1.6 inches in the table grid and in every cell with a fixed layout, 9.5-point cells, "What it needs" cells of at most five words and no count of landlords; the row labels were shortened so that each row is one line (widths measured in Calibri from Word's own font files before building).
- `qa/memo_page_check.py` renders the file to `outputs/memo.pdf` and measures it. Microsoft Word on this machine refuses the AppleScript save-as command (error -1708 for every format, also in its own container folder), so Pages exports the PDF (Calibri and Calibri Bold embedded) and macOS PDFKit reads it back: one US Letter page, 36 text lines, the lowest line 139.6 points (1.94 inches) above the bottom margin, 9.4 lines to spare at 14.8 points a line, the header on one line, the four table rows 17.4 points apart (one line each). Result in `qa/memo_page_check.md`. A probe copy with eight extra lines was tried first; Pages opened the probe files only intermittently, so the check measures the rendered page instead.

### 2. Top 3

- Assumptions in the present tense. The office line counts providers and countries from the rows: seven providers in six countries (The Office Group, Zagrebtower, IndiQube, GPT Space & Co, WeWork, WorkEZ, Common Desk; the UK, Croatia, India, Australia, Singapore and the US); JLL, CBRE and the Zagrebtower charges are on the same saving line but are not providers. "Any Salesforce agreement the group holds" replaces "the group's Salesforce relationship" there and in `V0002`'s rationale, which is a fact about the group the file does not show.

### 3. Sheet text: 174 cells on 172 rows

- Decision-led rationales: every row whose saving rests on a group decision (118 rows: a saving line tagged with a decision and a base saving above zero) leads with the group function it moves to and gives the vendor-only fallback second; the four named (Jensten, 4i, Infosys, Weking) and 114 others reworded. Check V10, with the decision phrases listed in `qa/check_outputs.py`, fails when the phrase is missing, the fallback is missing on a line that has a without-decision case, or the fallback comes first.
- Corporate-group wording removed (AWS, LinkedIn, Microsoft 365, npm, the Amazon marketplaces, PDF Butler, Slack, Trello and Atlassian, Papertrail and SolarWinds, the ICICI insurers). C12 now requires naming only for duplicate records of one vendor: the five merge groups and the same-brand link groups (Telefónica, HR Solution International, Bupa, Allianz Australia, Acclime, Apple, GRT Hotels, DHL); `groups()` marks them `duplicate`.
- "of not acting:" replaced by a plain clause (`V0015`, `V0030`); "excluded from the savings base" by "no saving counted" (17 rows; C15 updated); "the parent's" by "the group's" (7 cells).
- `V0022`'s risk note no longer cites WeWork's reported Singapore cuts: the log mentions a report but records no source for it. `V0018`'s note keeps the Gordons Partnership merger, whose source (the firm's announcement, fetched in the second pass) is now in `qa/verification_log.csv` and `qa/research/logs/claude_log.csv`.
- Every Terminate row whose base saving is under half its spend (53 rows; four more sit a cent under half through rounding and are not counted, corrected from 57 in step 8) says why in a clause: the pay passed through on employer-of-record rows, the processing fee on payroll rows, "stopped until Finance confirms" on unidentified payees, no saving counted on deal and one-off costs, and the budget line's rate on small marketing and software rows. Check V11, with a cent of tolerance for 50% lines.
- Office rows labeled Consolidate start "Consolidate the offices into one hub space under a remote operating model: exit this space" (JLL and CBRE, property advice rather than space, use the same opening and say the advice ends with the exits); the hub's own lease (`V0007`, Optimize) says keep and right-size.
- Weking's rationale starts with Finance confirming the contract and the work, since a company founded in 2023 is the eighth-largest vendor.

### 4. Workbook

- Column I reads "No saving counted: " and the reason for every row whose base saving is zero, by saving line (`ZERO_SAVING_REASONS` in `scripts/05_build_sheet.py`; the build stops on a zero without a reason); column J is headed "Vendor identified online (Yes/No)"; column H shows whole dollars through its number format, while the values stay exact so that the column still sums to the base saving to the cent.

### 5. Methodology, README and the manual review

- The methodology opens with the repository address and says "Twenty prompts directed the analysis; they are logged in prompts/log.md in the order given": the log is not called verbatim, because one housekeeping omission is marked in it. The README says the same. Both record the manual review in one line.
- `qa/manual_review.md` records the reviewer's check of the 25 largest rows (rows 2 to 26, $6,194,521 of $7,887,360, 78.5% of spend) against their source links and the line-by-line read of the Top 3 and the memo: no changes.

### 6. Where it is implemented and checked

- `qa/check_outputs.py`: C12 and C15 reworded, V10 and V11 added with three planted errors (82 in the self-test); `scripts/merge_validate.py` (the check list); `scripts/03_savings.py` (cost of delay); `scripts/05_build_sheet.py`; `scripts/06_build_memo_docx.py`; `qa/memo_page_check.py` (new); `outputs/batches/*.csv`; the documents, the README and `docs/recommendation_rules.md`. All 49 checks pass; both self-tests pass, with 82 and 16 planted errors.

## 2026-11-11: Top 3, memo, methodology, README and sheet workbook (prompt 19, step 6)

### 1. Rules for everything a reader sees

- The readers are the CEO and CFO of the group and the people assessing the work; none has seen the repository. The Top 3, the memo and the methodology (which go into the sheet) carry no project vocabulary (lever, cluster, depends_on, hint, batch); check D3 enforces it on the three documents and C19 on the reader-facing columns, where the two cells that said "lever" were reworded.
- American English everywhere a reader sees it: the four documents and the description, rationale and risk_note columns. 81 cells on 57 rows changed (programme to program, licence to license, centre to center, organisation to organization, labour to labor and the rest); check C20 covers the columns and D4 the documents, each against a list of common British forms.
- "The acquired business" and "the group"; group decisions presented as decisions with their value, never as facts about the group; plain, short sentences, past tense about the work.

### 2. Presentation figures

- `scripts/03_savings.py` writes `outputs/analysis/savings_summary.md`: every figure rounded to the nearest $1,000, every total the sum of the rounded lines above it, so that parts add to totals; percentages are whole numbers of the rounded total. Spend $7,887,000; base saving $2,229,000 (28%), low $1,566,000, high $3,097,000; year 1 $1,209,000; vendor action alone $1,264,000; the three opportunities and the second wave with their values; $274,000 that falls away without action; $171,000 that must not be cut; 319 of 386 rows verified (99% of spend); the second-pass figures from `qa/second_pass_review.csv`.
- Check D1 confirms that every dollar figure and percentage in the four documents appears in a file under `outputs/analysis` or `qa`; D2 that every table with a Total row adds up. Both have planted errors in the self-test (five document cases, 79 planted errors in all).

### 3. The documents

- `outputs/top3_opportunities.md`: the three opportunities ranked by base saving (office exit $669,000; back-office services to the group's shared functions $653,000; the Salesforce platform agreement $515,000), each with a title of at most 12 words, an explanation of 70 to 100 words (99, 100 and 99) and the base figure, then one line on the second wave and one on the spend that falls away. The Salesforce text says the product runs on the platform, the negotiation is price and terms, never exit, and the figure is the value of a negotiation that starts when the contract and usage data arrive.
- `outputs/memo.md` and `outputs/memo.docx`: one page to the CEO and CFO from Chaitanya Laxman, dated November 11, 2026, 429 words outside the table (limit 430), in the order asked: subject with the number, bottom line, context, the four-row table with its total, decisions needed with their value against vendor action alone and the date needed, the plan in four periods with one line on how it is run, four risks, what is not counted, one line on scale. `scripts/06_build_memo_docx.py` builds the Word file (US Letter, 0.75 inch margins, 10.5 point, the table as a table) and prints the word count.
- `outputs/methodology.md`: 398 words in short lines under Approach, Tools, Prompts and Validation and evidence, closing with the limits. The tools are stated as used: Claude Code CLI with Claude Opus 5.5 to the classification and Claude Fable 5.1 after, research agents, Python 3.11 with openpyxl and python-docx (the tables are CSV through the standard library; pandas was not needed), web search and fetch, git and GitHub.
- `README.md`: what this is, results in five lines, the steps with prompt numbers and commits, the repository map, how to re-run, the checks and evidence, assumptions and limits, and the note that the names and costs were modified by the provider of the data. `docs/evidence` was already removed in step 5; no other empty folder or stray file remained.

### 4. The sheet workbook

- `scripts/05_build_sheet.py` opens the raw workbook from a binary handle and saves the filled copy as `outputs/sheet/Vendor Analysis Assessment - Chaitanya Laxman.xlsx`; the raw file is never written. The Department dropdown (B2:B387 from Config) is kept. The vendor tab gets B, D and E filled in the original order and six new headed columns in the header's own style: F Rationale, G Key risk, H Estimated annual saving (USD, base case), I Savings opportunity, J Verified online (Yes or No), K Source. The Top 3 tab gets the titles in B, the explanations in C and D headed "Estimated annual savings (USD)"; the Methodology tab the methodology lines from row 2; the CEOCFO Recommendations tab row 2 "Memo (Google Doc): [link to be added]" and then the memo, one line per row with its table across columns A to D.
- `verify()` in the same script reads the workbook back and confirms every cell against the source files, the names and costs against the raw file, the row order, that every department is in the Config list, that the dropdown is there, and that column H sums to the base saving to the cent; `qa/check_outputs.py` runs it as check W1.

### 5. Where it is implemented and checked

- `scripts/03_savings.py` (the summary), `scripts/savings_model.py` (rounding helpers, the must-not-cut list shared with the insights), `scripts/05_build_sheet.py` and `scripts/06_build_memo_docx.py` (new), `outputs/batches/*.csv` (the American-English pass), `requirements.txt` (openpyxl, python-docx), `docs/recommendation_rules.md` (the American-English rule).
- `qa/check_outputs.py`: C20, D1 to D4 and W1, run by `scripts/merge_validate.py` and listed in `qa/validation_report.md`; the self-test adds a British-English row, a risk note that says "lever" and five document cases, 79 planted errors in all. All 47 checks pass; both self-tests pass, with 79 and 16 planted errors.
- Every script named in the README was run in order from a clean copy of the committed tree with a fresh virtual environment before this step was committed.

## 2026-11-11: second-pass review and reader-facing text (prompt 18, step 5)

### 1. The working files are in the repository

- Everything that produced the classification is copied from the session's scratch space, as it ran: the research brief (`prompts/research_brief.md`), the agent input lists, findings, lookup logs and failed attempts (`qa/research/`, with a README), the per-batch classification lines (`qa/classification_lines/`), and the three scratch scripts, with their paths pointed at the repository: `scripts/classify_tools.py` (the batch builder and log assembler), `scripts/research_inputs.py` and `scripts/build_hints.py`. 97 files; 27 URLs that carry a private individual's name are withheld in them as in the assembled log (step 3b). Two downloaded third-party documents were not copied. `docs/evidence` stayed empty and is removed.

### 2. The known error and its cause

- `V0116` Orionw LLC is a Singapore boutique law practice in technology, media, telecoms and fintech (identified by the user; its own site, fetched by the main session and logged, confirms it). The first pass had it as an outsourced IT contractor: the research agent's first query carried hint 60's framing ("Orionw LLC software development"), the second was the bare name, both found nothing, and the builder's rule for unverified rows then kept the hint's reading as the best inference with "confirm with Finance". The row moves to Legal, cluster Legal, Consolidate into the group's law firm panel, verified TRUE, confidence high; its lever is Law firms and legal resourcing.
- The same cause, a hint followed where the search found nothing, applies to every row that was both unverified and hinted: 24 rows. All were re-verified fresh in Stage 2. Three had the wrong reading: `V0116`; `V0065` Pingo, a Zagreb painting and glazing contractor rather than an unidentified payee (now Facilities, a one-off decorating contractor); and `V0358` Platinum Office, a Split business consultancy rather than the office-supplies company of hint 76. Four were confirmed (`V0074`, `V0106`, `V0176`, `V0315`), and the rest stayed unfound.

### 3. Stage 1, all 386 rows, no web

- Four reviewer agents that had not seen the classification read each row's research finding beside the final department, sub_function, cost_cluster, recommendation and description, with the three rule documents, and flagged every row where the final row does not follow from the finding, follows a hint the finding contradicts, or breaks a rule. 18 rows were flagged (25 flag lines); agreement by field was 98.2% to 99.7%. Every flag is resolved in `qa/second_pass_review.csv`: 11 rows changed (`V0038`, `V0096`, `V0117`, `V0127`, `V0141`, `V0182`, `V0213` description, `V0224`, `V0330`, `V0349` and the `V0121` wording), the rest kept with a reason, among them the step 4b decisions on `V0057` and `V0121`, the register's placement of seconded lawyers (`V0033`), and the step 3 research findings on Computershare-Caboodle (`V0211`) and trendig (`V0213`), which the rule documents now record (C8 and T3 amended).

### 4. Stage 2, fresh verification

- Agents that saw neither the hint nor the first-pass row established from the vendor's own site or a reliable directory what each vendor does, in order: the Stage 1 flags, the 24 same-cause rows, every row at or above $10,000 (77 rows), then a seeded random sample of 30 of the rest (seed 2026). 142 rows, $7,500,631 (95.1% of spend); the search limit was never reached and no planned row was left unfinished. Agreement with the first pass: 96.5% on every field (5 rows disagreed: `V0065`, `V0116`, `V0127`, `V0279`, `V0358`); 16 more rows were reworded for precision; 14 rows the first pass could not verify now are (`V0018`, `V0065`, `V0106`, `V0116`, `V0127`, `V0129`, `V0176`, `V0210`, `V0225`, `V0244`, `V0271`, `V0279`, `V0315`, `V0358`), so the verification exceptions fall from 81 to 67.
- Findings that change a row's reading: Calm Achiever (`V0127`) is an Indian productivity-training business, now Consolidate into the group's development programmes on the training lever; Treći Posao (`V0279`) is a Split restaurant operator, now a team-meal row; Weking (`V0009`) is confirmed in the Croatian register as a Rijeka software development company founded in 2023, so the entity is no longer unconfirmed (the work still is) and its confidence rises from low to medium; Bisley Law (`V0018`) merged into Gordons Partnership in January 2024, which explains the non-trading entry and sharpens Finance question 7. Nefron (`V0038`) and Mosaic Concept (`V0096`), registered as organisers of meetings and fairs, move to Marketing and the events cluster, still Terminate until Finance confirms what they supplied.
- The vendor names in this data were modified by the provider, so a name the web does not confirm is a question for Finance, never evidence of a problem with the payee (step 4b). The review report says so.
- `qa/second_pass_review.csv` (187 rows: every flag and every covered vendor, with first-pass value, reviewer finding, verdict and resolution) and `qa/second_pass_report.md` (what each stage looked for, coverage, agreement by field, every disagreement, every row changed before and after, what was not covered) are written by the review script from the scratch files.

### 5. Text a reader of the sheet will see

- Every description, rationale and risk note that referred to the project's own workings (hints, the Optimize and Terminate lists, rules, searches, sources, steps, prompts or files) now states the fact or the action directly: 263 cells rewritten in the text pass, 282 with the review's refinements. Where what a vendor does is not established, the description gives the best reading and ends "(unconfirmed)" in place of "confirm with Finance" (the 67 unverified rows and a few whose product is not shown).
- The ten Office footprint rationales lead with the base case the savings assume (exit under the remote operating model, keeping one touchdown space at the engineering hub), then the fallback (one flexible provider).
- A risk note is required on every Optimize row at or above $25,000: one clause naming the main risk of acting, or of not acting where the row must not be cut (`V0015` Telefónica, `V0030` student labour). Eleven rows gained one; `V0002` already had one, and its step 3b exception is now covered by the threshold.

### 6. Where it is implemented and checked

- `outputs/batches/*.csv` (29 rows changed by the review, 185 by the text pass), merged into `outputs/vendors_classified.csv`; `qa/verification_exceptions.csv` (14 rows removed); `qa/verification_log.csv` and `qa/research/logs/claude_log.csv` (the OrionW lookup); `docs/taxonomy.md` (T3), `docs/clusters.md` (C8), `docs/savings_assumptions.md` (the lever rows and analyst calls for `V0009`, `V0065`, `V0116`, `V0127`), `docs/recommendation_rules.md` (the reader-facing rules), `scripts/savings_model.py` (`V0127` to the training lever; `V0065` off the unidentified lever), `scripts/04_insights.py` (the Bisley Law and Weking wording).
- `qa/check_outputs.py`: C16 requires a risk note on every Optimize row at or above $25,000 and none on smaller ones; C19 fails any of the three columns that carries a workings phrase (`WORKINGS_PHRASES`); V9 lists every Terminate row on a lever with a base below 50% outside the Excluded opportunity and every Optimize row on a lever above 50%, and passes only where each has a recorded reason (`RECOMMENDATION_LEVER_EXCEPTIONS`: employer-of-record and payroll providers, whose levers save the service fee; Terminate rows on the Other marketing and Other software levers, where the lever's rate is set across the budget; Optimize rows on the Office footprint and Office running costs levers, which fall with the space under the remote operating model rather than by a vendor action). C14 expects "work unconfirmed" on `V0009`, "oem terms unconfirmed" on `V0006` and "invoicing entity" on `V0018`; C13 expects `V0009` at medium confidence. Six planted errors are added, 72 in all; `scripts/merge_validate.py` prints the cross-tab of recommendation by lever in `qa/validation_report.md`.
- All 41 checks pass; both self-tests pass, with 72 and 16 planted errors.

### 7. Result

From `outputs/analysis/savings.md`, after the review: run-rate saving $1,565,930 / $2,229,687 / $3,095,673 (base 28.3% of spend; $2,247,704 before the review), without any acquirer decision $1,263,566, year 1 $1,208,570. By opportunity (base): Salesforce platform agreement $514,601; Office exit $669,290; Back office into group shared services $653,457; Second wave $392,339. Recommendations: 125 Optimize, 110 Consolidate, 151 Terminate.

## 2026-11-11: assumption decisions (prompt 18, step 4b)

The seven points raised in step 4 (section 4 of the next entry), decided:

1. **Employee hardware** is a lever of its own: the nine hardware rows (`V0066`, `V0123`, `V0131`, `V0167`, `V0172`, `V0175`, `V0229`, `V0260`, `V0378`) and Shree Info System (`V0048`); 5 / 10 / 20; without decision 5; 0.6; `group_it_procurement`. The rest of the cluster keeps the lever, now named "Other cloud and IT".
2. **MultiSport stays.** Benefit Systems (`V0057`) is an employee benefit at the engineering hub: recommendation Optimize, rationale to keep it and review take-up and the employee co-payment, no risk note, lever unchanged at 0%. Gym4You (`V0121`) becomes Consolidate into the MultiSport card, on the Team events, perks and wellness lever (60% base), with the risk note that the gyms staff use must be in the MultiSport network first.
3. **Bisley Law stays on the law-firms lever.** Whoever the payee proves to be, the spend is legal work that follows that lever; the payee check is a control action, not a savings assumption. The finding is reworded wherever it appears (the row's description, rationale and risk note; Finance question 7; the step 3b entry; `insights.md`). The provider of this data modified vendor names, so a name that matches no trading firm is a question for Finance, not evidence of a problem. The same caution applies to every statement about unmatched or unverified names: in `insights.md` (sections 4 and 10) and in this file, where the step 3 and 3b entries record what the searches found and this entry records how to read it.
4. **Salesforce:** no change to the model. The documents present the figure as the value of a negotiation that starts when the contract and usage data arrive; the register's reasoning says so.
5. **Unidentified and individual payees:** no change. One-off payments to individuals are a control finding and carry no saving; the one-off lever's reasoning says so.
6. **Couriers and postage** is a lever of its own: the nine courier, postage, delivery and mail rows of Office running costs (`V0196`, `V0232`, `V0240`, `V0303`, `V0316`, `V0336`, `V0368`, `V0371`, `V0377`); 5 / 10 / 20; 0.6; no tag. The two Amazon marketplace rows stay in Office running costs.
7. **Weking:** no change to the model; its share is marked provisional in the register (the lever's "Applies to") and in `insights.md`, until Finance answers question 3.

The External training and coaching lever is confirmed as set in step 4.

Where it is implemented: `docs/savings_assumptions.md` (the two new levers, the renamed lever, the reworded cells, the analyst-call table); `scripts/savings_model.py` (the lever map); `outputs/batches/batch_01.csv`, `batch_02.csv` and `batch_04.csv` (`V0018`, `V0057`, `V0121`), merged by `scripts/merge_validate.py`; `qa/check_outputs.py` (C13 expects Optimize for `V0057` and Consolidate for `V0121`; C14 expects "invoicing entity" in the `V0018` risk note; one planted error added, 67 in all); `scripts/04_insights.py`; and the savings and insights files re-run.

## 2026-11-11: savings model and insights (prompt 17, step 4)

### 1. The register

- A tenth acquirer decision, `group_engineering_sourcing`: the contractor consultancies are replaced by the group's own engineering sourcing. It carries the Outsourced engineering and contractors lever (`V0009`, `V0019`, `V0116`, `V0185`), which closes the second open point of step 3b.
- The Salesforce levers are restated for the platform reading, the first open point of step 3b: the lever on `V0002` is the platform agreement renegotiated at change of control, with internal seats trued down separately. It is a vendor action and carries no tag; co-terming with the parent's Salesforce relationship is part of that action and gets no tag of its own. `parent_crm_instance` now reaches only HubSpot.
- Every lever carries `pct_low`, `pct_base` and `pct_high` (run-rate saving as a share of 12-month spend), `pct_without_decision` (what vendor action alone achieves if the tagged decision is not taken; equal to the base on untagged levers), `year1_factor` (0.5 where the renewal or notice date is unknown, higher for policy changes that start within 90 days, lower where the change waits for a year-end or a migration), `depends_on` and one sentence of reasoning.
- The vendor actions of step 2f are now the Salesforce platform agreement, AWS and Navan; the insurance re-broke is the without-decision case of the commercial insurance lever rather than a lever of its own. `group_it_procurement` keeps its row, but no lever carries it, because the assumption given for employee hardware is a vendor action (section 4).
- 39 levers in five opportunities: Salesforce platform agreement (4 levers), Office exit (2), Back office into group shared services (15), Second wave (12), Excluded (6). Each row ends with exactly one lever, in the order of precedence written in `docs/savings_assumptions.md` and coded in `scripts/savings_model.py`.

### 2. Levers added or split beyond the assumptions list

- Added with its own percentages: External training and coaching (`V0020`, `V0075`, `V0079`, $87,694; 25 / 50 / 75; without decision 25; 0.75; `group_talent_function`), because the list has no line for training and the rows are Consolidate into the group's development programmes. Open for confirmation.
- Added at 0%: Bank, payment and certification fees (`V0216`, `V0198`, `V0142`, $5,299), because the list has no line for them and the fees follow transaction volume or the certificates customers ask for.
- Split by tag: HR and finance systems (`group_systems`) and HubSpot (`parent_crm_instance`) share their percentages, not their tag; Employer-of-record providers (without decision 0) and Payroll processing providers (without decision 10) are two levers under `group_payroll`.
- Split by sub_function inside a cluster: AWS, the telecom lines and the rest of Cloud, telecom and IT; the agencies, TM Forum and the rest of marketing; the auditors, the secretarial providers, the contingent-fee adviser and the fees inside the audit cluster; the brokers, the insurers and the statutory cover and benefit schemes inside Insurance and benefits.
- Statutory cover and benefit schemes also holds the statutory occupational health rows, which are not addressable, so that every row outside the savings base sits on a 0% lever.
- No other row fits the employment-law test: `V0202` is a recurring relationship and `V0264` a US firm whose one-off payment is not shown to be settlement advice.

### 3. Rows whose lever is an analyst call

Recorded in `docs/savings_assumptions.md` ("Lever assignment") and repeated in `outputs/analysis/savings.md`:

| Row | Lever | Why |
|---|---|---|
| `V0351` Mithras Consultants | Audit, tax and accounting firms | actuarial valuations are an accounting requirement, so they follow the group auditor |
| `V0211` Computershare-Caboodle | Other software subscriptions | a benefits platform fee, not pay or cover |
| `V0098` Mercer, `V0273` Doctor Anywhere | Employee health and life insurance | benefits consulting and a health benefit |
| `V0057` Benefit Systems, `V0121` Gym4You | Statutory cover and benefit schemes | the gym schemes the assumption names, although both are Terminate in the classification |
| `V0058` Smart Group Services | Payroll processing providers | HR outsourcing, unconfirmed; the closest lever |
| `V0179` Radius Group | Employer-of-record providers | global payroll and expansion services |
| `V0020` Big Frontier, `V0075` Ramiro, `V0079` Emerge | External training and coaching | the lever added above |
| `V0065` Pingo, `V0074` Bijeli Pijesak, `V0137` Orcola | Unidentified and individual payees | Terminate until identified, not the engineering sourcing lever of their cluster |
| `V0309` Avoxi, `V0363` Click Send | Other cloud and IT, including employee hardware | telephony and an SMS API that do not end with the offices |
| `V0168` Cision | Other marketing, media and events | a press release wire, not an agency |
| `V0076` Visalogic | Law firms and legal resourcing | immigration work follows the legal cluster into the panel |
| `V0216` Raiffeisenbank, `V0198` FastSpring, `V0142` Bureau Veritas | Bank, payment and certification fees | the lever added above |
| `V0203`, `V0291` Amazon marketplaces | Office running costs | they follow their cluster as office consumables |

### 4. Where the data argues against an assumption

The assumptions are kept as given (prompt 17); these are the proposed changes, each decided in step 4b (the entry above).

1. **Employee hardware carries no tag.** The nine hardware rows and the Chennai distributor (`V0048`) sit in Other cloud and IT at 10% with no tag, while their rationales name group IT procurement (step 2e) and `group_it_procurement` is a registered decision with no lever. Proposed: a separate Employee hardware lever at the same 5 / 10 / 20 with without-decision 5 and the tag, or retire the decision.
2. **The gym schemes are Terminate at 0%.** Benefit Systems (`V0057`, $16,900) and Gym4You (`V0121`, $3,692) are Terminate in the classification (a perk with no commercial case) but 0% here under the gym-schemes line. Proposed: the Team events, perks and wellness lever (40 / 60 / 75) for both, worth $12,355 base, or Optimize in the classification.
3. **Bisley Law is a control finding at 30%.** `V0018` ($67,414) takes the law-firms lever, yet the finding of step 3b says no payment should continue until Finance confirms the entity. Proposed: hold it at 0% until Finance answers question 7, or model it like an unidentified payee at 50%; the law-firms lever would then be $52,289 minus $20,224 base.
4. **The Salesforce base rests on an unread contract.** The forensic pass said no Salesforce saving should be sized before the contract is read; the model sizes 15% of $3,117,226 at the prompt's request. The figure is the value of a negotiation the company cannot start until the contract and the usage data arrive (requests 2 and 3 in `insights.md`).
5. **The one-off rule removes every individual from the unidentified-payee lever.** The six individuals and 13 other unidentified rows are non-recurring, so they sit in One-off spend that falls away at 0%; the lever holds the cluster's 18 recurring rows and the three unidentified contractors. Proposed: treat Unidentified and individual payees like the two recurring categories, so the stop-until-identified saving applies to the whole cluster ($50,939), worth $25,470 base rather than $17,809.
6. **Couriers and marketplaces follow the office.** Eight courier and postage rows ($2,519) and the two Amazon marketplace rows ($1,340) take the Office running costs lever at 70% with `remote_operating_model`, although a remote company still ships parcels and the card policy removes the marketplaces whatever the office decision. Immaterial; proposed: 10% and no tag for the couriers.
7. **Weking's saving rests on an unconfirmed entity.** The largest row under `group_engineering_sourcing` (`V0009`, $43,228 base) is a vendor whose entity Finance has not confirmed (question 3); the saving is provisional until it does.

### 5. Where it is implemented

- `docs/savings_assumptions.md`: rewritten, with the tenth decision, the five numbers per lever, the reasoning, the order of precedence and the analyst calls. `docs/recommendation_rules.md` names ten decisions and the restated vendor actions.
- `scripts/savings_model.py` (new): the register parser, the lever map and the order of precedence, the figures, the roll-ups and the reconciliation. `scripts/03_savings.py` (new): writes `outputs/analysis/savings.csv` (one row per vendor, full precision) and `outputs/analysis/savings.md` (whole dollars: totals, excluded spend by reason, savings by opportunity, cluster and lever, the assumptions, the acquirer decisions with the value of each, the 15 largest vendor savings, the savings on non-recurring rows, the reconciliation and the analyst calls), then runs the savings checks. `scripts/04_insights.py` (new): writes `outputs/analysis/insights.md` from the files in the repository, checking that every row it names carries the fact it is used for.
- `qa/check_outputs.py`: savings checks V1 to V8 (low <= base <= high; without decision <= base; year 1 = base times a factor between 0 and 1; no saving on a non-addressable or M&A row; no saving above spend; every row has one registered lever with the register's values and every lever is used, with the rows matching the classification; every tag is a registered decision; the roll-ups in `savings.md` equal the sums of the rows). They run once `savings.csv` exists, in `run()` and from `03_savings.py`. The self-test builds synthetic savings rows from the synthetic classification and the real register; 13 planted errors are added, 66 in all. S6's vendor actions are the three above, and `retag` finds the `depends_on` column by its header.
- `scripts/merge_validate.py`: passes the savings paths to `run()`, so `qa/validation_report.md` lists the V checks (39 checks); its self-test passes paths that do not exist, so they show as pending there.
- All 39 checks pass; both self-tests pass, with 66 and 16 planted errors.

### 6. Result

From `outputs/analysis/savings.md`:

| Measure | Value |
|---|---|
| Total spend | $7,887,360 (386 rows) |
| Recurring base | $7,556,683 (95.8%) |
| Spend on levers with a base above 0% | $7,319,579 (92.8%) |
| Run-rate saving, low / base / high | $1,577,593 / $2,247,348 / $3,113,593 (base 28.5% of spend) |
| Without any acquirer decision | $1,283,210 (16.3%) |
| Year 1 | $1,221,188 (15.5%) |
| By opportunity (base) | Salesforce platform agreement $514,601; Office exit $671,503; Back office into group shared services $650,213; Second wave $411,030; Excluded $0 |
| Value of each decision (base with it minus without it) | `remote_operating_model` $467,473; `group_auditor` $138,410; `group_talent_function` $131,906; `group_systems` $71,233; `group_engineering_sourcing` $43,267; `group_legal` $34,859; `group_insurance_programme` $34,776; `parent_crm_instance` $22,531; `group_payroll` $19,681; `group_it_procurement` $0 |

The Top 3, the methodology, the memo and the README are not written in this step.

## 2026-11-11: SaaS department reading (prompt 17, step 3c)

### 1. The reading

- The workbook's `Config` list names the functions of a software company: Engineering, Product, Support, Professional Services, SaaS, Sales, Marketing, G&A, Finance, Legal, Facilities, M&A. Read that way, SaaS is the function that runs the hosted product, not a label for any software subscription. A department answers "whose budget is this", and the platform the product runs on, its hosting and the tools that keep it running are the SaaS function's budget.
- The alternative reading, SaaS as a bucket for subscriptions with no single owning function, was the rule from prompt 6 until this step. It put $151,092 of company-wide tools (Google Workspace, Microsoft 365, Slack, Atlassian and the rest) under SaaS and left the platform, hosting and monitoring in Engineering. It answers "what kind of purchase is this" rather than "whose budget is this", which is the question the department column asks.
- Under either reading the platform and hosting rows fit SaaS: Salesforce, PDF Butler, AWS, Papertrail, SolarWinds, UptimeRobot, GoDaddy and DNSimple are subscriptions to hosted services and the cost of running a hosted product. Only the company-wide tools move with the choice of reading, and they go to G&A as corporate IT.

### 2. The rule

`docs/taxonomy.md` rule 2 is rewritten, and rules 1, 7 and 9, the departments table and tie-breaks T2 and T5 follow it:

- SaaS holds the platform and hosting the product runs on and the tools that keep it running: platform and ISV licences, cloud hosting, monitoring and logging, DNS and domains, and third-party components delivered with the product.
- Company-wide software with no single owning function (productivity suites, messaging, meetings, e-signature, password management, automation and work-management tools) goes to G&A, with a `sub_function` that starts "Corporate IT".
- Software used by one function stays with that function. Developer tools stay in Engineering.

`docs/clusters.md` changes only its sentences on Slack and PDF Butler; no cluster moves.

### 3. Rows moved

23 rows. A description changed only where it named the owning team (seven rows, where "engineering" becomes "SaaS operations"); every other column is kept.

| Row | From | To | Other change |
|---|---|---|---|
| Salesforce UK Ltd (`V0002`) | Engineering | SaaS | none |
| Cloudcrossing BVBA, PDF Butler (`V0006`) | Product | SaaS | none |
| Amazon Web Services (`V0014`, `V0103`) | Engineering | SaaS | description ends "for SaaS operations" in place of "run by engineering" |
| Papertrail (`V0130`), SolarWinds (`V0311`), UptimeRobot (`V0350`) | Engineering | SaaS | description ends "used by SaaS operations" in place of the engineering team |
| GoDaddy (`V0214`), DNSimple (`V0278`) | Engineering | SaaS | description: "used by SaaS operations for the company's domains" |
| Cloud Technology Solutions (`V0023`), Microsoft Ireland (`V0081`) | SaaS | G&A | sub_function "Corporate IT: productivity suite (Google Workspace, resold)" and "(Microsoft 365)" |
| Veniture (`V0032`), Trello (`V0091`), Smartsheet (`V0145`), Atlassian (`V0297`) | SaaS | G&A | sub_function "Corporate IT: work management ..." or "Corporate IT: Atlassian licences and partner services" |
| Workato (`V0060`), Zapier (`V0310`) | SaaS | G&A | sub_function "Corporate IT: integration platform (Workato)" and "Corporate IT: workflow automation (Zapier)" |
| GoTo (`V0089`), Slack (`V0173`) | SaaS | G&A | sub_function "Corporate IT: meetings, calling and remote access (GoTo)" and "Corporate IT: workplace messaging (Slack)" |
| Adobe (`V0117`), DocuSign (`V0194`), FormSwift (`V0281`), LastPass (`V0288`) | SaaS | G&A | sub_function "Corporate IT: design and document software", "e-signature", "online document forms", "password manager" |

- The Google reseller (`V0023`) goes to G&A, not SaaS: its verified description and its log entry show Google Workspace licences for all staff, not cloud hosting.
- Rows considered and left where they are: NCC software escrow (`V0144`, Engineering: a customer-contract safeguard, not hosting); Click Send (`V0363`, Engineering: nothing shows the SMS API is delivered with the product, T5); the developer tools JetBrains, npm, AG Grid and GitKraken, with Backoffice Associates and Make And Grow (Engineering); Kimble (Professional Services, rule 1); Yoxel (Sales, internal-CRM tooling); Aha! and Figma (Product); Epignosis and Pluralsight (G&A as HR and training software, not corporate IT); Google Ireland (`V0043`, Marketing, most likely Google Ads).

### 4. Where it is implemented

- `outputs/batches/batch_01.csv` to `batch_09.csv`, merged by `scripts/merge_validate.py` into `outputs/vendors_classified.csv` and `qa/validation_report.md`; `docs/taxonomy.md`, `docs/clusters.md` and this file.
- `qa/check_outputs.py`: C13 expects SaaS for `V0002`, `V0006`, the two AWS rows and the five hosting, logging, domain and monitoring rows, and G&A for Slack and the two productivity suites; C14 expects a `sub_function` that starts "Corporate IT" on `V0023`, `V0081` and `V0173`; S4 confirms the six new ids. Three planted errors are added, 53 in all.
- All 31 checks pass, and both self-tests pass, with 53 and 16 planted errors. `scripts/02_clean.py` was re-run as the docs check and passed with unchanged outputs.

### 5. Result

From `qa/validation_report.md`:

| Department | Vendors | Spend | Share of spend | Share before step 3c |
|---|---|---|---|---|
| SaaS | 9 | $3,442,832 | 43.6% | 1.9% |
| G&A | 221 | $1,714,984 | 21.7% | 19.8% |
| Facilities | 51 | $973,386 | 12.3% | 12.3% |
| Finance | 24 | $645,242 | 8.2% | 8.2% |
| Engineering | 16 | $285,673 | 3.6% | 44.6% |
| M&A | 4 | $226,932 | 2.9% | 2.9% |
| Marketing | 24 | $201,520 | 2.6% | 2.6% |
| Legal | 24 | $197,752 | 2.5% | 2.5% |
| Sales | 8 | $138,344 | 1.8% | 1.8% |
| Professional Services | 2 | $56,367 | 0.7% | 0.7% |
| Product | 2 | $4,149 | 0.1% | 2.7% |
| Support | 1 | $178 | 0.0% | 0.0% |

Recommendations, clusters, confidence and addressability are unchanged: 124 Optimize, 108 Consolidate, 154 Terminate.

## 2026-11-10: platform reclassification (prompt 16, step 3b)

### 1. Salesforce is the product platform, not the sales team's CRM

- The evidence is in the ledger. Salesforce UK Ltd (`V0002`) is 39.5% of all third-party spend, which no company pays for sales seats. Around it sit Salesforce-native vendors: a document-generation app at $209K (Cloudcrossing's PDF Butler, `V0006`), a PSA on the Salesforce platform (Kimble, `V0027`), a Salesforce consultancy supplying developers (Weking, `V0009`), a Salesforce-specialist recruiter (Mason Frank, `V0034`) and a Salesforce email-sync tool (Yoxel, `V0170`). And the company sells to telecoms, where Salesforce-native products are common.
- The Salesforce spend is therefore platform and ISV licence cost for a product built on Salesforce, with a smaller internal CRM component. Finance question 2 stays open for the split between the two.
- `docs/taxonomy.md`: rule 1 is amended. Salesforce platform licences, and Salesforce-ecosystem vendors that supply product engineering or embedded product components, go to Engineering, or to Product for an embedded component; only internal-CRM tooling goes to Sales. The departments table, rules 9 and 10 and tie-breaks T1 and T2 follow. Kimble stays in Professional Services as PSA software, and Yoxel stays in Sales as internal-CRM tooling. Superseded in step 3c: the platform licences and the components embedded in or delivered with the product go to SaaS.
- `docs/clusters.md`: Salesforce platform (cluster 1) describes Salesforce as platform and ISV licences plus internal CRM seats, and Salesforce-specialist services go to the cluster of the lever that captures their saving (C1). NSDL moves to Statutory and government (cluster 16 and C8).

### 2. Rows reclassified

Every other column rule is kept.

| Row | Changed | Kept |
|---|---|---|
| Salesforce UK Ltd (`V0002`) | Engineering. Description: Salesforce platform and ISV licences for the company's Salesforce-native product, plus internal CRM seats; the largest single cost. Rationale: renegotiate the platform agreement at change of control (co-term with the parent's Salesforce relationship, multi-year commitment, true-down of internal seats audited separately from platform licences), with Slack in the same Salesforce group renewal | Optimize; cluster Salesforce platform; one recommendation with Slack (`V0173`) in the Salesforce link group |
| Weking d.o.o. (`V0009`) | Engineering; cluster Outsourced engineering and contractors; Consolidate into the group's engineering sourcing model; risk note: product knowledge held by the consultancy's developers must be transferred first | Confidence low; `verified` TRUE on its website. The description now ends "confirm with Finance" (hint 77); before this step it said only that the legal entity is unconfirmed |
| Cloudcrossing BVBA (`V0006`) | Product. Description: a Salesforce-native document generation app that at this spend is most likely embedded in or delivered with the product, not internal sales tooling; confirm OEM terms with Finance. Rationale: renegotiate OEM or volume pricing within the platform review | Optimize; cluster Salesforce platform; confidence medium |
| Mason Frank International Ltd (`V0034`) | Cluster Recruiting and HR outsourcing, as its lever is ending the agency, not the Salesforce contract; the rationale counts its saving in the recruiting agencies lever | Terminate; G&A |
| NSDL (`V0284`) | `is_addressable` FALSE; cluster Statutory and government; the rationale ends "non-discretionary, excluded from the savings base" | Optimize; Finance |

- With NSDL, the 17 rows outside the savings base total $121,657, the forensic exclusion in section 10 of `outputs/analysis/01_forensics.md`.
- **Exception:** `V0002` is the one Optimize row with a risk note, "the product depends on this platform, so the lever is commercial terms, never exit". Every other Optimize row keeps an empty risk note, and C16 now checks both.

### 3. Bisley Law is a control finding for Finance

- Companies House lists Bisley Law Ltd (`V0018`, $67,414) as non-trading, and no website or SRA record describes its services. Finance must confirm which entity invoiced and for what before any payment continues. It is question 7 below. Reworded in step 4b: the provider of this data modified vendor names, so an unmatched name is a question for Finance, not evidence of a problem; the spend is legal work on the law-firms lever, and the payee check is a control action.
- The row stays Consolidate; its risk note now carries the question for Finance.
- Question 8 asks for the PDF Butler OEM terms that the `V0006` description refers to Finance.

### 4. URLs that name a person are withheld

- In `outputs/vendors_classified.csv`, the batch CSVs and `qa/verification_log.csv` (columns `query` and `url_found`), every URL whose address carries a private individual's name is replaced by the directory's root domain and a note. This supersedes the step 3 practice of citing a sole trader's register page whose address carries the owner's name.
- "URL withheld: names the owner": Croatian sole-trader (obrt) register pages whose address carries the owner's name after "vl." (vlasnik, owner): `V0038`, `V0240`, `V0243`.
- "URL withheld: names an individual": addresses that carry a person's name without showing that person to be the vendor's owner. These are register pages of health practices or institutions named after a doctor (`V0328`, `V0382`, `V0384`) and adviser or author profile pages (`V0017`, `V0079`, `V0153`).
- The source URL changes on `V0038`, `V0153`, `V0240`, `V0243` and `V0384`, which stay `verified` TRUE because the withheld page is still the evidence; the other four ids change only in the log. The log entry for `V0092` was already withheld in step 3.
- `V0024` (Navan, Inc) cited `https://navan.com/llm-info`, a page Navan publishes for AI tools. Its source is now the Navan rebrand press release already used for `V0003`; the log keeps the original lookup.

### 5. Housekeeping

- The step 2f heading appeared twice; the duplicate is removed.
- `scripts/00_data_profile.py` is re-run, so `outputs/analysis/00_data_profile.md` matches its script again. The only line that changes is the one on `docs/taxonomy.md`, which the committed profile still described as not yet written.

### 6. Where it is implemented

- `outputs/batches/batch_01.csv`, `batch_04.csv`, `batch_06.csv`, `batch_07.csv`, `batch_08.csv` and `batch_10.csv`, merged by `scripts/merge_validate.py` into `outputs/vendors_classified.csv` and `qa/validation_report.md`; `qa/verification_log.csv`; `docs/taxonomy.md`, `docs/clusters.md` and this file.
- `qa/check_outputs.py`: C13 expects the outcomes above, and Mason Frank's expected cluster changes from Salesforce platform to Recruiting and HR outsourcing. C14 also checks wording in risk notes and descriptions (`V0002`, `V0006`, `V0009`, `V0018`). C16 also fails an Optimize row with a risk note, except `V0002`. S4 confirms the four new ids. Six planted errors are added, 50 in all.
- All 31 checks pass, and both self-tests pass, with 50 and 16 planted errors.

### 7. Result

From `qa/validation_report.md`:

| Department | Vendors | Spend | Share of spend |
|---|---|---|---|
| Engineering | 24 | $3,519,830 | 44.6% |
| G&A | 207 | $1,563,892 | 19.8% |
| Facilities | 51 | $973,386 | 12.3% |
| Finance | 24 | $645,242 | 8.2% |
| M&A | 4 | $226,932 | 2.9% |
| Product | 3 | $212,824 | 2.7% |
| Marketing | 24 | $201,520 | 2.6% |
| Legal | 24 | $197,752 | 2.5% |
| SaaS | 14 | $151,092 | 1.9% |
| Sales | 8 | $138,344 | 1.8% |
| Professional Services | 2 | $56,367 | 0.7% |
| Support | 1 | $178 | 0.0% |

Sales falls from 45.7% of spend to 1.8%, and Engineering rises from 3.3% to 44.6%. Recommendations: 124 Optimize, 108 Consolidate, 154 Terminate.

### 8. Left for the savings step

- The Salesforce levers. The licence audit, a vendor action tagged `none`, becomes the true-down of internal seats, audited separately from the platform licences. The savings step also settles whether co-terming with the parent's Salesforce relationship needs a `depends_on` tag, and how much of the spend the CRM-instance lever (`parent_crm_instance`) can reach now that most of it is platform licences.
- Weking's Consolidate depends on the group's engineering sourcing model, which is not one of the nine registered decisions.

## 2026-11-10: classification with web verification (prompt 15, step 3)

### 1. The two pending verifications are settled

- **Sodexo and Pluxee become a merge.** The Bloomberg LEI record lists Sodexo SVC India Private Limited as the former legal name of Pluxee India Private Limited, changed on 20 May 2024. Pluxee India describes itself as formerly Sodexo Benefits & Rewards Services, an employee benefits and meal-card provider. Under the rule of step 2c this is a rename, so `V0054` and `V0128` are one relationship. Hint 36's "office catering" does not fit `V0054`, and its rationale says so.
- **The 4i merge is confirmed.** 4i Management Consulting Private Limited (Bangalore, incorporated 2018) lists directors who are partners of 4i Advisory Services, and both firms sit in Koramangala, Bangalore: one advisory practice billing through two entities. Confidence stays medium because the contracts are not visible; if Finance shows two separate engagements, the rows become a link.
- Implemented in `scripts/vsa_common.py` (merge groups 4i and Pluxee; the Sodexo and Pluxee link removed), `qa/vendor_groups.csv`, `outputs/vendors_clean.csv`, the forensics and cleaning reports (5 merges, 381 vendors, 14 link groups), `qa/check_outputs.py` (the per-row links are Amazon and Microsoft; a planted error for a split Pluxee merge, 44 in all), `docs/recommendation_rules.md` and the notes in `docs/vendor_hints.md`. The lookups are in `qa/verification_log.csv`.

### 2. How the verification was run

- Every vendor was searched on the web by its cleaned name, with the country from the legal form where it helped. Helper agents did the searching, 20 vendors each, and recorded what each source established; the classification was then written batch by batch against the docs.
- `qa/verification_log.csv` holds one row per lookup, failed ones included: `vendor_id`, `query`, `url_found`, `established`.
- A vendor that repeated searches could not establish has `verified` FALSE, confidence low, a description ending "confirm with Finance" (the form of hint 77), and a one-line reason in `qa/verification_exceptions.csv`.
- For personal names, the searches looked only for a business trading under the name; no personal details were recorded.
- The session allows 200 web searches shared by all agents, refilling at about 100 an hour. An agent whose search was refused stopped, wrote rows only for the vendors it had finished, and the rest were searched in a later run. Refused searches never ran, so they are not in the log. No vendor was marked unverified without being searched.
- Pages that addressed text to AI assistants appeared twice in search results; they were ignored and never used as sources.

### 3. Interpretations applied in the classification

- **`is_recurring`** is TRUE when the kind of spend repeats year on year: subscriptions and licences, rent, insurance, retained advisers, regular purchases such as hardware, couriers, and travel, including city hotels used for business stays. It is FALSE for one-off spend: deal costs, the data room and sponsor fees, team outings, restaurant meals and gifts bought for an occasion, office moves, resort or venue bookings for offsites, and one-off legal matters.
- **Unverified rows** (`verified` FALSE) follow the "confirm with Finance" form of hint 77. Where neither the name nor a hint shows the function, the row is an unidentified payee: G&A (T12), cluster Unidentified and individual payees unless hint 77 points to contractors (C12), and Terminate until identified. Where the name or a hint does show the function (a law firm, a caterer, a payroll firm, a tax adviser), the row follows the rule for that function and stays unverified.
- **Hints the searches overturned**, each noted in its rationale: Cloudcrossing (`V0006`, a Salesforce document app, not a consulting partner), Big Frontier (`V0020`, leadership development, not marketing), Veniture (`V0032`, an Atlassian partner), Shree Info System Solutions (`V0048`, a hardware distributor, so consolidated into group IT procurement like the named hardware vendors), Sodexo SVC India (`V0054`, Pluxee's former name), Plus Your Business (`V0056`, a HubSpot consultancy), Smart Group Services (`V0058`, a consultancy at an HR brand's address), TP Prime (`V0067`, accounting), Ramiro (`V0075`, HR training), Omonia (`V0083`) and Akton (`V0141`, telecoms), Mosaic Concept (`V0096`) and Nefron (`V0038`, event organisers by registry), Limes Plus (`V0097`, office supplies), Caboodle (`V0211`, an employee benefits platform), and trendig (`V0213`, training). Weking (`V0009`) points to a Salesforce consultancy, with low confidence.
- **Retained vendors and group functions** named in Consolidate rationales: WeWork for coworking (already the Singapore provider; Common Desk is now part of WeWork), JLL for property advice, Hrvatski Telekom for Croatian telecoms, New Star Networks for UK telecoms, Google Workspace through CTS as the one productivity suite, Veniture as the channel for the Atlassian estate, Workato for integration, Cognism for contact data, Infosys for outsourced development, Carrington for PR, 4imprint for promotional products, UPS through Rhea for couriers, CSC for corporate secretarial work, Navan for hotels and travel paid directly, and Salesforce for HubSpot and Yoxel. The group functions named are the group auditor, the group insurance programme, the group law firm panel, the parent's HRIS and ERP, group IT procurement and the group's development programmes.
- **Croatian sole traders**: the business register's page is cited even where its URL carries the owner's name, because that name is part of the registered business name; nothing else about the owner is recorded. One log URL about an unrelated sole trader was withheld. Superseded in step 3b: such URLs are now withheld.
- **Points for Finance** that surfaced in the research: small UK employment-law payments that may be contributions to departing employees' settlement-agreement advice (`V0230`, `V0231`, `V0241`); Pixsy (`V0237`), which may be a copyright claim settlement rather than a service; FastSpring (`V0198`), fees on the company's sales or a software purchase; the billing country of T-Mobile (`V0140`); Clime India (`V0181`), possibly Acclime India; and N S Shastri And Co (`V0164`), whose name is shared with the founding partner of the 4i practice.

### 4. Result

All 386 rows are classified in ten batches, merged into `outputs/vendors_classified.csv` in sheet order, and every check passes (M1 to M7, S1 to S6, C1 to C18; `qa/validation_report.md`). The figures below come from that report.

- Verification: 305 rows verified on the web (97.5% of spend); 81 not verified (2.5% of spend), each listed with its reason. Every vendor had at least one web search except the unnamed payee (`V0325`), which has no name to search; `qa/verification_log.csv` holds 1,065 lookups.
- Recommendations: 125 Optimize (60.9% of spend), 107 Consolidate (30.1%), 154 Terminate (9.0%). Terminate is mostly tail spend: food, events, gifts, retail purchases and unidentified payees.
- Confidence: 177 high (70.9% of spend), 108 medium, 101 low (6.9% of spend).

## 2026-11-10: remaining decision tags (prompt 14, step 2f)

### 1. The four points raised after step 2e are approved

The sixth decision name `group_it_procurement`; the hardware rule ahead of the size test; the QA checks for the nine hardware rows and the three advisers; and Finance question 6.

### 2. Three more decision names

- `group_payroll`: employer-of-record and payroll outsourcing.
- `group_systems`: HR and finance systems migrating to the parent's HRIS and ERP.
- `group_legal`: law firm panel consolidation.

That makes nine decisions in `docs/savings_assumptions.md`.

### 3. Every assumption carries a tag

`docs/savings_assumptions.md` now lists every lever in `docs/recommendation_rules.md`, each with its `depends_on` tag. The savings percentages are still set in the savings step.

- Purely vendor actions carry `none`. The cases named are the Salesforce licence audit, AWS savings plans, Navan policy and the insurance re-broke. The same test, that the company can act with its own vendors without any acquirer decision, gives `none` to:
  - the tool consolidations (two productivity suites, work-management and integration tools, contact-data tools, HubSpot alongside Salesforce marketing);
  - one entity per vendor;
  - the Terminate categories that need no decision (perks, events, gifts and memberships; food, groceries, gifts and marketplace purchases through AP; unidentified payees; deal and transaction advisers);
  - tail spend, and the general Consolidate and Optimize levers.
- Every other lever carries the decision it depends on: coworking and offices (`remote_operating_model`), recruiting agencies (`group_talent_function`), insurers (`group_insurance_programme`), auditors and accountants (`group_auditor`), the CRM instance (`parent_crm_instance`), employee hardware (`group_it_procurement`), employer-of-record and payroll outsourcing (`group_payroll`), HR and finance systems (`group_systems`) and law firms (`group_legal`).
- LinkedIn's seat review is the one Optimize-list lever not named as a vendor action, so it carries `group_talent_function`: LinkedIn sits in Recruiting and HR outsourcing, and how many recruiting seats the company needs depends on who does its hiring. Open for confirmation.
- The insurance re-broke carries `none` as decided, although the Optimize list words it "re-broke under the group programme" (prompt 6). Moving the company's cover into the group programme is the separate insurers lever, tagged `group_insurance_programme`.
- The two fixed rows, student labour and outside the savings base, count no saving, so they carry `none`.

### 4. Where it is implemented

- `docs/savings_assumptions.md`: the three decision names, and the table of levers with a tag on every row.
- `docs/recommendation_rules.md`: the section "Savings that depend on the acquirer's decisions" names the nine decisions and the four vendor actions.
- `qa/check_outputs.py`: new structural check S6, under which every assumption carries `none` or registered decision names, never both, and the four named vendor actions carry `none`. Four planted errors are added to the self-test, 43 in all.
- `scripts/merge_validate.py`: the report's description of the checks names S6.

## 2026-11-10: decision tags, hardware rule, merge script (prompt 13, step 2e)

### 1. Savings that depend on the acquirer are tagged

- Every savings assumption that depends on a choice by the acquirer carries a `depends_on` tag with that decision's name, in `docs/savings_assumptions.md` and in `outputs/analysis/savings.md`. The decisions named: remote operating model (`remote_operating_model`), group talent function (`group_talent_function`), group insurance programme (`group_insurance_programme`), group auditor (`group_auditor`) and parent CRM instance (`parent_crm_instance`).
- `group_it_procurement` is added for the hardware rule below, since that saving needs the acquirer's choice too. An assumption that needs no such choice carries `none`.
- The memo presents the Top 3 as decisions with their value, not as facts about the parent.

### 2. Employee hardware is Consolidate, not Terminate

- Employee hardware is Consolidate into group IT procurement: the four Apple entities (`V0123`, `V0172`, `V0175`, `V0229`), HP (`V0167`), Currys (`V0378`), Magazin Računalni Sistemi (`V0066`), Sniper Systems (`V0131`) and E-Disti (`V0260`). Each of their rationales names group IT procurement.
- Terminate remains for food, groceries, gifts and marketplace purchases through AP. The Amazon marketplace rows (`V0203`, `V0291`) stay Terminate under it.
- The rule is step 4 of the order of application, ahead of the size test, because E-Disti and Currys are under $1,000 and the size test would otherwise send them to tail-spend policy.

### 3. Advisers whose spend may include sale-related work stay in the recurring base

- BDO (`V0004`), Bisley Law (`V0018`) and Grant Thornton (`V0029`) keep `is_recurring` TRUE, so they are not treated as the non-recurring deal advisers of the Terminate list.
- When `insights.md` is written, it notes that the recurring figure is likely lower for this reason. Question 6 for Finance asks for the sale-related share.

### 4. Batch format and the merge script

- The classification is written in batches of 40 vendors, one CSV each, `outputs/batches/batch_NN.csv` numbered from 01, with exactly the 16 columns of the classification spec, in its order. The 386 rows make nine batches of 40 and a tenth of 26.
- `scripts/merge_validate.py` checks the batches (M1 to M7: file names and numbering, headers, batch sizes, row shape, each `vendor_id` once, numeric spend, the reasons file). It then merges them, sorts by `vendor_id`, writes `outputs/vendors_classified.csv`, runs `qa/check_outputs.py`, and writes `qa/validation_report.md`. The report holds counts, distributions by department, recommendation, cluster and confidence, the low-confidence list sorted by spend, the "Verification exceptions" section, every check, and every failure with its full detail.
- The batches have no column for a verification reason, and the report is rebuilt on every run, so the reasons live in `qa/verification_exceptions.csv` (`vendor_id`, `reason`), kept by the verification step. The script copies them under "Verification exceptions", and C17 compares that list with the `verified` column, both ways.
- The merged file is written even when a check fails, so that one run reports every failure. The exit code is 1 when any check fails, and also when there is no batch file, in which case nothing is written.
- `python scripts/merge_validate.py --self-test` merges synthetic batches in a temporary directory. Shuffled batches come out in sheet order and pass every check; a second run, and a different shuffle, give byte-identical output; and 16 planted errors are each caught.

### 5. Where it is implemented

- `docs/recommendation_rules.md`: the hardware rule under Consolidate, the narrowed Terminate category, the adviser note, step 4 of the order of application, and the sections "Savings that depend on the acquirer's decisions" and "Recurring base".
- `docs/savings_assumptions.md`: new; the register of decision names and of the assumptions fixed so far.
- `qa/check_outputs.py`: C13 and C14 cover the nine hardware rows (Consolidate, with a rationale that names group IT procurement) and the three advisers (`is_recurring` TRUE); S4 confirms that the new ids are those vendors; three planted errors are added, 39 in all. A `run()` function and full details serve the merge script.
- `scripts/merge_validate.py`: new.
- `scripts/02_clean.py`: its no-dash check covers the new doc. In it and in `qa/check_outputs.py`, the dashes the code tests for are now written as escapes, so no file in the repository contains one.

## 2026-11-10: sheet order (prompt 12, step 2d-fix3)

- `outputs/vendors_classified.csv` is written in the original sheet row order, `vendor_id` ascending (`V0002` to `V0387`), because its Department, Description and Suggestions columns are pasted straight into the Google Sheet and must line up row for row with the source.
- `merge_validate.py`, the script that merges the classification batches, sorts to that order before writing, whatever order the batches came in. It was written in step 2e as `scripts/merge_validate.py`.
- C18 matches `vendor_name_original` and `vendor_name_clean` to `outputs/vendors_clean.csv` by `vendor_id`, no longer by position, and also confirms the order. In the self-test, a shuffled file and two swapped rows each fail C18 alone, with no name mismatches reported, which shows the names are matched by id and the order is checked separately.

## 2026-11-10: group recommendation rule (prompt 9, step 2d)

### 1. Which rows share a recommendation

The exception proposed in step 2c is approved, and the rule is restated:

- One recommendation per merge group, since a merge is the same vendor relationship: Navan, AWS, TM Forum, and 4i while the merge is proposed.
- One recommendation per link group whose products are the same kind of service: the same-brand groups (Apple, Bupa, HR Solution International, Acclime, DHL, Telefónica, Allianz Australia, GRT Hotels & Resorts) and the shared-parent groups Salesforce with Slack, Atlassian with Trello, SolarWinds with Papertrail, and the two ICICI insurers.
- A recommendation per row for shared-parent links with different services: Amazon (the two marketplaces and AWS), Microsoft (Microsoft 365, LinkedIn and npm), and Sodexo and Pluxee if the link stands.
- Either way, every grouped row's rationale names its group.

### 2. Outcomes fixed for the per-row groups

| Row | Recommendation | Rule |
|---|---|---|
| AWS (`V0014`, `V0103`) | Optimize | named in the Optimize list: savings plans, one organisation |
| Amazon.co.uk (`V0203`), Amazon (Aus) (`V0291`) | Terminate | consumer retail purchases through AP |
| Microsoft 365 (`V0081`) | Consolidate | two productivity suites |
| LinkedIn (`V0026`) | Optimize | seat review |
| npm (`V0125`) | follows the developer-tool rule | department Engineering (taxonomy rule 9), cluster Software subscriptions (non-Salesforce) (clusters C10), and a recommendation from the order of application like any other developer tool, not inherited from the Microsoft group |

### 3. Where it is implemented

- `scripts/vsa_common.py`: every link group carries `recommendation`, either `shared` or `per row`, and every merge and link group lists the names a rationale may use for it.
- `qa/vendor_groups.csv`: new column `link_recommendation`, `shared` or `per row` for every linked row.
- `docs/recommendation_rules.md`: the section "Merged and linked rows" and the order of application follow the restated rule.
- `outputs/analysis/01_forensics.md` and `02_cleaning_report.md` show the recommendation scope of each link group.

### 4. The QA check

Updated in step 2d-fix (prompt 10): the expected columns follow the classification spec, and checks C16 and C17 are added. Corrected in step 2d-fix2 (prompt 11): C17 enforces the verification-exceptions rule below, and C18 checks the names. Changed in step 2d-fix3 (prompt 12): C18 matches the names by `vendor_id` and confirms the original sheet order. Extended in step 2e (prompt 13): C13 and C14 cover the hardware rule and the advisers kept in the recurring base, and `scripts/merge_validate.py` runs the checks and writes `qa/validation_report.md`. Extended in step 2f (prompt 14): S6 checks the `depends_on` tags. Extended in step 3b (prompt 16): C13 and C14 cover the platform reclassification, C14 also reads risk notes and descriptions, and C16 fails an Optimize row with a risk note, except `V0002`. Extended in step 3c (prompt 17): C13 and C14 cover the SaaS department reading, and C14 also reads sub_functions. Extended in step 4 (prompt 17): the savings checks V1 to V8 run on `outputs/analysis/savings.csv`. Extended in step 5 (prompt 18): C16 requires a risk note on every Optimize row at or above $25,000, C19 keeps the project's workings out of the reader-facing text, and V9 tests the recommendation against the lever. Extended in step 6 (prompt 19): C20 and D4 check for British forms, D1 and D2 trace every figure and total in the documents, D3 keeps the project vocabulary out of them, and W1 reads the sheet workbook back against its sources.

`qa/check_outputs.py` enforces these rules. Its structural checks run now; its classification checks run once `outputs/vendors_classified.csv` exists. `python qa/check_outputs.py` checks the real files; `python qa/check_outputs.py --self-test` runs the classification checks on a synthetic classification and validation report, and S6 on the savings register, clean and then with 53 planted errors, and shows each error caught.

| Check | Rule |
|---|---|
| S1 to S6 | group definitions and the merge map agree; the per-row links are exactly Amazon and Microsoft (Sodexo and Pluxee became a merge in step 3); the rows fixed by decisions are the vendors the decisions name; the taxonomy and cluster lists load; every savings assumption carries `none` or registered decision names, and the four named vendor actions carry `none` |
| C1, C2 | the 16 columns of the classification spec are present; exactly one row per source row (386), no duplicates |
| C3 to C6 | departments, clusters and recommendations take allowed values; `is_addressable`, `is_recurring` and `verified` are TRUE or FALSE; confidence is high, medium or low |
| C7 to C9 | one-line descriptions without the banned phrases; one-sentence rationales; no em or en dashes |
| C10 | total `spend_12m` equals the clean file's total exactly |
| C11 | the rows of each merge group and of each shared link group carry one recommendation |
| C12 | every row that is a duplicate record of one vendor (a merge group or a same-brand link group) names the other record in its rationale, while rows linked only through a corporate parent need not (step 7); where the row's own name already contains the shared name, the rationale must also show the grouping with a word such as "group", "both" or "entities" |
| C13, C14 | the outcomes, and the wording of rationales, risk notes, descriptions and sub_functions, fixed by decisions (steps 2b to 3c; the two readings of the platform bill in `V0002`'s rationale, step 11) |
| C15 | rows outside the savings base say "non-discretionary, no saving counted" (step 7; "excluded from the savings base" until then) |
| C16 | `risk_note` is non-empty for every Terminate and Consolidate row and for every Optimize row at or above $25,000 (step 5), and empty for every smaller Optimize row |
| C17 | every row has `verified` TRUE, except rows with `verified` FALSE listed under "Verification exceptions" in `qa/validation_report.md`; a FALSE row not listed there fails, and a listed `vendor_id` that is not FALSE in the file fails |
| C18 | `vendor_name_original` and `vendor_name_clean` match `outputs/vendors_clean.csv` by `vendor_id`, and the rows are in the original sheet order, `vendor_id` ascending |
| C19 | descriptions, rationales and risk notes never refer to the project's own workings: hints, lists, rules, searches, sources, steps, prompts or files (step 5), nor to the project vocabulary lever, cluster, depends_on or batch (step 6) |
| C20 | descriptions, rationales and risk notes are in American English: none of the common British forms (step 6) |
| D1 to D4 | the four documents (step 6): every dollar figure and percentage appears in a file under `outputs/analysis` or `qa`; every table with a Total row adds up; no project vocabulary in the Top 3, the memo or the methodology; American English |
| D5 | every calculation the Top 3 states reproduces from `savings.csv` (step 9): the spend named is one saving line's spend to the dollar, the product is spend times rate to the dollar, lines left out are stated as one figure, and the parts add to the stated total, which rounds to the opportunity's base saving |
| W1 | the sheet workbook matches its sources cell by cell (column I reads "No saving counted: " and the reason where the base saving is zero, column J is headed "Vendor identified online (Yes/No)" and column H shows whole dollars, step 7), keeps the raw row order and the Department dropdown, uses only Config departments, and its saving column sums to the base saving (step 6) |
| V1 to V8 | the savings file (step 4): low <= base <= high; without decision <= base; year 1 is the base times a factor between 0 and 1; no saving on a non-addressable or M&A row; no saving above spend; every row has one registered lever and every lever is used; every tag is a registered decision; the roll-ups in `savings.md` reconcile to the cent |
| V9 | every Terminate row on a lever with a base below 50% outside the Excluded opportunity, and every Optimize row on a lever above 50%, is fixed or has a recorded reason (step 5) |
| V10 | every row whose saving rests on a group decision (a lever tagged with a decision, base saving above zero) leads its rationale with the group function it moves to and gives the vendor-only fallback second (step 7) |
| V11 | every Terminate row whose base saving is under half its spend says why in a clause: pay passed through, a processing fee, stopped until confirmed, or no saving counted (step 7) |

Columns of `outputs/vendors_classified.csv`, as in the classification spec: `vendor_id`, `vendor_name_original`, `vendor_name_clean`, `spend_12m`, `department`, `sub_function`, `description`, `recommendation`, `rationale`, `risk_note`, `cost_cluster`, `is_addressable`, `is_recurring`, `confidence`, `verified`, `source_url`. `spend_12m` replaces the earlier `cost_usd`. Other columns may be added.

The verification-exceptions rule (step 2d-fix2): every row must have `verified` TRUE. A row with `verified` FALSE must appear by `vendor_id`, with a one-line reason, under a heading "Verification exceptions" in `qa/validation_report.md`, and nothing else counts. C17 reads only that file and that heading: the lines under a heading whose text is exactly "Verification exceptions", up to the next heading of the same or a higher level. A line there that carries a `vendor_id` lists that row, and it must carry exactly one `vendor_id` and the reason on the same line, in the form `- Vnnnn: reason`. Lines without a `vendor_id` are ignored, and so are vendor names without an id, other headings and other files. From step 2e, `scripts/merge_validate.py` writes `qa/validation_report.md` and copies this section from `qa/verification_exceptions.csv`, which the verification step keeps; the QA check only reads the report.

## 2026-11-10: decisions confirmed (prompt 8, step 2c)

### 1. The step 2b proposals are confirmed

- The eight links that followed from the merge policy stand: Bupa, Apple, the Amazon marketplaces, HR Solution International, Acclime, DHL, Telefónica and GRT Hotels & Resorts.
- AWS stays merged.
- Student labour is Optimize (addressable, 0% savings assumption).

### 2. Sodexo and Pluxee: the web verification decides

If the Sodexo SVC India invoices (`V0054`) are meal cards billed under Pluxee India's former name, it is a rename and the two rows become a merge. If they are catering, the link stands. Until the verification, the two rows stay linked.

### 3. The sheet deliverable is per row

All 386 original rows get their own department, description and recommendation. Merges and links exist only for ranking and savings roll-ups. Rows in a merge or link group carry the same recommendation and a rationale that names the group.

In practice:

- `outputs/vendors_classified.csv` has exactly 386 rows, one per source row, keyed by `vendor_id`. It fills the sheet's Department, 1-line Description and Suggestions columns for every row.
- Department, description and cluster are set row by row, so rows of one group can differ where the rows themselves differ (Slack is SaaS while Salesforce is Sales).
- The recommendation is set once per group and repeated on every row of it. Each row's rationale names the group, so a reader of a single row sees the connection ("one of two Navan entities", "part of the Bupa link group").
- The under-$1,000 rule is measured on the group total, so all rows of a group land on the same side of it.
- Rankings use the merged view (`canonical_vendor`); savings roll-ups use the cost clusters and, where one negotiation covers a link group, the group total.
- The QA script checks that the rows of every group share one recommendation and that each of their rationales names the group.

Refined in step 2d: link groups whose rows are different services take a recommendation per row, and the size test uses the group total only for groups that share a recommendation.

### 4. Open point: two link groups where one recommendation does not fit (resolved in step 2d)

Applying point 3 to every link group meets two shared-parent groups whose rows are different products with different levers under `docs/recommendation_rules.md`:

| Link group | Rows | What the rules give each row on its own |
|---|---|---|
| Amazon | AWS (`V0014`, `V0103`, merged); Amazon.co.uk (`V0203`); Amazon (Aus) (`V0291`) | AWS: Optimize (named in the Optimize list). The marketplaces: Terminate (consumer retail purchases through AP) |
| Microsoft | LinkedIn (`V0026`); Microsoft Ireland (`V0081`, Microsoft 365 in the taxonomy); npm (`V0125`) | LinkedIn: Optimize (seat review). Microsoft 365: Consolidate (two productivity suites). npm: a developer tool, decided on its own |

Sodexo and Pluxee would join them if the link stands, as on-site catering and meal cards are different services.

Proposed resolution, awaiting confirmation: one shared recommendation for every merge and for every link whose rows supply the same kind of thing (same-brand links, and the shared-parent links Salesforce with Slack, Atlassian with Trello, SolarWinds with Papertrail, and the two ICICI insurers). Shared-parent and same-lineage links whose rows are different products (Amazon, Microsoft, and Sodexo and Pluxee if the link stands) keep row-level recommendations, and their rationales still name the group.

## 2026-11-10: rule decisions (prompt 7, step 2b)

### 1. Department and cluster answer different questions

The proposed tie-breaks in `docs/taxonomy.md` and `docs/clusters.md` and the order of application in `docs/recommendation_rules.md` are approved, with one principle made explicit: department answers "whose budget is this"; `cost_cluster` answers "which lever captures the saving". They can differ.

- Mason Frank: G&A by department (recruiting), Salesforce platform by cluster, so its saving rolls into the Salesforce opportunity.
- Slack: SaaS by department, Salesforce platform by cluster, because it is Salesforce-owned and goes into the same renewal.

Implemented in `docs/taxonomy.md` (introduction, T1) and `docs/clusters.md` (introduction, Salesforce platform, C1).

### 2. Merge policy

Merge only when it is the same vendor relationship under a changed or variant name: a rename, a spelling variant, or the same contract moved between entities. Where two entities share a parent or brand but supply different products or contracts, record a link, not a merge.

Applied to every group of the step 2 merge map. "Decision" marks the cases named in prompt 7; "policy" marks cases that follow from the policy, any of which can be reversed.

| Group | Step 2 | Now | Source | Why |
|---|---|---|---|---|
| Navan | merge | merge | decision | rename (TripActions to Navan) |
| TM Forum | merge | merge | policy | spelling variant |
| AWS | merge | merge | policy | one service and customer agreement under two entity names (Inc. and LLC) |
| 4i | merge | proposed merge | decision | to be confirmed or reversed by web verification |
| Sodexo and Pluxee | merge | link | decision | same lineage, but on-site catering and meal cards are different services and contracts |
| Allianz Australia | merge | link | decision | separate state workers' compensation policies |
| Bupa | merge | link | policy | separate entities and insurance contracts |
| Apple | merge | link | policy | four regional entities with separate purchases |
| Amazon marketplaces | merge | link | policy | separate country marketplaces, linked to AWS through the Amazon parent |
| HR Solution International | merge | link | policy | a GmbH and an AG, presumably separate country contracts |
| Acclime | merge | link | policy | separate entities, presumably separate engagements |
| DHL | merge | link | policy | not shown to be one account |
| Telefónica | merge | link | policy | two group entities; what each payment is goes to Finance |
| GRT Hotels & Resorts | merge | link | policy | two hotels of one group |

Result: 386 rows become 382 vendors (383 if the 4i merge is reversed), with 15 link groups, which include the six shared-parent links from step 2 (Slack with Salesforce, Trello with Atlassian, Papertrail with SolarWinds, LinkedIn and npm with Microsoft, the two ICICI insurers, and AWS with the Amazon marketplaces).

Note for the web verification: the entity name Sodexo SVC India Private Limited may be the former name of Pluxee India Private Limited. If so, and if `V0054` invoices meal cards rather than on-site catering, the two rows are one relationship renamed and the policy makes them a merge.

Implemented in `scripts/vsa_common.py` (`MERGE_GROUPS`, `LINK_GROUPS`), `qa/vendor_groups.csv`, `outputs/vendors_clean.csv`, `outputs/analysis/02_cleaning_report.md` and `outputs/analysis/01_forensics.md` (section 6).

### 3. The memo is also a Google Doc

`outputs/memo.md` stays the source of truth. The user creates the Google Doc from it and pastes the link and the text into the CEOCFO Recommendations tab. The memo therefore has to fit one page as a Google Doc and paste cleanly as plain text: headings, short paragraphs or bullets, no wide tables.

### 4. Student labour is addressable, at 0%

`is_addressable` TRUE, cluster Student labour, savings assumption 0%, rationale "workforce cost, set by the hiring plan, not a vendor action". The recommendation label is Optimize: the decision fixed addressability, assumption and rationale but not the label, and Optimize is the only one of the three that fits a cost with no vendor action. Applies to `V0030`, `V0086` and `V0186`.

Implemented in `docs/recommendation_rules.md` and `docs/clusters.md`.

### 5. Telefónica is a question for Finance

Are the Telefónica payments fees, rebates or connectivity? Until Finance answers: department Sales, recommendation Optimize, `is_addressable` FALSE, and the rationale says that if they are rebates they belong against revenue rather than in vendor spend. Applies to `V0015` and `V0093` ($96,037 together).

Implemented in `docs/recommendation_rules.md` and `docs/clusters.md`.

## Open questions for Finance

Questions the file cannot answer, collected from `outputs/analysis/01_forensics.md` and from later decisions. Each one changes a classification or a savings figure.

| # | Question | Vendors | Why it matters |
|---|---|---|---|
| 1 | Are the Telefónica payments fees, rebates or connectivity? | `V0015`, `V0093` | Rebates belong against revenue; connectivity would be telecom spend |
| 2 | What does the Salesforce contract cover: a partner revenue share on the product (on which rate tier, and with what counted as net revenue), licences for staff, or both, and is there a change-of-control clause? | `V0002` | 39.5% of spend. Step 11 reads the bill as most likely a partner revenue share plus internal seats, with 15% as a placeholder between the two readings until the contract is read; the reading and the rate tier set the saving, and the seat count sets only the internal-seat part |
| 3 | What do the Croatian companies of unknown function supply, starting with Weking d.o.o.? | `V0009` and the 12 others listed in `docs/vendor_hints.md` | $309,614 that cannot yet be described or recommended with confidence |
| 4 | What was the City of Zagreb spatial-planning payment for? | `V0073` | $11,637, probably one-off |
| 5 | Which group entity does the Cayman Islands Government payment relate to? | `V0361` | The legal-entity map behind the payee list |
| 6 | How much of the BDO, Bisley Law and Grant Thornton spend was sale-related work? | `V0004`, `V0018`, `V0029` | They stay in the recurring base (step 2e); the sale-related share would come out of it |
| 7 | Which entity invoices as Bisley Law Ltd, and for what? The firm merged into Gordons Partnership in January 2024 and its company is now registered as non-trading (step 5), so the invoices most likely come from the successor firm; this is a question, not evidence of a problem (step 4b) | `V0018` | $67,414 of legal work, which follows the law-firms lever whoever the payee proves to be; the payee check is a control action |
| 8 | Is PDF Butler licensed on OEM terms, embedded in or delivered with the product? | `V0006` | $208,675; OEM or volume pricing is renegotiated within the platform review (step 3b) |
