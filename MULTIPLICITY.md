# Multiplicity Accounting

The submission deliberately does **not** present all analyses as one pre-registered family.

The original EigenPlaces study stage contains:

1. `EP_original_main_27` — 27 non-degenerate main comparisons.
2. `EP_original_component_21` — 21 component-ladder comparisons after deterministic top-10 R@10 contrasts are excluded where appropriate.
3. `EP_original_conditional_LU_6` — 6 targeted High-SU/Low-LU comparisons.

Reviewer-motivated extensions added later contain:

4. `EP_reviewer_fair_controls_12` — 3 datasets × 2 metrics × 2 source-tuned controls.
5. `CP_reviewer_controls_18` — 3 datasets × 2 metrics × 3 comparisons.
6. `CP_reviewer_LU_increment_6` — 3 datasets × 2 metrics.

Total: **90 tests** across six separately BH-FDR-corrected inferential families.

`results/inferential_families/all_confirmatory_tests_90.csv` contains every row.

## Why two archived EigenPlaces CSVs have larger family counts

Historical files under `archive/legacy/` were saved before deterministic R@10 comparisons were removed from the final family definitions. To make the final manuscript accounting auditable, `scripts/build_canonical_inferential_families.py` filters those archived raw p-values according to the final definitions and recomputes BH-FDR, yielding exactly 27 and 21 tests. The archived files are retained rather than overwritten.
