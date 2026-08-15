# Archive

Per-repo ADRs as they stood when the estate moved to a single governed
Decision set. **Content is unchanged** — these files are copies, not edits.

## These are historical, not individually superseded

The whole set is marked historical at once. No attempt has been made to walk
each ADR and decide whether some later Decision replaces it, because that
walk is what the seeded `DEC-NNNN` register does, and doing it twice would
produce two answers.

Treat an archived ADR as evidence of what was decided and why at the time. Do
not treat it as current, do not cite it as authority, and do not resolve a
disagreement between an archived ADR and a Decision in favour of the ADR.

| Repository | ADRs archived |
|---|---|
| `DeltaZulu.Agent/` | 18 + README |
| `DeltaZulu.Platform/` | 16 + README |
| `DeltaZulu.LocalStream/` | 12 + README |
| `DeltaZulu.Parse/` | 5 |

`DeltaZulu.Forward`, `DeltaZulu.LogCluster` and `DeltaZulu.DurableBuffer` had no
`docs/adr/` directory to archive. DurableBuffer's missing ADR record is itself a
finding — it is a published package with no recorded decisions at all.

## Numbering collisions this archive preserves

The archive keeps the original numbers, so the collisions that motivated global
numbering are visible here rather than hidden:

- **Agent ADR 0014** (*MessagePack is the type-contract wire format; Avro is
  superseded*) and **Platform ADR 0014** (*HTTP ingestion and type-fidelity
  registry*) are different decisions sharing a number, and both are cited as
  "ADR 0014" in prose.
- **The Agent carries two ADR 0003 documents**:
  `0003-parser-dispatch-and-relp-native-boundaries.md` and
  `0003-profile-kql-preserves-source-event-shape.md`. A citation to "Agent ADR
  0003" does not resolve.

See `RECOVERY.md` for what is recoverable from these files and what should be
re-examined before it is trusted.
