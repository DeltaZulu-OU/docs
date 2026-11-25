#!/usr/bin/env python3
"""Check relative Markdown links in current, maintained estate documentation.

Historical imports, archived ADRs and immutable dated verification reports are
excluded: their links are evidence of the original documents, not a live API.
This checks parsed Markdown links/images, including resolved reference links,
and Markdown heading/explicit anchor fragments. External URLs, non-Markdown
fragments and historical source documents are not verified.
"""
from __future__ import annotations

from pathlib import Path
from datetime import date
import re
import sys
from urllib.parse import unquote, urlsplit
from collections import Counter

from markdown_it import MarkdownIt

PARSER = MarkdownIt("commonmark").enable("table")
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


def walk_tokens(tokens):
    for token in tokens:
        yield token
        if token.children:
            yield from walk_tokens(token.children)


def slug(text: str) -> str:
    # GitHub-style heading slug for ordinary Unicode letters, digits,
    # underscores, hyphens and whitespace. Explicit HTML anchors also work.
    return re.sub(r"[^\w\s-]", "", text.lower()).replace(" ", "-")


def anchors(source: str) -> set[str]:
    tokens = PARSER.parse(source)
    result = set()
    used = Counter()
    for i, token in enumerate(tokens):
        if token.type == "heading_open" and i + 1 < len(tokens):
            inline = tokens[i + 1]
            heading = "".join(t.content for t in walk_tokens(inline.children or [])
                              if t.type in {"text", "code_inline"})
            base = slug(heading)
            name = base
            while name in result:
                used[base] += 1
                name = f"{base}-{used[base]}"
            result.add(name)
    for token in walk_tokens(tokens):
        if token.type in {"html_inline", "html_block"}:
            result.update(re.findall(r'''(?:id|name)\s*=\s*["']([^"']+)["']''',
                                     token.content, re.IGNORECASE))
    return result


def links_for(root: Path, paths: list[str]) -> list[str]:
    root = root.resolve()
    errors: list[str] = []
    anchor_cache = {}
    for rel in paths:
        source = root / rel
        if not source.is_file():
            errors.append(f"{rel}: maintained source document missing")
            continue
        tokens = PARSER.parse(source.read_text(encoding="utf-8"))
        for token in walk_tokens(tokens):
            if token.type not in {"link_open", "image"}:
                continue
            href = token.attrGet("href" if token.type == "link_open" else "src")
            if not href:
                continue
            parts = urlsplit(href)
            if parts.scheme or parts.netloc:
                continue
            target = unquote(parts.path)
            resolved = (source.parent / target).resolve() if target else source.resolve()
            if not resolved.is_relative_to(root) or not resolved.exists():
                errors.append(f"{rel}: broken local link {href!r}")
                continue
            if parts.fragment and resolved.is_file() and resolved.suffix.lower() == ".md":
                if resolved not in anchor_cache:
                    anchor_cache[resolved] = anchors(resolved.read_text(encoding="utf-8"))
                if unquote(parts.fragment) not in anchor_cache[resolved]:
                    errors.append(f"{rel}: unknown Markdown anchor {href!r}")
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
    print(f"Checked parsed relative links and Markdown anchors in {len(paths)} maintained documents (historical files excluded)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
