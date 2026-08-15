#!/usr/bin/env python3
"""Verify that Accepted Decisions still govern code that exists.

Two modes:

  --collect            Parse decisions/, write the set of repositories named by
                       Accepted Decisions to .governed-repos.txt.

  --verify --root DIR  For each Accepted Decision, confirm every path under
                       governs.paths and every type under governs.types still
                       exists in the corresponding checkout under DIR.

Exit code 1 if any governed path or type is missing, or if a repository a
Decision governs could not be checked out. Unverifiable is treated as failing:
silently passing a check that did not run is the failure mode this whole
workflow exists to prevent.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys

import yaml

DECISIONS = pathlib.Path("decisions")
FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)

# A type is "present" if it is declared. Matching the declaration rather than
# any mention avoids passing on a comment that merely names a deleted type.
DECL_KEYWORDS = ("class", "struct", "record", "interface", "enum", "delegate")


def load_decisions() -> list[tuple[pathlib.Path, dict]]:
    out = []
    if not DECISIONS.is_dir():
        return out
    for path in sorted(DECISIONS.glob("DEC-*.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER.match(text)
        if not match:
            print(f"::error file={path}::missing YAML front-matter")
            out.append((path, {}))
            continue
        try:
            meta = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            print(f"::error file={path}::unparseable front-matter: {exc}")
            meta = {}
        out.append((path, meta))
    return out


def accepted(decisions):
    return [(p, m) for p, m in decisions if m.get("status") == "Accepted"]


def collect() -> int:
    repos: set[str] = set()
    for path, meta in accepted(load_decisions()):
        named = meta.get("repos") or []
        if not named:
            print(f"::warning file={path}::Accepted Decision names no repos")
        repos.update(named)
    pathlib.Path(".governed-repos.txt").write_text(
        "".join(f"{r}\n" for r in sorted(repos)), encoding="utf-8"
    )
    print(f"{len(repos)} repository(ies) governed by Accepted Decisions")
    for r in sorted(repos):
        print(f"  {r}")
    return 0


def type_is_declared(repo_root: pathlib.Path, fq_name: str) -> bool:
    """True if the type's simple name is declared somewhere in the checkout."""
    simple = fq_name.rsplit(".", 1)[-1]
    pattern = re.compile(
        r"\b(?:" + "|".join(DECL_KEYWORDS) + r")\s+" + re.escape(simple) + r"\b"
    )
    for source in repo_root.rglob("*.cs"):
        try:
            if pattern.search(source.read_text(encoding="utf-8", errors="ignore")):
                return True
        except OSError:
            continue
    return False


def verify(root: pathlib.Path) -> int:
    failures = 0
    checked = 0
    for path, meta in accepted(load_decisions()):
        governs = meta.get("governs") or {}
        repos = meta.get("repos") or []
        paths = governs.get("paths") or []
        types = governs.get("types") or []
        if not paths and not types:
            continue

        for repo in repos:
            repo_root = root / repo
            if not repo_root.is_dir():
                print(
                    f"::error file={path}::{meta.get('id')} governs {repo}, "
                    "which could not be checked out — cannot verify"
                )
                failures += 1
                continue

            for governed in paths:
                checked += 1
                if not (repo_root / governed).exists():
                    print(
                        f"::error file={path}::{meta.get('id')} governs "
                        f"{repo}/{governed}, which no longer exists"
                    )
                    failures += 1

            for fq_name in types:
                checked += 1
                if not type_is_declared(repo_root, fq_name):
                    print(
                        f"::error file={path}::{meta.get('id')} governs type "
                        f"{fq_name}, which is not declared in {repo}"
                    )
                    failures += 1

    print(f"{checked} governed entry(ies) checked, {failures} failure(s)")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collect", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(".governed"))
    args = parser.parse_args()

    if args.collect:
        return collect()
    if args.verify:
        return verify(args.root)
    parser.error("one of --collect or --verify is required")


if __name__ == "__main__":
    sys.exit(main())
