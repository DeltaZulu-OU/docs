---
id: DEC-0029
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0001]
---

# DEC-0029 — Gold is governed by extracted event time; ingest time is provenance, never detection input

## Context

Every record in the pipeline carries at least two candidate timestamps: when the
event happened at the source, and when the estate received it. Detections,
ordering and windowing all need one clock, and picking it per component produces
a system where the answer depends on which component is asked.

Ingest time is always available and always well-formed, which makes it the easy
default and the wrong one: it measures the pipeline, not the world.

## Decision

Event time is **extracted during the Silver-to-Gold transformation**, and Gold is
governed by it. Detection windows, ordering and correlation all use extracted
event time.

Ingest time is **stored** on the record as provenance. It is never an input to
detection.

The reorder buffer between Proton and DuckLake sorts on the **same extracted
event time** (`DEC-0031`), so one clock governs transformation, detection and
lake ordering rather than three.

CON-0001 applies to the carrier: KQL `datetime` is UTC-only, the carrier is
`System.DateTime` with `Kind=Utc`, and never `DateTimeOffset`.

## Consequences

- A source with a broken or absent clock degrades detection rather than ingest.
  That is the correct place for the damage to land — the record still arrives,
  is still stored, and is still huntable — but it means clock quality becomes a
  detection-quality concern and needs to be measurable.
- Keeping ingest time makes the gap between the two observable, which is the only
  way to see source clock skew and transport delay at all. Discarding it would
  make both permanently invisible.
- Detection windows are subject to late arrival: an event arriving after its
  window has closed is late by event time even though it is prompt by ingest
  time. This is inherent to choosing event time and is not a defect to be fixed
  by quietly reverting to ingest time.
- `TimestampOrigin`, among the nine FWD-CONTRACT-v2 provenance fields, becomes
  load-bearing rather than merely useful: a fallback-assigned time and an observed
  one are indistinguishable once written, and this Decision makes the difference
  govern detection.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Govern Gold by ingest time | Measures the pipeline rather than the world; two events that happened seconds apart at the source correlate or fail to correlate depending on transport delay | — |
| Carry both and let each rule choose | Makes correlation between two rules undefined whenever they chose differently, and moves a system-wide invariant into per-rule metadata | — |
| Extract event time at the agent instead | The agent has the parsing context but not the normalisation context, and doing it centrally keeps one implementation rather than one per source platform | — |
| Discard ingest time once event time is extracted | Removes the only signal that reveals source clock skew and transport delay | — |

## Revisit trigger

Reopen if a detection class requires arrival-order semantics that event time
cannot express — for example a rule about the transport itself rather than about
the events it carries. Such a rule is a statement about the pipeline, and should
be examined for whether it belongs in DQM rather than in the detection catalogue.
