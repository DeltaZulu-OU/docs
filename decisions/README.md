# Decisions

Choices the estate has made. Globally numbered `DEC-NNNN` across all repositories
— the numbering is global precisely because the per-repo scheme it replaces
produced collisions that citations could not disambiguate (Agent ADR 0014 and
Platform ADR 0014 decide opposite things; the Agent carries two different ADR
0003 documents).

## Status values

| Status | Meaning |
|---|---|
| `Proposed` | Written down, not yet binding. |
| `Accepted` | Binding. Subject to `governs-check`. |
| `Superseded` | Replaced by a later Decision, which it names. Kept, never deleted. |
| `Rejected` | Considered and declined. Kept — a recorded rejection is what stops the idea being silently rebuilt. |

## Required front-matter

```yaml
---
id: DEC-NNNN
status: Accepted
repos: [DeltaZulu.Kql, DeltaZulu.Agent]
governs:
  types: [DeltaZulu.Kql.KqlTypes]
  paths: [src/DeltaZulu.Kql/KqlTypes.cs]
cites: [CON-0002, CON-0006]
---
```

`governs` is the enforcement hook: `.github/workflows/governs-check.yml` fails if
a symbol or path named there stops existing while the Decision is `Accepted`.
Only claim what the Decision genuinely governs — an over-broad `governs` block
turns the check into noise, and a check people ignore is worse than no check.

## Required sections

**Alternatives rejected.** What else was considered, why it was not chosen, and
which Constraint it failed. A Decision with no rejected alternatives did not
decide anything; it recorded a default.

**Revisit trigger.** The named, checkable condition under which this Decision
should be reopened. Not a date — a condition: *"if Rx.Kql is replaced or drops
its Kusto.Language 9.2.0 floor"*, *"if the collector acquires a repository"*.

The trigger is mandatory because the estate has four documented cases of a
decision made on rationale that later stopped holding, where nothing recorded
what would invalidate it and so nobody looked. Those cases are listed in
`archive/RECOVERY.md`, and they are the reason this section is not optional.

## Seed set

`DEC-0001` through `DEC-0021` are seeded from the D1–D21 register in
`architecture/PIPELINE.md`, renumbered to global `DEC-NNNN`. Each carries a
`supersedes:` field naming its original `D`-number so citations to the register
still resolve.

Status is carried across honestly rather than promoted: `DEC-0011` (Silver→Golden
dual-compiled), `DEC-0013` (Golden semantic model) and `DEC-0021` (threshold
semantics) are `Proposed`, not `Accepted`, because the register recorded them as
Proposed or Open and nothing since has settled them.

Three of the seeded Decisions carry corrections the register did not:

- **`DEC-0012`** records that `ILogicalSchemaRegistry` has no implementation
  anywhere under `src/` — not merely no production consumers. Found by
  `governs-check` rejecting an earlier draft of the Decision itself.
- **`DEC-0017`** retires Agent ADR 0016's bespoke-native-sink premise against
  shipped `ProtonHttpExecutor` code, and names ADR 0012's Enterprise-gating claim
  as the factual error it propagated from.
- **`DEC-0003`** states explicitly that the per-field conversion policy *refines*
  reject-not-coerce rather than reversing it, because a reader encountering the
  narrowing without that sentence will read it as an overturn.

## Still open in the seed set

- **`DEC-0013`** — Golden as OCSF-derived semantics versus Platform ADR 0007's
  DeltaZulu-owned names. Must reach `Accepted` or be split before `DEC-0011`
  leaves `Proposed`.
- **`DEC-0011`** — stays `Proposed` until the CI equivalence test exists. See
  `reports/2026-08-15-golden-placement.md`.
- **`DEC-0021`** — window semantics unsettled.

## Amendments these Decisions require in the archived ADRs

Recorded here because the archive is frozen and cannot carry them:

- Platform ADR 0007's *"agents do not map into Silver … or enrichments"* clause
  contradicts `DEC-0005` and is struck by it.
- Agent ADR 0016's bespoke-native-sink premise is retired by `DEC-0017`.
- LocalStream ADR-0006's at-least-once delivery still needs reconciling against
  Forward's delivery-correctness gate. Not yet done — no Decision covers it.
- Platform ADR 0002's *"Translation uses a controlled relational model before
  emitting backend SQL"* (as a Platform-owned mechanism) is retired by
  `DEC-0032`, which moves the relational IR and translator to `DeltaZulu.Kql`.
- Platform ADR 0016's *"Backend-neutral relational emission lives at the
  application/domain boundary"* is retired by `DEC-0032` for the same reason.
