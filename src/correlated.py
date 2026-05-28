"""Correlated LogNormal salary generator via Gaussian copula.

A 50-person team budget is modelled as ``S = S_1 + S_2 + ... + S_n`` where
each ``S_i`` is LogNormal with the same marginal moments and the dependence
between salaries is specified by an equicorrelation parameter ``rho`` on the
underlying normals (Gaussian copula).

The key results this module supports (see ``notes/phase4-budget-application.md``):

- The mean ``E[S]`` is invariant in ``rho`` (linearity of expectation).
- The variance ``Var(S)`` scales as ``n * sigma^2 * (1 + (n - 1) * rho)`` on
  the LogNormal scale up to the small bias introduced by the lognormal
  transform; in practice for moderate ``sigma_log`` it tracks the Gaussian
  formula closely.
- Negative correlation reduces variance below the independent case, bounded
  by ``rho >= -1 / (n - 1)`` (positive-semidefinite constraint).
"""

from __future__ import annotations

import numpy as np

# ──────────────────────────────────────────────────────────────────────────────
# LogNormal parameter conversion
# ──────────────────────────────────────────────────────────────────────────────


def lognormal_parameters_from_moments(mean: float, variance: float) -> tuple[float, float]:
    r"""Solve for ``(mu_log, sigma_log)`` of a LogNormal given target moments.

    Uses the identities

    .. math::

        E[S] = \exp(\mu + \sigma^2 / 2), \qquad
        \text{Var}(S) = (\exp(\sigma^2) - 1)\, \exp(2\mu + \sigma^2).

    Inverting gives ``sigma^2 = ln(1 + CV^2)`` and ``mu = ln(mean) - sigma^2/2``
    where ``CV = SD / mean`` is the coefficient of variation.

    Parameters
    ----------
    mean : float
        Target ``E[S]``. Must be positive.
    variance : float
        Target ``Var(S)``. Must be non-negative.

    Returns
    -------
    (mu_log, sigma_log) : tuple of float
        Parameters such that ``log(S) ~ Normal(mu_log, sigma_log^2)``.
    """
    if mean <= 0:
        raise ValueError(f"mean must be positive; got {mean}")
    if variance < 0:
        raise ValueError(f"variance must be non-negative; got {variance}")
    cv_sq = variance / mean**2
    sigma_log_sq = np.log(1.0 + cv_sq)
    sigma_log = float(np.sqrt(sigma_log_sq))
    mu_log = float(np.log(mean) - sigma_log_sq / 2.0)
    return mu_log, sigma_log


def lognormal_correlation_from_gaussian(rho_gaussian: float, sigma_log: float) -> float:
    r"""Map Gaussian-copula correlation ``rho_Z`` to the resulting LogNormal correlation.

    For LogNormal marginals with parameter ``sigma_log`` and underlying-normal
    correlation ``rho_Z``, the LogNormal correlation is

    .. math::

        \rho_X = \frac{\exp(\rho_Z \sigma^2) - 1}{\exp(\sigma^2) - 1}.

    For small ``sigma_log`` (say ``sigma_log < 0.3``), ``rho_X ≈ rho_Z`` within
    a few percent. The bias matters more for highly skewed marginals.
    """
    sigma_sq = sigma_log**2
    denom = np.exp(sigma_sq) - 1.0
    if denom <= 0:
        return float(rho_gaussian)
    return float((np.exp(rho_gaussian * sigma_sq) - 1.0) / denom)


# ──────────────────────────────────────────────────────────────────────────────
# Equicorrelated bound
# ──────────────────────────────────────────────────────────────────────────────


def min_equicorrelation(n: int) -> float:
    """Return the lower bound ``-1 / (n - 1)`` for equicorrelation in dimension ``n``.

    Equicorrelated covariance matrices are positive-semidefinite only when
    ``rho >= -1 / (n - 1)`` (and ``rho <= 1``).
    """
    if n < 2:
        raise ValueError(f"n must be at least 2 for equicorrelation; got {n}")
    return -1.0 / (n - 1)


# ──────────────────────────────────────────────────────────────────────────────
# Sampling
# ──────────────────────────────────────────────────────────────────────────────


def _sample_equicorrelated_normals(
    n: int,
    rho: float,
    size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Draw ``size`` realizations of ``n`` equicorrelated standard normals.

    For ``rho >= 0`` uses the one-factor decomposition
    ``Z_i = sqrt(rho) F + sqrt(1 - rho) E_i`` (fast: O(n) per realization,
    no Cholesky).

    For ``rho < 0`` uses the full multivariate normal sampler with the
    equicorrelated covariance matrix, which handles the negative-correlation
    regime correctly down to ``rho = -1 / (n - 1)``.
    """
    if rho > 1.0 + 1e-12:
        raise ValueError(f"rho must be at most 1; got {rho}")
    lower = -1.0 / (n - 1)
    if rho < lower - 1e-12:
        raise ValueError(
            f"rho must be at least -1/(n-1) = {lower:.6f} for n = {n}; got {rho}"
        )

    if rho >= 0.0:
        # One-factor decomposition (exact for any rho in [0, 1]).
        common = rng.standard_normal((size, 1))
        idiosyncratic = rng.standard_normal((size, n))
        return np.sqrt(rho) * common + np.sqrt(1.0 - rho) * idiosyncratic

    # Full covariance for negative rho.
    cov = (1.0 - rho) * np.eye(n) + rho * np.ones((n, n))
    return rng.multivariate_normal(
        mean=np.zeros(n), cov=cov, size=size, check_valid="ignore"
    )


def sample_correlated_lognormals(
    n: int,
    rho: float,
    mu_log: float,
    sigma_log: float,
    size: int,
    rng: np.random.Generator,
) -> np.ndarray:
    r"""Draw ``size`` realizations of ``n`` equicorrelated LogNormal variables.

    Each sample is constructed as ``S_i = exp(mu_log + sigma_log * Z_i)`` where
    the ``Z_i`` are standard normals with equicorrelation ``rho`` (Gaussian
    copula). The marginal distribution of each ``S_i`` is
    ``LogNormal(mu_log, sigma_log)``.

    Parameters
    ----------
    n : int
        Number of variables in each realization (e.g. team size).
    rho : float
        Equicorrelation on the underlying normals. Must satisfy
        ``-1/(n-1) <= rho <= 1``.
    mu_log : float
        ``mu`` parameter of the LogNormal marginal.
    sigma_log : float
        ``sigma`` parameter of the LogNormal marginal. Must be positive.
    size : int
        Number of independent realizations to draw.
    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    samples : ndarray, shape (size, n)
        Each row is one realization of the ``n`` correlated salaries.
    """
    if sigma_log <= 0:
        raise ValueError(f"sigma_log must be positive; got {sigma_log}")
    z = _sample_equicorrelated_normals(n, rho, size, rng)
    return np.exp(mu_log + sigma_log * z)
