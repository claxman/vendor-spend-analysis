# Vendor hints

Analyst knowledge about specific vendors, given in prompt 6 (`prompts/log.md`) and reproduced here verbatim, one hint per row. Use these alongside general knowledge; depart from a hint only with a stated reason, recorded with the classification.

Each hint is mapped to the rows it covers, shown as `vendor_id` (V plus the source row) and the vendor name with mojibake repaired. `scripts/02_clean.py` checks that every id exists and every name matches. 79 hints cover 172 of 386 rows; the other 214 rows are classified from their names and general knowledge, with confidence set to match.

| # | Analyst hint (verbatim) | Rows in this file |
|---|---|---|
| 1 | Cloudcrossing BVBA: Belgian Salesforce consulting partner. | `V0006` Cloudcrossing Bvba |
| 2 | Kimble Applications: PSA software on the Salesforce platform (now Kantata). | `V0027` Kimble Applications Ltd |
| 3 | Mason Frank: Salesforce-specialist recruitment agency. | `V0034` Mason Frank International Ltd |
| 4 | Yoxel: Salesforce email and calendar sync. | `V0170` Yoxel, Inc |
| 5 | Navan (both entities): corporate travel and expense platform. | `V0003` Navan (Tripactions Inc); `V0024` Navan, Inc |
| 6 | TOG UK Properties: The Office Group, London flexible offices. | `V0005` Tog Uk Properties Limited |
| 7 | Zagrebtower: Zagreb office lease. | `V0007` Zagrebtower D.O.O. |
| 8 | Innovent Spaces: Chennai coworking. | `V0008` Innovent Spaces Private Limited |
| 9 | GPT Space & Co: Australian flexible workspace. | `V0011` Gpt Space & Co |
| 10 | Work Easy Space Solutions: Indian coworking. | `V0063` Work Easy Space Solutions Private Limited |
| 11 | Common Desk: US coworking. | `V0118` Common Desk, Llc |
| 12 | BDO LLP, Grant Thornton, PwC, Crowe Horwath Revizija, Collards, McBurneys, N S Shastri, Pinnacle Partnership, Taxstudio, Porezno Savjetništvo Tuk, Eurofast: audit, tax and accounting across the UK, Croatia, India, Greece. | `V0004` Bdo Llp; `V0029` Grant Thornton; `V0108` Pricewaterhousecoopers Llp; `V0114` Crowe Horwath Revizija D.O.O.; `V0070` Collards Chartered Accountants; `V0153` Mcburneys Charted Accountants; `V0164` N S Shastri And Co; `V0109` Pinnacle Partnership Ca; `V0064` Taxstudio, Ltd.; `V0176` Porezno Savjetništvo Tuk D.O.O.; `V0052` Eurofast International Ltd-Greec |
| 13 | Granttree: UK R&D tax credit claims consultancy paid as a share of the claim. | `V0068` Granttree Limited |
| 14 | 4i Advisory Services and 4i Management Consulting: Indian management and finance consulting, confirm scope. | `V0017` 4I Advisory Services; `V0072` 4I Management Consulting Private Limited |
| 15 | RSM UK Corporate Finance, Houlihan Lokey: M&A advisers. | `V0013` Rsm Uk Corporate Finance Llp; `V0035` Houlihan Lokey Advisors, Llc |
| 16 | SS&C Intralinks: virtual data room. | `V0031` Ss&C Intralinks Inc |
| 17 | Vector Capital Management: private equity sponsor fees, non-recurring after the sale. | `V0036` Vector Capital Management Lp |
| 18 | Westbrook Advisers: advisory, scope unknown. | `V0062` Westbrook Advisers |
| 19 | Jensten Insurance Brokers: UK commercial insurance broker. | `V0010` Jensten Insurance Brokers |
| 20 | Aetna, Agram Life, Care Health, Bupa (two entities), Cigna SG, ICICI Lombard, ICICI Prudential: employee health and life insurance by country. | `V0012` Aetna Life And Casualty Ltd; `V0042` Agram Life Osiguranje D.O.O.; `V0045` Care Health Insurance Company Limited; `V0047` Bupa- Supplier; `V0071` Bupa Australia; `V0069` Cigna Sg; `V0095` Icici Lombard Gic Ltd; `V0143` Cici Prudential Life Insurance Co. Ltd. |
| 21 | Allianz Australia Workers' Compensation and icare NSW: statutory workers' compensation. | `V0094` Allianz Australia Workers' Compensation (Victoria) Limited; `V0201` Icare Nsw |
| 22 | Mercer: benefits consulting. | `V0098` Mercer Limited |
| 23 | Harmonic Group, Cedar Recruitment: finance recruitment agencies. | `V0021` Harmonic Group Limited; `V0051` Cedar Recruitment Ltd |
| 24 | Technet IT Recruitment: IT recruitment. | `V0049` Technet It Recruitment |
| 25 | Accutrainee: legal trainee placement. | `V0033` Accutrainee Limited |
| 26 | Info Edge: Naukri job board. | `V0138` Info Edge India Limited |
| 27 | LinkedIn Ireland: recruiter licences, ads or Sales Navigator; default G&A recruiting, confidence medium. | `V0026` Linkedin Ireland Limited |
| 28 | HR Solution International GmbH and AG: HR outsourcing or employer of record in DACH. | `V0016` Hr Solution International Gmbh; `V0090` Hrsolution International Ag |
| 29 | Australian Payroll Professionals: payroll outsourcing. | `V0111` Australian Payroll Professionals Pty Ltd |
| 30 | Radius Group: likely global payroll and expansion services, confidence low. | `V0179` Radius Group, Inc |
| 31 | Peakon: employee engagement surveys. | `V0055` Peakon Aps |
| 32 | Performancepro: performance management software. | `V0080` Performancepro |
| 33 | Emerge Development Consultancy: leadership training. | `V0079` Emerge Development Consultancy Ltd |
| 34 | Epignosis: TalentLMS. | `V0221` Epignosis Llc |
| 35 | Kryterion: certification exam delivery, likely for customer or partner certification. | `V0124` Kryterion, Inc. |
| 36 | Pluxee and Sodexo India: meal benefits and office catering. | `V0128` Pluxee India Private Limited; `V0054` Sodexo Svc India Private Limited |
| 37 | Benefit Systems d.o.o.: MultiSport employee sports card. | `V0057` Benefit Systems D.O.O. |
| 38 | Green Commute Initiative: UK cycle-to-work scheme. | `V0100` Green Commute Initiative |
| 39 | Inside Edge Novated Leasing: Australian salary-packaged car leasing. | `V0195` Inside Edge Novated Leasing |
| 40 | Visalogic: UK immigration services. | `V0076` Visalogic Limited |
| 41 | Intertrust Singapore, Acclime (two entities), Capitol Services: corporate secretarial and registered agent. | `V0088` Intertrust Singapore Corporate Services Pte Ltd - Csc; `V0099` Acclime Corporate Services; `V0105` Acclime Usa, Inc; `V0334` Capitol Services |
| 42 | Computershare-Caboodle, Bigshare, NSDL: share plan administration and depository. | `V0211` Computershare-Caboodle Technology Limited; `V0305` Bigshare Services Private Limited; `V0284` National Securities Depository Limited(Nsdl) |
| 43 | Raiffeisenbank Austria d.d.: Croatian bank fees. | `V0216` Raiffeisenbank Austria D.D. |
| 44 | FastSpring: merchant-of-record payment processing. | `V0198` Fastspring |
| 45 | Ariba: SAP Ariba supplier network fees, customer-mandated. | `V0191` Ariba Inc |
| 46 | Telefónica Global Services GmbH and Telefónica Compras Electrónicas: payments to a customer's procurement or partner platform, confidence low, flag as a commercial dependency, do not terminate. | `V0015` Telefonica Global Services Gmbh; `V0093` Telefónica Compras Electrónicas S.L. |
| 47 | TM Forum (two spellings): telecom industry association membership and events. | `V0025` Tmforum; `V0249` Tm Forum |
| 48 | Terrapinn: conference organiser. | `V0150` Terrapinn Holdings Ltd |
| 49 | Big Frontier (Cult of Monday): Australian marketing agency. | `V0020` Big Frontier Pty Ltd (Cult Of Monday) |
| 50 | MightyHive: programmatic media agency. | `V0050` Mightyhive Ltd |
| 51 | Plus Your Business: LinkedIn marketing training. | `V0056` Plus Your Business Ltd |
| 52 | Uberflip: content experience platform. | `V0041` Uberflip |
| 53 | Cognism, Lusha, 6sense: B2B contact and intent data. | `V0040` Cognism Limited; `V0156` Lusha; `V0352` 6Sense Insights Inc |
| 54 | Outreach: sales engagement. | `V0084` Outreach Corporation |
| 55 | Carrington Communications, Cision PR Newswire: PR. | `V0184` Carrington Communications; `V0168` Cision Pr Newswire |
| 56 | Smashing Media: UX publication and conferences. | `V0220` Smashing Media Ag |
| 57 | Pixsy: image copyright monitoring. | `V0237` Pixsy Inc |
| 58 | Cloud Technology Solutions: UK Google Cloud and Workspace reseller. | `V0023` Cloud Technology Solutions Ltd |
| 59 | New Star Networks: UK telecom and IT managed services. | `V0046` New Star Networks(Nsn) |
| 60 | Infosys, Shree Info System Solutions, Crayond Digital, Orionw, Trending Technology Services: outsourced IT and development, confirm whether customer-project subcontracting. | `V0019` Infosys; `V0048` Shree Info System Solutions Pvt Ltd; `V0185` Crayond Digital Private Limited; `V0116` Orionw Llc; `V0213` Trending Technology Services Gmbh |
| 61 | Magazin Računalni Sistemi, E-Disti, Sniper Systems: IT hardware resellers. | `V0066` Magazin Raunalni Sistemi D.O.O.; `V0260` E-Disti D.O.O.; `V0131` Sniper Systems And Solutions Private Limited |
| 62 | NCC Services: software escrow. | `V0144` Ncc Services Limited |
| 63 | Bureau Veritas Croatia: ISO certification audits. | `V0142` Bureau Veritas Croatia D.O.O. |
| 64 | Centar za Sigurnost: occupational safety and fire protection services. | `V0106` Centar Za Sigurnost D.O.O. |
| 65 | Nastavni Zavod za Javno Zdravstvo, Specijalistička ordinacija medicine rada (three), Ustanova za zdravstvenu skrb: statutory occupational health examinations. | `V0300` Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar; `V0382` Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos; `V0383` Specijalisticka Ordinacija Medicine Rada Helena Blazic; `V0384` Ustanova Za Medicinu Rada I Sporta Dr. Novacki; `V0328` Ustanova Za Zdravstvenu Skrb P.P. |
| 66 | Grad Zagreb, Grad Split: municipal fees. | `V0073` Grad Zagreb, Gradski Ured Za Prostorno Uređenje,..; `V0139` Grad Split |
| 67 | Zagrebački Holding: Zagreb city utilities. | `V0321` Zagrebački Holding D.O.O. |
| 68 | HEP Elektra: electricity. | `V0119` Hep Elektra D.O.O. |
| 69 | Hrvatski Telekom, Telemach, T-Mobile, Vodafone Australia, Starhub, BT, Inet Telecoms, Zettanet: telecom and internet. | `V0053` Hrvatski Telekom D.D.; `V0104` Telemach Hrvatska D.O.O.; `V0140` T-Mobile; `V0135` Vodafone (Australian); `V0163` Starhub Ltd (Supplier); `V0188` British Telecommunications; `V0356` Inet Telecoms Ltd.; `V0306` Zettanet |
| 70 | Avoxi: cloud telephony numbers. | `V0309` Avoxi Inc |
| 71 | Click Send: SMS API. | `V0363` Click Send Pty Ltd |
| 72 | Studentski Centar (Zagreb, Split, Karlovac): Croatian student-service work contracts, contingent labour, not a vendor service. | `V0030` Sveučilište U Zagrebu, Studentski Centar; `V0086` Studentski Centar - Split; `V0186` Studentski Centar Karlovac |
| 73 | Hrvatski Nezavisni Izvoznici Softvera, Split Tech City: industry and community memberships. | `V0318` Hrvatski Nezavisnici Izvoznici Softvera; `V0283` Split Tech City |
| 74 | Entrio: event ticketing. | `V0257` Entrio Tehnologije D.O.O. |
| 75 | Lajnap, Escape Art, Maniax, Sportkart, Paint & Fun, Paint&Wine, DJs For U, Blitz Cinestar, Good Game Global, Chamiers and P S Recreation Clubs, Sportska Udruga Split, Friends Sports Club: team events and recreation. | `V0187` Lajnap Comedy Booking D.O.O.; `V0326` Escape Art D.O.O.; `V0277` Maniax Melbourne Cbd; `V0323` Sportkart D.O.O.; `V0183` Paint & Fun Vl. Martina Milkova Nikolova; `V0315` Paint&Wine, Vl. Stevo Dosen; `V0298` Djs For U; `V0265` Blitz - Cinestar D.O.O.; `V0146` Good Game Global D.O.O.; `V0192` Chamiers Recreation Club; `V0197` P S Recreation Club; `V0354` Sportska Udruga Split; `V0227` Friends Sports Club |
| 76 | Konzum, Spar, Müller, Pepco, Ikea Hrvatska, Officeworks, Platinum Office, Roto Dinamic, Fero-Term, Brodomerkur: office groceries, supplies and furniture. | `V0061` Konzum Plus D.O.O.; `V0274` Spar Hrvatska D.O.O.; `V0207` Müller Trgovina Zagreb D.O.O.; `V0343` Pepco Croatia D.O.O.; `V0136` Ikea Hrvatska D.O.O.; `V0362` Officeworks; `V0358` Platinum Office D.O.O.; `V0248` Roto Dinamic D.O.O.; `V0327` Fero-Term; `V0379` Brodomerkur D.D. |
| 77 | Weking d.o.o., Veniture d.o.o., Nefron obrt, Bijeli Pijesak obrt, Smart Group Services, TP Prime, Pingo, Ramiro, Omonia, Mosaic Concept, Limes Plus, Orcola, Akton: Croatian companies or sole traders of unknown function, most likely contractors; department by best inference, confidence low, description ends with "confirm with Finance". | `V0009` Weking D.O.O.; `V0032` Veniture D.O.O.; `V0038` Nefron - Obrt Za Poslovne Usluge; `V0074` Bijeli Pijesak Obrt Za Poslovno Savjetovanje; `V0058` Smart Group Services D.O.O.; `V0067` Tp Prime D.O.O.; `V0065` Pingo D.O.O.; `V0075` Ramiro D.O.O.; `V0083` Omonia D.O.O.; `V0096` Mosaic Concept D.O.O.; `V0097` Limes Plus D.O.O.; `V0137` Orcola D.O.O.; `V0141` Akton D.O.O. |
| 78 | Stipe Piric, John Smith, Fabiola Thistlewhaite, George Anchor, Susan Lee, Ansar Madovic: individual payees, likely contractors or reimbursements, G&A, confidence low. | `V0160` Stipe Piric; `V0165` John Smith; `V0166` Fabiola Thistlewhaite; `V0169` George Anchor; `V0177` Susan Lee; `V0178` Ansar Madovic |
| 79 | (Blank): unnamed payee, G&A, Terminate, control gap. | `V0325` (Blank) |

