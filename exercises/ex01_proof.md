# Exercises — Phase 1: Linearity of Expectation

Paper exercises. Work them by hand before reading the solution notes (`notes/phase1-proof.md`). Suggested time budget: 60–90 minutes for the whole set.

## Proofs

### 1. Discrete case (two variables)

Prove the discrete case for two variables. Let $X$ and $Y$ be discrete with joint PMF $p_{X,Y}(x, y)$. Show:

$$
E[X + Y] = \sum_{x, y} (x + y)\, p_{X,Y}(x, y) = \sum_x x\, p_X(x) + \sum_y y\, p_Y(y) = E[X] + E[Y].
$$

**Tasks:**

- Carry the derivation step by step. Mark which step uses marginalization and which (if any) uses factorization.
- Identify exactly where independence would be invoked, and confirm it is **not** used.
- Justify the order-of-summation exchange.

### 2. Generalization to n variables

Prove the result for $n$ variables by induction on $n$. State your inductive hypothesis precisely. Confirm that the base case ($n = 1$ or $n = 2$, your choice) and the inductive step are both independence-free.

### 3. General case via the Lebesgue integral

Let $X$ and $Y$ be integrable random variables on a common probability space $(\Omega, \mathcal{F}, P)$. Show:

$$
E[X + Y] = \int_\Omega (X + Y)\, dP = \int_\Omega X\, dP + \int_\Omega Y\, dP = E[X] + E[Y].
$$

**Tasks:**

- State precisely the integrability assumption that prevents the $\infty - \infty$ pathology.
- Indicate which property of the Lebesgue integral is doing the work (no need to re-derive the integral itself).

### 4. Counterexample for products

Construct a counterexample showing $E[XY] \ne E[X]E[Y]$ in general. Let $X, Y \in \{-1, +1\}$ with

$$
P(X = Y = +1) = P(X = Y = -1) = \tfrac{1}{2},
$$

and zero mass on the off-diagonal points.

**Tasks:**

- Compute the marginal PMFs $p_X$ and $p_Y$.
- Compute $E[X]$, $E[Y]$, and $E[XY]$ directly from the joint PMF.
- Show $E[XY] \ne E[X] E[Y]$ and compute the covariance.
- Verify that, despite this, $E[X + Y] = E[X] + E[Y]$ still holds.

### 5. Independence ⇒ multiplicative expectation (and a partial converse)

Prove that if $X$ and $Y$ are independent discrete random variables, then $E[XY] = E[X] E[Y]$. *Use the fact that the joint PMF factors as $p_{X,Y}(x, y) = p_X(x)\, p_Y(y)$.*

Then state the converse ($E[XY] = E[X] E[Y] \stackrel{?}{\Longrightarrow}$ $X \perp Y$) and produce a counterexample showing that **zero-covariance dependent variables exist**.

*Hint for the counterexample.* Let $Z$ be uniform on $\{-1, 0, +1\}$ and let $X = Z$, $Y = Z^2$. Compute $\text{Cov}(X, Y)$ and verify $X$ and $Y$ are not independent (they share all their information).

---

## Computations

### 6. Three dice

Three fair six-sided dice are rolled. Let $S$ be their sum. Compute $E[S]$ in two ways:

a. Directly from the PMF of $S$ (enumerate the values $S \in \{3, 4, \ldots, 18\}$ and their probabilities).
b. Via linearity, using $E[D_i] = 3.5$.

**Compare the effort.** Then ask: if the three dice were *correlated* (e.g., glued so all three always show the same face), would your answer to (b) change? Would (a) still apply?

### 7. Binomial mean

Let $X \sim \text{Bin}(n, p)$. Compute $E[X]$ via linearity by writing $X = \sum_{i=1}^n B_i$ with $B_i \sim \text{Bernoulli}(p)$. Compare with the direct PMF calculation $\sum_{k=0}^n k \binom{n}{k} p^k (1-p)^{n-k}$ (which requires the identity $k \binom{n}{k} = n \binom{n-1}{k-1}$).

### 8. Two-stock portfolio

Two stocks have daily returns $R_1, R_2$ with $E[R_i] = 0.0008$ and correlation $\rho = 0.65$. Compute the expected return of an equal-weight portfolio,

$$
E\!\left[\tfrac{1}{2} R_1 + \tfrac{1}{2} R_2\right].
$$

*The answer should not contain $\rho$.* If your answer does, recheck where you used the joint distribution — you almost certainly assumed something you didn't need.

---

## Reflection (do this last, in writing)

Answer in 2–4 sentences each:

a. In one sentence, what is the structural reason linearity holds without independence but $E[XY] = E[X] E[Y]$ does not?

b. Give a concrete scenario from your own work (budget modelling, forecasting, A/B testing — anything) where (i) you needed only the mean of a sum and (ii) you needed the variance of a sum. For (i), did you (or anyone you know) waste effort modelling joint structure? For (ii), did anyone treat correlations as a nuisance instead of as the load-bearing input?

c. If a colleague tells you "we assumed independence to compute the expected total revenue", what is the minimum-effort phrasing that fixes their understanding without making them feel cornered?
