---
id: CON-0002
status: Accepted
subject: Kusto.Language scope
---

# CON-0002 — Kusto.Language contains no CLR type mapping

`Microsoft.Azure.Kusto.Language` models the KQL type system — symbols, widening,
aliases, parsing, semantic analysis. It does not state which CLR type carries a
given KQL scalar, because it is not a data-plane library and never materialises
a value.

## Consequences

- The CLR carrier map is the estate's to own and to define. It cannot be looked
  up from the package, only decided and then held.
- Because the map is ours, it is also ours to keep total: every member of the
  surfaced type set must have a carrier, asserted at type-initialisation rather
  than discovered at runtime.

## Verified

`reports/2026-08-15-kusto-language-preflight.md` — the reflected public surface
of `ScalarSymbol` and `ScalarTypes` on both versions exposes name, aliases and
widening, and nothing resembling a `System.Type`.
