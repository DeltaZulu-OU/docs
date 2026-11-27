# Remaining component documentation reconciliation — 27 November 2026

Retrieved all nine remaining non-index Markdown documents at the pinned
revisions below. Inspected introductions, section inventories and selected
claims; not an exhaustive line-by-line audit or runtime test.

| Component | Pinned document | Classification | Work |
|---|---|---|---|
| Parse | [COMPARISON.md](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/blob/731b5b1d77696e1eff9cf24c4e26561d31b7a93b/docs/COMPARISON.md) | Pinned upstream audit; distinguish confirmed divergence from unresolved gaps | C12/C14 |
| Parse | [PACKAGE_README.md](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/blob/731b5b1d77696e1eff9cf24c4e26561d31b7a93b/docs/PACKAGE_README.md) | Version-specific pilot feed instructions; verify published identity | C14 |
| Parse | [RULEBASE_SEMANTICS.md](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/blob/731b5b1d77696e1eff9cf24c4e26561d31b7a93b/docs/RULEBASE_SEMANTICS.md) | Pinned priority and tie reference; qualify uncovered combinations | C12 |
| LogCluster | [ARCHITECTURE.md](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/blob/f17c749b80d5cdba05745ffaa249f90ac404ddfe/docs/ARCHITECTURE.md) | Algorithm reference; distinguish mining from scoring/rendering | C15 |
| LogCluster | [CLI.md](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/blob/f17c749b80d5cdba05745ffaa249f90ac404ddfe/docs/CLI.md) | Local usage reference; validate limits and output | C15 |
| LogCluster | [COMPARISON.md](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/blob/f17c749b80d5cdba05745ffaa249f90ac404ddfe/docs/COMPARISON.md) | Limited C/Perl compatibility, narrow edge merging, exact counters | C15 |
| LogCluster | [DEVELOPMENT.md](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/blob/f17c749b80d5cdba05745ffaa249f90ac404ddfe/docs/DEVELOPMENT.md) | Package dependency and locked restore reference; rebaseline | C14/C15 |
| LocalStream | [LOCAL_STREAM_ARCHITECTURE.md](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/docs/LOCAL_STREAM_ARCHITECTURE.md) | Mixed historical design and core reference; Query qualification separate | C05/C07 |
| DurableBuffer | [DURABLE_BUFFER_ARCHITECTURE.md](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/blob/1fb8ecaaea402894f94ec84e7aa11aae8d7bf984/docs/DURABLE_BUFFER_ARCHITECTURE.md) | Queue reference; sealed durability and application dispatch; wrapper hypothetical | C05/C12 |

## Findings and qualification

Parse's rulebase note pins upstream 13e89c3f and explicitly identifies
unspecified ties and corpus gaps. Preserve the distinction between
deliberate divergence and defects; do not infer full parity.

LogCluster's comparison describes only narrow edge-anchor merging,
not full aggregate-support semantics. Its exact counting and input
limits differ from upstream approximate sketches. DEC-0035 and C15
remain the approval and qualification boundaries.

LocalStream's authority note already separates core from Query and
Query.LiteDB. Retention independent of consumption and optional
DurableBuffer use align with DEC-0033. The older processor model does
not establish current integrated execution.

DurableBuffer explicitly excludes open in-memory chunks from durability.
Its proposed wrapper criteria are not a LocalStream implementation
contract. C05 must qualify actual acceptance and recovery boundaries.

The [component boundary register](../architecture/COMPONENT-BOUNDARIES.md) preserves these
requirements centrally. Across the estate, all 44 inventoried docs/
Markdown files now have index or targeted content coverage (8 indexes,
36 other files). This does not establish exhaustive review, current
runtime conformance, or closure of C08. Local documentation migration,
historical milestone verification and active legacy wiring reconciliation
remain open. No component files changed.
