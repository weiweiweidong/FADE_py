"""f01: MSCN patch variance."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f01 from FADE paper."""

    name = "f01"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return np.nanvar(context.to_patches(context.mscn), axis=2, ddof=1)


feature = FeatureImpl()
