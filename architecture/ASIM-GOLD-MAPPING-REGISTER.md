# ASIM Gold mapping register — navigation and open findings

> **Consolidated conventions:** [DEC-0038](../decisions/DEC-0038-medallion-schema-conventions.md) governs Medallion naming, field resolution and record-local normalization. Authentication is the first cross-platform conformance family; Windows is the first implemented contributor.

**Status:** Navigation page; not an independent mapping contract or conformance
certificate. The canonical source-field inventory and candidate mappings are
maintained in [ASIM-GOLD-MAPPING-BASELINE.md](ASIM-GOLD-MAPPING-BASELINE.md).
This path is retained so previously published references continue to resolve.

**Authority:** Accepted `DEC-0038` (consolidated schema conventions), `DEC-0029` (observed event time), and
`DEC-0033` (LocalStream/Query and DuckLake). The Platform implementation
is **not** certified ASIM-conformant.

**Naming:** DEC-0038 retains the singular PascalCase identifiers selected in
[DEC-0034](../decisions/DEC-0034-mvp-asim-tables-and-views.md), unqualified
in KQL and under `golden` in SQL. The archived `*Activity` names are
not the current target.

The [normalization reference methodology](NORMALIZATION-REFERENCE-CATALOGUE.md) extends C10 to parser expressions, enumeration mappings and source-scoped aliases. The existing baseline remains the mapping authority.

## Baseline and verification responsibilities

| Purpose | Authoritative location |
|---|---|
| Four current telemetry Gold families, all 71 declared fields, source/Silver mappings and candidate ASIM conversions | [ASIM-GOLD-MAPPING-BASELINE.md](ASIM-GOLD-MAPPING-BASELINE.md) |
| Source-level field/type/order drift detection | [gold_inventory_check.py](../.github/scripts/gold_inventory_check.py), invoked by `governs-check` |
| Cross-component source findings, event-time defect C11 and test matrix T01–T10 | [C03/C10 source verification](../reports/2026-11-23-c03-c10-source-verification.md) |
| Forward's field-value datetime and duration mismatch | [Forward contract audit](../reports/2026-11-23-forward-type-contract-audit.md) |
| Remediation ordering and acceptance gates | [Consistency and correctness roadmap](../roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md) |

The ASIM baseline records the **reviewed documentation** for DNS, Network
Session, Process Event and Authentication schema version 1.0.0, including
per-family Microsoft reference links. The baseline now pins Microsoft's tester snapshot and links the [1,225-entry reverse field inventory](ASIM-GOLD-TARGET-FIELDS.csv). Reconcile the tester against the published schema prose and source-specific fixtures before claiming conformance.

## Unresolved mapping and quality gates

| ID | Outstanding check | Policy boundary |
|---|---|---|
| C10 | Versioned source→Silver→Gold→ASIM field mappings, type/enumeration fidelity, conditional fields and extensions for the eight approved telemetry families (four current declarations) | DEC-0013 and DEC-0034 accepted; implementation not verified |
| C11 (EVT-01) | Missing/invalid source event time must not be replaced silently with ingest time in Gold/detections | DEC-0029 accepted; retain in Bronze and Silver, record a reason alongside null observed time, exclude from event-time detection, and verify all eight contributors |
| C03 | Wire tag-4 UTC datetime compatibility, registry duration-unit mismatch, end-to-end provenance | Incompatible wire format changes require owner approval |
| C07 | Stable Gold/alert identities and replay-safe DuckLake writes | DEC-0030/0033 accepted; end-to-end integration not verified |

`EVT-01` and `C11` refer to the **same** event-time fallback defect; they are
not separate implementation tasks.

Operational `AlertEvent` and `AlertEntity` views are inventoried in the
baseline but **have not** been mapped to or certified against ASIM schemas.
[DEC-0034](../decisions/DEC-0034-mvp-asim-tables-and-views.md) approves four additional telemetry families (File Event, User Management, Registry Event and Audit Event). The current source inventory remains four families. The reference inventory now covers eight; the additional 539 entries require semantic mapping and source verification during C10. See [reference tooling](../tools/asim/README.md).

**Detection consumer contract:** DEC-0036 requires the query binding adapter to record rule-to-field dependencies, relevant mapping and schema revisions, source applicability and missing/invalid input diagnostics. This is C10 work in the existing mapping authority, not another catalogue or extra Gold view. See [detection provenance](DETECTION-PROVENANCE.md).
