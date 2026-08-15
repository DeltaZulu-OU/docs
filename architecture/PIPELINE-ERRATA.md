# `PIPELINE.md` — errata

`PIPELINE.md` is imported verbatim as it was handed to the estate on 15 August
2026. It is not edited, so that citations to it remain stable and so that what
was believed at import time stays legible.

This file records where Wave 0 verification found the document's claims to be
wrong, incomplete, or unverified. Each entry names the evidence.

## Refuted

### §6.6 — "Restore cannot succeed on a clean checkout"

**Refuted.** On .NET SDK 10.0.110, `dotnet restore --locked-mode` against
Platform's pre-fix tree with an empty package cache **exits 0 and generates the
13 lock files during the run**. CI was not failing.

The underlying defect is real and arguably worse than described: locked mode was
a silent no-op, so CI asserted nothing about dependency reproducibility while
appearing to verify it. Evidence and fix in
`reports/2026-08-15-platform-ci-restore.md`.

### §6.6 — "`DeltaZulu.Parse` commits its lock files correctly, so this is a Platform-specific defect rather than a fleet convention problem"

**Half refuted.** The lock-file half is correct: Parse commits 5 lock files and
its `.gitignore` re-includes them by negation.

The `NuGet.config` half is not. Parse's committed `NuGet.config` has **no
`<packageSources>` section at all** — the identical defect. So does the Agent's,
where it is not latent: `dotnet restore` from a clean Agent checkout fails
NU1100 for all five `DeltaZulu.*` packages. Parse's CI works only because
`publish.yml` builds a temporary config at run time and calls
`dotnet nuget add source`. The defect is a fleet convention problem for
`NuGet.config` and a Platform-specific one only for lock files.

### §2 and gap 16 — "Either the published packages diverge from source, or the pins are aspirational"

**Neither.** Both packages were published exactly once, from commits where no
`<Version>` was declared, so MSBuild's default `1.0.0` shipped — which is exactly
what the Agent pins. The pins match published reality.

The real defect runs the other way: LocalStream's source was changed on
2026-08-13 (commit `7899423`) to declare `0.1.0`, *below* its published version,
apparently to satisfy a publish guard that tests for *unpublished* rather than
for *forward*. Evidence in `reports/2026-08-15-version-pin-reconciliation.md`.

## Understated

### Gap 4 / D12 — "`ILogicalSchemaRegistry` has no production consumers"

**Worse than stated.** `LogicalSchemaRegistry.cs` declares the enums, the record
types, and `public interface ILogicalSchemaRegistry`. **No implementation of that
interface exists anywhere under `src/`** — the only `LogicalSchemaRegistry` class
in the repository is in the test project.

It is not a second authority lacking consumers; it is an interface with no
production implementation. This explains why the §11.1 divergences can persist
unobserved: nothing executes the code path they describe. Found by
`governs-check` rejecting a draft of `DEC-0012`.

### Gap 15 — "ADR number collisions across repositories"

**Understated.** The document names the Agent-0014/Platform-0014 collision. The
Agent additionally carries **two different ADR 0003 documents** —
`0003-parser-dispatch-and-relp-native-boundaries.md` and
`0003-profile-kql-preserves-source-event-shape.md` — so a citation to "Agent ADR
0003" does not resolve *within a single repository*. The collision problem is not
only cross-repo.

## Mis-cited

### `archive/RECOVERY.md` sources — "the ADR-5 semantic-view layer"

The instruction set accompanying this import referred to an "ADR-5 semantic-view
layer" among recoverable rejections. **There is no Parse ADR 0005**, and there
never has been — `git log` over `docs/adr/0005*` in Parse returns nothing.

The semantic view layer is reserved in **Parse ADR-1** (which reserves the word
"normalization" for it) and narrowed in **Parse ADR-3** (*the semantic view layer
does not do schema mapping*). Recorded so that a future search for "ADR-5" does
not conclude the layer was deleted when it was never built.

## Unverified, flagged

### §2 and §6.1 — "374 upstream parity cases pass"

**Not verified.** CON-0012 records why the number is not checkable from the
repository: the corpus is scraped from liblognorm's `tests/*.sh` at run time and
filtered twice, and no case is committed. Figures of 374 and 381 have both been
recorded; they cannot both be right.

Session 9 must report the actual count when it extracts and commits the corpus —
and must do so **before** the scraper is retired, since deleting the workflow
deletes the corpus.

### §11 — wire tag 4 encodes `DateTimeOffset`

The document records tag 4 as `DateTimeOffset` in ISO 8601. The estate type
contract (CON-0001, and `CLAUDE.md`) fixes the carrier as `System.DateTime` with
`Kind=Utc`, never `DateTimeOffset` — reinforced by CON-0008, since Rx.Kql
compares `DateTimeOffset` via local wall clock.

These are in tension. `DEC-0003` governs the tagged encoding and FWD-CONTRACT-v2
is expected to resolve it by carrying `DateTime` UTC on the wire, with
`Kind=Unspecified` rejected as `Unrepresentable`. Recorded here so the tension is
not mistaken for a settled position on either side.
