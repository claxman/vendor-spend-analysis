# Decisions

Decisions taken during the analysis, newest first. Each records what was decided and where it is implemented. The prompts that carried them are in `prompts/log.md`.

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

Updated in step 2d-fix (prompt 10): the expected columns follow the classification spec, and checks C16 and C17 are added. Corrected in step 2d-fix2 (prompt 11): C17 enforces the verification-exceptions rule below, and C18 checks the names. Changed in step 2d-fix3 (prompt 12): C18 matches the names by `vendor_id` and confirms the original sheet order. Extended in step 2e (prompt 13): C13 and C14 cover the hardware rule and the advisers kept in the recurring base, and `scripts/merge_validate.py` runs the checks and writes `qa/validation_report.md`. Extended in step 2f (prompt 14): S6 checks the `depends_on` tags. Extended in step 3b (prompt 16): C13 and C14 cover the platform reclassification, C14 also reads risk notes and descriptions, and C16 fails an Optimize row with a risk note, except `V0002`. Extended in step 3c (prompt 17): C13 and C14 cover the SaaS department reading, and C14 also reads sub_functions.

`qa/check_outputs.py` enforces these rules. Its structural checks run now; its classification checks run once `outputs/vendors_classified.csv` exists. `python qa/check_outputs.py` checks the real files; `python qa/check_outputs.py --self-test` runs the classification checks on a synthetic classification and validation report, and S6 on the savings register, clean and then with 53 planted errors, and shows each error caught.

| Check | Rule |
|---|---|
| S1 to S6 | group definitions and the merge map agree; the per-row links are exactly Amazon and Microsoft (Sodexo and Pluxee became a merge in step 3); the rows fixed by decisions are the vendors the decisions name; the taxonomy and cluster lists load; every savings assumption carries `none` or registered decision names, and the four named vendor actions carry `none` |
| C1, C2 | the 16 columns of the classification spec are present; exactly one row per source row (386), no duplicates |
| C3 to C6 | departments, clusters and recommendations take allowed values; `is_addressable`, `is_recurring` and `verified` are TRUE or FALSE; confidence is high, medium or low |
| C7 to C9 | one-line descriptions without the banned phrases; one-sentence rationales; no em or en dashes |
| C10 | total `spend_12m` equals the clean file's total exactly |
| C11 | the rows of each merge group and of each shared link group carry one recommendation |
| C12 | every grouped row's rationale names its group, per-row links included; where the row's own name already contains the group's name, the rationale must also show the grouping with a word such as "group", "both" or "entities" |
| C13, C14 | the outcomes, and the wording of rationales, risk notes, descriptions and sub_functions, fixed by decisions (steps 2b to 3c) |
| C15 | rows outside the savings base say "non-discretionary, excluded from the savings base" |
| C16 | `risk_note` is non-empty for every Terminate and Consolidate row, and empty for every Optimize row except `V0002` (step 3b) |
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
| 2 | What does the Salesforce contract cover: staff CRM licences, platform or OEM fees tied to the product, or a prepayment? | `V0002` | 39.5% of spend. Step 3b treats it as platform and ISV licences for the product plus internal CRM seats; the split between the two sets the seat true-down |
| 3 | What do the Croatian companies of unknown function supply, starting with Weking d.o.o.? | `V0009` and the 12 others listed in `docs/vendor_hints.md` | $309,614 that cannot yet be described or recommended with confidence |
| 4 | What was the City of Zagreb spatial-planning payment for? | `V0073` | $11,637, probably one-off |
| 5 | Which group entity does the Cayman Islands Government payment relate to? | `V0361` | The legal-entity map behind the payee list |
| 6 | How much of the BDO, Bisley Law and Grant Thornton spend was sale-related work? | `V0004`, `V0018`, `V0029` | They stay in the recurring base (step 2e); the sale-related share would come out of it |
| 7 | Which entity invoiced as Bisley Law Ltd, and for what? The name matches no trading law firm on the public registers, which the modified vendor names can explain, so this is a question, not evidence of a problem (step 4b) | `V0018` | $67,414 of legal work, which follows the law-firms lever whoever the payee proves to be; the payee check is a control action |
| 8 | Is PDF Butler licensed on OEM terms, embedded in or delivered with the product? | `V0006` | $208,675; OEM or volume pricing is renegotiated within the platform review (step 3b) |
