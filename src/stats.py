"""Sample statistics helpers for the correlation-sweep simulation.

Thin layer on top of numpy that returns the quantities the budget application
cares about: sample mean of a total, sample variance, normal-approx CI on the
mean, and the effective sample size under equicorrelation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy import stats as sp_stats


@dataclass(frozen=True)
class MeanCI:
    """Sample mean and a normal-approximation confidence interval."""

    mean: float
    se: float
    half_width: float
    lower: float
    upper: float
    confidence: float


def mean_with_ci(samples: np.ndarray, confidence: float = 0.95) -> MeanCI:
    """Sample mean of ``samples`` with a normal-approximation confidence interval.

    The CI uses the sample standard error and a normal critical value
    ``z = Phi^{-1}((1 + confidence) / 2)``. For ``confidence = 0.95`` this gives
    the usual 1.96. Appropriate when ``len(samples)`` is moderately large (CLT
    regime); for the K = 10,000 reps used in Phase 4 this is fine.

    Parameters
    ----------
    samples : ndarray
        One-dimensional array of samples (e.g. realizations of the team total).
    confidence : float, optional
        Confidence level in ``(0, 1)``. Default ``0.95``.

    Returns
    -------
    MeanCI
        Mean, SE, half-width, lower bound, upper bound, and the confidence level.
    """
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must be in (0, 1); got {confidence}")
    samples = np.asarray(samples, dtype=float).ravel()
    if samples.size < 2:
        raise ValueError(f"need at least 2 samples to compute SE; got {samples.size}")

    mean = float(samples.mean())
    se = float(samples.std(ddof=1) / np.sqrt(samples.size))
    z = float(sp_stats.norm.ppf((1.0 + confidence) / 2.0))
    half = z * se
    return MeanCI(
        mean=mean,
        se=se,
        half_width=half,
        lower=mean - half,
        upper=mean + half,
        confidence=confidence,
    )


def variance_of_total(samples: np.ndarray) -> float:
    """Sample variance of a 1-D array of totals (unbiased, ``ddof=1``)."""
    samples = np.asarray(samples, dtype=float).ravel()
    if samples.size < 2:
        raise ValueError(f"need at least 2 samples to compute variance; got {samples.size}")
    return float(samples.var(ddof=1))


def effective_sample_size(n: int, rho: float) -> float:
    r"""Effective sample size under equicorrelation.

    .. math::

        n_\text{eff} = \frac{n}{1 + (n - 1)\rho}.

    For ``rho = 0`` returns ``n``. For ``rho`` approaching ``-1/(n-1)`` the
    formula tends to ``+\infty`` (perfect cancellation). For ``rho`` close to
    ``1`` it tends to ``1`` (no diversification).
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    if n == 1:
        return 1.0
    denom = 1.0 + (n - 1) * rho
    # At rho = -1/(n-1) the denominator is mathematically 0 but floating point
    # gives a value of order 1e-16 from 49 * (-1/49) + 1. Treat tiny non-positive
    # values as the PSD bound: n_eff diverges.
    if denom <= 1e-12:
        return float("inf")
    return n / denom
