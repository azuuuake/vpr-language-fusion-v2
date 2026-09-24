# Precision-Weighted Visual-Language Reranking for VPR

This repository accompanies **“Precision-Weighted Visual-Language Reranking for Visual Place Recognition: A Controlled Evaluation.”**

Its purpose is using for verification: The menuscript is self-contained; this repository is an audit trail and reproducibility aid.

## Start here

1. **Evidence map:** [`EVIDENCE.md`](EVIDENCE.md)
2. **Fast numerical audit:** [`python scripts/verification.py`]
3. **Full method/configuration:** [`configs/final_config.json`](configs/final_config.json)
4. **All six inferential families / 90 tests:** [`results/inferential_families/all_confirmatory_tests_90.csv`](results/inferential_families/all_confirmatory_tests_90.csv)
5. **Reproduce Table 1 from matrices:** see [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md)
6. **Known exact-tie convention:** [`KNOWN_NOTES.md`](KNOWN_NOTES.md)

## Headline result

PWF provides selected retrieval gains, especially at R@5, but does **not** consistently outperform equally source-calibrated constant fusion or tuned sigmoid gating across the evaluated backbones and datasets. The language-uncertainty statistic predicts language-ranking error on AmsterTime and MSLS under the evaluated caption pipelines, but no corresponding conditional association remains on Nordland.

## Evaluated configurations

| Item | EigenPlaces | CosPlace |
|---|---:|---:|
| Visual backbone | ResNet-50, 2048-D | ResNet-18, 512-D |
| PWF `(rho, M_c)` | `(3, 10)` | `(8, 10)` |
| Source-tuned constant alpha | `0.84` | `0.63` |
| Source-tuned SG `(tau, theta)` | `(1, 0.085)` | `(3, 0.045)` |

Common settings: `K_u=10`, `lambda=0.5`, `epsilon=1e-9`, MSLS split seed `42`, 5,000 paired bootstrap resamples.

Text encoder: `BAAI/bge-large-en-v1.5` (BGE-L). MSLS and AmsterTime use LaVPR-provided descriptions. Nordland uses offline `Salesforce/blip-image-captioning-base` captions for summer database and winter query images. This caption-provenance asymmetry is explicitly treated as a limitation, not resolved as a causal comparison.

## Repository layout

```text
configs/                     frozen final configuration
src/                         canonical PWF and statistical code
scripts/                     claim verifier and matrix-level reproduction
results/paper_tables/        exact paper table values
results/inferential_families/ all six BH-FDR families
results/diagnostics/         oracle, alpha, LU and candidate-composition evidence
results/calibration/         source-only calibration sweeps
archive/                     historical/raw evidence preserved for audit
notebooks/                   archived reviewer-extension notebook
paper/                       bibliography source
```

The large locked matrices are packaged separately as the GitHub Release asset `locked_matrices.zip`; see `data/README.md`.

## One-command audit

```bash
python -m pip install -r requirements.txt
python scripts/verification.py
```

Expected final line:

```text
PASS: all frozen headline numerical evidence and family counts verified.
```

## Version freeze

Tag/release the exact submission state as:

```text
acra2026-submission-v1
```
