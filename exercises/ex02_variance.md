# Exercises — Phase 2: Variance of a Sum

Paper exercises. Work them before consulting `notes/phase2-variance.md`. Time budget: 60–90 minutes.

## Proofs

### 1. The two-variable decomposition

Derive
$$
\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)
$$
starting from the definition $\text{Var}(Z) = E[(Z - E[Z])^2]$. Identify each step where you use linearity of expectation. The proof should use independence **zero times**.

### 2. Generalization to n variables

Show that for any square-integrable $X_1, \ldots, X_n$:
$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2 \sum_{1 \le i < j \le n} \text{Cov}(X_i, X_j).
$$
Two proof paths are acceptable: (a) expand the square inside the expectation; (b) induct on $n$ using the $n = 2$ result. Pick one and carry it through.

### 3. Matrix form

Let $\mathbf{X} = (X_1, \ldots, X_n)^\top$, $\boldsymbol{1} \in \mathbb{R}^n$ the all-ones vector, and $\Sigma$ the covariance matrix of $\mathbf{X}$. Show:
$$
\text{Var}(\boldsymbol{1}^\top \mathbf{X}) = \boldsymbol{1}^\top \Sigma\, \boldsymbol{1}.
$$
More generally, for any constant $\mathbf{a} \in \mathbb{R}^n$, $\text{Var}(\mathbf{a}^\top \mathbf{X}) = \mathbf{a}^\top \Sigma\, \mathbf{a}$. Use the identity $(\mathbf{a}^\top \mathbf{v})^2 = \mathbf{a}^\top \mathbf{v} \mathbf{v}^\top \mathbf{a}$.

### 4. Equicorrelation formula

Suppose $\text{Var}(X_i) = \sigma^2$ for all $i$ and $\text{Cov}(X_i, X_j) = \rho \sigma^2$ for all $i \ne j$ (equicorrelation). Prove:
$$
\text{Var}\!\left(\sum_{i=1}^n X_i\right) = n \sigma^2 \big(1 + (n-1)\rho\big).
$$

Plot this in your head as a function of $\rho$: at $\rho = 0$ you get $n \sigma^2$ (the textbook "square-root-of-n" world); at $\rho = 1$ you get $n^2 \sigma^2$ (no diversification at all); at $\rho = -1/(n-1)$ you get $0$ (perfect cancellation).

### 5. Lower bound on $\rho$ from positive-semidefiniteness

Show that for the equicorrelated covariance matrix
$$
\Sigma = \sigma^2 \big[(1 - \rho) I + \rho J\big]
$$
(where $J$ is the all-ones matrix) to be positive-semidefinite, $\rho$ must satisfy
$$
-\frac{1}{n-1} \le \rho \le 1.
$$
*Hint:* find the eigenvalues of $(1 - \rho) I + \rho J$. There are exactly two distinct ones.

Compute the lower bound for $n = 2, 5, 10, 50, 100$. Note how fast it approaches $0$ as $n$ grows — in large portfolios, only the *tiniest* negative correlations are even feasible.

---

## Computations

### 6. Two correlated LogNormal salaries

Two LogNormal salaries with $E[S_i] = 10{,}000$ and $\text{Var}(S_i) = 4 \times 10^6$ (so $\text{SD}(S_i) = 2{,}000$).

For $\rho \in \{-0.5, 0, +0.5, +0.9\}$:

a. Compute $\text{Var}(S_1 + S_2)$.
b. Compute $\text{SD}(S_1 + S_2)$.
c. By what **factor** does the standard deviation change from $\rho = 0$ to $\rho = +0.9$?

### 7. Effective sample size

Under equicorrelation $\rho$, the variance of the sample mean of $n$ observations is
$$
\text{Var}(\bar X) = \frac{\sigma^2}{n} \big(1 + (n-1)\rho\big) = \frac{\sigma^2}{n_\text{eff}}.
$$

a. Show $n_\text{eff} = n / (1 + (n-1)\rho)$.
b. Compute $n_\text{eff}$ for $n = 50$ and $\rho \in \{0, 0.05, 0.1, 0.2, 0.5, 0.9\}$.
c. The 95% CI for $\bar X$ scales as $1.96 \cdot \sigma / \sqrt{n_\text{eff}}$. Compute the **ratio** of the CI width at $\rho = 0.2$ versus $\rho = 0$. *Sanity check:* it should be approximately $3.13$.

### 8. Portfolio variance under equicorrelation

A portfolio of 100 stocks, each with $\sigma_i = 0.02$ daily and pairwise correlation $\rho = 0.3$. Equal weights $w_i = 1/100$.

a. Under **independence**, what is the portfolio standard deviation $\sigma_p$? (The textbook diversification result.)
b. Under **equicorrelation $\rho = 0.3$**, what is $\sigma_p$?
c. Compute the ratio (b)/(a). Why doesn't diversification work as well as the independence formula suggests?
d. Take $n \to \infty$ at fixed $\rho > 0$. Show $\sigma_p \to \sigma \sqrt{\rho}$, not $0$. This is the **diversification floor**.

---

## Reflection (in writing, 2–4 sentences each)

a. State, in one sentence, the structural reason variance picks up a cross term but the mean does not.

b. Pick a real budget you have built (or seen) and identify a place where positive correlation between line items was probably present but treated as zero. Estimate, qualitatively, by how much the variance of the total was understated.

c. The TIL contrasts $E[X+Y] = E[X] + E[Y]$ (always) with $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X,Y)$ (general). Which line of that contrast do you think is more commonly misremembered or mis-applied in practice, and why?
