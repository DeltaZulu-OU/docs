---
id: DEC-0013
status: Accepted
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: []
supersedes: D13
---

# DEC-0013 — Golden semantic model and naming

> **Consolidated conventions:** [DEC-0038](DEC-0038-medallion-schema-conventions.md) supersedes the schema and naming provisions of this decision. Remaining requirements retain their status.

## Context

The historical architecture presented OCSF-derived semantics in an ASIM-like
shape, while archived Platform ADR 0007 preferred DeltaZulu-owned names with
optional OCSF lineage. Neither expressed the current choice. On 2026-11-23
the owner explicitly selected **ASIM schemas, or schemas derived from ASIM,
wherever practicable, rather than OCSF**.

Microsoft Sentinel's Advanced Security Information Model (ASIM) defines
activity/event and entity schemas with common and schema-specific fields,
entity-role prefixes, value formats, enumerations, mandatory/conditional
fields and aliases. This is a substantive semantic model, not merely a
naming convention. ASIM's source-to-normalized mapping supports fields
outside its defined schema, but doing so must not misrepresent compatibility.

The single logical field contract still belongs to DeltaZulu's C#-owned
catalogue under `DEC-0012`. `DEC-0033` places stream processing in
LocalStream/Query and durable Gold in DuckLake, without Proton. A schema
source of inspiration does not create a dependency on Microsoft Sentinel.

## Decision

1. **ASIM-first canonical Gold.** For each supported event or entity family,
   prefer the corresponding published ASIM schema. Reuse ASIM field names,
   field roles, entity prefixes, types, allowed values and semantics as
   closely as the underlying evidence and the DeltaZulu runtime permit.
   Relevant starting families include DNS, authentication, network session,
   process, file, registry, audit and alert events. This is a preference,
   not a claim that all of those families are currently implemented.
2. **Derive explicitly when necessary.** When no applicable ASIM schema exists,
   or the source contains facts the applicable ASIM schema cannot express
   faithfully, derive a DeltaZulu-owned schema or extension using ASIM's
   naming and entity conventions where appropriate. Document each mapping,
   omission, extra field and semantic deviation. Preserve source evidence
   rather than fabricating values for missing mandatory ASIM fields.
   Inapplicable or incomplete mappings must not be represented as conformant.
3. **ASIM is the reference, not an automatically updated authority.** Pin the
   reference schema and version for each mapping. Version DeltaZulu's own
   logical contracts and review upstream ASIM changes explicitly before
   adopting them; external changes must not silently alter stored Gold,
   detection fields, or public query behavior.
4. **Respect internal invariants.** ASIM alignment cannot silently override
   `DEC-0003`'s declared-type/normalization rules, `DEC-0016`'s
   collection-tier and null-reason provenance, `DEC-0029`'s event-time
   policy, or `CON-0014`'s canonical duration ticks. Where ASIM's
   logical types differ from CLR or DuckDB physical types, use explicit,
   tested mappings without lossy coercion. Event identity and replay
   guarantees from `DEC-0030` also remain binding.
5. **OCSF is not the Gold schema authority.** Do not author canonical Gold
   from OCSF, require OCSF lineage, or retain an OCSF-based parallel
   model. Future OCSF export could be separately proposed but is not
   approved by this Decision.
6. **Separate mapping from execution.** Normalize source-specific Silver
   into the ASIM-aligned Gold contract through governed transformations.
   Gold is persisted to DuckLake under `DEC-0033`. This Decision does
   not require Microsoft's Sentinel runtime, its proprietary tables,
   unifying parser functions, or a Proton processor.

### Gold view naming

The approved MVP view names are recorded in
[DEC-0034](DEC-0034-mvp-asim-tables-and-views.md). Use singular PascalCase
ASIM family identifiers for telemetry (for example, `Dns`,
`NetworkSession`, `ProcessEvent`), retaining the existing
DeltaZulu operational names `AlertEvent` and `AlertEntity`.
KQL exposes the unqualified logical names; the current SQL view namespace
is `golden` (for example, `golden.Dns`). Gold is the architectural layer,
not a rename of the SQL schema to `gold`. Native Sentinel table names and
parser function names are external references, not DeltaZulu view names.
The historical Platform ADR 0007 `*Activity` naming target is superseded
by DEC-0013 and the approved selection in DEC-0034. This clarification
preserves existing public names; it does not authorize renaming persisted
relations or changing query compatibility.

## Conformance and implementation requirements

A schema-mapping register must record for each Gold event family:

| Entry | Required evidence |
|---|---|
| Reference | ASIM schema name, canonical documentation URL and reviewed version |
| Fields | Source-to-Gold mapping; ASIM mandatory, recommended and conditional fields; any unpopulated fields and why |
| Values | Enumerated normalization, source-value retention, null and absent-field meaning |
| Extensions | DeltaZulu-only fields, names, types, rationale and whether they are ASIM-compatible or ASIM-derived |
| Physical representation | Declared KQL type and DuckLake mapping, timezone, duration scale and loss behavior |
| Verification | Fixtures and schema conformance results; unsupported/partial mappings made explicit |

Do not claim full ASIM compliance merely because field names match. Any
ASIM unifying parser or query integration is a separate implementation and
verification question. ASIM's Microsoft Sentinel query-time parsers and
native normalized tables are not required implementation dependencies.

## Consequences

Gold schema selection is settled: **ASIM-first, explicitly derived where
necessary, no OCSF base**. Schema family coverage, exact extensions,
version mappings and source-level fidelity remain engineering work,
to be verified before publishing a stable Gold catalogue or detection pack.

This Decision replaces the unresolved alternatives previously recorded here.
It does not assert that the current Platform schema implementation has already
been migrated to ASIM or that Microsoft Sentinel integration works.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| OCSF-derived canonical Gold | Contradicts the selected ASIM-first model and creates an unnecessary competing schema authority | — |
| Unstructured DeltaZulu-only naming where ASIM already covers the event | Forfeits ASIM's existing normalized vocabulary and portability without a source-specific need | — |
| Treat every derived mapping as fully ASIM-conformant | Masks missing required fields, incompatible enum values and type semantics | — |
| Automatically follow upstream ASIM revisions | Changes Gold contracts and potentially detections without an estate version/migration decision | — |

## Revisit trigger

Reopen if an event family cannot be represented using ASIM or a faithful
ASIM-derived extension without unacceptable semantic loss, with concrete
source examples and mapping fixtures. Reopen versioning rules if a supported
ASIM revision materially changes field meaning, required fields or enum values.

## References

- [Microsoft: ASIM schemas](https://learn.microsoft.com/en-us/azure/sentinel/normalization-about-schemas)
- [Microsoft: ASIM normalization architecture](https://learn.microsoft.com/en-us/azure/sentinel/normalization)
- [Microsoft: Developing ASIM parsers](https://learn.microsoft.com/en-us/azure/sentinel/normalization-develop-parsers)
