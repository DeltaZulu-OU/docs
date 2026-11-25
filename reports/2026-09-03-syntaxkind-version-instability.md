# Session — SyntaxKind version instability (Kusto.Language 9.2.0 vs 12.4.1)

Date: 2026-09-03. Environment: clean cloud container, .NET SDK 10.0.111.
Method: real cross-repo consumption, not a synthetic probe. `DeltaZulu.Kql`'s
relational IR and KQL→RelNode translator (extracted from `DeltaZulu.Platform`
in this session, see `DEC-0032`) were packed locally and wired into
`DeltaZulu.Platform`, which pins `Microsoft.Azure.Kusto.Language` `12.4.1`
while `DeltaZulu.Kql` compiles against the `9.2.0` floor (`CON-0006`).

## Verdict: `Kusto.Language.Syntax.SyntaxKind`'s underlying values are NOT stable across the version span

A prior compile-time-only probe (naming every `Kusto.Language.Syntax` type and
`SyntaxKind` member the translator uses, compiled against `[9.2.0]` and again
against `[12.4.1]`) passed cleanly on both. That probe could not have caught
this: the bug is not about a symbol's *existence*, but about an *enum member's
integer value* — invisible to any check that only verifies compilation.

## How it surfaced

Every full-solution Platform test run against the locally packed
`DeltaZulu.Kql` build failed ~12 tests with diagnostics like:

```
[Translate/Error] Unsupported literal kind: StringLiteralExpression
[Translate/Error] Unsupported binary operator: EqualExpression
```

for KQL containing plain string literals and equality comparisons — code paths
the translator's own conformance suite (210/210, both Kusto.Language versions)
had already exercised without incident.

## Root cause, confirmed directly

A throwaway console probe read `(int)SyntaxKind.X` against each package version:

| `SyntaxKind` member | 9.2.0 | 12.4.1 |
|---|---:|---:|
| `StringLiteralExpression` | 439 | 348 |
| `LongLiteralExpression` | 433 | 342 |
| `EqualExpression` | 487 | 406 |
| `GreaterThanExpression` | 485 | 404 |
| `AndExpression` | 489 | 408 |

`SyntaxKind` is a plain enum. A C# `switch` on an enum value compiles to an
integer comparison against a constant baked in at **compile time** — of the
*compiling* assembly's Kusto.Language version. `DeltaZulu.Kql` compiles
against 9.2.0, so its translator's `switch (someKind)` statements baked in
9.2.0's numbers. Platform pins 12.4.1 exactly; at runtime the CLR loads
12.4.1's `SyntaxKind`, whose members carry different integers. Every case
label silently failed to match.

This is a fundamentally different risk than the already-known divergences in
`ScalarTypes.All` membership (`CON-0003`) and the `single` alias (`CON-0005`):
those are differences in *what a reference-typed API returns*, resolved by
member dispatch against whichever assembly is actually loaded — safe by
construction. An enum `switch` is not: it is a compile-time-baked constant
comparison, and the estate's existing type contract (`KqlTypes.cs`) has never
switched on a Kusto.Language enum for exactly this reason. The translator
broke that discipline throughout; see the fix in `DEC-0032`'s governed commits
(compare `SyntaxKind.ToString()` — the name — never the enum value).

## Why the existing 9.2.0/12.4.1 conformance strategy cannot catch this class of bug

`DeltaZulu.Kql.Tests.V1241` recompiles the library's *sources* against 12.4.1
rather than referencing the built 9.2.0 assembly. That is the right strategy
for API-surface compatibility (`CON-0006`'s stated purpose), but it makes this
class of bug **structurally invisible**: recompiling the source against 12.4.1
means the `switch` statements' baked-in constants also become 12.4.1's
numbers, so the mismatch never appears within a single, self-consistently
compiled test run. The mismatch exists only across a real compiled-for-9.2.0 /
loaded-at-12.4.1 boundary — precisely how a real consumer (Platform) uses the
packaged binary, and precisely what this session's real integration test
exposed that no in-repo test could.

## Assessment

A real consumer pinned to a different exact Kusto.Language version than
`DeltaZulu.Kql`'s compile floor is not a downstream integration detail — for
any code that compares a Kusto.Language enum, it is effectively part of this
package's own test surface. See `CON-0021`.
