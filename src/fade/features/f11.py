"""f11: mean saturation."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f11 from FADE paper."""

    name = "f11"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.Is), axis=2)


feature = FeatureImpl()
