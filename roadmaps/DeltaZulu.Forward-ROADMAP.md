# Roadmap and integration gates

DeltaZulu.Forward's binary framing, typed handshake, credit-window flow
control, UUID deduplication, schema exchange, and logging provider are already
implemented. Remaining work is primarily integration and operational
validation rather than construction of another Forward state machine.

## Cross-repository reconciliation

Before planning DeltaZulu.Agent integration, reconcile its description of a
RELP-derived text transport and Avro payloads with this repository's fixed
16-byte binary header and MessagePack `ForwardLogBatch` contract. Determine
whether the Agent documentation is stale, Avro names a separate future catalog
encoding, or the repositories need a design-reconciliation ADR. Pending that
decision, scope Agent work as wiring the daemon to `ForwardSession` and
`ForwardConnection`, not reimplementing the protocol.

When DeltaZulu.Platform's schema-versioning work is designed, evaluate how
rule-to-parser-version binding composes with Forward's fingerprint negotiation
and `SchemaRequest`/`SchemaResponse` exchange. Transport schema discovery and
rule compatibility are adjacent guarantees, not interchangeable ones.

## Delivery correctness gate

Collectors may provide one shared `ForwardDedupWindow` to successive accepted
sessions, protecting reconnect redelivery while the process and bounded entry
remain alive. That is not durable idempotency. Before production alert
materialization, verify end to end that a batch acknowledged immediately before
a disconnect cannot be applied twice after either reconnect or collector
restart. The durable ingest layer must key its independent idempotency check on
the batch UUID.

## Production framework gate

The package currently targets `net10.0`. Production adoption by
DeltaZulu.Agent requires the maintainers to validate that deployment runtime
and explicitly decide whether the package also needs to multi-target another
framework.

## Constraint: no fallback wire format

Do not add NDJSON or another degraded outage format to Forward. Spooling and
replay belong in the caller's transport adapter (for example,
`DeltaZulu.DurableBuffer`); a fallback here would become a second permanent
consumer contract and undermine type fidelity.

---

## Corrections applied on migration (2026-08-16)

**The "Cross-repository reconciliation" question is answered.** It asks whether
the Agent's description of "RELP-derived text transport and Avro payloads" is
stale, whether Avro names a separate future catalog encoding, or whether a
design-reconciliation ADR is needed.

Answered: the Agent's description is **stale**. Avro was chosen in Agent ADR 0010
and superseded by ADR 0014 in favour of MessagePack, now `DEC-0001`; Arrow was
likewise superseded by ADR 0015, now `DEC-0004`. Both are recorded as recoverable
rejections in `archive/RECOVERY.md`. No reconciliation ADR is required — the
question predates the answer. Scope Agent work as wiring the daemon to
`ForwardSession` and `ForwardConnection`, exactly as the section already
concludes.

**The "Constraint: no fallback wire format" section is complete.** It has been
described elsewhere as an empty heading; it is not, and never was. The constraint
is stated with its justification.

Note that the constraint is scoped to Forward by its wording, and
`DeltaZulu.Platform.Ingestion.RawLogNdjsonCodec` exists outside that scope. Today
its only consumers are a DuckDb seeding converter and tests, so it is not a
violation. See `DEC-0022` for why that boundary should be stated explicitly
before the collector is built beside it.

**The delivery-correctness gate is still open** and is now tracked as part of
FWD-CONTRACT-v2 item 3 — durable dedup keyed on the batch UUID, independent of
the process-lifetime `ForwardDedupWindow`.

---

## Review trigger

**Next review: 2026-11-16.** Migrated to `DeltaZulu-OU/docs` on 2026-08-16 from
its origin repository, which no longer carries a copy.

Review earlier than the date above if any of these happen:

- a Decision this roadmap depends on changes status in `decisions/`;
- a phase named here completes, or is found to have been overtaken;
- a claim in it is contradicted by the code, as several already were.

A roadmap with no review date becomes an archaeological artefact that still reads
as a commitment. That is what this section exists to prevent.
