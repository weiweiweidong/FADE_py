"""f02: variance of non-negative vertical MSCN products."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext


class FeatureImpl(Feature):
    """Feature f02 from FADE paper."""

    name = "f02"

    def compute(self, context: FeatureContext) -> np.ndarray:
        with np.errstate(invalid="ignore", divide="ignore"):
            tmp = context.mscn_v_patches.copy()
            tmp[tmp < 0] = np.nan
            return np.nanvar(tmp, axis=2, ddof=1)


feature = FeatureImpl()
