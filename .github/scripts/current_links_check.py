#!/usr/bin/env python3
"""Check relative Markdown links in current, maintained estate documentation.

Historical imports, archived ADRs and immutable dated verification reports are
excluded: their links are evidence of the original documents, not a live API.
This verifies local link targets, not external URLs, fragment anchors or claims.
"""
from __future__ import annotations

from pathlib import Path
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


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    paths = maintained_paths(root)
    failures = links_for(root, paths)
    for failure in failures:
        print(f"::error::{failure}")
    if failures:
        return 1
    print(f"Checked relative links in {len(paths)} maintained documents (historical files excluded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
