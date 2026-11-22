---
id: DEC-0033
status: Accepted
repos: [DeltaZulu.LocalStream, DeltaZulu.Platform]
governs:
  types:
    DeltaZulu.LocalStream: [LocalStreamHost, TumblingWindowAggregateOperator]
  paths:
    DeltaZulu.LocalStream:
      - src/DeltaZulu.LocalStream/LocalStreamHost.cs
      - src/DeltaZulu.LocalStream.Query/Operators/TumblingWindowAggregateOperator.cs
cites: [CON-0001, CON-0006, CON-0013, CON-0014]
supersedes: [DEC-0010, DEC-0017, DEC-0020, DEC-0027, DEC-0028, DEC-0031]
---

# DEC-0033 — Replace Proton streaming with LocalStream; preserve DuckLake as the read surface

## Context

The estate has decided **not to use Timeplus Proton** as its streaming
processor. Earlier accepted Decisions and current architecture prose still
describe Proton-based Gold transformation, materialised views and continuous
detection. Those statements are no longer the target. The replacement is the
estate-owned [DeltaZulu.LocalStream](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream).

Source inspected on 2026-11-23: LocalStream `16f27b44fa16bcde6e9316662b25ac85ae0d4642`.
The repository currently contains three distinct projects: the payload-opaque
`DeltaZulu.LocalStream` append-only log, `DeltaZulu.LocalStream.Query` with
stateful time/window/aggregate/result-change primitives, and
`DeltaZulu.LocalStream.Query.LiteDB` with durable state/result stores.
These existing components **do not yet establish** a complete deployed KQL
binding, Gold transformation, detection-evaluation or lake-sink pipeline.
A target architecture is not a verified implementation.

## Decision

1. **No Proton in the target data-processing or detection path.** Do not
   introduce Proton-dependent ingestion, schema emission, materialised views,
   continuous detections or alert emission. Existing Proton code must be
   treated as legacy migration work, not evidence that Proton is approved.
2. **LocalStream is the node-local durable stream substrate.** Its core owns
   topics, partitions, offsets, independent named subscriptions, retention,
   replay and processor dispatch. It is payload-opaque and independent of
   KQL, `DeltaZulu.Kql` and Kusto.Language (`CON-0013`). LocalStream is not
   a network transport; `DeltaZulu.Forward` continues to own inter-node
   transfer. `DeltaZulu.DurableBuffer` remains an optional edge queue, not
   a required LocalStream dependency.
3. **Stream-query and stateful processing belong outside the core.**
   `DeltaZulu.LocalStream.Query` is the separate package for time/watermark,
   windowed aggregation, keyed state, output intent and result-change
   primitives. The optional LiteDB package can persist that state. Any
   KQL parsing/binding and mapping to these operators belongs in an explicit
   query-owning adapter, using `Microsoft.Azure.Kusto.Language`; do not
   claim such integration is complete merely because operators exist.
   This preserves `DEC-0032` and the `DeltaZulu.Kql` type contract.
4. **DuckLake remains the durable evidence and analyst read surface.**
   Persist Bronze once, retain Silver for reprocessing, and write canonical
   Gold and alerts into DuckLake. LocalStream retention is bounded replay
   storage, not a second evidence lake. Users hunt and investigate against
   DuckLake, not LocalStream. Gold keeps a single logical field contract
   generated from the C# schema authority of `DEC-0012`; no Proton schema
   projection is required.
5. **Preserve event-time and provenance invariants.** Extracted event time
   governs Gold processing, windows and correlation (`DEC-0029`).
   Retain ingest time as provenance. Stable event and alert identifiers,
   idempotent lake sinks, replay semantics and explainable unresolved
   evidence remain required (`DEC-0030`). Do not imply that the former
   Proton-to-DuckLake reorder buffer or its latency/ordering guarantees
   automatically apply to LocalStream.
6. **Preserve the narrow first-phase scope.** Near-real-time processing
   remains first; scheduled detection is deferred (`DEC-0026`).
   `DEC-0011`'s dual Proton/DuckLake SQL compilation proposal is
   **Rejected**. The feasibility and semantics of KQL-to-stream-operator
   binding, DuckDB hunting translation and any stream-to-lake reorder or
   materialization design must be verified independently.

The `governs` entries verify that the existing core and Query primitives
remain present. They do not assert production integration or feature parity
with Proton, and do not mechanically enforce the no-Proton rule.

## Consequences

The external Proton runtime and its dual-engine Gold semantic parity problem
leave the target design. A different verification obligation takes their
place: correct LocalStream processor behavior, state/checkpoint/replay
semantics, event-time windows, idempotent writes into DuckLake, and the
ability to reconstruct alerts from persisted evidence.

LocalStream core delivery is at-least-once, ordered only within a partition,
and retention can expire before a subscriber catches up. Every sink must
handle duplicates and `OffsetExpired` explicitly. Query operators and
persistence adapters exist, but end-to-end KQL binding and Platform
integration must be demonstrated, not inferred from project names.

The following accepted decisions are **Superseded** by this change because
their obligations depend on Proton: `DEC-0010`, `DEC-0017`,
`DEC-0020`, `DEC-0027`, `DEC-0028`, `DEC-0031`.
The durable Bronze rule, single logical Gold schema and DuckLake read
surface survive here. The `DEC-0011` proposal is **Rejected**, not silently
implemented in another engine. The other Decisions remain independently
binding unless amended.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Keep Proton as streaming processor | Conflicts with the decided in-estate LocalStream processing model and retains an unwanted external runtime | — |
| Put KQL grammar, stateful query semantics or CLR type inference inside core LocalStream | Breaks the payload-opaque core and mixes storage with language and type authorities | CON-0013, CON-0006 |
| Treat core LocalStream processors as a drop-in replacement for Proton SQL | Existing primitive processors do not provide full query-language semantics or confirmed end-to-end integration | — |
| Make LocalStream itself the historical analyst query surface | Confuses a bounded node-local replay log with the durable lake and its governed analytics | — |

## Revisit trigger

Reopen if verified query, latency, state or operational requirements cannot be
satisfied by LocalStream and its separated query layer, with reproducible
tests and quantified gaps. A proposal to reintroduce Proton or another
streaming engine requires a new explicit Decision, not a silent fallback.
