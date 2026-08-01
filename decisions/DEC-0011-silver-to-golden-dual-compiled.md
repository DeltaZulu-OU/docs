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

## Status note — narrowed 2026-08-17

`DEC-0027` settles that Proton is never queried by users; DuckLake is the sole
read surface for both Gold and alerts. That changes what the equivalence test
below has to prove, though not whether it is still required.

Before `DEC-0027`, the concern was a dual-query-surface discrepancy: a user
reading Proton's Gold and a user reading DuckLake's Gold seeing different
answers to the same question. That concern no longer applies, because there is
only one user-facing answer — DuckLake's.

What survives is narrower and still real: **an alert's evidentiary basis has to
be reconstructible from the record an analyst will actually be looking at.**
`DEC-0030` has alerts reference Gold by identifier rather than embedding it, so
an alert fired against Proton's live Gold is only useful if the identifier it
cites resolves in DuckLake's Gold to a row that means the same thing. Divergence
here does not surface as two users seeing different numbers — it surfaces as an
alert an analyst cannot investigate, or a hunt that fails to find what a
detection already found.

The DQM-specified test — cross-engine divergence rate, including null and
reason equality, per build plus a production sample (DQM §6.3, primitive at
§5.7) — is still the right instrument. Its purpose is now audit and
reconstructibility rather than user-facing consistency, and that is a narrower
thing to guarantee: it is checked offline against build and production samples,
not live on every read, because no read ever compares the two engines directly.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| B — Proton authors, lake mirrors | Inverts the durability ordering the design rests on: a Proton outage becomes a permanent hole in the evidence lake. **Ruled out regardless** | — |
| C — Separate .NET mapper | Held as the fallback. Provenance and null-reason semantics are natural in C# and awkward in ClickHouse-dialect SQL. Costs a hop of detection latency | — |
| D — Mapper plus Proton twin | Two implementations in two languages. Rule out unless benchmarks force it | — |

## Revisit trigger

Fall back to option C if writing sparse null-reason maps, closed reason enumerations, and versioned tier-matrix lookups in ClickHouse-dialect SQL proves to be the thing that fights you. Re-examine if the equivalence test cannot be made to pass on a hostile fixture.
