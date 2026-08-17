# Section 11.1 divergences — verified against the code

Date: 2026-08-16. Session 13. Written as a verification pass, then extended after
two narrow Platform fixes were applied — see "Corrections applied" below.

**One verdict in this report was itself wrong and is corrected in place: item 6.**
Attempting to write a test for it showed the fault was unreachable. That is
recorded rather than quietly edited, because a verification report that hides its
own corrections is worth less than one that shows them.

`architecture/PIPELINE.md` §11.1 lists thirteen "known divergences, all open" in
`LogicalSchemaRegistry` and its projection, and gap 9 rates the set P1 at
"weeks". Before collapsing the two schema authorities on top of that list, each
item was checked against `DeltaZulu.Platform` at `b1c0222`.

## Headline: most of the list is refuted. Fixing it as written would mean changing correct code.

**Eight of thirteen** are wrong against current code — seven found on the first
pass and one more (item 6) found when a test was written to reproduce it. Two are
confirmed. One is confirmed but inherent rather than a defect. Two are partial.

**And the one defect that matters most is not on the list at all**:
`ILogicalSchemaRegistry` has no implementation anywhere under `src/` (recorded in
`DEC-0012`). The registry is not a second authority with no consumers; it is an
interface with no production implementation. That is why these divergences could
persist unobserved — for the most part, nothing executes the code path they
describe.

Gap 9's "weeks" estimate should be revisited downward on this evidence.

## Item by item

| # | §11.1 claim | Verdict |
|---|---|---|
| 1 | No floating-point logical family; wire tag 2 has no destination | **REFUTED** |
| 2 | Duration ticks versus microseconds | **CONFIRMED, and worse** |
| 3 | Timestamp fidelity — DuckDB `TIMESTAMP` carries no offset | **CONFIRMED (inherent)** |
| 4 | Proton timestamp regression — projection emits bare `datetime64` | **REFUTED** |
| 5 | Split decimal truth — `Double` plus a `DECIMAL(p,s)` override | **REFUTED as written** |
| 6 | Unmapped families throw an opaque *sequence contains no matching element* | **REFUTED on re-test** — unreachable |
| 7 | `ToKustoType`'s `_ => KustoType.String` default | **REFUTED — never existed** |
| 8 | `Uuid`/`IpAddress` diverge between DuckDB `VARCHAR` and Proton `uuid`/`ipv6` | **CONFIRMED** |
| 9 | Projection filters on `SourcePath` rather than `Promoted` | **REFUTED as written** |
| 10 | Dynamic bag unimplemented; silent field loss | **CONFIRMED** |
| 11 | `ParserCanonicalization` unenforced | **PARTIAL** |
| 12 | Boolean lexemes lack declared polarity | **REFUTED** |
| 13 | `ToSilverTable` drops `ProducerFamily` and `Version`, so families collide | **REFUTED** |

### 1 — Refuted

`LogicalFieldFamily` has a `FloatingPoint` member. `ToDuckDbType` maps it to
`DuckDbType.Double` and `ToKustoType` to `KustoType.Real`. Wire tag 2 has a
destination.

### 2 — Confirmed, and worse than stated

`LogicalSchemaRegistry.Duration(...)` defaults to
`LogicalDurationUnit.Microseconds`, and `BuiltInLogicalSchemas` uses that default
for `SessionDuration`. Confirmed.

The stronger finding: `LogicalDurationUnit` has exactly three members —
`Milliseconds`, `Microseconds`, `Nanoseconds`. **There is no `Ticks`.** CON-0014
fixes the canonical unit at ticks (100 ns), and the registry's enum cannot
express it at all. This is not a wrong default to flip; it is a missing member,
and adding it changes a contract enum plus both backend mappings. That is
Decision work, not a repair, which is why nothing was changed here.

### 3 — Confirmed, inherent

DuckDB `TIMESTAMP` is microsecond precision with no offset. `TIMESTAMP_NS` is
selected for nanosecond fields, so the precision half is handled; the offset half
is not a defect but a consequence of CON-0001 — KQL `datetime` is UTC-only, so
there is no offset to preserve. Worth removing from the divergence list rather
than fixing.

