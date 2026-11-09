# Data profile: vendor_analysis_assessment.xlsx

Generated 2026-11-10 by `scripts/00_data_profile.py`. The workbook was opened read-only and not modified. Source SHA-256: `5473deb2fcb040a8ee5d54f91c9b1bca6467afc24839695fbd522fb414318a30`.

## 1. Workbook overview

| Sheet | Used range | Rows with values | Data rows (below header) | Named columns | Formula cells |
|---|---|---|---|---|---|
| Vendor Analysis Assessment | A1:O814 | 387 | 386 | 5 of 15 | 0 |
| Top 3 Opportunities | A1:D7 | 4 | 3 | 2 of 4 | 0 |
| Methodology | A1:B7 | 1 | 0 | 1 of 2 | 0 |
| CEOCFO Recommendations | A1:B7 | 1 | 0 | 1 of 2 | 0 |
| Config | A1:A13 | 13 | 12 | 1 of 1 | 0 |

Sheets: 5, all visible. Defined names: none.

## 2. Sheet `Vendor Analysis Assessment`

### Columns, types and blanks

Used range `A1:O814`: 814 rows x 15 columns, sheet state `visible`. Rows with any value: 387. Header row: 1. Data rows (2 to 387): 386. Trailing blank rows inside the used range: 427. Formula cells: 0. Data validation: B2:B387: type=list, formula=Config!$A$2:$A814.

| Col | Header | Non-blank | Blank | Value types (count) | Number formats (count) |
|---|---|---|---|---|---|
| A | Vendor Name | 386 | 0 | str: 386 | `General`: 386 |
| B | Department | 0 | 386 | (none) | (none) |
| C | Last 12 months Cost (USD) | 386 | 0 | float: 386 | `"$"#,##0`: 386 |
| D | 1-line Description on what the Vendor does | 0 | 386 | (none) | (none) |
| E | Suggestions (Consolidate / Terminate / Optimize costs) | 0 | 386 | (none) | (none) |
| F | (no header) | 0 | 386 | (none) | (none) |
| G | (no header) | 0 | 386 | (none) | (none) |
| H | (no header) | 0 | 386 | (none) | (none) |
| I | (no header) | 0 | 386 | (none) | (none) |
| J | (no header) | 0 | 386 | (none) | (none) |
| K | (no header) | 0 | 386 | (none) | (none) |
| L | (no header) | 0 | 386 | (none) | (none) |
| M | (no header) | 0 | 386 | (none) | (none) |
| N | (no header) | 0 | 386 | (none) | (none) |
| O | (no header) | 0 | 386 | (none) | (none) |

### Row counts

- Rows with any value below the header: 386
- Rows with a vendor name: 386 (386 distinct name strings)
- Rows with a value but no vendor name: 0
- Rows with a numeric 12-month cost: 386
- Rows with a vendor name but a non-numeric or blank cost: 0
- Department filled: 0 of 386; Description filled: 0; Suggestions filled: 0
- Rows are sorted by cost, largest first, except for 2 adjacent pair(s) out of order (rows 125 and 126, 291 and 292); row number is an approximate spend rank

### Vendor name hygiene

