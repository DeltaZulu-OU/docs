# Session handoff — continuing the DeltaZulu corrections

Date: 2026-08-16. Paste the block in §1 into a new session. Everything below it
is context that session can read from this repository once it starts.

---

## 1. The prompt

> Continue the DeltaZulu estate correction work. All nine repositories are clean
> and pushed; nothing is in flight.
>
> **Use the branch `claude/deltazulu-corrections-waves-l7ly9k` in every repository.
> Do not create new branches and do not push anywhere else.** It already exists on
> all nine remotes. `DeltaZulu.Kql`'s branch also carries a merge of `main`, so
> check it out rather than branching from `main`.
>
> Repositories: `DeltaZulu-OU/docs`, `DeltaZulu.Kql`, `DeltaZulu.Parse`,
> `DeltaZulu.Forward`, `DeltaZulu.LogCluster`, `DeltaZulu.LocalStream`,
> `DeltaZulu.DurableBuffer`, `DeltaZulu.Agent`, `DeltaZulu.Platform`. Attach all
> nine with push access.
>
> **First, before any other work, verify you can read the package feed:**
>
> ```
> dotnet restore   # in a project referencing DeltaZulu.Kql 1.1.0-preview.1
> ```
>
> from `https://nuget.pkg.github.com/DeltaZulu-OU/index.json`. The previous session
> could not — every attempt returned **401 Unauthorized**, because the GitHub App
> installation token carried no `packages` scope at all. A `packages:read` grant was
> requested and had not taken effect before that session ended; a session token is
> minted at session start, so a new session is the expected way to pick it up.
>
> **If the restore still returns 401, stop and ask me for the permission before
> starting any work that depends on it.** Do not commit code you cannot build and
> test — the blocked work touches a wire contract and a 197-test parser, and
> unverified changes there are worse than no changes. Ask, then take the unblocked
> work in §5 instead.
>
> Read `reports/2026-08-16-session-handoff.md` in `DeltaZulu-OU/docs` for full
> state, then `README.md`, `architecture/PIPELINE-ERRATA.md` and
> `architecture/DATA-QUALITY-MONITORING-INTEGRATION.md` in the same repository.
>
> Two standing decisions already made, which you should not relitigate:
> FWD-CONTRACT-v2 carries **all nine** provenance fields in one revision, not
> three; and the collector lives in `DeltaZulu.Platform` as its own deployable
> (`DEC-0022`).

---

## 2. Branch and state

Every repository is on `claude/deltazulu-corrections-waves-l7ly9k`, working tree
clean, local and remote identical:

| Repository | Head |
|---|---|
| `docs` | `d6a30b3e` |
| `DeltaZulu.Kql` | `26c3a6fd` |
| `DeltaZulu.Parse` | `f6317f3c` |
| `DeltaZulu.Forward` | `09c184fa` |
| `DeltaZulu.LogCluster` | `de0b619c` |
| `DeltaZulu.LocalStream` | `aad70d3d` |
| `DeltaZulu.DurableBuffer` | `071de55e` |
| `DeltaZulu.Platform` | `430afc84` |
| `DeltaZulu.Agent` | `1b6e4d1d` |

No pull requests have been opened. `DeltaZulu.Kql`'s branch contains a merge of
`main` (the released `1.1.0-preview.1` version bump), so branching afresh from
`main` would lose the session's work.

## 3. The permission to ask for

**What is needed:** `packages:read` for the Claude Code GitHub App installation on
`DeltaZulu-OU`, or a PAT with `read:packages` supplied as an environment variable
in the remote environment settings. Not pasted into chat.

**What it unblocks:** consuming `DeltaZulu.Kql 1.1.0-preview.1`, which gates

- FWD-CONTRACT-v2's two remaining items — retyping `Fields` as
  `IReadOnlyDictionary<string, KqlValue>` and resolving wire type names through
  `ScalarSymbol` with `FromName`, validated against `ClrCarrier`;
- Parse type-system commits **B** and **D**, where `ScalarSymbol` replaces
  `KqlType` on `ParserInfo`, on `SyslogEnvelope`, and in the rewritten fixtures.

**How to verify it landed:** restore any project referencing
`DeltaZulu.Kql 1.1.0-preview.1` against the org feed. Success means the grant is
live. A 401 means it is not, whatever the settings page says — the previous
session confirmed the App token also cannot *publish*, so the scope is absent in
both directions.

**Note:** the repository-level `GITHUB_TOKEN` inside a workflow *does* carry
`packages: write`, which is why `DeltaZulu.Kql` was releasable by
`workflow_dispatch` while the session itself could not push a package.

## 4. What was completed

Wave 0 in full, and most of Wave 1.

- **Session 0** — estate `CLAUDE.md` in all nine repositories.
- **Session 1** — Kusto.Language 9.2.0 vs 12.4.1 pre-flight. The stop condition
  fired on two narrow deltas, both absorbable and both handled in code.
- **Session 2** — Platform lock files committed, `deltazulu-github` source
  defined.
