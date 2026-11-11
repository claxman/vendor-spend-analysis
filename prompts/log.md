# Prompt log

Every prompt that directed the analysis, verbatim and in the order received. Requests for a status summary and file housekeeping are not analysis prompts and are not logged. Where a logged prompt also carried a housekeeping instruction, the omission is marked in place.

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

## Prompt 13 (2026-11-10)

```text
Add to docs/decisions.md and the rules: (1) every savings assumption that depends on a choice by the acquirer (remote operating model, group talent function, group insurance programme, group auditor, parent CRM instance) is tagged with a depends_on decision name in docs/savings_assumptions.md and savings.md, and the memo presents the Top 3 as decisions with their value, not as facts about the parent. (2) Employee hardware (Apple entities, HP, Currys, Magazin Računalni Sistemi, Sniper Systems, E-Disti) is Consolidate into group IT procurement, not Terminate; Terminate remains for food, groceries, gifts and marketplace purchases through AP. (3) Where an adviser's spend plausibly includes sale-related work (BDO, Bisley Law, Grant Thornton), keep it in the recurring base and note in insights.md later that the recurring figure is likely lower.

Batch format for classification: one CSV per batch of 40 vendors in outputs/batches/batch_NN.csv, with exactly these 16 columns: vendor_id, vendor_name_original, vendor_name_clean, spend_12m, department, sub_function, description, recommendation, rationale, risk_note, cost_cluster, is_addressable, is_recurring, confidence, verified, source_url. Write scripts/merge_validate.py now: it merges the batches, sorts by vendor_id, writes outputs/vendors_classified.csv, runs qa/check_outputs.py, and writes qa/validation_report.md with counts, distributions by department, recommendation, cluster and confidence, the low-confidence list sorted by spend, a "Verification exceptions" section, and every failure. Commit as "Step 2e: decision tags, hardware rule, merge script".
```

## Prompt 14 (2026-11-10)

```text
Approved on all four. Add depends_on names for the other three: group_payroll (employer-of-record and payroll outsourcing), group_systems (HR and finance systems migrating to the parent's HRIS and ERP), group_legal (law firm panel consolidation). Every assumption in docs/savings_assumptions.md that is not purely a vendor action now carries a tag; the ones that are purely vendor actions (Salesforce licence audit, AWS savings plans, Navan policy, insurance re-broke) carry none. Commit as "Step 2f: remaining decision tags". Then stop; the next prompt starts classification.
```

## Prompt 15 (2026-11-10)

```text
Read CLAUDE.md, every file in docs/ and outputs/vendors_clean.csv before classifying.

Classify every vendor in batches of 40 in original sheet order (vendor_id ascending), using docs/taxonomy.md, docs/recommendation_rules.md, docs/vendor_hints.md, docs/clusters.md and docs/decisions.md. For every vendor, run a web search on the cleaned vendor name (add the country from the legal form or address where useful) and base the description and department on what the vendor's own site or a reliable directory says; record the URL in source_url and set verified TRUE. Only if repeated searches find nothing usable, set verified FALSE, use the "confirm with Finance" form from the hints, and add the vendor_id with a one-line reason to qa/verification_exceptions.csv. Log every lookup, including failed ones, to qa/verification_log.csv with vendor_id, query used, URL found, and what it established. If a search contradicts a hint, follow the search and note it in the rationale. Resolve the two pending verifications: the 4i merge, and Sodexo versus Pluxee.

Each batch is outputs/batches/batch_NN.csv with exactly the 16 columns in order: vendor_id, vendor_name_original, vendor_name_clean, spend_12m, department (Config values only), sub_function, description (one line, 5 to 25 words, specific, what the vendor does and for which team, no banned phrases), recommendation (Terminate, Consolidate or Optimize exactly, following the group rules in decisions.md), rationale (one sentence; for Consolidate name the retained vendor or group function; for grouped rows name the group), risk_note (required for every Terminate and Consolidate: one clause naming the main risk of acting; empty for Optimize), cost_cluster, is_addressable, is_recurring, confidence (high, medium, low), verified, source_url.

Print a three-line summary per batch, commit after every two batches so nothing is lost, and work through all ten batches without stopping. Commit the last as "Step 3: classification with web verification".
```

## Message during prompt 15 (2026-11-10)

Note: a nudge sent while step 3 was running, not an instruction.

```text
why can't you do it now?
```

## Prompt 16 (2026-11-10)

Note: housekeeping instruction omitted: moving a local status file out of the repository folder.

