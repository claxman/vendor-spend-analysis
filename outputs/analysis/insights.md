# Insights

Written 2026-11-11 by `scripts/04_insights.py` from `outputs/vendors_classified.csv`, `outputs/analysis/savings.csv`, `qa/vendor_groups.csv`, `outputs/analysis/01_forensic_flags.csv`, `qa/verification_exceptions.csv`, `docs/savings_assumptions.md` and `docs/decisions.md`. Every figure is computed from those files and every finding names its rows. Total spend in the file: $7,887,360 across 386 rows and 381 vendors after the 5 merges. Whole dollars; the costs are the file's modified values.

## 1. Platform dependency and concentration

- The product runs on Salesforce. `V0002` Salesforce UK Ltd is $3,117,226, 39.5% of all spend, and the Salesforce platform cluster (the platform, PDF Butler, Kimble, Yoxel and Slack: `V0002`, `V0006`, `V0027`, `V0170`, `V0173`) is $3,382,759, 42.9%. Salesforce-specialist labour adds $182,241 (`V0009`, `V0034`).
- Concentration on the merged view: the top vendor is 39.5% of spend, the top 10 are 64.7%, the top 50 are 89.0%; the other 331 vendors share 11.0%.
- The platform agreement is the largest single lever in the model, $467,584 base run-rate ($311,723 to $779,306), and the largest dependency: the lever is commercial terms at change of control, never exit, and the figure is the value of a negotiation that starts when the contract and usage data arrive (Finance question 2).

## 2. What falls away without action, the recurring base, and the sale-related share

- Non-recurring spend: 117 rows, $345,186 (4.4%). Of it, M&A and transaction costs (`V0013`, `V0031`, `V0035`, `V0036`) are $226,932 and fall away with the sale; another 46 one-off rows ($47,199) fall away without action and carry no saving in the model; 63 rows ($57,488) in travel and team events carry a saving because the category recurs even when the payee does not.
- The recurring base is 269 rows, $7,542,174 (95.6%).
- It still holds $457,034 of adviser spend that plausibly includes sale-related work: `V0004`, `V0018`, `V0029` (BDO, Bisley Law, Grant Thornton; step 2e). The recurring figure is therefore likely lower than shown; Finance question 6 asks for the sale-related share.

## 3. Vendors that must not be cut

- Customer-mandated platform fees (Telefónica, Ariba): 3 rows, $97,400 (1.2%); `V0015`, `V0093`, `V0191`
- Software escrow for customer contracts: 1 row, $3,036 (0.0%); `V0144`
- ISO certification audits: 1 row, $3,200 (0.0%); `V0142`
- Statutory workers' compensation and occupational health: 8 rows, $8,610 (0.1%); `V0094`, `V0201`, `V0212`, `V0300`, `V0328`, `V0382`, `V0383`, `V0384`
- Taxes, government fees, regulators and the depository: 6 rows, $15,646 (0.2%); `V0073`, `V0139`, `V0284`, `V0333`, `V0353`, `V0361`
- Salary-sacrifice schemes (cycle to work, novated leasing): 2 rows, $6,689 (0.1%); `V0100`, `V0195`
- Meal and benefit cards: 2 rows, $21,804 (0.3%); `V0054`, `V0128`
- The contingent-fee R&D tax credit adviser: 1 row, $13,659 (0.2%); `V0068`
- Together $170,046. The 17 rows outside the savings base ($121,657) are among them; the rest stay addressable but carry a 0% assumption or a keep-and-review rationale in the classification.

## 4. Control findings

