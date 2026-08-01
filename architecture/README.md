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
| `DATA-QUALITY-MONITORING-INTEGRATION.md` | What the DQM import changes about planned work — chiefly that FWD-CONTRACT-v2's record-field set grows from three to nine, all irreversible. |
| `NRT-PIPELINE.md` | The phase-one near-real-time architecture, 17 August 2026. Rewritten in place; `DEC-0026`-`DEC-0031` are its binding form. |
| `GOVERNING-DECISIONS.md` | Which Decisions govern which repository, generated from front-matter. |

`PIPELINE.md` is left unedited so that citations to it stay stable and so that
what was believed at import time remains legible. Corrections live alongside it
rather than inside it. Read both.

Its D1–D21 register has been seeded into `decisions/` as `DEC-0001`–`DEC-0021`
under global numbering, which resolves the Agent-0014/Platform-0014 collision by
giving each decision a number that means one thing estate-wide.

## Per-repo architecture — pending migration

Existing architecture documents still live in their own repositories:

- `DeltaZulu.Agent/docs/` — ARCHITECTURE.md and 16 further documents
- `DeltaZulu.Platform/docs/` — including `docs/analytics/` and `docs/reviews/`
- `DeltaZulu.LocalStream/docs/LOCAL_STREAM_ARCHITECTURE.md`
- `DeltaZulu.Parse/docs/`

Migration is Session 19 work. It is deliberately not done ahead of the Decision
set stabilising: each document has to be reconciled against the Decisions that
now govern it, and reconciling against a moving set means doing it twice.
