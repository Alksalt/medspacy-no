Research complete. Here is the memo.

---

# medspacy-no — Seed Materials Memo

Compiled 2026-06-10. All trigger lists below are pulled from primary sources; Norwegian candidates are my proposals and need physician sign-off where flagged.

## SWEDISH-TRIGGERS

Source paper: Skeppstedt M. (2011), *Negation detection in Swedish clinical text: An adaption of NegEx to Swedish*, J. Biomed. Semantics 2(Suppl 3):S3. Open access: [Springer/BMC](https://link.springer.com/article/10.1186/2041-1480-2-S3-S3) · [PMC3194175](https://pmc.ncbi.nlm.nih.gov/articles/PMC3194175/). The paper states the full trigger set is published as a separate file and "can be used together with the original NegEx program."

Full verbatim list fetched from that file: **http://people.dsv.su.se/~mariask/resources/triggers.txt** (ISO-8859-1 encoded, 42 entries, tab-separated `phrase \t [tag]`). Tags: `[pren]` = pre-negation, `[post]` = post-negation, `[pseu]` = pseudo-negation. This is the actual evaluated Swedish lexicon, reproduced exactly:

| Swedish phrase | Tag |
|---|---|
| saknas | post |
| negativt | post |
| osannolikt | post |
| inget avvikande | post |
| förnekas | post |
| inte | pren |
| ej | pren |
| ingen | pren |
| utan | pren |
| inga | pren |
| inget | pren |
| har inte | pren |
| inga tecken | pren |
| kan inte | pren |
| inte har | pren |
| utesluta | pren |
| förnekar | pren |
| inte kan | pren |
| icke | pren |
| aldrig | pren |
| saknar | pren |
| uteslutas | pren |
| patienten inte | pren |
| känner sig inte | pren |
| utan några | pren |
| kunde inte | pren |
| inte kunnat | pren |
| utan tecken | pren |
| inte visar | pren |
| inte kunna | pren |
| inget som | pren |
| fri från | pren |
| avsaknad av | pren |
| vet inte | pseu |
| inte vet | pseu |
| kan inte uteslutas | pseu |
| inte bara | pseu |
| inte utesluta | pseu |
| inte orsaka | pseu |
| inte nödvändigtvis | pseu |
| ingen ändring | pseu |
| ingen förändring | pseu |

Counts: 5 post, 28 pren, 9 pseu = 42 (the paper rounds this to "41 triggers"). This published file is the substrate to port — not the paper tables, which only show the most frequent subset.

## POSTER-RULES

Source: Budrionis A., Dalianis H., Yigzaw K.Y., Makhlysheva A., Chomutare T. (2018), *Negation detection in Norwegian medical text: Porting a Swedish NegEx to Norwegian (Work in progress)*, Norwegian Centre for E-health Research (UNN Tromsø) + DSV/Stockholm University. Poster page: [ehealthresearch.no](https://ehealthresearch.no/en/posters/negation-detection-in-norwegian-medical-text-porting-a-swedish-negex-to-norwegian-work-in-progress) · full PDF: [Poster_2018-14_A0](https://ehealthresearch.no/files/documents/Postere/Poster_2018-14_A0-Negation-detection-in-Norwegian-medical-texts.pdf). Contact printed on poster: **andrius.budrionis@ehealthresearch.no**, +47 913 60 982.

Important caveat: the poster does **not** publish the individual Norwegian trigger phrases. It only reports rule *counts* and a couple of in-text examples. Everything it shows:

- Rule expansion vs. Swedish original (40 Swedish rules → +27 new = 67 Norwegian rules):
  - **POST-negation**: 15 Norwegian (5 in Swedish version)
  - **PREN (pre-negation)**: 34 Norwegian (26 in Swedish version)
  - **PSEU (pseudo-negation)**: 18 Norwegian (9 in Swedish version)
- Actual Norwegian triggers visible anywhere on the poster (from worked examples only):
  - `ikke` — "…hadde **ikke** tegn til [NEGATED]peritonitt[NEGATED]." (i.e. pattern *ikke tegn til*)
  - `ikke-` (prefix) — "**ikke**-operable metastaser" (flagged as a tokenization hazard: `ikke -operable` vs `ikke-operable`)
- Method: ported Skeppstedt's Swedish NegEx; added Norwegian ICD-10 (2017) term list (19,021 symptoms/diagnoses) from [ehelse.no ICD-10](https://ehelse.no/standarder-kodeverk-og-referansekatalog/helsefaglige-kodeverk/kodeverket-icd-10-og-icd-11) plus 23 GI-surgery terms. Corpus: 170 Tidsskriftet GI-surgery articles (294,745 words).
- Results (Table 1, no gold standard): 70 negated findings on full corpus; manually-labelled sub-corpus (75,614 words) had 29 negations; exact-string matching and Norwegian tokenization named as the main weaknesses.

Bottom line: the poster confirms the porting approach and rule-count deltas but gives no reusable Norwegian lexicon. The Norwegian trigger list has to be reconstructed from the Swedish file (next section).

## NO-CANDIDATES

Norwegian bokmål clinical equivalents proposed by me. Category mirrors the Swedish tag (pre = NEGATED_EXISTENCE pre, post = NEGATED_EXISTENCE post, pseu = PSEUDO). "False friend" = the literal cognate is wrong/Nynorsk/Swedish and must not be copied. "UNCERTAIN → review" = send to physician.

| Swedish | Norwegian candidate(s) | Note / category |
|---|---|---|
| saknas | mangler; (savnes) | post. "savnes" drifts to "is missed" — prefer "mangler" |
| negativt | negativt | post. Direct (e.g. "CRP negativt") |
| osannolikt | usannsynlig | post, but UNCERTAIN → review: "improbable" is hedged, may belong in PSEU/possible-existence rather than hard negation |
| inget avvikande | intet avvikende; ingen avvikende funn; (i.a.b. = intet å bemerke) | post. Add the idiom "intet å bemerke" |
| förnekas | benektes | post. False friend: "fornektes" exists but "benekte" is the clinical verb for denying symptoms |
| inte | ikke | pren. Core |
| ej | ej; ikke | pren. "ej" is used in Norwegian charting ("ej aktuelt") — keep both |
| ingen | ingen | pren. Direct |
| utan | uten | pren. False friend: do NOT keep "utan" (that is Swedish/Nynorsk); bokmål is "uten" |
| inga | ingen | pren. "inga" is Nynorsk/dialect; bokmål plural is "ingen" |
| inget | intet; ingenting | pren. "intet" formal, "ingenting" neutral |
| har inte | har ikke | pren |
| inga tecken | ingen tegn; ingen tegn til | pren. "tegn til" is the productive clinical frame |
| kan inte | kan ikke | pren |
| inte har | ikke har | pren |
| utesluta | utelukke | pren. False friend spelling: not "utesluta" |
| förnekar | benekter | pren. False friend: prefer "benekter" over "fornekter" |
| inte kan | ikke kan | pren |
| icke | ikke; ikke- | pren. Swedish prefix "icke" → bokmål "ikke-" (ikke-operabel) |
| aldrig | aldri | pren |
| saknar | mangler | pren |
| uteslutas | utelukkes | pren |
| patienten inte | pasienten ikke | pren |
| känner sig inte | føler seg ikke | pren |
| utan några | uten noen | pren |
| kunde inte | kunne ikke | pren |
| inte kunnat | ikke kunnet | pren |
| utan tecken | uten tegn; uten tegn til | pren |
| inte visar | viser ikke; ikke viser | pren. Word-order variants — both needed |
| inte kunna | ikke kunne | pren |
| inget som | intet som; ingenting som | pren |
| fri från | fri for | pren. False friend: NOT "fri fra"; the clinical idiom is "fri for" (free of) |
| avsaknad av | fravær av; mangel på | pren. "avsaknad" is not a Norwegian word |
| vet inte | vet ikke | pseu |
| inte vet | ikke vet | pseu |
| kan inte uteslutas | kan ikke utelukkes | pseu. Critical: means "cannot be ruled out" → finding is NOT negated |
| inte bara | ikke bare | pseu |
| inte utesluta | ikke utelukke | pseu |
| inte orsaka | ikke forårsake | pseu |
| inte nödvändigtvis | ikke nødvendigvis | pseu |
| ingen ändring | ingen endring | pseu. False friend: Swedish "ändring" → bokmål "endring" (not "ending") |
| ingen förändring | ingen forandring | pseu. False friend: "förändring" → "forandring" |

Flagged for physician review: `osannolikt → usannsynlig` (hedge vs. negation), plus all rows marked "False friend" should be confirmed against real Norwegian charting style (terse EPJ Norwegian differs from prose). Worth adding from the poster examples but absent in the Swedish file: `ikke tegn til`, `ikke-` prefix, and bokmål abbreviation forms (`u.a.` = uten anmerkning, `i.a.b.` = intet å bemerke) for the post-negation set.

## CONTACTS

- **Lilja Øvrelid** — Professor, leader of the Language Technology Group (LTG), Department of Informatics, University of Oslo; co-director, Integreat. Email: **liljao@ifi.uio.no**. Page: [mn.uio.no/ifi/.../liljao](https://www.mn.uio.no/ifi/english/people/aca/liljao/index.html). This is the right rights-holder contact for **NorSynthClinical** (hosted under [github.com/ltgoslo/NorSynthClinical](https://github.com/ltgoslo/NorSynthClinical)); she is also a co-author on the LTG clinical-NLP work.

- **Synnøve Bråten (Bråthen)** — author of **NorSynthClinical-PHI** ([github.com/synnobra/NorSynthClinical-PHI](https://github.com/synnobra/NorSynthClinical-PHI)). At the time of the source paper she was at the Dept. of Computer and Systems Sciences (DSV), Stockholm University. Only email printed in the paper is personal: **synnovebr@hotmail.com** (NODALIDA 2021, [aclanthology.org/2021.nodalida-main.22](https://aclanthology.org/2021.nodalida-main.22/)). No current institutional address is verifiable on any official page. Recommend CC'ing the stable senior co-author **Hercules Dalianis — hercules@dsv.su.se** (DSV Stockholm), who co-authored both NorSynthClinical-PHI and the Tromsø poster, for the PHI corpus permission.

- **Pål H. Brekke** — MD PhD, cardiologist, OUS Rikshospitalet; now Medical Director at DIPS AS; affiliated with the BigMed project. Profile: [ous-research.no/.../18806](https://www.ous-research.no/home/edvardsen/group%20members/18806) (no email published). LinkedIn: [linkedin.com/in/pal-h-brekke](https://www.linkedin.com/in/pal-h-brekke/). **No email is exposed on any official OUS/UiO/DIPS page.** Do not guess — OUS uses `fornavn.etternavn@ous-hf.no` as a pattern, but that is UNVERIFIED for him; route via OUS Kardiologi or LinkedIn/DIPS. He is a stakeholder/advisor contact, not a rights-holder for the two corpora.

Rights mapping for the permission ask: NorSynthClinical → Øvrelid/LTG; NorSynthClinical-PHI → Bråten + Dalianis.

## EMAIL-NO

Bokmål, plain, ~105 words in body, three paragraphs:

Hei,

Jeg utvikler en åpen kildekode-pakke for norsk klinisk språkteknologi (medspacy-no) og ønsker å lage et lite, annotert evalueringssett for negasjons- og kontekstdeteksjon. Jeg vil gjerne be om tillatelse til å gjenbruke setninger fra NorSynthClinical og NorSynthClinical-PHI som grunnlag for dette settet, med tydelig kreditering til dere som opphavspersoner.

Grunnen til at jeg spør, er at repositoriene ikke har en LICENSE-fil, og jeg vil forsikre meg om at bruken er i orden før jeg publiserer. Datasettet vil forbli åpent tilgjengelig, og bidraget deres vil bli oppgitt i dokumentasjonen.

Tusen takk for arbeidet dere har delt. Jeg setter stor pris på et svar.

Med vennlig hilsen
Oleksandr Altukhov
utdannet lege (cand.med.), Kristiansund
alksalt.com

## UPSTREAM-NAMING

- **PR #293** ([github.com/medspacy/medspacy/pull/293](https://github.com/medspacy/medspacy/pull/293)) — adds multilingual support: a `language_code` argument to `medspacy.load()` and components, and per-language resource folders. Ships skeletons for German, Spanish, French, Italian, Dutch, Polish, Portuguese; French and Spanish are most mature (include ConText rules), others mostly RuSH section rules. Author calls for community rule contributions. No explicit discussion of ISO standards or `nb` vs `no`.
- **Issue #264** ([github.com/medspacy/medspacy/issues/264](https://github.com/medspacy/medspacy/issues/264)) — the design thread that motivated #293. Proposes moving English resources to `resources/en/` and adding e.g. `resources/pl/`. Debates fork vs. upstream contribution; raises concerns about multi-language test suites and package bloat. No maintainer ruling on a code-naming standard.
- **Actual convention in the repo** ([resources/](https://github.com/medspacy/medspacy/tree/master/resources)): two-letter **ISO 639-1** folders — `de, en, es, fr, it, nl, pl, pt`. No contributor doc beyond "match this layout + add a `language_code`."

Recommendation: **use `nb`** (folder `resources/nb/`, `medspacy.load(language_code="nb")`). Rationale that decides it: medspacy passes `language_code` to spaCy (`spacy.blank(language_code)`), and spaCy ships Norwegian only as **Bokmål `nb`** (e.g. `nb_core_news_sm`); spaCy has no `no` macrolanguage class, so `language_code="no"` would fail to instantiate a spaCy pipeline. `nb` is also a valid ISO 639-1 code and fits the existing two-letter folder pattern. Reserve `nn` if Nynorsk is ever added. When upstreaming, mirror the `resources/<code>/` layout and expect to be asked for ConText + section rules per the #293 template.

## ABBREVIATION-SOURCES

Public Norwegian clinical/medical abbreviation lists usable to seed a clinical tokenizer (so "u.a.", "i.a.b.", "bl.tr.", etc. survive sentence segmentation):

1. **Helsedirektoratet — per-guideline "Forkortelser" pages.** Authoritative, domain-scoped. Stroke: [helsedirektoratet.no/.../hjerneslag/forkortelser](https://www.helsedirektoratet.no/retningslinjer/hjerneslag/forkortelser); addiction: [.../avrusning.../forkortelser-og-sentrale-begreper](https://www.helsedirektoratet.no/retningslinjer/avrusning-fra-rusmidler-og-vanedannende-legemidler/forkortelser-og-sentrale-begreper). Each guideline carries its own list (stroke page covers items like TIA, NIHSS, rtPA). Scrape per guideline and union them.

2. **UNN Labhåndbok — Forkortelser** ([labhandbok.unn.no/forkortelser/category929.html](https://labhandbok.unn.no/forkortelser/category929.html)). Lab/specimen and unit codes. Examples: `S` = serum, `P` = plasma, `U` = urin, `BM` = benmarg, `EDTA`, `kPa`. Good for the lab-results register.

3. **Tidsskrift for Den norske legeforening — forfatterveiledning / style.** Discourages non-standard abbreviations and lists accepted ones; useful as a normative whitelist. Author guidelines at [tidsskriftet.no/forfatterveiledning](https://tidsskriftet.no/forfatterveiledning).

4. **Tidsskriftet Michael — "Forkortelser"** ([michaeljournal.no/article/2022/04/Forkortelser](https://www.michaeljournal.no/article/2022/04/Forkortelser)). ~80 entries, academic/general-practice slant. Examples: `EPJ` = elektronisk pasientjournal, `NKLM` = Nasjonalt kompetansesenter for legevaktmedisin, `OSKE` = objektiv strukturert klinisk eksamen, `AFE` = allmennmedisinsk forskningsenhet.

5. **Store medisinske leksikon (SNL)** — "Forkortelser" taxonomy [sml.snl.no/.taxonomy/3962](https://sml.snl.no/.taxonomy/3962) and "Ordforklaringer medisin" [sml.snl.no/.taxonomy/212](https://sml.snl.no/.taxonomy/212). Encyclopedic, broad (e.g. `CRP`, `EKG`). Open/CC-friendly source.

6. **Felleskatalogen — medisinsk ordbok / ordliste.** Drug and clinical terms: ordbok [felleskatalogen.no/medisin/ordbok/a](https://www.felleskatalogen.no/medisin/ordbok/a); downloadable ordliste PDF [felleskatalogen.no/medisin-vet/dokument/ordliste.pdf](https://www.felleskatalogen.no/medisin-vet/dokument/ordliste.pdf) (note: the PDF is the veterinary list; use the web ordbok for human-medicine terms).

Practical note for the tokenizer: the highest-value entries are the period-bearing charting abbreviations (`u.a.`, `i.a.b.`, `bl.tr.`, `temp.`, `tilst.`, `obs.`, `susp.`, `dvs.`, `ca.`) that break naive sentence splitters — these are best harvested from UNN-type house lists and the Helsedirektoratet guideline glossaries rather than the encyclopedic sources. Pair this with the Norwegian ICD-10 term list ([ehelse.no ICD-10](https://ehelse.no/standarder-kodeverk-og-referansekatalog/helsefaglige-kodeverk/kodeverket-icd-10-og-icd-11)) used by the Tromsø poster for the entity side.

Local artifacts saved during research: `/tmp/sv_triggers.txt` (verbatim Swedish lexicon), `/tmp/poster.txt` (full poster text), `/tmp/nodalida.pdf` (NorSynthClinical-PHI paper).