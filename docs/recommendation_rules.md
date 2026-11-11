# Recommendation rules

Every row of the sheet, all 386 of them, gets exactly one recommendation from {Terminate, Consolidate, Optimize} and a one-sentence rationale. Rows in a merge group, or in a link group marked `shared` in `qa/vendor_groups.csv`, carry the same recommendation; every grouped row's rationale names its group (see "Merged and linked rows" below). A recommendation is a decision label: any savings figure attached to it is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`).

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

Employee hardware is also Consolidate, into group IT procurement, not Terminate (decision of 2026-11-10, step 2e): the four Apple entities, HP, Currys, Magazin Računalni Sistemi, Sniper Systems and E-Disti. Their rationale names group IT procurement as the channel to keep.

Name the retained vendor in the rationale. Where the vendor to keep is the parent's incumbent and is not in this file, the rationale names it by role ("the parent's group insurance programme", "the parent's finance system"), because the parent's vendors are not known.

## Terminate

Redundant after acquisition by a remote-first parent with its own talent, finance and legal functions:

- recruiting agencies
- employer-of-record and payroll outsourcing where the parent's payroll covers the country
- deal and transaction advisers (non-recurring)
- perks, events, gifts and memberships without a commercial justification
- food, groceries, gifts and marketplace purchases through AP (employee hardware is not in this category: see Consolidate)
- unidentified payees until identified

Where the case depends on something this file cannot show, such as whether the parent's payroll covers a country, the rationale states the condition ("terminate once the parent's payroll covers Germany").

An adviser whose spend plausibly includes sale-related work as well as its usual work (BDO, Bisley Law, Grant Thornton) is not one of the non-recurring deal and transaction advisers: its spend stays in the recurring base (see "Recurring base" below, step 2e).

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

A savings assumption is the share of addressable spend the savings script counts as saved, written next to the figure it produces (`CLAUDE.md`). Two were fixed here first; the rest were set lever by lever in step 4, as low, base and high cases with a without-decision case and a year-1 factor (`docs/savings_assumptions.md`, `outputs/analysis/savings.md`).

| Spend | `is_addressable` | Savings assumption | Rationale |
|---|---|---|---|
| Student labour (cluster Student labour) | TRUE | 0% | workforce cost, set by the hiring plan, not a vendor action |
| Statutory payees, customer-mandated fees, Telefónica | FALSE | none: outside the savings base | non-discretionary, excluded from the savings base |

Every assumption is also entered in `docs/savings_assumptions.md` with its `depends_on` tag (next section).

## Savings that depend on the acquirer's decisions

Decided in steps 2e and 2f (prompts 13 and 14). A savings assumption that holds only if the acquirer makes a particular choice is tagged with that decision's name in a `depends_on` column, in `docs/savings_assumptions.md` and in `outputs/analysis/savings.md` next to the figure. There are ten decisions: the remote operating model, the group talent function, the group insurance programme, the group auditor, the parent CRM instance and group IT procurement (step 2e), group payroll, group systems and group legal (step 2f), and group engineering sourcing (step 4). A lever that is purely a vendor action carries `none`; the cases named in step 2f were the Salesforce licence audit, AWS savings plans, Navan policy and the insurance re-broke, and from step 4 the licence audit is restated as the Salesforce platform agreement lever while the re-broke is the without-decision case of the commercial insurance lever. `docs/savings_assumptions.md` gives the tag names, and the tag, the percentages and the year-1 factor of every lever.

The memo presents the Top 3 as decisions with their value, not as facts about the parent: what the CEO and CFO would decide, what it is worth a year under the stated assumption, and which decision the value depends on. The spend file shows what the company spends, not what the parent has or runs.

## Recurring base

`is_recurring` TRUE puts a row's spend in the recurring base. BDO (`V0004`), Bisley Law (`V0018`) and Grant Thornton (`V0029`) stay in it although their spend plausibly includes sale-related work (step 2e). When `insights.md` is written, it notes that the recurring figure is therefore likely lower than shown.

