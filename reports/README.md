# Reports

Verification output. Constraints cite these; Decisions cite Constraints.

A report records what was checked, how, and what the check returned — including
when the answer refuted the premise that motivated the check. Reports are dated
and are not rewritten: a later check that reaches a different conclusion is a
later report.

| Date | Report | Outcome |
|---|---|---|
| 2026-08-15 | `2026-08-15-kusto-language-preflight.md` | Kusto.Language 9.2.0 vs 12.4.1. Four API members identical; `ScalarTypes.All` membership and the `single` alias differ. Both deltas absorbable. Raw probe output alongside. |
| 2026-08-15 | `2026-08-15-platform-ci-restore.md` | Locked-mode restore was a silent no-op, not a failure. `deltazulu-github` undefined in Agent, Platform and Parse alike. |
| 2026-08-15 | `2026-08-15-version-pin-reconciliation.md` | Agent's 1.0.0 pins match published reality. LocalStream's source has since declared 0.1.0, below its published version. |
| 2026-08-15 | `2026-08-15-golden-placement.md` | Section 9 decision memo. Option A recommended, C as fallback, B ruled out. `DEC-0011` stays Proposed until the CI equivalence test exists. |
| 2026-08-16 | `2026-08-16-collector-ownership.md` | Collector belongs in `DeltaZulu.Platform` as its own deployable. Recorded as `DEC-0022`. Flags the existing `RawLogNdjsonCodec` boundary. |
| 2026-08-16 | `2026-08-16-package-publishing-blocked.md` | `dotnet nuget push` returns 401: the session token has no `packages` scope. Blocks FWD-CONTRACT-v2 items 3–11 and Parse commits B/D. Publish workflow added to `DeltaZulu.Kql`. |
| 2026-08-16 | `2026-08-16-schema-divergence-verification.md` | Section 11.1 verified against code: seven of thirteen divergences refuted, two confirmed, `_ => KustoType.String` never existed. Gap 9's "weeks" estimate should come down. |
| 2026-08-16 | `2026-08-16-session-handoff.md` | State of all nine branches, the `packages:read` permission a continuing session must ask for, what is done, what is next, and the claims that did not survive contact with the source. |
| 2026-08-17 | `2026-08-17-platform-11-1-and-feed-recheck.md` | Feed still 401; an endpoint split isolates it to a missing `packages` permission rather than a bad token, a proxy fault or a NuGet misconfiguration. §11.1 items 8 and 11 closed: native `UUID`/`INET`, and `ParserCanonicalization` performed rather than only validated. DuckDB reads offsetless timestamps in the session timezone, so the session is now pinned to UTC. `DEC-0023` accepted. |
| 2026-08-23 | `2026-08-23-multi-repo-change-correctness-review.md` | Re-execution of the prior session's claims: suite re-run green, native `UUID` read-back verified live (previously untested), `DEC-0011`'s DQM citations checked against the imported text, the whole `GOVERNING-DECISIONS.md` index diffed against all 31 Decisions with zero mismatches. Headline finding: every date this session wrote is stamped 17 August, six days before the actual session date. |
| 2026-08-24 | `2026-08-24-forward-datetime-carrier.md` | `DeltaZulu.Forward` 0.3.1 normalizes every datetime field value to `DateTimeOffset` and treats `Kind = Unspecified` as UTC, contradicting `CON-0001` twice. A caller cannot comply by choosing `DateTime`: the library widens it. `FWD-CONTRACT-v1` §10 specifies the behaviour, so the fix is a versioned wire break and is left to a Decision. |
