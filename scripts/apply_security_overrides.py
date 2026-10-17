#!/usr/bin/env python3
"""Replace upstream pins for packages that have a security override."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def package_name(requirement: str) -> str:
    return re.split(r"[<>=!~;\[]", requirement, maxsplit=1)[0].strip().lower()


requirements_path = Path(sys.argv[1])
overrides_path = Path(sys.argv[2])
overrides = [
    line.strip()
    for line in overrides_path.read_text().splitlines()
    if line.strip() and not line.lstrip().startswith("#")
]
overridden_names = {package_name(line) for line in overrides}
requirements = [
    line
    for line in requirements_path.read_text().splitlines()
    if package_name(line) not in overridden_names
]
requirements_path.write_text("\n".join(requirements + overrides) + "\n")