## Merged and linked rows

The sheet is filled per row (step 2c): all 386 rows get their own department, description and recommendation, and merges and links exist only for ranking and savings roll-ups. Which rows share a recommendation (step 2d):

- One recommendation per merge group, the same vendor relationship: Navan, AWS, TM Forum, 4i and Pluxee. The web verification of step 3 confirmed the 4i merge and found Sodexo SVC India to be Pluxee India's former name.
- One recommendation per link group whose products are the same kind of service: the same-brand groups (Apple, Bupa, HR Solution International, Acclime, DHL, Telefónica, Allianz Australia, GRT Hotels & Resorts) and the shared-parent groups Salesforce with Slack, Atlassian with Trello, SolarWinds with Papertrail, and the two ICICI insurers. These are marked `shared` in the `link_recommendation` column of `qa/vendor_groups.csv`.
- A recommendation per row for shared-parent or same-lineage links whose rows are different services: Amazon (AWS and the two marketplaces) and Microsoft (Microsoft 365, LinkedIn and npm). These are marked `per row`.
- In every case each grouped row's rationale names its group, for example "one of two Navan entities" or "part of the Microsoft group". Where the row's own name already contains the group's name, the rationale also shows the grouping in words such as "both", "group" or "entities".
- Size tests such as the under-$1,000 rule use the group total for a group that shares a recommendation, and the row otherwise.

Outcomes fixed for the per-row groups (step 2d): AWS is Optimize (Optimize list); Amazon.co.uk and Amazon (Aus) are Terminate (marketplace purchases through AP); Microsoft 365 is Consolidate (two productivity suites); LinkedIn is Optimize (seat review); npm follows the developer-tool rule: department Engineering, cluster Software subscriptions (non-Salesforce), and a recommendation from the order of application below, like any other developer tool.

## Order of application (approved 2026-11-10)

The rules above can point two ways for the same vendor; for example, Navan is paid through two entities (Consolidate) but is named under Optimize. The first step that applies decides. For a group that shares a recommendation the steps are applied once, to the group; the rows of a per-row link group are taken one by one. Step 4 was added in step 2e.

1. Statutory payee, customer-mandated fee or Telefónica payment: Optimize, not addressable, "non-discretionary, excluded from the savings base"; for Telefónica the rationale adds that rebates would belong against revenue. This comes first so that nothing non-discretionary is terminated or consolidated.
2. Student labour: Optimize, addressable, 0% savings assumption, rationale "workforce cost, set by the hiring plan, not a vendor action". Label confirmed 2026-11-10 (step 2c).
3. Named in the Optimize list (Salesforce, AWS, Navan, the insurance broker, LinkedIn): Optimize. Where the vendor is paid through two entities, the rationale names the one entity to keep.
4. Employee hardware (the four Apple entities, HP, Currys, Magazin Računalni Sistemi, Sniper Systems, E-Disti): Consolidate into group IT procurement, whatever the amount. It comes before the size test so that the small hardware rows are consolidated too.
5. Unidentified payee: Terminate until identified.
6. Under $1,000 in 12-month spend, measured on the group total for a group that shares a recommendation, otherwise on the row: Terminate if non-essential, otherwise Optimize with "fold into tail-spend policy".
7. In a Terminate category: Terminate, stating any condition.
8. The same vendor paid through more than one entity, whether merged or linked as the same brand: Consolidate, naming the entity to keep.
9. The same function as other vendors: Consolidate, naming the vendor to keep.
10. Anything else essential: Optimize, naming the lever (price, volume or policy).

## Writing the rationale

One sentence that names something specific. For Consolidate, it names the vendor or entity to keep; for Optimize, the lever; for Terminate, what makes the vendor redundant or the condition that would. For a row in a merge or link group, it also names the group. Plain wording, no em dashes, none of the banned phrases from `CLAUDE.md`.
