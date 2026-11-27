# Temporal execution review — 27 November 2026

Documentation-only audit against [LocalStream b900684](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/b900684308248a83a08550e0d66a8c52adad62fd)
and [docs efbbd03](https://github.com/DeltaZulu-OU/docs/tree/efbbd03ffbf79c722dcce748c620cc3544343f86).
The permanent candidate specification is the
[detection result contract](../architecture/DETECTION-RESULT-CONTRACT.md).
DEC-0021 remains Proposed; [DEC-0029](../decisions/DEC-0029-gold-is-governed-by-event-time.md) remains binding.

| Finding | Source observation | Candidate disposition |
|---|---|---|
| TMP-01 | [TumblingWindowAssigner](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Time/TumblingWindowAssigner.cs) uses checked UTC ticks, Unix epoch alignment and floor division. | Retain; verify KQL binding and representable boundaries. |
| TMP-02 | [WatermarkTracker](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Time/WatermarkTracker.cs) keys progress by integer partition; unseen partitions join only on first observation. | Namespace-aware assignment and explicit unseen policy. |
| TMP-03 | Tracker excludes sources at idle timeout and holds watermark when none active; caller supplies clock. | Record exclusion and returning-source behavior; distinguish activity from valid event-time progress. |
| TMP-04 | [LateEventEvaluator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Time/LateEventEvaluator.cs) finalizes at watermark >= end + lateness; equality with watermark is on-time unless window finalized. | Retain candidate boundary semantics; test exact ticks. |
| TMP-05 | Finalization deadline beyond representable maximum returns false indefinitely. | Reject unsupported policy/window explicitly; no immortal state. |
| TMP-06 | [Aggregate operator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingWindowAggregateOperator.cs) accepts caller watermark, finalizes explicit key/window, emits value-less finalize change with source range. | Define admission/advance ordering, durable deadline discovery, independent temporal cause and immutable revision linkage. |
| TMP-07 | Tracker captures progress but prior audit found checkpoint watermark can be overwritten by null. | Persist full temporal state atomically; unchanged differs from reset. |

Source inspection only; no tests or benchmarks executed. Existing
unit tests were not run. The following fixtures specify candidate
acceptance, not current behavior.

| Fixture | Expected invariant |
|---|---|
| Epoch minus one tick; exact start/end; UTC offset equivalent | Mathematical floor, half-open membership, identical UTC grouping |
| Near minimum/maximum timestamp and overflowing deadline | Explicit unsupported-range outcome; no immortal window |
| Two topics with partition 0; assigned unseen partition | Separate progress; unseen blocks unless approved exclusion |
| Idle timeout minus one tick, exact timeout, all idle, returning source | Recorded policy; monotonic watermark; no wall-clock completeness |
| Invalid timestamp and valid future outlier | Invalid never advances; future plausibility follows approved source policy |
| Event equals watermark; one tick behind; deadline minus one tick and equality | Exact admission/finalization boundaries |
| Batch resizing with later event advancing watermark | Earlier record not classified against future batch progress |
| Cross-partition interleaving and replayed idle decision | Equivalent admission under agreed ordering/decision contract |
| Timer fires twice, crash before/after temporal commit | Recoverable idempotent finalization without fabricated source range |
| Correction followed by value-less finalization marker | Finalized revision resolves exact value and evidence despite retry |
| No input or no matching events | No synthetic absence/threshold alert without explicit semantics |
| Too-late event after finalization; missing required evidence | Retain evidence and disposition; no silent mutation or clean non-match |
| State expiry with undelivered output | Preserve recovery obligations before reclamation |

## Approval boundary

Owner approval remains necessary for unseen/idle exclusion policy,
numerical disorder/lateness/idle budgets, future timestamp plausibility,
post-finalization corrections and operational alert eligibility.
The proposed initial tumbling contract does not establish sequence,
absence, sliding windows or scheduled detection semantics.
C06/C07 joint gate and C11 integration remain open.