- Names matching Python's Title Case exactly: 99.5% (the source applied Title Case to every name, so acronyms such as `Bdo Llp`, `Rsm Uk`, `Ss&C Intralinks`, `Dhl` and possessives such as `Kat'S Kitchen` are casing artifacts)
- Leading or trailing whitespace: none
- Internal double spaces: none
- ALL CAPS names: none
- all lower-case names: none
- Names containing digits (after mojibake repair): 6: `4I Advisory Services`; `4I Management Consulting Private Limited`; `Gym4You D.O.O.`; `4Imprint Direct Ltd`; `6Sense Insights Inc`; `Kall Kwik Centre 565`
- Names shorter than 3 characters: none
- Longest name: 60 characters (1: `Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos`)
- Placeholder names: 1: `(Blank)`
- Names with non-ASCII characters: 11: `Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar`; `Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,..`; `Telefã³Nica Compras Electrã³Nicas S.L.`; `Oâ€™Donnell Salzano Lawyers`; `Garaå¾A Firule D.O.O.`; `Porezno Savjetniå¡Tvo Tuk D.O.O.`; `Mãœller Trgovina Zagreb D.O.O.`; `Catering Iviä‡ D.O.O.`; `Super Odrediå¡Te D.O.O.`; `Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Å Tampar`; `Zagrebaä_x008d_Ki Holding D.O.O.`
- Names with Excel `_xHHHH_` escapes (characters the source encoding could not store): 2: `Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar`; `Zagrebaä_x008d_Ki Holding D.O.O.`
- Names containing an em dash: none
- Names with a parenthetical (alias, former name, region or unit): 17: `Navan (Tripactions Inc)`; `Big Frontier Pty Ltd (Cult Of Monday)`; `New Star Networks(Nsn)`; `Jones Lang Lasalle (Nsw) Pty Ltd`; `Allianz Australia Workers' Compensation (Victoria) Limited`; `Calm Achiever(A Unit Of Mohsin Ali Vakil)`; `Trocadero (London) Hotel Ltd`; `Vodafone (Australian)`; `United Flow Ltd (The Goodness Project)`; `Starhub Ltd (Supplier)`; `Edwardian Pastoria Hotels Ltd (The Londoner)`; `National Securities Depository Limited(Nsdl)`; `Amazon (Aus)`; `(Blank)`; `Australian Taxation Office (Ato)` (and 2 more)
- Names with a ` - ` alias separator (brand vs legal entity or location): 11: `Nefron - Obrt Za Poslovne Usluge`; `Poles Ltd - Hanbury Manor`; `Studentski Centar - Split`; `Intertrust Singapore Corporate Services Pte Ltd - Csc`; `Radisson Grt - Unit Of Hotels & Resorts Pvt Ltd`; `Apple - Amer`; `Klg - Kalra Legal Group`; `Marvie Hotel - Krupa D.O.O.`; `Blitz - Cinestar D.O.O.`; `Hilton Garden Inn - Zagreb City Hotels D.O.O.`; `Farmacia - Specijalizirana Prodavaonica D.O.O.`
- Names with a hyphenated 2 to 5 letter tag right after the legal form (country tag, sometimes truncated): 2: `Salesforce Uk Ltd-Uk`; `Eurofast International Ltd-Greec`
- Names ending in `..` (truncated in the source): 1: `Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,..`
- Names tagged `Supplier`: 2: `Bupa- Supplier`; `Starhub Ltd (Supplier)`
- Card-statement style descriptors containing `*`: 1: `Uber *Eats`

**Encoding damage (mojibake)**

11 names contain UTF-8 text that was decoded as Windows-1252 and then Title Cased. The repair below (re-encode as cp1252, decode as UTF-8, fix the case of the letter after each repaired character) is proposed, not applied; each row should be eyeballed.

| Row | As stored | Proposed repair | Cost |
|---|---|---|---|
| 30 | Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar | Sveučilište U Zagrebu, Studentski Centar | $44,299 |
| 73 | Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,.. | Grad Zagreb, Gradski Ured Za Prostorno Uređenje,.. | $11,637 |
| 93 | Telefã³Nica Compras Electrã³Nicas S.L. | Telefónica Compras Electrónicas S.L. | $6,157 |
| 129 | Oâ€™Donnell Salzano Lawyers | O’Donnell Salzano Lawyers | $3,955 |
| 147 | Garaå¾A Firule D.O.O. | Garaža Firule D.O.O. | $2,930 |
| 176 | Porezno Savjetniå¡Tvo Tuk D.O.O. | Porezno Savjetništvo Tuk D.O.O. | $1,813 |
| 207 | Mãœller Trgovina Zagreb D.O.O. | Müller Trgovina Zagreb D.O.O. | $1,051 |
| 233 | Catering Iviä‡ D.O.O. | Catering Ivić D.O.O. | $669 |
| 267 | Super Odrediå¡Te D.O.O. | Super Odredište D.O.O. | $378 |
| 300 | Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Å Tampar | Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar | $199 |
| 321 | Zagrebaä_x008d_Ki Holding D.O.O. | Zagrebački Holding D.O.O. | $143 |

### Exact duplicate vendor names

None. Every one of the vendor name strings is unique.

