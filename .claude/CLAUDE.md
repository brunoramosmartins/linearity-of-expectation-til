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
