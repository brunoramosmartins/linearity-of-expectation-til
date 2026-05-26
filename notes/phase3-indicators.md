# Phase 3 — Indicator Variables and Classical Applications

## 1. The Trick

Many counting questions can be phrased as "how many things of type X happen?". Each such question has a random variable $N$ whose value is the count.

**The indicator-variable trick** is to write
$$
N = \sum_{i \in \mathcal{I}} \mathbb{1}_{A_i},
$$
where $\mathcal{I}$ is the index set of "things that could happen" and $A_i$ is the event "thing $i$ happened". The indicator $\mathbb{1}_{A_i}$ takes value $1$ if $A_i$ occurs and $0$ otherwise.

Then by **linearity of expectation** (Phase 1):
$$
E[N] = \sum_{i \in \mathcal{I}} E[\mathbb{1}_{A_i}] = \sum_{i \in \mathcal{I}} P(A_i).
$$

That is: the expected count is the sum of the probabilities of the individual events, **regardless of whether the events $A_i$ are independent or not**. The decoupling is exactly the Phase 1 result, packaged into a one-line algorithm.

### Why this is the most useful theorem in probability

The trick reduces a hard counting problem (which would otherwise require generating functions, recursion, or inclusion–exclusion) to:

1. **Identify** the indicators: name the events $A_i$ and the index set.
2. **Compute** a single probability $P(A_i)$ — typically a one-line calculation by symmetry.
3. **Sum** $\sum_i P(A_i)$ — often a closed form.

The four problems below all yield to this template. None of them would yield to a direct PMF calculation in less than several pages.

---

## 2. Coupon Collector

### Problem

A vendor sells $n$ distinct types of coupons; each purchase yields a uniformly random coupon, independent of past purchases. Let $T$ be the number of purchases needed to collect **all** $n$ types. What is $E[T]$?

### Indicator decomposition

Define $T_i$ as the number of additional purchases needed to acquire the **$i$-th new** coupon, *given that $i - 1$ distinct coupons have already been collected*. Then
$$
T = T_1 + T_2 + \cdots + T_n.
$$

After collecting $i - 1$ distinct coupons, each new purchase is a "new" coupon with probability $p_i = (n - i + 1) / n$ (there are $n - i + 1$ uncollected types out of $n$). So $T_i$ is a **geometric** random variable with success probability $p_i$:
$$
T_i \sim \text{Geometric}(p_i), \qquad E[T_i] = \frac{1}{p_i} = \frac{n}{n - i + 1}.
$$

### Apply linearity

By linearity:
$$
E[T] = \sum_{i=1}^n E[T_i] = \sum_{i=1}^n \frac{n}{n - i + 1} = n \sum_{k=1}^n \frac{1}{k} = n\, H_n,
$$
where $H_n = 1 + 1/2 + \cdots + 1/n$ is the $n$-th harmonic number. Since $H_n \approx \ln n + \gamma$ (with $\gamma \approx 0.5772$ the Euler–Mascheroni constant), we have $E[T] \approx n \ln n + \gamma n$.

### Numerics

| $n$ | $H_n$ | $E[T] = n H_n$ |
|----:|------:|---------------:|
|   5 | 2.283 |  11.42 |
|  10 | 2.929 |  29.29 |
|  20 | 3.598 |  71.95 |
|  50 | 4.499 | 224.96 |
| 100 | 5.187 | 518.74 |

To collect all $52$ playing cards (one per draw), you would expect $52 \cdot H_{52} \approx 235.98$ draws — about $4.5 \times$ as many as the number of cards.

### Remark — independence is used here, but not by linearity

The $T_i$ are themselves independent (each one starts fresh once the previous goal is reached, and successive draws are i.i.d.). Independence was used in computing $E[T_i] = 1/p_i$. But the **linearity step** $E[T] = \sum E[T_i]$ does not need it — that is the headline.

If we modified the problem so that purchases came in mildly correlated batches (e.g., adjacent draws favoured the same coupon type), the $T_i$ would no longer be independent, the individual $E[T_i]$ would change, but the decomposition $E[T] = \sum E[T_i]$ would still hold by linearity.

### Compared with the alternative

Computing $E[T]$ from the PMF of $T$ requires the Stirling-number-of-the-second-kind machinery:
$$
P(T = k) = \frac{n!\, S(k - 1, n - 1)}{n^k},
$$
where $S$ denotes Stirling numbers. Then
$$
E[T] = \sum_{k=n}^\infty k \cdot \frac{n!\, S(k - 1, n - 1)}{n^k},
$$
an awful sum. The indicator-variable approach gives $E[T] = n H_n$ in three lines.

---

## 3. Hat-Check / Fixed Points of a Random Permutation

### Problem

