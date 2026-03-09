"""Entropy operators."""

from __future__ import annotations

import numpy as np


def patch_entropy(Ig_int: np.ndarray, patch_row_num: int, patch_col_num: int, patch_size: int) -> np.ndarray:
    """Compute Shannon entropy for each non-overlapping patch."""
    N = patch_row_num * patch_col_num
    area = patch_size * patch_size

    flat = (
        Ig_int[: patch_row_num * patch_size, : patch_col_num * patch_size]
        .reshape(patch_row_num, patch_size, patch_col_num, patch_size)
        .transpose(0, 2, 1, 3)
        .reshape(N, area)
    )

    offsets = np.arange(N, dtype=np.int32) * 256
    flat_idx = flat + offsets[:, np.newaxis]
    counts = np.bincount(flat_idx.ravel(), minlength=N * 256).reshape(N, 256).astype(np.float64)

    probs = counts / area
    with np.errstate(divide="ignore", invalid="ignore"):
        log_probs = np.where(probs > 0.0, np.log2(probs), 0.0)
    ent = -(probs * log_probs).sum(axis=1)
    return ent.reshape(patch_row_num, patch_col_num)