- Duplicate vendor records: 5 vendors appear under two names each (Navan (TripActions Inc) and Navan, Inc, `V0003`, `V0024`; Amazon Web Services LLC and Amazon Web Services Inc., `V0014`, `V0103`; 4i Advisory Services and 4i Management Consulting Private Limited, `V0017`, `V0072`; Tmforum and TM Forum, `V0025`, `V0249`; Sodexo SVC India Private Limited and Pluxee India Private Limited, `V0054`, `V0128`), $691,318 in all; two more names carry a Supplier tag that suggests a second record of the same company (`V0047`, `V0163`). A vendor master with duplicate records calls for a duplicate-payment review, which needs invoice-level data: this file holds 12-month totals, and its identical amounts are explained by the cost modification (`outputs/analysis/01_forensics.md`, section 2).
- Individual and unnamed payees: 6 individuals paid through AP ($12,220; `V0160`, `V0165`, `V0166`, `V0169`, `V0177`, `V0178`), 2 single-word names that may be people (`V0148`, `V0373`) and one payment with no vendor name (`V0325`, $137). Each is a contractor-status or reimbursement question before it is a saving.
- A law firm paid under a name that no longer trades: `V0018` Bisley Law Ltd, $67,414. The firm merged into Gordons Partnership in January 2024 and its company is now registered as non-trading, so the question for Finance is which entity invoices now (question 7). The provider of this data also modified vendor names, so an unmatched name is a question, not evidence of a problem. The spend is legal work and follows the law-firms lever whoever the payee proves to be; the payee check is a control action.
- Sole traders paid at contractor scale: 3 Croatian obrt rows of $5,000 or more, $48,815 (`V0038`, `V0074`, `V0092`), and 13 Croatian companies of unknown function ($309,614, led by `V0009` Weking at $144,093, whose $43,228 base saving is provisional until Finance confirms the work it supplies). One-person businesses supplying labour carry an employment-status question as well as an identification one; with modified vendor names, an unidentified name is a question for Finance, not a finding against the payee.
- Retail merchants in the vendor master: the forensic pass flags 56 consumer or retail payees, $83,926; 5 of them are employee hardware that stays (`V0123`, `V0172`, `V0175`, `V0229`, `V0378`), the other 51 ($75,640) are food, groceries, gifts, gyms and marketplaces that a purchasing-card and expense policy removes from the vendor master. The vendor count falls from 381 to 330 once they go.

## 5. Country and legal-entity footprint

Where the statutory, payroll, secretarial, insurance and audit payees place the company's entities and staff. Each id is a row whose sub_function or description names the country.

| Country | Statutory | Payroll and employer of record | Corporate secretarial and registry | Insurance | Benefit schemes | Audit, tax and accounting | Bank | Spend of these rows |
|---|---|---|---|---|---|---|---|---|
| United Kingdom | `V0353` |  |  | `V0010`, `V0047` | `V0100`, `V0211` | `V0004`, `V0070`, `V0108`, `V0068` |  | $546,447 |
| Croatia | `V0073`, `V0139`, `V0300`, `V0328`, `V0382`, `V0383`, `V0384` |  |  | `V0042` |  | `V0067`, `V0114`, `V0176` | `V0216` | $61,042 |
| India | `V0284` |  | `V0305` | `V0045`, `V0095`, `V0143` | `V0054`, `V0128` | `V0017`, `V0072`, `V0164`, `V0351` |  | $141,734 |
| Australia | `V0333`, `V0201`, `V0094`, `V0212` | `V0111` |  | `V0071` | `V0195` | `V0153` |  | $29,203 |
| Singapore |  |  | `V0088` | `V0069` | `V0273` | `V0109` |  | $25,791 |
| United States |  |  | `V0105`, `V0334` | `V0078` |  | `V0064` |  | $29,858 |
| Germany and Switzerland |  | `V0016`, `V0090` |  |  |  |  |  | $87,810 |
| Greece |  |  |  |  |  | `V0052` |  | $18,164 |
| Cayman Islands | `V0361` |  |  |  |  |  |  | $56 |

