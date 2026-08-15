---
id: CON-0014
status: Accepted
subject: Timespan unit
---

# CON-0014 — Wire tag 5 is ticks; the registry defaults to microseconds

The Forward wire format encodes `TimeSpan` under tag 5 as **ticks** (100 ns).
Platform's `LogicalSchemaRegistry` defaults the same logical duration to
**microseconds** (1000 ns).

These differ by a factor of ten. Every duration crossing that boundary is wrong
by an order of magnitude, silently, in whichever direction the boundary is
crossed.

## The canonical unit is ticks

The registry's microseconds default is the defect. This constraint records the
divergence as a fact; correcting the registry is Decision work, and it is a
contract-level correction rather than a Platform-local one.

## Consequences

- `DeltaZulu.Kql`'s carrier for `timespan` is `System.TimeSpan`, whose own
  resolution is ticks — so the wire and the carrier already agree and the
  registry is the outlier.
- A factor-of-ten error in a duration does not look like corruption. It looks
  like a plausible number, which is why this must be fixed at the contract
  rather than patched where it is noticed.
