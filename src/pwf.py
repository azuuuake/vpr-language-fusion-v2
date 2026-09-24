"""
This file implements the equations and fixed conventions reported in the paper. It operates on precomputed visual/language similarity matrices.
"""
from __future__ import annotations
import numpy as np

EPS = 1e-9
DEFAULT_LAMBDA = 0.5
DEFAULT_KU = 10


def topk_idx(scores: np.ndarray, k: int) -> np.ndarray:
    """Stable descending top-k indices."""
    return np.argsort(-np.asarray(scores), axis=1, kind="stable")[:, :k]


def statistical_uncertainty(sorted_scores: np.ndarray, lam: float = DEFAULT_LAMBDA,
                            eps: float = EPS) -> np.ndarray:
    """SU/LU statistic: lambda*RS + (1-lambda)*SD; input is descending per row."""
    x = np.asarray(sorted_scores, dtype=float)
    if x.ndim != 2 or x.shape[1] < 2:
        raise ValueError("sorted_scores must have shape (N,K), K>=2")
    best = x[:, [0]]
    rs = np.mean(x[:, 1:] / (best + eps), axis=1)
    sd = np.median(x, axis=1) / (x[:, 0] + eps)
    return lam * rs + (1.0 - lam) * sd


def _z(x: np.ndarray, eps: float = EPS) -> np.ndarray:
    return (x - x.mean()) / (x.std() + eps)


def pwf_retrieve(V: np.ndarray, L: np.ndarray, rho: float, mc: int = 10,
                 ku: int = DEFAULT_KU, lam: float = DEFAULT_LAMBDA,
                 eps: float = EPS, su_only: bool = False):
    """PWF candidate reranking. Returns (ranked database indices, visual alpha)."""
    idx = topk_idx(V, mc)
    v = np.take_along_axis(V, idx, axis=1)
    l = np.take_along_axis(L, idx, axis=1)
    if mc < ku:
        raise ValueError("M_c must be >= K_u")
    # Visual top candidates are already in descending visual order.
    su = statistical_uncertainty(v[:, :ku], lam, eps)
    lu_scores = np.sort(l[:, :ku], axis=1)[:, ::-1]
    lu = statistical_uncertainty(lu_scores, lam, eps)
    suz = _z(su, eps)
    luz = np.zeros_like(lu) if su_only else _z(lu, eps)
    sigma_v2 = np.logaddexp(0.0, suz) + eps
    sigma_l2 = np.logaddexp(0.0, luz) + eps
    alpha = rho * sigma_l2 / (sigma_v2 + rho * sigma_l2 + eps)
    fused = alpha[:, None] * v + (1.0 - alpha[:, None]) * l
    order = np.argsort(-fused, axis=1, kind="stable")
    return np.take_along_axis(idx, order, axis=1), alpha


def constant_top10(V: np.ndarray, L: np.ndarray, alpha: float):
    idx = topk_idx(V, 10)
    v = np.take_along_axis(V, idx, axis=1)
    l = np.take_along_axis(L, idx, axis=1)
    fused = alpha * v + (1.0 - alpha) * l
    order = np.argsort(-fused, axis=1, kind="stable")
    return np.take_along_axis(idx, order, axis=1)


def sigmoid_gated_top10(V: np.ndarray, L: np.ndarray, tau: float, theta: float,
                        lam: float = DEFAULT_LAMBDA, eps: float = EPS):
    idx = topk_idx(V, 10)
    v = np.take_along_axis(V, idx, axis=1)
    l = np.take_along_axis(L, idx, axis=1)
    su = statistical_uncertainty(v, lam, eps)
    z = _z(su, eps)
    alpha = 1.0 / (1.0 + np.exp(z / tau))
    alpha = np.where(l.std(axis=1) >= theta, alpha, 1.0)
    fused = alpha[:, None] * v + (1.0 - alpha[:, None]) * l
    order = np.argsort(-fused, axis=1, kind="stable")
    return np.take_along_axis(idx, order, axis=1), alpha


def correct_at_k(ranked: np.ndarray, positive: np.ndarray, k: int) -> np.ndarray:
    return np.any(np.take_along_axis(positive, ranked[:, :k], axis=1), axis=1)


def recalls(ranked: np.ndarray, positive: np.ndarray, ks=(1,5,10)):
    return {f"R@{k}": 100.0 * correct_at_k(ranked, positive, k).mean() for k in ks}
