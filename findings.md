# findings.md — full-repo review of medspacy-no (2026-06-10)

**Resolution status (2026-06-10, same day):** all findings fixed and verified — `uv run pytest` now passes (28 passed, 1 xfailed), clinical numerics tokenize correctly, release gate covers abbreviations/classifier/paper.md. One exception: the L6 sub-item "create/push the public GitHub remote" is intentionally left for the owner (outward-facing action); local history is committed in bisectable chunks.

Scope: every tracked file (src, tests, scripts, resources, CI, pyproject, docs). All behavioral claims verified by running code against the project venv (medspacy 1.3.1, spacy 3.8.14). Review only — nothing fixed.

Verified working: all medspacy factory config keys used by the loader (`rules`, `language_code`, `rules_path`) match medspacy 1.3.1 signatures; `ConTextRule.from_json` / `SectionRule.from_json` paths are correct; `replace_managed_components=True` works; the three scripts run with correct exit codes; CI-style `uv run python -m pytest` passes 20 + 1 xfail; outward-text constraints hold (README/PERMISSION-EMAIL use "utdannet lege (master i medisin)", no first-mover claims, no non-commercial framing); resource sync, packaging test, and owner-review TSV are internally consistent.

---

## HIGH

### H1 — The declared quality gate `uv run pytest` fails at collection

`tests/test_owner_review.py:5` does `from scripts.check_owner_review import ...`. `scripts/` has no `__init__.py` and is not on `pythonpath` (`pyproject.toml:70` lists only `"src"`). It only resolves when CWD is on `sys.path`, i.e. `python -m pytest` from repo root. Result, reproduced:

- `uv run pytest` → `ModuleNotFoundError: No module named 'scripts'`, collection error, exit 2.
- `uv run python -m pytest` → 20 passed, 1 xfailed.

The broken invocation is the one specified everywhere that matters: ship profile `quality_gates` in both `CLAUDE.md` files, `AGENTS.md:88` JOSS checklist, `docs/PLAN.md:115`. CI passes only because `ci.yml:32` happens to use the `-m` form.

Fix: add `"."` to `[tool.pytest.ini_options] pythonpath` in `pyproject.toml` (paths are rootdir-relative), so both invocations work. Then align README/CONTRIBUTING dev commands. Longer-term: move `validate_owner_review` into `medspacy_no/validation.py` and make `scripts/check_owner_review.py` a thin wrapper, so tests import package code instead of a script.

### H2 — Clinical tokenizer splits decimal commas, times, and BP ratios

`tokenizer.py:47-48` adds every punctuation char except `.` as an infix between *any* two characters. Reproduced against `spacy.blank("nb")`:

| input | default nb tokenizer | medspacy-no tokenizer |
|---|---|---|
| `37,5` | `37,5` | `37`, `,`, `5` |
| `08:30` | `08:30` | `08`, `:`, `30` |
| `120/80.` | `120/80.` | `120`, `/`, `80.` |
| `2-3` | `2-3` | `2`, `-`, `3` |

Norwegian vitals are written with decimal commas; temps, BP, doses, and times are everywhere in clinical notes. Shredding them changes token distances inside ConText scope windows and corrupts any downstream numeric extraction. The motivating case was only hyphen-splitting so the `ikke-` prefix trigger can match (`ikke-operable` → `ikke`, `-`, `operable` — poster-flagged hazard, covered by `tests/test_tokenizer.py:30`).

Fix: replace the blanket infix with a letter-bounded hyphen split, e.g. `r"(?<=[A-Za-zÆØÅæøå])-(?=[A-Za-zÆØÅæøå])"`, and add only specific extra chars if a concrete trigger needs them. Add regression tests asserting `37,5`, `08:30`, `120/80`, and `2-3` stay single tokens while `ikke-operable` still splits.

---

## MEDIUM

### M1 — `load_nb` silently keeps stale managed components when a feature flag is off

`_loader.py:136-140`: `managed` includes `medspacy_pyrush`/`medspacy_sectionizer` only when the corresponding `enable_*` is True. Reproduced: a pipeline that already contains `medspacy_pyrush` (e.g. configured with English rules) passes through `load_nb(..., enable_pyrush=False)` with no error and the stale component retained. This contradicts the docstring (`_loader.py:33-35`): "existing managed components are treated as ambiguous stale config."

Fix: build `managed` from all four component names unconditionally; keep `enable_*` controlling only what gets re-added. Add a test for the disabled-but-present case.

### M2 — Tokenizer replacement loses model tokenizer fidelity and has no opt-out

`tokenizer.py:43-61` builds the new tokenizer from class-level `nlp.Defaults` but takes `token_match` from the live `nlp.tokenizer`, and omits `url_match` entirely (the default nb tokenizer has one — verified non-None). Consequences: URL tokenization changes; any tokenizer customization serialized with a loaded model or applied by the caller is discarded; `load_nb` mutates a caller-supplied `Language` in place with no flag to skip tokenizer replacement and no docstring warning.

Fix: pass `url_match=nlp.tokenizer.url_match` and source exceptions from the live tokenizer where available; add `replace_tokenizer: bool = True` to `load_nb`; state the in-place mutation in the `load_nb` docstring.

### M3 — Clinical abbreviation list is unreviewed clinical content hardcoded in code

