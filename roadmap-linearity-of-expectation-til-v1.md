# Roadmap: The Most Useful Theorem in Probability Has No Independence Hypothesis

## Linearity of Expectation — Proof, Variance Counterpoint, and Applications in Budget Modelling

---

## Project Context

Build a **portfolio-grade Today I Learned (TIL)** post on linearity of expectation — the result that $E\!\left[\sum X_i\right] = \sum E[X_i]$ holds without any independence assumption. The TIL is short by design (~300–400 words, Hook / Insight / Example / Takeaway format), but the project around it goes deep: a rigorous proof in both discrete and general cases, a deliberate counterpoint showing why variance *does* need independence, the indicator-variable trick applied to four classical problems, and a budget-modelling simulation that demonstrates the practical payoff. This is **TIL #1 in a planned series**; subsequent TILs in the same repository may cover variance decomposition, the law of total expectation, and concentration inequalities.

### How This Relates to the Author's Other Portfolio Work

| Aspect | Monte Carlo article | Probabilistic Cost Modelling article | This TIL |
|--------|---------------------|--------------------------------------|----------|
| Core question | How to simulate a total budget | Which distributions model components | Why correlations don't affect the mean |
| Mathematical depth | LLN, CLT, variance reduction | MLE, GoF, mixture models | Linearity of expectation, variance decomposition |
| Final length | ~6,000 words | ~6,700 words | ~350 words |
| Role in portfolio | Long-form technical article | Long-form technical article | Short, sharp aphorism with proof |

The TIL is the smallest piece in the portfolio. Its job is to plant a single counterintuitive fact firmly in the reader's head — that independence is not required for the mean of a sum — and to make that fact useful for someone who builds budgets.

### Tech Stack

- Python 3.x
- numpy / scipy (sampling, correlated random variables)
- matplotlib / seaborn (publication-quality figures)
- pandas (small wrangling)
- ruff (linter)
- pytest (testing — author runs manually)

### Author Background

Analytics Engineer transitioning to Data Science / Machine Learning. Background in Mathematics (formal proofs, calculus, linear algebra). Currently working in IT headcount budgeting. Portfolio oriented toward statistical thinking, probabilistic modelling, and applied ML. Publication targets: GitHub Pages (via existing MD → HTML pipeline) and Medium.

### What This Project Is

This is a **TIL for portfolio and personal technical development**, not production software. The final piece is short and follows a tight Hook / Insight / Example / Takeaway format. The development process is deliberately disproportionate to the output length: paper exercises, multiple application proofs, and a correlation-sweep simulation all live in the repository even though only a fraction surfaces in the published TIL. The asymmetry is intentional — the author wants to *own* the result, not just quote it.

---

## Thesis (v0.1)

> "Linearity of expectation — $E\!\left[\sum X_i\right] = \sum E[X_i]$ — holds without any independence, joint-distribution, or identically-distributed assumption. This is not a special case or a textbook simplification; it is a consequence of the linearity of the integral. For a working budget analyst, this means correlation structure is irrelevant when estimating a mean total, but indispensable when estimating its variance or confidence interval. Confusing the two questions is one of the quiet ways a probabilistic budget gets wrong."

### Central Axis

The mean of a sum is bullet-proof. The variance of a sum is fragile. They are not the same question.

```
E[X + Y]   = E[X] + E[Y]                          ← always
Var(X + Y) = Var(X) + Var(Y) + 2·Cov(X, Y)        ← independence-sensitive
```

---

## GitHub Semantic Guide

### Tags

Immutable snapshots marking the end of each phase.

**Convention:** `v0.x-phase-name` for internal milestones, `v1.0.0` for the public portfolio release.

```bash
# After Phase 0
git tag -a v0.1-foundation -m "Phase 0: thesis, scope, project scaffold"
git push origin v0.1-foundation

# Public release
git tag -a v1.0.0 -m "v1.0.0: Linearity of Expectation TIL — proof, variance counterpoint, applications"
git push origin v1.0.0
```

**When to create a tag:** After the phase's PR is merged into `main`.

### Releases

**Rule:** Create a release only when there is external value.

| Tag | Release? | Reasoning |
|-----|----------|-----------|
| `v0.1-foundation` | No | Internal scaffolding |
| `v0.2-proof` | No | Theory notes only |
| `v0.3-variance` | No | Theory notes only |
| `v0.4-indicators` | No | Theory and applications notes |
| `v0.5-simulation` | Yes (pre-release) | Reusable correlation-sweep code + figures |
| `v0.6-article-draft` | Yes (pre-release) | Full draft TIL for feedback |
| `v1.0.0` | **Yes (stable)** | Published TIL |

