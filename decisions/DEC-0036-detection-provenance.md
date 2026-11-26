---
id: DEC-0036
status: Accepted
repos: [DeltaZulu.Platform, DeltaZulu.LocalStream]
governs:
  types: []
  paths: []
cites: [CON-0013, CON-0014, CON-0015]
---

# DEC-0036 — Make detection provenance a first-class contract independent of alert identity

## Context

Accepted by the owner on 2026-11-26. Collection, delivery and transformation
provenance explain how telemetry reached Gold; detection provenance must
explain how an analytic produced a result from that evidence. DEC-0030
establishes reference-based alert evidence and excludes rule version from
alert deduplication. It does not establish rule revision history or causal
evaluation records.

Tenzir's [Sigma operator reference](https://tenzir.com/docs/reference/operators/sigma/)
and [execution guide](https://tenzir.com/docs/guides/detect/execute-sigma-rules/)
provide a useful precedent: separate analytic identity, applied policy,
evidence and causal match details. Its metrics also distinguish processed
events from evaluable rule/schema pairs. The [motivating article](https://tenzir.com/blog/detection-provenance-trace-firing-rules-to-their-source/)
could not be retrieved during review; these accessible technical references,
not the inaccessible article, support the comparison. They are inspiration,
not a dependency, conformance claim or an adoption of OCSF.

## Decision

1. Detection provenance is a cross-cutting requirement of NRT detection.
   Every emitted detection result must identify the stable analytic,
   immutable original rule revision, effective evaluated policy, binding
   context (schema and relevant mapping revisions), deployment and
   execution-engine identity, and the evidence and causal decision
   sufficient to explain its emission. Retain resolvable artifacts, not
   merely mutable URLs, human-readable version labels or hashes without
   their referenced content. Distinguish exact artifact identity from
   semantic equivalence. Preserve parameters, exclusions and effective
   configuration without copying secrets into provenance.
2. Detection results are distinct from operational alerts and adjudication.
   Retain rule revision identity independently of alert deduplication.
   DEC-0030 remains binding: do not add rule version to its alert identity
   key, duplicate original telemetry in alert rows, silently retract alerts
   or overwrite their historical explanation on replay. The detailed result,
   window, evidence-reference and revision keys remain C07 design work;
   DEC-0021 window/correction semantics remain Proposed.
3. Record a bounded deterministic causal explanation for emitted results,
   with references to contributing Gold records and, where applicable,
   intermediate detection results. Explain applicable predicates and
   correlation/window decisions, including negative and absence conditions
   with their evaluation scope, time bounds and completeness limitations.
   Store richer field/operator traces selectively; disclose unavailable,
   truncated or redacted evidence rather than implying a full trace.
   Do not require full predicate tracing of every evaluated input.
4. Treat each bound rule as a consumer of declared fields, types, family,
   source applicability and time semantics. Record distinguishable
   applicability, successful match/non-match and incomplete or failed
   evaluation outcomes; do not silently weaken an unbound rule or treat
   missing required evidence as a clean non-match. Valid null/absence
   predicates follow the language contract. Aggregate diagnostic metrics
   per rule revision and appropriate source/schema/mapping scope; do not
   claim detection recall, precision or source completeness from them.
5. Preserve the established package boundaries. Platform owns rule
   content, binding, deployment, provenance policy, persistence and
   analyst presentation; LocalStream.Query provides generic operator and
   result/evidence hooks only where required. Core LocalStream remains
   payload-opaque and independent of KQL and detection-specific schemas.
   DeltaZulu.Kql remains a scalar representation contract (DEC-0032).
   No AI, new language engine, OCSF authority, extra public Gold view or
   Agent/Forward wire change is authorised by this Decision.
6. Design the provenance contract and jointly agree the C06/C07 interface
   before committing production detection operators, result schemas or
   alert persistence to an incompatible design. C06 owns semantic evidence
   and evaluation behavior; C07 owns durable identity, linkage and
   replay. C04, C10, C11, C14 and C16 support these gates through existing
   roadmap rows. Prototypes and independent prerequisite work may proceed.
   The [architecture contract](../architecture/DETECTION-PROVENANCE.md)
   elaborates testable requirements; the consolidated roadmap is the sole
   planning authority.

## Consequences

Immutable rule/policy and binding artifacts must remain accessible for
the supported evidence lifetime. Access control, redaction, retention,
bounded trace size and resource cost must be designed and tested. Missing
or expired references must be explicit. A content digest identifies bytes;
it is not by itself a proof of correct execution or cryptographic attestation.
Existing Bronze integrity, canary policy, event-time correction, result
identity and adjudication decisions are not resolved by this Decision.
No existing implementation or new public schema is certified here.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Store only rule ID and alert description | Loses the executed revision, causal decision and evidence context | — |
| Embed entire telemetry and rule content in every alert | Duplicates retained evidence and breaks reference-based alert policy in DEC-0030 | — |
| Include rule version in alert deduplication | Conflicts with DEC-0030 replay semantics | — |
| Persist every predicate invocation for every event | Unbounded cost without a demonstrated operational requirement | — |
| Treat missing or unbound fields as ordinary non-matches | Conceals evaluation and coverage gaps | CON-0015 |
| Make core LocalStream or DeltaZulu.Kql detection-aware | Violates payload opacity and the separation of type and query responsibilities | CON-0013 |

## Revisit trigger

Reopen if a reproducible fixture cannot explain a result or reconstruct
its references under the accepted policy, if bounded trace and retention
cost cannot satisfy measured operational budgets, or if a supported
operator requires a different causal representation. Changes to alert
deduplication, public schema scope, physical retention or correction
policy require their own explicit review.
