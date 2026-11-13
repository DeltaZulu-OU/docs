# Roadmap

This roadmap tracks planned work for making DeltaZulu.LogCluster a maintainable parser-suggestion component while preserving the mining core as a reusable LogCluster implementation.

## Status

* **P0 — done.** `DeltaZulu.Parse` exposes the public `ILiblognormParserCatalog` / `LiblognormParserCatalog.Instance` catalog API described below.
* **P1 — done.** `DeltaZulu.Suggester` references `DeltaZulu.Parse` (NuGet package) and `LiblognormSuggestionEngine` is now a thin adapter over `LiblognormParserCatalog.Instance`. The local `LiblognormMotifs` shim has been removed and regression tests prove suggestions come from Parse metadata and full-match validation.
* **P2–P4** remain open.

## Prioritized phases

| Priority | Phase | Goal | Suggested changes | Exit criteria |
| --- | --- | --- | --- | --- |
| P0 (done) | Parse parser catalog contract | Make `DeltaZulu.Parse` the canonical source for liblognorm parser names, priorities, and whole-sample validators. | Add a public `ILiblognormParserCatalog` in `DeltaZulu.Parse` that exposes parser descriptors, `WordParserName`, `RestParserName`, lookup by parser name, and `IsFullMatch` validation. Keep parser IDs, parser delegates, `Npb`, dispatch details, and extraction internals private. | `DeltaZulu.Parse` publishes or otherwise exposes a consumable catalog API that the suggester can reference without duplicating parser syntax. |
| P1 (done) | Suggester catalog integration | Replace the local motif shim with an adapter over the Parse catalog. | Add `DeltaZulu.Parse` as a project/package reference to `DeltaZulu.Suggester`; update `LiblognormSuggestionEngine` to use `LiblognormParserCatalog.Instance`; remove duplicated regex/IP/date checks once Parse validators cover the supported motifs. | `DeltaZulu.Suggester` no longer defines canonical parser names or validator logic locally; tests prove suggestions come from Parse metadata and full-match validation. |
| P2 | Rule-rendering hardening | Use shared parser metadata consistently while keeping LogCluster mining independent. | Keep `DeltaZulu.LogCluster` dependent only on `IGapSuggestionEngine`; preserve conservative handling for unresolved internal gaps; add regression coverage for fallback-only `rest` and sample-inferable parser selection. | Core mining code remains parser-package agnostic, and rule rendering behavior is covered by tests for specific parsers, fallback parsers, and unresolved gaps. |
| P3 | Packaging and repository workflow | Make the cross-repository dependency repeatable for development and CI. | Package reference to `DeltaZulu.Parse` is in place via `Directory.Packages.props` and `NuGet.config`. Keep restore/build instructions current for package consumers. | A clean checkout can restore, build, and test with the Parse-backed suggester in CI and local development. |
| P4 | Expanded parser suggestions | Broaden supported parser suggestions after the catalog integration is stable. | Review `DeltaZulu.Parse` parser descriptors for additional sample-inferable motifs such as structured parsers; add confidence tests and user-facing warnings for ambiguous motifs. | New parser suggestions are data-driven from the catalog, have regression tests, and preserve human-reviewable output. |

## Proposed Parse catalog shape

The suggester needs a metadata-only public surface from `DeltaZulu.Parse`. It does not need access to `Npb`, parser delegates, field extraction, parser IDs, or PDAG internals.

```csharp
namespace DeltaZulu.Parse;

public enum LiblognormParserSuggestionUse
{
    None,
    InferFromSample,
    FallbackOnly,
}

public sealed record LiblognormParserDescriptor(
    string Name,
    int Priority,
    LiblognormParserSuggestionUse SuggestionUse,
    bool RequiresConfiguration)
{
    public bool CanInferFromSample => SuggestionUse == LiblognormParserSuggestionUse.InferFromSample;

    public bool CanRenderWithoutConfiguration => !RequiresConfiguration;
}

public interface ILiblognormParserCatalog
{
    IReadOnlyList<LiblognormParserDescriptor> Parsers { get; }

    string WordParserName { get; }

    string RestParserName { get; }

    bool TryGetParser(string name, out LiblognormParserDescriptor parser);

    bool IsFullMatch(string parserName, ReadOnlySpan<char> sample);
}
```

`DeltaZulu.Parse` can implement this as a thin public adapter over its internal parser table. `InferFromSample` identifies parsers the suggester may infer from observed gap samples, while `FallbackOnly` covers renderable fallback motifs such as `rest` that should not win sample-based recognition.

---

## Corrections applied on migration (2026-08-16)

**`LiblognormParserDescriptor` does not exist and will not.** This roadmap
proposes that type and an interface exposing
`IReadOnlyList<LiblognormParserDescriptor>` / `TryGetParser`. `DeltaZulu.Parse`
shipped **`ParserDescriptor`** instead, in `ParserCatalog.cs`. Any work planned
against the proposed name must be re-read against the shipped one.

