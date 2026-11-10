# Department taxonomy

The only departments allowed are the 12 values in the workbook's `Config` sheet, spelled exactly as there and listed here in the same order. The workbook's Department column (B2:B387) is a dropdown validated against `Config!$A$2:$A814` with the error alert on, so any other spelling would be rejected in the workbook. `scripts/02_clean.py` checks that the table below and `Config` agree, character for character.

A department answers one question: whose budget is this? The cost cluster (`docs/clusters.md`) answers another: which lever captures the saving? The two can differ (decision of 2026-11-10, `docs/decisions.md`). Slack is SaaS by department and Salesforce platform by cluster, because it is Salesforce-owned and goes into the same renewal. Cloudcrossing's PDF Butler is Product by department, as a component embedded in or delivered with the product, and Salesforce platform by cluster (step 3b). Mason Frank is G&A by department, as a recruiting agency, and from step 3b Recruiting and HR outsourcing by cluster, because its lever is ending the agency, not the Salesforce contract.

Recommendations follow `docs/recommendation_rules.md`; analyst knowledge about specific vendors is in `docs/vendor_hints.md`.

## Departments

| # | Department | Holds |
|---|---|---|
| 1 | Engineering | Cloud hosting and domains, developer tools, monitoring, outsourced development and IT services, software escrow, Croatian sole-trader or d.o.o. contractors whose names suggest technical work, student labour contracts; the Salesforce platform and ISV licences of the company's Salesforce-native product, and Salesforce-ecosystem vendors that supply product engineering (step 3b). |
| 2 | Facilities | Leases and coworking, property services, utilities, telecom and internet lines, parking, security, cleaning, waste, storage, movers, office supplies, furniture, office groceries and catering. |
| 3 | G&A | HR (recruiting agencies, LinkedIn, job boards, payroll and employer-of-record providers, HR software); insurance and benefits (insurers, brokers, meal cards, gym, cycle-to-work, novated leasing, wellness, occupational health); travel and entertainment (Navan, airlines, hotels, restaurants, team events, gifts); training; employee IT equipment; couriers and postage; government and statutory payments; individual and unidentified payees; consumer retail purchases. |
| 4 | Legal | Law firms, notaries, IP, immigration services, data-protection registration, corporate secretarial and registered-agent services. |
| 5 | M&A | Deal advisers, data rooms, sponsor and transaction fees. |
| 6 | Marketing | Agencies, media, PR, events, sponsorships, industry memberships (TM Forum), swag and print, stock assets; marketing software (HubSpot, Uberflip, Semrush). |
| 7 | SaaS | Cross-functional subscriptions with no single owning function: Google Workspace and its reseller, Microsoft 365, Slack, GoTo, Trello, Atlassian, Smartsheet, Zapier, Workato, DocuSign, LastPass, Formswift, Adobe. |
| 8 | Product | Product management and design software (Aha!, Figma); components embedded in or delivered with the product, such as a Salesforce-native app (step 3b). |
| 9 | Professional Services | The company's own services-delivery department, not external advisers: PSA software (Kimble), customer training and certification delivery, subcontractors on customer projects. |
| 10 | Sales | Of the Salesforce ecosystem, only internal-CRM tooling, such as the add-ons and integrations the sales team uses (step 3b); customer-mandated procurement platform fees (Telefónica Global Services, Telefónica Compras Electrónicas, SAP Ariba). |
| 11 | Support | Support tooling and telephony for support lines. |
| 12 | Finance | Audit, tax, accounting, R&D tax credit advisers, finance systems (Sage, Planful), payment processing, bank fees, share registry and depository services. |

## Assignment rules

These are the rules as given (prompt 6 in `prompts/log.md`), with rule 1 amended in step 3b (prompt 16) and rules 9 and 10 following it.

