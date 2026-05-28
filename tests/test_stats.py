"""Tests for ``src/stats.py``."""

from __future__ import annotations

import numpy as np
import pytest

from src.stats import MeanCI, effective_sample_size, mean_with_ci, variance_of_total

SEED = 20260527


class TestMeanWithCI:
    def test_returns_mean_ci_dataclass(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(1000)
        result = mean_with_ci(samples)
        assert isinstance(result, MeanCI)

    def test_basic_coverage(self):
        """For a sample of size 10,000 from N(0, 1), the 95% CI should contain 0."""
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(10_000)
        result = mean_with_ci(samples, confidence=0.95)
        assert result.lower < 0 < result.upper

    def test_se_formula(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(10_000)
        result = mean_with_ci(samples)
        expected_se = samples.std(ddof=1) / np.sqrt(samples.size)
        assert result.se == pytest.approx(expected_se)

    def test_z_for_95pct(self):
        # half_width / se should be ~1.96
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(10_000)
        result = mean_with_ci(samples, confidence=0.95)
        assert result.half_width / result.se == pytest.approx(1.959964, rel=1e-3)

    def test_z_for_99pct(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(10_000)
        result = mean_with_ci(samples, confidence=0.99)
        assert result.half_width / result.se == pytest.approx(2.5758293, rel=1e-3)

    def test_widens_with_confidence(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(10_000)
        r90 = mean_with_ci(samples, confidence=0.90)
        r95 = mean_with_ci(samples, confidence=0.95)
        r99 = mean_with_ci(samples, confidence=0.99)
        assert r90.half_width < r95.half_width < r99.half_width

    def test_invalid_confidence(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(100)
        with pytest.raises(ValueError):
            mean_with_ci(samples, confidence=0.0)
        with pytest.raises(ValueError):
            mean_with_ci(samples, confidence=1.0)

    def test_too_few_samples(self):
        with pytest.raises(ValueError):
            mean_with_ci(np.array([1.0]))


class TestVarianceOfTotal:
    def test_matches_numpy(self):
        rng = np.random.default_rng(SEED)
        samples = rng.standard_normal(1000)
        assert variance_of_total(samples) == pytest.approx(samples.var(ddof=1))

    def test_too_few_samples(self):
        with pytest.raises(ValueError):
            variance_of_total(np.array([1.0]))


class TestEffectiveSampleSize:
    @pytest.mark.parametrize(
        "n, rho, expected",
        [
            (50, 0.0, 50.0),       # independent case: n_eff = n
            (50, 1.0, 1.0),        # perfect correlation: n_eff = 1
            (1, 0.5, 1.0),         # n = 1 edge case
            (50, 0.2, 50 / 10.8),  # ~4.63
            (50, 0.05, 50 / 3.45), # ~14.49
        ],
    )
    def test_known_values(self, n, rho, expected):
        assert effective_sample_size(n, rho) == pytest.approx(expected, rel=1e-6)

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            effective_sample_size(0, 0.5)

    def test_lower_psd_bound_returns_inf(self):
        n = 50
        rho = -1 / (n - 1)
        # 1 + (n - 1) * rho = 0 at the bound; formula diverges.
        assert effective_sample_size(n, rho) == float("inf")
