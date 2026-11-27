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

## Result and evidence identity — candidate contract

The [identity source review](../reports/2026-11-27-result-identity-review.md) records implementation gaps.
The following domains are conceptual, not approved physical schemas.
DEC-0030, DEC-0036 and DEC-0037 remain authoritative.

| Domain | Equality and lifetime |
|---|---|
| Artifact | Exact immutable content and artifact kind; retain resolvable bytes |
| Effective deployment | Actual bound rule revision, parameters, exclusions, schema/mapping, engine and policy artifacts |
| Execution transaction | One recoverable commit attempt/outcome in a state generation; input ranges or timer causes |
| Logical result | Bound query revision/output/operator and canonical logical coordinates, including window where applicable |
| Result revision | Immutable committed value, causal evidence and evaluation disposition within logical result |
| Delivery intent | Exact staged change and target; retries preserve payload and identity |
| Evidence reference | Immutable retained occurrence/representation reference, independent of later equivalence resolution |
| Evidence equivalence | Strongest justified source/acquisition/stream scope, with historical resolution basis |
| Operational alert | Stable rule identity and citing evidence equivalence under DEC-0030; excludes rule revision/run |

Do not require logical result or revision IDs to survive arbitrary
changes in rule, deployment or temporal policy. Semantic replay
equivalence is a separately evaluated relation. Transaction ranges and
processing attempts are provenance, not alert identity. Persist exact
staged intent bytes before dispatch; immutable content must not change
after staging. Include target in delivery identity if multiple targets
are supported, or enforce one target explicitly. A repeated identity
with different immutable content is a conflict, not successful dedup.

Use versioned domain-separated canonical framing; reject malformed
text or use a reversible representation. SHA-256 is a candidate
index/identifier, not proof of content equality or execution. Resolve
digest collisions explicitly. Never use a digest alone as evidence.
A logical sequence number may order revisions in a generation but
does not prove semantic equivalence across replay interleavings.

### Evidence and causal explanation

Store immutable references to contributing Gold representations and
intermediate results, with role and relevant occurrence/multiplicity.
For order-sensitive operators preserve the order required by their
semantics. For set-based alert equivalence, a candidate is canonical
sorting and deduplication of resolved citing identifiers; preserve
original causal multiplicity separately. Window/group discrimination,
role-sensitive equivalence and changed evidence policy require owner
approval before freezing the alert key. Do not infer a universal
source identity or use payload hashes to deduplicate real occurrences.

A causal record identifies the effective deployment, logical result
revision, operator/predicate outcome, admitted evidence, evaluated
scope, temporal policy and completeness limitations. Preserve original
artifact content, not merely a label or digest. Keep secrets outside
the provenance record. Negative conditions require an explicit scope,
bounds and completeness basis; lack of an event alone is insufficient.
Absence and sequence remain outside the initial qualified operator
surface. Bounded explanations may reference a durable evidence
manifest; do not silently truncate mandatory causal references.
If mandatory evidence cannot be retained, fail or mark evaluation
incomplete under the approved policy. Optional traces disclose
truncation, redaction and expiry.

### Replay and identity reconciliation

| Scenario | Candidate required behavior |
|---|---|
| Retry exact committed intent | Same target/identity/content; no duplicate durable result |
| Same evidence, corrected rule revision | Preserve new result provenance; suppress equivalent operational alert under DEC-0030 |
| Previously missed evidence | May emit new alert under approved identity/window policy |
| Changed contributing evidence | Preserve immutable revisions; alert eligibility remains open |
| Stronger evidence identity established later | Preserve historical references and basis; reconcile existing alert equivalence before creating another alert |
| Conflicting content under same reference | Explicit integrity conflict; no silent overwrite |
| Gold reference missing or expired | Report unresolved/expired status; reconcile where possible |
| Rule correction changes previous match to non-match | No automatic alert retraction or historical explanation rewrite |

Identity promotion is not a destructive rewrite. Record a versioned
equivalence assertion with basis and scope; candidate lookup checks
existing alerts under justified equivalent identifiers before creating
a new one. Concurrent promotion and alert creation require a verified
serialization or atomic uniqueness protocol. Do not merge identities
on ambiguous evidence; preserve separate references and report
unresolved equivalence. Exact physical alias/index mechanism and
reconciliation of previously distinct alerts remain open.

Persist result and evidence linkage with an idempotent acceptance
boundary. Where Gold and result/alert commits cannot share a verified
transaction, use explicit unresolved linkage and recoverable
reconciliation; no implied cross-store atomicity. Operational alert
creation and its deduplication authority must agree atomically or
through a proven recovery protocol. An append-only writer alone
does not establish uniqueness. Preserve original alert explanation;
later evaluations can be retained independently without modifying it.

