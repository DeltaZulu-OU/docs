# Near-real-time pipeline — LocalStream target architecture

**Current target: 2026-11-23.** DEC-0033 replaces Timeplus Proton with
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
          Platform ingest host
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
| KQL binding adapter | Kusto.Language parsing, schema-aware binding and mapping to approved operators | Not verified as an end-to-end path |
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

Gold retains one logical C#-authored field contract under
`DEC-0012`, **ASIM-first schema naming and semantics under Accepted
`DEC-0013`**, and documented DeltaZulu extensions where ASIM cannot
faithfully represent source evidence. OCSF is not the Gold base. The approved MVP is eight telemetry families
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

**Verified implementation mismatch:** seven Silver contributors use an
`EventTimestamp` helper that falls back to Bronze `ingest_time` on missing or
unparseable source timestamps; the DNS server contributor does so explicitly.
This contradicts DEC-0029 when such rows are used for detections. Treat as
C11/P0 pending test-backed correction, not as an accepted event-time policy.

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

C05 must distinguish Forward acceptance/credit, durable LocalStream append, subscription checkpoint and DuckLake commit. No ACK timing, independent subscriber progress or exactly-once guarantee is inferred from topology. C10 traces authoritative Agent extraction through Forward/Bronze to Silver; projection of structured fields is not necessarily reparsing. The current event-time defect remains C11. C04 and C07 retain proposed assurance and window-result questions rather than introducing implicit policies.

## Detection provenance

[DEC-0036](../decisions/DEC-0036-detection-provenance.md) requires a deterministic causal result contract independent of alert deduplication. Platform owns immutable rule/effective-policy, binding and deployment artifacts; Query operators provide generic causal/evidence hooks. Persist bounded result explanations and evidence references in DuckLake. The [target contract](DETECTION-PROVENANCE.md) defines logical roles and verification boundaries. C06/C07 must agree their interface before production detection/persistence implementation; C10/C11 supply mapping and temporal validity, C04 measures evaluation health, C14 identifies execution artifacts and C16 exposes authorized explanations. No new Gold views, wire contract or change to core payload opacity is implied.

## Implementation and decision status

Phase one remains NRT-only; scheduled detections are deferred
(`DEC-0026`). `DEC-0013` (ASIM-first Gold naming) is now
**Accepted**, but its mappings are not yet verified as implemented.
`DEC-0021` (threshold/window semantics), `DEC-0024` (Bronze integrity),
and `DEC-0025` (adjudication) remain Proposed. A current architecture
description does not promote them to Accepted.

Open engineering work: KQL-to-operator binding, deterministic state,
sink idempotency and checkpoint coordination, window/late-event policies,
Gold/alert linkage, producer/sink conservation, runtime resource budgets,
and removal or retirement of legacy Proton integration.

Source check: LocalStream repository `main` at
`16f27b44fa16bcde6e9316662b25ac85ae0d4642`. Source files show
the core stream host, window/watermark operators and LiteDB state/result
stores. No build, test execution or complete Platform integration
was established by this document review.
