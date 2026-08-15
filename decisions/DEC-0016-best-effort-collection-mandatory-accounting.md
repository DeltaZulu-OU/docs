---
id: DEC-0016
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: [CON-0015]
supersedes: D16
---

# DEC-0016 — Best-effort collection, mandatory loss accounting

## Context

Collection is best-effort because it must be: no engineering recovers a `CurrentDirectory` from an exited process. Accounting is not best-effort, and it is cheap in a way collection improvements are not.

## Decision

Every Golden record carries `CollectionTier`, field provenance, and null reasons from the closed `KqlNullReason` enumeration (CON-0015). The catalogue holds a versioned tier-by-field availability matrix.

## Consequences

**This is the only design property that cannot be retrofitted.** A year of rows written without tier stamps and null reasons cannot be given them later, because the information was never captured at write time.

The hazard is specific to Golden. Silver is self-documenting about its limits — a source family lacking a field simply has no such column. Golden has the column for everyone, so a Sysmon-derived null and a 4688-derived null are indistinguishable. The layer analysts query is the layer where absence becomes ambiguous.

The matrix must be versioned: a row written under version 3 must be interpreted with version 3, or adding an enrichment tier next year silently rewrites the meaning of every null already in the lake.

**Status is `Accepted` and unimplemented.** No repository currently carries `CollectionTier`, the null-reason enum, or the matrix.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Infer tier from which fields are populated | Destroys the absent-versus-negative-evidence distinction — the exact failure this exists to prevent | — |
| Per-field reason columns | Schema doubling. The derivable-plus-exceptions design is what keeps this affordable | — |
| Defer to a later wave | Converts a scheduling decision into permanent data loss | — |

## Revisit trigger

None. This Decision does not get deferred; deferral is the failure mode it names. If it is not implemented before rows are written at volume, record that as accepted permanent loss rather than as a delay.
