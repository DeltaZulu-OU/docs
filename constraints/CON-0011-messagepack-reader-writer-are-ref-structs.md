---
id: CON-0011
status: Accepted
subject: MessagePack API shape
---

# CON-0011 — `MessagePackWriter` and `MessagePackReader` are `ref struct`

Both types are `ref struct`. They cannot be boxed, captured in a lambda, stored
in a field, used in an `async` method across an await, or appear as a generic
type argument.

## Consequences

- Serialisation code cannot be structured around async or around closures over
  the reader/writer. The shape of the API constrains the shape of the code that
  uses it, and formatter implementations must pass `ref` through the call chain.
- Recursion depth must be tracked explicitly through `ref` parameters —
  relevant because untrusted input needs depth limiting and the natural
  idioms for carrying that state are unavailable.
