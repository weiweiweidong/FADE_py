"""Patch extraction helpers."""

from __future__ import annotations

import numpy as np


def to_patches(arr: np.ndarray, patch_row_num: int, patch_col_num: int, patch_size: int) -> np.ndarray:
    """Reshape a 2-D array into flattened non-overlapping patches."""
    arr = arr[: patch_row_num * patch_size, : patch_col_num * patch_size]
    return (
        arr.reshape(patch_row_num, patch_size, patch_col_num, patch_size)
        .transpose(0, 2, 1, 3)
        .reshape(patch_row_num, patch_col_num, patch_size * patch_size)
    )

