#!/usr/bin/env python3
"""Set catalog revisions from clean autopatch build markers."""

import json
import re
import sys
from pathlib import Path

catalog_path = Path(sys.argv[1])
markers = Path(sys.argv[2])
catalog = json.loads(catalog_path.read_text())
clean_revisions = {}
for path in markers.glob("*.clean"):
    match = re.fullmatch(r"(.+)-r(\d+)", path.stem)
    if not match:
        continue
    version, revision = match.groups()
    clean_revisions[version] = int(revision)
for entry in catalog["versions"]:
    if entry["version"] in clean_revisions:
        entry["revision"] = clean_revisions[entry["version"]]
catalog_path.write_text(json.dumps(catalog, indent=2) + "\n")
print(" ".join(sorted(clean_revisions)))
