---
id: DEC-0010
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: [ProtonSchemaEmitter]
  paths: [src/DeltaZulu.Platform.Data.Proton/ProtonSchemaEmitter.cs]
cites: []
supersedes: D10
---

# DEC-0010 — Bronze write-once; Proton holds no durable Bronze or Silver

## Context

Bronze is evidence, not a processing input. Proton is a detection engine, not a lake.

## Decision

Bronze is written once and is replayable. Proton's `silver_*` streams are short-TTL staging with a TTL set explicitly at creation and bounded by detection windows.

**`ProtonSchemaEmitter`'s Bronze-stream and Silver-materialised-view emission must be stripped.** It currently instantiates a second medallion chain alongside the lake's, which is the exact duplication this Decision and principle 5.3 exist to remove.

## Consequences

Proton's Silver TTL becomes a correctness parameter rather than a tuning detail: allowed to drift, it becomes a second lake with no evidence guarantees.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Durable Bronze in Proton | A second medallion chain; two authorities for one contract | — |

## Revisit trigger

If Proton acquires evidence-grade durability guarantees and the lake does not, this ordering is worth re-examining. Not before.
