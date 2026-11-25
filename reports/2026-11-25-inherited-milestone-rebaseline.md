# Inherited milestone rebaseline and cross-repository documentation verification — 2026-11-25

Scope: source inspection, existing exact-revision push-test workflow evidence, and documentation-only updates. No application builds/tests were independently executed. Code snapshots below precede the documentation-only commits. Do not substitute security/dependency scheduled workflow successes for application unit-test evidence.

## Source and test evidence

| Project | Source revision | Exact-revision push-test evidence |
|---|---|---|
| Agent | [32f8abc](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/tree/32f8abc824396c5f08cbcbade8045463bb2a4c3d) | [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/actions/runs/32734167156) |
| Platform | [60d6588](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f) | [Unit Tests failed](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/32734957185): restore failed on Ubuntu, Windows and macOS; build and test skipped. Job log endpoint returned HTTP 410; exact package error unavailable. |
| Forward | [fba0c5c](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/tree/fba0c5c63a1ee506373012ad458276ec807e542a) | [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/actions/runs/32734377941) |
| LogCluster | [881f0f1](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/tree/881f0f1b79b1e1cee72898cdada0bb69e39ffc76) | No push-test run returned for this exact revision. Existing fixtures and scheduled successes are not execution evidence. |
| Parse | [ad923dc](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/tree/ad923dc716fc7048c58b46628913a4484ad95cd2) | [Build/Test/Pack passed](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/actions/runs/32734807241); [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/actions/runs/32734807246) |
| Kql | [2f61c60](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/tree/2f61c60db6a5df28c8ead33cab8de105e086bb13) | [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/actions/runs/31962705813) |
| LocalStream | [16f27b4](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/tree/16f27b44fa16bcde6e9316662b25ac85ae0d4642) | [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/actions/runs/33553739275) |
| DurableBuffer | [3d20e94](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/tree/3d20e940ad32fcf553bea5efaee646b585f84625) | [Unit Tests passed](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/actions/runs/32734280201) |

## Inherited milestone disposition

This is dated supporting evidence, not a second active roadmap. Work-item IDs refer to the consolidated table; phase labels below refer to the historical imports.

| Roadmap / inherited milestone | Source/test observation | Disposition |
|---|---|---|
| C12 Agent phase 2 / 10 | TextInputRecord and StructuredInputRecord exist. ExecutionPlanCompiler groups physical-resource bindings; tests explicitly cover grouping, conflicting settings and disabled profiles. AgentRuntime still constructs ChannelOutputMultiplexer and the plan's full runtime activation is not established. | Planning primitives implemented; verify actual orchestration before closing phases. |
| C12 phases 2a, 3–8 | Syslog, auditd, Windows, ETW and KQL filter sources/tests exist; Parse contains PDAG, structured parser, catalog, syslog and rulebase tests. Source evidence does not prove all framing adapters, parse.query behavior, single-pass PDAG or post-Parse auditd assembly. | Partial; source-specific trace and parity remain. |
| C12 phases 9–13 | Pipeline project references LocalStream **and** DurableBuffer; runtime retains ChannelOutputMultiplexer (AgentRuntime.cs:111 at pinned revision). | Migration remains open; delivery/replay C05, pipeline ownership C12. |
| C12 phases 14–17, 19 | ProfileReloadSource, observability, checkpoints and integration fixtures exist. Compatibility Syslog/Auditd parsers remain. | Do not mark parser retirement, reload safety or performance gates complete without targeted tests/benchmarks. Phase 18 Proton sink retired by DEC-0033. |
| C13 M1–M3 | CLI Program rejects removed raw commands, dispatches --tui, --tail and --metrics; ProfileWorkbenchMode, TailMode and TUI classes exist. | Source implemented for these modes; usability and bounded live-tail acceptance still needs targeted execution. |
| C13 M4–M6 | SqliteMetricsStateWriter emits metrics best-effort, SqliteMetricsStateProvider reads read-only state and MetricsDashboardTui exists. | Implementation present; full dashboard/fault/metric coverage remains unverified. |
| C13 M7–M8 | ServiceControlCommand calls systemctl; explicitly rejects unsupported platforms. The inspected state path uses SQLite. | Systemctl service commands implemented; cross-platform controls and bounded local IPC remain unverified. Do not claim IPC from SQLite alone. |
| C14 Package versions and build | Agent pins Forward 0.3.1, LocalStream/DurableBuffer 1.0.0 and Parse 0.1.1. LocalStream build props declare 0.1.0; DurableBuffer build props lack explicit Version. Platform's exact-revision restore failed on all OS. Parse's build/pack succeeded. | Confirm feed/version provenance and restore error on fresh run before publication; no current registry access proof. |
| C15 historical P0/P1 | SuggestionEngine takes IParserCatalog and defaults to ParserCatalog.Instance; Suggester package references Parse 0.1.1; DefaultInstance_IsBackedByTheParseCatalog tests recognition/priority. | API migration source implemented. Exact-revision LogCluster test execution unavailable. |
| C15 historical P2 | Miner tests cover internal multiword gaps, unresolved warnings, trailing separators, streaming/materialized equivalence and fallback parser selection. | Source regression fixtures exist; run CI and parity corpus before closing. |
| C15 historical P3/P4 and counter width | Unit-test workflow specifies locked restore; default MaxRecords=5,000,000 (long), TokenizedRecord enforces caller-provided long maximum; miner DiscoverFrequentWords returns int RecordCount and scorer computes Math.Log(1 + recordCount). | Default bounds mitigate ordinary usage, but raised limits and int arithmetic still require explicit upper-bound/checked/widening tests. No verified overflow incident or full Perl parity claimed. |
| C16 phases 1–5 and 8–12 | Platform query executor, query validation fixtures, alert writer, incident repository, dashboards, governance validation and agent management classes/tests exist. | Source evidence, not completion proof; Platform restore failure blocks test-backed status. NRT and lake behavior remain C06/C07. Proton phases 3A/3C/6/7 cannot be retained as target work. |
| C17 control plane | Agent ControlPlaneClient requires HTTPS and implements enroll, heartbeat, bundle pull/ack and command-result endpoints. Platform has AgentCommandService, closed AgentCommandType and tests for auth/enrollment/policy/commands. | API/service primitives implemented. Verify daemon wiring, tenant ownership, replay/expiry, signing, rollback, and end-to-end behavior. No TUF conformance or production rollout proof. |

