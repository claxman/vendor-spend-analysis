# Validation report

Written by `scripts/merge_validate.py`, which merged the batch files in `outputs/batches/` into `outputs/vendors_classified.csv`, sorted by `vendor_id` (the original sheet order), and ran `qa/check_outputs.py` on it. The report is rebuilt on every run and is not edited by hand: the reason for a row with `verified` FALSE goes in `qa/verification_exceptions.csv`.

**Result: PASS.** All 31 checks passed.

## Counts

| Measure | Value |
|---|---|
| Batch files merged | 10 (batch_01.csv to batch_10.csv) |
| Rows in the batches | 386 |
| Distinct vendor_ids | 386 |
| Source rows in `outputs/vendors_clean.csv` | 386 |
| Source rows in no batch | 0 |
| Total `spend_12m` | $7,887,360 (source total $7,887,360) |
| `verified` TRUE | 305 vendors, $7,687,092 (97.5% of spend) |
| `verified` FALSE | 81 vendors, $200,268 (2.5% of spend) |
| `is_addressable` TRUE | 369 vendors, $7,765,704 (98.5% of spend) |
| `is_recurring` TRUE | 270 vendors, $7,556,683 (95.8% of spend) |
| Confidence low | 101 vendors, $543,894 (6.9% of spend) |

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
| Engineering | 16 | 4.1% | $285,673 | 3.6% |
| Facilities | 51 | 13.2% | $973,386 | 12.3% |
| G&A | 221 | 57.3% | $1,714,984 | 21.7% |
| Legal | 24 | 6.2% | $197,752 | 2.5% |
| M&A | 4 | 1.0% | $226,932 | 2.9% |
| Marketing | 24 | 6.2% | $201,520 | 2.6% |
| SaaS | 9 | 2.3% | $3,442,832 | 43.6% |
| Product | 2 | 0.5% | $4,149 | 0.1% |
| Professional Services | 2 | 0.5% | $56,367 | 0.7% |
| Sales | 8 | 2.1% | $138,344 | 1.8% |
| Support | 1 | 0.3% | $178 | 0.0% |
| Finance | 24 | 6.2% | $645,242 | 8.2% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by recommendation

| Recommendation | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| Terminate | 154 | 39.9% | $707,786 | 9.0% |
| Consolidate | 108 | 28.0% | $2,519,694 | 31.9% |
| Optimize | 124 | 32.1% | $4,659,880 | 59.1% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by cost cluster

| Cost cluster | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| Salesforce platform | 5 | 1.3% | $3,382,759 | 42.9% |
| Office footprint | 10 | 2.6% | $837,043 | 10.6% |
| Office running costs | 44 | 11.4% | $71,130 | 0.9% |
| Travel and entertainment | 49 | 12.7% | $464,995 | 5.9% |
| Team events, perks and wellness | 37 | 9.6% | $81,157 | 1.0% |
| Audit, tax, accounting and corporate services | 24 | 6.2% | $590,674 | 7.5% |
| M&A and transaction costs | 4 | 1.0% | $226,932 | 2.9% |
| Legal | 19 | 4.9% | $179,798 | 2.3% |
| Insurance and benefits | 25 | 6.5% | $428,012 | 5.4% |
| Recruiting and HR outsourcing | 18 | 4.7% | $404,135 | 5.1% |
| Cloud, telecom and IT | 30 | 7.8% | $238,201 | 3.0% |
| Outsourced engineering and contractors | 8 | 2.1% | $246,157 | 3.1% |
| Software subscriptions (non-Salesforce) | 39 | 10.1% | $377,257 | 4.8% |
| Marketing agencies, media and memberships | 25 | 6.5% | $141,008 | 1.8% |
| Customer-mandated platform fees | 3 | 0.8% | $97,400 | 1.2% |
| Statutory and government | 6 | 1.6% | $15,646 | 0.2% |
| Student labour | 3 | 0.8% | $54,117 | 0.7% |
| Unidentified and individual payees | 37 | 9.6% | $50,939 | 0.6% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Distribution by confidence

| Confidence | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| high | 177 | 45.9% | $5,589,504 | 70.9% |
| medium | 108 | 28.0% | $1,753,963 | 22.2% |
| low | 101 | 26.2% | $543,894 | 6.9% |
| Total | 386 | 100.0% | $7,887,360 | 100.0% |

