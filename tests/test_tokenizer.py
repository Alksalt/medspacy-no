from __future__ import annotations

import spacy

from medspacy_no.tokenizer import create_norwegian_clinical_tokenizer


def test_period_bearing_clinical_abbreviations_remain_single_tokens() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)
    text = "u.a. i.a.b. f.eks. bl.a. tbl. susp. ø.h. kl. evt. mg. obs. i.v. i.m. s.c. p.o. bl.tr. temp."

    tokens = [token.text for token in nlp(text)]

    for abbreviation in text.split():
        assert abbreviation in tokens


def test_clinical_abbreviation_titlecase_variants_remain_single_tokens() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)
    text = "Tbl. Ø.h. Obs. Temp."

    tokens = [token.text for token in nlp(text)]

    for abbreviation in text.split():
        assert abbreviation in tokens


def test_hyphenated_ikke_prefix_is_tokenized_for_context_matching() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)

    tokens = [token.text for token in nlp("ikke-operable metastaser")]

    assert tokens == ["ikke", "-", "operable", "metastaser"]


def test_clinical_numerics_stay_single_tokens() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)

    tokens = [token.text for token in nlp("Temp 37,5 kl. 08:30 BT 120/80 og 2-3 anfall")]

    for numeric in ("37,5", "08:30", "120/80", "2-3"):
        assert numeric in tokens


def test_url_tokenization_matches_default_tokenizer() -> None:
    text = "Se https://www.felleskatalogen.no/medisin for dosering."
    default_nlp = spacy.blank("nb")
    default_tokens = [token.text for token in default_nlp(text)]

    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)
    clinical_tokens = [token.text for token in nlp(text)]

    assert clinical_tokens == default_tokens


def test_custom_abbreviations_parameter_overrides_bundled_list() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp, abbreviations=("pas.",))

    tokens = [token.text for token in nlp("pas. mottatt u.a. i dag")]

    assert "pas." in tokens
    assert "u.a." not in tokens
