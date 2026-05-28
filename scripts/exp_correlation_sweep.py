"""Correlation-sweep simulation for the 50-person team budget.

Run from the repo root:

    python scripts/exp_correlation_sweep.py

For each rho in a small grid, draws K = 10,000 realizations of n = 50
LogNormal salaries (Gaussian copula, equicorrelated), computes the total
S = sum S_i, and tabulates the sample mean, sample variance, and 95% CI
half-width of the total. Saves:

- ``figures/correlation_sweep.png``: three-panel figure (mean, variance,
  95% CI half-width vs rho).
- prints the summary table to stdout.

Marginal calibration: each salary has E[S_i] = 10,000 (R$) and
SD(S_i) = 2,000 (CV = 20%). The total mean is therefore 50 * 10,000 =
500,000 regardless of rho — that is the headline that the figure makes
visually obvious.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.correlated import (
    lognormal_parameters_from_moments,
    sample_correlated_lognormals,
)
from src.stats import mean_with_ci

# ── Parameters ──────────────────────────────────────────────────────────────

SEED = 20260527
N = 50
K = 10_000
RHO_GRID = [-0.02, -0.01, 0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9]
TARGET_MEAN = 10_000.0      # R$ per employee
TARGET_VAR = 4_000_000.0    # SD = 2_000 (CV = 0.2)

OUTPUT_FIG = Path("figures") / "correlation_sweep.png"


def run_sweep() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    mu, sigma = lognormal_parameters_from_moments(TARGET_MEAN, TARGET_VAR)

    rows = []
    for rho in RHO_GRID:
        samples = sample_correlated_lognormals(
            n=N, rho=rho, mu_log=mu, sigma_log=sigma, size=K, rng=rng
        )
        totals = samples.sum(axis=1)
        ci = mean_with_ci(totals, confidence=0.95)
        rows.append(
            {
                "rho":             rho,
                "mean_total":      ci.mean,
                "se_mean":         ci.se,
                "var_total":       float(totals.var(ddof=1)),
                "sd_total":        float(totals.std(ddof=1)),
                "ci_half_width":   1.959964 * float(totals.std(ddof=1)),  # 95% half-width of one realization
            }
        )
    return pd.DataFrame(rows)


def plot_sweep(df: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(12.5, 3.8), sharex=True)

    # Panel 1 — sample mean of the total
    ax = axes[0]
    target_total = N * TARGET_MEAN
    ax.plot(df["rho"], df["mean_total"], marker="o", linewidth=1.5)
    ax.axhline(target_total, color="black", linestyle="--", linewidth=0.8,
               label=f"E[S] = {target_total:,.0f}")
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"sample mean of total $\bar S$")
    ax.set_title("Mean is invariant in $\\rho$")
    ax.set_ylim(target_total * 0.97, target_total * 1.03)
    ax.legend(loc="lower right", fontsize=9)

    # Panel 2 — sample variance of the total
    ax = axes[1]
    ax.plot(df["rho"], df["var_total"], marker="o", linewidth=1.5, color="C3")
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"sample $\mathrm{Var}(S)$")
    ax.set_title("Variance grows linearly in $\\rho$")
    ax.set_yscale("log")

    # Panel 3 — 95% half-width of one realization (sqrt of variance, scaled)
    ax = axes[2]
    ax.plot(df["rho"], df["ci_half_width"], marker="o", linewidth=1.5, color="C2")
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"$1.96 \cdot \mathrm{SD}(S)$")
    ax.set_title("95% half-width of one realization")

    fig.suptitle(
        f"Team total: n = {N} LogNormal salaries, K = {K:,} sims, seed = {SEED}",
        fontsize=10,
    )
    plt.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    df = run_sweep()

    pd.set_option("display.float_format", lambda v: f"{v:,.2f}")
    print("Correlation-sweep simulation")
    print(f"n = {N}, K = {K:,}, seed = {SEED}")
    print(f"Marginal: E[S_i] = {TARGET_MEAN:,.0f}, SD(S_i) = {np.sqrt(TARGET_VAR):,.0f}")
    print(f"Expected total mean (analytical): {N * TARGET_MEAN:,.0f}")
    print()
    print(df.to_string(index=False))
    print()

    plot_sweep(df, OUTPUT_FIG)
    print(f"Figure written to: {OUTPUT_FIG}")


if __name__ == "__main__":
    main()
