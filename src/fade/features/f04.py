"""f04: mean local standard deviation."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f04 from FADE paper."""

    name = "f04"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.sigma_map), axis=2)


feature = FeatureImpl()
