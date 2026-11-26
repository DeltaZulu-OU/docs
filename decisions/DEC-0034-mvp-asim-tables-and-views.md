---
id: DEC-0034
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0001, CON-0006, CON-0014]
---

# DEC-0034 — Select the MVP ASIM tables and views from pinned reference files

> **Consolidated conventions:** [DEC-0038](DEC-0038-medallion-schema-conventions.md) supersedes the schema and naming provisions of this decision. Remaining requirements retain their status.

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

## Decision

### MVP scope

On 2026-11-25 the owner approved eight telemetry families for the MVP:
the four currently registered families plus File Event, User Management,
Registry Event and Audit Event. Web Session and DHCP Event were explicitly
excluded from the MVP. Together with two existing operational alert views,
the target comprises ten Gold logical views. Retain existing logical names;
physical table naming and any compatibility migration are implementation
work under C10 and C07. The following upstream table and parser names
identify references, not DeltaZulu runtime dependencies.

| ASIM family | Upstream normalized table | Upstream unifying parser YAML stems | DeltaZulu KQL view | Current or candidate source coverage |
|---|---|---|---|---|
| DNS | ASimDnsActivityLogs | ASimDns, imDns | `Dns` | Sysmon 22; Windows DNS Server 256/257 |
| Network Session | ASimNetworkSessionLogs | ASimNetworkSession, imNetworkSession | `NetworkSession` | Sysmon 3; Windows Security 5156 |
| Process Event | ASimProcessEventLogs | ASimProcessEvent, imProcessEvent | `ProcessEvent` | Sysmon 1; Windows Security 4688 |
| Authentication | ASimAuthenticationEventLogs | ASimAuthentication, imAuthentication | `Authentication` | Windows Security 4624/4625 |
| File Event | ASimFileEventLogs | ASimFileEvent, imFileEvent | `FileEvent` | Candidate: Sysmon 11, 23, 26; selected Windows Security events |
| User Management | ASimUserManagementActivityLogs | ASimUserManagement, imUserManagement | `UserManagement` | Candidate: Windows Security / Active Directory account and group changes |
| Registry Event | ASimRegistryEventLogs | ASimRegistryEvent, imRegistryEvent | `RegistryEvent` | Candidate: Sysmon 12, 13, 14; Windows Security 4657 |
| Audit Event | ASimAuditEventLogs | ASimAuditEvent, imAuditEvent | `AuditEvent` | Candidate: Windows Security and System audit events, including 1102 and service/task changes |

### Naming convention

Use singular PascalCase ASIM family names under DEC-0013. The public KQL
identifier is the unqualified name in the table; the SQL view is
`golden.<Name>` (for example, `golden.Dns`). `GoldenSchema` in
`SchemaConventions` is `golden`; `ApprovedViewCatalog` registers the
unqualified `CanonicalViewDef.Name` as the Kusto table symbol. Do not
use the historical `*Activity` names, `ASim*Logs` native table names,
`im*`/`_Im_*` parser names, pluralized names or a new `gold` SQL namespace
as alternative canonical identifiers. Backing table names are separate
physical implementation details. Any compatibility alias or rename needs
explicit migration review.

The first four rows have existing C# declarations and eight declared Silver
contributors. The last four are approved scope, not implemented contracts;
source coverage is illustrative until verified. Keep Audit Event semantics
distinct from more specific families and preserve event identity if a source
record contributes to multiple views.

One governed logical contract per family serves NRT and durable hunting.
Persist canonical Gold in DuckLake; expose its query surface without
creating a second independently maintained schema or executing Sentinel
parser functions. Alias projection is generated from the same contract;
any public compatibility name requires explicit migration review.

Preserve existing Bronze and Silver retention, including the nullable
observed-time policy under DEC-0029. Do not import Microsoft workspace,
billing, subscription or ingestion-time semantics unconditionally.

Keep existing AlertEvent and AlertEntity operational views under C07/C16
and DEC-0030. These are the ninth and tenth logical views, not additional
ASIM telemetry families: KQL `AlertEvent` and `AlertEntity`, SQL
`golden.AlertEvent` and `golden.AlertEntity`, currently backed by
`lake.alert_events` and `lake.alert_entities` respectively. Do not equate AlertEntity with ASIM AssetEntity,
or claim Alert Event conformance, without independent mappings. Web Session
and DHCP Event are explicitly outside the approved MVP. Agent Event,
external Alert Event telemetry, Asset Entity and Email Event also remain
outside the selected scope. These exclusions do not reject later support.

### Acquire immutable reference files

