"""The API version must count up whenever the API description changes.

If these fail: bump API_VERSION in src/spakr/api/versions.py, then run
`python -m spakr.api.snapshot` and commit tests/api_contract.snapshot.
"""

import json
import subprocess
from pathlib import Path

import pytest

from spakr.api import API_VERSION
from spakr.api.snapshot import SNAPSHOT, current_contract, render


def test_snapshot_matches_generated_description():
    assert SNAPSHOT.is_file(), "run: python -m spakr.api.snapshot"
    assert SNAPSHOT.read_text() == render(current_contract()), (
        "The API description changed. Bump API_VERSION (src/spakr/api/versions.py), "
        "run `python -m spakr.api.snapshot` and commit the snapshot."
    )


def test_changed_snapshot_has_higher_version_than_main():
    root = Path(__file__).resolve().parents[1]
    try:
        old = subprocess.run(
            ["git", "show", "origin/main:tests/api_contract.snapshot"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        pytest.skip("origin/main snapshot not available")
    old_contract = json.loads(old)
    if old_contract["openapi"] != current_contract()["openapi"]:
        assert API_VERSION > old_contract["api_version"], (
            "The API description differs from main but API_VERSION was not increased."
        )
