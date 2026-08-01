---
id: DEC-0022
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0016]
---

# DEC-0022 — The collector is a project inside `DeltaZulu.Platform`, deployed separately

## Context

CON-0016: the collector has no repository. `DEC-0019` says what it *is* — the
Forward server host that decodes once and writes three destinations — without
saying where it lives, and governance attaches to repositories, so the ingestion
path is currently governed by nothing.

Full options analysis in `reports/2026-08-16-collector-ownership.md`.

## Decision

The collector lives in `DeltaZulu.Platform`, as its own executable rather than as
a service hosted inside `DeltaZulu.Platform.Web`.

The catalogue is the contract the collector must agree with, and it is the
artefact that changes most. Co-locating them means a catalogue change and its
collector consequence land in one commit and one CI run, instead of a cross-repo
version handshake over a package feed the estate has not yet got working from a
clean container.

Both sink adapters — `Data.DuckDb` and `Data.Proton`, the latter already shipping
`ProtonHttpExecutor` — are in the same repository.

The separate-executable qualifier is load-bearing: ingest availability must not
be coupled to the Blazor host's deployment lifecycle or its threat surface.

## Status note — accepted 2026-08-17

Accepted because the NRT pipeline work already depends on it as settled: `DEC-0027`
places the collector's downstream consumers (Proton and DuckLake) without
revisiting where the collector itself lives, and `DEC-0031`'s reorder buffer sits
between Proton and DuckLake on the assumption that the write path Platform hosts
is the one described here. Leaving this `Proposed` while later Decisions built on
it as fact would have made the dependency silent.

Acceptance does not resolve the open item this Decision itself names: the
`RawLogNdjsonCodec` boundary. It remains confined to seeding — a fixtures path,
not an ingest path — and stays that way until a Decision says otherwise. If it
ever carries agent telemetry into Silver, it becomes the banned second ingest
contract arriving through a different door, and this acceptance does not license
that; it only settles where the collector that must not do that lives.

No `governs:` entry is added by this acceptance. `DeltaZulu.Platform.Ingestion`
remains a library project — no `OutputType` is set, so it builds as one, not the
standalone executable this Decision requires — so there is no concrete symbol yet
for `governs-check` to hold to the "separate executable" qualifier. That
qualifier becomes checkable, and should be added to `governs:`, once the
executable exists.

## Consequences

- Platform's Decision set governs the ingestion path. That is the point of the
  choice, and it is also its main cost.
- Platform's CI gates the collector. Acceptable only because locked-mode restore
  began enforcing something on 2026-08-15; it would not have been before.
- `DeltaZulu.Platform.Ingestion` already exists as a proto-collector, so this
  ratifies where the work has been going rather than redirecting it.
- **`RawLogNdjsonCodec` needs an explicit boundary before the collector is built
  beside it.** Forward's standing constraint bans a degraded fallback format from
  Forward so that there is one typed ingest contract. That codec is in Platform,
  not Forward, and its only consumers today are a DuckDb seeding converter and
  its tests — a fixtures path, not an ingest path, so not currently a violation.
  If it ever carries agent telemetry into Silver it becomes the banned second
  ingest contract arriving through a different door, and the repository boundary
  will have been a technicality rather than a distinction. Confine it to seeding
  explicitly while that is still cheap to state.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| A project inside `DeltaZulu.Forward` | Gives a transport protocol library hard dependencies on DuckDB and Proton, neither of which belongs on the Agent's dependency graph. Also makes Forward host the sink adapters its no-fallback constraint exists to keep it free of | — |
| A new repository | Turns every catalogue change into a cross-repository version handshake over a feed that does not yet restore from a clean container, and adds an eighth owned surface to an estate already flagged for that (gap 18) | — |
| A hosted service inside `Platform.Web` | Couples ingest availability to the Blazor host's deployment lifecycle, and puts ingest on the threat surface of a host with no real authentication (gap 5) | — |

## Revisit trigger

Extract the collector to its own repository if either:

- it needs a release cadence independent of the catalogue — for example tenants
  running collectors at different versions against one Platform; or
- a second consumer of the type-contract catalogue emerges outside Platform. In
  that case the **catalogue** is the thing that should move to its own home, and
  the collector should follow it rather than the reverse.
