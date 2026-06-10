from __future__ import annotations

import sys
from pathlib import Path

from medspacy_no.validation import (
    validate_context_rules,
    validate_resource_sync,
    validate_rush_rules,
    validate_section_rules,
)


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOURCES = ROOT / "resources" / "nb"
PACKAGE_RESOURCES = ROOT / "src" / "medspacy_no" / "resources" / "nb"


def main() -> int:
    errors = []
    errors.extend(validate_context_rules(ROOT_RESOURCES / "context_rules.json"))
    errors.extend(validate_section_rules(ROOT_RESOURCES / "section_patterns.json"))
    errors.extend(validate_rush_rules(ROOT_RESOURCES / "rush_rules.tsv"))
    errors.extend(validate_resource_sync(ROOT_RESOURCES, PACKAGE_RESOURCES))

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Norwegian medspaCy resources are schema-valid and synchronized.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
