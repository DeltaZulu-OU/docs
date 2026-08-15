---
id: CON-0009
status: Accepted
subject: decimal range
---

# CON-0009 — `System.Decimal` is narrower than KQL `decimal`

KQL `decimal` is a 128-bit type with 38 significant digits. `System.Decimal` has
a maximum magnitude of approximately 7.92 x 10^28 and 28–29 significant digits.

The CLR carrier is therefore **narrower than the type it carries**. This is a
known, accepted narrowing (KI-002), not an oversight.

## Consequences

- Values legal in KQL `decimal` are not always representable in the carrier.
  Conversion must detect and report this per field rather than overflow or
  saturate.
- Rounding to fit is forbidden. A value that does not fit is `OutOfRange`, and
  the field becomes a typed null carrying that reason. Producing a nearby number
  that was never in the data is the failure mode this constraint exists to
  prevent.
- The same reasoning covers `ulong` above `long.MaxValue`: the alias table maps
  `ulong` to `long` (CON-0005), so a `ulong` beyond that ceiling has no
  representable type and is `OutOfRange`.
