from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ALLOWED_CONTEXT_CATEGORIES = frozenset(
    {
        "NEGATED_EXISTENCE",
        "POSSIBLE_EXISTENCE",
        "HYPOTHETICAL",
        "HISTORICAL",
        "FAMILY",
        "TERMINATE",
        "PSEUDO",
    }
)
ALLOWED_CONTEXT_DIRECTIONS = frozenset(
    {"FORWARD", "BACKWARD", "BIDIRECTIONAL", "TERMINATE", "PSEUDO"}
)
CONTEXT_REQUIRED_KEYS = frozenset({"category", "literal", "pattern", "direction"})
SECTION_REQUIRED_KEYS = frozenset({"category", "literal"})
RESOURCE_FILENAMES = ("context_rules.json", "section_patterns.json", "rush_rules.tsv")


def validate_context_rules(path: str | Path) -> list[str]:
    path = Path(path)
    errors: list[str] = []
    data = _read_json_object(path, errors)
    if data is None:
        return errors

    if set(data) != {"context_rules"}:
        errors.append(f"{path}: expected only top-level key 'context_rules'")
        return errors

    rules = data["context_rules"]
    if not isinstance(rules, list) or not rules:
        errors.append(f"{path}: 'context_rules' must be a non-empty list")
        return errors

    seen: set[tuple[str, str, str]] = set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"{path}: context rule {index} must be an object")
            continue

        missing = CONTEXT_REQUIRED_KEYS.difference(rule)
        if missing:
            errors.append(f"{path}: context rule {index} missing keys {sorted(missing)}")

        category = rule.get("category")
        direction = rule.get("direction")
        literal = rule.get("literal")
        if category not in ALLOWED_CONTEXT_CATEGORIES:
            errors.append(f"{path}: context rule {index} has unknown category {category!r}")
        if direction not in ALLOWED_CONTEXT_DIRECTIONS:
            errors.append(f"{path}: context rule {index} has unknown direction {direction!r}")
        if not isinstance(literal, str) or not literal:
            errors.append(f"{path}: context rule {index} must have a non-empty literal")

        key = (str(literal), str(category), str(direction))
        if key in seen:
            errors.append(f"{path}: duplicate context rule {key}")
        seen.add(key)

    if not errors:
        errors.extend(_validate_medspacy_context_loadable(path))
    return errors


def validate_section_rules(path: str | Path) -> list[str]:
    path = Path(path)
    errors: list[str] = []
    data = _read_json_object(path, errors)
    if data is None:
        return errors

    if set(data) != {"section_rules"}:
        errors.append(f"{path}: expected only top-level key 'section_rules'")
        return errors

    rules = data["section_rules"]
    if not isinstance(rules, list) or not rules:
        errors.append(f"{path}: 'section_rules' must be a non-empty list")
        return errors

    seen: set[tuple[str, str]] = set()
    for index, rule in enumerate(rules):
        if not isinstance(rule, dict):
            errors.append(f"{path}: section rule {index} must be an object")
            continue

        missing = SECTION_REQUIRED_KEYS.difference(rule)
        if missing:
            errors.append(f"{path}: section rule {index} missing keys {sorted(missing)}")

        category = rule.get("category")
        literal = rule.get("literal")
        if not isinstance(category, str) or not category:
            errors.append(f"{path}: section rule {index} must have a non-empty category")
        if not isinstance(literal, str) or not literal:
            errors.append(f"{path}: section rule {index} must have a non-empty literal")

        key = (str(literal), str(category))
        if key in seen:
            errors.append(f"{path}: duplicate section rule {key}")
        seen.add(key)

    if not errors:
        errors.extend(_validate_medspacy_section_loadable(path))
    return errors


def validate_rush_rules(path: str | Path) -> list[str]:
    path = Path(path)
    if not path.exists():
        return [f"{path}: file does not exist"]

    text = path.read_text()
    errors = []
    if "@Version" not in text:
        errors.append(f"{path}: missing @Version header")
    if "@MaxRepeatLength" not in text:
        errors.append(f"{path}: missing @MaxRepeatLength header")
    if "\tstbegin" not in text:
        errors.append(f"{path}: missing stbegin rules")
    if "\tstend" not in text:
        errors.append(f"{path}: missing stend rules")
    return errors


def validate_resource_sync(root_resource_dir: str | Path, package_resource_dir: str | Path) -> list[str]:
    root_resource_dir = Path(root_resource_dir)
    package_resource_dir = Path(package_resource_dir)
    errors = []

    for filename in RESOURCE_FILENAMES:
        root_file = root_resource_dir / filename
        package_file = package_resource_dir / filename
        if not root_file.exists():
            errors.append(f"{root_file}: file does not exist")
            continue
        if not package_file.exists():
            errors.append(f"{package_file}: file does not exist")
            continue
        if root_file.read_bytes() != package_file.read_bytes():
            errors.append(f"{filename}: root and packaged resources differ")

    return errors


def _read_json_object(path: Path, errors: list[str]) -> dict[str, Any] | None:
    if not path.exists():
        errors.append(f"{path}: file does not exist")
        return None

    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"{path}: invalid JSON: {exc}")
        return None

    if not isinstance(data, dict):
        errors.append(f"{path}: expected a JSON object")
        return None
    return data


def _validate_medspacy_context_loadable(path: Path) -> list[str]:
    from medspacy.context.context_rule import ConTextRule

    try:
        ConTextRule.from_json(path)
    except Exception as exc:  # pragma: no cover - exact medspaCy exception varies.
        return [f"{path}: medspaCy cannot load context rules: {exc}"]
    return []


def _validate_medspacy_section_loadable(path: Path) -> list[str]:
    from medspacy.section_detection.section_rule import SectionRule

    try:
        SectionRule.from_json(path)
    except Exception as exc:  # pragma: no cover - exact medspaCy exception varies.
        return [f"{path}: medspaCy cannot load section rules: {exc}"]
    return []