Case and whitespace-insensitive duplicates (same letters, different case or spacing): none.

### Fuzzy duplicate vendor names

Method: repair mojibake, strip accents, lower-case, replace `&` with `and`, collapse dotted abbreviations (`D.O.O.` to `doo`), drop punctuation, then drop legal-form tokens (Ltd, Limited, Inc, LLC, GmbH, D.O.O., J.D.O.O., D.D., Obrt, Bvba, Pvt, Private, Pty, Pte, Corp, Co, ...), geography tokens (Uk, Us, Ireland, India, Australia, Croatia, Zagreb, Split, London, International, Global, ...), stop words (the, and, of, za, i, u) and noise (`Supplier`). The remaining tokens form the matching key. Keys are a matching aid only; display names keep the original wording.

**Tier 1: same key** (4 groups). Almost certainly the same vendor billed through different legal entities, regions or spellings.

| Key | Names (row, cost) | Combined cost |
|---|---|---|
| amazon web services | `Amazon Web Services Llc` (row 14, $106,399); `Amazon Web Services Inc.` (row 103, $5,153) | $111,552 |
| bupa | `Bupa- Supplier` (row 47, $22,800); `Bupa Australia` (row 71, $12,463) | $35,263 |
| apple | `Apple Pty Ltd` (row 172, $2,031); `Apple - Amer` (row 229, $764) | $2,795 |
| amazon | `Amazon.Co.Uk` (row 203, $1,107); `Amazon (Aus)` (row 291, $233) | $1,340 |

**Tier 2: near matches between different keys** (19 pairs). Rules: difflib ratio >= 0.85 (similar spelling), one key's tokens all appear in the other (token subset), or at least two tokens shared covering half of the shorter key (shared tokens). Review candidates, not confirmed duplicates; some are distinct vendors of the same type, which matters for consolidation rather than deduplication.

| Vendor A (row, cost) | Vendor B (row, cost) | Ratio | Rule |
|---|---|---|---|
| `Navan, Inc` (row 24, $57,929) | `Navan (Tripactions Inc)` (row 3, $357,984) | 0.45 | token subset |
| `Amazon.Co.Uk` (row 203, $1,107); `Amazon (Aus)` (row 291, $233) | `Amazon Web Services Llc` (row 14, $106,399); `Amazon Web Services Inc.` (row 103, $5,153) | 0.48 | token subset |
| `Hr Solution International Gmbh` (row 16, $80,823) | `Hrsolution International Ag` (row 90, $6,987) | 0.95 | similar spelling |
| `Tm Forum` (row 249, $510) | `Tmforum` (row 25, $57,560) | 0.93 | similar spelling |
| `Studentski Centar - Split` (row 86, $8,269) | `Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar` (row 30, $44,299) | 0.63 | token subset |
| `Studentski Centar Karlovac` (row 186, $1,549) | `Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar` (row 30, $44,299) | 0.54 | shared tokens |
| `Grad Split` (row 139, $3,483) | `Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,..` (row 73, $11,637) | 0.20 | token subset |
| `Acclime Corporate Services` (row 99, $5,413) | `Intertrust Singapore Corporate Services Pte Ltd - Csc` (row 88, $7,360) | 0.71 | shared tokens |
| `Bijeli Pijesak Obrt Za Poslovno Savjetovanje` (row 74, $11,605) | `Teb Poslovno Savjetovanje D.O.O.` (row 330, $129) | 0.75 | shared tokens |
| `Acclime Usa, Inc` (row 105, $4,995) | `Acclime Corporate Services` (row 99, $5,413) | 0.42 | token subset |
| `Studentski Centar - Split` (row 86, $8,269) | `Studentski Centar Karlovac` (row 186, $1,549) | 0.79 | token subset |
| `Allianz Wa` (row 212, $971) | `Allianz Australia Workers' Compensation (Victoria) Limited` (row 94, $6,099) | 0.40 | token subset |
| `Apple Pty Ltd` (row 172, $2,031); `Apple - Amer` (row 229, $764) | `Apple Retail Uk Ltd` (row 123, $3,548) | 0.59 | token subset |
| `Apple Pty Ltd` (row 172, $2,031); `Apple - Amer` (row 229, $764) | `Apple Distribution International Ltd` (row 175, $1,913) | 0.43 | token subset |
| `Grt Hotels And Resorts P Ltd` (row 171, $2,032) | `Radisson Grt - Unit Of Hotels & Resorts Pvt Ltd` (row 190, $1,406) | 0.69 | shared tokens |
| `Chamiers Recreation Club` (row 192, $1,338) | `P S Recreation Club` (row 197, $1,219) | 0.79 | shared tokens |
| `Dhl` (row 303, $191) | `Dhl Express (Uk) Ltd` (row 336, $119) | 0.43 | token subset |
| `Garden City D.O.O.` (row 372, $45) | `Hilton Garden Inn - Zagreb City Hotels D.O.O.` (row 348, $82) | 0.55 | token subset |
| `Specijalisticka Ordinacija Medicine Rada Helena Blazic` (row 383, $20) | `Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos` (row 382, $20) | 0.80 | shared tokens |

