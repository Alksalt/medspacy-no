from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_release_ready_check_fails_on_fixture_resources() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_release_ready.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert "fixture" in result.stderr
    assert "owner_reviewed=false" in result.stderr
    assert "rush_rules.tsv" in result.stderr
    assert "abbreviations.txt" in result.stderr
    assert "Private :: Do Not Upload" in result.stderr
    assert "paper.md" in result.stderr
