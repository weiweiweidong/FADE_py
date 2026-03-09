"""Base protocol for FADE feature modules."""

from __future__ import annotations

from typing import Protocol

import numpy as np

from ..models.context import FeatureContext


class Feature(Protocol):
    """Protocol that every feature module must implement."""

    name: str

    def compute(self, context: FeatureContext) -> np.ndarray:
        """Return a per-patch 2-D feature map."""
        ...

