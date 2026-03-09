"""Public API for FADE."""

from __future__ import annotations

from typing import Tuple

import numpy as np

from .pipeline import FadePipeline

_default_pipeline = FadePipeline.default()


def fade(I: np.ndarray) -> float:
    """Compute FADE score for an RGB image."""
    score, _ = _default_pipeline.run(I)
    return score


def fade_with_map(I: np.ndarray) -> Tuple[float, np.ndarray]:
    """Compute FADE score and per-patch fog-density map."""
    return _default_pipeline.run(I)

