from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_security_overrides import validate


class ValidateSecurityOverridesTest(unittest.TestCase):
    def validate_text(self, baseline: str, candidate: str) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            before = root / "before.txt"
            after = root / "after.txt"
            before.write_text(baseline)
            after.write_text(candidate)
            validate(before, after)

    def test_accepts_additions_and_higher_floors(self) -> None:
        self.validate_text(
            "Pillow>=13.0.0\nDjango>=5.2.17,<5.3\n",
            "Pillow>=13.1.0\nDjango>=5.2.18,<5.3\nnew-package>=1.0\n",
        )

    def test_rejects_removed_override(self) -> None:
        with self.assertRaisesRegex(ValueError, "removed"):
            self.validate_text("Pillow>=13.0.0\n", "Django>=5.2\n")

    def test_rejects_downgraded_floor(self) -> None:
        with self.assertRaisesRegex(ValueError, "downgraded"):
            self.validate_text("Pillow>=13.0.0\n", "Pillow>=12.3.0\n")

    def test_rejects_changed_upper_bound(self) -> None:
        with self.assertRaisesRegex(ValueError, "upper bound"):
            self.validate_text("Django>=5.2,<5.3\n", "Django>=5.3,<6\n")

    def test_rejects_malformed_or_duplicate_requirements(self) -> None:
        with self.assertRaisesRegex(ValueError, "malformed"):
            self.validate_text("Pillow>=13.0.0\n", "mework>=3.17.2 garbage\n")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.validate_text("Pillow>=13.0.0\n", "Pillow>=13\npillow>=14\n")


if __name__ == "__main__":
    unittest.main()
