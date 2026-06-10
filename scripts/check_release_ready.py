from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from medspacy_no.validation import (
    RELEASE_MIN_CONTEXT_RULES,
    RELEASE_MIN_SECTION_RULES,
    RELEASE_REQUIRED_SECTION_CATEGORIES,
    load_abbreviations,
)


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOURCES = ROOT / "resources" / "nb"
PACKAGE_RESOURCES = ROOT / "src" / "medspacy_no" / "resources" / "nb"

NON_PRODUCTION_MARKERS = ("placeholder", "smoke", "owner-reviewed p1", "owner_reviewed: false")
PRIVATE_CLASSIFIER = "Private :: Do Not Upload"


def main() -> int:
    errors = check_release_ready(ROOT_RESOURCES, PACKAGE_RESOURCES, project_root=ROOT)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("medspacy-no resources are release-ready.")
    return 0


def check_release_ready(
    root_resource_dir: Path,
    package_resource_dir: Path,
    *,
    project_root: Path | None = None,
    min_context_counts: Mapping[str, int] = RELEASE_MIN_CONTEXT_RULES,
    min_section_rules: int = RELEASE_MIN_SECTION_RULES,
    required_section_categories: Sequence[str] = RELEASE_REQUIRED_SECTION_CATEGORIES,
) -> list[str]:
    errors: list[str] = []
    errors.extend(_check_context_rules(root_resource_dir / "context_rules.json", min_context_counts))
    errors.extend(
        _check_section_rules(
            root_resource_dir / "section_patterns.json",
            min_section_rules,
            required_section_categories,
        )
    )
    errors.extend(_check_rush_rules(root_resource_dir / "rush_rules.tsv"))
    errors.extend(_check_abbreviations(root_resource_dir / "abbreviations.txt"))
    errors.extend(_check_packaged_copy(root_resource_dir, package_resource_dir))
    if project_root is not None:
        errors.extend(_check_packaging_metadata(project_root))
    return errors


def _check_context_rules(path: Path, min_context_counts: Mapping[str, int]) -> list[str]:
    errors: list[str] = []
    data = _read_json(path, errors)
    if data is None:
        return errors
    rules = data.get("context_rules", []) if isinstance(data, dict) else []
    errors.extend(_fixture_errors(path, rules))

    counts: dict[str, int] = {}
    for rule in rules:
        if isinstance(rule, dict):
            category = str(rule.get("category"))
            counts[category] = counts.get(category, 0) + 1

    for category, minimum in min_context_counts.items():
        actual = counts.get(category, 0)
        if actual < minimum:
            errors.append(f"{path}: {category} has {actual} rules; release requires at least {minimum}")

    return errors


def _check_section_rules(
    path: Path,
    min_section_rules: int,
    required_section_categories: Sequence[str],
) -> list[str]:
    errors: list[str] = []
    data = _read_json(path, errors)
    if data is None:
        return errors
    rules = data.get("section_rules", []) if isinstance(data, dict) else []
    errors.extend(_fixture_errors(path, rules))

    if len(rules) < min_section_rules:
        errors.append(f"{path}: has {len(rules)} section rules; release requires at least {min_section_rules}")

    categories = {str(rule.get("category")) for rule in rules if isinstance(rule, dict)}
    for required in required_section_categories:
        if required not in categories:
            errors.append(f"{path}: missing required section category {required!r}")

    return errors


def _check_rush_rules(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path}: file does not exist"]

    text = path.read_text()
    lowered = text.lower()
    errors: list[str] = []
    for marker in NON_PRODUCTION_MARKERS:
        if marker in lowered:
            errors.append(f"{path}: contains non-production PyRuSH marker {marker!r}")
    if text.count("\tstbegin") < 5:
        errors.append(f"{path}: has too few stbegin rules for release")
    if text.count("\tstend") < 5:
        errors.append(f"{path}: has too few stend rules for release")
    return errors


def _check_abbreviations(path: Path) -> list[str]:
    if not path.exists():
        return [f"{path}: file does not exist"]

    errors: list[str] = []
    lowered = path.read_text().lower()
    for marker in NON_PRODUCTION_MARKERS:
        if marker in lowered:
            errors.append(f"{path}: contains non-production abbreviation marker {marker!r}")
    if not load_abbreviations(path):
        errors.append(f"{path}: must contain at least one abbreviation")
    return errors


def _check_packaged_copy(root_resource_dir: Path, package_resource_dir: Path) -> list[str]:
    if not root_resource_dir.is_dir():
        return [f"{root_resource_dir}: resource directory does not exist"]

    errors: list[str] = []
    for root_path in sorted(root_resource_dir.iterdir()):
        if not root_path.is_file():
            continue
        package_path = package_resource_dir / root_path.name
        if not package_path.exists():
            errors.append(f"{package_path}: packaged resource copy is missing")
        elif package_path.read_bytes() != root_path.read_bytes():
            errors.append(f"{root_path.name}: root and packaged resources differ")
    return errors


def _check_packaging_metadata(project_root: Path) -> list[str]:
    errors: list[str] = []

    pyproject = project_root / "pyproject.toml"
    if not pyproject.exists():
        errors.append(f"{pyproject}: file does not exist")
    elif PRIVATE_CLASSIFIER in pyproject.read_text():
        errors.append(f"{pyproject}: remove the {PRIVATE_CLASSIFIER!r} classifier before release")

    paper = project_root / "paper.md"
    if not paper.exists():
        errors.append(f"{paper}: JOSS paper.md is missing")

    return errors


def _fixture_errors(path: Path, rules: Any) -> list[str]:
    errors: list[str] = []
    if not isinstance(rules, list):
        return [f"{path}: expected a list of rules"]

    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            continue
        literal = str(rule.get("literal", ""))
        metadata = rule.get("metadata")
        if "__medspacy_no_fixture" in literal.lower():
            errors.append(f"{path}: rule {index} is a fixture literal")
        if isinstance(metadata, dict):
            if metadata.get("fixture") is True:
                errors.append(f"{path}: rule {index} has fixture=true")
            if metadata.get("owner_reviewed") is False:
                errors.append(f"{path}: rule {index} has owner_reviewed=false")
    return errors


def _read_json(path: Path, errors: list[str]) -> Any:
    if not path.exists():
        errors.append(f"{path}: file does not exist")
        return None
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None


if __name__ == "__main__":
    raise SystemExit(main())
