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
| C01 | Fail-closed Decision metadata, production declaration checks, generated index, regression tests | **Completed in docs; latest governs-check and CodeQL runs passed** | Re-run CI whenever governance metadata or checked repositories change |
| C02 | Remove refuted claims, correct historical report index, clarify proposed/rejected statuses | **Documentation corrected**; Constraint reclassification deferred | No Accepted Decision depends on a refuted current implementation claim; Constraint taxonomy decision recorded separately |
| C03 | Forward/KQL datetime carrier, duration ticks, provenance and wire compatibility | **Source audit completed** (FWD-01–05); Forward TimeSpan codec uses ticks, Platform registry defaults to microseconds; tag-4 policy unresolved | Round-trip and compatibility fixtures, type/reason mapping, no silent offset or duration loss |
| C04 | Bronze integrity, manifest signing, restore and canary-retention requirements | **Proposed decisions remain open** | Accepted integrity/canary Decisions and destructive/replay test evidence before regulated production claims |
| C10 | ASIM-first field mapping for four current Gold families and operational alert views | **Source inventory established**: 71 Gold telemetry fields across 4 families; mappings unverified | Versioned ASIM 1.0.0 field register, mandatory-field coverage, source fixtures and compatibility migration plan |
| C11 | Stop silent ingest-time promotion into event time | **P0 source violation confirmed**: helper used by 7 Silver views plus DNS server explicit fallback | T04: all 8 contributors preserve absent/estimated event-time semantics and never implicitly substitute ingest time in detections |

## P1 — LocalStream processing and persisted evidence

| ID | Work | Current state | Completion gate |
|---|---|---|---|
| C05 | Forward ACK to LocalStream append, offsets, durability, replay, subscription identity and `OffsetExpired` | Target topology accepted, end-to-end behavior unverified | Crash-point and duplicate/restart tests demonstrate conservation and explicit recovery |
| C06 | Kusto.Language binding into LocalStream.Query, DuckDB hunting subset, event time, watermark and threshold semantics | Query primitives exist; **EVT-01 event-time fallback conflicts with DEC-0029**; binding and DEC-0021 semantics unresolved | Supported KQL conformance corpus and deliberately rejected unsupported operators |
| C07 | Gold/alert lake sink idempotency, result-change identity, checkpoint coordination and evidence linkage | `DEC-0030` and `DEC-0033` bind the invariants, implementation unverified | Repeatable replay/crash tests prove stable alert identity and observable/recoverable evidence gaps |

## P2 — documentation convergence

| ID | Work | Current state | Completion gate |
|---|---|---|---|
| C08 | Rebaseline imported roadmaps and Platform/Agent per-repo docs; inventory legacy Proton code | Current indexes warn about supersession and overdue review; full source migration pending | Each roadmap is either reviewed as current or explicitly historical; no active work item prescribes Proton |
| C09 | Extend governance to reference checks, rule-state dependencies, dated review coverage and contract test links | Metadata/index checking implemented; semantic and review-date checks pending | CI produces reproducible drift reports, without equating type existence with behavior |

## C10 — ASIM Gold mapping (DEC-0013 Accepted)

**Source inventory completed, ASIM conformance not verified.** Four active
Gold families and eight Silver contributors are documented in
`architecture/ASIM-GOLD-MAPPING-REGISTER.md`. Start with pinned ASIM schema
references, mapping fixtures and the EVT-01–04 defects. Treat C10 as P0
contract work parallel to C03. Do not publish a compatibility claim before
per-family conformance tests pass.

## ASIM Gold mapping work (DEC-0013 Accepted)

Initial C10 source inventory and candidate mapping register:
[`architecture/ASIM-GOLD-MAPPING-BASELINE.md`](../architecture/ASIM-GOLD-MAPPING-BASELINE.md).
It covers the 4 implemented telemetry contract families, 8 Silver contributors,
3 Bronze sources and separately tracks the 2 operations views. **Candidate
mappings are not approved field transformations or tested ASIM conformance.**
The `governs-check` workflow now detects field-name/type/order drift against
this register from Platform's current C# source; functional ASIM conformance
remains to be tested independently.

Create a versioned mapping register for each implemented event family, using
Microsoft's published ASIM schema and documented mandatory/conditional
fields. Start from actual ingested telemetry coverage, not a promised list of
event families. Document ASIM-derived extensions, enum/field conversions,
Gold KQL types, null/provenance fields, and per-schema conformance fixtures.
Avoid claiming full ASIM compatibility until source-specific tests support it.
This decision does not unblock C03/C04/C05/C07 or decide DEC-0021.

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

The initial six owner questions are recorded historically in
`reports/2026-11-23-consistency-corrections.md`. **Gold naming (DEC-0013) is
now resolved ASIM-first**; the other owner decisions remain outstanding.
The historical report is not rewritten.

## C03/C11 regression scope

Source-verified findings and the ten required test groups T01–T10 are in
[`reports/2026-11-23-c03-c10-source-verification.md`](../reports/2026-11-23-c03-c10-source-verification.md).
C11 is a code-versus-DEC-0029 inconsistency; it does not require a new schema
name or new engine choice, but its unavailable-event-time processing behavior
must be verified before claiming correction. C03 field tag 4 must not change
without the owner's versioning decision.

## Evidence log

- `reports/2026-11-23-proton-localstream-reconciliation.md`
- `reports/2026-11-23-consistency-corrections.md`
- `reports/2026-08-24-forward-datetime-carrier.md`
- `reports/2026-08-16-schema-divergence-verification.md`
- `reports/2026-11-23-forward-type-contract-audit.md`
- `architecture/ASIM-GOLD-MAPPING-REGISTER.md`
