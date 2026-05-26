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
