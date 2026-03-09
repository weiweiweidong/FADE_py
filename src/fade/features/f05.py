"""f05: mean coefficient of variation."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f05 from FADE paper."""

    name = "f05"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.cv), axis=2)


feature = FeatureImpl()
