"""Shared pytest fixtures for FADE test suite."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

# ---------------------------------------------------------------------------
# Synthetic image fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def rng() -> np.random.Generator:
    """Seeded RNG for reproducible random images."""
    return np.random.default_rng(42)


@pytest.fixture(scope="session")
def tiny_rgb(rng: np.random.Generator) -> np.ndarray:
    """16×16×3 uint8 — 2×2 patch grid. Minimal valid input."""
    return rng.integers(0, 256, (16, 16, 3), dtype=np.uint8)


@pytest.fixture(scope="session")
def standard_rgb(rng: np.random.Generator) -> np.ndarray:
    """64×80×3 uint8 — 8×10 patch grid. Standard unit-test image."""
    return rng.integers(0, 256, (64, 80, 3), dtype=np.uint8)


@pytest.fixture(scope="session")
def nonaligned_rgb(rng: np.random.Generator) -> np.ndarray:
    """70×75×3 uint8 — not divisible by 8. Tests cropping logic."""
    return rng.integers(0, 256, (70, 75, 3), dtype=np.uint8)


@pytest.fixture(scope="session")
def uniform_rgb() -> np.ndarray:
    """Pure gray (128,128,128) — constant-valued, degenerate edge case."""
    return np.full((32, 32, 3), 128, dtype=np.uint8)


@pytest.fixture(scope="session")
def checkerboard_rgb() -> np.ndarray:
    """8×8 checkerboard pattern — maximises local contrast."""
    checker = (np.indices((64, 64)).sum(axis=0) % 2).astype(np.uint8)
    return np.stack([checker * 255] * 3, axis=-1)


# ---------------------------------------------------------------------------
# FeatureContext fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session")
def tiny_context(tiny_rgb: np.ndarray):
    from fade.models.context import FeatureContext
    return FeatureContext(image=tiny_rgb)


@pytest.fixture(scope="session")
def standard_context(standard_rgb: np.ndarray):
    from fade.models.context import FeatureContext
    return FeatureContext(image=standard_rgb)


@pytest.fixture(scope="session")
def uniform_context(uniform_rgb: np.ndarray):
    from fade.models.context import FeatureContext
    return FeatureContext(image=uniform_rgb)


# ---------------------------------------------------------------------------
# Real-image fixtures (slow — require disk I/O)
# ---------------------------------------------------------------------------

TEST_IMAGE_DIR = Path(__file__).parent.parent / "test_image"


def _load_image(path: Path) -> np.ndarray:
    import matplotlib.pyplot as plt
    img = plt.imread(str(path))
    if img.dtype != np.uint8:
        img = (img * 255).clip(0, 255).astype(np.uint8)
    return img[:, :, :3]


@pytest.fixture(scope="session")
def real_clear_image() -> np.ndarray:
    """Clear scene — expected FADE ≈ 0.91."""
    return _load_image(TEST_IMAGE_DIR / "test_image1.png")


@pytest.fixture(scope="session")
def real_moderate_fog_image() -> np.ndarray:
    """Moderate fog — expected FADE ≈ 2.71."""
    return _load_image(TEST_IMAGE_DIR / "test_image2.JPG")


@pytest.fixture(scope="session")
def real_dense_fog_image() -> np.ndarray:
    """Dense fog — expected FADE ≈ 5.77."""
    return _load_image(TEST_IMAGE_DIR / "test_image3.jpg")
