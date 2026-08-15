---
id: DEC-0014
status: Accepted
repos: [DeltaZulu.Agent]
governs:
  types: []
  paths: []
cites: []
supersedes: D14
---

# DEC-0014 — Windows: ETW Kernel-Process always on; Sysmon recommended, never assumed

## Context

Sysmon supplies materially more than Security Event 4688, but cannot be assumed present. Two findings shape the fallback: Windows exposes a process start key giving reuse-immune identity without Sysmon, and ETW is higher-integrity than the Security log for the same event — 4688 is dispatched by the kernel to `lsass.exe`, so it can be tampered with from within that process, whereas `Microsoft-Windows-Kernel-Process` `ProcessStart` is logged directly by the kernel.

## Decision

ETW Kernel-Process is always enabled and forms the spine. Sysmon is recommended and never assumed. Three tiers (A: Sysmon EID 1, B: ETW plus userland enrichment, C: Security 4688) are stamped onto every record.

## Consequences

The honest residual caveat is a *bias*, not a percentage: userland enrichment misses concentrate on short-lived processes, which is where a good deal of malicious activity lives. Sysmon avoids this because its driver callback runs synchronously in the creating thread's context; a userland ETW consumer is asynchronous by construction and cannot.

Fields split by where they come from rather than by process lifetime, which makes the fallback stronger than it first appears: hashes and `OriginalFileName` are read from the image file and survive process exit.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Require Sysmon | Cannot be assumed across a managed fleet | — |
| 4688 only | LSASS-mediated, materially less complete, command line only when audit policy allows | — |

## Revisit trigger

Build Tier B only after measuring the short-lived-process miss rate. If ETW hooking, PEB reads and image hashing start turning the agent into an EDR-adjacent sensor, that scope creep is the trigger to stop and re-argue.
