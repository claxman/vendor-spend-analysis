# Prompt log

Every prompt given to Claude for this project, verbatim, in the order received.

## Prompt 1 (2026-11-10)

```text
Initialise a git repo here, create CLAUDE.md with the content I paste next, create the folders data/raw, outputs/batches, outputs/analysis, scripts, qa, prompts, docs/evidence, add a .gitignore for Python, make the first commit, then create a public GitHub repo named vendor-spend-analysis with gh and push.
```

## Prompt 2 (2026-11-10)

Pasted content for CLAUDE.md:

```text
# Vendor Spend Analysis (acquisition due diligence)

Role: I am the VP of Operations of an acquired company. The final memo is for the CEO and CFO of the parent.
Input: data/raw/vendor_analysis_assessment.xlsx (about 400 vendors, 12 months of spend; real vendors with modified names and costs). Never modify the raw file.
Outputs: outputs/vendors_classified.csv, outputs/analysis/, outputs/top3_opportunities.md, outputs/methodology.md, outputs/memo.md, README.md.

Rules
- Never invent facts about a vendor or the company. If a vendor's function cannot be inferred from its name, say so and set confidence=low.
- Descriptions are one line and specific: what the vendor does and for which team. Banned phrases: "business services", "software company", "service provider", "solutions", "various services", "technology company".
- Departments only from docs/taxonomy.md. Recommendations only from {Terminate, Consolidate, Optimize}, each with a one-sentence rationale.
- Every savings figure is computed by a script from the spend data, with its assumption written next to it.
- Every number in the memo must trace to a file in outputs/analysis.
- Append every prompt I give you to prompts/log.md verbatim before acting on it.
- Commit after each step with a message naming the step.
- No em dashes anywhere.
```
