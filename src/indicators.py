"""Empirical simulators and exact-value helpers for the Phase 3 indicator-variable examples.

Each problem comes with:
- a ``simulate_*`` function that draws a single realization of the count, and
- an ``expected_*`` function returning the closed-form mean (for verification).

All simulators take a ``numpy.random.Generator`` so callers control seeding.
The implementations are deliberately straightforward; speed was not a goal.
"""

from __future__ import annotations

import numpy as np

# ──────────────────────────────────────────────────────────────────────────────
# Coupon collector
# ──────────────────────────────────────────────────────────────────────────────


def simulate_coupon_collector(n: int, rng: np.random.Generator) -> int:
    """Number of draws to collect all ``n`` distinct coupon types.

    Each draw is uniform on ``{0, 1, ..., n-1}`` and independent of past draws.

    Parameters
    ----------
    n : int
        Number of distinct coupon types. Must be a positive integer.
    rng : numpy.random.Generator
        Random number generator.

    Returns
    -------
    int
        Number of draws until all ``n`` types have appeared at least once.
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    seen = np.zeros(n, dtype=bool)
    draws = 0
    while not seen.all():
        c = rng.integers(0, n)
        seen[c] = True
        draws += 1
    return draws


def expected_coupon_collector(n: int) -> float:
    r"""Closed-form expectation ``E[T] = n * H_n`` for the coupon collector.

    Uses ``H_n = sum_{k=1}^n 1/k``.
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    harmonic_n = float(np.sum(1.0 / np.arange(1, n + 1)))
    return n * harmonic_n


# ──────────────────────────────────────────────────────────────────────────────
# Hat-check / fixed points of a random permutation
# ──────────────────────────────────────────────────────────────────────────────


def simulate_hat_check(n: int, rng: np.random.Generator) -> int:
    """Number of fixed points of a uniform random permutation of ``n`` elements.

    A fixed point is an index ``i`` such that ``perm[i] == i``.
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    perm = rng.permutation(n)
    return int(np.sum(perm == np.arange(n)))


def expected_hat_check(n: int) -> float:
    """Closed-form expectation ``E[F] = 1`` for any ``n >= 1``."""
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    return 1.0


# ──────────────────────────────────────────────────────────────────────────────
# Inversions in a random permutation
# ──────────────────────────────────────────────────────────────────────────────


def count_inversions(perm: np.ndarray) -> int:
    """Number of inversions in a permutation.

    An inversion is a pair ``(i, j)`` with ``i < j`` and ``perm[i] > perm[j]``.

    Uses the merge-sort style O(n log n) approach by sorting via numpy and
    counting via cumulative comparisons (a naive O(n^2) implementation, but
    plenty fast for ``n <= 2000``).
    """
    perm = np.asarray(perm)
    n = len(perm)
    total = 0
    for i in range(n - 1):
        total += int(np.sum(perm[i + 1 :] < perm[i]))
    return total


def simulate_inversions(n: int, rng: np.random.Generator) -> int:
    """Number of inversions in a uniform random permutation of ``n`` elements."""
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    perm = rng.permutation(n)
    return count_inversions(perm)


def expected_inversions(n: int) -> float:
    """Closed-form expectation ``E[I] = n(n-1)/4``."""
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    return n * (n - 1) / 4.0


# ──────────────────────────────────────────────────────────────────────────────
# Triangles in G(n, p)
# ──────────────────────────────────────────────────────────────────────────────


def simulate_triangles_gnp(n: int, p: float, rng: np.random.Generator) -> int:
    """Number of triangles in an Erdos-Renyi random graph ``G(n, p)``.

    Builds the symmetric adjacency matrix ``A`` by drawing each upper-triangular
    entry as ``Bernoulli(p)``, then counts triangles via ``trace(A^3) / 6``
    (each triangle contributes to the trace through six length-three closed
    walks: 3 starting vertices x 2 orientations).
    """
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"p must be in [0, 1]; got {p}")
    if n < 3:
        return 0
    upper = np.triu(rng.random((n, n)) < p, k=1).astype(np.int64)
    a = upper + upper.T
    a3 = np.linalg.matrix_power(a, 3)
    return int(np.trace(a3) // 6)


def expected_triangles_gnp(n: int, p: float) -> float:
    """Closed-form expectation ``E[T] = C(n, 3) * p^3``."""
    if n < 1:
        raise ValueError(f"n must be a positive integer; got {n}")
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"p must be in [0, 1]; got {p}")
    if n < 3:
        return 0.0
    return n * (n - 1) * (n - 2) / 6.0 * p**3


# ──────────────────────────────────────────────────────────────────────────────
# Convenience: run many simulations and return empirical mean + SE
# ──────────────────────────────────────────────────────────────────────────────


def empirical_mean(
    simulator,
    n_reps: int,
    rng: np.random.Generator,
    *args,
    **kwargs,
) -> tuple[float, float]:
    """Run ``simulator`` ``n_reps`` times and return ``(mean, standard_error)``.

    Parameters
    ----------
    simulator : callable
        A ``simulate_*`` function from this module. It must accept ``rng`` as
        its final positional or keyword argument.
    n_reps : int
        Number of independent replications.
    rng : numpy.random.Generator
        Random number generator passed to ``simulator`` each call.
    *args, **kwargs
        Forwarded to ``simulator``.

    Returns
    -------
    (mean, standard_error) : tuple of float
        Sample mean of the simulator output and the standard error of that
        mean (``sample_std / sqrt(n_reps)``).
    """
    if n_reps < 2:
        raise ValueError(f"n_reps must be at least 2 to compute a standard error; got {n_reps}")
    values = np.array([simulator(*args, rng=rng, **kwargs) for _ in range(n_reps)], dtype=float)
    return float(values.mean()), float(values.std(ddof=1) / np.sqrt(n_reps))
