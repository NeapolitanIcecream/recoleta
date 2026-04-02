# Repository Guidelines

## Project Structure & Module Organization
Core code lives in `recoleta/`, with package-level entry points under `recoleta/cli/`, stage orchestration under `recoleta/pipeline/`, SQLite persistence under `recoleta/storage/`, and trend generation in `recoleta/trends.py` plus related publish/site modules. RAG-specific code is isolated under `recoleta/rag/`. Tests live in `tests/`; spec-style files such as `test_recoleta_specs_ingest.py` document expected behavior, while targeted regression tests cover bugs and edge cases. Design notes are in `docs/design/`, ADRs in `docs/adr/`, and helper scripts in `scripts/`. Treat `bench-out*` directories as generated experiment output unless a task explicitly requires them.

## Build, Test, and Development Commands
Use `uv` for local setup and execution.

- `uv sync --group dev`: install runtime and development dependencies.
- `uv run ruff check .`: run lint checks used in CI.
- `uv run pyright`: run static type checking before larger refactors.
- `uv run pytest`: run the full test suite.
- `uv run pytest tests/test_recoleta_specs_ingest.py -q`: run a focused spec or regression test while iterating.
- `uv run recoleta --help`: smoke-test the CLI entry point.
- `uv run python scripts/refactor_audit.py`: audit structural hotspots and refactor pressure using ruff, lizard, complexipy, and vulture.

## Coding Style & Naming Conventions
Target Python 3.14+, use 4-space indentation, and keep code typed. Follow the existing style: `from __future__ import annotations`, `snake_case` for modules/functions/tests, and `PascalCase` for classes. Prefer `pathlib.Path` over raw path strings and keep CLI/help text explicit. Let Ruff drive import ordering and formatting decisions; avoid manual style churn unrelated to the change.

## Testing Guidelines
Pytest is the test runner; `pytest-asyncio` and `respx` support async and HTTP-facing code paths. Add or update tests with every behavior change, especially around pipeline stages, storage, trends, and observability. Keep tests deterministic: use `tmp_path`, `monkeypatch`, and fixtures from `tests/spec_support.py` instead of live network calls. Name new files `test_<feature>.py` and new cases `test_<behavior>`.

## Commit & Pull Request Guidelines
Recent history uses short imperative subjects with optional Conventional Commit scopes, for example `fix(trends): constrain rag searches` and `feat(trends): inject overview pack`. Match that pattern when possible. Keep commits focused, mention config or schema changes in the body, and include the commands you ran (`uv run pytest`, `uv run ruff check .`) in the PR description. If a change affects CLI output, Markdown publishing, or trend documents, include a representative sample in the PR.

## Project-local Codex Skills
Project-specific skills live under `.cursor/skills/`. When a task clearly matches one, load its `SKILL.md` before proceeding.

- `research-site-design-language`: Use for site visuals, UI copy, badges, card hierarchy, section ordering, and markdown-to-site rendering changes. It keeps fixed research-facing chrome in English while allowing long-form body copy to follow the source language.
  When a new design rule becomes canonical or an old one is superseded, update the skill in the same change.
- `proactive-refactoring-methodology`: Use for code-quality audits, structural hotspot reviews, refactor prioritization, and corruption checks based on ruff C901, lizard, complexipy, and vulture. It pairs the audit script with the existing architecture roadmap so refactors follow change axes instead of raw file size.
