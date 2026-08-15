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

## Seed set — not yet imported

The D1–D21 register in the consolidated architecture document is intended to seed
this directory, renumbered to global `DEC-NNNN`. That import is pending: the
consolidated document has not yet been placed in this repository. Until it is,
this directory holds only the template below.

Open questions the import must resolve, recorded so they are not lost:

- **D13** — Golden as OCSF-derived versus Platform ADR 0007's DeltaZulu-owned
  names. Note that OCSF and ASIM appear in exactly one file fleet-wide and in no
  source file, which is evidence about how settled the OCSF reading actually is.
- **D11** — pending the Golden placement decision memo.
- **D21** — threshold semantics.
- Platform ADR 0007's *"agents do not map into Silver … or enrichments"* clause
  contradicts settled D5 and needs striking.
- Agent ADR 0016's bespoke-native-sink premise is contradicted by shipped
  `ProtonHttpExecutor` code and needs retiring.
- LocalStream ADR-0006's at-least-once delivery needs reconciling against
  Forward's delivery-correctness gate.
