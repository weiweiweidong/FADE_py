"""Reference statistics loader for fog-free/foggy feature distributions."""

from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
from typing import Any

import scipy.io


@lru_cache(maxsize=1)
def load_reference_stats() -> tuple[dict[str, Any], dict[str, Any]]:
    """Load and cache reference `.mat` statistics."""
    data_dir = files("fade").joinpath("data")
    fogfree = scipy.io.loadmat(str(data_dir / "natural_fogfree_image_features_ps8.mat"))
    foggy = scipy.io.loadmat(str(data_dir / "natural_foggy_image_features_ps8.mat"))
    return fogfree, foggy

