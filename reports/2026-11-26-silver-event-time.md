# Silver observed event time verification

The Platform [C11 branch](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/a1f6193e7be10d86486f9002a3a0c76890eafbd1) changes the eight registered Silver contributors from Platform master `4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb`. Scope is the observed-time rule in DEC-0029 and null handling in DEC-0038. DEC-0036 also requires exclusion diagnostics at the point of detection evaluation.

| Silver source | Source timestamp inputs | Resolution |
|---|---|---|
| Sysmon 1, 3, 22 | `$.UtcTime` | The field explicitly denotes UTC. Both offset-bearing and unqualified UTC values are accepted. |
| Security 4624, 4625, 4688, 5156 | `$.TimeCreated` | Require an explicit offset or Z and normalize to UTC. |
| Windows DNS Server 256/257 | `$.TimeCreated`, then `$.EventTime` | Use the first trustworthy source instant in the existing precedence order. A malformed first value can fall through to a valid second value. Both require a zone. |

When the sources cannot establish an instant, Silver retains the row with a null Timestamp. TimestampNullReason distinguishes Missing (no candidate key), Null (a supplied JSON null and no non-null candidate), MissingOffset (the selected raw clock needs a zone) and Invalid. A valid timestamp has a null reason. Bronze inputs and the public Gold column list are unchanged. On regenerating the views, affected historical rows may move out of previously populated time buckets. Time-based counts can decrease while Silver row counts remain stable. Existing persisted detection results require separate migration review.

The linux-x64 check used SDK 10.0.404, locked restore and the Release test suite. All 1,346 cases passed, zero failed and zero skipped. Eight parameterized cases in ObservedEventTimeTests executed the actual emitted DuckDB views and checked results for absence, JSON null, malformed and out-of-range values, UTC, offsets, and arrivals years after the event. The DNS fixture also checked competing timestamp fields. This execution does not verify a live Proton deployment or a production detection engine.

The inspected Platform source has no call to LocalStream.Query's TumblingWindowAggregateOperator or WatermarkTracker. The LocalStream operator accepts a non-null EventTimeUtc. An integration test must exercise the actual Platform-to-operator boundary once wired, demonstrating that excluded rows contribute a reason to diagnostics without changing the watermark, window state or alerts. Hosted branch CI and deployment verification remain outstanding. C11 stays open.
