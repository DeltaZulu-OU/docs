# C03/C10 source verification — ASIM baseline, datetime, duration and event time

**Date:** 2026-11-23. **Status:** source inspection; no .NET build or application tests performed.

## Evidence revisions

- [Platform at `60d6588`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f)
- [Forward at `fba0c5c`](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/tree/fba0c5c63a1ee506373012ad458276ec807e542a)
- [Kql at `2f61c60`](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/tree/2f61c60db6a5df28c8ead33cab8de105e086bb13)
- ASIM [schema version reference](https://learn.microsoft.com/en-us/azure/sentinel/normalization-about-schemas) and [four schema-specific reference pages](../architecture/ASIM-GOLD-MAPPING-BASELINE.md) consulted 2026-11-23.

## Finding C11 — source event time silently replaced by ingestion time (P0)

[SilverParserContributors.cs](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Silver/SilverParserContributors.cs)
contains a common `EventTimestamp(jsonPath)` helper using
`COALESCE(TRY_CAST(source_event_time AS TIMESTAMP), ingest_time)`.
Seven Silver contributors use that helper; the DNS server query contributor
implements the same fallback explicitly. **All eight declared Silver
contributors can therefore output an ingest-derived `Timestamp`** when
source event time is absent or unparseable.

This is a concrete disagreement with Accepted `DEC-0029`, which states
that extracted event time, not ingestion time, governs Gold and detections.
It does not mean an actual production detection has fired incorrectly:
runtime execution and consumer behavior were not tested.

**Correctness requirement:** retain a distinguished unavailable/estimated
event-time condition and timestamp origin, and ensure unobserved ingestion
time cannot enter an event-time detection window without an explicit governed
policy. Do not silently claim strict ASIM `EventStartTime` from `ingest_time`.
Use observed source timestamps where available. The precise treatment of
records lacking a trustworthy event time should be exercised in fixtures
before production deployment.

## Finding C03-1 — Forward datetime wire conflicts with KQL carrier (P0)

`DeltaZulu.Kql/KqlTypes.cs`: declared `datetime` carrier is UTC
`DateTime`. Its normalization accepts UTC directly, converts Local to UTC,
**rejects `DateTimeKind.Unspecified`**, and converts inbound
`DateTimeOffset` to `UtcDateTime` (removing original offset).

`DeltaZulu.Forward/ForwardValueNormalizer.cs`: `Normalize` retains
`DateTimeOffset` as-is; converts `DateTime` into `DateTimeOffset`;
**treats `Unspecified` as UTC**, and retains Local's explicit offset.
The normalizer applies recursively to nested maps/arrays.

`ForwardObjectFormatter.cs`: field tag 4 is `DateTimeOffset`, serialized
as an ISO-8601 roundtrip string; decode returns `DateTimeOffset`.
Existing `ForwardCoreTests` explicitly assert offset preservation, so
this mismatch is an intentionally tested wire behavior, not an unobserved
format bug. Transport metadata `ForwardLogRecord.CreatedAt` and
`ForwardLogBatch.CreatedAt` are independent offset-bearing fields;
do not conflate them with declared KQL field values.

**Open owner decision:** versioned replacement of field tag 4 with the
UTC KQL carrier, or explicitly revised type authority. Do not change
wire encoding, historical fixtures or compatibility policy in this review.

## Finding C03-2 — duration units diverge between wire and catalogue (P0)

`ForwardObjectFormatter.cs` writes tag-5 `TimeSpan.Ticks` and reads
`new TimeSpan(Int64)`, consistent with `CON-0014`. `DeltaZulu.Kql`
uses `TimeSpan` as its timespan carrier.

Platform's `LogicalFieldType.Duration` defaults to
`LogicalDurationUnit.Microseconds`; that enum has no `Ticks` member
at the inspected source revision. `KustoType.ToDefaultDuckDbType` maps
timespan to BIGINT with the comment "stored as microseconds".
No demonstrated conversion adapter reconciles this with the
wire's 100-ns tick unit. The type is numerically BIGINT in both cases,
so schema type checks alone cannot catch the scale mismatch.

**Requirement:** agree on explicit unit metadata and exercise scalar,
array, nested, max/min and negative duration fixtures through actual
Forward→Platform→DuckLake serialization. Don't silently interpret ticks
as microseconds or vice versa.

## Finding C03-3 — provenance type declarations and tests exist (partial)

`ForwardLogRecord` contains ten named optional provenance properties
in nine historical DQM inventory rows, including collection tier,
null reasons, timestamp origin and parser generation. The
`ForwardProvenanceTests` source includes round-trip, absence-versus-default,
enum ordinal and old-v1-record decoding tests. Those are **test definitions
inspected**, not tests executed during this review.

Whether the Agent populates each property, Forward transports it in all
paths, and Gold persists its semantics in DuckLake remains unverified.

## ASIM contract exposure

The Platform `MedallionSchemaCatalog` defines four telemetry Gold
families (Dns 13 fields, NetworkSession 18, ProcessEvent 14,
Authentication 26), eight Silver contributors and three Bronze tables.
The `OperationsSchemaContracts` separately exposes AlertEvent and
AlertEntity Gold read views over append-only lake tables.

The telemetry schemas presently have none of ASIM's exact mandatory
common field names as declared columns (including `EventType`,
`EventResult`, `EventStartTime`, `EventEndTime`,
`EventSchema`, `EventSchemaVersion`, `EventCount` and
reporting-device fields). Naming and semantic conversion are required.
The complete source-field inventory and candidate conversions are in
[`ASIM-GOLD-MAPPING-BASELINE.md`](../architecture/ASIM-GOLD-MAPPING-BASELINE.md).
Do not treat those candidates as implemented or as a full conformance claim.

## Execution-ready regression matrix (not executed here)

| ID | Fixture | Required observation |
|---|---|---|
| T01 | UTC, Local, Unspecified DateTime and DateTimeOffset across scalar/array/map | KQL normalization rejects Unspecified, preserves instant, and any Forward deviation is visible |
| T02 | Old tag-4 encoded field with nonzero offset | Decoder migration/compatibility behavior explicit; no silent offset or time-zone drift |
| T03 | TimeSpan at 1 tick, 10 ticks, 1 microsecond, negative and maximum supported | Wire ticks and DuckLake units agree or an explicit loss/conversion error occurs |
| T04 | Missing, unparseable and offset-bearing source event timestamps in each of 8 Silver contributors | No silent ingest-time promotion into event-time detections |
| T05 | Presence/absence/unknown null reasons, tier and TimestampOrigin across pipeline | Preserve distinction and lineage through Gold; no default invented |
| T06 | DNS numeric QTYPE/RCODE and raw Sysmon QueryResults | ASIM numeric vs name fields correct; raw evidence preserved |
| T07 | Authentication 4624/4625 success/failure, SID roles and port conversions | EventType=Logon and result reflects outcome; identifiers scoped |
| T08 | Process 4688 hex PID, Sysmon multi-hash, unknown command line | Correct TargetProcessId and SHA256, partial ASIM mapping declared where mandatory absent |
| T09 | Network 5156 numeric protocol and Sysmon direction | EndpointNetworkSession and directional aliases are verified, not invented |
| T10 | Replay of duplicate events and missing references | Gold and alert IDs stable, correction/unknown semantics disclosed |

No application code or production wire format was changed. Acceptance
requires tests and explicit owner approval for incompatible wire changes.
