# medspacy-no — decisions

Imperatives only. Carry into every session.

- Reuse medspacy's exact rule formats for context_rules.json ({category, literal, pattern, direction}) and section_patterns.json ({literal, category}) — zero new schema.
- Ship PyPI package medspacy-no standalone first; open the upstream PR to medspacy only after PyPI is live.
- Open the nb-vs-no naming issue upstream before submitting the PR — do not assume `nb` is accepted.
- Never redistribute NorSynthClinical, NorSynthClinical-PHI, or NorMedTerm derivatives without written permission from the authors (Øvrelid, Brekke, Bråten) — those repos have no LICENSE file and are all-rights-reserved by default. The own synthetic gold set stands alone if permission lags.
- State the synthetic-eval limitation plainly in any paper. No hedging, no minimizing.
- OSI license only — MIT or Apache-2.0.
- Do not gate the software release on a conference acceptance. JOSS is rolling; submit as soon as tests + docs + paper.md are ready.
- Clinical NLP Workshop 2027 and NoDaLiDa 2027 are the targets for the eval/linguistics paper.
- Trigger-lexicon authoring, gold-set authoring, and false-friend validation are owner-only clinical-language steps — no agent substitution.
- Never Haiku.
- Use `uv` for all Python tooling — never bare pip, pip3, python, or python3.
- Never hardcode values (model names, paths, rule counts) — pass as parameters with documented defaults.
