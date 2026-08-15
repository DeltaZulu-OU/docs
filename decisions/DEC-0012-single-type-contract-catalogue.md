---
id: DEC-0012
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: [ILogicalSchemaRegistry, MedallionSchemaCatalog]
  paths: [src/DeltaZulu.Platform.Domain/Analytics/Schema/LogicalSchemaRegistry.cs, src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/MedallionSchemaCatalog.cs]
cites: [CON-0014, CON-0015]
supersedes: D12
---

# DEC-0012 — Type-contract catalogue is the single authority, producer-agnostic

## Context

**Settled in principle, violated in practice.** `LogicalSchemaRegistry` and `MedallionSchemaCatalog`/`SchemaObjectDef` are two authorities for one contract, and the former has no production consumers.

**It is worse than that, verified 2026-08-15.** `LogicalSchemaRegistry.cs` in `DeltaZulu.Platform.Domain` declares the enums, the record types, and `public interface ILogicalSchemaRegistry` — and **no implementation of that interface exists anywhere under `src/`**. The only `LogicalSchemaRegistry` class in the repository is in the test project. So the registry is not merely a second authority with no consumers; it is an interface with no production implementation, which is why the section 11.1 divergences can persist unnoticed — nothing executes the code path they describe.

This was found by `governs-check` rejecting an earlier draft of this Decision that claimed to govern a type named `LogicalSchemaRegistry`.

## Decision

One producer-agnostic catalogue is the authority for field names, types, and their physical projections into each engine.

## Consequences

The section 11.1 divergence list is largely a consequence of the split rather than a set of independent bugs. Two of its entries are load-bearing beyond their apparent size: `ToKustoType`'s `_ => KustoType.String` default is exactly the silent coercion DEC-0003 forbids *and* exactly the closed-enum fallthrough the estate rule bans; and the duration ticks-versus-microseconds divergence is CON-0014, a factor-of-ten error that looks like a plausible number rather than like corruption.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Keep both authorities, sync them | Hand-maintained agreement between two schema authorities diverges on a timescale of months | — |

## Revisit trigger

Revisit if a genuine second consumer emerges whose needs the single catalogue cannot express — not if the two merely prove awkward to merge.
