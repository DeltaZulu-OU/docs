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

The target LocalStream.Query processing path evaluates detections and persists
alerts to DuckLake (`DEC-0033`). Its end-to-end integration remains to be
verified. Because the LocalStream log makes replay a normal operation,
the same event can be evaluated more than once, and the alert table needs a
defined identity or replay silently manufactures incidents.

Separately, an alert has to carry enough for an analyst to act, without becoming
a copy of the data it describes.

## Decision

**Alerts reference Gold by identifier.** An alert carries sufficient enrichment
and metadata to be read on its own terms, but related logs are **linked by
identifier and never joined into the alert or duplicated inside it**.

**The alert identity key excludes rule version.** Deduplication is on rule
identity and the citing event identifiers, carried by the resolved evidence identity preserved through Silver, LocalStream-derived Gold, DuckLake Gold and alert evidence. [DEC-0037](DEC-0037-event-identity-boundaries.md) defines source-stable, acquisition-stable, stream-occurrence-stable and unresolved scopes. Independent reacquisition is deduplicable only where source-stable identity is justified; unresolved upstream identity does not prevent distinct evidence references.

**Replay must not produce duplicate alerts for equivalent retained evidence within its established identity scope. Replay may legitimately produce new alerts for old events.** For equivalent retained evidence, excluding rule version prevents a corrected rule from re-alerting evidence already associated with the same operational alert identity. Previously missed evidence may produce a new alert when the agreed identity and window policy permits it. Independent reacquisition without established source equivalence is outside this guarantee. Surfacing a genuine detection that was previously missed
is the point of correcting a rule.

## Consequences

- Alert storage stays proportional to detections rather than to telemetry. For example, an aggregate detection emitting one alert on a thousand contributing events references their identifiers rather than copying a thousand rows.
- The alert table exists only in DuckLake, with a LocalStream processing sink
  as producer rather than Proton. The Proton dual-schema requirement in
  `DEC-0028` is superseded by `DEC-0033`.
- **A corrected rule cannot retract an alert its previous version raised.** The
  identity that suppresses duplicates also prevents the correction from being
  visible as a change to the existing alert. Withdrawing a false positive is a
  separate operation on the alert, not a consequence of replay.
- Evidence resolution depends on referenced Gold being persisted. A sink
  can crash between writing Gold and an alert, leaving a dangling reference.
  No ordering-window guarantee survives the supersession of `DEC-0031`.
  The read path must report unresolved evidence explicitly; sink retries and
  reconciliation require integration tests.
- Evidence equivalence and immutable evidence references are separate mechanisms under DEC-0037. Both must remain resolvable; a later identity reconciliation must not rewrite historical references.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Join related logs into the alert row | Duplicates telemetry into the alert store, so storage scales with events rather than detections, and the copy immediately begins to diverge from Gold | — |
| Include rule version in the identity key | Every rule correction re-alerts every event the old version already caught, burying the newly-caught events the correction was made for | — |
| Suppress all alerts for events older than some threshold | Discards the genuinely valuable case — a real detection the previous rule missed — in order to avoid the duplicate case that identity already handles | — |
| Alerts with no evidence references, self-contained only | Loses the path from an alert back to the full record set in Gold, which is where investigation actually happens | — |

**Open design boundary (2026-11-25):** the accepted stable identity and rule-version exclusion remain unchanged. C07 must specify canonical ordering/deduplication of evidence identifiers, stable identity versus result revision, group/window coordinates, evidence additions/removals and replay under changed rule versions. C06/DEC-0021 window semantics must be decided before selecting a window-result identity. Do not infer a new identity key or correction/retraction policy from this note.

**Detection provenance (DEC-0036, accepted 2026-11-26):** persist the actual rule revision, effective policy, deployment and causal result/evidence references independently of the alert deduplication key. Do not overwrite an original alert's historical explanation on replay. C07 resolves detailed result and evidence identities with C06; the accepted alert identity and retraction boundary above are unchanged. See [DEC-0036](DEC-0036-detection-provenance.md).

## Revisit trigger

Reopen if analysts need a corrected rule to visibly amend or retract alerts its
earlier version raised. That is a legitimate requirement and this identity scheme
cannot express it — it would need alert versioning, which is a larger change than
adding a field to the key.
