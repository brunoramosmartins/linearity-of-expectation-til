# linearity-of-expectation-til

A portfolio-grade **TIL (Today I Learned)** on the **Linearity of Expectation** — the result that

$$E\!\left[\sum_{i} X_i\right] = \sum_{i} E[X_i]$$

holds **without any independence assumption**. The repository contains the rigorous proof (discrete and general cases), a deliberate variance counterpoint, four classical applications of the indicator-variable trick, and a budget-modelling simulation demonstrating the practical payoff.

The final TIL is short (~300–400 words). The supporting material is intentionally larger — the goal is to *own* the result, not just quote it.

## Project Status

**Phase 0 — Foundation** (in progress).
Subsequent phases produce the proof, the variance counterpoint, the indicator-variable applications, the budget simulation, the TIL itself, and the publication pass. See [`roadmap-linearity-of-expectation-til-v1.md`](./roadmap-linearity-of-expectation-til-v1.md) for the full plan.

## Repository Structure

```
linearity-of-expectation-til/
├── .claude/           # Claude Code project rules (CLAUDE.md)
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
├── requirements.txt
├── pyproject.toml
└── roadmap-linearity-of-expectation-til-v1.md
```

## Setup

The author is on **Windows + Python 3.10** and does not use `make`. All commands below are listed explicitly.

### 1. Create the virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Bash (Git Bash / WSL):

```bash
python -m venv .venv
source .venv/Scripts/activate    # or .venv/bin/activate on Linux/macOS
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. (Optional) Install the project in editable mode

```bash
pip install -e .
```

This makes `src/` importable as `from src.<module> import ...`.

## Quality Checks

These are run **manually by the author** (per [`.claude/CLAUDE.md`](./.claude/CLAUDE.md)):

```bash
# Lint + format
ruff check .
ruff format .

# Tests
pytest tests/
```

## GitHub Setup (one-time, after creating the GitHub repo)

```bash
bash .github/setup/labels.sh    owner/repo
bash .github/setup/milestones.sh owner/repo
bash .github/setup/issues.sh    owner/repo
```

Replace `owner/repo` with the actual GitHub slug.

## Workflow

- **Branches** follow `phase-N/short-description`, `fix/...`, `docs/...`.
- **Commits** follow [Conventional Commits](https://www.conventionalcommits.org/): `<type>(<scope>): <description>`.
- **Tags** mark the end of each phase (`v0.x-phase-name`); `v1.0.0` is the public release.
- **Releases** are created only when there is external value (simulation, draft TIL, final TIL).

See [`.claude/CLAUDE.md`](./.claude/CLAUDE.md) for the full set of project rules.

## License

[MIT](./LICENSE) — see file for full text.

## Author

Bruno Ramos Martins — Analytics Engineer transitioning to Data Science / Machine Learning. Portfolio oriented toward statistical thinking, probabilistic modelling, and applied ML.
