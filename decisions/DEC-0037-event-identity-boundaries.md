---
id: DEC-0037
status: Accepted
repos: [DeltaZulu.Agent, DeltaZulu.Forward, DeltaZulu.Platform, DeltaZulu.LocalStream]
governs:
  types: []
  paths: []
cites: []
---

# DEC-0037 — Separate event identity domains and deduplication boundaries

## Context

Accepted by the owner on 2026-11-26, including all five reviewed architectural principles.

DEC-0030 requires stable citing event identifiers for alert replay and evidence linkage. DEC-0036 requires resolvable causal evidence. Neither establishes universal source identity across independent acquisition. The pinned source reconciliation shows that native identity evidence varies by input and may be lost during projection or forwarding.

## Decision

Distinguish native record identity, acquisition identity, canonical source-event identity, delivery and batch identity, stream occurrence, Gold representation, detection result/revision and operational alert identity. Equality in one domain does not establish equality in another.

Agent or the original collector assigns acquisition identity once and captures native identity evidence. Forward preserves available evidence without redefining RecordId or DeliveryId. Platform owns canonical source identity resolution and versioned namespace policy. LocalStream core remains payload-opaque; its existing stream occurrence identity supports replay independently of source identity.

Resolve identity at the strongest justified scope: source-stable (validated native occurrence and namespace), acquisition-stable (same retained acquisition), stream-occurrence-stable (same durable occurrence), or unresolved. These are scopes of equivalence, not confidence scores. Never infer source equality from payload equality, a classification code, a hostname alone, or an unscoped native record number. Preserve identity basis and historical resolution across scheme changes. An unresolved upstream identity must not prevent retention of the record or creation of a distinct evidence reference. Reference allocation identifies retained evidence independently of any claim of source-event equivalence. If stronger identity evidence becomes available later, record the newly established equivalence separately and preserve immutable historical references and their original resolution basis. C07 must specify and test reconciliation against existing alert identities so that identity promotion alone does not manufacture duplicate alerts. The physical reconciliation mechanism remains open.

DEC-0030's rule-version exclusion, reference-based evidence and separate adjudication remain binding. Its replay guarantee applies to equivalent retained evidence under the agreed identity scope; independent reacquisition cannot be universally deduplicated. This clarification governs the operative DEC-0030 replay guarantee. Window and changed-evidence policies remain open.

No physical wire property, schema, digest format, source namespace scheme, package release or production change is approved by this Decision. Determine whether acquisition identity alone, native identity evidence, or a structured extension is needed after consumer and source verification. Preserve the existing transport retry contract.

## Consequences

C04 distinguishes duplicate acquisition from duplicate delivery only where supported by evidence. C05 verifies propagation and mixed-version behavior. C07 defines alert/evidence keys and historical resolution. C10 separates Gold representation identity from source lineage. C12 verifies input-specific identity capabilities. C14 verifies compatibility and resource cost. These are completion criteria of existing roadmap rows, not a new roadmap.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Overload RecordId or DeliveryId | Changes existing semantics and conflates identity domains | — |
| Universal content hash as event identity | Identical genuine occurrences can have identical content | — |
| Require source-stable identity for every input | Some sources lack sufficient occurrence evidence | — |
| Derive all identity in Platform without preserving edge evidence | Information lost at acquisition cannot be recovered | — |
| Introduce both new wire identifiers immediately | Consumer requirements and mixed-version compatibility are not established | — |

## Revisit trigger

Reopen if a supported input or consumer cannot preserve evidence within its stated identity scope, if a reproducible replay fixture violates DEC-0030, or if the accepted separation cannot meet measured resource or compatibility requirements.
