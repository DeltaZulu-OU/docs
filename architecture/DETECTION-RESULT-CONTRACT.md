# Joint C06/C07 detection result contract

> **Consolidated conventions:** [DEC-0038](../decisions/DEC-0038-medallion-schema-conventions.md) governs Medallion naming, field resolution and record-local normalization. Authentication is the first cross-platform conformance family; Windows is the first implemented contributor.

Status: design directions approved by owner 2026-11-26; detailed contract and implementation verification open. Governed by [DEC-0036](../decisions/DEC-0036-detection-provenance.md), [DEC-0030](../decisions/DEC-0030-alert-identity-and-replay.md) and [DEC-0021](../decisions/DEC-0021-threshold-as-windowed-aggregate.md) (Proposed). This is not a physical schema or separate roadmap.

## Identity and replay

Reuse assigned detection and accepted-version IDs. Derived identities use a versioned, domain-separated, unambiguous canonical encoding and deterministic digest; SHA-256 is the initial candidate. Source identity is distinct from stream position, Gold representation identity, logical result key, immutable result revision and query change identity. The current query change ID includes revision and transaction range offsets and cannot serve as the operational alert key. The candidate correction separates transaction identity from semantic result/change identity: a batch range is execution metadata, not a semantic discriminator. Preserve exact causal evidence separately; do not merely remove offsets and assume that logical versions are invariant under reordered inputs. Preserve DEC-0030 rule-version exclusion and canonical citing source event identities. Verify namespace, multiplicity, ordering, duplicate evidence, null encoding, typed group keys, timestamp precision and collision handling before freezing key formats. A changed evidence set is not automatically a new operational alert.

Under [DEC-0037](../decisions/DEC-0037-event-identity-boundaries.md), distinguish native record, acquisition, source-stable, delivery, batch and stream occurrence identities. Platform resolves canonical source identity at the strongest justified scope and preserves the basis; unresolved upstream identity still permits distinct evidence references. Replay deduplication is scoped to equivalent retained evidence, not arbitrary independent reacquisition. Identity promotion must preserve historical evidence references and reconcile existing alert equivalence without generating duplicates solely because the identity basis changed. Physical Forward representation remains open pending source, consumer and compatibility verification.

Recovery determinism (restart preserves committed state and intents),
semantic replay equivalence (equivalent final results/evidence under the
same policy), and transition determinism (identical intermediate revisions)
are distinct guarantees. Require recovery and supported semantic
equivalence; define where transition equivalence is needed, including
whether provisional revisions can differ under different microbatch
boundaries or partition interleavings. Order-sensitive operators require
an explicit ordering or recoverable decision trace. Rule revision and
deployment remain immutable provenance; operational alert deduplication
continues to exclude rule version under DEC-0030.

## Temporal direction

Start with half-open event-time tumbling windows and immediate atomic detection. Provisional aggregate changes remain internal; operational aggregate alerts use finalized results. Specify watermark progression, idle partitions, allowed lateness and finalization using existing LocalStream policies. Missing or invalid observed time is excluded with reason under DEC-0029. Post-finalization evidence additions, removals and new-alert eligibility need explicit policy and fixtures before DEC-0021 can become Accepted. Never silently retract or overwrite an alert. No numerical lateness or latency setting is established.

## Execution and persistence

Platform owns binding, immutable effective deployment and artifact resolution, detection-specific interpretation and alert policy. LocalStream.Query supplies generic causal facts and references; core remains payload-opaque. Prefer normalized immutable artifacts, result revisions and typed evidence relationships; no new public Gold views. Preserve source and intermediate-result references, evidence roles, evaluated scope and bounded causal summary. Retain original content, not only digests. Detailed traces are selective and bounded; disclose truncation, redaction and expiry. Evaluate existing transactional staged output before selecting an additional coordinator. Physical DDL, storage allocation and transaction semantics remain open. See the [candidate local execution and recovery contract](NRT-PIPELINE.md#local-execution-and-recovery--candidate-contract) and [source validation](../reports/2026-11-27-localstream-execution-validation.md). Checkpoint progress, timers and output intents must share the state commit boundary; external sink acceptance is a separate idempotent protocol. Keep corrections/finalization causally ordered and never translate internal revisions into operational alert retractions.

For query recovery, the committed state checkpoint is authoritative;
subscription cursors are reconciled to it without skipping uncommitted
evidence. See [delivery acceptance and checkpoint reconciliation](NRT-PIPELINE.md#delivery-acceptance-and-checkpoint-reconciliation).
A delivery receipt proves only its declared durable sink outcome, not
source equivalence or alert identity. Preserve the distinction under
DEC-0037.

## First vertical slice and acceptance

Use the existing Authentication family after verifying applicable C10/C11 mappings. Start with atomic and compound predicates, then threshold, distinct aggregation, sequence and absence. Each increment includes binding, execution, persistence, replay and negative tests. Test duplicate delivery, changed stream offsets, rule revision, changed deployment, null/absence, invalid input, window boundaries, late corrections, restart, partial writes, expiry and unauthorized evidence access. Measure mandatory provenance overhead and diagnostic budgets; no numerical limits approved. C04 quality counters distinguish evaluation units and outcomes. C16 reads persisted explanations, never reconstructs them from the current rule.

## Gate

Complete the [source reconciliation](../reports/2026-11-26-detection-provenance-source-reconciliation.md), settle exact identity and correction semantics, verify relevant C03/C05/C10/C11/C14 prerequisites, and demonstrate the contract with fixtures before committing production interfaces. DEC-0021 remains Proposed. No implementation completion is claimed.

## Source identity and recovery conformance cases

| Case | Required invariant |
|---|---|
| Same acquired event mapped twice | Stable acquisition identity; delivery IDs may differ |
| Same batch retried | Existing batch ACK/dedup contract unchanged |
| Same native record number on different sources or source epochs | Distinct source identities |
| Identical payload from two genuine events | Do not deduplicate by payload alone |
| One source event represented in multiple Gold families | Distinct representation identities; shared source lineage |
| Windows Security EventId 4625 on multiple records | Classification code never used as unique identity |
| Same evidence under changed rule version or run | Operational alert identity unchanged under DEC-0030 |
| Crash after staged output commit, before external write | Recover exact pending intent |
| Crash after external write, before delivery confirmation | Idempotent sink retry; no duplicate result or alert |
| Missing or ambiguous source identity | Explicit unresolved lineage; no invented stable identity |
| Same group/window from multiple transport partitions | One logical aggregate under the applicable domain |
| Replay with different batch boundaries | Agreed semantic equivalence; transition differences only where permitted |
| Assigned but unseen or returning idle partition | Explicit completeness/lateness policy; no fabricated time progress |
| Timer wakeup without new input | Recoverable cause; no fabricated source offset or watermark |
| Multiple pending corrections and finalization | Causal materialization despite retry/restart |
| Budget exhaustion or unread evidence expiry | Explicit incomplete/failure outcome; no silent clean non-match |

The legacy mediation fallback key is not the target alert identity. Verify existing state transaction implementations before selecting any new coordinator. See the source reconciliation report for pinned observations.
