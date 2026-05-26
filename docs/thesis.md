# Thesis — Linearity of Expectation TIL

## Central Claim (v0.1)

> Linearity of expectation — $E\!\left[\sum_{i} X_i\right] = \sum_{i} E[X_i]$ — holds without any independence, joint-distribution, or identically-distributed assumption. This is not a special case or a textbook simplification; it is a direct consequence of the linearity of the integral. For a working budget analyst, this means **correlation structure is irrelevant when estimating a mean total, but indispensable when estimating its variance or confidence interval.** Confusing the two questions is one of the quiet ways a probabilistic budget gets wrong.

The claim is falsifiable: produce a counterexample where $E[X + Y] \ne E[X] + E[Y]$ for integrable random variables on a common probability space, and the thesis collapses. No such counterexample exists — that is the point.

## Central Axis

The **mean** of a sum is bullet-proof. The **variance** of a sum is fragile. They are not the same question.

$$
\begin{aligned}
E[X + Y]   &= E[X] + E[Y] && \leftarrow \text{always} \\
\text{Var}(X + Y) &= \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y) && \leftarrow \text{independence-sensitive}
\end{aligned}
$$

## Scope

The TIL and its supporting repository cover:

1. **Rigorous proof of linearity of expectation** in two settings:
   - Discrete case (sum over the joint PMF).
   - General case via the linearity of the Lebesgue integral, under integrability.
2. **Variance counterpoint:** algebraic and matrix-form derivation of $\text{Var}\!\left(\sum X_i\right)$, plus the effective-sample-size argument under equicorrelation.
3. **Four classical applications of the indicator-variable trick:**
   - Coupon collector ($E[T] = n H_n$).
   - Hat-check / derangements ($E[\text{fixed points}] = 1$).
   - Inversions in a random permutation ($E[I] = n(n-1)/4$).
   - Triangles in $G(n, p)$ ($E[T] = \binom{n}{3} p^3$).
4. **Budget-modelling simulation:** 50-person team with LogNormal salaries under correlation $\rho \in \{-0.5, -0.2, 0, 0.2, 0.5, 0.9\}$, demonstrating mean stability and variance sensitivity.

## Anti-Scope

The following are deliberately **excluded** from this TIL and will be covered in future TILs in the same series:

- Conditional expectation $E[X \mid \mathcal{G}]$ and its tower property.
- Law of total expectation (formal treatment).
- Martingales and optional stopping.
- Concentration inequalities (Markov, Chebyshev, Chernoff, Hoeffding).
- Copulas beyond the Gaussian case used for simulation.
- Bayesian interpretation of expectation.

The exclusion is intentional: the TIL is a 300–400 word piece, and the supporting repository is sized to *own* the headline result, not to survey the surrounding theory.

## Target Reader

A **technically competent generalist**: someone with a background in quantitative work — analytics, engineering, applied science, finance — who has seen expected values before but has not stopped to verify which assumptions the basic results actually need. The reader appreciates a one-line proof but cares more about why the result is *useful* than about measure theory.

### Prerequisites Assumed

- Definition of a random variable and its expected value.
- Familiarity with elementary probability (sample spaces, PMFs, basic distributions like Binomial and LogNormal).
- Comfort reading $\sum$ and $\int$ notation.

### Prerequisites *Not* Assumed

- Measure theory, $\sigma$-algebras, Lebesgue integration (the general proof is sketched, not used as the primary path).
- Copulas, multivariate distributions beyond the Gaussian.
- Any prior exposure to the indicator-variable trick.

## Abstract

Linearity of expectation — the statement that $E[X + Y] = E[X] + E[Y]$ for any integrable random variables — is the rare probabilistic identity that needs no independence assumption. This TIL proves the identity in both the discrete and general (Lebesgue) settings, contrasts it sharply with the variance of a sum (which *does* depend on covariance), and demonstrates the practical payoff on a budget-modelling problem: a 50-person team with correlated LogNormal salaries shows a stable mean total across correlation regimes and a variance that swings by more than $2\times$. The intended takeaway is operational — when the question is *how big is the average*, correlation does not matter; when the question is *how wrong could we be*, it matters a great deal.

## Role in the Portfolio

This is **TIL #1** in a planned series. It is the smallest piece in the author's portfolio (~350 words versus the ~6,000-word Monte Carlo and probabilistic cost modelling articles), and its job is to plant one counterintuitive fact firmly in the reader's head — that independence is *not* required for the mean of a sum — and to make that fact useful for someone who builds budgets.

Subsequent TILs in the series may cover variance decomposition in depth, the law of total expectation, and concentration inequalities. Each TIL is designed to compose with the others without requiring them.
