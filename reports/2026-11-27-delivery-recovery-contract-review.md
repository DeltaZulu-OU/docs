# Delivery and recovery contract review — 27 November 2026

## Scope

Follow-up to the [execution validation](2026-11-27-localstream-execution-validation.md).
This is a documentation-only source audit, not failure reproduction or a
new Accepted Decision. The permanent candidate contract is in the
[NRT pipeline](../architecture/NRT-PIPELINE.md). C05/C07 remain open.
No production source, API, schema or package was changed.

| Repository | Inspected revision |
|---|---|
| Forward | [19b3d00](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/tree/19b3d000697922870742f52ba46e8b4fc3de3ee6) |
| LocalStream | [b900684](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/b900684308248a83a08550e0d66a8c52adad62fd) |
| Platform | [d6b3a43](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/d6b3a435466d57317e4c70a26948ea5d68075675) |
| docs | [22177ed](https://github.com/DeltaZulu-OU/docs/tree/22177ed98d259287de8685241bce3d9cc968e260) |

## Source observations

| ID | Observation | Consequence / verification required |
|---|---|---|
| DLV-01 | [ForwardSession](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/blob/19b3d000697922870742f52ba46e8b4fc3de3ee6/src/DeltaZulu.Forward/ForwardSession.cs) generates a new batch UUID for each SendBatchAsync invocation. | Reinvoking a send after ambiguous ACK is not itself stable delivery identity. Trace actual Agent retry path before claiming a failure or changing the wire contract. |
| DLV-02 | [ForwardDedupWindow](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/blob/19b3d000697922870742f52ba46e8b4fc3de3ee6/src/DeltaZulu.Forward/ForwardDedupWindow.cs) is a bounded process-memory set/FIFO; admission precedes handler completion. ForwardSession returns success for already-admitted IDs. | Shared window across sessions can confuse in-flight with committed; concurrent duplicate while original fails is a critical candidate failure. Test with a blocked handler and separate sessions. Eviction/restart also require durable acceptance reconciliation. |
| DLV-03 | [ForwardCreditWindow](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/blob/19b3d000697922870742f52ba46e8b4fc3de3ee6/src/DeltaZulu.Forward/ForwardCreditWindow.cs) clamps available credit on shrink and increments or grants credit on release. | Source-level counterexample: capacity 3, three acquisitions, shrink to 1, release one: one credit becomes available while two remain outstanding. Test shrink, zero-capacity and cancellation interleavings; distinguish credits from storage acceptance. |
| DLV-04 | [LocalStreamRawLogPublisher](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Ingestion/PubSub/LocalStreamRawLogPublisher.cs) appends individually, generates occurrence IDs by default, and throws on failed append. | A prefix can be appended before a failed batch. Retrying with new occurrences can duplicate a prefix; no batch atomicity or durable per-item retry is demonstrated. Trace actual caller and identity scope. |
| DLV-05 | [LocalStreamBronzeWriter](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Data.DuckDb/Ingestion/LocalStreamBronzeWriter.cs) writes Bronze and receipt in one transaction; receipt key is topic, partition, offset, event ID. | Reuse candidate for same occurrence replay. No proof of cross-epoch uniqueness, conflicting content detection, source-event deduplication or catalog/storage durability. Verify actual DuckLake configuration and commit/restart behavior. |
| DLV-06 | [LocalStreamBronzeConsumer](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Data.DuckDb/Ingestion/LocalStreamBronzeConsumer.cs) writes before committing each offset and propagates OffsetExpired; generic subscriber overload does not promise idempotency. | Preserve write-before-checkpoint. Verify production wiring uses transactional writer, not generic overload; crash after lake commit and before cursor write must be harmless. |
| DLV-07 | [LocalStreamConsumer](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream/LocalStreamConsumer.cs) reads partitions sequentially; committed offset is inclusive and next read starts at offset + 1. No checkpoint starts at earliest retained. [SubscriptionStore](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream/Subscriptions/SubscriptionStore.cs) writes supplied offsets without monotonic/contiguous validation. | Caller can regress/skip progress; new required subscription can start after already-expired evidence with no explicit gap. Test initialization, fairness, concurrent ownership, invalid offsets and expiry. Temp/rename is not by itself proof of power-loss durability. |
| DLV-08 | [LocalStreamIngestionService](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Web/Analytics/Hosting/LocalStreamIngestionService.cs) starts the local host and drains Bronze in Platform.Web. | Existing hosted ingestion does not demonstrate separate Forward collector executable or independently available telemetry plane under DEC-0022. |

These observations are pinned code facts and reasoned failure scenarios.
No concurrency test, runtime fault injection, storage durability test or
Agent end-to-end trace was executed. DLV-03 is a state-machine
counterexample derived from the code, not a measured runtime result.
Do not infer loss or duplication in production from these findings alone.

## Minimum recovery test matrix

| Fixture | Acceptance |
|---|---|
| Same batch UUID arrives on two sessions while original handler is blocked, then original fails | Duplicate must not receive durable success before acceptance; retry remains possible |
| ACK lost after durable acceptance; reconnect; process restart; dedup eviction | Retry follows declared identity scope; no false durable acknowledgement |
| Failure at every record boundary of a multi-record append | Accepted prefix recovered without silent loss; duplicate handling explicit and scope-correct |
| Credit window shrinks below outstanding count, including zero | No new grant until capacity allows; cancellations do not leak permits; storage pressure separately enforced |
| Bronze commit succeeds before subscription checkpoint; crash at each boundary | Same occurrence replay does not duplicate Bronze; receipt and evidence agree |
| Recreated stream or conflicting identity/content | No incorrect deduplication or silent replacement; explicit conflict |
| No checkpoint with earliest retained offset greater than intended start | Required evidence gap surfaced before processing or reset |
| Subscription cursor ahead of state; behind state; missing or stale generation | Recover according to authoritative state progress; never skip uncommitted work |
| Retention expires unread data while output sink is unavailable | Recover from verified retained evidence or declare incomplete scope; no silent success |
| Web redeploy during collector intake | Separate collector target remains available subject to its own lifecycle |

The tests belong to existing C05/C07 and supporting C14. They are not
new roadmap tasks. Retention budgets, ACK persistence boundary, exact
receipt schema, namespace/epoch scheme and physical replay strategy
remain open. DEC-0030 and DEC-0037 prohibit conflating delivery
deduplication, source equivalence and alert identity.
