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

## Rule-rendering validation (new evidence, not independently reproduced)

The reported property check took candidate patterns marked executable and attempted to parse the candidate's own contributing records using DeltaZulu.Parse built from `main`. Among 1,740 executable rules, 341 reportedly failed to parse at least one contributing record (341/1,740 = **19.6%**). Those failures covered 7,260 of 43,514 contributing record occurrences (**16.7%**). This is a rule-level failure count plus an affected-line count, **not** proof that all 7,260 line parses individually failed. The exact evaluator, input provenance, treatment of repeated records, and failed-rule-to-line mapping must be retained to reproduce these figures.

| Candidate defect | Required reproduction | Proposed corrective acceptance |
| --- | --- | --- |
| Gap separators | A filled gap with different whitespace on its left and right | Track and render both sides rather than choosing one modal separator |
| Variable separator widths | Same candidate with differing whitespace lengths | `%-:whitespace%` recognized by the tested Parse version and every contributing line parses |
| Trailing whitespace | Records ending in spaces, tabs, and mixed separators | Preserve evidence without silently trimming; prove exact suffix representation, or a bounded closing parser such as `%-:rest%` when valid |
| Optional gap adjacency | `login *{0,1}` with and without gap text | Keep the separator required by the line and validate both variants |
| Clock time versus IPv6 | Clock-time samples receiving `ipv6` parser votes | Reject misclassification through Parse catalog full-match and parser-priority checks |
| Parser catalog and warnings | Fallback-only and invalid parser names | All executable rules contain supported parsers; ambiguous cases remain sketches |

The key product-level property is stronger than successful rule compilation: **for each emitted executable candidate, the parser must successfully parse each record contributing to that candidate's support**, with records preserved as mined. Track distinct input occurrence IDs rather than assuming sequence numbers are unique. An executable rule may otherwise be syntactically valid yet unusable for the data it was derived from.

**Version boundary:** the reported 341 failed rules were tested using Parse built from `main`. They do not establish the exact behavior of the published `DeltaZulu.Parse` 0.1.1 package. Repeat the property suite against both versions and document divergences. This is part of P2's release gate.

## Reproducibility fields to complete

- Exact upstream `ristov/logcluster` SHA and command line including disabled `--aggrsup` and `--wweight`.
- Toolchain, operating system, input identity/hash, record ordering, minimum support and separator behavior.
- Canonical comparison procedure for pattern and support pairs; clarify whether sorting, escaping, whitespace or output ranking was normalized.
- Per-mode match counts and percentages, including outlier counts; distinguish exact cluster-set equality from candidate-level percentage.
- Ground-truth accuracy against a licensed Loghub corpus, including precision/recall or template-level F1 and provenance.
- Full tests and CI artifacts for 48-run failure cases and patched reproduction.
- Exact Parse `main` commit, published 0.1.1 artifact version/hash, executable-rule property harness, per-rule failures and contributing-line identifiers.

## Dataset and licensing

Avoid committing Loghub raw samples to the AGPL repository without validated redistribution permission. Prefer permitted runtime fetching or generated synthetic fixtures. Commit only original, non-infringing expected-output fixtures generated from a pinned upstream commit after confirming those outputs themselves are suitable for redistribution.

## Acceptance gates

P3 clean locked restore and feed authentication precedes CI acceptance. **P5 mining correctness and P2 rendered-rule round-trip correctness are both release gates.** P6 exact upstream no-merge parity and P7 measured accuracy precede acceptance of DEC-0032. The sequence is P3, P5, P2, P6, P7, P8, P4, P9. This report remains an evidence register until reproducibility fields are filled.
