#!/usr/bin/env python3
"""
Reproduce the 20-split EigenPlaces calibration-sensitivity analysis.

This script uses the same PWF implementation, search grid, source-calibration
objective, deterministic tie-breaking rule, and precomputed matrices as the
camera-ready paper.

It evaluates 20 total 30% MSLS calibration splits:
  - the primary seed-42 split
  - 19 alternative splits

For each split:
  1. Generate a 222-query MSLS calibration subset and 518-query held-out subset.
  2. Select (rho, M_c) by maximising calibration R@1.
  3. Break ties by preferring smaller M_c, then smaller rho.
  4. Freeze the selected configuration.
  5. Evaluate it on MSLS held-out, full AmsterTime, and full Nordland.

Usage:
  python scripts/calibration_split_sensitivity_20seeds.py \
      --data-dir /path/to/locked_matrices

Expected matrix filenames in --data-dir:
  msls_eigenplaces_visual.npy
  msls_language.npy
  msls_positive.npy
  amstertime_eigenplaces_visual.npy
  amstertime_language.npy
  amstertime_positive.npy
  nordland_eigenplaces_visual.npy
  nordland_language.npy
  nordland_positive.npy

Optional verification file:
  msls_calibration_split_indices.npz

Output:
  results/diagnostics/calibration_split_sensitivity_20seeds.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.pwf import pwf_retrieve, recalls  # noqa: E402


SEEDS = [
    1, 7, 21, 42, 84, 100, 123, 256, 512, 999,
    2, 5, 11, 17, 33, 64, 128, 333, 777, 2026,
]

RHO_GRID = [1, 1.5, 2, 3, 4, 6, 8, 10, 12, 16, 20, 30]
MC_GRID = [10, 20, 50, 100]

N_MSLS = 740
N_CAL = 222
PRIMARY_SEED = 42


def load(path: Path) -> np.ndarray:
    return np.load(path, allow_pickle=False)


def make_split(seed: int, n_queries: int = N_MSLS, n_cal: int = N_CAL):
    """Generate the paper's deterministic 30/70 query split."""
    perm = np.random.default_rng(seed).permutation(n_queries)
    return perm[:n_cal], perm[n_cal:]


def select_pwf(V_cal: np.ndarray, L_cal: np.ndarray, P_cal: np.ndarray):
    """
    Select PWF hyperparameters by calibration R@1.

    Tie-breaking follows the paper:
      1. smaller M_c
      2. smaller rho

    MC_GRID and RHO_GRID are therefore traversed in ascending tie-preference
    order, and the first configuration is retained when R@1 ties exactly.
    """
    best = None

    for mc in MC_GRID:
        for rho in RHO_GRID:
            ranked, _ = pwf_retrieve(V_cal, L_cal, rho=rho, mc=mc)
            r1 = recalls(ranked, P_cal, ks=(1,))["R@1"]

            if best is None or r1 > best["calibration_R1"] + 1e-12:
                best = {
                    "rho": rho,
                    "M_c": mc,
                    "calibration_R1": r1,
                }

    return best


def evaluate(V: np.ndarray, L: np.ndarray, P: np.ndarray, rho: float, mc: int):
    ranked, _ = pwf_retrieve(V, L, rho=rho, mc=mc)
    rr = recalls(ranked, P, ks=(1, 5, 10))
    return rr["R@1"], rr["R@5"], rr["R@10"]


def verify_primary_split(data_dir: Path):
    """
    If the frozen primary split file is available, verify that the generated
    seed-42 split is identical to the released split.
    """
    split_path = data_dir / "msls_calibration_split_indices.npz"
    if not split_path.exists():
        print("Note: frozen seed-42 split file not found; skipping split identity check.")
        return

    stored = np.load(split_path, allow_pickle=False)
    cal42, eval42 = make_split(PRIMARY_SEED)

    # Released file uses these names in the reproducibility package.
    stored_cal = stored["calibration_indices"]
    stored_eval = stored["evaluation_indices"]

    if not np.array_equal(cal42, stored_cal):
        raise RuntimeError(
            "Generated seed-42 calibration indices do not match the frozen release split."
        )
    if not np.array_equal(eval42, stored_eval):
        raise RuntimeError(
            "Generated seed-42 evaluation indices do not match the frozen release split."
        )

    print("Verified: generated seed-42 split matches the frozen release split exactly.")


def main(data_dir: str):
    data = Path(data_dir)

    V_msls = load(data / "msls_eigenplaces_visual.npy")
    L_msls = load(data / "msls_language.npy")
    P_msls = load(data / "msls_positive.npy").astype(bool)

    V_amster = load(data / "amstertime_eigenplaces_visual.npy")
    L_amster = load(data / "amstertime_language.npy")
    P_amster = load(data / "amstertime_positive.npy").astype(bool)

    V_nord = load(data / "nordland_eigenplaces_visual.npy")
    L_nord = load(data / "nordland_language.npy")
    P_nord = load(data / "nordland_positive.npy").astype(bool)

    if V_msls.shape[0] != N_MSLS:
        raise ValueError(
            f"Expected {N_MSLS} MSLS queries, found {V_msls.shape[0]}."
        )

    verify_primary_split(data)

    rows = []

    for seed in SEEDS:
        cal_idx, eval_idx = make_split(seed)

        best = select_pwf(
            V_msls[cal_idx],
            L_msls[cal_idx],
            P_msls[cal_idx],
        )

        rho = best["rho"]
        mc = best["M_c"]

        msls_r1, msls_r5, msls_r10 = evaluate(
            V_msls[eval_idx],
            L_msls[eval_idx],
            P_msls[eval_idx],
            rho,
            mc,
        )

        amster_r1, amster_r5, amster_r10 = evaluate(
            V_amster,
            L_amster,
            P_amster,
            rho,
            mc,
        )

        nord_r1, nord_r5, nord_r10 = evaluate(
            V_nord,
            L_nord,
            P_nord,
            rho,
            mc,
        )

        rows.append(
            {
                "seed": seed,
                "rho": rho,
                "M_c": mc,
                "calibration_R1": best["calibration_R1"],
                "MSLS_heldout_R1": msls_r1,
                "MSLS_heldout_R5": msls_r5,
                "MSLS_heldout_R10": msls_r10,
                "AmsterTime_R1": amster_r1,
                "AmsterTime_R5": amster_r5,
                "AmsterTime_R10": amster_r10,
                "Nordland_R1": nord_r1,
                "Nordland_R5": nord_r5,
                "Nordland_R10": nord_r10,
            }
        )

        print(
            f"seed={seed:4d}  rho={rho:>4}  M_c={mc:3d}  "
            f"MSLS R@1={msls_r1:6.2f}  "
            f"AmsterTime R@1={amster_r1:6.2f}  "
            f"Nordland R@1={nord_r1:6.2f}"
        )

    df = pd.DataFrame(rows)

    out = ROOT / "results" / "diagnostics" / "calibration_split_sensitivity_20seeds.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)

    print("\n20-split R@1 summary")
    for col in ["MSLS_heldout_R1", "AmsterTime_R1", "Nordland_R1"]:
        x = df[col].to_numpy()
        print(
            f"{col:18s}: mean={x.mean():.2f}, "
            f"SD={x.std(ddof=1):.2f}, "
            f"range=[{x.min():.2f}, {x.max():.2f}]"
        )

    print("\nPrimary seed-42 row")
    print(df.loc[df["seed"] == PRIMARY_SEED].to_string(index=False))

    print(f"\nSaved: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        required=True,
        help="Directory containing the locked reproducibility matrices.",
    )
    args = parser.parse_args()
    main(args.data_dir)
