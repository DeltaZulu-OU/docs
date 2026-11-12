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

P0 and P1 remain complete. P2, P3 and P4 retain their existing identities and historical design rationale. P3 moves first. Each numbered item should remain one independently reviewable change (one PR if PRs are later requested); no PRs are opened during this work.

| Order | Phase | Change | Exit criterion | Status |
| --- | --- | --- | --- | --- |
| 1 | P3.1 | Define authenticated `deltazulu-github` feed in `NuGet.config` | Clean clone restores Parse 0.1.1 on all CI runners | Feed defined on branch; authentication and verification pending |
| 1 | P3.2 | Track and commit `packages.lock.json` throughout solution | Locked restore succeeds for committed graph and fails on stale lock | Ignore removed on branch; generation pending |
| 1 | P3.3 | Correct README link to centralized roadmap | Link resolves to `DeltaZulu-OU/docs/roadmaps/DeltaZulu.LogCluster-ROADMAP.md` | Pending |
| 2 | P5.1 | Template-liveness guard for variant groups | Six previously crashing cases complete | Fix branch committed; execution pending |
| 2 | P5.2 | Prevent targets re-entering subsequent merge groups | Conservation holds across corpus | Fix branch committed; execution pending |
| 2 | P5.3 | Bound later stream passes and handle unknown tokens as infrequent | Growing source does not throw | Fix branch committed; execution pending |
| 2 | P5.4 | Remove sequence guard in support counting | Zero and repeated sequence numbers counted | Fix branch committed; execution pending |
| 2 | P5.5 | Widen record/support/outlier/observation/scoring counters | Consistently `long`, overflow and API regression tests pass | Pending |
| 3 | P6.1 | Add merge modes none, edge, variants, all | None matches unmerged upstream patterns/support | Pending; default unchanged |
| 3 | P6.2 | Pin Perl commit and compare expected patterns/support/outliers | 100% unmerged fixture parity; commit only expected outputs | Pending |
| 3 | P6.3 | File reproducible parity report under `reports/` | Source commit, flags, inputs, output counts and limitations published | Pending; preliminary figures supplied |
| 4 | P7.1 | Compare merge modes to Loghub ground-truth templates | Accuracy by mode, reproducible scripts, license compliance | Pending |
| 4 | P7.2 | Draft and accept DEC-0032 governing defaults, diversity and edge rule | Decision accepted on evidence, revisit threshold measurable | Proposed pending evidence |
| 4 | P7.3 | Implement chosen diversity and edge criteria | `up`/`down` and `login`/`login failed` remain distinct, recurring IPs can merge | Pending decision |
| 5 | P2.1 | Existing rule rendering and fallback-parser hardening | No false executable claims; engine remains package-agnostic | Open |
| 5 | P2.2 | Observe separators from non-empty gaps | `login *{0,1}` retains the separator | Pending |
| 5 | P2.3 | DeltaZulu.Parse executable-rule round trip | Every marked-executable rule parses its contributing lines | Pending |
| 6 | P8.1 | BenchmarkDotNet with memory diagnostics | Representative materialize and stream baseline | Pending |
| 6 | P8.2 | Reuse separator strings | Allocation drop exceeds run variance | Pending |
| 6 | P8.3 | Skip merge index when merging disabled; trim singletons before sort | Peak memory decreases at support 2 | Pending |
| 6 | P8.4 | Revisit ShouldStream default | Measurement-backed Decision; current heuristic retained meanwhile | Pending |
| 6 | P8.5 | Optional vocabulary sketch | Only if demonstrated memory pressure requires it | Deferred |
| 7 | P4 | Existing broader Parse catalog parser suggestions | Current P4 acceptance unchanged | Pending |
| 8 | P9 | Relative support, separator flag, line-counted word classes | Requester and parity test for each option | On demand |

## Evidence, licensing and dependency order

Initial, user-supplied comparison figures: 7,039/7,039 clusters without merging, approximately 86% with one merge disabled, approximately 34% at current defaults, and six crashes plus 13 support over-counts across 48 runs. These are **not independently reproduced or accepted**. Record the exact pinned Perl commit, input corpus, flags, comparator normalization, matching denominator, and per-mode results before treating them as release-quality evidence.

Do not commit Loghub datasets to the AGPL project without confirming redistribution rights. Fetch datasets at test runtime where permitted, or use synthetic samples. Consult `CON-0012` for the existing license precedent. The proposed Decision is `DEC-0032`; it must not be promoted to Accepted before the P6/P7 evidence exists.

P3 precedes any P5 CI acceptance, and P5 blocks releases until correctness is demonstrated. P6 precedes P7 so the Decision can cite objective parity and ground-truth accuracy. P2 follows merge semantics; P8 follows measured correctness. The single-run figures 4.1s/203MB and 5.1s/570MB do not establish a strategy default.

Next review remains 2026-11-16, or earlier when code or reproducible evidence contradicts the roadmap.

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
