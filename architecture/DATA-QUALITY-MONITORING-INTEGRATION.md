# DQM rev. 2 — integration into the estate plan

Date: 2026-08-16. Companion to `DATA-QUALITY-MONITORING.md`, which is imported
verbatim. This file holds what the import *changes* about work already planned.

## The finding that must not wait: FWD-CONTRACT-v2 triples in scope

FWD-CONTRACT-v2 was scoped to add three provenance fields to `ForwardLogRecord`
— `CollectionTier`, a sparse null-reason map, and the availability-matrix
version. DQM §4.1 requires **nine**, and every one of them is irreversible for
the same reason the original three were: the information exists at the moment of
writing and nowhere afterwards.

| Field | In original v2 scope | Set at | Why it cannot be backfilled |
|---|---|---|---|
| `CollectionTier` | yes | M0 | A null's meaning is tier-dependent |
| `NullReasons` | yes | M4–M6 | The moment of failure is the only moment it is known |
| `MatrixVersion` | yes | M6 | A row written under matrix v3 must be read under v3 |
| **`TimestampOrigin`** | **no** | M3/M6 | A fallback-assigned time is indistinguishable from an observed one once written |
| **`ParserId` / `ParserVersion`** | **no** | M3 | Attribution of a bad extraction to a generation |
| **`RulebaseHash`** | **no** | M3 | Fleet divergence is undetectable without it |
| **`ParserLocationAgentId`** | **no** | M3 | Under a multi-hop topology, parsing may happen at any hop |
| **`OriginAgentId`** | **no** | M0 | Multi-hop identity and loop detection |
| **`HopCount`** | **no** | M9 | Loop prevention and topology observability |

`ParserGeneration`, `FilterBoundaryVersion`, `EnrichmentSnapshots` and
`RawEventId` were already designed elsewhere and are unaffected in status,
though they belong to the same record.

**This is the single most time-critical consequence of the import.** The
correction set already argued that adding provenance while the contract is
stabilising is a contract *field*, and adding it afterwards is a contract
*revision*. That argument now applies to six more fields, and the fuzzing harness
is still being built around the current shape. Landing v2 with three of nine
means a second revision for the other six, on a contract with a compatibility
window and a fleet to roll through.

`TimestampOrigin` deserves separate emphasis. DQM calls it the cheapest
high-value addition in the document and notes it is the one place where a
surveyed competitor implements DeltaZulu's own stated principle better than
DeltaZulu does. It is a closed six-member enumeration on the record. The cost is
trivial; the consequence of omitting it is that every event time in the lake is
of unknown provenance forever.

## How the DQM waves map onto the estate waves

DQM §12 numbers its own waves 1–8. Those are **not** the estate's Wave 0–5 from
`PIPELINE.md` §16, and conflating them would be an easy and expensive mistake.
The mapping:

| DQM wave | Estate placement | Note |
|---|---|---|
| **1 — irreversible record fields** | **Estate Wave 1, inside FWD-CONTRACT-v2** | Not a follow-on. These are contract fields |
| **2 — structural counters** (M1–M3) | Estate Wave 4, with Agent Phases 6–8 | Phase 8's auditd assembly hits this immediately |
| **2a — external ground truth** (canary, reconciler, receiver inventory) | **Can start now — no dependencies** | See below |
| **3 — reconciliation identities** | Follows DQM wave 2 | Cheap once counters exist |
| **3a — durability** (digests, manifests, restore) | **Estate Wave 1, alongside the collector** | Digest at write time or never |
| 4 — delivery offsets, RPO gauge | Estate Wave 1–3, follows the collector | |
| 5 — semantic (enum mismatch, cross-engine divergence) | Estate Wave 3, with `DEC-0011` | |
| 6 — timeliness | Estate Wave 3, needs the Golden MV | |
| 7 — coverage (data contracts, rule validity) | Estate Wave 3 product layer | |
| 8 — adjudication | Last | Worthless without 1 and 7 |

