import json
import subprocess
import sys
from pathlib import Path

from scripts.released_image_matrix import matrix, released_revisions

ROOT = Path(__file__).parents[1]


def test_released_revisions_uses_highest_tag() -> None:
    assert released_revisions(
        ["v4.7.3-r1", "v4.7.3-r2", "v4.7.3-r6-broken", "unrelated"]
    ) == {"4.7.3": 2}


def test_matrix_ignores_catalog_revision_and_uses_release_tags() -> None:
    catalog = {"versions": [{"version": "4.7.3", "revision": 6}]}

    assert matrix(catalog, ["v4.7.3-r2"]) == {
        "include": [
            {"version": "4.7.3", "current_revision": 2, "next_revision": 3}
        ]
    }


def test_first_release_starts_at_revision_zero() -> None:
    catalog = {"versions": [{"version": "4.8.0", "revision": 0}]}

    assert matrix(catalog, []) == {
        "include": [
            {"version": "4.8.0", "current_revision": -1, "next_revision": 0}
        ]
    }


def test_promote_sets_marker_revision_instead_of_incrementing(tmp_path: Path) -> None:
    catalog = tmp_path / "versions.json"
    markers = tmp_path / "markers"
    markers.mkdir()
    catalog.write_text(
        json.dumps({"versions": [{"version": "4.7.3", "revision": 6}]})
    )
    (markers / "4.7.3-r3.clean").touch()

    subprocess.run(
        [
            sys.executable,
            ROOT / "scripts" / "promote_clean_builds.py",
            catalog,
            markers,
        ],
        check=True,
    )

    assert json.loads(catalog.read_text())["versions"][0]["revision"] == 3
