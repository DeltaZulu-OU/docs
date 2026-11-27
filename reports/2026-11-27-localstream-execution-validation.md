# LocalStream execution architecture validation — 27 November 2026

## Scope and evidence

Documentation-only source review. The owner requested validation and
correction of the central design, not code changes. Current authority is
the [NRT pipeline](../architecture/NRT-PIPELINE.md), the
[joint detection result contract](../architecture/DETECTION-RESULT-CONTRACT.md)
and the [consolidated roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md).
Accepted Decisions remain binding; proposed semantics and implementation
choices below are not new Accepted Decisions.

| Repository | Pinned revision |
|---|---|
| docs | [bb3fddb](https://github.com/DeltaZulu-OU/docs/tree/bb3fddb2f6545839c3e94f824ba9cc5601254702) |
| LocalStream | [b900684](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/b900684308248a83a08550e0d66a8c52adad62fd) |
| Kql | [a94dda9](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/tree/a94dda9cfd87c950b4996cffdb33f3d4c980b485) |
| Platform | [d6b3a43](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/d6b3a435466d57317e4c70a26948ea5d68075675) |

Method: inspect state interfaces, both state stores, result construction,
aggregate state and accumulator, watermark tracker, pinned package
version, KQL carrier and Platform NRT compiler, and reconcile with current
central decisions. No runtime tests, fault injection, benchmarks or
product build executed. Source-confirmed design exposure does not
establish the frequency or exact manifestation of runtime failures.

## Findings and candidate corrections

| ID / priority | Source observation or design gap | Candidate correction and existing owner |
|---|---|---|
| A01 P0 | [LiteDbStateStore](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query.LiteDB/LiteDbStateStore.cs) opens a transaction after a semaphore await and returns an asynchronous transaction interface. [LiteDB 5.0.21 API](https://docs.dndocs.com/n/LiteDB/5.0.21/api/LiteDB.ILiteDatabase.html) specifies per-thread transactions; the [pin](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/Directory.Packages.props) is 5.0.21. Semaphore serialization is not thread affinity. | C07: asynchronous orchestration outside a same-thread synchronous transaction; deterministic forced-switch regression; dedicated thread only if justified. |
| A02 P0 | [CheckpointManifest](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/State/CheckpointManifest.cs) stores one range and cursor per domain; both stores replace the checkpoint. Nonoverlap is checked but contiguous monotonic progress is not enforced by these transaction methods. | C05/C07: per-source contiguous progress map, explicit initial position, gap/duplicate/partial-overlap handling, reconcile subscription cursor; bound or compact range ledger safely. |
| A03 P0 | [StateKey](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/State/StateKey.cs) and [aggregate operator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingWindowAggregateOperator.cs) include physical partition. Domain also carries a partition assignment. | C06: one logical group/window per applicable domain; partition ownership is transport/replay metadata, not grouping. |
| A04 P0 | [ResultIdentityBuilder](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Results/ResultIdentityBuilder.cs) hashes range endpoints together with revision and logical version; changing batch boundaries can change IDs. | C06/C07: separate transaction, result key, immutable revision/change, causal evidence and operational alert identity. Do not assume identical intermediate transitions under arbitrary interleavings. |
| A05 P0 | Both [LiteDB](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query.LiteDB/LiteDbStateStore.cs) and [in-memory](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/State/InMemoryQueryStateStore.cs) stores materialize all pending intents sorted by change hash. Delivery deletes intents by ID. | C07: persistent causal sequence, indexed bounded paging, idempotent sink acceptance, recovery after delivery-before-ack, clarify receipt retention. |
| A06 P0 | [IStateTransaction](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/State/IStateTransaction.cs) requires SourceRange, including finalization. | C06/C07: explicit source/temporal/maintenance causes; durable timer changes, no invented offsets. |
| A07 P0 | [KqlValue](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/a94dda9cfd87c950b4996cffdb33f3d4c980b485/src/DeltaZulu.Kql/KqlValue.cs) uses CLR type/value equality and HashCode.Combine; typed null factory accepts a scalar symbol. | C06: bound expression/grouping/distinct semantics and canonical key encoders; validate null, coercion, dynamic and UTC ticks. CLR hashes are not durable IDs. |
| A08 P0 | DEC-0033 specifies bounded retention, at-least-once delivery and partition-local order. Required subscription alone does not prove conservation. | C05: separate append/ACK/lake commit, expiry handling, replay source and evidence reconciliation. |
| A09 P0 | [WatermarkTracker](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Time/WatermarkTracker.cs) advances on observed partitions, keys by integer partition, excludes idle partitions and never regresses. Unseen assigned partitions do not participate. | C06: source-scoped progress, explicit unseen/idle/rejoining policy and deterministic or recorded ordering for order-sensitive operators. No ambient-clock inference of completeness. |
| A10 P1 | [ExactDistinctAccumulator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/ExactDistinctAccumulator.cs) already enforces per-accumulator cardinality/byte budgets using a SortedSet; [aggregate](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingAggregateState.cs) serializes the complete state on every update. Domain-wide budgets are not established. | C06/C07/C16: measure serialization amplification and bound aggregate state, queues, timers, outbox, ledger and evidence; optimize only after measurement. |
| A11 P0 | Existing NRT responsibility diagram omitted explicit collector deployable. | C05: restore DEC-0022 boundary without claiming a verified process topology. |
| A12 P0 | LiteDB CompleteTransaction ignores Commit/Rollback boolean; CommitAsync marks completed before completion and releases writer in finally. A failed or wrong-thread commit can be reported as successful; actual failure mode untested. | C07: confirm outcomes, contain ambiguous commits, recover durable state before acknowledging progress. Atomically commit state/progress/timers/intents. |
| A13 P0 | Both stores overwrite previous watermark with null if the transaction does not call SetWatermark. Tracker's processing-time Advance removes idle inputs but cannot independently establish event-time completeness. | C06/C07/C11: preserve unchanged temporal state, distinguish explicit reset, persist sufficient decisions; no missing-time advancement. |
| A14 P0 | Range ledger rejects partially overlapping replay and permits exact already-committed range replay; result identity includes range and logical version. | C05/C07: distinguish recovery, final semantic and transition equivalence. Resume at first uncommitted offset; test batch resizing and cross-partition ordering. |
| A15 P1 | State serialization and result identity already have format versions; changed domain/key/checkpoint semantics may invalidate persisted data and consumers. | C14/C07: explicit migration or verified replay/rebuild from retained evidence, versioning and packed-consumer checks; no silent state reuse. |
| A16 P1 | Distinct budget exceptions exist but no integrated exhaustion, evidence expiry or output backpressure policy was verified. | C05/C06/C07/C16: explicit failure/incomplete coverage or backpressure; never silently lose evidence. |

Platform's [NrtRuleCompiler](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Application/Analytics/Nrt/NrtRuleCompiler.cs) still emits SQL and deployment DDL
through an injected backend. This is not evidence of a bound LocalStream
execution path. The Kql library remains scalar representation only.
The C11 Silver source correction is already recorded as integrated in
the roadmap; runtime diagnostics and watermark exclusion remain open.

## Algorithm and storage proportionality

Retain a source-progress map, indexed logical state, persistent ordered
outbox, durable deadline index and bounded input buffers. A heap is a
candidate timer accelerator, not a required second durable scheduler.
Existing distinct membership is O(log n) comparisons plus byte comparison
cost; full-state encoding is proportional to encoded state size, not O(1).
Hash-set membership may be expected O(1) with collision handling but
canonical serialization may require sorting. Index access and range
paging costs depend on actual backend query plans. Benchmark high
cardinality, serialization bytes, commit latency, recovery time, outbox
paging, disk usage and retained evidence. No numerical limits or
performance claims are approved here.

Retain LiteDB conditionally. Compare alternatives only if correctness,
operational or measured workload requirements cannot be satisfied.
Do not introduce distributed coordination, new storage engines, custom
storage trees, generic DAG scheduling, multicore sharding or a KQL
interpreter in DeltaZulu.Kql in the initial scope.

## Acceptance fixtures (not executed)

| Fixture | Required outcome |
|---|---|
| Explicitly coordinated two-thread begin/access/commit and rollback; forced suspension | No wrong-thread operation in corrected contract; baseline failure recorded rather than relying on Task.Yield scheduling |
| Commit false/throw, cancellation and process crash before/during/after commit | All-or-nothing durable state/progress/outbox; ambiguous result resolved from durable state; no external ACK on unconfirmed commit |
| Multiple domains, writer contention and shutdown | Exclusive mutation; no leaked gate/transaction; bounded cancellation |
| Unequal partition progress, gaps, duplicates and partially overlapping retry | No skip/regression; restart at correct per-source position |
| Same key across partitions; same partition number across topics | Correct grouping and independently scoped source progress |
| Replay with changed batch size and interleaving | Agreed semantic equivalence; separately specified intermediate identity/ordering behavior |
| Correction followed by finalization, sink failure and retry | Bounded causal paging; no duplicate logical result/alert |
| Timer without input; unchanged temporal state; unseen/idle/rejoining partitions | Recoverable transition and explicit completeness; no fabricated event-time progress |
| Invalid or missing observed time | Bronze/Silver retained with reason; no event-time detection or watermark advance |
| KQL typed null, strings, numeric coercion, dynamic, datetime precision, canonical grouping | Independent conformance fixtures; unsupported semantics explicitly rejected |
| Required consumer falls behind retention | Explicit incomplete/failure status and approved replay/reconciliation path |
| High cardinality, large state, outbox backlog and timer/evidence budget | Enforced measurable limits, no silent loss; benchmark current and candidate execution |
| Rule revision or state format changes during replay | Historical provenance intact; versioned compatibility or verified rebuild |

## Disposition

Use the existing C05/C06/C07 sequence and joint gate in DEC-0036; independent
reproduction and transaction-correctness prerequisites may precede the
joint gate. Preserve C10/C11 normalization and observed-time prerequisites,
C14 compatibility and C16 analyst/operational requirements. DEC-0021
window and correction semantics remain Proposed; DEC-0030 alert identity
and separate adjudication, DEC-0037 evidence identity scopes, DEC-0038
schema authority and CON-0021 binary compatibility remain unchanged.
No new roadmap, accepted decision, runtime implementation or release is
claimed. The proposed synchronous boundary, progress map and ordered outbox
are design directions pending implementation qualification, not proof of
correctness.
