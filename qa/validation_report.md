# Validation report

Written by `scripts/merge_validate.py`, which merged the batch files in `outputs/batches/` into `outputs/vendors_classified.csv`, sorted by `vendor_id` (the original sheet order), and ran `qa/check_outputs.py` on it. The report is rebuilt on every run and is not edited by hand: the reason for a row with `verified` FALSE goes in `qa/verification_exceptions.csv`.

**Result: PASS.** All 50 checks passed.

## Counts

| Measure | Value |
|---|---|
| Batch files merged | 10 (batch_01.csv to batch_10.csv) |
| Rows in the batches | 386 |
| Distinct vendor_ids | 386 |
| Source rows in `outputs/vendors_clean.csv` | 386 |
| Source rows in no batch | 0 |
| Total `spend_12m` | $7,887,360 (source total $7,887,360) |
| `verified` TRUE | 319 vendors, $7,791,090 (98.8% of spend) |
| `verified` FALSE | 67 vendors, $96,270 (1.2% of spend) |
| `is_addressable` TRUE | 369 vendors, $7,765,704 (98.5% of spend) |
| `is_recurring` TRUE | 269 vendors, $7,542,174 (95.6% of spend) |
| Confidence low | 85 vendors, $278,612 (3.5% of spend) |

Rows per batch:

| Batch | Rows | Lowest vendor_id | Highest vendor_id |
|---|---|---|---|
| batch_01.csv | 40 | V0002 | V0041 |
| batch_02.csv | 40 | V0042 | V0081 |
| batch_03.csv | 40 | V0082 | V0121 |
| batch_04.csv | 40 | V0122 | V0161 |
| batch_05.csv | 40 | V0162 | V0201 |
| batch_06.csv | 40 | V0202 | V0241 |
| batch_07.csv | 40 | V0242 | V0281 |
| batch_08.csv | 40 | V0282 | V0321 |
| batch_09.csv | 40 | V0322 | V0361 |
| batch_10.csv | 26 | V0362 | V0387 |

## Distribution by department

| Department | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| Engineering | 15 | 3.9% | $281,648 | 3.6% |
| Facilities | 51 | 13.2% | $987,833 | 12.5% |
| G&A | 221 | 57.3% | $1,664,402 | 21.1% |
| Legal | 25 | 6.5% | $201,777 | 2.6% |
| M&A | 4 | 1.0% | $226,932 | 2.9% |
| Marketing | 25 | 6.5% | $237,785 | 3.0% |
| SaaS | 9 | 2.3% | $3,442,832 | 43.6% |
| Product | 2 | 0.5% | $4,149 | 0.1% |
| Professional Services | 2 | 0.5% | $56,367 | 0.7% |
| Sales | 8 | 2.1% | $138,344 | 1.8% |
| Support | 1 | 0.3% | $178 | 0.0% |
| Finance | 23 | 6.0% | $645,113 | 8.2% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by recommendation

| Recommendation | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| Terminate | 151 | 39.1% | $668,676 | 8.5% |
| Consolidate | 110 | 28.5% | $2,527,458 | 32.0% |
| Optimize | 125 | 32.4% | $4,691,227 | 59.5% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by cost cluster

| Cost cluster | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| Salesforce platform | 5 | 1.3% | $3,382,759 | 42.9% |
| Office footprint | 10 | 2.6% | $837,043 | 10.6% |
| Office running costs | 44 | 11.4% | $85,577 | 1.1% |
| Travel and entertainment | 50 | 13.0% | $465,303 | 5.9% |
| Team events, perks and wellness | 35 | 9.1% | $44,812 | 0.6% |
| Audit, tax, accounting and corporate services | 24 | 6.2% | $590,674 | 7.5% |
| M&A and transaction costs | 4 | 1.0% | $226,932 | 2.9% |
| Legal | 20 | 5.2% | $183,823 | 2.3% |
| Insurance and benefits | 25 | 6.5% | $428,012 | 5.4% |
| Recruiting and HR outsourcing | 19 | 4.9% | $408,206 | 5.2% |
| Cloud, telecom and IT | 30 | 7.8% | $238,201 | 3.0% |
| Outsourced engineering and contractors | 6 | 1.6% | $227,624 | 2.9% |
| Software subscriptions (non-Salesforce) | 39 | 10.1% | $377,257 | 4.8% |
| Marketing agencies, media and memberships | 27 | 7.0% | $177,352 | 2.2% |
| Customer-mandated platform fees | 3 | 0.8% | $97,400 | 1.2% |
| Statutory and government | 6 | 1.6% | $15,646 | 0.2% |
| Student labour | 3 | 0.8% | $54,117 | 0.7% |
| Unidentified and individual payees | 36 | 9.3% | $46,622 | 0.6% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by confidence

