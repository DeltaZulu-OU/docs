# ASIM-first Gold mapping baseline — source inventory and candidate mappings

**Review:** 2026-11-23. **Status:** source-backed design inventory, NOT an implemented migration or claim of ASIM compliance.
**Governing Decisions:** Accepted `DEC-0013` (ASIM-first Gold), `DEC-0012` (single schema catalogue), `DEC-0029` (event time), `DEC-0033` (LocalStream / DuckLake).

## Source revision and reference pin

- Platform source: [`60d6588071eb187cddf61baa77b9991cc793e25f`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f).
- Gold definitions: [`GoldenEventContracts.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Golden/GoldenEventContracts.cs).
- Silver contributors: [`SilverParserContributors.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Silver/SilverParserContributors.cs).
- Microsoft ASIM [schema overview](https://learn.microsoft.com/en-us/azure/sentinel/normalization-about-schemas): reviewed 2026-11-23. The listed DNS, Network Session, Process Event and Authentication schema versions are **1.0.0**.
- Per-family references: [DNS](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-dns), [Network Session](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-network), [Process Event](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-process-event), [Authentication](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-authentication).

**Pin limitation:** These are reviewed web-document versions, not a vendored, immutable ASIM schema specification or exact Git revision of schema test fixtures. Before automated conformance gating, pin reviewed source artifacts and document any differences between the documentation and test corpus.

## Actual source coverage

| Surface | Present in source | Interpretation |
|---|---|---|
| Bronze tables | `dns_server_event`, `windows_security_event`, `windows_sysmon_event` | Three raw source-family table definitions; not proof of operational collectors |
| Silver contributors | DNS server 256/257, Sysmon 22; Network Security 5156, Sysmon 3; Process Security 4688, Sysmon 1; Authentication Security 4624, 4625 | Eight declared source→Gold contributors; mapping correctness unverified |
| Gold telemetry contracts | `Dns`, `NetworkSession`, `ProcessEvent`, `Authentication` | Four C#-defined canonical view contracts, **71 field entries** |
| Gold operational views | `AlertEvent`, `AlertEntity` backed by `lake.alert_events`/`lake.alert_entities` | Additional operational query views, NOT evaluated against ASIM Alert Event or Asset Entity schemas |

## Mandatory ASIM common fields: gap register

ASIM 1.0.0 schema references list `EventCount`, `EventStartTime`, `EventEndTime`, `EventType`, `EventResult`, `EventProduct`, `EventVendor`, `EventSchema`, `EventSchemaVersion`, and `Dvc` as mandatory/common. The four current Gold telemetry contract definitions **do not directly declare these names**. Source metadata may be available in Bronze, but derivation has not been verified. A point-in-time source event may set start=end only after its source instant is known; `ingest_time` is not a substitute for event time. `EventUid`, reporting-device details, and conditional entity-ID type fields also need explicit derivation.

## Mapping status vocabulary

`conditional`: candidate name exists but valid only when source field is present; `transform`: requires semantic or type conversion; `direction`: endpoint vs wire direction must be established; `context`: source-scoped identity requires additional provenance; `verify`: plausible direct mapping needs source fixtures; `extension`: ASIM-derived field rather than a verified standard member; `review`: cannot safely commit to a canonical field yet; `unsafe`: source mapping has a directly observable semantic hazard.

**Important:** Every target below is a **candidate**, not an approved per-field mapping. No source value, enum, or type should be rewritten based on this table without a fixture verifying it.

## `golden.Dns` — 13 fields (DNS ASIM 1.0.0)

| Existing Gold field | Existing Kusto / DuckDB | Candidate ASIM target or extension | Disposition | Required check |
|---|---|---|---|---|
| `Timestamp` | `DateTime / Timestamp` | `EventStartTime / EventEndTime` | transform | Source event time only; COALESCE with ingest_time must be removed from detection semantics. |
| `DeviceName` | `String / Varchar` | `DvcHostname` | transform | Ensure host value follows ASIM hostname/FQDN semantics. |
| `ActionType` | `String / Varchar` | `EventType` | transform | DnsQuery literal is not the ASIM Query event type; distinguish request/response. |
| `QueryName` | `String / Varchar` | `DnsQuery` | transform | Query name parsing, trailing-dot handling, and raw-value preservation. |
| `QueryType` | `String / Varchar` | `DnsQueryType / DnsQueryTypeName` | transform | Existing string can be numeric RR type or mnemonic; normalize separately. |
| `ResponseCode` | `String / Varchar` | `DnsResponseCode / EventResultDetails` | transform | Existing string may be integer or symbolic status; distinguish numeric and normalized name. |
| `ResponseName` | `String / Varchar` | `DnsResponseName` | verify | Confirm whether each source stores unparsed answer, DNS name or aggregated results. |
| `ResponseIP` | `String / Varchar` | `ASIM-derived answer-IP field` | extension | No approved 1:1 field; retain response evidence, verify extraction and avoid fabricating an IP. |
| `SrcIpAddr` | `String / Varchar` | `SrcIpAddr` | conditional | Already named like ASIM; null in Sysmon EID22 contributor. |
| `SrcPortNumber` | `Int / Integer` | `SrcPortNumber` | conditional | Already named like ASIM; null in Sysmon EID22 contributor. |
| `Protocol` | `String / Varchar` | `NetworkProtocol` | transform | Normalize TCP/UDP and distinguish DNS vs network protocol metadata. |
| `ReportId` | `String / Varchar` | `EventOriginalUid` | context | Scoped EventRecordID; cannot directly serve as globally stable EventUid. |
| `AdditionalFields` | `Dynamic / Json` | `AdditionalFields` | review | Currently entire raw_log rather than only extras; preserve Bronze evidence lineage. |

## `golden.NetworkSession` — 18 fields (Network Session ASIM 1.0.0)

| Existing Gold field | Existing Kusto / DuckDB | Candidate ASIM target or extension | Disposition | Required check |
|---|---|---|---|---|
| `Timestamp` | `DateTime / Timestamp` | `EventStartTime / EventEndTime` | transform | Must never substitute ingestion time as detection time. |
| `DeviceName` | `String / Varchar` | `DvcHostname` | transform | Reporting endpoint vs source/destination entity must remain distinct. |
| `ActionType` | `String / Varchar` | `DvcAction / EventResult` | transform | ConnectionAllowed/ConnectionSuccess are not ASIM EventType; derive EndpointNetworkSession separately. |
| `LocalIP` | `String / Varchar` | `LocalIpAddr; SrcIpAddr / DstIpAddr` | direction | Local is endpoint-relative; Src/Dst requires NetworkDirection, not a static rename. |
| `LocalPort` | `Int / Integer` | `SrcPortNumber / DstPortNumber` | direction | Endpoint-relative port; no unconditional LocalPortNumber contract assumed. |
| `RemoteIP` | `String / Varchar` | `RemoteIpAddr; SrcIpAddr / DstIpAddr` | direction | Direction-dependent alias, not automatically destination. |
| `RemotePort` | `Int / Integer` | `SrcPortNumber / DstPortNumber` | direction | Direction-dependent mapping; preserve endpoint-local meaning. |
| `Protocol` | `String / Varchar` | `NetworkProtocol` | transform | Windows 5156 may use protocol numbers; normalize according to IANA. |
| `RemoteUrl` | `String / Varchar` | `RemoteHostname or extension` | review | Hostname and URL are different logical types; avoid unverified coercion. |
| `LocalIPType` | `String / Varchar` | `DeltaZulu-derived IP classification` | extension | Requires type vocabulary and source semantics. |
| `RemoteIPType` | `String / Varchar` | `DeltaZulu-derived IP classification` | extension | Requires type vocabulary and source semantics. |
| `InitiatingProcessFileName` | `String / Varchar` | `SrcProcessName candidate` | review | Basename versus full process path needs a documented decision per source. |
| `InitiatingProcessFolderPath` | `String / Varchar` | `SrcProcessName candidate` | review | The source stores application/full image path, not necessarily only a folder. |
| `InitiatingProcessId` | `Long / BigInt` | `SrcProcessId` | transform | ASIM process ID is a string representation; existing Gold KQL long. |
| `InitiatingProcessCommandLine` | `String / Varchar` | `DeltaZulu-derived process metadata` | extension | No assumed first-class ASIM network field; preserve evidence and validate extension. |
| `InitiatingProcessAccountName` | `String / Varchar` | `ASIM source user entity candidate` | review | Role, username type and domain must be reconstructed before mapping. |
| `InitiatingProcessSHA256` | `String / Varchar` | `DeltaZulu-derived process hash` | extension | Identify exact algorithm and parse hash value before asserting SHA256. |
| `ReportId` | `String / Varchar` | `EventOriginalUid` | context | Source-scoped ID; derive stable EventUid separately. |

## `golden.ProcessEvent` — 14 fields (Process Event ASIM 1.0.0)

| Existing Gold field | Existing Kusto / DuckDB | Candidate ASIM target or extension | Disposition | Required check |
|---|---|---|---|---|
| `Timestamp` | `DateTime / Timestamp` | `EventStartTime / EventEndTime` | transform | Source event time required for processing; record origin. |
| `DeviceId` | `String / Varchar` | `DvcId (+ DvcIdType)` | conditional | DvcIdType required when device ID present; current contributors set null. |
| `DeviceName` | `String / Varchar` | `DvcHostname` | transform | Validate hostname semantics. |
| `ActionType` | `String / Varchar` | `EventType` | transform | ProcessCreated literal is consistent with ASIM enum; verify remaining event classes. |
| `FileName` | `String / Varchar` | `TargetProcessFilename` | transform | Existing field is basename; do not populate TargetProcessName from basename alone. |
| `FolderPath` | `String / Varchar` | `TargetProcessName` | transform | Existing field contains full image path, not parent directory; correct semantic labeling. |
| `SHA256` | `String / Varchar` | `TargetProcessSHA256` | unsafe | Sysmon source copies entire $.Hashes list into SHA256; extract/validate SHA256 before populating. |
| `ProcessId` | `Long / BigInt` | `TargetProcessId` | transform | ASIM field type string while Gold uses long; verify hex/decimal Windows 4688 input conversion. |
| `ProcessCommandLine` | `String / Varchar` | `TargetProcessCommandLine` | conditional | Mandatory for ASIM process-created events, but source may omit; represent incomplete mapping. |
| `AccountName` | `String / Varchar` | `TargetUsername / ActorUsername` | review | Credentials associated with executed process vs initiator need source-by-source role mapping. |
| `InitiatingProcessFileName` | `String / Varchar` | `ParentProcessName candidate` | review | Current field stores basename; parent full image path may be available in original source. |
| `InitiatingProcessCommandLine` | `String / Varchar` | `DeltaZulu-derived parent command-line` | extension | Do not invent a first-class ASIM ParentProcessCommandLine field. |
| `ReportId` | `String / Varchar` | `EventOriginalUid` | context | Source scoped; construct EventUid independently from stable provenance. |
| `AdditionalFields` | `Dynamic / Json` | `AdditionalFields` | review | Whole raw_log; retain source fidelity without duplicating unbounded data unnecessarily. |

## `golden.Authentication` — 26 fields (Authentication ASIM 1.0.0)

| Existing Gold field | Existing Kusto / DuckDB | Candidate ASIM target or extension | Disposition | Required check |
|---|---|---|---|---|
| `Timestamp` | `DateTime / Timestamp` | `EventStartTime / EventEndTime` | transform | Use event-time source; never quietly replace with ingest_time. |
| `DeviceName` | `String / Varchar` | `DvcHostname` | transform | Target/reporting host should not be confused with source workstation. |
| `ActionType` | `String / Varchar` | `EventType + EventResult` | transform | LogonSuccess/LogonFailure must become Logon with Success/Failure results. |
| `EventId` | `String / Varchar` | `EventOriginalType` | review | Windows 4624/4625 event type, not ASIM EventUid. |
| `AccountName` | `String / Varchar` | `TargetUsername` | transform | Combine with domain when available and set UsernameType as appropriate. |
| `AccountDomain` | `String / Varchar` | `TargetUsername / TargetUser domain` | transform | Domain formatting must follow ASIM username conventions, preserve original. |
| `SubjectUserName` | `String / Varchar` | `ActorUsername` | transform | Distinguish actor from target user. |
| `SubjectDomainName` | `String / Varchar` | `ActorUsername / Actor user domain` | transform | Preserve source-domain semantics. |
| `SubjectUserSid` | `String / Varchar` | `ActorUserId (+ ActorUserIdType)` | conditional | SID type required when ID exists. |
| `SubjectUserSid_resolved` | `String / Varchar` | `DeltaZulu-derived resolved SID` | extension | Keep resolved label separate from original SID. |
| `TargetUserSid` | `String / Varchar` | `TargetUserId (+ TargetUserIdType)` | conditional | SID type required when ID exists. |
| `TargetUserSid_resolved` | `String / Varchar` | `DeltaZulu-derived resolved SID` | extension | Preserve SID and display resolution separately. |
| `LogonType` | `String / Varchar` | `EventOriginalSubType` | review | Windows numeric logon type; map to ASIM EventSubType only with verified enum equivalence. |
| `LogonType_resolved` | `String / Varchar` | `EventSubType` | transform | Normalize Windows types to ASIM allowed values; preserve original code and description. |
| `Status` | `String / Varchar` | `EventOriginalResultDetails` | review | Raw NTSTATUS code, do not equate with canonical failure description. |
| `Status_resolved` | `String / Varchar` | `EventResultDetails candidate` | transform | Map to ASIM allowed result-detail enum, not arbitrary symbolic NTSTATUS. |
| `SubStatus` | `String / Varchar` | `DeltaZulu-derived auth substatus` | extension | Preserve raw detail. |
| `SubStatus_resolved` | `String / Varchar` | `DeltaZulu-derived auth substatus name` | extension | Preserve resolved detail. |
| `SourceIP` | `String / Varchar` | `SrcIpAddr` | transform | Parse IP address; preserve source-specific unknown tokens. |
| `SourcePort` | `String / Varchar` | `SrcPortNumber` | transform | Current Gold uses Kusto string, while ASIM expects integer; validate and reject invalid. |
| `WorkstationName` | `String / Varchar` | `SrcHostname` | transform | Source host, not reporting DvcHostname. |
| `AuthenticationPackageName` | `String / Varchar` | `LogonProtocol candidate` | review | Package and authentication protocol may differ; do not assume equivalence. |
| `FailureReason` | `String / Varchar` | `EventOriginalResultDetails` | review | Original message resource ID. |
| `FailureReason_resolved` | `String / Varchar` | `EventResultDetails candidate` | transform | ASIM normalized vocabulary required; keep source explanation. |
| `ReportId` | `String / Varchar` | `EventOriginalUid` | context | Source EventRecordID must be scoped for uniqueness. |
| `AdditionalFields` | `Dynamic / Json` | `AdditionalFields` | review | Whole raw_log; preserve Bronze lineage and document duplication. |

## Per-family acceptance fixtures

| Family | Minimal acceptance scenarios |
|---|---|
| DNS | Query (including invalid/tunneling names and trailing dot), numeric vs named QTYPE/RCODE, query without response, client-only Sysmon EID22, DNS server request/response segmentation, ambiguous `QueryResults` |
| Network Session | Inbound and outbound endpoint session, Security 5156 numeric protocol, Sysmon 3 `Initiated`, absent direction, host versus URL, valid/invalid/overflowing ports and process identifiers |
| Process Event | Security 4688 process ID in hexadecimal/decimal, absent command line, Sysmon 1 multi-hash payload, complete image path versus filename, target/actor/parent role boundaries |
| Authentication | 4624 success and 4625 failure, subject versus target identity, source port as string, NTSTATUS/substatus, Windows logon type to ASIM EventSubType and unknown codes |
| Common | Missing/invalid source event time must not be silently promoted from ingestion time; mandatory ASIM field presence with provenance; partial mapping must be labeled derived, not ASIM-conformant |

## Acceptance and migration boundaries

1. For every family, pin a versioned mapping profile and record the complete input-to-output field transformation (including missing/unknown semantics).
2. Add shared common fields and all conditional companion fields where supported; never fabricate mandatory values when absent. A source that lacks required data remains partially mapped or unsupported.
3. Preserve existing source evidence and old Gold consumer compatibility through an explicit migration plan; a field rename is a breaking query contract unless aliases/views are managed.
4. Keep stable event identity, observed event time, null reasons, collection tiers and physical duration ticks unchanged by the ASIM naming decision.
5. Run real DuckDB conformance and replay tests against fixed fixture data before setting any family to `Verified`.

**Related source-verified blockers:** [`reports/2026-11-23-c03-c10-source-verification.md`](../reports/2026-11-23-c03-c10-source-verification.md).
