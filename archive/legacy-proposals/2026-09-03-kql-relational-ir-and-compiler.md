---
id: DEC-0032
status: Proposed
repos: [DeltaZulu.Kql, DeltaZulu.Platform]
governs:
  types:
    DeltaZulu.Kql: [DeltaZulu.Kql.Relational.RelNode, DeltaZulu.Kql.Relational.ScalarExpr, DeltaZulu.Kql.Compilation.KqlRelationalCompiler, DeltaZulu.Kql.Compilation.IKqlSchemaCatalog]
    DeltaZulu.Platform: [DeltaZulu.Platform.Domain.Analytics.Catalog.ApprovedViewCatalogSchemaAdapter, DeltaZulu.Platform.Domain.Analytics.Policy.KqlDiagnosticAdapter]
  paths:
    DeltaZulu.Kql: [src/DeltaZulu.Kql/Relational/RelNode.cs, src/DeltaZulu.Kql/Compilation/KqlRelationalCompiler.cs, src/DeltaZulu.Kql/Compilation/IKqlSchemaCatalog.cs]
    DeltaZulu.Platform: [src/DeltaZulu.Platform.Domain/Analytics/Catalog/ApprovedViewCatalogSchemaAdapter.cs, src/DeltaZulu.Platform.Domain/Analytics/Policy/KqlDiagnosticAdapter.cs]
cites: [CON-0002, CON-0006, CON-0021]
---

# DEC-0032 — The KQL relational IR and KQL→RelNode compiler are owned by `DeltaZulu.Kql`, not `DeltaZulu.Platform`

## Context

`DeltaZulu.Platform` grew its own `RelNode`/`ScalarExpr` relational IR and a
KQL→RelNode translator (`Application.Analytics.Translation`) as an internal
implementation detail of its DuckDB and Proton SQL emitters. Neither the IR
nor the translator depended on anything Platform-specific: the IR had zero
non-BCL dependencies, and the translator's only Platform couplings were three
members of an approved-table catalog and one diagnostics-accumulation method
(`CON-0002` — Kusto.Language itself carries no CLR type mapping, so this
boundary was always the estate's to own, not Kusto's). `DeltaZulu.LocalStream`
needs exactly this IR and must not take on a dependency on `DeltaZulu.Platform`
to get it.

**Archived Platform ADR 0002 states "Translation uses a controlled relational
model before emitting backend SQL" as a Platform-owned mechanism, and archived
Platform ADR 0016 states "Backend-neutral relational emission lives at the
application/domain boundary" — both asserting the relational model and
translator belong to Platform's own Application/Domain layer. Both premises
are retired by this Decision.** The archive is frozen and cannot carry the
correction; it is recorded here and in `decisions/README.md`.

## Decision

`DeltaZulu.Kql` owns the relational IR (`DeltaZulu.Kql.Relational.RelNode`/
`ScalarExpr` and supporting types — scan/filter/project/extend/aggregate/sort/
limit/sample/distinct/join/let-binding nodes; column/literal/binary/unary/
function-call/case/window scalars) and the KQL-to-relational compiler
(`DeltaZulu.Kql.Compilation.KqlRelationalCompiler.Compile(string,
IKqlSchemaCatalog) -> KqlCompilationResult`). `DeltaZulu.Platform` consumes
that IR through a package reference and keeps everything backend-specific:
the DuckDB and Proton SQL emitters, the relational planner, `QueryRuntime`,
and detection deployment. `IKqlSchemaCatalog` is a narrow, backend-neutral
schema contract (table existence, column names/types) that says nothing about
approval policy; `DeltaZulu.Platform`'s `ApprovedViewCatalog` — which does own
medallion/approval policy — reaches the compiler through
`ApprovedViewCatalogSchemaAdapter`, a thin adapter, not a copy.

Dependency direction: `Microsoft.Azure.Kusto.Language` → `DeltaZulu.Kql` →
`DeltaZulu.Platform`, never the reverse. **Platform ADR 0002's
relational-model-as-Platform-mechanism framing and ADR 0016's
application/domain-boundary placement are both retired**; the relational IR
and its compiler are `DeltaZulu.Kql`'s, not Platform's, going forward.

