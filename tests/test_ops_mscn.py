"""Tests for ops/mscn.py — gaussian_window and compute_mscn_components."""

from __future__ import annotations

import numpy as np
import pytest

from fade.ops.mscn import compute_mscn_components, gaussian_window


# ---------------------------------------------------------------------------
# gaussian_window
# ---------------------------------------------------------------------------

class TestGaussianWindow:

    def test_shape_default(self):
        w = gaussian_window()
        assert w.shape == (7, 7)

    @pytest.mark.parametrize("size", [5, 7, 11])
    def test_sums_to_one(self, size):
        w = gaussian_window(size=size)
        assert abs(w.sum() - 1.0) < 1e-12

    def test_all_positive(self):
        w = gaussian_window(size=7)
        assert np.all(w > 0)

    def test_symmetric(self):
        w = gaussian_window(size=7)
        np.testing.assert_array_equal(w, w.T)

    def test_symmetric_horizontal(self):
        w = gaussian_window(size=7)
        np.testing.assert_array_almost_equal(w, w[:, ::-1])

    def test_center_is_max(self):
        w = gaussian_window(size=7)
        assert w[3, 3] == w.max()

    def test_default_sigma_equals_size_over_six(self):
        w_default = gaussian_window(size=7)
        w_explicit = gaussian_window(size=7, sigma=7.0 / 6.0)
        np.testing.assert_array_almost_equal(w_default, w_explicit)

    def test_smaller_sigma_more_peaked(self):
        w_narrow = gaussian_window(size=7, sigma=1.0)
        w_wide = gaussian_window(size=7, sigma=2.0)
        assert w_narrow[3, 3] > w_wide[3, 3]

    def test_custom_size(self):
        w = gaussian_window(size=5, sigma=1.0)
        assert w.shape == (5, 5)
        assert abs(w.sum() - 1.0) < 1e-12


# ---------------------------------------------------------------------------
# compute_mscn_components
# ---------------------------------------------------------------------------

class TestComputeMscnComponents:

    def _make_float(self, img: np.ndarray) -> np.ndarray:
        from fade.models.context import FeatureContext
        ctx = FeatureContext(image=img)
        return ctx.Ig_int.astype(np.float64)

    def test_output_shapes_match_input(self, standard_rgb):
        Ig_f = self._make_float(standard_rgb)
        mscn, sigma_map, cv = compute_mscn_components(Ig_f)
        assert mscn.shape == Ig_f.shape
        assert sigma_map.shape == Ig_f.shape
        assert cv.shape == Ig_f.shape

    def test_sigma_map_nonnegative(self, standard_rgb):
        Ig_f = self._make_float(standard_rgb)
        _, sigma_map, _ = compute_mscn_components(Ig_f)
        assert np.all(sigma_map >= 0)

    def test_no_nan_inf_for_random_image(self, standard_rgb):
        Ig_f = self._make_float(standard_rgb)
        mscn, sigma_map, _ = compute_mscn_components(Ig_f)
        assert not np.any(np.isnan(mscn))
        assert not np.any(np.isinf(mscn))
        assert not np.any(np.isnan(sigma_map))
        assert not np.any(np.isinf(sigma_map))

    def test_uniform_image_mscn_near_zero(self, uniform_rgb):
        """Interior pixels of a uniform image should have MSCN ≈ 0."""
        Ig_f = self._make_float(uniform_rgb)
        mscn, _, _ = compute_mscn_components(Ig_f)
        interior = mscn[3:-3, 3:-3]
        assert np.max(np.abs(interior)) < 0.01

    def test_uniform_image_no_nan(self, uniform_rgb):
        """sigma+1 offset ensures MSCN is finite even when sigma=0."""
        Ig_f = self._make_float(uniform_rgb)
        mscn, _, _ = compute_mscn_components(Ig_f)
        assert not np.any(np.isnan(mscn))
        assert not np.any(np.isinf(mscn))

    def test_mscn_reasonable_range_natural_image(self, standard_rgb):
        """MSCN values for natural images should be well within [-20, 20]."""
        Ig_f = self._make_float(standard_rgb)
        mscn, _, _ = compute_mscn_components(Ig_f)
        assert np.all(mscn > -20)
        assert np.all(mscn < 20)

    def test_sigma_map_uniform_image_near_zero(self, uniform_rgb):
        """Uniform image has no local variation → sigma ≈ 0 in interior."""
        Ig_f = self._make_float(uniform_rgb)
        _, sigma_map, _ = compute_mscn_components(Ig_f)
        interior = sigma_map[3:-3, 3:-3]
        assert np.max(interior) < 1.0

    def test_reproducible(self, standard_rgb):
        Ig_f = self._make_float(standard_rgb)
        mscn1, s1, cv1 = compute_mscn_components(Ig_f)
        mscn2, s2, cv2 = compute_mscn_components(Ig_f)
        np.testing.assert_array_equal(mscn1, mscn2)
        np.testing.assert_array_equal(s1, s2)
        np.testing.assert_array_equal(cv1, cv2)
