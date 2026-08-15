# Roadmaps

Forward plans. **Every roadmap carries a dated review trigger** — a date by which
someone looks at it again and either advances it or records why it stalled. A
roadmap without one becomes an archaeological artefact that still reads as a
commitment.

## Pending migration

Roadmaps still live in their own repositories. Known corrections to apply when
they move, each already identified:

| Roadmap | Correction |
|---|---|
| LogCluster | Proposes `LiblognormParserDescriptor`; Parse shipped `ParserDescriptor`. The roadmap names a type that was never built under that name. |
| Forward | Asks a question that Agent ADRs 0014 and 0015 already answered. |
| Forward | Carries an empty "no fallback wire format" heading — a constraint with a title and no body. |
| DurableBuffer | Has no ADR record at all, despite being a published package. |

The Forward empty-heading case is worth noting beyond its own fix: a heading
asserting a constraint, with nothing under it, is indistinguishable from a
constraint that was decided and then lost. It has to be treated as unrecorded.