| Confidence | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| high | 179 | 46.4% | $5,595,342 | 70.9% |
| medium | 122 | 31.6% | $2,013,407 | 25.5% |
| low | 85 | 22.0% | $278,612 | 3.5% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Low-confidence vendors

85 vendors, $278,612 (3.5% of spend), sorted by spend, largest first.

| vendor_id | Vendor | Spend | Department | Recommendation | Description |
|---|---|---|---|---|---|
| V0015 | Telefonica Global Services GmbH | $89,880 | Sales | Optimize | Global procurement company of the Telefónica group in Munich, a customer's buying arm; what these payments cover is for Finance |
| V0038 | Nefron - Obrt Za Poslovne Usluge | $30,614 | Marketing | Terminate | Podstrana sole trader registered to organize meetings and trade fairs; what it supplied the company is not shown (unconfirmed) |
| V0043 | Google Ireland Limited | $24,798 | Marketing | Optimize | Google's Dublin billing entity for Ads and Cloud in Europe; the product bought is not shown, most likely Google Ads (unconfirmed) |
| V0074 | Bijeli Pijesak Obrt Za Poslovno Savjetovanje | $11,605 | G&A | Terminate | Croatian sole trader whose name says business consulting; the work is not established (unconfirmed) |
| V0082 | Catering Muring | $9,603 | Facilities | Terminate | Caterer by its name, most likely office catering for the Croatian office (unconfirmed) |
| V0087 | The Guardian | $8,070 | Marketing | Optimize | UK newspaper publisher selling subscriptions, advertising and Guardian Jobs recruitment ads; which was bought is unconfirmed, for marketing or HR |
| V0092 | Obrt Sjaj Sunca | $6,596 | G&A | Terminate | Croatian sole trader in Split whose activity is not established (unconfirmed) |
| V0093 | Telefónica Compras Electrónicas S.L. | $6,157 | Sales | Optimize | Telefónica's Madrid procurement company running the group purchasing platform suppliers must use; what these payments cover is for Finance |
| V0096 | Mosaic Concept d.o.o. | $5,731 | Marketing | Terminate | Zagreb micro company registered to organize meetings and business fairs; what it supplied the company is not shown (unconfirmed) |
| V0102 | Athlete Service Ltd | $5,285 | G&A | Terminate | UK cycling and triathlon retailer selling bikes, clothing and accessories, per a company-data site; what was bought is unconfirmed |
| V0107 | Profi Bar d.o.o. | $4,917 | G&A | Terminate | Croatian company whose name suggests a bar or drinks supplier; what it provides is not established (unconfirmed) |
| V0110 | The Virtual Legal Counsel Ltd | $4,800 | Legal | Consolidate | London company whose name suggests outsourced in-house legal counsel, registered as a management consultancy, for legal (unconfirmed) |
| V0111 | Australian Payroll Professionals Pty Ltd | $4,399 | G&A | Terminate | Payroll outsourcing for Australian staff by its name (unconfirmed) |
| V0137 | Orcola d.o.o. | $3,545 | G&A | Terminate | Croatian company whose function its name does not show, most likely a contractor (unconfirmed) |
| V0140 | T-Mobile | $3,357 | Facilities | Consolidate | Mobile telecom services under Deutsche Telekom's T-Mobile brand; the billing company and country are not shown, for staff lines |
| V0147 | Garaža Firule d.o.o. | $2,930 | Facilities | Optimize | Split company tied to an underground garage with parking, most likely staff parking (unconfirmed) |
| V0148 | Crossland | $2,924 | G&A | Terminate | Payee name shared by many unrelated businesses, among them a solicitor and a 4imprint brand; which one was paid is not established (unconfirmed) |
| V0149 | It London | $2,838 | G&A | Terminate | Payee whose name suggests IT services in London; no business trades under this name (unconfirmed) |
| V0151 | Elemental Life Solutions LLP | $2,807 | G&A | Terminate | LLP whose name does not show its function; not in the UK or Indian company registers (unconfirmed) |
| V0157 | My Foodiverse LLP | $2,489 | G&A | Terminate | LLP whose name suggests a food business; not in the UK or Indian company registers (unconfirmed) |
| V0160 | Stipe Piric | $2,302 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0162 | Pink Ribbon Shop | $2,251 | G&A | Terminate | Charity merchandise shop by its name, selling pink ribbon items for breast cancer charities; which shop was paid is not established (unconfirmed) |
| V0164 | N S Shastri And Co | $2,194 | Finance | Consolidate | Indian accounting and tax firm by its name, for the finance team (unconfirmed) |
| V0165 | John Smith | $2,163 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0166 | Fabiola Thistlewhaite | $2,154 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0169 | George Anchor | $2,107 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0177 | Susan Lee | $1,762 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0178 | Ansar Madovic | $1,732 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement, paid through AP (unconfirmed) |
| V0180 | Aquila Remete d.o.o. | $1,706 | G&A | Terminate | Croatian company, possibly in Zagreb's Remete area, whose function its name does not show (unconfirmed) |
| V0181 | Clime India Private Limited | $1,678 | G&A | Terminate | Indian company whose function is not established; the name may be a truncation of Acclime India (unconfirmed) |
| V0182 | Golden Mean, Inc | $1,659 | G&A | Terminate | Company with a US legal form whose function its name does not show (unconfirmed) |
| V0183 | Paint & Fun Vl. Martina Milkova Nikolova | $1,654 | G&A | Terminate | Painting-party business by its name, used for team events (unconfirmed) |
| V0189 | ETM Concessions Ltd | $1,419 | G&A | Terminate | UK company of the ETM Group whose activity is not established (unconfirmed) |
| V0192 | Chamiers Recreation Club | $1,338 | G&A | Terminate | Recreation club by its name, used for team events or recreation (unconfirmed) |
| V0197 | P S Recreation Club | $1,219 | G&A | Terminate | Recreation club by its name, used for team events or recreation (unconfirmed) |
| V0205 | Oladi d.o.o. | $1,064 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0208 | Lunch Nutrition d.o.o. | $1,012 | G&A | Terminate | Zagreb workplace meal service delivering balanced lunches to employees, with business accounts for employers, for staff meals |
| V0209 | Winmaxi Tours & Travels | $1,001 | G&A | Consolidate | Travel and tours business by its name, location unknown (unconfirmed) |
| V0215 | Time Out Group | $920 | G&A | Terminate | Time Out media and food-market group, paid for advertising or food at a Time Out Market; which is not shown |
| V0217 | Galop-Prijevoz d.o.o. | $908 | G&A | Terminate | Croatian company whose name means transport; what it carried is not established (unconfirmed) |
| V0219 | Urbani Eventi d.o.o. | $851 | G&A | Terminate | Croatian company whose name means urban events (unconfirmed) |
| V0223 | BB Football Scouting j.d.o.o. | $823 | G&A | Terminate | Croatian company whose name suggests football scouting; what it supplied is not established (unconfirmed) |
| V0226 | President Hotel And Tower Co., Ltd | $803 | G&A | Optimize | Hotel company by its name, most likely in Bangkok (unconfirmed) |
| V0227 | Friends Sports Club | $797 | G&A | Terminate | Sports club by its name, used for team recreation (unconfirmed) |
| V0233 | Catering Ivić d.o.o. | $669 | Facilities | Terminate | Caterer by its name, for office or event catering (unconfirmed) |
| V0234 | Blink Events | $664 | G&A | Terminate | Events business by its name, location unknown (unconfirmed) |
| V0235 | Grafo-Jan | $662 | Marketing | Terminate | Business whose name may suggest printing or graphics; not found under any spelling (unconfirmed) |
| V0236 | Mesa Verde | $662 | G&A | Terminate | Payee whose function its name does not show (unconfirmed) |
| V0253 | Streamlinereforms Inc | $483 | G&A | Terminate | US company whose function its name does not show (unconfirmed) |
| V0254 | Make And Grow Ltd | $483 | Engineering | Optimize | Small London company registered for software publishing and IT services; the product bought is not shown |
| V0256 | Rudan d.o.o. | $473 | G&A | Optimize | Istrian company in energy services and hotels; the AP data does not show which was bought, most likely a hotel stay |
| V0263 | Tiganda j.d.o.o. | $432 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0266 | Lancefield Bus Service | $412 | G&A | Terminate | Bus service by its name in Lancefield, Victoria, most likely transport for a team offsite (unconfirmed) |
| V0267 | Super Odredište d.o.o. | $378 | G&A | Terminate | Croatian company registered among other things to stage performances; its main activity is not shown (unconfirmed) |
| V0272 | Niva Transport j.d.o.o. | $358 | G&A | Terminate | Croatian company whose name suggests transport; what it carried is not established (unconfirmed) |
| V0285 | Adamma Info Services Private Limited | $273 | G&A | Terminate | Indian information services company by its name; its service is not established (unconfirmed) |
| V0289 | Taste Of Health | $259 | G&A | Terminate | Food business by its name, location unknown (unconfirmed) |
| V0290 | Infodata | $241 | Engineering | Optimize | Zagreb firm servicing IT equipment, printers, servers and networks, used for office IT repairs |
| V0293 | Bella Operation A/S | $241 | G&A | Optimize | Copenhagen congress venue and hotel operator; whether the charge was a hotel stay or an event fee is not shown |
| V0294 | The Plant Man | $235 | Facilities | Terminate | Office plant or landscaping supplier by its name, most likely office plants (unconfirmed) |
| V0295 | Media Promo Plus d.o.o. | $226 | Marketing | Terminate | Croatian company whose name suggests media and promotional work (unconfirmed) |
| V0296 | Expert-Ing d.o.o. | $225 | G&A | Terminate | Croatian company whose name suggests engineering; what it does is not established (unconfirmed) |
| V0301 | Rishi Events And Entainment | $198 | G&A | Terminate | Events and entertainment business by its name, most likely in India (unconfirmed) |
| V0302 | Kosmaz Technologies Croatia | $195 | G&A | Terminate | Payee whose name suggests a Croatian tech firm; no record of it in Croatia (unconfirmed) |
| V0312 | Xenon Savjetovanje d.o.o. | $164 | G&A | Terminate | Zagreb micro company registered for business and management consultancy; the advice bought is not shown |
| V0317 | Advena | $154 | G&A | Terminate | Payee name shared by a UK regulatory consultancy and an Australian security firm; which one was paid is not established (unconfirmed) |
| V0319 | Monile j.d.o.o. | $152 | G&A | Terminate | Croatian company name shared by a menswear brand owner and a Split bar; which one was paid is not established (unconfirmed) |
| V0320 | Puzzle Promotion j.d.o.o. | $143 | Marketing | Terminate | Croatian company whose name suggests promotional work (unconfirmed) |
| V0322 | Event Ors | $143 | G&A | Terminate | Events business by its name, matching several unrelated event firms (unconfirmed) |
| V0325 | (Blank) | $137 | G&A | Terminate | Unnamed payee with no vendor name in the ledger, a control gap (unconfirmed) |
| V0331 | Illunis d.o.o. | $128 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0335 | Bonus Opinio d.o.o. | $120 | G&A | Terminate | Croatian company registered for publishing and online services; its actual product is not shown (unconfirmed) |
| V0338 | Soho Kitchen Ltd | $104 | Facilities | Terminate | Caterer or kitchen by its name in London (unconfirmed) |
| V0339 | Fortis Trade j.d.o.o. | $95 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0340 | Till Trade d.o.o. | $93 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0344 | Lemia d.o.o. | $88 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0346 | Meluba Limited | $88 | G&A | Terminate | UK company in Kettering whose activity is not established (unconfirmed) |
| V0354 | Sportska Udruga Split | $66 | G&A | Terminate | Sports association in Split by its name, used for team recreation (unconfirmed) |
| V0358 | Platinum Office d.o.o. | $62 | G&A | Terminate | Split micro company registered for business and management consultancy; the advice bought is not shown (unconfirmed) |
| V0360 | New Block d.o.o. | $56 | G&A | Terminate | Croatian company whose function its name does not show (unconfirmed) |
| V0365 | Shilton Hospitality LLP | $55 | G&A | Optimize | Bengaluru hospitality group running business hotels, dining and catering, paid for a stay or meal |
| V0367 | Istra Wine | $53 | G&A | Terminate | Wine seller by its name, most likely Istrian wine bought as gifts (unconfirmed) |
| V0373 | Livingstone | $41 | G&A | Terminate | Payee name shared by many unrelated businesses, possibly an Australian office supplies distributor (unconfirmed) |
| V0382 | Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos | $20 | G&A | Optimize | Croatian occupational and sports medicine practice by its name, for statutory staff examinations (unconfirmed) |
| V0383 | Specijalisticka Ordinacija Medicine Rada Helena Blazic | $20 | G&A | Optimize | Croatian occupational medicine practice by its name, for statutory staff examinations (unconfirmed) |

