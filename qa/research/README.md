# Research working files

The files that produced the web verification of step 3, copied from the session's scratch space in step 5 (prompt 18) as they ran. Nothing here is edited by the later steps; `qa/verification_log.csv` and `qa/verification_exceptions.csv` are the assembled results.

- `inputs/input_NN*.txt`: the vendor lists given to the research agents, one vendor per line (vendor_id, cleaned name, AP name, 12-month spend, legal-form clue, analyst hint or "no hint", name note). Written by `scripts/research_inputs.py`. Batches were split in halves (a, b) and, where a run stopped at the search limit, continued in a further file (a2, b2, c).
- `findings/batch_NN*_findings.csv`: one row per vendor the agent finished: `vendor_id`, `verified`, `source_url`, `what_it_does`, `country`, `identity_confidence`, `hint_check` (agrees, contradicts or no hint) and `notes`.
- `logs/batch_NN*_log.csv`: every lookup the agent ran, failed ones included: `vendor_id`, `query`, `url_found`, `established`. `logs/claude_log.csv` holds the lookups the main session ran itself (the 4i and Pluxee questions, and rows re-checked while classifying). `scripts/classify_tools.py log` assembled `qa/verification_log.csv` from these files.
- `failed_attempts/`: findings and logs of runs that stopped at the search limit and were re-run; superseded by the files above and kept for completeness.
- The brief every agent worked from is `prompts/research_brief.md`. The per-batch classification lines the builder read are in `qa/classification_lines/`.

URLs that carry a private individual's name are withheld in every file here, as in the assembled log (`docs/decisions.md`, step 3b): the directory's root domain stands in their place with the note "URL withheld: names the owner" or "names an individual". Two downloaded documents and their extracted text, used for one lookup, were not copied: they are third-party files, not the project's work.
