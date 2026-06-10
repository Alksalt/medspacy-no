from __future__ import annotations

from pathlib import Path
from typing import Any

import spacy
from spacy.language import Language

from .tokenizer import create_norwegian_clinical_tokenizer
from .validation import validate_context_rules, validate_rush_rules, validate_section_rules


DEFAULT_MODEL = "nb_core_news_lg"


def load_nb(
    model: str | Language = DEFAULT_MODEL,
    *,
    resource_dir: str | Path | None = None,
    enable_pyrush: bool = True,
    enable_sections: bool = True,
    **model_kwargs: Any,
) -> Language:
    """Load a Norwegian Bokmal medspaCy pipeline.

    Args:
        model: A spaCy model name or an existing ``Language`` object.
        resource_dir: Directory containing ``context_rules.json``,
            ``section_patterns.json``, and ``rush_rules.tsv``.
        enable_pyrush: Add the PyRuSH sentence splitter with Norwegian rules.
        enable_sections: Add the medspaCy sectionizer with Norwegian rules.
        **model_kwargs: Extra keyword arguments passed to ``spacy.load`` when
            ``model`` is a string.
    """

    nlp = _load_base_model(model, model_kwargs)
    resources = _resolve_resource_dir(resource_dir)
    _validate_resources(resources, enable_pyrush=enable_pyrush, enable_sections=enable_sections)

    # Importing medspacy registers component factories with spaCy.
    import medspacy  # noqa: F401

    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)

    if enable_pyrush and "medspacy_pyrush" not in nlp.pipe_names:
        nlp.add_pipe(
            "medspacy_pyrush",
            config={"rules_path": str(resources / "rush_rules.tsv")},
        )

    if "medspacy_target_matcher" not in nlp.pipe_names:
        nlp.add_pipe("medspacy_target_matcher")

    if "medspacy_context" not in nlp.pipe_names:
        nlp.add_pipe(
            "medspacy_context",
            config={
                "rules": str(resources / "context_rules.json"),
                "language_code": "nb",
            },
        )

    if enable_sections and "medspacy_sectionizer" not in nlp.pipe_names:
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
        if model.lang != "nb":
            raise ValueError(f"load_nb expects a Norwegian Bokmal spaCy pipeline, got {model.lang!r}.")
        return model

    try:
        return spacy.load(model, **model_kwargs)
    except OSError as exc:
        if model == DEFAULT_MODEL:
            raise OSError(
                f"{exc}\nInstall the default Bokmal model with: "
                f"uv run python -m spacy download {DEFAULT_MODEL}"
            ) from exc
        raise


def _resolve_resource_dir(resource_dir: str | Path | None) -> Path:
    if resource_dir is None:
        return Path(__file__).resolve().parent / "resources" / "nb"
    return Path(resource_dir)


def _validate_resources(
    resource_dir: Path,
    *,
    enable_pyrush: bool,
    enable_sections: bool,
) -> None:
    errors = validate_context_rules(resource_dir / "context_rules.json")
    if enable_sections:
        errors.extend(validate_section_rules(resource_dir / "section_patterns.json"))
    if enable_pyrush:
        errors.extend(validate_rush_rules(resource_dir / "rush_rules.tsv"))

    if errors:
        joined = "\n".join(f"- {error}" for error in errors)
        raise ValueError(f"Invalid medspacy-no resources in {resource_dir}:\n{joined}")
