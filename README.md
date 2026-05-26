# linearity-of-expectation-til

A portfolio-grade **TIL (Today I Learned)** on the **Linearity of Expectation** — the result that

$$E\!\left[\sum_{i} X_i\right] = \sum_{i} E[X_i]$$

holds **without any independence assumption**. The repository contains the rigorous proof (discrete and general cases), a deliberate variance counterpoint, four classical applications of the indicator-variable trick, and a budget-modelling simulation demonstrating the practical payoff.

The final TIL is short (~300–400 words). The supporting material is intentionally larger — the goal is to *own* the result, not just quote it.

## Project Status

- [x] **Phase 0 — Foundation:** thesis, scope, project scaffold, GitHub configuration.
- [x] **Phase 1 — Proof and Counterexample:** rigorous proof of linearity in discrete and general settings, plus the counterexample for products.
- [x] **Phase 2 — Variance Counterpoint:** $\text{Var}(X+Y)$ decomposition, equicorrelation, effective sample size.
- [ ] **Phase 3 — Indicator Variables and Applications** (in progress): coupon collector, hat-check, inversions, triangles in $G(n, p)$.
- [ ] **Phase 4 — Budget Modelling Simulation**
- [ ] **Phase 5 — TIL Writing**
- [ ] **Phase 6 — Review & Publish**

## Repository Structure

```
linearity-of-expectation-til/
├── .github/           # Issue/PR templates and setup scripts
├── article/           # Final TIL source (Phase 5)
├── docs/              # Thesis, scope, outline
├── exercises/         # Paper exercises (one file per phase)
├── figures/           # Generated plots
├── notebooks/         # Jupyter notebooks (exploration)
├── notes/             # Phase-by-phase theory notes
├── scripts/           # Standalone experiment scripts
├── src/               # Reusable source code
├── tests/             # Unit tests (author runs manually)
├── pyproject.toml     # Dependencies (runtime + dev + notebooks extras)
└── LICENSE
```

## Setup

The author is on **Windows + Python 3.10** and does not use `make`. All commands below are listed explicitly.

### 1. Create the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

On Bash (Git Bash / WSL):

```bash
python -m venv .venv
source .venv/Scripts/activate    # or .venv/bin/activate on Linux/macOS
python -m pip install --upgrade pip
```

### 2. Install the project (editable) with all extras

Dependencies live in `pyproject.toml`. Install in editable mode plus both extras groups (`dev` = ruff/pytest, `notebooks` = jupyter/ipykernel):

```bash
pip install -e ".[dev,notebooks]"
```

This also makes `src/` importable as `from src.<module> import ...`.

Variants:

```bash
pip install -e .                  # runtime only (numpy/scipy/pandas/matplotlib/seaborn)
pip install -e ".[dev]"           # runtime + ruff + pytest
pip install -e ".[notebooks]"     # runtime + jupyter
```

## Quality Checks

These are run **manually by the author**:

```bash
# Lint + format
ruff check .
ruff format .

# Tests
pytest tests/
```

## GitHub Setup

Labels, milestones, and the initial set of issues can be created either via the GitHub web UI (Issues tab → Labels / Milestones / New issue), or by running the setup scripts in `.github/setup/` (these require the [`gh`](https://cli.github.com/) CLI):

```bash
bash .github/setup/labels.sh    owner/repo
bash .github/setup/milestones.sh owner/repo
bash .github/setup/issues.sh    owner/repo
```

## Workflow

- **Branches** follow `phase-N/short-description`, `fix/...`, `docs/...`.
- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.
- **Tags** mark the end of each phase (`v0.x-phase-name`); `v1.0.0` is the public release.
- **Releases** are created only when there is external value (simulation, draft TIL, final TIL).

## License

[MIT](./LICENSE) — see file for full text.

## Author

Bruno Ramos Martins — Analytics Engineer transitioning to Data Science / Machine Learning. Portfolio oriented toward statistical thinking, probabilistic modelling, and applied ML.
