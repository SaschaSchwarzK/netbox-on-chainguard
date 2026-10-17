from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "update_security_overrides.py"


class UpdateSecurityOverridesTest(unittest.TestCase):
    def test_updates_all_severities_from_both_scanners(self) -> None:
        grype = {
            "matches": [
                {
                    "artifact": {
                        "name": "low_package",
                        "type": "python",
                        "version": "1.0",
                    },
                    "vulnerability": {
                        "id": "CVE-LOW",
                        "severity": "Low",
                        "fix": {"versions": ["1.1"]},
                    },
                },
                {
                    "artifact": {
                        "name": "ignored-os-package",
                        "type": "apk",
                        "version": "1.0",
                    },
                    "vulnerability": {
                        "id": "CVE-OS",
                        "severity": "Critical",
                        "fix": {"versions": ["2.0"]},
                    },
                },
            ]
        }
        trivy = {
            "Results": [
                {
                    "Class": "lang-pkgs",
                    "Type": "python-pkg",
                    "Vulnerabilities": [
                        {
                            "VulnerabilityID": "CVE-MEDIUM",
                            "PkgName": "medium-package",
                            "Severity": "MEDIUM",
                            "FixedVersion": "2.3",
                        }
                    ],
                },
                {
                    "Class": "lang-pkgs",
                    "Type": "npm",
                    "Vulnerabilities": [
                        {
                            "VulnerabilityID": "CVE-NPM",
                            "PkgName": "ignored-npm-package",
                            "Severity": "HIGH",
                            "FixedVersion": "9.0",
                        }
                    ],
                },
            ]
        }

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            grype_path = root / "grype.json"
            trivy_path = root / "trivy.json"
            requirements_path = root / "requirements.txt"
            grype_path.write_text(json.dumps(grype))
            trivy_path.write_text(json.dumps(trivy))
            requirements_path.write_text("low-package>=1.0,<2\n")

            subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    str(grype_path),
                    str(trivy_path),
                    str(requirements_path),
                ],
                check=True,
            )

            self.assertEqual(
                requirements_path.read_text(),
                "low-package>=1.1,<2\nmedium-package>=2.3\n",
            )


if __name__ == "__main__":
    unittest.main()
