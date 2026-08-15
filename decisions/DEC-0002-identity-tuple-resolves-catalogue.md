---
id: DEC-0002
status: Accepted
repos: [DeltaZulu.Forward]
governs:
  types: [ForwardLogRecord]
  paths: [src/DeltaZulu.Forward/ForwardLogEnvelope.cs]
cites: []
supersedes: D2
---

# DEC-0002 — Per-record identity tuple resolves the catalogue entry

## Context

With no wire-carried schema (DEC-0001), the collector needs another way to know what it is decoding.

## Decision

`(SourceType, SourceName, ProfileId, ProfileVersion)` on each record resolves the catalogue entry at the collector.

## Consequences

Removes the need for a wire-carried schema. Makes the catalogue a hard runtime dependency of the collector: an unresolvable tuple is a dead-letter, not a best guess.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Wire-carried schema per batch | Bytes on every batch for information that changes rarely | — |
| Schema fingerprint only | Requires a fetch round-trip on first sight; retained as the `SchemaRequest`/`SchemaResponse` path rather than the primary mechanism | — |

## Revisit trigger

If profiles start varying their field sets within a single `ProfileVersion`, the tuple stops being sufficient and the fingerprint path must become primary.
