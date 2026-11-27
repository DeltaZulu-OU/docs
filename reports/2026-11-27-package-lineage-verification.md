# Package lineage and qualification branch verification — 27 November 2026

Follow-up to [25 November package lineage](2026-11-25-package-lineage.md)
and [repository baseline](2026-11-27-repository-baseline-verification.md).
Previous docs CI passed both workflows. Authenticated GitHub metadata
and selected source inspected; no package bytes downloaded or new tests run.

## LocalStream publication

Directory.Build.props at b900684308248a83a08550e0d66a8c52adad62fd
sets Version 1.1.0. Annotated v1.1.0 tag object
f7118396c53b408f724b159bd7a2b5708922a006 resolves to that commit.
[Publication run 46048442186](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/actions/runs/46048442186)
completed successfully on manual dispatch at that revision. The workflow
packs core, Query and Query.LiteDB, inspects contents, uploads artifacts
and pushes packages. Artifact 15223496430, nuget-package-1.1.0, is
unexpired until 2027-02-25T18:18:17Z. GitHub reports archive digest
sha256:12a7f3cf487933e884e1ef3401e9e02e3a8433eba5d1d02fa1566c56d18d4bf7.
This is not a per-package hash or independent byte verification.
Platform declares all three packages at 1.1.0; Agent retains core 1.0.0.
The earlier report's 0.1.0 source version and core-only publication
workflow are historical, not current. Independent registry resolution,
nuspec metadata, per-package hashes and consumer compatibility remain open.

## Existing branch qualification

| Repository / branch | Head | Ahead / behind default | Evidence |
|---|---|---|---|
| LocalStream build/track-portable-restore-graph | 197a0831d04188c1d48117da81fb9df1e6f1ecff | 1 / 2 | Earlier Linux tests/pack passed; no matching Actions runs returned; reconcile with 1.1.0 publication. |
| DurableBuffer build/track-portable-restore-graph | e677fd32c080235d5f563f19d0c540e575efa5ce | 1 / 0 | Earlier Linux 94 tests/pack passed; no matching Actions runs returned. |
| LocalStream fix/query-package-publication | b900684308248a83a08550e0d66a8c52adad62fd | 0 / 0 | Already at main; publication and unit tests successful. |
| LocalStream test/query-output-recovery | 36ad1074e172a6f7da9a85eb55319690f895332d | 1 / 1 | One test file changed; no matching Actions runs returned. C07 qualification open. |
| LogCluster fix/miner-record-count-boundaries | 91e2013afe65e673cd21f05ec8cefac6d43bd292 | 1 / 1 | Earlier Linux 27 tests and limited Perl fixture passed; no matching Actions runs returned. |

Ahead/behind counts are GitHub comparisons against current defaults.
Absence of returned runs is not proof no tests ever ran. Reconcile
divergent branches before integration, regenerate locks against current
package versions and qualify three-host matrices. No branches merged
in component repositories.

## Outstanding evidence

Generic tag/release listing endpoint was rejected by the connector.
Exact LocalStream tag and artifact endpoints succeeded. DurableBuffer,
Forward, Parse and Kql release lineage was not independently refreshed;
retain the earlier pinned evidence with its limitations. MessagePack
advisory verification, packed Kusto.Language consumer tests and
LogCluster RID-specific publication remain open. No new version or
upgrade policy selected.
