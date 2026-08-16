# Collector ownership — decision memo

Date: 2026-08-16. Session 12. **Memo only — no code was written.**

Concerns CON-0016 and gap 7: the collector terminates the Forward transport
(`DEC-0019`), decodes once, and writes three destinations — and it has no
repository, no host, and no sink adapters. `architecture/PIPELINE.md` §3 calls
this the highest-leverage outstanding organisational decision, because
governance attaches to repositories and so this choice determines which Decision
set governs the ingestion path.

## Recommendation: a project inside `DeltaZulu.Platform`, built as its own deployable, not inside the Web host.

## What the collector actually needs

| Need | Where it lives today |
|---|---|
| Forward server session handling | `DeltaZulu.Forward` (library, already has both sides) |
| Type-contract catalogue resolution | `DeltaZulu.Platform.Domain` |
| DuckLake write path | `DeltaZulu.Platform.Data.DuckDb` |
| Proton HTTP ingest | `DeltaZulu.Platform.Data.Proton` (`ProtonHttpExecutor` ships today) |
| Durable spool with per-sink cursors | Nothing. To be written |

Four of the five already exist, and three of those four are in Platform.

## The options

### A project inside `DeltaZulu.Forward` — rejected

The collector needs DuckDB and Proton clients. Putting it in Forward gives a
**transport protocol library** a hard dependency on two storage engines, which is
a category error: Forward is consumed by the Agent, where neither engine has any
business being on the dependency graph.

Forward also carries a standing constraint that no degraded fallback format may
be added to it, precisely so it stays a single typed contract. A repository that
also hosts sink adapters stops being the thing that constraint protects.

### A new repository — rejected, with one condition that would reverse this

Cleanest ownership and an independent release cadence. Two arguments against, one
of which is decisive:

1. **The catalogue is the contract, and it changes most.** `DEC-0002` resolves a
   catalogue entry per record from the identity tuple, and `DEC-0012` makes the
   catalogue the single authority. A collector in its own repository turns every
   catalogue change into a cross-repository version handshake on the one artefact
   that changes most often. The estate's package-feed path is already a
   documented weak point — the `deltazulu-github` source is undefined in three
   repositories' committed `NuGet.config`, and restoring `DeltaZulu.*` from a
   clean container still needs a PAT nobody has wired up.
2. **Gap 18.** Five decisions each shed a dependency, and the aggregate owned
   surface is already flagged as large for a team this size. An eighth repository
   with its own versioning discipline and compatibility matrix is a real cost
   against a benefit that is mostly tidiness.

### A project inside `DeltaZulu.Platform` — recommended

It puts the collector next to the catalogue it must agree with, and next to both
sink adapters it must drive. A catalogue change and its collector consequence
land in one commit, in one repository, verified by one CI run.

**The important qualifier: same repository, separate deployable.** The collector
must be its own executable, not a hosted service inside `DeltaZulu.Platform.Web`.
Ingest availability must not be coupled to the Blazor host's deployment
lifecycle — you should not restart ingestion to ship a dashboard change, and the
Web host's security posture (no real authentication today, gap 5) should not be
on the ingest path's threat surface.

## What the recommendation costs, stated plainly

- **Platform's Decision set governs ingestion.** That is the whole point of the
  choice, but it means Platform's ADR history — including the two amendments
  already recorded against it, ADR 0007's agent-boundary clause and ADR 0016's
  retired premise — is the governing set.
- **Platform's CI gates the collector.** Now acceptable: lock files are committed
  and locked-mode restore actually enforces something as of 2026-08-15. It would
  not have been acceptable a day earlier.
- **Repository-level policies are shared**, including release cadence for
  anything published from Platform.

## A finding that bears directly on this

`DeltaZulu.Platform.Ingestion` **already exists** and is a proto-collector: an
in-memory raw-log bus (`InMemoryRawLogBus`, `IRawLogPubSub`, `RawLogBatch`,
`RawLogEnvelope`) and an NDJSON codec (`RawLogNdjsonCodec`).

Two things follow.

**First, it strengthens the recommendation.** The estate has already, without
deciding to, started building the collector inside Platform. Choosing Platform
ratifies where the work went; choosing anything else means moving it.

**Second, and more importantly: the NDJSON codec deserves scrutiny.** Forward's
standing constraint forbids adding NDJSON or any degraded fallback *to Forward*,
on the grounds that a fallback becomes a second permanent consumer contract and
undermines type fidelity. The constraint is scoped to Forward by its wording, and
`RawLogNdjsonCodec` is in Platform — but if it ever carries agent telemetry into
Silver, it is the banned second ingest contract arriving through a different
door, and the scoping is a technicality rather than a distinction.

Current consumers are one seeding converter
(`Data.DuckDb/Seeding/SeedSqlRawLogNdjsonConverter.cs`) and its tests. That is a
seeding and fixtures path, not a live ingest path, so **it is not currently a
violation**. It should be explicitly confined to that role before the collector
is built alongside it, because the cheapest moment to state that boundary is
before something starts depending on it.

Whether `Platform.Ingestion` is the collector's home project or is superseded by
a new one is an implementation detail for whoever builds it. The NDJSON boundary
is not.

## Recorded as

`DEC-0022`, status `Proposed`, with the revisit trigger below.

**Revisit trigger:** extract the collector to its own repository if either (a) it
needs a release cadence independent of the catalogue — for example, tenants
running collectors at different versions against one Platform — or (b) a second
consumer of the type-contract catalogue emerges outside Platform, at which point
the catalogue itself is the thing that should move, and the collector should
follow it rather than the reverse.
