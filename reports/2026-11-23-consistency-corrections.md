# Consistency and correctness audit — factual corrections and deferred decisions

**Date:** 2026-11-23. **Authority:** This is a verification report, not a new
Decision. The binding streaming architecture remains `DEC-0033`.

## Method and evidence

Inspected global Decisions (`DEC-0001`–`DEC-0033`), 20 Constraints,
the governing-index workflow and the current architecture/roadmap summaries.
Checked source files on the existing `master` / `main` branches of
`DeltaZulu.Forward`, `DeltaZulu.LocalStream` and `DeltaZulu.Platform`.
This review **did not build, run application tests, deploy a pipeline, or
prove runtime semantic conformance**. Source and historical reports have
different evidentiary dates.

Sources inspected:

- [docs governance baseline](https://github.com/DeltaZulu-OU/docs/commit/e2f5b5eaed492d9d98239245661be584b7eef820)
- [Forward source](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/tree/fba0c5c63a1ee506373012ad458276ec807e542a)
- [LocalStream source](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/16f27b44fa16bcde6e9316662b25ac85ae0d4642)
- [Platform source](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f)

## Corrected without changing policy

| Finding | Evidence and correction |
|---|---|
| DEC-0012 asserted a coercing `ToKustoType` fallback | Removed the refuted implementation claim. The older source-verification report had already determined `_ => KustoType.String` never existed. The single-catalogue Decision remains Accepted. |
| Historical schema review summary miscounted its table | The thirteen itemized verdicts comprise **eight refuted, three confirmed defects, one inherent limitation and one partial item**. The August report is preserved verbatim; its current index points to this correction. |
| DEC-0013 placed two undecided options under rejected alternatives | Relabeled the options as pending, retaining `Proposed` status. Removed the stale gate on now-Rejected DEC-0011. |
| DEC-0032 retained an old dual-compilation revisit condition | Replaced with the current LocalStream/Platform language boundary and documented that DEC-0011's gate is no longer pending. |
| DEC-0016 said no repository has collection tier or null-reason fields | Current Forward has `ForwardCollectionTier`, `ForwardNullReason`, and record properties `CollectionTier`, `NullReasons` and `MatrixVersion`. Updated implementation-status language; **end-to-end Gold persistence remains unverified**. |
| DQM inventory called nine rows nine fields | `ParserId` and `ParserVersion` share a row. The list is **nine rows containing ten named properties**. All ten already appear on `ForwardLogRecord` as optional fields. |
| Canary prototype and production emitter readiness conflated | DEC-0023 explicitly blocks production injection into Bronze until a retention/filtering policy is decided. Independent canary prototyping is permitted without asserting the undecided policy. |
| Archived ADRs sometimes call themselves current | The archive stays frozen; the archive index now explicitly rejects those historical authority claims. |
| Current docs' governing index relied on manual maintenance | Added fail-closed front-matter checks, production-only type-existence search, regression tests, and an index generator with a CI drift check. These do not prove semantic conformance. |
| Roadmap index described LocalStream as complete | It now distinguishes implemented primitives from unverified end-to-end Platform, KQL and lake integration. |

## Constraints deliberately left unmodified

`CON-0016` is an August implementation snapshot stating no collector
project exists. `DEC-0022` subsequently assigns Platform ownership and a
Platform `Ingestion` project exists, but the prescribed standalone executable
remains unverified. Under the repository's immutable-Constraint policy, this
review adds a warning to `constraints/README.md` rather than rewriting the
historical assertion or silently choosing a replacement classification.

`CON-0020` contains both integrity observations and design prescriptions.
Separating its external facts from controlled integrity obligations depends on
a decision about `DEC-0024`; this review does not accept that proposal.

## Unresolved source-level correctness issue: Forward datetime

At Forward source revision `fba0c5c`:

- `ForwardValueNormalizer.NormalizeDateTime` converts `DateTime` values
  to `DateTimeOffset`, including assuming `Unspecified` means UTC.
- `ForwardObjectFormatter` retains a `DateTimeOffset` field-value tag 4,
  encoded as an ISO-8601 string.
- `ForwardLogRecord.CreatedAt` and `ForwardLogBatch.CreatedAt` are also
  `DateTimeOffset`, but are **transport metadata**, not automatically
  declared KQL scalar field values.

The field-value behavior conflicts with `CON-0001` and `DEC-0003`.
Fixing it may require a versioned wire change. This report makes no change
to encoding or to the accepted type contract.

## LocalStream target remains an unverified integration

The Platform tree inspected still contains `DeltaZulu.Platform.Data.Proton`
source and no LocalStream-named files. LocalStream has distinct core, Query
and LiteDB projects. `DEC-0033` is a target decision, not proof that
Platform has implemented it. Transactional coordination with DuckLake,
watermark and late-event behavior, and evidence reconstruction need
integration tests and executable acceptance criteria.

## Decisions explicitly deferred to the owner

1. Forward tag-4 KQL datetime migration and compatibility versioning.
2. Bronze digests/manifests/restores and signing-key custody (`DEC-0024`).
3. Canary retention versus filtering from write-once Bronze (`DEC-0023`).
4. Gold semantics/naming (`DEC-0013`).
5. Threshold/window, late-event and correction behavior (`DEC-0021`).
6. Governance classification/supersession of internal-state Constraints
   (`CON-0016`, `CON-0020`).

No pending choice above was implicitly accepted. See
`roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md` for execution gates.
