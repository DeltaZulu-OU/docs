# LogCluster upstream alignment — preliminary evidence register

Date: 2026-11-13. Status: **unverified external measurements; not a reproduced verification report**.

## Supplied observations

| Comparison | Supplied result | Verification |
| --- | --- | --- |
| Candidate patterns/support with all custom merges removed | 7,039/7,039 clusters | Not independently reproduced; exact upstream commit and flags pending |
| One merge disabled | Approximately 86% alignment | Denominator and mode unspecified |
| Current default merge configuration | Approximately 34% alignment | Denominator and comparator procedure pending |
| Initial defect corpus | Six crashes and 13 over-counts in 48 runs | Tests and corpus not supplied to this repository |
| Local patched mining | Zero crashes and zero over-counts in 48 runs | Supplied report; CI regression pending |

The above values are supplied as project findings. They must not be presented as independently verified results or a release acceptance record.

## Reproducibility fields to complete

- Exact upstream `ristov/logcluster` SHA and command line including disabled `--aggrsup` and `--wweight`.
- Toolchain, operating system, input identity/hash, record ordering, minimum support and separator behavior.
- Canonical comparison procedure for pattern and support pairs; clarify whether sorting, escaping, whitespace or output ranking was normalized.
- Per-mode match counts and percentages, including outlier counts; distinguish exact cluster-set equality from candidate-level percentage.
- Ground-truth accuracy against a licensed Loghub corpus, including precision/recall or template-level F1 and provenance.
- Full tests and CI artifacts for 48-run failure cases and patched reproduction.

## Dataset and licensing

Avoid committing Loghub raw samples to the AGPL repository without validated redistribution permission. Prefer permitted runtime fetching or generated synthetic fixtures. Commit only original, non-infringing expected-output fixtures generated from a pinned upstream commit after confirming those outputs themselves are suitable for redistribution.

## Acceptance gates

P3 clean locked restore and feed authentication, P5 invariants and counter widths, P6 exact upstream no-merge parity, and P7 measurable accuracy precede acceptance of DEC-0032. This report is an evidence register until the reproducibility fields are filled.
