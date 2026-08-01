# The near-real-time pipeline

What the estate is building in phase one, and the contracts that hold it
together. Agreed 17 August 2026.

Unlike `PIPELINE.md`, this document is not an import: it is rewritten in place as
the architecture changes, per the `architecture/` convention. The commitments it
describes are recorded as `DEC-0026`–`DEC-0031`; this document is the narrative
those Decisions are the binding form of.

## Shape

```text
Agents → Collector → Durable Silver buffer → Proton → Live Gold → NRT detections
                    └──────────────────────────────→ DuckLake Bronze, Silver
                                                        │
                                    Proton ─ reorder buffer ─→ DuckLake Gold
                                                                DuckLake Alerts
```

Two runtimes, with a strict division of role. **Timeplus Proton** is the
streaming engine: it transforms Silver into Gold and evaluates detections against
that live Gold. **DuckLake** is the governed historical lakehouse and the only
surface anybody queries.

| Stage | Responsibility | Primary outcome |
|---|---|---|
| Agents | Parse source logs locally; emit raw Bronze and parsed NDJSON Silver | Parsing stays near the source and off the central stream processor |
| Collector | Preserve source context and event identity; write Bronze and Silver to DuckLake; publish Silver to the durable buffer | Durable intake, replay, and decoupling of ingest from processing |
| DuckLake Bronze | Immutable raw logs | Forensics, parser improvement, provenance, recovery from parser defects |
| DuckLake Silver | Parsed, not yet centrally normalised NDJSON | Historical inspection and reprocessing input |
| Proton — Gold transformation | Central normalisation, schema alignment, filtering, derived fields, enrichment | A live canonical Gold representation |
| Proton — NRT detections | Continuous evaluation against live Gold | Sub-second detection and alert generation |
| Reorder buffer | Short window, sorted by extracted event time | Ordered, time-clustered writes into DuckLake |
| DuckLake Gold | Authoritative historical Gold | Hunting, audit, replay, future backfill |
| DuckLake Alerts | Alerts pushed by Proton, referencing Gold | Operational response and investigation |

## The Gold contract

Gold is **one logical schema with two physical realisations**. Proton holds the
hot live one; DuckLake persists the historical one. The logical shape — fields,
names, semantics — is identical by construction, because both are **generated
from C# code, which is the single source of truth** (`DEC-0028`). A field is
added by changing that code, never by altering either physical schema directly.

The schema library aligns partially with ASIM-like tables from Azure Sentinel and
Defender. Partial is the operative word: alignment is a starting point for
familiar field naming, not a compatibility guarantee.

Physical type alignment between DuckDB and Proton is **best effort**. Where the
two stacks express a type differently, the divergence is declared per target in
the generator rather than discovered per emitter. Differing type *names* across
engines are normal and are not divergences — `BIGINT` and `int64` are the same
shape spelled two ways. What the rule constrains is shape and semantics.

Known physical divergences today:

| Family | DuckDB | Proton | Note |
|---|---|---|---|
| Dynamic / Nested | `JSON` | `VARCHAR` | Aligned. DuckDB's `JSON` is an extension type over `VARCHAR`, so nothing diverges representationally, and the `JSON` declaration buys write-time validity checking. No `tuple` |
| IpAddress | `INET` | `ipv6` | Same address, different representation; IPv4 is native in `INET` and IPv4-mapped in Proton |
| Duration | `int64` | `int64` | Shape matches; the *unit* is the divergence. CON-0014 fixes ticks and `LogicalDurationUnit` has no `Ticks` member |
| Binary / Array / Map | — | — | Undeclared on both sides; currently explicit rejections rather than invented mappings |

Duration is the one worth watching, because it passes a shape check and is still
wrong: identical physical type, different meaning.

## Detections read live Gold, never the lake

Detection rules consume Proton's live Gold. They must **not** wait for Gold to
land in DuckLake and read it back — that round trip forfeits the latency the
design exists for.

The **KQL-in-YAML rule catalogue** remains the single rule interface. KQL is
transpiled to Proton SQL for continuous detection, and the same KQL is
transpilable to DuckDB for threat hunting and offline validation against
DuckLake. The second target does not imply the rule runs as a scheduled
detection: hunting and scheduled execution are distinct, and in phase one rule
metadata permits only the NRT execution type (`DEC-0026`).

## Time

Gold is governed by **extracted event time** (`DEC-0029`). Ingest time is also
recorded, but it is provenance and is never an input to detection. The reorder
buffer sorts on the same extracted event time, so one clock governs
transformation, detection, and lake ordering.

## The two buffers

They are different things with different requirements, and conflating them would
be expensive.

The **Silver buffer**, between collector and Proton, is the replay source of
truth. It needs real durability and retention. It decouples agents and collectors
from Proton availability, and it is what lets Proton rebuild Gold and bounded
detection state after a restart or a rule correction.

The **reorder buffer**, between Proton and DuckLake, holds a short window and
sorts by event time (`DEC-0031`). It exists for two reasons that would each
justify it alone: it bounds the window in which an alert can reference Gold rows
not yet persisted, and it makes DuckLake's Gold time-clustered, which is the
pruning key for essentially every hunting query. It can be lightweight
*precisely because replay exists* — if it loses records in flight, Proton
regenerates them from the Silver buffer. That cheapness is purchased by the
replay path, and would be revoked with it.

## Identity, alerts, and replay

A **stable event identifier** is carried from the agent through Silver, Proton
Gold, DuckLake Gold, and alert evidence. It is what makes both alert
deduplication and evidence linkage implementable.

Alerts are pushed by Proton into DuckLake's alert tables and **reference Gold by
identifier** (`DEC-0030`). An alert carries enough enrichment and metadata to be
read on its own terms, but related logs are linked by identifier and never joined
into the alert or duplicated inside it.

The alert identity key **excludes rule version**, and that exclusion is doing
real work. Replaying a corrected rule over historical events does not re-alert
events that already alerted, because dedup holds on identity. It *does* alert
events the previous rule missed — and surfacing a genuine detection that was
previously missed is valuable, not noise. Suppressing it would make rule
correction pointless. So: replay never produces duplicate alerts, and old events
with no existing alert may legitimately raise one.

## What is deliberately not decided

Recorded here so that silence is not mistaken for resolution.

- **Enrichment is deferred.** Reference-data home, refresh path, and what a
  detection sees during a stale or mid-refresh lookup are all open.
- **Bronze payload digests** remain `DEC-0024`, still `Proposed`. CON-0020 makes
  this irreversible: a Bronze row written without a digest cannot be given one
  later. The collector is being designed now, which is the last cheap moment.
- **Gold schema migration mechanics.** Generation from C# guarantees the two
  physical schemas agree at build time; it does not by itself say how a running
  Proton and an existing DuckLake table migrate in step when a field is added.
- **Late arrivals past the sort window** must be appended out of order, since
  dropping them would be loss. DuckLake Gold is therefore *mostly* sorted, and no
  reader should assume strict ordering.
- **Unresolved evidence on the read path.** The reorder buffer bounds the window,
  but a crash between the Gold write and the alert write can still leave a
  dangling reference. The read path should say so rather than render an empty
  result.
- **The three physical divergences** in the table above.
