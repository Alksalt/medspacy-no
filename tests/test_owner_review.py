from __future__ import annotations

from pathlib import Path

from scripts.check_owner_review import ALLOWED_STATUSES, REVIEW_FILE, validate_owner_review


def test_owner_review_worksheet_is_valid() -> None:
    assert validate_owner_review(REVIEW_FILE) == []


def test_context_rule_candidates_use_allowed_review_statuses() -> None:
    with REVIEW_FILE.open(newline="") as file:
        import csv

        rows = list(csv.DictReader(file, delimiter="\t"))

    assert rows
    assert {row["review_status"] for row in rows} <= ALLOWED_STATUSES


def test_approved_rows_require_clinical_review_metadata(tmp_path: Path) -> None:
    path = tmp_path / "context_rule_candidates.tsv"
    path.write_text(
        "\t".join(
            [
                "source",
                "swedish_phrase",
                "source_tag",
                "norwegian_candidate",
                "proposed_category",
                "proposed_direction",
                "review_status",
                "clinical_reviewer",
                "reviewed_date",
                "review_notes",
            ]
        )
        + "\n"
        + "\t".join(
            [
                "Skeppstedt 2011",
                "inte",
                "pren",
                "ikke",
                "NEGATED_EXISTENCE",
                "FORWARD",
                "approved",
                "",
                "",
                "",
            ]
        )
        + "\n"
    )

    errors = validate_owner_review(path)

    assert any("clinical_reviewer" in error for error in errors)
    assert any("reviewed_date" in error for error in errors)
    assert any("review_notes" in error for error in errors)
