#!/bin/bash
# Creates all project issues with full bodies. Run after labels and milestones.
# Usage: bash .github/setup/issues.sh owner/repo

set -euo pipefail

REPO="${1:?Usage: bash issues.sh owner/repo}"

echo "Creating issues for $REPO..."

# ──────────────────────────────────────────────
# PHASE 0 — Foundation
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 0] Write thesis and define scope" \
  --label "phase:0,type:documentation,priority:high" \
  --milestone "Phase 0 — Foundation" \
  --body "## Context
The thesis anchors the TIL. It must be a falsifiable claim about why
linearity of expectation matters specifically because it does not
require independence — and what that means for budget work.

## Tasks
- [ ] Draft central claim (v0.1)
- [ ] Define scope: proof, variance counterpoint, four indicator-variable
      applications, budget simulation
- [ ] Define anti-scope: conditional expectation, total expectation law,
      martingales, concentration inequalities (these are future TILs)
- [ ] Identify target reader and prerequisites (basic probability,
      definition of expected value)
- [ ] Write 1-paragraph abstract

## Definition of Done
- [ ] \`docs/thesis.md\` exists with thesis, scope, anti-scope, audience,
      and abstract
- [ ] Thesis is a single falsifiable sentence

## References
- The author's prior Monte Carlo and probabilistic cost modelling articles"

gh issue create --repo "$REPO" \
  --title "[Phase 0] Configure repository, GitHub templates, and Claude Code rules" \
  --label "phase:0,type:infrastructure,priority:high" \
  --milestone "Phase 0 — Foundation" \
  --body "## Context
Same scaffolding as the Benford TIL repo, adjusted for this topic.

## Tasks
- [ ] Initialize all directories with \`.gitkeep\` where needed
- [ ] Create \`.claude/CLAUDE.md\` with project rules
- [ ] Create \`.github/ISSUE_TEMPLATE/task.md\` and \`bug.md\`
- [ ] Create \`.github/PULL_REQUEST_TEMPLATE.md\`
- [ ] Create \`.github/setup/labels.sh\`, \`milestones.sh\`, \`issues.sh\`
- [ ] Write \`requirements.txt\` with pinned versions
- [ ] Write \`pyproject.toml\` with ruff config
- [ ] Write initial \`README.md\`

## Definition of Done
- [ ] Running the three setup scripts in order produces a fully configured repo
- [ ] \`ruff check .\` passes on the empty scaffold"

# ──────────────────────────────────────────────
# PHASE 1 — Proof and Counterexample
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 1] Prove linearity of expectation in discrete and general cases" \
  --label "phase:1,type:theory,priority:critical" \
  --milestone "Phase 1 — Proof and Counterexample" \
  --body "## Context
The proof is short, but it is the technical core of the TIL. It must be
done rigorously in two settings: discrete (sum over joint PMF) and
general (linearity of the Lebesgue integral).

## Tasks
- [ ] Discrete proof for two variables, then generalize to n variables
- [ ] General proof via linearity of the integral, assuming integrability
- [ ] Standard counterexample: E[XY] ≠ E[X]E[Y] for dependent X, Y
- [ ] Explicit construction with X, Y ∈ {0, 1}, P(X=Y) = 1, p = 1/2
- [ ] Write proof to \`notes/phase1-proof.md\` with no skipped algebra

## Definition of Done
- [ ] Both proofs typed up
- [ ] Counterexample fully worked
- [ ] Exercises drafted in \`exercises/ex01_proof.md\`

## References
- Ross, S. (2014). A First Course in Probability, 9th ed., Ch. 7
- Grimmett & Stirzaker (2001). Probability and Random Processes, Ch. 3"

# ──────────────────────────────────────────────
# PHASE 2 — Variance Counterpoint
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 2] Derive the variance decomposition and show why correlations matter" \
  --label "phase:2,type:theory,priority:high" \
  --milestone "Phase 2 — Variance Counterpoint" \
  --body "## Context
The TIL's main rhetorical move is the contrast between mean and variance.
This phase produces the formal derivation of Var(X+Y) and a numerical
example showing the variance gap between independent and correlated cases.

## Tasks
- [ ] Derive Var(X+Y) = Var(X) + Var(Y) + 2 Cov(X, Y) from definition
- [ ] Generalize to Var(Σ X_i) = Σ Var(X_i) + 2 Σ_{i<j} Cov(X_i, X_j)
- [ ] Numerical example: two LogNormal salaries with ρ ∈ {-0.5, 0, +0.5, +0.9}
- [ ] Tabulate mean, variance, and 95% CI width for each ρ
- [ ] Write notes to \`notes/phase2-variance.md\`

## Definition of Done
- [ ] Decomposition derived in two ways (algebraic and via matrix form)
- [ ] Exercises in \`exercises/ex02_variance.md\`"

# ──────────────────────────────────────────────
# PHASE 3 — Indicator Variables and Applications
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 3] Apply indicator variables to four classical problems" \
  --label "phase:3,type:theory,priority:high" \
  --milestone "Phase 3 — Indicator Variables and Applications" \
  --body "## Context
The indicator-variable trick — write a count as a sum of 0/1 indicators
and use linearity — is the application that makes the theorem famous.
This phase covers four problems where the trick produces a one-line
solution that would otherwise need a generating function or recursion.

## Tasks
- [ ] Coupon collector: E[T] = n · H_n via T = Σ T_i and E[T_i] = n/(n-i+1)
- [ ] Hat-check / derangements: E[fixed points] = 1 regardless of n
- [ ] Inversions in a random permutation: E[I] = n(n-1)/4
- [ ] Triangle count in a random graph G(n, p): E[T] = C(n,3) · p^3
- [ ] Each solution: state problem, define indicators, apply linearity,
      compare with the alternative (much longer) approach
- [ ] Write notes to \`notes/phase3-indicators.md\`

## Definition of Done
- [ ] All four problems solved in \`notes/phase3-indicators.md\`
- [ ] Exercises in \`exercises/ex03_indicators.md\`
- [ ] Implementation in \`src/indicators.py\` for empirical verification

## References
- Mitzenmacher & Upfal (2017). Probability and Computing, 2nd ed., Ch. 2
- Motwani & Raghavan (1995). Randomized Algorithms, Ch. 3"

# ──────────────────────────────────────────────
# PHASE 4 — Budget Modelling Simulation
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 4] Run correlation-sweep simulation on a 50-person team" \
  --label "phase:4,type:experiment,priority:high" \
  --milestone "Phase 4 — Budget Modelling Simulation" \
  --body "## Context
The example in the TIL is a 50-person team with LogNormal salaries. The
simulation must visually confirm that the sample mean is stable across
correlation regimes while the variance and CI width change dramatically.

## Tasks
- [ ] Implement \`src/correlated.py\`: LogNormal marginals via Gaussian
      copula with controllable ρ
- [ ] For each ρ ∈ {-0.5, -0.2, 0, 0.2, 0.5, 0.9}, run K = 10,000 reps
      of n = 50 salaries; compute total
- [ ] Plot: (a) sample mean of total vs ρ (flat line), (b) sample
      variance vs ρ (rising line), (c) 95% CI width vs ρ
- [ ] Produce \`figures/correlation_sweep.png\`
- [ ] Edge case: include the negative-correlation regime (variance drops
      *below* independent case) — a counterintuitive bonus

## Definition of Done
- [ ] Figure shows the mean is visually flat across ρ
- [ ] Figure shows variance varying by at least 2× across the ρ range
- [ ] All scripts use a fixed seed"

# ──────────────────────────────────────────────
# PHASE 5 — TIL Writing
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 5] Write the TIL in Hook / Insight / Example / Takeaway format" \
  --label "phase:5,type:writing,priority:critical" \
  --milestone "Phase 5 — TIL Writing" \
  --body "## Context
Compose the final TIL. Format is strict: Hook / Insight / Example /
Takeaway. Word count 300–400.

## Tasks
- [ ] Draft Hook (50–80 words): the independence-everywhere setup
- [ ] Draft Insight (80–120 words): the theorem + one-line proof sketch
- [ ] Draft Example (100–150 words): the 50-person team with R\$ figures
- [ ] Draft Takeaway (50–80 words): mean vs variance, when each matters
- [ ] Optionally embed \`figures/correlation_sweep.png\`
- [ ] Polish notation and LaTeX

## Definition of Done
- [ ] Word count between 300 and 400
- [ ] Every claim traces to a note or exercise
- [ ] The TIL reads cleanly without the figure (figure is enrichment, not load-bearing)"

# ──────────────────────────────────────────────
# PHASE 6 — Review & Publish
# ──────────────────────────────────────────────

gh issue create --repo "$REPO" \
  --title "[Phase 6] Mathematical and reproducibility review" \
  --label "phase:6,type:review,priority:critical" \
  --milestone "Phase 6 — Review & Publish" \
  --body "## Context
Final pass before publication.

## Tasks
- [ ] Re-derive the variance formula on paper
- [ ] Run \`pytest tests/\` and \`ruff check .\` on a clean clone
- [ ] Re-run all scripts with fixed seeds and confirm figure parity
- [ ] Validate every external reference

## Definition of Done
- [ ] Reviewer's checklist (in PR description) fully ticked"

gh issue create --repo "$REPO" \
  --title "[Phase 6] Publish to GitHub Pages and Medium" \
  --label "phase:6,type:content,priority:high" \
  --milestone "Phase 6 — Review & Publish" \
  --body "## Context
Push the TIL through the MD → HTML pipeline and cross-post.

## Tasks
- [ ] Push article through MD → HTML pipeline
- [ ] Cross-post to Medium with canonical link
- [ ] Draft LinkedIn announcement
- [ ] Tag \`v1.0.0\` and create stable release

## Definition of Done
- [ ] Public URL live on GitHub Pages
- [ ] Medium article published with canonical link"

echo "All issues created successfully."
