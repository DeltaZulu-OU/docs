#!/usr/bin/env python3
"""Offline extraction and reconciliation of pinned ASIM reference metadata."""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import sys

from markdown_it import MarkdownIt
import yaml

from reference import CACHE, FAMILIES, MANIFEST, OUTPUT, ROOT, atomic_write, read_manifest, read_verified

TYPES = {"string", "datetime", "long", "bool", "dynamic", "int", "real", "decimal", "timespan", "guid"}
CLASSES = {"Mandatory", "Recommended", "Optional", "Conditional", "Alias"}
TESTER_HEADER = ["ColumnName", "ColumnType", "Class", "Schema", "LogicalType", "ListOfValues",
                 "Aliased", "DynamicType", "ArrayValuesType"]
MAPPING_HEADER = ["family", "field", "kql_type", "requirement", "logical_type", "related_field",
                  "reference_scope", "disposition", "candidate_input"]
MAPPING = ROOT.parent.parent / "architecture" / "ASIM-GOLD-TARGET-FIELDS.csv"


class UniqueYamlLoader(yaml.BaseLoader):
    """Preserve source scalar spelling and reject duplicate mapping keys."""


def unique_mapping(loader, node):
    result = {}
    for key, value in loader.construct_pairs(node, deep=True):
        if not isinstance(key, str) or key in result:
            raise ValueError(f"invalid or duplicate YAML key: {key!r}")
        result[key] = value
    return result


UniqueYamlLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def parse_yaml(text: str) -> dict:
    obj = yaml.load(text, Loader=UniqueYamlLoader)
    if not isinstance(obj, dict):
        raise ValueError("expected YAML mapping")
    return obj


def rows(text: str, header: list[str]):
    reader = csv.DictReader(io.StringIO(text, newline=""), strict=True)
    if reader.fieldnames != header:
        raise ValueError(f"unexpected CSV header: {reader.fieldnames!r}")
    for row in reader:
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f"malformed CSV row {reader.line_num}")
        yield row


def parse_tester(text: str) -> tuple[dict, list]:
    scopes = {s: {} for s in ("Common", *FAMILIES)}
    for row in rows(text, TESTER_HEADER):
        scope, name = row["Schema"], row["ColumnName"]
        if scope not in scopes:
            continue
        if not name or row["ColumnType"] not in TYPES or row["Class"] not in CLASSES:
            raise ValueError(f"unrecognized tester field/type/class: {scope}/{name}: {row}")
        if name in scopes[scope]:
            raise ValueError(f"duplicate tester field: {scope}/{name}")
        scopes[scope][name] = row
    if any(not fields for fields in scopes.values()):
        raise ValueError("missing tester scope")
    merged, overrides = {}, []
    for family in FAMILIES:
        common = scopes["Common"]
        specific = scopes[family]
        for name in sorted(common.keys() & specific.keys()):
            if any(common[name][k] != specific[name][k] for k in TESTER_HEADER if k != "Schema"):
                overrides.append({"family": family, "field": name, "common": common[name], "family_specific": specific[name]})
        merged[family] = dict(sorted((common | specific).items()))
    return merged, overrides


def parse_native(text: str, table: str) -> dict[str, str]:
    tokens = MarkdownIt("commonmark").enable("table").parse(text)
    titles = [tokens[i+1].content for i, t in enumerate(tokens[:-1]) if t.type == "heading_open" and t.tag == "h1"]
    if table not in titles:
        raise ValueError(f"native table heading missing: {table}")
    starts = [i for i,t in enumerate(tokens[:-1]) if t.type == "heading_open" and t.tag == "h2" and tokens[i+1].content == "Columns"]
    if len(starts) != 1:
        raise ValueError(f"expected one Columns section: {table}")
    result = []
    current = None
    in_table = False
    for token in tokens[starts[0]+3:]:
        if token.type == "heading_open" or token.type == "table_close":
            break
        if token.type == "table_open":
            in_table = True
        elif in_table and token.type == "tr_open":
            current = []
        elif in_table and token.type == "inline" and current is not None:
            current.append(token.content.strip())
        elif in_table and token.type == "tr_close":
            result.append(current)
            current = None
    if not result or result[0] != ["Column", "Type", "Description"]:
        raise ValueError(f"unexpected native column header: {table}")
    fields = {}
    for row in result[1:]:
        if len(row) != 3 or not row[0] or row[1] not in TYPES or row[0] in fields:
            raise ValueError(f"duplicate or unrecognized native column: {table}: {row}")
        fields[row[0]] = row[1]
    if not fields:
        raise ValueError(f"empty native table: {table}")
    return fields


