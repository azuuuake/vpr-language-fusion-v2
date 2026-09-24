# VPR Language Fusion — Project Evidence Summary

Date: 2026-06-08

---

## 1. GitHub Repository

Repository:

https://github.com/azuuuake/vpr-language-fusion

Latest confirmed commit:

c1bad19 Add reproducibility scripts and result evidence

The repository contains the clean reproducibility code, result CSVs, README, requirements file, and supporting scripts.

Important GitHub files:

- README.md
- requirements.txt
- .gitignore
- src/su_metric.py
- scripts/run_b1_baseline.py
- scripts/run_b2_baseline.py
- scripts/run_method.py
- scripts/run_tau_ablation.py
- scripts/create_nordland_clean.py
- scripts/check_similarity_sorting.py
- scripts/download_amstertime.sh
- scripts/run_amstertime_cosplace.sh
- results/baseline_results.csv
- results/msls_val_tau_ablation.csv
- results/amstertime_paired_bootstrap_r1.csv

---

## 2. Main Google Drive Folder

Main Drive folder:

/content/gdrive/MyDrive/vpr_research/

Folder structure:

- embeddings/
- results/
- figures/
- notes/
- papers/
- amstertime_raw/
- msls_raw/
- nordland_raw/
- nordland_clean_subset/
- evidence/
  - inventory/
  - repro_checks/
  - final_tables/
  - notebook_archive/
  - logs/

---

## 3. Saved Similarity and Ground-Truth Matrices

Folder:

/content/gdrive/MyDrive/vpr_research/embeddings/

Main matrices:

AmsterTime:
- amstertime_visual_sim_matrix.npy
- amstertime_lang_sim_matrix.npy
- amstertime_fixed_fusion_alpha05_matrix.npy
- amstertime_positive_matrix.npy

MSLS-val:
- msls_val_visual_sim_matrix.npy
- msls_val_lang_sim_matrix.npy
- msls_val_fixed_fusion_alpha05_matrix.npy
- msls_val_positive_matrix.npy

Nordland-clean:
- nordland_clean_visual_sim_matrix.npy
- nordland_clean_lang_sim_matrix.npy
- nordland_clean_fixed_fusion_alpha05_matrix.npy
- nordland_clean_positive_matrix.npy

Prompted Nordland exploratory files:
- nordland_clean_prompted_lang_sim_matrix.npy
- nordland_clean_prompted_fixed_fusion_alpha05_matrix.npy

Matrix shape inventory:

/content/gdrive/MyDrive/vpr_research/evidence/inventory/matrix_shape_inventory.csv

The matrix shape inventory confirms:
- AmsterTime matrices: (1231, 1231)
- MSLS-val matrices: (740, 18871)
- Nordland-clean matrices: (400, 400)

---

## 4. Final Result Tables

Main result folder:

/content/gdrive/MyDrive/vpr_research/results/

Important files:

- baseline_results.csv
- msls_val_tau_ablation.csv
- amstertime_paired_bootstrap_r1.csv
- text_sim_separation_stats.csv

Backup copies:

/content/gdrive/MyDrive/vpr_research/evidence/final_tables/

Files:
- baseline_results.csv
- msls_val_tau_ablation.csv
- amstertime_paired_bootstrap_r1.csv

---

## 5. Figures

Folder:

/content/gdrive/MyDrive/vpr_research/figures/

Confirmed figures:

- su_calibration_msls.png
- su_calibration_msls_final_v2.png
- text_sim_separation.png

Figure meaning:

1. su_calibration_msls_final_v2.png
   - Shows that SU is a meaningful uncertainty proxy on MSLS-val.
   - R@1 drops from 1.00 in the most confident SU decile to 0.392 in the most uncertain decile.
   - The top axis shows the mean SU value per decile.

2. text_sim_separation.png
   - Compares language cosine similarity distributions for correct matches vs wrong visual top-1 predictions.
   - Supports the paper’s claim that language reliability is dataset-dependent.

---

## 6. Reproduction Check

Folder:

/content/gdrive/MyDrive/vpr_research/evidence/repro_checks/

Main file:

- reproduction_check_from_saved_matrices.csv

Summary:

The saved visual similarity matrices, language similarity matrices, and positive ground-truth matrices reproduced all reported B1, B2, Confidence-Gated-Top10, and Confidence-Gated-Full results across AmsterTime, MSLS-val, and Nordland-clean.

