# Result identity review — 27 November 2026

Documentation-only source audit. The [candidate contract](../architecture/DETECTION-RESULT-CONTRACT.md)
is governed by DEC-0030, DEC-0036 and DEC-0037. No runtime tests executed.

| ID | Pinned source observation | Qualification |
|---|---|---|
| ID-01 | [ResultIdentityBuilder](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Results/ResultIdentityBuilder.cs) uses versioned length framing, big-endian integers and SHA-256, including source range and logical version. | Retain framing direction; separate transaction from semantic identity. |
| ID-02 | Builder uses default Encoding.UTF8.GetBytes; malformed UTF-16 can be replaced. | Reject malformed input or use reversible encoding; test collisions before freezing. |
| ID-03 | [ResultIdentity](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Results/ResultIdentity.cs) requires SourceRange and logical version. | Independent timer cause and generation-aware revision semantics; no fabricated offsets. |
| ID-04 | [OutputIntent](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/State/OutputIntent.cs) exposes target and ReadOnlyMemory payload with init setter; constructor does not copy backing memory. | Snapshot immutable bytes at durable staging boundary; verify actual store copying and target uniqueness. |
| ID-05 | [AlertMediationService](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Application/Analytics/Mediation/AlertMediationService.cs) fallback materialization key includes rule version, run, source view, source ID or alert ID and evidence hash. | Not DEC-0030 operational identity; distinguish legacy materialization from target dedup. |
| ID-06 | [DuckDbAlertLakeWriter](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Data.DuckDb/Analytics/Alerts/DuckDbAlertLakeWriter.cs) appends with INSERT; no dedup protocol established by this writer. | Verify whole persistence path, concurrent acceptance and restart; do not claim production duplicates from source alone. |

## Acceptance fixtures

| Fixture | Required invariant |
|---|---|
| Same evidence, changed batch ranges and run | Separate execution provenance; agreed semantic equivalence |
| Same logical group across partitions | One logical result under bound domain |
| Two revisions with different evidence | Immutable causal references; no overwrite |
| Retry same intent to same target; two targets | Idempotent acceptance scoped to target |
| Mutate original payload buffer after staging | Durable staged bytes unchanged |
| Malformed text and forced digest collision | Explicit rejection or reversible framing; collision-safe comparison |
| Same source event with multiple Gold representations | Distinct references, justified source equivalence |
| Independent reacquisition without stable source evidence | No invented equivalence |
| Identity promotion concurrent with alert creation | No new duplicate solely due to promotion |
| Corrected rule matches same evidence or previously missed evidence | Suppress equivalent alert; allow newly eligible alert |
| Corrected rule no longer matches | No automatic retraction |
| Missing Gold, crash after result/alert acceptance, expiry | Recoverable linkage or explicit unresolved/expired state |
| Mandatory evidence exceeds budget; optional trace truncated | Explicit incomplete/failure or disclosed optional truncation |
| Negative condition with incomplete scope | No false claim of completeness |

No physical key format, alert window discriminator, changed-evidence
policy, identity promotion storage mechanism or retention budget is
approved here. C06/C07 joint gate remains open. No Accepted Decision
or product code changed.
