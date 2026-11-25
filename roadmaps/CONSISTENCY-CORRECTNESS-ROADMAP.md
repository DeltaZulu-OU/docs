# Consolidated DeltaZulu roadmap

**Baseline:** 2026-11-25. **Next review:** 2026-12-07, or on a new
accepted decision, contract change or completed integration suite.

This is the **single consolidated planning table** for the DeltaZulu estate's consistency, correctness and inherited product work. Inherited product entries are candidates pending source/test verification and owner prioritization, not new commitments. Each task has exactly one stable `Cnn` work-item identifier.
`DEC-nnnn` identifies a governing architectural decision, and `CON-nnnn`
identifies a constraint; neither is a separate work item. Source-audit labels
such as `EVT-01` and `FWD-01` are findings attached to a work item, not
additional tasks. Prior identifiers remain valid for traceability.

**Status terminology:** `Done (docs)` means the documentation or checker
was changed, **not** that the runtime behavior was implemented. `Audited`
means source was inspected without application tests. `Open` means work
or policy remains outstanding. Only tested behavior may be called verified. `Rebaseline` means a surviving historical topic has been captured, but scope/status/priority must be validated against source and CI. `P—` means priority is not assigned, not deferred.

## Consolidated execution table

| Work item | Priority | Affected projects | Work and current status | Completion criterion | Governing decision / outstanding approval |
|---|---|---|---|---|---|
| **C01** | P0 | `docs`; governed repositories (read-only checks) | **Done (docs).** Metadata validation, checkout fail-closed enforcement, generated Decision index, production declaration checks, tests and CI checks. | Keep governance and CodeQL workflows passing on updates; report source checks as existence checks, not behavior proofs. | Documentation governance; no new owner approval. |
| **C02** | P0 | `docs` | **Mostly done (docs).** Corrected refuted source claims, report summaries, Decision states and archival authority. Collector, timestamp and integrity qualifications recorded; historical Constraint classification remains open. | Accepted Decisions and active docs contain no known refuted current claims; historical artifacts remain intact and any reclassification is explicit. | Classification of mixed factual/policy records (see constraints index) requires owner approval. |
| **C03** | P0 | `DeltaZulu.Forward`, `DeltaZulu.Kql`, `DeltaZulu.Platform`, `docs` | **Audited.** Datetime field tag 4 conflicts with the KQL carrier; Forward TimeSpan codec uses ticks while Platform registry defaults to microseconds; provenance propagation unverified. | Compatible old/new codec tests, explicit UTC/rejection policy (ambiguity, invalid local wall time, overflow and unspecified kind), exact duration-scale and provenance round trips through the lake. | `DEC-0003`; owner must approve incompatible wire policy. |
| **C04** | P0 | `DeltaZulu.Agent`, `DeltaZulu.Platform`, `DeltaZulu.Forward`, `docs` | **Open.** Bronze write-time digests, partition manifests, restore tests and production canary-retention policy are not approved as a complete control set. Ground-truth measurement vs delivery guarantees and manifest rollback threat model are documented. | Accepted assurance policy, signing-key custody model, restoration evidence and destructive/replay tests. | `DEC-0023`, `DEC-0024`; owner decisions pending, including reporting semantics. |
| **C10** | P0 | `DeltaZulu.Agent`, `DeltaZulu.Parse`, `DeltaZulu.Forward`, `DeltaZulu.Platform`, `DeltaZulu.Kql`, `docs` | **Audited; mapping open.** Four telemetry Gold families, 71 declared fields, eight Silver contributors and two separately inventoried alert views. ASIM-first is accepted but field-level conformance is unverified; 686 target-field entries inventoried from a pinned Microsoft tester snapshot; documentation/tester reconciliation, semantic dispositions and Agent-to-Silver lineage remain open. | Pinned tester reference established; reconcile published schema/conditions, per-family mapping/extension register, types and enum fixtures, provenance and migration tests. | `DEC-0013` Accepted; no further schema-family choice required to begin. |
| **C11** | P0 | `DeltaZulu.Platform`, `docs` | **Audited; correction open.** All eight Silver contributors may substitute ingest time for missing/invalid source event time. Historical finding label: `EVT-01` (same task). | All eight source fixtures distinguish observed, absent and invalid event time; no implicit ingestion-time input to event-time detections. | `DEC-0029` Accepted; unavailable-time handling must be explicit and tested. |
| **C05** | P1 | `DeltaZulu.Agent`, `DeltaZulu.Forward`, `DeltaZulu.LocalStream`, `DeltaZulu.Platform` | **Open.** Collector ACK/append boundaries, offset checkpoints, replay, retention and `OffsetExpired` behavior lack end-to-end verification; target subscription fan-out clarified, separate collector executable still unverified. | Crash-point and duplicate/restart fixtures demonstrate conservation, recoverability and explicit expiry behavior. | `DEC-0019`, `DEC-0022`, `DEC-0033`. |
| **C06** | P1 | `DeltaZulu.Platform`, `DeltaZulu.LocalStream` (Query), `DeltaZulu.Kql` | **Open.** Kusto.Language binding, event-time windows, lateness, threshold semantics and supported DuckDB hunting subset are unverified. Depends on C10 and C11. | Semantic corpus demonstrates allowed operators, explicit rejection of unsupported syntax, watermark/late-event behavior and reproducible outputs. | `DEC-0032`, `DEC-0033`; `DEC-0021` threshold/window decision pending. |
| **C07** | P1 | `DeltaZulu.Platform`, `DeltaZulu.LocalStream` (Query/LiteDB) | **Open.** Idempotent Gold/alert DuckLake sinks, result-change identity, checkpoint coordination and evidence references lack integration proof; window-result identity and evidence-set revisions remain open. Depends on C05/C06. | Replay/crash tests preserve stable event/alert identities, disclose unresolved references and reconcile partial writes. | `DEC-0030`, `DEC-0033`. |
| **C08** | P1 | `docs`, `DeltaZulu.Agent`, `DeltaZulu.Platform`, `DeltaZulu.Forward`, `DeltaZulu.LocalStream`, `DeltaZulu.Parse`, `DeltaZulu.LogCluster`, `DeltaZulu.DurableBuffer`, `DeltaZulu.Kql` | **Partially done (docs).** Six imported plans reconciled; all eight local docs indexes corrected and Agent/Platform/LocalStream architecture scope notes added. Remaining component-specific references, full milestone verification, and Proton source migration stay open. | Every active document is current or explicitly historical; obsolete Proton tasks are not actionable; project responsibilities match accepted Decisions. | `DEC-0033`, `DEC-0013`; no automatic implementation changes. |
| **C09** | P1 | `docs`; governed repositories (read-only checks) | **Partially done (docs).** Metadata/relationship, checkout, lexical declaration, local-link and Gold catalogue checks hardened; active roadmap structure and review-date warning added; parsed local/reference links and Markdown anchors added; external links, full semantic conformance and advanced GitHub anchor equivalence remain open. | Reproducible CI detects missing/broken current references, contradictory Decision states and stale roadmap reviews without claiming code conformance. | Governance policy; no new owner approval. |
| **C12** | P— | `DeltaZulu.Agent`, `DeltaZulu.Parse`, `DeltaZulu.LocalStream`, `DeltaZulu.Kql` | **Partial source/CI evidence.** Acquisition plan/compiler and fixtures present; runtime still constructs ChannelOutputMultiplexer and references DurableBuffer. Verify actual plan-driven execution, parser migration, state/filter ordering, reload/observability and parity. Delivery belongs to C05. | Validate each inherited phase against source, tests and benchmarks; retain only gaps. | DEC-0005–0009, DEC-0014–0016, DEC-0033; inherited scope/priorities not newly approved. |
| **C13** | P— | `DeltaZulu.Agent` | **Partial source/CI evidence.** CLI workbench, tail, metrics, SQLite reader/writer and systemctl lifecycle commands present. Verify mode behavior, bounded display/fault metrics, portability and local IPC. | Verify each milestone against CLI/Daemon/ProfileWorkbench source and integration tests. | Historical controller plan; confirm surviving scope and priority. |
| **C14** | P— | `DeltaZulu.Forward`, `DeltaZulu.Kql`, `DeltaZulu.Parse`, `DeltaZulu.Agent`, `DeltaZulu.Platform`, `DeltaZulu.LocalStream`, `DeltaZulu.DurableBuffer` | **Blocked verification.** Platform exact-revision restore failed on all three OS; logs expired. Parse build/pack passed. Verify package feed/version provenance, LocalStream 0.1.0 source vs Agent 1.0.0 pin, DurableBuffer explicit version and consumer compatibility. No new wire fallback. | Clean restore/build/pack and supported consumer compatibility tests; verify publishing rights and version status. | CON-0006 and DEC-0001–0004; framework changes require explicit review. |
| **C15** | P— | `DeltaZulu.LogCluster`, `DeltaZulu.Parse` | **Source implemented in part.** Parse catalogue adapter and rendering regressions present; exact-revision push-test evidence unavailable. Raised MaxRecords may exceed int miner/scorer arithmetic; verify boundaries, Perl parity, locked restore and scope before closure. | Validate current APIs and parity fixtures, negative/rendering/counter tests, locked restore and packaging. | No new scope or previous-phase completion assumed. |
| **C16** | P— | `DeltaZulu.Platform` | **Source evidence; tests blocked by C14.** Query, governance, alert/incident and UI primitives present; verify product requirements, safe shared execution, Operations workflows, enrichment/suppression/correlation/triage. NRT/persistence C06/C07; scheduled detection deferred. | Verify historical phases 1–12 and product requirements against current source/tests; prioritize only surviving gaps. | DEC-0026, DEC-0030, DEC-0032, DEC-0033; validate retained query safety/operations requirements. |
| **C17** | P— | `DeltaZulu.Agent`, `DeltaZulu.Platform` | **Partial source evidence.** HTTPS pull client, enroll/heartbeat/policy/command endpoints and Platform command/auth service fixtures exist. Verify daemon wiring, tenant scope, expiry, audited execution, signed metadata/TUF, certificate lifecycle and rollout. Platform tests blocked by C14. | Review source and tests against security requirements; confirm tenant scoping, audited command lifecycle, signed metadata trust/rollback/expiry and rollout gates. | Historical Platform ADRs 0012/0013/0015; binding status and scope require explicit review, not automatic acceptance. |

