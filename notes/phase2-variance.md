# Phase 2 — Variance Counterpoint

## 1. Why this phase exists

Phase 1 established that the mean of a sum is independence-free. This phase establishes the contrast: the **variance** of a sum is not. The variance picks up a covariance term for every pair of summands, and covariance is exactly the structural object that independence would zero out. So the same correlation that the mean ignored controls how the variance grows, and how wide the confidence interval around the total becomes.

The rhetorical move of the TIL is this contrast. Skip this phase and the TIL has no edge.

---

## 2. Statement

**Proposition (Variance of a sum).** Let $X_1, \ldots, X_n$ be square-integrable random variables on a common probability space (that is, $E[X_i^2] < \infty$ for each $i$, so $\text{Var}(X_i)$ exists). Then

$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2 \sum_{1 \le i < j \le n} \text{Cov}(X_i, X_j).
$$

Equivalently, with $\mathbf{X} = (X_1, \ldots, X_n)^\top$ and $\boldsymbol{1} = (1, \ldots, 1)^\top \in \mathbb{R}^n$, and $\Sigma$ the $n \times n$ covariance matrix with $\Sigma_{ij} = \text{Cov}(X_i, X_j)$:

$$
\text{Var}(\boldsymbol{1}^\top \mathbf{X}) = \boldsymbol{1}^\top \Sigma \boldsymbol{1}.
$$

**Corollary (independent case).** If the $X_i$ are pairwise uncorrelated (in particular, independent), every $\text{Cov}(X_i, X_j) = 0$ for $i \ne j$, and the formula collapses to

$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i).
$$

The independent case is the rare one. The general case is the formula above, and the cross terms are not negligible — they are the whole game whenever the $X_i$ share a common driver.

---

## 3. Derivation from the Definition (n = 2)

Recall $\text{Var}(Z) := E[(Z - E[Z])^2] = E[Z^2] - E[Z]^2$.

Let $\mu_X = E[X]$, $\mu_Y = E[Y]$, so $\mu_X + \mu_Y = E[X + Y]$ by linearity (Phase 1).

Expand directly:

$$
\text{Var}(X + Y) = E\!\left[\big((X + Y) - (\mu_X + \mu_Y)\big)^2\right] = E\!\left[\big((X - \mu_X) + (Y - \mu_Y)\big)^2\right].
$$

Let $\widetilde{X} = X - \mu_X$ and $\widetilde{Y} = Y - \mu_Y$ (the centered versions). Then

$$
(X + Y - \mu_X - \mu_Y)^2 = (\widetilde{X} + \widetilde{Y})^2 = \widetilde{X}^2 + 2\, \widetilde{X}\widetilde{Y} + \widetilde{Y}^2.
$$

Take expectation, applying linearity of $E$:

$$
\text{Var}(X + Y) = E[\widetilde{X}^2] + 2\, E[\widetilde{X}\widetilde{Y}] + E[\widetilde{Y}^2].
$$

Identify each term:

- $E[\widetilde{X}^2] = E[(X - \mu_X)^2] = \text{Var}(X)$,
- $E[\widetilde{Y}^2] = \text{Var}(Y)$,
- $E[\widetilde{X}\widetilde{Y}] = E[(X - \mu_X)(Y - \mu_Y)] = \text{Cov}(X, Y)$ by definition.

Hence:

$$
\boxed{\; \text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y). \;}
$$

### Remark — where linearity does the heavy lifting

The proof uses linearity of expectation **three times** (once on the sum, once on the expansion, once on the centered expression). It uses no independence assumption. The cross term $2\,\text{Cov}(X, Y)$ does not disappear — it appears exactly because the integral of a product is, in general, not the product of the integrals.

---

## 4. Generalization to n Variables

Same argument, applied to $\sum_{i=1}^n X_i$:

$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = E\!\left[\Big(\sum_{i=1}^n (X_i - \mu_i)\Big)^2\right] = E\!\left[\sum_{i=1}^n \sum_{j=1}^n (X_i - \mu_i)(X_j - \mu_j)\right].
$$

Linearity of expectation pushes the sum out:

$$
= \sum_{i=1}^n \sum_{j=1}^n E[(X_i - \mu_i)(X_j - \mu_j)] = \sum_{i=1}^n \sum_{j=1}^n \text{Cov}(X_i, X_j).
$$