```text
Append this prompt to prompts/log.md as prompt 16, and log the unlogged message "why can't you do it now?" (sent during step 3) in its place in the sequence with a one-line note that it was a nudge, not an instruction. [two sentences omitted]

Then make these changes and record each one in docs/decisions.md under a new heading "2026-11-10: platform reclassification (prompt 16, step 3b)":

1. Salesforce is the product platform, not the sales team's CRM. Evidence from the ledger: one vendor is 39.5% of all third-party spend, which no company pays for sales seats; around it sit Salesforce-native vendors (a document-generation app at $209K, a PSA on the Salesforce platform, a Salesforce consultancy supplying developers, a Salesforce-specialist recruiter, a Salesforce email-sync tool); and the company sells to telecoms, where Salesforce-native products are common. Treat the Salesforce spend as platform and ISV licence cost for a product built on Salesforce, with a smaller internal CRM component. Update docs/taxonomy.md: Salesforce platform licences and Salesforce-ecosystem vendors that supply product engineering or embedded product components go to Engineering (or Product for an embedded component); only internal-CRM tooling goes to Sales.

2. Reclassify, keeping every other column rule:
   - V0002 Salesforce UK Ltd: department Engineering. Description: Salesforce platform and ISV licences for the company's Salesforce-native product, plus internal CRM seats; the largest single cost. Recommendation Optimize. Rationale: renegotiate the platform agreement at change of control (co-term with the parent's Salesforce relationship, multi-year commitment, true-down of internal seats audited separately from platform licences). Risk note is allowed on Optimize here as an exception recorded in decisions.md: the product depends on this platform, so the lever is commercial terms, never exit.
   - V0009 Weking d.o.o.: department Engineering, cost_cluster "Outsourced engineering and contractors", recommendation Consolidate into the group's engineering sourcing model, risk note: product knowledge held by the consultancy's developers must be transferred first. Keep confidence low and "confirm with Finance".
   - V0006 Cloudcrossing BVBA (PDF Butler): department Product, description stating it is a Salesforce-native document generation app and that at this spend it is most likely embedded in or delivered with the product rather than used by internal sales; confirm OEM terms with Finance. Recommendation Optimize: renegotiate OEM or volume pricing within the platform review. Cluster stays Salesforce platform.
   - Mason Frank: cost_cluster "Recruiting and HR outsourcing" (its lever is agency termination, not the Salesforce contract). Recommendation stays.
   - NSDL (V0284): is_addressable FALSE, cost_cluster "Statutory and government", rationale "non-discretionary, excluded from the savings base", so the classification matches the forensic exclusion.

3. Bisley Law (V0018, $67,414): add to the Finance questions in docs/decisions.md as a control finding: Companies House lists the entity as non-trading and no website or SRA record describes its services; Finance must confirm which entity invoiced and for what before any payment continues. Keep the row Consolidate; add that finding to its risk note.

4. Privacy: in outputs/vendors_classified.csv, the batch CSVs and qa/verification_log.csv, replace every URL that contains a private individual's name (sole-trader register pages and similar) with the directory's root domain and the note "URL withheld: names the owner", and list the affected vendor_ids in docs/decisions.md. Replace the V0024 source_url with the Navan rebrand press release already used for V0003.

5. Fix the repeated heading at docs/decisions.md lines 39 and 41. Re-run scripts/00_data_profile.py so the committed profile matches its script, and check the diff is only the taxonomy line.

Re-run scripts/merge_validate.py and both self-tests; everything must pass. Print the new department distribution by spend. Commit as "Step 3b: platform reclassification and housekeeping" and push.
```

## Prompt 17 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 17. It has two parts, one commit each.

PART A: department reading for "SaaS" (step 3c)

The Config list names the functions of a software company: Engineering, Product, Support, Professional Services, SaaS, Sales, Marketing, G&A, Finance, Legal, Facilities, M&A. Read that way, "SaaS" is the function that runs the hosted product, not a label for any software subscription. Rewrite the rule in docs/taxonomy.md:
- SaaS holds the platform and hosting the product runs on and the tools that keep it running: platform and ISV licences, cloud hosting, monitoring and logging, DNS and domains, and third-party components delivered with the product.
- Company-wide software with no single owning function (productivity suites, messaging, meetings, e-signature, password management, automation and work-management tools) goes to G&A, with a sub_function that starts "Corporate IT".
- Software used by one function stays with that function. Developer tools stay in Engineering.

