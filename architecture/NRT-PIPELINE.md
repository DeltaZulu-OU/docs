# Near-real-time pipeline — LocalStream target architecture

**Current target: 2026-11-27.** DEC-0033 replaces Timeplus Proton with
DeltaZulu.LocalStream and its separate Query package. This describes
the agreed target and does not certify that every adapter is implemented.
The prior Proton plan in `PIPELINE.md` is a historical import; see
`PIPELINE-ERRATA.md`.

## Processing topology

```text
Agent collection/parsing
     │
     ├── node-local LocalStream (optional agent replay)
     └── DeltaZulu.Forward (network transport)
                  │
                  ▼
          Platform collector executable (DEC-0022)
                  │
          ├── DuckLake Bronze (write-once raw evidence)
          ├── DuckLake Silver (retained parsed records)
          └── platform-local LocalStream (durable log)
                             │
                     independent subscribers
                             │
                  LocalStream.Query / processors
                             │
                     Gold + detections / alerts
                             │
                     idempotent lake sinks
                             ▼
                     DuckLake Gold + Alerts
                             │
                     hunting and investigation
```

This diagram is a responsibility map, not a verified deployment.
The collector is a separate Platform deployable under DEC-0022; the diagram
neither assigns every downstream consumer to its process nor fixes the
physical persistence sequence.
LocalStream is not a network transport. Forward remains inter-node
transport; DurableBuffer is an optional edge queue. The exact ingest
sequencing, topics, commit/ACK boundaries and end-to-end sink topology
require integration tests.

## Separate package boundaries

| Package or layer | Responsibility | Source-level status |
|---|---|---|
| `DeltaZulu.LocalStream` | Payload-opaque topics, partitions, ordered offsets, replay, independent subscriptions, retention and processor hosting | Implemented primitives |
| `DeltaZulu.LocalStream.Query` | Already-bound query operators, keyed state, event-time windows, watermarks, aggregates and result changes | Implemented primitives; not full KQL execution |
| `DeltaZulu.LocalStream.Query.LiteDB` | Optional durable state and query-result stores | Implemented adapters; production behavior unverified |
| `DeltaZulu.Kql` | Declared scalar representation and normalization | Existing type library; not an expression evaluator |
| Platform query-owning adapter | Kusto.Language binding, schema-aware planning, language semantics and mapping to approved operators | Existing compiler is SQL/DDL-oriented; stream binding not verified |
| Lake sink adapters | Stable, idempotent persistence of Bronze/Silver/Gold and alert records | Must prove replay, crash/retry and loss handling |

Core LocalStream remains KQL-independent and payload-opaque
(`CON-0013`). `DeltaZulu.Kql` remains the declared-type/CLR-carrier
contract, not the stream-query processor (`DEC-0032`).

## Data and queries

DuckLake retains Bronze evidence, parsed Silver, canonical Gold and
alerts, and remains the **only user-facing analytics read surface**.
LocalStream is bounded node-local replay storage, never a substitute
for the historical lake. No Proton ingestion, materialised views,
Gold schemas, or SQL detection engine belong in the target.

**Source-level correction gate (2026-11-23):** the existing Gold contracts
contain 71 fields across DNS, Network Session, Process Event and Authentication,
but do not yet declare ASIM's mandatory common field names. The proposed
field-by-field adaptation and the remaining conformance gaps are recorded in
`ASIM-GOLD-MAPPING-BASELINE.md`. That document is a candidate mapping,
not a deployment-ready schema contract.

[DEC-0038](../decisions/DEC-0038-medallion-schema-conventions.md) consolidates the single C#-owned catalogue, layer-specific naming and field handling, ASIM-first Gold semantics and documented DeltaZulu extensions. Bronze preserves source spelling; governed Silver and Gold logical fields use PascalCase. Source aliases are explicit and record-local normalization preserves lineage. OCSF is not the Gold base. The approved MVP is eight telemetry families
and two operational views under [DEC-0034](../decisions/DEC-0034-mvp-asim-tables-and-views.md).
Use singular PascalCase logical names in KQL and `golden.<Name>` for SQL
views; Gold as an architectural layer does not rename the SQL schema.
The archived `*Activity` migration is superseded.
The Proton physical-schema projection requirements of
`DEC-0028` are superseded. DuckLake mappings must preserve declared
types, null reasons and canonical duration ticks (`CON-0014`).

KQL may remain an authoring surface, but support must be verified
independently for binding KQL to stream operators and translating
allowed hunting queries to DuckDB. `DEC-0011`'s dual Proton/DuckDB
compilation proposal is Rejected. Parsing or AST comparison is not
an oracle for behavioral equivalence.

## Event time, replay and alert evidence

