# Recommendation rules

Every vendor gets exactly one recommendation from {Terminate, Consolidate, Optimize} and a one-sentence rationale. Rows merged into one vendor in `qa/vendor_groups.csv` get one recommendation for the whole group. A recommendation is a decision label: any savings figure attached to it is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`).

The context is fixed by the brief: the company has been acquired by a remote-first parent that has its own talent, finance and legal functions.

## Consolidate

Two or more vendors serve the same function, or the same vendor is paid through more than one entity. The cases named in the brief:

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

Statutory payees and customer-mandated fees are also Optimize, with the rationale "non-discretionary, excluded from the savings base".

## Vendors under $1,000

Still classified. Terminate if non-essential; otherwise Optimize with the note "fold into tail-spend policy".

## Order of application (proposed by Claude, to confirm or change)

The rules above can point two ways for the same vendor; for example, Navan is paid through two entities (Consolidate) but is named under Optimize. The first step that applies decides.

1. Statutory payee or customer-mandated fee: Optimize, "non-discretionary, excluded from the savings base". This comes first so that nothing non-discretionary is terminated or consolidated.
2. Named in the Optimize list (Salesforce, AWS, Navan, the insurance broker, LinkedIn): Optimize. Where the vendor is paid through two entities, the rationale names the one entity to keep.
3. Unidentified payee: Terminate until identified.
4. Under $1,000 in 12-month spend, measured on the merged vendor: Terminate if non-essential, otherwise Optimize with "fold into tail-spend policy".
5. In a Terminate category: Terminate, stating any condition.
6. The same vendor paid through more than one entity: Consolidate, naming the entity to keep.
7. The same function as other vendors: Consolidate, naming the vendor to keep.
8. Anything else essential: Optimize, naming the lever (price, volume or policy).

## Writing the rationale

One sentence that names something specific. For Consolidate, it names the vendor or entity to keep; for Optimize, the lever; for Terminate, what makes the vendor redundant or the condition that would. Plain wording, no em dashes, none of the banned phrases from `CLAUDE.md`.
