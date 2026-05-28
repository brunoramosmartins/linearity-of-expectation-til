"""Tests for ``src/correlated.py``."""

from __future__ import annotations

import numpy as np
import pytest

from src.correlated import (
    lognormal_correlation_from_gaussian,
    lognormal_parameters_from_moments,
    min_equicorrelation,
    sample_correlated_lognormals,
)

SEED = 20260527


# ──────────────────────────────────────────────────────────────────────────────
# Parameter conversion
# ──────────────────────────────────────────────────────────────────────────────


class TestLognormalParameters:
    def test_roundtrip_moments(self):
        # Pick target moments, solve for (mu, sigma), check that the LogNormal
        # with those parameters has the requested moments.
        target_mean = 10_000.0
        target_var = 4_000_000.0
        mu, sigma = lognormal_parameters_from_moments(target_mean, target_var)
        recovered_mean = np.exp(mu + sigma**2 / 2)
        recovered_var = (np.exp(sigma**2) - 1) * np.exp(2 * mu + sigma**2)
        assert recovered_mean == pytest.approx(target_mean, rel=1e-10)
        assert recovered_var == pytest.approx(target_var, rel=1e-10)

    def test_zero_variance(self):
        mu, sigma = lognormal_parameters_from_moments(100.0, 0.0)
        assert sigma == pytest.approx(0.0)
        assert mu == pytest.approx(np.log(100.0))

    def test_invalid_mean(self):
        with pytest.raises(ValueError):
            lognormal_parameters_from_moments(0.0, 1.0)
        with pytest.raises(ValueError):
            lognormal_parameters_from_moments(-1.0, 1.0)

    def test_invalid_variance(self):
        with pytest.raises(ValueError):
            lognormal_parameters_from_moments(10.0, -0.1)


class TestCorrelationMapping:
    def test_zero_rho(self):
        # rho_Z = 0 should give rho_X = 0
        assert lognormal_correlation_from_gaussian(0.0, 0.2) == pytest.approx(0.0, abs=1e-12)

    def test_unit_rho(self):
        # rho_Z = 1 should give rho_X = 1
        assert lognormal_correlation_from_gaussian(1.0, 0.2) == pytest.approx(1.0)

    def test_small_sigma_close_to_identity(self):
        # For small sigma_log, rho_X ≈ rho_Z
        for rho_z in [-0.3, 0.1, 0.5, 0.9]:
            rho_x = lognormal_correlation_from_gaussian(rho_z, 0.1)
            assert abs(rho_x - rho_z) < 0.01


# ──────────────────────────────────────────────────────────────────────────────
# PSD lower bound
# ──────────────────────────────────────────────────────────────────────────────


class TestMinEquicorrelation:
    @pytest.mark.parametrize("n,expected", [(2, -1.0), (5, -0.25), (50, -1 / 49)])
    def test_known_values(self, n, expected):
        assert min_equicorrelation(n) == pytest.approx(expected)

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            min_equicorrelation(1)


# ──────────────────────────────────────────────────────────────────────────────
# Sampling: marginal moments preserved across rho
# ──────────────────────────────────────────────────────────────────────────────


