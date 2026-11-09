# Cleaning report

Generated 2026-11-10 by `scripts/02_clean.py`. The raw workbook was opened read-only; SHA-256 `5473deb2fcb040a8ee5d54f91c9b1bca6467afc24839695fbd522fb414318a30` before and after. Nothing is classified here.

Outputs:

- `outputs/vendors_clean.csv`: one row per source row with `vendor_id`, the original name (`vendor_name_raw`), the clean name (`vendor_name_clean`), the matching key, the merge group, the canonical vendor, the link group, the exact cost as stored, and notes on the name.
- `qa/vendor_groups.csv`: the entity merge map, one row per source row, with decision (merge, proposed merge or keep), relationship, confidence, link group and type, and reason.
- `qa/name_changes.csv`: every change from original to clean name, one line per step.

Decisions of 2026-11-10 applied (`docs/decisions.md`): the merge policy in section 4.

## 1. Checks

| Check | Result | Pass |
|---|---|---|
| Rows in the raw sheet equal rows in outputs/vendors_clean.csv and qa/vendor_groups.csv | 386 = 386 = 386 | yes |
| vendor_id is unique and equals V plus the source row | 386 distinct | yes |
| Original names kept verbatim in vendor_name_raw | all rows | yes |
| Total cost after cleaning equals the raw total exactly | $7,887,360.40 = $7,887,360.40 | yes |
| Every cost value round-trips unchanged | all rows | yes |
| Raw workbook unchanged by the run | SHA-256 5473deb2fcb040a8... | yes |
| Each row is in at most one merge group and at most one link group | 8 merged rows in 4 groups; 35 linked rows in 15 groups | yes |
| Every merge group is a confirmed or a proposed merge | Navan: merge, AWS: merge, TM Forum: merge, 4i: proposed merge | yes |
| docs/taxonomy.md departments equal Config A2:A13, same spelling and order | 12 listed: Engineering, Facilities, G&A, Legal, M&A, Marketing, SaaS, Product, Professional Services, Sales, Support, Finance | yes |
| docs/clusters.md holds exactly the 18 clusters of prompt 6, in order | 18 listed | yes |
| docs/recommendation_rules.md has a section for each of Terminate, Consolidate, Optimize | Terminate, Consolidate, Optimize | yes |
| docs/vendor_hints.md: every hint is verbatim from prompt 6 | 79 hints; 0 not verbatim | yes |
| docs/vendor_hints.md: every vendor_id exists and its name matches the file | 172 ids (172 distinct); 0 unknown ids; 0 name mismatches | yes |
| docs/taxonomy.md has no em or en dash | clean | yes |
| docs/recommendation_rules.md has no em or en dash | clean | yes |
| docs/vendor_hints.md has no em or en dash | clean | yes |
| docs/clusters.md has no em or en dash | clean | yes |
| docs/decisions.md has no em or en dash | clean | yes |

## 2. What the cleaning does

