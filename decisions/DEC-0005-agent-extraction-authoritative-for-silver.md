---
id: DEC-0005
status: Accepted
repos: [DeltaZulu.Parse]
governs:
  types: [KqlType]
  paths: [src/DeltaZulu.Parse/KqlType.cs]
cites: []
supersedes: D5
---

# DEC-0005 — Agent extraction is authoritative for Silver

## Context

The agent must parse anyway in order to evaluate `filter.query`. The question is whether the server discards that work and reparses.

## Decision

Fields extracted on the endpoint are authoritative for Silver. The server does not reparse.

**Platform ADR 0007's clause stating that agents do not map into Silver or enrichments contradicts this and must be struck.**

**Boundary clarification (2026-11-25):** JSON field projection, typed decoding and canonical mapping are not by themselves evidence of discarded endpoint extraction. Current Silver contributors read `raw_log`; C10 must trace Agent → Forward → Bronze → Silver to establish whether declared agent fields survive. The rule against routinely discarding authoritative endpoint extraction remains binding. Direct non-agent source handling and assurance/replay exceptions must be explicitly scoped; no new exception is approved here.

## Consequences

Discarding and reparsing would double CPU for no gain. Silver's quality becomes a function of the agent generation that produced each row, which is why the reparse sample (a stratified ~1% of Bronze) exists as an assurance mechanism rather than a correction mechanism.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Server-side reparse from Bronze | Doubles CPU; the agent has already parsed to filter | — |
| Agent sends raw only | Loses the typing established at PDAG compile time | — |

## Revisit trigger

If agent-side parser defects are found at a rate the stratified reparse sample cannot absorb, server-side reparse becomes the cheaper correctness mechanism and this should be reopened.
