#!/usr/bin/env python3
"""Check scanner JSON and create a vulnerability delta report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class InvalidScanReport(ValueError):
    """Raised when a scanner did not produce a usable JSON report."""


def load_report(path: Path) -> dict[str, Any]:
    try:
        contents = path.read_text()
    except OSError as error:
        raise InvalidScanReport(f"cannot read scan report {path}: {error}") from error

    if not contents.strip():
        raise InvalidScanReport(
            f"scan report {path} is empty; the scanner likely failed"
        )

    try:
        data = json.loads(contents)
    except json.JSONDecodeError as error:
        location = f"line {error.lineno} column {error.colno}"
        raise InvalidScanReport(
            f"scan report {path} is not valid JSON: {error.msg} at {location}"
        ) from error

    if not isinstance(data, dict):
        raise InvalidScanReport(f"scan report {path} must contain a JSON object")
    if "matches" not in data and "Results" not in data:
        raise InvalidScanReport(f"scan report {path} is neither Grype nor Trivy JSON")
    return data


def findings(paths: list[Path]) -> dict[tuple[str, str, str], dict[str, str]]:
    found: dict[tuple[str, str, str], dict[str, str]] = {}
    for path in paths:
        data = load_report(path)
        if "matches" in data:  # Grype
            rows = (
                {
                    "id": row["vulnerability"]["id"],
                    "severity": row["vulnerability"].get("severity", "Unknown"),
                    "package": row["artifact"].get("name", "unknown"),
                    "installed": row["artifact"].get("version", "unknown"),
                    "fixed": ", ".join(
                        row["vulnerability"].get("fix", {}).get("versions", [])
                    )
                    or "unfixed",
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
    lines += [
        "| Severity | Package | Installed | Fixed | Vulnerability |",
        "|---|---|---|---|---|",
    ]
    for row in sorted(
        rows, key=lambda item: (item["severity"], item["id"], item["package"])
    ):
        lines.append(
            f"| {row['severity']} | `{row['package']}` | `{row['installed']}` | "
            f"`{row['fixed']}` | {row['id']} |"
        )
    return lines + [""]


def print_severe(rows: list[dict[str, str]]) -> None:
    for row in rows:
        print(
            f"{row['severity']}: {row['id']} in {row['package']} "
            f"{row['installed']} (fixed: {row['fixed']})"
        )


def main() -> int:
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

    try:
        if args.command == "check":
            severe = [
                row
                for row in findings(args.files).values()
                if row["severity"].lower() in {"critical", "high"}
            ]
            if severe:
                print_severe(severe)
                return 1
            print("No critical or high vulnerabilities found.")
            return 0

        before = findings(args.before)
        after = findings(args.after)
    except InvalidScanReport as error:
        parser.error(str(error))

    resolved = [row for key, row in before.items() if key not in after]
    remaining = list(after.values())
    severe = [
        row for row in remaining if row["severity"].lower() in {"critical", "high"}
    ]
    lines = [f"Security report for `{args.image}`", ""]
    lines += table("Resolved vulnerabilities", resolved)
    lines += table("Remaining vulnerabilities", remaining)
    lines += ["## Release decision", ""]
    lines.append(
        "✅ Eligible for release: no critical or high vulnerabilities remain."
        if not severe
        else "❌ Blocked: critical or high vulnerabilities remain."
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines) + "\n")
    if severe:
        print_severe(severe)
        print(f"Release blocked; full vulnerability report: {args.output}")
    return 1 if severe else 0


if __name__ == "__main__":
    raise SystemExit(main())
