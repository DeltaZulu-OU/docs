# Session 1 — Pre-flight report (Kusto.Language 9.2.0 vs 12.4.1)

Date: 2026-08-15. Environment: clean cloud container, .NET SDK 10.0.110, nuget.org reachable.
Method: two throwaway projects, identical `Program.cs`, bracket-pinned to `[9.2.0]` and `[12.4.1]`.
Nothing was fixed; one user-level NuGet source was added for a feed test and removed afterwards.

## Verdict: the stop condition FIRED — items (2) and (3) differ between versions

The differences are two, both narrow. Whether they sink the span assumption is a design call,
not a fact call — see "Assessment" at the end.

---

## Item 1 — Four API members, both versions: CONFIRMED

The same source file compiles and runs against both versions. Reflection dumps are
byte-identical across versions:

| Member | Shape (identical in 9.2.0 and 12.4.1) |
|---|---|
| `ScalarTypes.All` | public static field, `IReadOnlyList<ScalarSymbol>` |
| `ScalarTypes.GetSymbol` | public static method, `ScalarSymbol (string)` |
| `ScalarSymbol.From` | public static method, `ScalarSymbol (string)` |
| `ScalarSymbol.IsWiderThan` | public instance method, `bool (ScalarSymbol)` |

## Item 2 — Alias tables: DIFFER (one alias)

Identical in both versions for the required seven types, except `real`:

| Type | 9.2.0 aliases | 12.4.1 aliases |
|---|---|---|
| `bool` | boolean | boolean |
| `datetime` | date | date |
| `guid` | uniqueid, uuid | uniqueid, uuid |
| `int` | int16, int32, int8, uint, uint16, uint32, uint8 | (same) |
| `long` | int64, uint64, ulong | (same) |
| `real` | double, float, **single** | double, float |
| `timespan` | time | time |

- `ulong`/`uint64` → `long`: CONFIRMED in both (via both `From` and `GetSymbol`).
- Behavioral consequence: `From("single")`/`GetSymbol("single")` returns `real` in 9.2.0
  and **null** in 12.4.1. Every other probed spelling resolves identically in both.

## Item 3 — `ScalarTypes.All` membership: DIFFERS (one member)

| | 9.2.0 | 12.4.1 |
|---|---|---|
| Count | **11** | **12** |
| Members | bool, datetime, decimal, dynamic, guid, int, long, real, string, timespan, type | same **plus `null`** |
| `type` in All | yes | yes |
| `null` in All | **no** | yes |
| `unknown` in All | no | no |
| `ScalarTypes.Null` static | **absent** | present |
| `ScalarTypes.Unknown` static | present (not in All) | present (not in All) |

Note for Session 6: CON-0003 as drafted ("twelve including `Type` and `Null`") is true of
12.4.1 only. In 9.2.0 the list is eleven and `ScalarTypes.Null` does not exist.

Widening lattice (`IsWiderThan`, full pairwise) — IDENTICAL in both versions:
`decimal > int`, `decimal > long`, `decimal > real`, `long > int`, `real > int`,
`real > long`, `string > dynamic`. `null` (12.4.1) participates in no relation.

## Item 4 — Agent's Rx.Kql resolution: CONFIRMED 9.2.0

An isolated project referencing only `Microsoft.Rx.Kql [3.5.3]` resolves
`Microsoft.Azure.Kusto.Language` **9.2.0** transitively. In the Agent itself,
`Microsoft.Rx.Kql` 3.5.3 is referenced by `DeltaZulu.Agent.Filter` only; no Agent project
references Kusto.Language directly, and none of Parse/Forward/LogCluster/LocalStream/
DurableBuffer source trees reference Kusto at all — so 9.2.0 is the Agent-process
resolution. (Full in-repo `dotnet list package` was blocked by the feed problem in item 7.)

Incidental finding: Rx.Kql 3.5.3 also drags in `Newtonsoft.Json` 10.0.3
(known **high** vulnerability GHSA-5crp-9r3c-p9vr) and `System.Drawing.Common` 4.7.0
(known **critical** GHSA-rxg9-xrhp-64gj) transitively.

## Item 5 — Platform's 12.4.1 reference: CONFIRMED, but the pin is a minimum

`Directory.Packages.props` line 27: `Version="12.4.1"` — a plain minimum, **not** the
`[12.4.1]` exact pin the plan calls for. Consumers: direct `PackageReference` in
`DeltaZulu.Platform.Domain` and `DeltaZulu.Platform.Application` (Analytics/Translation
uses `Kusto.Language.Syntax`/`Symbols` heavily); tests exercise it too.

## Item 6 — nuget.org availability: CONFIRMED

Both 9.2.0 (catalog 2021-04-26) and 12.4.1 (catalog 2026-07-21) are `listed: true`,
no deprecation, no vulnerability records. Both bracket-pinned restores succeeded.

## Item 7 — `deltazulu-github` restore from a clean container: REFUTED

- From a clean checkout, `dotnet restore` of the Agent fails: NU1100 for every
  `DeltaZulu.*` package. The Agent's own `NuGet.config` maps `DeltaZulu.*` to
  `deltazulu-github` but defines **no `<packageSources>` section at all** — the same
  defect class as Platform's gap 2, present in **Agent, Platform, and Parse alike**.
- The instruction's claim that Parse's config "is correct" is REFUTED as far as the
  committed file goes: Parse works only because its CI (`publish.yml`) creates a temp
  config and runs `dotnet nuget add source` with `GITHUB_TOKEN` at run time. That
  run-time-injection pattern is the actual working reference.
- With the source added manually in this container, the feed answers **401 Unauthorized**:
  this session's GitHub App installation token has no `read:packages` grant, and no PAT is
  present in the environment. A PAT-based verification has to happen where the PAT lives.

## Assessment (for the revisit the stop condition demands)

Both deltas are narrow and characterized:

1. The planned `DeltaZulu.Kql` surface is "All minus `Type`, `Null`". Filtering **by name**
   yields the identical 10-member set on both versions — the `null` membership delta
   vanishes behind the planned surface, provided the filter tolerates `Null` being absent.
2. The `single` alias is the only divergent spelling. If `DeltaZulu.Kql.FromName` delegates
   blindly, `FromName("single")` gives `real` in the Agent process and `null` in the
   Platform process. The surface must take an explicit position on `single`
   (reject in both, or map in both) rather than inherit the divergence.

Raw probe outputs preserved: `kusto-preflight/out920.txt`, `kusto-preflight/out1241.txt`
(scratchpad), diff-clean except the lines quoted above.
