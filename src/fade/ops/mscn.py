"""MSCN-related operators."""

from __future__ import annotations

import numpy as np
from scipy import ndimage


def gaussian_window(size: int = 7, sigma: float | None = None) -> np.ndarray:
    """Build a normalized 2-D Gaussian kernel."""
    if sigma is None:
        sigma = size / 6.0
    center = size // 2
    y, x = np.mgrid[0:size, 0:size] - center
    kernel = np.exp(-(x**2 + y**2) / (2.0 * sigma**2))
    return kernel / kernel.sum()


def compute_mscn_components(Ig_f: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute MSCN map, local sigma map, and coefficient of variation."""
    win = gaussian_window(size=7, sigma=7.0 / 6.0)
    mu = ndimage.convolve(Ig_f, win, mode="nearest")
    sigma_map = np.sqrt(np.abs(ndimage.convolve(Ig_f * Ig_f, win, mode="nearest") - mu * mu))
    mscn = (Ig_f - mu) / (sigma_map + 1.0)
    cv = sigma_map / mu
    return mscn, sigma_map, cv

