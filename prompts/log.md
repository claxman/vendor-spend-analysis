# Prompt log

Every prompt given to Claude for this project, verbatim, in the order received.

## Prompt 1 (2026-11-10)

```text
Initialise a git repo here, create CLAUDE.md with the content I paste next, create the folders data/raw, outputs/batches, outputs/analysis, scripts, qa, prompts, docs/evidence, add a .gitignore for Python, make the first commit, then create a public GitHub repo named vendor-spend-analysis with gh and push.
```

## Prompt 2 (2026-11-10)

Pasted content for CLAUDE.md:

```text
# Vendor Spend Analysis (acquisition due diligence)

Role: I am the VP of Operations of an acquired company. The final memo is for the CEO and CFO of the parent.
Input: data/raw/vendor_analysis_assessment.xlsx (about 400 vendors, 12 months of spend; real vendors with modified names and costs). Never modify the raw file.
Outputs: outputs/vendors_classified.csv, outputs/analysis/, outputs/top3_opportunities.md, outputs/methodology.md, outputs/memo.md, README.md.

Rules
- Never invent facts about a vendor or the company. If a vendor's function cannot be inferred from its name, say so and set confidence=low.
- Descriptions are one line and specific: what the vendor does and for which team. Banned phrases: "business services", "software company", "service provider", "solutions", "various services", "technology company".
- Departments only from docs/taxonomy.md. Recommendations only from {Terminate, Consolidate, Optimize}, each with a one-sentence rationale.
- Every savings figure is computed by a script from the spend data, with its assumption written next to it.
- Every number in the memo must trace to a file in outputs/analysis.
- Append every prompt I give you to prompts/log.md verbatim before acting on it.
- Commit after each step with a message naming the step.
- No em dashes anywhere.
```

## Prompt 3 (2026-11-10)

```text
Commit the raw file as "Step 0b: add raw vendor data". Do not add it to .gitignore.
```

## Prompt 4 (2026-11-10)

```text
Read data/raw/vendor_analysis_assessment.xlsx. For every sheet list the columns, row count, data types, blanks, exact and fuzzy duplicate vendor names, currency hints, total 12-month spend, and the spend distribution: top 10 vendors and their share, top 50 share, count and total of vendors under $1,000. Write it to outputs/analysis/00_data_profile.md with the cleaning steps you propose. Do not change the raw file.
```

## Prompt 5 (2026-11-10)

Prompts 5 and 6 arrived together in one message. Prompt 6 was pasted twice with identical text; it is logged once.

```text
Before the taxonomy work, run a forensic pass on the workbook and write outputs/analysis/01_forensics.md. Check and report: hidden or very-hidden sheets, hidden rows and columns, cell notes and comments, defined names, conditional formats, white-on-white text, data validation on every column, anything in columns F to O and rows 388 to 814 beyond formatting. Then on the vendor rows: groups of rows sharing an identical cost value to the cent (possible duplicate payments or duplicated rows); near-duplicate names across the whole list after mojibake repair and legal-form stripping; names that look like individuals; names that look like consumer or retail purchases (Apple, Amazon, food, streaming, gyms); government, tax, court and regulator payees; memberships and associations; agencies and recruiters; insurers and benefits; telecoms and utilities; any vendor that is plausibly a customer rather than a supplier; costs that are round numbers versus costs with many decimals, and whether that precision split means anything; and the distribution of first digits. For each finding say what it implies for classification or for the memo. Flag anything suspicious you cannot explain. Commit as "Step 1b: forensic pass". Do not classify anything yet.
```

## Prompt 6 (2026-11-10)