- **Session 3** — version-pin reconciliation.
- **Sessions 4, 6, 7** — the `docs` repository: constraints `CON-0001`–`CON-0020`,
  decisions `DEC-0001`–`DEC-0025`, archive of 54 ADRs, `governs-check` with a
  tested checker.
- **Session 5** — Golden placement memo. Option A, fallback C, B ruled out.
- **Session 8** — `DeltaZulu.Kql` built, 58 conformance tests against both
  Kusto.Language versions, released by the maintainer as `1.1.0-preview.1`.
- **Session 9** — liblognorm parity corpus extracted and committed, 384 cases
  pinned to a named upstream commit.
- **Session 10 (security half)** — `DepthStep` and collision-resistant hashing in
  `ForwardObjectFormatter`.
- **Session 10 (provenance half)** — all nine FWD-CONTRACT-v2 provenance fields on
  `ForwardLogRecord`, 73 tests.
- **Session 12** — collector ownership, `DEC-0022`.
- **Session 13** — §11.1 verified; two narrow Platform fixes; Platform suite
  1319 passing.
- **Session 19** — documentation consolidated into `docs`, per-repo
  `docs/README.md` and `CONTRIBUTING.md`, six roadmaps migrated with review
  triggers.
- **DQM rev. 2** imported with an integration companion.
- **Version guard** — a shared script in the four publishing repositories that
  refuses a version that does not move forward.

## 5. What to do next

**If the feed works**, in this order:

1. FWD-CONTRACT-v2's two remaining items (Forward).
2. Parse commits **A**–**D**. Note commit D's plan to drop the `v2-iptables` and
   `cisco-interface-spec` motifs costs **20 cases** of committed parity coverage —
   15 and 5 respectively — not the 1 an earlier undercount suggested. Decide
   deliberately.
3. Session 11's remaining items, then Session 14 onward.

**If the feed is still blocked**, ask for the permission, then take:

- Platform's confirmed §11.1 items — the `Uuid`/`IpAddress` cross-engine
  divergence toward DuckDB's native `UUID`/`INET`, and applying
  `ParserCanonicalization` at projection time.
- `DEC-0023` needs accepting before DQM wave 2a (canary emitter, reconciler,
  receiver-side inventory) is worth building against. That work has no
  dependencies on anything blocked.

## 6. Decisions already taken — do not relitigate

- **FWD-CONTRACT-v2 carries all nine provenance fields in one revision.** Landing
  three would mean a second contract revision on a contract with a compatibility
  window and a fleet to roll through.
- **The collector lives in `DeltaZulu.Platform` as its own deployable**, not
  inside the Blazor host. `DEC-0022`.
- **Golden placement is option A**, fallback C, B ruled out. `DEC-0011` stays
  `Proposed` until the CI equivalence test exists.
- **`DEC-0013`, `DEC-0021`, `DEC-0023`, `DEC-0024`, `DEC-0025` are `Proposed`**
  and genuinely open.

## 7. Things that will surprise you

**The written record runs ahead of the code in both directions.** Six documented
defects did not survive contact with the source, and two real ones were missing
from every document. Verify before fixing; it has paid for itself repeatedly.

Specifically refuted: `ToKustoType`'s `_ => KustoType.String` default **never
existed in the repository's history**; Platform's test suite **is green** (1319),
contrary to `PIPELINE.md` and gap 19; locked-mode restore was a **silent no-op**,
not a failure; Forward's "no fallback wire format" heading is **not empty**; the
LocalStream/DurableBuffer pins **match published reality**; eight of §11.1's
thirteen divergences are wrong.

Missing from every document: `ILogicalSchemaRegistry` has **no implementation
anywhere under `src/`**, and the Agent carries **two different ADR 0003
documents**.

**The version guard will fail LocalStream's next publish** until its declared
`0.1.0` is raised above the published `1.0.0`. That is the guard working on the
defect it was written for, not a regression.

**`DeltaZulu.Platform.Ingestion` already exists as a proto-collector** and
contains `RawLogNdjsonCodec` — the degraded format Forward's standing constraint
bans. Its only consumers today are a DuckDb seeding converter and tests, so it is
not a violation, but the boundary should be stated before the collector is built
beside it. `DEC-0022` records this.

**`CefFirewallV1` silently loses a field today.** It declares `AgentBuild` with
`DynamicBag` placement, `ToSilverTable` emits only `TopLevel` fields, and no bag
column exists. A characterisation test pins this deliberately; fixing it means
updating a failing assertion.

## 8. Working conventions this session followed

- Verify a claimed defect against the source before fixing it, and record
  refutations as findings rather than discarding them.
- Correct your own errors in place and say so — this report corrects one of its
  own verdicts, and `2026-08-16-schema-divergence-verification.md` corrects
  another.
- Run the tests. Every repository's suite was green at every push: Parse 197,
  Kql 58×2, Forward 73, Platform 1319.
- `governs-check` in `docs` must pass. It has caught two modelling errors in this
  work already.
- Commit messages explain *why*, and name what was measured rather than assumed.
