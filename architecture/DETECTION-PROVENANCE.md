# Detection provenance — target contract

**Status:** Accepted methodology under [DEC-0036](../decisions/DEC-0036-detection-provenance.md),
2026-11-26. This document specifies logical requirements and verification
boundaries, not implemented APIs, SQL DDL or a separate roadmap.
The [consolidated roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md) owns all work items and sequencing.

## Logical model

| Logical artifact | Responsibility and minimum information |
|---|---|
| DetectionRule | Stable analytic identity and authoring language |
| DetectionRuleRevision | Immutable source definition, origin/revision where available, content digest and resolvable original |
| DetectionDeployment | Effective policy/configuration, immutable binding context, relevant Gold and mapping revisions, engine/build/dependency identity and activation scope |
| DetectionResult | Evaluation/result identity, analytic and revision references, deployment, outcome, relevant event-time coordinates and causal summary |
| DetectionEvidence | Typed references to Gold family/record identity and intermediate result revisions; evidence roles and availability |
| DetectionTrace | Bounded condition/operator and correlation explanation, with completeness/redaction status |
| AlertEvent / AlertEntity | Existing operational views; link to the triggering result without changing DEC-0030 deduplication |

Names here describe roles; they do not mandate separate tables, C# classes,
public identifiers or a particular storage layout. The approved ten public
Gold views under DEC-0034 remain unchanged. Content hashes need documented
serialization and algorithm choices; retain actual content for inspection.
Execution context must identify dynamic lookup/enrichment versions when
they affect the decision, or explicitly declare that exact replay cannot
be guaranteed. A compiled-plan fingerprint alone is insufficient.

## Causal evaluation contract

The Platform query-owning adapter binds required fields and their types,
source applicability and temporal semantics before execution. Generic
LocalStream.Query operators may expose evidence and state transitions
without taking a dependency on rule languages, ASIM or Platform models.
Core LocalStream and Forward remain unchanged by this contract.

A positive predicate identifies the resolved input and the outcome; a
negative predicate records the actual evaluated condition rather than
fabricating a positive observable. Absence and sequential correlation
require the inspected scope, correlation key, time bounds, ordering and
watermark/completeness context appropriate to the operator. An absent
observation is not proof that an event never occurred. Aggregate results
identify contributing evidence, group/window, measured value and
decision threshold where applicable. Intermediate results are linked by
their actual revisions; changes of evidence or late results must not
silently rewrite earlier explanations.

Persist the standard causal summary and references for every emitted
result. Detailed field values and operator traces are optional diagnostic
data with access control, explicit bounds, redaction, expiry and declared
truncation. Do not sample away the minimum emitted-result record. Agree
measurable byte, state, cardinality and latency budgets before production;
test high-cardinality windows and replay. No specific numerical limit or
retention duration is approved yet.

## Evaluation quality

For each rule revision and explicitly defined evaluation unit (an input
event for a stateless predicate, a window/result opportunity for an
aggregate, or a defined correlation opportunity), distinguish:

| Outcome | Meaning |
|---|---|
| Not applicable | Outside the rule's declared source/schema or time applicability |
| Matched | Applicable evaluation completed with a positive result |
| Not matched | Applicable evaluation completed with a negative result under defined language semantics |
| Missing required data | Evaluation cannot establish the required condition because evidence is absent |
| Invalid data | Required input violates the declared semantic/type contract |
| Binding failure | Rule cannot bind required fields/operators to a supported context |
| Evaluation failure | Runtime execution did not establish a result |

Binding failures before individual evaluations require a rule/deployment
health metric and explicit unavailable coverage, not an invented event
count. Valid null/absence predicates may evaluate successfully. Excluded
missing/invalid observed timestamps remain visible in C11/DQM rather than
being evaluated using ingest time. Pending windows are not completed
non-matches.

For a defined scope and completed applicable opportunities, evaluation
coverage is (matched + not matched) / (matched + not matched + incomplete
or failed applicable evaluations). Count each opportunity once under a
documented retry/deduplication policy; report the denominator and
excluded/not-applicable/pending counts separately. Do not mix event,
window and correlation denominators. Zero or unknown denominators are
unavailable, not 100%. This is an evaluation-health measure, not
precision, recall, delivery assurance or source-wide completeness.
Retain bounded aggregate counters, not a full trace of every non-match.

## Verification boundaries

| Existing work item | Required evidence |
|---|---|
| C04 | Quality counters distinguish successful evaluation, coverage gaps and failures; artifact/reference integrity and expiry are explicit without asserting cryptographic attestation |
| C05 | Existing delivery/replay fixtures preserve evidence identifiers through retry and expiry; no new wire or ACK contract follows |
| C06 | Rule/policy/binding identity and causal result interface agreed with C07 before production implementation; semantic fixtures cover positive, negative, null, missing, unbound, runtime failure, aggregate, sequence and absence cases; resource overhead measured |
| C07 | Durable artifact and result references survive restart/replay, rule updates, partial writes and expiry; same-evidence alert dedup follows DEC-0030; original alert explanation remains intact; unresolved references disclosed |
| C10 | Rule-to-field dependency inventory ties applicability, types and source/mapping revisions to the existing C# Gold contract; incompatible or incomplete mappings are explicit |
| C11 | Missing/invalid observed time excludes event-time evaluation and is separately counted with reason; no ingest-time substitution |
| C14 | Build/package and engine/dependency identities can resolve executed artifacts; cross-version semantic and resource regression fixtures remain reproducible |
| C16 | Authorized analysts can navigate alert to exact evaluated revision, causal explanation and permitted evidence; unavailable/redacted evidence is shown explicitly |

## Design decisions still open

C06/C07 must agree result and evidence identity domains, immutable artifact
representation, canonical serialization, window/result revision and
retraction semantics, and persistence/checkpoint coordination. C04/C07/C16
must agree retention horizons, access controls, redaction and diagnostic
budgets. Physical schema, API and instrumentation mechanisms must follow
source-backed design and tests. No new acceptance of DEC-0021, DEC-0024,
DEC-0025 or changed DEC-0030 alert identity is implied. Scheduled detection
remains deferred under DEC-0026.

## Result identity and reconciliation

The [candidate result and evidence identity contract](DETECTION-RESULT-CONTRACT.md#result-and-evidence-identity--candidate-contract) separates execution, revision, intent, reference, equivalence and operational alert domains. It specifies candidate causal evidence, replay and promotion obligations without changing DEC-0030/0036/0037. Physical persistence and changed-evidence policy remain open.
