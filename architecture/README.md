# Architecture

Estate-wide current **target architecture**, implementation notes and dated
historical imports. Current-target narratives are revised in place, but an
Accepted Decision sets policy and a source or integration check establishes
implementation status. Historical imports remain preserved as evidence.

## Contents

| Document | Status |
|---|---|
| `PIPELINE.md` | The consolidated architecture, 15 August 2026. Supersedes the 12 August revision. **Imported verbatim and not edited.** |
| `PIPELINE-ERRATA.md` | Where Wave 0 verification found `PIPELINE.md`'s claims refuted, understated, mis-cited or unverified. |
| `DATA-QUALITY-MONITORING.md` | DQM rev. 2, 16 August 2026. Metrics, measurement points M0–M17 plus the external MX and MZ, and the eight quality planes. **Imported verbatim.** |
| `DATA-QUALITY-MONITORING-INTEGRATION.md` | What the DQM import changes about planned work. Its inventory has nine rows but **ten named provenance properties**; LocalStream replaces historical Proton dependencies. |
| `NRT-PIPELINE.md` | **Current target, updated 27 November 2026:** LocalStream/Query instead of Proton (`DEC-0033`); consolidated Medallion schema conventions (`DEC-0038`). |
| `ASIM-GOLD-MAPPING-BASELINE.md` | **Canonical ASIM mapping baseline**: source-inventoried Gold fields, reviewed ASIM 1.0.0 candidate mappings, pinned 1,225-entry tester reverse inventory and proposed fixtures; **not implemented or certified**. |
| `ASIM-GOLD-MAPPING-REGISTER.md` | Compatibility navigation to the canonical baseline; identifies C03/C10/C11/C07 gates. Not an independent register. |
| [DETECTION-PROVENANCE.md](DETECTION-PROVENANCE.md) | Target logical contract for causal detection results, rule revision and evidence lineage under DEC-0036; implementation open. |
| [DETECTION-RESULT-CONTRACT.md](DETECTION-RESULT-CONTRACT.md) | Approved design directions; detailed C06/C07 identity, temporal and persistence contract gates remain open. |
| [NORMALIZATION-REFERENCE-CATALOGUE.md](NORMALIZATION-REFERENCE-CATALOGUE.md) | Provider-neutral reference extraction and normalization verification methodology under DEC-0038; implementation open. |
| [AGENT-ACQUISITION-CONTRACT.md](AGENT-ACQUISITION-CONTRACT.md) | Agent acquisition, state/filter ordering, enrichment and local query boundaries; runtime qualification open. |
| [PLATFORM-RESPONSIBILITY-CONTRACT.md](PLATFORM-RESPONSIBILITY-CONTRACT.md) | Platform ownership, analytics, governance and management boundaries; legacy wiring qualification open. |
| [COMPONENT-BOUNDARIES.md](COMPONENT-BOUNDARIES.md) | Parse, LogCluster, LocalStream and DurableBuffer ownership and qualification. |
| `GOVERNING-DECISIONS.md` | Which Decisions govern which repository, generated from front-matter. |

`PIPELINE.md` is left unedited so that historical citations stay stable.
It is **not** the current processing architecture: its Proton statements are
superseded by `DEC-0033`. For the present design start with
`NRT-PIPELINE.md`; read `PIPELINE.md` together with `PIPELINE-ERRATA.md`
only to understand earlier reasoning.

Its D1–D21 register has been seeded into `decisions/` as `DEC-0001`–`DEC-0021`
under global numbering, which resolves the Agent-0014/Platform-0014 collision by
giving each decision a number that means one thing estate-wide.

## Authority and conflict handling

| Record | Authority |
|---|---|
| Applicable Constraints | External facts within their stated version and scope; supersede if refuted |
| Accepted Decisions | Binding estate policy, subject to explicit supersession |
| Current architecture | Target contract interpreting Accepted Decisions; candidate sections require approval |
| Component source and tests | Observed implementation at a pinned revision; tests qualify only their exercised scope |
| Consolidated roadmap | Work, dependencies and open approvals, not independent architectural policy |
| Dated reports and archives | Historical evidence, not current implementation or binding policy |

If a target narrative conflicts with an Accepted Decision, correct the
narrative or seek a new Decision. If source conflicts with policy, record
the discrepancy and qualification requirement under its existing C item.
Do not treat source presence, a green build or an existence check as
proof of deployed behavior. Proposed Decisions and candidate contracts
must not be promoted by documentation edits alone.

The [27 November authority audit](../reports/2026-11-27-documentation-authority-audit.md) pins all eight component
documentation indexes and identifies the remaining legacy Proton source
inventory. Local documents remain implementation references until
individually reconciled; no blanket migration or deletion is implied.

## Per-repo architecture — pending migration

Existing architecture documents still live in their own repositories:

- `DeltaZulu.Agent/docs/` — ARCHITECTURE.md and 16 further documents
- `DeltaZulu.Platform/docs/` — including `docs/analytics/` and `docs/reviews/`
- `DeltaZulu.LocalStream/docs/LOCAL_STREAM_ARCHITECTURE.md`
- `DeltaZulu.Parse/docs/`

All eight repository documentation indexes now point to the current estate target and consolidated roadmap. Agent, Platform and LocalStream architecture documents carry explicit authority/scope notes; see the [rebaseline report](../reports/2026-11-25-inherited-milestone-rebaseline.md). Per-repository documents may still describe earlier choices. Until reviewed
against `DEC-0033` and the global Decision set, treat them as implementation
references or historical plans, **not a second governing authority**. Their
migration and source-level rebaseline remain explicit roadmap work; the target
narrative above does not imply the LocalStream integration is implemented.


The [consolidation assessment](../reports/2026-11-27-documentation-consolidation.md) distinguishes the completed inventory pass from outstanding C08 implementation and historical milestone verification.
