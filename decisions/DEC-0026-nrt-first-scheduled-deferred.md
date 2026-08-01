---
id: DEC-0026
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: []
---

# DEC-0026 — Phase one builds the NRT path only; scheduled detections are deferred

## Context

The rule catalogue can express detections that run continuously and detections
that run on a schedule. Building both at once means the first release carries two
execution models, two deployment mechanisms and two sets of operational
behaviour, before either has been observed under load.

The NRT path is the one that determines whether the architecture works at all: it
exercises the transport, the durable buffer, the Gold contract, replay, and alert
identity. The scheduled path exercises none of those independently.

## Decision

Phase one builds the near-real-time path only. Rule metadata permits the **NRT
execution type and no other**, and no scheduled-task deployment mechanism is
built.

Threat hunting against DuckLake is unaffected and is not a scheduled detection.
The same KQL that transpiles to Proton SQL for continuous detection also
transpiles to DuckDB for hunting and offline validation. Being able to run a rule
over history interactively is not the same capability as scheduling it, and the
metadata must not blur them.

Scheduled detections, scheduled-rule metadata and scheduled-task deployment are
revisited once the NRT pipeline has demonstrated its latency, correctness, replay
behaviour and operational characteristics.

## Consequences

- Detections that are genuinely periodic — long-window aggregations, low-frequency
  correlation — have no home in phase one. Some of these are real detections that
  customers will ask for, and the answer for now is hunting rather than alerting.
- Rule metadata carries an execution-type field with one legal value. That looks
  redundant and is not: it is the extension point, and adding it later would mean
  rewriting every rule already authored.
- The NRT path gets the whole of the team's operational attention during the
  period when its failure modes are least understood.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Build both execution types together | Doubles the deployment and operational surface before either model has been observed under load, and the scheduled path depends on nothing the NRT path does not already prove | — |
| Build scheduled first, NRT later | Scheduled execution over DuckLake would work without the buffer, the Gold contract or replay, so it would defer every hard question rather than answer one | — |
| Omit the execution-type field until it is needed | Retrofitting it means rewriting every rule authored before it existed | — |

## Revisit trigger

Reopen when the NRT pipeline has run in production long enough to characterise
its latency, replay and failure behaviour — or earlier if a detection class that
cannot be expressed continuously becomes a delivery commitment rather than a
preference.
