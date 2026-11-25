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
        raise ValueError("decisions/ missing; refusing empty governance check")
    for path in sorted(DECISIONS.glob("DEC-*.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONT_MATTER.match(text)
        if not match:
            raise ValueError(f"{path}: missing YAML front matter")
        try:
            meta = yaml.safe_load(match.group(1))
        except yaml.YAMLError as exc:
            raise ValueError(f"{path}: malformed YAML: {exc}") from exc
        if not isinstance(meta, dict):
            raise ValueError(f"{path}: front matter must be a mapping")
        if meta.get("id") != path.name[:8] or not re.fullmatch(r"DEC-\d{4}", str(meta.get("id"))):
            raise ValueError(f"{path}: id does not match filename")
        if meta.get("status") not in {"Proposed", "Accepted", "Superseded", "Rejected"}:
            raise ValueError(f"{path}: invalid or missing status")
        repos = meta.get("repos")
        if not isinstance(repos, list) or any(not isinstance(r, str) or not re.fullmatch(r"DeltaZulu\.[A-Za-z][A-Za-z0-9]*", r) for r in repos):
            raise ValueError(f"{path}: repos must be a list of repository names")
        governs = meta.get("governs")
        if not isinstance(governs, dict):
            raise ValueError(f"{path}: governs must be a mapping")
        for field in ("types", "paths"):
            entry = governs.get(field)
            if isinstance(entry, dict):
                if any(name not in repos for name in entry):
                    raise ValueError(f"{path}: governs.{field} references an undeclared repo")
                values = list(entry.values())
            else:
                values = [entry]
            if any(not isinstance(v, list) or any(not isinstance(s, str) or not s for s in v) for v in values):
                raise ValueError(f"{path}: governs.{field} must contain string lists")
        if (governs.get("types") or governs.get("paths")) and not repos:
            raise ValueError(f"{path}: governs entries have no repository")
        cites = meta.get("cites")
        if not isinstance(cites, list):
            raise ValueError(f"{path}: cites must be a list")
        for cid in cites:
            if not isinstance(cid, str) or not re.fullmatch(r"CON-\d{4}", cid):
                raise ValueError(f"{path}: invalid Constraint citation {cid!r}")
            if not list(pathlib.Path("constraints").glob(cid + "-*.md")):
                raise ValueError(f"{path}: missing Constraint {cid}")
        if meta.get("status") == "Superseded" and not meta.get("superseded_by"):
            raise ValueError(f"{path}: Superseded Decision missing superseded_by")
        out.append((path, meta))
    if not out:
        raise ValueError("no Decision files found")
    by_id = {meta["id"]: meta for _, meta in out}
    if len(by_id) != len(out):
        raise ValueError("duplicate Decision identifiers")
    successors = {}
    for path, meta in out:
        identifier = meta["id"]
        status = meta["status"]
        for field, required in (("superseded_by", "Superseded"), ("rejected_by", "Rejected")):
            target = meta.get(field)
            if target is None:
                continue
            if (not isinstance(target, str) or target not in by_id
                    or target == identifier or status != required):
                raise ValueError(f"{path}: invalid {field} target {target!r}")
            if by_id[target]["status"] not in {"Accepted", "Superseded"}:
                raise ValueError(f"{path}: {field} target was not accepted")
            successors[identifier] = target
        prior = meta.get("supersedes", [])
        prior = [prior] if isinstance(prior, str) else prior
        if not isinstance(prior, list) or any(not isinstance(x, str) for x in prior):
            raise ValueError(f"{path}: invalid supersedes list")
        for old in prior:
            if re.fullmatch(r"D\d+", old):
                continue  # historical PIPELINE.md aliases
            if old not in by_id or old == identifier:
                raise ValueError(f"{path}: invalid supersedes target {old!r}")
            if (by_id[old]["status"] != "Superseded"
                    or by_id[old].get("superseded_by") != identifier
                    or status not in {"Accepted", "Superseded"}):
                raise ValueError(f"{path}: nonreciprocal supersession of {old}")
    for identifier, target in successors.items():
        if by_id[identifier]["status"] == "Superseded":
            prior = by_id[target].get("supersedes", [])
            prior = [prior] if isinstance(prior, str) else prior
            if identifier not in prior:
                raise ValueError(f"{identifier}: missing reciprocal supersedes on {target}")
        seen = {identifier}
        while target in successors:
            if target in seen:
                raise ValueError(f"{identifier}: cyclic Decision relationships")
            seen.add(target)
            target = successors[target]
    return out


def accepted(decisions):
    return [(p, m) for p, m in decisions if m.get("status") == "Accepted"]


def collect() -> int:
    repos: set[str] = set()
    for path, meta in accepted(load_decisions()):
        named = meta.get("repos") or []
        governs = meta.get("governs") or {}
        claims = bool(governs.get("types")) or bool(governs.get("paths"))
        # A principle-level Decision legitimately governs no code and names no
        # repos; that is not worth a warning. Claiming to govern symbols while
        # naming no repository to look in is an inconsistency, and is.
        if claims and not named:
            print(
                f"::warning file={path}::{meta.get('id')} claims governs entries "
                "but names no repos, so they can never be checked"
            )
        repos.update(named)
    pathlib.Path(".governed-repos.txt").write_text(
        "".join(f"{r}\n" for r in sorted(repos)), encoding="utf-8"
    )
    print(f"{len(repos)} repository(ies) governed by Accepted Decisions")
    for r in sorted(repos):
        print(f"  {r}")
    return 0


# Lexical approximation: not a C# compiler or proof of namespace/build membership.
NON_CODE = re.compile(
    r'//[^\n]*|/\*[\s\S]*?\*/|'
    r'\$*("{3,})[\s\S]*?\1|'
    r'(?:\$@|@\$|@)"(?:""|[^"])*"|'
    r'\$?"(?:\\.|[^"\\])*"|'
    r"'(?:\\.|[^'\\])*'"
)


def code_only(source: str) -> str:
    return NON_CODE.sub(lambda m: " " * len(m.group(0)), source)


def type_is_declared(repo_root: pathlib.Path, fq_name: str) -> bool:
    """True if the type's simple name is declared somewhere in the checkout."""
    simple = fq_name.rsplit(".", 1)[-1]
    pattern = re.compile(
        r"\b(?:" + "|".join(DECL_KEYWORDS) + r")\s+" + re.escape(simple) + r"\b"
    )
    source_root = repo_root / "src"
    if not source_root.is_dir():
        return False
    for source in source_root.rglob("*.cs"):
        try:
            content = code_only(source.read_text(encoding="utf-8"))
            if not pattern.search(content):
                continue
            if "." not in fq_name:
                return True
            namespace = fq_name.rsplit(".", 1)[0]
            if re.search(r"\bnamespace\s+" + re.escape(namespace) + r"\s*[;{]", content):
                return True
        except (OSError, UnicodeError):
            continue
    return False


def _for_repo(entry, repo: str) -> list[str]:
    """Resolve a governs list for one repository.

    Two shapes are accepted. A flat list applies to every repository the Decision
    names, which is right when one Decision governs one codebase. A mapping keyed
    by repository name applies per repository, which is what a Decision spanning
    two repositories needs — it governs different symbols in each, and demanding
    that every symbol exist in every repository would be nonsense.
    """
    if entry is None:
        return []
    if isinstance(entry, dict):
        return entry.get(repo) or []
    return list(entry)


def verify(root: pathlib.Path) -> int:
    failures = 0
    checked = 0
    for path, meta in accepted(load_decisions()):
        governs = meta.get("governs") or {}
        repos = meta.get("repos") or []
        for repo in repos:
            paths = _for_repo(governs.get("paths"), repo)
            types = _for_repo(governs.get("types"), repo)
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
                candidate = (repo_root / governed).resolve()
                if not candidate.is_relative_to(repo_root.resolve()) or not candidate.exists():
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

    try:
        if args.collect:
            return collect()
        if args.verify:
            return verify(args.root)
    except (ValueError, OSError) as exc:
        print(f"::error::{exc}")
        return 1
    parser.error("one of --collect or --verify is required")


if __name__ == "__main__":
    sys.exit(main())
