# Savings assumptions

The register of the assumptions behind the savings figures. Every savings figure is computed by a script from the spend data, with its assumption written next to it (`CLAUDE.md`). `outputs/analysis/savings.md`, which the savings script writes, repeats each assumption and its `depends_on` tag next to the figure it produces. Decided in step 2e (prompt 13); see `docs/decisions.md`.

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

The first five are named in prompt 13. `group_it_procurement` was added for the hardware rule in the same prompt, under which employee hardware is consolidated into group IT procurement.

Rules for the tag:

- An assumption that needs none of these decisions, such as a lever the company can pull on its own at renewal, carries `depends_on` = `none`.
- An assumption that needs more than one decision lists every name, separated by commas.
- A new decision gets a row in the table above, with its name and what it means, before any assumption uses it.
- The memo presents each of the Top 3 as a decision with its value, naming the decision it depends on, not as a fact about the parent.

## Assumptions

| Lever | Applies to | Savings assumption | depends_on | Basis |
|---|---|---|---|---|
| Student labour | cluster Student labour | 0% | `none` | workforce cost, set by the hiring plan, not a vendor action (step 2b) |
| Outside the savings base | statutory payees, customer-mandated fees and the Telefónica payments (`is_addressable` FALSE) | not counted: outside the savings base | `none` | non-discretionary, excluded from the savings base (step 2b) |

The assumptions for the other levers are set lever by lever in the savings step, each with its `depends_on` tag.
