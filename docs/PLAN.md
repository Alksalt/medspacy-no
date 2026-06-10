# docs/PLAN.md — v0.1 phased plan

Source: `docs/RESEARCH.md` section RECOMMENDED-V01. This plan is executable; start from `docs/SEEDS.md`.

## phase 1 — resources/nb/ triple

### context_rules.json format

medspaCy 1.3.1 expects a JSON object with a `context_rules` wrapper key. Each entry is one of:

```json
{
  "context_rules": [
    {"category": "NEGATED_EXISTENCE", "literal": "ingen", "pattern": null, "direction": "FORWARD"},
    {"category": "NEGATED_EXISTENCE", "literal": "ikke tegn til",
     "pattern": [{"LOWER": "ikke"}, {"LOWER": "tegn"}, {"LOWER": "til"}],
     "direction": "FORWARD"}
  ]
}
```

Fields:
- `category` — one of `NEGATED_EXISTENCE`, `POSSIBLE_EXISTENCE`, `HYPOTHETICAL`, `HISTORICAL`, `FAMILY`
- `literal` — plain string; used for display and as fallback match if `pattern` is null
- `pattern` — null or a spaCy Matcher token-pattern array (use for morphology, optional tokens, inline alternation)
- `direction` — `FORWARD`, `BACKWARD`, or `TERMINATE`

Lexicon size targets:

| category | target | seed sources |
|---|---|---|
| NEGATED_EXISTENCE | ~60 | Skeppstedt PRE + POST lists; poster PREN/POST; clinical: ingen, uten, ikke, fri for, negativ for, avkreftet, benekter, utelukket, verken…eller |
| POSSIBLE_EXISTENCE | ~30 | uncertainty: kan ikke utelukkes, mulig, mistenkt, mistanke om, obs mulig, sannsynlig, trolig, eventuelt |
| HYPOTHETICAL | ~20 | hvis, dersom, ved, obs (as modifier), ved behov, i tilfelle |
| HISTORICAL | ~15 | tidligere, gjennomgått, gjennomgikk, anamnestisk, i anamnesen, for X år siden |
| FAMILY | ~25 | mor har, far har, søsken har, barn har, foreldre, familiær forekomst av, hereditet for, arv |
| TERMINATE | ~15 | full-stop patterns, colon-header markers, list-item separators |

Total target: 120–180 rules. Quality over quantity. Each rule must be validated against authentic clinical Norwegian usage by the owner before commit.

### section_patterns.json format

```json
{
  "section_rules": [
    {"literal": "Aktuelt:", "category": "history_of_present_illness"},
    {"literal": "AKTUELT", "category": "history_of_present_illness"},
    {"literal": "Aktuelt", "category": "history_of_present_illness"}
  ]
}
```

Encode each canonical heading with at minimum: plain, uppercase, trailing-colon, and common abbreviated forms. Headings to cover:

| literals (representative — encode all variants) | category |
|---|---|
| Innkomstgrunn, Henvisningsårsak, Innleggelsesårsak | chief_complaint |
| Tidligere sykdommer, Tidl. sykdommer, Sykehistorie, Tidligere sykehistorie | past_medical_history |
| Familie, Familieanamnese, Hereditet | family_history |
| Sosialt, Sosialanamnese, Sivilstatus | social_history |
| Aktuelt, Aktuell anamnese, Anamnese | history_of_present_illness |
| Naturlige funksjoner, Nat. funk. | natural_functions |
| Stimulantia, Røyk, Alkohol | social_history |
| Allergier, Cave, Kritisk informasjon, Overfølsomhet | allergies |
| Medikamenter, Faste medisiner, Medisinliste, Medikamenter ved innkomst | medications |
| Status presens, Funn, Objektiv undersøkelse | physical_exam |
| Vurdering, Konklusjon | observation_and_plan |
| Tiltak, Plan, Videre plan | observation_and_plan |
| Sammenfatning, Epikrise, Utskrivingsnotat | (map to summary/discharge) |
| Diagnose(r), Diagnoser | diagnoses |
| Behandling, Behandlingsforløp | hospital_course |
| Anbefaling, Videre oppfølging | patient_instructions |

Note: `natural_functions` is not in medspacy's existing category set. Open an upstream discussion before the PR; use a local extension for the standalone PyPI package in the meantime.

### rush_rules.tsv

PyRuSH rules file. Norwegian clinical abbreviation list for the tokenizer (do not split on internal periods):

f.eks., bl.a., tbl., susp., u.a., ø.h., kl., mg., evt., jf., pga., ift., mtp., ivf., s.c., i.m., i.v., obs., ca., dr., prof., st., avd., sengepost, NaCl, ml., dl., mmol/l, μmol/l

Unit-test by running the tokenizer and senter on short telegraphic note fragments, not on news sentences. Failing case pattern: `"Ingen diaré. Diuresen god. Afebryl."` split incorrectly at abbreviation periods.

## phase 2 — Python package

`pyproject.toml` with:
- `name = "medspacy-no"`
- `license = {text = "MIT"}`
- `dependencies = ["medspacy>=1.3", "spacy[nb]>=3.7"]`

`load_nb(model="nb_core_news_lg")` — single public function. Accepts a model name or an existing spaCy `Language`. Load the spaCy model, install the Norwegian clinical tokenizer, then add medspaCy components with explicit bundled rule paths. Do not rely on `medspacy.load(language_code="nb")` finding resources inside the `medspacy` package.

Package data: include `resources/nb/*.json` and `resources/nb/*.tsv` in `MANIFEST.in` and `pyproject.toml` package-data declaration.

## phase 3 — eval design

Gold set: 300–500 sentences authored by the owner (utdannet lege, cand.med.). Distribution:
- ~100 NEGATED_EXISTENCE
- ~60 POSSIBLE_EXISTENCE
- ~40 HYPOTHETICAL
- ~30 HISTORICAL
- ~50 FAMILY
- ~100 affirmed controls (no modifier trigger present — used for NPV / false-negation rate, mirroring Skeppstedt's design)

Substrate: NorSynthClinical sentences (with permission) or original synthetic text if permission lags.

IAA: double-annotate ≥100 sentences with a clinical colleague. Report Cohen's κ. κ ≥0.80 is the target for submission.

Metrics: per-category precision, recall, F1. Report separately for affirmed-only sentences (false-negation rate). State the synthetic limitation plainly in every results table.

## phase 4 — JOSS submission

Paper checklist:
- OSI license (MIT or Apache-2.0) in repo root — required
- `uv run pytest` passes — required
- `paper.md`: statement of need (no Norwegian ConText module exists), description, installation instructions, references to Skeppstedt 2011 + medspacy AMIA 2021 + the 2018 Norwegian poster
- Author affiliations: Oleksandr Altukhov, independent (Kristiansund, Norway)
- JOSS submission at joss.theoj.org; select "Natural Language Processing" subject area

## phase 5 — upstream PR

1. Open a GitHub issue on medspacy/medspacy: "Norwegian Bokmål support — confirm `nb` vs `no` directory naming and `natural_functions` section category". Link the PyPI package.
2. After maintainer confirmation, open a PR adding `resources/nb/` only. No Python code changes. Title: "Add Norwegian Bokmål (nb) language resources". Body includes: link to PyPI package, JOSS DOI, eval summary.
3. Mirror the style of PR #293 (the May 2024 multilingual PR): small, focused, well-documented diff.