The **Affected projects** column indicates which codebases or documentation
need coordination, not which projects have already been modified.

## Dependency and execution sequence

C12–C17 consolidate surviving topics from the six [historical imports](README.md). Their detail and original milestone identifiers remain in the linked historical documents, not independent active roadmaps. Unverified past completion labels are not current claims. The [inherited milestone rebaseline](../reports/2026-11-25-inherited-milestone-rebaseline.md) records source and exact-revision CI evidence, including Platform restore failure (C14) and unverified LogCluster test execution (C15).

Continue **C02, C08 and C09** as documentation-only reconciliation.
**C03 and C10** can proceed independently through source and contract
verification; **C11** must be resolved before event-time Gold mappings
are certified. Implement **C05** independently of the Gold mapping.
Then complete **C06** once C10/C11 and its window policy are settled,
followed by **C07** after C05/C06. **C04**'s policy decisions must precede
claims about evidentiary integrity in production.

C10's canonical mapping inventory is
[ASIM-GOLD-MAPPING-BASELINE.md](../architecture/ASIM-GOLD-MAPPING-BASELINE.md).
[ASIM-GOLD-MAPPING-REGISTER.md](../architecture/ASIM-GOLD-MAPPING-REGISTER.md)
is a stable navigation page, not a second mapping authority.
The register covers the four declared telemetry Gold families; operational
alert views are identified separately. The checked source field names,
types and order do **not** establish semantic ASIM compliance.

