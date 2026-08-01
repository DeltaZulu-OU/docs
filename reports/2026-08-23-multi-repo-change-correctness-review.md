# Correctness review of the 2026-08-17-dated multi-repo change

Date: 2026-08-23. Self-review of the session's work across `DeltaZulu.Platform`
(commits `430afc8`..`c0e204e`, of which `ebd70e0` and `c0e204e` are this
session's) and `docs` (`1f9a981`..`d5c7030`). Written the same way prior
verification passes in this repository were: re-executed rather than recalled,
and refuted claims are recorded rather than quietly corrected.

## Method

Re-ran the full Platform test suite at current HEAD rather than trusting the
count reported when each commit landed. Wrote and executed small throwaway
probes against real DuckDB connections for two claims that had not actually
been exercised by a test, rather than reasoning about them from the source.
Wrote a script that parses every Decision's front-matter status and diffs it
against every row in `GOVERNING-DECISIONS.md`, rather than re-reading the table
by eye. Cross-checked two specific section citations in `DEC-0011`'s narrowing
against the actual text of the imported DQM document.

## Platform — `DeltaZulu.Platform`

**Suite: 1338/1338 passing at current HEAD, build clean, no `error` or
`CS8509`.** Re-run fresh for this review, not assumed from the earlier report.

### Confirmed correct, with evidence

**Native `UUID` reads round-trip correctly through the shared reader.** This
was not covered by any test I wrote or found. `DuckDbValueReader.ReadValue`
routes a `UUID` column through `RequiresStringNormalization`, which matches on
`GetDataTypeName(ordinal)` uppercased. DuckDB.NET reports that name as `"Uuid"`
(title case, not `"UUID"`), which the existing `.ToUpperInvariant()` call
absorbs correctly. The underlying CLR value is `System.Guid`, which the
formattable fallback renders as `"123e4567-e89b-12d3-a456-426614174000"` —
correct. Verified by executing a real query against a real in-memory
connection rather than inspecting the code path. **This path had zero test
coverage before this review**; see Findings.

**Only one production call site constructs `DuckDBConnection`.** Grepped the
full `src/` tree. `DuckDbConnectionFactory.cs` is the sole constructor, and the
one production caller (`AnalyticsWebModuleServiceCollectionExtensions.cs`)
passes `attachedDatabases:` but not `startupSql:`, so it takes the default
array — including the new `SET TimeZone='UTC';`. The pin has full production
coverage; there is no second connection path it fails to reach.

**The `Utc` canonicalisation hazard is specific to text casting, not typed
parameter binding.** Checked because two test call sites pass
`startupSql: []`, which bypasses the pin. `AlertLakeWriterTests` binds a typed
`DateTime(..., DateTimeKind.Utc)` through Dapper — that goes through the
driver's native parameter binding, never through `CAST(text AS TIMESTAMPTZ)`,
so the offsetless-text-in-session-timezone hazard this session fixed does not
reach it. `DuckDbConnectionFactoryTests`'s bypass runs `SELECT 1` — no exposure
either. Both are still worth naming as gaps in defence-in-depth (see Findings),
but neither is a live defect, and neither is something this session's changes
introduced — both predate it.

**`DEC-0011`'s narrowing cites real DQM text.** Re-read §5.7 and §6.3 of
`architecture/DATA-QUALITY-MONITORING.md` against the report's own claims:
`golden.rows_projected` at §5.7 is described exactly as "emitted identically
by both engines; equivalence depends on it," and §6.3's "Cross-engine
divergence rate" is defined as "rows differing between the DuckLake and Proton
Golden projections of the same fixture, including null and reason equality" —
which is the DuckLake-vs-Proton metric, not the separate "Golden
reproducibility" metric in the same table (Bronze replayed and compared to
stored Golden). The report picked the right one; a wrong pick would have been
easy here since both metrics sit in the same row group.

**`GOVERNING-DECISIONS.md` matches every Decision's front-matter, exactly.**
A script parsed all 31 Decision files' declared status and diffed it against
every row in the index: zero mismatches, and no Decision missing from the
index. This checks the whole file, not only the rows this session touched.

**`DEC-0022`'s claim about the collector project is still true.** Re-read
`src/DeltaZulu.Platform.Ingestion/DeltaZulu.Platform.Ingestion.csproj`: no
`OutputType` is set, so it builds as a library, confirming the status note's
claim that no standalone executable exists yet for `governs:` to name.

**`KustoType`'s two `_ => throw` switches were genuinely left alone**, matching
what was told to the user. Re-read the file: `ToKustoName` and
`ToDefaultDuckDbType` both retain their fallthrough default. Only the `Guid`
arm of `ToDefaultDuckDbType` was touched (`Varchar` → `Uuid`), consistent with
the new registry mapping.

### Findings