`CLINICAL_ABBREVIATIONS` (`tokenizer.py:12-37`) is clinical-language content (same character as the PyRuSH rules the scaffold deliberately fixtures) but ships un-marked: no `fixture`/`owner_reviewed` metadata, not covered by `check_release_ready.py`, not in the owner-review workflow. It also diverges from the seed list in `docs/PLAN.md:80` (missing `ift.`, `ivf.`, `prof.`, `st.`, `avd.`, `ml.`, `dl.`, and others). DECISIONS.md bans hardcoded values; `create_norwegian_clinical_tokenizer` takes no abbreviations parameter.

Fix: move the list to `resources/nb/abbreviations.txt` (synced, packaged, owner-review metadata in a header comment), accept `abbreviations: Iterable[str] | None = None` with the bundled file as documented default, and add an abbreviation-file check to `check_release_ready.py` + the owner-review packet.

### M4 — Release-count thresholds are duplicated and already drifting

Two independent hardcodings of the P1 rule-count gate: `tests/test_resources.py:82-87` (5 categories, no TERMINATE) vs `scripts/check_release_ready.py:13-21` (6 categories incl. `TERMINATE >= 15`, plus `MIN_SECTION_RULES = 40`). They already disagree. DECISIONS.md: "Never hardcode values (... rule counts) — pass as parameters with documented defaults."

Fix: define thresholds once (constants in `medspacy_no/validation.py`, or a small `release_thresholds.json`), import from both the test and the script, and make `check_release_ready()` accept them as parameters with those defaults.

### M5 — `check_release_ready.py` crashes instead of reporting on missing/invalid files

`_check_rush_rules` (`scripts/check_release_ready.py:80`) calls `path.read_text()` and `_read_json` (`:127`) calls `json.loads` with no existence/parse guards. A missing or malformed resource file produces a traceback (exit 1 by accident) rather than an error line, unlike `validation.py`, which guards both cases. `tests/test_release_ready.py:21-23` would mask this as "passing" since it only greps stderr.

Fix: guard for existence and JSON errors, returning error strings like `validation.py` does.

---

## LOW

### L1 — Doc drift (four instances)

- `CLAUDE.md:37` workspace map lists `paper.md` ("JOSS paper") — the file does not exist anywhere in the repo.
- `docs/PLAN.md:89` specifies `spacy[nb]>=3.7` — no `nb` extra exists in spaCy; `pyproject.toml:40` is correct.
- `docs/PLAN.md:26` says direction is one of `FORWARD`, `BACKWARD`, `TERMINATE`, but the validator and medspacy also accept `BIDIRECTIONAL`/`PSEUDO`, and the owner-review TSV already uses both.
- `README.md:17` "medspacy ≥1.3" vs `pyproject.toml:39` `>=1.3.1`.

Fix: remove or stub `paper.md` in the map; correct PLAN.md's dependency line and direction list; align the README version floor.

### L2 — Validator is stricter than the medspacy schema it claims to mirror

medspacy's `ConTextRule.from_dict` treats `pattern` and `direction` as optional (`direction` defaults to `BIDIRECTIONAL`) and allows `allowed_types`/`excluded_types`/`max_scope`/`max_targets`/`metadata`. `validation.py:22` requires `pattern` and `direction` on every rule and `validation.py:34` rejects any top-level key besides `context_rules`. A file medspacy loads fine can fail this validator. The strictness is defensible as a project profile but is undocumented and sits next to "zero new schema" in DECISIONS.md.

Fix: add a module docstring to `validation.py` stating the project profile is intentionally stricter than medspacy (all four keys explicit, single wrapper key) and why.

### L3 — setuptools only present transitively, but the build depends on it

`python -m build --no-isolation` (CI `ci.yml:34`, `tests/test_packaging.py:17`) needs setuptools in the venv; build-system requires `setuptools>=77.0.3` (`pyproject.toml:2`). Nothing in the dev group declares it — it arrives transitively via `pyrush` (unconditional) and `spacy`. If either drops the dep, the build and test break.

Fix: add `setuptools>=77.0.3` to `[dependency-groups].dev`.

### L4 — Dev dependencies declared twice

`[project.optional-dependencies].dev` (`pyproject.toml:43-48`) duplicates `[dependency-groups].dev` (`:50-55`). Two lists to keep in sync.

Fix: keep only `[dependency-groups].dev` (uv-native; CI uses `uv sync --dev`).

### L5 — Release gate misses packaging-level blockers

`check_release_ready.py` validates resources only. It does not check removal of the `"Private :: Do Not Upload"` classifier (`pyproject.toml:28`) or the existence of `paper.md`, both of which are stated release/JOSS gates.

Fix: add both checks to `check_release_ready()`.

### L6 — No remote, one commit, large uncommitted working set

`git remote -v` is empty; history is a single commit (`1e3900a`) with 20 modified + 6 untracked files on top of it. JOSS screening explicitly requires public development history over time, and the workspace practice is bisectable per-phase commits.

Fix: commit the current state in logical chunks (CI, loader/tokenizer, validation/scripts, docs) and create/push `github.com/Alksalt/medspacy-no` when ready to start the public-history clock.

### L7 — No test covers `replace_managed_components=True`

`tests/test_loader.py:70-75` covers only the rejection path. The replace path works (verified manually) but is untested.

Fix: add a test that pre-adds a managed component and asserts `replace_managed_components=True` rebuilds the pipeline.
