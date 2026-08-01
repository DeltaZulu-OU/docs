---
id: DEC-0023
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: [CON-0017, CON-0018, CON-0019]
---

# DEC-0023 — Completeness is measured by external canaries, and unmeasurable sources say so

## Context

CON-0017: nothing inside the pipeline distinguishes loss from a genuine fall in
activity. CON-0018: a component cannot report its own absence. CON-0019: a UDP
source has no obtainable completeness figure at all.

The estate currently measures internal conservation and has no completeness
evidence of any kind.

## Decision

Completeness is established by a **sequence-numbered, NTP-synchronised canary
emitter outside the pipeline** (MX), reconciled against what the lake actually
holds, and observed at three stages so a shortfall is attributable to
acquisition, transport or lake rather than merely detected.

Two properties are not optional. **Duplication is counted separately from loss**
and never netted against it — they are independent defects and netting hides
both. And **a source on a transport with no delivery guarantee is rendered as
unmeasurable**, never as an assumed rate.

Absence detection is computed at the receiver from an expected-source inventory,
and a minimal liveness heartbeat travels the control-plane channel rather than
the data path.

## Status note — accepted 2026-08-17

Accepted so that DQM wave 2a — canary emitter, reconciler, receiver-side source
inventory — has a settled position to be built against. The decision has no
dependencies on the type catalogue, the transport, Golden or a published package,
which is why it could be accepted while other work was blocked on a package feed.

Acceptance settles the measurement principle and the two non-optional properties:
duplication is counted separately from loss and never netted against it, and a
source on a transport with no delivery guarantee is rendered as unmeasurable
rather than assigned an assumed rate.

Acceptance does **not** settle the two questions recorded under Consequences as
open, and neither is treated as resolved by silence:

- Canary injection into a Windows Security channel or an ETW session still has no
  identified mechanism. The fallback of reading provider drop counters measures
  something weaker, and adopting it would narrow what "completeness" claims for
  those sources.
- **Whether canaries are filtered from Bronze or retained and marked is still
  open, and it blocks the emitter rather than the principle.** It needs its own
  Decision before the emitter writes anything, because `DEC-0010` makes Bronze
  write-once: filtering is a content-based routing judgement taken at write time
  and cannot be undone afterwards, while retaining and marking can be reversed at
  query time. The asymmetry is an argument about reversibility, not a resolution
  — recorded here so the emitter is not built on an assumption nobody made
  deliberately.

## Consequences

- This is the only work that makes "completeness" an honest word in a customer
  conversation.
- It has **no dependencies** on the type catalogue, the transport, Golden or any
  published package, so it can start immediately and survives every subsequent
  change.
- The proportion of sources that are unmeasurable becomes a reported figure,
  making the limit of the claim visible rather than a footnote.
- Open: canary injection into a Windows Security channel or an ETW session has no
  obvious mechanism, and the fallback of reading provider drop counters measures
  something weaker. Whether canaries are filtered from Bronze or retained and
  marked is a genuine decision with no obviously correct answer.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Infer completeness from event-rate baselines | A fall in rate is equally consistent with loss, quiet sources and a filter change | CON-0017 |
| Rely on internal conservation accounting | Proves the pipeline did not lose what it received; says nothing about what it received | CON-0017 |
| Agent-reported liveness alone | Silent exactly when the agent dies | CON-0018 |
| Report an assumed rate for UDP sources | Fabricates a number | CON-0019 |

## Revisit trigger

Reopen if a source-side producer exposes trustworthy sequence numbers or
counters natively, which would make canaries redundant for that class — the
canary is a substitute for ground truth, not an end in itself.
