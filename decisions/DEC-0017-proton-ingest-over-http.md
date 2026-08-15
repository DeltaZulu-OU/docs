---
id: DEC-0017
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: [ProtonHttpExecutor]
  paths: [src/DeltaZulu.Platform.Data.Proton/ProtonHttpExecutor.cs]
cites: []
supersedes: D17
---

# DEC-0017 — Proton ingest over HTTP

## Context

Settled by precedent rather than by argument: the Platform already ships `ProtonHttpExecutor` and typed Bronze publishers against the OSS image.

**Agent ADR 0012 rejected the REST ingest API as "documented as a Timeplus Enterprise feature". That is a factual error, and it propagated into ADR 0016.** See `archive/RECOVERY.md` Part 2.

## Decision

Proton ingest is over HTTP, in the array-of-arrays positional form. **Agent ADR 0016's bespoke-native-sink premise is retired.**

## Consequences

The array-of-arrays form fits a catalogue that already owns column order. The JSON hop is a *governed* type-loss boundary between two known schemas — materially weaker than the original NDJSON problem, but it is the only such boundary in the design and must be recorded as one rather than left implicit.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Bespoke native sink | Premise was a factual error about Enterprise gating; contradicted by shipped code | — |
| Kafka-API-compatible intermediate | Adds a broker whose properties DEC-0019 moved onto the collector | — |

## Revisit trigger

If Proton's HTTP ingest gains a documented throughput ceiling the deployment cannot live under, benchmark before re-opening — Wave 5 has the Proton ceiling measurement.
