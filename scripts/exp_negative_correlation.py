"""Negative-correlation regime for the 50-person team budget.

Run from the repo root:

    python scripts/exp_negative_correlation.py

In dimension n = 50, the PSD lower bound on the equicorrelation is
rho >= -1/(n-1) ≈ -0.0204. We sweep rho across the feasible negative
range and show:

- the mean of the total is invariant (still 500,000),
- the variance of the total **drops below** the independent case,
- the effective sample size **increases** above n.

This is the "counterintuitive bonus" referenced in the roadmap: negative
correlation is variance-reducing, and is the structural reason hedging /
diversification across countercyclical components works.

Saves ``figures/negative_correlation.png``.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.correlated import (
    lognormal_parameters_from_moments,
    min_equicorrelation,
    sample_correlated_lognormals,
)
from src.stats import effective_sample_size

# ── Parameters ──────────────────────────────────────────────────────────────

SEED = 20260527
N = 50
K = 10_000
TARGET_MEAN = 10_000.0
TARGET_VAR = 4_000_000.0
OUTPUT_FIG = Path("figures") / "negative_correlation.png"


def run_sweep() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    mu, sigma = lognormal_parameters_from_moments(TARGET_MEAN, TARGET_VAR)

    # PSD bound is -1/(n-1). Stay slightly above it for numerical safety.
    lower = min_equicorrelation(N)
    rho_grid = np.linspace(lower + 0.002, 0.0, 9)

    rows = []
    for rho in rho_grid:
        samples = sample_correlated_lognormals(
            n=N, rho=float(rho), mu_log=mu, sigma_log=sigma, size=K, rng=rng,
        )
        totals = samples.sum(axis=1)
        rows.append(
            {
                "rho":         float(rho),
                "mean_total":  float(totals.mean()),
                "var_total":   float(totals.var(ddof=1)),
                "sd_total":    float(totals.std(ddof=1)),
                "n_eff":       effective_sample_size(N, float(rho)),
            }
        )

    df = pd.DataFrame(rows)
    # Mark the independent baseline for reference
    independent_var = df.loc[df["rho"].sub(0.0).abs().idxmin(), "var_total"]
    df["var_ratio_vs_independent"] = df["var_total"] / independent_var
    return df


def plot_sweep(df: pd.DataFrame, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))

    ax = axes[0]
    ax.plot(df["rho"], df["var_ratio_vs_independent"], marker="o", linewidth=1.5, color="C3")
    ax.axhline(1.0, color="black", linestyle="--", linewidth=0.8,
               label="independent baseline")
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"$\mathrm{Var}(S) / \mathrm{Var}_{\rho=0}(S)$")
    ax.set_title("Variance of total relative to independent case")
    ax.legend(loc="upper left", fontsize=9)

    ax = axes[1]
    ax.plot(df["rho"], df["n_eff"], marker="o", linewidth=1.5, color="C2")
    ax.axhline(N, color="black", linestyle="--", linewidth=0.8, label=f"n = {N}")
    ax.set_xlabel(r"correlation $\rho$")
    ax.set_ylabel(r"$n_{\text{eff}} = n / (1 + (n-1)\rho)$")
    ax.set_title("Effective sample size")
    ax.legend(loc="upper left", fontsize=9)

    fig.suptitle(
        f"Negative-correlation regime: n = {N}, K = {K:,} sims, seed = {SEED}",
        fontsize=10,
    )
    plt.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output, dpi=150)
    plt.close(fig)


def main() -> None:
    df = run_sweep()

    pd.set_option("display.float_format", lambda v: f"{v:,.3f}")
    print("Negative-correlation sweep")
    print(f"n = {N}, K = {K:,}, seed = {SEED}")
    print(f"PSD lower bound on rho: {min_equicorrelation(N):.4f}")
    print()
    print(df.to_string(index=False))
    print()

    plot_sweep(df, OUTPUT_FIG)
    print(f"Figure written to: {OUTPUT_FIG}")


if __name__ == "__main__":
    main()
