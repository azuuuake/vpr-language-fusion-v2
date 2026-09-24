"""Statistical utilities matching the reported analysis."""
from __future__ import annotations
import numpy as np


def bh_fdr(p_values):
    p = np.asarray(p_values, dtype=float)
    order = np.argsort(p)
    q = np.empty_like(p)
    prev = 1.0
    m = len(p)
    for rank_i in range(m - 1, -1, -1):
        idx = order[rank_i]
        prev = min(prev, p[idx] * m / (rank_i + 1))
        q[idx] = min(prev, 1.0)
    return q


def paired_bootstrap(a, b, B=5000, seed=42):
    a = np.asarray(a, dtype=bool); b = np.asarray(b, dtype=bool)
    if len(a) != len(b): raise ValueError("paired arrays must have equal length")
    n = len(a); point = 100.0 * (a.mean() - b.mean())
    rng = np.random.default_rng(seed)
    diffs = np.empty(B)
    for i in range(B):
        ix = rng.integers(0, n, n)
        diffs[i] = 100.0 * (a[ix].mean() - b[ix].mean())
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    tail = np.sum(diffs <= 0) if point >= 0 else np.sum(diffs >= 0)
    p = min(1.0, 2.0 * (tail + 1) / (B + 1))
    return point, lo, hi, p