### 4 — Refuted

The registry emits
`datetime64(3|6|9, 'UTC')`, chosen from `LogicalTimestampPrecision`, and
`ProtonType` independently emits `datetime64({digits}, 'UTC')`. Neither drops
precision, and neither drops the UTC timezone.

### 5 — Refuted as written

`LogicalFieldType.Decimal(precision, scale)` emits `DECIMAL(p,s)` for DuckDB,
`decimal(p,s)` for Proton, and `KustoType.Decimal` for KQL. No `Double` anywhere
on the decimal path.

There is a weaker version of the concern that survives: `ColumnDef` carries both
the coarse `DuckDbType` enum and the precise `duck.TypeName` string, so a
consumer reading the enum gets `Decimal` without precision or scale. That is a
loss of *parameters*, not the split truth about the *type* the item describes.

### 6 — Refuted on re-test. **This corrects an earlier verdict in this same report.**

The first pass recorded this as "confirmed, wrong location", having found
`Single(m => m.Target == target)` in `LogicalSchemaProjection.Mapping` and
reasoned that it would throw *"Sequence contains no matching element"*.

Attempting to reach it proved otherwise. `LogicalSchemaValidator.ValidateField`
already requires exactly one mapping per target:

```csharp
foreach (var target in Enum.GetValues<RegistryProjectionTarget>())
    if (type.BackendMappings.Count(m => m.Target == target) != 1)
        throw new ArgumentException($"Field '{field.Name}' must have exactly one {target} mapping.");
```

Every public entry point — `ToSilverTable`, `ToAgentSink` — calls `Validate`
first, so a missing mapping is rejected with a message naming both the field and
the target, and `Single` is never reached. A test written to trigger the opaque
error instead caught the clear one.

`Mapping` was still given a named error, but as **defence in depth** for a future
path that skips validation, not as a fix for a live fault. Recording the
distinction because "we fixed an opaque error" and "the opaque error was
unreachable" are different claims, and only the second is true.

The family switches (`ToDuckDbType`, `ToKustoType`) do throw, with clear messages
naming the family — and have been made exhaustive, see below.

### 7 — Refuted, and it never existed

Neither `ToKustoType` overload has a `_ => KustoType.String` default. The
family-based one throws `ArgumentOutOfRangeException`; the string-based one in
`ProtonType.cs` also throws. `git log -S"_ => KustoType.String" --all` returns
nothing, so this was never in the repository's history.

This item is quoted in the correction set as *"the exact coercion D3 forbids, and
exactly the fallthrough arm the estate rule bans"* — a vivid example that turns
out to describe code that does not exist.

A narrower version of the estate-rule concern does apply: these switches use
`_ => throw` over closed DeltaZulu enums. A throwing default is far safer than a
coercing one, but it still defers to runtime what exhaustive listing would catch
at compile time (CS8509). Worth tightening; not a coercion.

### 8 — Confirmed

`ToDuckDbType` maps both `Uuid` and `IpAddress` to `DuckDbType.Varchar`, while
Proton uses `uuid` and `ipv6`. Equality, ordering and comparison semantics
therefore differ per engine for the same logical field, and DuckDB has native
`UUID` and `INET` types available. This is a genuine cross-engine divergence and
it is exactly the class `DEC-0011`'s equivalence test would catch.

### 9 — Refuted as written

`ToSilverTable` filters on `f.Parser?.Placement == ParserFieldPlacement.TopLevel`.
It filters on neither `SourcePath` nor a `Promoted` flag — no `Promoted` property
exists on `LogicalFieldDef` at all.

### 10 — Confirmed

`ToSilverTable` selects only `TopLevel` fields, and emits no bag column.
`DynamicBag` fields are therefore absent from the Silver table and present in no
bag: absence from the table is not presence in the bag. `ParserFieldContract`
validates that a `DynamicBag` placement carries a path and that `TopLevel` does
not, so the *declaration* is checked while the *routing* is unimplemented —
silent field loss, as described.