`DeltaZulu.Platform.Application.Analytics.Translation.KustoQueryCompiler` and
`KustoToRelational` remain as public compatibility facades — their existing
call sites (`NrtRuleCompiler`, `ScheduledDetectionService`, `LanguageService`,
`KqlQuerySyntaxValidator`, `QueryRuntime.DataOnly`) needed no change — but
carry no independent translation logic; both delegate to
`KqlRelationalCompiler`. Platform's own `RelNode.cs` and the eight internal
translator files it previously owned are deleted, not duplicated.

## Consequences

- One canonical KQL→RelNode implementation serves `DeltaZulu.Platform`,
  `DeltaZulu.LocalStream` (not yet integrated), and future tooling, instead of
  each maintaining its own.
- `CON-0006`'s version-span discipline now extends past the type contract
  (`KqlTypes`) to a KQL parser/translator, which is a materially larger
  Kusto.Language surface. `CON-0021` was found and closed as part of this
  move: comparing `Kusto.Language.Syntax.SyntaxKind` by enum value rather than
  by name silently breaks across the version span in exactly the way `CON-0006`
  warns about, and no amount of same-repo conformance testing catches it — only
  a real cross-repo consumption test (packing `DeltaZulu.Kql` and running
  `DeltaZulu.Platform`'s suite against it) surfaced it. Any future
  Kusto.Language-facing code added to `DeltaZulu.Kql` must be verified the same
  way, not just compiled against both versions.
- Two diagnostic message wordings changed as part of the move, deliberately:
  the unapproved-table message no longer says "golden.\*"/"hunting view"
  (medallion-specific wording a shared package must not own), and a
  hash-function argument-validation message no longer names DuckDB
  specifically. No test in either repository asserted the exact prior wording.
- A pre-existing bug — join-related diagnostics in the translator pass a
  string code into the `detail` parameter position rather than `code`, so
  `KqlDiagnostic.Code` stays `"GEN000"` for them — was carried over unfixed
  rather than silently corrected during the move, per the estate's practice of
  not combining extraction with unrelated fixes.
- `IKqlSchemaCatalog.KqlColumnSchema` carries a column's type as a plain KQL
  type name (`string`), not a Kusto.Language `ScalarSymbol` — confirmed
  necessary, not merely preferred, by a real `CS0012` compiling Platform's
  adapter against a locally packed `DeltaZulu.Kql` build: `ScalarSymbol`-typed
  public members carry the compiling assembly's exact Kusto.Language version
  identity in their metadata, which a consumer pinned to a different exact
  version cannot resolve at compile time. `KqlTypes.FromName` recovers a
  `ScalarSymbol` from the name only where a single Kusto.Language version is
  already fixed (inside `DeltaZulu.Kql`, or inside one consumer).

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Keep `RelNode` typed with `ScalarSymbol`/Kusto.Language syntax types | A consumer pinned to a different exact Kusto.Language version than `DeltaZulu.Kql`'s compile floor cannot resolve those types at compile time (`CS0012`, confirmed) | `CON-0006` |
| Split the translator into a separate `DeltaZulu.Kql.Compiler` package compiled against a higher Kusto.Language floor | Unnecessary: a throwaway probe confirmed the full translator's C# API surface compiles identically against `[9.2.0]` and `[12.4.1]`; the real incompatibility found (`CON-0021`) is an enum-value bug fixable in place, not an API-surface gap requiring a version floor increase | `CON-0006` |
| Have `DeltaZulu.Kql` depend on `DeltaZulu.Platform`'s `ApprovedViewCatalog` directly | Reverses the intended dependency direction and couples the shared compiler to Platform's medallion policy | — |
| Fix the join-diagnostic `code`/`detail` bug while moving the code | Changes observable diagnostic output during a move meant to be behavior-preserving; the estate's stated practice is not to combine extraction with unrelated fixes | — |

## Revisit trigger

When the `DeltaZulu.Kql` and `DeltaZulu.Platform` branches implementing this
move merge to their default branches, this Decision's status should move to
`Accepted` (currently `Proposed`: `governs-check` checks out default branches,
and the governed paths exist only on feature branches as of this writing).
Also revisit if `DeltaZulu.LocalStream` integration reveals the `RelNode` IR
needs a shape `DeltaZulu.Platform`'s emitters did not exercise.
