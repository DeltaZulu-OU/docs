---
id: DEC-0038
status: Accepted
repos: [DeltaZulu.Agent, DeltaZulu.Parse, DeltaZulu.Forward, DeltaZulu.Platform, DeltaZulu.Kql, DeltaZulu.LocalStream]
governs:
  types: []
  paths: []
cites: [CON-0014, CON-0015]
---

# DEC-0038 — Consolidated Medallion schema, naming and field normalization conventions

## Context

Owner approved the consolidated conventions on 2026-11-26. Existing decisions distribute schema authority, naming and normalization across layers. Native spelling differences such as EventId/EventID and RecordId/EventRecordID require explicit semantic mapping rather than implicit equivalence.

## Decision

### Authority and supersession

DeltaZulu owns its logical contracts, field definitions, types, enumerations and versions. One producer-independent governed catalogue is authoritative for each logical contract and generated physical projections. Prefer pinned ASIM semantics, names, entity roles, types and values wherever faithful; explicitly document extensions, omissions and deviations. OCSF is not the canonical authority. External names identify reference material, not runtime prefixes or namespaces. No Sentinel runtime dependency.

This decision supersedes the schema and naming provisions of DEC-0012, DEC-0013 and DEC-0034; their remaining requirements and approved MVP inventory remain binding. DEC-0028 remains Superseded by DEC-0033; retain code-generated contracts without reviving Proton. DEC-0005/0006, DEC-0003, DEC-0016, DEC-0029, DEC-0030, DEC-0032, DEC-0033, DEC-0036 and DEC-0037 retain their respective boundaries.

### Layer and relation conventions

| Layer/object | Convention | Example |
|---|---|---|
| Bronze | Source evidence, minimally interpreted; physical relation snake_case | bronze.windows_security_event |
| Silver | Typed source-specific telemetry; physical relation snake_case | silver.windows_security_event |
| Silver normalization contributor | Descriptive snake_case | silver.v_authentication_windows_security_eid4624 |
| Gold | Source-independent logical singular PascalCase | Authentication |
| Gold SQL view | golden namespace, singular PascalCase | golden.Authentication |
| Physical backing relation | snake_case, not public query identifier | lake.alert_events |

Retain Authentication, Dns, NetworkSession, ProcessEvent, FileEvent, RegistryEvent, UserManagement, AuditEvent, AlertEvent and AlertEntity. KQL names are unqualified. No historical Activity suffix, vendor table/parser prefix, pluralized public name or alternative gold namespace.

### Bronze

Preserve original source spelling, capitalization, nesting and meaning where the format permits. System-owned envelope columns use snake_case (ingest_time, source_name, provider, host, raw_log, raw_text). Isolate source-controlled fields from system metadata; no overwrite of acquisition, delivery, provenance or identity metadata. No silent rename, merge, coercion or discard. Original-byte preservation follows collection and integrity policy; structured JSON is not proof of byte equality.

### Silver

DeltaZulu-owned typed logical fields use PascalCase; native names remain mapping inputs and provenance. Retain source-specific semantics where Gold owns normalization. Agent-authoritative extraction remains authoritative; no routine server reparse. Declare source path, target, type, transformation, null behavior and source version. Explicit source-scoped aliases require established semantic equivalence; generic case or punctuation conversion does not establish it.

### Gold and field naming

Use PascalCase logical fields, source-independent semantic roles and pinned reference spelling for adopted fields (SrcIpAddr, DvcFQDN). New custom fields use conventional PascalCase acronym treatment (EventId, SourceIpAddress, ProcessGuid). Use established entity prefixes (Src, Dst, Actor, Target, Dvc) where applicable, typed identity companions and explicit distinction between classification and occurrence identity. Avoid ambiguous Id, Type or Status and physical storage types in names; use unit suffixes where needed, not instead of declared types. Separate operation, outcome, context, method, protocol and native classification where supported. Canonical user identity is not inherently a Windows SID. Equivalent Windows, Linux, macOS, cloud and application events contribute to common families.