### Milestones

Each phase = one milestone. All issues within a phase belong to its milestone.

### Issues

Full body: Context, Tasks, Definition of Done, References. Title: `[Phase X] Short description`.

### Relationship

```
Issue → belongs to → Milestone (1 per phase)
Milestone completion → triggers → Tag
Tag (when externally valuable) → triggers → Release
```

---

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                         TIL PIPELINE                             │
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐          │
│  │   Theory    │───▶│    Code     │───▶│   Figures   │          │
│  │   Notes     │    │   (src/)    │    │ (figures/)  │          │
│  │  (notes/)   │    │             │    │             │          │
│  └─────────────┘    └──────┬──────┘    └──────┬──────┘          │
│                            │                  │                  │
│                ┌───────────┴──────────────────┘                  │
│                ▼                                                  │
│  ┌──────────────────────────────────┐                            │
│  │       TIL (article/)             │                            │
│  │  linearity-of-expectation-til.md │                            │
│  └──────────────┬───────────────────┘                            │
│                 │                                                 │
│                 ▼                                                 │
│  ┌──────────────────────────────────┐                            │
│  │  Author's MD → HTML pipeline     │                            │
│  │  (external repo: github.io)      │                            │
│  │  + Medium cross-post             │                            │
│  └──────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                  SIMULATION FLOW (Phase 4)                       │
│                                                                  │
│  ┌────────────────────┐                                          │
│  │ Salary generator    │  Same marginals (LogNormal),            │
│  │ src/correlated.py   │  varying correlation ρ ∈ {-0.5,…,+0.9}  │
│  └─────────┬──────────┘                                          │
│            │                                                     │
│            ▼                                                     │
│  ┌────────────────────┐                                          │
│  │  Compute statistics │  For each ρ, K = 10,000 reps:           │
│  │  src/stats.py       │  - sample mean of total                 │
│  └─────────┬──────────┘  - sample variance of total              │
│            │              - 95% CI width                          │
│            ▼                                                     │
│  ┌──────────────────────────────────┐                            │
│  │  Mean-stable, variance-sensitive │                            │
│  │  figures/correlation_sweep.png   │                            │
│  └──────────────────────────────────┘                            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Repository Structure

```
linearity-of-expectation-til/
│
├── .claude/
│   └── CLAUDE.md                       # Claude Code project rules
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── task.md
│   │   └── bug.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── setup/
│       ├── labels.sh
│       ├── milestones.sh
│       └── issues.sh
│
├── article/                            # Final TIL source
│   └── linearity-of-expectation-til.md
│
├── docs/                               # Project planning documents
│   ├── thesis.md
│   └── outline.md
│
├── src/                                # Reusable source code
│   ├── __init__.py
│   ├── correlated.py                   # Correlated salary generator (Gaussian copula)
│   ├── indicators.py                   # Indicator-variable helpers for classical apps
│   └── stats.py                        # Sample mean / variance / CI helpers
│
├── scripts/                            # Standalone experiment scripts
│   ├── exp_correlation_sweep.py        # Mean stable, variance sensitive
│   ├── exp_coupon_collector.py         # E[T] = n·H_n via indicators
│   ├── exp_hat_check.py                # E[fixed points] = 1 regardless of n
│   └── exp_negative_correlation.py     # Variance can be smaller than independent case
│
├── notebooks/                          # Jupyter notebooks (exploration)
│   ├── 01_proof_intuition.ipynb
│   ├── 02_variance_counterpoint.ipynb
│   └── 03_indicator_applications.ipynb
│
├── exercises/                          # Paper exercises (LaTeX-compatible MD)
│   ├── ex01_proof.md
│   ├── ex02_variance.md
│   └── ex03_indicators.md
│
├── figures/                            # Generated plots and diagrams
│   └── .gitkeep
│
├── notes/                              # Phase-by-phase theory notes
│   ├── phase1-proof.md
│   ├── phase2-variance.md
│   ├── phase3-indicators.md
│   └── phase4-budget-application.md
│
├── tests/                              # Unit tests (author runs manually)
│   ├── test_correlated.py
│   ├── test_indicators.py
│   └── test_stats.py
│
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## Claude Code Configuration

### File: `.claude/CLAUDE.md`

```markdown
# Project Rules — Linearity of Expectation TIL

## What This Project Is