**C11 Silver correction:** all eight contributors now retain missing or
invalid observed timestamps as null with an explicit reason, as recorded in
the [verification report](../reports/2026-11-26-silver-event-time.md) and
consolidated roadmap. Integrated three-host CI passed according to C11.
The downstream evaluation diagnostics and watermark exclusion remain open.
Retain affected records in Bronze/Silver; do not substitute ingest time for
observed time or admit them to event-time processing.

Extracted event time governs Gold windows and correlation; ingest time
remains provenance (`DEC-0029`). LocalStream delivery is at-least-once,
with ordering only within each partition. Retention may expire before
a subscriber catches up; `OffsetExpired` requires deliberate
recovery or reset. There is no exactly-once or global ordering claim.

Sinks must be replay-safe and idempotent. Alerts retain stable identity,
deduplicate across replay and reference Gold by identifier
(`DEC-0030`). A crashed or partial lake write may leave unresolved
evidence. The read path must disclose missing references and the sink
must be tested for correction/reconciliation. The former
Proton-to-DuckLake reorder window (`DEC-0031`) is **not inherited**.
An alternative window or lake clustering policy needs its own evidence
and decision.

### Delivery and source-lineage verification

C05 must distinguish Forward acceptance/credit, durable LocalStream append, subscription checkpoint and DuckLake commit. No ACK timing, independent subscriber progress or exactly-once guarantee is inferred from topology. C10 traces authoritative Agent extraction through Forward/Bronze to Silver; projection of structured fields is not necessarily reparsing. Downstream event-time integration remains C11. C04 and C07 retain proposed assurance and window-result questions rather than introducing implicit policies.

## Local execution and recovery — candidate contract

The [27 November source validation](../reports/2026-11-27-localstream-execution-validation.md) identifies concrete gaps
in the current Query and LiteDB primitives. These design corrections are
proposed implementation directions within C05/C06/C07, not new Accepted
Decisions or verified behavior. Preserve the existing package boundaries,
segmented transport and optional LiteDB adapter. No new engine is justified
without measured failure to satisfy the workload.

Asynchronous bounded input acquisition and sink delivery surround a
synchronous transaction boundary. Begin, state access, mutation, commit
and rollback must execute on the owning thread with no suspension while
a LiteDB transaction is open. Check transaction outcomes; a failed or
ambiguous commit must not advance external progress. Start with exclusive
mutation ownership per query state domain; the existing database-wide
writer gate may serialize different domains. Dedicated thread execution
is an alternative only if required. Do not hold database transactions open
during network I/O, backpressure waits or lake writes.

Persist operator state, contiguous committed progress for every assigned
source topic/partition, temporal state, durable timer changes and ordered
output intents atomically. Use a stable stream namespace/epoch where
needed to distinguish recreated sources. A source batch may cover one
partition at a time; the checkpoint must still represent the complete
domain. Specify inclusive/exclusive offsets and initialization; never
advance over unread gaps or regress on retries. Reconcile subscription
progress against the state checkpoint before replay; prune any committed
range ledger only after its recovery obligations are discharged.

Logical group/window identity is independent of the physical input
partition. If future parallel execution is necessary, use stable logical
ownership rather than change grouping semantics. Platform supplies bound
comparisons and canonical typed key encoding; Query implements generic
operators, not KQL. Preserve UTC tick precision and distinguish grouping,
expression equality and durable identity.

Durable output sequences must preserve causality within the relevant
domain (or explicitly defined narrower ordering scope). Fetch bounded
pages through indexed progress, retry with the same identity and verify
durable sink acceptance before retiring intents. A hash is not an order.
Never claim an atomic transaction spans LocalStream state and DuckLake.

Temporal/maintenance transitions must have recoverable causes without
invented source ranges. Processing-time wakeups are not evidence of
event-time completeness. Define assigned but unseen, idle and returning
partitions, per-source progress, deterministic ties and lateness policy
before finalization; use persisted decisions when required for replay.
Missing trustworthy observed time cannot advance event-time watermarks.

Bound queues, microbatch size/bytes/time, state/cardinality, timer count,
pending outbox, evidence/provenance and replay ledgers. On exhaustion
apply explicit backpressure or fail the affected evaluation with a
diagnostic; never silently drop required evidence or turn incompleteness
into a non-match. Retention expiry requires an explicit recovery/failure
path under C05, even for a required subscription. Benchmark before
changing the persistence engine, adding shards or a generic DAG runtime.

### Delivery acceptance and checkpoint reconciliation

The [delivery recovery audit](../reports/2026-11-27-delivery-recovery-contract-review.md) identifies additional Forward,
Bronze and subscription boundaries. The following is a candidate
protocol, not an approved physical ingest sequence or wire change.

