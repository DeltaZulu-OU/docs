---
id: CON-0001
status: Accepted
subject: KQL datetime
---

# CON-0001 — KQL `datetime` is UTC-only

KQL's `datetime` scalar carries no timezone offset. There is no offset-bearing
scalar type in the language: a moment is either UTC or it is not representable.

## Consequences

- The CLR carrier is `System.DateTime` with `Kind = Utc`. Never
  `System.DateTimeOffset` — that type carries an offset KQL cannot express, so
  it silently loses information the moment it crosses the boundary.
- `DateTime` with `Kind = Unspecified` is not convertible. It is not UTC and
  claiming otherwise invents a fact. It must be rejected, not assumed.
- `DateTime` with `Kind = Local` is convertible via `ToUniversalTime()`, which
  is lossless and total.

## Verified

Language reference, and the absence of any offset-bearing member in
`ScalarTypes.All` on both 9.2.0 and 12.4.1 (`reports/2026-08-15-kusto-language-preflight.md`).
