# medspacy-no

Norwegian language module for [medspacy](https://github.com/medspacy/medspacy): ConText trigger rules for clinical negation, uncertainty, hypothetical, historical, and family contexts + Norwegian clinical section detection + clinical sentence segmentation.

Distributed as a standalone PyPI package. Intended as an upstream contribution to medspacy `resources/nb/`.

Current state: infrastructure-first scaffold. The package, loader, validators, tokenizer, and build checks exist; the production clinical rules are still owner-reviewed P1 work. The resource files currently contain non-production smoke fixtures so the package contract can be tested without delegating clinical-language authoring to an automated agent.

## install

```
uv add medspacy-no
```

Requires Python ≥3.9, medspacy ≥1.3, and the spaCy Norwegian Bokmål model:

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
```

ConText categories: `NEGATED_EXISTENCE`, `POSSIBLE_EXISTENCE`, `HYPOTHETICAL`, `HISTORICAL`, `FAMILY`. Rule format is medspacy's standard cycontext schema — zero new schema.

Production section categories will cover the interregional strukturert innkomstjournal standard (Alme & Karlsen 2014) and the Epikrise v1.2 / HIS 80226 heading set after owner review.

## development

```
uv run python -m pytest
uv run python scripts/validate_resources.py
uv run python scripts/check_owner_review.py
```

The test suite includes an expected release-blocker xfail for production rule counts. That xfail should only be removed after the owner-authored `resources/nb/` triple is clinically reviewed.

## evaluation

_Evaluation results pending. Gold set: physician-authored synthetic corpus, 300–500 sentences, per-category P/R/F, Cohen's κ on ≥100 double-annotated sentences. Note: evaluation is conducted on synthetic clinical text; no de-identified real Norwegian EHR corpus is openly available._

## license

MIT

## citation

_Citation pending JOSS submission._

## author

Oleksandr Altukhov — utdannet lege (cand.med.), agentic-AI engineer, Kristiansund. GitHub: [Alksalt](https://github.com/Alksalt). Web: [alksalt.com](https://alksalt.com).
