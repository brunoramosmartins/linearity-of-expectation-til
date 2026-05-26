"""Empirical verification of E[T] = n * H_n for the coupon collector problem.

Run from the repo root:

    python scripts/exp_coupon_collector.py

Sweeps n in a small grid, reports empirical mean and standard error against
the closed-form expectation, and writes the table to stdout. Useful as a
sanity check that ``src.indicators`` is behaving and as a quick demo for
the TIL.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src.indicators import (
    empirical_mean,
    expected_coupon_collector,
    simulate_coupon_collector,
)

SEED = 20260526
N_REPS = 5_000
N_GRID = [5, 10, 20, 50, 100]


def main() -> None:
    rng = np.random.default_rng(SEED)
    rows = []
    for n in N_GRID:
        analytical = expected_coupon_collector(n)
        mean, se = empirical_mean(simulate_coupon_collector, N_REPS, rng, n=n)
        rows.append(
            {
                "n": n,
                "E[T] = n*H_n": analytical,
                "empirical mean": mean,
                "empirical SE": se,
                "|gap| / SE": abs(mean - analytical) / se,
            }
        )

    df = pd.DataFrame(rows)
    pd.set_option("display.float_format", "{:.3f}".format)
    print("Coupon collector — empirical vs analytical")
    print(f"Reps per n: {N_REPS:,}; seed: {SEED}")
    print()
    print(df.to_string(index=False))
    print()
    print("Expected: |gap| / SE should be < 4 with overwhelming probability.")


if __name__ == "__main__":
    main()
