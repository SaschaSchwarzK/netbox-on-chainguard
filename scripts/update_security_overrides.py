#!/usr/bin/env python3
"""Raise Python security floors for every fixable scanner finding."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


def name(requirement: str) -> str:
    return (
        re.split(r"[<>=!~;\[]", requirement, maxsplit=1)[0]
        .strip()
        .lower()
        .replace("_", "-")
    )


*scan_names, requirements_name = sys.argv[1:]
scan_paths = map(Path, scan_names)
requirements_path = Path(requirements_name)
lines = [
    line.strip() for line in requirements_path.read_text().splitlines() if line.strip()
]
positions = {
    name(line): index for index, line in enumerate(lines) if not line.startswith("#")
}
candidates: dict[str, tuple[str, str]] = {}


def version_key(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version)[:4])


def add_candidate(package: str, fixed: str) -> None:
    package = package.replace("_", "-")
    key = package.lower()
    previous = candidates.get(key)
    if previous is None or version_key(fixed) > version_key(previous[1]):
        candidates[key] = (package, fixed)


for scan_path in scan_paths:
    data = json.loads(scan_path.read_text())
    for match in data.get("matches", []):  # Grype
        vulnerability = match.get("vulnerability", {})
        artifact = match.get("artifact", {})
        if artifact.get("type", "").lower() not in {"python", "pypi"}:
            continue
        fixes = vulnerability.get("fix", {}).get("versions", [])
        if fixes:
            add_candidate(artifact.get("name", ""), fixes[0])

    for result in data.get("Results", []):  # Trivy
        result_type = result.get("Type", "").lower()
        if result_type not in {"python", "python-pkg", "pypi"}:
            continue
        for vulnerability in result.get("Vulnerabilities") or []:
            fixed = vulnerability.get("FixedVersion")
            if fixed:
                add_candidate(
                    vulnerability.get("PkgName", ""), fixed.split(",")[0].strip()
                )

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