This is a **TIL (Today I Learned) for portfolio and personal technical
development**. It is NOT production software. The primary deliverable is
a short written TIL (~300–400 words, Hook / Insight / Example / Takeaway
format), supported by rigorous notes, paper exercises, and a reproducible
simulation.

The repository is deliberately disproportionate to the TIL length — most
of the depth lives in `notes/` and `exercises/`, not in the final article.
Target reader of the article: a technically competent generalist who
appreciates a one-line proof but wants to see why the result matters.

## Development Rules

### Git & GitHub — CRITICAL RULES

1. **NEVER commit directly.** After any implementation, present the commit
   message and changed files in chat for the author's validation.

2. **NEVER create branches.** The author creates all branches manually.
   When suggesting a branch, only mention the name in the commit/PR proposal.

3. **NEVER create PRs automatically.** Present the PR details in chat.

4. **NEVER push to any branch.** All git operations are done by the author.

5. Follow Conventional Commits: `<type>(<scope>): <short description>`

### Output Format for Commits

After every implementation, present the commit proposal in a **fenced code
block ready to copy**:

~~~
```
git add <files>
git commit -m "<type>(<scope>): <short description>"
```
~~~

### Output Format for PRs

Present the PR proposal in a **fenced code block ready to copy**:

~~~
```
gh pr create \
  --base main \
  --head phase-1/proof-and-counterexample \
  --title "feat(theory): Phase 1 — linearity of expectation proof" \
  --body "## Summary

Adds the rigorous proof of linearity of expectation (discrete and
general cases) plus the standard counterexample showing E[XY] ≠ E[X]E[Y]
in general.

### Deliverables
- \`notes/phase1-proof.md\`
- \`exercises/ex01_proof.md\`
- \`notebooks/01_proof_intuition.ipynb\`

### Checklist
- [x] Code runs without errors
- [x] Tests created (author will run)
- [ ] Author ran \`ruff check .\`
- [ ] Author ran \`pytest tests/\`

Closes #3" \
  --milestone "Phase 1 — Proof and Counterexample"
```
~~~

### Output Format for Tags and Releases

~~~
```
# Tag
git tag -a v0.2-proof -m "Phase 1: linearity of expectation proof"
git push origin v0.2-proof
```
~~~

~~~
```
# Release (only for phases with external value)
gh release create v0.5-simulation \
  --title "v0.5 — Correlation-sweep simulation" \
  --notes "Reproducible mean-stable, variance-sensitive demonstration." \
  --prerelease
```
~~~

### Testing & Linting — CRITICAL

- **Create tests** in `tests/` but **NEVER run them.**
- **NEVER run `ruff`.**
- After creating tests, say:
  "Tests created. Please run `pytest tests/` and `ruff check .` and share
  any failures so we can debug together."

### Code Style

- Python 3.10+ syntax
- Type hints on all function signatures
- Google-style docstrings on public functions
- numpy-style docstrings for mathematical functions
- No Makefile (author is on Windows without `make`)
- Document all commands in `README.md`

### Mathematical Content

- All derivations step-by-step with no skipped algebra
- LaTeX-compatible: `$$...$$` for display, `$...$` for inline
- Every theorem/proposition: statement → proof → example
- Exercises go in `exercises/`, one file per substantive phase

### TIL Output

- Final deliverable: `article/linearity-of-expectation-til.md`
- Processed by the author's existing MD → HTML pipeline (separate repo)
- Format: Hook / Insight / Example / Takeaway (strict)
- Word count target: 300–400 (do not exceed without justification)
- Figures referenced with relative paths: `../figures/<filename>.png`
```

---

## GitHub Setup Scripts

### File: `.github/setup/labels.sh`

```bash
#!/bin/bash
# Creates all project labels. Run once after repo creation.
# Usage: bash .github/setup/labels.sh owner/repo

set -euo pipefail

REPO="${1:?Usage: bash labels.sh owner/repo}"

echo "Creating labels for $REPO..."

# --- Phase labels ---
gh label create "phase:0" --color "0E8A16" --description "Phase 0 — Foundation" --repo "$REPO" --force
gh label create "phase:1" --color "1D76DB" --description "Phase 1 — Proof and Counterexample" --repo "$REPO" --force
gh label create "phase:2" --color "5319E7" --description "Phase 2 — Variance Counterpoint" --repo "$REPO" --force
gh label create "phase:3" --color "D93F0B" --description "Phase 3 — Indicator Variables and Applications" --repo "$REPO" --force
gh label create "phase:4" --color "FBCA04" --description "Phase 4 — Budget Modelling Simulation" --repo "$REPO" --force
gh label create "phase:5" --color "0E8A16" --description "Phase 5 — TIL Writing" --repo "$REPO" --force
gh label create "phase:6" --color "5319E7" --description "Phase 6 — Review & Publish" --repo "$REPO" --force