## Bound scalar and grouping semantics — candidate contract

[DEC-0032](../decisions/DEC-0032-kql-type-versus-query-language-boundary.md)
remains binding. The [semantic source review](../reports/2026-11-27-kql-semantic-review.md) distinguishes
current implementation from candidate behavior.

Platform binds authored KQL against the approved schema and Kusto.Language
symbols, resolves overloads and result types, and rejects unsupported
operators with structured diagnostics before deployment. Reuse the
existing relational representation where its semantics suffice; do not
assume a SQL translation or successful parse proves stream equivalence.
LocalStream.Query receives bound operations and opaque canonical keys.
DeltaZulu.Kql retains declared scalar representation and normalization.
Do not introduce a second grammar, general interpreter or new package.

| Semantic operation | Required distinction |
|---|---|
| Representation | Declared scalar type, carrier, value and loss provenance |
| Expression comparison | Bound operator, coercion, null and string semantics |
| Grouping | Equivalence relation over bound group coordinates |
| Exact distinct | Bound aggregate inclusion policy and equivalence |
| Persistent identity | Versioned canonical encoding of the applicable equivalence class |

Preserve absent fields, typed nulls, conversion failures and legitimate
empty strings as distinct provenance. Do not extend or merge the closed
collection and conversion reason enumerations (CON-0015). A typed null
carrier is not proof that a language-level string null is supported.
Apply KQL predicate semantics at the bound operator boundary, not CLR
Boolean coercion or SQL three-valued logic by assumption. Only a true
predicate admits a row; preserve evaluation diagnostics independently
of ordinary non-match. Unsupported or failed evaluation is not a clean
non-match.

### Initial supported surface and qualification

Start with the Authentication atomic and compound predicates, typed
literals, explicit supported comparisons and Boolean operators, then
fixed-window grouping, count and exact distinct aggregation. The actual
operator allowlist must follow authored rules and conformance evidence.
Count admitted rows independently of whether a distinct operand is
included. Distinguish exact count_distinct from approximate dcount;
do not substitute either silently. Null inclusion, empty-input results,
numeric promotion, string comparison and function overloads must be
verified for each supported operation. Defer dynamic grouping,
nonfinite real keys and other unqualified cases rather than invent
semantics. A valid KQL construct may be unsupported in NRT.

### Canonical key contract

Use an explicit format version and domain, ordered tuple arity,
stable type tags, null/value markers and unambiguous length framing.
Encode values after the bound grouping/distinct equivalence policy,
not before coercion. Equal values under that policy must produce equal
bytes; unequal values must not collapse. Separate evidence identity,
group keys and distinct operands. Use full canonical bytes for equality;
if a digest indexes them, verify equality on collision. Never persist
CLR hash codes, symbol references, culture-dependent formatting or
numeric SyntaxKind values. A textual key carrier may use a reversible
encoding of bytes; raw delimiter concatenation is insufficient.

| Type family | Candidate encoding obligations |
|---|---|
| bool, int, long | Explicit tags and fixed-width integer representation; bound promotion first |
| decimal | Canonical coefficient/scale for equal values, normalize signed zero |
| real | Specify signed zero and nonfinite semantics before support; no silent lossy grouping |
| string | Exact bound comparison semantics; preserve empty and whitespace; strict reversible encoding, no implicit case folding or Unicode normalization |
| datetime, timespan | UTC DateTime carrier under CON-0001; signed duration ticks under CON-0014; preserve 100 ns precision |
| guid | Explicit stable byte order, independent of CLR memory layout |
| dynamic | Defer key support until recursive type, object order, array order, null and numeric semantics are qualified |

Physical tag values, byte order and version migration are not frozen.
Do not reuse Forward wire tags as semantic identity by assumption.
A default KqlValue or unsupported declared type must be rejected at
the binding/value boundary. Do not turn a conversion-loss placeholder
into an ordinary value without the declared policy.

Exact distinct membership uses canonical bytes, not digest alone.
Represent excluded operands explicitly rather than inserting a null
sentinel or empty byte sequence unconditionally. Budget exhaustion
must fail or mark the affected evaluation incomplete, never switch
to approximate counting. Keep logical group identity independent of
transport partition. Qualify packed-library consumers across the
supported Kusto.Language version span under CON-0021/C14; source
recompilation alone is insufficient.

## Temporal direction — candidate contract

