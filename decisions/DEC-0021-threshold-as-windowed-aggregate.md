---
id: DEC-0021
status: Proposed
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D21
---

# DEC-0021 — Detection threshold expressed inside the KQL as a windowed aggregate

## Context

"Alert on at least N matches" is ambiguous in a continuously updating view: a cumulative count crosses the threshold once and stays crossed.

## Decision

The threshold is expressed inside the KQL as a windowed aggregate with a predicate, rather than as a separate engine-specific scalar.

## Consequences

If adopted, the threshold must be explicit in the authored KQL, bound and tested using LocalStream.Query operators under DEC-0033. No Proton/DuckDB dual-dialect compilation is planned. The exact window, late-arrival, correction and output semantics remain Proposed and require conformance fixtures.

**Status stays `Proposed`: the exact window semantics are not settled.**

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Engine-specific scalar alongside the rule | Invisible to the author; translates differently per engine | — |
| Cumulative count | Crosses once and stays crossed | — |

## Revisit trigger

Settle the window semantics before the first threshold rule is authored, or existing rules will encode whichever reading the implementation happened to take.
