# LocalStream consolidated qualification — 27 November 2026

## Scope and evidence

Documentation review complete; runtime qualification open. This report
reconciles the six detailed source reports covering seven workstreams.
No new runtime tests, benchmarks or source audit beyond those reports
were performed. The [existing roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md)
remains the sole active consolidation plan.

| Source review | Scope |
|---|---|
| [Execution validation](2026-11-27-localstream-execution-validation.md) | Boundaries, transaction lifecycle |
| [Delivery recovery](2026-11-27-delivery-recovery-contract-review.md) | ACK, checkpoint and replay |
| [Temporal execution](2026-11-27-temporal-execution-review.md) | Windows, watermark, timers |
| [KQL semantics](2026-11-27-kql-semantic-review.md) | Binding, equality, exact distinct |
| [Result identity](2026-11-27-result-identity-review.md) | Causal references, revisions and alert equivalence |
| [Resource qualification](2026-11-27-resource-qualification-review.md) | Budgets, complexity and performance |

## Cross-contract reconciliation

| Potential tension | Required interpretation |
|---|---|
| Bounded replay vs durable evidence | LocalStream expiry is not evidence deletion authority; recover approved equivalent evidence or report missing coverage. |
| Atomic state vs asynchronous orchestration | Keep LiteDB transaction work thread-affine; external I/O outside transaction; resolve uncertain commits before ACK. |
| Per-event semantics vs microbatch cache | Evaluate each event against preceding logical temporal state; flush dirty state once only if causal transitions survive. |
| Provisional changes vs final alerts | Internal revisions may be staged; operational aggregate alert policy requires approval. No silent coalescing of observable changes. |
| Monotonic watermark vs idle sources | Explicit recorded idle policy; no wall-clock-only completeness claim; returning sources cannot regress committed watermark. |
| Replay vs identity stability | Exact retry identity, semantic final equivalence and transition equivalence are separate; no arbitrary cross-policy identity guarantee. |
| Immutable evidence vs identity promotion | Preserve historical references; version equivalence assertions and reconcile concurrent alert creation. |
| Bounded state vs exact detection | Backpressure or explicit incomplete/failure; no silent approximation, evidence truncation or successful non-match. |
| DuckLake authority vs local recovery state | Local state owns execution progress; DuckLake owns durable evidence and analyst queries; no assumed cross-store atomicity. |
| Consolidation vs product development | Correct demonstrated existing defects; preserve future functionality and approval gates without requiring all product work for roadmap closure. |

## Consolidated acceptance suites

The following suites group existing fixtures; retain individual source
report assertions and identifiers for traceability. No suite is marked
passed by this report.

| Suite | Work items | Minimum assertions |
|---|---|---|
| Baseline and carrier | C03/C10/C11/C14 | Locked builds, packed consumer, UTC ticks, duration scale, nullable observed time and mapping provenance |
| Transport and evidence | C05 | Pending duplicate ACK, credit shrink, partial append, durable receipt, required subscription initialization, expiry |
| Transaction and recovery | C07 | Forced thread switch, false/throw commit, crash boundaries, contiguous source map, cursor ahead/behind, ordered bounded intents |
| Bound operator conformance | C06 | Null/absence/failure, promotion, string semantics, canonical framing, exact distinct and collision fixtures |
| Temporal conformance | C06/C07/C11 | Boundary arithmetic, unseen/idle/rejoin, invalid/future time, independent timer, batch invariance, finalization overflow |
| Causal and sink integration | C05/C06/C07/C16 | Immutable revision, Gold linkage, retry acceptance, evidence promotion, rule correction, expiry, analyst navigation |
| Resource and compatibility | C14/C05/C07 | Hot/cold keys, malformed state, budgets, outage, disk pressure, restart, retention, migration and reproducible benchmark |

## Owner approval register

| Policy group | Decision boundary | Candidate direction / unresolved choice |
|---|---|---|
| Delivery acceptance | C05, DEC-0022/0033 | Select durable ACK boundary and retry identity; spool versus lake remains open. |
| Temporal policy | C06, DEC-0021 Proposed | Tumbling first, unseen blocks by default; lateness, idle, future time, threshold and post-finalization corrections require approval. |
| Supported semantics | C06, DEC-0032 | Approve initial bound operator surface after reference qualification; exact versus approximate operators explicit. |
| Result and evidence identity | C06/C07, DEC-0030/0036/0037 | Approve canonical format, group/window discriminator, changed evidence and promotion reconciliation. |
| Persistence and retention | C07/C04/C16 | Approve receipt lifetime, evidence/trace retention, access and recovery protocol; no new storage engine assumed. |
| Resource objectives | C14 | Approve representative workloads, service objectives, limits and incomplete-outcome/isolation policy after baseline measurement. |
| Compatibility | C03/C14 | Approve incompatible wire/state changes or explicit migration/rebuild; no silent release reuse. |

DEC-0029 remains Accepted; missing trustworthy observed time is retained
in Bronze/Silver with reason and excluded from event-time detection.
DEC-0032/0033/0036/0037/0038 remain binding. No Accepted Decision changed.

## Handoff

The next engineering activity, if separately authorized, is baseline
verification and reproduction of existing defects under the established
roadmap sequence. Candidate product execution changes require the joint
C06/C07 gate. Keep one bounded worker per owned execution domain as the
initial candidate; no new engine or general interpreter is proposed.
The architecture review is complete as documentation, not a claim of
implementation readiness or closure of any roadmap item.
