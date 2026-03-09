"""f08: mean contrast energy on red-green channel."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f08 from FADE paper."""

    name = "f08"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.CE_rg), axis=2)


feature = FeatureImpl()
