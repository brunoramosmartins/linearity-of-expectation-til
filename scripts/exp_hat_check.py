"""Empirical verification of E[F] = 1 (and Var(F) = 1) for the hat-check problem.

Run from the repo root:

    python scripts/exp_hat_check.py

The striking thing about the hat-check problem is that both moments equal
exactly 1 for every n. We verify across a grid of n that the empirical mean
and variance converge to 1, and that the distribution looks Poisson(1) for
moderate n.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.indicators import expected_hat_check, simulate_hat_check

SEED = 20260526
N_REPS = 20_000
N_GRID = [5, 10, 20, 50, 100, 500]


def main() -> None:
    rng = np.random.default_rng(SEED)
    rows = []
    for n in N_GRID:
        analytical_mean = expected_hat_check(n)
        samples = np.array(
            [simulate_hat_check(n, rng) for _ in range(N_REPS)],
            dtype=float,
        )
        mean = samples.mean()
        var = samples.var(ddof=1)
        se_mean = samples.std(ddof=1) / np.sqrt(N_REPS)
        rows.append(
            {
                "n": n,
                "E[F] (analytical)": analytical_mean,
                "empirical mean": mean,
                "empirical Var(F)": var,
                "empirical SE(mean)": se_mean,
                "|mean - 1| / SE": abs(mean - analytical_mean) / se_mean,
            }
        )

    df = pd.DataFrame(rows)
    pd.set_option("display.float_format", "{:.4f}".format)
    print("Hat-check — empirical vs analytical")
    print(f"Reps per n: {N_REPS:,}; seed: {SEED}")
    print()
    print(df.to_string(index=False))
    print()
    print(
        "Expected: both 'empirical mean' and 'empirical Var(F)' converge to 1.0 "
        "for every n. (For n >= 10, F is approximately Poisson(1).)"
    )


if __name__ == "__main__":
    main()
