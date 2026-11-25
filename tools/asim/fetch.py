#!/usr/bin/env python3
"""Explicit network operation: acquire immutable files and verify Git blobs."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys
from urllib.parse import quote
from urllib.request import Request, urlopen

from reference import CACHE, MANIFEST, MAX_BYTES, atomic_write, cache_path, read_manifest, read_verified, verify_bytes


def acquire(manifest: dict, cache: Path) -> None:
    for entry in manifest["files"]:
        target = cache_path(cache, manifest, entry)
        if target.exists():
            read_verified(cache, manifest, entry)
            continue
        source = manifest["sources"][entry["source"]]
        url = ("https://raw.githubusercontent.com/" + source["repository"] + "/"
               + source["commit"] + "/" + quote(entry["path"], safe="/"))
        with urlopen(Request(url, headers={"User-Agent": "DeltaZulu-ASIM-reference/0.1.0"}), timeout=30) as response:
            data = response.read(MAX_BYTES + 1)
        verify_bytes(entry, data)
        atomic_write(target, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--cache", type=Path, default=CACHE)
    args = parser.parse_args()
    try:
        manifest = read_manifest(args.manifest)
        acquire(manifest, args.cache)
        print(f"Verified {len(manifest['files'])} pinned reference files")
        return 0
    except (OSError, ValueError, KeyError) as exc:
        print(f"ASIM acquisition failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
