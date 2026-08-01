# Governing Decisions by repository

Generated from each Decision's `repos:` front-matter, so it cannot drift from the
Decisions themselves. Each repository's `docs/README.md` points here.

A Decision listed against a repository governs code in it, and `governs-check`
fails if a symbol or path it names stops existing. A Decision with no repository
is estate-wide — a principle rather than a claim on one codebase.

## DeltaZulu.Kql

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0003`](../decisions/DEC-0003-tagged-encoding-normalise-or-reject.md) | Accepted | Ten-type tagged encoding; normalise-or-reject |

## DeltaZulu.Parse

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0005`](../decisions/DEC-0005-agent-extraction-authoritative-for-silver.md) | Accepted | Agent extraction is authoritative for Silver |

## DeltaZulu.Forward

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0001`](../decisions/DEC-0001-messagepack-wire-format.md) | Accepted | Wire format is MessagePack `ForwardLogBatch` in `TypedBatch` frames |
| [`DEC-0002`](../decisions/DEC-0002-identity-tuple-resolves-catalogue.md) | Accepted | Per-record identity tuple resolves the catalogue entry |
| [`DEC-0003`](../decisions/DEC-0003-tagged-encoding-normalise-or-reject.md) | Accepted | Ten-type tagged encoding; normalise-or-reject |
| [`DEC-0019`](../decisions/DEC-0019-collector-is-forward-server-host.md) | Accepted | Collector is the Forward server host |

## DeltaZulu.LogCluster

_No Decision names this repository yet._

## DeltaZulu.LocalStream

_No Decision names this repository yet._

## DeltaZulu.DurableBuffer

_No Decision names this repository yet._

## DeltaZulu.Agent

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0008`](../decisions/DEC-0008-filter-may-drop-if-declared.md) | Accepted | Filter may drop; must be declared, versioned, counted |
| [`DEC-0009`](../decisions/DEC-0009-state-updates-unconditionally.md) | Accepted | State machines update unconditionally, before filtering |
| [`DEC-0014`](../decisions/DEC-0014-windows-etw-always-sysmon-recommended.md) | Accepted | Windows: ETW Kernel-Process always on; Sysmon recommended, never assumed |
| [`DEC-0015`](../decisions/DEC-0015-uniform-derived-processkey.md) | Accepted | Uniform derived `ProcessKey` by documented precedence |

## DeltaZulu.Platform

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0010`](../decisions/DEC-0010-bronze-write-once-proton-staging-only.md) | Accepted | Bronze write-once; Proton holds no durable Bronze or Silver |
| [`DEC-0012`](../decisions/DEC-0012-single-type-contract-catalogue.md) | Accepted | Type-contract catalogue is the single authority, producer-agnostic |
| [`DEC-0013`](../decisions/DEC-0013-golden-semantic-model.md) | Proposed | Golden semantic model and naming |
| [`DEC-0017`](../decisions/DEC-0017-proton-ingest-over-http.md) | Accepted | Proton ingest over HTTP |
| [`DEC-0020`](../decisions/DEC-0020-golden-as-materialised-view.md) | Accepted | Golden is a materialised view into a declared target stream |
| [`DEC-0022`](../decisions/DEC-0022-collector-lives-in-platform.md) | Proposed | The collector is a project inside `DeltaZulu.Platform`, deployed separately |
| [`DEC-0024`](../decisions/DEC-0024-bronze-integrity-controls.md) | Proposed | Bronze carries integrity controls, not just a retention setting |
| [`DEC-0027`](../decisions/DEC-0027-proton-is-not-a-query-surface.md) | Accepted | Proton is a streaming runtime, not a query surface |
| [`DEC-0028`](../decisions/DEC-0028-gold-schema-generated-from-code.md) | Accepted | One Gold contract generated from C#; physical alignment is best effort |
| [`DEC-0029`](../decisions/DEC-0029-gold-is-governed-by-event-time.md) | Accepted | Gold is governed by extracted event time; ingest time is provenance |
| [`DEC-0030`](../decisions/DEC-0030-alert-identity-and-replay.md) | Accepted | Alerts reference Gold by identifier; identity excludes rule version |
| [`DEC-0031`](../decisions/DEC-0031-reorder-buffer-between-proton-and-ducklake.md) | Accepted | Short event-time reorder buffer between Proton and DuckLake |

## Estate-wide (no single repository)

| Decision | Status | Subject |
|---|---|---|
| [`DEC-0004`](../decisions/DEC-0004-no-arrow-catalogue-typed-records.md) | Accepted | No Arrow; catalogue-typed records with per-backend adapters |
| [`DEC-0006`](../decisions/DEC-0006-server-maps-and-enriches.md) | Accepted | Server performs mapping and enrichment, not parsing |
| [`DEC-0007`](../decisions/DEC-0007-agent-enriches-perishable-context-only.md) | Accepted | Agent enriches only perishable local context |
| [`DEC-0011`](../decisions/DEC-0011-silver-to-golden-dual-compiled.md) | Proposed | Silver→Golden authored once in KQL, compiled to both dialects |
| [`DEC-0016`](../decisions/DEC-0016-best-effort-collection-mandatory-accounting.md) | Accepted | Best-effort collection, mandatory loss accounting |
| [`DEC-0018`](../decisions/DEC-0018-lake-is-ducklake.md) | Accepted | Lake is DuckLake with a SQL catalogue database |
| [`DEC-0021`](../decisions/DEC-0021-threshold-as-windowed-aggregate.md) | Proposed | Detection threshold expressed inside the KQL as a windowed aggregate |
| [`DEC-0023`](../decisions/DEC-0023-completeness-requires-external-canaries.md) | Accepted | Completeness is measured by external canaries, and unmeasurable sources say so |
| [`DEC-0025`](../decisions/DEC-0025-adjudication-boundary.md) | Proposed | DeltaZulu measures precision, never recall, and splits a miss into its two causes |
| [`DEC-0026`](../decisions/DEC-0026-nrt-first-scheduled-deferred.md) | Accepted | Phase one builds the NRT path only; scheduled detections deferred |
