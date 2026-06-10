# Data Governance

medspacy-no must not contain real patient text, identifiable health information, or memorized clinical cases.

## Allowed Data

- Synthetic sentences authored for this project by the owner.
- Public example text with a compatible license and attribution.
- Third-party synthetic corpus excerpts only when written permission explicitly covers adaptation, annotation, redistribution, public hosting, and archival.

## Gold Set Requirements

Before adding an evaluation corpus, create a dataset card that states:

- source and authorship for each sentence group
- annotation labels and schema
- clinical reviewer and review date
- PHI exclusion method
- redistribution license
- known limitations, including synthetic-text evaluation

## Prohibited Data

- Real EHR text.
- Patient-identifiable text or PHI.
- Text derived from memory of a specific patient encounter.
- Third-party text without a compatible license or written permission.
