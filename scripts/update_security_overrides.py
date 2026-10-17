#!/usr/bin/env python3
"""Raise Python security floors from fixed versions reported by Grype."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def name(requirement: str) -> str:
    return re.split(r"[<>=!~;\[]", requirement, maxsplit=1)[0].strip().lower().replace("_", "-")


scan_path, requirements_path = map(Path, sys.argv[1:3])
lines = [line.strip() for line in requirements_path.read_text().splitlines() if line.strip()]
positions = {name(line): index for index, line in enumerate(lines) if not line.startswith("#")}
data = json.loads(scan_path.read_text())
candidates: dict[str, tuple[str, str]] = {}


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version)[:4])

for match in data.get("matches", []):
    vulnerability = match.get("vulnerability", {})
    artifact = match.get("artifact", {})
    if vulnerability.get("severity", "").lower() not in {"critical", "high"}:
        continue
    if artifact.get("type", "").lower() not in {"python", "pypi"}:
        continue
    fixes = vulnerability.get("fix", {}).get("versions", [])
    if not fixes:
        continue
    package = artifact.get("name", "").replace("_", "-")
    fixed = fixes[0]
    key = package.lower()
    previous = candidates.get(key)
    if previous is None or version_key(fixed) > version_key(previous[1]):
        candidates[key] = (package, fixed)

for key, (package, fixed) in candidates.items():
    upper = ""
    extras = ""
    if key in positions:
        old = lines[positions[key]]
        package = re.split(r"[<>=!~;\[]", old, maxsplit=1)[0].strip()
        match_upper = re.search(r"(,<[^,;]+)", old)
        upper = match_upper.group(1) if match_upper else ""
        match_extras = re.search(r"(\[[^]]+\])", old)
        extras = match_extras.group(1) if match_extras else ""
        current_floor = re.search(r">=([^,;]+)", old)
        if current_floor and version_key(current_floor.group(1)) > version_key(fixed):
            fixed = current_floor.group(1)
        lines[positions[key]] = f"{package}{extras}>={fixed}{upper}"
    else:
        positions[key] = len(lines)
        lines.append(f"{package}>={fixed}")

# social-auth-app-django 5.x caps social-auth-core below 5.0. Keep the pair
# compatible when a core security advisory requires the newer major line.
if "social-auth-core" in candidates:
    key = "social-auth-app-django"
    requirement = "social-auth-app-django>=6.0.0"
    if key in positions:
        lines[positions[key]] = requirement
    else:
        lines.append(requirement)

requirements_path.write_text("\n".join(lines) + "\n")