## Verification exceptions

Every row with `verified` FALSE, by `vendor_id`, with a one-line reason, as kept in `qa/verification_exceptions.csv`. Check C17 compares this list with the `verified` column, both ways.

- V0074: no registry entry or other source was found for the sole trader after three searches
- V0082: two searches found no business named Catering Muring
- V0092: a directory snippet places a sole trader of this name in Split, but no readable source shows its activity
- V0107: no company named Profi Bar d.o.o. was found after two searches
- V0111: no company or business name was found in search results or in four ABN register records
- V0137: no company named Orcola d.o.o. was found in Croatian registries or elsewhere after two searches
- V0147: court and land registry notices tie the company to an underground garage in Split, but no source states its activity
- V0148: the name matches many unrelated businesses and no legal form or location narrows it down
- V0149: no business named IT London was found after two searches
- V0151: no LLP of this name was found in UK or Indian registries after two searches
- V0157: no entity named My Foodiverse LLP was found in UK or Indian registries after two searches
- V0160: individual payee; no business record to verify against
- V0162: two searches found several charity pink ribbon shops but none that matches this payee
- V0164: two searches found no firm named N S Shastri And Co
- V0165: individual payee; no business record to verify against
- V0166: individual payee; no business record to verify against
- V0169: individual payee; no business record to verify against
- V0177: individual payee; no business record to verify against
- V0178: individual payee; no business record to verify against
- V0180: no company named Aquila Remete d.o.o. was found after two searches
- V0181: no company named Clime India Private Limited was found after two searches
- V0182: no company named Golden Mean, Inc was found after two searches
- V0183: no business trading as Paint & Fun was found after two searches
- V0189: Companies House lists ETM Concessions Limited but no source states what it does
- V0192: no club named Chamiers Recreation Club was found after two searches
- V0197: no club named P S Recreation Club was found after two searches
- V0205: no company named Oladi d.o.o. was found in Croatian registries after two searches
- V0209: no business named Winmaxi Tours & Travels was found after two searches
- V0217: no company named Galop-Prijevoz d.o.o. was found in Croatian registries after two searches
- V0219: no company named Urbani Eventi d.o.o. was found in Croatian registries after two searches
- V0223: no company named BB Football Scouting j.d.o.o. was found after two searches
- V0226: two searches and a page fetch found no company of this name
- V0227: no club named Friends Sports Club was found after two searches
- V0233: no company named Catering Ivić d.o.o. was found after two searches
- V0234: no business named Blink Events was found after two searches
- V0235: no business named Grafo-Jan was found under any spelling after two searches
- V0236: no business named Mesa Verde was found in Zagreb or Chennai after two searches
- V0253: no company named Streamlinereforms Inc or Streamline Reforms was found after two searches
- V0263: no registry entry or website for Tiganda j.d.o.o. was found after two searches
- V0266: no business named Lancefield Bus Service was found; results were only public bus route news
- V0267: the company appears on a paywalled registry page that does not show its main activity
- V0272: no registry entry or website for Niva Transport j.d.o.o. was found after two searches
- V0285: two searches found only a job listing and no registry record or description of the business
- V0289: the generic name matched only unrelated food businesses after two searches
- V0294: two possible UK businesses match the name but neither is confirmed
- V0295: no company named Media Promo Plus d.o.o. was found after two searches
- V0296: no registry or website record for Expert-Ing d.o.o. was found after two searches
- V0301: no business matching Rishi Events And Entainment was found after two searches
- V0302: no registry entry, website or other record for Kosmaz Technologies in Croatia was found after two searches
- V0317: two companies named Advena exist in payer countries and nothing ties either to this payee
- V0319: two Croatian companies named Monile exist, neither as a j.d.o.o., and nothing ties either to this payee
- V0320: no company named Puzzle Promotion j.d.o.o. was found after two searches
- V0322: no business named Event Ors was found, and the joined spelling matches several unrelated event firms
- V0325: the payee has no name in the source data, so there is nothing to search
- V0331: no registry entry, website or other record for Illunis d.o.o. in Croatia was found after two searches
- V0335: the company exists on a paywalled registry page that does not show its main activity or product
- V0338: no UK company named Soho Kitchen Ltd was found after two searches
- V0339: no registry entry, website or other record for Fortis Trade j.d.o.o. was found after two searches
- V0340: no registry entry, website or other record for Till Trade d.o.o. was found after two searches
- V0344: no Croatian company named Lemia d.o.o. was found after two searches
- V0346: Companies House lists Meluba Limited but no readable source shows what it does
- V0354: no association registered as Sportska udruga Split was found after two searches
- V0360: no registry entry, website or other record for New Block d.o.o. was found after two searches
- V0367: no business trading as Istra Wine was found after two searches
- V0373: several unrelated businesses share the name and nothing ties one to this payee
- V0382: no web record of the practice was found after two searches
- V0383: no web record of the practice was found after two searches

