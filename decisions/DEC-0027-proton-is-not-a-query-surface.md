---
id: DEC-0027
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: []
---

# DEC-0027 — Proton is a streaming runtime, not a query surface; DuckLake is the only thing users read

## Context

The estate runs two engines that both hold Gold records. Without an explicit
rule about which one users query, the answer drifts toward "whichever is
convenient", and the two engines acquire user-visible behaviour that must then
be kept consistent forever.

## Decision

**Proton is internal.** No user queries it, directly or through the product. It
transforms Silver into Gold and evaluates detections against that live Gold, and
its outputs reach users only by being written somewhere else.

**DuckLake is the sole read surface** — Gold for threat hunting and history,
alerts for response. Alerts are therefore stored in DuckLake and pushed there by
Proton, rather than being read from Proton on demand.

## Consequences

- Cross-engine equivalence becomes an asymmetric and much narrower question. The
  test that matters is not "do both engines return the same rows to a user" — one
  of them never returns rows to a user — but "is a detection that fired in Proton
  reconstructible in DuckLake for hunting". That is smaller and more tractable
  than a dual-query-surface guarantee, and it narrows what `DEC-0011` has to
  prove.
- Proton needs no query authorisation model, no tenant isolation on the read path,
  and no user-facing query surface to secure.
- Alert latency to the analyst is bounded by the Proton-to-DuckLake write and the
  reorder window (`DEC-0031`), not by detection latency. Detection stays
  sub-second; visibility does not, and that is the accepted trade.
- Anything a user must see has to be written to DuckLake deliberately. There is
  no fallback of exposing a Proton stream directly, and asking for one is a
  signal that something is missing from the lake rather than a shortcut.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Let users query Proton for live data | Creates a second user-visible surface with its own dialect, authorisation model and consistency semantics, and makes every Gold divergence between the engines a user-visible defect | — |
| Read alerts from Proton on demand | Couples the response workflow to streaming-runtime availability, and leaves alerts with no durable home | — |
| Serve hunting from Proton and history from DuckLake | Splits one user question across two engines by recency, so the answer depends on how old the data is | — |

## Revisit trigger

Reopen if a product requirement cannot be met by writing to DuckLake — for
example a live operational view whose latency budget is below the reorder window.
The correct first response is still to write it to the lake; only a demonstrated
inability to do so reopens this.