**Tier 3: same leading token only** (9 groups with at least one pair not flagged above). Weak signal; listed because a shared brand word (Apple, Telefonica) or a shared Croatian noun (hotel, grad, ustanova) is worth one look.

- `telefonica`: `Telefã³Nica Compras Electrã³Nicas S.L.` (row 93, $6,157); `Telefonica Global Services Gmbh` (row 15, $89,880)
- `4i`: `4I Advisory Services` (row 17, $71,860); `4I Management Consulting Private Limited` (row 72, $12,117)
- `new`: `New Block D.O.O.` (row 360, $56); `New Star Networks(Nsn)` (row 46, $23,887)
- `hrvatski`: `Hrvatski Nezavisnici Izvoznici Softvera` (row 318, $154); `Hrvatski Telekom D.D.` (row 53, $18,084)
- `catering`: `Catering Iviä‡ D.O.O.` (row 233, $669); `Catering Muring` (row 82, $9,603)
- `apple`: `Apple Pty Ltd` (row 172, $2,031); `Apple - Amer` (row 229, $764); `Apple Distribution International Ltd` (row 175, $1,913); `Apple Retail Uk Ltd` (row 123, $3,548)
- `paint`: `Paint & Fun Vl. Martina Milkova Nikolova` (row 183, $1,654); `Paint&Wine, Vl. Stevo Dosen` (row 315, $159)
- `hotel`: `Hotel Laguna D.D.` (row 304, $190); `Hotel Zonar` (row 247, $523)
- `ustanova`: `Ustanova Za Medicinu Rada I Sporta Dr. Novacki` (row 384, $20); `Ustanova Za Zdravstvenu Skrb P.P.` (row 328, $131)

### Currency hints

- Cost column header: `Last 12 months Cost (USD)` (states USD explicitly).
- Excel number formats on numeric cost cells: `"$"#,##0`: 386
- Cost cells stored as text (would need parsing): 0
- Costs with a fractional part: 386 of 386; most decimal digits seen: 15. Invoice totals are rarely this precise, which is consistent with the values having been converted from other currencies or scaled (the brief says costs were modified). No FX rate, original currency or invoice date column exists, so the conversion cannot be checked or reversed.
- Currency symbols or ISO codes inside text cells (name, department, description, suggestions), checked after mojibake repair: none. Before repair row 129 `Oâ€™Donnell Salzano Lawyers` showed a stray currency sign that is encoding damage, not a currency.
- Legal-form and geography tokens in vendor names (where the vendor is incorporated, which hints at the original billing currency but does not prove it): `doo` (82), `ltd` (52), `limited` (41), `inc` (26), `private` (12), `uk` (11), `llc` (9), `llp` (8), `jdoo` (7), `pty` (6), `co` (5), `croatia` (5), `international` (5), `ireland` (5), `obrt` (5), `zagreb` (5), `dd` (4), `india` (4), `london` (4), `split` (4), `ag` (3), `australian` (3), `global` (3), `gmbh` (3), `hrvatska` (3), `pte` (3), `australia` (2), `company` (2), `melbourne` (2), `nsw` (2), `pc` (2), `pvt` (2), `singapore` (2), `sro` (2), `vl` (2), `amer` (1), `aps` (1), `aus` (1), `bvba` (1), `chennai` (1), `corporation` (1), `greec` (1), `lp` (1), `oy` (1), `pp` (1), `sg` (1), `sl` (1), `usa` (1), `victoria` (1), `wa` (1)
- Rows with a Croatian legal form (D.O.O., J.D.O.O., D.D., Obrt): 98 of 386

