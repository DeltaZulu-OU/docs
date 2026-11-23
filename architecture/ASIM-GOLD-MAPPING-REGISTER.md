# ASIM-first Gold: source inventory and mapping work register

**Audit:** 2026-11-23. **Platform revision:** [60d6588](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f).
**Authority:** Accepted DEC-0013 (ASIM-first), DEC-0012 (single C# contract),
DEC-0029 (event time), DEC-0033 (LocalStream/DuckLake).
**Status:** Source inventory only; no ASIM field-level conformance verified.

## Current implemented schema declarations

The [MedallionSchemaCatalog](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/MedallionSchemaCatalog.cs)
defines **four** canonical Gold views, **eight** Silver parser contributors
and **three** Bronze source-family tables.

| Gold view | Silver contributors | ASIM schema family to evaluate |
|---|---|---|
| `golden.Dns` | `v_dns_windows_sysmon_eid22`, `v_dns_server_query_event` | DNS activity |
| `golden.NetworkSession` | `v_networksession_windows_sysmon_eid3`, `v_networksession_windows_security_eid5156` | Network session |
| `golden.ProcessEvent` | `v_processevent_windows_sysmon_eid1`, `v_processevent_windows_security_eid4688` | Process event |
| `golden.Authentication` | `v_authentication_windows_security_eid4624`, `v_authentication_windows_security_eid4625` | Authentication |

All four ASIM matches are **candidates**, not verified conformance claims.
File, registry, audit and alert families are outside the inspected active
canonical-view list; do not invent implementations for them.

The actual Gold fields are declared in
[`GoldenEventContracts.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Golden/GoldenEventContracts.cs).
They are not automatically ASIM-conformant. Examples:

| Current family | Current declared fields to reconcile | Specific risk |
|---|---|---|
| DNS | `Timestamp`, `ActionType`, `QueryName`, `QueryType`, `ResponseCode`, `SrcIpAddr`, `ResponseIP`, `AdditionalFields` | Action/result vocabulary, client/resolver roles and answer cardinality |
| Network session | `Timestamp`, `LocalIP`, `RemoteIP`, `LocalPort`, `RemotePort`, `Protocol`, `InitiatingProcessId` | Local/remote versus source/destination direction, process role |
| Process event | `Timestamp`, `FileName`, `FolderPath`, `ProcessId`, `ProcessCommandLine`, `InitiatingProcessFileName`, `SHA256` | Parent/target process roles, event type and stable process identity |
| Authentication | `Timestamp`, `AccountName`, `SubjectUserName`, `TargetUserSid`, `LogonType`, `Status`, `SourceIP`, `SourcePort` | Actor roles, result semantics, Windows-specific fields and port typing |

## Verified source-level findings requiring tests or repair

**EVT-01 — Ingest time substituted for event time (DEC-0029 conflict).**
[`SilverParserContributors.EventTimestamp`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Silver/SilverParserContributors.cs)
returns `COALESCE(TRY_CAST(source_event_time AS TIMESTAMP), ingest_time)`.
The DNS Server contributor uses the same fallback explicitly. Missing or
unparseable source timestamps can therefore masquerade as event timestamps.
Preserve missing/invalid source-time status rather than silently substituting
ingest time. The choice of quarantine, nullable event time or exclusion from
event-time detection requires an implementation policy and tests.

**EVT-02 — Logical duration registry differs from canonical ticks.**
[`LogicalSchemaRegistry.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/LogicalSchemaRegistry.cs)
has `LogicalDurationUnit` values Milliseconds/Microseconds/Nanoseconds,
defaults to Microseconds and retains Proton backend projections. This conflicts
with CON-0014 canonical ticks and DEC-0033 target topology. Trace registry
consumers before migrating enum values or removing backend projections.

**EVT-03 — Digest and numeric field normalization need fixtures.**
Sysmon network-session projection assigns raw `$.Hashes` to
`InitiatingProcessSHA256`, without evidence of extracting a SHA-256 entry.
Authentication `SourcePort` is declared as `Varchar/String`.
Verify source shapes, canonical value parsing and ASIM types before
publishing normalized fields.

**EVT-04 — Provenance projection remains unverified.**
Forward declares `CollectionTier`, `NullReasons` and `MatrixVersion`.
The inspected Gold view declarations do not include these fields. Determine
whether they are retained in linked evidence or otherwise queryable; do
not infer that every stored record loses provenance.

## Mapping register completion requirements

For **each** of the four families, produce a pinned published ASIM schema
name, version, documentation URL and retrieval date. Enumerate all fields,
their source/Silver/Gold mappings, required and conditional field coverage,
enum normalization, null/provenance semantics, ASIM-derived extensions,
logical KQL and physical DuckLake types, and test fixture references.
Mark each mapping as `candidate`, `ASIM-derived`, or `ASIM-conformant`
based on evidence. Do not claim full ASIM compatibility from field names.

The exact published ASIM field lists and versions have **not** been verified
in this audit. The mapping register is deliberately incomplete until those
references are pinned and tested.
