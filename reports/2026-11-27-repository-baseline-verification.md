# Repository baseline verification — 27 November 2026

Authenticated GitHub branch, recursive tree, workflow and selected
configuration inspection. All eight default heads match the earlier
documentation inventory. All returned workflow runs at those heads
completed successfully. No fresh restore, build, package extraction,
vulnerability scan or compatibility test was performed.

| Repository | Default revision | Projects | Tracked lock files | Root SDK pin | Successful run IDs |
|---|---|---:|---:|---|---|
| Agent | e2aac89dafc2f8499e4e4d22ebed97cec75714fe | 11 | 0 | absent | 45637108879, 45637110180 |
| Platform | d6b3a435466d57317e4c70a26948ea5d68075675 | 13 | 14 | 10.0.404 | 46060583689, 46060583798 |
| Forward | 19b3d000697922870742f52ba46e8b4fc3de3ee6 | 4 | 0 | absent | 46045662911, 45618925109 |
| Kql | a94dda9cfd87c950b4996cffdb33f3d4c980b485 | 3 | 3 | absent | 45836981752, 45618937584 |
| Parse | 731b5b1d77696e1eff9cf24c4e26561d31b7a93b | 4 | 4 | absent | 45618952634, 45618952000 |
| LogCluster | f17c749b80d5cdba05745ffaa249f90ac404ddfe | 4 | 3 | 10.0.404 | 45637079240 |
| LocalStream | b900684308248a83a08550e0d66a8c52adad62fd | 6 | 0 | absent | 46048442186, 46047895999, 46047894931 |
| DurableBuffer | 1fb8ecaaea402894f94ec84e7aa11aae8d7bf984 | 2 | 0 | absent | 45809752349, 45618946356 |

## Findings

- Agent, Forward, LocalStream and DurableBuffer set RestorePackagesWithLockFile
  in Directory.Build.props and invoke dotnet restore --locked-mode in
  unit-tests.yml, but have no tracked lock files. Successful CI is not
  evidence of a fixed dependency graph. Verify clean restore behavior
  and commit generated locks during corrective engineering.
- Those four workflows select 10.0.x, not an exact SDK. Platform and
  LogCluster global.json pin 10.0.404 with rollForward disabled. Kql
  and Parse have no root global.json; workflow SDK selection not
  inspected in this pass.
- Kql, Parse and Platform have a colocated lock for every inventoried
  project. Platform has one additional lock. LogCluster CLI lacks a
  colocated lock; determine solution membership, custom lock path and
  RID publish behavior before declaring the exact corrective change.
- Forward central package version remains MessagePack 3.1.8. Earlier
  NU1902 evidence remains an open verification/remediation gate;
  this pass does not establish current advisory applicability.
- Agent declares Forward 0.3.1, Parse 0.1.1, DurableBuffer 1.0.0 and
  LocalStream 1.0.0. Platform declares LocalStream, Query and Query.LiteDB
  1.1.0. LogCluster declares Parse 0.1.1. These are declared versions,
  not independently verified resolved package bytes.
- Kql declares Microsoft.Azure.Kusto.Language 9.2.0 and Platform
  12.4.1. CON-0021 packed consumer qualification remains open.

## Remaining C14 evidence

Reconcile current release tags, package hashes and actual consumer
resolution against the [package lineage report](2026-11-25-package-lineage.md).
Inspect the existing LocalStream/DurableBuffer qualification branches
and their three-host results, verify MessagePack advisory and upgrade
compatibility, exercise packed Kql consumers across the version span,
and qualify LogCluster RID-specific locked publication. Preserve
source/CI/package distinctions; no default branch changes or new
policy authorized by this report.