Reclassify by that rule and list every row you move:
- V0002 Salesforce UK and V0006 PDF Butler to SaaS.
- AWS (V0014, V0103) and the hosting, monitoring, logging, DNS and domain rows now in Engineering to SaaS.
- The rows now in SaaS to G&A or to the function that uses them. The Google reseller moves to SaaS only if its verified description shows cloud hosting rather than Workspace licences.
Change a description only where it names the owning team. Record the decision in docs/decisions.md as "SaaS department reading (prompt 17, step 3c)" with this reasoning, the alternative reading (SaaS as a bucket for subscriptions), and the point that platform and hosting rows fit SaaS under either reading. Update the fixed-outcome checks, re-run scripts/merge_validate.py and both self-tests, print the department distribution by spend, and commit as "Step 3c: SaaS department reading".

PART B: savings model and insights (step 4)

Read docs/savings_assumptions.md and the two open points in the step 3b decisions entry first.

1. Register
- Add a tenth acquirer decision, group_engineering_sourcing: contractor consultancies are replaced by the group's own engineering sourcing.
- Restate the Salesforce levers for the platform reading: the lever on V0002 is the platform agreement renegotiated at change of control, with internal seats trued down separately. It is a vendor action and carries no tag.
- Every lever carries pct_low, pct_base and pct_high (run-rate saving as a share of 12-month spend), pct_without_decision (what vendor action alone achieves if the tagged acquirer decision is not taken; equal to pct_base for untagged levers), year1_factor (the share of the first 12 months in which the saving is live), depends_on, and one sentence of reasoning. Convention for year1_factor: 0.5 where the renewal or notice date is unknown, higher for policy changes that start within 90 days, lower where the change waits for a year-end or a migration.

2. Assumptions, written as low / base / high; without decision; year-1 factor; tag. Map them onto the registered levers by each row's cluster and sub_function, splitting or adding levers where needed. Every row ends with exactly one lever. If the data contradicts an assumption, keep the assumption, and say so with your proposed change in the final summary.

Salesforce platform
- Salesforce UK (V0002): 10 / 15 / 25; 0.5; no tag. The base sits below the usual licence-audit range because part of this spend is platform and ISV fees that do not shrink with a seat count, and the contract is not visible.
- PDF Butler (V0006): 10 / 20 / 30; 0.5; no tag.
- Kimble: 5 / 10 / 15; 0.5; no tag.
- Slack and Yoxel: 0, negotiated inside the Salesforce renewal.

Office
- Office footprint: 60 / 75 / 90; without decision 25 (right-size onto one flexible provider); 0.5; remote_operating_model. The base keeps a quarter of the spend for a touchdown space at the engineering hub and registered addresses.
- Office running costs: 50 / 70 / 80; without decision 20; 0.5; remote_operating_model.

Back office
- Audit, tax and accounting firms: 25 / 35 / 45; without decision 10 (tender); 0.4 because an auditor changes at the financial year-end; group_auditor.
- Corporate secretarial, registered agent and share registry: 10 / 20 / 30; 0.5; no tag.
- R&D tax credit adviser paid as a share of the claim: 0. The fee is contingent on cash recovered, so cutting it reduces cash.
- Law firms and legal resourcing: 20 / 30 / 40; without decision 10; 0.6; group_legal.
- Employment-law firms paid small one-off sums that fit settlement-agreement advice for departing employees (V0230, V0231, V0241 and any other row the same test fits): 0. These are one payment per leaver, not a vendor relationship.
- Recruitment agencies and job boards: 80 / 100 / 100; without decision 30 (preferred suppliers and a fee cap); 0.9; group_talent_function. Say in the reasoning that this spend follows hiring volume.
- LinkedIn: 20 / 30 / 50; without decision 20; 0.6; group_talent_function.
- Employer-of-record providers: 10 / 15 / 25; without decision 0; 0.5; group_payroll. These invoices usually carry the employees' pay as a pass-through, so only the service fee is addressable.
- Payroll processing providers: 25 / 40 / 60; without decision 10; 0.5; group_payroll.
- Commercial insurance placed through brokers: 15 / 25 / 35; without decision 10 (re-broke); 0.5; group_insurance_programme.
- Employee health and life insurance: 5 / 10 / 15; without decision 5; 0.5; group_insurance_programme. Benefits are part of pay, so the lever is broking and scheme terms, not cover.
- Statutory workers' compensation, salary-sacrifice schemes, meal cards and gym schemes: 0. Pay and statutory cover are people decisions outside a vendor model.
- Finance and HR systems the group would replace (accounting, planning, engagement, performance) and HubSpot: 60 / 80 / 100; without decision 10; 0.25 because the saving starts after migration; group_systems, and parent_crm_instance for HubSpot. The base nets off extra seats on the group's systems.