- Nine jurisdictions show, with Aetna (`V0012`, $124,661) writing expatriate cover from Bermuda and Acclime (`V0099`) serving an Asian entity the file does not name. The Cayman Islands fee (`V0361`) implies an entity the legal-entity map should confirm (Finance question 5).
- The cost that follows the footprint: the audit, tax and accounting firms, the employer-of-record and payroll providers and the corporate secretarial and registry providers are 25 rows, $682,086 (8.6%), with a base saving of $219,154 that depends on `group_auditor` and `group_payroll`. Every entity kept keeps an auditor, a payroll and a company secretary.

## 6. Software overlap

Software rows (the Salesforce platform and the non-Salesforce subscriptions): 44 rows, $3,760,016. Tools per function after the step 3c reading:

| Department | Tools | Spend | Rows |
|---|---|---|---|
| SaaS | 5 | $3,330,045 | `V0002`, `V0006`, `V0130`, `V0311`, `V0350` |
| G&A | 18 | $179,369 | `V0023`, `V0032`, `V0055`, `V0060`, `V0080`, `V0081`, `V0089`, `V0091`, `V0117`, `V0145`, `V0173`, `V0194`, `V0221`, `V0276`, `V0281`, `V0288`, `V0297`, `V0310` |
| Finance | 3 | $75,246 | `V0028`, `V0039`, `V0238` |
| Marketing | 3 | $62,008 | `V0037`, `V0041`, `V0133` |
| Professional Services | 2 | $56,367 | `V0027`, `V0124` |
| Sales | 5 | $40,944 | `V0040`, `V0084`, `V0156`, `V0170`, `V0352` |
| Engineering | 6 | $11,888 | `V0113`, `V0125`, `V0155`, `V0204`, `V0254`, `V0366` |
| Product | 2 | $4,149 | `V0122`, `V0259` |

- G&A holds 14 company-wide tools under Corporate IT ($151,092). The overlaps the classification names, each a Consolidate or Terminate case:
  - Two productivity suites: $70,483 (`V0023`, `V0081`)
  - Three work-management tools and an Atlassian partner: $49,235 (`V0091`, `V0145`, `V0297`, `V0032`)
  - Two integration and automation platforms: $16,268 (`V0060`, `V0310`)
  - Three contact and intent data tools: $29,694 (`V0040`, `V0156`, `V0352`)
  - Three monitoring and logging tools: $4,144 (`V0130`, `V0311`, `V0350`)
  - Two meeting and messaging tools: $9,306 (`V0173`, `V0089`)
  - Three document and e-signature tools: $5,538 (`V0194`, `V0281`, `V0117`)
  - Two learning platforms: $1,151 (`V0221`, `V0276`)
  - Marketing automation (HubSpot) alongside the Salesforce platform's own marketing: $32,187 (`V0037`)

## 7. Signs of leavers in the last 12 months

The file has no headcount, but some rows are the kind of spend that leavers and a shrinking footprint produce:
- three one-off payments to UK employment-law firms, of the size of an employer's contribution to a departing employee's settlement-agreement advice: $1,930 (`V0230`, `V0231`, `V0241`)
- a laptop and monitor return service for employers with remote staff: $88 (`V0345`)
- two office moves and a self-storage unit for office equipment or archives: $2,951 (`V0161`, `V0269`, `V0282`)
- a virtual UK address and mail scanning: $670 (`V0232`)
- What it implies: seat counts and space should be sized on current headcount, not on the 12 months of spend. The seat-based rows (`V0002`, `V0023`, `V0081`, `V0173`, `V0026`, `V0027`) are $3,298,096, and the coworking and office rows (10 rows) are $837,043; both are priced for the peak if staff have left. Headcount by site and entity, now and 12 months ago, is the data request in section 10.

## 8. Retention risk at the engineering hub

