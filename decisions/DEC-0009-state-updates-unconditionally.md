---
id: DEC-0009
status: Accepted
repos: [DeltaZulu.Agent]
governs:
  types: []
  paths: []
cites: []
supersedes: D9
---

# DEC-0009 — State machines update unconditionally, before filtering

## Context

Borrowed from LAUREL, whose documentation states that filtered events are still used for process tracking.

## Decision

Every event reaches the agent's state machines. Filtering (DEC-0008) applies only to what is transmitted, never to what state consumes.

## Consequences

A dropped process-creation record that never updates the process table causes every subsequent event referencing that PID to resolve wrongly. The corruption is silent and compounding, and its symptom is a plausible-looking process tree that is incorrect — the kind of defect that survives review precisely because the output looks right.

The saving from pre-filtering is small; the failure is unbounded. That asymmetry is the whole argument.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Filter before state update | Small CPU saving against unbounded, silent state corruption | — |

## Revisit trigger

None foreseen. If this is ever reopened, the burden is on showing that the state machines are not consulted for any downstream resolution.
