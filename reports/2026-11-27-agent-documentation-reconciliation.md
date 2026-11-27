# Agent documentation reconciliation — 27 November 2026

Pinned Agent [e2aac89](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/tree/e2aac89dafc2f8499e4e4d22ebed97cec75714fe/docs).
Retrieved all 14 non-index documents; reviewed introductions, section
inventories, selected boundary claims and targeted conflicting sections.
This is a targeted content audit, not exhaustive line-by-line verification
or source/runtime conformance testing. The earlier authority audit covers
docs/README.md.

| Document | Classification and disposition | Existing work |
|---|---|---|
| ARCHITECTURE.md | Mixed historical target and candidate design; authority note supersedes Proton/direct lake topology; verify plan, PDAG, dispatcher and multiplexer migration | C08/C12/C05 |
| AUDITD_LAUREL_KQL_TRANSFORM.md | Implementation reference; verify assembly, constituent fields and profile behavior; no edge canonicalization | C10/C12 |
| COLLECTION_COVERAGE_EVALUATION.md | Candidate coverage model; distinguish dispositions and external ground truth; historical ADR is not independent authority | C04/C12 |
| ENDPOINT_SCHEMA_EXPECTATIONS.md | Candidate CLI schema contract; remove dual Proton/DuckDB premise from target interpretation | C03/C13 |
| ETW_SCHEMA_BOUNDARIES.md | Implementation reference; native versus derived fields, provenance and lifecycle fixtures survive | C10/C12 |
| FORWARD_PROTOCOL_SPECIFICATION.md | Historical detailed wire reference; reliability guarantees contradicted by prior source audit; no wire change approved | C03/C05 |
| KQL_SUPPORT_BOUNDARY.md | Local engine reference; qualify pinned engine and shims independently of Platform | C12/C13 |
| LOG_UTILIZATION_AGENT_REQUIREMENTS.md | Candidate bounded observation contract; separate forwarding acceptance and final coverage evaluation | C04/C05/C12 |
| REALTIMEKQL_ETW_COMPARISON.md | Historical comparative implementation evidence; recheck library and session claims | C12 |
| REALTIMEKQL_INFLUENCES.md | Historical design rationale; NDJSON example not production Forward wire | C08/C12 |
| REALTIMEKQL_TABLE_HANDLING_COMPARISON.md | Historical comparison and candidate resource catalogue | C12/C13 |
| REALTIME_TABLE_STREAMING_GAP_ANALYSIS.md | Dated July 21 gap analysis; no independent active roadmap | C12/C13 |
| RPC_AGENT_PLATFORM_ALIGNMENT.md | Mixed implementation reference and candidate enrichment; ordering and lookup ownership require reconciliation | C10/C12 |
| RXKQL_CAPABILITY_MATRIX.md | Version-specific executable test reference; 3.5.3 claim and tests require current baseline verification | C14/C12/C13 |

## Specific discrepancies

| Finding | Evidence and disposition |
|---|---|
| AGDOC-01 | ARCHITECTURE calls itself authoritative and depicts Proton/direct DuckDB and collector decode before Agent topics. Its November 25 scope note already qualifies these. DEC-0033 and DEC-0022 govern; no topology migration claimed. |
| AGDOC-02 | FORWARD_PROTOCOL sections 8.2/8.4/8.5 describe safe credit shrink and admitted-UUID deduplication. The [delivery audit](2026-11-27-delivery-recovery-contract-review.md) identifies credit overgrant and pending duplicate ACK exposure. Admission is not durable acceptance; preserve wire reference but qualify reliability claims under C05. |
| AGDOC-03 | RPC alignment describes filter-then-enrich transitional ordering and an open target question. DEC-0009 requires unconditional state updates; output projection ordering is separate. DEC-0006/0007 place reconstructable lookup server-side; verify RPC lookup exception rather than assume one. |
| AGDOC-04 | ENDPOINT_SCHEMA_EXPECTATIONS retains Proton/DuckDB parity language; DEC-0033 retires that premise. Catalog logical type, nullability, precision and units remain relevant. |
| AGDOC-05 | Coverage evaluation acknowledges discardedCount ambiguity; retain explicit dispositions and distinguish local observation from external ground truth under DEC-0023. |
| AGDOC-06 | RealTimeKql comparison/gap plans and Rx.Kql capability matrix describe different dates and scopes. No historical phase completion or package version is treated as current test evidence. |

The [Agent acquisition contract](../architecture/AGENT-ACQUISITION-CONTRACT.md) centralizes surviving
boundary requirements and candidate distinctions. Local files are unchanged
during the documentation-first pass. C08/C12/C13 and related verification
remain open. Next inspect Platform documentation and legacy wiring.
