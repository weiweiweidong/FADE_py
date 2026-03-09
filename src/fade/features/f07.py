"""f07: mean contrast energy on blue-yellow channel."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f07 from FADE paper."""

    name = "f07"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.CE_by), axis=2)


feature = FeatureImpl()
