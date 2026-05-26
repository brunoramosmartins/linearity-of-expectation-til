# Phase 1 — Linearity of Expectation: Proof and Counterexample

## 1. Statement

**Theorem (Linearity of Expectation).** Let $X_1, \ldots, X_n$ be integrable random variables on a common probability space $(\Omega, \mathcal{F}, P)$, and let $a_1, \ldots, a_n \in \mathbb{R}$. Then

$$
E\!\left[\sum_{i=1}^n a_i X_i\right] = \sum_{i=1}^n a_i\, E[X_i].
$$

In particular, taking $a_i = 1$ for all $i$:

$$
E\!\left[\sum_{i=1}^n X_i\right] = \sum_{i=1}^n E[X_i].
$$

**What is not assumed:** independence; identical distributions; uncorrelatedness; any constraint on the joint distribution beyond the existence of $E[X_i]$ for each $i$ and a common probability space.

---

## 2. Discrete Proof (n = 2)

Let $X$ and $Y$ be discrete random variables with joint probability mass function $p_{X,Y}(x, y) = P(X = x, Y = y)$, taking values in countable sets $\mathcal{X}$ and $\mathcal{Y}$, with marginals

$$
p_X(x) = \sum_{y \in \mathcal{Y}} p_{X,Y}(x, y), \qquad p_Y(y) = \sum_{x \in \mathcal{X}} p_{X,Y}(x, y).
$$

Assume $E[|X|] < \infty$ and $E[|Y|] < \infty$ (so all sums below converge absolutely and we may rearrange freely).

By the definition of expectation applied to the random variable $X + Y$:

$$
E[X + Y] = \sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} (x + y)\, p_{X,Y}(x, y).
$$

Split the sum into the $x$-part and the $y$-part:

$$
= \sum_{x} \sum_{y} x \cdot p_{X,Y}(x, y) + \sum_{x} \sum_{y} y \cdot p_{X,Y}(x, y).
$$

In the first double sum, $x$ does not depend on $y$, so we can pull it outside the inner sum:

$$
\sum_{x} \sum_{y} x \cdot p_{X,Y}(x, y) = \sum_{x} x \underbrace{\sum_{y} p_{X,Y}(x, y)}_{=\, p_X(x)} = \sum_{x} x\, p_X(x) = E[X].
$$

Symmetrically, in the second double sum, $y$ does not depend on $x$, so we exchange the order of summation (allowed by absolute convergence) and pull $y$ out:

$$
\sum_{x} \sum_{y} y \cdot p_{X,Y}(x, y) = \sum_{y} y \underbrace{\sum_{x} p_{X,Y}(x, y)}_{=\, p_Y(y)} = \sum_{y} y\, p_Y(y) = E[Y].
$$

Adding the two pieces:

$$
\boxed{\; E[X + Y] = E[X] + E[Y]. \;}
$$

### Where would independence have entered?

Independence is the statement $p_{X,Y}(x, y) = p_X(x)\, p_Y(y)$. Trace the proof above: the joint $p_{X,Y}(x, y)$ appears, but we **never factor it**. We only **marginalize** it — summing over $y$ to recover $p_X(x)$ and over $x$ to recover $p_Y(y)$. Marginalization is the definition of the marginal PMF; it does not require any factorization. The proof is independence-free by construction.

---

## 3. Discrete Proof (general n, by induction)

**Base case ($n = 1$):** $E[X_1] = E[X_1]$. Trivially true.

**Inductive step.** Assume the result holds for $n$ variables; show it holds for $n+1$.

Let $S_n = \sum_{i=1}^n X_i$. Each $S_n$ is a function of $X_1, \ldots, X_n$, hence a random variable on the same probability space. By the $n = 2$ case applied to $S_n$ and $X_{n+1}$:

$$
E[S_{n+1}] = E[S_n + X_{n+1}] = E[S_n] + E[X_{n+1}].
$$

By the inductive hypothesis, $E[S_n] = \sum_{i=1}^n E[X_i]$, so

$$
E[S_{n+1}] = \sum_{i=1}^n E[X_i] + E[X_{n+1}] = \sum_{i=1}^{n+1} E[X_i]. \qquad \blacksquare
$$

The constant multiplier $a_i$ goes through by the same kind of argument: $\sum_{x} (a x)\, p_X(x) = a \sum_{x} x\, p_X(x) = a E[X]$.

---

## 4. General Proof (via linearity of the integral)