### Total 12-month spend and distribution

- Total 12-month spend (sum of numeric costs): **$7,887,360** across 386 vendor rows (exact: 7,887,360.40)
- Mean $20,434; median $1,298; min $18; max $3,117,226
- Zero-cost rows: 0; negative-cost rows: 0

**Top 10 vendors (as recorded, one row each)**

| Rank | Vendor | Row | 12-month cost | Share | Cumulative |
|---|---|---|---|---|---|
| 1 | Salesforce Uk Ltd-Uk | 2 | $3,117,226 | 39.5% | 39.5% |
| 2 | Navan (Tripactions Inc) | 3 | $357,984 | 4.5% | 44.1% |
| 3 | Bdo Llp | 4 | $343,081 | 4.3% | 48.4% |
| 4 | Tog Uk Properties Limited | 5 | $263,821 | 3.3% | 51.8% |
| 5 | Cloudcrossing Bvba | 6 | $208,675 | 2.6% | 54.4% |
| 6 | Zagrebtower D.O.O. | 7 | $183,754 | 2.3% | 56.7% |
| 7 | Innovent Spaces Private Limited | 8 | $147,348 | 1.9% | 58.6% |
| 8 | Weking D.O.O. | 9 | $144,093 | 1.8% | 60.4% |
| 9 | Jensten Insurance Brokers | 10 | $142,700 | 1.8% | 62.2% |
| 10 | Gpt Space & Co | 11 | $133,507 | 1.7% | 63.9% |

**Concentration**

| Vendors | Spend | Share of total |
|---|---|---|
| Top 1 | $3,117,226 | 39.5% |
| Top 10 | $5,042,189 | 63.9% |
| Top 20 | $5,898,424 | 74.8% |
| Top 50 | $6,981,334 | 88.5% |
| Top 100 | $7,538,134 | 95.6% |

The top 28 vendors (7.3% of vendor rows) account for 80% of spend.

**Vendors under $1,000**

- Count: 178 of 386 vendor rows (46.1%)
- Total spend: $55,354 (0.7% of total)

**Spend bands**

| Band | Vendors | Share of vendors | Spend | Share of spend |
|---|---|---|---|---|
| under $1,000 | 178 | 46.1% | $55,354 | 0.7% |
| $1,000 to $9,999 | 129 | 33.4% | $442,936 | 5.6% |
| $10,000 to $99,999 | 66 | 17.1% | $1,998,743 | 25.3% |
| $100,000 to $999,999 | 12 | 3.1% | $2,273,102 | 28.8% |
| $1,000,000 and above | 1 | 0.3% | $3,117,226 | 39.5% |

## 3. Sheet `Top 3 Opportunities`

Used range `A1:D7`: 7 rows x 4 columns, sheet state `visible`. Rows with any value: 4. Header row: 1. Data rows (2 to 4): 3. Trailing blank rows inside the used range: 3. Formula cells: 0. Data validation: none.

| Col | Header | Non-blank | Blank | Value types (count) | Number formats (count) |
|---|---|---|---|---|---|
| A | (no header) | 3 | 0 | str: 3 | `General`: 3 |
| B | Opportunity | 0 | 3 | (none) | (none) |
| C | Explanation | 0 | 3 | (none) | (none) |
| D | (no header) | 0 | 3 | (none) | (none) |

Non-blank cells, verbatim:

- `B1`: Opportunity
- `C1`: Explanation
- `A2`: Opportunity 1
- `A3`: Opportunity 2
- `A4`: Opportunity 3

## 4. Sheet `Methodology`

Used range `A1:B7`: 7 rows x 2 columns, sheet state `visible`. Rows with any value: 1. Header row: 1. Data rows (2 to 1): 0. Trailing blank rows inside the used range: 6. Formula cells: 0. Data validation: none.

