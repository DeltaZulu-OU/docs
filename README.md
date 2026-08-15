# DeltaZulu estate documentation

The single home for Constraints, Decisions, architecture, roadmaps, and archived
per-repo ADRs across the DeltaZulu estate.

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
| `architecture/` | Per-repo and estate architecture | Always current. Rewritten in place. |
| `roadmaps/` | Forward plans | Every roadmap carries a dated review trigger. |
| `archive/` | Historical per-repo ADRs, content unchanged | Frozen. Read-only history. |
| `reports/` | Verification output and decision memos that Decisions cite as evidence | Append-only in practice; dated. |

`reports/` is not in the original layout specification. It was added because
Constraints must cite verified evidence and that evidence needs somewhere to
live that is neither a fact nor a decision.

## Where to start

`architecture/PIPELINE.md` is the consolidated architecture — read it with
`architecture/PIPELINE-ERRATA.md`, which records where Wave 0 verification found
its claims refuted or understated. `decisions/` holds `DEC-0001`–`DEC-0021`
seeded from that document's D1–D21 register.

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
stale or the deletion was unauthorised; both need a human.

## The deletion rule

Deleting a project, a public type, or a line of work requires either a status
note on the governing Decision or a new Decision with status `Rejected`.
Deleting the code is the easy half; recording why it stopped being the plan is
the half that keeps the next reader from rebuilding it.
