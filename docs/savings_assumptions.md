# Savings assumptions

The register of the assumptions behind the savings figures. Every savings figure is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`). `outputs/analysis/savings.md`, which the savings script writes, repeats each assumption and its `depends_on` tag next to the figure it produces. Decided in steps 2e and 2f (prompts 13 and 14); see `docs/decisions.md`.

## Acquirer decisions

Some savings happen only if the acquirer makes a particular choice. Every savings assumption that depends on such a choice is tagged with the decision's name in a `depends_on` column, here and in `savings.md`. The spend file shows what the company spends; it does not show what the parent has, runs or intends. A saving that needs one of these choices is therefore the value of a decision, not a fact about the parent.

| depends_on | The decision | Where it mainly applies (cost cluster) |
|---|---|---|
| `remote_operating_model` | Adopt a remote operating model for the company in place of its own offices and coworking | Office footprint; Office running costs |
| `group_talent_function` | Hand the company's hiring to the group talent function | Recruiting and HR outsourcing |
| `group_insurance_programme` | Move the company's insurance cover into the group insurance programme | Insurance and benefits |
| `group_auditor` | Appoint the group auditor for the company's entities | Audit, tax, accounting and corporate services |
| `parent_crm_instance` | Move the company's CRM onto the parent's CRM instance | Salesforce platform |
| `group_it_procurement` | Buy employee hardware through group IT procurement | Cloud, telecom and IT (the employee hardware rows) |
| `group_payroll` | Pay the company's staff through group payroll in place of employer-of-record and payroll outsourcing | Recruiting and HR outsourcing |
| `group_systems` | Migrate the company's HR and finance systems to the parent's HRIS and ERP | Software subscriptions (non-Salesforce) |
| `group_legal` | Consolidate the company's law firms into the group's law firm panel | Legal |

The first five are named in prompt 13, and `group_it_procurement` was added there for the hardware rule. `group_payroll`, `group_systems` and `group_legal` were added in step 2f (prompt 14).

Rules for the tag:

- A lever that is purely a vendor action, one the company can take with its own vendors without any of the decisions above, carries `depends_on` = `none`. The cases named in step 2f are the Salesforce licence audit, AWS savings plans, Navan policy and the insurance re-broke.
- Every other assumption carries the name of each decision it depends on, separated by commas.
- A new decision gets a row in the table above, with its name and what it means, before any assumption uses it.
- The memo presents each of the Top 3 as a decision with its value, naming the decision it depends on, not as a fact about the parent.
- Check S6 in `qa/check_outputs.py` enforces the first three rules on the table below.

## Assumptions

One row per lever in `docs/recommendation_rules.md`. Each lever's savings assumption is set in the savings step, with its basis; only the two fixed rows at the end have one now. Levers that depend on a decision come first, in the order of the table above, then the vendor actions, then the fixed rows.

| Lever | Rule | Applies to | Savings assumption | depends_on |
|---|---|---|---|---|
| Coworking and offices | Consolidate: coworking providers | offices and coworking, with their running costs (Office footprint, Office running costs) | set in the savings step | `remote_operating_model` |
| Recruiting agencies | Terminate: recruiting agencies | recruiting agencies, once the group talent function does the hiring | set in the savings step | `group_talent_function` |
| LinkedIn seat review | Optimize list: LinkedIn, seat review | LinkedIn seats, in Recruiting and HR outsourcing: how many the company needs depends on who does its hiring | set in the savings step | `group_talent_function` |
| Insurers | Consolidate: insurers across countries | the company's policies, moved into the group insurance programme | set in the savings step | `group_insurance_programme` |
| Audit and accounting | Consolidate: auditors and accountants across countries | auditors and accountants across the company's countries | set in the savings step | `group_auditor` |
| CRM instance | Acquirer decision (step 2e) | Salesforce platform; how much of the Salesforce spend it can reach depends on Finance question 2, what the contract covers | set in the savings step | `parent_crm_instance` |
| Employee hardware | Consolidate: employee hardware (step 2e) | the four Apple entities, HP, Currys, Magazin Računalni Sistemi, Sniper Systems and E-Disti, bought through group IT procurement | set in the savings step | `group_it_procurement` |
| Payroll and employer of record | Terminate: employer-of-record and payroll outsourcing | employer-of-record and payroll outsourcing, country by country as group payroll covers it | set in the savings step | `group_payroll` |
| HR and finance systems | Consolidate: HR and finance systems the parent already runs | HR and finance systems, migrated to the parent's HRIS and ERP | set in the savings step | `group_systems` |
| Law firms | Consolidate: law firms | law firm panel consolidation | set in the savings step | `group_legal` |
| Salesforce licence audit | Optimize list: Salesforce licences | audit and right-size the Salesforce licences at renewal | set in the savings step | `none` |
| AWS savings plans | Optimize list: AWS; Consolidate: cloud accounts under two entities | savings plans, and one organisation for the accounts under two entities | set in the savings step | `none` |
| Navan policy | Optimize list: Navan | travel policy, one entity | set in the savings step | `none` |
| Insurance re-broke | Optimize list: insurance broker | the broker takes the company's policies back to market; moving the cover into the group programme is the Insurers lever above | set in the savings step | `none` |
| Productivity suites | Consolidate: two productivity suites | Google Workspace and Microsoft 365, keeping one | set in the savings step | `none` |
| Work-management and integration tools | Consolidate: several work-management or integration tools | the overlapping tools, keeping the fewest that cover the need | set in the savings step | `none` |
| Contact-data tools | Consolidate: several contact-data tools | the overlapping contact and intent data tools | set in the savings step | `none` |
| HubSpot | Consolidate: HubSpot alongside Salesforce marketing | HubSpot, where Salesforce marketing covers the need | set in the savings step | `none` |
| One entity per vendor | Order of application, step 8 | a vendor paid through more than one entity, consolidated onto the entity to keep | set in the savings step | `none` |
| Perks, events, gifts and memberships | Terminate: without a commercial justification | perks, events, gifts and memberships | set in the savings step | `none` |
| Purchases through AP | Terminate: food, groceries, gifts and marketplace purchases through AP | food, groceries, gifts and marketplace purchases | set in the savings step | `none` |
| Unidentified payees | Terminate: until identified | payees whose function is not known | set in the savings step | `none` |
| Deal and transaction advisers | Terminate: non-recurring | deal and transaction advisers, whose work ends with the sale; BDO, Bisley Law and Grant Thornton stay in the recurring base (step 2e) | set in the savings step | `none` |
| Tail spend | Vendors under $1,000 | terminate the non-essential, fold the rest into tail-spend policy | set in the savings step | `none` |
| Other same-function vendors | Order of application, step 9 | vendors with the same function as others, consolidated onto the one to keep | set in the savings step | `none` |
| Other essential vendors | Order of application, step 10 | price, volume or policy | set in the savings step | `none` |
| Student labour | Order of application, step 2 | cluster Student labour | 0%: workforce cost, set by the hiring plan, not a vendor action | `none` |
| Outside the savings base | Order of application, step 1 | statutory payees, customer-mandated fees and the Telefónica payments (`is_addressable` FALSE) | not counted: non-discretionary, excluded from the savings base | `none` |

The two fixed rows count no saving, so no decision changes them.