```text
The workbook structure audit has been done separately: no hidden sheets, rows or columns, no comments, no defined names, no conditional formats, no content beyond A1:E387; the only validation is the Department dropdown on B2:B387 referencing Config!A2:A814; column E is free text. Re-verify those facts quickly with openpyxl and record them as an addendum in outputs/analysis/00_data_profile.md.

Create docs/taxonomy.md with the 12 departments exactly as in Config (Engineering, Facilities, G&A, Legal, M&A, Marketing, SaaS, Product, Professional Services, Sales, Support, Finance) and these assignment rules:
- Function-specific software goes to the function that uses it: Salesforce and its partners and integrations to Sales; HubSpot, Uberflip, Semrush to Marketing; Aha!, Figma to Product; Sage, Planful to Finance; Peakon, Performancepro to G&A as HR software; Kimble to Professional Services. SaaS holds cross-functional subscriptions with no single owning function: Google Workspace and its reseller, Microsoft 365, Slack, GoTo, Trello, Atlassian, Smartsheet, Zapier, Workato, DocuSign, LastPass, Formswift, Adobe.
- Professional Services means the company's own services-delivery department, not external advisers: PSA software, customer training and certification delivery, subcontractors on customer projects. External advisers go to Finance, Legal, M&A or G&A by what they do.
- Finance: audit, tax, accounting, R&D tax credit advisers, finance systems, payment processing, bank fees, share registry and depository services.
- M&A: deal advisers, data rooms, sponsor and transaction fees.
- Legal: law firms, notaries, IP, immigration services, data-protection registration, corporate secretarial and registered-agent services.
- G&A: HR (recruiting agencies, LinkedIn, job boards, payroll and employer-of-record providers, HR software), insurance and benefits (insurers, brokers, meal cards, gym, cycle-to-work, novated leasing, wellness, occupational health), travel and entertainment (Navan, airlines, hotels, restaurants, team events, gifts), training, employee IT equipment, couriers and postage, government and statutory payments, individual and unidentified payees, consumer retail purchases.
- Facilities: leases and coworking, property services, utilities, telecom and internet lines, parking, security, cleaning, waste, storage, movers, office supplies, furniture, office groceries and catering.
- Engineering: cloud hosting and domains, developer tools, monitoring, outsourced development and IT services, software escrow, Croatian sole-trader or d.o.o. contractors whose names suggest technical work, student labour contracts.
- Sales also holds customer-mandated procurement platform fees (Telefónica Global Services, Telefónica Compras Electrónicas, SAP Ariba).
- Marketing holds agencies, media, PR, events, sponsorships, industry memberships (TM Forum), swag and print, stock assets.
- Support holds support tooling and telephony for support lines.

Create docs/recommendation_rules.md:
- Consolidate: two or more vendors serve the same function (insurers across countries, auditors and accountants across countries, law firms, coworking providers, cloud accounts under two entities, two productivity suites, several work-management or integration tools, several contact-data tools, HubSpot alongside Salesforce marketing, HR and finance systems the parent already runs), or the same vendor is paid through more than one entity. Name the retained vendor in the rationale.
- Terminate: redundant after acquisition by a remote-first parent with its own talent, finance and legal functions: recruiting agencies, employer-of-record and payroll outsourcing where the parent's payroll covers the country, deal and transaction advisers (non-recurring), perks, events, gifts and memberships without a commercial justification, consumer retail purchases through AP, unidentified payees until identified.
- Optimize: essential sole vendors where the lever is price, volume or policy: Salesforce licences (audit and right-size at renewal), AWS (savings plans, one organisation), Navan (travel policy, one entity), insurance broker (re-broke under the group programme), LinkedIn (seat review). Also statutory payees and customer-mandated fees, with the rationale "non-discretionary, excluded from the savings base".
- Vendors under $1,000 are still classified; Terminate if non-essential, otherwise Optimize with the note "fold into tail-spend policy".

Create docs/vendor_hints.md with this analyst knowledge, to be used alongside your own and overridden only with a stated reason:
Cloudcrossing BVBA: Belgian Salesforce consulting partner. Kimble Applications: PSA software on the Salesforce platform (now Kantata). Mason Frank: Salesforce-specialist recruitment agency. Yoxel: Salesforce email and calendar sync. Navan (both entities): corporate travel and expense platform. TOG UK Properties: The Office Group, London flexible offices. Zagrebtower: Zagreb office lease. Innovent Spaces: Chennai coworking. GPT Space & Co: Australian flexible workspace. Work Easy Space Solutions: Indian coworking. Common Desk: US coworking. BDO LLP, Grant Thornton, PwC, Crowe Horwath Revizija, Collards, McBurneys, N S Shastri, Pinnacle Partnership, Taxstudio, Porezno Savjetništvo Tuk, Eurofast: audit, tax and accounting across the UK, Croatia, India, Greece. Granttree: UK R&D tax credit claims consultancy paid as a share of the claim. 4i Advisory Services and 4i Management Consulting: Indian management and finance consulting, confirm scope. RSM UK Corporate Finance, Houlihan Lokey: M&A advisers. SS&C Intralinks: virtual data room. Vector Capital Management: private equity sponsor fees, non-recurring after the sale. Westbrook Advisers: advisory, scope unknown. Jensten Insurance Brokers: UK commercial insurance broker. Aetna, Agram Life, Care Health, Bupa (two entities), Cigna SG, ICICI Lombard, ICICI Prudential: employee health and life insurance by country. Allianz Australia Workers' Compensation and icare NSW: statutory workers' compensation. Mercer: benefits consulting. Harmonic Group, Cedar Recruitment: finance recruitment agencies. Technet IT Recruitment: IT recruitment. Accutrainee: legal trainee placement. Info Edge: Naukri job board. LinkedIn Ireland: recruiter licences, ads or Sales Navigator; default G&A recruiting, confidence medium. HR Solution International GmbH and AG: HR outsourcing or employer of record in DACH. Australian Payroll Professionals: payroll outsourcing. Radius Group: likely global payroll and expansion services, confidence low. Peakon: employee engagement surveys. Performancepro: performance management software. Emerge Development Consultancy: leadership training. Epignosis: TalentLMS. Kryterion: certification exam delivery, likely for customer or partner certification. Pluxee and Sodexo India: meal benefits and office catering. Benefit Systems d.o.o.: MultiSport employee sports card. Green Commute Initiative: UK cycle-to-work scheme. Inside Edge Novated Leasing: Australian salary-packaged car leasing. Visalogic: UK immigration services. Intertrust Singapore, Acclime (two entities), Capitol Services: corporate secretarial and registered agent. Computershare-Caboodle, Bigshare, NSDL: share plan administration and depository. Raiffeisenbank Austria d.d.: Croatian bank fees. FastSpring: merchant-of-record payment processing. Ariba: SAP Ariba supplier network fees, customer-mandated. Telefónica Global Services GmbH and Telefónica Compras Electrónicas: payments to a customer's procurement or partner platform, confidence low, flag as a commercial dependency, do not terminate. TM Forum (two spellings): telecom industry association membership and events. Terrapinn: conference organiser. Big Frontier (Cult of Monday): Australian marketing agency. MightyHive: programmatic media agency. Plus Your Business: LinkedIn marketing training. Uberflip: content experience platform. Cognism, Lusha, 6sense: B2B contact and intent data. Outreach: sales engagement. Carrington Communications, Cision PR Newswire: PR. Smashing Media: UX publication and conferences. Pixsy: image copyright monitoring. Cloud Technology Solutions: UK Google Cloud and Workspace reseller. New Star Networks: UK telecom and IT managed services. Infosys, Shree Info System Solutions, Crayond Digital, Orionw, Trending Technology Services: outsourced IT and development, confirm whether customer-project subcontracting. Magazin Računalni Sistemi, E-Disti, Sniper Systems: IT hardware resellers. NCC Services: software escrow. Bureau Veritas Croatia: ISO certification audits. Centar za Sigurnost: occupational safety and fire protection services. Nastavni Zavod za Javno Zdravstvo, Specijalistička ordinacija medicine rada (three), Ustanova za zdravstvenu skrb: statutory occupational health examinations. Grad Zagreb, Grad Split: municipal fees. Zagrebački Holding: Zagreb city utilities. HEP Elektra: electricity. Hrvatski Telekom, Telemach, T-Mobile, Vodafone Australia, Starhub, BT, Inet Telecoms, Zettanet: telecom and internet. Avoxi: cloud telephony numbers. Click Send: SMS API. Studentski Centar (Zagreb, Split, Karlovac): Croatian student-service work contracts, contingent labour, not a vendor service. Hrvatski Nezavisni Izvoznici Softvera, Split Tech City: industry and community memberships. Entrio: event ticketing. Lajnap, Escape Art, Maniax, Sportkart, Paint & Fun, Paint&Wine, DJs For U, Blitz Cinestar, Good Game Global, Chamiers and P S Recreation Clubs, Sportska Udruga Split, Friends Sports Club: team events and recreation. Konzum, Spar, Müller, Pepco, Ikea Hrvatska, Officeworks, Platinum Office, Roto Dinamic, Fero-Term, Brodomerkur: office groceries, supplies and furniture. Weking d.o.o., Veniture d.o.o., Nefron obrt, Bijeli Pijesak obrt, Smart Group Services, TP Prime, Pingo, Ramiro, Omonia, Mosaic Concept, Limes Plus, Orcola, Akton: Croatian companies or sole traders of unknown function, most likely contractors; department by best inference, confidence low, description ends with "confirm with Finance". Stipe Piric, John Smith, Fabiola Thistlewhaite, George Anchor, Susan Lee, Ansar Madovic: individual payees, likely contractors or reimbursements, G&A, confidence low. (Blank): unnamed payee, G&A, Terminate, control gap.

Create docs/clusters.md: every vendor also gets exactly one cost_cluster from this fixed list, used for savings roll-ups: Salesforce platform; Office footprint; Office running costs; Travel and entertainment; Team events, perks and wellness; Audit, tax, accounting and corporate services; M&A and transaction costs; Legal; Insurance and benefits; Recruiting and HR outsourcing; Cloud, telecom and IT; Outsourced engineering and contractors; Software subscriptions (non-Salesforce); Marketing agencies, media and memberships; Customer-mandated platform fees; Statutory and government; Student labour; Unidentified and individual payees.

Then run the cleaning you proposed: stable vendor ids, the mojibake repair table, acronym casing (AWS, BDO, DHL, HP, SS&C, TOG, GPT, JLL, CBRE, NCC, HEP, PwC), legal-form stripping for matching only, and the entity merge map in qa/vendor_groups.csv. Keep original names in one column and cleaned names in another. Never touch the raw file. Commit as "Step 2: taxonomy, rules, hints, clusters and cleaning".
```