### Resolution and aliases

Preserve exact declared spelling. Generate SQL projections and KQL identifiers from the same contract; respect engine-specific identifier semantics. Use explicit canonical mapping targets, reject ambiguous collisions including case-only collisions where a supported consumer cannot distinguish them. Source lookup follows source-format semantics; case-insensitive lookup requires explicit source mapping and collision behavior. Unknown fields do not automatically become canonical. Use format-aware SQL quoting, JSON access and KQL binding.

One canonical definition per field. Aliases derive from it and declare target, reason, applicability and compatibility lifetime; never conceal differing types, roles or meanings. No duplicate persisted values solely for aliases absent measured approved optimization. Public renames require migration review.

### Normalization

Deterministic, versioned, traceable record-local contributors may use direct assignment, rename, typed conversion, constants, conditions, static enumeration lookup, structured/regex extraction and scalar normalization. Stateful analytics, temporal correlation, aggregation and operational deduplication are separate. Structured and regex extraction in reference parsers describes source extraction requirements; it does not authorize routine server-side re-extraction of authoritative Agent fields under DEC-0005/0006. Multiple family contributions preserve shared lineage and distinct representation identities under DEC-0037. No fabricated facts; preserve original evidence for many-to-one value mappings.

Distinguish absent, null, inapplicable, unsupported, invalid and failed conversion where representable. No invented empty string, zero, false, ingest time or identifier substitutes. Preserve null/loss reasons. DEC-0029 governs observed time; DEC-0037 governs identity. Logical types are independent of wire and database representation; generate projections from catalogue, honor UTC, duration ticks and loss contracts, diagnose unknown types rather than silently coercing to string.

### Reference catalogue and evolution

Maintain a provider-neutral Normalization Reference Catalogue: schema definitions, native structures, source-to-canonical mappings, expressions, enumeration mappings, constraints, validation definitions and fixtures. Microsoft Sentinel is the initial reference provider. Pin revisions, paths, content hashes, parser/schema versions and applicable licenses. Deterministic offline regeneration; external parsers are evidence, not runtime dependencies.

Version logical schemas and mappings independently as needed. Classify additive, corrective and breaking changes by producer, consumer, persistence and detection impact. Renames, type/semantic/enum changes and incompatible null behavior require migration assessment. Preserve historical schema/mapping identities for provenance. No automatic upstream adoption. This decision does not authorize existing relation renames, published contract changes or incompatible wire changes.

### Verification

Validate exact spelling, collisions, source variants, missing/invalid/ambiguous fields, conversion failures, enumeration mappings, metadata isolation, alias equivalence, version compatibility, identity and evidence preservation and equivalent cross-platform semantics. Authentication is the first conformance family; Windows first implemented contributor, Linux and macOS fixtures inform later contributors. No claim of current conformance.

## Consequences

Apply relevant completion criteria to C03, C05, C06, C07, C10, C11, C12 and C14 without new roadmap IDs or priority changes. Physical naming and cross-engine resolution require executable verification before migration.

## Alternatives rejected

| Alternative | Why not |
|---|---|
| Independent layer authorities | Contract drift |
| Uniform case conversion | Native meaning loss and collisions |
| Gold naming in Bronze | Evidence loss |
| Native naming in Gold | Source-dependent analytics |
| Vendor prefixes | Confuses reference and ownership |
| Implicit aliases | Conceals ambiguity |
| Automatic upstream adoption | Uncontrolled compatibility changes |

## Revisit trigger

Reopen on reproducible evidence that a supported source, engine or store cannot preserve these contracts without unacceptable fidelity, compatibility or performance costs.

## References

- https://learn.microsoft.com/en-us/azure/sentinel/normalization-about-schemas
- https://learn.microsoft.com/en-us/azure/sentinel/isv/normalization-develop-parsers
- https://github.com/Azure/Azure-Sentinel/tree/master/Parsers
