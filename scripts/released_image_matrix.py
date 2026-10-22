#!/usr/bin/env python3
"""Build the autopatch matrix from revisions that have a release tag."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def released_revisions(tags: list[str]) -> dict[str, int]:
    revisions: dict[str, int] = {}
    for tag in tags:
        match = re.fullmatch(r"v(.+)-r(\d+)", tag)
        if match:
            version, revision = match.groups()
            revisions[version] = max(revisions.get(version, -1), int(revision))
    return revisions


def matrix(catalog: dict[str, Any], tags: list[str]) -> dict[str, object]:
    released = released_revisions(tags)
    include = []
    for entry in catalog["versions"]:
        version = entry["version"]
        current_revision = released.get(version, -1)
        include.append(
            {
                "version": version,
                "current_revision": current_revision,
                "next_revision": current_revision + 1,
            }
        )
    return {"include": include}


def main() -> None:
    catalog = json.loads(Path(sys.argv[1]).read_text())
    tags = subprocess.run(
        ["git", "tag", "--list"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    print(json.dumps(matrix(catalog, tags), separators=(",", ":")))


if __name__ == "__main__":
    main()
