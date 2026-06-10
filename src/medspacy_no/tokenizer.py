from __future__ import annotations

from pathlib import Path
from typing import Iterable

from spacy.lang.char_classes import ALPHA
from spacy.language import Language
from spacy.symbols import ORTH
from spacy.tokenizer import Tokenizer
from spacy.util import compile_infix_regex, compile_prefix_regex, compile_suffix_regex

from .validation import load_abbreviations


DEFAULT_ABBREVIATIONS_PATH = Path(__file__).resolve().parent / "resources" / "nb" / "abbreviations.txt"

# Split hyphens between letters only ("ikke-operable" -> "ikke", "-",
# "operable") so the "ikke-" prefix trigger can match. Punctuation between
# digits is left alone: clinical numerics like "37,5", "08:30", and "120/80"
# must stay single tokens.
LETTER_HYPHEN_INFIX = rf"(?<=[{ALPHA}])-(?=[{ALPHA}])"


def create_norwegian_clinical_tokenizer(
    nlp: Language,
    abbreviations: Iterable[str] | None = None,
) -> Tokenizer:
    """Create a tokenizer tuned for Norwegian clinical-note abbreviations.

    Args:
        nlp: The pipeline whose tokenizer settings are used as the base.
            Exception rules, ``token_match``, and ``url_match`` are taken from
            the live ``nlp.tokenizer`` when available (falling back to
            ``nlp.Defaults``); infixes are rebuilt from ``nlp.Defaults`` plus
            the letter-bounded hyphen split, so custom infixes on a replaced
            tokenizer are not preserved.
        abbreviations: Period-bearing abbreviations to keep as single tokens.
            Defaults to the bundled ``resources/nb/abbreviations.txt``.
    """

    if abbreviations is None:
        abbreviations = load_abbreviations(DEFAULT_ABBREVIATIONS_PATH)

    base_rules = getattr(nlp.tokenizer, "rules", None) or nlp.Defaults.tokenizer_exceptions
    tokenizer_exceptions = dict(base_rules)
    for abbreviation in _abbreviation_variants(tuple(abbreviations)):
        tokenizer_exceptions[abbreviation] = [{ORTH: abbreviation}]

    infixes = tuple(nlp.Defaults.infixes) + (LETTER_HYPHEN_INFIX,)

    prefix_search = getattr(nlp.tokenizer, "prefix_search", None)
    if prefix_search is None:
        prefix_search = compile_prefix_regex(nlp.Defaults.prefixes).search
    suffix_search = getattr(nlp.tokenizer, "suffix_search", None)
    if suffix_search is None:
        suffix_search = compile_suffix_regex(nlp.Defaults.suffixes).search

    return Tokenizer(
        nlp.vocab,
        rules=tokenizer_exceptions,
        prefix_search=prefix_search,
        suffix_search=suffix_search,
        infix_finditer=compile_infix_regex(infixes).finditer,
        token_match=getattr(nlp.tokenizer, "token_match", None),
        url_match=getattr(nlp.tokenizer, "url_match", None),
    )


def _abbreviation_variants(abbreviations: tuple[str, ...]) -> set[str]:
    variants: set[str] = set()
    for abbreviation in abbreviations:
        variants.add(abbreviation)
        variants.add(abbreviation.lower())
        variants.add(abbreviation.upper())
        variants.add(abbreviation[:1].upper() + abbreviation[1:])
    return variants
