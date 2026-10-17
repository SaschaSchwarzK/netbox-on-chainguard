#!/usr/bin/env python3
"""Check scanner JSON and create a vulnerability delta report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def findings(paths: list[Path]) -> dict[tuple[str, str, str], dict[str, str]]:
    found: dict[tuple[str, str, str], dict[str, str]] = {}
    for path in paths:
        data = json.loads(path.read_text())
        if "matches" in data:  # Grype
            rows = (
                {
                    "id": row["vulnerability"]["id"],
                    "severity": row["vulnerability"].get("severity", "Unknown"),
                    "package": row["artifact"].get("name", "unknown"),
                    "installed": row["artifact"].get("version", "unknown"),
                    "fixed": ", ".join(row["vulnerability"].get("fix", {}).get("versions", [])) or "unfixed",
                }
                for row in data.get("matches", [])
            )
        else:  # Trivy
            rows = (
                {
                    "id": row["VulnerabilityID"],
                    "severity": row.get("Severity", "Unknown"),
                    "package": row.get("PkgName", "unknown"),
                    "installed": row.get("InstalledVersion", "unknown"),
                    "fixed": row.get("FixedVersion") or "unfixed",
                }
                for result in data.get("Results", [])
                for row in result.get("Vulnerabilities") or []
            )
        for row in rows:
            found[(row["id"], row["package"], row["installed"])] = row
    return found


def table(title: str, rows: list[dict[str, str]]) -> list[str]:
    lines = [f"## {title}", ""]
    if not rows:
        return lines + ["None.", ""]
    lines += ["| Severity | Package | Installed | Fixed | Vulnerability |", "|---|---|---|---|---|"]
    for row in sorted(rows, key=lambda item: (item["severity"], item["id"], item["package"])):
        lines.append(
            f"| {row['severity']} | `{row['package']}` | `{row['installed']}` | "
            f"`{row['fixed']}` | {row['id']} |"
        )
    return lines + [""]


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="command", required=True)
check = subparsers.add_parser("check")
check.add_argument("files", nargs="+", type=Path)
report = subparsers.add_parser("report")
report.add_argument("--before", nargs="+", required=True, type=Path)
report.add_argument("--after", nargs="+", required=True, type=Path)
report.add_argument("--image", required=True)
report.add_argument("--output", required=True, type=Path)
args = parser.parse_args()

if args.command == "check":
    severe = [row for row in findings(args.files).values() if row["severity"].lower() in {"critical", "high"}]
    if severe:
        for row in severe:
            print(f"{row['severity']}: {row['id']} in {row['package']} {row['installed']} (fixed: {row['fixed']})")
        raise SystemExit(1)
    print("No critical or high vulnerabilities found.")
else:
    before = findings(args.before)
    after = findings(args.after)
    resolved = [row for key, row in before.items() if key not in after]
    remaining = list(after.values())
    severe = [row for row in remaining if row["severity"].lower() in {"critical", "high"}]
    lines = [f"Security report for `{args.image}`", ""]
    lines += table("Resolved vulnerabilities", resolved)
    lines += table("Remaining vulnerabilities", remaining)
    lines += ["## Release decision", ""]
    lines.append("✅ Eligible for release: no critical or high vulnerabilities remain." if not severe else "❌ Blocked: critical or high vulnerabilities remain.")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n")
    raise SystemExit(1 if severe else 0)
