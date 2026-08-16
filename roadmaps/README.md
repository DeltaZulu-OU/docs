# Roadmaps

Forward plans, migrated here on 2026-08-16 from the repositories that used to
carry them. **Every roadmap carries a dated review trigger**, and the trigger is
a condition as well as a date — a roadmap without one becomes an archaeological
artefact that still reads as a commitment.

| Roadmap | Origin | Next review |
|---|---|---|
| `DeltaZulu.Agent-ROADMAP.md` | `DeltaZulu.Agent/docs/ROADMAP.md` | 2026-11-16 |
| `DeltaZulu.Agent-DZAGENTCTL_CONTROLLER_ROADMAP.md` | `DeltaZulu.Agent/docs/` | 2026-11-16 |
| `DeltaZulu.Forward-ROADMAP.md` | `DeltaZulu.Forward/ROADMAP.md` | 2026-11-16 |
| `DeltaZulu.LogCluster-ROADMAP.md` | `DeltaZulu.LogCluster/docs/ROADMAP.md` | 2026-11-16 |
| `DeltaZulu.Platform-ROADMAP.md` | `DeltaZulu.Platform/docs/ROADMAP.md` | 2026-11-16 |
| `DeltaZulu.Platform-AGENT_MANAGEMENT_ROADMAP.md` | `DeltaZulu.Platform/docs/` | 2026-11-16 |

`DeltaZulu.Kql`, `DeltaZulu.LocalStream` and `DeltaZulu.DurableBuffer` have no
roadmap. For the first two that is reasonable — both are complete libraries with
narrow surfaces. For DurableBuffer it is part of a wider gap: it is a **published
package with no ADR record and no roadmap at all**, so nothing states what it has
decided or where it is going.

## Corrections applied on migration

Corrections are appended to each file rather than edited into its body, so the
original text stays legible and the correction is visibly a later act.

- **Forward** asks whether the Agent's description of "RELP-derived text
  transport and Avro payloads" is stale. It is — answered by `DEC-0001` and
  `DEC-0004` (Agent ADRs 0014 and 0015, which superseded ADR 0010's Avro and
  Arrow choices). The question predates its answer, and no reconciliation ADR is
  needed.
- **LogCluster** proposes a `LiblognormParserDescriptor` type and an interface
  around it. Parse shipped `ParserDescriptor`, in `ParserCatalog.cs`. Work
  planned against the proposed name has to be re-read against the shipped one.
- **LogCluster** also carries the counter-width defect (`int` counters against
  `long` inputs, wrapping above `int.MaxValue` and yielding `NaN` from
  `Math.Log(1 + recordCount)`) and now records that dropping `v2-iptables` or
  `cisco-interface-spec` costs 20 cases of committed parity coverage, not the 1
  case an earlier undercount suggested.

## One claim refuted

Forward's **"Constraint: no fallback wire format" section is not an empty
heading.** It has been described that way — as "a constraint with a title and no
body", which would make it indistinguishable from a constraint decided and then
lost. It is complete, with its justification, and reads:

> Do not add NDJSON or another degraded outage format to Forward. Spooling and
> replay belong in the caller's transport adapter […]; a fallback here would
> become a second permanent consumer contract and undermine type fidelity.

The live question about that constraint is not whether it was recorded but how
far it reaches: it is scoped to Forward by its wording, and
`DeltaZulu.Platform.Ingestion.RawLogNdjsonCodec` sits outside that scope. See
`DEC-0022`.
