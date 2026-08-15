---
id: DEC-0015
status: Accepted
repos: [DeltaZulu.Agent]
governs:
  types: []
  paths: []
cites: []
supersedes: D15
---

# DEC-0015 — Uniform derived `ProcessKey` by documented precedence

## Context

Sysmon's `ProcessGuid` is Sysmon-scoped and exists nowhere else on the host, so a network event captured by the agent's own ETW consumer cannot join to it.

## Decision

A single derived `ProcessKey` resolves by documented precedence — start key, then `ProcessGuid`, then a host-boot-PID-start-time composite — with all components retained.

## Consequences

Without a uniform key, hosts that gain Sysmon or lose ETW mid-stream produce records that do not join against their own earlier records, and process trees fragment at exactly the boundary least expected. The start key is system-scoped and available at every tier, which is why it leads the precedence.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| `ProcessGuid` as the spine | Sysmon-scoped; unavailable to the agent's own ETW consumer | — |
| PID plus creation time only | Not reuse-immune | — |

## Revisit trigger

If Windows changes the start key's availability or semantics, the precedence order must be re-derived rather than patched.