Second wave
- Navan: 15 / 25 / 35; 0.75; no tag.
- Other travel, hotels, restaurants and food through AP: 30 / 50 / 70; 0.75; no tag. Part of this spend returns through expenses.
- Team events, perks and wellness: 40 / 60 / 75; 0.75; no tag. The rest stays as a per-head culture budget.
- Other software subscriptions: 15 / 25 / 35; 0.6; no tag.
- AWS: 10 / 20 / 30; 0.6; no tag.
- Telecom and internet providers: 25 / 40 / 60; without decision 15; 0.5; remote_operating_model.
- Other cloud and IT, including employee hardware: 5 / 10 / 20; 0.6; no tag.
- Marketing agencies: 30 / 50 / 70; 0.75; no tag.
- TM Forum: 0 / 0 / 100; no tag. It is a go-to-market credential; the high case applies only if the parent holds a membership that covers subsidiaries.
- Other marketing, media and events: 20 / 30 / 50; 0.75; no tag.
- Outsourced engineering and contractors: 20 / 30 / 40; without decision 10; 0.5; group_engineering_sourcing. The work continues, so the saving is the rate difference.
- Unidentified and individual payees: 30 / 50 / 70; 0.75; no tag.

Excluded, each on its own line in the report
- M&A and transaction costs: 0, non-recurring, falls away without action.
- Customer-mandated platform fees, Statutory and government, Student labour: 0.
- Any other row with is_recurring FALSE gets 0 and is reported as one-off spend that falls away, except in "Travel and entertainment" and "Team events, perks and wellness", where the category recurs even when the payee does not.

3. Opportunities. Each lever belongs to one: "Salesforce platform agreement" (the Salesforce platform levers), "Office exit" (the two office levers), "Back office into group shared services" (the levers under Back office), "Second wave", or "Excluded".

4. scripts/03_savings.py reads outputs/vendors_classified.csv and the register, hard-codes no spend figure, and writes:
- outputs/analysis/savings.csv, one row per vendor: vendor_id, name, spend, cluster, lever, opportunity, the four percentages, year1_factor, depends_on, run-rate saving low, base and high, saving without the decision, year-1 saving.
- outputs/analysis/savings.md: total spend; recurring base; excluded spend by reason; savings by opportunity and by cluster (run-rate low, base and high, without decision, year 1, share of spend); one table of acquirer decisions with the saving with each, without it, and the difference as the value of that decision; the 15 largest vendor savings; the savings that sit on non-recurring rows; and a reconciliation showing vendor rows sum to levers, clusters and opportunities to the cent. Whole dollars in the markdown, full precision in the CSV.

5. QA. Add checks to qa/check_outputs.py, each with a planted error: low <= base <= high; without decision <= base; year 1 <= base; no saving on a non-addressable or M&A row; no saving above spend; every row has one registered lever and every lever is used; every tag is a registered decision; the roll-ups reconcile. Re-run both self-tests.

6. outputs/analysis/insights.md, built only from files in the repository, one short section each with figures and vendor_ids:
- platform dependency and concentration (top 1, 10 and 50; the Salesforce platform share);
- what falls away without action, the recurring base, and the sale-related share that may sit inside BDO, Bisley Law and Grant Thornton;
- vendors that must not be cut: customer-mandated fees, escrow, certification, statutory payees, salary-sacrifice schemes, the contingent-fee tax adviser;
- control findings: duplicate vendor records and the duplicate-payment review they call for; individual and unnamed payees; the law firm filed as non-trading (V0018); sole traders paid at contractor scale; retail merchants in the vendor master and the vendor count once a card policy removes them;
- the country and legal-entity footprint shown by statutory, payroll, secretarial and insurance vendors, and the audit, payroll and secretarial cost that follows it;
- software overlap, as a count of tools per function;
- signs of leavers in the last 12 months and what they imply for seat and space counts;
- retention risk at the engineering hub (perks, contractors and student labour in Croatia);
- timing constraints: insurance renewals, audit year-end, lease notice, system migration;
- data limits and the requests that follow: monthly AP ledger, contract register with renewal and notice dates, the Salesforce contract and usage, headcount by site and entity.

