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

## Independent branch validation

| Project | Branch commit | Validation on Linux x64 with SDK 10.0.404 |
|---|---|---|
| DurableBuffer | [e677fd3](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/commit/e677fd32c080235d5f563f19d0c540e575efa5ce) | Two generated locks, unchanged on locked restore. Release build, 94 tests and local pack passed. The net10.0 package declares Logging.Abstractions 10.0.10. |
| LocalStream | [197a083](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/197a0831d04188c1d48117da81fb9df1e6f1ecff) | Six generated locks, unchanged on locked restore. Release build and 59 core, 55 Query and 10 LiteDB tests passed. All three local packages built. Query depends on core 0.1.0. The LiteDB adapter depends on Query 0.1.0 and LiteDB 5.0.21. |
| LogCluster | [91e2013](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/commit/91e2013afe65e673cd21f05ec8cefac6d43bd292) | Locked restore, Release build and all 27 tests passed. The Parse 0.1.1 release asset satisfied the committed NuGet content hash. Its nuspec identifies commit be982d01acf3ff453bc8a751f8063b7de11ee6b2, also the release tag target. |

Both build branches use only the public source for their actual dependency sets. CI selects the pinned SDK and checks for new or modified lockfiles. Package versions and publication settings were preserved. The LogCluster branch bounds the configured input count at Int32.MaxValue while retaining its public long option type. At precisely Int32.MaxValue the previous scoring expression evaluated integer addition before converting to double. The regression exercises that value without allocating records. These branches are unmerged.

