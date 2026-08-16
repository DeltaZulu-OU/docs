---
id: DEC-0025
status: Proposed
repos: []
governs:
  types: []
  paths: []
cites: [CON-0017]
---

# DEC-0025 — DeltaZulu measures precision, never recall, and splits a miss into its two causes

## Context

No surveyed platform natively measures false negatives. Alert counts,
dispositions, tuning history and ATT&CK mappings are all equally consistent with
excellent and with poor recall — a falling alert count means better tuning or
lost telemetry, and nothing internal distinguishes them.

## Decision

Three positions, stated so they hold under commercial pressure:

- DeltaZulu **can** measure precision, given analyst dispositions **and a
  disposition coverage figure reported alongside**. Precision below high coverage
  is meaningless and must not be shown without it.
- DeltaZulu **cannot** measure recall from any pipeline metric. Recall estimates
  come only from simulation ground truth, per campaign, and are never inferred
  from alert volume.
- DeltaZulu **can** do what the surveyed platforms cannot: split a miss into a
  **content gap** (telemetry reached Golden, no rule fired) and a **collection
  gap** (telemetry never arrived) — and in the second case name the field and the
  reason it was absent.

**Adjudication gets no live health indicator, by design.** Precision and recall
move on the timescale of a purple-team campaign, not an alert queue, and a live
light would invite exactly the inference this Decision exists to prevent.

## Consequences

- The miss-attribution split is the join between detection engineering and the
  quality instrumentation, and it is the whole argument for that instrumentation.
- It depends entirely on `RecordId` lineage, `CollectionTier`, null reasons and
  the capability matrix — which is to say it depends on the full nine-field
  provenance set landing in FWD-CONTRACT-v2. Without those, this Decision is
  unimplementable and DeltaZulu's position collapses to the same "no alert" the
  rest of the market reports.
- The narrower claim is defensible. "We measure false negatives" would not be.
- Open: simulation cadence determines whether the split is a quarterly report or
  an operational signal. Continuous low-rate simulation gives a live figure but
  risks alert fatigue and contaminating the precision measurement; campaign-based
  simulation is cleaner but stale for most of its life.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Infer recall from alert-volume trends | Equally consistent with better tuning and with lost telemetry | CON-0017 |
| Report precision without disposition coverage | Precision over an unadjudicated majority is not a measurement | — |
| Treat an ATT&CK mapping as coverage | A mapping is an inventory, not a working control | — |
| A live adjudication health light | Invites the volume-as-recall inference on a timescale the metric cannot support | CON-0017 |

## Revisit trigger

Reopen if a simulation harness achieves continuous coverage broad enough that a
recall estimate stops being campaign-bound — at which point the cadence question
above is the thing that has been answered.