Do not write the Top 3, methodology, memo or README yet. Commit as "Step 4: savings model and insights" and push. Then print savings.md in full, the lever table, every row where you chose the lever yourself, and every assumption you would change.
```

## Prompt 18 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 18. Three parts.

PART A: assumption decisions (step 4b)

Your seven points, decided:
1. Add a lever "Employee hardware" for the nine hardware rows and Shree Info System: 5 / 10 / 20; without decision 5; 0.6; group_it_procurement.
2. V0057 MultiSport is an employee benefit at the engineering hub and stays: recommendation Optimize, rationale to keep it and review take-up and the employee co-payment, lever unchanged at 0. V0121 Gym4You becomes Consolidate into the MultiSport card, on the Team events, perks and wellness lever, with the risk note that the gyms staff use must be in the MultiSport network first.
3. Bisley Law stays on the law-firms lever: whoever the payee proves to be, the spend is legal work that follows that lever, and the payee check is a control action, not a savings assumption. Reword the finding wherever it appears. The provider of this data modified vendor names, so a name that matches no trading firm is a question for Finance, not evidence of a problem. Apply the same caution to every statement about unmatched or unverified names in insights.md and decisions.md.
4. Salesforce: no change to the model. The documents will present the figure as the value of a negotiation that starts when the contract and usage data arrive.
5. Unidentified and individual payees: no change. One-off payments to individuals are a control finding and carry no saving.
6. Add a lever "Couriers and postage": 5 / 10 / 20; 0.6; no tag. The two Amazon marketplace rows stay where they are.
7. Weking: no change to the model; mark its share as provisional in the register and in insights.md.
The External training and coaching lever is confirmed as you set it.

Re-run scripts/03_savings.py, scripts/04_insights.py and the QA. Commit as "Step 4b: assumption decisions".

PART B: second-pass review (step 5)

1. Keep the working files. Copy from the session scratchpad into the repository everything that produced the classification: the research brief, the research findings and lookup logs, the batch builder and the per-batch classification lines. Put them where a reader would look (the brief under prompts/, the builder under scripts/, findings and batch lines under qa/), apply the URL withholding rule, and remove docs/evidence if it stays empty.

2. A known error to trace first. V0116 OrionW LLC is a Singapore law firm that specialises in technology, media and telecoms law, not an IT contractor. Move it to Legal and the law-firms lever. Find out why the first pass kept the wrong reading, and check every other row for the same cause.

3. Stage 1, all 386 rows, no web. Start a reviewer agent that has not seen how the rows were classified. It reads each row's research finding beside the final description, department, sub_function, cost_cluster and recommendation, and flags every row where the final row does not follow from the finding, follows a hint the finding contradicts, or breaks docs/taxonomy.md or docs/recommendation_rules.md.

4. Stage 2, fresh verification, in this order until done or the search limit stops you: every Stage 1 flag; every row at or above $10,000; then a seeded random sample of 30 of the remaining rows. For each, an agent that has seen neither the hint nor the first-pass result establishes from the vendor's own site or a reliable directory what the vendor does, in one line with its source. Compare that with the first pass.

5. Resolve every disagreement in the main session: change the row, or keep it with a one-line reason. Write qa/second_pass_review.csv (vendor_id, stage, field, first-pass value, reviewer finding, verdict, resolution) and qa/second_pass_report.md: what each stage looked for, rows and spend covered, agreement rate by field, every disagreement with its resolution, every row changed with before and after, and what was not covered and why.

PART C: text a reader of the sheet will see (still step 5)

The description, rationale and risk_note columns go into the sheet and are read by someone who has never seen this repository.
1. Rewrite every cell that refers to the project's own workings: hints, lists, rules, searches, sources, steps, prompts or files ("per the hint", "named in the Optimize list", "under the Terminate rule", "search shows", "no source confirms it"). State the fact or the action directly.
2. Where what a vendor does is not established, give the best reading and end the description with "(unconfirmed)" in place of "confirm with Finance". Descriptions stay one line of 5 to 25 words.
3. Office footprint rows: the rationale leads with the base case the savings assume (exit under the remote operating model, keeping one touchdown space at the engineering hub), then the fallback (one flexible provider).
4. A risk_note is now also required on every Optimize row at or above $25,000: one clause naming the main risk of acting, or of not acting where the row must not be cut. Update C16.
5. Add checks with planted errors: the three columns contain none of the workings phrases; a check that lists every Terminate row with a base saving under 50% whose lever is not one-off or excluded, and every Optimize row above 50%, each one then fixed or given a recorded reason. Print the cross-tab of recommendation by lever in qa/validation_report.md.

Then re-run the merge, the savings, the insights and all QA with both self-tests, commit as "Step 5: second-pass review and reader-facing text" and push. Print: the new savings totals by opportunity; Stage 1 and Stage 2 coverage and agreement rates; every row changed in this prompt with before and after; the count of text cells rewritten; anything not covered.
```

## Prompt 19 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 19. Run it after prompt 18 is committed. It writes the four documents and the sheet workbook. Read CLAUDE.md, docs/decisions.md, outputs/analysis/savings.md, outputs/analysis/insights.md, qa/validation_report.md and qa/second_pass_report.md first.

