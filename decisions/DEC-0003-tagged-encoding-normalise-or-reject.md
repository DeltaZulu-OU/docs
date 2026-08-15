---
id: DEC-0003
status: Accepted
repos: [DeltaZulu.Forward]
governs:
  types: [ForwardValueNormalizer]
  paths: [src/DeltaZulu.Forward/ForwardValueNormalizer.cs]
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