## Low-confidence vendors

101 vendors, $543,894 (6.9% of spend), sorted by spend, largest first.

| vendor_id | Vendor | Spend | Department | Recommendation | Description |
|---|---|---|---|---|---|
| V0009 | Weking d.o.o. | $144,093 | Engineering | Consolidate | Zagreb Salesforce and CloudSense consultancy supplying consultants and developers, per its website, most likely to product engineering; entity unconfirmed, confirm with Finance |
| V0015 | Telefonica Global Services GmbH | $89,880 | Sales | Optimize | Global procurement company of the Telefónica group in Munich, a customer's buying arm; what these payments cover is for Finance |
| V0018 | Bisley Law Ltd | $67,414 | Legal | Consolidate | UK company named as a law practice; Companies House lists it as non-trading and no source shows its work, confirm with Finance |
| V0038 | Nefron - Obrt Za Poslovne Usluge | $30,614 | G&A | Terminate | Podstrana sole trader registered to organise meetings and trade fairs; what it supplied the company is not shown, confirm with Finance |
| V0043 | Google Ireland Limited | $24,798 | Marketing | Optimize | Google's Dublin billing entity for Ads and Cloud in Europe; the product bought is not shown, most likely Google Ads, confirm with Finance |
| V0058 | Smart Group Services d.o.o. | $16,438 | G&A | Terminate | Zagreb consultancy at the address of the Smart Group HR brand (recruitment, payroll, employee leasing); the service bought is unconfirmed |
| V0065 | Pingo d.o.o. | $14,508 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, most likely a contractor, confirm with Finance |
| V0074 | Bijeli Pijesak Obrt Za Poslovno Savjetovanje | $11,605 | G&A | Terminate | Croatian sole trader whose name says business consulting; no registry entry or source shows the work, confirm with Finance |
| V0082 | Catering Muring | $9,603 | Facilities | Terminate | Caterer by its name, office catering under the taxonomy tie-break; no public source confirms the business, confirm with Finance |
| V0087 | The Guardian | $8,070 | Marketing | Optimize | UK newspaper publisher selling subscriptions, advertising and Guardian Jobs recruitment ads; which was bought is unconfirmed, for marketing or HR |
| V0092 | Obrt Sjaj Sunca | $6,596 | G&A | Terminate | Croatian sole trader in Split, by a directory snippet, whose activity no readable source shows, confirm with Finance |
| V0093 | Telefónica Compras Electrónicas S.L. | $6,157 | Sales | Optimize | Telefónica's Madrid procurement company running the group purchasing platform suppliers must use; what these payments cover is for Finance |
| V0096 | Mosaic Concept d.o.o. | $5,731 | G&A | Terminate | Zagreb micro company registered to organise meetings and business fairs; what it supplied the company is not shown, confirm with Finance |
| V0102 | Athlete Service Ltd | $5,285 | G&A | Terminate | UK cycling and triathlon retailer selling bikes, clothing and accessories, per a company-data site; what was bought is unconfirmed |
| V0106 | Centar Za Sigurnost d.o.o. | $4,991 | Facilities | Optimize | Occupational safety and fire protection services in Croatia per the hint; no public source confirms this company, confirm with Finance |
| V0107 | Profi Bar d.o.o. | $4,917 | G&A | Terminate | Croatian company whose name suggests a bar or drinks supplier; no public source shows what it provides, confirm with Finance |
| V0110 | The Virtual Legal Counsel Ltd | $4,800 | Legal | Consolidate | London company whose name suggests outsourced in-house legal counsel; registered as a management consultancy, services unconfirmed, for legal |
| V0111 | Australian Payroll Professionals Pty Ltd | $4,399 | G&A | Terminate | Payroll outsourcing for Australian staff per its name and the hint; no public source confirms the company, confirm with Finance |
| V0127 | Calm Achiever (A Unit Of Mohsin Ali Vakil) | $4,071 | G&A | Terminate | Indian sole proprietorship trading as Calm Achiever, function not evident from the name or any source, confirm with Finance |
| V0116 | Orionw LLC | $4,025 | Engineering | Consolidate | Outsourced IT and development per the hint; no public source traces Orionw LLC, confirm with Finance |
| V0129 | O'Donnell Salzano Lawyers | $3,955 | Legal | Consolidate | Law practice by its name; no public source confirms the firm, its location or services, confirm with Finance |
| V0137 | Orcola d.o.o. | $3,545 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, most likely a contractor, confirm with Finance |
| V0140 | T-Mobile | $3,357 | Facilities | Consolidate | Mobile telecom services under Deutsche Telekom's T-Mobile brand; the billing company and country are not shown, for staff lines |
| V0147 | Garaža Firule d.o.o. | $2,930 | Facilities | Optimize | Split company that court records tie to an underground garage with parking; its activity is not stated, confirm with Finance |
| V0148 | Crossland | $2,924 | G&A | Terminate | Payee name shared by many unrelated businesses, among them a solicitor and a 4imprint brand; which one is unknown, confirm with Finance |
| V0149 | It London | $2,838 | G&A | Terminate | Payee whose name suggests IT services in London; no business by this name was found, confirm with Finance |
| V0151 | Elemental Life Solutions LLP | $2,807 | G&A | Terminate | LLP whose name does not show its function and which no UK or Indian registry search found, confirm with Finance |
| V0157 | My Foodiverse LLP | $2,489 | G&A | Terminate | LLP whose name suggests a food business, not found in UK or Indian registries, confirm with Finance |
| V0160 | Stipe Piric | $2,302 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0162 | Pink Ribbon Shop | $2,251 | G&A | Terminate | Charity merchandise shop by its name, selling pink ribbon items for breast cancer charities; which shop is unknown, confirm with Finance |
| V0164 | N S Shastri And Co | $2,194 | Finance | Consolidate | Indian accounting and tax firm per the hint; no public source confirms the firm, confirm with Finance |
| V0165 | John Smith | $2,163 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0166 | Fabiola Thistlewhaite | $2,154 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0169 | George Anchor | $2,107 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0176 | Porezno Savjetništvo Tuk d.o.o. | $1,813 | Finance | Consolidate | Croatian tax advisory firm by its name and the hint; no public source confirms the company, confirm with Finance |
| V0177 | Susan Lee | $1,762 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0178 | Ansar Madovic | $1,732 | G&A | Terminate | Individual payee, likely a contractor or an expense reimbursement per the hint, paid through AP; confirm with Finance |
| V0180 | Aquila Remete d.o.o. | $1,706 | G&A | Terminate | Croatian company, possibly in Zagreb's Remete area, whose function neither its name nor any source shows, confirm with Finance |
| V0181 | Clime India Private Limited | $1,678 | G&A | Terminate | Indian company whose function no source shows; the name may be a truncation of Acclime India, confirm with Finance |
| V0182 | Golden Mean, Inc | $1,659 | G&A | Terminate | US company whose function neither its name nor any public source shows, confirm with Finance |
| V0183 | Paint & Fun Vl. Martina Milkova Nikolova | $1,654 | G&A | Terminate | Painting-party business by its name and the hint, used for team events; no source confirms it, confirm with Finance |
| V0189 | ETM Concessions Ltd | $1,419 | G&A | Terminate | UK company of the ETM Group whose activity no source states, confirm with Finance |
| V0192 | Chamiers Recreation Club | $1,338 | G&A | Terminate | Recreation club per the hint, used for team events or recreation; no source confirms it, confirm with Finance |
| V0197 | P S Recreation Club | $1,219 | G&A | Terminate | Recreation club per the hint, used for team events or recreation; no source confirms it, confirm with Finance |
| V0205 | Oladi d.o.o. | $1,064 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0208 | Lunch Nutrition d.o.o. | $1,012 | G&A | Terminate | Zagreb workplace meal service delivering balanced lunches to employees, with business accounts for employers, for staff meals |
| V0209 | Winmaxi Tours & Travels | $1,001 | G&A | Consolidate | Travel and tours business by its name, location unknown; no public source confirms it, confirm with Finance |
| V0210 | Digitalna Produkcija j.d.o.o. | $993 | Marketing | Terminate | Croatian company whose name means digital production, most likely media or content work; no source confirms it, confirm with Finance |
| V0215 | Time Out Group | $920 | G&A | Terminate | Time Out media and food-market group, paid for advertising or food at a Time Out Market; which is not shown |
| V0217 | Galop-Prijevoz d.o.o. | $908 | G&A | Terminate | Croatian company whose name means transport; no source confirms it or what it carried, confirm with Finance |
| V0219 | Urbani Eventi d.o.o. | $851 | G&A | Terminate | Croatian company whose name means urban events; no source confirms it, confirm with Finance |
| V0223 | BB Football Scouting j.d.o.o. | $823 | G&A | Terminate | Croatian company whose name suggests football scouting; no source confirms it or what it supplied, confirm with Finance |
| V0224 | Boe Croatia d.o.o. | $814 | Facilities | Optimize | Zagreb real estate company at the Zagrebtower address, most likely billing charges tied to the Zagreb office space |
| V0225 | Potomac d.o.o. | $806 | G&A | Terminate | Croatian company linked to the Croata tie and accessories brand, so probably corporate gifts; activity unconfirmed, confirm with Finance |
| V0226 | President Hotel And Tower Co., Ltd | $803 | G&A | Optimize | Hotel company by its name, most likely in Bangkok; no source confirms it, confirm with Finance |
| V0227 | Friends Sports Club | $797 | G&A | Terminate | Sports club per the hint, used for team recreation; no source confirms it, confirm with Finance |
| V0233 | Catering Ivić d.o.o. | $669 | Facilities | Terminate | Caterer by its name, for office or event catering; no source confirms the company, confirm with Finance |
| V0234 | Blink Events | $664 | G&A | Terminate | Events business by its name, location unknown; no source confirms it, confirm with Finance |
| V0235 | Grafo-Jan | $662 | Marketing | Terminate | Business whose name may suggest printing or graphics; no source confirms it under any spelling, confirm with Finance |
| V0236 | Mesa Verde | $662 | G&A | Terminate | Payee whose function neither its name nor any public source shows, confirm with Finance |
| V0244 | Oakberry Jr d.o.o. | $535 | G&A | Terminate | Zagreb company whose name matches the Oakberry acai bowl food brand; no source states its activity, confirm with Finance |
| V0253 | Streamlinereforms Inc | $483 | G&A | Terminate | US company whose function neither its name nor any public source shows, confirm with Finance |
| V0254 | Make And Grow Ltd | $483 | Engineering | Optimize | Small London company registered for software publishing and IT services; the product bought is not shown |
| V0256 | Rudan d.o.o. | $473 | G&A | Optimize | Istrian company in energy services and hotels; the AP data does not show which was bought, most likely a hotel stay |
| V0263 | Tiganda j.d.o.o. | $432 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0266 | Lancefield Bus Service | $412 | G&A | Terminate | Bus service by its name in Lancefield, Victoria, most likely transport for a team offsite; confirm with Finance |
| V0267 | Super Odredište d.o.o. | $378 | G&A | Terminate | Croatian company registered among other things to stage performances; its main activity is not shown, confirm with Finance |
| V0271 | Inicijativa Centar Za Edukaciju | $358 | G&A | Terminate | Croatian education centre by its name, most likely a training course; no source confirms it, confirm with Finance |
| V0272 | Niva Transport j.d.o.o. | $358 | G&A | Terminate | Croatian company whose name suggests transport; no source confirms it or what it carried, confirm with Finance |
| V0279 | Treci Posao d.o.o. | $307 | G&A | Terminate | Croatian company whose name means third job; no public source shows what it does, confirm with Finance |
| V0285 | Adamma Info Services Private Limited | $273 | G&A | Terminate | Indian company known only from a job listing for a verification analyst; its service is not shown, confirm with Finance |
| V0289 | Taste Of Health | $259 | G&A | Terminate | Food business by its name, location unknown; no source identifies which one, confirm with Finance |
| V0290 | Infodata | $241 | Engineering | Optimize | Zagreb firm servicing IT equipment, printers, servers and networks, used for office IT repairs |
| V0293 | Bella Operation A/S | $241 | G&A | Optimize | Copenhagen congress venue and hotel operator; whether the charge was a hotel stay or an event fee is not shown |
| V0294 | The Plant Man | $235 | Facilities | Terminate | Office plant or landscaping supplier by its name, most likely office plants; no source confirms which, confirm with Finance |
| V0295 | Media Promo Plus d.o.o. | $226 | Marketing | Terminate | Croatian company whose name suggests media and promotional work; no source confirms it, confirm with Finance |
| V0296 | Expert-Ing d.o.o. | $225 | G&A | Terminate | Croatian company whose name suggests engineering; no registry entry or source shows what it does, confirm with Finance |
| V0301 | Rishi Events And Entainment | $198 | G&A | Terminate | Events and entertainment business by its name, most likely in India; no source confirms it, confirm with Finance |
| V0302 | Kosmaz Technologies Croatia | $195 | G&A | Terminate | Payee whose name suggests a Croatian tech firm; no record of it in Croatia was found, confirm with Finance |
| V0312 | Xenon Savjetovanje d.o.o. | $164 | G&A | Terminate | Zagreb micro company registered for business and management consultancy; the advice bought is not shown |
| V0315 | Paint&Wine, Vl. Stevo Dosen | $159 | G&A | Terminate | Paint-and-wine studio by its name and the hint, used for team events; no source confirms it, confirm with Finance |
| V0317 | Advena | $154 | G&A | Terminate | Payee name shared by a UK regulatory consultancy and an Australian security firm; which one is unknown, confirm with Finance |
| V0319 | Monile j.d.o.o. | $152 | G&A | Terminate | Croatian company name shared by a menswear brand owner and a Split bar; which one is unknown, confirm with Finance |
| V0320 | Puzzle Promotion j.d.o.o. | $143 | Marketing | Terminate | Croatian company whose name suggests promotional work; no source confirms it, confirm with Finance |
| V0322 | Event Ors | $143 | G&A | Terminate | Events business by its name, matching several unrelated event firms; no source confirms which, confirm with Finance |
| V0325 | (Blank) | $137 | G&A | Terminate | Unnamed payee with no vendor name in the ledger, a control gap; nothing to search, confirm with Finance |
| V0331 | Illunis d.o.o. | $128 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0335 | Bonus Opinio d.o.o. | $120 | G&A | Terminate | Croatian company registered for publishing and online services; its actual product is not shown, confirm with Finance |
| V0338 | Soho Kitchen Ltd | $104 | Facilities | Terminate | Caterer or kitchen by its name in London; no source confirms the company, confirm with Finance |
| V0339 | Fortis Trade j.d.o.o. | $95 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0340 | Till Trade d.o.o. | $93 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0344 | Lemia d.o.o. | $88 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0346 | Meluba Limited | $88 | G&A | Terminate | UK company in Kettering whose activity no readable source shows, confirm with Finance |
| V0354 | Sportska Udruga Split | $66 | G&A | Terminate | Sports association in Split per the hint, used for team recreation; no source confirms it, confirm with Finance |
| V0358 | Platinum Office d.o.o. | $62 | Facilities | Optimize | Office supplies company per the hint, listed in a Croatian registry; what it provides is not shown, confirm with Finance |
| V0360 | New Block d.o.o. | $56 | G&A | Terminate | Croatian company whose function neither its name nor any public source shows, confirm with Finance |
| V0365 | Shilton Hospitality LLP | $55 | G&A | Optimize | Bengaluru hospitality group running business hotels, dining and catering, paid for a stay or meal |
| V0367 | Istra Wine | $53 | G&A | Terminate | Wine seller by its name, most likely Istrian wine bought as gifts; no source confirms it, confirm with Finance |
| V0373 | Livingstone | $41 | G&A | Terminate | Payee name shared by many unrelated businesses, possibly an Australian office supplies distributor; confirm with Finance |
| V0382 | Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos | $20 | G&A | Optimize | Croatian occupational and sports medicine practice, by its name and the hint, for statutory staff examinations; confirm with Finance |
| V0383 | Specijalisticka Ordinacija Medicine Rada Helena Blazic | $20 | G&A | Optimize | Croatian occupational medicine practice, by its name and the hint, for statutory staff examinations; confirm with Finance |

