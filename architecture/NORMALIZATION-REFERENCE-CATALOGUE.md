# Normalization Reference Catalogue

**Status:** methodology under Accepted [DEC-0038](../decisions/DEC-0038-medallion-schema-conventions.md); source mapping and conformance work open under C10/C12/C14. This document is not a second schema authority or new runtime dependency.

## Reference layers

| Layer | Evidence | Purpose |
|---|---|---|
| Logical schema | Published field definitions, roles, types, conditions and values | Canonical semantic candidates |
| Native table | Published source-specific structures | Input and representation constraints |
| Parser implementation | Pinned YAML and embedded KQL | Source extraction, field mapping and transformation evidence |
| Validation | Tester definitions and source fixtures | Candidate conformance requirements |

Microsoft Sentinel is the initial provider. The existing [mapping baseline](ASIM-GOLD-MAPPING-BASELINE.md) and [target-field inventory](ASIM-GOLD-TARGET-FIELDS.csv) remain the mapping register; the C# catalogue governs runtime contracts. Retain upstream names only in reference attribution and provenance. Do not rename existing paths or public identifiers.

## Extraction and review

Use the existing [offline reference tooling](../tools/asim/README.md) for pinned acquisition and metadata extraction. Inspect relevant KQL expressions and source schemas on demand, recording unresolved dependencies and unsupported constructs where they affect a mapping. Syntax alone cannot establish binding or behavioral equivalence. Do not silently approximate. A standalone AST analyser, automated dependency closure and exhaustive transformation extraction are deferred until a measured need justifies them.

Classify filters, direct mappings, renames, constants, typed conversions, conditional expressions, static lookups, structured/text extraction, dynamic objects, aliases and projections. Distinguish source extraction (Agent/Parse) from Platform record-local mapping and enrichment under DEC-0005/0006. Do not copy reference parser execution into the server or implement all Kusto operators. Stateful analytics remain outside normalization.

Each candidate mapping records source selector/path and type, canonical target and type, expression or enumeration, source and target versions, missing/invalid/collision behavior, original evidence retention, applicability, component ownership, reference location, compatibility disposition and fixture. Distinguish verified source evidence, inferred mappings and unresolved candidates. No automatic adoption, fabricated values or implicit case folding.

## Authentication first

The current manifest pins Azure/Azure-Sentinel at b2c15c11d6666b9ddf80091663e6c8009058fbcb and includes the filtering Windows contributor. The following additional parser paths and Git blobs are included in the manifest and were verified against that same revision. Their semantic applicability requires source-specific fixtures; acquisition does not imply conformance.

| File under Parsers/ASimAuthentication/Parsers | Git blob |
|---|---|
| ASimAuthenticationMicrosoftWindowsEvent.yaml | 460c1e6866429cf9c4d4e58716330208af97f4ea |
| ASimAuthenticationSshd.yaml | ab84c53973cd50328b4eb9bbfce9a0aa46be4ee5 |
| vimAuthenticationSshd.yaml | 5e5bb977ba8adf1a5684f934e6d5cb1ee7115fd6 |
| ASimAuthenticationSu.yaml | f699735e684d5b42a1bac54d3412d620107f68d7 |
| vimAuthenticationSu.yaml | 7246f04392ef2db124fe64c919a065e512e2fc35 |
| ASimAuthenticationSudo.yaml | ffae8f6bb74091238ad9227107f604370762d11e |
| vimAuthenticationSudo.yaml | 8f4faca650270a2749b300ef673512e8cce93df9 |

Reference: [pinned Authentication parser directory](https://github.com/Azure/Azure-Sentinel/tree/b2c15c11d6666b9ddf80091663e6c8009058fbcb/Parsers/ASimAuthentication/Parsers). Linux and macOS acquisition and source coverage remain open; do not infer macOS support from Linux parsers.

Start with Windows Security 4624/4625 in an end-to-end Authentication detection slice, then add logoff and OpenSSH. First reconcile operation, result, actor/target, source/reporting device, authentication method/protocol, native classification, occurrence identity and observed time. Verify actual Windows Agent output before correcting mapping mismatches. Add synthetic and captured Linux and macOS fixtures as sources become available. Test exact names, case collisions, nulls, conversion failures, native value preservation and equivalent detection semantics; do not claim platform coverage from synthetic fixtures alone.

## Completion

C10 owns semantic dispositions and conformance, C12 source acquisition/extraction, C14 deterministic regeneration and capability compatibility. C06/C07 consume verified mappings and lineage. No new roadmap IDs, Gold views, wire changes or public field renames are authorized.