DEC-0021 remains Proposed. The initial scope is immediate atomic
detection and fixed, epoch-aligned, half-open event-time tumbling windows.
Threshold predicates belong in authored KQL if DEC-0021 is accepted.
Sliding/session windows, sequence and absence require separate semantics.
The [temporal source review](../reports/2026-11-27-temporal-execution-review.md) records current behavior and
unexecuted conformance fixtures.

### Time and window assignment

Observed time is authoritative under DEC-0029. Preserve UTC 100 ns ticks;
never substitute ingestion or processing time. Invalid or unavailable
observed time remains in Bronze/Silver with reason and cannot contribute
to event-time operators or watermark progress. Valid timestamps outside
the supported window arithmetic range require explicit evaluation
diagnostics, not clamping into a different window. Future-time plausibility
policy is source-specific and remains open.

For positive fixed duration D, epoch E and observed time t, assign
start = E + floor((t - E)/D) * D, end = start + D.
Use checked integer ticks and mathematical floor for pre-epoch values.
Membership is start <= t < end. Bind only KQL expressions whose
window alignment and type semantics are demonstrated equivalent.

### Progress and completeness

Track assigned source namespace/topic/partition, maximum valid observed
event time, last activity, initialization and idle status. A candidate
watermark is the minimum active source maximum minus configured
out-of-orderness, bounded to the representable time range; published
watermark is monotonic within an execution generation. It is a policy
estimate, not proof that no older evidence can arrive.

An assigned but unseen source blocks advancement by default until it
has valid progress or an explicitly approved exclusion. Distinguish
transport activity from valid event-time progress: invalid timestamps
cannot advance the latter. Idle exclusion is a recorded policy decision,
not proof of completeness. If all sources are idle or unseen, hold the
watermark. Returning sources cannot regress it; classify their records
against the previously committed watermark. A missing required evidence
range is a coverage failure, not an idle source. No numerical disorder,
idle or lateness settings are approved.

### Window lifecycle and transaction order

| Condition | Candidate disposition |
|---|---|
| Watermark absent or event time >= previous watermark, window not final | On-time update |
| Event time < previous watermark, watermark < end + allowed lateness | Late accepted; update provisional result |
| Watermark >= end + allowed lateness | Finalization eligible; later arrivals cannot mutate that finalized revision silently |
| Finalization deadline unrepresentable | Reject unsupported window/policy combination explicitly |
| No matching events | No synthetic aggregate or absence alert unless explicitly specified |

Allowed lateness is nonnegative and distinct from out-of-orderness.
At equality with the finalization deadline, the window is eligible to
finalize. Evaluate an input against prior committed temporal progress,
apply its admitted effects, advance progress and finalize eligible
windows in causal order. Define equivalent behavior across microbatch
boundaries; do not classify a record against a watermark advanced by
later records in the same batch. The ordering of cross-partition inputs
and idle decisions must be specified or recorded where it affects
admission or finalization.

Persist complete progress, window state, timer changes and ordered
output intents in the same state transaction. A timer wakeup may
reevaluate idle policy or discover due windows; it cannot invent an
event timestamp or source range. Use a durable deadline index and
recoverable temporal cause. Repeated timer delivery is idempotent.
A finalization result must reference the exact immutable aggregate
revision and evidence; do not assume a value-less finalize marker is
sufficient without causal delivery and durable prior value.

Provisional changes remain internal. Operational aggregate alerts use
finalized results under the candidate direction. Preserve too-late
evidence and record its evaluation disposition. Whether post-finalization
evidence creates a correction, a new eligible result or only a diagnostic
requires owner approval; no silent retraction or overwrite of alerts.
State reclamation follows finalized-result durability, evidence retention
and replay obligations, not the timer alone.

### Replay and acceptance

Recovery must reproduce committed progress, admitted evidence and pending
intents. Semantic replay equivalence is conditional on equivalent
admission and temporal decisions; identical input sets alone are not
sufficient when late-event policy is order-sensitive. Persist or
deterministically reconstruct relevant source order, policy revision,
idle decisions and temporal causes. Do not require global ordering for
operators whose declared semantics do not depend on it.

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

## Resource limits and causal conservation

The [resource qualification contract](NRT-PIPELINE.md#resource-qualification--candidate-contract) governs bounded execution. Mandatory evidence and exact aggregate semantics cannot be silently discarded to satisfy a budget. Distinguish serialized bytes from working-set memory; bounded optional trace truncation must be disclosed. The candidate transaction-local cache must preserve temporal admission and causal transitions.
