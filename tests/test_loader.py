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
