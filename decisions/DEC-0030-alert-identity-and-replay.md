---
id: DEC-0030
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: []
---

# DEC-0030 — Alerts reference Gold by identifier, and dedup on an identity that excludes rule version

## Context

Proton evaluates detections and writes alerts to DuckLake (`DEC-0027`). Because
the Silver buffer makes replay a normal operation rather than an exceptional one,
the same event can be evaluated more than once, and the alert table needs a
defined identity or replay silently manufactures incidents.

Separately, an alert has to carry enough for an analyst to act, without becoming
a copy of the data it describes.

## Decision

**Alerts reference Gold by identifier.** An alert carries sufficient enrichment
and metadata to be read on its own terms, but related logs are **linked by
identifier and never joined into the alert or duplicated inside it**.

**The alert identity key excludes rule version.** Deduplication is on rule
identity and the citing event identifiers, carried by the stable event identifier
that runs from the agent through Silver, Proton Gold, DuckLake Gold and alert
evidence.

**Replay never produces duplicate alerts. Replay may legitimately produce new
alerts for old events.** These are not in tension, and the exclusion of rule
version is what makes both true at once: replaying a corrected rule over history
does not re-alert events that already alerted, because dedup holds on identity;
it does alert events the previous rule missed, because those have no existing
alert to dedup against. Surfacing a genuine detection that was previously missed
is the point of correcting a rule.

## Consequences

- Alert storage stays proportional to detections rather than to telemetry. A rule
  firing on a thousand events produces one alert referencing a thousand
  identifiers, not a thousand copied rows.
- The alert table has no dual-shape problem. It exists only in DuckLake, with
  Proton as producer rather than store, so it needs DuckDB-only governance and no
  cross-engine type negotiation — unlike Gold (`DEC-0028`).
- **A corrected rule cannot retract an alert its previous version raised.** The
  identity that suppresses duplicates also prevents the correction from being
  visible as a change to the existing alert. Withdrawing a false positive is a
  separate operation on the alert, not a consequence of replay.
- Evidence resolution depends on the referenced Gold rows being present. The
  reorder buffer bounds the window in which they are not (`DEC-0031`), but a
  crash between the Gold write and the alert write can still leave a dangling
  reference. The read path must say so rather than render an empty result.
- The stable event identifier becomes load-bearing for two separate mechanisms —
  dedup and evidence linkage — so weakening it breaks both at once.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Join related logs into the alert row | Duplicates telemetry into the alert store, so storage scales with events rather than detections, and the copy immediately begins to diverge from Gold | — |
| Include rule version in the identity key | Every rule correction re-alerts every event the old version already caught, burying the newly-caught events the correction was made for | — |
| Suppress all alerts for events older than some threshold | Discards the genuinely valuable case — a real detection the previous rule missed — in order to avoid the duplicate case that identity already handles | — |
| Alerts with no evidence references, self-contained only | Loses the path from an alert back to the full record set in Gold, which is where investigation actually happens | — |

## Revisit trigger

Reopen if analysts need a corrected rule to visibly amend or retract alerts its
earlier version raised. That is a legitimate requirement and this identity scheme
cannot express it — it would need alert versioning, which is a larger change than
adding a field to the key.
