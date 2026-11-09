# Forensic pass: vendor_analysis_assessment.xlsx

Generated 2026-11-10 by `scripts/01_forensics.py`. The workbook was opened read-only; its SHA-256 was `5473deb2fcb040a8ee5d54f91c9b1bca6467afc24839695fbd522fb414318a30` before and after the run. Nothing is classified here: departments, descriptions and recommendations come later. Vendor names are shown with the mojibake repaired; `vendor_id` is `V` plus the source row number. Total spend in the file: $7,887,360 across 386 rows.

## Summary

- **Structure is clean.** Nothing hidden, no comments, no conditional formats, no formulas, nothing outside A1:E387; the only validation is the Department dropdown. One hidden built-in name exists for the AutoFilter. Section 1.
- **Identical amounts are not duplicate payments.** 23 groups (51 rows) share a cost to every decimal, but they are unrelated payees on adjacent rows, the largest $2,838, and the amounts sit on a discrete grid left by the cost modification. Section 2.
- **Decimals mean nothing.** No round numbers at all; precision changes block by block with the cost modification. Quote whole dollars. Section 3.
- **First digits conform** to Benford's law (acceptable conformity, p = 0.18). Section 4.
- **Row order is not a rank.** The sheet is 3 sorted blocks end to end. Section 5.
- **14 entity merges** (30 rows) give 370 vendors; Navan, already second, grows to $415,913 across its old and new names. Six parent links (Slack under Salesforce, Trello under Atlassian, and others) are kept as links, not merges. Section 6.
- **Customer-mandated payees:** Telefónica's two procurement entities and SAP Ariba, $97,400. Non-discretionary; confirm what the Telefónica payments are. Bupa and StarHub carry a Supplier tag and may also be customers. Sections 7.8 and 8.
- **Savings base:** $121,657 of statutory and customer-mandated spend is excluded. Section 10.
- **Unidentified payees:** 69 names, $472,522 (6.0% of spend), led by Weking d.o.o. at $144,093. Sections 7.10 and 8.
- **Consumer and retail purchases:** 56 vendors, $83,926; a card and expense policy issue, not a negotiation. Section 7.2.
- **Salesforce is 39.5% of spend** and the file does not say what the contract covers. Section 8.

## 1. Workbook structure

Re-verified with openpyxl and, for what openpyxl does not surface, the raw package XML. The separate structure audit is confirmed in the addendum of `00_data_profile.md`; this table adds the remaining checks.

