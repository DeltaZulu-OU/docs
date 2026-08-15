---
id: CON-0013
status: Accepted
subject: LocalStream payload opacity
---

# CON-0013 — LocalStream carries payload bytes verbatim

`DeltaZulu.LocalStream` stores and returns `byte[] PayloadJson` exactly as
given. It does not parse, validate, or interpret the payload.

## Consequences

- The opacity is load-bearing, not incidental. It is what lets LocalStream and
  DurableBuffer stay out of the type contract entirely: they cannot disagree
  with `DeltaZulu.Kql` about a type they never look at.
- Neither `DeltaZulu.Kql` nor a `Kusto.Language` pin may be added to
  LocalStream or DurableBuffer. Doing so would drag both into CON-0006's version
  span for no benefit, and would give two more components an opinion about a
  contract they exist to be neutral about.
