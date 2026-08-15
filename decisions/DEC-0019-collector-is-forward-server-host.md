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

## Consequences

Fan-out to multiple consumers is **not available** — one consumer per sink. The backpressure path is architecturally clean, since the transport already defines window-adjustment `Control` frames, so sink slowness propagates to the endpoint as flow control rather than as silent spool growth.

**CON-0016 applies: the collector has no repository.** This Decision names what the collector is without naming where it lives, which is why the ownership question is a separate open memo.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Message broker between collector and sinks | Adds an operational dependency whose properties the spool now provides | — |
| Ingest endpoint inside the Platform Web host | Conflates the control plane with the telemetry plane | — |

## Revisit trigger

Revisit if fan-out to multiple independent consumers per sink becomes a requirement — that is the property the broker provided and the spool does not.
