---
id: DEC-0034
status: Proposed
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0001, CON-0006, CON-0014]
---

# DEC-0034 — Select the MVP ASIM tables and views from pinned reference files

## Context

DEC-0013 establishes ASIM-first Gold; DEC-0012 and DEC-0033 retain a
DeltaZulu-owned logical C# contract and DuckLake persistence. They do not
select the complete MVP catalogue or require Sentinel runtime compatibility.
The current Platform MedallionSchemaCatalog registers four telemetry
families, eight source-specific Silver contributors and three Bronze
source tables. AlertEvent and AlertEntity are separate operational views.

Microsoft publishes native normalized tables, query-time ASIM parser
outputs, and logical schemas. They are not interchangeable. Parser outputs
can add aliases and derived fields and remove Azure-specific columns. The
pinned native parser YAML also declares schema versions older than the
reviewed 1.0.0 logical-schema documentation. Treat those version and field
differences as evidence to reconcile, not automatic mappings.

FalconForceTeam/KQLAnalyzer provides a useful precedent: acquire Microsoft
documentation, extract table/column definitions and regenerate a local
machine-readable environment. Its extraction code does not itself download
the repositories and may coerce unrecognized types to string. DeltaZulu
must neither depend on that application nor reproduce such coercion.

## Decision (proposed)

### MVP scope

Select the four currently registered telemetry families as the initial
MVP scope, subject to owner approval. Retain their current logical names;
physical table naming and any compatibility migration are implementation
work under C10 and C07. The following upstream table and parser names
identify references, not DeltaZulu runtime dependencies.

| ASIM family | Upstream normalized table | Upstream unifying parser YAML stems | DeltaZulu Gold logical view | Existing Silver contributors |
|---|---|---|---|---|
| DNS | ASimDnsActivityLogs | ASimDns, imDns | golden.Dns | Sysmon 22; Windows DNS Server 256/257 |
| Network Session | ASimNetworkSessionLogs | ASimNetworkSession, imNetworkSession | golden.NetworkSession | Sysmon 3; Windows Security 5156 |
| Process Event | ASimProcessEventLogs | ASimProcessEvent, imProcessEvent | golden.ProcessEvent | Sysmon 1; Windows Security 4688 |
| Authentication | ASimAuthenticationEventLogs | ASimAuthentication, imAuthentication | golden.Authentication | Windows Security 4624/4625 |

One governed logical contract per family serves NRT and durable hunting.
Persist canonical Gold in DuckLake; expose its query surface without
creating a second independently maintained schema or executing Sentinel
parser functions. Alias projection is generated from the same contract;
any public compatibility name requires explicit migration review.

Preserve existing Bronze and Silver retention, including the nullable
observed-time policy under DEC-0029. Do not import Microsoft workspace,
billing, subscription or ingestion-time semantics unconditionally.

Keep existing AlertEvent and AlertEntity operational views under C07/C16
and DEC-0030. Do not equate AlertEntity with ASIM AssetEntity, or claim
Alert Event conformance, without independent mappings. Additional ASIM
families (Agent Event, Alert Event as external normalized telemetry,
Asset Entity, Audit Event, DHCP Event, Email Event, File Event, Registry
Event, User Management and Web Session) are outside this proposed MVP
telemetry selection; this is not rejection of later support.

### Acquire immutable reference files

Use a small, offline-capable acquisition and extraction workflow inspired
by KQLAnalyzer, not a runtime or copied-code dependency.

| Evidence source | Pinned revision / scope | Role |
|---|---|---|
| Azure/Azure-Sentinel | b2c15c11d6666b9ddf80091663e6c8009058fbcb | ASIM common/entity YAML, ASimTester.csv, selected parser YAML and applicable source parser tests |
| MicrosoftDocs/azure-monitor-docs | d2df7cc0aa1e85c13fc73bf96668f0a149b647e4 | Four native normalized table Markdown definitions under articles/azure-monitor/reference/tables/ |
| Microsoft Learn ASIM schema documentation | Per-family reviewed version and source snapshot, to be pinned during C10 | Logical field meanings, requirement conditions, entity roles and enumerations |

The four table reference filenames are asimdnsactivitylogs.md,
asimnetworksessionlogs.md, asimprocesseventlogs.md and
asimauthenticationeventlogs.md. Their inspected Git blobs are respectively
dea510ba577481cf74299c65122dd46e930269bb,
b8c538b0b8355e1100f7d421d3ef13c69015503f,
9b7a128f87e2f91cb3ad96d99c656a798b57f3b2 and
6ed5ff81f5bc67d1a011ecb3b9cb59f3ecb14c52.
ASimTester.csv is blob de261f4c8e3d41f35801c00ca830aec01cbc8c94.