Let $X, Y$ be integrable random variables on $(\Omega, \mathcal{F}, P)$, meaning $E[|X|] = \int_\Omega |X|\, dP < \infty$ and similarly for $Y$. The expectation is defined as the Lebesgue integral:

$$
E[X] := \int_\Omega X\, dP.
$$

The Lebesgue integral is **linear**: for any integrable $f, g : \Omega \to \mathbb{R}$ and constants $a, b \in \mathbb{R}$,

$$
\int_\Omega (a f + b g)\, dP = a \int_\Omega f\, dP + b \int_\Omega g\, dP.
$$

This is a property of the integral itself (proved in any measure theory text via the standard construction: simple functions, monotone convergence, then $f = f^+ - f^-$). It does not depend on any structure of $f$ and $g$ beyond integrability.

Applying linearity with $f = X$, $g = Y$, $a = b = 1$:

$$
E[X + Y] = \int_\Omega (X + Y)\, dP = \int_\Omega X\, dP + \int_\Omega Y\, dP = E[X] + E[Y]. \qquad \blacksquare
$$

### Why integrability matters

Without $E[|X|], E[|Y|] < \infty$, the right-hand side could be of the form $\infty - \infty$, which is undefined. For example, let $X$ have $E[X^+] = E[X^-] = \infty$: then $E[X]$ itself is undefined, and "linearity" is vacuous. Integrability is the cheapest hypothesis that makes the statement meaningful, and it is the only one we need.

---

## 5. Counterexample for Products

**Claim.** $E[XY] = E[X]\, E[Y]$ requires independence (or at least zero covariance). It is **not** a free corollary of the definition of expectation.

**Construction.** Let $(X, Y)$ be a discrete random vector with the following joint PMF:

| $(x, y)$ | $(-1, -1)$ | $(+1, +1)$ |
|----------|:----------:|:----------:|
| $p_{X,Y}$ | $1/2$ | $1/2$ |

That is: $P(X = Y = -1) = P(X = Y = +1) = 1/2$, and the joint distribution puts zero mass on the off-diagonal points $(-1, +1)$ and $(+1, -1)$. Equivalently: $X$ and $Y$ are *the same coin flip*, recoded as $\{-1, +1\}$.

**Marginals.** Summing the joint PMF:

$$
p_X(-1) = p_{X,Y}(-1, -1) + p_{X,Y}(-1, +1) = 1/2 + 0 = 1/2,
$$
$$
p_X(+1) = p_{X,Y}(+1, -1) + p_{X,Y}(+1, +1) = 0 + 1/2 = 1/2,
$$

and identically $p_Y(-1) = p_Y(+1) = 1/2$.

**Expectations.** By definition:

$$
E[X] = (-1)\cdot \tfrac{1}{2} + (+1)\cdot \tfrac{1}{2} = 0, \qquad E[Y] = 0.
$$

**Product.** Compute $E[XY]$ directly from the joint PMF:

$$
E[XY] = \sum_{x,y} (xy)\, p_{X,Y}(x, y) = (-1)(-1)\cdot \tfrac{1}{2} + (+1)(+1)\cdot \tfrac{1}{2} = \tfrac{1}{2} + \tfrac{1}{2} = 1.
$$

**Compare.** $E[X]\, E[Y] = 0 \cdot 0 = 0$, but $E[XY] = 1$. Hence

$$
\boxed{\; E[XY] \ne E[X]\, E[Y]. \;}
$$

The identity for products fails — and it fails because $X$ and $Y$ are perfectly dependent ($X = Y$ as random variables).

### Sanity check using linearity (still holds)

Even though $E[XY] \ne E[X] E[Y]$, the **sum** formula must still hold. Verify:

$$
E[X + Y] = \sum_{x,y} (x + y)\, p_{X,Y}(x,y) = (-1 + -1)\cdot \tfrac{1}{2} + (+1 + +1)\cdot \tfrac{1}{2} = -1 + 1 = 0.
$$

And $E[X] + E[Y] = 0 + 0 = 0$. Match. The dependence between $X$ and $Y$ is total, but the sum identity is untouched.

---

## 6. The Asymmetry: Why Sum Is Independence-Free but Product Is Not

The integral is **linear in its argument**: $\int (X + Y)\,dP = \int X\,dP + \int Y\,dP$ for any $X, Y$. But the integral is **not multiplicative** in general: there is no rule that says $\int XY\, dP = \int X\,dP \cdot \int Y\,dP$.