Use a small, offline-capable acquisition and extraction workflow inspired
by KQLAnalyzer, not a runtime or copied-code dependency.

| Evidence source | Pinned revision / scope | Role |
|---|---|---|
| Azure/Azure-Sentinel | b2c15c11d6666b9ddf80091663e6c8009058fbcb | ASIM common/entity YAML, ASimTester.csv, selected parser YAML and applicable source parser tests |
| MicrosoftDocs/azure-monitor-docs | d2df7cc0aa1e85c13fc73bf96668f0a149b647e4 | Eight native normalized table Markdown definitions under articles/azure-monitor/reference/tables/ |
| Microsoft Learn ASIM schema documentation | Per-family reviewed version and source snapshot, to be pinned during C10 | Logical field meanings, requirement conditions, entity roles and enumerations |

The eight native table Markdown files have been verified at the pinned
revision:

| Filename | Git blob |
|---|---|
| asimdnsactivitylogs.md | dea510ba577481cf74299c65122dd46e930269bb |
| asimnetworksessionlogs.md | b8c538b0b8355e1100f7d421d3ef13c69015503f |
| asimprocesseventlogs.md | 9b7a128f87e2f91cb3ad96d99c656a798b57f3b2 |
| asimauthenticationeventlogs.md | 6ed5ff81f5bc67d1a011ecb3b9cb59f3ecb14c52 |
| asimfileeventlogs.md | 41f99804bed22597b493a04809d4efa5355c4c15 |
| asimusermanagementactivitylogs.md | 90b3e69b5315d180305cd5513e8ce402b1552092 |
| asimregistryeventlogs.md | d07ad252fd451a3d9eec30c51ea89cc2af51ff66 |
| asimauditeventlogs.md | ee5282302289448bfcb98ab21f7ae753e34fa7d0 |

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

Extend the existing C10 target-field inventory and mapping baseline from
four to eight telemetry families, preserving the current verified source
inventory until new contracts exist. Reconcile all selected families. The reference snapshots and generated
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
- All eight native table references, logical families, relevant source
  contributors and aliases are accounted for. Conflicts between reference
  layers are visible and resolved or explicitly marked unresolved.
- The existing C10 mapping inventory covers applicable fields, types,
  requirements, enum values, source availability and intentional deviations.
- Catalogue checks verify exact canonical view names, the SQL namespace,
  KQL registration and C# contracts against the approved catalogue;
  fixtures for all eight existing contributors and every newly admitted
  contributor verify source semantics, event time and provenance. Replay
  and durable persistence remain C05/C07 gates.
- Schema changes and additional families require reviewed scope and
  migration evidence. Upstream changes cannot modify the running catalogue.

## Consequences

The MVP expands from four declared telemetry contracts to eight approved
telemetry families, retaining two independent operational alert views.
The additional four require C10 catalogue, source mapping and fixture work. Reference acquisition
becomes reproducible and reviewable. Maintaining multiple external
reference layers adds reconciliation work, but avoids confusing native
table layouts with logical schemas. Unsupported source fields remain
visible gaps rather than fabricated normalized values. No new runtime
dependency, package publication or automatic schema migration follows
from this Decision. C10 retains implementation and verification ownership.

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

- [Platform source: schema conventions](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Analytics/Schema/SchemaConventions.cs)
- [Platform source: approved KQL catalogue](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Analytics/Catalog/ApprovedViewCatalog.cs)
- [Platform source: operational view contracts](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Analytics/Schema/OperationsSchemaContracts.cs)

- [DEC-0013 — ASIM-first Gold](DEC-0013-golden-semantic-model.md)
- [DEC-0033 — LocalStream and DuckLake](DEC-0033-localstream-replaces-proton.md)
- [C10 mapping baseline](../architecture/ASIM-GOLD-MAPPING-BASELINE.md)
- [Consolidated roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md)
- [Pinned Azure Sentinel ASIM reference](https://github.com/Azure/Azure-Sentinel/tree/b2c15c11d6666b9ddf80091663e6c8009058fbcb/ASIM)
- [Pinned parser catalogue](https://github.com/Azure/Azure-Sentinel/tree/b2c15c11d6666b9ddf80091663e6c8009058fbcb/Parsers)
- [Pinned native table documentation](https://github.com/MicrosoftDocs/azure-monitor-docs/tree/d2df7cc0aa1e85c13fc73bf96668f0a149b647e4/articles/azure-monitor/reference/tables)
- [KQLAnalyzer — acquisition and extraction precedent](https://github.com/FalconForceTeam/KQLAnalyzer)
