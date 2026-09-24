# Evidence Index

This page is the shortest route for someone to quickly verify the menuscript.

| ID | Paper information | Primary evidence | What to check |
|---|---|---|---|
| C01 | PWF/SU/LU equations and SU-only ablation | `src/pwf.py`, `configs/final_config.json` | Exact formulas, `epsilon=1e-9`, `K_u=10`, `lambda=.5` |
| C02 | 222/518 MSLS split, seed 42; dataset sizes | `data/msls_calibration_split_indices.npz`, `configs/final_config.json`, matrix release | Split lengths and matrix shapes |
| C03 | BGE-L text encoder and caption provenance | `archive/provenance/lavpr_bge_log_evidence.txt`, `DATA_AND_LICENSE.md` | `BAAI/bge-large-en-v1.5`; Nordland BLIP vs LaVPR descriptions |
| C04 | Source-calibrated settings | `results/calibration/`, `configs/final_config.json` | PWF `(3,10)` / `(8,10)`, constant `.84` / `.63`, SG settings and tie rules |
| C05 | Table 1 retrieval metrics | `results/paper_tables/table1_retrieval_metrics.csv` | Every R@1/R@5/R@10 number |
| C06 | EigenPlaces fair-control significance | `results/inferential_families/eigenplaces_fair_controls_BH12.csv` | AmsterTime and Nordland R@5 survivors; no R@1 survivor |
| C07 | CosPlace significance | `results/inferential_families/cosplace_controls_BH18.csv` | Three AmsterTime BH-FDR survivors |
| C08 | LU increment | `results/inferential_families/cosplace_LU_increment_BH6.csv` | Nordland R@5 = -1.50 pp, q≈.0312; other CP LU increments non-significant |
| C09 | Target-oracle constant envelope | `results/diagnostics/adaptive_vs_oracle_constant_envelope.csv` | PWF-vs-oracle differences; target labels used only diagnostically |
| C10 | PWF alpha distributions | `results/diagnostics/alpha_distribution_all_settings.csv` | EP means ~.71-.72; CP means ~.85-.86 |
| C11 | Pooled LU AUROC | `results/diagnostics/final_combined_LU_validity_two_backbones.csv` | Six AUROCs and CIs |
| C12 | Conditional LU-error association | `results/diagnostics/conditional_LU_logistic_controlling_k.csv` | ORs >1 for AmsterTime/MSLS; Nordland CIs cross 1 |
| C13 | Candidate composition | `results/diagnostics/language_error_vs_chance_by_positive_count.csv` | Error behavior by number of positives in top-10 |
| C14 | Multiplicity | `results/inferential_families/all_confirmatory_tests_90.csv`, `MULTIPLICITY.md` | Six separately defined families totaling 90 tests |
| C15 | R@10 invariant for top-10 rerankers | `src/pwf.py`, Table 1 CSV | Candidate membership is unchanged |
| C16 | EP/AmsterTime exact tie | `KNOWN_NOTES.md` | Why paper visual R@1 is 43.46 while NumPy stable sort can give 43.379 |

For a machine check of the headline numeric claims, run:

```bash
python scripts/verification.py
```
