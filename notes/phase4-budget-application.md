# Phase 4 — Budget Modelling Simulation

## 1. The scenario

A 50-person team. Each monthly salary $S_i$ is drawn from a LogNormal distribution with target moments

$$
E[S_i] = R\$\, 10{,}000, \qquad \text{Var}(S_i) = (R\$\, 2{,}000)^2 = 4 \times 10^6,
$$

i.e., a coefficient of variation $\text{CV} = 0.20$. The total monthly budget is

$$
S = \sum_{i=1}^{50} S_i.
$$

Salaries within a team share common drivers — industry compensation bands, role mix, location market dynamics — so the $S_i$ are **not** independent. We model the dependence with a **Gaussian copula** on the underlying log-normals: the $\log S_i$ are jointly normal with equicorrelation $\rho$ on the common-driver scale.

The goal of this phase is to show, in code, that

1. $E[S] = 50 \cdot 10{,}000 = R\$\, 500{,}000$ for every value of $\rho$ in the feasible range (linearity, Phase 1).
2. $\text{Var}(S)$ scales as $50\,\sigma^2(1 + 49\rho)$ on the equicorrelated normals, and tracks the analogous formula on the LogNormal scale up to a small bias from the lognormal transform (Phase 2).
3. The 95% confidence band on the total widens dramatically as $\rho$ increases — at $\rho = 0.2$ (a modest within-team correlation), the band is about $3.3\times$ as wide as the independent assumption would predict.
4. Negative correlation, allowed up to $\rho \ge -1/(n-1) \approx -0.0204$ by positive-semidefiniteness, **reduces** the variance of the total below the independent case.

The TIL pulls one number from this — typically the variance ratio at $\rho = 0.2$ — to make its central rhetorical move.

---

## 2. LogNormal calibration

Given target moments $E[S] = m$ and $\text{Var}(S) = v$, the LogNormal parameters $(\mu, \sigma)$ on $\log S$ solve

$$
m = e^{\mu + \sigma^2/2}, \qquad v = (e^{\sigma^2} - 1)\, e^{2\mu + \sigma^2}.
$$

Eliminating gives the closed-form

$$
\sigma^2 = \ln\!\left(1 + \frac{v}{m^2}\right) = \ln(1 + \text{CV}^2), \qquad \mu = \ln m - \frac{\sigma^2}{2}.
$$

For our numbers ($m = 10{,}000$, $\text{CV} = 0.2$):

$$
\sigma^2 = \ln(1.04) \approx 0.03922, \qquad \sigma \approx 0.1980, \qquad \mu = \ln(10{,}000) - 0.0196 \approx 9.1907.
$$

This is implemented in `src.correlated.lognormal_parameters_from_moments`. The function and its inverse have a roundtrip test in `tests/test_correlated.py`.

---

## 3. Dependence via Gaussian copula

Let $\mathbf{Z} = (Z_1, \ldots, Z_n)$ be jointly normal with $\text{Var}(Z_i) = 1$ and $\text{Cov}(Z_i, Z_j) = \rho$ for $i \ne j$ (equicorrelation). Define

$$
S_i = \exp(\mu + \sigma Z_i).
$$

Each $S_i$ has marginal $\text{LogNormal}(\mu, \sigma)$, *regardless* of $\rho$ — the marginal is set by $(\mu, \sigma)$ alone, and the joint dependence is the copula.

The induced LogNormal correlation is

$$
\rho_X = \frac{e^{\rho \sigma^2} - 1}{e^{\sigma^2} - 1}.
$$

For our $\sigma^2 \approx 0.039$, $\rho_X \approx \rho$ to within roughly $2\%$ at $\rho = 0.5$. So we will index plots and tables by $\rho$ (the Gaussian-copula parameter) and note that $\rho_X$ is essentially the same number for this calibration.

### Implementation

