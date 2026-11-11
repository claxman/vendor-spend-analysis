# Savings model

Written 2026-11-11 by `scripts/03_savings.py` from `outputs/vendors_classified.csv` (386 rows) and the register `docs/savings_assumptions.md` (41 levers, 10 acquirer decisions). Every figure is the row's 12-month spend times a percentage from the register; no spend figure is typed into the script. Whole dollars here, full precision in `outputs/analysis/savings.csv`. The costs are the file's modified values (`outputs/analysis/01_forensics.md`, section 3). A saving tagged with a decision is the value of that decision, not a fact about the parent (`docs/savings_assumptions.md`).

## Totals

| Measure | Value |
|---|---|
| Vendor rows | 386 (41 levers in use) |
| Total spend, 12 months | $7,887,360 |
| Recurring base (`is_recurring` TRUE) | 270 rows, $7,556,683 (95.8%) |
| Non-recurring spend (`is_recurring` FALSE) | 116 rows, $330,678 (4.2%) |
| Addressable spend (`is_addressable` TRUE) | 369 rows, $7,765,704 (98.5%) |
| Spend on levers with a base above 0% | 300 rows, $7,323,271 (92.8%) |
| Run-rate saving, low / base / high | $1,577,675 / $2,247,704 / $3,114,502 |
| Base saving as a share of total spend | 28.5% |
| Saving without any acquirer decision (vendor action alone) | $1,282,569 (16.3%) |
| Year-1 saving (base times each lever's year-1 factor) | $1,221,950 (15.5%) |

## Excluded spend by reason

Every lever with a 0% base case, one line each. The spend stays in the file's total and out of the savings.

| Reason (lever) | Opportunity | Rows | Spend | Share of spend | High case | Why |
|---|---|---|---|---|---|---|
| Slack and Yoxel inside the Salesforce renewal | Salesforce platform agreement | 2 | $4,033 | 0.1% | $0 | Both are negotiated inside the Salesforce renewal, so no separate saving is counted. |
| R&D tax credit adviser (contingent fee) | Back office into group shared services | 1 | $13,659 | 0.2% | $0 | The fee is contingent on cash recovered, so cutting it reduces cash. |
| Employment-law settlement advice | Back office into group shared services | 3 | $1,930 | 0.0% | $0 | These are one payment per leaver for settlement-agreement advice, not a vendor relationship. |
| Statutory cover and benefit schemes | Back office into group shared services | 13 | $54,004 | 0.7% | $0 | Pay and statutory cover are people decisions outside a vendor model. |
| TM Forum | Second wave | 2 | $58,070 | 0.7% | $58,070 | A go-to-market credential; the high case applies only if the parent holds a membership that covers subsidiaries. |
| M&A and transaction costs | Excluded | 4 | $226,932 | 2.9% | $0 | Non-recurring deal costs that fall away without action. |
| Customer-mandated platform fees | Excluded | 3 | $97,400 | 1.2% | $0 | Fees a customer requires the company to pay: not addressable. |
| Statutory and government | Excluded | 6 | $15,646 | 0.2% | $0 | Taxes, government fees and regulators: not addressable. |
| Student labour | Excluded | 3 | $54,117 | 0.7% | $0 | Workforce cost, set by the hiring plan, not a vendor action. |
| One-off spend that falls away | Excluded | 46 | $32,998 | 0.4% | $0 | One-off spend falls away without action, so no saving is claimed on it; one-off payments to individuals are a control finding, not a saving (step 4b). |
| Bank, payment and certification fees | Excluded | 3 | $5,299 | 0.1% | $0 | Added in step 4: fees set by transaction volume or by the certificates customers ask for, with no vendor action modelled. |
| Total |  | 86 | $564,090 | 7.2% | $58,070 |  |

## Savings by opportunity

| Opportunity | Rows | Spend | Low | Base | High | Without decision | Year 1 | Base share of spend |
|---|---|---|---|---|---|---|---|---|
| Salesforce platform agreement | 5 | $3,382,759 | $335,231 | $514,601 | $849,833 | $514,601 | $257,301 | 15.2% |
| Office exit | 33 | $896,401 | $531,905 | $669,333 | $800,825 | $221,132 | $334,667 | 74.7% |
| Back office into group shared services | 82 | $1,742,298 | $456,767 | $650,213 | $824,900 | $196,816 | $356,469 | 37.3% |
| Second wave | 201 | $1,433,509 | $253,772 | $413,556 | $638,944 | $350,020 | $273,514 | 28.8% |
| Excluded | 65 | $432,393 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Total | 386 | $7,887,360 | $1,577,675 | $2,247,704 | $3,114,502 | $1,282,569 | $1,221,950 | 28.5% |

## Savings by cost cluster

| Cost cluster | Rows | Spend | Low | Base | High | Without decision | Year 1 | Base share of spend |
|---|---|---|---|---|---|---|---|---|
| Salesforce platform | 5 | $3,382,759 | $335,231 | $514,601 | $849,833 | $514,601 | $257,301 | 15.2% |
| Office footprint | 10 | $837,043 | $502,226 | $627,782 | $753,338 | $209,261 | $313,891 | 75.0% |
| Audit, tax, accounting and corporate services | 24 | $590,674 | $140,218 | $197,389 | $254,561 | $58,979 | $79,317 | 33.4% |
| Travel and entertainment | 49 | $464,995 | $77,112 | $128,519 | $179,927 | $128,519 | $96,390 | 27.6% |
| Insurance and benefits | 25 | $428,012 | $34,924 | $62,158 | $89,392 | $27,382 | $31,104 | 14.5% |
| Recruiting and HR outsourcing | 18 | $404,135 | $166,544 | $231,463 | $277,622 | $79,876 | $188,032 | 57.3% |
| Software subscriptions (non-Salesforce) | 39 | $377,257 | $116,659 | $167,641 | $218,624 | $73,877 | $63,079 | 44.4% |
| Outsourced engineering and contractors | 8 | $246,157 | $52,165 | $79,730 | $107,295 | $36,463 | $43,572 | 32.4% |
| Cloud, telecom and IT | 30 | $238,201 | $31,666 | $56,243 | $87,152 | $35,974 | $30,910 | 23.6% |
| M&A and transaction costs | 4 | $226,932 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Legal | 19 | $179,798 | $34,859 | $52,289 | $69,718 | $17,430 | $31,373 | 29.1% |
| Marketing agencies, media and memberships | 25 | $141,008 | $19,850 | $31,664 | $105,808 | $31,664 | $23,748 | 22.5% |
| Customer-mandated platform fees | 3 | $97,400 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Team events, perks and wellness | 37 | $81,157 | $25,703 | $38,554 | $48,192 | $38,554 | $28,915 | 47.5% |
| Office running costs | 44 | $71,130 | $29,834 | $41,861 | $48,107 | $12,182 | $20,961 | 58.9% |
| Student labour | 3 | $54,117 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Unidentified and individual payees | 37 | $50,939 | $10,685 | $17,809 | $24,933 | $17,809 | $13,357 | 35.0% |
| Statutory and government | 6 | $15,646 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Total | 386 | $7,887,360 | $1,577,675 | $2,247,704 | $3,114,502 | $1,282,569 | $1,221,950 | 28.5% |

## Savings by lever

| Lever | Opportunity | depends_on | Rows | Spend | Low | Base | High | Without decision | Year 1 | Base share of spend |
|---|---|---|---|---|---|---|---|---|---|---|
| Salesforce platform agreement | Salesforce platform agreement | none | 1 | $3,117,226 | $311,723 | $467,584 | $779,306 | $467,584 | $233,792 | 15.0% |
| PDF Butler OEM pricing | Salesforce platform agreement | none | 1 | $208,675 | $20,868 | $41,735 | $62,603 | $41,735 | $20,868 | 20.0% |
| Kimble PSA licences | Salesforce platform agreement | none | 1 | $52,825 | $2,641 | $5,283 | $7,924 | $5,283 | $2,641 | 10.0% |
| Slack and Yoxel inside the Salesforce renewal | Salesforce platform agreement | none | 2 | $4,033 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Office footprint | Office exit | remote_operating_model | 10 | $837,043 | $502,226 | $627,782 | $753,338 | $209,261 | $313,891 | 75.0% |
| Office running costs | Office exit | remote_operating_model | 23 | $59,359 | $29,679 | $41,551 | $47,487 | $11,872 | $20,775 | 70.0% |
| Audit, tax and accounting firms | Back office into group shared services | group_auditor | 15 | $553,641 | $138,410 | $193,774 | $249,138 | $55,364 | $77,510 | 35.0% |
| Corporate secretarial, registered agent and share registry | Back office into group shared services | none | 5 | $18,075 | $1,808 | $3,615 | $5,423 | $3,615 | $1,808 | 20.0% |
| R&D tax credit adviser (contingent fee) | Back office into group shared services | none | 1 | $13,659 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Law firms and legal resourcing | Back office into group shared services | group_legal | 12 | $174,296 | $34,859 | $52,289 | $69,718 | $17,430 | $31,373 | 30.0% |
| Employment-law settlement advice | Back office into group shared services | none | 3 | $1,930 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Recruitment agencies and job boards | Back office into group shared services | group_talent_function | 7 | $149,179 | $119,344 | $149,179 | $149,179 | $44,754 | $134,262 | 100.0% |
| LinkedIn | Back office into group shared services | group_talent_function | 1 | $55,573 | $11,115 | $16,672 | $27,786 | $11,115 | $10,003 | 30.0% |
| External training and coaching | Back office into group shared services | group_talent_function | 3 | $87,694 | $21,923 | $43,847 | $65,770 | $21,923 | $32,885 | 50.0% |
| Employer-of-record providers | Back office into group shared services | group_payroll | 3 | $89,532 | $8,953 | $13,430 | $22,383 | $0 | $6,715 | 15.0% |
| Payroll processing providers | Back office into group shared services | group_payroll | 2 | $20,838 | $5,209 | $8,335 | $12,503 | $2,084 | $4,168 | 40.0% |
| Commercial insurance through brokers | Back office into group shared services | group_insurance_programme | 2 | $152,800 | $22,920 | $38,200 | $53,480 | $15,280 | $19,100 | 25.0% |
| Employee health and life insurance | Back office into group shared services | group_insurance_programme | 10 | $237,127 | $11,856 | $23,713 | $35,569 | $11,856 | $11,856 | 10.0% |
| Statutory cover and benefit schemes | Back office into group shared services | none | 13 | $54,004 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| HR and finance systems | Back office into group shared services | group_systems | 4 | $101,762 | $61,057 | $81,410 | $101,762 | $10,176 | $20,352 | 80.0% |
| HubSpot | Back office into group shared services | parent_crm_instance | 1 | $32,187 | $19,312 | $25,750 | $32,187 | $3,219 | $6,437 | 80.0% |
| Navan | Second wave | none | 2 | $415,913 | $62,387 | $103,978 | $145,570 | $103,978 | $77,984 | 25.0% |
| Other travel, hotels, restaurants and food through AP | Second wave | none | 47 | $49,082 | $14,725 | $24,541 | $34,358 | $24,541 | $18,406 | 50.0% |
| Team events, perks and wellness | Second wave | none | 36 | $64,257 | $25,703 | $38,554 | $48,192 | $38,554 | $28,915 | 60.0% |
| Other software subscriptions | Second wave | none | 33 | $242,907 | $36,436 | $60,727 | $85,018 | $60,727 | $36,436 | 25.0% |
| AWS | Second wave | none | 2 | $111,552 | $11,155 | $22,310 | $33,466 | $22,310 | $13,386 | 20.0% |
| Telecom and internet providers | Second wave | remote_operating_model | 11 | $70,891 | $17,723 | $28,356 | $42,534 | $10,634 | $14,178 | 40.0% |
| Other cloud and IT | Second wave | none | 7 | $4,833 | $242 | $483 | $967 | $483 | $290 | 10.0% |
| Employee hardware | Second wave | group_it_procurement | 10 | $50,925 | $2,546 | $5,093 | $10,185 | $2,546 | $3,056 | 10.0% |
| Couriers and postage | Second wave | none | 9 | $3,100 | $155 | $310 | $620 | $310 | $186 | 10.0% |
| Marketing agencies | Second wave | none | 3 | $37,770 | $11,331 | $18,885 | $26,439 | $18,885 | $14,164 | 50.0% |
| TM Forum | Second wave | none | 2 | $58,070 | $0 | $0 | $58,070 | $0 | $0 | 0.0% |
| Other marketing, media and events | Second wave | none | 14 | $42,598 | $8,520 | $12,779 | $21,299 | $12,779 | $9,584 | 30.0% |
| Outsourced engineering and contractors | Second wave | group_engineering_sourcing | 4 | $216,335 | $43,267 | $64,900 | $86,534 | $21,633 | $32,450 | 30.0% |
| Unidentified and individual payees | Second wave | none | 21 | $65,276 | $19,583 | $32,638 | $45,693 | $32,638 | $24,479 | 50.0% |
| M&A and transaction costs | Excluded | none | 4 | $226,932 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Customer-mandated platform fees | Excluded | none | 3 | $97,400 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Statutory and government | Excluded | none | 6 | $15,646 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Student labour | Excluded | none | 3 | $54,117 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| One-off spend that falls away | Excluded | none | 46 | $32,998 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Bank, payment and certification fees | Excluded | none | 3 | $5,299 | $0 | $0 | $0 | $0 | $0 | 0.0% |
| Total |  |  | 386 | $7,887,360 | $1,577,675 | $2,247,704 | $3,114,502 | $1,282,569 | $1,221,950 | 28.5% |

## Assumptions behind each lever

The register, repeated next to the figures it produces. Percentages are of each row's 12-month spend; the year-1 factor is the share of the first 12 months in which the saving is live.

| Lever | Applies to | Low / base / high | Without decision | Year-1 factor | depends_on | Reasoning |
|---|---|---|---|---|---|---|
| Salesforce platform agreement | Salesforce UK (`V0002`) | 10% / 15% / 25% | 15% | 0.5 | none | The platform agreement is renegotiated at change of control, with internal seats trued down separately; the base sits below the usual licence-audit range because part of this spend is platform and ISV fees that do not shrink with a seat count, and the contract is not visible, so the figure is the value of a negotiation that starts when the contract and usage data arrive (step 4b). |
| PDF Butler OEM pricing | Cloudcrossing's PDF Butler (`V0006`) | 10% / 20% / 30% | 20% | 0.5 | none | OEM or volume pricing for a document app delivered with the product is renegotiated inside the platform review, at a renewal date the file does not show. |
| Kimble PSA licences | Kimble (`V0027`) | 5% / 10% / 15% | 10% | 0.5 | none | PSA seats on the Salesforce platform are right-sized at a renewal whose date is unknown. |
| Slack and Yoxel inside the Salesforce renewal | Slack (`V0173`) and Yoxel (`V0170`) | 0% / 0% / 0% | 0% | 0.5 | none | Both are negotiated inside the Salesforce renewal, so no separate saving is counted. |
| Office footprint | cluster Office footprint | 60% / 75% / 90% | 25% | 0.5 | remote_operating_model | The base keeps a quarter of the spend for a touchdown space at the engineering hub and registered addresses; without the decision the company right-sizes onto one flexible provider; the lease notice dates are unknown. |
| Office running costs | cluster Office running costs, recurring rows, except couriers and postage (step 4b) | 50% / 70% / 80% | 20% | 0.5 | remote_operating_model | Utilities, cleaning, parking, supplies and catering fall with the space; without the decision only consumables and catering are cut; the timing follows the leases. |
| Audit, tax and accounting firms | the auditors, accountants and tax advisers in cluster Audit, tax, accounting and corporate services, and the actuarial valuations (`V0351`) | 25% / 35% / 45% | 10% | 0.4 | group_auditor | The group auditor takes over entity by entity at the financial year-end, so year 1 is 0.4; without the decision a tender across the firms is worth 10%. |
| Corporate secretarial, registered agent and share registry | `V0088`, `V0099`, `V0105`, `V0334`, `V0305` | 10% / 20% / 30% | 20% | 0.5 | none | One provider across the entities at renewals whose dates are unknown; a vendor action that needs no group decision. |
| R&D tax credit adviser (contingent fee) | GrantTree (`V0068`) | 0% / 0% / 0% | 0% | 0.5 | none | The fee is contingent on cash recovered, so cutting it reduces cash. |
| Law firms and legal resourcing | cluster Legal, recurring rows: law firms, seconded lawyers, outsourced counsel, immigration and trade mark work | 20% / 30% / 40% | 10% | 0.6 | group_legal | Panel consolidation and the group legal function take over most external work within the year; without the decision a rate review is worth 10%. |
| Employment-law settlement advice | `V0230`, `V0231`, `V0241`: small one-off payments to employment-law firms | 0% / 0% / 0% | 0% | 0.5 | none | These are one payment per leaver for settlement-agreement advice, not a vendor relationship. |
| Recruitment agencies and job boards | the recruitment agencies, staffing firms and job boards in cluster Recruiting and HR outsourcing | 80% / 100% / 100% | 30% | 0.9 | group_talent_function | This spend follows hiring volume: with the group talent function hiring, the agencies and job boards end as open mandates close; without it, preferred suppliers and a fee cap are worth 30%. |
| LinkedIn | LinkedIn (`V0026`) | 20% / 30% / 50% | 20% | 0.6 | group_talent_function | Recruiter seats fall when the group talent function does the hiring; the seat review alone is worth 20% at the next renewal. |
| External training and coaching | leadership development, coaching and skills training in cluster Recruiting and HR outsourcing (`V0020`, `V0075`, `V0079`) | 25% / 50% / 75% | 25% | 0.75 | group_talent_function | Added in step 4: the group's own development programmes replace discretionary coaching and training; without the decision a cap on coaching spend is worth 25%; the change starts within 90 days. |
| Employer-of-record providers | `V0016`, `V0090`, `V0179` | 10% / 15% / 25% | 0% | 0.5 | group_payroll | These invoices usually carry the employees' pay as a pass-through, so only the service fee is addressable, and only group payroll removes it. |
| Payroll processing providers | `V0111`, `V0058` | 25% / 40% / 60% | 10% | 0.5 | group_payroll | Group payroll replaces outsourced processing as each country migrates; without it a re-tender is worth 10%. |
| Commercial insurance through brokers | the broker and the US agency (`V0010`, `V0078`) | 15% / 25% / 35% | 10% | 0.5 | group_insurance_programme | Cover placed through brokers moves into the group programme at renewal; without the decision a re-broke is worth 10%. |
| Employee health and life insurance | the health and life insurers, the benefits consultant and the telehealth plan (`V0012`, `V0042`, `V0045`, `V0047`, `V0069`, `V0071`, `V0095`, `V0143`, `V0098`, `V0273`) | 5% / 10% / 15% | 5% | 0.5 | group_insurance_programme | Benefits are part of pay, so the lever is broking and scheme terms, not cover; the group programme improves the terms, and broking alone is worth 5%. |
| Statutory cover and benefit schemes | statutory workers' compensation and occupational health (`V0094`, `V0201`, `V0212`, `V0300`, `V0328`, `V0382`, `V0383`, `V0384`), salary-sacrifice schemes (`V0100`, `V0195`), meal cards (`V0054`, `V0128`) and the MultiSport gym scheme (`V0057`; Gym4You, `V0121`, consolidates into it from step 4b) | 0% / 0% / 0% | 0% | 0.5 | none | Pay and statutory cover are people decisions outside a vendor model. |
| HR and finance systems | accounting, planning, engagement and performance systems (`V0028`, `V0039`, `V0055`, `V0080`) | 60% / 80% / 100% | 10% | 0.25 | group_systems | The saving starts after the migration to the parent's HRIS and ERP, so year 1 is 0.25; the base nets off extra seats on the group's systems; without the decision a seat review is worth 10%. |
| HubSpot | HubSpot (`V0037`) | 60% / 80% / 100% | 10% | 0.25 | parent_crm_instance | Marketing automation moves onto the parent's CRM instance after migration, netting off extra seats there; without the decision a seat review is worth 10%. |
| Navan | Navan (`V0003`, `V0024`) | 15% / 25% / 35% | 25% | 0.75 | none | A travel policy on one entity starts within 90 days; the saving is on the travel booked through the platform, not on a platform fee. |
| Other travel, hotels, restaurants and food through AP | cluster Travel and entertainment except Navan, recurring or not | 30% / 50% / 70% | 50% | 0.75 | none | Travel and meals paid directly move under the policy and through Navan; part of this spend returns through expenses, which is why the base is 50%. |
| Team events, perks and wellness | cluster Team events, perks and wellness except the MultiSport card, recurring or not | 40% / 60% / 75% | 60% | 0.75 | none | The rest stays as a per-head culture budget; the policy starts within 90 days. |
| Other software subscriptions | cluster Software subscriptions (non-Salesforce), recurring rows, except the HR and finance systems and HubSpot; also the benefits platform (`V0211`) | 15% / 25% / 35% | 25% | 0.6 | none | Overlapping tools are consolidated and seats trued down at renewals spread through the year. |
| AWS | AWS (`V0014`, `V0103`) | 10% / 20% / 30% | 20% | 0.6 | none | Savings plans and one organisation for the accounts under two entities, bought within the year. |
| Telecom and internet providers | the telecom, internet and mobile lines in cluster Cloud, telecom and IT | 25% / 40% / 60% | 15% | 0.5 | remote_operating_model | Office lines end with the offices; without the decision a re-tender of lines and plans is worth 15%; the contract end dates are unknown. |
| Other cloud and IT | the rest of cluster Cloud, telecom and IT: IT services, software escrow, domains and DNS, telephony numbers and the SMS API | 5% / 10% / 20% | 10% | 0.6 | none | Scope and price reviews on escrow, domains and IT services at renewals spread through the year; small vendor actions. |
| Employee hardware | the nine hardware rows and the Chennai distributor (`V0066`, `V0123`, `V0131`, `V0167`, `V0172`, `V0175`, `V0229`, `V0260`, `V0378`, `V0048`) | 5% / 10% / 20% | 5% | 0.6 | group_it_procurement | Group IT procurement prices and a standard device list (step 4b); without the decision a preferred reseller is worth 5%; small, because hardware follows headcount. |
| Couriers and postage | the courier, postage, delivery and mail rows in cluster Office running costs (`V0196`, `V0232`, `V0240`, `V0303`, `V0316`, `V0336`, `V0368`, `V0371`, `V0377`) | 5% / 10% / 20% | 10% | 0.6 | none | One courier account and a postage policy (step 4b); a remote company still ships parcels, so the saving is price, not volume. |
| Marketing agencies | the marketing, media and PR agencies (`V0050`, `V0056`, `V0184`) | 30% / 50% / 70% | 50% | 0.75 | none | Agency retainers are consolidated or ended within 90 days. |
| TM Forum | TM Forum (`V0025`, `V0249`) | 0% / 0% / 100% | 0% | 0.5 | none | A go-to-market credential; the high case applies only if the parent holds a membership that covers subsidiaries. |
| Other marketing, media and events | the rest of cluster Marketing agencies, media and memberships, recurring rows | 20% / 30% / 50% | 30% | 0.75 | none | Media, events, memberships, print and stock assets are cut back under one marketing budget within 90 days. |
| Outsourced engineering and contractors | the consultancies and development firms in cluster Outsourced engineering and contractors (`V0009`, whose share is provisional until Finance confirms the entity, question 3; `V0019`, `V0116`, `V0185`) | 20% / 30% / 40% | 10% | 0.5 | group_engineering_sourcing | The work continues, so the saving is the rate difference between the consultancies and the group's engineering sourcing; without the decision a rate renegotiation is worth 10%. |
| Unidentified and individual payees | cluster Unidentified and individual payees, recurring rows, and the unidentified contractors (`V0065`, `V0074`, `V0137`) | 30% / 50% / 70% | 50% | 0.75 | none | Payments stop until Finance identifies the payee, and some are then re-approved; the stop starts within 90 days. |
| M&A and transaction costs | cluster M&A and transaction costs | 0% / 0% / 0% | 0% | 0.5 | none | Non-recurring deal costs that fall away without action. |
| Customer-mandated platform fees | cluster Customer-mandated platform fees | 0% / 0% / 0% | 0% | 0.5 | none | Fees a customer requires the company to pay: not addressable. |
| Statutory and government | cluster Statutory and government | 0% / 0% / 0% | 0% | 0.5 | none | Taxes, government fees and regulators: not addressable. |
| Student labour | cluster Student labour | 0% / 0% / 0% | 0% | 0.5 | none | Workforce cost, set by the hiring plan, not a vendor action. |
| One-off spend that falls away | any other row with `is_recurring` FALSE, outside Travel and entertainment and Team events, perks and wellness | 0% / 0% / 0% | 0% | 0.5 | none | One-off spend falls away without action, so no saving is claimed on it; one-off payments to individuals are a control finding, not a saving (step 4b). |
| Bank, payment and certification fees | bank fees, payment processing and ISO certification audits (`V0216`, `V0198`, `V0142`) | 0% / 0% / 0% | 0% | 0.5 | none | Added in step 4: fees set by transaction volume or by the certificates customers ask for, with no vendor action modelled. |

## Acquirer decisions

For each decision: the base saving of the levers that depend on it, what vendor action alone achieves without it, and the difference as the value of the decision. A lever with no tag is in none of these rows.

| Decision | Levers | Rows | Spend | Saving with the decision (base) | Saving without it | Value of the decision | Year 1 with the decision |
|---|---|---|---|---|---|---|---|
| `remote_operating_model` | Office footprint; Office running costs; Telecom and internet providers | 44 | $967,292 | $697,689 | $231,766 | $465,923 | $348,845 |
| `group_talent_function` | Recruitment agencies and job boards; LinkedIn; External training and coaching | 11 | $292,446 | $209,698 | $77,792 | $131,906 | $177,150 |
| `group_insurance_programme` | Commercial insurance through brokers; Employee health and life insurance | 12 | $389,927 | $61,913 | $27,136 | $34,776 | $30,956 |
| `group_auditor` | Audit, tax and accounting firms | 15 | $553,641 | $193,774 | $55,364 | $138,410 | $77,510 |
| `parent_crm_instance` | HubSpot | 1 | $32,187 | $25,750 | $3,219 | $22,531 | $6,437 |
| `group_it_procurement` | Employee hardware | 10 | $50,925 | $5,093 | $2,546 | $2,546 | $3,056 |
| `group_payroll` | Employer-of-record providers; Payroll processing providers | 5 | $110,370 | $21,765 | $2,084 | $19,681 | $10,882 |
| `group_systems` | HR and finance systems | 4 | $101,762 | $81,410 | $10,176 | $71,233 | $20,352 |
| `group_legal` | Law firms and legal resourcing | 12 | $174,296 | $52,289 | $17,430 | $34,859 | $31,373 |
| `group_engineering_sourcing` | Outsourced engineering and contractors | 4 | $216,335 | $64,900 | $21,633 | $43,267 | $32,450 |
| Total |  | 118 | $2,889,181 | $1,414,281 | $449,146 | $965,134 | $739,012 |

## Largest vendor savings

The 15 rows with the largest base saving.

| vendor_id | Vendor | Cost cluster | Lever | Spend | Low | Base | High | Without decision | Year 1 | depends_on |
|---|---|---|---|---|---|---|---|---|---|---|
| V0002 | Salesforce UK Ltd | Salesforce platform | Salesforce platform agreement | $3,117,226 | $311,723 | $467,584 | $779,306 | $467,584 | $233,792 | none |
| V0005 | TOG UK Properties Limited | Office footprint | Office footprint | $263,821 | $158,293 | $197,866 | $237,439 | $65,955 | $98,933 | remote_operating_model |
| V0007 | Zagrebtower d.o.o. | Office footprint | Office footprint | $183,754 | $110,253 | $137,816 | $165,379 | $45,939 | $68,908 | remote_operating_model |
| V0004 | BDO LLP | Audit, tax, accounting and corporate services | Audit, tax and accounting firms | $343,081 | $85,770 | $120,078 | $154,387 | $34,308 | $48,031 | group_auditor |
| V0008 | Innovent Spaces Private Limited | Office footprint | Office footprint | $147,348 | $88,409 | $110,511 | $132,613 | $36,837 | $55,255 | remote_operating_model |
| V0011 | GPT Space & Co | Office footprint | Office footprint | $133,507 | $80,104 | $100,130 | $120,156 | $33,377 | $50,065 | remote_operating_model |
| V0003 | Navan (TripActions Inc) | Travel and entertainment | Navan | $357,984 | $53,698 | $89,496 | $125,294 | $89,496 | $67,122 | none |
| V0021 | Harmonic Group Limited | Recruiting and HR outsourcing | Recruitment agencies and job boards | $65,418 | $52,334 | $65,418 | $65,418 | $19,625 | $58,876 | group_talent_function |
| V0022 | WeWork Singapore Pte. Ltd. | Office footprint | Office footprint | $64,373 | $38,624 | $48,280 | $57,936 | $16,093 | $24,140 | remote_operating_model |
| V0009 | Weking d.o.o. | Outsourced engineering and contractors | Outsourced engineering and contractors | $144,093 | $28,819 | $43,228 | $57,637 | $14,409 | $21,614 | group_engineering_sourcing |
| V0006 | Cloudcrossing BVBA | Salesforce platform | PDF Butler OEM pricing | $208,675 | $20,868 | $41,735 | $62,603 | $41,735 | $20,868 | none |
| V0034 | Mason Frank International Ltd | Recruiting and HR outsourcing | Recruitment agencies and job boards | $38,148 | $30,518 | $38,148 | $38,148 | $11,444 | $34,333 | group_talent_function |
| V0028 | Sage UK Limited | Software subscriptions (non-Salesforce) | HR and finance systems | $46,895 | $28,137 | $37,516 | $46,895 | $4,689 | $9,379 | group_systems |
| V0010 | Jensten Insurance Brokers | Insurance and benefits | Commercial insurance through brokers | $142,700 | $21,405 | $35,675 | $49,945 | $14,270 | $17,837 | group_insurance_programme |
| V0020 | Big Frontier Pty Ltd (Cult Of Monday) | Recruiting and HR outsourcing | External training and coaching | $66,131 | $16,533 | $33,066 | $49,598 | $16,533 | $24,799 | group_talent_function |

## Savings on non-recurring rows

116 rows have `is_recurring` FALSE ($330,678). A saving sits on them only in Travel and entertainment and Team events, perks and wellness, where the category recurs even when the payee does not; every other non-recurring row is in "One-off spend that falls away" at 0%.

| Lever | Non-recurring rows | Spend | Base saving | Year 1 |
|---|---|---|---|---|
| Other travel, hotels, restaurants and food through AP | 34 | $36,562 | $18,281 | $13,711 |
| Team events, perks and wellness | 28 | $20,618 | $12,371 | $9,278 |
| Employment-law settlement advice | 3 | $1,930 | $0 | $0 |
| M&A and transaction costs | 4 | $226,932 | $0 | $0 |
| One-off spend that falls away | 46 | $32,998 | $0 | $0 |
| Statutory and government | 1 | $11,637 | $0 | $0 |
| Total | 116 | $330,678 | $30,652 | $22,989 |

The ten largest:

| vendor_id | Vendor | Lever | Spend | Base saving |
|---|---|---|---|---|
| V0077 | Poles Ltd - Hanbury Manor | Other travel, hotels, restaurants and food through AP | $10,488 | $5,244 |
| V0102 | Athlete Service Ltd | Team events, perks and wellness | $5,285 | $3,171 |
| V0101 | Tattu Manchester Limited | Other travel, hotels, restaurants and food through AP | $5,366 | $2,683 |
| V0112 | Inter Continental Chennai Mahabalipuram Resort | Other travel, hotels, restaurants and food through AP | $4,393 | $2,196 |
| V0115 | Puducherry Backwater Resort Private Limited | Other travel, hotels, restaurants and food through AP | $4,056 | $2,028 |
| V0146 | Good Game Global d.o.o. | Team events, perks and wellness | $2,954 | $1,772 |
| V0162 | Pink Ribbon Shop | Team events, perks and wellness | $2,251 | $1,350 |
| V0154 | Cleverland Winery Resort | Other travel, hotels, restaurants and food through AP | $2,663 | $1,331 |
| V0183 | Paint & Fun Vl. Martina Milkova Nikolova | Team events, perks and wellness | $1,654 | $993 |
| V0187 | Lajnap Comedy Booking d.o.o. | Team events, perks and wellness | $1,536 | $922 |

## Reconciliation

The vendor rows sum to the levers, the clusters and the opportunities. Largest difference: $0.00.

| Measure | Vendor rows | Sum of levers | Sum of clusters | Sum of opportunities | Largest difference |
|---|---|---|---|---|---|
| Rows | 386 | 386 | 386 | 386 | 0 |
| Spend | $7,887,360.40 | $7,887,360.40 | $7,887,360.40 | $7,887,360.40 | $0.00 |
| Low | $1,577,675.01 | $1,577,675.01 | $1,577,675.01 | $1,577,675.01 | $0.00 |
| Base | $2,247,703.53 | $2,247,703.53 | $2,247,703.53 | $2,247,703.53 | $0.00 |
| High | $3,114,502.20 | $3,114,502.20 | $3,114,502.20 | $3,114,502.20 | $0.00 |
| Without decision | $1,282,569.07 | $1,282,569.07 | $1,282,569.07 | $1,282,569.07 | $0.00 |
| Year 1 | $1,221,950.21 | $1,221,950.21 | $1,221,950.21 | $1,221,950.21 | $0.00 |

## Lever assignments decided in this step

Rows whose lever is an analyst call rather than a cluster rule or a row the register names (`docs/savings_assumptions.md`, "Lever assignment").

| vendor_id | Vendor | Lever | Why |
|---|---|---|---|
| V0020 | Big Frontier Pty Ltd (Cult Of Monday) | External training and coaching | a lever added in step 4, because the assumptions list has no line for training |
| V0057 | Benefit Systems d.o.o. | Statutory cover and benefit schemes | the MultiSport card is the gym scheme the assumption names; it stays as an employee benefit at the hub (step 4b), and Gym4You consolidates into it on the Team events lever |
| V0058 | Smart Group Services d.o.o. | Payroll processing providers | HR outsourcing, unconfirmed; the closest lever by sub_function, and its rationale already waits for group payroll |
| V0065 | Pingo d.o.o. | Unidentified and individual payees | Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of its cluster |
| V0074 | Bijeli Pijesak Obrt Za Poslovno Savjetovanje | Unidentified and individual payees | Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of its cluster |
| V0075 | Ramiro d.o.o. | External training and coaching | a lever added in step 4, because the assumptions list has no line for training |
| V0076 | Visalogic Limited | Law firms and legal resourcing | immigration work follows the legal cluster into the panel |
| V0079 | Emerge Development Consultancy Ltd | External training and coaching | a lever added in step 4, because the assumptions list has no line for training |
| V0098 | Mercer Limited | Employee health and life insurance | benefits consulting is the broking and scheme-terms work that the lever describes |
| V0137 | Orcola d.o.o. | Unidentified and individual payees | Terminate until identified, so the unidentified-payee lever rather than the engineering sourcing lever of its cluster |
| V0142 | Bureau Veritas Croatia d.o.o. | Bank, payment and certification fees | a lever added in step 4 at 0%, because the assumptions list has no line for certification audits |
| V0168 | Cision PR Newswire | Other marketing, media and events | a press release wire, not an agency |
| V0179 | Radius Group, Inc | Employer-of-record providers | global payroll and expansion services are employer-of-record work |
| V0198 | FastSpring | Bank, payment and certification fees | a lever added in step 4 at 0%, because the assumptions list has no line for payment processing |
| V0203 | Amazon.co.uk | Office running costs | follows its cluster as office consumables (confirmed in step 4b), although the card policy that removes it does not depend on the office decision |
| V0211 | Computershare-Caboodle Technology Limited | Other software subscriptions | a benefits platform fee, not pay or cover, so it is software rather than a benefit scheme |
| V0216 | Raiffeisenbank Austria d.d. | Bank, payment and certification fees | a lever added in step 4 at 0%, because the assumptions list has no line for bank fees |
| V0273 | Doctor Anywhere Operations Pte Ltd | Employee health and life insurance | a health benefit for Singapore staff |
| V0291 | Amazon (Aus) | Office running costs | follows its cluster as office consumables (confirmed in step 4b), although the card policy that removes it does not depend on the office decision |
| V0309 | Avoxi Inc | Other cloud and IT | telephony numbers that do not end with the offices, so not the telecom lever |
| V0351 | Mithras Consultants | Audit, tax and accounting firms | actuarial valuations are an accounting requirement of the Indian entity, so they follow the group auditor |
| V0363 | Click Send Pty Ltd | Other cloud and IT | an SMS API that does not end with the offices, so not the telecom lever |
