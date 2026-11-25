# Package lineage and final build matrices

## Default-branch baseline

Snapshot taken on 25 November 2026. The application column identifies workflows at the exact revision. Other successful runs included dependency and repository scans. Open PR counts include dependency updates. Lock counts include tracked NuGet dependency locks only.

| Repository | Branch | Revision | Open PRs | Locks | Application or governance run |
|---|---|---|---:|---:|---|
| docs | master | [`97f518851`](https://github.com/DeltaZulu-OU/docs/commit/97f518851979a9de19782a03c092d7035649ac99) | 0 | 0 | [governs-check](https://github.com/DeltaZulu-OU/docs/actions/runs/45621654436) |
| DeltaZulu.Agent | master | [`069d26b7d`](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/commit/069d26b7d1bac819538b275f6a9a492992f0cd3b) | 5 | 0 | [Unit Tests](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/actions/runs/45619165875) |
| DeltaZulu.DurableBuffer | master | [`1fb8ecaae`](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/commit/1fb8ecaaea402894f94ec84e7aa11aae8d7bf984) | 4 | 0 | No matching run at this revision |
| DeltaZulu.Forward | master | [`19b3d0006`](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/commit/19b3d000697922870742f52ba46e8b4fc3de3ee6) | 5 | 0 | No matching run at this revision |
| DeltaZulu.Kql | main | [`a94dda9cf`](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/commit/a94dda9cfd87c950b4996cffdb33f3d4c980b485) | 4 | 3 | No matching run at this revision |
| DeltaZulu.LocalStream | main | [`aeec9a53e`](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/aeec9a53e1fde876739e3b014644b8e08cb00ae9) | 4 | 0 | No matching run at this revision |
| DeltaZulu.LogCluster | master | [`7770d422a`](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/commit/7770d422a1f433102e0689fbc97ad174506106b5) | 3 | 6 | [Unit Tests](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/actions/runs/45621203831) |
| DeltaZulu.Parse | master | [`731b5b1d7`](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/commit/731b5b1d77696e1eff9cf24c4e26561d31b7a93b) | 3 | 4 | [Build, Test, and Pack](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/actions/runs/45618952634) |
| DeltaZulu.Platform | master | [`e89755e6b`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/e89755e6b37fe40c720e483eba01916accc56a2d) | 5 | 14 | [Unit Tests](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/45621349535) |

Platform run 45621349535 passed locked restore, unchanged-lock verification, Release build and tests on all three hosts. Each job log reports 1,338 passed, zero failed and zero skipped. LogCluster run 45621203831 passed the same sequence with 25 tests per host. Governance run 45621654436 passed for the docs revision above. The Platform tests establish a build baseline for C16 and C17. Individual user workflows and cross-tenant controls still require their own evidence.

## Published and source versions

| Package | Source version | Public GitHub Packages listing | Consumer evidence |
|---|---|---|---|
| DeltaZulu.LocalStream | 0.1.0 | [1.0.0](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.LocalStream) | Agent central version 1.0.0 |
| DeltaZulu.DurableBuffer | 1.0.0 (SDK default) | [1.0.0](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.DurableBuffer) | Agent central version 1.0.0 |
| DeltaZulu.Forward | 0.3.1 | [0.3.1](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.Forward) | Agent central version 0.3.1 |
| DeltaZulu.Parse | 0.1.1 | [0.1.1](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.Parse) | Agent and LogCluster central version 0.1.1 |
| DeltaZulu.Kql | 1.1.0-preview.1 | [1.1.0-preview.1](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.Kql) | Library declares Kusto.Language 9.2.0 minimum |
| DeltaZulu.LocalStream.Query | 0.1.0 | [HTTP 404](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.LocalStream.Query) | Project reference to LocalStream core |
| DeltaZulu.LocalStream.Query.LiteDB | 0.1.0 | [HTTP 404](https://github.com/orgs/DeltaZulu-OU/packages/nuget/package/DeltaZulu.LocalStream.Query.LiteDB) | Project reference to Query, LiteDB 5.0.21 |

Registry values are the versions displayed by the public package pages. A 404 leaves package visibility and publication unresolved. The LocalStream publication workflow packs the core project only. Agent and Platform are applications. LogCluster sets IsPackable=false and has a separate Native AOT CLI publication surface.

SDK 10.0.404 evaluated Version, PackageVersion and TargetFramework on the current LocalStream core and DurableBuffer projects. Both target net10.0. LocalStream returned 0.1.0 for both version properties. DurableBuffer returned 1.0.0 for both. Its next distinct release needs an intentional version selection. An explicit property is unnecessary to reproduce the current effective number.

LocalStream [publish run 30011960723](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/actions/runs/30011960723) succeeded at `ce7d95a3ae3dc7a1ecded73099199abf045feae9`, the commit referenced by the annotated v1.0.0 tag. The version property was absent there. Commit [0645090](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/064509053828ba8a2e5887ebe480f0a582cd2fd0) subsequently added 0.1.0. Seven files under the core project differ between the tag and current main. Changing the version back to 1.0.0 would reuse a published identity for different source.

DurableBuffer [publish run 29861111418](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/actions/runs/29861111418) succeeded at `5574911e843dde8d1a4b869433908b3b1b009397`. No release tag was present in the fetched repository. Both historical job-log endpoints returned HTTP 410 and neither run retained a package artifact. The anonymous NuGet endpoints required authentication. The public registry pages, historical workflows and refs establish release lineage. Binary hashes, embedded repository metadata and an independent consumer restore remain outstanding.

Agent specifies both packages as 1.0.0 in Directory.Packages.props. Runtime, Filter, CLI, Pipeline and ProfileWorkbench reference both directly. Daemon references DurableBuffer directly. No NuGet dependency lock is tracked anywhere in Agent at the recorded revision. Its workflow invokes locked restore, but the repository supplies no reviewed package hashes. The passing Agent matrix demonstrates application compilation against its CI restore. It does not demonstrate compilation against current LocalStream main or DurableBuffer master.

The two opaque core projects reference Logging.Abstractions without Kusto dependencies. Platform Domain and Application reference Kusto.Toolkit and Kusto.Language. Platform centrally requests 2.2.0 and 12.4.1 respectively. Agent Filter depends on Microsoft.Rx.Kql 3.5.3. The supported Kusto.Language span and exact application constraints are governed by CON-0006. Tests against both supported runtime combinations remain open.