| Col | Header | Non-blank | Blank | Value types (count) | Number formats (count) |
|---|---|---|---|---|---|
| A | Please provide a brief explanation for how you approached working through this. (what was your methodology, prompt(s), tools, etc) | 0 | 0 | (none) | (none) |
| B | (no header) | 0 | 0 | (none) | (none) |

Non-blank cells, verbatim:

- `A1`: Please provide a brief explanation for how you approached working through this.<br>(what was your methodology, prompt(s), tools, etc)

## 5. Sheet `CEOCFO Recommendations`

Used range `A1:B7`: 7 rows x 2 columns, sheet state `visible`. Rows with any value: 1. Header row: 1. Data rows (2 to 1): 0. Trailing blank rows inside the used range: 6. Formula cells: 0. Data validation: none.

| Col | Header | Non-blank | Blank | Value types (count) | Number formats (count) |
|---|---|---|---|---|---|
| A | Please prepare a short memo (maximum 1 page) summarizing your findings and recommendations to the CEO and CFO.  Please keep in mind that these are busy people; position your points accordingly, focus on what really matters, and do not exceed the number of pages; do not overemphasize things that are obvious to them but also keep in mind they have many things going on and may not remember immediately certain points  Please provide a Google Doc link to your memo below | 0 | 0 | (none) | (none) |
| B | (no header) | 0 | 0 | (none) | (none) |

Non-blank cells, verbatim:

- `A1`: Please prepare a short memo (maximum 1 page) summarizing your findings and recommendations to the CEO and CFO. <br>Please keep in mind that these are busy people; position your points accordingly, focus on what really matters, and do not exceed the number of pages; do not overemphasize things that are obvious to them but also keep in mind they have many things going on and may not remember immediately certain points<br><br>Please provide a Google Doc link to your memo below

## 6. Sheet `Config`

Used range `A1:A13`: 13 rows x 1 columns, sheet state `visible`. Rows with any value: 13. Header row: 1. Data rows (2 to 13): 12. Trailing blank rows inside the used range: 0. Formula cells: 0. Data validation: none.

| Col | Header | Non-blank | Blank | Value types (count) | Number formats (count) |
|---|---|---|---|---|---|
| A | Department | 12 | 0 | str: 12 | `General`: 12 |

Non-blank cells, verbatim:

- `A1`: Department
- `A2`: Engineering
- `A3`: Facilities
- `A4`: G&A
- `A5`: Legal
- `A6`: M&A
- `A7`: Marketing
- `A8`: SaaS
- `A9`: Product
- `A10`: Professional Services
- `A11`: Sales
- `A12`: Support
- `A13`: Finance

## 7. Observations that affect the analysis

- Vendor rows: 386. The brief says about 400 vendors; consistent.
- The used range runs to row 814 and column O, but only columns A to E carry a header and only rows 2 to 387 carry data. The remaining 427 rows and 10 columns are formatting only.
- `Department`, `1-line Description` and `Suggestions` are empty on every row: these three columns are the deliverable, to be produced as `outputs/vendors_classified.csv`.
- Costs are hard-coded values (no formulas), all numeric, labelled USD in the header and formatted as whole dollars in Excel while carrying up to 15 decimals underneath. Sums must use the underlying values, not the displayed ones.
- The sheet is sorted by cost, largest first, apart from 2 adjacent pair(s) out of order, so row number is only an approximate spend rank.
- `Config` lists 12 departments: `Engineering`, `Facilities`, `G&A`, `Legal`, `M&A`, `Marketing`, `SaaS`, `Product`, `Professional Services`, `Sales`, `Support`, `Finance`. `docs/taxonomy.md`, which CLAUDE.md names as the only allowed source of departments, does not exist yet.
- Several `Config` entries are spend categories rather than departments (`SaaS`, `Professional Services`) and others overlap (`G&A` with `Finance`, `Legal`, `Facilities`). The taxonomy needs a precedence rule before classification starts.
- Data validation rules in the workbook: B2:B387: type=list, formula=Config!$A$2:$A814. The Department column is a dropdown over the `Config` list, so department values must match `Config` character for character.
- The template sheets ask for three opportunities (`Opportunity`, `Explanation`), a methodology note, and a memo of at most one page delivered as a Google Doc link. CLAUDE.md specifies `outputs/memo.md`; whether a Google Doc is also required is a question for the user.

