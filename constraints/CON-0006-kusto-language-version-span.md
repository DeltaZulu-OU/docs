---
id: CON-0006
status: Accepted
subject: Kusto.Language version span
---

# CON-0006 — Rx.Kql pins 9.2.0; Platform runs 12.4.1; `DeltaZulu.Kql` must span both

`Microsoft.Rx.Kql` 3.5.3 resolves `Microsoft.Azure.Kusto.Language` **9.2.0**
transitively. `DeltaZulu.Platform` references **12.4.1**. Three majors apart, and
no single version satisfies both.

Assembly identity only has to agree **within a process**, and Platform never
hosts Rx.Kql. So the span is legal — but it is a span, not a version.

| Boundary | Pin | Why |
|---|---|---|
| `DeltaZulu.Kql` compile target | 9.2.0, **minimum not exact** | Must bind at runtime against both |
| Agent process (Parse, Forward, Rx.Kql) | `[9.2.0]` exact | Rx.Kql floors it |
| Platform process | `[12.4.1]` exact | Already there; do not downgrade |
| Parse, LogCluster, Forward as libraries | minimum 9.2.0, **no exact pin** | Hosted by both |

**Rx.Kql sets the Agent's floor; Platform sets the ceiling; `DeltaZulu.Kql` must
span them.** Replacing Rx.Kql collapses the span — that is the condition under
which this constraint stops binding.

## Consequences

- `DeltaZulu.Kql` may use only API present in 9.2.0 **and** unchanged through
  12.4.1. The verified-identical surface is `ScalarTypes.All`,
  `ScalarSymbol.IsWiderThan`, `ScalarSymbol.From`, `ScalarTypes.GetSymbol`.
- Two things inside that surface are *not* identical across the span, and the
  span holds only because both are absorbable: `All` membership (CON-0003) and
  the `single` alias (CON-0005).
- Anything added to `DeltaZulu.Kql`'s dependency on Kusto.Language must be
  re-verified on both versions before it ships. One-version verification is not
  verification.

## Verified

`reports/2026-08-15-kusto-language-preflight.md`, items 1, 4 and 5. Platform's
reference is at `Directory.Packages.props`; note it is currently a plain minimum
rather than the `[12.4.1]` exact pin this constraint's table calls for.
