---
id: CON-0015
status: Accepted
subject: Collection-loss enumeration
---

# CON-0015 — `KqlNullReason` is closed and specified

`KqlNullReason` answers *why is this field absent* — a **collection**-time fact.
Its members are specified and the enumeration is closed:

```
NotAvailableAtTier, ProcessExited, AccessDenied, FileDeleted,
PolicyDisabled, HashFailed, EnrichmentSourceUnavailable, RecordSourceMissing
```

It is owned by the type-contract catalogue. **Do not modify it.**

## The other enumeration

`KqlLossReason` answers a different question — *why could this value not be
represented* — a **conversion**-time fact. Its members are
`None, OutOfRange, Narrowed, Unrepresentable, Malformed`, and it is owned by
`DeltaZulu.Kql`.

## Consequences

- The two enumerations must never be merged. Merging them would make "the
  process exited" and "the decimal overflowed" the same kind of fact, and no
  consumer could then distinguish a collection gap from a representation
  failure — which is precisely the distinction provenance exists to record.
- Neither enumeration may be switched over with a `_ =>` fallthrough arm. Both
  are closed; a fallthrough silently absorbs a member added later.
