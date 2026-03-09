"""f10: mean dark channel."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f10 from FADE paper."""

    name = "f10"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.mean(context.to_patches(context.Id), axis=2)


feature = FeatureImpl()
