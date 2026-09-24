# Known Notes

## 1. EigenPlaces / AmsterTime visual-only exact tie

The paper reports **43.46% R@1 (535/1231)** for the EigenPlaces AmsterTime visual baseline, following the original auto_VPR / `torch.topk` benchmark convention.

A later NumPy stable-sort reanalysis of the saved similarity matrix gives **43.379% (534/1231)** because one query contains an exact similarity tie whose ordering differs between the two retrieval implementations. This is a one-query tie convention, not a changed descriptor or ground truth. PWF, tuned-control, R@5 and inferential conclusions are unchanged.

For this reason:
- `results/paper_tables/table1_retrieval_metrics.csv` preserves the benchmark value used in the manuscript;
- `scripts/reproduction_from_matrices.py` may print 43.379% for that single visual-only cell when using NumPy stable sorting.

## 2. Numerical epsilon

The final paper and canonical implementation use `epsilon = 1e-9`. The archived CosPlace reviewer-extension notebook originally contained `1e-8`. A final consistency rerun with `1e-9` reproduced the frozen CosPlace PWF/SU-only/constant/SG Table 1 metrics and alpha means at the reported precision. The notebook is kept as an archive; `src/pwf.py` is the canonical submission implementation.

## 3. Caption provenance is intentionally not treated as controlled

MSLS and AmsterTime use LaVPR-provided descriptions; Nordland uses offline BLIP-base captions. Therefore dataset domain and caption-generation pipeline are confounded. The repository exposes the resulting diagnostics but does not claim that dataset identity alone causes the Nordland LU behavior.