$n$ people leave their hats at the door. The hats are returned uniformly at random — that is, the assignment is drawn uniformly from all $n!$ permutations of $\{1, \ldots, n\}$. Let $F$ be the number of people who receive their **own** hat back. What is $E[F]$?

### Indicator decomposition

For $i = 1, \ldots, n$ let
$$
I_i = \mathbb{1}\{\text{person } i \text{ gets own hat back}\}.
$$
Then $F = I_1 + I_2 + \cdots + I_n$.

For a uniformly random permutation, person $i$'s position is equally likely to receive any of the $n$ hats. So
$$
P(I_i = 1) = \frac{1}{n}.
$$

### Apply linearity

$$
E[F] = \sum_{i=1}^n P(I_i = 1) = n \cdot \frac{1}{n} = 1.
$$

**Regardless of $n$, the expected number of fixed points is exactly $1$.** Whether $n = 5$, $n = 50$, or $n = 5{,}000{,}000$, you expect one person to get their own hat back.

### Why this is striking

The $I_i$ are **strongly dependent**. If $I_i = 1$ (person $i$ got their own hat), it changes the conditional distribution for every other person — there are now $(n-1)!$ permutations consistent with this, and the remaining assignment is uniform on those. So the events are not independent, and they are not even pairwise independent (the conditional probability shifts).

But linearity does not care. The dependence shows up in the *variance* of $F$, not in $E[F]$.

### The variance, for completeness

For $i \ne j$, $P(I_i = 1, I_j = 1) = \frac{(n-2)!}{n!} = \frac{1}{n(n-1)}$, so
$$
\text{Cov}(I_i, I_j) = \frac{1}{n(n-1)} - \frac{1}{n^2} = \frac{1}{n^2(n-1)}.
$$

Using $\text{Var}(F) = \sum \text{Var}(I_i) + 2 \sum_{i<j} \text{Cov}(I_i, I_j)$:
$$
\text{Var}(F) = n \cdot \frac{1}{n}\!\left(1 - \frac{1}{n}\right) + 2 \binom{n}{2} \cdot \frac{1}{n^2(n-1)} = \left(1 - \frac{1}{n}\right) + \frac{1}{n} = 1.
$$

So $E[F] = \text{Var}(F) = 1$ for every $n \ge 2$. The number of fixed points of a random permutation is **asymptotically Poisson(1)** — both moments match exactly for any $n$, and the full distribution converges. That is the "derangement" classical result.

### Compared with the alternative

The direct attack computes $P(F = k)$ via inclusion–exclusion on the events $\{I_i = 1\}$:
$$
P(F = k) = \frac{1}{k!} \sum_{j=0}^{n-k} \frac{(-1)^j}{j!},
$$
and then $E[F] = \sum k \cdot P(F = k)$. The result is the same, but the derivation is several pages. The indicator approach gives $E[F] = 1$ in one line.

---

## 4. Inversions in a Random Permutation

### Problem

Let $\sigma$ be a uniformly random permutation of $\{1, 2, \ldots, n\}$. An **inversion** is an ordered pair $(i, j)$ with $i < j$ but $\sigma(i) > \sigma(j)$. Let $I$ be the total number of inversions. What is $E[I]$?

Inversions count how "out of order" the permutation is. The identity has $0$ inversions; the reversed permutation has $\binom{n}{2}$. The sorting complexity of insertion sort is exactly $I$.

### Indicator decomposition

For each ordered pair $1 \le i < j \le n$, define
$$
I_{ij} = \mathbb{1}\{\sigma(i) > \sigma(j)\}.
$$
Then $I = \sum_{1 \le i < j \le n} I_{ij}$.

By symmetry — under a uniform random permutation, $(\sigma(i), \sigma(j))$ is equally likely to be in either order — $P(I_{ij} = 1) = 1/2$.

### Apply linearity

$$
E[I] = \sum_{1 \le i < j \le n} P(I_{ij} = 1) = \binom{n}{2} \cdot \frac{1}{2} = \frac{n(n-1)}{4}.
$$

### Numerics

| $n$ | $\binom{n}{2}$ | $E[I] = n(n-1)/4$ |
|----:|---------------:|------------------:|
|   5 |  10 |   2.5  |
|  10 |  45 |  11.25 |
|  20 | 190 |  47.5  |
|  50 | 1225 | 306.25 |
| 100 | 4950 | 1237.5 |

A random permutation of $\{1, \ldots, 100\}$ has, on average, $1237.5$ pairs out of order — out of a maximum possible $4950$. Half-sorted on average, by linearity, exactly.

### Why the indicators are not independent

If $I_{12} = 1$ (i.e., $\sigma(1) > \sigma(2)$) and $I_{23} = 1$ (i.e., $\sigma(2) > \sigma(3)$), then $\sigma(1) > \sigma(3)$, which forces $I_{13} = 1$. So the indicators on overlapping pairs are *not* independent — they satisfy logical constraints. Linearity is again unbothered.

