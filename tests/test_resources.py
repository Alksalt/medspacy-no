from __future__ import annotations

import json
from pathlib import Path

import pytest

from medspacy_no.validation import (
    ALLOWED_CONTEXT_CATEGORIES,
    ALLOWED_CONTEXT_DIRECTIONS,
    validate_context_rules,
    validate_rush_rules,
    validate_resource_sync,
    validate_section_rules,
)


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOURCES = ROOT / "resources" / "nb"
PACKAGE_RESOURCES = ROOT / "src" / "medspacy_no" / "resources" / "nb"


def test_context_rules_use_medspacy_wrapper_schema() -> None:
    data = json.loads((ROOT_RESOURCES / "context_rules.json").read_text())

    assert set(data) == {"context_rules"}
    assert data["context_rules"]
    assert validate_context_rules(ROOT_RESOURCES / "context_rules.json") == []


def test_context_rules_reject_unknown_categories_and_directions(tmp_path: Path) -> None:
    path = tmp_path / "context_rules.json"
    path.write_text(
        json.dumps(
            {
                "context_rules": [
                    {
                        "category": "NOT_A_CONTEXT",
                        "literal": "ingen",
                        "pattern": None,
                        "direction": "SIDEWAYS",
                    }
                ]
            }
        )
    )

    errors = validate_context_rules(path)

    assert any("NOT_A_CONTEXT" in error for error in errors)
    assert any("SIDEWAYS" in error for error in errors)
    assert "NEGATED_EXISTENCE" in ALLOWED_CONTEXT_CATEGORIES
    assert "FORWARD" in ALLOWED_CONTEXT_DIRECTIONS


def test_section_rules_use_medspacy_wrapper_schema() -> None:
    data = json.loads((ROOT_RESOURCES / "section_patterns.json").read_text())

    assert set(data) == {"section_rules"}
    assert data["section_rules"]
    assert validate_section_rules(ROOT_RESOURCES / "section_patterns.json") == []


def test_rush_rules_have_required_pyrush_header() -> None:
    assert validate_rush_rules(ROOT_RESOURCES / "rush_rules.tsv") == []


def test_resource_copies_are_synchronized() -> None:
    assert validate_resource_sync(ROOT_RESOURCES, PACKAGE_RESOURCES) == []


@pytest.mark.xfail(
    reason="Production rule counts require owner-authored, clinically reviewed P1 resources.",
    strict=False,
)
def test_release_blocker_context_rule_counts_are_p1_ready() -> None:
    data = json.loads((ROOT_RESOURCES / "context_rules.json").read_text())
    categories = {}
    for rule in data["context_rules"]:
        categories[rule["category"]] = categories.get(rule["category"], 0) + 1

    assert categories["NEGATED_EXISTENCE"] >= 60
    assert categories["POSSIBLE_EXISTENCE"] >= 30
    assert categories["HYPOTHETICAL"] >= 20
    assert categories["HISTORICAL"] >= 15
    assert categories["FAMILY"] >= 25