When $X$ and $Y$ are independent, the joint distribution factors as $p_{X,Y}(x,y) = p_X(x) p_Y(y)$, and the multiplicative identity can be recovered:

$$
E[XY] = \sum_{x,y} xy\, p_X(x) p_Y(y) = \left(\sum_x x\, p_X(x)\right)\left(\sum_y y\, p_Y(y)\right) = E[X]\, E[Y].
$$

So independence is exactly the structural hypothesis that lets the product cross the expectation operator. The sum needs no such structure because addition does not require the joint distribution to factor — it only requires marginalization, which is always available.

This is the headline of the TIL: **mean of a sum is bullet-proof, mean of a product is fragile**. The two are different problems with different prerequisites.

---

## 7. Consequence: $\text{Cov}$ is the gap

Define $\text{Cov}(X, Y) := E[XY] - E[X]\, E[Y]$. Then $X, Y$ independent $\Rightarrow$ $\text{Cov}(X, Y) = 0$. In the counterexample above, $\text{Cov}(X, Y) = 1 - 0 = 1$ — the maximum possible for variables of variance 1 each. This sets up Phase 2: covariance is the bookkeeping for what independence buys you in the *variance* formula, and tells you nothing about the mean.

---

## 8. Worked Examples Using Linearity

### 8.1. Sum of three fair dice

Let $D_1, D_2, D_3$ be the outcomes of three independent fair six-sided dice, $S = D_1 + D_2 + D_3$.

**Via linearity:** $E[D_i] = (1+2+3+4+5+6)/6 = 21/6 = 3.5$, so $E[S] = 3 \cdot 3.5 = 10.5$.

**Direct computation (for comparison):** would require the PMF of $S$ over $\{3, 4, \ldots, 18\}$ — sixteen probabilities to enumerate, then weight and sum. The linearity approach takes one line.

Note: the dice happen to be independent here, but the linearity argument would give $E[S] = 10.5$ even if they were correlated (e.g., three dice all showing the same value with probability $1/6$ each).

### 8.2. Binomial mean

Let $X \sim \text{Bin}(n, p)$. Write $X = \sum_{i=1}^n B_i$ where $B_i \sim \text{Bernoulli}(p)$, $E[B_i] = p$. By linearity:

$$
E[X] = \sum_{i=1}^n E[B_i] = n p.
$$

Compare with the direct calculation:

$$
E[X] = \sum_{k=0}^n k \binom{n}{k} p^k (1-p)^{n-k},
$$

which requires the identity $k \binom{n}{k} = n \binom{n-1}{k-1}$ and a reindexing — a more involved argument for the same answer.

### 8.3. Equal-weight two-stock portfolio

Two stocks with daily returns $R_1, R_2$, $E[R_i] = 0.0008$, correlation $\rho = 0.65$. Equal-weight portfolio return:

$$
E\!\left[\tfrac{1}{2} R_1 + \tfrac{1}{2} R_2\right] = \tfrac{1}{2} E[R_1] + \tfrac{1}{2} E[R_2] = 0.0008.
$$

The correlation $\rho$ does **not** appear. It will appear in the variance and in the Sharpe ratio — but the expected return is purely a function of the marginal means.

---

## 9. Summary

- $E[X + Y] = E[X] + E[Y]$ for any integrable $X, Y$ on a common probability space.
- The discrete proof works by marginalizing the joint PMF — never by factoring it. Marginalization is unconditional; factorization is the additional structure that independence provides.
- The general proof reduces to a single line: the Lebesgue integral is linear.
- The analogous identity for products fails without independence: the counterexample $X = Y$ on $\{-1, +1\}$ gives $E[XY] = 1$ but $E[X]E[Y] = 0$.
- The gap $E[XY] - E[X]E[Y]$ is the covariance, which is the right object for variance arithmetic (Phase 2) but irrelevant for the mean.

## References

- Ross, S. (2014). *A First Course in Probability*, 9th ed. Pearson. Chapter 7, §7.2 ("Expectation of Sums of Random Variables").
- Grimmett, G. & Stirzaker, D. (2001). *Probability and Random Processes*, 3rd ed. Oxford University Press. Chapter 3.
- Durrett, R. (2019). *Probability: Theory and Examples*, 5th ed. Cambridge University Press. Chapter 1 — for the measure-theoretic construction of $E[X] = \int X\,dP$ and the linearity of the integral.