- 117 rows name Croatia, Zagreb or Split in their sub_function or description, $625,379 (7.9%): the hub's office and parking ($191,225; `V0007`, `V0224`, `V0134`, `V0147`), student labour ($54,117; `V0030`, `V0086`, `V0186`), the Salesforce consultancy and the unidentified contractors ($173,752; `V0009`, `V0065`, `V0074`, `V0137`) and the perks and events ($56,937; `V0057`, `V0121`, `V0038`, `V0096`).
- The model cuts the hub from several sides at once: 60% off team events, 30% off the consultancies, the end of the agency hiring, and the office exit keeps only a touchdown space. The MultiSport card and the gym are at 0% in the model but Terminate in the classification. Product knowledge sits with the consultancy's developers (`V0009` risk note), so the sequence matters: transfer the knowledge and settle the sourcing model before the perks and the space change, and keep the per-head culture budget the team-events assumption leaves.

## 9. Timing constraints

The year-1 saving is $1,208,570 against a base run-rate of $2,229,687, because the levers wait for dates the file does not show:

| Year-1 factor | What it waits for | Levers |
|---|---|---|
| 0.25 | a system migration | HR and finance systems; HubSpot |
| 0.4 | the financial year-end, when an auditor changes | Audit, tax and accounting firms |
| 0.5 | a renewal or notice date the file does not show | Salesforce platform agreement; PDF Butler OEM pricing; Kimble PSA licences; Office footprint; Office running costs; Corporate secretarial, registered agent and share registry; Employer-of-record providers; Payroll processing providers; Commercial insurance through brokers; Employee health and life insurance; Telecom and internet providers; Outsourced engineering and contractors |
| 0.6 | renewals spread through the year | Law firms and legal resourcing; LinkedIn; Other software subscriptions; AWS; Other cloud and IT; Employee hardware; Couriers and postage |
| 0.75 | a policy change within 90 days | External training and coaching; Navan; Other travel, hotels, restaurants and food through AP; Team events, perks and wellness; Marketing agencies; Other marketing, media and events; Unidentified and individual payees |
| 0.9 | open mandates closing | Recruitment agencies and job boards |

- Insurance renewals: the broker and the insurers (`V0010`, `V0012`, `V0042`, `V0045`, `V0047`, `V0069`, `V0071`, `V0095`, `V0143`) move at renewal, and the file does not show when that is.
- Audit year-end: the group auditor takes over at the year-end of each entity (`V0004`, `V0017`, `V0029`, `V0114` and the other firms in section 5).
- Lease notice: the office footprint (`V0005`, `V0007`, `V0008`, `V0011`, `V0022` and the smaller rows) follows notice periods that are not in the file.
- System migration: Sage, Planful, Peakon, Performancepro and HubSpot (`V0028`, `V0039`, `V0055`, `V0080`, `V0037`) save only after the migration to the parent's systems, so they carry a 0.25 factor.

## 10. Data limits and the requests that follow

- The file is one 12-month total per vendor: no dates, invoices, entities, cost centres or approvers, and the costs were modified by the data owner. 67 rows ($96,270) could not be verified on the web and 85 rows ($278,612) carry low confidence; 69 payees ($472,522) have names that do not show their function. The provider of this data modified vendor names, so a name that matches no trading firm, or that the web does not confirm, is a question for Finance and never evidence of a problem with the payee. The Salesforce contract, 39.5% of spend, is not visible. 8 questions for Finance are open in `docs/decisions.md`.
- Requests, in the order they unlock the figures:
  1. The monthly AP ledger for the 12 months, with invoice number, date, paying entity, cost centre and approver: it settles the duplicate-payment review, the one-off against recurring split, the leavers question and the identification of the payees in section 4.
  2. The contract register with renewal and notice dates for insurance, the leases and coworking, the Salesforce agreement, the HR and finance systems and the telecom lines: it turns the year-1 factors in section 9 from conventions into dates.
  3. The Salesforce contract and usage: licence counts by product, the split between platform and ISV fees and internal CRM seats, the OEM terms for PDF Butler, and any change-of-control clause.
  4. Headcount by site and entity, now and 12 months ago: it sizes the seats, the space, the payroll and the insurance cover, and it tests the leavers reading in section 7.
