# Recommendation rules

Every row of the sheet, all 386 of them, gets exactly one recommendation from {Terminate, Consolidate, Optimize} and a one-sentence rationale. Rows in a merge or link group in `qa/vendor_groups.csv` carry the same recommendation, and each rationale names the group (see "Merged and linked rows" below). A recommendation is a decision label: any savings figure attached to it is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`).

The context is fixed by the brief: the company has been acquired by a remote-first parent that has its own talent, finance and legal functions.

## Consolidate

Two or more vendors serve the same function, or the same vendor is paid through more than one entity (merged in `qa/vendor_groups.csv`, or linked there as the same brand through separate entities). The cases named in the brief:

- insurers across countries
- auditors and accountants across countries
- law firms
- coworking providers
- cloud accounts under two entities
- two productivity suites
- several work-management or integration tools
- several contact-data tools
- HubSpot alongside Salesforce marketing
- HR and finance systems the parent already runs

Name the retained vendor in the rationale. Where the vendor to keep is the parent's incumbent and is not in this file, the rationale names it by role ("the parent's group insurance programme", "the parent's finance system"), because the parent's vendors are not known.

## Terminate

Redundant after acquisition by a remote-first parent with its own talent, finance and legal functions:

- recruiting agencies
- employer-of-record and payroll outsourcing where the parent's payroll covers the country
- deal and transaction advisers (non-recurring)
- perks, events, gifts and memberships without a commercial justification
- consumer retail purchases through AP
- unidentified payees until identified

Where the case depends on something this file cannot show, such as whether the parent's payroll covers a country, the rationale states the condition ("terminate once the parent's payroll covers Germany").

## Optimize

Essential sole vendors where the lever is price, volume or policy:

- Salesforce licences: audit and right-size at renewal
- AWS: savings plans, one organisation
- Navan: travel policy, one entity
- insurance broker: re-broke under the group programme
- LinkedIn: seat review

Statutory payees and customer-mandated fees are also Optimize, with the rationale "non-discretionary, excluded from the savings base". Neither is addressable.

The Telefónica payments (`V0015`, `V0093`) are a question for Finance: fees, rebates or connectivity. Until Finance answers they are classified Sales, Optimize, not addressable, and the rationale says that if they are rebates they belong against revenue rather than in vendor spend (decision of 2026-11-10).

## Vendors under $1,000

Still classified. Terminate if non-essential; otherwise Optimize with the note "fold into tail-spend policy".

## Addressability and savings assumptions

Every row carries `is_addressable` (decision of 2026-11-10):

- FALSE for statutory payees (taxes, government and municipal fees, regulators and statutory registrations, statutory workers' compensation and occupational health) and for customer-mandated fees, the Telefónica payments included. They are excluded from the savings base.
- TRUE for everything else, student labour included.

A savings assumption is the share of addressable spend the savings script counts as saved, written next to the figure it produces (`CLAUDE.md`). Two are fixed now; the rest are set lever by lever in the savings step.

| Spend | `is_addressable` | Savings assumption | Rationale |
|---|---|---|---|
| Student labour (cluster Student labour) | TRUE | 0% | workforce cost, set by the hiring plan, not a vendor action |
| Statutory payees, customer-mandated fees, Telefónica | FALSE | none: outside the savings base | non-discretionary, excluded from the savings base |

## Merged and linked rows

The sheet is filled per row (decision of 2026-11-10, step 2c): all 386 rows get their own department, description and recommendation, and merges and links exist only for ranking and savings roll-ups.

- Rows in one merge or link group carry the same recommendation, decided once for the group.
- Each of their rationales names the group, for example "one of two Navan entities" or "part of the Bupa link group".
- Size tests, such as the under-$1,000 rule, use the group total.
- Open point: the Amazon and Microsoft shared-parent groups mix products these rules treat differently; see `docs/decisions.md`, step 2c, point 4. Their department and description can be set now; their recommendations wait until it is settled.

## Order of application (approved 2026-11-10)

The rules above can point two ways for the same vendor; for example, Navan is paid through two entities (Consolidate) but is named under Optimize. The first step that applies decides. For a merge or link group the steps are applied once, to the group.

1. Statutory payee, customer-mandated fee or Telefónica payment: Optimize, not addressable, "non-discretionary, excluded from the savings base"; for Telefónica the rationale adds that rebates would belong against revenue. This comes first so that nothing non-discretionary is terminated or consolidated.
2. Student labour: Optimize, addressable, 0% savings assumption, rationale "workforce cost, set by the hiring plan, not a vendor action". Label confirmed 2026-11-10 (step 2c).
3. Named in the Optimize list (Salesforce, AWS, Navan, the insurance broker, LinkedIn): Optimize. Where the vendor is paid through two entities, the rationale names the one entity to keep.
4. Unidentified payee: Terminate until identified.
5. Under $1,000 in 12-month spend, measured on the merge or link group total, or on the row when it is in no group: Terminate if non-essential, otherwise Optimize with "fold into tail-spend policy".
6. In a Terminate category: Terminate, stating any condition.
7. The same vendor paid through more than one entity, whether merged or linked as the same brand: Consolidate, naming the entity to keep.
8. The same function as other vendors: Consolidate, naming the vendor to keep.
9. Anything else essential: Optimize, naming the lever (price, volume or policy).

## Writing the rationale

One sentence that names something specific. For Consolidate, it names the vendor or entity to keep; for Optimize, the lever; for Terminate, what makes the vendor redundant or the condition that would. For a row in a merge or link group, it also names the group. Plain wording, no em dashes, none of the banned phrases from `CLAUDE.md`.
