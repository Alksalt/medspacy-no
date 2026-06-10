# AGENTS.md — medspacy-no

Capability and operating brief. Read **CLAUDE.md** for orientation, constraints, and ship profile. Implementation dossier: `docs/RESEARCH.md`. Live state: `status.md`.

## build phases

### P1 — resources/nb/ triple (days)

Three files constitute the core deliverable. All are the owner's clinical-language work seeded from published sources.

**`resources/nb/context_rules.json`** — JSON object with a `context_rules` list of `{category, literal, pattern, direction}` objects. Exact medspacy 1.3.1 format as `resources/en/context_rules.json`. `pattern` is `null` for plain phrase match or a spaCy Matcher token-pattern array for morphology-sensitive rules. Target ~120–180 rules total:

| category | target count | notes |
|---|---|---|
| NEGATED_EXISTENCE | ~60 | pre- and post-negation; covers "ingen", "uten", "ikke tegn til", "fri for", "negativ for", "avkreftet", "verken…eller" |
| POSSIBLE_EXISTENCE | ~30 | uncertainty; "kan ikke utelukkes", "mulig", "mistenkt", "obs mulig" |
| HYPOTHETICAL | ~20 | "hvis", "dersom", "obs", "ved behov" |
| HISTORICAL | ~15 | "tidligere", "gjennomgått", "anamnese" |
| FAMILY | ~25 | "mor/far/søsken/barn har", "familiær", "hereditet for" |
| TERMINATE | ~15 | sentence-break markers |

Seed from: Skeppstedt's published Swedish triggers (direct linguistic donor) + the 2018 Tromsø e-health poster's reported Norwegian rule set + `docs/SEEDS.md`. Hand-validate every trigger against clinical Norwegian usage. Swedish false-friends (sv "ej" vs no "ikke/ei") must be caught by the owner, not automated.

**`resources/nb/section_patterns.json`** — JSON object with a `section_rules` list of `{literal, category}` objects encoding the interregional strukturert innkomstjournal heading standard + epikrise sections (HIS 80226 / Helsepersonelloven §45a). Encode each heading with multiple casings and colon variants (`"Aktuelt"`, `"AKTUELT"`, `"Aktuelt:"`, `"Tidl. sykdommer"`, `"Tidligere sykdommer"`, etc.). Mapping target:

| Norwegian heading | medspacy category |
|---|---|
| Innkomstgrunn / Henvisningsårsak | chief_complaint |
| Tidligere sykdommer | past_medical_history |
| Familie / Sosialt / Hereditet | family_history / social_history |
| Aktuelt (aktuell anamnese) | history_of_present_illness |
| Naturlige funksjoner | natural_functions (new; open upstream discussion before PR) |
| Stimulantia | social_history |
| Allergier / Cave / Kritisk informasjon | allergies |
| Medikamenter (faste medisiner) | medications |
| Status presens / Funn | physical_exam |
| Vurdering | observation_and_plan |
| Tiltak / Plan | observation_and_plan |
| Sammenfatning / Epikrise | (epicrisis summary) |

**`resources/nb/rush_rules.tsv`** — PyRuSH clinical sentence rules for Norwegian. News-trained senter degrades on telegraphic notes, abbreviation-heavy text, list items, and missing terminal punctuation. These rules + the clinical abbreviation tokenizer (f.eks., bl.a., tbl., susp., u.a., ø.h., kl., mg., evt.) replace the parser-based sentencizer for clinical text. Unit-test on note-style fragments, not news text.

**Owner-only steps in P1** (do not delegate to automated agent):
- Authoring and validating every trigger in `context_rules.json`
- Validating Swedish-origin triggers against clinical Norwegian usage
- Writing and reviewing `section_patterns.json` literals against real sykehjem/sykehus note formats
- Building and curating the gold set (P3)

### P2 — PyPI package medspacy-no

Thin Python package wrapping the resources triple. Public interface:

```python
from medspacy_no import load_nb
nlp = load_nb()          # loads nb_core_news_lg, then adds medspacy components with bundled nb resources
```

Package structure:
```
src/medspacy_no/
    __init__.py          # exports load_nb()
    _loader.py           # loads spaCy model + medspacy components with explicit bundled resources/nb/
tests/
    test_context.py      # per-category P/R on synthetic gold
    test_sections.py     # section detection on known headings
    test_tokenizer.py    # clinical abbreviation tokenizer unit tests
pyproject.toml           # uv/setuptools; OSI license field
```

`nb_core_news_lg` recommended for vectors (entity work); `nb_core_news_sm` works for rule-based ConText. Do not hardcode model name — pass as parameter with `lg` as default.

### P3 — physician-authored synthetic gold set

300–500 sentences authored by the owner (utdannet lege, master i medisin, daily clinical Norwegian). Annotation design:
- Cover all five ConText categories + affirmed controls.
- Include an "affirmed-only" subset (~100 sentences containing no modifier triggers) to measure false-negation rate, mirroring Skeppstedt 2011's NPV design.
- Substrate: extend NorSynthClinical + NorSynthClinical-PHI sentences (with permission) or write independently.
- Double-annotate ≥100 sentences with a clinical colleague for inter-annotator agreement (Cohen's κ). κ target ≥0.80 for JOSS/workshop submission.
- Report per-category precision, recall, F1 against the gold set.
- State explicitly in any paper that evaluation is on synthetic text (identical limitation accepted in NorSynthClinical, Skeppstedt, and the Dutch medspacy module).

### P4 — JOSS submission

Rolling submission; no deadline. Required: public clonable repo, OSI license, passing tests, documentation, `paper.md` (~250–1000 words), production resources, release-readiness checks, public development history, research-use evidence, open-source workflow signals, and AI usage disclosure. Rule-based clinical NLP package is in scope once feature-complete; fixture scaffolds are not. Do not wait for a conference acceptance to prepare, but do not submit before the JOSS public-history and feature-completeness gates are met. JOSS reference: joss.readthedocs.io.

JOSS checklist:
- OSI license (MIT or Apache-2.0) in repo root
- `uv run pytest` passes
- `uv run python scripts/check_release_ready.py` passes
- `paper.md` with statement of need, citations, author affiliations
- API docs (docstrings + README usage sketch)
- Contribution guidelines

### P5 — upstream PR to medspacy

After PyPI ships and JOSS is submitted:
1. Open an upstream issue on medspacy asking maintainers to confirm preferred ISO code (`nb` vs `no`) for Norwegian Bokmål and whether `natural_functions` section category should be namespaced.
2. After maintainer response, submit a focused PR adding `resources/nb/` (context_rules.json, section_patterns.json, rush_rules.tsv). Mirror the structure of PR #293 (the 7-language multilingual PR, May 2024). Keep the PR small and reviewable.
3. Cite the PyPI package and JOSS paper in the PR description.

## delegation policy

| task | model | notes |
|---|---|---|
| rule-design review, phase planning, JOSS paper draft | opus | judgment tasks |
| Python implementation (loader, tokenizer, tests, pyproject.toml) | sonnet | |
| parallel implementation tasks (separate files, no shared state) | sonnet × N | fan out freely |
| trigger-lexicon authoring | owner only | clinical-language work |
| gold-set authoring | owner only | clinical-language work |
| false-friend validation (Swedish → Norwegian) | owner only | clinical-language work |

Never Haiku for any task in this project.
