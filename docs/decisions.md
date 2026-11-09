# Decisions

Decisions taken during the analysis, newest first. Each records what was decided and where it is implemented. The prompts that carried them are in `prompts/log.md`.

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

### 4. Open point: two link groups where one recommendation does not fit

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

Questions the file cannot answer, collected from `outputs/analysis/01_forensics.md`. Each one changes a classification or a savings figure.

| # | Question | Vendors | Why it matters |
|---|---|---|---|
| 1 | Are the Telefónica payments fees, rebates or connectivity? | `V0015`, `V0093` | Rebates belong against revenue; connectivity would be telecom spend |
| 2 | What does the Salesforce contract cover: staff CRM licences, platform or OEM fees tied to the product, or a prepayment? | `V0002` | 39.5% of spend; the lever depends on the answer |
| 3 | What do the Croatian companies of unknown function supply, starting with Weking d.o.o.? | `V0009` and the 12 others listed in `docs/vendor_hints.md` | $309,614 that cannot yet be described or recommended with confidence |
| 4 | What was the City of Zagreb spatial-planning payment for? | `V0073` | $11,637, probably one-off |
| 5 | Which group entity does the Cayman Islands Government payment relate to? | `V0361` | The legal-entity map behind the payee list |
