"""f12: colorfulness."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f12 from FADE paper."""

    name = "f12"

    def compute(self, context: FeatureContext) -> np.ndarray:
        rg_p = context.to_patches(context.rg)
        by_p = context.to_patches(context.by)

        rg_std = np.std(rg_p, axis=2, ddof=1)
        by_std = np.std(by_p, axis=2, ddof=1)
        rg_mean = np.mean(rg_p, axis=2)
        by_mean = np.mean(by_p, axis=2)
        return np.sqrt(rg_std**2 + by_std**2) + 0.3 * np.sqrt(rg_mean**2 + by_mean**2)


feature = FeatureImpl()