**Counter widths remain a live defect.** `MaxRecords` and
`TokenizedRecord.Stream` are `long`, while `DiscoverFrequentWords`,
`MiningResult.RecordCount`, `MiningResult.OutlierCount`,
`PatternCandidate.Support`, `GapStatistics.Observations` and
`CandidateScorer.Score` are `int`. Above `int.MaxValue` they wrap, and
`Math.Log(1 + recordCount)` then yields `NaN`. Widening them is scheduled work,
not a proposal.

**Motif removals are more expensive than they look.** Any plan to drop
`v2-iptables` or `cisco-interface-spec` should know that the committed parity
corpus covers them with 15 and 5 cases respectively — 20 cases of upstream
coverage forfeited. An earlier count that read only the JSON rulebase syntax
reported 1 and 0, which made the removal look nearly free.

---

## Corrections applied on 2026-11-13

**Shipped defaults versus the mining core.** The frequent-anchor pipeline remains reusable, but the shipped merge defaults differ from unmodified Perl `logcluster.pl`. Upstream `--aggrsup` and `--wweight` are opt-in. The roadmap must not equate the algorithmic lineage with default-output parity.

**P3 is a release gate and remains open.** The repository's ignored `packages.lock.json` files meant `dotnet restore --locked-mode` did not enforce a committed resolution; see `reports/2026-08-15-platform-ci-restore.md`. `DeltaZulu.Suggester` directly references `DeltaZulu.Parse` 0.1.1, making the undefined `deltazulu-github` source an active defect. A fix branch defines the feed and removes the ignore rule, but lock files, feed authentication, and clean-clone verification remain outstanding.

**Counter-width inconsistency is not resolved.** `MaxRecords` is `long`, but record, support, outlier, observation and some scoring counts remain `int`. This is P5.5, not a completed fix.

## Updated execution order and exit criteria

P0 and P1 remain done. The existing P2, P3 and P4 identities are preserved. Execution order is **P3 → P5 → P2 → P6 → P7 → P8 → P4 → P9**. Each row below is one independently reviewable change (one PR if PRs are later requested); the current development instruction is to use branches without opening PRs.

| Order | Phase | ID | Change | Exit criterion | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | P3 | P3.1 | Authenticate GitHub Packages feed in the CI workflow using `packages: read` and a token | Clean checkout resolves the Parse 0.1.1 package on the CI matrix | Workflow token injection committed on branch; package permission and restore unverified |
| 1 | P3 | P3.2 | Track and commit every `packages.lock.json` | Locked restore succeeds on the pinned graph and rejects deliberately stale locks | Ignore rule removed on branch; lock files pending |
| 1 | P3 | P3.3 | Document feed URL, token scope, and bootstrap in `docs/DEVELOPMENT.md` | Developer instructions produce a successful authenticated restore | Instructions committed; clean-clone validation pending |
| 1 | P3 | P3.4 | Correct README link to centralized roadmap | Link resolves to `DeltaZulu-OU/docs/roadmaps/DeltaZulu.LogCluster-ROADMAP.md` | Implemented on P3 branch; verification pending |
| 2 | P5 | P5.1 | Skip stale template merge groups | Six previously crashing corpus runs complete | Fix branch committed; tests not executed |
| 2 | P5 | P5.2 | Exclude merge targets from subsequent variant groups | Support conservation across all corpus cases | Fix branch committed; tests not executed |
| 2 | P5 | P5.3 | Bound passes 2–3 to pass-1 record count; treat newly encountered tokens as infrequent | Growing source does not throw; strategies agree for stable input | Fix branch committed; tests not executed |
| 2 | P5 | P5.4 | Count candidate support independently of `SequenceNumber` | Zero and duplicate sequence values count once per input record | Fix branch committed; tests not executed |
| 2 | P5 | P5.5 | Widen record, support, outlier, observation and scoring counts to `long` | Overflow tests, API compatibility review and corpus invariants pass | Pending |
| 3 | P2 | P2.1 | Record leading and trailing separators for each populated gap independently | Differing separators are represented without silently collapsing them | Pending |
| 3 | P2 | P2.2 | Emit Parse-supported `%-:whitespace%` for variable-width separators | Candidate's contributing records parse in supported Parse version | Pending |
| 3 | P2 | P2.3 | Preserve trailing whitespace through matching, without silently trimming source records | Trailing-space and tab cases round-trip; any `%-:rest%` fallback validated | Pending |
| 3 | P2 | P2.4 | Preserve separator adjacent to optional gaps | `login *{0,1}` renders with its required space | Pending |
| 3 | P2 | P2.5 | Prevent clock-time samples being classified as `ipv6` | Time and IPv6 counterexamples validated against Parse catalog | Pending |
| 3 | P2 | P2.6 | Preserve existing fallback warnings and executable parser-name validation | No invalid parser name; unresolved gaps are marked non-executable | Existing tests; extend corpus |
| 3 | P2 | P2.7 | Execute every marked-executable rule against its contributing records through Parse 0.1.1 | Every executable candidate parses at least `Support` contributing lines, with no false executable flags | Pending; observed failures are release-blocking |
| 4 | P6 | P6.1 | Add merge switch: `none`, `edge`, `variants`, `all` | `none` gives a no-merge baseline without silently changing defaults | Pending |
| 4 | P6 | P6.2 | Pin Perl `logcluster.pl` commit and compare expected pattern/support/outlier data | Exact no-merge parity for versioned inputs; expected outputs only committed | Pending |
| 4 | P6 | P6.3 | File reproducible verification report under `reports/` | Command lines, inputs, comparator, exact counts and failures documented | Preliminary register exists; verification pending |
| 5 | P7 | P7.1 | Compare every merge mode against licensed Loghub ground truth | Reproducible accuracy metrics, including false merges and splits | Pending |
| 5 | P7 | P7.2 | Accept `DEC-0032` after evidence selects default, diversity and edge criteria | Accepted Decision names governing code that exists and quantitative revisit triggers | Proposed; default unchanged |
| 5 | P7 | P7.3 | Implement accepted low-diversity and edge semantics | `up`/`down` and `login`/`login failed` remain distinct; recurring IPs can merge | Pending Decision |
| 6 | P8 | P8.1 | Add BenchmarkDotNet baseline with allocation diagnostics for both strategies | Representative repeatable measurements | Pending |
| 6 | P8 | P8.2 | Share separator strings between token records | Allocation decrease exceeds measurement variance | Pending |
| 6 | P8 | P8.3 | Avoid merge index when merging is disabled | Peak memory improvement shown at support 2 | Pending |
| 6 | P8 | P8.4 | Revisit `ShouldStream` default using measured data | Strategy choice justified by baseline; current default unchanged meanwhile | Pending |
| 7 | P4 | P4 | Preserve broader parser catalog suggestions and ambiguity warnings | Existing P4 exit criterion unchanged | Pending |
| 8 | P9 | P9.1 | Relative support | Named requester and upstream parity test | On demand |
| 8 | P9 | P9.2 | Configurable `--separator` | Named requester and upstream parity test | On demand |
| 8 | P9 | P9.3 | Word classes counted once per line, as in LogClusterC | Named requester and upstream parity test | On demand |

