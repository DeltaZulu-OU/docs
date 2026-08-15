---
id: CON-0005
status: Accepted
subject: Type name aliases
---

# CON-0005 — Alias tables, both versions

`ScalarSymbol.Aliases` verbatim, as reflected from each package:

| Type | 9.2.0 | 12.4.1 |
|---|---|---|
| `bool` | boolean | boolean |
| `datetime` | date | date |
| `decimal` | *(none)* | *(none)* |
| `dynamic` | *(none)* | *(none)* |
| `guid` | uniqueid, uuid | uniqueid, uuid |
| `int` | int16, int32, int8, uint, uint16, uint32, uint8 | int16, int32, int8, uint, uint16, uint32, uint8 |
| `long` | int64, uint64, ulong | int64, uint64, ulong |
| `real` | double, float, **single** | double, float |
| `string` | *(none)* | *(none)* |
| `timespan` | time | time |
| `type` | *(none)* | *(none)* |
| `null` | — *(type absent)* | *(none)* |

## The `single` divergence

`single` is an alias of `real` in 9.2.0 and **not an alias in 12.4.1**.
Consequently `ScalarSymbol.From("single")` and `ScalarTypes.GetSymbol("single")`
return `real` in the Agent's process and **null** in Platform's process.

Every other spelling probed resolves identically across both versions, including
the load-bearing case: `ulong` and `uint64` both resolve to `long`.

## Consequences

- A type-name resolver that delegates blindly to `From`/`GetSymbol` is
  process-dependent for exactly one input. Any estate-owned resolver must take
  an explicit position on `single` — reject it in both, or map it in both —
  rather than inherit the divergence.
- Note that `uint`, `uint32` and friends resolve to `int`, and `ulong`/`uint64`
  to `long`. The alias table is lossy about signedness: a `ulong` above
  `long.MaxValue` has no representable KQL type, which is a conversion problem
  (CON-0009's neighbourhood), not a naming one.

## Verified

`reports/2026-08-15-kusto-language-preflight.md`, item 2.