1. Function-specific software goes to the function that uses it: HubSpot, Uberflip, Semrush to Marketing; Aha!, Figma to Product; Sage, Planful to Finance; Peakon, Performancepro to G&A as HR software; Kimble to Professional Services. Salesforce (amended in step 3b): the Salesforce platform licences, and Salesforce-ecosystem vendors that supply product engineering or embedded product components, go to Engineering, or to Product for an embedded component; only internal-CRM tooling goes to Sales.
2. SaaS holds cross-functional subscriptions with no single owning function: Google Workspace and its reseller, Microsoft 365, Slack, GoTo, Trello, Atlassian, Smartsheet, Zapier, Workato, DocuSign, LastPass, Formswift, Adobe.
3. Professional Services means the company's own services-delivery department, not external advisers: PSA software, customer training and certification delivery, subcontractors on customer projects. External advisers go to Finance, Legal, M&A or G&A by what they do.
4. Finance: audit, tax, accounting, R&D tax credit advisers, finance systems, payment processing, bank fees, share registry and depository services.
5. M&A: deal advisers, data rooms, sponsor and transaction fees.
6. Legal: law firms, notaries, IP, immigration services, data-protection registration, corporate secretarial and registered-agent services.
7. G&A: HR (recruiting agencies, LinkedIn, job boards, payroll and employer-of-record providers, HR software), insurance and benefits (insurers, brokers, meal cards, gym, cycle-to-work, novated leasing, wellness, occupational health), travel and entertainment (Navan, airlines, hotels, restaurants, team events, gifts), training, employee IT equipment, couriers and postage, government and statutory payments, individual and unidentified payees, consumer retail purchases.
8. Facilities: leases and coworking, property services, utilities, telecom and internet lines, parking, security, cleaning, waste, storage, movers, office supplies, furniture, office groceries and catering.
9. Engineering: cloud hosting and domains, developer tools, monitoring, outsourced development and IT services, software escrow, Croatian sole-trader or d.o.o. contractors whose names suggest technical work, student labour contracts; from step 3b also the Salesforce platform licences and the Salesforce-ecosystem vendors that supply product engineering (rule 1).
10. Sales also holds customer-mandated procurement platform fees (Telefónica Global Services, Telefónica Compras Electrónicas, SAP Ariba). Of the Salesforce ecosystem it holds only internal-CRM tooling (rule 1, step 3b).
11. Marketing holds agencies, media, PR, events, sponsorships, industry memberships (TM Forum), swag and print, stock assets.
12. Support holds support tooling and telephony for support lines.

## Tie-breaks (approved 2026-11-10)

These settle cases the rules above leave open, without overriding any of them. Each names the vendors it decides; the defaults change only with evidence, and the classification states which way it went.

| # | Situation | Proposed department | Vendors it decides |
|---|---|---|---|
| T1 | A vendor specialised in one ecosystem but doing a generic job | What the vendor does, not whose ecosystem it serves: a Salesforce-specialist recruiter is a recruiting agency (rule 7) | Mason Frank: G&A (its cost cluster is Recruiting and HR outsourcing from step 3b, `docs/clusters.md` C1) |
| T2 | A Salesforce-ecosystem vendor | By what it supplies (rule 1, amended in step 3b): product engineering to Engineering, a component embedded in or delivered with the product to Product, internal-CRM tooling to Sales; Professional Services only with evidence that its work is delivered to customers (rule 3) | Cloudcrossing (PDF Butler): Product; Weking: Engineering; Yoxel: Sales; Kimble stays in Professional Services as PSA software (rule 1) |
| T3 | Outsourced development that may be customer-project subcontracting | Engineering by default (rule 9); Professional Services with evidence (rule 3) | Infosys, Shree Info System Solutions, Crayond Digital, Orionw, Trending Technology Services |
| T4 | Food and drink | Groceries and catering for the office: Facilities (rule 8). Restaurants, team meals and food delivery: G&A, travel and entertainment (rule 7) | Konzum, Catering Muring, City Pantry: Facilities; Tattu, Gaucho, Uber Eats, Wolt: G&A |
| T5 | Telephony and messaging | Lines and mobile plans: Facilities (rule 8). Numbers used for support lines: Support (rule 12). Messaging APIs used by the product: Engineering | Avoxi: Support; Click Send: Engineering |
| T6 | Telecom sold together with managed IT | Facilities when the spend is lines and connectivity (rule 8); Engineering when it is managed IT services (rule 9). Default Facilities, as the analyst hint names telecom first | New Star Networks |
| T7 | Learning, publications and certification | Employee training, whatever the function: G&A (rule 7). Customer or partner training and certification delivery: Professional Services (rule 3) | Kryterion: Professional Services; Epignosis (TalentLMS), Pluralsight, PMI, Interaction Design Foundation, Smashing Media, Plus Your Business, Emerge: G&A unless shown to serve customers |
| T8 | IT hardware | Laptops, phones and accessories: G&A, employee IT equipment (rule 7). Servers and network equipment: Engineering | Apple, HP, Currys, Magazin Računalni Sistemi, E-Disti, Sniper Systems: G&A by default |
| T9 | Statutory and publicly owned payees | G&A (rule 7), except data-protection registration (Legal, rule 6) and utilities, even when publicly owned (Facilities, rule 8). Student work contracts stay in Engineering (rule 9) | ICO: Legal; HEP Elektra, Zagrebački Holding: Facilities; student centres: Engineering |
| T10 | Safety, certification and compliance services | Fire protection and building safety: Facilities, as security (rule 8). ISO certification audits: G&A | Centar za Sigurnost: Facilities; Bureau Veritas Croatia: G&A |
| T11 | Images and copyright | Stock assets: Marketing (rule 11). Copyright monitoring and enforcement: Legal, as IP (rule 6) | Freepik: Marketing; Pixsy: Legal |
| T12 | Function not evident from the name | Best inference, confidence low, and a description that says the function cannot be inferred from the name (CLAUDE.md). Individuals and unidentified payees: G&A (rule 7) | The Croatian companies listed as unknown in `docs/vendor_hints.md`, the six individuals, (Blank), and the payees in section 7.10 of `outputs/analysis/01_forensics.md` |
