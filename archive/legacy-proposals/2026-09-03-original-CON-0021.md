---
id: CON-0021
status: Accepted
subject: Kusto.Language SyntaxKind values are not stable across the version span
---

# CON-0021 — `Kusto.Language.Syntax.SyntaxKind`'s underlying values differ between 9.2.0 and 12.4.1

**The enum's integer values are not stable across the version span this
estate spans (CON-0006).** Verified directly by reflection against both
package versions:

| `SyntaxKind` member | 9.2.0 | 12.4.1 |
|---|---:|---:|
| `StringLiteralExpression` | 439 | 348 |
| `LongLiteralExpression` | 433 | 342 |
| `EqualExpression` | 487 | 406 |
| `GreaterThanExpression` | 485 | 404 |
| `AndExpression` | 489 | 408 |

A C# `switch` (or `==`) on an enum value compiles to an integer comparison
against a constant baked in at compile time, using the *compiling* assembly's
numbering. Code that compiles against Kusto.Language 9.2.0 (the floor
`CON-0006` sets for `DeltaZulu.Kql`) but runs in a process that loads 12.4.1
(Platform's exact pin) will silently mismatch on every `SyntaxKind` case,
because the runtime-loaded enum's members carry different integers than the
ones baked into the compiled `switch`.

This is categorically different from `ScalarTypes.All` membership (`CON-0003`)
or the `single` alias (`CON-0005`): those are differences in what a
*reference-typed* API returns, resolved by member dispatch against whichever
assembly is actually loaded at runtime — safe regardless of which version
compiled the caller. An enum comparison is not: it is a compile-time-baked
constant, indifferent to which assembly is loaded later.

## Consequences

- Any code comparing a `Kusto.Language.Syntax.SyntaxKind` value must compare
  by **name** (`kind.ToString() == "EqualExpression"`, or a `switch` on
  `kind.ToString()`), never by enum member. `ToString()` resolves the name
  from whichever Kusto.Language assembly is actually loaded, so it is correct
  regardless of which version compiled the comparing code.
- This applies to every Kusto.Language enum, not only `SyntaxKind` — any enum
  from that package is compile-time-baked the same way. Nothing else in the
  estate's Kusto.Language-facing code currently switches on a different one.
- The existing 9.2.0/12.4.1 conformance strategy (source-recompiled against
  12.4.1, per `DeltaZulu.Kql.Tests.V1241`) cannot catch this class of bug: it
  always compiles and runs against a *single, self-consistent* version, so a
  compile-time-baked constant always matches at runtime within that test
  project. The mismatch appears only across a real compiled-for-9.2.0 /
  loaded-at-12.4.1 boundary. A real consumer pinned to a different exact
  Kusto.Language version than `DeltaZulu.Kql`'s compile floor is therefore
  part of this package's effective test surface for any enum-comparing code,
  not merely a downstream integration detail.

## Verified

`reports/2026-09-03-syntaxkind-version-instability.md`. Found by real
cross-repo consumption (packing `DeltaZulu.Kql` locally and running
`DeltaZulu.Platform`'s test suite against it) while extracting the KQL
relational translator into `DeltaZulu.Kql` — see `DEC-0032`.