Split the double sum into diagonal ($i = j$) and off-diagonal ($i \ne j$) terms. Note $\text{Cov}(X_i, X_i) = \text{Var}(X_i)$ and $\text{Cov}(X_i, X_j) = \text{Cov}(X_j, X_i)$ (symmetry):

$$
= \underbrace{\sum_{i=1}^n \text{Var}(X_i)}_{\text{diagonal}} + \underbrace{\sum_{i \ne j} \text{Cov}(X_i, X_j)}_{\text{off-diagonal, symmetric}}.
$$

The off-diagonal sum has $n(n-1)$ terms, but each unordered pair $\{i, j\}$ appears twice (once as $(i,j)$ and once as $(j,i)$), so we may write it as $2 \sum_{i < j} \text{Cov}(X_i, X_j)$. Hence:

$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2 \sum_{1 \le i < j \le n} \text{Cov}(X_i, X_j). \qquad \blacksquare
$$

---

## 5. Matrix Form

Let $\mathbf{X} = (X_1, \ldots, X_n)^\top$, $\boldsymbol{\mu} = E[\mathbf{X}] = (\mu_1, \ldots, \mu_n)^\top$, and $\Sigma = E[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^\top]$ — the $n \times n$ covariance matrix.

For any constant vector $\mathbf{a} \in \mathbb{R}^n$:

$$
\text{Var}(\mathbf{a}^\top \mathbf{X}) = E[(\mathbf{a}^\top \mathbf{X} - \mathbf{a}^\top \boldsymbol{\mu})^2] = E[(\mathbf{a}^\top (\mathbf{X} - \boldsymbol{\mu}))^2].
$$

Use the identity $(\mathbf{a}^\top \mathbf{v})^2 = \mathbf{a}^\top \mathbf{v}\mathbf{v}^\top \mathbf{a}$ (since $\mathbf{a}^\top \mathbf{v}$ is a scalar):

