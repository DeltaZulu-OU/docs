# Agent acquisition and endpoint boundary

Current target interpretation of Accepted DEC-0005–0009, DEC-0014–0016,
DEC-0032/0033/0037/0038. This is not a claim of runtime conformance.
See the [source-document reconciliation](../reports/2026-11-27-agent-documentation-reconciliation.md) for inherited
requirements and unresolved implementation questions.

## Ownership and ordering

Acquire and frame source records, preserve native facts and acquisition
identity, structurally extract plaintext through Parse, and distinguish
native decoding from semantic normalization. Endpoint extraction is
authoritative for Silver; Platform maps canonical names and reconstructable
lookup enrichment. Preserve raw evidence and extraction lineage.
Only endpoint-perishable context belongs to Agent enrichment.

Every acquired event reaches applicable state machines before transmission
filtering under DEC-0009. Version and count declared filter drops under
DEC-0008. State update and output projection are distinct: the exact
position of output enrichment relative to filtering is not settled by
the historical RPC document. Reconstructable RPC operation-name lookup
belongs server-side unless an explicit exception is approved. Preserve
native interface/opnum and perishable context without inventing locality.

Forward owns inter-node typed MessagePack delivery. LocalStream is a
node-local payload-opaque substrate; DurableBuffer is an optional edge
queue. Platform owns the separate collector and DuckLake evidence.
No Proton or direct Agent lake sink is part of the target.
The two-topic Agent topology, parser-domain PDAG and coordinated dispatcher
are inherited candidate implementation details requiring C12 source and
test reconciliation, not newly approved requirements.

## Source schemas and local queries

Keep native ETW envelope/payload fields distinct from decoded, correlated
and enriched fields; retain provenance, source/schema versions and
explicit unresolved context. DEC-0014/0015 govern Windows collection and
derived process identity. Auditd assembly and native record grouping
must preserve constituent evidence and extraction lineage; verify
current parser/profile behavior before claiming support.

The local Rx.Kql profile and workbench engine is not the Platform detection
language contract. Qualify the pinned package, compatibility shims,
resource binding and actual profile execution separately from Platform
Kusto.Language binding. Local table aliases and schema navigation do not
establish Gold tables or multi-stream execution. Preserve the historical
resource catalogue, CLI discovery, daemon/workbench parity and schema
fixtures as C12/C13 candidates pending source verification.

## Coverage and management

Agent emits bounded source health, collection, filter and delivery facts;
Platform owns coverage evaluation, rule applicability and analyst verdicts.
Do not collapse parser no-match, declared filtering, operational failure,
unavailable source and unknown coverage into one discard counter.
A local counter is not ground truth; external canaries and explicit
unmeasurable sources remain governed by DEC-0023. Delivery success must
follow the qualified C05 durable acceptance boundary. Collection tier,
field provenance and closed null reasons remain required under DEC-0016.

Agent does not own detection rules, suppression, severity, tenant-wide
lookup or analyst alert identity. Management-plane security and CLI
qualification remain C17/C13. No new product scope or wire change is
authorized by this specification.