Acquire only needed files at the reviewed revisions. Record repository,
commit, path, content hash, applicable licence and acquisition tool
version. Cache originals locally without modification. Normal builds and
tests must not fetch mutable upstream content. An explicit update command
may fetch a new candidate snapshot and produce a reviewable diff; no
automatic adoption. Retain required provenance and observe applicable
licence conditions before redistribution of upstream material.

### Extract and reconcile

Use format-aware YAML, CSV and Markdown parsers. Produce deterministic
machine-readable reference inventories recording native table columns,
logical schema fields, requirements, logical types, allowed values,
aliases, and parser versions separately. Unknown/ambiguous types,
duplicates, missing inputs and conflicting definitions require explicit
diagnostics; no silent string fallback. Distinguish legitimate alias
definitions from conflicts. Do not copy arbitrary parser logic or infer
runtime behaviour merely from static output schemas.

Reconcile each selected family with the existing C10 target-field
inventory and mapping baseline. The reference snapshots and generated
inventories are evidence, not another canonical catalogue. C# remains
the internal schema authority. Preserve declared types, observed time,
duration precision, original source identity and provenance. Azure-only
fields, unsupported optional fields, and source-specific gaps receive
explicit dispositions. Do not fabricate mandatory values or claim full
conformance merely because field names or types match.

Kusto.Language may be used for offline parser output analysis with
explicit table/function symbols at the existing supported version
boundaries; syntactic/semantic analysis does not establish execution or
mapping equivalence. The ASIM parser definitions are review inputs, not
required execution dependencies. No AI component is introduced.

### Acceptance criteria

- A clean acquisition at the pinned commits reproduces the selected
  reference files and manifest; extraction from identical local files
  generates identical output without network access.
- All four native table references, logical families, relevant source
  contributors and aliases are accounted for. Conflicts between reference
  layers are visible and resolved or explicitly marked unresolved.
- The existing C10 mapping inventory covers applicable fields, types,
  requirements, enum values, source availability and intentional deviations.
- Catalogue checks verify the C# contracts and actual registered views;
  fixtures for all eight contributors verify source semantics, event time
  and provenance. Replay and durable persistence remain C05/C07 gates.
- Schema changes and additional families require reviewed scope and
  migration evidence. Upstream changes cannot modify the running catalogue.

## Consequences

The MVP remains bounded to existing source-backed telemetry families while
retaining the independent operational alert surfaces. Reference acquisition
becomes reproducible and reviewable. Maintaining multiple external
reference layers adds reconciliation work, but avoids confusing native
table layouts with logical schemas. Unsupported source fields remain
visible gaps rather than fabricated normalized values. No new runtime
dependency, package publication or automatic schema migration follows
from this proposal. C10 retains implementation and verification ownership.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Import every ASIM schema for the MVP | Expands collection, semantics, storage and verification beyond the existing source-backed scope | — |
| Use KQLAnalyzer as a runtime dependency or copy its generated catalogue unchanged | Its catalogue targets Microsoft table/function environments, not the complete ASIM semantic contract; unknown-type fallback is incompatible with DEC-0003 | CON-0006 |
| Use native table definitions alone | Misses logical requirements and query-time aliases, and may adopt Azure-specific semantics | — |
| Use ASimTester.csv alone | Tester inventory does not establish native physical layout or complete semantic/version conformance | — |
| Fetch current upstream definitions during every build | Unreviewed external changes could alter the supported catalogue and queries | — |
| Maintain independent hand-written C# and external-reference-derived runtime schemas | Creates parallel authorities contrary to DEC-0012/DEC-0033 | CON-0014 |

## Revisit trigger

Reopen when a validated detection or investigation requirement cannot be
served by the selected families, when a supported source requires a new
family, or when a pinned ASIM reference change materially alters field
semantics or compatibility. Changes require source-backed mapping and
test evidence rather than an automatically widened catalogue.

## References

- [DEC-0013 — ASIM-first Gold](DEC-0013-golden-semantic-model.md)
- [DEC-0033 — LocalStream and DuckLake](DEC-0033-localstream-replaces-proton.md)
- [C10 mapping baseline](../architecture/ASIM-GOLD-MAPPING-BASELINE.md)
- [Consolidated roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md)
- [Pinned Azure Sentinel ASIM reference](https://github.com/Azure/Azure-Sentinel/tree/b2c15c11d6666b9ddf80091663e6c8009058fbcb/ASIM)
- [Pinned parser catalogue](https://github.com/Azure/Azure-Sentinel/tree/b2c15c11d6666b9ddf80091663e6c8009058fbcb/Parsers)
- [Pinned native table documentation](https://github.com/MicrosoftDocs/azure-monitor-docs/tree/d2df7cc0aa1e85c13fc73bf96668f0a149b647e4/articles/azure-monitor/reference/tables)
- [KQLAnalyzer — acquisition and extraction precedent](https://github.com/FalconForceTeam/KQLAnalyzer)
