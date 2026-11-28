# DuckDB conversion qualification and deferred precision findings

Date: 2026-11-28

## Scope and disposition

Platform candidate [40478fe](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/40478fe98b4c4c7db317b786d95b171ce29f70e8), branch `build/qualify-duckdb-conversions`, uses DuckDB.NET 1.5.6.1 and native DuckDB 1.5.6. The inspected provider revision is [7ac3220](https://github.com/Giorgi/DuckDB.NET/tree/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c).

Owner direction, 28 November: document precision findings internally and defer further provider workarounds. The owner will decide whether to file upstream issues or submit fixes. Do not create upstream issues or PRs, fork the provider, introduce alternative temporal storage, silently normalise timestamps, or add further conversion workarounds as part of this qualification. Existing qualified conversion changes remain on the candidate branch; this report does not authorise a new KQL temporal or dynamic representation. Revisit the deferred findings when a provider fix is available or the owner explicitly reopens the work.

## Executed evidence

| Run | Scope | Result |
| --- | --- | --- |
| [46132827716](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46132827716) | Baseline managed 1.5.5.0 / native 1.5.5 | 4/4 characterisation tests; negative interval conversion throws OverflowException; wide fractional decimal narrows to zero |
| [46134514851](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46134514851) | Candidate managed 1.5.6.1 / native 1.5.6 | 4/4 characterisation tests; negative interval regression corrected |
| [46157150057](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46157150057) | Native JSON and INET probes | 55/55 |
| [46160505985](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46160505985) | Native result projection | 65/65 |
| [46160616132](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46160616132) | Extended qualification and full Platform regression, Windows | 76/76 targeted; 1422/1422 full regression; locked restore and audit passed, no vulnerable packages reported by configured sources across 13 projects |

Characterisation tests record observed behaviour; a passing characterisation test does not establish lossless conversion. Cross-platform candidate qualification is documented below. Passing conversion and regression tests does not by itself establish lossless production persistence for all KQL temporal values.

## Deferred findings

| Finding | Evidence and root cause | Classification and follow-up |
| --- | --- | --- |
| DateTimeOffset to TIMESTAMPTZ | [DateTimeExtensions.cs:41,68–70](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Data/Extensions/DateTimeExtensions.cs#L41-L70): integer division of UTC ticks before subtracting epoch microseconds floors to earlier microsecond. Inputs +1/+9 ticks relative to epoch become 0; -1/-9 become -10. | Reproduced; native microsecond precision limit and intentional narrowing. An upstream strict-conversion option could signal loss but cannot increase native precision. |
| TimeSpan to INTERVAL | [DuckDBInterval.cs:44–45](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Bindings/DuckDBInterval.cs#L44-L45): signed residual ticks divided by 10 towards zero. Inputs +/-1 and +/-9 ticks become zero. | Reproduced; native microsecond precision limit and intentional narrowing. Negative aligned intervals are fixed in 1.5.6.1. |
| TIMESTAMP_NS to DateTime | [DateTimeVectorDataReader.cs:155–171](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Data/DataChunk/Reader/DateTimeVectorDataReader.cs#L155-L171): signed nanoseconds divided by 100 towards zero. 2026-01-01 00:00:00.123456789 becomes .1234567; 1969-12-31 23:59:59.999999999 becomes 1970-01-01 00:00:00.0000000. [Upstream test](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Test/TemporalConversionTests.cs#L180) explicitly expects truncation. | Reproduced; CLR tick resolution limit and intentional narrowing. Provider-specific DuckDBTimestamp also loses submicrosecond precision. |
| TIMESTAMP_NS write overflow | [DateTimeExtensions.cs:46–49](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Data/Extensions/DateTimeExtensions.cs#L46-L49): multiplication of epoch-relative ticks by 100 without explicit checked arithmetic; comment acknowledges wrapping. | Source-confirmed risk, runtime reproduction pending. Candidate upstream fix: checked range validation, including reserved infinity values. |
| DECIMAL narrowing | [DecimalVectorDataReader.cs:99–127](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Data/DataChunk/Reader/DecimalVectorDataReader.cs#L99-L127): excess fractional digits truncated, decimal arithmetic can narrow. DECIMAL(38,30) value 10^-30 reads as zero through default managed conversion. | Reproduced; provider offers exact DuckDBDecimal carrier. Default conversion policy is lossy, not a native storage defect. Existing checked scalar conversion remains qualified. |
| TIMESTAMPTZ Kind | [DateTimeVectorDataReader.cs:113–118](https://github.com/Giorgi/DuckDB.NET/blob/7ac3220f8fe5eaba150ac8172c1f3bdbabf7a5c/DuckDB.NET.Data/DataChunk/Reader/DateTimeVectorDataReader.cs#L113-L118): default DateTime construction leaves Kind unspecified. | Reproduced; DateTimeOffset typed read provides UTC instant. Existing candidate uses UTC DateTime for TIMESTAMPTZ. |
| Nested decimal and logical aliases | Default nested materialisation uses child default CLR values; GetDataTypeName reports physical type ID (INET as Struct). | Provider API/conversion limitations. Existing candidate uses native final result projection and DESCRIBE. No further workaround authorised. |

KQL datetime and timespan use 100 ns resolution; TIMESTAMP, TIMESTAMPTZ and INTERVAL use microseconds. TIMESTAMP_NS has nanosecond resolution but a narrower range (approximately 1677–2262) than KQL datetime (years 1–9999). Upstream fixes cannot by themselves resolve the native representation mismatch. Four positive/negative microsecond-aligned DateTimeOffset and TimeSpan cases survived database closure and reopening exactly. No permanent storage or loss policy is approved by this report.

## Production exposure (source inspection)

DuckDbRawLogSubscriber and LocalStreamBronzeWriter bind ingest timestamps through Dapper. DuckDbAgentObservationWriter and DuckDbSourceObservationWriter bind observation/window timestamps through the shared append-only writer. DuckDbAlertLakeWriter and DuckDbAlertEntityLakeWriter emit ISO timestamps into TIMESTAMP columns. DuckDbValueReader reads native temporal values. DuckDbScalarEmitter already rejects submicrosecond typed timestamp and parsed TimeSpan literals in the candidate. These are exposure paths, not independently reproduced production defects. Do not blanket-reject ordinary ingestion timestamps or alter detection-window semantics without an approved temporal contract.

## DB work package disposition

| ID | Status at candidate |
| --- | --- |
| DB01 | Exact scalar decimal conversion verified; upstream default narrowing documented |
| DB02 | Partial; temporal precision/range findings deferred, KQL datetime policy open |
| DB03 | GUID verified |
| DB04 | Supported nested result presentation verified; not lossless KQL dynamic storage |
| DB05 | Explicit failure propagation verified on tested paths |
| DB06 | Aligned signed interval read/write and persistence verified; submicrosecond parameter narrowing deferred |
| DB07 | Native type classification verified on tested paths |
| DB08 | Native INET result conversion verified |

Native JSON preserves tested wide/narrow decimal tokens and nulls; non-finite floating values are rejected as invalid strict JSON, and nested INET/non-string-keyed maps are rejected conservatively. Existing projection tests cover duplicate names, quoted identifiers, ordering and single execution in the tested data-only path. Developer-mode EXPLAIN ANALYZE re-execution remains a separate Platform concern, not a provider precision defect.

## Three-platform candidate qualification and direct integration

The final pre-cleanup candidate `91f5a962ca5e7cce52175d599ebc7d8131c50d18` passed [workflow run 46171447930](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46171447930) on Ubuntu, Windows and macOS. Each host completed locked restore, configured-source direct/transitive vulnerability audit, unchanged lock graph verification, 76 targeted scalar/result conversion tests, Release solution build and 1,422 full regression tests. Across the three hosts, 4,494 test executions passed (228 targeted plus 4,266 full regressions), with no reported failed or skipped tests. The run does not establish zero compiler/analyser warnings; warnings including CS8524 and CA1873 had appeared during qualification.

The temporary `.github/workflows/duckdb-conversion-qualification.yml` was deleted in [cleanup commit 55bde60f](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/commit/55bde60f71bf4f083b02201999b9e2df0e0d7d6d). The cleaned candidate retained the production corrections, lockfiles, scalar conversion and result projection regressions. GitHub comparison before integration reported 17 commits ahead and zero behind `master`, and no temporary workflow in the resulting diff. The `master` ref was then advanced non-forcibly from `d6b3a435466d57317e4c70a26948ea5d68075675` to `55bde60f71bf4f083b02201999b9e2df0e0d7d6d`; subsequent comparison confirmed the branch and `master` were identical.

Permanent CI was triggered at the integrated commit: [Unit Tests run 46179453486](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46179453486) and [Push on master run 46179452888](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/actions/runs/46179452888). Both were **in progress at the evidence checkpoint**; their eventual outcomes must be verified before the post-integration gate is marked passed. The permanent Unit Tests workflow covers three-host locked restore, unchanged lockfiles, Release build and regression tests, but does not itself run the explicit vulnerability audit performed by candidate qualification.

This closes the scoped *branch integration action*, not all Platform dependency qualification. DB02/DB06 100 ns vs microsecond limitations, provider-side precision behaviour, KQL datetime and dynamic semantics, complete C03 and estate-wide C14 remain open under the owner's documented deferral. No additional DuckDB.NET workaround, package publication, issue or pull request was introduced.

## Next gate

Three-host candidate qualification and direct integration are complete. Verify the outcomes of the two permanent master workflows cited above before marking post-integration CI qualified. Then resume Kql and the remaining dependency roadmap without new precision fixes. C03 and C14 remain open; deferred precision findings are not closed or accepted as a permanent KQL contract. No upstream issue, PR or package publication was made.
