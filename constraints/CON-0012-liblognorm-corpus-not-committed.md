---
id: CON-0012
status: Accepted
subject: Parity corpus provenance
---

# CON-0012 — liblognorm's corpus is not committed

`scratch/parity_check.py` scrapes its test cases out of liblognorm's `tests/*.sh`
at run time, and filters them twice before use. No case is committed to the
repository.

## Consequences

- The corpus exists only as long as the upstream source is reachable and the
  scraper still parses it. Deleting the workflow deletes the corpus with no
  warning and no diff.
- The case count is therefore not a documented number but a run-time outcome.
  Figures of 374 and 381 have both been recorded; neither has been verified, and
  they cannot both be right.
- Extracting and committing the corpus is a one-way door: it must happen before
  the scraper is retired, not after.
