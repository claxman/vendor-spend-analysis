# Cost clusters

Every vendor also gets exactly one `cost_cluster` from the fixed list below (prompt 6 in `prompts/log.md`), used for savings roll-ups. A cluster answers one question: which lever captures the saving? A department (`docs/taxonomy.md`) answers another: whose budget is this? The two can differ (decision of 2026-11-10, `docs/decisions.md`). Kimble is Professional Services by department and Salesforce platform by cluster. Mason Frank is G&A by department and Salesforce platform by cluster, so its saving rolls into the Salesforce opportunity. Slack is SaaS by department and Salesforce platform by cluster, because it is Salesforce-owned and goes into the same renewal. Rows merged into one vendor in `qa/vendor_groups.csv` share one cluster; linked vendors are clustered one by one. `scripts/02_clean.py` checks that the table below holds exactly these 18 names, in this order.

## Clusters

| # | cost_cluster | Holds |
|---|---|---|
| 1 | Salesforce platform | Salesforce itself; vendors that exist to implement, extend or integrate the Salesforce org: Salesforce consulting partners (Cloudcrossing) and Salesforce-native apps and integrations (Kimble, Yoxel); and spend whose saving the Salesforce lever captures: Salesforce-owned products renewed with it (Slack) and Salesforce-specialist services (Mason Frank). |
| 2 | Office footprint | The right to occupy space: leases, coworking and flexible-office memberships (TOG, Zagrebtower, Innovent Spaces, GPT Space & Co, Work Easy, Common Desk, WeWork), property agents and managers (JLL, CBRE). |
| 3 | Office running costs | Everything that keeps occupied space running: electricity and city utilities, cleaning, security and fire safety, waste, parking, storage, movers, office supplies, furniture, plants, office groceries and catering, couriers and postage. |
| 4 | Travel and entertainment | The travel platform (Navan), airlines, hotels and resorts, ground transport, travel agencies, restaurants and team meals. |
| 5 | Team events, perks and wellness | Activities and venues booked as team events, gifts, gyms and sports cards, recreation clubs, wellness programmes. |
| 6 | Audit, tax, accounting and corporate services | Auditors, accountants, tax and R&D tax credit advisers, corporate secretarial and registered agents, share registry and depository, bank fees, payment processing, certification audits. |
| 7 | M&A and transaction costs | Deal advisers, data rooms, sponsor and transaction fees. |
| 8 | Legal | Law firms, notaries, IP and copyright, immigration services. |
| 9 | Insurance and benefits | Insurers, insurance brokers, benefits consultants, statutory workers' compensation, occupational health examinations, meal cards, cycle-to-work, novated leasing, telehealth. |
| 10 | Recruiting and HR outsourcing | Recruitment agencies, job boards and LinkedIn recruiting, employer-of-record and payroll outsourcing, external training and coaching. Salesforce-specialist recruiting is in Salesforce platform. |
| 11 | Cloud, telecom and IT | Cloud hosting (AWS), domains and DNS, telecom and internet lines, telephony and messaging APIs, IT hardware and its resellers, managed IT services, software escrow. |
| 12 | Outsourced engineering and contractors | Outsourced development and IT service firms, and Croatian d.o.o. and obrt contractors, including the Croatian companies that `docs/vendor_hints.md` lists as most likely contractors. |
| 13 | Software subscriptions (non-Salesforce) | All other licensed or subscription software: productivity and collaboration (Google Workspace and its reseller, Microsoft 365, GoTo; Slack is in Salesforce platform), work management, integration, HR and finance systems, marketing and sales tools, contact and intent data, developer and monitoring tools, design and product tools, learning platforms. |
| 14 | Marketing agencies, media and memberships | Marketing, PR, media and event agencies, conferences and sponsorships, industry, community and professional memberships (TM Forum, Split Tech City, PMI), swag and print, stock assets, media subscriptions and advertising. |
| 15 | Customer-mandated platform fees | Fees a customer requires the company to pay to sell to it: Telefónica Global Services, Telefónica Compras Electrónicas, SAP Ariba. Not addressable. Whether the Telefónica payments are fees, rebates or connectivity is a question for Finance (`docs/decisions.md`). |
| 16 | Statutory and government | Taxes, government and municipal fees, regulators and statutory registrations (ICO). Not addressable. |
| 17 | Student labour | Croatian student-service work contracts invoiced by student centres (Zagreb, Split, Karlovac). Addressable (`is_addressable` TRUE) with a 0% savings assumption: workforce cost, set by the hiring plan, not a vendor action. |
| 18 | Unidentified and individual payees | Individuals, the unnamed payee (Blank), and payees whose function cannot be inferred and for which no hint points elsewhere. |

## Tie-breaks (approved 2026-11-10)

| # | Situation | Cluster |
|---|---|---|
| C1 | Salesforce-specialist services and Salesforce-owned products | Salesforce platform, because the Salesforce lever captures the saving: Mason Frank (G&A by department) rolls into the Salesforce opportunity; Slack (SaaS by department) is Salesforce-owned and goes into the same renewal, and is linked to Salesforce in `qa/vendor_groups.csv`. Decided 2026-11-10 |
| C2 | Telecom lines against electricity and city utilities | Telecom and internet in Cloud, telecom and IT, as IT negotiates them; electricity, water and waste in Office running costs, even when the supplier is publicly owned (HEP Elektra, Zagrebački Holding) |
| C3 | Hotels and resorts used for offsites | Travel and entertainment, unless the booking is plainly an event venue or activity, which goes to Team events, perks and wellness |
| C4 | Gyms and sports cards against tax-advantaged benefits | Gyms, sports cards (Benefit Systems MultiSport) and recreation clubs in Team events, perks and wellness; meal cards (Pluxee), cycle-to-work and novated leasing in Insurance and benefits |
| C5 | Statutory insurance and statutory medical examinations | Insurance and benefits (workers' compensation including icare NSW, occupational health clinics). Statutory and government holds payments that are a fee or tax rather than cover or a service. Being statutory, these stay not addressable whatever their cluster |
| C6 | Corporate secretarial and registered agents | Audit, tax, accounting and corporate services, although the department is Legal |
| C7 | Data-protection registration | Statutory and government (ICO), although the department is Legal |
| C8 | Share registry and depository | Audit, tax, accounting and corporate services (Computershare-Caboodle, Bigshare, NSDL), not Statutory and government |
| C9 | Google Workspace through a reseller | Software subscriptions (non-Salesforce) for both Google and Cloud Technology Solutions, so that the two productivity suites sit in one cluster |
| C10 | Developer and monitoring tools sold as software | Software subscriptions (non-Salesforce) (JetBrains, GitKraken, npm, AG Grid, Papertrail, SolarWinds, Uptime Robot); hosting, domains and DNS stay in Cloud, telecom and IT |
| C11 | Learning | Platforms and course subscriptions in Software subscriptions (non-Salesforce) (Pluralsight, TalentLMS); professional memberships in Marketing agencies, media and memberships (PMI, Interaction Design Foundation); trainers and coaches in Recruiting and HR outsourcing (Emerge, Plus Your Business) |
| C12 | Payees of unknown function | Outsourced engineering and contractors only where the analyst hints say most likely contractors; every other unknown goes to Unidentified and individual payees |
