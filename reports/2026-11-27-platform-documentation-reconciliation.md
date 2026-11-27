# Platform documentation reconciliation — 27 November 2026

Pinned [Platform d6b3a43](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/d6b3a435466d57317e4c70a26948ea5d68075675/docs).
Retrieved all 13 non-index documents and inspected introductions,
section inventories and selected claims. The translation dictionary
is approximately 772 KB; individual entries were not exhaustively
reviewed. No runtime tests or product edits.

| Document | Classification and disposition | Work |
|---|---|---|
| ARCHITECTURE.md | Mixed target and implementation; authority note qualifies legacy Proton/direct lake design | C08/C05/C06/C07 |
| TARGET_USER_STORIES.md | Historical/candidate backlog; preserve workflow outcomes, not Proton or scheduled execution | C16/C06 |
| analytics/KQL-to-DuckDB-translation-spec.md | Detailed relational translation reference; illustrative symbols not approved views | C06/C10 |
| analytics/README.md | Local navigation; active references not independent policy | C08 |
| analytics/kql-duckdb-comparison-register.md | Semantic parity evidence methodology; not live Kusto validation | C06 |
| analytics/kql-syntax-coverage-checklist.md | Historical capability tracker; verify statuses and stale reference path | C06/C08 |
| architecture/agent-control-plane.md | Management implementation reference and candidate requirements | C17 |
| architecture/agent-daemon-responsibilities.md | Historical daemon specification; separate Agent exists, simulator is not daemon qualification | C12/C17 |
| design/PRODUCT_IDENTITY.md | Local UI/design reference; three-module inventory stale against host registration | C16 |
| reviews/BRANCH_CONFLICT_ANALYSIS_2026-08-12.md | Historical branch dispositions; not current merge or test status | C08/C14 |
| reviews/DOCUMENTATION_CODE_GAP_ANALYSIS_2026-07-19.md | Historical source audit; even its supersession note retains obsolete Quack/Proton direction | C08/C05 |
| reviews/PRODUCTION_V1_GAP_ANALYSIS.md | Historical readiness audit; rebaseline surviving gates, not dated completion claims | C14/C16/C17 |
| reviews/TYPE_CONTRACT_CATALOG_PATCH_REVIEW_2026-08-12.md | Historical rejected patch and adaptation; retain single logical authority, retire dual-engine premise | C03/C10 |

## Source-pinned legacy wiring

| Source | Observation |
|---|---|
| [Solution](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/DeltaZulu.Platform.slnx) | Data.Proton remains a solution project. |
| [Web project](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Web/DeltaZulu.Platform.Web.csproj) | Direct Data.Proton project reference. |
| [Test project](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/tests/DeltaZulu.Platform.Tests/DeltaZulu.Platform.Tests.csproj) | Direct Data.Proton project reference. |
| [Program](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Web/Program.cs) | Calls AddAnalyticsWebModule; registers four modules including Agent Management. |
| [Analytics registrations](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Web/Analytics/Hosting/AnalyticsWebModuleServiceCollectionExtensions.cs) | Registers LocalStream host, raw publisher, Bronze writer/consumer and hosted ingestion service; also calls AddProtonDetectionBackend and AddProtonStreaming and registers AlertMediationService. |
| [Proton registrations](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Data.Proton/ProtonServiceCollectionExtensions.cs) | Registers compilation backend, deployer, keyed schema emitter/applier, HTTP executor, source publishers and subscriber. |
| [Ingestion project](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Ingestion/DeltaZulu.Platform.Ingestion.csproj) | References LocalStream package. |
| [LocalStream ingestion service](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Web/Analytics/Hosting/LocalStreamIngestionService.cs) | Web-hosted ingestion resolves Bronze consumer; not proof of separate collector. |

## Discrepancies and migration gates

| ID | Finding and disposition |
|---|---|
| PLDOC-01 | Legacy Proton is registered in Web composition, not just present in tree. DEC-0033 target discrepancy. Trace actual callers/configuration and qualify replacement before removal; no runtime invocation demonstrated. |
| PLDOC-02 | Historical architecture and stories retain direct Agent Quack/Proton and scheduled detection. DEC-0022/0026/0033 govern. Preserve workflow outcomes, not mechanisms. |
| PLDOC-03 | Three-module product identity and stories omit Agent Management; four registrations observed. Registration is not feature completion. |
| PLDOC-04 | Translation dictionary and checklist are not executable parity proof. Checklist cites obsolete docs/KQL-to-DuckDB-translation-spec.md location; actual path is docs/analytics/. Preserve reference and rebaseline C06. |
| PLDOC-05 | Daemon document describes simulator-era state. Agent is a separate repository; qualify current protocol, signing and rollout under C17. |
| PLDOC-06 | Historical gap and patch reviews contain obsolete supersession guidance. Preserve dated evidence, qualify current target centrally; local broken/obsolete references remain migration work. |

Before retiring Proton, trace compilation/deployment callers, keyed
schema consumers, publisher/subscriber and mediation dependencies,
configuration and deployment artifacts. Qualify separate collector,
bound NRT execution, durable state/intent recovery, canonical lake
sinks and evidence reconciliation under C05/C06/C07. Verify no active
legacy registrations or references remain and preserve surviving
behavioral tests. This is a deferred implementation gate, not a
removal authorization.

The [Platform responsibility contract](../architecture/PLATFORM-RESPONSIBILITY-CONTRACT.md) centralizes
surviving boundaries. No Accepted Decisions changed.
