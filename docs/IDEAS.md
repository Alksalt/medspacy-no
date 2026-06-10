# docs/IDEAS.md — v0.2+ backlog

Ideas for after v0.1 ships to PyPI and JOSS is submitted. Not a commitment list — scope them before picking up.

## NorMedTerm-seeded target matcher

NorMedTerm (LTG/UiO, 77k+ Norwegian medical entities, 12 semantic categories, ICD codes) as the medspacy `TargetMatcher` / QuickUMLS-equivalent layer. v0.1 leaves target matching to the user; v0.2 could bundle a `load_nb(targets=True)` path that initializes the TargetMatcher from NorMedTerm. Current repo terms state CC BY 4.0, so attribution is required; bundling still needs a deliberate data-size/provenance decision.

## QuickUMLS Norwegian concept database

UMLS contains Norwegian MeSH synonyms and some SNOMED CT Norwegian translations. QuickUMLS can build a lookup index from any UMLS release. Requires a UMLS API license (free for researchers). Would turn `medspacy-no` into a full entity-detection + modification pipeline comparable to the English medspacy stack. Evaluate after v0.1 evidence base exists.

## nynorsk variants

Norwegian Nynorsk is used in parts of Vestland and Møre og Romsdal — clinically marginal but politically visible. spaCy has no `nn` model with production-quality segmentation; NorNE has Nynorsk gold. Track spaCy `nn` model development; add a thin `resources/nn/` module when a viable base pipeline exists. Do not prioritize over Bokmål completeness.

## Danish and Swedish sibling modules

The linguistic donor chain is clear: Swedish (Skeppstedt 2011) → Norwegian → Danish. DaCy (Danish spaCy pipeline) has no clinical negation module. A `medspacy-da` port would be a straightforward second contribution after `medspacy-no` is established. Swedish medspacy (`sv`) is similarly absent. Value: expands citation surface; demonstrates the resource methodology; strengthens a NoDaLiDa Nordic-track paper. Do not start before `medspacy-no` v0.1 is peer-reviewed.

## integration into the FHIR harness Norwegian track

The ehelse FHIR safety harness project has a Norwegian clinical text track. medspacy-no provides the negation/uncertainty layer that makes entity-level assertions extractable from free text into FHIR resources. Integration path: `medspacy_no.load_nb()` as a pipeline step in the harness text processor. Scope after both projects have stable APIs.

## integration into the ICD-10 benchmark pipeline

The ICD-10 Norwegian coding benchmark (NorMedBench, ehelse idea #1) depends on accurate negation handling: a "no fever" mention should not count as a positive ICD signal. Plugging medspacy-no into the benchmark's pre-processing pipeline is a natural v0.2 integration. Coordinate API design with NorMedBench so the interface is clean before v0.1 locks.

## larger and more diverse gold set

v0.1 gold set is ~300–500 sentences, synthetic, single-domain (internal medicine / cardiology substrate from NorSynthClinical). v0.2 target: 1000+ sentences spanning surgery notes, psychiatry, GP records, discharge summaries. Requires additional clinical colleagues for annotation. Strengthens any journal submission.
