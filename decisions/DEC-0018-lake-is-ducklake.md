---
id: DEC-0018
status: Accepted
repos: []
governs:
  types: []
  paths: []
cites: []
supersedes: D18
---

# DEC-0018 — Lake is DuckLake with a SQL catalogue database

## Context

The lake must support concurrent readers and writers across processes. An embedded DuckDB file does not, and Quack remains a beta extension not expected to mature until DuckDB 2.0 in autumn 2026.

## Decision

The lake is DuckLake — Parquet data with metadata in a SQL catalogue database — not an embedded DuckDB file.

## Consequences

Catalogue choice is a deployment decision, not a detail: SQLite hides the single-writer model adequately for multiple local clients, while multiple collectors want PostgreSQL. Under sustained concurrent write load the commit retry budget can be exhausted, making batch sizing and commit frequency tuning parameters.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Embedded DuckDB file | No concurrent multi-process access | — |
| DuckDB plus Quack | Beta extension; maturity not expected until DuckDB 2.0 | — |

## Revisit trigger

If DuckLake's backward-compatibility guarantee is broken in a major version, or write contention proves unmanageable at target volume, reopen.
