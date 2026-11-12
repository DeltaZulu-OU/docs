# DeltaZulu.LogCluster roadmap

Updated 2026-11-13. Governing roadmap for the miner, the Parse-backed suggestion layer, and packaging. Each numbered change is a separately reviewable work item and, if submitted for review, one PR. Development may use branches without opening PRs.

## Principle and ordering

Correctness and baseline parity precede changing merge semantics. Rendering and parser round trips follow the merge Decision. Measure allocation and performance before changing the streaming default. Upstream option parity is demand-driven rather than a release gate.

Current implementation branches are stacked, **not merged into master**. Branch status means implementation committed, not CI-verified. The pinned Perl reference fixtures and corpus-derived accuracy report are not yet complete.

## Work items

| Order | ID | Work item | Exit criterion | Status |
| --- | --- | --- | --- | --- |
| 0 | 0.1 | Correct clean restore: locked restore without tracked locks; remove package mapping to undefined source | Clean clone restores/builds/tests on CI matrix | Implemented on `fix/0-1-clean-restore`; unverified |
| 0 | 0.2 | Generate expected pattern/support pairs using pinned `logcluster.pl` commit, default upstream heuristics off; commit expected outputs only | Integration test matches fixture pairs 100% with no merge | Pending; use synthetic input unless redistribution rights verified |
| 0 | 0.3 | Corpus invariants: no exceptions, support plus outliers equals records, strategy parity | Corpus tests fail on pre-fix master and pass after fixes | Tests committed on `test/0-3-mining-invariants`; execution pending |
| 1 | 1.1 | Skip stale template-group keys | All previously crashing cases complete | Implemented on `fix/1-1-stale-merge-groups`; unverified |
| 1 | 1.2 | Prevent reuse of a merge target in subsequent groups | Support conservation across corpus | Implemented on `fix/1-2-merge-target-reuse`; unverified |
| 1 | 1.3 | Cap passes 2–3 to pass-1 record count, treat new tokens as infrequent | Growing source does not throw | Implemented on `fix/1-3-growing-stream`; unverified |
| 1 | 1.4 | Count support per record rather than sequence number | Zero/duplicate sequence numbers counted | Implemented on `fix/1-4-support-sequence`; unverified |
| 2 | 2.1 | Expose merge mode: none, edge, variants, all | None reaches 100% on upstream no-merge fixtures | Pending |
| 2 | 2.2 | Compare all modes to Loghub ground truth | Accuracy report under `reports/`, with licensing review | Pending |
| 2 | 2.3 | Decide default merge mode, following 2.2 | Governing Decision filed in `DeltaZulu-OU/docs/decisions` | Pending; no default changed |
| 2 | 2.4 | Tighten low-diversity merging | `up`/`down` remain separate; recurring IPs still merge | Pending; choose >=3 distinct, motif gate, or per-candidate word dependency through a Decision |
| 2 | 2.5 | Constrain edge merging | `login` and `login failed` remain separate | Pending; decide support-retaining upstream behavior or gap-range restriction |
| 3 | 3.1 | Pick gap separator using observations with non-empty gaps | `login *{0,1}` retains its space | Pending |
| 3 | 3.2 | Execute rendered rules with DeltaZulu.Parse against contributing lines | Every marked-executable rule round-trips | Pending; acceptance gate for parser suggestions |
| 4 | 4.1 | BenchmarkDotNet baseline, memory diagnostics | Both strategies characterized on representative inputs | Pending |
| 4 | 4.2 | Reuse separator strings | Allocation improvement exceeds run variance | Pending |
| 4 | 4.3 | Review `ShouldStream` default | Decision supported by benchmarks | Pending; retain existing heuristic |
| 4 | 4.4 | Avoid merge index with mode none; filter singletons before sorting | Peak memory improves at support 2 | Pending |
| 4 | 4.5 | Optional word sketch before dictionary | Introduce only with a demonstrated memory-constrained corpus | Deferred |
| 5 | 5.1 | Relative support and configurable separator | Implement only if requested | On demand |
| 5 | 5.2 | Word classes | If implemented, count each class once per record as LogClusterC does | On demand |
| 5 | 5.3 | Full aggregate-support merging and dump files | User demand and tests justify complexity | On demand |
| 6 | 6.1 | Correct README roadmap link and comparison claims | Link points here; opt-in upstream behavior and sourced parity figures documented | Pending |

## Existing Parse integration and release work

| Previous ID | Description | Current interpretation | Status |
| --- | --- | --- | --- |
| P0 | Public Parse parser catalog | Implemented as `ParserDescriptor` and `ParserCatalog`, not old proposed `LiblognormParserDescriptor` | Done |
| P1 | Suggester uses Parse catalog instead of local motif shim | Integrated through NuGet package and adapter | Done |
| P2 | Parser rendering validation and warnings | Fold into 3.1–3.2, preserving `IGapSuggestionEngine` separation | Partially covered, needs 3.2 |
| P3 | Packaging, clean restore, development workflow | 0.1 must be validated before packaging or release | Open |
| P4 | Expanded parser motifs | Demand-driven, after verified round trips | Deferred |

## Additional previously recorded defect

Counter widths are inconsistent: input limits use `long`, but several support, outlier, record, observation and scoring counters use `int`. Plan a distinct counter-width fix before lifting practical corpus limits toward `int.MaxValue`; do not silently change public API types without compatibility review.

## Evidence and decision constraints

Keep Loghub samples out of this AGPL repository until their redistribution rights are established. Synthetic inputs and committed upstream-generated expected outputs are acceptable. Pin the upstream Perl commit and record command-line flags, environment and normalization used to generate fixtures. Compare sets of (pattern, support), rather than score ordering, because ranking differs intentionally.

For 2.3, report precision/recall or clustering accuracy per merge mode before selecting a default. No Decision is recorded yet. For 4.3, the previous 4.1s/203 MB streaming versus 5.1s/570 MB materialized measurements are a single-run hypothesis, not a baseline.

When running the latest stacked branch, include the Linux, macOS and Windows CI matrix and at least one representative production-day corpus whose redistribution is allowed. Confirm that the parity tests actually fail against the initial master before marking this track complete.

## Decision references and review

ADRs, Decisions, architecture and central roadmaps live in `DeltaZulu-OU/docs` per `CLAUDE.md`. No merge-default Decision is yet authorised without 2.2. Next review: 2026-11-16, or sooner after CI evidence or an upstream compatibility change.