The differential fixture used upstream [logcluster.pl at e3b74b9](https://github.com/ristov/logcluster/tree/e3b74b99ab831bfedabf5ee3f428abb394945769). Input consisted of the following UTF-8 lines, each terminated by LF, SHA-256 `2df8ffcf481d400e649aef30f880a1eecfc5a07d3187b387eb37502305cff646`.

```text
svc start red done
svc start blue done
svc start amber done
unique
```

At minimum support two, Perl and both .NET strategies returned one pattern, `svc start *{1,1} done`, support three, and one outlier, `unique`. Materialized and streaming JSON outputs were byte-identical. This covers a fixed internal single-token gap. Merge, variable-width, weighting and other reference-corpus cases remain open.

Native publication has a separate failure. On linux-x64 an explicit RID locked publish fails first with NU1004 on the portable LogCluster core and Suggester projects. They inherit the publish RID but their lockfiles contain no RID-specific targets. A normal locked restore followed by host-native publish without another restore passed dependency resolution. The local ILLink task host then failed at ComputeManagedAssemblies with MSB4216. The executor denied the Unix socket used by MSBuild named pipes. No native binary was produced. Ordinary CLI unit tests cannot close this gate.

## Component links and Platform feature evidence

Applied the central Markdown link checker to each component README and docs Markdown, excluding archive, adr, reviews and roadmap files. It found 65 broken link or fragment occurrences in 48 files scanned across eight repositories. The narrow repairs touched 18 files. The same scan returned zero errors after the edits. Relocated references were checked against the corresponding central file. Historical phase references resolve to the imported plan. Active priorities resolve to the consolidated roadmap. External URL availability and semantic review of all prose remain separate.

| Component | Documentation correction |
|---|---|
| Agent | [e2aac89](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/commit/e2aac89dafc2f8499e4e4d22ebed97cec75714fe) |
| LocalStream | [222d654](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/222d654c15d5d32b5606fc8a11b874b472ea7995) |
| LogCluster | [f17c749](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/commit/f17c749b80d5cdba05745ffaa249f90ac404ddfe) |
| Platform | [4c5aafc](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb) |

The Ubuntu [TRX artifact](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/45621349535/artifacts/15024013310) contains 1,338 individual passed outcomes. Matching these results to source at e89755e shows where application evidence is stronger than a suite-level green check.

| Scope | Executed evidence | Boundary |
|---|---|---|
| C17, Agent API | All 15 AgentApiEndpointTests passed, including enroll → heartbeat → policy pull → ACK, command delivery/result audit, another agent’s command and bundle rejection, missing/unknown credentials, expired bootstrap token and credential rotation. | Real loopback HTTP server with SQLite and fake observation sinks. The client is a test HttpClient. Production daemon TLS, cross-tenant isolation, signed metadata and rollout recovery require separate evidence. |
| C16, shared query execution | Three QueryServiceExecutionContractTests passed. Interactive and dashboard requests selected their intended purpose and recorded history. Diagnostic results recorded a failure summary. | The fixture substitutes the executor and history repository. Production backend admission and execution remain open. |
| C16, rule validation | Six QuerySyntaxCheckTests and eight QueryExecutionDryRunCheckTests passed. | These results cover the fixtures’ configured validation paths. |
| C16, incident and evidence storage | Nine IncidentCandidateRepositoryTests and six CandidateEvidenceRepositoryTests passed. | Repository operations alone cannot demonstrate operator triage, enrichment or suppression workflows. |

## Follow-up verification — 25 November 2026

The current branch references and workflow job conclusions were independently retrieved again. Platform run 45621349535 and LogCluster run 45621203831 passed all restore, lock verification, build and test steps on all three hosts. Subsequent default-branch changes are documentation changes for LogCluster and LocalStream, not changes to the tested mining or streaming source. Current docs revision feada2f5 passed [governance run 45638022344](https://github.com/DeltaZulu-OU/docs/actions/runs/45638022344), including governance tests, generated index, maintained links, governed repository checkout and Gold inventory checks.

[Agent run 45637110180](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/actions/runs/45637110180) at e2aac89dafc2f8499e4e4d22ebed97cec75714fe passed restore/build/test on all three hosts. Job logs report 335 application tests plus three fuzz-regression tests on Ubuntu; Windows and macOS each report 334 application tests passed, one skipped, plus three fuzz-regression tests. Windows skipped EnsureFifo_CreatesLinuxNamedPipe. The workflow installs 10.0.x without a global.json pin, defines the DeltaZulu feed at runtime and invokes locked restore, but no lockfiles are tracked. The current run does not establish the exact dependency hashes or SDK selection. Capture generated locks, SDK diagnostics and effective sources from a clean restore before enforcing the graph. Do not change package versions as part of lock capture.

The existing engineering branches remain unmerged: LocalStream build/track-portable-restore-graph (197a083) is one commit ahead and one documentation commit behind main; DurableBuffer build/track-portable-restore-graph (e677fd3) is one ahead and zero behind master; LogCluster fix/miner-record-count-boundaries (91e2013) is one ahead and one documentation commit behind master. The inspected unit-test workflows have manual dispatch but no feature-branch push trigger. No application-test Actions run for these branch revisions was found in the retrieved histories. Their earlier local Linux verification is retained; three-host branch CI and pack verification remain open. Do not dispatch the publication workflows for validation: they can publish packages and LocalStream can create a release tag.

Direct Git-tree inspection confirms seven differing core source blobs between LocalStream's published tag target ce7d95a3 and current main 222d654. The published source lacks the newer Key and EventTimeUtc properties in AppendOptions and StreamRecord<T>, and the corresponding optional key and eventTimeUtc fields in RecordEnvelope. Thus source-level compatibility with existing Agent usage does not prove the published package provides the newer event-time metadata contract. Verify old/new persistence and consumer behavior, then select a new release identity; do not downgrade or reuse 1.0.0. The GitHub compare endpoint reported no common ancestor for the release commit and current main; the two trees were inspected directly instead. DurableBuffer's current master and publication revision 5574911 have identical src/ blobs; their compare shows only documentation and release workflow/script changes. This strengthens source lineage but is not a binary hash or independent restore proof. Historical publish jobs succeeded, with no retained package artifact available through the retrieved artifact listings.

Agent restore/build logs on all hosts also report NU1902 for transitive MessagePack 3.1.8 ([GHSA-qhrr-8q5h-9q3h](https://github.com/advisories/GHSA-qhrr-8q5h-9q3h), CVE-2026-92707; patched in 3.1.9). Forward master Directory.Packages.props declares 3.1.8. Current ForwardMessagePackOptions registers ForwardObjectFormatter before ContractlessStandardResolver and selects UntrustedData; its custom array/map decoder checks depth before constructing containers. The advisory specifically concerns PrimitiveObjectFormatter; product reachability is not demonstrated by the dependency warning alone, nor is the published Forward binary verified by current source. Verify published resolver paths, update to a compatible patched dependency in a separate scoped change, and run existing typed wire and malformed-payload tests. Track the dependency under C14 and retain C03 wire-compatibility requirements.

The present GitHub connection exposes read access to workflow jobs and artifacts but no manual-dispatch action or authenticated NuGet binary retrieval. The local executor has no .NET SDK. Fresh cross-platform branch runs, independent binary restore and explicit-RID Native AOT execution were not performed in this follow-up. No application source, feature branch, package version, release tag or Decision was changed.
