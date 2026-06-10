from __future__ import annotations

import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_build_artifacts_include_bundled_nb_resources(tmp_path: Path) -> None:
    out_dir = tmp_path / "dist"

    subprocess.run(
        [sys.executable, "-m", "build", "--no-isolation", "--outdir", str(out_dir)],
        cwd=ROOT,
        check=True,
    )

    wheel = next(out_dir.glob("medspacy_no-*.whl"))
    sdist = next(out_dir.glob("medspacy_no-*.tar.gz"))

    expected = {
        "medspacy_no/resources/nb/context_rules.json",
        "medspacy_no/resources/nb/section_patterns.json",
        "medspacy_no/resources/nb/rush_rules.tsv",
    }

    with zipfile.ZipFile(wheel) as archive:
        assert expected <= set(archive.namelist())

    expected_sdist = {f"src/{name}" for name in expected}
    with tarfile.open(sdist) as archive:
        names = {"/".join(Path(name).parts[1:]) for name in archive.getnames()}
        assert expected_sdist <= names
