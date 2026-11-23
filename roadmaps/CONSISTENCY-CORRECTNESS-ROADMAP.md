# Consistency and correctness roadmap — LocalStream target

**Baseline:** 2026-11-23. **Governing architecture:** `DEC-0033`.
**Review:** 2026-12-07, or sooner when a pending owner decision is recorded,
a contract is changed, or the first LocalStream-to-DuckLake integration suite
is available. Dates are review checkpoints, not implementation commitments.

This plan distinguishes documentation fixes, source-level verification and
choices requiring owner approval. No task here silently authorizes a
contract break, new streaming engine or changed detection semantics.

## P0 — correctness and governance

| ID | Work | Current state | Completion gate |
|---|---|---|---|
| C01 | Fail-closed Decision metadata, production declaration checks, generated index, regression tests | **Implemented in docs**; remote workflow verification outstanding | CI executes unit tests, rejects malformed metadata and detects a stale index or missing governed symbol |
| C02 | Remove refuted claims, correct historical report index, clarify proposed/rejected statuses | **Documentation corrected**; Constraint reclassification deferred | No Accepted Decision depends on a refuted current implementation claim; Constraint taxonomy decision recorded separately |
| C03 | Forward/KQL datetime carrier, duration ticks, provenance and wire compatibility | **Verification open; owner decision required for field-value tag 4** | Round-trip and compatibility fixtures, type/reason mapping, no silent offset or duration loss |
| C04 | Bronze integrity, manifest signing, restore and canary-retention requirements | **Proposed decisions remain open** | Accepted integrity/canary Decisions and destructive/replay test evidence before regulated production claims |

## P1 — LocalStream processing and persisted evidence

| ID | Work | Current state | Completion gate |
|---|---|---|---|
| C05 | Forward ACK to LocalStream append, offsets, durability, replay, subscription identity and `OffsetExpired` | Target topology accepted, end-to-end behavior unverified | Crash-point and duplicate/restart tests demonstrate conservation and explicit recovery |
| C06 | Kusto.Language binding into LocalStream.Query, DuckDB hunting subset, event time, watermark and threshold semantics | Query primitives implemented; binding and DEC-0021 policy unresolved | Supported KQL conformance corpus and deliberately rejected unsupported operators |
| C07 | Gold/alert lake sink idempotency, result-change identity, checkpoint coordination and evidence linkage | `DEC-0030` and `DEC-0033` bind the invariants, implementation unverified | Repeatable replay/crash tests prove stable alert identity and observable/recoverable evidence gaps |

## P2 — documentation convergence

| ID | Work | Current state | Completion gate |
|---|---|---|---|
| C08 | Rebaseline imported roadmaps and Platform/Agent per-repo docs; inventory legacy Proton code | Current indexes warn about supersession and overdue review; full source migration pending | Each roadmap is either reviewed as current or explicitly historical; no active work item prescribes Proton |
| C09 | Extend governance to reference checks, rule-state dependencies, dated review coverage and contract test links | Metadata/index checking implemented; semantic and review-date checks pending | CI produces reproducible drift reports, without equating type existence with behavior |

## Implementation principles

- Keep `DeltaZulu.LocalStream` core payload-opaque. Bind KQL only in a
  query-owning layer; do not promote source-only query primitives into a
  claim of production readiness.
- Maintain Forward's network-transport boundary, the collector's Platform
  ownership and DuckLake as durable evidence and user-visible query surface.
- Prove crash/replay invariants at the interaction points, not with
  independent unit-test successes alone.
- Keep immutable historical Constraints and reports untouched; add dated
  corrections, and obtain an explicit decision before reclassification.
- Never promote `Proposed` into `Accepted` based only on a convenient
  statement in an architecture narrative.

## Owner decisions blocking acceptance

The six owner decisions are enumerated in
`reports/2026-11-23-consistency-corrections.md`. They are deliberately
not represented as completed tasks or settled defaults.

## Evidence log

- `reports/2026-11-23-proton-localstream-reconciliation.md`
- `reports/2026-11-23-consistency-corrections.md`
- `reports/2026-08-24-forward-datetime-carrier.md`
- `reports/2026-08-16-schema-divergence-verification.md`
