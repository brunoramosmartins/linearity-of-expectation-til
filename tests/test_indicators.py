"""Tests for ``src/indicators.py``.

Two kinds of checks:

1. **Unit checks** on the exact-value functions and the simulators' invariants
   (return types, value ranges, edge cases).
2. **Statistical checks** that empirical means converge to the closed-form
   expectations. Sample sizes are chosen so the 4-sigma confidence interval
   safely contains the true mean — failures should be rare under correct code.
"""

from __future__ import annotations

import numpy as np
import pytest

from src.indicators import (
    count_inversions,
    empirical_mean,
    expected_coupon_collector,
    expected_hat_check,
    expected_inversions,
    expected_triangles_gnp,
    simulate_coupon_collector,
    simulate_hat_check,
    simulate_inversions,
    simulate_triangles_gnp,
)

SEED = 20260525  # fixed for reproducibility of statistical checks


# ──────────────────────────────────────────────────────────────────────────────
# Exact-value functions
# ──────────────────────────────────────────────────────────────────────────────


class TestExpectedValues:
    def test_coupon_collector_small(self):
        # n=1: must draw exactly 1 coupon; n=2: H_2 = 1.5 so E[T] = 3
        assert expected_coupon_collector(1) == pytest.approx(1.0)
        assert expected_coupon_collector(2) == pytest.approx(3.0)

    def test_coupon_collector_n10(self):
        # H_10 ≈ 2.928968 → E[T] ≈ 29.28968
        assert expected_coupon_collector(10) == pytest.approx(29.28968, rel=1e-5)

    def test_hat_check_invariant(self):
        # E[F] = 1 for every n >= 1
        for n in [1, 2, 5, 10, 100, 1000]:
            assert expected_hat_check(n) == 1.0

    def test_inversions_formula(self):
        # E[I] = n(n-1)/4
        assert expected_inversions(2) == pytest.approx(0.5)
        assert expected_inversions(10) == pytest.approx(22.5)
        assert expected_inversions(100) == pytest.approx(2475.0)

    def test_triangles_gnp_formula(self):
        # E[T] = C(n,3) * p^3
        assert expected_triangles_gnp(10, 0.5) == pytest.approx(120 * 0.125)
        assert expected_triangles_gnp(100, 0.1) == pytest.approx(161700 * 1e-3)

    def test_triangles_gnp_small_n(self):
        # n < 3 has no triangles
        assert expected_triangles_gnp(1, 0.5) == 0.0
        assert expected_triangles_gnp(2, 0.5) == 0.0

    @pytest.mark.parametrize("bad_n", [0, -1])
    def test_negative_n_raises(self, bad_n):
        with pytest.raises(ValueError):
            expected_coupon_collector(bad_n)
        with pytest.raises(ValueError):
            expected_hat_check(bad_n)
        with pytest.raises(ValueError):
            expected_inversions(bad_n)

    @pytest.mark.parametrize("bad_p", [-0.1, 1.1])
    def test_bad_p_raises(self, bad_p):
        with pytest.raises(ValueError):
            expected_triangles_gnp(10, bad_p)


# ──────────────────────────────────────────────────────────────────────────────
# Simulator invariants
# ──────────────────────────────────────────────────────────────────────────────


class TestSimulatorInvariants:
    def setup_method(self):
        self.rng = np.random.default_rng(SEED)

    def test_coupon_collector_returns_at_least_n(self):
        for n in [1, 5, 20]:
            t = simulate_coupon_collector(n, self.rng)
            assert isinstance(t, int)
            assert t >= n  # cannot collect n distinct coupons in fewer than n draws

    def test_hat_check_returns_in_range(self):
        for n in [1, 5, 50]:
            f = simulate_hat_check(n, self.rng)
            assert isinstance(f, int)
            assert 0 <= f <= n

    def test_inversions_returns_in_range(self):
        for n in [1, 5, 50]:
            inv = simulate_inversions(n, self.rng)
            assert isinstance(inv, int)
            assert 0 <= inv <= n * (n - 1) // 2

    def test_count_inversions_sorted_is_zero(self):
        assert count_inversions(np.array([0, 1, 2, 3, 4])) == 0

    def test_count_inversions_reverse_is_max(self):
        n = 5
        # reversed: every pair is inverted
        assert count_inversions(np.array([4, 3, 2, 1, 0])) == n * (n - 1) // 2

    def test_triangles_gnp_range(self):
        for n in [3, 5, 10]:
            t = simulate_triangles_gnp(n, 0.5, self.rng)
            assert isinstance(t, int)
            assert 0 <= t <= n * (n - 1) * (n - 2) // 6

    def test_triangles_gnp_p_zero(self):
        # No edges → no triangles
        for n in [3, 5, 20]:
            assert simulate_triangles_gnp(n, 0.0, self.rng) == 0

    def test_triangles_gnp_p_one(self):
        # Complete graph → C(n, 3) triangles
        for n in [3, 5, 10]:
            assert simulate_triangles_gnp(n, 1.0, self.rng) == n * (n - 1) * (n - 2) // 6


# ──────────────────────────────────────────────────────────────────────────────
# Statistical checks: empirical mean ≈ analytical
# ──────────────────────────────────────────────────────────────────────────────


class TestStatisticalConvergence:
    """Each check uses a sample size large enough that |empirical - analytical|
    is below 4 standard errors with overwhelming probability.

    These tests are deterministic given the fixed seed: they pass or fail the
    same way every run.
    """

    def test_coupon_collector_n10(self):
        rng = np.random.default_rng(SEED)
        analytical = expected_coupon_collector(10)
        mean, se = empirical_mean(simulate_coupon_collector, n_reps=5_000, rng=rng, n=10)
        assert abs(mean - analytical) < 4 * se

    def test_hat_check_n20(self):
        rng = np.random.default_rng(SEED + 1)
        analytical = expected_hat_check(20)
        mean, se = empirical_mean(simulate_hat_check, n_reps=10_000, rng=rng, n=20)
        assert abs(mean - analytical) < 4 * se

    def test_inversions_n50(self):
        rng = np.random.default_rng(SEED + 2)
        analytical = expected_inversions(50)
        mean, se = empirical_mean(simulate_inversions, n_reps=2_000, rng=rng, n=50)
        assert abs(mean - analytical) < 4 * se

    def test_triangles_n30_p_03(self):
        rng = np.random.default_rng(SEED + 3)
        analytical = expected_triangles_gnp(30, 0.3)
        mean, se = empirical_mean(
            simulate_triangles_gnp, n_reps=2_000, rng=rng, n=30, p=0.3
        )
        assert abs(mean - analytical) < 4 * se
