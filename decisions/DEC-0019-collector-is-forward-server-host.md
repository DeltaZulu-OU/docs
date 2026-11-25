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

LocalStream supports independent named subscriptions under DEC-0033; the historical one-consumer-per-sink limitation does not describe the target. Forward transport credits, collector acceptance, durable append, downstream commits and retention are distinct boundaries. Credit adjustment alone does not prove durable acceptance or propagation of backpressure across the complete path. C05 verifies these properties, including independent subscribers, slow consumers, retry, expiry and crash recovery.

**Ownership is resolved, implementation remains incomplete.** `CON-0016` recorded the original absence of a collector home. `DEC-0022` subsequently placed the collector in `DeltaZulu.Platform` as a separate deployable. The inspected Platform tree contains `DeltaZulu.Platform.Ingestion` as a library project, but not the required standalone collector executable. The original ownership memo is no longer open; validating and implementing its executable boundary remain engineering work.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Message broker between collector and sinks | Adds an operational dependency whose properties the spool now provides | — |
| Ingest endpoint inside the Platform Web host | Conflates the control plane with the telemetry plane | — |

## Revisit trigger

Revisit if node-local subscriptions and Forward transport cannot meet measured fan-out, retention or recovery requirements without a different boundary.
