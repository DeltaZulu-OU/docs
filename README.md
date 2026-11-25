# DeltaZulu estate documentation

The single home for Constraints, Decisions, target architecture, roadmaps,
source-verification reports and archived per-repo ADRs across DeltaZulu.
**Accepted Decisions govern intent; dated code audits describe observed source;
passing integration tests are required to establish deployed correctness.**

Before this repository existed, every repo kept its own `docs/adr/`. Two
consequences made that untenable: decision numbers collided across repos while
citing each other (Agent ADR 0014 and Platform ADR 0014 are opposite decisions
sharing a citation; Agent itself carries two different ADR 0003 documents), and
decisions made on rationale that later stopped holding were never revisited
because nothing recorded what would invalidate them.

## Layout

| Directory | Contents | Mutability |
|---|---|---|
| `constraints/` | `CON-NNNN-*.md` — facts about the world | **Immutable.** A constraint that turns out to be false is superseded by a new one, never edited. |
| `decisions/` | `DEC-NNNN-*.md` — choices the estate has made | Rewritable. Global numbering across all repos. |
| `architecture/` | Current target architecture, candidate contracts, historical imports and errata | Current narratives revised in place; dated imports preserved. |
| `roadmaps/` | One active execution table and historical imported plans | Active table carries a review trigger; imported statuses are historical. |
| `archive/` | Historical per-repo ADRs, content unchanged | Frozen. Read-only history. |
| `reports/` | Verification output and decision memos that Decisions cite as evidence | Append-only in practice; dated. |

`reports/` is not in the original layout specification. It was added because
Constraints must cite verified evidence and that evidence needs somewhere to
live that is neither a fact nor a decision.

## Where to start

`architecture/NRT-PIPELINE.md` is the **current target** for near-real-time
processing, governed by `DEC-0033`: LocalStream/Query, not Proton, with
DuckLake as durable evidence and analyst read surface. `PIPELINE.md` is a
verbatim historical import and must be read with `PIPELINE-ERRATA.md`.
`decisions/` holds `DEC-0001`–`DEC-0033`, including Rejected,
Superseded and Proposed records; only Accepted Decisions are binding.
`DEC-0013` adopts ASIM-first Gold schemas; the four-family source inventory
and candidate mappings are in `architecture/ASIM-GOLD-MAPPING-BASELINE.md`.
All active work is tracked in the [consolidated roadmap](roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md). Imported plans retain detail but do not constitute independent commitments.

`architecture/GOVERNING-DECISIONS.md` indexes which Decisions govern which
repository. Regenerate it with `python3 .github/scripts/governing_index.py --write`;
CI checks for drift with `--check`.

## Constraints versus Decisions

A **Constraint** is a fact: something true about a dependency, a format, a
protocol, or a platform, which the estate does not control and cannot vote on.
`KQL datetime is UTC-only` is a constraint. Constraints are immutable because
the past tense of a fact does not stop being true — if the world changes, the
new fact gets a new number and the old one is marked superseded.

A **Decision** is a choice: something the estate could have done differently.
Decisions cite the Constraints that bound them.

## Decision front-matter

Every Decision carries:

```yaml
---
id: DEC-0001
status: Accepted        # Proposed | Accepted | Superseded | Rejected
repos: [DeltaZulu.Kql, DeltaZulu.Parse]
governs:
  types: [DeltaZulu.Kql.KqlTypes, DeltaZulu.Kql.KqlValue]
  paths: [src/DeltaZulu.Kql/KqlTypes.cs]
cites: [CON-0002, CON-0006]
---
```

and two mandatory sections:

- **Alternatives rejected** — what else was considered, why it was not chosen,
  and which Constraint it failed. A decision with no rejected alternatives was
  not a decision.
- **Revisit trigger** — the named, checkable condition that invalidates this
  decision. This section exists because four decisions in the estate's history
  were made on rationale that outlived its conditions and nobody noticed. See
  `archive/RECOVERY.md`.

## Enforcement

`.github/workflows/governs-check.yml` checks out the repos named in each
`Accepted` Decision's `repos:` list and fails if any symbol or path under
`governs:` no longer exists. A Decision that governs deleted code is either
stale or the deletion was unauthorised; both need a human. The checker also
rejects malformed Decision metadata and inconsistent supersession relationships, requires successful checkout, verifies the generated index, checks maintained inline local links and compares the registered Gold inventory. Existence
checks search production `src/` declarations; they **do not prove behavior,
compatibility, public API accessibility, or end-to-end conformance**.

## The deletion rule

Deleting a project, a public type, or a line of work requires either a status
note on the governing Decision or a new Decision with status `Rejected`.
Deleting the code is the easy half; recording why it stopped being the plan is
the half that keeps the next reader from rebuilding it.
