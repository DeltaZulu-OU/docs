# C06/C07 detection provenance — initial source reconciliation

Date: 2026-11-26. Scope: selected source contracts, not a complete implementation or test audit. DEC-0036 is Accepted; C06/C07 remain open.

## Observed contracts

| Source at pinned revision | Observation | Disposition |
|---|---|---|
| [Platform accepted version](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Detection/References/AcceptedDetectionVersionRef.cs) | Stable detection/version IDs, optional Git SHA, sequence and acceptance time | Reuse; verify content resolution and retention |
| [Platform detection projection](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Analytics/Detections/DetectionRecord.cs) | Query, hash, version, suppression policy and optional accepted version ID | Extend or reconcile; verify immutable effective deployment |
| [Platform alert writer](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Data.DuckDb/Analytics/Alerts/DuckDbAlertLakeWriter.cs) | Ordinary INSERT into lake.alert_events; no uniqueness enforcement in inspected writer | Verify surrounding deduplication and replace or adapt sink for DEC-0030/0033; not proof of end-to-end duplicates |
| [LocalStream record](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream/StreamRecord.cs) | EventId distinct from stream coordinates; nullable event time | Reuse; verify producer namespace and Gold lineage |
| [LocalStream result identity](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/Results/ResultIdentityBuilder.cs) | SHA-256, versioned length-delimited fields, query revision and source offsets | Reuse for change identity only, never substitute for alert identity |
| [LocalStream query change](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/Results/QueryChange.cs) | Upsert/correction/delete/finalize; source range, logical key and version | Extend generic causal hooks if needed; source range alone does not identify all contributors |
| [LocalStream tumbling operator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/Operators/TumblingWindowAggregateOperator.cs) | Transactional state, late-event decision, corrections and finalization | Reuse; verify boundary and recovery fixtures |

## Next verification

Trace Agent and Forward event identity generation and propagation, Gold representation cardinality, Platform accepted-content resolution and binding, LocalStream state/outbox/checkpoint behavior, existing test coverage and DuckLake sink integration. Verify CON-0021 against packed consumers. No tests executed in this review; no production interface certified. See the [proposed joint contract](../architecture/DETECTION-RESULT-CONTRACT.md) for design directions and unresolved gates. The consolidated roadmap remains the only planning authority.

## Identity propagation and legacy mediation follow-up

| Pinned source | Verified observation | Required verification or remediation |
|---|---|---|
| [Agent resource record](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/blob/e2aac89dafc2f8499e4e4d22ebed97cec75714fe/src/DeltaZulu.Pipeline/Core/Events/ResourceOutputRecord.cs) | Source metadata can carry eventUid; projection metadata preservation explicitly lists five delivery fields but not eventUid | Test source-shaped projections and identity preservation; do not assign source identity to derived aggregates |
| [Agent mapper](https://github.com/DeltaZulu-OU/DeltaZulu.Agent/blob/e2aac89dafc2f8499e4e4d22ebed97cec75714fe/src/DeltaZulu.Pipeline/Core/Delivery/ResourceOutputRecordForwardMapper.cs) | RecordId/ID or fresh GUID; fresh DeliveryId; eventUid not explicitly mapped | C05: test repeated mapping and buffered retries separately; define stable acquisition identity and namespace |
| [Forward record](https://github.com/DeltaZulu-OU/DeltaZulu.Forward/blob/19b3d000697922870742f52ba46e8b4fc3de3ee6/src/DeltaZulu.Forward/ForwardLogEnvelope.cs) | RecordId documented batch-local; BatchId dedup/ACK; optional OriginAgentId | Do not equate batch dedup with event dedup; evaluate existing carriers before any wire change |
| [Raw ingestion](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Ingestion/PubSub/RawLogEnvelope.cs) | No dedicated event identity property | Trace actual collector routes and payload identity before asserting end-to-end loss |
| [Gold contracts](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Golden/GoldenEventContracts.cs) | Authentication EventId is Windows Security event code | C10: separate classification code from unique evidence identity |
| [Legacy mediation](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/4c5aafcdc3c2ba92e7c1c933e2c982d1516ec1fb/src/DeltaZulu.Platform.Application/Analytics/Mediation/AlertMediationService.cs) | Fallback materialization key includes version and run ID; logs permanent loss after three failed writes | C07: do not reuse as DEC-0030 alert dedup key; replace legacy Proton mediation in target integration |
| [State transaction](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/State/IStateTransaction.cs) | State, watermark, output intents and cursor commit exposed together | Verify concrete backend atomicity and recovery |
| [Output intent](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/State/OutputIntent.cs) | Target, change ID and exact payload | Reuse candidate; verify durable payload ownership and idempotent sink |
| [Checkpoint](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/222d654c15d5d32b5606fc8a11b874b472ea7995/src/DeltaZulu.LocalStream.Query/State/CheckpointManifest.cs) | Domain, range, cursor, watermark and generation | Verify crash recovery and expiry behavior |

These are static observations, not executed regressions. Neither end-to-end identity loss nor a need for a wire change has been established.