## Recommendation by lever

Rows per recommendation on each savings lever, with the lever's base saving percentage. Check V9 lists the Terminate rows on levers below 50% outside the Excluded opportunity and the Optimize rows on levers above 50%, each fixed or given a recorded reason.

| Lever | Opportunity | Base % | Terminate | Consolidate | Optimize | Rows | Spend |
|---|---|---|---|---|---|---|---|
| Salesforce platform agreement | Salesforce platform agreement | 15 | 0 | 0 | 1 | 1 | $3,117,226 |
| Navan | Second wave | 25 | 0 | 0 | 2 | 2 | $415,913 |
| Audit, tax and accounting firms | Back office into group shared services | 35 | 0 | 14 | 1 | 15 | $553,641 |
| Office footprint | Office exit | 75 | 0 | 8 | 2 | 10 | $837,043 |
| PDF Butler OEM pricing | Salesforce platform agreement | 20 | 0 | 0 | 1 | 1 | $208,675 |
| Outsourced engineering and contractors | Second wave | 30 | 0 | 3 | 0 | 3 | $212,310 |
| Commercial insurance through brokers | Back office into group shared services | 25 | 0 | 1 | 1 | 2 | $152,800 |
| Employee health and life insurance | Back office into group shared services | 10 | 0 | 9 | 1 | 10 | $237,127 |
| M&A and transaction costs | Excluded | 0 | 4 | 0 | 0 | 4 | $226,932 |
| AWS | Second wave | 20 | 0 | 0 | 2 | 2 | $111,552 |
| Customer-mandated platform fees | Excluded | 0 | 0 | 0 | 3 | 3 | $97,400 |
| Employer-of-record providers | Back office into group shared services | 15 | 3 | 0 | 0 | 3 | $89,532 |
| Law firms and legal resourcing | Back office into group shared services | 30 | 0 | 12 | 1 | 13 | $178,321 |
| External training and coaching | Back office into group shared services | 50 | 0 | 4 | 0 | 4 | $91,765 |
| Recruitment agencies and job boards | Back office into group shared services | 100 | 7 | 0 | 0 | 7 | $149,179 |
| Other software subscriptions | Second wave | 25 | 2 | 12 | 19 | 33 | $242,907 |
| TM Forum | Second wave | 0 | 0 | 2 | 0 | 2 | $58,070 |
| LinkedIn | Back office into group shared services | 30 | 0 | 0 | 1 | 1 | $55,573 |
| Kimble PSA licences | Salesforce platform agreement | 10 | 0 | 0 | 1 | 1 | $52,825 |
| HR and finance systems | Back office into group shared services | 80 | 0 | 4 | 0 | 4 | $101,762 |
| Student labour | Excluded | 0 | 0 | 0 | 3 | 3 | $54,117 |
| HubSpot | Back office into group shared services | 80 | 0 | 1 | 0 | 1 | $32,187 |
| Other marketing, media and events | Second wave | 30 | 7 | 2 | 7 | 16 | $78,942 |
| Telecom and internet providers | Second wave | 40 | 0 | 7 | 4 | 11 | $70,891 |
| Employee hardware | Second wave | 10 | 0 | 10 | 0 | 10 | $50,925 |
| Marketing agencies | Second wave | 50 | 0 | 2 | 1 | 3 | $37,770 |
| Statutory cover and benefit schemes | Back office into group shared services | 0 | 0 | 2 | 11 | 13 | $54,004 |
| Payroll processing providers | Back office into group shared services | 40 | 2 | 0 | 0 | 2 | $20,838 |
| Office running costs | Office exit | 70 | 12 | 1 | 9 | 22 | $59,297 |
| One-off spend that falls away | Excluded | 0 | 35 | 2 | 9 | 46 | $47,199 |
| R&D tax credit adviser (contingent fee) | Back office into group shared services | 0 | 0 | 0 | 1 | 1 | $13,659 |
| Statutory and government | Excluded | 0 | 0 | 0 | 6 | 6 | $15,646 |
| Unidentified and individual payees | Second wave | 50 | 20 | 0 | 0 | 20 | $46,759 |
| Other travel, hotels, restaurants and food through AP | Second wave | 50 | 26 | 8 | 14 | 48 | $49,390 |
| Corporate secretarial, registered agent and share registry | Back office into group shared services | 20 | 0 | 3 | 2 | 5 | $18,075 |
| Team events, perks and wellness | Second wave | 60 | 33 | 1 | 0 | 34 | $27,912 |
| Bank, payment and certification fees | Excluded | 0 | 0 | 0 | 3 | 3 | $5,299 |
| Other cloud and IT | Second wave | 10 | 0 | 0 | 7 | 7 | $4,833 |
| Slack and Yoxel inside the Salesforce renewal | Salesforce platform agreement | 0 | 0 | 1 | 1 | 2 | $4,033 |
| Couriers and postage | Second wave | 10 | 0 | 1 | 8 | 9 | $3,100 |
| Employment-law settlement advice | Back office into group shared services | 0 | 0 | 0 | 3 | 3 | $1,930 |
| Total |  |  | 151 | 110 | 125 | 386 | $7,887,360 |

