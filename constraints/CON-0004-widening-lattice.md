---
id: CON-0004
status: Accepted
subject: Widening lattice
---

# CON-0004 — Widening lattice per `IsWiderThan`

The full pairwise widening relation over `ScalarTypes.All`, **identical on 9.2.0
and 12.4.1**:

```
decimal > int
decimal > long
decimal > real
long    > int
real    > int
real    > long
string  > dynamic
```

Every other ordered pair is false. `null` (12.4.1 only) participates in no
relation in either direction.

## Consequences

- `IsWiderThan` is the authority on widening. The estate does not restate it,
  re-derive it, or maintain a parallel table — it asks.
- The relation being identical across the span is what makes a single conversion
  policy possible for both the Agent and Platform processes.
- Note what the lattice does **not** say: that a widening conversion is lossless
  in the CLR carriers. `long > int` is exact; `real > long` is not, above 2^53.
  Lossless-ness is a property of the carriers, and is CON-0009's subject.

## Verified

`reports/2026-08-15-kusto-language-preflight.md` — full pairwise enumeration,
diff-clean between versions.