## Prompt 7 (2026-11-10)

```text
Decisions:

1. Proposed rules approved, with one principle made explicit in docs/taxonomy.md and docs/clusters.md: department answers "whose budget is this", cost_cluster answers "which lever captures the saving". They can differ. Mason Frank is G&A (recruiting) by department and Salesforce platform by cluster, so its saving rolls into the Salesforce opportunity. Slack is SaaS by department and Salesforce platform by cluster, with the rationale that it is Salesforce-owned and goes into the same renewal.

2. Merge only when it is the same vendor relationship under a changed or variant name (Navan rename, spelling variants, the same contract moved between entities). Where two entities share a parent but supply different products or contracts, record a link, not a merge. So: Sodexo India and Pluxee India become a link (same lineage, but on-site catering and meal cards are different services and contracts); Allianz WA and Allianz Australia Workers' Compensation become a link; the two 4i firms stay a proposed merge to be confirmed or reversed by the web verification in the next step. Update qa/vendor_groups.csv and the cleaning report accordingly.

3. Yes, the memo must also be a Google Doc. outputs/memo.md stays the source of truth; I will create the Doc from it and paste the link and the text into the CEOCFO Recommendations tab.

Two rule changes before classification: student labour is addressable (is_addressable TRUE, cluster Student labour) but carries a 0 percent savings assumption with the rationale "workforce cost, set by the hiring plan, not a vendor action". And treat the Telefónica payments as a question for Finance: fees, rebates or connectivity; classify Sales, Optimize, non-addressable, and say in the rationale that if they are rebates they belong against revenue rather than in vendor spend.

Commit as "Step 2b: rule decisions".
```

