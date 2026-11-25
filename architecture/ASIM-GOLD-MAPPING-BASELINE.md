# ASIM-first Gold mapping baseline — source inventory and candidate mappings

**Review:** 2026-11-23. **Status:** source-backed design inventory, NOT an implemented migration or claim of ASIM compliance.
**Governing Decisions:** Accepted `DEC-0013` (ASIM-first Gold), `DEC-0012` (single schema catalogue), `DEC-0029` (event time), `DEC-0033` (LocalStream / DuckLake).

**Approved target scope:** [DEC-0034](../decisions/DEC-0034-mvp-asim-tables-and-views.md) selects eight telemetry families plus two operational alert views. This baseline still inventories the four existing telemetry contracts. Extend it for File Event, User Management, Registry Event and Audit Event during C10; do not interpret approval as source implementation or conformance.

## Source revision and reference pin

- Platform source: [`60d6588071eb187cddf61baa77b9991cc793e25f`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/tree/60d6588071eb187cddf61baa77b9991cc793e25f).
- Gold definitions: [`GoldenEventContracts.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Golden/GoldenEventContracts.cs).
- Silver contributors: [`SilverParserContributors.cs`](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/60d6588071eb187cddf61baa77b9991cc793e25f/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Silver/SilverParserContributors.cs).
- Microsoft ASIM [schema overview](https://learn.microsoft.com/en-us/azure/sentinel/normalization-about-schemas): reviewed 2026-11-23. The listed DNS, Network Session, Process Event and Authentication schema versions are **1.0.0**.
- Per-family references: [DNS](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-dns), [Network Session](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-network), [Process Event](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-process-event), [Authentication](https://learn.microsoft.com/en-us/azure/sentinel/normalization-schema-authentication).

**Pinned tester reference (2026-11-25):** [Microsoft ASimTester.csv](https://github.com/Azure/Azure-Sentinel/blob/b2c15c11d6666b9ddf80091663e6c8009058fbcb/ASIM/dev/ASimTester/ASimTester.csv), Git blob `de261f4c8e3d41f35801c00ca830aec01cbc8c94`. The machine-readable [target field inventory](ASIM-GOLD-TARGET-FIELDS.csv) accounts for every tester field in the four families, merging Common rows by field name with family-specific rows taking precedence. This is the reverse-index appendix to this baseline, not a separate schema contract. The tester and published schema documentation must still be reconciled where they differ; its snapshot is not a claim that each tester row belongs to ASIM 1.0.0 or that Microsoft-specific runtime fields apply unchanged.

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

**Drift check:** the `governs-check` workflow runs
`.github/scripts/gold_inventory_check.py` against the latest checked-out
Platform C# field declarations. It compares the four families, every field
name, declared Kusto/DuckDB type and column order. It **does not** validate
ASIM enum normalization, mandatory values, role semantics or integration.


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


## Target-side gap accounting (reviewed 2026-11-25)

This supplements the existing-field inventory without creating another mapping authority. Use the referenced family schema and common-fields specification for the complete upstream field set. The following dispositions apply to all eight contributors; none is a verified production mapping.

| Target requirement | Candidate source / disposition | Verification gate |
|---|---|---|
| EventCount | 1 only for a proved single event; aggregate cardinality from source | No assumed count for aggregated/unknown input |
| EventStartTime, EventEndTime | observed source timestamp(s); equal only for an instantaneous event | C11, UTC normalization, time interval semantics |
| EventType | source event and family-specific operation | schema-specific vocabulary, no inference from name alone |
| EventResult | explicit success/failure/result, or documented family derivation | unknown evidence must not become success |
| EventProduct, EventVendor | verified source profile/catalog metadata | distinguish reporting product from agent and collector |
| EventSchema, EventSchemaVersion | schema registration, not source assertion | publish only correct schema/version and conformance status |
| Dvc | reporting device alias with role-preserving source metadata | confirm identity and companion type rules |

Additional family requirements and conditional groups:

- DNS: account for DNS query name and mandatory DNS result detail; use request-vs-response semantics and verified response-code name lookup. Preserve query/answer multiplicity. Source/destination device identity, domain and username companions apply only when their triggering fields are populated.
- Network Session: distinguish endpoint-relative and wire roles; validate endpoint event type, direction, result/action derivation, port/protocol values and application protocol companions. Source/destination device and user ID/domain/name type companions and threat field applicability must be checked.
- Process Event: account for actor username, acting PID, target process name/PID and command line (mandatory in the published table); preserve creator/parent/target roles. Validate conditional username/ID types, hash type and rule alias when applicable. Missing process evidence is a gap, not a fabricated value.
- Authentication: account for logon versus other operations and result details, Windows status/substatus and account roles. Conditional actor/target user types, source/target device ID/domain types, target application type and threat field must follow the actual populated trigger fields.

Recommended fields remain optional implementation scope but must be inventoried, and any exclusion recorded. Use the common-fields and family reference tables (including prose conditions and alias rules) to enumerate every target field before freezing the C# contract. The grouped accounting above is supplemented by the pinned tester-derived reverse inventory below. Complete semantic dispositions, documentation/tester discrepancy review and source fixtures remain C10 acceptance gates. No new schema is published here.

## Pinned reverse field inventory

| Family | Tester-specific rows | Rows after Common merge |
|---|---:|---:|
| DNS | 153 | 156 |
| Network Session | 189 | 192 |
| Process Event | 170 | 173 |
| Authentication | 162 | 165 |
| Total | 674 | 686 |

The CSV records every target field, type, requirement class, logical type, related field (including conditional triggers/alias relationships where supplied), reference scope and preliminary disposition. Candidate inputs are deliberately conservative, unverified and not executable transformations. An empty candidate is a review item, not an assertion of impossibility. Optional fields require scope review, not mandatory implementation. Family-specific rows override Common rows; the complete upstream record (including enum lists and dynamic shape constraints) remains retrievable at the pinned reference. Counts include aliases and Microsoft-specific columns such as `Type` and `TimeGenerated`; document derivations or explicit DeltaZulu deviations rather than silently inventing their values. The tester also identifies `Src` as mandatory for DNS and mandatory actor/target process fields in ProcessEvent. Confirm conditions against published prose before freezing mappings. No semantic conformance or deployment verified.
