# Reports

Verification output. Constraints cite these; Decisions cite Constraints.

A report records what was checked, how, and what the check returned — including
when the answer refuted the premise that motivated the check. Reports are dated
and are not rewritten: a later check that reaches a different conclusion is a
later report.

| Date | Report | Outcome |
|---|---|---|
| 2026-08-15 | `2026-08-15-kusto-language-preflight.md` | Kusto.Language 9.2.0 vs 12.4.1. Four API members identical; `ScalarTypes.All` membership and the `single` alias differ. Both deltas absorbable. Raw probe output alongside. |
| 2026-08-15 | `2026-08-15-platform-ci-restore.md` | Locked-mode restore was a silent no-op, not a failure. `deltazulu-github` undefined in Agent, Platform and Parse alike. |
| 2026-08-15 | `2026-08-15-version-pin-reconciliation.md` | Agent's 1.0.0 pins match published reality. LocalStream's source has since declared 0.1.0, below its published version. |
| 2026-08-15 | `2026-08-15-golden-placement.md` | Section 9 decision memo. Option A recommended, C as fallback, B ruled out. `DEC-0011` stays Proposed until the CI equivalence test exists. |
