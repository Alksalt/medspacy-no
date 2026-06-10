from __future__ import annotations

import re
import string

from spacy.language import Language
from spacy.symbols import ORTH
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex


CLINICAL_ABBREVIATIONS = (
    "bl.a.",
    "ca.",
    "dvs.",
    "evt.",
    "f.eks.",
    "i.a.b.",
    "jf.",
    "kl.",
    "mtp.",
    "pga.",
    "susp.",
    "tbl.",
    "u.a.",
    "ø.h.",
)


def create_norwegian_clinical_tokenizer(nlp: Language) -> Tokenizer:
    """Create a tokenizer tuned for Norwegian clinical-note abbreviations."""

    tokenizer_exceptions = nlp.Defaults.tokenizer_exceptions.copy()
    for abbreviation in CLINICAL_ABBREVIATIONS:
        tokenizer_exceptions[abbreviation] = [{ORTH: abbreviation}]

    punctuation_chars = string.punctuation.replace(".", "")
    infixes = tuple(nlp.Defaults.infixes) + (rf"[{re.escape(punctuation_chars)}]",)

    prefix_re = compile_prefix_regex(nlp.Defaults.prefixes)
    suffix_re = compile_suffix_regex(nlp.Defaults.suffixes)
    infix_re = compile_infix_regex(infixes)

    return Tokenizer(
        nlp.vocab,
        rules=tokenizer_exceptions,
        prefix_search=prefix_re.search,
        suffix_search=suffix_re.search,
        infix_finditer=infix_re.finditer,
        token_match=nlp.tokenizer.token_match,
    )