C11 is the same finding previously called `EVT-01`. Its source and test
matrix appear in
[the C03/C10/C11 verification report](../reports/2026-11-23-c03-c10-source-verification.md).
The Forward wire contract investigation remains in
[the C03 audit](../reports/2026-11-23-forward-type-contract-audit.md).

## Owner decision register

The following are **unresolved policy questions**, not more task IDs:
Forward's UTC datetime wire migration and backward compatibility (C03);
Bronze evidence attestation and signing-key custody (C04); production
canary retention or filtering and ground-truth completeness reporting (C04); window-threshold and late-event
correction semantics (C06); historical Constraint reclassification
(C02); and adjudication/precision reporting (`DEC-0025`, not currently
an implementation gate in this roadmap). Reconfirm C12–C17 product scope, priorities and archived security obligations after source/test checks.

**Resolved:** `DEC-0013` specifies **ASIM-first Gold** (not OCSF),
and `DEC-0033` specifies **LocalStream instead of Proton**. Decisions
remain recorded in `decisions/`; this roadmap links to them rather
than creating parallel decision numbering.

## Architecture and verification boundaries

`DeltaZulu.Forward` owns inter-node transport; LocalStream core
remains payload-opaque; LocalStream.Query owns stream operators; KQL
parsing and binding belong in a query-owning adapter; DuckLake owns
durable evidence and user-visible queries. No AI capability is included.

The P0/P1/P2 rows describe **work still to be verified**, not
permission to make breaking contract changes. No Proton-based
processing is allowed in the target. Preserve immutable historical
Constraints and dated reports; append new verification rather than
rewriting old evidence.

**Supporting reports:** [inherited milestone rebaseline](../reports/2026-11-25-inherited-milestone-rebaseline.md), [consolidation review](../reports/2026-11-25-consolidation-review.md),
[architecture reconciliation](../reports/2026-11-23-proton-localstream-reconciliation.md),
[consistency corrections](../reports/2026-11-23-consistency-corrections.md),
[schema divergence verification](../reports/2026-08-16-schema-divergence-verification.md),
and [datetime carrier investigation](../reports/2026-08-24-forward-datetime-carrier.md).
