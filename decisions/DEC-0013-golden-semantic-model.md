---
id: DEC-0013
status: Proposed
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: []
supersedes: D13
---

# DEC-0013 — Golden semantic model and naming

## Context

**Open, and the register recorded it as open.** The consolidated document proposes OCSF-derived semantics in an ASIM-like flat shape. Platform ADR 0007 says DeltaZulu-owned names with optional OCSF lineage. These are different decisions.

One piece of evidence bears on how settled the OCSF reading is: *OCSF* and *ASIM* appear in exactly one file fleet-wide and in no source file.

## Decision

**Not decided.** Recorded as `Proposed` so it is visibly open rather than absorbed by default.

## Consequences

Every detection, dashboard and approved view binds to table and field names, so deciding this after content exists is a migration rather than a refactor. It gates the class-grouping rule in Wave 3.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| OCSF-derived semantics | Not yet reconciled against Platform ADR 0007 | — |
| DeltaZulu-owned names with OCSF lineage | Platform ADR 0007's position; not yet reconciled against the consolidated document | — |

## Revisit trigger

Decide before the first Silver→Golden mapping is written. This Decision must reach `Accepted` or be split before DEC-0011 leaves `Proposed`.