1. **Stable ids.** `vendor_id` is `V` plus the source row number (`V0002` to `V0387`), so every later number traces to one row of the raw sheet.
2. **Original names kept.** `vendor_name_raw` is the cell text exactly; all repairs go to `vendor_name_clean`.
3. **Mojibake repaired**, then one dropped letter restored (table below).
4. **Tags and truncation marks** moved out of the display name and into `name_notes`.
5. **Casing.** The source Title Cased every name, so acronyms, legal forms and brands are restored: the acronyms named in prompt 6 (BDO, DHL, HP, SS&C, TOG, GPT, CBRE, NCC, HEP, plus PricewaterhouseCoopers and LaSalle), other acronyms in the names, legal forms (LLP, LLC, GmbH; d.o.o. and d.d. in lower case as written in Croatia), brand casing (HubSpot, LinkedIn, DocuSign) and possessives (Kat's). AWS is the canonical name of the merged Amazon Web Services group; PwC and JLL are the canonical names of PricewaterhouseCoopers LLP and Jones Lang LaSalle.
6. **Matching key** (`match_key`): the clean name with accents, legal forms, geography, stop words and the Supplier tag removed. It is used for matching only and never displayed.
7. **Entity merge map.** 4 merge groups (1 proposed) covering 8 rows; every other row is its own group, and `group_id` is the vendor_id of the group's largest row. 15 link groups tie related vendors together without merging them (`link_group`).

## 3. Name changes

226 changes on 191 of 386 rows:

| Step | Changes | Rows |
|---|---|---|
| mojibake | 11 | 11 |
| manual fix | 1 | 1 |
| punctuation | 1 | 1 |
| spacing | 3 | 3 |
| tag | 5 | 5 |
| casing | 205 | 183 |

### Mojibake repair table

| vendor_id | As stored | Repaired | How | Final clean name |
|---|---|---|---|---|
| V0030 | Sveuä_x008d_Iliå¡Te U Zagrebu, Studentski Centar | Sveučilište U Zagrebu, Studentski Centar | mojibake | Sveučilište U Zagrebu, Studentski Centar |
| V0066 | Magazin Raunalni Sistemi D.O.O. | Magazin Računalni Sistemi D.O.O. | manual fix | Magazin Računalni Sistemi d.o.o. |
| V0073 | Grad Zagreb, Gradski Ured Za Prostorno Ureä‘Enje,.. | Grad Zagreb, Gradski Ured Za Prostorno Uređenje,.. | mojibake | Grad Zagreb, Gradski Ured Za Prostorno Uređenje |
| V0093 | Telefã³Nica Compras Electrã³Nicas S.L. | Telefónica Compras Electrónicas S.L. | mojibake | Telefónica Compras Electrónicas S.L. |
| V0129 | Oâ€™Donnell Salzano Lawyers | O’Donnell Salzano Lawyers | mojibake | O'Donnell Salzano Lawyers |
| V0147 | Garaå¾A Firule D.O.O. | Garaža Firule D.O.O. | mojibake | Garaža Firule d.o.o. |
| V0176 | Porezno Savjetniå¡Tvo Tuk D.O.O. | Porezno Savjetništvo Tuk D.O.O. | mojibake | Porezno Savjetništvo Tuk d.o.o. |
| V0207 | Mãœller Trgovina Zagreb D.O.O. | Müller Trgovina Zagreb D.O.O. | mojibake | Müller Trgovina Zagreb d.o.o. |
| V0233 | Catering Iviä‡ D.O.O. | Catering Ivić D.O.O. | mojibake | Catering Ivić d.o.o. |
| V0267 | Super Odrediå¡Te D.O.O. | Super Odredište D.O.O. | mojibake | Super Odredište d.o.o. |
| V0300 | Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Å Tampar | Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar | mojibake | Nastavni Zavod Za Javno Zdravstvo Dr. Andrija Štampar |
| V0321 | Zagrebaä_x008d_Ki Holding D.O.O. | Zagrebački Holding D.O.O. | mojibake | Zagrebački Holding d.o.o. |

### Tags and truncation

| vendor_id | Before | After | Reason |
|---|---|---|---|
| V0002 | Salesforce Uk Ltd-Uk | Salesforce Uk Ltd | country tag -Uk removed |
| V0047 | Bupa- Supplier | Bupa | Supplier tag removed; the source system appears to hold a second record for this company |
| V0052 | Eurofast International Ltd-Greec | Eurofast International Ltd | country tag -Greec (Greece, cut short in the source) removed |
| V0073 | Grad Zagreb, Gradski Ured Za Prostorno Uređenje,.. | Grad Zagreb, Gradski Ured Za Prostorno Uređenje | name cut short in the source; trailing ,.. removed |
| V0163 | Starhub Ltd (Supplier) | Starhub Ltd | Supplier tag removed; the source system appears to hold a second record for this company |

### Names kept as in the source, with a note

| vendor_id | Clean name | Note |
|---|---|---|
| V0143 | Cici Prudential Life Insurance Co. Ltd. | spelled Cici in the source; the analyst hint identifies it as ICICI Prudential |
| V0153 | McBurneys Charted Accountants | Charted (sic) kept as in the source |
| V0318 | Hrvatski Nezavisnici Izvoznici Softvera | Nezavisnici as in the source; the analyst hint spells it Nezavisni |
| V0325 | (Blank) | placeholder: the source has no vendor name |
| V0370 | Uber *Eats | card-statement descriptor, suggesting a card transaction |

Casing changes (205 rule applications on 183 rows) are listed in full in `qa/name_changes.csv`. The first rows affected, before and after casing:

| vendor_id | Before casing | After casing | Rules |
|---|---|---|---|
| V0002 | Salesforce Uk Ltd | Salesforce UK Ltd | acronym |
| V0003 | Navan (Tripactions Inc) | Navan (TripActions Inc) | brand casing |
| V0004 | Bdo Llp | BDO LLP | legal form, acronym |
| V0005 | Tog Uk Properties Limited | TOG UK Properties Limited | acronym |
| V0006 | Cloudcrossing Bvba | Cloudcrossing BVBA | legal form |
| V0007 | Zagrebtower D.O.O. | Zagrebtower d.o.o. | Croatian legal form written in lower case |
| V0009 | Weking D.O.O. | Weking d.o.o. | Croatian legal form written in lower case |
| V0011 | Gpt Space & Co | GPT Space & Co | acronym |
| V0013 | Rsm Uk Corporate Finance Llp | RSM UK Corporate Finance LLP | legal form, acronym |
| V0014 | Amazon Web Services Llc | Amazon Web Services LLC | legal form |
| V0015 | Telefonica Global Services Gmbh | Telefonica Global Services GmbH | legal form |
| V0016 | Hr Solution International Gmbh | HR Solution International GmbH | legal form, acronym |
| V0017 | 4I Advisory Services | 4i Advisory Services | brand casing |
| V0022 | Wework Singapore Pte. Ltd. | WeWork Singapore Pte. Ltd. | brand casing |
| V0026 | Linkedin Ireland Limited | LinkedIn Ireland Limited | brand casing |

## 4. Entity merge map

Policy (decision of 2026-11-10, `docs/decisions.md`): merge only when it is the same vendor relationship under a changed or variant name (a rename, a spelling variant, the same contract moved between entities). Where entities share a parent or brand but supply different products or contracts, or share a lineage, the vendors stay separate and are tied together through `link_group`.

386 rows become 382 vendors (383 if the proposed merge is reversed).

### Merges

| Canonical vendor | group_id | Rows | 12-month cost | Status | Relationship | Confidence | Reason |
|---|---|---|---|---|---|---|---|
| Navan | V0003 | V0003, V0024 | $415,913 | merge | renamed entity | high | TripActions Inc renamed itself Navan Inc in 2023; both rows are the same travel and expense platform |
| AWS | V0014 | V0014, V0103 | $111,552 | merge | same service, entity name variant | high | one AWS relationship, the same cloud service and customer agreement, billed under the Inc. and LLC entity names |
| 4i | V0017 | V0017, V0072 | $83,978 | proposed merge | same group, other entity | medium | shared and unusual 4i brand, both advisory or consulting in India; to be confirmed or reversed by web verification |
| TM Forum | V0025 | V0025, V0249 | $58,070 | merge | spelling variant | high | Tmforum and Tm Forum are two spellings of the same association |

### Links

Linked vendors stay separate rows and separate vendors. The combined spend is shown because one negotiation can cover the group; it is not added to any one vendor.

| Link group | Type | Rows | Combined 12-month cost | Reason |
|---|---|---|---|---|
| Salesforce | shared parent | V0002 Salesforce UK Ltd; V0173 Slack Technologies Limited | $3,119,215 | Slack has been a Salesforce company since 2021, so it goes into the same renewal |
| Amazon | shared parent | V0014 Amazon Web Services LLC; V0103 Amazon Web Services Inc.; V0203 Amazon.co.uk; V0291 Amazon (Aus) | $112,893 | AWS and the Amazon marketplaces in the UK and Australia share a parent but are different services and purchases |
| Telefónica | same brand, separate entities | V0015 Telefonica Global Services GmbH; V0093 Telefónica Compras Electrónicas S.L. | $96,037 | two Telefónica group entities (Global Services GmbH, Compras Electrónicas S.L.); what each payment is goes to Finance |
| HR Solution International | same brand, separate entities | V0016 HR Solution International GmbH; V0090 Hrsolution International AG | $87,810 | a GmbH and an AG, so two legal entities and presumably two country contracts; a merge only if one contract moved between them |
| Microsoft | shared parent | V0026 LinkedIn Ireland Limited; V0081 Microsoft Ireland Operations Limited; V0125 npm Inc | $68,929 | LinkedIn and npm (through GitHub) are Microsoft companies |
| Bupa | same brand, separate entities | V0047 Bupa; V0071 Bupa Australia | $35,263 | two Bupa entities with separate insurance contracts, one of them Bupa Australia |
| Sodexo and Pluxee | same lineage | V0054 Sodexo SVC India Private Limited; V0128 Pluxee India Private Limited | $21,804 | Pluxee was demerged from Sodexo in 2024; on-site catering and meal cards are different services and contracts (decision of 2026-11-10) |
| Acclime | same brand, separate entities | V0099 Acclime Corporate Services; V0105 Acclime USA, Inc | $10,408 | Acclime's corporate services entity and its US entity, presumably separate engagements |
| ICICI group | shared parent | V0095 ICICI Lombard GIC Ltd; V0143 Cici Prudential Life Insurance Co. Ltd. | $9,167 | ICICI Lombard (general insurance) and ICICI Prudential (life insurance) are separate ICICI group insurers |
| Apple | same brand, separate entities | V0123 Apple Retail UK Ltd; V0172 Apple Pty Ltd; V0175 Apple Distribution International Ltd; V0229 Apple - AMER | $8,256 | four Apple regional entities (UK retail, Australia, Ireland, Americas) with separate purchases |
| Allianz Australia | same brand, separate entities | V0094 Allianz Australia Workers' Compensation (Victoria) Limited; V0212 Allianz WA | $7,069 | Allianz workers' compensation in Victoria and, by the Wa suffix, Western Australia: separate state policies (decision of 2026-11-10) |
| Atlassian | shared parent | V0091 Trello; V0297 Atlassian Pty Ltd | $6,898 | Trello is an Atlassian product |
| SolarWinds | shared parent | V0130 Papertrail Inc; V0311 SolarWinds, Inc | $4,066 | Papertrail is a SolarWinds product |
| GRT Hotels & Resorts | same brand, separate entities | V0171 GRT Hotels And Resorts P Ltd; V0190 Radisson GRT - Unit Of Hotels & Resorts Pvt Ltd | $3,437 | two hotels of the GRT group; the Radisson row names itself a unit of GRT Hotels & Resorts |
| DHL | same brand, separate entities | V0303 DHL; V0336 DHL Express (UK) Ltd | $310 | a bare DHL record and DHL Express (UK); the file does not show that they are one account |

### Reviewed and kept as different vendors

From the near-duplicate search in `01_forensics.md`, candidates that are neither merged nor linked:

| Rows | Verdict | Reason |
|---|---|---|
| V0030 Sveučilište U Zagrebu, Studentski Centar; V0086 Studentski Centar - Split; V0186 Studentski Centar Karlovac | different vendors, same type | three different university student centres (Zagreb, Split, Karlovac) offering the same student-work service |
| V0073 Grad Zagreb, Gradski Ured Za Prostorno Uređenje; V0139 Grad Split | different vendors | two different cities (Zagreb, Split) |
| V0088 Intertrust Singapore Corporate Services Pte Ltd - CSC; V0099 Acclime Corporate Services; V0105 Acclime USA, Inc | different vendors, same type | Intertrust and Acclime both sell corporate secretarial services; only the words Corporate Services are shared |
| V0074 Bijeli Pijesak Obrt Za Poslovno Savjetovanje; V0330 TEB Poslovno Savjetovanje d.o.o. | different vendors | unrelated firms whose names both contain poslovno savjetovanje (business consulting) |
| V0192 Chamiers Recreation Club; V0197 P S Recreation Club | different vendors, same type | two different recreation clubs |
| V0382 Specijalisticka Ordinacija Medicine Rada I Sporta Ina Kardos; V0383 Specijalisticka Ordinacija Medicine Rada Helena Blazic | different vendors, same type | two occupational-medicine practices run by different doctors |
| V0348 Hilton Garden Inn - Zagreb City Hotels d.o.o.; V0372 Garden City d.o.o. | different vendors | share only the words Garden and City |
| V0046 New Star Networks (NSN); V0360 New Block d.o.o. | different vendors | share only the word New |
| V0053 Hrvatski Telekom d.d.; V0318 Hrvatski Nezavisnici Izvoznici Softvera | different vendors | share only Hrvatski (Croatian) |
| V0082 Catering Muring; V0233 Catering Ivić d.o.o. | different vendors, same type | two different caterers |
| V0183 Paint & Fun Vl. Martina Milkova Nikolova; V0315 Paint&Wine, Vl. Stevo Dosen | different vendors, same type | two painting-event sole traders with different owners |
| V0247 Hotel Zonar; V0304 Hotel Laguna d.d. | different vendors, same type | two different hotels |
| V0328 Ustanova Za Zdravstvenu Skrb P.P.; V0384 Ustanova Za Medicinu Rada I Sporta Dr. Novacki | different vendors, same type | two different health institutions |

## 5. Largest vendors after merging

| Rank | Canonical vendor | group_id | Rows | 12-month cost | Share | Cumulative |
|---|---|---|---|---|---|---|
| 1 | Salesforce UK Ltd | V0002 | 1 | $3,117,226 | 39.5% | 39.5% |
| 2 | Navan | V0003 | 2 | $415,913 | 5.3% | 44.8% |
| 3 | BDO LLP | V0004 | 1 | $343,081 | 4.3% | 49.1% |
| 4 | TOG UK Properties Limited | V0005 | 1 | $263,821 | 3.3% | 52.5% |
| 5 | Cloudcrossing BVBA | V0006 | 1 | $208,675 | 2.6% | 55.1% |
| 6 | Zagrebtower d.o.o. | V0007 | 1 | $183,754 | 2.3% | 57.5% |
| 7 | Innovent Spaces Private Limited | V0008 | 1 | $147,348 | 1.9% | 59.3% |
| 8 | Weking d.o.o. | V0009 | 1 | $144,093 | 1.8% | 61.2% |
| 9 | Jensten Insurance Brokers | V0010 | 1 | $142,700 | 1.8% | 63.0% |
| 10 | GPT Space & Co | V0011 | 1 | $133,507 | 1.7% | 64.7% |
| 11 | Aetna Life And Casualty Ltd | V0012 | 1 | $124,661 | 1.6% | 66.2% |
| 12 | RSM UK Corporate Finance LLP | V0013 | 1 | $117,078 | 1.5% | 67.7% |
| 13 | AWS | V0014 | 2 | $111,552 | 1.4% | 69.1% |
| 14 | Telefonica Global Services GmbH | V0015 | 1 | $89,880 | 1.1% | 70.3% |
| 15 | 4i | V0017 | 2 | $83,978 | 1.1% | 71.3% |

Total: $7,887,360 across 382 vendors (386 rows). Linked vendors are ranked separately; see section 4 for link-group totals.

## 6. Analyst hint coverage

`docs/vendor_hints.md` maps its hints to 172 rows; the other 214 rows have no hint and are classified from their names and general knowledge.