$$
= E[\mathbf{a}^\top (\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^\top \mathbf{a}] = \mathbf{a}^\top \underbrace{E[(\mathbf{X} - \boldsymbol{\mu})(\mathbf{X} - \boldsymbol{\mu})^\top]}_{=\,\Sigma} \mathbf{a} = \mathbf{a}^\top \Sigma \mathbf{a}.
$$

Taking $\mathbf{a} = \boldsymbol{1}$:

$$
\boxed{\; \text{Var}\!\left(\sum_{i=1}^n X_i\right) = \boldsymbol{1}^\top \Sigma\, \boldsymbol{1} = \sum_{i, j} \Sigma_{ij}. \;}
$$

The variance of the sum is the **sum of every entry of the covariance matrix** — diagonal plus all off-diagonal entries. The independent case is exactly the case where $\Sigma$ is diagonal.

---

## 6. Equicorrelation: the Useful Special Case

In the budget application (Phase 4) we will model $n$ employees whose salaries share a common driver (industry, role, location) with a fixed pairwise correlation $\rho$ and a common variance $\sigma^2$. This is the **equicorrelated** model:

$$
\text{Var}(X_i) = \sigma^2, \quad \text{Cov}(X_i, X_j) = \rho\, \sigma^2 \quad \text{for } i \ne j.
$$

Plug into the variance formula:

$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = n \sigma^2 + 2 \binom{n}{2} \rho \sigma^2 = n \sigma^2 + n(n-1) \rho \sigma^2 = n \sigma^2 \big(1 + (n-1)\rho\big).
$$

So:

$$
\boxed{\; \text{Var}\!\left(\sum_{i=1}^n X_i\right) = n \sigma^2 \big(1 + (n-1)\rho\big). \;}
$$

### Limits

| $\rho$ | Variance of sum | $\sqrt{\text{Var}}$ scaling in $n$ |
|------:|:----------------|:----------------------------------|
| $\rho = 0$ (independent) | $n \sigma^2$ | $\sqrt{n}\, \sigma$ (the textbook square-root law) |
| $\rho = 1$ (perfect positive) | $n^2 \sigma^2$ | $n\, \sigma$ (linear in $n$ — diversification gone) |
| $\rho = -1/(n-1)$ (lower bound) | $0$ | $0$ — perfectly cancelling |

The independent case is the *middle* of the range, not the default.

### Lower bound on $\rho$ (positive-semidefinite constraint)

For the equicorrelated covariance matrix $\Sigma = \sigma^2 \big[(1 - \rho) I + \rho J\big]$ (where $J$ is the all-ones matrix) to be a valid covariance matrix, it must be positive-semidefinite. The eigenvalues of $(1 - \rho) I + \rho J$ are:

- $1 - \rho$ with multiplicity $n - 1$,
- $1 + (n-1)\rho$ with multiplicity $1$.

Both must be $\ge 0$:

$$
\rho \le 1 \quad \text{and} \quad \rho \ge -\tfrac{1}{n-1}.
$$

So **negative correlation is allowed**, but it cannot be more negative than $-1/(n-1)$. For $n = 50$, that lower bound is about $-0.0204$. The interesting negative-correlation regime in budgets is therefore mild (e.g., $\rho = -0.01$), not the cinematic $\rho = -1$ of two-variable examples.

---

## 7. Effective Sample Size

If we draw $n$ correlated observations from a common distribution with variance $\sigma^2$ and equicorrelation $\rho$, the variance of the **sample mean** $\bar X = \frac{1}{n}\sum X_i$ is

$$
\text{Var}(\bar X) = \frac{1}{n^2} \cdot n \sigma^2 \big(1 + (n-1)\rho\big) = \frac{\sigma^2}{n} \big(1 + (n-1)\rho\big).
$$

If the observations were independent, $\text{Var}(\bar X) = \sigma^2 / n_{\text{eff}}$. Solving for $n_{\text{eff}}$:

$$
\boxed{\; n_{\text{eff}} = \frac{n}{1 + (n-1)\rho}. \;}
$$

This is the **effective sample size** under equicorrelation. It is the number of *independent* observations whose sample mean would have the same variance as our $n$ correlated observations.

### Numbers to internalize

| $n$ | $\rho$ | $n_\text{eff}$ |
|----:|------:|---------------:|
|  50 | 0.00  | 50.00 |
|  50 | 0.05  | 16.84 |
|  50 | 0.10  | 10.20 |
|  50 | 0.20  |  5.10 |
|  50 | 0.50  |  2.04 |
|  50 | 0.90  |  1.12 |

A correlation of just $0.2$ (modest by the standards of within-team salary structure) cuts the effective sample size from 50 down to ~5. The 95% confidence interval for the mean total **widens by a factor of $\sqrt{50/5.1} \approx 3.13$** compared to the independent assumption. This is the failure mode the TIL is warning against.

---

## 8. Negative-Correlation Counterintuition

Most working analysts intuit that correlation makes things "less precise" and stop there. The full picture: negative correlation makes the variance of the sum **smaller** than the independent case.

For two variables with correlation $\rho < 0$ and equal variance $\sigma^2$:

$$
\text{Var}(X_1 + X_2) = 2\sigma^2 (1 + \rho) < 2\sigma^2.
$$

Concrete example: a pairs-trade where $X_1$ is the return on stock A and $X_2$ is the return on a short position in stock B. If A and B are positively correlated, the long–short position has $X_1$ and $X_2$ negatively correlated, and the variance of the combined position is **smaller** than either leg alone. Variance reduction by negative correlation is the structural reason hedging works.

In the budget application: if you genuinely have two roles whose salary movements are negatively correlated (rare but possible — e.g., a fixed-base + commission salesperson plus a salaried back-office function whose comp moves countercyclically), the variance of the total budget is *smaller* than if you'd assumed independence. Most analysts overestimate uncertainty in this regime.

---

## 9. Numerical Example — Two LogNormal Salaries

Set up:

- Marginal: $S_i \sim \text{LogNormal}(\mu, \sigma)$ with $E[S_i] = 10{,}000$ and $\text{Var}(S_i) = 4 \times 10^6$ (so $\text{SD}(S_i) = 2{,}000$ and the coefficient of variation is $20\%$).
- LogNormal parameters: $\sigma^2_{\log} = \ln\!\big(1 + \text{CV}^2\big) = \ln(1.04) \approx 0.03922$, so $\sigma_{\log} \approx 0.1980$, and $\mu_{\log} = \ln(10{,}000) - \sigma^2_{\log}/2 \approx 9.1907$.
- Dependence: induced by a Gaussian copula with correlation $\rho_Z$ on the underlying normals; the resulting LogNormal correlation is $\rho_X = (e^{\rho_Z \sigma^2_{\log}} - 1) / (e^{\sigma^2_{\log}} - 1)$, which for our $\sigma^2_{\log} \approx 0.04$ is very close to $\rho_Z$ itself (within $\sim 2\%$). We will report results indexed by $\rho_X$.

By the formulas above:

$$
E[S_1 + S_2] = 20{,}000 \quad \text{for every } \rho_X,
$$

$$
\text{Var}(S_1 + S_2) = 2 \cdot 4 \times 10^6 \cdot (1 + \rho_X) = 8 \times 10^6 (1 + \rho_X).
$$

Tabulated (the 95% CI is computed via the normal approximation $\bar S \pm 1.96 \cdot \text{SD}(\bar S)$; for a single realization of the total, $\bar S = (S_1 + S_2)$ so $\text{SD}(\bar S) = \sqrt{\text{Var}(S_1 + S_2)}$):

| $\rho_X$ | $E[S_1+S_2]$ | $\text{Var}(S_1+S_2)$ | $\text{SD}(S_1+S_2)$ | 95% half-width |
|--------:|:-----------:|:---------------------:|:--------------------:|:--------------:|
| $-0.5$  | 20{,}000    | $4 \times 10^6$       | 2{,}000              | 3{,}920        |
| $\phantom{-}0.0$ | 20{,}000 | $8 \times 10^6$       | 2{,}828              | 5{,}544        |
| $+0.5$  | 20{,}000    | $1.2 \times 10^7$     | 3{,}464              | 6{,}789        |
| $+0.9$  | 20{,}000    | $1.52 \times 10^7$    | 3{,}899              | 7{,}642        |

**Read the table:** column 2 is identical across all rows (linearity); column 3 swings by a factor of $3.8\times$ across the range; the half-width of the 95% CI nearly doubles from $\rho = -0.5$ to $\rho = +0.9$.

The factor going from $\rho = 0$ (independent) to $\rho = 0.9$ is $\sqrt{1.9} \approx 1.38\times$ on the standard deviation — modest in absolute terms because we only have 2 variables. The same calculation on $n = 50$ employees, where the formula gives $50 \sigma^2 (1 + 49\rho)$, blows up much more violently: independence gives $50 \sigma^2$, equicorrelation $\rho = 0.2$ gives $50 \sigma^2 \cdot 10.8 = 540 \sigma^2$ — a $10.8\times$ jump in variance and a $\sqrt{10.8} \approx 3.29\times$ jump in standard deviation. That is the Phase 4 picture.

---

## 10. Summary

- $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)$. The cross term is the signature of dependence.
- General form: $\text{Var}(\sum X_i) = \sum \text{Var}(X_i) + 2 \sum_{i<j} \text{Cov}(X_i, X_j) = \boldsymbol{1}^\top \Sigma\, \boldsymbol{1}$.
- Equicorrelation: $\text{Var}(\sum X_i) = n \sigma^2 (1 + (n-1)\rho)$. Linear in $\rho$.
- Effective sample size: $n_\text{eff} = n / (1 + (n-1)\rho)$. Small $\rho$ kills $n_\text{eff}$ quickly when $n$ is large.
- Negative correlation reduces the variance of the sum. Bounded below by $\rho = -1/(n-1)$.
- The **mean** of the sum is invariant across all of this. The **variance** moves by orders of magnitude.

## Why this is the central rhetorical move of the TIL

A reader who has only seen "the mean of a sum is the sum of the means" might walk away thinking sums are easy and uncorrelated. The contrast with the variance formula is what fixes that. The two formulas live one line apart in any probability textbook, and the gap between them — the cross term — is the most expensive object in applied probability work.

## References

- Ross, S. (2014). *A First Course in Probability*, 9th ed. Pearson. Chapter 7, §7.4 (variance of sums and covariance).
- Grimmett, G. & Stirzaker, D. (2001). *Probability and Random Processes*, 3rd ed. Oxford University Press. Chapter 3.
- Mood, A., Graybill, F. & Boes, D. (1974). *Introduction to the Theory of Statistics*, 3rd ed. McGraw-Hill. Chapter IV.
- For the equicorrelated PSD bound: any treatment of compound-symmetric / equicorrelation models in multivariate statistics (e.g., Anderson, T.W. *An Introduction to Multivariate Statistical Analysis*, Chapter 3).
