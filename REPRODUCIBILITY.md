# Reproducibility Guide

## Level 1 — verification without large data

```bash
pip install -r requirements.txt
python scripts/verification.py
```

This checks the frozen table values, the six inferential-family sizes, BH-FDR headline comparisons, oracle-envelope examples, alpha summaries and LU validity results.

## Level 2 — reproduction of Table 1 from derived matrices

Download the GitHub Release asset `locked_matrices.zip`, extract it, then run:

```bash
python scripts/reproduce_from_locked_matrices.py --data-dir /path/to/locked_matrices
```

The asset contains visual similarity matrices for both backbones, shared language-similarity matrices, positive matrices and the MSLS calibration/evaluation split. These are derived numerical artifacts; no raw benchmark images are redistributed.

### Expected matrix shapes

- AmsterTime: `(1231, 1231)`
- MSLS-val: `(740, 18871)`
- Nordland-aligned: `(400, 400)`

MSLS is then subset using the frozen 222/518 split from `msls_calibration_split_indices.npz`.

## Level 3 — inspect source calibration

Calibration sweeps are stored under `results/calibration/`. The frozen rule is to maximize calibration R@1 using only the 222-query MSLS source split, then apply the method-specific deterministic tie rule in `configs/final_config.json`.

## Statistical inference

All reported paired bootstrap tests use 5,000 query-level resamples and seed 42. BH-FDR is applied separately within the six inferential families documented in `MULTIPLICITY.md`. The `all_confirmatory_tests_90.csv` file exposes every test, including non-significant rows.

## LU diagnostics

The direct AUROC and conditional logistic outputs are stored under `results/diagnostics/`. Conditional models use `LU_z + C(k_positive)` whenever more than one positive-count stratum exists; AmsterTime retained pools have `k=1` throughout and therefore use no `k` term.
