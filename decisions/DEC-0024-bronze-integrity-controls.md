---
id: DEC-0024
status: Proposed
repos: [DeltaZulu.Platform]
governs:
  types: []
  paths: []
cites: [CON-0020]
---

# DEC-0024 — Bronze carries integrity controls, not just a retention setting

## Context

Bronze is described throughout the architecture as retained evidence for
compliance and replay. Nothing in the design demonstrates that the evidence is
still what was written. CON-0020 explains why that gap closes at write time or
not at all.

## Decision

Three controls, in ascending cost, all of which the collector must be designed
around rather than have added later:

1. **A payload digest computed at M12** and stored beside the Bronze record. One
   hash per record; makes silent alteration detectable at read time.
2. **A signed per-partition manifest** covering the file list and their digests.
   This is what detects *deletion*, which a per-record digest cannot.
3. **Scheduled restore testing against the oldest retained partition.** Restoring
   yesterday proves nothing about eleven months ago, and this is the only control
   that establishes the retention claim is true.

For a regulated deployment the second and third are not optional. The third is
the one most often skipped, because it is operational rather than architectural.

## Consequences

- The collector (`DEC-0022`) acquires a write-path requirement it did not have.
- The measured RTO becomes a fact rather than a policy statement.
- Any digest mismatch is an **integrity incident**, not a quality metric, and
  belongs on a different escalation path from the rest of this instrumentation.
- Open: manifest signing needs a key custody model a managed-service operator can
  hold without being able to forge a manifest. The obvious answers trade a
  customer-held key with a support burden against an operator-held key with a
  weaker assurance claim. That is a commercial decision as much as a technical
  one, and it is not resolved here.

## Alternatives rejected

| Alternative | Why not | Constraint it failed |
|---|---|---|
| Rely on Parquet page CRCs | Detect corruption, not modification | CON-0020 |
| Compute digests during a later verification sweep | Attests to what is there now, not what was written | CON-0020 |
| Per-record digests alone | Cannot detect deletion — a removed record leaves no digest | CON-0020 |
| Treat configured retention as the control | A policy setting is not a demonstration | CON-0020 |

## Revisit trigger

Reopen if the lake gains native immutability or write-once semantics that make
external attestation redundant, or if a customer's regulatory regime dictates a
specific attestation scheme.