## Checks

The merge checks M1 to M7 on the batches, then `qa/check_outputs.py` on the merged file: structural checks S1 to S6, classification checks C1 to C20, the savings checks V1 to V11 once `outputs/analysis/savings.csv` exists (steps 4 and 5), and the document checks D1 to D5 and the sheet check W1 once the documents and the workbook exist (step 6).

| Check | Result | Rule |
|---|---|---|
| M1 | PASS | Batch files are named batch_NN.csv and numbered from 01 without gaps |
| M2 | PASS | Every batch has exactly the 16 columns of the classification spec, in its order |
| M3 | PASS | Every batch holds at most 40 vendors, and every batch but the last exactly 40 |
| M4 | PASS | Every row has as many fields as its batch's header |
| M5 | PASS | No vendor_id appears more than once across the batches |
| M6 | PASS | spend_12m is a finite number in every row |
| M7 | PASS | The verification reasons file has the columns vendor_id and reason, lists each vendor_id once, and each reason is one line without em or en dashes |
| S1 | PASS | Link groups are marked shared or per row; per row exactly for Amazon and Microsoft |
| S2 | PASS | Every group's rows exist and every group has names a rationale can use |
| S3 | PASS | qa/vendor_groups.csv agrees with the group definitions (decision, link recommendation) |
| S4 | PASS | Rows fixed by decisions are the vendors the decisions name |
| S5 | PASS | Taxonomy and cluster lists load (12 departments, 18 clusters) |
| S6 | PASS | Every savings assumption in docs/savings_assumptions.md carries depends_on: none, or decision names registered there; the levers named as vendor actions carry none |
| C1 | PASS | The columns of the classification spec are present |
| C2 | PASS | One row per source row (386), no duplicates, no extras |
| C3 | PASS | Departments come from docs/taxonomy.md |
| C4 | PASS | Cost clusters come from docs/clusters.md |
| C5 | PASS | Recommendations are Terminate, Consolidate or Optimize |
| C6 | PASS | is_addressable, is_recurring and verified are TRUE or FALSE; confidence is high, medium or low |
| C7 | PASS | Descriptions are one non-empty line without the banned phrases |
| C8 | PASS | Rationales are one sentence ending in a full stop |
| C9 | PASS | No em or en dash in any field |
| C10 | PASS | Total spend_12m equals the clean file's total exactly |
| C11 | PASS | Rows of each merge group and each shared link group carry one recommendation |
| C12 | PASS | Every row that is a duplicate record of one vendor (a merge group or a same-brand link group) names the other record in its rationale; rows linked only through a corporate parent need not (step 7) |
| C13 | PASS | Outcomes fixed by recorded decisions |
| C14 | PASS | Rationale, risk-note and description wording fixed by recorded decisions |
| C15 | PASS | Rows outside the savings base say "non-discretionary, no saving counted" (step 7) |
| C16 | PASS | Every Terminate and Consolidate row, and every Optimize row at or above $25,000 (step 5), has a risk_note; smaller Optimize rows have none |
| C17 | PASS | Every row is verified TRUE, or FALSE and listed with a reason under "Verification exceptions" in qa/validation_report.md; every listed id is FALSE in the file |
| C18 | PASS | vendor_name_original and vendor_name_clean match outputs/vendors_clean.csv by vendor_id, and the rows are in the original sheet order (vendor_id ascending) |
| C19 | PASS | Descriptions, rationales and risk notes never refer to the project's own workings: hints, lists, rules, searches, sources, steps, prompts or files (step 5) |
| C20 | PASS | Descriptions, rationales and risk notes are in American English: none of the common British forms (step 6) |
| V1 | PASS | pct_low <= pct_base <= pct_high on every row, all within 0 and 100 |
| V2 | PASS | pct_without_decision <= pct_base on every row, and equal to it on untagged rows |
| V3 | PASS | The year-1 saving is the base saving times a factor between 0 and 1, so never above the base |
| V4 | PASS | No saving on a row that is not addressable or in the M&A cluster |
| V5 | PASS | No saving above the row's spend, and spend is a non-negative number |
| V6 | PASS | Every row has one registered lever with the register's values, every lever is used, and the rows are the classification's rows with their spend, cluster and name |
| V7 | PASS | Every depends_on tag, on the rows and in the register, is none or a registered decision |
| V8 | PASS | The roll-ups by opportunity, cluster and lever in outputs/analysis/savings.md equal the sums of the vendor rows, and their totals equal the file's total |
| V9 | PASS | Every Terminate row on a lever with a base below 50% outside the Excluded opportunity, and every Optimize row on a lever above 50%, is fixed or has a recorded reason (step 5) |
| V10 | PASS | Every row whose saving rests on a group decision leads its rationale with the group function it moves to and gives the vendor-only fallback second (step 7) |
| V11 | PASS | Every Terminate row whose base saving is under half its spend says why in a clause: pay passed through, a processing fee, stopped until confirmed, or no saving counted (step 7) |
| D1 | PASS | Every dollar figure and percentage in the four documents appears in a file under outputs/analysis or qa (savings_summary.md first) |
| D2 | PASS | Every table with a Total row in the documents adds up |
| D3 | PASS | No project vocabulary (lever, cluster, depends_on, hint, batch) in the Top 3, the memo or the methodology |
| D4 | PASS | The four documents are in American English: none of the common British forms |
| D5 | PASS | Every calculation in the Top 3 reproduces from savings.csv: each rate of a spend names one saving line's spend to the dollar, its product is spend times rate to the dollar, and the products and the other lines add to the stated total, which rounds to the opportunity's base saving (step 9) |
| W1 | PASS | outputs/sheet/Vendor Analysis Assessment - Chaitanya Laxman.xlsx matches its sources cell by cell, keeps the raw row order and the Department dropdown, uses only Config departments, and its saving column sums to the base saving |

## Failures

None: all 50 checks passed.
