# Joint C06/C07 detection result contract

Status: design directions approved by owner 2026-11-26; detailed contract and implementation verification open. Governed by [DEC-0036](../decisions/DEC-0036-detection-provenance.md), [DEC-0030](../decisions/DEC-0030-alert-identity-and-replay.md) and [DEC-0021](../decisions/DEC-0021-threshold-as-windowed-aggregate.md) (Proposed). This is not a physical schema or separate roadmap.

## Identity and replay

Reuse assigned detection and accepted-version IDs. Derived identities use a versioned, domain-separated, unambiguous canonical encoding and deterministic digest; SHA-256 is the initial candidate. Source identity is distinct from stream position, Gold representation identity, logical result key, immutable result revision and query change identity. A query change ID includes revision and stream offsets and cannot serve as the operational alert key. Preserve DEC-0030 rule-version exclusion and canonical citing source event identities. Verify namespace, multiplicity, ordering, duplicate evidence, null encoding, typed group keys, timestamp precision and collision handling before freezing key formats. A changed evidence set is not automatically a new operational alert.

## Temporal direction

Start with half-open event-time tumbling windows and immediate atomic detection. Provisional aggregate changes remain internal; operational aggregate alerts use finalized results. Specify watermark progression, idle partitions, allowed lateness and finalization using existing LocalStream policies. Missing or invalid observed time is excluded with reason under DEC-0029. Post-finalization evidence additions, removals and new-alert eligibility need explicit policy and fixtures before DEC-0021 can become Accepted. Never silently retract or overwrite an alert. No numerical lateness or latency setting is established.

## Execution and persistence

Platform owns binding, immutable effective deployment and artifact resolution, detection-specific interpretation and alert policy. LocalStream.Query supplies generic causal facts and references; core remains payload-opaque. Prefer normalized immutable artifacts, result revisions and typed evidence relationships; no new public Gold views. Preserve source and intermediate-result references, evidence roles, evaluated scope and bounded causal summary. Retain original content, not only digests. Detailed traces are selective and bounded; disclose truncation, redaction and expiry. Evaluate existing transactional staged output before selecting an additional coordinator. Physical DDL, storage allocation and transaction semantics remain open.

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

The legacy mediation fallback key is not the target alert identity. Verify existing state transaction implementations before selecting any new coordinator. See the source reconciliation report for pinned observations.
