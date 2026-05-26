# Outline — Linearity of Expectation TIL

Working outline of the final TIL. Numbers in parentheses are target word counts. Strict format: **Hook / Insight / Example / Takeaway**, total 300–400 words.

## Hook (50–80)

**Beat:** In every applied probability class, independence shows up so early and so often that it feels like a prerequisite for everything. It is not. There is exactly one result you actually use every day that does not need it — and you've been using it without checking the fine print.

**Setup:** A budget analyst combines correlated salary estimates; an algorithmist counts triangles in a random graph; a portfolio manager sums asset returns. All three reach for the same formula. All three are right to.

## Insight (80–120)

**Statement of the theorem.** For any integrable $X_1, \ldots, X_n$ on a common probability space:

$$E\!\left[\sum_{i=1}^n X_i\right] = \sum_{i=1}^n E[X_i].$$

No independence. No identically distributed. No joint-distribution assumption beyond a common space and integrability.

**One-line proof sketch:**

$$E[X + Y] = \int (X + Y)\, dP = \int X\, dP + \int Y\, dP = E[X] + E[Y].$$

That's the whole argument. The linearity of the integral does all the work.

**Why this is surprising:** the analogous identity for products, $E[XY] = E[X] E[Y]$, *does* require independence. The mean and the product are different operations, and the integral is linear in one but not the other.

## Example (100–150)

**Setup:** 50-person team, monthly salaries drawn from LogNormal with $E[S_i] = R\$ 10{,}000$. The HR team estimates that salaries are positively correlated within bands (people in similar roles, similar levels).

**Question 1 — Expected total budget:** $E\!\left[\sum_{i=1}^{50} S_i\right] = \sum_{i=1}^{50} E[S_i] = R\$ 500{,}000$. The correlation does not enter the formula.

**Question 2 — Variance of total:** for equicorrelation $\rho$,

$$\text{Var}\!\left(\sum_{i=1}^{50} S_i\right) = 50\,\sigma^2 \big(1 + 49\rho\big).$$

At $\rho = 0.2$, the variance is **roughly $10\times$** the independent-case value, and the 95% CI for the total widens by about $\sqrt{10} \approx 3.2\times$.

**Punchline:** same mean, very different uncertainty.

→ Optional embed: `../figures/correlation_sweep.png`.

## Takeaway (50–80)

Two operational rules:

1. **For the mean of a sum:** do not waste time modelling joint dependence. The marginals fix the answer.
2. **For the variance / CI / quantile of a sum:** the joint dependence is the whole game.

Confusing the two questions produces budgets whose central estimates are correct but whose risk bands are off by a factor of 3 — the kind of error that is invisible until the quarter when everything correlates at once.

---

## Notes on Sources

- Hook draws from `notes/phase1-proof.md` (the independence-everywhere framing).
- Insight uses the proof from `notes/phase1-proof.md` (general/integral case).
- Example uses figures and numbers from `notes/phase4-budget-application.md` and `scripts/exp_correlation_sweep.py`.
- Takeaway echoes the contrast formalized in `notes/phase2-variance.md`.

## Open Questions

- Whether to include the $\rho = -0.5$ regime in the headline example (counterintuitive but distracts from the main point — currently deferred to the figure).
- Whether to mention measure theory by name in the Insight or only allude to "the integral" (currently allude only, to preserve audience).
