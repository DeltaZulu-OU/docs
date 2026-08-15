---
id: CON-0016
status: Accepted
subject: Collector ownership
---

# CON-0016 — The collector has no repository

The collector — the component that terminates the Forward transport and lands
rows — exists in design and in discussion, but not as a repository, a project,
or a directory anywhere in the estate.

## Consequences

- No Decision set governs the ingestion path, because governance attaches to
  repositories and there is no repository to attach to. Decisions about the
  collector currently land wherever the discussion happened.
- This is an organisational fact with a technical consequence, and it blocks
  more than it appears to: the dual-send design's Silver-to-Bronze join, the
  wire-version negotiation rollout, and the golden-placement question all name
  the collector as the component that does the work.
- Choosing its home is therefore a prerequisite to those decisions, not a
  tidying task that can follow them.