All 12 method-dataset combinations passed the reproduction check within rounding tolerance.

Confirmed reproduced results:

AmsterTime:
- B1 visual:      43.461 / 63.444 / 70.187
- B2 fixed:       43.623 / 65.800 / 73.436
- Gated top-10:   43.217 / 63.769 / 70.187
- Gated full:     43.461 / 63.769 / 70.512
- Language active: 401 / 1231

MSLS-val:
- B1 visual:      84.865 / 90.946 / 92.838
- B2 fixed:       84.459 / 91.486 / 93.243
- Gated top-10:   85.135 / 91.081 / 92.838
- Gated full:     85.000 / 90.946 / 92.703
- Language active: 205 / 740

Nordland-clean:
- B1 visual:      52.750 / 76.250 / 87.750
- B2 fixed:       45.750 / 75.000 / 83.750
- Gated top-10:   53.000 / 76.000 / 87.750
- Gated full:     52.250 / 74.500 / 85.000
- Language active: 165 / 400

---

## 7. Artifact Inventory

Folder:

/content/gdrive/MyDrive/vpr_research/evidence/inventory/

Important inventory files:

- drive_file_inventory_before_cleanup.csv
- drive_file_inventory_after_cleanup.csv
- expected_artifacts_inventory.csv
- expected_artifacts_inventory_after_copy.csv
- expected_artifacts_inventory_FINAL.csv
- matrix_shape_inventory.csv

Final status:

All expected artifacts are present:
- matrices
- result CSVs
- figures
- final table backups
- notebook archive README
- reproduction check CSV

---

## 8. Notebook Archive

Folder:

/content/gdrive/MyDrive/vpr_research/evidence/notebook_archive/

Important file:

- README.txt

Purpose:

This folder is for raw exploratory notebook evidence only. It may contain failed attempts, intermediate checks, debugging cells, and successful runs. It is not the official reproducibility path.

Official reproducibility path:
1. GitHub scripts
2. saved matrices in embeddings/
3. result CSVs in results/
4. evidence CSVs in evidence/

---

## 9. Main Paper Result Framing

The main contribution is not that language always improves VPR.

The correct framing is:

Fixed-weight language fusion can be harmful when generated language descriptions are noisy, generic, or semantically unreliable. Confidence-gated top-10 reranking provides a safer alternative by applying language selectively based on visual uncertainty and language-score discriminability.

Primary method:

Confidence-Gated-Top10

Main R@1 results:

AmsterTime:
- B1 visual: 43.4
- B2 fixed: 43.6
- Ours top-10: 43.2
- Interpretation: statistically indistinguishable from B1; -3 queries vs B1, bootstrap CI includes zero.

MSLS-val:
- B1 visual: 84.9
- B2 fixed: 84.5
- Ours top-10: 85.1
- Interpretation: best R@1.

Nordland-clean:
- B1 visual: 52.8
- B2 fixed: 45.8
- Ours top-10: 53.0
- Interpretation: fixed fusion drops by 7.0pp; gated top-10 recovers the degradation and improves by +7.2pp over B2.

---

## 10. Important Discussion Point

The language variance threshold detects low-discriminability language similarity patterns, but it does not verify whether captions are semantically correct.

This is important for Nordland-clean.

In Nordland-clean:
- language active: 165 / 400 queries
- activation rate: 41.3%
- B2 fixed fusion degraded R@1 from 52.8 to 45.8
- gated top-10 recovered R@1 to 53.0

This means the gate worked as intended, but caption hallucination/noise limited the gain over B1. This is not a bug. It is a real limitation and should be discussed in the paper.

Suggested paper wording:

A limitation of the proposed language discriminability filter is that it measures the spread of language similarity scores rather than the semantic correctness of generated captions. This was most visible in Nordland-clean, where some generated captions were varied enough to pass the language filter but remained semantically unreliable for place recognition. Consequently, confidence-gated reranking recovered the degradation caused by fixed fusion, but the gain over the visual-only baseline remained small. Future work should combine confidence-gated fusion with caption-quality estimation or VPR-specific caption generation.

---

## 11. Current Project Status

Completed:
- GitHub repo cleaned and pushed
- Drive folder cleaned
- matrices found and verified
- result CSVs copied to Drive
- figures generated
- reproduction check passed
- reproducibility note saved
- project evidence summary saved

Next recommended task:
Write the paper Results and Discussion sections using the verified numbers and saved evidence.
