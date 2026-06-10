# CLAUDE.md — medspacy-no

Norwegian language module for medspacy: ConText trigger rules (negation/uncertainty/hypothetical/historical/family) + Norwegian clinical section detection + clinical sentence segmentation. Distributed as PyPI package `medspacy-no` first, upstream PR to medspacy second. Cheapest citable artifact in the ehelse portfolio — supports the Helse Midt-Norge PhD application due 1 Sept 2026.

## current status (2026-06-10)

Infrastructure-first scaffold implemented. Recommended first ship of the portfolio (days of work). Research complete; see `docs/RESEARCH.md` for the full implementation dossier. `docs/SEEDS.md` (Swedish trigger list + 2018 Tromsø poster rules + Norwegian candidates table + abbreviation sources) and `docs/PERMISSION-EMAIL.md` (bokmål draft to LTG/UiO authors) are present. Production clinical resources remain owner-only P1 work.

## hard constraints

- Reuse medspacy's exact rule formats (JSON schema is fixed — zero new schema).
- PyPI standalone package first; upstream PR only after PyPI ships.
- Open the `nb` vs `no` naming issue upstream before the PR.
- Never redistribute NorSynthClinical / NorSynthClinical-PHI / NorMedTerm derivatives without written permission from LTG/UiO (Øvrelid, Brekke) and Bråten — those repos carry no LICENSE file.
- State the synthetic-eval limitation plainly in any publication. No hedging.
- OSI license only (MIT or Apache-2.0).
- Do not gate the software release on a conference. JOSS runs rolling; Clinical NLP Workshop 2027 / NoDaLiDa 2027 are the eval-paper targets.
- Trigger-lexicon authoring, gold-set authoring, and false-friend validation are owner-only clinical-language steps — do not delegate to an automated agent.
- Never Haiku. Opus for rule-design review and planning; Sonnet for implementation.

## workspace map

```
docs/RESEARCH.md       implementation dossier (source of truth — do not edit)
docs/SEEDS.md          trigger lexicon seeds (arriving — builder starts here)
docs/PERMISSION-EMAIL.md  bokmål draft to LTG/UiO authors
docs/PLAN.md           phased v0.1 plan
docs/IDEAS.md          v0.2+ backlog
docs/THOUGHTS.md       open questions and design tensions
docs/SOURCES.md        all URLs from the dossier
DECISIONS.md           hard imperatives for this project
status.md              live state + dated next actions
README.md              public repo skeleton
resources/nb/          owner-facing resource files; currently synchronized smoke fixtures
src/medspacy_no/       Python package source + bundled resources/nb/ copy
tests/                 pytest suite, including release-blocker xfail for P1 rule counts
paper.md               JOSS paper
```

## ship profile

```yaml
base_branch: main
ship_method: push
quality_gates:
  - uv run pytest
wiki_path: "/Users/ol/Library/Mobile Documents/iCloud~md~obsidian/Documents/alt-wiki/projects/ehelse/"
```
