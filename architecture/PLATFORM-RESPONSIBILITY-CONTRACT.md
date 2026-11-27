# Platform responsibility and execution boundaries

Current target interpretation of Accepted DEC-0005/0006/0007,
DEC-0012/0013/0018/0019/0022/0026/0029/0030/0032/0033/0034/0036/0037/0038.
See the [Platform reconciliation report](../reports/2026-11-27-platform-documentation-reconciliation.md) for source evidence.
No new policy or production readiness claim is made here.

## Data and execution ownership

Platform owns the separately deployed Forward collector, canonical
mapping and reconstructable enrichment, logical schema catalogue,
DuckLake evidence persistence and governed analyst reads. Preserve
authoritative Agent extraction and source lineage; distinguish decoding
and mapping from routine reparsing. The Agent does not write the lake
directly. LocalStream owns bounded node-local replay, Query owns generic
bound operators, and Platform owns schema binding, detection semantics
and persistence integration. Scheduled detection is deferred.

The current Web host has LocalStream ingestion registrations alongside
legacy Proton registrations. This is an implementation discrepancy,
not an alternative target. Retire legacy compilation, deployment,
schema and streaming dependencies only after tracing callers and
qualifying their surviving responsibilities. Do not replace them with
a new engine or silently remove working evidence paths.

## Analytics and governance

The approved logical view catalogue controls real query sources.
Illustrative KQL translation examples do not register Gold aliases.
Platform owns Kusto.Language binding and typed diagnostics; the
DuckDB relational hunting adapter and LocalStream bound execution
adapter require separate semantic qualification. The detailed local
translation dictionary and comparison register are reference material,
not proof of implemented coverage. Compare typed values, names,
column order, multiplicity and ordering where semantically required.
No silent approximation is permitted in detection execution.
Unsupported or failed execution is not a clean nonmatch.

Preserve governed rule revisions, effective deployment identity,
evidence lineage and explicit applicability/outcome distinctions under
DEC-0036. Operational alert identity follows DEC-0030 and evidence
identity follows DEC-0037. The
[detection result contract](DETECTION-RESULT-CONTRACT.md) governs
candidate C06/C07 qualification; do not infer that a legacy mediation
service satisfies it. Historical user stories and gap analyses do not
establish current production readiness.

## Product and management surfaces

The inspected Web composition registers Analytics, Governance,
Operations and Agent Management. Registration is not feature
completion. C16 qualifies shared analytics execution, governed
content, investigation and operational workflows; C17 qualifies
management. Keep telemetry transfer separate from management HTTPS.

Inherited management requirements include pull-based enrollment,
credential recovery and rotation, policy bundle validation, constrained
commands, explicit application acknowledgement, health observations,
bounded retries and rollback. Treat historical TUF signing, expiry,
rollback protection, tenant isolation and rollout details as
qualification requirements under C17, not verified implementation
or newly Accepted Decisions. Development simulator certificate
bypass is not a production trust policy.

Local product styling and implementation guides may remain component
references. Central Decisions and roadmap govern cross-component
scope, and historical plans cannot create independent commitments.
