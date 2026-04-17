---
name: proactive-refactoring-methodology
description: Evaluate whether the codebase is accumulating structural debt and decide what to refactor next using ruff C901, lizard, complexipy, and vulture. Use when the user asks for code-quality audits, refactor prioritization, architecture hotspots, code corrosion checks, or dead-code review.
---

# Proactive Refactoring Methodology

Use this skill when the goal is to judge whether the current code is merely large or already hard to change safely, or when an agent needs a low-ambiguity next refactor target.

## Workflow

1. Run `uv run ruff check .` first to confirm the normal lint baseline.
2. Run `uv run python scripts/refactor_audit.py` for a whole-repo audit, or pass a narrowed scope such as `uv run python scripts/refactor_audit.py recoleta/pipeline recoleta/site.py`.
3. When you have coverage data, pass it with `--coverage-json <path>`; override the git lookback window with `--lookback-days <days>` only when the default six-month window is clearly wrong for the task.
4. Read `output/refactor-audit/report.md` first for the repo verdict, the agent routing queue, and the subsystem summary.
5. Use `output/refactor-audit/report.json` to inspect symbol-level hotspot evidence, file-level routing scores, history/coupling signals, and baseline changes.
6. Plan refactors by change axis, not by raw file size. Reuse the existing architecture roadmap before inventing a new decomposition.
7. Only run `--update-baseline` when the debt was genuinely reduced or the previous baseline schema/semantics were clearly obsolete.

## Interpretation Rules

- `ruff` C901 is the early warning signal for local control-flow growth.
- `lizard` shows structure pressure through `CCN`, `NLOC`, and parameter count.
- `complexipy` is the main “hard to change safely” signal.
- `vulture` is not permission to delete code. It only produces review candidates.
- The file-level `agent_routing_queue` is the primary “what should an agent touch next?” view. It combines churn, change coupling, ambiguity signals, coverage risk, static pressure, and dead-code concentration.
- The repo verdict now separates `debt_status` from `routing_pressure`. Regression gates still follow hotspots and dead-code baseline changes; routing pressure is advisory.
- The repo verdict includes `signal_health`. Treat `partial` as a real downgrade: the queue is still useful, but missing coverage means the coverage-risk component is inactive.
- Shared-commit coupling ignores commits that touch more than the configured tracked-file threshold. That removes obvious sweep commits, but it is still a heuristic, not a ground-truth dependency graph.
- When you run the audit on an explicit file outside the default target set, history scoring still follows that file instead of silently zeroing it out.
- A symbol hit by both `complexipy` and `lizard` is still a strong local refactor target, but the file-level routing rank should win when it conflicts with a low-churn isolated hotspot.
- `investigate_now` and `investigate_soon` mean the file is a better next refactor candidate than a plain `watch` file, even if all contained hotspots are only `monitor`.
- `refactor_now` still means the scope is already expensive to change and should not keep absorbing behavior work without decomposition.

## Change Discipline

- Behavior changes still require tests.
- Pure structural refactors still require regression coverage to stay green.
- Do not “fix” the audit by raising thresholds to match the current debt level.
- Prefer reducing baseline items through extraction, deletion, or simplification.
