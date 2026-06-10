# medspacy-no — Implementation Dossier

## MEDSPACY-ARCHITECTURE

**Multilingual was added May 2024; the design is "resources keyed by language code".** The restructure landed in PR #293 "Issue 264 other languages", authored by `burgersmoke` (Andrew Eyre/Kelly Peterson's group) and merged by `jianlins` on 2024-05-14 ([github.com/medspacy/medspacy/pull/293](https://github.com/medspacy/medspacy/pull/293)). It was triggered by issue #264, opened by `@mpasternak` (Polish group) on 2023-12-12, which debated "integrated language dirs vs. a thin translating wrapper"; the maintainers chose integrated language directories ([github.com/medspacy/medspacy/issues/264](https://github.com/medspacy/medspacy/issues/264)).

**Resource layout (verified via GitHub tree on `master`).** Eight language dirs exist, none Norwegian:
```
resources/{de,en,es,fr,it,nl,pl,pt}/
  context_rules.json      # ConText trigger rules
  section_patterns.json   # section-header rules
  rush_rules.tsv          # PyRuSH sentence-segmentation rules
  quickumls/              # optional UMLS concept DB (binary)
```
Source: `gh api repos/medspacy/medspacy/git/trees/master?recursive=1`. Maturity is uneven — only `en`, `fr`, `es`, `nl` have non-trivial ConText rules; `de/it/pl/pt` are largely skeletal ([github.com/medspacy/medspacy/blob/master/README.md](https://github.com/medspacy/medspacy/blob/master/README.md)).

**ConText rule format (`context_rules.json`).** A flat JSON list of objects with exactly four fields — the `cycontext`/`ConTextRule.from_json` format:
```json
{"category": "NEGATED_EXISTENCE", "literal": "absence of", "pattern": null, "direction": "FORWARD"}
{"category": "NEGATED_EXISTENCE", "literal": "ruled out",
 "pattern": [{"LOWER": {"IN": ["ruled","rules"]}},
             {"LOWER": {"IN": ["him","her","them","patient","pt"]}, "OP": "?"},
             {"LOWER": "out"}], "direction": "FORWARD"}
```
`pattern` is `null` (plain phrase match on `literal`) or a spaCy `Matcher` token-pattern array. Categories used in `en` (~140 rules): `NEGATED_EXISTENCE`, `POSSIBLE_EXISTENCE`, `HYPOTHETICAL`, `HISTORICAL`, `FAMILY`. Directions: `FORWARD`, `BACKWARD`, `TERMINATE` ([raw.githubusercontent.com/medspacy/medspacy/master/resources/en/context_rules.json](https://raw.githubusercontent.com/medspacy/medspacy/master/resources/en/context_rules.json)).

**Section rule format (`section_patterns.json`).** List of `{"literal": "...", "category": "..."}` (the `SectionRule` class also supports an optional `pattern` field, but the `en` file uses literals only). ~25 categories: `chief_complaint`, `past_medical_history`, `medications`, `allergies`, `family_history`, `social_history`, `history_of_present_illness`, `hospital_course`, `physical_exam`, `observation_and_plan`, `diagnoses`, `problem_list`, `labs_and_studies`, `imaging`, `signature`, etc. ([raw.githubusercontent.com/medspacy/medspacy/master/resources/en/section_patterns.json](https://raw.githubusercontent.com/medspacy/medspacy/master/resources/en/section_patterns.json)).

**Language loading mechanism (verified in source `medspacy/context/context.py`).** `ConText.__init__` takes `language_code: str = 'en'` and builds the resource path directly:
```python
self.DEFAULT_RULES_FILEPATH = path.join(
    Path(__file__).resolve().parents[2], "resources",
    language_code.lower(), "context_rules.json")
...
if rules == "default":
    self.add(ConTextRule.from_json(self.DEFAULT_RULES_FILEPATH))
```
So **a new language is enabled simply by creating `resources/<code>/context_rules.json` and passing `language_code="<code>"`** (the docstring: "Language code to use (ISO code) as a default for loading resources … see the /resources directory") ([github.com/medspacy/medspacy/blob/master/medspacy/context/context.py](https://github.com/medspacy/medspacy/blob/master/medspacy/context/context.py)). A language module therefore minimally consists of: a spaCy base pipeline of that language + a `context_rules.json` (+ optional `section_patterns.json`, `rush_rules.tsv`).

**Maintainer activity / PR patterns.** Repo is actively maintained in 2026: recent merged PRs include #335 sectionizer fix and #325 "Alec context refactor" + #326 "Release: CI/CD Improvements" (March–April 2026). Small focused PRs and doc fixes are merged routinely; the multilingual PR #293 was 25 commits and merged cleanly. Current release 1.3.1 (2024-11-21). Core authors: H. Eyre, A.B. Chapman, K.S. Peterson et al. (paper: "Launching into clinical space with medspaCy", AMIA 2021) ([semanticscholar.org/paper/07644c0aedf88eec0e848a3329cd924754689a79](https://www.semanticscholar.org/paper/Launching-into-clinical-space-with-medspaCy:-a-new-Eyre-Chapman/07644c0aedf88eec0e848a3329cd924754689a79)). I found **no separate "medspacy multilingual" AMIA/MIE paper** — the multilingual work exists only as code/README, not a published poster (searched AMIA/MIE; the Geneva/multilingual paper the brief references could not be located and likely does not exist as a citable artifact).

## PRIOR-ART

**Swedish NegEx — Skeppstedt 2011 (the canonical Scandinavian base).** "Negation detection in Swedish clinical text: An adaption of NegEx to Swedish", J Biomed Semantics 2(Suppl 3):S3. Precision 75.2%, recall 81.9% on 558 sentences containing negation triggers; NPV 96.5% on 342 sentences without. Conclusion: trigger-phrase approach transfers to Swedish but precision drops vs English. **Trigger list is published and reusable** ([jbiomedsem.biomedcentral.com/articles/10.1186/2041-1480-2-S3-S3](https://jbiomedsem.biomedcentral.com/articles/10.1186/2041-1480-2-S3-S3), [pmc.ncbi.nlm.nih.gov/articles/PMC3194175/](https://pmc.ncbi.nlm.nih.gov/articles/PMC3194175/)). This is the direct linguistic donor for Norwegian.

**The abandoned Norwegian ConText/NegEx — found it.** Poster 14-2018, "Negation detection in Norwegian medical text: Porting a Swedish NegEx to Norwegian (Work in progress)", by **Hercules Dalianis, Kassaye Yitbarek Yigzaw, Alexandra Makhlysheva, Taridzo Chomutare — Norwegian Centre for E-health Research** ([ehealthresearch.no/en/posters/negation-detection-in-norwegian-medical-text-porting-a-swedish-negex-to-norwegian-work-in-progress](https://ehealthresearch.no/en/posters/negation-detection-in-norwegian-medical-text-porting-a-swedish-negex-to-norwegian-work-in-progress)). How far they got: translated the Swedish 40-rule set and extended it; reported counts ~15 POST, ~34 PREN, ~18 PSEUDO rules (27 newly added). Data: 170 gastro-surgery articles from *Tidsskriftet Den norske legeforening* (294,745 words), ICD-10 2017 (19,021 symptom/diagnosis terms); manually labeled sub-corpus 75,614 words (29 negations); detected 70 negated findings corpus-wide. Status: WIP, never productized/published as a tool — **the gap medspacy-no fills.** Note: they used *journal articles*, not real EHR text, and flagged tokenization problems — so their rule set is a starting lexicon, not a validated clinical resource.

**Danish.** DaCy is a general SpaCy-based Danish pipeline (NER/POS/dep), state-of-the-art for Danish but **no dedicated clinical-negation/ConText module** ([github.com/centre-for-humanities-computing/DaCy](https://github.com/centre-for-humanities-computing/DaCy), [arxiv.org/abs/2107.05295](https://arxiv.org/abs/2107.05295)). No reusable Danish clinical negation lexicon surfaced.

**Dutch (relevant as a medspacy precedent).** medspacy's `nl` ConText rules derive from peer-reviewed work — "Negation detection in Dutch clinical texts: an evaluation of rule-based and ML methods" ([arxiv.org/pdf/2209.00470](https://arxiv.org/pdf/2209.00470)). This is the template for "publish a language ConText module + eval".

**Norwegian negation lexicon availability.** There is **no clean, openly licensed Norwegian negation-trigger lexicon**. The only Norwegian-specific trigger set is the abandoned e-health poster's (not released as a file). NorMedTerm (below) gives medical *entities*, not modifiers. So the v0.1 trigger lexicon must be authored by the physician-builder, seeded from Skeppstedt's Swedish triggers + the poster's reported Norwegian rules + clinical knowledge.

## EVAL-DATA

**NorSynthClinical (ltgoslo).** "Data and system for family history extraction from a synthetic corpus of Norwegian clinical text"; authors Pål Brekke, Øystein Nytrø, Lilja Øvrelid; LOUHI@EMNLP 2018 ("Iterative development of family history annotation guidelines…"); BigMed-funded. Contents: ~477 sentences / ~6,030 tokens of synthetic clinical text (genetic-cardiology domain expert). **Annotation layers: entities + relations for family history only — NO negation, NO uncertainty annotation.** Files: `all_sentences.vert.entity`, `all_sentences.vert.parse.entity`, `synthetic_data.zip`. **No LICENSE file in repo** (license field empty) ([github.com/ltgoslo/NorSynthClinical](https://github.com/ltgoslo/NorSynthClinical), [aclanthology.org/W18-5600](https://aclanthology.org/W18-5600/)). It does carry family-history *relations*, so it is partially usable for the FAMILY ConText category but gives no negation/uncertainty gold.

**NorSynthClinical-PHI (synnobra).** Synthetic corpus extending NSC, built as a de-identification reference standard; author Synnøve Bråten (MSc Health Informatics). Nine PHI tags only: First_Name, Last_Name, Age, Health_Care_Unit, Phone_Number, Social_Security_Number, Date_Full, Date_Part, Location. Files: `reference_standard_annotated.conll`, `.txt`, `Annotation_guidelines.pdf`. **No LICENSE file.** **No negation/uncertainty layer** ([github.com/synnobra/NorSynthClinical-PHI](https://github.com/synnobra/NorSynthClinical-PHI)). Useful only as additional synthetic Norwegian clinical *substrate text*, not as ConText gold.

**NorMedTerm (ltgoslo).** 77,000+ Norwegian medical entities across 12 semantic categories (CONDITION, ANAT-LOC, PROCEDURE, SUBSTANCE, ABBREV, etc.), TSV with ICD codes; sources include Medisinsk ordbok, FEST, ALOC, NorSynthClinical; BigMed-funded ([github.com/ltgoslo/NorMedTerm](https://github.com/ltgoslo/NorMedTerm), paper [aclanthology.org/2020.multilingualbio-1.2.pdf](https://aclanthology.org/2020.multilingualbio-1.2.pdf)). **No LICENSE file.** This is the **target-concept dictionary** (the entities ConText modifies), not a negation resource — valuable as the medspacy `TargetMatcher` / QuickUMLS-equivalent layer.

**Other open Norwegian clinical-adjacent text.** *Tidsskriftet Den norske legeforening* articles (used by the e-health poster) are journal prose, not EHR. Helsenorge/NAV/Helfo public docs are administrative, not clinical-note style. **No de-identified real Norwegian EHR corpus is openly available.** All three open assets above lack ConText-relevant annotation.

**Conclusion — cheapest valid eval.** Since no open Norwegian corpus carries negation/uncertainty/historical labels, the correct and cheapest v0.1 eval is a **self-authored synthetic gold set by the physician-builder**: 300–500 sentences covering NEGATED_EXISTENCE, POSSIBLE_EXISTENCE (uncertainty), HYPOTHETICAL, HISTORICAL, FAMILY, each entity tagged with its ConText status. Reuse NorSynthClinical + NorSynthClinical-PHI sentences as realistic substrate (extends, doesn't reinvent), and use NorMedTerm to seed target entities. This mirrors exactly how the Swedish/Dutch evals were bootstrapped and is defensible for publication as a synthetic benchmark (note both NSC repos lack explicit licenses — for redistribution, email the LTG/UiO authors for permission or keep your derivative set under your own license with attribution).

## SPACY-NO

**Language code is `nb`** (Bokmål; clinical Norwegian is overwhelmingly Bokmål — no equivalent-quality Nynorsk pipeline). Models: `nb_core_news_sm/md/lg`, trained on UD Norwegian-Bokmaal + NorNE (news domain) ([spacy.io/models/nb](https://spacy.io/models/nb)).

**`nb_core_news_sm` v3.7.0 metrics** ([huggingface.co/spacy/nb_core_news_sm](https://huggingface.co/spacy/nb_core_news_sm)): token_acc 99.81%, POS 96.74%, **sentence segmentation P/R/F = 91.96 / 93.48 / 92.71**, dep UAS 88.41 / LAS 85.16, NER F 75.19. Pipeline: tok2vec → morphologizer → parser → trainable_lemmatizer → senter → ner → attribute_ruler.

**Clinical-text caveat.** Segmentation is parser/senter-based and trained on news; it degrades on telegraphic clinical notes, abbreviation-heavy text, list items, and missing terminal punctuation (cf. long-standing Norwegian segmentation issues, spaCy issue #4401 — [github.com/explosion/spaCy/issues/4401](https://github.com/explosion/spaCy/issues/4401)). For medspacy-no, **add medspacy's PyRuSH-based segmentation via `resources/nb/rush_rules.tsv` and a custom clinical tokenizer** handling Norwegian clinical abbreviations (f.eks., bl.a., tbl., susp., u.a., ø.h., kl., mg., evt.) rather than relying on the parser sentencizer. Use `nb_core_news_lg` for vectors if doing entity work; `sm` is fine for rule-based ConText.

## SECTION-DETECTION

**Norwegian structured admission journal (innkomstjournal) has a de-facto standard heading set** from the interregional standardization effort (Alme & Karlsen, "Ny strukturert innkomstjournal i norske sykehus", EHiN 2014; Tidsskriftet "Structured electronic health records" 2014 — [tidsskriftet.no/en/2014/02/structured-electronic-health-records](https://tidsskriftet.no/en/2014/02/structured-electronic-health-records)). Canonical headings (map each to a medspacy section category):

| Norwegian heading | medspacy category |
|---|---|
| Innkomstgrunn / Henvisningsårsak | chief_complaint / reason_for_examination |
| Tidligere sykdommer | past_medical_history |
| Familie / Sosialt, Hereditet | family_history / social_history |
| Aktuelt (aktuell anamnese) | history_of_present_illness |
| Naturlige funksjoner | (new: natural_functions) |
| Stimulantia | social_history |
| Allergier / Cave / Kritisk informasjon | allergies |
| Medikamenter (faste medisiner) | medications |
| Status presens / Funn | physical_exam |
| Vurdering | observation_and_plan |
| Tiltak / Plan | observation_and_plan / patient_instructions |
| Sammenfatning | (epicrisis summary) |

Student-facing concrete lists: [studmed.uio.no/journalwiki Innkomstjournal](https://studmed.uio.no/journalwiki/index.php/Innkomstjournal).

**Epikrise is legally and technically standardized.** Content duty under Helsepersonelloven §45a ([helsedirektoratet.no/rundskriv/helsepersonelloven-med-kommentarer/dokumentasjonsplikt/-45a.epikrise](https://www.helsedirektoratet.no/rundskriv/helsepersonelloven-med-kommentarer/dokumentasjonsplikt/-45a.epikrise)); message standard **Epikrise v1.2 / HIS 80226** ([helsedirektoratet.no/standarder/epikrise-v1.2](https://www.helsedirektoratet.no/standarder/epikrise-v1.2)). Epikrise sections mirror the admission journal plus diagnoser, behandling/forløp, and videre oppfølging/anbefaling. There is no single machine-readable national heading vocabulary — the v0.1 `section_patterns.json` should encode the heading list above as literals plus common casings/colons (`Aktuelt:`, `AKTUELT`, `Tidl. sykdommer`, `Medikamenter ved innkomst`).

## PUBLICATION

- **NoDaLiDa: biennial, odd years.** NoDaLiDa/Baltic-HLT 2025 was Tallinn, 2–5 March 2025 (paper deadline was 21 Oct 2024) ([nodalida-bhlt2025.eu/call-for-papers](https://www.nodalida-bhlt2025.eu/call-for-papers), [nealt-org.github.io/nodalida/](https://nealt-org.github.io/nodalida/)). **Next edition ≈ 2027 — too far for near-term.** Strongest *topical* fit (Nordic, low-resource) but timing-blocked.
- **Clinical NLP Workshop (ACL family) — best fit.** Clinical NLP 2026 deadline was 16 Feb 2026 (PASSED; workshop 16 May 2026) and explicitly added a **special track for "Clinical NLP in low-resource settings (languages other than English)"** ([aclweb.org/portal/content/8th-clinical-natural-language-processing-workshop](https://www.aclweb.org/portal/content/8th-clinical-natural-language-processing-workshop)). Target the **2027 edition** (annual; CFP typically Dec–Feb).
- **LOUHI (Health Text Mining).** ACL Anthology lists editions through 2022 (13th); no confirmed 2023–2026 edition in sources ([aclanthology.org/venues/louhi/](https://aclanthology.org/venues/louhi/)). Historically EMNLP-collocated — watch **EMNLP 2026, Budapest, 24–29 Oct 2026** workshop slate ([2026.emnlp.org/](https://2026.emnlp.org/)).
- **RANLP workshops:** RANLP is biennial odd years (next 2027); BioNLP-style workshops attach to it. Secondary option.
- **JOSS — recommended for the package itself.** Rolling submissions, no deadline; in scope for research software with scholarly significance; requires public clonable repo, OSI license, tests, docs, and a short `paper.md` ([joss.readthedocs.io/en/latest/submitting.html](https://joss.readthedocs.io/en/latest/submitting.html), [joss.readthedocs.io/en/latest/review_criteria.html](https://joss.readthedocs.io/en/latest/review_criteria.html)). Pre-trained ML models are out of scope, but a **rule-based ConText package is squarely in scope.** Pair JOSS (software) + a Clinical NLP workshop short paper (evaluation/linguistics).

## RISKS

- **No real Norwegian EHR eval data.** All open corpora are synthetic and lack negation/uncertainty gold. Mitigation: self-authored synthetic benchmark; be explicit in the paper that results are on synthetic text (same limitation accepted for NorSynthClinical and the Swedish/Dutch work).
- **License ambiguity.** NorSynthClinical, NorSynthClinical-PHI, and NorMedTerm all **lack a LICENSE file** (GitHub reports no license = all-rights-reserved by default). Redistributing derived eval sets needs author permission. Mitigation: email LTG/UiO (Øvrelid, Brekke) and Bråten; or build a fully independent synthetic set.
- **spaCy segmentation on clinical text.** News-trained senter mis-splits telegraphic notes; bad sentence boundaries silently break ConText scope. Mitigation: PyRuSH rules + Norwegian clinical abbreviation tokenizer; unit-test on note-style fragments.
- **Upstream code-naming.** medspacy resource dirs use ISO codes (`en`, `fr`); upstreaming Norwegian means `resources/nb/`. Verify the maintainers accept `nb` (vs `no`) before a PR — section categories like `natural_functions` are non-English-specific and may need an upstream discussion.
- **Trigger lexicon provenance.** The abandoned poster's rules aren't published as a file and were derived on journal articles, not notes — treat as seed, validate every trigger against clinical usage to avoid Swedish false-friends (e.g., Swedish "ej" vs Norwegian "ikke/ei").
- **Venue timing.** NoDaLiDa 2027 and Clinical NLP 2027 are the realistic paper windows; don't gate the software release on a conference — ship to PyPI + JOSS first.

## RECOMMENDED-V01

**Rule-file format (reuse medspacy's exactly — zero new schema):**
- `resources/nb/context_rules.json` — list of `{category, literal, pattern, direction}`. Categories: `NEGATED_EXISTENCE`, `POSSIBLE_EXISTENCE` (uncertainty), `HYPOTHETICAL`, `HISTORICAL`, `FAMILY`. Directions: `FORWARD`, `BACKWARD`, `TERMINATE`. Use `pattern: null` for plain phrases; spaCy token patterns for morphology (Norwegian negation often inflects/attaches: "ingen", "uten", "verken…eller", "afkreftet/avkreftet", "ikke tegn til", "fri for", "negativ for").
- `resources/nb/section_patterns.json` — `{literal, category}` for the innkomstjournal/epikrise headings table above (multiple casings + colon variants per heading).
- `resources/nb/rush_rules.tsv` — PyRuSH clinical sentence rules.

**Lexicon size target:** ~120–180 ConText rules for v0.1 — calibrated against medspacy `en` (~140 across 5 categories) and Skeppstedt Swedish (~40 negation triggers base). Breakdown target: ~60 NEGATED_EXISTENCE (pre + post), ~30 POSSIBLE_EXISTENCE/uncertainty, ~20 HYPOTHETICAL, ~15 HISTORICAL, ~25 FAMILY, ~15 TERMINATE. Seed from Skeppstedt's published Swedish triggers + the e-health poster's reported Norwegian rules, then hand-validate.

**Eval design:** physician-authored synthetic gold set, 300–500 sentences, ~split across the 5 categories + affirmed controls; substrate drawn from NorSynthClinical/-PHI sentences (extends existing work). Report per-category P/R/F vs the synthetic gold; include a small "affirmed-only" subset to measure false-negation rate (mirrors Skeppstedt's NPV-on-no-trigger design). Double-annotate ≥100 sentences for an IAA (κ) number — cheap and expected by reviewers.

**Distribution route — do both, in this order:**
1. **Standalone PyPI package `medspacy-no`** first: thin layer shipping `resources/nb/*` + a `load_nb()` helper that calls `medspacy.load(language_code="nb")` over `nb_core_news_lg`, plus the Norwegian clinical tokenizer/sectionizer. Fast to ship, you control versioning, no waiting on upstream review.
2. **Then upstream PR** adding `resources/nb/` to medspacy (low-friction: matches the established `language_code` pattern; maintainers actively merge such PRs — #293 added 7 languages this way). Coordinate the `nb` vs `no` dir naming and any new section categories with maintainers via an issue first.

**Paper/JOSS plan:**
- **JOSS submission** for the package as soon as it has tests + docs + an OSI license (MIT/Apache-2.0) — rolling, no deadline, in-scope for rule-based clinical NLP.
- **Clinical NLP Workshop 2027** (ACL family, low-resource track) for the evaluation+linguistics paper; NoDaLiDa 2027 as the Nordic-audience alternative. Both ~1 year out — ship software now, write the paper against the 2027 CFPs.