## Notes from mapping the hints (added by Claude)

None of these overrides a hint.

1. `V0212` Allianz Wa is not named in the hints. Its name and its pairing with `V0094` point to the same Allianz workers' compensation business, in Western Australia, so it takes the same hint. The two are separate state policies and are linked, not merged (decision of 2026-11-10).
2. Pluxee and Sodexo India: the web verification decided (decision of step 2c, settled in step 3). Sodexo SVC India Private Limited is the former legal name of Pluxee India Private Limited, renamed in May 2024, the meal-card and benefits business, so the two rows are a merge. This departs from hint 36 on one point: Sodexo SVC India is not office catering.
3. Spellings in the file that differ from the hints: ICICI Prudential is `Cici Prudential` (`V0143`); Hrvatski Nezavisni Izvoznici Softvera is `Hrvatski Nezavisnici Izvoznici Softvera` (`V0318`); Magazin Računalni Sistemi is `Magazin Raunalni Sistemi` (`V0066`, the č restored in the clean name); McBurneys is `Mcburneys Charted Accountants` (`V0153`). The three "Specijalistička ordinacija medicine rada" rows are `V0382` and `V0383` (specijalistička ordinacija) and `V0384` (ustanova za medicinu rada).
4. Corporate parents that link vendors in this file: Slack (`V0173`) is a Salesforce company; Trello (`V0091`) is an Atlassian product; Papertrail (`V0130`) is a SolarWinds product; LinkedIn (`V0026`) and npm (`V0125`) are Microsoft companies; ICICI Lombard (`V0095`) and ICICI Prudential (`V0143`) are separate ICICI group insurers. These are recorded as links (`link_group`) in `qa/vendor_groups.csv`, not as merges.
5. Ownership changes worth knowing when the parent's own systems are compared: Kimble merged into Kantata (as the hint says), Peakon is part of Workday, and Navan traded as TripActions until 2023.
6. Hints that name two entities ("Bupa (two entities)", "Acclime (two entities)", "HR Solution International GmbH and AG", the two Telefónica entities) describe the same brand, not one contract. Under the merge policy of 2026-11-10 these rows are linked rather than merged; only Navan (rename), TM Forum (spelling), AWS (one service under two entity names), 4i (one firm under two entities, confirmed by web verification in step 3) and Pluxee (rename, step 3) are merged. See `docs/decisions.md`.
