from __future__ import annotations

from pathlib import Path

import pytest
import spacy

from medspacy_no import load_nb


ROOT = Path(__file__).resolve().parents[1]
ROOT_RESOURCES = ROOT / "resources" / "nb"


def test_load_nb_accepts_existing_nb_language_with_explicit_resources() -> None:
    base = spacy.blank("nb")

    nlp = load_nb(
        base,
        resource_dir=ROOT_RESOURCES,
        enable_pyrush=False,
        enable_sections=True,
    )

    assert nlp.lang == "nb"
    assert "medspacy_target_matcher" in nlp.pipe_names
    assert "medspacy_context" in nlp.pipe_names
    assert "medspacy_sectionizer" in nlp.pipe_names


def test_load_nb_uses_bundled_resources_by_default_with_existing_language() -> None:
    nlp = load_nb(spacy.blank("nb"), enable_pyrush=False)

    assert "medspacy_context" in nlp.pipe_names


def test_load_nb_can_enable_pyrush_with_bundled_rules() -> None:
    nlp = load_nb(spacy.blank("nb"), enable_pyrush=True, enable_sections=False)

    assert "medspacy_pyrush" in nlp.pipe_names
    assert list(nlp("Dette er en setning. Dette er en til.").sents)


def test_load_nb_missing_default_model_message(monkeypatch: pytest.MonkeyPatch) -> None:
    def missing_model(*args: object, **kwargs: object) -> object:
        raise OSError("[E050] Can't find model 'nb_core_news_lg'.")

    monkeypatch.setattr(spacy, "load", missing_model)

    with pytest.raises(OSError, match="uv run python -m spacy download nb_core_news_lg"):
        load_nb()


def test_load_nb_rejects_non_nb_model_loaded_from_name(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(spacy, "load", lambda *args, **kwargs: spacy.blank("en"))

    with pytest.raises(ValueError, match="Norwegian Bokmal"):
        load_nb("en_core_web_sm")


def test_load_nb_places_pyrush_before_parser_when_parser_exists() -> None:
    base = spacy.blank("nb")
    base.add_pipe("parser")

    nlp = load_nb(base, resource_dir=ROOT_RESOURCES, enable_pyrush=True, enable_sections=False)

    assert nlp.pipe_names.index("medspacy_pyrush") < nlp.pipe_names.index("parser")


def test_load_nb_rejects_existing_managed_medspacy_component() -> None:
    base = spacy.blank("nb")
    base.add_pipe("sentencizer", name="medspacy_context")

    with pytest.raises(ValueError, match="medspacy_context"):
        load_nb(base, resource_dir=ROOT_RESOURCES, enable_pyrush=False, enable_sections=False)


def test_load_nb_rejects_existing_managed_component_even_when_disabled() -> None:
    base = spacy.blank("nb")
    base.add_pipe("sentencizer", name="medspacy_pyrush")

    with pytest.raises(ValueError, match="medspacy_pyrush"):
        load_nb(base, resource_dir=ROOT_RESOURCES, enable_pyrush=False, enable_sections=False)


def test_load_nb_replace_managed_components_rebuilds_pipeline() -> None:
    base = spacy.blank("nb")
    base.add_pipe("sentencizer", name="medspacy_context")
    base.add_pipe("sentencizer", name="medspacy_pyrush")

    nlp = load_nb(
        base,
        resource_dir=ROOT_RESOURCES,
        enable_pyrush=False,
        enable_sections=False,
        replace_managed_components=True,
    )

    assert nlp.pipe_names.count("medspacy_context") == 1
    assert "medspacy_pyrush" not in nlp.pipe_names


def test_load_nb_keeps_custom_tokenizer_when_replace_tokenizer_is_false() -> None:
    base = spacy.blank("nb")
    original_tokenizer = base.tokenizer

    nlp = load_nb(
        base,
        resource_dir=ROOT_RESOURCES,
        enable_pyrush=False,
        enable_sections=False,
        replace_tokenizer=False,
    )

    assert nlp.tokenizer is original_tokenizer
