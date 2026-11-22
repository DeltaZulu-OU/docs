---
id: DEC-0032
status: Accepted
repos: [DeltaZulu.Kql, DeltaZulu.Platform]
governs:
  types:
    DeltaZulu.Kql: [KqlTypes]
  paths:
    DeltaZulu.Kql: [src/DeltaZulu.Kql/KqlTypes.cs]
cites: [CON-0002, CON-0006, CON-0009, CON-0014, CON-0015]
---

# DEC-0032 — Keep the KQL type contract separate from query-language processing

## Context

The source review at `reports/2026-11-23-sqlglot-kql-boundary-review.md`
compared SQLGlot's SQL parser, AST, optimizer and dialect generators with
`DeltaZulu.Kql`. They solve different problems: SQLGlot processes query
languages, while `DeltaZulu.Kql` maps declared KQL scalar types to CLR
carriers and reports representation loss. `Microsoft.Azure.Kusto.Language`
already supplies the underlying KQL language model.

`DEC-0003` governs typed value normalization and encoding; `DEC-0012`
governs the Platform field/schema catalogue. Neither requires the type
contract to own parsing or query transformation. The accepted archived
Platform ADR 0002 already specifies Kusto-based parsing, controlled
relational translation and one execution path. `DEC-0011`'s dual-compiled
Silver-to-Gold approach remains `Proposed`, not accepted.

## Decision

1. **Preserve the scope of `DeltaZulu.Kql`.** It owns the supported
   `ScalarSymbol` surface, CLR carrier mapping, declared `KqlValue`
   values, per-field normalization and `KqlLossReason`. It does not own
   a query grammar, AST, scope resolver, optimizer, SQL generator or executor.
2. **Retain `Microsoft.Azure.Kusto.Language` as the KQL language
   authority.** Query-owning components, including `DeltaZulu.Platform`,
   should use its syntax, symbol and semantic-analysis facilities instead
   of maintaining another KQL grammar or symbol system. The application
   continues to own schema policy, safe translation, structured diagnostics
   for unsupported features, and execution controls.
3. **Do not adopt SQLGlot as a KQL language dependency.** Its SQL
   architecture offers relevant techniques, but support for SQL dialects
   does not establish Kusto KQL conformance. No new query-analysis module,
   transpiler or rewrite pipeline is authorized by this Decision.
4. **Preserve distinct authorities.** `DEC-0012`'s catalogue owns logical
   field contracts and physical projections; `DeltaZulu.Kql` owns
   scalar representation. Do not infer declared KQL types from CLR
   runtime values or duplicate `ScalarSymbol`'s type relationships.
5. **Do not change established execution choices.** `DEC-0027` keeps
   DuckLake the sole user-visible read surface, with Proton internal.
   `DEC-0011` remains `Proposed` until its own equivalence gate is met.
   AST round-tripping alone is not evidence of semantic equivalence.

The `governs` entries anchor the existing `KqlTypes` surface in CI;
they do not mechanically enforce the responsibility boundary.

## Consequences

The type contract stays small and retains its Kusto.Language 9.2.0–12.4.1
compatibility requirement (`CON-0006`). Query analysis may evolve in
query-owning components without expanding that contract. The cost is
continued reliance on Microsoft Kusto semantics and separate validation
for any cross-engine emission or optimization.

The accompanying source report records three **unverified engineering
questions** about normalization and binary compatibility. It neither
declares test failures nor changes `DEC-0003`.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Expand `DeltaZulu.Kql` into a general KQL compiler | Duplicates language responsibility and couples the type contract to query evolution | CON-0002, CON-0006 |
| Use SQLGlot's SQL AST as the KQL authority | A SQL parser or dialect generator is not automatically KQL-conformant | — |
| Derive declared KQL types from CLR values or duplicate Kusto type symbols | Violates type fidelity and risks contradictory type answers | CON-0009, CON-0015 |
| Build a new transpiler or optimizer immediately | No verified feature gap or approved boundary justifies it | — |

## Revisit trigger

Reopen if a reproducible requirement, with a failing semantic fixture,
demonstrates that Kusto.Language plus the existing controlled query path
cannot provide a required capability. Also reopen the compatibility
aspect if the supported Kusto.Language versions lose their common
required API. A decision on `DEC-0011` must satisfy that Decision's own
cross-backend evidence requirements.
