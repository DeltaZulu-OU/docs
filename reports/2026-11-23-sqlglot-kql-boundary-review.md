# SQLGlot versus DeltaZulu.Kql — source review

**Date:** 2026-11-23. **Method:** Repository source and documentation
inspection only; no build, test execution, benchmark, or live backend
comparison was performed.

**Revisions inspected:** [DeltaZulu.Kql at
`2f61c60`](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/tree/2f61c60db6a5df28c8ead33cab8de105e086bb13)
and [SQLGlot at
`089891f`](https://github.com/tobymao/sqlglot/tree/089891f2521780e2c5b243005017af9db62f25a6).
The existing estate Decisions and archived Platform ADRs were checked
on `DeltaZulu-OU/docs` before this amendment.

## Question and findings

Should SQLGlot capabilities be added to `DeltaZulu.Kql`?

SQLGlot implements SQL parsing, AST transformations, query-scope analysis,
logical optimization, lineage, structural diffing and multi-dialect SQL
generation. The inspected built-in dialect directory has no Kusto KQL
dialect. This does not exclude plugins or future implementation.

`DeltaZulu.Kql` exposes a deliberately small KQL **type contract**:
`KqlTypes.All`, `FromName`, `ClrCarrier` and `TryNormalize`, together
with `KqlValue` and `KqlLossReason`. It delegates KQL type semantics
to `Microsoft.Azure.Kusto.Language` and does not implement parsing,
optimization, SQL transpilation or execution.

These are different layers, so a direct feature-parity comparison would
misstate the purpose of `DeltaZulu.Kql`. The resulting boundary
decision is `DEC-0032`.

## Existing authorities

| Authority | Decision / evidence | Status |
|---|---|---|
| Tagged values and conversion-loss semantics | `DEC-0003` | Accepted |
| Platform logical field and schema catalogue | `DEC-0012` | Accepted |
| KQL language parsing, controlled translation, shared query execution | Archived Platform ADR 0002 | Accepted in archive |
| DuckLake as the user-facing read surface | `DEC-0027` | Accepted |
| KQL Silver-to-Gold compiled for two engines | `DEC-0011` | **Proposed** |

## Verification questions — not confirmed defects

1. **Scope of the "never throws" promise.** `KqlTypes.TryNormalize`
   explicitly throws for a null `target`. Also, converting an arbitrary
   non-scalar object to `string` can call its `ToString()`, which may
   throw. Clarify valid-input preconditions or test and handle adversarial
   conversions. The existing hostile matrix does not prove behavior for
   arbitrary caller-defined conversion methods.
2. **Typed-null on unsupported targets.** When `target.Name` is outside
   the supported carrier map, `TryNormalize` returns `false` and
   `result = default` rather than a typed null of the requested symbol.
   Decide whether unsupported symbols are outside the contract, and
   make the stated failure behavior and tests agree.
3. **Shipped binary compatibility.** Tests under
   `DeltaZulu.Kql.Tests.V1241` compile the sources against
   Kusto.Language 12.4.1 rather than loading the library binary built
   against 9.2.0. They establish source compatibility. If runtime
   binary loading is part of the release guarantee, test the shipped
   9.2.0-built DLL in a 12.4.1 host.

These observations warrant tests or clarification, not an automatic change
to the value contract. No repository code was modified by this review.

## Future query-analysis validation

Only after a concrete requirement emerges, prototype Kusto.Language
syntax and semantic analysis in the query-owning layer. Build fixtures
for nested scopes, aliases, dynamic and null values, datetime/timespan,
unsupported operators and backend-specific functions. For cross-engine
translation, compare actual execution behavior and diagnostics;
AST equivalence is not sufficient.

## Reviewed sources

- [SQLGlot](https://github.com/tobymao/sqlglot)
- [DeltaZulu.Kql README](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/main/README.md)
- [KqlTypes.cs](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/main/src/DeltaZulu.Kql/KqlTypes.cs)
- [KqlValue.cs](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/main/src/DeltaZulu.Kql/KqlValue.cs)
- [TryNormalizeTests.cs](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/main/tests/DeltaZulu.Kql.Tests/TryNormalizeTests.cs)
- [12.4.1 conformance project](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/main/tests/DeltaZulu.Kql.Tests.V1241/DeltaZulu.Kql.Tests.V1241.csproj)
- [Archived Platform ADR 0002](../archive/DeltaZulu.Platform/0002-analytics-query-safety-and-execution.md)
