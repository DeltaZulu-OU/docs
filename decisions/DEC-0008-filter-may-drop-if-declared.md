---
id: DEC-0008
status: Accepted
repos: [DeltaZulu.Agent]
governs:
  types: []
  paths: []
cites: []
supersedes: D8
---

# DEC-0008 — Filter may drop; must be declared, versioned, counted

## Context

Endpoint volume control is a real deployment requirement, and dropping at the edge is the same category of decision as an auditd ruleset or a Sysmon configuration — both discard events before any agent sees them.

## Decision

`filter.query` may drop events. Every drop is declared in a versioned, exportable statement of the collection boundary, and counted.

## Consequences

What makes dropping acceptable is that the boundary is *stated* rather than emergent. An uncounted drop is indistinguishable from an absence, which is the failure this whole design is organised against.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| No edge filtering | Volume control is a genuine deployment requirement | — |
| Undeclared filtering | An uncounted drop destroys the absent-versus-negative-evidence distinction | — |

## Revisit trigger

If drop counters show a filter discarding materially more than its author expected, the declaration is wrong rather than the counter — reopen the profile, not this Decision.
