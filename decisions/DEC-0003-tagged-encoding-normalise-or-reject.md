---
id: DEC-0003
status: Accepted
repos: [DeltaZulu.Forward, DeltaZulu.Kql]
governs:
  types:
    DeltaZulu.Forward: [ForwardValueNormalizer, ForwardObjectFormatter]
    DeltaZulu.Kql: [KqlTypes, KqlValue, KqlLossReason]
  paths:
    DeltaZulu.Forward: [src/DeltaZulu.Forward/ForwardValueNormalizer.cs]
    DeltaZulu.Kql: [src/DeltaZulu.Kql/KqlTypes.cs]
cites: [CON-0009, CON-0014, CON-0015]
supersedes: D3
---

# DEC-0003 — Ten-type tagged encoding; normalise-or-reject

## Context

Plain MessagePack inference cannot distinguish a `DateTimeOffset` from a `decimal` from a `string` at an `object` boundary — all three decode as ambiguous strings.

## Decision

Values are encoded as a two-element array `[tag, payload]` over ten tags. Unmappable values are rejected rather than coerced, passed through, or dropped.

Silent coercion is the mechanism by which type-loss boundaries reappear after being closed. Failing visibly converts a data-quality defect into an engineering defect, which is the kind that gets fixed.

## Consequences

`DeltaZulu.Kql` implements the conversion half of this Decision as
`KqlTypes.TryNormalize`, which never throws and never rounds, and reports loss
through the `KqlLossReason` enumeration. `DeltaZulu.Forward` implements the
encoding half. Both repositories are governed here because a change to either
without the other reopens the boundary this Decision closes.

**Refined, not reversed, by the per-field policy.** Rejecting the whole batch with a `NotSupportedException` and rejecting a single field with a typed null plus a `KqlLossReason` both refuse to coerce; they differ only in blast radius. The per-field form is preferred because it preserves the rest of the record. Anyone reading the narrowing as an overturn of reject-not-coerce has read it wrongly.

CON-0014 applies: tag 5 is ticks, and the registry's microseconds default is the defect, not the wire.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Untagged inference | Cannot round-trip `DateTimeOffset` or `decimal` | CON-0010 |
| Coerce-to-string on failure | Reintroduces the type-loss boundary the catalogue exists to close | — |
| Silent drop | Destroys the absent-versus-negative-evidence distinction | — |

## Revisit trigger

If the carrier for `datetime` changes, tag 4's encoding changes with it — this Decision must be amended alongside, not after.