## Evidence and release gates

The supplied upstream findings are 7,039 of 7,039 clusters matching after custom merges were removed, approximately 86% with one merge off, and 34% at defaults. In 48 corpus runs the original code reportedly crashed six times and over-counted support 13 times. These are user-supplied measurements, not independently reproduced CI results.

The new rule-rendering findings report **341 failures among 1,740 suggested rules (19.6%)**, involving **7,260 of 43,514 contributing log lines (16.7%)**. These are two different denominators; do not treat line failures as an additional count of failed rules or infer that every affected line was itself parsed incorrectly. Reproduce the findings with the published Parse 0.1.1 package, since the earlier run used Parse built from `main`. A rule is accepted as executable only when it parses all of its own contributing lines, not merely a sampled subset.

P3 is the CI verification prerequisite. P5 and P2 are **both release gates**, including packaging-only releases. P6 and P7 follow once mining and rendering are correct; the proposed merge Decision must cite exact parity and accuracy evidence. P8 optimizations follow correctness. The earlier 4.1s/203 MB streaming and 5.1s/570 MB materialized measurements were single runs and are not benchmark evidence.

For reproducibility, retain the exact upstream commit and command flags; compare `(pattern, support)` pairs and outlier counts without conflating score ordering with parity. Fetch Loghub data at runtime only where its license permits, and do not commit source samples to this AGPL repository without redistribution clearance. Consult `CON-0012` as the existing governance precedent.

## Proposed policy decisions

**Default merge mode:** Keep existing behavior until `DEC-0032` is Accepted; evaluate `none` as the baseline rather than preemptively changing the default. **Trailing whitespace:** preserve source text, then model exact or variable terminal separators through executable Parse rules; `%-:rest%` must not be assumed safe without a round-trip test. **Release readiness:** both P5 and P2 block the next release. No decision is made here on a new default or on replacing the low-diversity and edge heuristics.

Next review remains 2026-11-16, or earlier when verified evidence or code contradicts the roadmap.

---

## Review trigger

**Next review: 2026-11-16.** Migrated to `DeltaZulu-OU/docs` on 2026-08-16 from
its origin repository, which no longer carries a copy.

Review earlier than the date above if any of these happen:

- a Decision this roadmap depends on changes status in `decisions/`;
- a phase named here completes, or is found to have been overtaken;
- a claim in it is contradicted by the code, as several already were.

A roadmap with no review date becomes an archaeological artefact that still reads
as a commitment. That is what this section exists to prevent.