Rules for everything written in this prompt
- The readers are the CEO and CFO of the parent and the people assessing this work. They have not seen this repository. No project vocabulary (lever, cluster, depends_on, hint, batch) in the Top 3, the memo or the sheet.
- American English everywhere a reader sees it (the brief writes "Optimize"): the four documents and the description, rationale and risk_note columns. Add a check for common British forms.
- Refer to "the acquired business" and "the group".
- Acquirer decisions are presented as decisions with their value, never as facts about the group.
- Plain, short sentences. Past tense about what was done in this project.

PART A: presentation figures
Extend scripts/03_savings.py to write outputs/analysis/savings_summary.md: the figures the documents may quote, rounded to the nearest $1,000, with every total computed as the sum of the rounded lines it shows, so that parts always add to totals. Include: total spend; run-rate saving low, base, high; year 1; saving from vendor action alone; each of the three opportunities and the second wave (spend, low, base, high, year 1, without the decision, value of the decision); spend that falls away without action; spend that must not be cut; rows and spend verified; the second-pass figures. Add a check with planted errors: every dollar figure and percentage in the four documents appears in savings_summary.md or another file under outputs/analysis or qa, and every table in the documents adds up.

PART B: outputs/top3_opportunities.md
The three opportunities, ranked by base saving. For each: a specific title of at most 12 words; an explanation of 70 to 100 words that gives the evidence from the vendor data (vendors, spend), the calculation (spend times assumption, with the range), the first-year figure and why it is lower, the decision or action it needs, and the main risk; and the estimated annual saving in USD (base). For the Salesforce opportunity say that the product runs on the platform, so the lever is price and terms and never exit, and that the figure is the value of a negotiation that starts when the contract and usage data arrive. End the file with one line for the second wave and one for spend that falls away without action.

PART C: outputs/memo.md and outputs/memo.docx
A one-page memo to the CEO and CFO of the group from Chaitanya Laxman, VP Operations of the acquired business, dated November 11, 2026. At most 430 words outside the table. Order:
1. Subject line that carries the number.
2. Bottom line in two sentences: what was reviewed, the run-rate saving and its share of spend, the first-year figure, the high case and what gets there, and that three moves carry most of it.
3. One sentence of context they may not remember: what the data is, and that one vendor is about 40% of spend because the product runs on its platform.
4. A table of four rows (the three opportunities and the second wave) plus a total: move, run-rate saving, year 1, what it needs.
5. "Decisions needed": the two or three decisions only they can take, each with what it is worth compared with vendor action alone, and the date needed to hold the year-1 figure.
6. "Plan": four lines, 0 to 30 days, 30 to 90, 90 to 180, and 6 to 12 months, with what happens in each (contracts, renewal dates and usage data first; notices and negotiations; exits and transfers; system and audit moves at year-end), and one line on how it is run: one owner per move, a weekly tracker, a saving counted only when the contract changes.
7. "Risks": at most four, one line each: platform dependency; retention at the engineering hub; notice periods and exit costs not yet known; vendors that customers or regulators require, which stay.
8. One closing line on scale: against group revenue the direct saving is modest, and the value is a review that repeats on every acquisition, with the share of third-party spend this one found.
Also say in one line what is not counted: deal and one-off costs that fall away on their own. Build memo.docx from the same text (US Letter, 0.75 inch margins, 10.5 point, the table as a real table) and report the word count. Every figure comes from savings_summary.md.

PART D: outputs/methodology.md
For the Methodology tab: at most 400 words, written as short lines that each fit one spreadsheet row, under four headings. Approach: the steps in order, one line each, from profiling to documents. Tools that produced the outputs: Claude Code CLI with the model and the research agents, Python with pandas and openpyxl, web search and fetch, git and GitHub. Prompts: how many, that they are logged in prompts/log.md, the prompts that shaped the work (at most six) with one line each on what they asked, and the research brief. Validation and evidence: the automated checks and what each group looks for, the planted-error self-tests, web verification coverage, the second-pass review with its coverage, agreement rates and number of rows changed, reconciliation to the cent, and the path of each evidence file. Close with the limits: one 12-month total per vendor, modified names and costs, no contracts or headcount, and the rows left unconfirmed.

PART E: README.md and tidying
README sections: what this is; results in five lines; how the work was done, step by step, with the prompt number and commit for each step; repository map (inputs, outputs, scripts, qa, docs, prompts) with one line per file; how to re-run every script in order; quality checks and where the evidence is; assumptions and limits; a note that vendor names and costs were modified by the provider of the data. Remove empty folders and stray files, and confirm that every script named in the README runs from a clean clone.

