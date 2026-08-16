# Section 11.1 divergences — verified against the code

Date: 2026-08-16. Session 13, first half. Verification only: **no Platform code
was changed.**

`architecture/PIPELINE.md` §11.1 lists thirteen "known divergences, all open" in
`LogicalSchemaRegistry` and its projection, and gap 9 rates the set P1 at
"weeks". Before collapsing the two schema authorities on top of that list, each
item was checked against `DeltaZulu.Platform` at `b1c0222`.

## Headline: most of the list is refuted. Fixing it as written would mean changing correct code.

Seven of thirteen are wrong against current code. Two are confirmed. Two are
confirmed but describe the wrong mechanism or location. Two are partial.

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
| 6 | Unmapped families throw an opaque *sequence contains no matching element* | **CONFIRMED, wrong location** |
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

### 6 — Confirmed, but not where the item says

The family switches (`ToDuckDbType`, `ToKustoType`) throw
`ArgumentOutOfRangeException` with a clear message naming the family. The opaque
error comes from `LogicalSchemaProjection.Mapping`:

```csharp
type.BackendMappings.Single(m => m.Target == target)
```

`Single` throws *"Sequence contains no matching element"* when a `LogicalFieldType`
lacks a mapping for the requested target. The symptom is real; the cause is a
missing backend mapping on a type, not an unmapped family.

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

## Method note

Every verdict above came from reading the code at `b1c0222`, and the `_ =>
KustoType.String` verdict additionally from searching the full history. The
pattern across Wave 0 and Wave 1 now has three instances — the CI restore claim,
the version-pin claim, and this list — where a documented defect did not survive
contact with the source. Verifying before fixing is earning its cost.