### 11 — Partial

`ParserCanonicalization` is declared (`None`, `Utc`, `MacLowerColon`,
`Ipv6Compressed`) and used in `BuiltInLogicalSchemas`, and the validator enforces
consistency — `Utc` is rejected on a non-`Timestamp` family. What is missing is
anything that *performs* the canonicalisation. So it is validated but not
applied, which is narrower than "ships as an enum with no integration".

### 12 — Refuted

`public sealed record BooleanLexemePair(string False, string True)`. Polarity is
declared by name, not positionally, and the validator rejects lexemes on a
non-`Boolean` family. The item describes an ordered `["true","false"]` list that
is not how this is modelled.

### 13 — Refuted

```csharp
new InternalTableDef("silver", $"{schema.ProducerFamily}_{schema.SchemaName}_v{schema.Version}", ...)
```

All three components are in the table name. Families do not collide and version
migration is not an in-place change.

## What Session 13 should actually do

The real work is smaller and different from the list:

1. **Implement `ILogicalSchemaRegistry`, or delete it.** One authority means one
   *implemented* authority. Everything else here is downstream of that choice,
   and it is a `DEC-0012` question rather than a bug fix.
2. **Add `Ticks` to `LogicalDurationUnit`** and map it in both backends, per
   CON-0014. Contract change — needs a Decision.
3. **Resolve `Uuid`/`IpAddress` cross-engine divergence** toward DuckDB's native
   `UUID`/`INET`.
4. **Implement dynamic-bag routing**, or reject `DynamicBag` placement at
   validation until it exists, so the loss is loud.
5. **Apply `ParserCanonicalization`** at projection or parse time.
6. Replace `Single` with a lookup that names the type and target when a backend
   mapping is missing.
7. Make the closed-enum switches exhaustive rather than `_ => throw`.

Items 1 and 2 are Decisions. Items 3–7 are ordinary work, and none of them is
weeks.

## Corrections applied to Platform after this verification

Two changes, both narrow, both verified against the full suite (1319 passing):

- **The closed-enum fallthroughs are gone.** `ToDuckDbType` and `ToKustoType`
  used `_ => throw` over `LogicalFieldFamily`. `Binary`, `Array` and `Map` are now
  listed as explicit rejections and the default arm is removed, so adding an enum
  member is a compile-time gap (CS8509) rather than a runtime surprise on
  whichever record first uses it. They are not given invented mappings, because
  choosing their physical types is a contract decision.
- **`Mapping` names the type and target** on a missing or duplicated backend
  mapping. Defence in depth, per item 6 above.

A characterisation test now pins the **dynamic-bag silent loss**, which item 10
confirmed and which turns out to be live in a shipped built-in schema:
`CefFirewallV1` declares `AgentBuild` with `DynamicBag` placement, `ToSilverTable`
emits only `TopLevel` fields, and no bag column exists — so that field is in no
column and no bag. The test asserts the current wrong behaviour deliberately, so
the defect is executable rather than described, and fixing it becomes an act that
updates a failing assertion rather than a silent behaviour change.

`DynamicBag` was **not** made a validation error, even though that would make the
loss loud, because a shipped built-in schema uses it and rejecting it would break
that schema rather than fix the routing.

## A refuted claim about the test suite

`PIPELINE.md` rates Platform testing at 55% with "a broad suite that is not
green", and gap 19 attributes that to a DuckDB `inet` extension download
returning HTTP 403. **Measured 2026-08-16: the suite is green, 1317 of 1317
passing** before these changes and 1319 of 1319 after. Whatever the 403 was, it
is not failing the suite now.

## Method note

Every verdict above came from reading the code at `b1c0222`, and the `_ =>
KustoType.String` verdict additionally from searching the full history. The
pattern across Wave 0 and Wave 1 now has three instances — the CI restore claim,
the version-pin claim, and this list — where a documented defect did not survive
contact with the source. Verifying before fixing is earning its cost.
