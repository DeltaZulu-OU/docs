# Resource qualification review — 27 November 2026

Source-only review of pinned LocalStream b900684. The permanent candidate
contract is in [NRT pipeline](../architecture/NRT-PIPELINE.md).
No benchmarks or runtime tests executed.

| ID | Source observation | Qualification |
|---|---|---|
| RES-01 | [ExactDistinctAccumulator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/ExactDistinctAccumulator.cs) copies operand before duplicate/budget checks, uses SortedSet Contains then Add. | Bound operand length before allocation; retain exact equality; measure duplicate-heavy workload. |
| RES-02 | [ExactDistinctStateCodec](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/ExactDistinctStateCodec.cs) materializes array and payload; restore allocates List capacity from count before checking minimum framing fits payload. | Reject count greater than (payload length minus 12)/4 before allocation; configured cardinality alone is insufficient. |
| RES-03 | [TumblingAggregateState](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingAggregateState.cs) restores tree and captures distinct payload then aggregate payload. | Measure transient allocations and full-state serialization; candidate cache per transaction. |
| RES-04 | [TumblingWindowAggregateOperator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingWindowAggregateOperator.cs) loads/saves and stages change for every admitted event. | Avoid repeated restore/serialize for same dirty key within transaction; preserve causal transitions. |
| RES-05 | [LiteDbStateStore](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query.LiteDB/LiteDbStateStore.cs) copies state and staged payload, orders pending domain intents by change ID and materializes array. | Snapshot copying at AddOutputIntent is confirmed for this adapter, narrowing ID-04; bound retrieval by causal sequence and bytes. |
| RES-06 | Same store inserts committed range metadata per commit and persists watermark JSON. | Measure growth and serialization; no safe compaction assumed. |
| RES-07 | [ExactDistinctPolicy](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/ExactDistinctPolicy.cs) bounds cardinality and serialized bytes per accumulator. | Add domain/global admission limits; no resident-memory guarantee. |

## Complexity model

Let n be distinct cardinality, B the sum of canonical value lengths,
L the maximum compared value length, m admitted events, g touched
logical windows, P pending intents and K tracked source partitions.
These are analytical bounds, not measured timings.

| Operation | Source-derived cost |
|---|---|
| Distinct lookup/insertion | O(L log(n+1)) worst-case comparison work plus operand copy |
| Serialize distinct state | O(n+B) time and payload bytes; reference array also O(n) |
| Restore distinct tree | O(n+B+n L log(n+1)) upper bound; tree nodes and value arrays |
| Aggregate capture | 41 + 4n + B bytes, plus temporary distinct payload |
| Repeated full capture of growing unique set | For m unique fixed-width values, cumulative serialized bytes 41m + (4+L)m(m+1)/2, excluding restore and database copies |
| Pending intent snapshot | O(P log(P+1)) comparison work plus materialization and payload retrieval; not bounded page retrieval |
| Candidate deadline index | O(log(W+1)) per indexed update and O(log(W+1)+d) ordered lookup for d due entries, excluding deletion/commit costs; W active deadlines |

A transaction-local cache reduces repeated restore/capture to touched
keys g per transaction if dirty state is flushed once. It does not
eliminate per-event evaluation, evidence or intent costs. A hash set
could reduce expected lookup work but requires collision-safe equality
and deterministic serialization; do not replace the tree without
measurement. A durable indexed deadline query is sufficient initially;
an in-memory heap is optional, not recovery authority.

## Qualification matrix

| Workload | Required measurement or invariant |
|---|---|
| Low/high cardinality and duplicate-heavy, long common prefixes | CPU, allocation, exactness, bytes per group |
| Hot key vs many cold groups; varying microbatch sizes | Restore/capture count, commit latency, RSS, semantic equivalence |
| Oversized operand and malformed count/short payload | Reject before disproportionate allocation |
| Many windows, stalled watermark, all idle | Bounded state and explicit coverage status |
| Many simultaneous deadlines | Bounded due retrieval and recoverable timer transitions |
| Slow/unavailable sink and large pending intents | Queue bytes/age, backpressure, drain capacity, no silent loss |
| Large evidence sets and optional traces | Mandatory references retained or explicit incomplete outcome |
| Disk full, low memory, crash and restart | Atomic recovery, no premature ACK, measured recovery time |
| Retention expiry during outage | Explicit missing range, no fabricated completeness |
| Long-running small transactions | Range metadata and journal/disk growth, safe reclamation |
| Cross-host packed consumer and state migration | Compatibility, exact results, resource cost |

Use a reproducible baseline with pinned source and workload seed,
bounded host resources, warm/cold runs and repeated measurements.
Report throughput at durable acceptance rather than enqueue rate.
No workload targets, budget values, new storage engines or
optimizations are approved by this review. C14 qualification remains
open. No product code or Accepted Decision changed.