# --- Type labels ---
gh label create "type:theory" --color "C5DEF5" --description "Mathematical derivation or proof" --repo "$REPO" --force
gh label create "type:code" --color "BFD4F2" --description "Implementation task" --repo "$REPO" --force
gh label create "type:experiment" --color "D4C5F9" --description "Experimental validation or simulation" --repo "$REPO" --force
gh label create "type:writing" --color "FEF2C0" --description "TIL writing task" --repo "$REPO" --force
gh label create "type:documentation" --color "0075CA" --description "Planning or project docs" --repo "$REPO" --force
gh label create "type:infrastructure" --color "E4E669" --description "Repo setup, CI, tooling" --repo "$REPO" --force
gh label create "type:review" --color "F9D0C4" --description "Review or validation task" --repo "$REPO" --force
gh label create "type:bug" --color "D73A4A" --description "Something is broken" --repo "$REPO" --force
gh label create "type:content" --color "BFDADC" --description "LinkedIn, Medium, or social content" --repo "$REPO" --force

# --- Priority labels ---
gh label create "priority:critical" --color "B60205" --description "Must be done, blocks other work" --repo "$REPO" --force
gh label create "priority:high" --color "D93F0B" --description "Important, do soon" --repo "$REPO" --force
gh label create "priority:medium" --color "FBCA04" --description "Can wait but should be done" --repo "$REPO" --force
gh label create "priority:low" --color "0E8A16" --description "Nice to have" --repo "$REPO" --force

echo "All labels created successfully."
```

### File: `.github/setup/milestones.sh`

```bash
#!/bin/bash
# Creates all project milestones. Run once after repo creation.
# Usage: bash .github/setup/milestones.sh owner/repo

set -euo pipefail

REPO="${1:?Usage: bash milestones.sh owner/repo}"

echo "Creating milestones for $REPO..."

gh api "repos/$REPO/milestones" -f title="Phase 0 — Foundation" \
  -f description="Thesis, scope, project scaffold, GitHub configuration." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 1 — Proof and Counterexample" \
  -f description="Rigorous proof of linearity of expectation in discrete and general cases, plus the standard counterexample for products." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 2 — Variance Counterpoint" \
  -f description="Var(X+Y) decomposition, cross-covariance, and why independence matters for variance but not mean." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 3 — Indicator Variables and Applications" \
  -f description="The indicator-variable trick applied to classical problems: coupon collector, hat-check, fixed points of permutations, inversions." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 4 — Budget Modelling Simulation" \
  -f description="Correlated salary simulation showing same mean, different variance across correlation regimes." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 5 — TIL Writing" \
  -f description="Full TIL assembly in Hook / Insight / Example / Takeaway format." \
  -f state="open" --silent

gh api "repos/$REPO/milestones" -f title="Phase 6 — Review & Publish" \
  -f description="Mathematical validation, code reproducibility, publication." \
  -f state="open" --silent

echo "All milestones created successfully."
```

### File: `.github/setup/issues.sh`

```bash
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
- [ ] All four problems solved in `notes/phase3-indicators.md`
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
```

---

## Phase 0 — Foundation

### Objective

Establish the project's intellectual and infrastructural baseline: a falsifiable thesis, a clean repository, and a Claude Code configuration that enforces the GitHub-native workflow throughout the project.

### Tasks

- [ ] **Write thesis and define scope** (Issue #1)
- [ ] **Configure repository, GitHub templates, and Claude Code rules** (Issue #2)

### Deliverables

- [ ] `docs/thesis.md`
- [ ] `.claude/CLAUDE.md`
- [ ] `.github/` templates and setup scripts
- [ ] `requirements.txt`, `pyproject.toml`, `README.md`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-0/foundation` |
| Merge strategy | Squash merge |
| PR title | `chore(setup): Phase 0 — thesis, scope, project scaffold` |
| Milestone | `Phase 0 — Foundation` |
| Tag | `v0.1-foundation` |
| Release | **No** — internal scaffolding |

---

## Phase 1 — Proof and Counterexample

### Objective