## Cross-repository documentation changes

All eight local documentation indexes previously linked the central docs `main` branch instead of its actual `master` branch, described historical PIPELINE.md as the estate pipeline, and some linked nonexistent archived repository directories. Each now links the current NRT target, governing index, single roadmap and valid archive destination. Removed stale version/build/status assertions from index pages; dated evidence remains available centrally.

| Project | Index commit | Architecture scope correction |
|---|---|---|
| Agent | [71e7aba](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/commit/71e7aba4f2e6cadeee8d2f86f1de565a250d4a60) | [069d26b](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/commit/069d26b7d1bac819538b275f6a9a492992f0cd3b) |
| Platform | [431f64f](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/431f64f4f91089f6345ecdeb88ff48f52be7a7c4) | [142ee62](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/142ee6262de10ebe6baa78227fd4f386ad9f5f9b) |
| Forward | [19b3d00](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/commit/19b3d000697922870742f52ba46e8b4fc3de3ee6) | Index only |
| LogCluster | [36c67b7](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/commit/36c67b7ac5585cc89bae0ca22cc261b32d055e4a) | Index only |
| Parse | [731b5b1](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/commit/731b5b1d77696e1eff9cf24c4e26561d31b7a93b) | Index only |
| Kql | [a94dda9](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/commit/a94dda9cfd87c950b4996cffdb33f3d4c980b485) | Index only |
| LocalStream | [baffc0e](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/baffc0eef972805dc1474682fc6af339aa8ce5d7) | [aeec9a5](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/commit/aeec9a53e1fde876739e3b014644b8e08cb00ae9) |
| DurableBuffer | [1fb8eca](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/commit/1fb8ecaaea402894f94ec84e7aa11aae8d7bf984) | Index only |

These are documentation-only commits; local architecture scope notes do not rewrite every historical passage. Additional component-specific references and remaining source/test verification belong to C08/C12–C17.

## ASIM and document validation

The [mapping baseline](../architecture/ASIM-GOLD-MAPPING-BASELINE.md) pins Microsoft's ASimTester.csv at b2c15c11d6666b9ddf80091663e6c8009058fbcb, with 686 merged family/field entries. This establishes exhaustive accounting of the selected tester rows, not exhaustive semantic conformance to every published ASIM field/condition. The CommonMark-based checker validates resolved reference links, inline links/images, local heading fragments and explicit anchors for maintained documents. Historical imports, external URLs, unresolved reference syntax rendered as text, and non-Markdown fragments are outside the check. Governance and CodeQL passed for central commit 45a5de2 before this report.

## Owner decisions

No Decision status, wire encoding, runtime or immutable Constraint changed. Pending decisions remain in the roadmap. P0/P1 engineering closure is not inferred from source presence or old CI. C14's immediate verification blocker is Platform restore failure; fresh logs are needed. C15 needs a current application test run. No new priority has been assigned to inherited work.