- `_sample_equicorrelated_normals(n, rho, size, rng)` builds the underlying normals. For $\rho \ge 0$ it uses the **one-factor decomposition** $Z_i = \sqrt{\rho}\, F + \sqrt{1 - \rho}\, E_i$ — cheap ($O(n)$ per realization), no Cholesky needed. For $\rho < 0$ it falls back to `np.random.Generator.multivariate_normal` with the equicorrelated covariance.
- `sample_correlated_lognormals(n, rho, mu_log, sigma_log, size, rng)` exponentiates: `np.exp(mu_log + sigma_log * Z)`.

Both live in `src/correlated.py`.

### PSD lower bound on $\rho$

The equicorrelated covariance matrix $(1 - \rho) I + \rho J$ has eigenvalues $1 - \rho$ (multiplicity $n - 1$) and $1 + (n - 1)\rho$ (multiplicity $1$). Both must be $\ge 0$, giving

$$
-\frac{1}{n - 1} \le \rho \le 1.
$$

For $n = 50$ the lower bound is $\approx -0.0204$. This is enforced in `_sample_equicorrelated_normals` — calling with $\rho$ below the bound raises `ValueError`.

---

## 4. The correlation sweep

`scripts/exp_correlation_sweep.py` runs, for each $\rho \in \{-0.02, -0.01, 0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9\}$, $K = 10{,}000$ independent realizations of the team total $S$ and reports:

- sample mean of the total,
- sample variance of the total,
- 95% half-width of one realization (i.e., $1.96\,\text{SD}(S)$).

The figure is saved to `figures/correlation_sweep.png`. Schematically:

| Panel | Variable | What it shows |
|------:|:---------|:--------------|
| 1 | mean total $\bar S$ vs $\rho$ | **flat line** at $\approx 500{,}000$ for every $\rho$. Linearity. |
| 2 | $\text{Var}(S)$ vs $\rho$ (log scale) | rising, roughly linear in $\rho$. Equicorrelation formula. |
| 3 | $1.96 \cdot \text{SD}(S)$ vs $\rho$ | $\sqrt{\rho}$ behaviour for large $\rho$ — uncertainty band widens. |

### Expected numbers (analytical, equicorrelated normals)

Using $\text{Var}(\sum S_i) \approx n \sigma_S^2 (1 + (n-1)\rho)$ on the LogNormal scale:

| $\rho$ | $\text{Var}(S)$ | $\text{SD}(S)$ | 95% half-width |
|------:|:------:|:------:|:------:|
| $0.0$  | $2.0 \times 10^8$ | 14{,}142 | 27{,}719 |
| $0.05$ | $6.9 \times 10^8$ | 26{,}268 | 51{,}485 |
| $0.10$ | $1.18 \times 10^9$ | 34{,}352 | 67{,}330 |
| $0.20$ | $2.16 \times 10^9$ | 46{,}476 | 91{,}094 |
| $0.50$ | $5.1 \times 10^9$  | 71{,}414 | 139{,}972 |
| $0.90$ | $9.04 \times 10^9$ | 95{,}079 | 186{,}355 |

**Read this:** the team total has expected value $500{,}000$ at every $\rho$. The half-width of the 95% band on a single month's actual total goes from $\pm R\$\, 27{,}700$ (independent) to $\pm R\$\, 91{,}100$ (at $\rho = 0.2$) — a $3.3\times$ widening for a correlation that any working analyst would consider modest.

The empirical sweep in the script confirms these numbers within a couple of percent (the small bias is the lognormal-vs-normal correlation transform).

---

## 5. Effective sample size in the budget context

The effective sample size formula from Phase 2,

$$
n_\text{eff} = \frac{n}{1 + (n - 1)\rho},
$$

translates the correlation directly into a "how many independent salaries is this worth?" number. For the 50-person team:

| $\rho$ | $n_\text{eff}$ |
|------:|:------:|
| $0.00$ | $50.00$ |
| $0.05$ | $16.84$ |
| $0.10$ | $10.20$ |
| $0.20$ | $5.10$ |
| $0.50$ | $2.04$ |
| $0.90$ | $1.12$ |

This is the headline column for an audience that has internalized "the square-root law". At $\rho = 0.2$, you have, statistically speaking, **five** independent salaries — not fifty. Any uncertainty band you would report under independence is widened by $\sqrt{50/5.1} \approx 3.13$.

