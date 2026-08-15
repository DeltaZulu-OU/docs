---
id: DEC-0006
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D6
---

# DEC-0006 — Server performs mapping and enrichment, not parsing

## Context

Enrichment lookup data — CMDB, GeoIP, threat intelligence, enum tables — is volatile, tenant-scoped, sometimes commercially licensed, and far larger than anything sensibly shipped to a fleet.

## Decision

Mapping to canonical names and enrichment from lookup data happen server-side. Parsing does not (DEC-0005).

## Consequences

Meaning can be corrected retroactively, because it is applied where the data is retained. This is the asymmetric-reversibility argument that decides most of the endpoint/server split.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Ship lookup tables to the fleet | Volatile, large, sometimes licensed; a semantic change could not be applied to already-collected events | — |

## Revisit trigger

If a lookup becomes both tiny and stable, and latency demands it at the edge, the split is worth re-examining for that lookup alone — not as a general reversal.
