"""f09: patch-wise grayscale entropy."""

from __future__ import annotations

import numpy as np

from .base import Feature
from ..models.context import FeatureContext
from ..ops.entropy import patch_entropy


class FeatureImpl(Feature):
    """Feature f09 from FADE paper."""

    name = "f09"

    def compute(self, context: FeatureContext) -> np.ndarray:
        return patch_entropy(
            context.Ig_int,
            context.patch_row_num,
            context.patch_col_num,
            context.patch_size,
        )


feature = FeatureImpl()