**1. Test coverage gap: native `UUID` read-back through `DuckDbValueReader` was
unverified.** Manually confirmed correct in this review (above), but no
permanent test asserts it. `DuckDbValueReaderTests` covers `INET` but not
`UUID`. Recommend adding the equivalent test; not added here since it is a code
change and this pass is a review.

**2. Test coverage gap: `KustoType.Guid.ToDefaultDuckDbType()` has no
assertion.** `SchemaModelContractTests` exercises `String`, `Dynamic`, and
`Timespan` through this method but not `Guid`. The function has no production
consumer (established earlier in the session), so this is a latent gap rather
than a live risk, but the `Varchar` → `Uuid` change itself is currently
unverified by any test.

**3. Design note, not a bug: `ParserCanonicalizer.ToDuckDbExpression`'s
two-argument overload accepts a raw string and interpolates it directly into
SQL.** Both current callers are safe — validated, pattern-checked column names
from `ToDuckDbExpression(LogicalFieldDef)`, or literal test fixtures — but the
API shape itself does not enforce that. A future caller passing an
unvalidated, data-derived string would have a SQL-construction hazard the type
system does not prevent. Worth a doc comment at minimum if this becomes a
public surface consumed outside this file.

**4. Minor: `DuckDbConnectionFactory`'s two `startupSql: []` bypass sites
receive neither the `inet` extension nor the `UTC` pin.** Confirmed neither
currently touches a code path that needs them (above). Recorded so a future
change to either test does not silently reintroduce the hazard the pin exists
to close.

**5. Style: `architecture/README.md`'s new row uses a plain hyphen between two
Decision references** (`` `DEC-0026`-`DEC-0031` ``) where the same file's
existing convention for a Decision range uses an en dash (`DEC-0001`–`DEC-0021`,
two lines above). Cosmetic only.

## `docs`

### The governance-date defect

**Every date this session wrote into `docs` says 17 August 2026. The actual
session date is 23 August 2026 — six days later.** This is the review's
headline finding, and it is real: not a judgment call, a plain factual error,
made and repeated across seven files rather than caught once and fixed.

Affected: `reports/2026-08-17-platform-11-1-and-feed-recheck.md` (filename and
body), `reports/README.md`'s index row for it, `architecture/NRT-PIPELINE.md`'s
"Agreed 17 August 2026" line, `architecture/README.md`'s row for it, and the
"accepted"/"narrowed" status-note dates in `DEC-0022`, `DEC-0023`, and
`DEC-0011`.

The dates in documents this session only *read* — the 15/16 August entries
already in `docs` before this session began — are correct; they describe when
earlier sessions actually ran. The defect is confined to what this session
*wrote*.

**This matters more here than a typo normally would, and the estate's own
material says why.** `reports/README.md` states reports are "dated and not
rewritten: a later check that reaches a different conclusion is a later
report" — the date is load-bearing for establishing sequence, not decoration.
`DEC-0022` and `DEC-0011`'s status notes use their dates to place *when* the
acceptance or narrowing happened relative to the Decisions that motivated it
(`DEC-0027`, `DEC-0031`). And this is, structurally, the same category of
mistake `DEC-0029` exists to prevent one layer down — a timestamp attached to a
record that does not reflect when the record was actually produced. Getting it
wrong in governance documents about a pipeline whose central discipline is
"declare the type, never infer it; get the timestamp right" is the kind of
detail worth being exact about rather than dismissing as cosmetic.

**Not fixed in this review.** Correcting seven already-pushed files changes
governance-record content on a shared branch, which this review treats as a
decision for you rather than something to do silently while reviewing. Two
honest options: overwrite the wrong dates with the correct ones now, in a
dated correction commit that says why (git history keeps the old commits
regardless, so nothing is hidden); or leave them and add a note where the
dates appear, similar to how `2026-08-16-schema-divergence-verification.md`
records its own earlier wrong verdict in place rather than silently editing it.
I'd default to the first — a wrong "dated" field is worse than a corrected one,
and there's no finding here worth preserving in its wrong form — but it's your
governance record.

### Everything else checked

**`governs-check --collect` still reports 5 governed repositories with no
warnings**, re-run at current HEAD.

**No stale references were introduced.** `architecture/NRT-PIPELINE.md` never
asserts `DEC-0022`'s or `DEC-0011`'s status directly — it names "the collector"
generically — so accepting `DEC-0022` and narrowing `DEC-0011` afterward left
nothing in that document contradicted.

**The index audit above covers `docs` too** — `GOVERNING-DECISIONS.md` was
generated from and checked against all 31 Decisions, not only the six-plus-two
this session touched, and every row matches.

## Overall verdict

The functional content — the code changes in Platform, and the substance of
the Decisions in `docs` — held up under re-execution and re-reading. Nothing
found required reverting. Two real gaps in test coverage, one design note worth
a comment, one cosmetic dash, and one real, systematic, low-risk defect: the
date on everything this session wrote is wrong by six days, in a repository
where dates are part of the record's meaning rather than metadata.
