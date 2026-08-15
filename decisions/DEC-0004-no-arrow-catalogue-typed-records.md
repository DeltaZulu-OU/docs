---
id: DEC-0004
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D4
---

# DEC-0004 — No Arrow; catalogue-typed records with per-backend adapters

## Context

A shared intermediate representation between wire and sinks was considered, with Arrow the natural candidate.

## Decision

The collector holds catalogue-typed records and hands them to per-backend adapters. No Arrow, no shared intermediate.

## Consequences

Avoids a second typed representation between wire and sinks — one more place two engines could disagree. Costs DuckDB's zero-copy Arrow ingest, and leaves two adapters to test independently.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Arrow as internal representation | A second typed representation between wire and sinks, for a row-at-a-time landing path that does not benefit from columnar layout | — |

## Revisit trigger

If the collector becomes columnar-analytical in its own right rather than a row-at-a-time landing path, the arithmetic changes and Arrow should be re-argued. Recorded in `archive/RECOVERY.md` as recoverable.
