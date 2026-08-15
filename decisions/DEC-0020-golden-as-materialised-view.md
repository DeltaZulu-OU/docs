---
id: DEC-0020
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: []
supersedes: D20
---

# DEC-0020 — Golden is a materialised view into a declared target stream

## Context

Timeplus logical views take no computing or storage resources because they are expanded into their SQL definition when queried.

## Decision

Golden is a materialised view writing `INTO` an explicitly declared target stream. Enrichment lives in that single Silver-to-Golden view, not in detection views. Dimension data lives in `versioned_kv` streams.

The compiler's authoring rule is mechanical: **if it joins or aggregates, materialise it; if it only filters or projects, a logical view is fine.** The KQL author will not be thinking about this, so the compiler must enforce it.

## Consequences

A logical Golden view would be inlined into every detection referencing it, so a hundred detection rules would maintain a hundred independent copies of the enrichment join state — cost scaling with rule count instead of with event rate.

The explicit `INTO` is not optional: without a target, an internal append stream is auto-created whose storage options cannot be customised and which is documented as unsuitable for production.

**A stall in the Golden view starves every detection simultaneously.** Its lag is a first-class operational metric and must be reported as a detection-surface outage rather than as quiet.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Logical Golden view | Enrichment join state scales with rule count | — |
| Materialised view without `INTO` | Uncustomisable internal stream; documented as unsuitable for production | — |
| Bidirectional stream-to-stream joins | Documented as exploration-only; both sides unbounded, buffering capped | — |

## Revisit trigger

If Proton's logical-view expansion stops being per-consumer, the cost argument changes and this is worth re-measuring.