### Two items are more urgent than their numbering suggests

**DQM wave 2a is buildable today and depends on nothing in this estate.** The
canary emitter sits outside the pipeline, the reconciler compares emitted
sequences against what the lake holds, and the receiver-side source inventory
lives at the aggregation node. None of it needs the type catalogue, the
transport, Golden, or a published package. It is also the only work that makes
"completeness" an honest word, and the cheapest way to find out whether current
loss rates are what anyone assumes.

**DQM wave 3a is irreversible in the same way wave 1 is.** A Bronze payload
written without a digest cannot be given one later — the digest attests to what
was written, and computing it afterwards attests only to what is there now,
which is the question it exists to answer. If the collector is built before this
is decided, every row it writes is permanently unattestable.

## Cross-engine divergence: DQM supplies the metric `DEC-0011` was waiting for

`DEC-0011` (Silver→Golden dual-compiled) is held at `Proposed` pending a CI
equivalence test, on the grounds that without it option A is option D with extra
steps. DQM §6.3 specifies exactly that test — **cross-engine divergence rate**,
including null and reason equality, per build plus a production sample — and
§5.7 specifies the primitive it needs (`golden.rows_projected`, emitted
identically by both engines).

That is the missing piece named. `DEC-0011` still stays `Proposed` until the test
*exists*, but the specification gap is now closed and the remaining work is
implementation rather than design.

## What contradicts, and what merely extends

Nothing in DQM contradicts a Constraint or an Accepted Decision. Three points
extend existing positions in ways worth recording:

- **`DEC-0016`** (best-effort collection, mandatory loss accounting) is the
  Decision DQM elaborates. Its field list grows per the table above.
- **`DEC-0021`** (threshold as windowed aggregate) is now *load-bearing for a
  metric*, not only for authoring clarity. DQM §14 notes that late-arrival
  exclusion presumes windowed aggregates; if content turns out to be
  predominantly stateless filters, that metric degrades from a correctness
  signal to an operational nicety. The threshold-placement decision determines
  which.
- **`DEC-0019`/`DEC-0022`** (the collector) acquire a requirement they did not
  have: M11 is the ACK boundary and M12 must write payload digests. Both are
  collector properties, and both are cheaper to design in than to add.

## The claim DeltaZulu should not make

DQM §11.2 is worth restating because it is the sort of position that erodes under
commercial pressure. DeltaZulu **can** measure precision given dispositions and a
coverage figure. It **cannot** measure recall from any pipeline metric, and no
roll-up produces one.

What it can do that the surveyed platforms cannot is split a miss into a
**content gap** (telemetry arrived, no rule fired) and a **collection gap**
(telemetry never arrived) — and in the second case name the field and the reason.
That requires `RecordId` lineage, `CollectionTier`, null reasons and the
capability matrix, which is to say it requires DQM wave 1, which is to say it
requires FWD-CONTRACT-v2 to carry all nine fields.

The narrower claim is defensible. The broader one would not be, and the
difference between them is the whole argument for doing wave 1 properly.

## Caveats carried from the import

DQM §1.1 states them and they should not be lost in summary. The underlying
survey's citations are unresolvable reference tokens rather than URLs, so **no
vendor-specific claim in it has been independently verified**, and none is
load-bearing here — what was adopted is the framework, not the comparisons. The
survey's two-decimal-place means over thirteen integer scores with unspecified
cells excluded are false precision that also rewards documentation gaps.

The self-assessment in §13 is a projection, not a measurement. Its own framing is
the right one: the movement from ~1.8 to ~4.2 is *the distance between a design
and a product*, and every row of the "with this document delivered" column is
unbuilt.

## Review trigger

**Next review: 2026-11-16**, or earlier if FWD-CONTRACT-v2 is drafted, if the
collector acquires a repository, or if any DQM wave-1 field is proposed for
deferral — that last one being the condition this whole document exists to make
visible.
