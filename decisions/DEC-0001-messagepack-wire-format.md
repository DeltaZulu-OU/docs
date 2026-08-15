---
id: DEC-0001
status: Accepted
repos: [DeltaZulu.Forward]
governs:
  types: [ForwardBatchEnvelope]
  paths: [src/DeltaZulu.Forward/ForwardBatchEnvelope.cs]
cites: [CON-0010, CON-0011]
supersedes: D1
---

# DEC-0001 — Wire format is MessagePack `ForwardLogBatch` in `TypedBatch` frames

## Context

Extracted field sets vary per record, because which fields a rulebase produces depends on which rule matched. A wire format demanding a fixed writer schema must therefore describe the variable case.

## Decision

The wire carries a MessagePack-encoded `ForwardLogBatch` inside `TypedBatch` frames.

## Consequences

MessagePack has no writer-reader schema resolution, so per-record identity (DEC-0002) carries that weight instead. Fleet schema lag becomes a compatibility-window question rather than a resolution-machinery question.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Avro | Variable field sets force `map<string,union>`, which discards per-field typing at exactly the point the catalogue exists to preserve it | — |
| Plain untagged MessagePack | Lossy at an `object` boundary; see DEC-0003 | CON-0010 |

## Revisit trigger

If the extracted field set becomes fixed per source family, Avro's schema resolution would buy something it currently does not, and this should be re-argued.
