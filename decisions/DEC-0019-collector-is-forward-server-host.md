---
id: DEC-0019
status: Accepted
repos: [DeltaZulu.Forward]
governs:
  types: []
  paths: []
cites: [CON-0016]
supersedes: D19
---

# DEC-0019 — Collector is the Forward server host

## Context

Removing the message broker moved four properties onto the collector: the durable buffer between collector and sinks, cursoring and replay, backpressure, and fan-out.

## Decision

The collector is a hosting shell around `DeltaZulu.Forward`'s server side. It terminates the transport, decodes once (principle 5.2), and writes three destinations.

## Scope clarification — 2026-11-23

DEC-0033 makes LocalStream the **in-process/node-local** streaming substrate,
not an external broker between nodes. This does not reverse the rejection of a
standalone Kafka-like operational dependency. Forward remains inter-node
transport, and the collector's target downstreams are local replay processing
and durable lake writes, not Proton. The original three-destination wording
below is a historical count, not a requirement to restore any Proton sink.

## Consequences

Fan-out to multiple consumers is **not available** — one consumer per sink. The backpressure path is architecturally clean, since the transport already defines window-adjustment `Control` frames, so sink slowness propagates to the endpoint as flow control rather than as silent spool growth.

**Ownership is resolved, implementation remains incomplete.** `CON-0016` recorded the original absence of a collector home. `DEC-0022` subsequently placed the collector in `DeltaZulu.Platform` as a separate deployable. The inspected Platform tree contains `DeltaZulu.Platform.Ingestion` as a library project, but not the required standalone collector executable. The original ownership memo is no longer open; validating and implementing its executable boundary remain engineering work.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Message broker between collector and sinks | Adds an operational dependency whose properties the spool now provides | — |
| Ingest endpoint inside the Platform Web host | Conflates the control plane with the telemetry plane | — |

## Revisit trigger

Revisit if fan-out to multiple independent consumers per sink becomes a requirement — that is the property the broker provided and the spool does not.