class TestSampler:
    def setup_method(self):
        self.target_mean = 10_000.0
        self.target_var = 4_000_000.0
        self.mu, self.sigma = lognormal_parameters_from_moments(
            self.target_mean, self.target_var
        )

    def test_shape(self):
        rng = np.random.default_rng(SEED)
        samples = sample_correlated_lognormals(
            n=50, rho=0.2, mu_log=self.mu, sigma_log=self.sigma, size=1000, rng=rng
        )
        assert samples.shape == (1000, 50)

    @pytest.mark.parametrize("rho", [0.0, 0.2, 0.5, 0.9])
    def test_marginal_mean_invariant(self, rho):
        """The marginal mean of each S_i must not depend on rho (linearity)."""
        rng = np.random.default_rng(SEED)
        n = 50
        samples = sample_correlated_lognormals(
            n=n, rho=rho, mu_log=self.mu, sigma_log=self.sigma, size=20_000, rng=rng
        )
        sample_mean = samples.mean()  # averages across all entries
        # Tolerance ~ 1% of target mean (relative)
        assert abs(sample_mean - self.target_mean) / self.target_mean < 0.01

    @pytest.mark.parametrize("rho", [0.0, 0.2, 0.5, 0.9])
    def test_marginal_variance_invariant(self, rho):
        """The marginal variance of each S_i must not depend on rho."""
        rng = np.random.default_rng(SEED)
        n = 50
        samples = sample_correlated_lognormals(
            n=n, rho=rho, mu_log=self.mu, sigma_log=self.sigma, size=20_000, rng=rng
        )
        # Per-column variance — averaged across columns to reduce noise.
        per_col_var = samples.var(axis=0, ddof=1).mean()
        assert abs(per_col_var - self.target_var) / self.target_var < 0.05

    def test_total_mean_invariant_across_rho(self):
        """E[sum S_i] = n * E[S_i] = 50 * 10,000 = 500,000 for every rho."""
        n = 50
        target_total = n * self.target_mean
        for rho in [-0.01, 0.0, 0.2, 0.5, 0.9]:
            rng = np.random.default_rng(SEED + int(round(rho * 100)))
            samples = sample_correlated_lognormals(
                n=n, rho=rho, mu_log=self.mu, sigma_log=self.sigma,
                size=10_000, rng=rng,
            )
            totals = samples.sum(axis=1)
            sample_mean_total = totals.mean()
            # SE of the mean is sqrt(Var(total) / K). For rho up to 0.9,
            # Var(total) can be up to ~50 * sigma^2 * 50 = 2500 * sigma^2.
            # Use a generous 3% tolerance.
            assert abs(sample_mean_total - target_total) / target_total < 0.03

    def test_total_variance_grows_with_rho(self):
        """Var(sum S_i) increases with rho across {0, 0.2, 0.5, 0.9}."""
        n = 50
        prior_var = None
        for rho in [0.0, 0.2, 0.5, 0.9]:
            rng = np.random.default_rng(SEED + 1)
            samples = sample_correlated_lognormals(
                n=n, rho=rho, mu_log=self.mu, sigma_log=self.sigma,
                size=10_000, rng=rng,
            )
            totals = samples.sum(axis=1)
            var = totals.var(ddof=1)
            if prior_var is not None:
                assert var > prior_var * 1.5  # variance should jump substantially
            prior_var = var

    def test_negative_rho_variance_below_independent(self):
        """At rho = -1/(n-1) + small slack, Var(sum) drops well below the independent case."""
        n = 50
        rng = np.random.default_rng(SEED + 2)
        independent_samples = sample_correlated_lognormals(
            n=n, rho=0.0, mu_log=self.mu, sigma_log=self.sigma, size=10_000, rng=rng,
        )
        rng = np.random.default_rng(SEED + 3)
        neg_samples = sample_correlated_lognormals(
            n=n, rho=-1 / (n - 1) + 0.001, mu_log=self.mu, sigma_log=self.sigma,
            size=10_000, rng=rng,
        )
        var_ind = independent_samples.sum(axis=1).var(ddof=1)
        var_neg = neg_samples.sum(axis=1).var(ddof=1)
        assert var_neg < var_ind  # negative correlation reduces variance of sum

    def test_invalid_rho_above(self):
        rng = np.random.default_rng(SEED)
        with pytest.raises(ValueError):
            sample_correlated_lognormals(
                n=10, rho=1.5, mu_log=self.mu, sigma_log=self.sigma, size=100, rng=rng,
            )

    def test_invalid_rho_below_bound(self):
        rng = np.random.default_rng(SEED)
        # n = 10 → bound is -1/9 ≈ -0.111
        with pytest.raises(ValueError):
            sample_correlated_lognormals(
                n=10, rho=-0.5, mu_log=self.mu, sigma_log=self.sigma, size=100, rng=rng,
            )
