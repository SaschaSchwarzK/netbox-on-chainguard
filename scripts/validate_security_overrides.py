#!/usr/bin/env python3
"""Reject autopatch overrides that weaken or corrupt the checked-in baseline."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIREMENT = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[A-Za-z0-9_,.-]+\])?"
    r"(?P<constraints>(?:[<>=!~]=?[^,;\s]+)(?:,(?:[<>=!~]=?[^,;\s]+))*)?$"
)


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def version_key(version: str) -> tuple[int, ...]:
    parts = [int(part) for part in re.findall(r"\d+", version)[:4]]
    return tuple(parts + [0] * (4 - len(parts)))


def parse(path: Path) -> dict[str, tuple[str, str | None, str | None]]:
    requirements: dict[str, tuple[str, str | None, str | None]] = {}
    for number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = REQUIREMENT.fullmatch(line)
        if not match:
            raise ValueError(f"{path}:{number}: malformed requirement: {line!r}")
        key = normalized(match.group("name"))
        if key in requirements:
            raise ValueError(f"{path}:{number}: duplicate package: {key}")
        constraints = match.group("constraints") or ""
        floor_match = re.search(r"(?:^|,)>=([^,]+)", constraints)
        ceiling_match = re.search(r"(?:^|,)<([^,=]+)", constraints)
        requirements[key] = (
            line,
            floor_match.group(1) if floor_match else None,
            ceiling_match.group(1) if ceiling_match else None,
        )
    return requirements


def validate(baseline_path: Path, candidate_path: Path) -> None:
    baseline = parse(baseline_path)
    candidate = parse(candidate_path)
    for package, (old_line, old_floor, old_ceiling) in baseline.items():
        if package not in candidate:
            raise ValueError(f"candidate removed {old_line!r}")
        new_line, new_floor, new_ceiling = candidate[package]
        if old_floor and not new_floor:
            raise ValueError(f"candidate removed the floor from {old_line!r}")
        if old_floor and version_key(new_floor) < version_key(old_floor):
            raise ValueError(f"candidate downgraded {package}: {old_floor} -> {new_floor}")
        if old_ceiling and new_ceiling != old_ceiling:
            raise ValueError(
                f"candidate changed the upper bound for {package}: "
                f"{old_ceiling} -> {new_ceiling or 'none'}"
            )
        if not new_line:
            raise AssertionError("unreachable")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("usage: validate_security_overrides.py BASELINE CANDIDATE")
    try:
        validate(Path(sys.argv[1]), Path(sys.argv[2]))
    except ValueError as error:
        print(f"unsafe security override update: {error}", file=sys.stderr)
        raise SystemExit(1)
