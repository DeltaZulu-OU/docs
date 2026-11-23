# Architecture

Per-repo and estate-wide architecture. Always current: these documents are
rewritten in place rather than superseded, because unlike Decisions they describe
what *is*, and there is only ever one present tense.

## Contents

| Document | Status |
|---|---|
| `PIPELINE.md` | The consolidated architecture, 15 August 2026. Supersedes the 12 August revision. **Imported verbatim and not edited.** |
| `PIPELINE-ERRATA.md` | Where Wave 0 verification found `PIPELINE.md`'s claims refuted, understated, mis-cited or unverified. |
| `DATA-QUALITY-MONITORING.md` | DQM rev. 2, 16 August 2026. Metrics, measurement points M0–M17 plus the external MX and MZ, and the eight quality planes. **Imported verbatim.** |
| `DATA-QUALITY-MONITORING-INTEGRATION.md` | What the DQM import changes about planned work. Its inventory has nine rows but **ten named provenance properties**; LocalStream replaces historical Proton dependencies. |
| `NRT-PIPELINE.md` | **Current target, 23 November 2026:** LocalStream/Query instead of Proton; binding replacement is `DEC-0033`. |
| `GOVERNING-DECISIONS.md` | Which Decisions govern which repository, generated from front-matter. |

`PIPELINE.md` is left unedited so that historical citations stay stable.
It is **not** the current processing architecture: its Proton statements are
superseded by `DEC-0033`. For the present design start with
`NRT-PIPELINE.md`; read `PIPELINE.md` together with `PIPELINE-ERRATA.md`
only to understand earlier reasoning.

Its D1–D21 register has been seeded into `decisions/` as `DEC-0001`–`DEC-0021`
under global numbering, which resolves the Agent-0014/Platform-0014 collision by
giving each decision a number that means one thing estate-wide.

## Per-repo architecture — pending migration

Existing architecture documents still live in their own repositories:

- `DeltaZulu.Agent/docs/` — ARCHITECTURE.md and 16 further documents
- `DeltaZulu.Platform/docs/` — including `docs/analytics/` and `docs/reviews/`
- `DeltaZulu.LocalStream/docs/LOCAL_STREAM_ARCHITECTURE.md`
- `DeltaZulu.Parse/docs/`

Per-repository documents may still describe earlier choices. Until reviewed
against `DEC-0033` and the global Decision set, treat them as implementation
references or historical plans, **not a second governing authority**. Their
migration and source-level rebaseline remain explicit roadmap work; the target
narrative above does not imply the LocalStream integration is implemented.
