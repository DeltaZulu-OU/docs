# Architecture

Per-repo and estate-wide architecture. Always current: these documents are
rewritten in place rather than superseded, because unlike Decisions they describe
what *is*, and there is only ever one present tense.

## Pending import — `PIPELINE.md`

The consolidated architecture document is intended to land here as
`architecture/PIPELINE.md`, superseding the 12 August revision, and its D1–D21
register is intended to seed `decisions/` renumbered to global `DEC-NNNN`.

**That document has not been provided to this repository and is not reproduced
here.** Writing it from memory would produce something that reads like the
original and differs from it in unknowable places, which is worse than its
absence.

Blocked on the import:

- `decisions/` seed set (D1–D21 → `DEC-NNNN`), and with it the resolution of
  gap 15's Agent-0014/Platform-0014 collision.
- The Golden placement memo (section 9, options A–D), which cannot be written
  against options this repository does not have.
- Section 11.1's divergence list, which the schema-authority work consumes.

## Per-repo architecture — pending migration

Existing architecture documents still live in their own repositories and have not
been moved:

- `DeltaZulu.Agent/docs/` — ARCHITECTURE.md and 16 further documents
- `DeltaZulu.Platform/docs/` — including `docs/analytics/` and `docs/reviews/`
- `DeltaZulu.LocalStream/docs/LOCAL_STREAM_ARCHITECTURE.md`
- `DeltaZulu.Parse/docs/`

Migration is deliberately not done ahead of the `PIPELINE.md` import: moving them
first would mean reconciling each against a consolidated document that is not
here to reconcile against.
