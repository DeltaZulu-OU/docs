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
  types:
    DeltaZulu.Kql: [DeltaZulu.Kql.KqlTypes]
  paths:
    DeltaZulu.Kql: [src/DeltaZulu.Kql/KqlTypes.cs]
cites: [CON-0002, CON-0006]
---
```

`governs` is the enforcement hook: `.github/workflows/governs-check.yml` fails if
a symbol or path named there stops existing while the Decision is `Accepted`.
For multi-repository Decisions, use repository-keyed lists when declarations differ; a flat list applies to every named repository. Only claim what the Decision genuinely governs — an over-broad `governs` block
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

The seed import preserved the original statuses. A later architecture change
(`DEC-0033`, accepted 2026-11-23) **Rejected** `DEC-0011`'s Proton/DuckLake
dual-compilation proposal. `DEC-0013` accepted ASIM-first Gold schemas at the time; DEC-0038 now governs canonical schema and naming, with DeltaZulu-owned names and ASIM reference alignment. `DEC-0021`
(window threshold semantics) remains `Proposed`; status must be read from each
Decision's current front matter, not inferred from the historical seed.

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

## Seed set status after subsequent decisions

- **`DEC-0013`** — Accepted, with schema and naming provisions superseded by DEC-0038; ASIM remains reference evidence, not canonical naming authority.
- **`DEC-0021`** — window threshold semantics, including late events and
  corrections, remain unsettled under LocalStream.Query.
- **`DEC-0011`** — Rejected by `DEC-0033`; its old equivalence gate is
  no longer a pending action. Earlier reports discussing the gate remain
  historical evidence.

`DEC-0033` supersedes the Proton-specific accepted decisions
`DEC-0010`, `DEC-0017`, `DEC-0020`, `DEC-0027`,
`DEC-0028` and `DEC-0031`. The accepted replacements for retained
Bronze, Gold and DuckLake responsibilities are recorded in `DEC-0033`.

## Historical conflicts resolved by current Decisions

These conflicts are documented here rather than editing the frozen archive:

- Platform ADR 0007's *"agents do not map into Silver … or enrichments"* clause
  contradicts `DEC-0005` and is struck by it.
- Agent ADR 0016's bespoke-native-sink premise was retired by `DEC-0017`,
  which is itself now Superseded by the no-Proton `DEC-0033`.
- LocalStream's at-least-once delivery and Forward's acknowledgment/deduplication
  requirements still need an end-to-end correctness proof. `DEC-0033` governs
  the target split, but it does not establish a tested transactional boundary.

- The historical [KQL compiler relocation proposal](../archive/legacy-proposals/2026-09-03-kql-relational-ir-and-compiler.md)
  used the same DEC-0032 identifier before the current Decision was assigned.
  Its proposed retirement of Platform ADRs 0002 and 0016 is not binding.
  References to DEC-0032 in the associated September 3 experiment denote
  that historical proposal; the current Accepted DEC-0032 governs ownership.
  The independent SyntaxKind findings remain relevant under CON-0021.

## Detection provenance

[DEC-0036](DEC-0036-detection-provenance.md) is Accepted: deterministic causal result provenance and immutable executed rule context are separate from alert identity under DEC-0030. The C06/C07 contract gate precedes production detection and persistence implementation; it does not settle pending window or correction policy.

## Event identity

[DEC-0037](DEC-0037-event-identity-boundaries.md) is Accepted; it separates identity domains, establishes scoped deduplication and leaves the Forward physical contract open.

## Medallion schema conventions

[DEC-0038](DEC-0038-medallion-schema-conventions.md) is Accepted; it supersedes the schema and naming provisions of DEC-0012, DEC-0013 and DEC-0034 while retaining their remaining requirements and MVP scope.