Produce the rigorous proof of linearity of expectation in two settings — discrete sums over a joint PMF and the general case via the linearity of the Lebesgue integral — and pair it with the standard counterexample showing that the analogous statement for products, $E[XY] = E[X] E[Y]$, fails without independence. The asymmetry between the two is the central pedagogical move of the TIL.

### Tasks

- [ ] **Prove linearity of expectation in discrete and general cases** (Issue #3)
- [ ] **Write theory notes**

### Deliverables

- [ ] `notes/phase1-proof.md`
- [ ] `exercises/ex01_proof.md`
- [ ] `notebooks/01_proof_intuition.ipynb`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-1/proof-and-counterexample` |
| Merge strategy | Squash merge |
| PR title | `feat(theory): Phase 1 — linearity of expectation proof` |
| Milestone | `Phase 1 — Proof and Counterexample` |
| Tag | `v0.2-proof` |
| Release | **No** — theory only |

### 📝 Exercises — After Phase 1

**File: `exercises/ex01_proof.md`**

#### Proofs (paper)

1. **Prove** the discrete case for two variables. Let $X$ and $Y$ be discrete with joint PMF $p_{X,Y}(x, y)$. Show:

   $$E[X + Y] = \sum_{x, y} (x + y)\, p_{X,Y}(x, y) = \sum_x x\, p_X(x) + \sum_y y\, p_Y(y) = E[X] + E[Y].$$

   Identify exactly where independence would be invoked, and confirm it is not used.

2. **Generalize** to $n$ variables by induction on $n$.

3. **Prove** the general case via the linearity of the Lebesgue integral. Let $X$ and $Y$ be integrable random variables on a common probability space $(\Omega, \mathcal{F}, P)$. Show:

   $$E[X + Y] = \int_\Omega (X + Y)\, dP = \int_\Omega X\, dP + \int_\Omega Y\, dP = E[X] + E[Y].$$

   State precisely the integrability assumption that prevents $\infty - \infty$ pathology.

4. **Construct a counterexample** for products. Let $X, Y \in \{-1, +1\}$ with $P(X = Y = 1) = P(X = Y = -1) = 1/2$. Compute $E[X]$, $E[Y]$, $E[XY]$, and show $E[XY] \ne E[X] E[Y]$.

5. **Prove** that if $X$ and $Y$ are independent, then $E[XY] = E[X] E[Y]$. *Use the fact that the joint PMF factors as $p_{X,Y}(x, y) = p_X(x) p_Y(y)$.* Then state the converse and produce a counterexample (zero-covariance dependent variables exist).

#### Computations (paper)

6. Three dice are rolled. Let $S$ be their sum. Compute $E[S]$ in two ways: (a) directly from the PMF of $S$, and (b) via linearity. Compare effort.

7. Let $X \sim \text{Bin}(n, p)$. Compute $E[X]$ via linearity by writing $X = \sum_{i=1}^n B_i$ with $B_i \sim \text{Bernoulli}(p)$. Compare with the direct PMF calculation.

8. Two stocks have daily returns $R_1, R_2$ with $E[R_i] = 0.0008$ and correlation $\rho = 0.65$. Compute the expected return of an equal-weight portfolio. *The answer should not contain $\rho$.*

---

## Phase 2 — Variance Counterpoint

### Objective

Derive the variance of a sum and show, both algebraically and numerically, why correlations affect variance even though they do not affect the mean. This phase produces the contrast that gives the TIL its rhetorical edge: the mean is bullet-proof; the variance is not.

### Tasks

- [ ] **Derive the variance decomposition and show why correlations matter** (Issue #4)
- [ ] **Write theory notes**

### Deliverables

- [ ] `notes/phase2-variance.md`
- [ ] `exercises/ex02_variance.md`
- [ ] `notebooks/02_variance_counterpoint.ipynb`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-2/variance-counterpoint` |
| Merge strategy | Squash merge |
| PR title | `feat(theory): Phase 2 — variance decomposition` |
| Milestone | `Phase 2 — Variance Counterpoint` |
| Tag | `v0.3-variance` |
| Release | **No** — theory only |

### 📝 Exercises — After Phase 2

**File: `exercises/ex02_variance.md`**

#### Proofs (paper)

1. **Derive** $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\,\text{Cov}(X, Y)$ from the definition $\text{Var}(Z) = E[(Z - E[Z])^2]$.

2. **Generalize** to $n$ variables:

   $$\text{Var}\!\left(\sum_{i=1}^n X_i\right) = \sum_{i=1}^n \text{Var}(X_i) + 2 \sum_{1 \le i < j \le n} \text{Cov}(X_i, X_j).$$

3. **Re-derive** the same result in matrix form. Let $\mathbf{X} = (X_1, \ldots, X_n)^\top$, $\boldsymbol{1} \in \mathbb{R}^n$, and $\Sigma$ the covariance matrix. Show:

   $$\text{Var}(\boldsymbol{1}^\top \mathbf{X}) = \boldsymbol{1}^\top \Sigma \boldsymbol{1}.$$

4. **Prove** that under positive equicorrelation $\rho > 0$ with common variance $\sigma^2$, $\text{Var}\!\left(\sum X_i\right) = n \sigma^2 (1 + (n - 1)\rho)$. *Plot this as a function of $\rho$ in your head: at $\rho = 1$, the variance is $n^2 \sigma^2$, not $n \sigma^2$.*

5. **Show** that negative equicorrelation can make $\text{Var}\!\left(\sum X_i\right)$ smaller than the independent case. State the lower bound on $\rho$ that keeps $\Sigma$ positive semidefinite.

#### Computations (paper)

6. Two LogNormal salaries with $E[S_i] = 10{,}000$ and $\text{Var}(S_i) = 4 \times 10^6$. Compute $\text{Var}(S_1 + S_2)$ for $\rho \in \{-0.5, 0, +0.5, +0.9\}$. *By what factor does the standard deviation change from the independent case at $\rho = +0.9$?*

7. The 95% CI width for the sample mean scales as $1.96 \cdot \sigma / \sqrt{n}$ under independence. Show that under equicorrelation $\rho$, the *effective* sample size shrinks to $n / (1 + (n-1)\rho)$. *Compute the effective $n$ when $n = 50$ and $\rho = 0.2$.*

8. A portfolio of 100 stocks each with $\sigma_i = 0.02$ daily and pairwise correlation $\rho = 0.3$. Compute portfolio variance under (a) independence and (b) the equicorrelated structure. *Why doesn't diversification work as well as the independent case suggests?*

---

## Phase 3 — Indicator Variables and Classical Applications

### Objective

Showcase the indicator-variable trick — express a count as a sum of 0/1 indicators and apply linearity — on four classical problems where it produces a one-line solution that would otherwise require generating functions, recursions, or careful inclusion-exclusion. This is the phase that demonstrates *why* the theorem is the most useful in probability.

### Tasks

- [ ] **Apply indicator variables to four classical problems** (Issue #5)
- [ ] **Implement empirical verification in `src/indicators.py`**
- [ ] **Write theory notes**

### Deliverables

- [ ] `notes/phase3-indicators.md`
- [ ] `exercises/ex03_indicators.md`
- [ ] `src/indicators.py`
- [ ] `tests/test_indicators.py`
- [ ] `notebooks/03_indicator_applications.ipynb`
- [ ] `scripts/exp_coupon_collector.py`
- [ ] `scripts/exp_hat_check.py`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-3/indicator-applications` |
| Merge strategy | Squash merge |
| PR title | `feat(theory): Phase 3 — indicator-variable applications` |
| Milestone | `Phase 3 — Indicator Variables and Applications` |
| Tag | `v0.4-indicators` |
| Release | **No** — theory and tools |

### 📝 Exercises — After Phase 3

**File: `exercises/ex03_indicators.md`**

#### Proofs (paper)

1. **Coupon collector.** There are $n$ distinct coupon types; each draw is uniform and independent. Let $T$ be the number of draws to collect all $n$. Define $T_i$ as the number of draws needed to get the $i$-th *new* coupon, given $i - 1$ collected. Show that $T_i \sim \text{Geometric}(\, (n - i + 1)/n\,)$, so $E[T_i] = n/(n - i + 1)$, and by linearity:

   $$E[T] = \sum_{i=1}^n \frac{n}{n - i + 1} = n \sum_{k=1}^n \frac{1}{k} = n H_n.$$

   *Note that the $T_i$ are independent here, but linearity would hold without this — independence is used only to compute the individual $E[T_i]$.*

2. **Hat-check.** $n$ people leave their hats; hats are returned uniformly at random. Let $F$ be the number who get their own hat back. Define $I_i = \mathbb{1}\{\text{person } i \text{ gets own hat}\}$. Show $P(I_i = 1) = 1/n$, hence $E[F] = n \cdot (1/n) = 1$. *Crucially, the $I_i$ are not independent — yet linearity gives the answer instantly.*

3. **Inversions in a random permutation.** For a uniform random permutation $\sigma$ of $\{1, \ldots, n\}$, let $I$ be the number of pairs $(i, j)$ with $i < j$ but $\sigma(i) > \sigma(j)$. Define $I_{ij} = \mathbb{1}\{\sigma(i) > \sigma(j)\}$ for $i < j$. Show $P(I_{ij} = 1) = 1/2$, and:

   $$E[I] = \binom{n}{2} \cdot \frac{1}{2} = \frac{n(n - 1)}{4}.$$

4. **Triangles in a random graph.** In $G(n, p)$, each of the $\binom{n}{2}$ edges exists independently with probability $p$. Let $T$ be the number of triangles. Show:

   $$E[T] = \binom{n}{3} p^3.$$

5. **Compare** each indicator-variable solution to the alternative (PMF computation or generating function). For coupon collector specifically, write out what computing $E[T]$ from the PMF of $T$ would look like — and why it is awful.

#### Computations (paper)

6. For $n = 10$ coupons, compute $E[T] = 10 \cdot H_{10}$ to two decimal places. *Sanity check: $H_{10} \approx 2.929$.*

7. For a 52-card deck shuffled uniformly, the expected number of cards in their original position is $1$, regardless of the deck size. *Verify by computing the variance: it is also approximately $1$, which is striking.*

8. A random graph $G(100, 0.1)$. Compute $E[T]$ for the number of triangles. *Is this number large enough that we should expect to see triangles in any realization?*

---

## Phase 4 — Budget Modelling Simulation

### Objective

Run the simulation that backs the example in the TIL: a 50-person team with LogNormal salaries under varying correlation regimes. Demonstrate empirically that the sample mean of the total is stable across correlations, while the variance and CI width are not. Include the counterintuitive negative-correlation regime as a bonus point.

### Tasks

- [ ] **Run correlation-sweep simulation on a 50-person team** (Issue #6)

### Deliverables

- [ ] `src/correlated.py`
- [ ] `src/stats.py`
- [ ] `tests/test_correlated.py`, `tests/test_stats.py`
- [ ] `scripts/exp_correlation_sweep.py`
- [ ] `scripts/exp_negative_correlation.py`
- [ ] `notes/phase4-budget-application.md`
- [ ] `figures/correlation_sweep.png`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-4/budget-simulation` |
| Merge strategy | Squash merge |
| PR title | `feat(experiments): Phase 4 — correlation-sweep simulation` |
| Milestone | `Phase 4 — Budget Modelling Simulation` |
| Tag | `v0.5-simulation` |
| Release | **Yes (pre-release)** — reusable simulation + figure for peer review |

---

## Phase 5 — TIL Writing

### Objective

Compose the final TIL in the strict Hook / Insight / Example / Takeaway format, matching the target length of 300–400 words. The figure from Phase 4 is optionally embedded — the TIL should read cleanly without it.

### TIL Structure

| Block | Source | Target Words |
|-------|--------|-------------:|
| Hook | Phase 1 (the independence-everywhere setup) | 50–80 |
| Insight | Phase 1 (theorem + one-line proof sketch) | 80–120 |
| Example | Phase 4 (50-person team) | 100–150 |
| Takeaway | Phase 2 (mean vs variance) | 50–80 |
| | **Total** | **300–400** |

### Tasks

- [ ] **Write the TIL in Hook / Insight / Example / Takeaway format** (Issue #7)

### Deliverables

- [ ] `article/linearity-of-expectation-til.md`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-5/til-writing` |
| Merge strategy | Squash merge |
| PR title | `feat(article): Phase 5 — full TIL draft` |
| Milestone | `Phase 5 — TIL Writing` |
| Tag | `v0.6-article-draft` |
| Release | **Yes (pre-release)** — full draft for feedback |

---

## Phase 6 — Review and Publish

### Objective

Final mathematical validation, code reproducibility check, and publication.

### Tasks

- [ ] **Mathematical and reproducibility review** (Issue #8)
- [ ] **Publish to GitHub Pages and Medium** (Issue #9)

### Deliverables

- [ ] Published TIL on GitHub Pages
- [ ] Medium cross-post with canonical link
- [ ] LinkedIn post draft
- [ ] Final `README.md`

### GitHub

| Item | Value |
|------|-------|
| Branch | `phase-6/publish` |
| Merge strategy | Squash merge |
| PR title | `chore(publish): Phase 6 — final review and publication` |
| Milestone | `Phase 6 — Review & Publish` |
| Tag | `v1.0.0` |
| Release | **Yes (stable)** — public portfolio release |

---

## GitHub Workflow Standards

### Branch Naming Convention

```
phase-N/short-description     # phase work
fix/short-description          # bug fixes
docs/short-description         # documentation only
```

### Conventional Commits

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(core): implement correlated salary generator` |
| `fix` | Bug fix | `fix(stats): correct CI width formula` |
| `docs` | Documentation | `docs(thesis): refine scope boundaries` |
| `test` | Tests | `test(indicators): cover hat-check edge cases` |
| `refactor` | Restructuring | `refactor(correlated): unify copula API` |
| `chore` | Maintenance | `chore(github): add issue templates` |
| `style` | Formatting | `style(article): fix LaTeX alignment` |

### Pull Request Template

```markdown
## Summary

Closes #

## Type of Change

- [ ] New feature (`feat`)
- [ ] Bug fix (`fix`)
- [ ] Documentation (`docs`)
- [ ] Refactor (`refactor`)
- [ ] Test (`test`)

## Checklist

- [ ] Code runs without errors
- [ ] Tests created (author will run `pytest tests/`)
- [ ] Author ran `ruff check .`
- [ ] Documentation updated (if applicable)
- [ ] Figures regenerated (if applicable)
- [ ] No hardcoded paths or secrets

## Mathematical Validation (if applicable)

- [ ] Derivations reviewed for correctness
- [ ] Numerical examples match code output
```

### Issue Templates

#### Task (`.github/ISSUE_TEMPLATE/task.md`)

```markdown
---
name: Task
about: A specific piece of work
labels: ''
---

## Context

## Tasks
- [ ] Task 1

## Definition of Done
- [ ] Criterion 1

## References
```

#### Bug (`.github/ISSUE_TEMPLATE/bug.md`)

```markdown
---
name: Bug
about: Something is not working as expected
labels: 'type:bug'
---

## Description

## Steps to Reproduce
1.

## Expected Behaviour

## Actual Behaviour

## Environment
- Python version:
- OS:
```

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 0 — Foundation | 1 day | Week 1 |
| Phase 1 — Proof and Counterexample | 2–3 days | Week 1 |
| Phase 2 — Variance Counterpoint | 2–3 days | Week 1–2 |
| Phase 3 — Indicator Variables and Applications | 3–4 days | Week 2 |
| Phase 4 — Budget Modelling Simulation | 2–3 days | Week 2–3 |
| Phase 5 — TIL Writing | 1–2 days | Week 3 |
| Phase 6 — Review & Publish | 1–2 days | Week 3 |

**Total: 2–3 weeks** (part-time, evenings and weekends).

*Paper exercises are done between phases. Budget 1–2 hours per exercise set.*

---

## Skills This TIL Develops

| Skill | How It's Demonstrated |
|-------|----------------------|
| Foundational probability | Rigorous proof of linearity in discrete and general cases |
| Measure-theoretic literacy | General proof via linearity of the Lebesgue integral |
| Combinatorial reasoning | Four indicator-variable applications, each with the trick made explicit |
| Variance / covariance algebra | Matrix-form derivation and the effective-sample-size formula under equicorrelation |
| Correlated random variable simulation | Gaussian copula for LogNormal marginals with controlled $\rho$ |
| Scientific communication | Tight 300–400 word TIL in a strict structural format |
| Software engineering | Modular code, fixed seeds, manual test/lint workflow, GitHub-native PR cadence |

---

## References

### Core Textbooks

- Ross, S. (2014). *A First Course in Probability*, 9th ed. Pearson. (Chapter 7: properties of expectation)
- Grimmett, G. & Stirzaker, D. (2001). *Probability and Random Processes*, 3rd ed. Oxford University Press.
- Durrett, R. (2019). *Probability: Theory and Examples*, 5th ed. Cambridge University Press.

### Supplementary

- Mitzenmacher, M. & Upfal, E. (2017). *Probability and Computing*, 2nd ed. Cambridge University Press. (Chapter 2 has the cleanest treatment of the indicator-variable technique.)
- Motwani, R. & Raghavan, P. (1995). *Randomized Algorithms*. Cambridge University Press.
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*, Vol. 1, 3rd ed. Wiley.

### Python Libraries

- NumPy: array operations, random sampling
- SciPy: `scipy.stats` (LogNormal), Gaussian copula via `multivariate_normal`
- Matplotlib / Seaborn: publication-quality figures
- Pandas: small dataset wrangling
