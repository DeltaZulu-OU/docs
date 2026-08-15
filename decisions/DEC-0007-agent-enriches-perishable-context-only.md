---
id: DEC-0007
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D7
---

# DEC-0007 — Agent enriches only perishable local context

## Context

One question decides what belongs in agent-side enrichment: can the server reconstruct this from retained data an hour from now?

## Decision

The agent adds only what exists nowhere else: process lineage, session identity, container and namespace membership, socket-to-process ownership. Everything reconstructable is server-side (DEC-0006).

## Consequences

Process lineage and session identity cannot be reconstructed from a log line after the fact, so the endpoint is the only place they exist at all. This is why DEC-0009's unconditional-state rule matters: the state feeding this enrichment must see every event.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Full agent-side enrichment | Fleet-wide distribution of volatile data; semantic changes unappliable retroactively | — |
| No agent-side enrichment | Perishable context is lost permanently | — |

## Revisit trigger

If an enrichment currently classed as perishable becomes reconstructable — for example because the state itself is shipped and retained — it moves server-side.
