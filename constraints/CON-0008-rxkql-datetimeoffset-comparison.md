---
id: CON-0008
status: Accepted
subject: Rx.Kql temporal comparison
---

# CON-0008 — Rx.Kql compares `DateTimeOffset` via local wall clock

Rx.Kql compares a `DateTimeOffset` through its `.DateTime` property, which
yields the **local wall-clock component** with the offset discarded — not
`.UtcDateTime`.

## Consequences

- Two moments that are equal in absolute time compare unequal if they were
  recorded at different offsets. Detection logic over such values is wrong in a
  way that varies with the collector's timezone and with daylight-saving
  transitions.
- This is an independent reason — beyond CON-0001 — that `DateTimeOffset` must
  never be the carrier. Even where KQL's own type system is not consulted, the
  engine that evaluates the comparison gets it wrong.
- The adapter converts to `DateTime` (Kind=Utc) before any value reaches Rx.Kql.
