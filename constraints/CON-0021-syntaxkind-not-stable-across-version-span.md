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
(Platform's exact pin) can silently mismatch on cases whose values differ,
because the runtime-loaded enum's members carry different integers than the
ones baked into the compiled `switch`.

This is categorically different from `ScalarTypes.All` membership (`CON-0003`)
or the `single` alias (`CON-0005`): those are differences in what a
*reference-typed* API returns, resolved by member dispatch against whichever
assembly is actually loaded at runtime — safe regardless of which version
compiled the caller. An enum comparison is not: it is a compile-time-baked
constant, indifferent to which assembly is loaded later.

## Consequences

A source-recompiled test against each version cannot demonstrate binary
compatibility when enum constants differ. C14 must include a consumer using
the already-built library against the other supported runtime dependency
version where the supported assembly loading contract permits it. C06
must verify affected query semantics. The evidence establishes instability
for the listed `SyntaxKind` members, not every member or every enumeration.
A name-based comparison is one possible mitigation, not a binding policy;
other enum types and the correctness of any mitigation require evidence.

## Verified

The historical [September 3 report](../reports/2026-09-03-syntaxkind-version-instability.md)
records reflection and a packed-library consumer experiment on the former
compiler-extraction branches. Its results have not been independently
rerun during this reconciliation. The experiment does not authorize the
archived compiler relocation; current DEC-0032 remains binding. The
[original Constraint wording](../archive/legacy-proposals/2026-09-03-original-CON-0021.md) is preserved verbatim as historical
evidence.
