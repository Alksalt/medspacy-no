# medspacy-no

Norwegian Bokmal language module for [medspacy](https://github.com/medspacy/medspacy): ConText trigger rules for clinical negation, uncertainty, hypothetical, historical, and family contexts + Norwegian clinical section detection + clinical sentence segmentation.

Planned as a standalone PyPI package, then as an upstream contribution to medspacy `resources/nb/`.

Current state: infrastructure-first pre-release scaffold. The package, loader, validators, tokenizer, and build checks exist; the production clinical rules are still owner-reviewed P1 work. The resource files currently contain non-production smoke fixtures so the package contract can be tested without delegating clinical-language authoring to an automated agent.

Do not use the current fixture resources for clinical work, research claims, or benchmark results.

## install

```
uv add medspacy-no
```

Requires Python ≥3.9, medspacy ≥1.3.1, and the spaCy Norwegian Bokmål model:

```
uv run python -m spacy download nb_core_news_lg
```

## usage

```python
from medspacy_no import load_nb

nlp = load_nb()
print(nlp.pipe_names)
```

Production clinical examples will be added after the owner-reviewed Norwegian rules replace the current smoke fixtures.

`load_nb()` defaults to `nb_core_news_lg`, accepts an existing spaCy `Language` object for tests, installs the Norwegian clinical tokenizer, and adds medspaCy components with explicit bundled resource paths. It does not rely on medspaCy finding `resources/nb/` inside the medspaCy package.

## what's inside

```
resources/nb/
    context_rules.json      medspaCy-wrapped ConText rules: {"context_rules": [...]}
    section_patterns.json   medspaCy-wrapped section rules: {"section_rules": [...]}
    rush_rules.tsv          PyRuSH clinical sentence segmentation rules
    abbreviations.txt       period-bearing clinical abbreviations kept as single tokens
```

ConText categories: `NEGATED_EXISTENCE`, `POSSIBLE_EXISTENCE`, `HYPOTHETICAL`, `HISTORICAL`, `FAMILY`. Rule format is medspacy's standard cycontext schema — zero new schema.

Production section categories will cover the interregional strukturert innkomstjournal standard (Alme & Karlsen 2014) and the Epikrise v1.2 / HIS 80226 heading set after owner review.

## development

```
uv run python -m pytest
uv run python scripts/validate_resources.py
uv run python scripts/check_owner_review.py
uv run python scripts/check_release_ready.py  # expected to fail until owner-reviewed P1 resources replace fixtures
```

The test suite includes an expected release-blocker xfail for production rule counts. That xfail should only be removed after the owner-authored `resources/nb/` triple is clinically reviewed.

**Note on history:** this repository was extracted from prior private work and published in June 2026; the public commit history therefore starts at publication. Pre-release status and evaluation limitations are described in this README.

## evaluation

_Evaluation results pending. Gold set: physician-authored synthetic corpus, 300–500 sentences, per-category P/R/F, Cohen's κ on ≥100 double-annotated sentences. Note: evaluation is conducted on synthetic clinical text; no openly redistributable Norwegian EHR ConText/assertion gold set is currently available._

KliniskVestBERT (2026) shows that Norwegian clinical NLP on real de-identified Helse Vest text exists, so this package does not claim to be the first Norwegian clinical NLP resource. The intended niche is an open Norwegian Bokmal medspaCy/ConText resource package.

## safety and privacy

This is research software, not a medical device or clinical decision-support system. Do not use it for patient care without local validation. Do not process identifiable patient data unless you have the required legal basis, approvals, and safeguards.

## license

MIT

## citation

_Citation pending JOSS submission._

## author

Oleksandr Altukhov — utdannet lege (master i medisin), agentic-AI engineer, Kristiansund. GitHub: [Alksalt](https://github.com/Alksalt). Web: [alksalt.com](https://alksalt.com).
