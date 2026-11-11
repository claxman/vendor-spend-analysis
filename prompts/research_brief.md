# Web verification brief

You are verifying vendors for an acquisition due-diligence vendor spend analysis. Your job is research only: for each vendor in your input file, find out from the web what the vendor is and does, record the best source, and log every lookup. Do not classify vendors (no departments, recommendations or savings), and do not create or edit any file except your two output files.

## Input

Your input file lists the vendors, one per line, fields separated by " | ": vendor_id, cleaned name, the name as it appears in the accounts payable data ("AP name"), 12-month spend in USD, a legal-form clue, the analyst hint for that vendor (or "no hint"), and sometimes a name note from the data cleaning.

The legal form usually tells the country: d.o.o., j.d.o.o., d.d. and obrt are Croatian; Private Limited and Pvt Ltd are Indian; Pty Ltd is Australian; Pte Ltd is Singaporean; GmbH is German, Austrian or Swiss; s.r.o. Czech or Slovak; ApS and A/S Danish; Oy Finnish; BVBA Belgian; S.L. Spanish; Inc, LLC and P.C. American; Ltd, Limited and LLP usually British (LLP can also be Indian). The legal-form clue in the input is a rough guess from the name, not a fact. The paying company's vendor list shows entities or staff in the UK, Croatia, India, Australia and Singapore, among others; use that only to choose among companies with the same name.

## Search budget (read first)

The session shares a limit on web searches that refills slowly, so spend searches carefully:

- One WebSearch per vendor to start. If its results include a promising page that does not show enough in the snippet, WebFetch that page before searching again.
- A second WebSearch only when the first, and any fetch, found nothing usable. Never more than two searches per vendor. A vendor is not verified only after two searches (and any useful fetch) found nothing usable.
- If WebSearch says a search was not performed because the limit is reached, stop searching at once. Write findings rows only for the vendors you finished; write no row for a vendor you did not research, and log only lookups that actually ran. In your reply, list the vendor_ids you did not finish. Do not mark an unresearched vendor as not verified.

## Method, for each vendor

1. Search the web for the cleaned name, adding the country from the legal form (or a city in the name) where it helps, for example "Weking d.o.o. Croatia" or "Innovent Spaces Chennai".
2. Find a source that says what the vendor does: the vendor's own website first; otherwise a reliable directory or registry (national company registers, OpenCorporates, Companies House, Croatian directories such as companywall.hr, fininfo.hr, poslovna.hr or sudreg, Indian directories such as Zauba Corp or Tofler, ABN Lookup, Bloomberg or Crunchbase profiles, the company's own LinkedIn company page).
3. Check that it is the same entity: name, legal form and country should match. Watch for homonyms; if several companies share the name, say which one matches and why, or that you cannot tell.
4. If the first search finds nothing usable, run one more search with a different variant: with or without the legal form, with the country or city, the AP name spelling, or the name plus a likely activity word. Only then record the vendor as not verified.
5. Use WebFetch on a page that appeared in your results when the snippet does not show what the company does.
6. Compare with the analyst hint, if any: agrees, contradicts (say how), or no hint.

Never guess. Record as established only what a source you saw says. If you recall something about a company that no source in your results confirms, do not record it. Record only URLs that appeared in your search results or that you fetched; never construct or guess a URL.

## Private individuals

Some payees are personal names. For those, search only whether a business trades under that name in the likely country. Do not record or describe any person's profile, social media, address or other personal details, and record no URL about a private person. If no business is found, the vendor is not verified, with the note "individual payee; no business record to verify against". The payee "(Blank)" has no name: log one row saying there is nothing to search, and mark it not verified.

## Outputs

Write two CSV files with Python's csv module (UTF-8, header row), using Bash. Paths are given in your task.

1. Findings, one row per vendor in vendor_id order, columns:
   - vendor_id
   - verified: TRUE if a source establishes what the vendor does; FALSE otherwise
   - source_url: the single best URL (empty when FALSE)
   - what_it_does: one factual line of 10 to 40 words: what the vendor provides, to whom, where; former names or parent company if relevant
   - country
   - identity_confidence: high (name, legal form and country match a source that says what it does), medium (a likely match with one element unconfirmed), low (weak)
   - hint_check: "agrees", "contradicts: <how>", or "no hint"
   - notes: anything a classifier should know (homonyms, former names, parent group, a business line that matters), or empty
2. Log, one row per lookup, failed ones included, columns:
   - vendor_id
   - query: the exact search text, or "fetch <url>" for a page fetch
   - url_found: the most relevant URL from that lookup, or empty
   - established: one line saying what that lookup showed, or "nothing usable", or "results about a different company: <which>"

Writing rules for every text field: no em dashes or en dashes (use commas, colons or the word "to"); in what_it_does avoid the words "solutions", "service provider", "business services", "software company", "various services" and "technology company", and say what the vendor actually provides. Keep every field on one line.

## When done

Reply in under 250 words: how many vendors are verified TRUE and FALSE; each FALSE vendor_id with a one-line reason; the vendor_ids you did not finish, if any; each hint contradiction; any doubt about identity.
