# 2026-04-03 CLI Orchestration Hotspot Reduction

## Baseline

- Audit date: `2026-04-03`
- Baseline source: `quality/refactor-baseline.json`
- Starting audit summary: `224` hotspots
- CLI slice summary from the initial audit: `48` hotspots
- CLI priority split from the initial audit: `24` `refactor_now` / `refactor_soon`
- Success gate: baseline diff must show `resolved >= 20`, `new = 0`, `worsened = 0`

## Target Hotspots

- `recoleta/cli/workflows.py::_build_granularity_plan`
- `recoleta/cli/workflows.py::_run_translation_step`
- `recoleta/cli/workflows.py::_run_site_deploy_step`
- `recoleta/cli/workflows.py::_execute_invocation`
- `recoleta/cli/workflows.py::execute_granularity_workflow`
- `recoleta/cli/workflows.py::execute_deploy_workflow`
- `recoleta/cli/workflows.py::run_daemon_start_command`
- `recoleta/cli/translate.py::run_translate_run_command`
- `recoleta/cli/translate.py::run_translate_backfill_command`
- `recoleta/cli/materialize.py::run_materialize_outputs_command`
- `recoleta/cli/publish.py::run_publish_command`
- `recoleta/cli/runs.py::_derive_run_context`
- `recoleta/cli/runs.py::_update_run_context`
- `recoleta/cli/__init__.py::_resolve_db_path`
- `recoleta/cli/site.py::run_site_build_command`
- `recoleta/cli/site.py::run_site_stage_command`
- `recoleta/cli/site.py::run_site_serve_command`
- `recoleta/cli/fleet.py::run_fleet_site_serve_command`
- `recoleta/cli/fleet.py::execute_fleet_deploy_workflow`
- `recoleta/cli/maintenance.py::run_gc_command`
- `recoleta/cli/maintenance.py::run_doctor_why_empty_command`
- `recoleta/cli/maintenance.py::_build_source_diagnostics_payload`
- `recoleta/cli/maintenance.py::run_stats_command`
- `recoleta/cli/maintenance.py::run_doctor_command`
- `recoleta/cli/maintenance.py::run_doctor_llm_command`

## Implemented Slice

- Added `recoleta/cli/workflow_models.py`, `recoleta/cli/workflow_steps.py`, and `recoleta/cli/workflow_runner.py` so `recoleta/cli/workflows.py` is back to public entrypoint orchestration.
- Added `recoleta/cli/command_support.py` and moved shared CLI runtime loading, managed-run setup, billing fetch, and error emission behind narrower helpers.
- Added `recoleta/cli/site_support.py` and moved site/fleet manifest loading, output path resolution, default-language handling, and item export scope normalization behind support helpers.
- Added `recoleta/cli/doctor_support.py` and moved source diagnostics, GC payload assembly, stats payload assembly, doctor status rendering, and LLM diagnostics behind smaller support functions.
- Reworked `recoleta/cli/translate.py`, `recoleta/cli/materialize.py`, `recoleta/cli/publish.py`, `recoleta/cli/site.py`, `recoleta/cli/fleet.py`, and `recoleta/cli/maintenance.py` around request/context dataclasses so the command surface stayed stable while the internal orchestration split by responsibility.
- Kept command names, option names, JSON field names, run-context fields, billing metric names, workspace lease behavior, and site deploy semantics unchanged.

## Final Audit Outcome

- Post-refactor audit command: `uv run python scripts/refactor_audit.py`
- Post-refactor hotspot summary: `202` hotspots
- Classification split: `58 refactor_now / 47 refactor_soon / 97 monitor`
- Baseline diff: `resolved=35`, `new=0`, `worsened=0`
- Verdict: `strained`
  Existing hotspots remain, but the current scope did not regress.
- Baseline update command: `uv run python scripts/refactor_audit.py --update-baseline`

This exceeds the branch gate of `resolved >= 20`.

## Validation Commands

- Focused regression suites:
  - `uv run pytest tests/test_recoleta_specs_run_once_cli.py tests/test_recoleta_specs_trends_cli_billing_report.py -q`
  - `uv run pytest tests/test_recoleta_specs_doctor_cli.py tests/test_recoleta_specs_maintenance_cli.py tests/test_instance_first_legacy_config_rejection.py tests/test_recoleta_specs_trends_cli_billing_report.py -q`
  - `uv run pytest tests/test_cli_v2_surface.py tests/test_instance_first_legacy_config_rejection.py tests/test_localization_translation.py tests/test_recoleta_specs_materialize_cli.py tests/test_recoleta_specs_doctor_cli.py tests/test_recoleta_specs_maintenance_cli.py tests/test_recoleta_specs_runs_cli.py -q`
- Full validation:
  - `uv run ruff check .`
  - `uv run pyright`
  - `uv run pytest`
  - `uv run python scripts/refactor_audit.py`
  - `uv run python scripts/refactor_audit.py --update-baseline`
