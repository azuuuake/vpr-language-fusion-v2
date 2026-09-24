# Data Provenance and Redistribution

## Visual data

Raw benchmark images are **not** redistributed here. For verification, anyone should obtain MSLS, AmsterTime and Nordland from their official sources under the corresponding dataset terms.

## Language descriptions

- MSLS and AmsterTime: descriptions supplied by the LaVPR benchmark.
- Nordland: generated offline with `Salesforce/blip-image-captioning-base` for the summer database and winter queries.
- Text encoding: `BAAI/bge-large-en-v1.5`, 1024-D, normalized embeddings, cosine similarity.

The public release asset contains derived similarity matrices, not raw image or description corpora. Before public upload, the repository owner should confirm that redistribution of each derived artifact is compatible with the upstream dataset/benchmark terms. If any term is uncertain, publish the scripts and result CSVs while providing acquisition instructions instead of the affected matrix.

## Ground truth

- MSLS: positive matrix aligned to the locked benchmark ordering; held-out split uses the frozen seed-42 indices.
- AmsterTime: official/index-aligned evaluation ordering used by the project.
- Nordland-aligned: 400-query aligned subset; a match is accepted within ±25 sampled frames.

