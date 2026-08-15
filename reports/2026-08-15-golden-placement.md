# Golden placement — decision memo

Date: 2026-08-15. Session 5. **This is a memo, not an implementation.** No code
was written and no compiler work was started.

Concerns section 9 of `architecture/PIPELINE.md`: whether lake Golden is derived
independently or mirrored from Proton. Recorded as gap 8, P1, "days to decide" —
and it gates the compiler target, so it must be decided before any compiler work
selects a shape by default.

## Recommendation: option A, with C held as the fallback. Rule out B regardless.

Recorded as `DEC-0011`, deliberately at status `Proposed` rather than `Accepted`.
The reason for that is the whole substance of this memo and is set out under
"The condition that makes A real" below.

## What is actually being decided

If Golden exists only in Proton, five things follow, and they compound:

1. Analysts hunt over Silver while detections evaluate Golden, so a saved hunting
   query cannot be promoted into detection content. The hunting-to-detection
   pivot is a product capability, not an implementation detail.
2. The Platform's own invariant — that analytics users query Golden views only —
   becomes unimplementable.
3. Investigating a fired alert cannot reproduce the Golden row that fired it,
   once the detection window has rolled.
4. Enrichment output is retained nowhere durable, so *materialise what you want
   to remember* has nothing to materialise into.
5. Field-level provenance would be computed in Proton and discarded with the
   window.

The fifth is the one that decides it. Provenance is the single property in this
design that cannot be retrofitted (DEC-0016). An arrangement in which it is
computed and then thrown away is not a latency trade-off; it is the permanent
loss of the thing the architecture exists to provide, arrived at by omission.

## The options

| Option | Shape | Assessment |
|---|---|---|
| **A. Dual-compiled** | Silver→Golden authored once in KQL, compiled to a DuckLake statement and a Proton materialised view | **Recommended.** Two emissions, one authoring |
| **B. Proton authors, lake mirrors** | Proton's Golden output written back to DuckLake | **Ruled out.** See below |
| **C. Separate .NET mapper** | A service reads Silver, writes Golden to both | **Fallback.** Costs a hop of detection latency |
| **D. Mapper plus Proton twin** | Mapper for the lake, compiled MV for the stream | Two implementations in two languages. Only if benchmarks force it |

### Why A

Golden as specified is overwhelmingly a **stateless per-record transformation**:
field renaming, type projection, enum retention, class assignment, tier and
null-reason stamping, observable extraction. The cross-record work — process
lineage, session identity — already happened on the endpoint, precisely because
it could not be reconstructed later (DEC-0007).

A stateless mapping does not need a streaming engine. And compiling it to both
dialects costs little, because the compiler already targets both dialects for
detection content. The marginal cost of A is therefore the equivalence test, not
the compiler.

### Why B is ruled out regardless

B makes the evidence lake downstream of the detection engine. That inverts the
durability ordering the entire design rests on: Bronze and Silver are evidence,
Proton is a detection engine with short-TTL staging (DEC-0010), and evidence must
not depend on the liveness of a component explicitly designed not to retain
anything.

Concretely, a Proton outage under B is a **permanent hole in the evidence lake**
unless Silver→Proton replay is guaranteed — and if that replay is guaranteed,
the mechanism that makes B survivable is the same mechanism that makes A work,
so B's claimed simplification has evaporated while its inversion remains.

This is a rule-out, not a ranking. It should not return in a later trade-off
discussion as "the simple option."

### Why C is the fallback rather than the recommendation

C's advantage is real and specific: sparse maps keyed by field name, closed
reason enumerations, and versioned tier-by-field matrix lookups are natural in
C# and awkward in ClickHouse-dialect SQL. If provenance semantics are the thing
that fights you, that is the signal to switch — not general dissatisfaction with
SQL.

Its cost is a hop of detection latency, which is acceptable, and a second
execution path, which is what A avoids.

## The condition that makes A real

**Without a per-source CI equivalence test, option A is option D with extra
steps.** Two compiled emissions of one authoring that are never compared are, in
practice, two implementations — they simply have not diverged *yet*, and nothing
will report the day they do.

Two conditions, both required:

1. **Shared-snapshot enrichment in both legs.** Dimension data lives in DuckLake
   tables *and* in Proton `versioned_kv` streams, both fed from one loader, with
   a shared snapshot version stamped into every enriched row. Without the shared
   version, the two legs can each be internally correct and disagree, and the
   disagreement is invisible because each looks right on its own.
2. **A per-source equivalence test in CI.** Take a fixed Silver fixture, run both
   compiled artifacts, assert row-for-row identity **including nulls and
   reasons**. Nulls are the point: a test that compares only non-null values
   would pass on precisely the divergence that matters most, since provenance
   lives in the null representation.

The fixture must be hostile rather than representative. Engine-specific
divergence concentrates in null handling, collation, and division semantics —
none of which a fixture drawn from typical traffic will exercise.

`DEC-0011` therefore stays at `Proposed` until that test exists. Promoting it to
`Accepted` beforehand would record a guarantee the estate does not have, which is
the failure mode `archive/RECOVERY.md` Part 2 documents four instances of.

## Recommended next step before committing

A one-day spike compiling a single real Silver→Golden mapping to both dialects
and diffing the output on a hostile fixture. That is the cheapest available test
of whether the provenance semantics are expressible in ClickHouse-dialect SQL at
acceptable effort — which is the only question on which the A-versus-C choice
actually turns.

Decide from that spike. Do not decide from preference about SQL.
