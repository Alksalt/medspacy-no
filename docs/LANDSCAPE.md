# Norwegian Clinical NLP Landscape Update

This note records post-scaffold source checks that refine the public claims in `README.md`, `docs/PLAN.md`, and future papers. It does not replace the implementation dossier.

## Current Positioning

medspacy-no should claim a narrow, defensible niche: an open Norwegian Bokmal medspaCy/ConText resource package with transparent rule files, clinical section detection, and clinical sentence segmentation.

Do not claim that no Norwegian clinical NLP exists. KliniskVestBERT was announced in 2026 as BERT models continued-pretrained on real de-identified Helse Vest clinical text, evaluated on synthetic Norwegian clinical benchmarks and real-world problems.

## Resource and License Notes

- NorSynthClinical and NorSynthClinical-PHI still require written permission before redistributing derivative sentences because the repos do not provide an explicit open license.
- NorMedTerm currently states CC BY 4.0 terms in its README. Treat it as usable with attribution, but make a separate decision before bundling or deriving package data from it.
- medspaCy currently has no Norwegian resource folder. Its README cites English, French, and Dutch ConText rule resources; Spanish exists as a resource folder but should not be described as having mature ConText rules without checking the current files.

## Sources

- https://arxiv.org/abs/2606.01904
- https://github.com/ltgoslo/NorMedTerm
- https://github.com/medspacy/medspacy
- https://github.com/medspacy/medspacy/tree/master/resources
