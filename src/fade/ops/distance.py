"""Distance operators."""

from __future__ import annotations

import numpy as np


def batch_mahalanobis(mu_matrix: np.ndarray, patch_var: np.ndarray, ref_cov: np.ndarray) -> np.ndarray:
    """Compute batched Mahalanobis distances for all patches."""
    feature_size = mu_matrix.shape[1]
    batch_cov = (patch_var[:, np.newaxis, np.newaxis] * np.ones((feature_size, feature_size)) + ref_cov) / 2.0
    mu_col = mu_matrix[:, :, np.newaxis]
    x = np.linalg.solve(batch_cov, mu_col)
    dist_sq = np.einsum("ni,ni->n", mu_matrix, x[:, :, 0])
    return np.sqrt(np.maximum(dist_sq, 0.0))

