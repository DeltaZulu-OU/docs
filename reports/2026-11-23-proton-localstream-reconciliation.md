# Proton-to-LocalStream architecture reconciliation

**Date:** 2026-11-23. **Basis:** User-confirmed architectural choice and
source inspection. **No runtime integration tests or code migration performed.**

## Evidence and boundaries

[DeltaZulu.LocalStream at `16f27b44`](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/16f27b44fa16bcde6e9316662b25ac85ae0d4642)
contains the durable append-only core, independent
`DeltaZulu.LocalStream.Query` package, and a LiteDB persistence adapter.
The core README documents at-least-once delivery, named subscriptions,
per-partition ordering, retention independent of subscriber progress,
replay and `OffsetExpired`.

`TumblingWindowAggregateOperator` explicitly processes *already-bound*
events. The available code establishes stream-processing primitives, not
a complete KQL compiler, Gold-transformer, detection pipeline or lake sink.
No performance or end-to-end correctness claims were tested.

## Governing changes

`DEC-0033` is Accepted: LocalStream/Query replace Timeplus Proton as the
stream processing target; Forward remains inter-node transport; DuckLake
remains durable storage and analyst read surface; core LocalStream stays
KQL-independent. Single logical Gold, event-time and stable alert identity
are retained.

| Decision | Prior status | New status | Treatment |
|---|---|---|---|
| DEC-0010 | Accepted | Superseded | Bronze write-once retained in DEC-0033; Proton staging retired |
| DEC-0011 | Proposed | Rejected | Abandoned dual Proton/DuckDB SQL compiler |
| DEC-0017 | Accepted | Superseded | Proton HTTP ingest retired |
| DEC-0020 | Accepted | Superseded | Proton materialised Gold view retired |
| DEC-0027 | Accepted | Superseded | DuckLake read rule retained; Proton-specific premise retired |
| DEC-0028 | Accepted | Superseded | C# Gold field authority retained; dual Proton physical-schema generation retired |
| DEC-0031 | Accepted | Superseded | Proton-to-DuckLake reorder buffer no longer a binding mechanism |

The still-Accepted `DEC-0026`, `DEC-0029`, `DEC-0030` and
`DEC-0032` were narrowly updated to remove Proton assumptions without
changing their NRT-only, event-time, alert identity or type boundaries.
`DEC-0021` remains Proposed, with window semantics now evaluated
for the LocalStream.Query processing layer.

## Documentation hierarchy

`architecture/NRT-PIPELINE.md` is the current target narrative.
`PIPELINE.md` and `DATA-QUALITY-MONITORING.md` are historical
imports and remain unedited. `PIPELINE-ERRATA.md` and
`DATA-QUALITY-MONITORING-INTEGRATION.md` explain the supersession.
Imported roadmaps require rebaseline before Proton tasks can be treated
as active. Other historical reports remain intact as dated evidence.

## Open implementation checks

1. Map approved KQL expressions to bound LocalStream.Query operators;
   separately verify the DuckDB hunting path.
2. Prove deterministic state/checkpoint behavior under retries, crashes,
   late events and partition replays; decide offset-expiry recovery.
3. Prove idempotent Bronze, Silver, Gold and alert persistence; verify
   source conservation and evidence reconstruction.
4. Evaluate whether lake output needs a new reorder/clustering mechanism,
   instead of inheriting superseded DEC-0031 guarantees.
5. Audit and retire legacy Proton-dependent Platform code. The target
   decision is not evidence that this migration has already occurred.
6. Independently reconcile earlier audit findings, including stale
   CON-0016 and the refuted implementation claim in DEC-0012, using
   code verification before editing a binding factual assertion.

No new substitute streaming engine, project, or backend has been authorized.
