# Savings assumptions

The register of the assumptions behind the savings figures. Every savings figure is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`). `scripts/03_savings.py` reads this register and `outputs/vendors_classified.csv`, hard-codes no spend figure, and writes `outputs/analysis/savings.csv` and `outputs/analysis/savings.md`, which repeat each assumption and its `depends_on` tag next to the figure it produces. The decision names and the tag rules were set in steps 2e and 2f (prompts 13 and 14); the levers and their percentages in step 4 (prompt 17). See `docs/decisions.md`.

## Acquirer decisions

Some savings happen only if the acquirer makes a particular choice. Every savings assumption that depends on such a choice is tagged with the decision's name in a `depends_on` column, here and in `savings.md`. The spend file shows what the company spends; it does not show what the parent has, runs or intends. A saving that needs one of these choices is therefore the value of a decision, not a fact about the parent.

| depends_on | The decision | Where it mainly applies (cost cluster) |
|---|---|---|
| `remote_operating_model` | Adopt a remote operating model for the company in place of its own offices and coworking | Office footprint; Office running costs; the telecom lines in Cloud, telecom and IT |
| `group_talent_function` | Hand the company's hiring to the group talent function | Recruiting and HR outsourcing |
| `group_insurance_programme` | Move the company's insurance cover into the group insurance programme | Insurance and benefits |
| `group_auditor` | Appoint the group auditor for the company's entities | Audit, tax, accounting and corporate services |
| `parent_crm_instance` | Move the company's CRM onto the parent's CRM instance | Software subscriptions (non-Salesforce): HubSpot. The Salesforce spend itself is the product platform (step 3b), so this decision no longer reaches it |
| `group_it_procurement` | Buy employee hardware through group IT procurement | Cloud, telecom and IT: the Employee hardware lever (step 4b) |
| `group_payroll` | Pay the company's staff through group payroll in place of employer-of-record and payroll outsourcing | Recruiting and HR outsourcing |
| `group_systems` | Migrate the company's HR and finance systems to the parent's HRIS and ERP | Software subscriptions (non-Salesforce) |
| `group_legal` | Consolidate the company's law firms into the group's law firm panel | Legal |
| `group_engineering_sourcing` | Replace the contractor consultancies with the group's own engineering sourcing | Outsourced engineering and contractors |

The first five are named in prompt 13, and `group_it_procurement` was added there for the hardware rule. `group_payroll`, `group_systems` and `group_legal` were added in step 2f (prompt 14). `group_engineering_sourcing` is the tenth, added in step 4 (prompt 17) for Weking and the other consultancies.

Rules for the tag:

- A lever that is purely a vendor action, one the company can take with its own vendors without any of the decisions above, carries `depends_on` = `none`. Step 2f named the Salesforce licence audit, AWS savings plans, Navan policy and the insurance re-broke. From step 4 the licence audit is restated for the platform reading as the Salesforce platform agreement lever, AWS and Navan keep their rows, and the insurance re-broke is the without-decision case of the commercial insurance lever rather than a lever of its own.
- Every other assumption carries the name of each decision it depends on, separated by commas.
- A new decision gets a row in the table above, with its name and what it means, before any assumption uses it.
- The memo presents each of the Top 3 as a decision with its value, naming the decision it depends on, not as a fact about the parent.
- Check S6 in `qa/check_outputs.py` enforces the first three rules on the table below.

## How the figures are computed

Every lever carries five numbers and a tag:

- `pct_low`, `pct_base` and `pct_high`: the run-rate saving as a share of the row's 12-month spend, in the low, base and high case.
- `pct_without_decision`: what vendor action alone achieves if the tagged acquirer decision is not taken. It equals `pct_base` for an untagged lever.
- `year1_factor`: the share of the first 12 months in which the saving is live. Convention: 0.5 where the renewal or notice date is unknown, higher for policy changes that start within 90 days, lower where the change waits for a year-end or a migration. On a lever with a 0% base it changes nothing and is written as 0.5.
- `depends_on`: `none`, or the decision the base case depends on.

For each vendor row, saving = spend_12m times the percentage, and the year-1 saving = the base saving times `year1_factor`. Each lever belongs to one opportunity: "Salesforce platform agreement", "Office exit", "Back office into group shared services", "Second wave" or "Excluded". Each row ends with exactly one lever, assigned by `scripts/savings_model.py` in this order: the M&A, customer-mandated, statutory and student-labour clusters take their own levers; the rows named under a lever below take it; any other row with `is_recurring` FALSE takes "One-off spend that falls away", except in Travel and entertainment and Team events, perks and wellness, where the category recurs even when the payee does not; every remaining row takes the lever of its cluster, split by sub_function where the table says so. Rows whose lever is an analyst call rather than a rule are listed in "Lever assignment" below and in `savings.md`.

## Assumptions

One row per lever. Percentages are whole numbers; `year1_factor` is a decimal. The "Applies to" column names the rows or the cluster and sub_function test that selects them.

| Lever | Opportunity | Applies to | pct_low | pct_base | pct_high | pct_without_decision | year1_factor | depends_on | Reasoning |
|---|---|---|---|---|---|---|---|---|---|
| Salesforce platform agreement | Salesforce platform agreement | Salesforce UK (`V0002`) | 10 | 15 | 25 | 15 | 0.5 | `none` | The platform agreement is renegotiated at change of control, with internal seats trued down separately; the base sits below the usual licence-audit range because part of this spend is platform and ISV fees that do not shrink with a seat count, and the contract is not visible, so the figure is the value of a negotiation that starts when the contract and usage data arrive (step 4b). |
| PDF Butler OEM pricing | Salesforce platform agreement | Cloudcrossing's PDF Butler (`V0006`) | 10 | 20 | 30 | 20 | 0.5 | `none` | OEM or volume pricing for a document app delivered with the product is renegotiated inside the platform review, at a renewal date the file does not show. |
| Kimble PSA licences | Salesforce platform agreement | Kimble (`V0027`) | 5 | 10 | 15 | 10 | 0.5 | `none` | PSA seats on the Salesforce platform are right-sized at a renewal whose date is unknown. |
| Slack and Yoxel inside the Salesforce renewal | Salesforce platform agreement | Slack (`V0173`) and Yoxel (`V0170`) | 0 | 0 | 0 | 0 | 0.5 | `none` | Both are negotiated inside the Salesforce renewal, so no separate saving is counted. |
| Office footprint | Office exit | cluster Office footprint | 60 | 75 | 90 | 25 | 0.5 | `remote_operating_model` | The base keeps a quarter of the spend for a touchdown space at the engineering hub and registered addresses; without the decision the company right-sizes onto one flexible provider; the lease notice dates are unknown. |
| Office running costs | Office exit | cluster Office running costs, recurring rows, except couriers and postage (step 4b) | 50 | 70 | 80 | 20 | 0.5 | `remote_operating_model` | Utilities, cleaning, parking, supplies and catering fall with the space; without the decision only consumables and catering are cut; the timing follows the leases. |
| Audit, tax and accounting firms | Back office into group shared services | the auditors, accountants and tax advisers in cluster Audit, tax, accounting and corporate services, and the actuarial valuations (`V0351`) | 25 | 35 | 45 | 10 | 0.4 | `group_auditor` | The group auditor takes over entity by entity at the financial year-end, so year 1 is 0.4; without the decision a tender across the firms is worth 10%. |
| Corporate secretarial, registered agent and share registry | Back office into group shared services | `V0088`, `V0099`, `V0105`, `V0334`, `V0305` | 10 | 20 | 30 | 20 | 0.5 | `none` | One provider across the entities at renewals whose dates are unknown; a vendor action that needs no group decision. |
| R&D tax credit adviser (contingent fee) | Back office into group shared services | GrantTree (`V0068`) | 0 | 0 | 0 | 0 | 0.5 | `none` | The fee is contingent on cash recovered, so cutting it reduces cash. |
| Law firms and legal resourcing | Back office into group shared services | cluster Legal, recurring rows: law firms, seconded lawyers, outsourced counsel, immigration and trade mark work | 20 | 30 | 40 | 10 | 0.6 | `group_legal` | Panel consolidation and the group legal function take over most external work within the year; without the decision a rate review is worth 10%. |
| Employment-law settlement advice | Back office into group shared services | `V0230`, `V0231`, `V0241`: small one-off payments to employment-law firms | 0 | 0 | 0 | 0 | 0.5 | `none` | These are one payment per leaver for settlement-agreement advice, not a vendor relationship. |
| Recruitment agencies and job boards | Back office into group shared services | the recruitment agencies, staffing firms and job boards in cluster Recruiting and HR outsourcing | 80 | 100 | 100 | 30 | 0.9 | `group_talent_function` | This spend follows hiring volume: with the group talent function hiring, the agencies and job boards end as open mandates close; without it, preferred suppliers and a fee cap are worth 30%. |
| LinkedIn | Back office into group shared services | LinkedIn (`V0026`) | 20 | 30 | 50 | 20 | 0.6 | `group_talent_function` | Recruiter seats fall when the group talent function does the hiring; the seat review alone is worth 20% at the next renewal. |
| External training and coaching | Back office into group shared services | leadership development, coaching and skills training in cluster Recruiting and HR outsourcing (`V0020`, `V0075`, `V0079`) | 25 | 50 | 75 | 25 | 0.75 | `group_talent_function` | Added in step 4: the group's own development programmes replace discretionary coaching and training; without the decision a cap on coaching spend is worth 25%; the change starts within 90 days. |
| Employer-of-record providers | Back office into group shared services | `V0016`, `V0090`, `V0179` | 10 | 15 | 25 | 0 | 0.5 | `group_payroll` | These invoices usually carry the employees' pay as a pass-through, so only the service fee is addressable, and only group payroll removes it. |
| Payroll processing providers | Back office into group shared services | `V0111`, `V0058` | 25 | 40 | 60 | 10 | 0.5 | `group_payroll` | Group payroll replaces outsourced processing as each country migrates; without it a re-tender is worth 10%. |
| Commercial insurance through brokers | Back office into group shared services | the broker and the US agency (`V0010`, `V0078`) | 15 | 25 | 35 | 10 | 0.5 | `group_insurance_programme` | Cover placed through brokers moves into the group programme at renewal; without the decision a re-broke is worth 10%. |
| Employee health and life insurance | Back office into group shared services | the health and life insurers, the benefits consultant and the telehealth plan (`V0012`, `V0042`, `V0045`, `V0047`, `V0069`, `V0071`, `V0095`, `V0143`, `V0098`, `V0273`) | 5 | 10 | 15 | 5 | 0.5 | `group_insurance_programme` | Benefits are part of pay, so the lever is broking and scheme terms, not cover; the group programme improves the terms, and broking alone is worth 5%. |
| Statutory cover and benefit schemes | Back office into group shared services | statutory workers' compensation and occupational health (`V0094`, `V0201`, `V0212`, `V0300`, `V0328`, `V0382`, `V0383`, `V0384`), salary-sacrifice schemes (`V0100`, `V0195`), meal cards (`V0054`, `V0128`) and the MultiSport gym scheme (`V0057`; Gym4You, `V0121`, consolidates into it from step 4b) | 0 | 0 | 0 | 0 | 0.5 | `none` | Pay and statutory cover are people decisions outside a vendor model. |
| HR and finance systems | Back office into group shared services | accounting, planning, engagement and performance systems (`V0028`, `V0039`, `V0055`, `V0080`) | 60 | 80 | 100 | 10 | 0.25 | `group_systems` | The saving starts after the migration to the parent's HRIS and ERP, so year 1 is 0.25; the base nets off extra seats on the group's systems; without the decision a seat review is worth 10%. |
| HubSpot | Back office into group shared services | HubSpot (`V0037`) | 60 | 80 | 100 | 10 | 0.25 | `parent_crm_instance` | Marketing automation moves onto the parent's CRM instance after migration, netting off extra seats there; without the decision a seat review is worth 10%. |
| Navan | Second wave | Navan (`V0003`, `V0024`) | 15 | 25 | 35 | 25 | 0.75 | `none` | A travel policy on one entity starts within 90 days; the saving is on the travel booked through the platform, not on a platform fee. |
| Other travel, hotels, restaurants and food through AP | Second wave | cluster Travel and entertainment except Navan, recurring or not | 30 | 50 | 70 | 50 | 0.75 | `none` | Travel and meals paid directly move under the policy and through Navan; part of this spend returns through expenses, which is why the base is 50%. |
| Team events, perks and wellness | Second wave | cluster Team events, perks and wellness except the MultiSport card, recurring or not | 40 | 60 | 75 | 60 | 0.75 | `none` | The rest stays as a per-head culture budget; the policy starts within 90 days. |
| Other software subscriptions | Second wave | cluster Software subscriptions (non-Salesforce), recurring rows, except the HR and finance systems and HubSpot; also the benefits platform (`V0211`) | 15 | 25 | 35 | 25 | 0.6 | `none` | Overlapping tools are consolidated and seats trued down at renewals spread through the year. |
| AWS | Second wave | AWS (`V0014`, `V0103`) | 10 | 20 | 30 | 20 | 0.6 | `none` | Savings plans and one organisation for the accounts under two entities, bought within the year. |
| Telecom and internet providers | Second wave | the telecom, internet and mobile lines in cluster Cloud, telecom and IT | 25 | 40 | 60 | 15 | 0.5 | `remote_operating_model` | Office lines end with the offices; without the decision a re-tender of lines and plans is worth 15%; the contract end dates are unknown. |
| Other cloud and IT | Second wave | the rest of cluster Cloud, telecom and IT: IT services, software escrow, domains and DNS, telephony numbers and the SMS API | 5 | 10 | 20 | 10 | 0.6 | `none` | Scope and price reviews on escrow, domains and IT services at renewals spread through the year; small vendor actions. |
| Employee hardware | Second wave | the nine hardware rows and the Chennai distributor (`V0066`, `V0123`, `V0131`, `V0167`, `V0172`, `V0175`, `V0229`, `V0260`, `V0378`, `V0048`) | 5 | 10 | 20 | 5 | 0.6 | `group_it_procurement` | Group IT procurement prices and a standard device list (step 4b); without the decision a preferred reseller is worth 5%; small, because hardware follows headcount. |
| Couriers and postage | Second wave | the courier, postage, delivery and mail rows in cluster Office running costs (`V0196`, `V0232`, `V0240`, `V0303`, `V0316`, `V0336`, `V0368`, `V0371`, `V0377`) | 5 | 10 | 20 | 10 | 0.6 | `none` | One courier account and a postage policy (step 4b); a remote company still ships parcels, so the saving is price, not volume. |
| Marketing agencies | Second wave | the marketing, media and PR agencies (`V0050`, `V0056`, `V0184`) | 30 | 50 | 70 | 50 | 0.75 | `none` | Agency retainers are consolidated or ended within 90 days. |
| TM Forum | Second wave | TM Forum (`V0025`, `V0249`) | 0 | 0 | 100 | 0 | 0.5 | `none` | A go-to-market credential; the high case applies only if the parent holds a membership that covers subsidiaries. |
| Other marketing, media and events | Second wave | the rest of cluster Marketing agencies, media and memberships, recurring rows | 20 | 30 | 50 | 30 | 0.75 | `none` | Media, events, memberships, print and stock assets are cut back under one marketing budget within 90 days. |
| Outsourced engineering and contractors | Second wave | the consultancies and development firms in cluster Outsourced engineering and contractors (`V0009`, whose share is provisional until Finance confirms the entity, question 3; `V0019`, `V0116`, `V0185`) | 20 | 30 | 40 | 10 | 0.5 | `group_engineering_sourcing` | The work continues, so the saving is the rate difference between the consultancies and the group's engineering sourcing; without the decision a rate renegotiation is worth 10%. |
| Unidentified and individual payees | Second wave | cluster Unidentified and individual payees, recurring rows, and the unidentified contractors (`V0065`, `V0074`, `V0137`) | 30 | 50 | 70 | 50 | 0.75 | `none` | Payments stop until Finance identifies the payee, and some are then re-approved; the stop starts within 90 days. |
| M&A and transaction costs | Excluded | cluster M&A and transaction costs | 0 | 0 | 0 | 0 | 0.5 | `none` | Non-recurring deal costs that fall away without action. |
| Customer-mandated platform fees | Excluded | cluster Customer-mandated platform fees | 0 | 0 | 0 | 0 | 0.5 | `none` | Fees a customer requires the company to pay: not addressable. |
| Statutory and government | Excluded | cluster Statutory and government | 0 | 0 | 0 | 0 | 0.5 | `none` | Taxes, government fees and regulators: not addressable. |
| Student labour | Excluded | cluster Student labour | 0 | 0 | 0 | 0 | 0.5 | `none` | Workforce cost, set by the hiring plan, not a vendor action. |
| One-off spend that falls away | Excluded | any other row with `is_recurring` FALSE, outside Travel and entertainment and Team events, perks and wellness | 0 | 0 | 0 | 0 | 0.5 | `none` | One-off spend falls away without action, so no saving is claimed on it; one-off payments to individuals are a control finding, not a saving (step 4b). |
| Bank, payment and certification fees | Excluded | bank fees, payment processing and ISO certification audits (`V0216`, `V0198`, `V0142`) | 0 | 0 | 0 | 0 | 0.5 | `none` | Added in step 4: fees set by transaction volume or by the certificates customers ask for, with no vendor action modelled. |

## Lever assignment

`scripts/savings_model.py` assigns the levers. Beyond the cluster defaults and the rows the table names, these rows are analyst calls, recorded here and repeated in `savings.md`:

| Row | Lever | Why |
|---|---|---|
| `V0351` Mithras Consultants | Audit, tax and accounting firms | actuarial valuations are an accounting requirement of the Indian entity, so they follow the group auditor |
| `V0211` Computershare-Caboodle | Other software subscriptions | a benefits platform fee, not pay or cover, so it is software rather than a benefit scheme |
| `V0098` Mercer | Employee health and life insurance | benefits consulting is the broking and scheme-terms work that this lever describes |
| `V0273` Doctor Anywhere | Employee health and life insurance | a health benefit for Singapore staff |
| `V0057` Benefit Systems | Statutory cover and benefit schemes | the MultiSport card is the gym scheme the assumption names; it stays as an employee benefit at the engineering hub (step 4b), and Gym4You (`V0121`) consolidates into it on the Team events, perks and wellness lever |
| `V0058` Smart Group Services | Payroll processing providers | HR outsourcing, unconfirmed; the closest lever by sub_function, and its rationale already waits for group payroll |
| `V0179` Radius Group | Employer-of-record providers | global payroll and expansion services are employer-of-record work |
| `V0020` Big Frontier, `V0075` Ramiro, `V0079` Emerge | External training and coaching | a lever added in step 4, because the assumptions list has no line for training |
| `V0065` Pingo, `V0074` Bijeli Pijesak, `V0137` Orcola | Unidentified and individual payees | Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of their cluster |
| `V0309` Avoxi, `V0363` Click Send | Other cloud and IT, including employee hardware | telephony numbers and an SMS API that do not end with the offices, so not the telecom lever |
| `V0168` Cision PR Newswire | Other marketing, media and events | a press release wire, not an agency |
| `V0076` Visalogic | Law firms and legal resourcing | immigration work follows the legal cluster into the panel; a separate immigration provider would be a different lever |
| `V0216` Raiffeisenbank, `V0198` FastSpring, `V0142` Bureau Veritas | Bank, payment and certification fees | a lever added in step 4 at 0%, because the assumptions list has no line for them |
| `V0203`, `V0291` Amazon marketplaces | Office running costs | they follow their cluster as office consumables (confirmed in step 4b), although the card policy that removes them does not depend on the office decision |

Employee hardware and Couriers and postage became named levers in step 4b, so the hardware and courier rows are no longer analyst calls. No other row fits the employment-law test: `V0202` Thomas Mansfield is a recurring relationship, and `V0264` Franklin, Gringer & Cohen is a US firm whose one-off payment is not shown to be settlement advice; both take their cluster's rule.