---

## 6. Negative-correlation regime

`scripts/exp_negative_correlation.py` sweeps $\rho$ from just above the PSD bound ($-0.0204 + 0.002 \approx -0.0184$) up to $\rho = 0$ in steps. Expected qualitative result: $\text{Var}(S)$ drops *below* the independent-case value, and $n_\text{eff}$ rises *above* 50.

| $\rho$ | $1 + (n-1)\rho$ | variance ratio vs independent |
|------:|:---------------:|:----------------:|
| $-0.0184$ | $0.0984$ | $\approx 0.10$ |
| $-0.010$  | $0.510$  | $\approx 0.51$ |
| $-0.005$  | $0.755$  | $\approx 0.76$ |
| $0.0$     | $1.000$  | $1.00$ |

So even at the most modest negative correlations available in $n = 50$, the variance of the total can be cut by half. This is the structural reason hedging works: a portfolio of countercyclical components has lower variance than the diagonal of its covariance matrix would suggest.

In a budget context, this regime is real but rare — it requires the cost structure of the team to have genuinely countercyclical components (e.g., a sales team whose commission moves opposite to a back-office team whose costs move with regulatory cycles). When it does occur, the conservative independent assumption *overstates* uncertainty, which has its own costs (overly wide reserves, unwarranted hedging).

The figure `figures/negative_correlation.png` shows the variance-ratio and $n_\text{eff}$ panels across this regime.

---

## 7. Operational rules for budget work

The two-line summary that the TIL is built around:

1. **Estimating the mean of a budget total:** correlation structure does not enter. Sum the marginal means. Done.
2. **Estimating the variance, the 95% band, or any tail risk of the budget total:** correlation structure is the input. Equicorrelation with $\rho = 0.2$ already widens the band by $3.3\times$ versus independence on $n = 50$.

The expensive failure mode is using the independent assumption for question 2 because you used it for question 1 and it "worked there". It worked for question 1 because of linearity; it cannot work for question 2 because the variance formula has a cross term.

### Two diagnostic questions for any budget model

When reviewing a probabilistic budget, ask:

a. *Where did the correlation structure enter?* — If the answer is "nowhere", the model is implicitly assuming $\rho = 0$. That is fine if the question is about the mean. If the question is about the 95% range, the model is wrong by at least the factor $\sqrt{1 + (n - 1) \rho}$.

b. *What value of $\rho$ would change the answer?* — If even a small positive correlation ($\rho = 0.05$ to $0.2$) materially changes the conclusion, then the model is fragile to dependence and you need a defensible estimate of $\rho$, not a default to $0$.

These two questions, asked of any "Monte Carlo budget" in the field, will surface the central issue this phase exists to highlight.

---

## 8. Outputs of this phase

- `src/correlated.py` — LogNormal Gaussian-copula sampler, parameter conversion, PSD-bound helper.
- `src/stats.py` — sample mean / SE / CI helpers and the effective-sample-size formula.
- `tests/test_correlated.py`, `tests/test_stats.py` — sanity tests on parameter roundtrips, marginal moment invariance across $\rho$, variance monotonicity in $\rho$, and the negative-correlation regime.
- `scripts/exp_correlation_sweep.py` — main sweep, table + 3-panel figure (`figures/correlation_sweep.png`).
- `scripts/exp_negative_correlation.py` — negative-$\rho$ regime, variance-ratio + $n_\text{eff}$ figure (`figures/negative_correlation.png`).
- `notes/phase4-budget-application.md` — this document.

## 9. What the TIL takes from here

The Example block of the published TIL (~100–150 words) will:

- State the 50-person team setup with $R\$\, 10{,}000$ marginals and a single $\rho$ value (probably $0.2$, the most common in-team estimate).
- Quote $E[S] = R\$\, 500{,}000$ as independence-free.
- Quote $\text{Var}(S)$ as $\sim 10\times$ the independent case.
- Embed (optionally) `figures/correlation_sweep.png`.

Everything else — the negative-correlation panel, the effective-sample-size table, the LogNormal calibration — lives in this repo as supporting evidence, not in the published TIL.