---

## 5. Triangles in a Random Graph $G(n, p)$

### Problem

In the Erdős–Rényi random graph $G(n, p)$, each of the $\binom{n}{2}$ potential edges between $n$ vertices is independently present with probability $p$. A **triangle** is a set of three vertices, all three pairs of which are connected. Let $T$ be the number of triangles. What is $E[T]$?

### Indicator decomposition

For each unordered triple $\{i, j, k\} \subseteq \{1, \ldots, n\}$, define
$$
T_{ijk} = \mathbb{1}\{\text{edges } ij, jk, ik \text{ all present}\}.
$$

Then $T = \sum_{\{i,j,k\}} T_{ijk}$, where the sum runs over all $\binom{n}{3}$ triples.

The three edges in any fixed triple are independent (by the $G(n, p)$ definition), each present with probability $p$. So
$$
P(T_{ijk} = 1) = p^3.
$$

### Apply linearity

$$
E[T] = \binom{n}{3} \cdot p^3 = \frac{n(n-1)(n-2)}{6}\, p^3.
$$

### Numerics

For $n = 100$ and $p = 0.1$:
$$
E[T] = \binom{100}{3} \cdot (0.1)^3 = 161{,}700 \cdot 0.001 = 161.7.
$$

A reasonable expectation that we will see triangles in any realization — and indeed, $G(100, 0.1)$ contains a substantial triangle structure with high probability.

For $n = 100$ and $p = 0.01$:
$$
E[T] = 161{,}700 \cdot 10^{-6} = 0.1617.
$$

At this sparser density, most realizations have *zero* triangles — the expected count is below $1$. This is the threshold regime that motivates much of random graph theory.

### Independence of edges, dependence of triangles

The edges are independent (built into the $G(n, p)$ model). But the **triangle indicators** $T_{ijk}$ are not independent: any two triangles that share an edge are positively correlated. For example, $T_{123}$ and $T_{124}$ share the edge $\{1, 2\}$, so $P(T_{123} = 1, T_{124} = 1) = p^5 > p^6 = P(T_{123} = 1) P(T_{124} = 1)$. Linearity ignores this dependence for the mean; it shows up in $\text{Var}(T)$ and in the variance-based thresholds for triangle existence.

---

## 6. A Cross-Cutting Pattern

In all four problems:

| Problem | Indicators | $P(A_i)$ | $|\mathcal{I}|$ | Total $E[N]$ |
|---|---|---|---|---|
| Coupon collector | $T_i$ — wait for $i$-th new coupon | $n/(n-i+1)$ | $n$ | $n H_n$ |
| Hat-check | $I_i$ — person $i$ gets own hat | $1/n$ | $n$ | $1$ |
| Inversions | $I_{ij}$ — pair $(i,j)$ inverted | $1/2$ | $\binom{n}{2}$ | $n(n-1)/4$ |
| Triangles | $T_{ijk}$ — triple forms triangle | $p^3$ | $\binom{n}{3}$ | $\binom{n}{3} p^3$ |

The template is identical in each: define indicators that decompose the count, compute one probability by symmetry, sum. The dependence structure of the indicators (independent in coupon collector and triangles; not independent in hat-check; logically constrained in inversions) **never enters** the mean computation.

---

## 7. When Linearity Is Not Enough

Linearity gives you $E[N]$. It tells you nothing about:

- $\text{Var}(N)$, which depends on $\text{Cov}(\mathbb{1}_{A_i}, \mathbb{1}_{A_j})$ — Phase 2 machinery.
- $P(N \ge k)$ for $k$ much larger than $E[N]$ — concentration inequalities, beyond this TIL's scope.
- The distribution of $N$ — requires generating functions or direct analysis.

But for the question "what is the *typical* count?", linearity is usually all you need, and it works without independence. That is the case the TIL makes.

---

## 8. References

- Mitzenmacher, M. & Upfal, E. (2017). *Probability and Computing*, 2nd ed. Cambridge University Press. Chapter 2 ("Discrete Random Variables and Expectation") has the cleanest single-chapter treatment of the indicator trick, including all four problems above.
- Motwani, R. & Raghavan, P. (1995). *Randomized Algorithms*. Cambridge University Press. Chapter 3 — covers triangles in random graphs and is the canonical reference for the threshold regime.
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*, Vol. 1, 3rd ed. Wiley. Chapter IV.4 has the classical hat-check / derangement derivation via inclusion–exclusion, for comparison.
- Bollobás, B. (2001). *Random Graphs*, 2nd ed. Cambridge University Press. The standard reference for $G(n, p)$.
