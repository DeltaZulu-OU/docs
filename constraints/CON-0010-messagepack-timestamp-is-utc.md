---
id: CON-0010
status: Accepted
subject: MessagePack timestamp
---

# CON-0010 — MessagePack timestamp extension is UTC, no offset

MessagePack's timestamp extension type (-1) encodes seconds and nanoseconds
since the Unix epoch. It has no offset field.

## Consequences

- The wire format agrees with KQL (CON-0001): a moment is UTC or it is not
  encodable. There is no representation gap to bridge and no offset to preserve.
- A `DateTimeOffset` on the wire would have to be encoded as something other
  than the native timestamp extension — a further reason the carrier decision is
  forced rather than chosen.
- Nanosecond precision on the wire exceeds the CLR carrier's 100 ns tick.
  Sub-tick precision is not representable in `System.DateTime`; see CON-0014 for
  the estate's canonical unit.