## Prompt 8 (2026-11-10)

```text
Approved on all three: links for the eight groups, AWS stays merged, student labour is Optimize. On Sodexo and Pluxee, let the web verification decide: if the Sodexo SVC India invoices are meal cards under the former name, it is a rename and becomes a merge; if they are catering, the link stands. One requirement to make explicit in docs/decisions.md: the sheet deliverable is per row, so all 386 original rows get their own department, description and recommendation, and merges and links exist only for ranking and savings roll-ups. Rows in a merge or link group carry the same recommendation and a rationale that names the group. Commit as "Step 2c: decisions confirmed".
```

## Prompt 9 (2026-11-10)

```text
Exception approved and the rule restated: one recommendation per merge group (same vendor relationship), and per same-brand link group where the products are the same kind of service (Salesforce and Slack, Atlassian and Trello, SolarWinds and Papertrail, the two ICICI insurers). Shared-parent links with different services (Amazon marketplaces and AWS; Microsoft 365, LinkedIn and npm; Sodexo and Pluxee if the link stands) take their own recommendation per row, with the rationale still naming the group. So AWS is Optimize, the two Amazon marketplace rows are Terminate as consumer retail through AP, Microsoft 365 is Consolidate, LinkedIn is Optimize, npm follows the developer-tool rule. Update docs/decisions.md and the QA check accordingly. Commit as "Step 2d: group recommendation rule".
```

## Prompt 10 (2026-11-10)

```text
Approved on all three. Align the QA's expected columns with the classification spec so nothing fails on naming: vendor_id, vendor_name_original, vendor_name_clean, spend_12m (use this name rather than cost_usd), department, sub_function, description, recommendation, rationale, risk_note, cost_cluster, is_addressable, is_recurring, confidence, verified, source_url. Add two checks: risk_note is non-empty for every Terminate and Consolidate row, and verified is TRUE for every row with any exception listed by name in the report. Re-run the self-test. Commit as "Step 2d-fix: QA columns".
```

## Prompt 11 (2026-11-10)

```text
C17 is inverted. The rule is: every row must have verified TRUE; any row with verified FALSE must appear by vendor_id, with a one-line reason, under a heading "Verification exceptions" in qa/validation_report.md, and nothing else counts. A FALSE row not listed there fails; a listed ID that is not FALSE in the file also fails. Point C17 only at that file and heading. Yes, add the one-line check that vendor_name_original and vendor_name_clean match outputs/vendors_clean.csv row for row. Re-run the self-test with planted errors for both. Commit as "Step 2d-fix2: verification exceptions".
```

## Prompt 12 (2026-11-10)

```text
Change C18 to match by vendor_id rather than by position. Separately, require that outputs/vendors_classified.csv is written in the original sheet row order (vendor_id ascending), because its Department, Description and Suggestions columns will be pasted straight into the Google Sheet and must line up row for row with the source. merge_validate.py sorts to that order before writing, whatever order the batches came in, and C18 then also confirms the order. Add a planted-error case for a shuffled file. Commit as "Step 2d-fix3: id matching and sheet order".
```
