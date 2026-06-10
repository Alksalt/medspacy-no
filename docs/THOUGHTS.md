# docs/THOUGHTS.md — open questions and design tensions

Working notes. These are not resolved decisions — they are tensions to watch and answer as the build progresses.

## nb vs no directory naming upstream

medspacy resource directories use ISO 639-1 codes. Norwegian Bokmål is `nb`; generic Norwegian is `no`. The correct code for this module is `nb` (spaCy's model is `nb_core_news_lg`; clinical Norwegian is Bokmål). However, the medspacy maintainers may have a different preference — upstream dirs like `de`, `fr`, `es` are top-level ISO 639-1 and some (like `nl`) are language codes rather than locale codes. Open an issue before the PR and do not commit to a directory name until confirmed. The PyPI standalone package can use `nb` internally without upstream coordination.

## natural_functions section category

"Naturlige funksjoner" (bowel habits, urination, sleep, appetite) is a standard innkomstjournal heading with no English equivalent in medspacy's category list. Options: (a) fold into `physical_exam` — wrong semantically; (b) fold into `observation_and_plan` — wrong; (c) introduce `natural_functions` as a new category in the upstream PR. Option (c) is correct but requires the maintainers to accept a non-English-named category. For the standalone PyPI package, define it locally. For the upstream PR, open the discussion first. Track whether the maintainers want to generalize to a `bodily_functions` category.

## news-trained senter degrades on telegraphic clinical notes

`nb_core_news_sm/lg` achieves F 92.7 sentence segmentation on news text. On telegraphic sykehjem/sykehus notes (missing terminal punctuation, abbreviation-heavy, list-style entries, colon-separated sections) this will drop substantially. Bad sentence boundaries silently break ConText scope windows — a trigger in sentence A modifies entity in sentence B when the senter fails to split them, or vice versa. Mitigation:
- Ship `rush_rules.tsv` with PyRuSH clinical rules.
- Custom tokenizer that does not split on known clinical abbreviation periods.
- Unit-test on note-style fragments, not news. Write at least 20 test sentences that expose the degradation.
- Open question: how much does the PyRuSH layer recover? Needs empirical measurement on the gold set.

## Swedish false-friend validation per trigger

The 2018 Tromsø poster translated Skeppstedt's Swedish rules to Norwegian. Swedish and Norwegian Bokmål are close but not identical — false friends exist at the clinical modifier level. Example: Swedish "ej" (not) has no direct Norwegian equivalent — Norwegian uses "ikke" or "ei" (dialects). Swedish "icke" is archaic Norwegian. Validate every Skeppstedt-origin trigger against actual clinical Norwegian usage before committing. This is the owner's job (daily clinical Norwegian in sykehjem documentation) and cannot be delegated to a rule-port script.

## poster rules derived from journal articles, not EHR text

The 2018 e-health poster (Dalianis et al.) tested on Tidsskriftet Den norske legeforening articles — formal medical prose, not clinical notes. EHR text is telegraphic, elliptical, abbreviation-heavy, and morphologically messier. The poster's rule set is a starting seed, not a validated clinical resource. Expect lower precision on real notes and test the gold set explicitly on note-style fragments, not article-style prose.

## colleague recruitment for kappa

Double-annotating ≥100 sentences requires a clinical colleague willing to spend ~2 hours on annotation. Who? Options: (a) a colleague at the sykehjem; (b) a clinical informatics contact at NTNU/St.Olavs; (c) a Norwegian medical student. The kappa number matters for peer review — a high κ (≥0.80) validates the annotation scheme. Recruit before the gold set is finished so the annotation session can happen immediately after authoring. This also opens a co-author slot on the eval paper, which is good for recruitment.

## permission timeline risk

NorSynthClinical and NorSynthClinical-PHI have no LICENSE files. Building the eval substrate on them requires permission from Øvrelid/Brekke (NorSynthClinical) and Bråten (NorSynthClinical-PHI). If permission lags, the gold set must be fully independently authored. Start the permission email process immediately and write the gold set in parallel — independent authorship is safer and faster anyway. The own gold set is a stronger contribution than a derivative.

## JOSS timeline vs software quality bar

JOSS reviewers look for: working code, passing tests, documentation, an OSI license, and a statement of need. They do not require publication-quality eval results — the peer-reviewed evaluation paper is separate. This means JOSS can be submitted before the gold set kappa is finalized, as long as basic tests (section detection, known-trigger unit tests) pass. Consider a two-stage release: PyPI + JOSS paper first, eval paper second.
