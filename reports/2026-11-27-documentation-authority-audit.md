# Documentation authority audit — 27 November 2026

C08 documentation-first pass. Default branch metadata, recursive path
inventories and docs/README.md contents were inspected. All eight indexes
explicitly subordinate local documentation to central Accepted Decisions.
The 44 Markdown paths under component docs/ include the eight indexes;
other file contents were not exhaustively reviewed. No runtime tests.

| Repository | Branch | Pinned index | Markdown paths |
|---|---|---|---|
| DeltaZulu.Forward | master | [19b3d00](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/blob/19b3d000697922870742f52ba46e8b4fc3de3ee6/docs/README.md) | 1 |
| DeltaZulu.Kql | main | [a94dda9](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/a94dda9cfd87c950b4996cffdb33f3d4c980b485/docs/README.md) | 1 |
| DeltaZulu.Parse | master | [731b5b1](https://github.com/DeltaZulu-OU/DeltaZulu.Parse/blob/731b5b1d77696e1eff9cf24c4e26561d31b7a93b/docs/README.md) | 4 |
| DeltaZulu.Agent | master | [e2aac89](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/blob/e2aac89dafc2f8499e4e4d22ebed97cec75714fe/docs/README.md) | 15 |
| DeltaZulu.Platform | master | [d6b3a43](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/docs/README.md) | 14 |
| DeltaZulu.LocalStream | main | [b900684](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/docs/README.md) | 2 |
| DeltaZulu.DurableBuffer | master | [1fb8eca](https://github.com/DeltaZulu-OU/DeltaZulu.DurableBuffer/blob/1fb8ecaaea402894f94ec84e7aa11aae8d7bf984/docs/README.md) | 2 |
| DeltaZulu.LogCluster | master | [f17c749](https://github.com/DeltaZulu-OU/DeltaZulu.LogCluster/blob/f17c749b80d5cdba05745ffaa249f90ac404ddfe/docs/README.md) | 5 |

## Findings

| ID | Observation | Disposition |
|---|---|---|
| DOC-01 | All eight indexes link central target, Decisions, Constraints, roadmap and reports. | Authority navigation verified at pinned revisions; individual local claims remain unqualified. |
| DOC-02 | Central architecture index described NRT target as 23 November despite 27 November revisions. | Update current index date; preserve dated reports. |
| DOC-03 | Platform tree contains legacy Proton project, DDL, SQL emitter, deployer, HTTP executor, schema and streaming adapters plus tests. | Retain as migration inventory under C08; no code removal during documentation pass. |
| DOC-04 | No Proton-named paths found in the other seven trees. | Path-name observation only; not proof of absence of references or dependencies. |
| DOC-05 | Agent and Platform indexes already explicitly qualify older Proton plans; LocalStream and DurableBuffer distinguish their storage roles. | Preserve these scope notes; inspect individual active documents next. |
| DOC-06 | Governing Decisions index is generated from explicit repo metadata, not a complete applicability map. DurableBuffer has no directly named Decision despite optional edge role in DEC-0033. | Read estate-wide and cross-component decisions by applicability; do not infer exemption or edit metadata without review. |

Platform legacy inventory is pinned at
[Data.Proton](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Data.Proton)
and [Proton tests](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/d6b3a435466d57317e4c70a26948ea5d68075675/tests/DeltaZulu.Platform.Tests/Analytics/Proton).
Presence does not establish active runtime wiring. The next content pass
must classify references as historical, current implementation, target
conflict or unresolved, and trace project references, configuration and
deployment wiring before proposing removal.

The [central authority register](../architecture/README.md#authority-and-conflict-handling)
is the permanent navigation and conflict-handling reference. C08 remains
open. No component files, Accepted Decisions or historical imports changed.
