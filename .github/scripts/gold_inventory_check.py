#!/usr/bin/env python3
"""Fail when Platform's C# Gold field inventory drifts from the ASIM mapping register.

This checks names, types, family coverage and field order only; it does NOT
certify semantic conformance, valid ASIM enumerations, or source transformations.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

EXPECTED = ("Dns", "NetworkSession", "ProcessEvent", "Authentication")
CONTRACT = Path("src/DeltaZulu.Platform.Domain/Analytics/Schema/Definitions/Medallion/Golden/GoldenEventContracts.cs")
REGISTER = Path("architecture/ASIM-GOLD-MAPPING-BASELINE.md")
SECTION = re.compile(r"public\s+static\s+readonly\s+IReadOnlyList<ColumnDef>\s+(\w+)Columns\s*=\s*\[([\s\S]*?)\];")
FIELD = re.compile(r'\bnew(?:\s+ColumnDef)?\s*\(\s*"([^"]+)"\s*,\s*DuckDbType\.(\w+)\s*,\s*KustoType\.(\w+)')
CATALOG = CONTRACT.parent.parent / "MedallionSchemaCatalog.cs"
CANONICAL = re.compile(r"CanonicalViews\s*\{\s*get;\s*\}\s*=\s*\[([\s\S]*?)\];")
DOC_SECTION = re.compile(r"^## `golden\.(\w+)` — (\d+) fields[^\n]*\n([\s\S]*?)(?=^## |\Z)", re.MULTILINE)
DOC_FIELD = re.compile(r"^\| `([^`]+)` \| `(\w+) / (\w+)` \|", re.MULTILINE)


def extract_code(source: str) -> dict[str, list[tuple[str, str, str]]]:
    result = {}
    for family, body in SECTION.findall(source):
        if family in result:
            raise ValueError(f"duplicate Gold C# definition: {family}")
        # Only recognize the current collection-expression syntax; fail on
        # unsupported items rather than silently omitting them.
        items = []
        start = depth = 0
        quoted = escaped = False
        for i, ch in enumerate(body):
            if quoted:
                if escaped:
                    escaped = False
                elif ch == "\\":
                    escaped = True
                elif ch == '"':
                    quoted = False
            elif ch == '"':
                quoted = True
            elif ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
            elif ch == "," and depth == 0:
                items.append(body[start:i].strip())
                start = i + 1
        items.append(body[start:].strip())
        if quoted or depth != 0:
            raise ValueError(f"unbalanced Gold column list: {family}")
        fields = []
        for item in filter(None, items):
            match = FIELD.match(item)
            if match is None:
                raise ValueError(f"unrecognized Gold column in {family}: {item}")
            field, duckdb, kusto = match.groups()
            fields.append((field, kusto, duckdb))
        if len({f[0] for f in fields}) != len(fields):
            raise ValueError(f"duplicate Gold field in {family}")
        result[family] = fields
        if not result[family]:
            raise ValueError(f"no columns parsed for Gold family {family}")
    return result


def extract_register(markdown: str) -> dict[str, list[tuple[str, str, str]]]:
    result = {}
    for family, count, body in DOC_SECTION.findall(markdown):
        if family in result:
            raise ValueError(f"duplicate ASIM register section: {family}")
        fields = DOC_FIELD.findall(body)
        if int(count) != len(fields):
            raise ValueError(f"ASIM register section {family}: expected {count}, found {len(fields)} rows")
        result[family] = fields
    return result


def check(source: str, markdown: str) -> list[str]:
    code = extract_code(source)
    docs = extract_register(markdown)
    failures = []
    for label, inventory in (("code", code), ("register", docs)):
        missing = set(EXPECTED) - set(inventory)
        unexpected = set(inventory) - set(EXPECTED)
        if missing:
            failures.append(f"{label}: missing families {sorted(missing)}")
        if unexpected:
            failures.append(f"{label}: unexpected families {sorted(unexpected)}; rebaseline explicitly")
    for family in EXPECTED:
        if family not in code or family not in docs:
            continue
        if code[family] != docs[family]:
            failures.append(
                f"{family}: source columns/types/order differ from registered mapping. "
                f"C#={code[family]!r}; docs={docs[family]!r}"
            )
    return failures


def check_catalog(source: str, families: set[str]) -> None:
    match = CANONICAL.search(source)
    if match is None:
        raise ValueError("cannot parse CanonicalViews registration")
    items = [s.strip() for s in match.group(1).split(",") if s.strip()]
    expected = {"GoldenEventContracts." + family for family in families}
    if len(items) != len(expected) or set(items) != expected:
        raise ValueError("CanonicalViews registration differs from Gold inventory")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".governed"))
    args = parser.parse_args()
    source_file = args.root / "DeltaZulu.Platform" / CONTRACT
    try:
        source = source_file.read_text(encoding="utf-8")
        inventory = extract_code(source)
        failures = check(source, REGISTER.read_text(encoding="utf-8"))
        check_catalog((args.root / "DeltaZulu.Platform" / CATALOG).read_text(encoding="utf-8"), set(inventory))
    except (OSError, ValueError) as exc:
        print(f"::error::{exc}")
        return 1
    for problem in failures:
        print(f"::error::{problem}")
    if failures:
        return 1
    print(f"ASIM register matches {len(inventory)} registered Gold schemas "
          f"({sum(map(len, inventory.values()))} field definitions). Semantic conformance NOT tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
