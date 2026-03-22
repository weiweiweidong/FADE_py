"""Tests for all 12 feature modules (f01–f12)."""

from __future__ import annotations

import numpy as np
import pytest

from fade.features import f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f12


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

ALL_FEATURES = [
    f01.feature, f02.feature, f03.feature, f04.feature,
    f05.feature, f06.feature, f07.feature, f08.feature,
    f09.feature, f10.feature, f11.feature, f12.feature,
]

ALL_FEATURE_IDS = [f.name for f in ALL_FEATURES]


# ---------------------------------------------------------------------------
# Parametrised checks that apply to every feature
# ---------------------------------------------------------------------------

class TestAllFeaturesCommon:

    @pytest.mark.parametrize("feat", ALL_FEATURES, ids=ALL_FEATURE_IDS)
    def test_output_shape_standard(self, feat, standard_context):
        ctx = standard_context
        result = feat.compute(ctx)
        assert result.shape == (ctx.patch_row_num, ctx.patch_col_num)

    @pytest.mark.parametrize("feat", ALL_FEATURES, ids=ALL_FEATURE_IDS)
    def test_output_shape_tiny(self, feat, tiny_context):
        ctx = tiny_context
        result = feat.compute(ctx)
        assert result.shape == (ctx.patch_row_num, ctx.patch_col_num)

    @pytest.mark.parametrize("feat", ALL_FEATURES, ids=ALL_FEATURE_IDS)
    def test_reproducible(self, feat, standard_context):
        r1 = feat.compute(standard_context)
        r2 = feat.compute(standard_context)
        np.testing.assert_array_equal(r1, r2)

    @pytest.mark.parametrize("feat", ALL_FEATURES, ids=ALL_FEATURE_IDS)
    def test_returns_2d_array(self, feat, standard_context):
        result = feat.compute(standard_context)
        assert result.ndim == 2

    @pytest.mark.parametrize("feat", ALL_FEATURES, ids=ALL_FEATURE_IDS)
    def test_dtype_is_float(self, feat, standard_context):
        result = feat.compute(standard_context)
        assert np.issubdtype(result.dtype, np.floating)


# ---------------------------------------------------------------------------
# Feature-specific value range and semantics
# ---------------------------------------------------------------------------

class TestF01MscnVariance:

    def test_nonnegative(self, standard_context):
        result = f01.feature.compute(standard_context)
        # nanvar can produce NaN for patches with <2 valid values, but not negative
        valid = result[~np.isnan(result)]
        assert np.all(valid >= 0)

    def test_uniform_image_near_zero(self, uniform_context):
        """Uniform MSCN → nearly zero variance per patch."""
        result = f01.feature.compute(uniform_context)
        valid = result[~np.isnan(result)]
        assert np.all(valid < 0.01)


class TestF02F03MscnProducts:
    """f02 (non-negative) and f03 (non-positive) MSCN vertical products."""

    def test_f02_nonnegative_where_finite(self, standard_context):
        result = f02.feature.compute(standard_context)
        valid = result[np.isfinite(result)]
        assert np.all(valid >= 0)

    def test_f03_nonnegative_where_finite(self, standard_context):
        result = f03.feature.compute(standard_context)
        valid = result[np.isfinite(result)]
        assert np.all(valid >= 0)

    def test_f02_uniform_no_crash(self, uniform_context):
        """Should not raise even when all values are NaN."""
        result = f02.feature.compute(uniform_context)
        assert result.shape == (uniform_context.patch_row_num, uniform_context.patch_col_num)

    def test_f03_uniform_no_crash(self, uniform_context):
        result = f03.feature.compute(uniform_context)
        assert result.shape == (uniform_context.patch_row_num, uniform_context.patch_col_num)


class TestF04F05LocalStats:

    def test_f04_sigma_mean_nonnegative(self, standard_context):
        result = f04.feature.compute(standard_context)
        assert np.all(result >= 0)

    def test_f05_cv_mean_nonnegative(self, standard_context):
        result = f05.feature.compute(standard_context)
        assert np.all(result >= 0)

    def test_f04_uniform_near_zero(self, uniform_context):
        """Uniform image has nearly zero local std in interior."""
        result = f04.feature.compute(uniform_context)
        assert np.max(result) < 1.0


class TestF06F07F08ContrastEnergy:

    def test_f06_nonnegative(self, standard_context):
        assert np.all(f06.feature.compute(standard_context) >= 0)

    def test_f07_nonnegative(self, standard_context):
        assert np.all(f07.feature.compute(standard_context) >= 0)

    def test_f08_nonnegative(self, standard_context):
        assert np.all(f08.feature.compute(standard_context) >= 0)

    def test_f06_uniform_zero(self, uniform_context):
        np.testing.assert_allclose(f06.feature.compute(uniform_context), 0.0)

    def test_f07_uniform_zero(self, uniform_context):
        np.testing.assert_allclose(f07.feature.compute(uniform_context), 0.0)

    def test_f08_uniform_zero(self, uniform_context):
        np.testing.assert_allclose(f08.feature.compute(uniform_context), 0.0)


class TestF09Entropy:

    def test_range_0_to_8(self, standard_context):
        result = f09.feature.compute(standard_context)
        assert np.all(result >= 0.0)
        assert np.all(result <= 8.0 + 1e-10)

    def test_no_nan_no_inf(self, standard_context):
        result = f09.feature.compute(standard_context)
        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))

    def test_uniform_image_entropy_zero(self, uniform_context):
        result = f09.feature.compute(uniform_context)
        np.testing.assert_allclose(result, 0.0, atol=1e-10)


class TestF10DarkChannel:

    def test_range_0_to_1(self, standard_context):
        result = f10.feature.compute(standard_context)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0 + 1e-6)

    def test_uniform_128_value(self, uniform_context):
        result = f10.feature.compute(uniform_context)
        np.testing.assert_allclose(result, 128.0 / 255.0, rtol=1e-4)


class TestF11Saturation:

    def test_range_0_to_1(self, standard_context):
        result = f11.feature.compute(standard_context)
        assert np.all(result >= 0.0)
        assert np.all(result <= 1.0 + 1e-6)

    def test_uniform_gray_saturation_zero(self, uniform_context):
        result = f11.feature.compute(uniform_context)
        np.testing.assert_allclose(result, 0.0, atol=1e-6)


class TestF12Colorfulness:

    def test_nonnegative(self, standard_context):
        result = f12.feature.compute(standard_context)
        assert np.all(result >= 0)

    def test_no_nan_no_inf(self, standard_context):
        result = f12.feature.compute(standard_context)
        assert not np.any(np.isnan(result))
        assert not np.any(np.isinf(result))

    def test_uniform_gray_colorfulness_near_zero(self, uniform_context):
        """Gray image (R=G=B) has zero rg and by variance → colorfulness ≈ 0."""
        result = f12.feature.compute(uniform_context)
        np.testing.assert_allclose(result, 0.0, atol=1e-6)