PART F: the sheet workbook
Write scripts/05_build_sheet.py. It copies the raw workbook to outputs/sheet/Vendor Analysis Assessment - Chaitanya Laxman.xlsx, never touching the raw file, keeps the Department dropdown, and fills:
- Vendor tab, rows 2 to 387 in the original order: B department, D description, E recommendation, then new headed columns F Rationale, G Key risk, H Estimated annual saving (USD, base case), I Savings opportunity, J Verified online (Yes or No), K Source.
- Top 3 Opportunities tab: titles in B, explanations in C, and D headed "Estimated annual savings (USD)".
- Methodology tab: the methodology lines from row 2 down, one per row.
- CEOCFO Recommendations tab: row 2 "Memo (Google Doc): [link to be added]", then the memo text below.
Add a check that reads the workbook back and confirms every cell against the source files, the row order against the raw file, that every department is in the Config list, and that column H sums to the base saving.

Run every check and both self-tests, commit as "Step 6: Top 3, memo, methodology, README and sheet workbook", push, and print the Top 3, the memo and the methodology in full with the memo's word count.
```

## Prompt 20 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 20. Final corrections before submission. The rules of prompt 19 still apply.

PART A: the memo must fit one page
memo.docx renders to two pages. Rebuild it to fit one US Letter page with at least eight lines to spare:
- To, From and Date on one line; Subject on the next; 2 point spacing after paragraphs; no blank lines.
- Table columns sized so every row fits on one line (first column about 3.4 inches, the two number columns about 1 inch, the last about 1.6), set in the table grid as well as the cells; "What it needs" at most five words per cell; no count of landlords.
- At most 360 words outside the table.
- Render it to PDF with whatever this machine has, confirm the page count and the spare lines, and say how it was checked. If nothing here can render it, say so.
Content changes:
- Decision values must tie to the table. The remote operating model is worth the office row's saving minus its fallback ($448,000 on the current figures), not the wider figure that includes telecom lines.
- One date for both decisions (December 15, 2026) and the cost of delay: one twelfth of the two decision values for each month, as a figure in savings_summary.md. Drop the breakdown in brackets.
- Salesforce bullet: no decision needed; it needs the contract, the usage data and group procurement at the table.
- Plan, 30 to 90 days: "put the travel and expense policy in place" instead of stopping perks and card spend, which contradicts the retention risk and the model.
- Retention risk: say that benefits and a hub space stay.
- Check that the words describing every figure match what the figure contains.

PART B: Top 3
- Assumptions in the present tense ("assumes", not "assumed").
- Count office providers and countries from the rows instead of "five cities".
- "Any Salesforce agreement the group holds", not "the group's Salesforce relationship": that is a fact about the group we do not have. Same change in the Salesforce row's rationale.

PART C: sheet text
1. Where a row's saving rests on a group decision, its rationale leads with that base case (the group function it moves to) and gives the vendor-only fallback second. Jensten, 4i, Infosys and Weking do not do this now; check every such row.
2. Only duplicate records of one vendor need to name the other record. Remove the wording about corporate groups ("part of the Microsoft group but a separate service", "apart from the Amazon marketplaces in the same group", "not a consulting partner") and relax C12 to match.
3. Replace "of not acting:" with a plain sentence, and "excluded from the savings base" with "no saving counted".
4. A risk note states no fact about a vendor that the verification log does not support. V0022's note about site cuts goes unless a logged source supports it.
5. Where a Terminate row's saving is under half its spend, the rationale says why in a clause (pay passed through, stopped until confirmed).
6. Office rows labeled Consolidate start "Consolidate the offices into one hub space under a remote operating model: exit this space", so label and text agree.
7. Weking: the rationale starts with confirming the contract and the work, since a company founded in 2023 is the eighth-largest vendor.
8. Workbook: when a row's base saving is zero, column I reads "No saving counted: " plus the reason, in place of the opportunity name or "Excluded"; column J is headed "Vendor identified online (Yes/No)"; column H shows whole dollars.

PART D: methodology and manual review
- First line: the repository address.
- The prompts line: "Twenty prompts directed the analysis; they are logged in prompts/log.md in the order given." Do not call the log verbatim there: one housekeeping omission is marked in it.
- MANUAL REVIEW. I checked each of the 25 largest rows (rows 2 to 26, 78.5% of spend) against its source link and read the Top 3 and the memo line by line. My changes: [NONE]. Record this in qa/manual_review.md, apply any changes, and add one line to the methodology and the README.Rebuild every output, run all checks and both self-tests, commit as "Step 7: final corrections" and push. Print the memo, its word count and how its page count was checked; the changed Top 3 sentences; and the number of sheet cells changed.
```