def compare_native(tester: dict, native: dict) -> dict:
    return {
        "native_only": sorted(native.keys() - tester.keys()),
        "tester_only": sorted(tester.keys() - native.keys()),
        "type_conflicts": [
            {"field": name, "tester": tester[name]["ColumnType"], "native": native[name]}
            for name in sorted(tester.keys() & native.keys())
            if tester[name]["ColumnType"] != native[name]
        ],
    }


def check_mapping(text: str, tester: dict) -> None:
    expected = {
        (family, name): (r["ColumnType"], r["Class"], r["LogicalType"], r["Aliased"], r["Schema"])
        for family, fields in tester.items() for name, r in fields.items()
    }
    seen = set()
    for r in rows(text, MAPPING_HEADER):
        key = (r["family"], r["field"])
        actual = tuple(r[k] for k in MAPPING_HEADER[2:7])
        if key in seen or key not in expected or actual != expected[key] or not r["disposition"]:
            raise ValueError(f"mapping inventory differs from pinned tester: {key}")
        seen.add(key)
    if seen != expected.keys():
        raise ValueError(f"mapping inventory missing {len(expected.keys() - seen)} tester entries")


def build_reference(manifest: dict, cache: Path) -> dict:
    tester = None
    overrides = []
    native, schemas, parsers, provenance = {}, {}, {}, []
    diagnostics = []
    for entry in manifest["files"]:
        data = read_verified(cache, manifest, entry)
        key = entry["source"] + "/" + entry["path"]
        provenance.append({**entry, "sha256": hashlib.sha256(data).hexdigest(), "size": len(data)})
        kind = entry["kind"]
        if kind in {"license", "upstream-test"}:
            continue
        text = data.decode("utf-8-sig")
        try:
            if kind == "tester":
                tester, overrides = parse_tester(text)
            elif kind == "native-table":
                family = entry["family"]
                native[family] = parse_native(text, manifest["families"][family])
            elif kind == "schema":
                meta = parse_yaml(text)
                schemas[key] = meta
                fields = meta.get("Fields", [])
                if not isinstance(fields, list):
                    raise ValueError("expected schema field list")
                seen = set()
                for field in fields:
                    if not isinstance(field, dict):
                        raise ValueError("invalid schema field")
                    name, typ = field.get("Name"), field.get("Type")
                    if not name or name in seen or typ not in TYPES or field.get("Class") not in CLASSES:
                        diagnostics.append({"source": key, "kind": "schema-field-review", "field": field})
                    seen.add(name)
            elif kind == "parser":
                meta = parse_yaml(text)
                # Never execute the upstream parser. Retain all metadata, with
                # the original query available in the verified reference cache.
                query = meta.pop("ParserQuery", None)
                parsers[key] = {"family": entry["family"], "has_query": bool(query), "metadata": meta}
                normalization = meta.get("Normalization")
                if not isinstance(normalization, dict) or not normalization.get("Schema") or not normalization.get("Version"):
                    diagnostics.append({"source": key, "kind": "parser-normalization-metadata-review"})
                elif normalization["Schema"] != entry["family"]:
                    diagnostics.append({"source": key, "kind": "parser-family-review", "declared": normalization["Schema"], "selected": entry["family"]})
        except (ValueError, yaml.YAMLError, csv.Error) as exc:
            raise ValueError(f"{key}: {exc}") from exc
    if tester is None or set(native) != set(FAMILIES):
        raise ValueError("missing selected reference inputs")
    return {
        "schema_version": 1,
        "tool_version": manifest["tool_version"],
        "sources": manifest["sources"],
        "families": manifest["families"],
        "provenance": provenance,
        "tester_fields": tester,
        "common_overrides": overrides,
        "native_tables": native,
        "native_tester_differences": {f: compare_native(tester[f], native[f]) for f in FAMILIES},
        "common_entity_metadata": schemas,
        "parser_metadata": parsers,
        "diagnostics": diagnostics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--cache", type=Path, default=CACHE)
    parser.add_argument("--output", type=Path, default=OUTPUT / "reference-catalogue.json")
    parser.add_argument("--mapping", type=Path, default=MAPPING)
    args = parser.parse_args()
    try:
        reference = build_reference(read_manifest(args.manifest), args.cache)
        check_mapping(args.mapping.read_text(encoding="utf-8"), reference["tester_fields"])
        atomic_write(args.output, (json.dumps(reference, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8"))
        for family in FAMILIES:
            diffs = reference["native_tester_differences"][family]
            print(f"{family}: {len(reference['tester_fields'][family])} tester fields, {len(reference['native_tables'][family])} native columns; "
                  f"{len(diffs['native_only'])} native-only, {len(diffs['tester_only'])} tester-only, {len(diffs['type_conflicts'])} type conflicts")
        print(f"{len(reference['diagnostics'])} metadata review diagnostics; no ASIM conformance claim")
        return 0
    except (OSError, ValueError, KeyError, csv.Error, yaml.YAMLError) as exc:
        print(f"ASIM extraction failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
