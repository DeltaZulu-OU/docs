---
id: DEC-0011
status: Proposed
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D11
---

# DEC-0011 — Silver→Golden authored once in KQL, compiled to both dialects

## Context

See `reports/2026-08-15-golden-placement.md` for the full options analysis. This is section 9 option A.

## Decision

Silver→Golden is authored once in KQL and compiled to a DuckLake statement and a Proton materialised view.

## Consequences

Two emissions, one authoring. **Status stays `Proposed` until the CI equivalence test exists** — without it, option A is option D with extra steps, and the difference is not visible from the outside.

Silver-to-Proton replay becomes mandatory rather than optional, because Silver is then the only thing from which Golden can be rebuilt after a Proton outage.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| B — Proton authors, lake mirrors | Inverts the durability ordering the design rests on: a Proton outage becomes a permanent hole in the evidence lake. **Ruled out regardless** | — |
| C — Separate .NET mapper | Held as the fallback. Provenance and null-reason semantics are natural in C# and awkward in ClickHouse-dialect SQL. Costs a hop of detection latency | — |
| D — Mapper plus Proton twin | Two implementations in two languages. Rule out unless benchmarks force it | — |

## Revisit trigger

Fall back to option C if writing sparse null-reason maps, closed reason enumerations, and versioned tier-matrix lookups in ClickHouse-dialect SQL proves to be the thing that fights you. Re-examine if the equivalence test cannot be made to pass on a hostile fixture.
