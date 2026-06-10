# Contributing

This project is infrastructure-first until the Norwegian clinical resources are owner-reviewed.

## Development

```
uv run python scripts/validate_resources.py
uv run python scripts/check_owner_review.py
uv run python scripts/check_release_ready.py  # fails until owner-reviewed production resources replace fixtures
uv run python -m compileall src/medspacy_no scripts tests
uv run python -m pytest
```

## Clinical Resource Boundary

Do not add production Norwegian ConText triggers, section headings, PyRuSH clinical rules, or gold-set labels unless they have been reviewed by the project owner. Automated agents may help with structure, validation, scripts, tests, and documentation; clinical-language approval remains owner-only.

Use [docs/P1_OWNER_REVIEW.md](docs/P1_OWNER_REVIEW.md) and [data/owner_review/context_rule_candidates.tsv](data/owner_review/context_rule_candidates.tsv) for the first review pass.

## Contribution and Support Policy

Open issues for code, packaging, documentation, and reproducible test failures. Clinical resource proposals must include provenance and remain unmerged until owner-reviewed.

Do not submit real patient text, PHI, memorized patient cases, or unlicensed third-party clinical text. By contributing resource examples, you attest that they are synthetic, public-domain, properly licensed, or independently authored with permission to redistribute.
