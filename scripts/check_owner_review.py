from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_FILE = ROOT / "data" / "owner_review" / "context_rule_candidates.tsv"
REQUIRED_COLUMNS = (
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
)
ALLOWED_STATUSES = {"pending", "approved", "rejected", "revise"}
ALLOWED_DIRECTIONS = {"FORWARD", "BACKWARD", "BIDIRECTIONAL", "TERMINATE", "PSEUDO"}
ALLOWED_CATEGORIES = {
    "NEGATED_EXISTENCE",
    "POSSIBLE_EXISTENCE",
    "HYPOTHETICAL",
    "HISTORICAL",
    "FAMILY",
    "TERMINATE",
    "PSEUDO",
}


def validate_owner_review(path: str | Path = REVIEW_FILE) -> list[str]:
    path = Path(path)
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: file does not exist"]

    with path.open(newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        if reader.fieldnames != list(REQUIRED_COLUMNS):
            return [f"{path}: expected columns {list(REQUIRED_COLUMNS)}, got {reader.fieldnames}"]
        rows = list(reader)

    if not rows:
        errors.append(f"{path}: must contain at least one candidate row")
        return errors

    seen: set[tuple[str, str, str, str, str]] = set()
    for line_number, row in enumerate(rows, start=2):
        _validate_required_cell(path, line_number, row, "source", errors)
        _validate_required_cell(path, line_number, row, "norwegian_candidate", errors)
        _validate_required_cell(path, line_number, row, "proposed_category", errors)
        _validate_required_cell(path, line_number, row, "proposed_direction", errors)
        _validate_required_cell(path, line_number, row, "review_status", errors)

        status = row["review_status"]
        category = row["proposed_category"]
        direction = row["proposed_direction"]
        candidate = row["norwegian_candidate"]
        source = row["source"]
        key = (source, row["swedish_phrase"], candidate, category, direction)

        if status not in ALLOWED_STATUSES:
            errors.append(f"{path}:{line_number}: unknown review_status {status!r}")
        if category not in ALLOWED_CATEGORIES:
            errors.append(f"{path}:{line_number}: unknown proposed_category {category!r}")
        if direction not in ALLOWED_DIRECTIONS:
            errors.append(f"{path}:{line_number}: unknown proposed_direction {direction!r}")
        if key in seen:
            errors.append(f"{path}:{line_number}: duplicate candidate {key}")
        seen.add(key)

        if status == "approved":
            if not row["clinical_reviewer"]:
                errors.append(f"{path}:{line_number}: approved row lacks clinical_reviewer")
            if not row["reviewed_date"]:
                errors.append(f"{path}:{line_number}: approved row lacks reviewed_date")
            if not row["review_notes"]:
                errors.append(f"{path}:{line_number}: approved row lacks review_notes")

    return errors


def _validate_required_cell(
    path: Path,
    line_number: int,
    row: dict[str, str],
    column: str,
    errors: list[str],
) -> None:
    if not row[column]:
        errors.append(f"{path}:{line_number}: missing {column}")


def main() -> int:
    errors = validate_owner_review()
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Owner review worksheet is structurally valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
