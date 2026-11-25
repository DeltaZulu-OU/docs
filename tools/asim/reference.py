"""Pinned ASIM reference acquisition primitives; not a runtime schema authority."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "sources.json"
CACHE = ROOT / ".cache"
OUTPUT = ROOT / "generated"
VERSION = "0.1.0"
FAMILIES = (
    "Dns", "NetworkSession", "ProcessEvent", "Authentication",
    "FileEvent", "UserManagement", "RegistryEvent", "AuditEvent",
)
SOURCES = {
    "sentinel": ("Azure/Azure-Sentinel", "MIT"),
    "monitor": ("MicrosoftDocs/azure-monitor-docs", "CC-BY-4.0"),
}
KINDS = {"license", "tester", "schema", "parser", "native-table", "upstream-test"}
HEX = re.compile(r"[0-9a-f]{40}")
MAX_BYTES = 8 * 1024 * 1024


def git_blob(data: bytes) -> str:
    # Git object identity, not an independent signature or trust assertion.
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def read_manifest(path: Path = MANIFEST) -> dict:
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate manifest key: {key}")
            result[key] = value
        return result

    m = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs)
    if m["schema_version"] != 1 or m["tool_version"] != VERSION:
        raise ValueError("unsupported manifest/tool version")
    if set(m["families"]) != set(FAMILIES) or len(set(m["families"].values())) != len(FAMILIES):
        raise ValueError("manifest must contain exactly the eight approved telemetry families")
    if set(m["sources"]) != set(SOURCES):
        raise ValueError("unexpected reference sources")
    for key, s in m["sources"].items():
        if (s["repository"], s["license"]) != SOURCES[key] or not HEX.fullmatch(s["commit"]):
            raise ValueError(f"unapproved or unpinned source: {key}")
    seen = set()
    native = []
    tester = 0
    licences = set()
    for f in m["files"]:
        path = PurePosixPath(f["path"])
        key = (f["source"], f["path"])
        if (key in seen or f["source"] not in SOURCES or f["kind"] not in KINDS
                or not HEX.fullmatch(f["blob"]) or path.is_absolute()
                or ".." in path.parts or "\\" in f["path"]
                or path.as_posix() != f["path"] or not path.parts):
            raise ValueError(f"invalid or duplicate manifest entry: {key}")
        seen.add(key)
        if f["kind"] in {"parser", "native-table", "upstream-test"}:
            if f.get("family") not in FAMILIES:
                raise ValueError(f"unapproved family in {key}")
        elif "family" in f:
            raise ValueError(f"unexpected family in {key}")
        if f["kind"] == "native-table":
            native.append(f["family"])
        elif f["kind"] == "tester":
            tester += 1
        elif f["kind"] == "license":
            licences.add(f["source"])
    if sorted(native) != sorted(FAMILIES) or tester != 1 or licences != set(SOURCES):
        raise ValueError("missing or duplicate native tables, tester or licences")
    return m


def cache_path(cache: Path, manifest: dict, entry: dict) -> Path:
    return cache / entry["source"] / manifest["sources"][entry["source"]]["commit"] / entry["path"]


def verify_bytes(entry: dict, data: bytes) -> None:
    if len(data) > MAX_BYTES or git_blob(data) != entry["blob"]:
        raise ValueError(f"size or Git blob mismatch: {entry['source']}/{entry['path']}")


def read_verified(cache: Path, manifest: dict, entry: dict) -> bytes:
    path = cache_path(cache, manifest, entry)
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    verify_bytes(entry, data)
    return data


def atomic_write(path: Path, data: bytes) -> None:
    import os
    import tempfile

    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as stream:
        tmp = Path(stream.name)
        try:
            stream.write(data)
            stream.close()
            os.replace(tmp, path)
        finally:
            tmp.unlink(missing_ok=True)
