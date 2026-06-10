from __future__ import annotations

from pathlib import Path
from typing import Any

import spacy
from spacy.language import Language

from .tokenizer import create_norwegian_clinical_tokenizer
from .validation import (
    load_abbreviations,
    validate_abbreviations,
    validate_context_rules,
    validate_rush_rules,
    validate_section_rules,
)


DEFAULT_MODEL = "nb_core_news_lg"


def load_nb(
    model: str | Language = DEFAULT_MODEL,
    *,
    resource_dir: str | Path | None = None,
    enable_pyrush: bool = True,
    enable_sections: bool = True,
    replace_tokenizer: bool = True,
    replace_managed_components: bool = False,
    **model_kwargs: Any,
) -> Language:
    """Load a Norwegian Bokmal medspaCy pipeline.

    When ``model`` is an existing ``Language`` object, it is modified in
    place (tokenizer replaced, components added) and returned.

    Args:
        model: A spaCy model name or an existing ``Language`` object.
        resource_dir: Directory containing ``context_rules.json``,
            ``section_patterns.json``, ``rush_rules.tsv``, and
            ``abbreviations.txt``.
        enable_pyrush: Add the PyRuSH sentence splitter with Norwegian rules.
        enable_sections: Add the medspaCy sectionizer with Norwegian rules.
        replace_tokenizer: Replace the pipeline tokenizer with the Norwegian
            clinical tokenizer built from the resource abbreviations. Set to
            False to keep a custom tokenizer.
        replace_managed_components: Remove existing medspaCy components managed
            by this loader before adding Norwegian components. By default,
            existing managed components are treated as ambiguous stale config.
        **model_kwargs: Extra keyword arguments passed to ``spacy.load`` when
            ``model`` is a string.
    """

    nlp = _load_base_model(model, model_kwargs)
    resources = _resolve_resource_dir(resource_dir)
    _validate_resources(
        resources,
        enable_pyrush=enable_pyrush,
        enable_sections=enable_sections,
        replace_tokenizer=replace_tokenizer,
    )

    # Importing medspacy registers component factories with spaCy.
    import medspacy  # noqa: F401

    _prepare_managed_components(nlp, replace=replace_managed_components)

    if replace_tokenizer:
        nlp.tokenizer = create_norwegian_clinical_tokenizer(
            nlp,
            abbreviations=load_abbreviations(resources / "abbreviations.txt"),
        )

    if enable_pyrush:
        _add_pyrush(nlp, resources / "rush_rules.tsv")

    nlp.add_pipe("medspacy_target_matcher")

    nlp.add_pipe(
        "medspacy_context",
        config={
            "rules": str(resources / "context_rules.json"),
            "language_code": "nb",
        },
    )

    if enable_sections:
        nlp.add_pipe(
            "medspacy_sectionizer",
            config={
                "rules": str(resources / "section_patterns.json"),
                "language_code": "nb",
            },
        )

    return nlp


def _load_base_model(model: str | Language, model_kwargs: dict[str, Any]) -> Language:
    if isinstance(model, Language):
        if model_kwargs:
            raise ValueError("model_kwargs can only be used when model is a spaCy model name.")
        _validate_nb_language(model)
        return model

    try:
        nlp = spacy.load(model, **model_kwargs)
    except OSError as exc:
        if model == DEFAULT_MODEL:
            raise OSError(
                f"{exc}\nInstall the default Bokmal model with: "
                f"uv run python -m spacy download {DEFAULT_MODEL}"
            ) from exc
        raise
    _validate_nb_language(nlp)
    return nlp


def _validate_nb_language(nlp: Language) -> None:
    if nlp.lang != "nb":
        raise ValueError(f"load_nb expects a Norwegian Bokmal spaCy pipeline, got {nlp.lang!r}.")


def _resolve_resource_dir(resource_dir: str | Path | None) -> Path:
    if resource_dir is None:
        return Path(__file__).resolve().parent / "resources" / "nb"
    return Path(resource_dir)


def _validate_resources(
    resource_dir: Path,
    *,
    enable_pyrush: bool,
    enable_sections: bool,
    replace_tokenizer: bool,
) -> None:
    errors = validate_context_rules(resource_dir / "context_rules.json")
    if enable_sections:
        errors.extend(validate_section_rules(resource_dir / "section_patterns.json"))
    if enable_pyrush:
        errors.extend(validate_rush_rules(resource_dir / "rush_rules.tsv"))
    if replace_tokenizer:
        errors.extend(validate_abbreviations(resource_dir / "abbreviations.txt"))

    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Invalid medspacy-no resources in {resource_dir}:\n{joined}")


# Components this loader owns. A pre-existing copy of any of these is
# ambiguous stale config (possibly built with non-Norwegian rules), even when
# the corresponding enable_* flag is off.
MANAGED_COMPONENTS = (
    "medspacy_target_matcher",
    "medspacy_context",
    "medspacy_pyrush",
    "medspacy_sectionizer",
)


def _prepare_managed_components(nlp: Language, *, replace: bool) -> None:
    existing = [name for name in MANAGED_COMPONENTS if name in nlp.pipe_names]
    if not existing:
        return

    if not replace:
        joined = ", ".join(existing)
        raise ValueError(
            f"Existing managed medspaCy component(s) found: {joined}. "
            "Pass replace_managed_components=True to rebuild them with Norwegian resources."
        )

    for name in existing:
        nlp.remove_pipe(name)


def _add_pyrush(nlp: Language, rules_path: Path) -> None:
    config = {"rules_path": str(rules_path)}
    if "parser" in nlp.pipe_names:
        nlp.add_pipe("medspacy_pyrush", before="parser", config=config)
    elif "senter" in nlp.pipe_names:
        nlp.add_pipe("medspacy_pyrush", before="senter", config=config)
    else:
        nlp.add_pipe("medspacy_pyrush", first=True, config=config)
