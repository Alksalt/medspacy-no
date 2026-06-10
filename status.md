# status — medspacy-no

## current state (2026-06-10)

Infrastructure-first package scaffold implemented. Research complete. This is the recommended first ship of the ehelse portfolio — days of work, not weeks.

All research artifacts are in place (2026-06-10):
- `docs/RESEARCH.md` — implementation dossier.
- `docs/SEEDS.md` — DELIVERED: the verbatim 42-trigger Swedish lexicon (fetched from Skeppstedt's published triggers.txt), the 2018 Tromsø poster details (no reusable lexicon published — rule counts only; contact andrius.budrionis@ehealthresearch.no), a full Swedish→Norwegian candidate table with false friends flagged for owner review, and 6 abbreviation sources. **Builder starts here.**
- `docs/PERMISSION-EMAIL.md` — DELIVERED: ready bokmål email. Recipients resolved: Øvrelid (liljao@ifi.uio.no) for NorSynthClinical; Bråten + CC Dalianis (hercules@dsv.su.se) for the PHI corpus. Brekke has no verified public email — skip.

**Naming question RESOLVED: use `nb`.** medspacy passes language_code to spaCy, and spaCy ships Norwegian only as Bokmål `nb` (`nb_core_news_*`) — `no` would fail to instantiate a pipeline. The upstream issue is now a courtesy heads-up, not an open question.

Nothing is blocked in code infrastructure. The production trigger lexicon, production section headings, production PyRuSH rules, and gold set require the owner's clinical-language judgment.

Implemented infrastructure (2026-06-10):
- `pyproject.toml`, MIT `LICENSE`, `uv.lock`, and `.gitignore`.
- `src/medspacy_no/` with `load_nb()`, Norwegian clinical tokenizer, resource validation helpers, and bundled `resources/nb/`.
- Root `resources/nb/` synchronized with packaged resources.
- `tests/` covering loader smoke behavior, tokenizer abbreviations, medspaCy wrapper schemas, resource sync, and package artifact inclusion.
- `scripts/validate_resources.py` and `scripts/check_owner_review.py` for explicit resource/review validation.
- `scripts/check_release_ready.py` for the intentionally failing release gate while fixtures remain.
- GitHub Actions CI scaffold in `.github/workflows/ci.yml`.
- Owner review packet: `docs/P1_OWNER_REVIEW.md` and `data/owner_review/context_rule_candidates.tsv`.
- Current resources are non-production smoke fixtures. The production rule-count test is marked xfail until owner-reviewed P1 resources replace them.

## build sequence

| step | depends on | status |
|---|---|---|
| receive docs/SEEDS.md + docs/PERMISSION-EMAIL.md | research agent | done |
| author resources/nb/context_rules.json (~150 rules) | SEEDS.md + owner | not started |
| owner-review context-rule candidates worksheet | SEEDS.md | ready for owner |
| author resources/nb/section_patterns.json | dossier heading table | not started |
| draft resources/nb/rush_rules.tsv | dossier + abbreviation sources | not started |
| implement src/medspacy_no/ + load_nb() | infrastructure fixtures | done |
| write tests/ suite | implementation | done |
| send permission email to LTG/UiO | PERMISSION-EMAIL.md | not started |
| author 300–500-sentence synthetic gold set | owner; NorSynthClinical substrate | not started |
| double-annotate ≥100 sentences (kappa) | gold set + colleague | not started |
| compute per-category P/R/F on gold set | tests + gold set | not started |
| publish to PyPI | package + tests | not started |
| submit to JOSS | PyPI + paper.md + production resources + public-history/eval evidence | not started |
| open nb-vs-no naming issue on medspacy | PyPI live | not started |
| upstream PR to medspacy resources/nb/ | naming issue resolved | not started |

## dated next actions

- **2026-06-10** — infrastructure-first scaffold implemented and tests added
- **2026-06-10** — git/CI/review packet prepared; all context-rule candidates remain `pending`
- **2026-06-10** — full-repo review (`findings.md`) and all fixes landed: `uv run pytest` gate repaired, tokenizer no longer splits clinical numerics (letter-bounded hyphen infix only), abbreviations moved to `resources/nb/abbreviations.txt` (owner-review gated), stale managed components always rejected, release thresholds single-sourced in `medspacy_no.validation`, release gate hardened (no crashes; checks Private classifier + paper.md). GitHub remote creation still pending owner go-ahead.
- **next** — owner reviews `data/owner_review/context_rule_candidates.tsv`, then begins authoring `context_rules.json`
- **next** — send permission email while lexicon authoring is in progress (parallel)
- **next** — keep release gate failing until owner-reviewed P1 resources replace smoke fixtures
