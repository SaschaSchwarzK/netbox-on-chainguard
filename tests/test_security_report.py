import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.security_report import InvalidScanReport, findings


class FindingsTest(unittest.TestCase):
    def test_rejects_empty_scanner_output_with_useful_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "grype.json"
            report.write_text("")

            with self.assertRaisesRegex(
                InvalidScanReport, r"grype\.json is empty; the scanner likely failed"
            ):
                findings([report])

    def test_rejects_unrecognized_json(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "scan.json"
            report.write_text(json.dumps({"unexpected": []}))

            with self.assertRaisesRegex(
                InvalidScanReport, "neither Grype nor Trivy JSON"
            ):
                findings([report])

    def test_accepts_empty_grype_and_trivy_reports(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            grype = root / "grype.json"
            trivy = root / "trivy.json"
            grype.write_text(json.dumps({"matches": []}))
            trivy.write_text(json.dumps({"Results": []}))

            self.assertEqual(findings([grype, trivy]), {})

    def test_report_prints_blocking_finding_before_failing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "before.json"
            after = root / "after.json"
            output = root / "report.md"
            before.write_text(json.dumps({"matches": []}))
            after.write_text(
                json.dumps(
                    {
                        "matches": [
                            {
                                "vulnerability": {
                                    "id": "CVE-2099-0001",
                                    "severity": "High",
                                    "fix": {"versions": ["2.0"]},
                                },
                                "artifact": {"name": "example", "version": "1.0"},
                            }
                        ]
                    }
                )
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "scripts/security_report.py",
                    "report",
                    "--before",
                    str(before),
                    "--after",
                    str(after),
                    "--image",
                    "example:test",
                    "--output",
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertIn(
                "High: CVE-2099-0001 in example 1.0 (fixed: 2.0)", result.stdout
            )
            self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