## Prompt 21 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 21. Wording corrections, then rebuild.

1. Memo subject line, in memo.md, memo.docx and the workbook tab: "Vendor review: $2,229,000 a year in savings, $1,209,000 of it in year 1". Keep the memo on one page.
2. README, "How to re-run": the sentence that says the classification "was written by hand" is wrong as a reader will take it. The classification lines were written by Claude Code in the session, vendor by vendor, from the research findings and the rules, not typed by a person and not generated by a script. Say that.
3. README, "What this is": "The outputs were produced in one Claude Code session, prompt by prompt, with the prompts that directed the analysis logged, every step committed and every figure computed by a script from the data."
4. Methodology: the heading "Tools" becomes "Tools that produced the outputs".
5. Manual review, in qa/manual_review.md, the README and the methodology line: say exactly what was done. Of the 25 largest rows (78.5% of spend), 13 were checked against their source links and 12 are well-known vendors read against my own knowledge; the Top 3 and the memo were read line by line; no changes.
6. Update the prompt count wherever it is stated, and add this step to the README table.

Rebuild the documents and the workbook, run all checks and both self-tests, re-run the memo page check, commit as "Step 8: wording corrections" and push. Print the changed lines and the page-check result.
```

## Prompt 22 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 22. Last corrections; the rules of prompt 19 still apply.

1. Top 3, the calculations must reproduce. As written, a reader who multiplies gets a different answer (75% of $896,000 is $672,000, not $669,000; 15% of $3,117,000 is $468,000, not $515,000). State each calculation with its own base and rate, from the savings files:
   - Offices: the lease and coworking spend at 75% and the running costs at 70%, with both spend figures, so the two products add to the saving shown.
   - Salesforce: 15% of the platform agreement, 20% of the document app and 10% of the PSA tool, with each spend figure, adding to the saving shown.
   - Back office: name the three largest lines with spend, rate and saving (audit and accounting, recruiters, finance and HR systems), and the rest as one figure, adding to the saving shown.
   Explanations may run to 120 words. Add a check that recomputes every "rate of spend" statement in the Top 3 from savings.csv and fails if the rounded product does not match.
2. Memo, the Scale line: replace it with one sentence that states what the saving is worth rather than calling it modest: the base saving as a share of this business's third-party spend, that it falls straight to operating profit, and that the same review repeats on every acquisition. The word limit outside the table is now 380; keep one page.
3. Methodology, two lines under Approach, and the word limit is now 450:
   - The department rule in one sentence: the Config list names company functions, so SaaS is read as the function that runs the hosted product (platform, hosting, monitoring); company-wide software sits in G&A as corporate IT and function-specific software with its function.
   - Config has no HR or IT department, so HR, recruiting, travel, benefits, insurance and corporate IT sit in G&A, which is why it holds the most rows.
   Reword the tools line to "Claude Opus 5.5 through the classification step, Claude Fable 5.1 after it."
4. README: under "What this is", add the two deliverable links: the Google Sheet https://docs.google.com/spreadsheets/d/1LBowVBvWB4T5Ii1-9YZGiAOpO9L_ngidNbsS86yXrgQ and the memo https://docs.google.com/document/d/1ZVG70hx3l9UNfTCQIN2medwAudMVrYi-nsck-Ck9fN0. Update the prompt count wherever it is stated and add this step to the README table.

Rebuild the documents and the workbook, run all checks and both self-tests and the memo page check, commit as "Step 9: calculations that reproduce" and push. Print the three Top 3 explanations, the new Scale line, the new methodology lines, and the memo word count and page result.
```

## Prompt 23 (2026-11-11)

```text
Append this prompt to prompts/log.md as prompt 23. Run it after prompt 22 is committed. Two small corrections.

1. Spelling: V0174's risk note says "notarisation"; make it "notarization". Add the -isation and -ise forms to the British-forms check and re-scan every reader-facing text.
2. What the review leaves out, made visible:
   - Top 3 file, one more closing line: the people-linked vendor spend that this review does not count (health and life cover, statutory cover, benefit schemes, employer-of-record pay, student labor, less the small savings already counted on those lines), as one figure from savings.csv, with the reason: it moves only with the workforce plan.
   - Memo, the "Not counted" line: add ", and people-linked spend that moves only with the workforce plan" with no new figure. Keep the word limit of 380 and one page.
   - insights.md: the same figure with its vendor_ids.
3. Update the prompt count wherever it is stated and add this step to the README table.

Rebuild, run all checks, both self-tests and the page check, commit as "Step 10: spelling and what is not counted" and push. Print the changed lines.
```
