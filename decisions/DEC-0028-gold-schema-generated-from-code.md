---
id: DEC-0028
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0014]
---

# DEC-0028 — One Gold contract generated from C#; physical alignment between engines is best effort

## Context

Gold exists in two physical realisations — Proton's live representation and
DuckLake's historical one. Hand-maintaining two schemas that must agree is a
standing invitation to drift, and drift between them is close to undetectable
from either side alone: each engine is internally consistent while disagreeing
with the other.

`DEC-0012` already establishes a single type-contract catalogue. This applies
that principle to the Gold schemas specifically, and names the mechanism.

## Decision

**The C# schema library is the source of truth.** Both the Proton and the
DuckLake Gold schemas are generated from it. Neither physical schema is edited
directly, and a field is added by changing the code and regenerating.

The library aligns **partially** with ASIM-like tables from Azure Sentinel and
Defender. Partial is load-bearing: the alignment buys familiar field naming for
people arriving from those products, and is not a compatibility guarantee.

**The logical shape is identical across both engines** — same fields, same names,
same semantics — because one generator emits both.

**Physical type alignment is best effort.** Where DuckDB and Proton cannot
express a type the same way, the divergence is declared per target in the
generator rather than left to each emitter. Differing type *names* are not
divergences: `BIGINT` and `int64` are one shape spelled twice. The rule
constrains shape and semantics, not spelling.

Declared divergences today:

| Family | DuckDB | Proton | Status |
|---|---|---|---|
| Dynamic / Nested | `JSON` | `VARCHAR` | Aligned. DuckDB's `JSON` is an extension type over `VARCHAR`, so the declaration costs nothing representationally and buys write-time validity. No `tuple` |
| IpAddress | `INET` | `ipv6` | Same address, different representation |
| Duration | `int64` | `int64` | Shape matches, unit diverges — see below |
| Binary / Array / Map | — | — | Undeclared on both sides; explicit rejections, not invented mappings |

## Consequences

- Shape identity is guaranteed structurally rather than by review. Two schemas
  that cannot be edited independently cannot drift independently.
- Adding a Gold field is a code change with a build, which is slower than a
  schema edit and is the point.
- **Duration is the dangerous entry.** Both engines use `int64`, so it passes any
  shape check while the *unit* differs. CON-0014 fixes ticks as canonical and
  `LogicalDurationUnit` still has no `Ticks` member. A divergence that survives
  the check designed to catch it is worse than one that fails loudly.
- Declaring `JSON` on the DuckDB side restores write-time JSON validity, which a
  bare `VARCHAR` would not. That rejection must be **accounted** as a recorded
  loss with a reason per `DEC-0016`, not faulted on — consistent with the
  estate's reject-not-coerce posture.
- Proton reports a `VARCHAR` column as `string` when described, so the alias
  survives DDL but not round-trip. Any Proton-side drift check needs alias
  normalisation, as `SchemaApplier.NormalizeType` already does for DuckDB.
  Without it every JSON column reports a permanent phantom mismatch, and people
  learn to ignore the check.
- Generation guarantees the two schemas agree at build time. It does not by
  itself say how a running Proton and an existing DuckLake table migrate in step
  when a field is added. That mechanism is not yet decided.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Maintain the two physical schemas by hand against a written spec | Drift is undetectable from either engine alone, since each stays internally consistent while disagreeing with the other | — |
| Generate Proton from DuckLake's schema, or the reverse | Makes one engine's type system the ceiling for the other, and encodes an accidental hierarchy between two runtimes with different strengths | — |
| Require exact physical type identity with no exceptions | Unbuildable: the stacks genuinely differ, and the rule would be broken on day one and then ignored | — |
| Full ASIM compatibility rather than partial | Commits the estate to another product's schema evolution, for a benefit that is familiarity rather than interoperability | — |

## Revisit trigger

Reopen if a third consumer of the Gold contract appears outside Platform, which
would make the generator rather than the schemas the thing that needs its own
home — or if the best-effort exception list grows to the point that "same shape"
stops being a fair description of what the two engines hold.
