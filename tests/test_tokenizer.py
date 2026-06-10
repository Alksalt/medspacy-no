from __future__ import annotations

import spacy

from medspacy_no.tokenizer import create_norwegian_clinical_tokenizer


def test_period_bearing_clinical_abbreviations_remain_single_tokens() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)
    text = "u.a. i.a.b. f.eks. bl.a. tbl. susp. ø.h. kl. evt."

    tokens = [token.text for token in nlp(text)]

    for abbreviation in text.split():
        assert abbreviation in tokens


def test_hyphenated_ikke_prefix_is_tokenized_for_context_matching() -> None:
    nlp = spacy.blank("nb")
    nlp.tokenizer = create_norwegian_clinical_tokenizer(nlp)

    tokens = [token.text for token in nlp("ikke-operable metastaser")]

    assert tokens == ["ikke", "-", "operable", "metastaser"]
