import json
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


if __name__ == "__main__":
    unittest.main()
