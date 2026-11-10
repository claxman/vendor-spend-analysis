# Decisions

Decisions taken during the analysis, newest first. Each records what was decided and where it is implemented. The prompts that carried them are in `prompts/log.md`.

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

Updated in step 2d-fix (prompt 10): the expected columns follow the classification spec, and checks C16 and C17 are added. Corrected in step 2d-fix2 (prompt 11): C17 enforces the verification-exceptions rule below, and C18 checks the names. Changed in step 2d-fix3 (prompt 12): C18 matches the names by `vendor_id` and confirms the original sheet order. Extended in step 2e (prompt 13): C13 and C14 cover the hardware rule and the advisers kept in the recurring base, and `scripts/merge_validate.py` runs the checks and writes `qa/validation_report.md`.

`qa/check_outputs.py` enforces these rules. Its structural checks run now; its classification checks run once `outputs/vendors_classified.csv` exists. `python qa/check_outputs.py` checks the real files; `python qa/check_outputs.py --self-test` runs the classification checks on a synthetic classification and validation report, clean and then with 39 planted errors, and shows each error caught.

| Check | Rule |
|---|---|
| S1 to S5 | group definitions and the merge map agree; the per-row links are exactly Amazon, Microsoft, and Sodexo and Pluxee; the rows fixed by decisions are the vendors the decisions name; the taxonomy and cluster lists load |
| C1, C2 | the 16 columns of the classification spec are present; exactly one row per source row (386), no duplicates |
| C3 to C6 | departments, clusters and recommendations take allowed values; `is_addressable`, `is_recurring` and `verified` are TRUE or FALSE; confidence is high, medium or low |
| C7 to C9 | one-line descriptions without the banned phrases; one-sentence rationales; no em or en dashes |
| C10 | total `spend_12m` equals the clean file's total exactly |
| C11 | the rows of each merge group and of each shared link group carry one recommendation |
| C12 | every grouped row's rationale names its group, per-row links included; where the row's own name already contains the group's name, the rationale must also show the grouping with a word such as "group", "both" or "entities" |
| C13, C14 | the outcomes and rationale wording fixed by decisions (steps 2b to 2e) |
| C15 | rows outside the savings base say "non-discretionary, excluded from the savings base" |
| C16 | `risk_note` is non-empty for every Terminate and Consolidate row |
| C17 | every row has `verified` TRUE, except rows with `verified` FALSE listed under "Verification exceptions" in `qa/validation_report.md`; a FALSE row not listed there fails, and a listed `vendor_id` that is not FALSE in the file fails |
| C18 | `vendor_name_original` and `vendor_name_clean` match `outputs/vendors_clean.csv` by `vendor_id`, and the rows are in the original sheet order, `vendor_id` ascending |

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
| 2 | What does the Salesforce contract cover: staff CRM licences, platform or OEM fees tied to the product, or a prepayment? | `V0002` | 39.5% of spend; the lever depends on the answer |
| 3 | What do the Croatian companies of unknown function supply, starting with Weking d.o.o.? | `V0009` and the 12 others listed in `docs/vendor_hints.md` | $309,614 that cannot yet be described or recommended with confidence |
| 4 | What was the City of Zagreb spatial-planning payment for? | `V0073` | $11,637, probably one-off |
| 5 | Which group entity does the Cayman Islands Government payment relate to? | `V0361` | The legal-entity map behind the payee list |
| 6 | How much of the BDO, Bisley Law and Grant Thornton spend was sale-related work? | `V0004`, `V0018`, `V0029` | They stay in the recurring base (step 2e); the sale-related share would come out of it |
