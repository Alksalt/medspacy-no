# P1 Owner Review Workflow

This file is the handoff point between the infrastructure scaffold and the owner-only clinical-language work.

## Context Rules

1. Open `data/owner_review/context_rule_candidates.tsv`.
2. For each row, decide whether the Norwegian candidate is clinically valid Bokmal charting language.
3. Set `review_status` to `approved`, `rejected`, or `revise`.
4. For every `approved` row, fill `clinical_reviewer`, `reviewed_date`, and `review_notes`.
5. Only after approval, convert the reviewed candidate into `resources/nb/context_rules.json` and the synchronized bundled copy under `src/medspacy_no/resources/nb/context_rules.json`.

Rows derived from Swedish false friends or uncertain notes must not be approved without explicit review notes.

## Section Patterns

Author `resources/nb/section_patterns.json` from real Norwegian innkomstjournal and epikrise heading style. Keep the medspaCy wrapper schema:

```json
{"section_rules": [{"literal": "Aktuelt:", "category": "history_of_present_illness"}]}
```

## PyRuSH Rules

Replace the current placeholder `rush_rules.tsv` with Norwegian clinical-note rules after checking note-style fragments with abbreviations, lists, and missing terminal punctuation.

## Tokenizer Abbreviations

Review `resources/nb/abbreviations.txt` (period-bearing charting abbreviations kept as single tokens; seeded from docs/RESEARCH.md and docs/PLAN.md, including candidates like `ift.`, `ivf.`, `prof.`, `st.`, `avd.`, `ml.`, `dl.` not yet added). After review, change the `# owner_reviewed: false` header line to `# owner_reviewed: true` and sync the copy under `src/medspacy_no/resources/nb/`. The release gate fails while the file is marked unreviewed.

## Release Gate

The expected xfail in `tests/test_resources.py::test_release_blocker_context_rule_counts_are_p1_ready` should only be removed when P1 resources are production-ready.
