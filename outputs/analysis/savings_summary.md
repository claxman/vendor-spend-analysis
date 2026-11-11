# Presentation figures

Written by `scripts/03_savings.py` with `outputs/analysis/savings.md`. These are the figures the Top 3, the memo, the methodology and the README may quote. Every dollar figure is rounded to the nearest $1,000 and every total is the sum of the rounded lines above it, so that parts always add to totals; percentages are whole numbers of the rounded total spend. The exact figures are in `savings.md` and `savings.csv`.

## Spend and savings

| Measure | Figure |
|---|---|
| Total spend, 12 months (the sum of the opportunity lines below) | $7,887,000 |
| Largest vendor, Salesforce UK, and its share of spend | $3,117,000 (40%) |
| Run-rate saving, low | $1,566,000 |
| Run-rate saving, base | $2,229,000 |
| Run-rate saving, high | $3,097,000 |
| Base saving as a share of spend | 28% |
| High saving as a share of spend | 39% |
| Year-1 saving | $1,209,000 |
| Year-1 saving as a share of spend | 15% |
| Saving from vendor action alone, with no group decision | $1,264,000 |
| Vendor action alone as a share of spend | 16% |
| Value of the group decisions together (base minus vendor action alone) | $965,000 |

## Opportunities

Base is the run-rate saving the documents quote. Year 1 is the share of the base live in the first 12 months. "Without the decision" is what vendor action alone achieves; the value of the decision is the difference.

| Opportunity | Spend | Low | Base | High | Year 1 | Without the decision | Value of the decision |
|---|---|---|---|---|---|---|---|
| Salesforce platform agreement | $3,383,000 | $335,000 | $515,000 | $850,000 | $257,000 | $515,000 | $0 |
| Office exit | $896,000 | $532,000 | $669,000 | $801,000 | $335,000 | $221,000 | $448,000 |
| Back office into group shared services | $1,750,000 | $459,000 | $653,000 | $830,000 | $359,000 | $198,000 | $455,000 |
| Second wave | $1,411,000 | $240,000 | $392,000 | $616,000 | $258,000 | $330,000 | $62,000 |
| Excluded | $447,000 | $0 | $0 | $0 | $0 | $0 | $0 |
| Total | $7,887,000 | $1,566,000 | $2,229,000 | $3,097,000 | $1,209,000 | $1,264,000 | $965,000 |

## Decisions for the group

For each decision only the group can take: the base saving of the moves that depend on it, what vendor action alone achieves without it, and the difference as the value of the decision.

| Decision | Spend | With the decision | Without it | Value of the decision | Year 1 |
|---|---|---|---|---|---|
| `remote_operating_model` | $967,000 | $698,000 | $232,000 | $466,000 | $349,000 |
| `group_talent_function` | $297,000 | $212,000 | $79,000 | $133,000 | $179,000 |
| `group_insurance_programme` | $390,000 | $62,000 | $27,000 | $35,000 | $31,000 |
| `group_auditor` | $554,000 | $194,000 | $55,000 | $139,000 | $78,000 |
| `parent_crm_instance` | $32,000 | $26,000 | $3,000 | $23,000 | $6,000 |
| `group_it_procurement` | $51,000 | $5,000 | $3,000 | $2,000 | $3,000 |
| `group_payroll` | $110,000 | $22,000 | $2,000 | $20,000 | $11,000 |
| `group_systems` | $102,000 | $81,000 | $10,000 | $71,000 | $20,000 |
| `group_legal` | $178,000 | $53,000 | $18,000 | $35,000 | $32,000 |
| `group_engineering_sourcing` | $212,000 | $64,000 | $21,000 | $43,000 | $32,000 |
| Total | $2,893,000 | $1,417,000 | $450,000 | $967,000 | $741,000 |

## Cost of delay

The two decisions the memo asks for, valued as in the Opportunities table (base minus without the decision), and what each month of delay costs: one twelfth of their value together.

| Measure | Figure |
|---|---|
| Value of the remote operating model (the Office exit line) | $448,000 |
| Value of the group shared functions (the Back office line) | $455,000 |
| The two decisions together | $903,000 |
| Cost of each month of delay, one twelfth of the two together | $75,000 |

## Spend that falls away without action

Deal and one-off costs that end on their own; they carry no saving in the model.

| Spend | Rows | Figure |
|---|---|---|
| M&A and transaction costs | 4 | $227,000 |
| One-off spend that falls away | 46 | $47,000 |
| Total | 50 | $274,000 |

## Spend that must not be cut

Payees that customers, regulators or employment terms require, or whose fee is contingent on cash recovered.

| Spend | Rows | Figure |
|---|---|---|
| Customer-mandated platform fees (Telefónica, Ariba) | 3 | $97,000 |
| Software escrow for customer contracts | 1 | $3,000 |
| ISO certification audits | 1 | $3,000 |
| Statutory workers' compensation and occupational health | 8 | $9,000 |
| Taxes, government fees, regulators and the depository | 6 | $16,000 |
| Salary-sacrifice schemes (cycle to work, novated leasing) | 2 | $7,000 |
| Meal and benefit cards | 2 | $22,000 |
| The contingent-fee R&D tax credit adviser | 1 | $14,000 |
| Total | 24 | $171,000 |

## Verification

| Measure | Figure |
|---|---|
| Rows verified online, from the vendor's own site or a reliable directory | 319 of 386 |
| Spend verified online | $7,791,000 (99%) |
| Rows left unconfirmed | 67 ($96,000) |

## Second-pass review

Stage 1: an independent read of every row against its research finding and the rules, without the web. Stage 2: fresh web verification, with neither the hint nor the first-pass row, of every flagged row, every row at or above $10,000 and a random sample.

| Measure | Figure |
|---|---|
| Stage 1 rows reviewed | 386 of 386 |
| Stage 1 rows flagged | 18 |
| Stage 2 rows verified fresh | 142 of 386 |
| Stage 2 spend covered | $7,501,000 (95%) |
| Stage 2 rows whose reading changed (department, function, group or recommendation) | 5 |
| Stage 2 agreement with the first pass | 96% |
| Rows changed by the review, any field | 25 |