## Verification exceptions

Every row with `verified` FALSE, by `vendor_id`, with a one-line reason, as kept in `qa/verification_exceptions.csv`. Check C17 compares this list with the `verified` column, both ways.

- V0018: Companies House lists Bisley Law Limited as a non-trading company and no website or SRA record describes its services
- V0065: no company named Pingo d.o.o. was found in Croatian registries or elsewhere after three searches
- V0074: no registry entry or other source was found for the sole trader after three searches
- V0082: two searches found no business named Catering Muring
- V0092: a directory snippet places a sole trader of this name in Split, but no readable source shows its activity
- V0106: no company named Centar za sigurnost d.o.o. was found in Croatian registries after two searches
- V0107: no company named Profi Bar d.o.o. was found after two searches
- V0111: no company or business name was found in search results or in four ABN register records
- V0116: no company named Orionw LLC was found after two searches
- V0127: individual payee (a sole proprietorship) with no business record to verify against after two searches
- V0129: two searches found no law firm named O'Donnell Salzano
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
- V0176: no company named Porezno Savjetništvo Tuk d.o.o. was found in Croatian directories after two searches
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
- V0210: no company named Digitalna Produkcija j.d.o.o. was found in Croatian registries after two searches
- V0217: no company named Galop-Prijevoz d.o.o. was found in Croatian registries after two searches
- V0219: no company named Urbani Eventi d.o.o. was found in Croatian registries after two searches
- V0223: no company named BB Football Scouting j.d.o.o. was found after two searches
- V0225: a Lider Media article ties it to the Croata brand but no source states what it does
- V0226: two searches and a page fetch found no company of this name
- V0227: no club named Friends Sports Club was found after two searches
- V0233: no company named Catering Ivić d.o.o. was found after two searches
- V0234: no business named Blink Events was found after two searches
- V0235: no business named Grafo-Jan was found under any spelling after two searches
- V0236: no business named Mesa Verde was found in Zagreb or Chennai after two searches
- V0244: a directory lists the company in Zagreb but no source states what it does
- V0253: no company named Streamlinereforms Inc or Streamline Reforms was found after two searches
- V0263: no registry entry or website for Tiganda j.d.o.o. was found after two searches
- V0266: no business named Lancefield Bus Service was found; results were only public bus route news
- V0267: the company appears on a paywalled registry page that does not show its main activity
- V0271: no organisation named Inicijativa Centar Za Edukaciju was found after two searches
- V0272: no registry entry or website for Niva Transport j.d.o.o. was found after two searches
- V0279: no registry entry or website for Treci Posao d.o.o. was found after two searches, with and without diacritics
- V0285: two searches found only a job listing and no registry record or description of the business
- V0289: the generic name matched only unrelated food businesses after two searches
- V0294: two possible UK businesses match the name but neither is confirmed
- V0295: no company named Media Promo Plus d.o.o. was found after two searches
- V0296: no registry or website record for Expert-Ing d.o.o. was found after two searches
- V0301: no business matching Rishi Events And Entainment was found after two searches
- V0302: no registry entry, website or other record for Kosmaz Technologies in Croatia was found after two searches
- V0315: no business trading as Paint&Wine was found after two searches by its trading name
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
- V0358: a paywalled registry listing names the company but no readable source shows what it provides
- V0360: no registry entry, website or other record for New Block d.o.o. was found after two searches
- V0367: no business trading as Istra Wine was found after two searches
- V0373: several unrelated businesses share the name and nothing ties one to this payee
- V0382: no web record of the practice was found after two searches
- V0383: no web record of the practice was found after two searches

## Checks

The merge checks M1 to M7 on the batches, then `qa/check_outputs.py` on the merged file: structural checks S1 to S6 and classification checks C1 to C18.

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
| C12 | PASS | Every grouped row's rationale names its group (per-row links included) |
| C13 | PASS | Outcomes fixed by recorded decisions |
| C14 | PASS | Rationale, risk-note and description wording fixed by recorded decisions |
| C15 | PASS | Rows outside the savings base say "non-discretionary, excluded from the savings base" |
| C16 | PASS | Every Terminate and Consolidate row has a risk_note; Optimize rows have none, except V0002 (step 3b) |
| C17 | PASS | Every row is verified TRUE, or FALSE and listed with a reason under "Verification exceptions" in qa/validation_report.md; every listed id is FALSE in the file |
| C18 | PASS | vendor_name_original and vendor_name_clean match outputs/vendors_clean.csv by vendor_id, and the rows are in the original sheet order (vendor_id ascending) |

## Failures

None: all 31 checks passed.