## 8. Proposed cleaning steps

1. **Work on a copy, never the raw file.** Read `data/raw/vendor_analysis_assessment.xlsx` and write a cleaned table to `outputs/vendors_clean.csv`. Record the raw file's SHA-256 (currently the value in this report's header) in the output and in a QA check so any change to the raw file is detected. Give every row a stable id `V` plus its source row number (`V0002` to `V0387`) so every number downstream traces back to a source row.
2. **Trim the used range.** Keep rows 2 to 387 (386 vendor rows) and columns A to E. Drop the 427 trailing formatted-but-empty rows and the 10 unnamed empty columns. Assert the row count is exactly 386 after loading.
3. **Keep costs as stored.** Costs are numeric USD with up to 15 decimals. Do not round the stored values; round only for display (whole dollars). Assert the cleaned total equals 7,887,360.40 to the cent. There are 0 zero and 0 negative values, so no sign handling is needed.
4. **Repair encoding damage, keeping the original.** Add `vendor_name_raw` (verbatim) and `vendor_name_clean`. Apply the cp1252 to UTF-8 repair shown in the mojibake table to the 11 affected names, resolving Excel `_x008d_` escapes first, then review each repair by eye. Strip accents only inside the matching key, never in the display name.
5. **Handle the placeholder row.** `(Blank)` (row 325, $137) carries spend but no vendor name. Keep the spend in every total, set the description to say the vendor name is missing in the source, and set `confidence=low`. A department still has to be chosen from the taxonomy; propose `G&A` and flag it as unassignable.
6. **Tidy names for display without changing meaning.** Remove the `Supplier` tag (2: `Bupa- Supplier`; `Starhub Ltd (Supplier)`), drop a trailing `..` truncation marker (1: `Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,..`), and keep hyphenated country tags such as `-Uk` or the truncated `-Greec` (2: `Salesforce Uk Ltd-Uk`; `Eurofast International Ltd-Greec`) out of the display name while noting them in a `name_notes` column. Keep parentheticals and ` - ` aliases as they are, since they carry the alias or venue. Do not expand truncated words; `Greec` stays an observation, not a correction.
7. **Fix casing only through an explicit, reviewable map.** The source Title Cased every name. For display in the memo, maintain `qa/display_names.csv` mapping the raw name to a corrected display form for well-known acronyms and possessives (BDO LLP, RSM UK, SS&C, DHL, CBRE, HP, Kat's Kitchen, GoDaddy.com). Matching always uses the lower-cased key, never the display form, so this step cannot affect any number.
8. **Decide duplicates explicitly and apply the merges in a mapping file.** Create `qa/vendor_groups.csv` with one line per source row: `vendor_id`, `vendor_name_clean`, `group_key`, `canonical_name`, `decision` (merge or keep), `reason`. Merge the 4 Tier 1 groups by default; review the 19 Tier 2 pairs one by one (the two Navan rows are the same company and together would be the second largest vendor; Tmforum and Tm Forum, Hr Solution and Hrsolution, the four Apple entities, DHL and Bupa are the same vendor families; the student centres, occupational-health clinics and hotels are different vendors of the same type and belong in consolidation analysis, not in a merge). Report spend both per source row and per canonical vendor so both views trace to the raw rows.
9. **Add a Croatian glossary before classifying.** 98 rows carry a Croatian legal form and many names describe the business in Croatian (savjetovanje, odvjetnicko drustvo, medicina rada, prijevoz, dostava, ugostiteljstvo, osiguranje, studentski centar, gradski ured). Write `docs/glossary_hr.md` listing each term used and its English meaning so descriptions for those rows are translations, not guesses.
10. **Flag names that cannot be classified from the name alone.** Names that read as individuals (`Ansar Madovic`, `Fabiola Thistlewhaite`, `George Anchor`, `John Smith`, `Stipe Piric`, `Susan Lee`), statutory or government payees (`Australian Taxation Office (Ato)`, `Cayman Islands Government`, `Grad Split`, `Grad Zagreb, Gradski Ured Za Prostorno Uređenje,..`, `Icare Nsw`, `Ico`), and retail or card-statement merchants (`Coles`, `M&S Simply Food`, `Pret A Manger`, `Uber *Eats`, `Officeworks`, `Currys Pc World`, `Snappy Snaps`, `Post Office Ltd`) get `confidence=low` and a description that says what can and cannot be inferred. Statutory payees do not fit Terminate, Consolidate or Optimize; ask the user whether to add a fourth label or to use Optimize with a `no action, statutory` rationale.
11. **Treat the long tail as a batch, not individually.** 178 rows (46.1% of rows) are under $1,000 and together total $55,354 (0.7% of spend). Every row still gets a department, description and recommendation, but classify them in batches and do not let them drive the memo. Any savings claimed on them must be the computed sum, not an estimate.
12. **Create the taxonomy from the workbook's own list.** Write `docs/taxonomy.md` with the 12 `Config` departments verbatim, a one-line definition each, inclusion examples from this vendor list, and a precedence rule for overlaps (for example: a tool used by one team goes to that team, a company-wide tool goes to `SaaS`; outside counsel goes to `Legal`, not `Professional Services`; rent and coworking go to `Facilities`, not `G&A`). Classification cannot start before this file exists.
13. **Automate the QA checks.** A `qa/check_outputs.py` script that asserts: 386 rows in and out; total spend equals the raw total to the cent; every department is in `docs/taxonomy.md`; every recommendation is one of Terminate, Consolidate, Optimize with a one-sentence rationale; no banned phrase appears in any description; no em dash appears in any output file; every savings figure in the memo matches a value in `outputs/analysis/`.

## Addendum: workbook structure re-verification

Added 2026-11-10. A structure audit was run separately; each of its findings is re-checked here with openpyxl. Three things openpyxl does not surface were read from the raw package XML: built-in defined names, extension-list (x14) validation and conditional formats, and threaded comments. Code: `structure_audit()` in `scripts/vsa_common.py`. The wider forensic checks are in `01_forensics.md`.

| Finding of the separate audit | Re-verified result | Status |
|---|---|---|
| No hidden sheets | 5 of 5 sheets visible in openpyxl and in workbook.xml; none hidden or very hidden | Confirmed |
| No hidden rows or columns | 0 hidden rows, 0 hidden columns, 0 zero-height rows, 0 zero-width columns, 0 outline-grouped rows or columns, across all 5 sheets | Confirmed |
| No comments | 0 cell notes; comment parts in the package: 0; the persons part used by threaded comments exists but lists 0 people | Confirmed |
| No defined names | 0 user-defined names (openpyxl lists 0); the XML holds 1 hidden built-in name: `_xlnm._FilterDatabase` = `'Vendor Analysis Assessment'!$A$1:$O$387`, which Excel and Google Sheets create automatically for an AutoFilter | Confirmed, with note |
| No conditional formats | 0 rules in openpyxl; 0 conditionalFormatting elements in the sheet XML, including the x14 extension list | Confirmed |
| No content beyond A1:E387 | last value at row 387, column E; the grid runs to O814 and rows 388 to 814 (6,405 cells) and columns F to O (3,870 cells) hold styling only; 0 formulas anywhere | Confirmed |
| Only validation: Department dropdown on B2:B387 referencing Config!A2:A814 | 1 rule in the workbook: `Vendor Analysis Assessment` B2:B387: type `list`, source `Config!$A$2:$A814`, blanks allowed, error alert on; 0 x14 extension rules | Confirmed |
| Column E is free text | no validation covers column E; the only covered column is B (no rule on A, C, D, E, F, G, H, I, J, K, L, M, N, O) | Confirmed |

Notes:

- AutoFilter on `$A$1:$O$387` with 0 filter criteria and no saved sort state, so no row is filtered out of view.
- Hyperlinks: `Vendor Analysis Assessment`!A203 links to http://amazon.co.uk. The target is the cell's own text, so this is most likely an automatic link rather than added content.
- The dropdown source runs to row 814 although `Config` holds values only in A1:A13, so rows 14 to 814 of the source are empty and the only non-blank choices are the 12 departments.
