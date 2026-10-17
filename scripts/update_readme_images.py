#!/usr/bin/env python3
"""Replace the generated released-image vulnerability table in README.md."""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

START = "<!-- released-images:start -->"
END = "<!-- released-images:end -->"


def vulnerability_link(identifier: str) -> str:
    if identifier.startswith("CVE-"):
        url = f"https://nvd.nist.gov/vuln/detail/{identifier}"
    elif identifier.startswith("GHSA-"):
        url = f"https://github.com/advisories/{identifier}"
    else:
        return identifier
    return f"[{identifier}]({url})"


def remaining_findings(report: Path) -> list[tuple[str, str]]:
    text = report.read_text()
    section = text.split("## Remaining vulnerabilities", 1)[-1].split("## Release decision", 1)[0]
    rows: list[tuple[str, str]] = []
    for line in section.splitlines():
        match = re.match(r"\| (Critical|High|Medium|Low|Negligible|Unknown) \|.*\| ([A-Z]+-[A-Za-z0-9-]+) \|$", line)
        if match:
            rows.append((match.group(1), match.group(2)))
    return rows


readme_path = Path(sys.argv[1])
catalog_path = Path(sys.argv[2])
reports_path = Path(sys.argv[3])
repository = sys.argv[4].lower()
preserve_missing = "--preserve-missing" in sys.argv[5:]
catalog = json.loads(catalog_path.read_text())
existing_readme = readme_path.read_text()
existing_rows: dict[str, str] = {}
if preserve_missing:
    for line in existing_readme.splitlines():
        match = re.search(r"`ghcr\.io/[^`]+:([^`]+)`", line)
        if match:
            existing_rows[match.group(1)] = line

lines = [
    START,
    "| NetBox | Image | Critical | High | Medium | Low | Current vulnerabilities |",
    "|---|---|---:|---:|---:|---:|---|",
]
for entry in reversed(catalog["versions"]):
    tag = f"{entry['version']}-r{entry['revision']}"
    report = reports_path / f"{tag}.md"
    if report.exists():
        findings = remaining_findings(report)
        counts = Counter(severity for severity, _ in findings)
        identifiers = sorted({identifier for _, identifier in findings})
        vulnerabilities = ", ".join(map(vulnerability_link, identifiers)) if identifiers else "✅ None"
        values = [str(counts.get(level, 0)) for level in ("Critical", "High", "Medium", "Low")]
    elif tag in existing_rows:
        lines.append(existing_rows[tag])
        continue
    else:
        values = ["—"] * 4
        vulnerabilities = "Scan report unavailable"
    image = f"`ghcr.io/{repository}:{tag}`"
    lines.append(f"| {entry['version']} | {image} | {' | '.join(values)} | {vulnerabilities} |")
lines.append(END)

replacement = "\n".join(lines)
if START not in existing_readme or END not in existing_readme:
    raise SystemExit("README release-image markers are missing")
readme = re.sub(
    re.escape(START) + r".*?" + re.escape(END),
    replacement,
    existing_readme,
    flags=re.DOTALL,
)
readme_path.write_text(readme)