| Check | Result | Implication |
|---|---|---|
| Hidden or very hidden sheets | none; 5 of 5 visible in openpyxl and workbook.xml | nothing hidden to recover |
| Hidden rows and columns | none on any sheet; no zero-height rows, zero-width columns or outline groups; AutoFilter `$A$1:$O$387` has 0 criteria | all 386 vendor rows are visible; the row count is complete for this file |
| Cell notes and comments | 0 notes; 0 comment parts; persons list empty | no reviewer context to use |
| Defined names | 0 user-defined; built-in only: `_xlnm._FilterDatabase` (hidden, 'Vendor Analysis Assessment'!$A$1:$O$387) | no named range feeds a hidden calculation |
| Conditional formats | 0 rules; 0 in the XML, extension list included | no colour-coded flags to interpret |
| White-on-white or hidden text | 0 cells; white text only in header cells (`Vendor Analysis Assessment` A1:E1; `Top 3 Opportunities` B1:C1; `Methodology` A1; `CEOCFO Recommendations` A1), all on fill FF073763 (dark blue); 0 cells with a `;;;` format; smallest font 8 pt | no hidden content |
| Data validation, column by column | B: list from `Config!$A$2:$A814`, blanks allowed, error alert on; none on A, C, D, E, F, G, H, I, J, K, L, M, N, O; 0 x14 extension rules; no rules on the other 4 sheets | Department values must match `Config` character for character; Description and Suggestions are free text |
| Columns F to O and rows 388 to 814 | no values, formulas, comments, hyperlinks or merged cells; 3,870 and 6,405 cells carry styles only (borders, fonts, number formats) | nothing outside A1:E387 to analyse |
| Formulas | 0 in the workbook | every cost is a typed value, not a calculation |
| Other objects | 1 hyperlink (A203 to http://amazon.co.uk); 0 images; 0 charts; 5 drawing parts, 0 with content; 0 merged cells; sheet protection on 0 sheets | harmless; the link is the cell's own text |
| Shared strings | 410 strings, 0 not used by any cell | no leftover text from deleted cells |
| Package contents | macros 0, external links 0, pivot caches 0, embedded objects 0, custom XML 0, document properties 0 | no external dependencies; author and dates are not recorded in the file |
| Origin | Google Sheets export: no document properties, Sheets default column width 12.63 and row height 15.75, empty drawing parts | the 814-row by 15-column grid is a Sheets grid size; see section 8 |

## 2. Identical amounts

23 groups of rows share an identical cost, to the cent and in fact to every stored decimal: 51 rows in all. Every group sits on consecutive rows of the sorted sheet (confirmed), the largest amount is $2,838, and with one exception the payees in a group are unrelated (a kitchen and the Australian tax office; an SMS API, a print shop and a hospitality firm).

| # | Amount | Rows | Vendors |
|---|---|---|---|
| 1 | $2,838.04 | 149, 150 | It London; Terrapinn Holdings Ltd |
| 2 | $1,654.46 | 183, 184 | Paint & Fun Vl. Martina Milkova Nikolova; Carrington Communications |
| 3 | $681.20 | 230, 231 | Klg - Kalra Legal Group; Kilgannon & Partners Llp |
| 4 | $662.47 | 235, 236 | Grafo-Jan; Mesa Verde |
| 5 | $482.80 | 253, 254 | Streamlinereforms Inc; Make And Grow Ltd |
| 6 | $472.58 | 256, 257 | Rudan D.O.O.; Entrio Tehnologije D.O.O. |
| 7 | $378.07 | 267, 268 | Super Odredište D.O.O.; Pmi Global Operations Center |
| 8 | $357.63 | 271, 272 | Inicijativa Centar Za Edukaciju; Niva Transport J.D.O.O. |
| 9 | $263.11 | 287, 288 | Stillmark Zagreb D.O.O.; Lastpass Ireland Limited |
| 10 | $183.37 | 306, 307 | Zettanet; Hahn Air |
| 11 | $153.89 | 317, 318 | Advena; Hrvatski Nezavisnici Izvoznici Softvera |
| 12 | $142.83 | 320, 321, 322 | Puzzle Promotion J.D.O.O.; Zagrebački Holding D.O.O.; Event Ors |
| 13 | $130.85 | 327, 328 | Fero-Term; Ustanova Za Zdravstvenu Skrb P.P. |
| 14 | $122.56 | 332, 333 | The Cook Kitchen; Australian Taxation Office (Ato) |
| 15 | $119.79 | 334, 335 | Capitol Services; Bonus Opinio D.O.O. |
| 16 | $118.87 | 336, 337 | Dhl Express (Uk) Ltd; Kat'S Kitchen D.O.O. |
| 17 | $89.38 | 342, 343 | Axil Coffee Roasters; Pepco Croatia D.O.O. |
| 18 | $87.54 | 344, 345, 346 | Lemia D.O.O.; Retriever Llc; Meluba Limited |
| 19 | $61.74 | 357, 358 | Wolt Enterprises Oy; Platinum Office D.O.O. |
| 20 | $56.21 | 360, 361, 362 | New Block D.O.O.; Cayman Islands Government; Officeworks |
| 21 | $55.29 | 363, 364, 365 | Click Send Pty Ltd; Kall Kwik Centre 565; Shilton Hospitality Llp |
| 22 | $49.76 | 369, 370 | Pan-Pek D.O.O.; Uber *Eats |
| 23 | $20.27 | 382, 383, 384 | Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos; Specijalisticka Ordinacija Medicine Rada Helena Blazic; Ustanova Za Medicinu Rada I Sporta Dr. Novacki |

Why these are not duplicate payments: 33 pairs of rows are within half a cent of each other, and widening the window a hundredfold, to 50 cents, adds only 1 more. If amounts were spread continuously, near misses would outnumber exact matches by about a hundred to one. Here exact matches are almost the only close pairs, so the amounts sit on a discrete grid. That is the pattern left when amounts recorded in whole units are multiplied by a common factor: two small amounts that were equal stay equal after scaling, and the many small vendors make such collisions common. The brief says costs were modified; this is consistent with that. No attempt is made to reverse the modification, because the data owner applied it on purpose and the analysis does not need it.

The one group that may be a genuinely identical price is the three Croatian occupational-medicine providers at $20.27 each, which plausibly charge the same fee for the statutory medical examination.

- Implication for classification: none. Every row stays, with its own cost.
- Implication for the memo: the file cannot support a duplicate-payment finding either way. If the CFO wants one, it needs invoice-level data (invoice number, date, amount, payee bank account). The methodology should say the ties were tested and explained.

## 3. Cost precision and round numbers

No cost is a whole dollar (0) or a whole cent (0). After rounding away binary floating-point noise, the stored precision ranges from 4 to 9 decimal places: 4 places: 8, 5 places: 19, 6 places: 88, 7 places: 183, 8 places: 29, 9 places: 59.

The precision is not random. It changes exactly where the sheet's sort order breaks (section 5):

| Rows | Vendors | Cost range | Decimal places (count) | 7th decimal digit |
|---|---|---|---|---|
| 2 to 125 | 124 | $3,117,226 to $3,535 | 4: 3, 5: 4, 6: 22, 7: 95 | always even (0, 2, 4, 6 or 8) |
| 126 to 291 | 166 | $4,078 to $233 | 4: 5, 5: 15, 6: 66, 7: 80 | always 0 or 5 |
| 292 to 387 | 96 | $248 to $18 | 7: 8, 8: 29, 9: 59 | any digit |

A 7th decimal that is always even in one block and always 0 or 5 in the next cannot come from invoices. It is the fingerprint of the modification, applied block by block with different settings. The round-versus-precise split therefore means nothing about vendors: not estimates against invoices, not currency, not accruals.

Round-number check. Costs of $100 or more within 50 cents of a round hundred: 8 of 337, against about 3.4 expected by chance (Poisson probability of 8 or more: 0.02). Costs of $1,000 or more within $5 of a round thousand: 1 of 208, against about 2.1 expected. The first is a weak excess that may mean a handful of originals were round contract prices; it cannot be used for anything.

| Row | Vendor | Cost |
|---|---|---|
| 10 | Jensten Insurance Brokers | $142,699.73 |
| 47 | Bupa- Supplier | $22,799.78 |
| 57 | Benefit Systems D.O.O. | $16,900.22 |
| 78 | Shoff Darby Companies | $10,100.47 |
| 110 | The Virtual Legal Counsel Ltd | $4,800.30 |
| 120 | Zivi Napitak D.O.O. | $3,699.58 |
| 130 | Papertrail Inc | $3,899.86 |
| 142 | Bureau Veritas Croatia D.O.O. | $3,199.93 |

- Implication for classification: none.
- Implication for the memo: quote whole dollars or thousands, never cents; state once that the figures are the file's modified values. Shares and rankings inside the file are internally consistent, which is all the analysis needs.

## 4. First-digit distribution

| First digit | Vendors | Observed | Benford expectation | Difference |
|---|---|---|---|---|
| 1 | 118 | 30.6% | 30.1% | +0.5 pts |
| 2 | 65 | 16.8% | 17.6% | -0.8 pts |
| 3 | 57 | 14.8% | 12.5% | +2.3 pts |
| 4 | 38 | 9.8% | 9.7% | +0.2 pts |
| 5 | 36 | 9.3% | 7.9% | +1.4 pts |
| 6 | 26 | 6.7% | 6.7% | +0.0 pts |
| 7 | 9 | 2.3% | 5.8% | -3.5 pts |
| 8 | 22 | 5.7% | 5.1% | +0.6 pts |
| 9 | 15 | 3.9% | 4.6% | -0.7 pts |

Chi-square 11.39 on 8 degrees of freedom, p = 0.18; mean absolute deviation 0.0109, which is acceptable conformity on Nigrini's first-digit scale. The largest gap is the digit 7 (fewer vendors than expected), within what a sample of this size produces.

Benford's law is scale-invariant, so multiplying blocks of costs by constants does not disturb it, and annual totals per vendor are sums of many invoices, which tend to conform anyway. Conformity here is therefore expected and proves little.

- Implication for classification: none.
- Implication for the memo: nothing to report. Fraud or error testing needs invoice-level data.

## 5. Row order

The sheet looks sorted by cost, largest first, but it is 3 separately sorted blocks placed end to end. Inside each block the order is strictly non-increasing; at each boundary the cost jumps up:

| Boundary (rows) | Last cost of the block above | First cost of the block below |
|---|---|---|
| 125 to 126 | $3,535 | $4,078 |
| 291 to 292 | $233 | $248 |

Removing 13 rows would make the whole sheet sorted (rows 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 290, 291). They are the rows where neighbouring blocks overlap in value at the two boundaries, which is what joining separately sorted blocks produces; nothing points to rows edited one by one. The boundaries coincide with the precision changes in section 3, so the blocks are where the modification settings changed.

- Implication for classification: none.
- Implication for the memo: rank vendors by cost, never by row number; near the two boundaries a vendor on a lower row can cost more than one above it.

## 6. Near-duplicate names

Method: the matching key from `00_data_profile.md` (mojibake repaired, accents stripped, lower case, legal forms, geography, stop words and the Supplier tag removed), searched in three tiers. Tier 1: same key (4 groups). Tier 2: similar spelling, a token subset, or two shared tokens covering half the shorter key (19 pairs). Tier 3: same first token where a pair was not already flagged (9 groups). Every candidate has a recorded verdict; the script stops if one does not.

| Tier | Rows and names | Verdict | Reason |
|---|---|---|---|
| 1: same key | 14 Amazon Web Services Llc; 103 Amazon Web Services Inc. | merge into AWS | Amazon Web Services billed through its LLC and its Inc entity |
| 1: same key | 47 Bupa- Supplier; 71 Bupa Australia | merge into Bupa | two Bupa entities: one tagged Supplier in the source, the other Bupa Australia |
| 1: same key | 172 Apple Pty Ltd; 229 Apple - Amer | merge into Apple | Apple billed through UK retail, Australian, Irish distribution and Americas entities |
| 1: same key | 203 Amazon.Co.Uk; 291 Amazon (Aus) | merge into Amazon (retail) | Amazon consumer marketplace in the UK and Australia; kept apart from AWS, a different service |
| 2: token subset | 3 Navan (Tripactions Inc); 24 Navan, Inc | merge into Navan | TripActions Inc renamed itself Navan Inc in 2023; both rows are the same travel and expense platform |
| 2: token subset | 14 Amazon Web Services Llc; 103 Amazon Web Services Inc.; 203 Amazon.Co.Uk; 291 Amazon (Aus) | same parent, different service | AWS (cloud) and the Amazon marketplace are different services; linked through parent_company only |
| 2: similar spelling | 16 Hr Solution International Gmbh; 90 Hrsolution International Ag | merge into HR Solution International | same brand billed through a GmbH and an AG |
| 2: similar spelling | 25 Tmforum; 249 Tm Forum | merge into TM Forum | Tmforum and Tm Forum are two spellings of the same association |
| 2: token subset | 30 Sveučilište U Zagrebu, Studentski Centar; 86 Studentski Centar - Split | different vendors, same type | three different university student centres (Zagreb, Split, Karlovac) offering the same student-work service |
| 2: shared tokens | 30 Sveučilište U Zagrebu, Studentski Centar; 186 Studentski Centar Karlovac | different vendors, same type | three different university student centres (Zagreb, Split, Karlovac) offering the same student-work service |
| 2: token subset | 73 Grad Zagreb, Gradski Ured Za Prostorno Uređenje,..; 139 Grad Split | different vendors | two different cities (Zagreb, Split) |
| 2: shared tokens | 88 Intertrust Singapore Corporate Services Pte Ltd - Csc; 99 Acclime Corporate Services | different vendors, same type | Intertrust and Acclime both sell corporate secretarial services; only the words Corporate Services are shared |
| 2: shared tokens | 74 Bijeli Pijesak Obrt Za Poslovno Savjetovanje; 330 Teb Poslovno Savjetovanje D.O.O. | different vendors | unrelated firms whose names both contain poslovno savjetovanje (business consulting) |
| 2: token subset | 99 Acclime Corporate Services; 105 Acclime Usa, Inc | merge into Acclime | Acclime billed through its corporate services entity and its US entity |
| 2: token subset | 86 Studentski Centar - Split; 186 Studentski Centar Karlovac | different vendors, same type | three different university student centres (Zagreb, Split, Karlovac) offering the same student-work service |
| 2: token subset | 94 Allianz Australia Workers' Compensation (Victoria) Limited; 212 Allianz Wa | merge into Allianz Australia | Allianz workers' compensation in Victoria and, by the Wa suffix, Western Australia |
| 2: token subset | 123 Apple Retail Uk Ltd; 172 Apple Pty Ltd; 229 Apple - Amer | merge into Apple | Apple billed through UK retail, Australian, Irish distribution and Americas entities |
| 2: token subset | 172 Apple Pty Ltd; 175 Apple Distribution International Ltd; 229 Apple - Amer | merge into Apple | Apple billed through UK retail, Australian, Irish distribution and Americas entities |
| 2: shared tokens | 171 Grt Hotels And Resorts P Ltd; 190 Radisson Grt - Unit Of Hotels & Resorts Pvt Ltd | merge into GRT Hotels & Resorts | the Radisson row names itself a unit of GRT Hotels & Resorts |
| 2: shared tokens | 192 Chamiers Recreation Club; 197 P S Recreation Club | different vendors, same type | two different recreation clubs |
| 2: token subset | 303 Dhl; 336 Dhl Express (Uk) Ltd | merge into DHL | DHL billed with and without the DHL Express (UK) entity name |
| 2: token subset | 348 Hilton Garden Inn - Zagreb City Hotels D.O.O.; 372 Garden City D.O.O. | different vendors | share only the words Garden and City |
| 2: shared tokens | 382 Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos; 383 Specijalisticka Ordinacija Medicine Rada Helena Blazic | different vendors, same type | two occupational-medicine practices run by different doctors |
| 3: same first token `telefonica` | 15 Telefonica Global Services Gmbh; 93 Telefónica Compras Electrónicas S.L. | merge into Telefónica | two Telefónica group entities (Global Services GmbH, Compras Electrónicas S.L.) |
| 3: same first token `4i` | 17 4I Advisory Services; 72 4I Management Consulting Private Limited | merge into 4i | shared and unusual 4i brand, both advisory or consulting in India; confirm the two firms are related |
| 3: same first token `new` | 46 New Star Networks(Nsn); 360 New Block D.O.O. | different vendors | share only the word New |
| 3: same first token `hrvatski` | 53 Hrvatski Telekom D.D.; 318 Hrvatski Nezavisnici Izvoznici Softvera | different vendors | share only Hrvatski (Croatian) |
| 3: same first token `catering` | 82 Catering Muring; 233 Catering Ivić D.O.O. | different vendors, same type | two different caterers |
| 3: same first token `apple` | 123 Apple Retail Uk Ltd; 172 Apple Pty Ltd; 175 Apple Distribution International Ltd; 229 Apple - Amer | merge into Apple | Apple billed through UK retail, Australian, Irish distribution and Americas entities |
| 3: same first token `paint` | 183 Paint & Fun Vl. Martina Milkova Nikolova; 315 Paint&Wine, Vl. Stevo Dosen | different vendors, same type | two painting-event sole traders with different owners |
| 3: same first token `hotel` | 247 Hotel Zonar; 304 Hotel Laguna D.D. | different vendors, same type | two different hotels |
| 3: same first token `ustanova` | 328 Ustanova Za Zdravstvenu Skrb P.P.; 384 Ustanova Za Medicinu Rada I Sporta Dr. Novacki | different vendors, same type | two different health institutions |

Links that string matching cannot find, from knowledge of the vendors:

| Rows and names | Treatment | Confidence | Reason |
|---|---|---|---|
| 54 Sodexo Svc India Private Limited; 128 Pluxee India Private Limited | merge into Pluxee India | medium | Sodexo SVC India, the Indian meal-benefits entity, was renamed Pluxee India around the 2024 Sodexo demerger; confirm with Finance |
| 2 Salesforce Uk Ltd-Uk; 173 Slack Technologies Limited | keep separate; parent Salesforce | high | Slack has been a Salesforce company since 2021, so it can be negotiated with the Salesforce renewal |
| 91 Trello; 297 Atlassian Pty Ltd | keep separate; parent Atlassian | high | Trello is an Atlassian product |
| 130 Papertrail Inc; 311 Solarwinds, Inc | keep separate; parent SolarWinds | high | Papertrail is a SolarWinds product |
| 26 Linkedin Ireland Limited; 81 Microsoft Ireland Operations Limited; 125 Npm Inc | keep separate; parent Microsoft | high | LinkedIn and npm (through GitHub) are Microsoft companies |
| 95 Icici Lombard Gic Ltd; 143 Cici Prudential Life Insurance Co. Ltd. | keep separate; parent ICICI group | high | ICICI Lombard (general insurance) and ICICI Prudential (life insurance) are separate ICICI group insurers |
| 14 Amazon Web Services Llc; 103 Amazon Web Services Inc.; 203 Amazon.Co.Uk; 291 Amazon (Aus) | keep separate; parent Amazon | high | AWS and the Amazon marketplace share a parent but are different services |

Result: 14 merge groups covering 30 rows, so 386 rows become 370 vendors. Combined spend of each group:

| Vendor after merge | Rows | Combined 12-month cost | Confidence |
|---|---|---|---|
| Navan | 3, 24 | $415,913 | high |
| AWS | 14, 103 | $111,552 | high |
| Telefónica | 15, 93 | $96,037 | high |
| HR Solution International | 16, 90 | $87,810 | high |
| 4i | 17, 72 | $83,978 | medium |
| TM Forum | 25, 249 | $58,070 | high |
| Bupa | 47, 71 | $35,263 | high |
| Pluxee India | 54, 128 | $21,804 | medium |
| Acclime | 99, 105 | $10,408 | high |
| Apple | 123, 172, 175, 229 | $8,256 | high |
| Allianz Australia | 94, 212 | $7,069 | medium |
| GRT Hotels & Resorts | 171, 190 | $3,437 | medium |
| Amazon (retail) | 203, 291 | $1,340 | high |
| DHL | 303, 336 | $310 | high |

- Implication for classification: merged rows are classified once, as one vendor, and the rationale names the entity to keep ("same vendor is paid through more than one entity"). Parent links do not merge vendors; they let a recommendation name the parent agreement (for example Slack inside the Salesforce renewal). Same-type vendors that are not merged (student centres, clinics, hotels, corporate secretaries) are consolidation questions for the classification step.
- Implication for the memo: the vendor count is 370, not 386. Navan, already second, grows from $357,984 to $415,913; Telefónica, HR Solution and 4i each exceed $80,000 once their entities are combined. Totals by vendor should always use the merged view.

## 7. Payee types

Flags describe what a vendor's name shows; they are not departments, and a vendor can carry several. Each subgroup is a pattern with an expected match count that the script checks. Full list, one row per vendor and flag: `outputs/analysis/01_forensic_flags.csv`.

### 7.1 Individuals and owner-named businesses

19 vendors, $71,092 (0.9% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Bare personal name | 6 | $12,220 | a given name and a surname with no business word or legal form | V0160 Stipe Piric ($2,302); V0165 John Smith ($2,163); V0166 Fabiola Thistlewhaite ($2,154); V0169 George Anchor ($2,107); V0177 Susan Lee ($1,762); V0178 Ansar Madovic ($1,732) |
| Single surname-like word | 2 | $2,965 | one surname-like word; a person cannot be told apart from a business | V0148 Crossland ($2,924); V0373 Livingstone ($41) |
| Business carrying its owner's name | 6 | $5,946 | vl. (vlasnik, owner), a unit of a named person, or a medical practice named after its doctor | V0127 Calm Achiever(A Unit Of Mohsin Ali Vakil) ($4,071); V0183 Paint & Fun Vl. Martina Milkova Nikolova ($1,654); V0315 Paint&Wine, Vl. Stevo Dosen ($159); V0382 Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos ($20); V0383 Specijalisticka Ordinacija Medicine Rada Helena Blazic ($20); V0384 Ustanova Za Medicinu Rada I Sporta Dr. Novacki ($20) |
| Croatian sole trader (obrt) | 5 | $49,961 | obrt is a Croatian sole-trader business owned by one person | V0038 Nefron - Obrt Za Poslovne Usluge ($30,614); V0074 Bijeli Pijesak Obrt Za Poslovno Savjetovanje ($11,605); V0092 Obrt Sjaj Sunca ($6,596); V0240 Trans-Agram Obrt Za Dostavu ($581); V0243 Obrt Za Ugostiteljstvo Mirakul ($565) |

- Implication for classification: The six bare personal names go to G&A with confidence low, per the analyst hint; their descriptions can say only that the payee is an individual and the purpose is not stated. Owner-named businesses are classified by what the business does (painting events, occupational medicine), not as individuals. Obrt rows are one-person businesses: where they supply labour they belong with contractors.
- Implication for the memo: Payments to individuals through accounts payable are a control point (contractor status, reimbursements booked as vendor spend), not a savings line; the amount is small.

### 7.2 Consumer or retail purchases

56 vendors, $83,926 (1.1% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Apple | 4 | $8,256 | Apple retail or Apple regional entities; may be employee IT equipment | V0123 Apple Retail Uk Ltd ($3,548); V0172 Apple Pty Ltd ($2,031); V0175 Apple Distribution International Ltd ($1,913); V0229 Apple - Amer ($764) |
| Amazon marketplace | 2 | $1,340 | Amazon consumer marketplace in the UK and Australia | V0203 Amazon.Co.Uk ($1,107); V0291 Amazon (Aus) ($233) |
| Supermarkets and food retail | 4 | $16,061 | supermarket chains in Croatia, Australia and the UK | V0061 Konzum Plus D.O.O. ($15,684); V0274 Spar Hrvatska D.O.O. ($341); V0385 M&S Simply Food ($19); V0387 Coles ($18) |
| General, electronics and online retail | 11 | $7,408 | high-street or online retailers, a pharmacy and a photo shop | V0136 Ikea Hrvatska D.O.O. ($3,610); V0162 Pink Ribbon Shop ($2,251); V0207 Müller Trgovina Zagreb D.O.O. ($1,051); V0314 Notino S.R.O. ($161); V0343 Pepco Croatia D.O.O. ($89); V0359 Snappy Snaps ($59); V0362 Officeworks ($56); V0374 Ekupi D.O.O. ($40); V0375 Farmacia - Specijalizirana Prodavaonica D.O.O. ($36); V0378 Currys Pc World ($30); V0380 Sport Vision D.O.O. ($26) |
| Restaurants, cafes, bakeries, caterers and food delivery | 25 | $25,608 | food or drink in the name, or a known food brand | V0082 Catering Muring ($9,603); V0101 Tattu Manchester Limited ($5,366); V0157 My Foodiverse Llp ($2,489); V0159 City Pantry Ltd ($2,419); V0208 Lunch Nutrition D.O.O. ($1,012); V0233 Catering Ivić D.O.O. ($669); V0243 Obrt Za Ugostiteljstvo Mirakul ($565); V0244 Oakberry Jr D.O.O. ($535); V0246 Magic Mountain Saloon ($524); V0258 Vivat Fina Vina D.O.O. ($467); V0275 Pepe'S Italian And Liquor ($339); V0280 Gaucho Restaurants ($302); V0286 The Riding House Cafe ($265); V0289 Taste Of Health ($259); V0332 The Cook Kitchen ($123); V0337 Kat'S Kitchen D.O.O. ($119); V0338 Soho Kitchen Ltd ($104); V0341 Pret A Manger ($92); V0342 Axil Coffee Roasters ($89); V0357 Wolt Enterprises Oy ($62); V0367 Istra Wine ($53); V0369 Pan-Pek D.O.O. ($50); V0370 Uber *Eats ($50); V0376 Cupcake Central (Life Is Sweet Bakery) ($35); V0386 Bakemono Bakers Melbourne ($18) |
| Gifts and flowers | 3 | $474 | flower delivery, gift cards and hampers | V0292 Regency Hampers Ltd ($248); V0313 Floom Ltd ($162); V0355 Prezzee ($64) |
| Gyms, sports cards and recreation clubs | 7 | $24,778 | gym, fitness studio or sports club in the name; Benefit Systems sells the MultiSport card (analyst hint) | V0057 Benefit Systems D.O.O. ($16,900); V0121 Gym4You D.O.O. ($3,692); V0192 Chamiers Recreation Club ($1,338); V0197 P S Recreation Club ($1,219); V0227 Friends Sports Club ($797); V0228 The Cycle Gap Adyar ($765); V0354 Sportska Udruga Split ($66) |

Streaming and consumer media subscriptions: none found (no Netflix, Spotify, Disney, YouTube, Apple TV or similar names).

- Implication for classification: Retail rows split by what was bought: Apple and electronics as employee IT equipment (G&A), groceries and office supplies (Facilities), restaurants and food delivery (G&A, travel and entertainment), gifts (G&A), gyms and sports cards (G&A, benefits). No streaming or consumer media subscriptions appear in the file.
- Implication for the memo: Many small rows and little money: the fix is a purchasing-card and expense policy, not a vendor negotiation. It belongs in the memo as one line on tail spend, if at all.

### 7.3 Government, tax, court and regulator payees

13 vendors, $74,991 (1.0% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Tax authority | 1 | $123 | the Australian Taxation Office | V0333 Australian Taxation Office (Ato) ($123) |
| Government and municipal bodies | 3 | $15,175 | a national government and two Croatian cities (grad means city) | V0073 Grad Zagreb, Gradski Ured Za Prostorno Uređenje,.. ($11,637); V0139 Grad Split ($3,483); V0361 Cayman Islands Government ($56) |
| Regulators and statutory schemes | 3 | $1,499 | Ico, presumably the UK data-protection regulator (ICO); the NSW workers' insurance agency (icare); India's securities depository (NSDL) | V0201 Icare Nsw ($1,150); V0284 National Securities Depository Limited(Nsdl) ($281); V0353 Ico ($67) |
| Public institutions | 4 | $54,316 | university student centres and a public health institute | V0030 Sveučilište U Zagrebu, Studentski Centar ($44,299); V0086 Studentski Centar - Split ($8,269); V0186 Studentski Centar Karlovac ($1,549); V0300 Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar ($199) |
| Publicly owned utilities | 2 | $3,878 | the City of Zagreb's utility holding company and the state power group's electricity supplier | V0119 Hep Elektra D.O.O. ($3,735); V0321 Zagrebački Holding D.O.O. ($143) |

Courts: none found.

- Implication for classification: Tax, government, regulator and statutory-scheme payees are non-discretionary: Optimize with the rationale "non-discretionary, excluded from the savings base"; ICO is data-protection registration (Legal). Two subgroups are not statutory despite public ownership: the student centres invoice student work, which is a labour decision, and the publicly owned utilities are ordinary utility bills (Facilities). No court payees appear.
- Implication for the memo: Only the statutory payees leave the savings base (total in section 10). Two items need an explanation from Finance: the City of Zagreb spatial planning office payment (large for a tenant) and the Cayman Islands Government payment (it implies a Cayman entity in the group structure).

### 7.4 Memberships and associations

11 vendors, $63,294 (0.8% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Industry and community associations | 4 | $58,508 | telecom industry body, Croatian software exporters' association, Split tech community | V0025 Tmforum ($57,560); V0249 Tm Forum ($510); V0283 Split Tech City ($284); V0318 Hrvatski Nezavisnici Izvoznici Softvera ($154) |
| Professional and learning memberships | 3 | $1,366 | Project Management Institute, a UX learning membership, a UX publisher and conference organiser | V0220 Smashing Media Ag ($850); V0268 Pmi Global Operations Center ($378); V0324 Interaction Design Foundation, Inc ($138) |
| Sports and recreation clubs | 4 | $3,420 | club in the name (udruga means association) | V0192 Chamiers Recreation Club ($1,338); V0197 P S Recreation Club ($1,219); V0227 Friends Sports Club ($797); V0354 Sportska Udruga Split ($66) |

- Implication for classification: TM Forum goes to Marketing (industry membership, per the taxonomy rules); clubs go with team events and perks; individual learning memberships go to training.
- Implication for the memo: TM Forum is the only material membership; everything else is tail spend. Whether TM Forum has a commercial justification depends on how much revenue comes from telecom customers.

### 7.5 Agencies and recruiters

31 vendors, $851,310 (10.8% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Recruitment agencies | 6 | $183,950 | recruitment or personnel in the name, or analyst hint | V0021 Harmonic Group Limited ($65,418); V0033 Accutrainee Limited ($38,841); V0034 Mason Frank International Ltd ($38,148); V0049 Technet It Recruitment ($21,952); V0051 Cedar Recruitment Ltd ($18,537); V0206 Integrated Personnel Services ($1,054) |
| Job boards and recruiting platforms | 2 | $59,109 | LinkedIn and Info Edge (Naukri), per analyst hints | V0026 Linkedin Ireland Limited ($55,573); V0138 Info Edge India Limited ($3,536) |
| Employer of record, payroll and HR outsourcing | 4 | $93,932 | payroll or HR outsourcing, per the name or analyst hint | V0016 Hr Solution International Gmbh ($80,823); V0090 Hrsolution International Ag ($6,987); V0111 Australian Payroll Professionals Pty Ltd ($4,399); V0179 Radius Group, Inc ($1,723) |
| Marketing, PR and media agencies | 7 | $90,299 | agency, PR, promotion or production in the name, or analyst hint | V0020 Big Frontier Pty Ltd (Cult Of Monday) ($66,131); V0050 Mightyhive Ltd ($19,042); V0168 Cision Pr Newswire ($2,110); V0184 Carrington Communications ($1,654); V0210 Digitalna Produkcija J.D.O.O. ($993); V0295 Media Promo Plus D.O.O. ($226); V0320 Puzzle Promotion J.D.O.O. ($143) |
| Event organisers and agencies | 8 | $6,923 | events, bookings or ticketing in the name, or analyst hint | V0150 Terrapinn Holdings Ltd ($2,838); V0187 Lajnap Comedy Booking D.O.O. ($1,536); V0219 Urbani Eventi D.O.O. ($851); V0234 Blink Events ($664); V0257 Entrio Tehnologije D.O.O. ($473); V0298 Djs For U ($220); V0301 Rishi Events And Entainment ($198); V0322 Event Ors ($143) |
| Travel management and travel agencies | 4 | $417,098 | travel platform, travel agency or ticketing airline | V0003 Navan (Tripactions Inc) ($357,984); V0024 Navan, Inc ($57,929); V0209 Winmaxi Tours & Travels ($1,001); V0307 Hahn Air ($183) |

- Implication for classification: Recruiters, job boards and payroll or employer-of-record providers go to G&A; marketing, PR and event agencies go to Marketing; travel management to G&A.
- Implication for the memo: Recruiting and HR outsourcing is a Terminate candidate once the parent's talent and payroll functions take over; marketing agencies are a Consolidate candidate.

### 7.6 Insurers and benefits

25 vendors, $434,013 (5.5% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Health, life and general insurers | 8 | $231,337 | insurer brands; osiguranje means insurance | V0012 Aetna Life And Casualty Ltd ($124,661); V0042 Agram Life Osiguranje D.O.O. ($24,952); V0045 Care Health Insurance Company Limited ($24,045); V0047 Bupa- Supplier ($22,800); V0069 Cigna Sg ($13,249); V0071 Bupa Australia ($12,463); V0095 Icici Lombard Gic Ltd ($5,972); V0143 Cici Prudential Life Insurance Co. Ltd. ($3,195) |
| Workers' compensation (statutory) | 3 | $8,220 | state workers' compensation schemes in Australia | V0094 Allianz Australia Workers' Compensation (Victoria) Limited ($6,099); V0201 Icare Nsw ($1,150); V0212 Allianz Wa ($971) |
| Brokers and benefits consultants | 2 | $148,143 | an insurance broker and a benefits consultant | V0010 Jensten Insurance Brokers ($142,700); V0098 Mercer Limited ($5,444) |
| Benefit schemes and wellness | 7 | $45,922 | meal cards, sports card, cycle-to-work, salary-packaged cars, telehealth and wellness | V0054 Sodexo Svc India Private Limited ($17,810); V0057 Benefit Systems D.O.O. ($16,900); V0100 Green Commute Initiative ($5,402); V0128 Pluxee India Private Limited ($3,994); V0195 Inside Edge Novated Leasing ($1,287); V0273 Doctor Anywhere Operations Pte Ltd ($347); V0308 Vitality Works ($182) |
| Occupational health | 5 | $391 | occupational medicine (medicina rada) and health institutions | V0300 Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar ($199); V0328 Ustanova Za Zdravstvenu Skrb P.P. ($131); V0382 Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos ($20); V0383 Specijalisticka Ordinacija Medicine Rada Helena Blazic ($20); V0384 Ustanova Za Medicinu Rada I Sporta Dr. Novacki ($20) |

- Implication for classification: All G&A. Workers' compensation and occupational health are statutory, so they are non-discretionary.
- Implication for the memo: Insurance spreads across several insurers in several countries plus a broker: the Consolidate case is moving these under the parent's group programme and re-broking.

### 7.7 Telecoms and utilities

14 vendors, $62,275 (0.8% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Telecom and internet | 9 | $58,078 | telecom operators and internet providers | V0046 New Star Networks(Nsn) ($23,887); V0053 Hrvatski Telekom D.D. ($18,084); V0104 Telemach Hrvatska D.O.O. ($5,134); V0135 Vodafone (Australian) ($3,672); V0140 T-Mobile ($3,357); V0163 Starhub Ltd (Supplier) ($2,205); V0188 British Telecommunications ($1,493); V0306 Zettanet ($183); V0356 Inet Telecoms Ltd. ($63) |
| Telephony and messaging APIs | 2 | $233 | cloud phone numbers and an SMS API | V0309 Avoxi Inc ($178); V0363 Click Send Pty Ltd ($55) |
| Electricity, city utilities and waste | 3 | $3,963 | electricity, the city utility company and waste collection | V0119 Hep Elektra D.O.O. ($3,735); V0321 Zagrebački Holding D.O.O. ($143); V0347 London Waste Management ($86) |

- Implication for classification: Lines and mobile plans go to Facilities; telephony that serves support lines to Support; SMS and phone APIs to Engineering, per the taxonomy rules.
- Implication for the memo: Small in total; they follow office decisions rather than drive them.

### 7.8 Plausibly a customer or customer-mandated

5 vendors, $122,405 (1.6% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Customer procurement entities | 2 | $96,037 | Telefónica group procurement (Global Services GmbH) and e-procurement (Compras Electrónicas) entities | V0015 Telefonica Global Services Gmbh ($89,880); V0093 Telefónica Compras Electrónicas S.L. ($6,157) |
| Customer-mandated supplier network | 1 | $1,363 | SAP Ariba charges suppliers fees when customers buy through it | V0191 Ariba Inc ($1,363) |
| Supplier tag in the name | 2 | $25,005 | the tag suggests the source system holds a second record for the same company, plausibly a customer account | V0047 Bupa- Supplier ($22,800); V0163 Starhub Ltd (Supplier) ($2,205) |

- Implication for classification: Telefónica and Ariba go to Sales as customer-mandated platform fees, confidence low, Optimize with the non-discretionary rationale, never Terminate. The two Supplier-tagged names are classified by what they supply (Bupa insurance, StarHub telecom), with a note that the company may also sell to them.
- Implication for the memo: Payments from a supplier to its customer's procurement entities are unusual. If they are rebates, credits or penalties rather than platform fees, they belong against revenue, not in vendor spend. Confirm before the memo quotes a total. Bupa and StarHub stay in the savings base, but any change to them needs a commercial check.

### 7.9 Travel and hospitality paid directly

20 vendors, $34,660 (0.4% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| Hotels and resorts | 15 | $31,967 | hotel, resort or hospitality in the name | V0077 Poles Ltd - Hanbury Manor ($10,488); V0112 Inter Continental Chennai Mahabalipuram Resort ($4,393); V0115 Puducherry Backwater Resort Private Limited ($4,056); V0132 Trocadero (London) Hotel Ltd ($3,868); V0154 Cleverland Winery Resort ($2,663); V0171 Grt Hotels And Resorts P Ltd ($2,032); V0190 Radisson Grt - Unit Of Hotels & Resorts Pvt Ltd ($1,406); V0226 President Hotel And Tower Co., Ltd ($803); V0247 Hotel Zonar ($523); V0250 Marvie Hotel - Krupa D.O.O. ($502); V0255 Obiteljski Hoteli D.O.O. ($474); V0262 Edwardian Pastoria Hotels Ltd (The Londoner) ($433); V0304 Hotel Laguna D.D. ($190); V0348 Hilton Garden Inn - Zagreb City Hotels D.O.O. ($82); V0365 Shilton Hospitality Llp ($55) |
| Airlines and ground transport | 5 | $2,693 | airline, bus service or transport (prijevoz) in the name | V0217 Galop-Prijevoz D.O.O. ($908); V0222 Croatia Airlines ($832); V0266 Lancefield Bus Service ($412); V0272 Niva Transport J.D.O.O. ($358); V0307 Hahn Air ($183) |

- Implication for classification: G&A, travel and entertainment.
- Implication for the memo: Hotels, airlines and ground transport paid directly are travel spend the travel platform does not see; a Navan policy lever has to cover them too.

### 7.10 Function not evident from the name

69 vendors, $472,522 (6.0% of spend).

| Subgroup | Vendors | Spend | Evidence | Vendors (largest first) |
|---|---|---|---|---|
| No function word, or only a generic one | 55 | $162,771 | the name says nothing about the service, or only consulting, advisory, services, trade or technologies | V0017 4I Advisory Services ($71,860); V0062 Westbrook Advisers ($15,360); V0072 4I Management Consulting Private Limited ($12,117); V0078 Shoff Darby Companies ($10,100); V0092 Obrt Sjaj Sunca ($6,596); V0102 Athlete Service Ltd ($5,285); V0107 Profi Bar D.O.O. ($4,917); V0127 Calm Achiever(A Unit Of Mohsin Ali Vakil) ($4,071); V0120 Zivi Napitak D.O.O. ($3,700); V0148 Crossland ($2,924); V0149 It London ($2,838); V0151 Elemental Life Solutions Llp ($2,807); V0180 Aquila Remete D.O.O. ($1,706); V0181 Clime India Private Limited ($1,678); V0182 Golden Mean, Inc ($1,659); V0189 Etm Concessions Ltd ($1,419); V0196 Rhea D.O.O. ($1,253); V0204 Backoffice Associates ($1,080); V0205 Oladi D.O.O. ($1,064); V0224 Boe Croatia D.O.O. ($814); V0225 Potomac D.O.O. ($806); V0231 Kilgannon & Partners Llp ($681); V0236 Mesa Verde ($662); V0245 Tau On-Line D.O.O. ($534); V0252 Yellow Submarine D.O.O. ($486); V0253 Streamlinereforms Inc ($483); V0254 Make And Grow Ltd ($483); V0256 Rudan D.O.O. ($473); V0261 Greencell Express Private Limited ($457); V0263 Tiganda J.D.O.O. ($432); V0267 Super Odredište D.O.O. ($378); V0270 Del Posto D.O.O. ($364); V0279 Treci Posao D.O.O. ($307); V0285 Adamma Info Services Private Limited ($273); V0287 Stillmark Zagreb D.O.O. ($263); V0290 Infodata ($241); V0293 Bella Operation A/S ($241); V0296 Expert-Ing D.O.O. ($225); V0302 Kosmaz Technologies Croatia ($195); V0312 Xenon Savjetovanje D.O.O. ($164); V0317 Advena ($154); V0319 Monile J.D.O.O. ($152); V0330 Teb Poslovno Savjetovanje D.O.O. ($129); V0331 Illunis D.O.O. ($128); V0335 Bonus Opinio D.O.O. ($120); V0339 Fortis Trade J.D.O.O. ($95); V0340 Till Trade D.O.O. ($93); V0344 Lemia D.O.O. ($88); V0345 Retriever Llc ($88); V0346 Meluba Limited ($88); V0351 Mithras Consultants ($77); V0360 New Block D.O.O. ($56); V0372 Garden City D.O.O. ($45); V0373 Livingstone ($41); V0381 Harissa D.O.O. ($21) |
| Croatian companies the analyst hints list as unknown | 13 | $309,614 | analyst hint: function unknown, most likely contractors; confirm with Finance | V0009 Weking D.O.O. ($144,093); V0032 Veniture D.O.O. ($39,342); V0038 Nefron - Obrt Za Poslovne Usluge ($30,614); V0058 Smart Group Services D.O.O. ($16,438); V0065 Pingo D.O.O. ($14,508); V0067 Tp Prime D.O.O. ($13,785); V0074 Bijeli Pijesak Obrt Za Poslovno Savjetovanje ($11,605); V0075 Ramiro D.O.O. ($11,516); V0083 Omonia D.O.O. ($9,559); V0096 Mosaic Concept D.O.O. ($5,731); V0097 Limes Plus D.O.O. ($5,624); V0137 Orcola D.O.O. ($3,545); V0141 Akton D.O.O. ($3,254) |
| Unnamed payee | 1 | $137 | the source holds the placeholder (Blank) instead of a vendor name | V0325 (Blank) ($137) |

- Implication for classification: Confidence low and a description that says the function cannot be inferred from the name (CLAUDE.md rule); for the Croatian companies the analyst hint applies and the description ends with "confirm with Finance".
- Implication for the memo: A visible share of spend cannot be described from the file alone. Recommendations on these payees stay provisional until Finance identifies them, and the memo should say so.

## 8. Suspicious or unexplained

1. **Salesforce is 39.5% of all spend.** V0002 Salesforce Uk Ltd-Uk ($3,117,226) is 39.5% of the total, 7.5 times the next vendor after merging, and more than the next 23 vendors combined. The file does not say whether this is CRM licences for staff, platform or OEM fees tied to the company's own product, or a multi-year prepayment. Implication: The savings lever depends entirely on which it is; no Salesforce saving should be sized before the contract is read.
2. **The eighth largest vendor cannot be identified.** V0009 Weking D.O.O. ($144,093) ranks eighth by cost and its name says nothing about its service. With the other hinted Croatian companies, 13 payees total $309,614; all payees whose function the name does not show total $472,522 (6.0%). Implication: Finance has to identify these before the memo relies on them; one-person Croatian companies supplying labour also carry an employment-status question.
3. **A supplier paying its customer's procurement entities.** Telefónica Global Services GmbH and Telefónica Compras Electrónicas S.L. receive $96,037. These are Telefónica's purchasing entities, so the company is most likely a Telefónica supplier. Implication: Platform fees are a cost of selling; rebates, credits or penalties are revenue items booked as vendor spend. Either way they are not discretionary.
4. **Two names carry a Supplier tag.** `Bupa- Supplier` and `Starhub Ltd (Supplier)`. A tag like this usually separates a vendor record from another record of the same company. Implication: If StarHub or Bupa are also customers, terminating or re-tendering them is a commercial decision, not a procurement one.
5. **A large municipal planning payment.** V0073 Grad Zagreb, Gradski Ured Za Prostorno Uređenje,.. ($11,637): the City of Zagreb's office for spatial planning. Fees of this size usually relate to permits or building works, which a tenant rarely pays. Implication: Likely one-off and non-discretionary; ask Finance what it was for.
6. **Government payees that point at the group structure.** V0361 Cayman Islands Government ($56) implies a Cayman Islands entity; V0333 Australian Taxation Office (Ato) ($123) is tax paid through accounts payable. Implication: Confirm the legal-entity map with the parent; tax payments are not vendor spend.
7. **Payees whose purpose is unclear.** V0223 Bb Football Scouting J.D.O.O. ($823) (a football scouting company) and V0162 Pink Ribbon Shop ($2,251) (a shop). Implication: Small, but they are the kind of line a CFO asks about; classify with confidence low.
8. **Card and expense transactions in an accounts-payable list.** `Uber *Eats` is a card-statement descriptor; 39 retail rows are under $1,000; 25 food and drink payees are paid as vendors; 20 hotels, airlines and transport companies are paid directly rather than through Navan. Implication: The vendor count overstates the supplier base; tail spend is a policy question (cards, expenses, Navan), not a negotiation.
9. **The same vendor under old and new names.** Navan is paid as `Navan (Tripactions Inc)` and `Navan, Inc`; Sodexo SVC India and Pluxee India appear side by side. Implication: The vendor master was not cleaned after renames; merge them (section 6) and recommend one entity.
10. **Grid size and dropdown source.** The vendor sheet's grid runs to row 814 and the Department dropdown reads `Config` rows 2 to 814, although the data ends at row 387 and `Config` at row 13. Implication: Consistent with a template or an earlier, longer version of the sheet. Nothing in the file shows whether the 386 rows are every vendor paid in the 12 months; the memo should call the total the spend in this file.
11. **Name damage beyond mojibake.** `Magazin Raunalni Sistemi` has lost the letter č (Računalni, computer); `Cici Prudential` is ICICI Prudential without its first letter; `Mcburneys Charted Accountants` misspells Chartered. Implication: The cleaning step repairs a display name only where the correct form is certain (the č); the others are noted, not rewritten.
12. **Explained, not suspicious.** Identical amounts (section 2), the precision pattern (section 3) and the row-order breaks (section 5) are all consequences of the cost modification; the first-digit test (section 4) shows nothing unusual. Implication: Mention once in the methodology; nothing for the memo.

Payees over $5,000 whose function the name does not show:

| Vendor | 12-month cost | Flag |
|---|---|---|
| V0009 Weking D.O.O. | $144,093 | Croatian companies the analyst hints list as unknown |
| V0017 4I Advisory Services | $71,860 | No function word, or only a generic one |
| V0032 Veniture D.O.O. | $39,342 | Croatian companies the analyst hints list as unknown |
| V0038 Nefron - Obrt Za Poslovne Usluge | $30,614 | Croatian companies the analyst hints list as unknown |
| V0058 Smart Group Services D.O.O. | $16,438 | Croatian companies the analyst hints list as unknown |
| V0062 Westbrook Advisers | $15,360 | No function word, or only a generic one |
| V0065 Pingo D.O.O. | $14,508 | Croatian companies the analyst hints list as unknown |
| V0067 Tp Prime D.O.O. | $13,785 | Croatian companies the analyst hints list as unknown |
| V0072 4I Management Consulting Private Limited | $12,117 | No function word, or only a generic one |
| V0074 Bijeli Pijesak Obrt Za Poslovno Savjetovanje | $11,605 | Croatian companies the analyst hints list as unknown |
| V0075 Ramiro D.O.O. | $11,516 | Croatian companies the analyst hints list as unknown |
| V0078 Shoff Darby Companies | $10,100 | No function word, or only a generic one |
| V0083 Omonia D.O.O. | $9,559 | Croatian companies the analyst hints list as unknown |
| V0092 Obrt Sjaj Sunca | $6,596 | No function word, or only a generic one |
| V0096 Mosaic Concept D.O.O. | $5,731 | Croatian companies the analyst hints list as unknown |
| V0097 Limes Plus D.O.O. | $5,624 | Croatian companies the analyst hints list as unknown |
| V0102 Athlete Service Ltd | $5,285 | No function word, or only a generic one |

## 9. What this means for classification

- Classify 386 rows but treat the 14 merge groups as single vendors, so each gets one department, one description and one recommendation that names the entity to keep.
- Set confidence low for the 69 payees whose function the name does not show and for the six individuals; say so in the description rather than guessing.
- Use the Croatian glossary terms surfaced here (obrt, vl., grad, osiguranje, medicina rada, prijevoz, dostava, ugostiteljstvo, savjetovanje, udruga) so Croatian descriptions are translations.
- Statutory, government and customer-mandated payees take Optimize with the non-discretionary rationale.
- Departments must match `Config` exactly; the dropdown enforces it in the workbook and the QA script will too.

## 10. What this means for the memo

- Excluded from the savings base: 14 statutory payees (tax, government, regulators, workers' compensation, occupational health) at $24,257, and 3 customer-mandated payees (Telefónica, Ariba) at $97,400, pending Finance's answer on Telefónica: $121,657 in all. Student centres, utilities and the Supplier-tagged names stay in the base.
- Provisional: $472,522 (6.0%) sits with payees the file does not identify.
- Candidate themes the forensic pass supports: insurance and benefits across 25 payees ($434,013); recruiting and HR outsourcing ($336,991); Navan as one vendor; Salesforce once its contract nature is known.
- Present money in whole dollars or thousands, call the total the spend in this file, and say once that costs were modified by the data owner.
