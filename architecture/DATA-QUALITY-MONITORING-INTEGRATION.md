# DQM rev. 2 — integration into the estate plan

Date: 2026-08-16. Companion to `DATA-QUALITY-MONITORING.md`, which is imported
verbatim. This file holds what the import *changes* about work already planned.

## Current-target note — 2026-11-23

This document predates DEC-0033. References to Proton and `DEC-0011`'s
dual-engine Gold equivalence describe an abandoned design, **not** a
pending implementation gate. LocalStream and its separate Query package
replace Proton for streaming processing; DuckLake remains the durable lake.
The provenance, loss and integrity invariants still apply.

## The finding that must not wait: FWD-CONTRACT-v2 triples in scope

FWD-CONTRACT-v2 was scoped to add three provenance fields to `ForwardLogRecord`
— `CollectionTier`, a sparse null-reason map, and the availability-matrix
version. The inventory below contains **nine rows but ten named properties**:
`ParserId` and `ParserVersion` occupy one table row while remaining separate
fields. Every property records potentially irreversible provenance. The earlier
"nine fields" claim counted table rows rather than field properties.

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
*revision*. That argument applies to **seven additional named properties**, not six.
As of 2026-11-23, `DeltaZulu.Forward` declares all ten properties as optional
record members; their end-to-end population, persistence, reader semantics and
version compatibility remain unverified. Declaring fields is not equivalent to
fully implementing the contract.

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
| **2a — external ground truth** (canary, reconciler, receiver inventory) | Prototype can start independently | Production canary writes need a retention/filtering Decision (DEC-0023) |
| **3 — reconciliation identities** | Follows DQM wave 2 | Cheap once counters exist |
| **3a — durability** (digests, manifests, restore) | **Estate Wave 1, alongside the collector** | Digest at write time or never |
| 4 — delivery offsets, RPO gauge | Estate Wave 1–3, follows the collector | |
| 5 — semantic (enum mismatch, stream-to-lake divergence) | Estate Wave 3, rebaseline for `DEC-0033` | |
| 6 — timeliness | Rebaseline for LocalStream-derived Gold and DuckLake persistence | Superseded Proton Golden MV is not a prerequisite |
| 7 — coverage (data contracts, rule validity) | Estate Wave 3 product layer | |
| 8 — adjudication | Last | Worthless without 1 and 7 |

### Two items are more urgent than their numbering suggests

**The DQM wave 2a prototype can begin independently.** An external emitter,
reconciler and receiver-side inventory do not need the full streaming pipeline
to be prototyped. Deploying canary events into write-once Bronze is a different
matter: `DEC-0023` explicitly leaves retained-and-marked versus filtered
undecided and blocks production emission until that choice is recorded.

**DQM wave 3a is irreversible in the same way wave 1 is.** A Bronze payload
written without a digest cannot be given one later — the digest attests to what
was written, and computing it afterwards attests only to what is there now,
which is the question it exists to answer. If the collector is built before this
is decided, every row it writes is permanently unattestable.

## Replace dual-engine parity with stream-to-lake correctness

The imported DQM §6.3 parity measure assumed Proton and DuckDB SQL
compilation under the formerly Proposed `DEC-0011`. That Decision is
now Rejected by `DEC-0033`. Proton-vs-DuckDB equivalence must not remain
a release gate.

Validate instead the LocalStream-to-DuckLake path: source conservation,
types and null reasons, event-time windows and late arrival, stable
Gold/alert identity, idempotent sink replay, and evidence
reconstructibility. Use hostile fixtures and actual integration
execution; no such passing suite is established by this document.

## Detection evaluation quality — 2026-11-26

[DEC-0036](../decisions/DEC-0036-detection-provenance.md) extends the existing data-contract/rule-validity coverage work. C04 records scoped evaluation health, C06 provides distinct successful, incomplete and failed outcomes, and C10/C11 provide declared field and temporal applicability. The [detection provenance contract](DETECTION-PROVENANCE.md) defines denominators and diagnostic boundaries. Evaluation coverage is neither source completeness nor recall; unbound rules and unknown denominators remain visible. Artifact hashes alone do not establish execution correctness or settle DEC-0024 integrity policy.

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
requires end-to-end preservation of the ten named properties in the nine-row inventory.

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

**Prior review date: 2026-11-16 (overdue).** Rebaseline after the next recorded
Bronze-integrity or canary-retention Decision, or after an end-to-end provenance
fixture demonstrates actual lake persistence. No new implementation deadline
is implied by this documentation correction.
