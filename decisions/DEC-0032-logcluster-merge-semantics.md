---
id: DEC-0032
status: Proposed
repos: [DeltaZulu.LogCluster]
governs:
  types: []
  paths: []
cites: []
---

# DEC-0032 — Select LogCluster merge semantics using measured evidence

## Context

DeltaZulu.LogCluster has the frequent-anchor mining model of Perl LogCluster, but its default edge and low-diversity merges are not equivalent to upstream default behavior. Current merging can combine semantically distinct messages, including state transitions and success/failure variants. Reliable parser suggestions depend on preserving source meaning and round-tripping rendered executable rules. The proposed default must therefore be chosen using pinned upstream parity cases and independent ground-truth accuracy. P3 and P5 correctness gates precede this change.

## Decision

**Unresolved — Proposed.** No default merge mode or heuristic replacement is authorised by this document yet.

The implementation is to expose `none`, `edge`, `variants`, and `all`, with `none` matching the unmerged upstream fixtures. After P6 proves that parity and P7 measures ground-truth accuracy by mode, record a single default and its compatibility impact here. Do not change the shipped default until the Decision is Accepted.

The Decision must also choose one low-diversity rule: at least three distinct variant values, a parser-motif gate, or per-candidate word dependency. It must choose an edge rule: retain the specific candidate and credit support to the general candidate, or require the absorbed word to fit an observed gap envelope. The accepted implementation must keep `up` separate from `down` and `login` separate from `login failed`, while allowing recurring IP values to merge where meaningful.

## Consequences

Explicit modes separate upstream baseline compatibility from heuristic optimization. Changing the default may alter produced patterns, support distribution, rule executability, or existing downstream snapshots. Additional merge machinery also has time and memory costs. The accepted choice requires versioned CLI documentation, migration guidance, and regression tests.

## Alternatives rejected

No alternative is rejected while this Decision is Proposed. The eventual accepted revision must list each evaluated mode and heuristic with the measured accuracy, implementation cost, and reason for rejection.

| Alternative under evaluation | Main concern | Evidence needed |
| --- | --- | --- |
| None | Leaves related variants separate | Upstream parity and false-split rate |
| Edge | May collapse distinct trailing/leading semantics | Ground-truth errors and gap-width validation |
| Variants | Diversity ratio does not encode meaning | State-word false merges and recurring-IP accuracy |
| All | Combines both error surfaces | Joint mismerge rate and support conservation |
| Minimum three distinct values | Cheap but semantic blindness remains | Precision across categorical vs IP fields |
| Motif gate | Couples merging to parser classification | Catalog availability and false-positive motifs |
| Per-candidate dependency | Additional state and CPU | Accuracy improvement versus allocation |

## Revisit trigger

After acceptance, reopen when a pinned parity suite drops below 100% in `none` mode, or when ground-truth template F1 under the selected default decreases by at least 2 percentage points on the same versioned corpus and evaluation procedure. These thresholds are review triggers, not acceptance thresholds for the initial choice.
