#!/usr/bin/env python3
"""Increment catalog revisions for clean autopatch build markers."""

import json
import sys
from pathlib import Path

catalog_path = Path(sys.argv[1])
markers = Path(sys.argv[2])
catalog = json.loads(catalog_path.read_text())
clean_versions = {path.stem for path in markers.glob("*.clean")}
for entry in catalog["versions"]:
    if entry["version"] in clean_versions:
        entry["revision"] += 1
catalog_path.write_text(json.dumps(catalog, indent=2) + "\n")
print(" ".join(sorted(clean_versions)))
