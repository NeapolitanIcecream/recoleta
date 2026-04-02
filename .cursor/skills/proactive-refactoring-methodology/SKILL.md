---
name: proactive-refactoring-methodology
description: Evaluate whether the codebase is accumulating structural debt and decide what to refactor next using ruff C901, lizard, complexipy, and vulture. Use when the user asks for code-quality audits, refactor prioritization, architecture hotspots, code corrosion checks, or dead-code review.
---

# Proactive Refactoring Methodology

Use this skill when the goal is to judge whether the current code is merely large or already hard to change safely.

## Workflow

1. Run `uv run ruff check .` first to confirm the normal lint baseline.
2. Run `uv run python scripts/refactor_audit.py` for a whole-repo audit, or pass a narrowed scope such as `uv run python scripts/refactor_audit.py recoleta/pipeline recoleta/site.py`.
3. Read `output/refactor-audit/report.md` first for the repo verdict and the prioritized queue.
4. Use `output/refactor-audit/report.json` to inspect function-level evidence, metric deltas, and baseline changes.
5. Plan refactors by change axis, not by raw file size. Reuse the existing architecture roadmap before inventing a new decomposition.
6. Only run `--update-baseline` when the debt was genuinely reduced or the old baseline was clearly wrong.

## Interpretation Rules

- `ruff` C901 is the early warning signal for local control-flow growth.
- `lizard` shows structure pressure through `CCN`, `NLOC`, and parameter count.
- `complexipy` is the main “hard to change safely” signal.
- `vulture` is not permission to delete code. It only produces review candidates.
- A symbol hit by both `complexipy` and `lizard` should be treated as the highest-priority refactor target.
- `refactor_now` means the scope is already expensive to change and should not keep absorbing behavior work without decomposition.

## Change Discipline

- Behavior changes still require tests.
- Pure structural refactors still require regression coverage to stay green.
- Do not “fix” the audit by raising thresholds to match the current debt level.
- Prefer reducing baseline items through extraction, deletion, or simplification.