| Boundary | Evidence required before advancing |
|---|---|
| Forward positive ACK | Entire accepted batch recoverable at the agreed durable boundary; duplicate success only after that acceptance is known |
| Collector append | Durable occurrence coordinates and retry reconciliation for every accepted item; partial batch completion is not whole-batch acceptance |
| Bronze/lake subscriber | Evidence and receipt durably committed together before subscription progress advances |
| Query input | State, source progress, timers and pending output committed together before acknowledging the consumed prefix |
| External result delivery | Idempotent sink durably accepts the original intent; only then retire it |

Credit, admission into a deduplication cache, successful decoding and
successful durable acceptance are different states. A concurrent
duplicate must wait or obtain a non-success outcome while the original
acceptance is pending. Bounded memory deduplication is an optimization,
not the durable acceptance authority. Existing transport IDs and
retry behavior must be traced before introducing new identity fields;
partial appends require reconciliation with an explicitly established
retry scope. The final ACK boundary (durable spool or lake) remains C05
design work, not resolved by this table.

For query-owned subscriptions, use the committed query state as the
authoritative recovery position, not the independently stored transport
cursor. Represent each assigned stream namespace/topic/partition with
its initialized inclusive last committed offset (or explicit
uninitialized status); next read is its successor. Persist assignment
and progress together. A newly created required consumer must record its
intended start rather than silently adopting the earliest retained offset.

| Restart observation | Candidate recovery action |
|---|---|
| Transport cursor equals state cursor | Read next uncommitted offset |
| Transport cursor behind state | Reconcile cursor to verified committed progress; do not reevaluate committed state |
| Transport cursor ahead of state | Stop normal consumption; recover missing prefix from verified retained evidence or declare incomplete scope |
| No checkpoint or unknown stream epoch | Validate explicit initial assignment and retained range; no implicit success or state reuse |
| Earliest retained offset exceeds required next offset | Record missing range; recover only from an approved equivalent replay source or mark affected scope incomplete |
| State commit outcome unknown | Reopen and inspect durable transaction generation/progress/intents before advancing |

Normal commits must not regress or skip an unprocessed gap. Administrative
reset is distinct from normal commit: define authorization, audit,
state rebuild and replay effects. A source epoch or incompatible state
format change cannot silently inherit a previous cursor. No checkpoint
alone proves durable evidence conservation.

For sink-only consumers, the sink receipt and evidence are the
authoritative durable outcome for replay, with a separately checkpointed
subscription. Scope receipt identity to the stream occurrence and
appropriate namespace, not payload equality or universal source-event
identity. Conflicting content under an existing identity is an explicit
error requiring reconciliation. A durable receipt must not outlive or
misrepresent the recoverable evidence it attests to; define retention
and rebuild behavior together. Verify actual DuckLake transactional
configuration; do not infer a cross-store transaction.

The minimum failure matrix covers admission-before-commit duplicates,
partial append, ACK loss, credit shrink, crash after sink commit,
retention expiry, cursor divergence, incompatible source epochs and
separate collector lifecycle. Required subscribers do not prevent
retention loss merely by existing. Backpressure must be bounded and
propagate before the recoverable evidence budget is exhausted; disclose
loss or incomplete evaluation when recovery is impossible.

The detailed [candidate temporal contract](DETECTION-RESULT-CONTRACT.md#temporal-direction--candidate-contract)
defines window membership, source initialization, watermark progression,
late admission, finalization and replay obligations. DEC-0021 remains
Proposed; no default numerical policy or post-finalization alert
behavior is approved.

## Detection provenance

[DEC-0036](../decisions/DEC-0036-detection-provenance.md) requires a deterministic causal result contract independent of alert deduplication. Platform owns immutable rule/effective-policy, binding and deployment artifacts; Query operators provide generic causal/evidence hooks. Persist bounded result explanations and evidence references in DuckLake. The [target contract](DETECTION-PROVENANCE.md) defines logical roles and verification boundaries. C06/C07 must agree their interface before production detection/persistence implementation; C10/C11 supply mapping and temporal validity, C04 measures evaluation health, C14 identifies execution artifacts and C16 exposes authorized explanations. No new Gold views, wire contract or change to core payload opacity is implied.

## Implementation and decision status

Phase one remains NRT-only; scheduled detections are deferred
(`DEC-0026`). `DEC-0038` (consolidated schema conventions) is **Accepted**, but its mappings are not yet verified as implemented.
`DEC-0021` (threshold/window semantics), `DEC-0024` (Bronze integrity),
and `DEC-0025` (adjudication) remain Proposed. A current architecture
description does not promote them to Accepted.

Open engineering work: KQL-to-operator binding, deterministic state,
sink idempotency and checkpoint coordination, window/late-event policies,
Gold/alert linkage, producer/sink conservation, runtime resource budgets,
and removal or retirement of legacy Proton integration.

Source check: see the [27 November validation report](../reports/2026-11-27-localstream-execution-validation.md) for pinned
LocalStream, Kql and Platform revisions, findings and unexecuted tests.
No runtime correction, new package release or end-to-end integration is
certified by this document update.
