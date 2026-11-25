# ASIM reference acquisition and extraction

This is C10 development tooling under [DEC-0034](../../decisions/DEC-0034-mvp-asim-tables-and-views.md), not a production dependency or a second logical schema authority. The eight selected telemetry families are the only target families. The two operational alert views remain DeltaZulu-owned.

The [manifest](sources.json) pins the upstream commit and Git blob identity for every selected file. It contains Microsoft's ASimTester, common and entity YAML, selected unifying/native/empty and Windows source parser YAML, relevant upstream test CSVs, eight native table definitions and licence files. Upstream test CSVs are retained as reference evidence, not executed tests of DeltaZulu. Official logical schema prose is a separate reference layer; a verified immutable source snapshot and field-level reconciliation remain open.

## Usage

Install the same Python dependencies used by the verification workflow:

```sh
python3 -m pip install PyYAML==6.0.3 markdown-it-py==4.2.0
```

Explicitly acquire and verify the pinned files:

```sh
python3 tools/asim/fetch.py
```

Extract locally and check the existing mapping inventory:

```sh
python3 tools/asim/extract.py
```

Run the offline unit tests:

```sh
python3 -m unittest discover -s tools/asim/tests -v
```

The local .cache directory is ignored. Corrupt cached files fail verification; remove the offending cache file and acquire again. Normal governance tests never download upstream files. The separate snapshot verification workflow is explicit and limited to the development branch or manual dispatch. Generated metadata is ignored by Git and available as a CI artifact when that workflow succeeds. The extractor performs no network access and does not execute Microsoft KQL. It validates the target-field CSV without altering its mapping dispositions.

Native columns, tester fields, family-specific overrides, common/entity metadata, parser metadata, and unresolved differences are separate. Unknown native/tester types, duplicate field keys, malformed files, missing files and hash mismatches fail closed. Upstream YAML schema-field or parser metadata discrepancies are reported with their original values. No silent string fallback, no automatic semantic mapping, and no assertion of ASIM conformance.

## Attribution and licensing

Azure/Azure-Sentinel content is copyright Microsoft Corporation, MIT; MicrosoftDocs/azure-monitor-docs documentation is provided under CC BY 4.0. The pinned upstream licence files are fetched and checked with the inputs. The generated catalogue is an adapted reference inventory; the provenance list includes original repository, revision, path, Git blob and SHA-256. The manifest specifies the applicable licences. Raw upstream files are not committed or distributed as repository content. Review attribution and applicable licence conditions before any further redistribution.

## Update procedure

Review and update the pinned revisions and file list explicitly; verify every Git blob against the selected revision. Fetch into a fresh revision-specific cache, regenerate, compare output, reconcile tester/native/documentation differences and review mapping changes. Never follow upstream master automatically or replace the C# contract from generated metadata.
