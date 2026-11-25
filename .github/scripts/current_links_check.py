#!/usr/bin/env python3
"""Check relative Markdown links in current, maintained estate documentation.

Historical imports, archived ADRs and immutable dated verification reports are
excluded: their links are evidence of the original documents, not a live API.
This verifies local link targets, not external URLs, fragment anchors or claims.
"""
from __future__ import annotations

from pathlib import Path
from datetime import date
import re
import sys
from urllib.parse import unquote

LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
CURRENT = [
    "README.md", "CLAUDE.md", "decisions/README.md", "constraints/README.md",
    "roadmaps/README.md", "roadmaps/CONSISTENCY-CORRECTNESS-ROADMAP.md",
    "reports/README.md",
]
HISTORICAL_ARCHITECTURE = {"PIPELINE.md", "DATA-QUALITY-MONITORING.md"}


def maintained_paths(root: Path) -> list[str]:
    return CURRENT + [
        p.relative_to(root).as_posix()
        for p in sorted((root / "architecture").rglob("*.md"))
        if p.name not in HISTORICAL_ARCHITECTURE
    ] + [
        p.relative_to(root).as_posix()
        for p in sorted((root / "decisions").glob("DEC-*.md"))
    ]


def links_for(root: Path, paths: list[str]) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    for rel in paths:
        source = root / rel
        if not source.is_file():
            errors.append(f"{rel}: maintained source document missing")
            continue
        # Inline Markdown links only. Reference-style links and fragments are
        # deliberately not validated; they require a Markdown parser.
        fence = None
        for number, line in enumerate(source.read_text(encoding="utf-8").splitlines(), 1):
            marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
            if marker:
                token, tail = marker.groups()
                if fence is None:
                    fence = token
                    continue
                if token[0] == fence[0] and len(token) >= len(fence) and not tail.strip():
                    fence = None
                    continue
            if fence is not None or line.startswith(("    ", "\t")):
                continue
            for match in LINK.finditer(line):
                target = match.group(1).strip().split("#", 1)[0].split("?", 1)[0]
                if not target or re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("//"):
                    continue
                resolved = (source.parent / unquote(target)).resolve()
                if not resolved.is_relative_to(root) or not resolved.exists():
                    errors.append(f"{rel}:{number}: broken local link {match.group(1)!r}")
    return errors


def roadmap_check(root: Path, today: date) -> tuple[list[str], list[str]]:
    """Validate the single active table and review trigger; warn if overdue."""
    roadmaps = root / "roadmaps"
    active = roadmaps / "CONSISTENCY-CORRECTNESS-ROADMAP.md"
    if not active.is_file():
        return ["active roadmap missing"], []
    source = active.read_text(encoding="utf-8")
    errors, warnings = [], []
    dates = re.findall(r"\*\*Next review:\*\* (\d{4}-\d{2}-\d{2})", source)
    if len(dates) != 1:
        errors.append("active roadmap requires exactly one next review date")
    else:
        try:
            due = date.fromisoformat(dates[0])
            if today > due:
                warnings.append(f"active roadmap review overdue since {due}")
        except ValueError:
            errors.append("invalid roadmap review date")
    header = "| Work item | Priority | Affected projects | Work and current status | Completion criterion | Governing decision / outstanding approval |"
    if source.count(header) != 1:
        errors.append("active roadmap requires exactly one execution table")
    ids = []
    for line in source.splitlines():
        if not line.startswith("| **C"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 6 or any(not c for c in cells):
            errors.append("invalid or incomplete roadmap row: " + line[:80])
            continue
        identifier = re.fullmatch(r"\*\*(C\d{2,})\*\*", cells[0])
        if not identifier:
            errors.append("invalid work identifier: " + cells[0])
            continue
        ids.append(identifier.group(1))
        if cells[1] not in {"P0", "P1", "P2", "P3", "P—"}:
            errors.append("invalid priority: " + cells[1])
    if not ids or len(set(ids)) != len(ids):
        errors.append("missing or duplicate roadmap work identifiers")
    for path in sorted(roadmaps.glob("DeltaZulu.*ROADMAP.md")):
        historical = path.read_text(encoding="utf-8")
        if not re.search(r"^> \*\*Historical import", historical, re.MULTILINE):
            errors.append(f"{path.name}: imported roadmap lacks historical designation")
    return errors, warnings


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    paths = maintained_paths(root)
    failures = links_for(root, paths)
    roadmap_errors, warnings = roadmap_check(root, date.today())
    failures.extend(roadmap_errors)
    for warning in warnings:
        print(f"::warning::{warning}")
    for failure in failures:
        print(f"::error::{failure}")
    if failures:
        return 1
    print(f"Checked relative links in {len(paths)} maintained documents (historical files excluded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
