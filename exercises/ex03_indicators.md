# Exercises — Phase 3: Indicator Variables

Paper exercises. Work them before consulting `notes/phase3-indicators.md`. Time budget: 90–120 minutes (these are the most varied of the project).

## Proofs

### 1. Coupon collector

There are $n$ distinct coupon types; each draw is uniform and independent. Let $T$ be the number of draws to collect all $n$.

a. Define $T_i$ as the number of draws to get the $i$-th *new* coupon, given $i - 1$ have been collected. Show that
$$
T_i \sim \text{Geometric}\!\left(\frac{n - i + 1}{n}\right) \quad \Rightarrow \quad E[T_i] = \frac{n}{n - i + 1}.
$$

b. Apply linearity to derive
$$
E[T] = \sum_{i=1}^n \frac{n}{n - i + 1} = n \sum_{k=1}^n \frac{1}{k} = n H_n.
$$

c. **Where is independence used?** State precisely which step requires the i.i.d. assumption on draws, and which step would survive without it.

### 2. Hat-check / derangements

$n$ people leave their hats; hats are returned by a uniform random permutation. Let $F$ be the number of fixed points (people who get own hat back).

a. Define $I_i = \mathbb{1}\{\text{person } i \text{ gets own hat}\}$. Show $P(I_i = 1) = 1/n$ from the uniformity of the permutation.

b. Apply linearity: $E[F] = n \cdot (1/n) = 1$, regardless of $n$.

c. **Show the $I_i$ are not independent.** Compute $P(I_1 = 1, I_2 = 1)$ and compare with $P(I_1 = 1)\, P(I_2 = 1)$. Confirm linearity nonetheless.

d. (Bonus.) Compute $\text{Var}(F)$ using the Phase 2 formula. Hint: it's a clean answer.

### 3. Inversions in a random permutation

For a uniform random permutation $\sigma$ of $\{1, \ldots, n\}$, an *inversion* is a pair $(i, j)$ with $i < j$ but $\sigma(i) > \sigma(j)$. Let $I$ be the number of inversions.

a. Define $I_{ij} = \mathbb{1}\{\sigma(i) > \sigma(j)\}$ for $i < j$. Show $P(I_{ij} = 1) = 1/2$ by a symmetry argument.

b. Apply linearity:
$$
E[I] = \binom{n}{2} \cdot \frac{1}{2} = \frac{n(n-1)}{4}.
$$

c. **Show the $I_{ij}$ are not independent**, in particular for overlapping pairs: if $I_{12} = I_{23} = 1$, then $I_{13} = 1$ is forced. Confirm linearity is undisturbed.

### 4. Triangles in $G(n, p)$

In the Erdős–Rényi random graph $G(n, p)$, each of the $\binom{n}{2}$ edges is present independently with probability $p$. Let $T$ be the number of triangles.

a. Define $T_{ijk} = \mathbb{1}\{\text{the three edges among } \{i,j,k\} \text{ are all present}\}$. Show $P(T_{ijk} = 1) = p^3$.

b. Apply linearity:
$$
E[T] = \binom{n}{3} \cdot p^3 = \frac{n(n-1)(n-2)}{6} p^3.
$$

c. The edges are independent, but the **triangle indicators** $T_{ijk}$ are not. Compute $P(T_{123} = 1, T_{124} = 1)$ — how many edges do these triples share, and what is the probability they all exist?

### 5. The comparison exercise

Pick the **coupon collector** problem specifically. Sketch (do not fully execute) what computing $E[T]$ from the PMF of $T$ would look like.

The PMF involves Stirling numbers of the second kind:
$$
P(T = k) = \frac{n!\, S(k - 1, n - 1)}{n^k}, \qquad k \ge n.
$$

a. Write down the expression $E[T] = \sum_{k \ge n} k \cdot P(T = k)$.

b. Comment on its tractability versus the indicator approach.

c. State, in your own words, what the indicator-variable trick has bought you. (One sentence; the answer is not "it's faster" — say something structural.)

---

## Computations

### 6. Coupon collector numerics

a. For $n = 10$, compute $E[T] = 10 \cdot H_{10}$ to two decimal places. *Sanity check: $H_{10} \approx 2.929$, so $E[T] \approx 29.29$.*

b. For a full standard deck of $n = 52$ cards (one card per draw, with replacement, until all 52 distinct values are seen), compute $E[T]$. Compare with the naive guess of "about $52$".

c. How much does $E[T]$ scale by when $n$ doubles from 50 to 100? *Hint: not by a factor of 2.*

### 7. Hat-check sanity check

For a uniformly random permutation of a $n = 52$ card deck, the expected number of cards in their original position is $1$, regardless of deck size.

a. Compute the variance of this count using the formula from Exercise 2(d).

b. Both mean and variance equal $1$. State the limiting distribution this implies.

### 8. Triangles in a sparse vs dense random graph

a. $G(100, 0.1)$: compute $E[T]$. Is this large enough that you expect to see triangles in any realization?

b. $G(100, 0.01)$: compute $E[T]$. Now most realizations have *zero* triangles. State the rough density threshold (in terms of $p$ as a function of $n$) at which triangles "appear".

c. (Bonus.) The triangle threshold in $G(n, p)$ is $p \sim 1/n$. Verify that at $p = 1/n$, $E[T] \to 1/6$ as $n \to \infty$ — so the *expectation* is constant in the threshold regime, but the *probability of zero triangles* tends to a non-trivial limit (which is what makes the threshold interesting).

---

## Reflection

a. The four problems in this phase have wildly different combinatorial structure (geometric waiting times, derangements, permutation statistics, random graphs). What do they share, structurally, that makes the indicator-variable trick the right tool for each?

b. Pick the problem that surprised you most. What was the surprise — the answer, the simplicity of the derivation, or something else?

c. Sketch a real-world problem from your own work (not from a textbook) that has the indicator structure: a count $N$ that is naturally a sum of 0/1 events. State what $E[N]$ would tell you, and whether you can compute it via linearity even when the events are dependent.
