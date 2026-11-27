# Dependency compatibility qualification

## MessagePack

The reviewed advisory [GHSA-qhrr-8q5h-9q3h](https://github.com/advisories/GHSA-qhrr-8q5h-9q3h), CVE-2026-92707, CVSS 5.3, covers MessagePack 3.0.0 through versions below 3.1.9. Forward declares 3.1.8; prior Agent restore logs show NU1902. Version exposure is confirmed, reachable PrimitiveObjectFormatter use is not. Review resolver fallbacks and object members; select a compatible patched version (at least 3.1.9, subject to current advisory review), test typed wire fixtures, malformed input and bounded allocation, pack under a fresh release identifier and verify downstream resolution. No new wire format is authorized.

## Kusto.Language

The [August preflight](2026-08-15-kusto-language-preflight.md) compiled separate probes against 9.2.0 and 12.4.1. Four inspected API shapes and widening relations matched. The single alias and All membership differed; the older version lacks ScalarTypes.Null. These were source compilation probes, not binary compatibility tests. Build Kql once against its declared minimum, pack once, restore that same package into two isolated consumer projects with exact Kusto version pins. Verify actual assembly resolution, supported ten types, aliases, typed null behavior, coercion and diagnostics. Include Agent Rx.Kql and Platform integration separately. Any unsupported runtime combination requires explicit CON-0021 reconciliation rather than silent fallback.

## Native publication

The [November lineage report](2026-11-25-package-lineage.md) records NU1004 on RID-specific locked publish for portable LogCluster and Suggester references. Host-native publish without another restore progressed to ILLink task-host MSB4216 in the restricted executor. Neither result establishes native publication success. Inspect project-specific effective restore properties, preserve portable lock coverage, qualify RID-specific restore and publish on authorized runners, execute native CLI smoke tests, and compare output with managed CLI fixtures. Do not disable locked restore merely to obtain a passing publish.

## Integration gates

Reconcile existing restore branches against current defaults without changing dependency versions during lock capture. Verify clean restores, unchanged tracked locks and exact SDK selection; test on Linux, Windows and macOS where supported. Verify publication metadata and package content hashes independently; retain LocalStream 1.1.0 archive digest as archive evidence only. Refresh other release lineage when authenticated artifact access is available. No new build, restore, package download or branch CI was executed in this pass. The previous report documents limitations of the available runner and package feed. Historical Rx.Kql transitive vulnerability findings require fresh resolved-graph audit, not an assertion of present exploitability.

C14 remains open. This is a corrective test specification, not approval to modify product code or publish packages.
