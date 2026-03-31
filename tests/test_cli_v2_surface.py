from __future__ import annotations

import importlib
from pathlib import Path

import pytest
from typer.testing import CliRunner

import recoleta.cli


cli_app_module = importlib.import_module("recoleta.cli.app")


def test_cli_root_help_exposes_only_v2_top_level_groups() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["--help"])

    assert result.exit_code == 0
    assert "fleet" in result.stdout
    assert "run" in result.stdout
    assert "daemon" in result.stdout
    assert "inspect" in result.stdout
    assert "repair" in result.stdout
    assert "stage" in result.stdout
    assert "admin" in result.stdout
    assert "trends-week" not in result.stdout
    assert "repair-streams" not in result.stdout
    assert "materialize" not in result.stdout


def test_removed_cli_entrypoints_show_direct_replacements_or_fail_closed() -> None:
    runner = CliRunner()

    site_result = runner.invoke(recoleta.cli.app, ["site", "gh-deploy"])
    materialize_result = runner.invoke(recoleta.cli.app, ["materialize", "outputs"])

    assert site_result.exit_code == 2
    assert "run deploy" in site_result.stdout
    assert materialize_result.exit_code == 2
    assert "repair outputs" in materialize_result.stdout


def test_repair_help_hides_legacy_streams_entrypoint() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["repair", "--help"])

    assert result.exit_code == 0
    assert "outputs" in result.stdout
    assert "streams" not in result.stdout


def test_admin_help_hides_removed_migrate_group() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["admin", "--help"])

    assert result.exit_code == 0
    assert "migrate" not in result.stdout


def test_legacy_translate_help_no_longer_exposes_scope_option() -> None:
    runner = CliRunner()

    run_result = runner.invoke(recoleta.cli.app, ["translate", "run", "--help"])
    backfill_result = runner.invoke(
        recoleta.cli.app,
        ["translate", "backfill", "--help"],
    )

    assert run_result.exit_code == 0
    assert "--scope" not in run_result.stdout
    assert backfill_result.exit_code == 0
    assert "--scope" not in backfill_result.stdout


@pytest.mark.parametrize(
    ("argv", "target_name", "expected"),
    [
        (["inspect", "health"], "run_doctor_command", {"command_name": "inspect health"}),
        (["inspect", "stats"], "run_stats_command", {"command_name": "inspect stats"}),
        (["inspect", "llm"], "run_doctor_llm_command", {"command_name": "inspect llm"}),
        (
            ["fleet", "run", "day", "--manifest", "/tmp/fleet.yaml"],
            "execute_fleet_granularity_workflow",
                {
                    "workflow_name": "day",
                    "command": "fleet run day",
                    "manifest_path": Path("/tmp/fleet.yaml").resolve(),
                },
            ),
        (
            ["fleet", "site", "build", "--manifest", "/tmp/fleet.yaml"],
            "run_fleet_site_build_command",
            {
                "command_name": "fleet site build",
                "manifest_path": Path("/tmp/fleet.yaml").resolve(),
            },
        ),
        (
            ["fleet", "site", "serve", "--manifest", "/tmp/fleet.yaml"],
            "run_fleet_site_serve_command",
            {
                "command_name": "fleet site serve",
                "manifest_path": Path("/tmp/fleet.yaml").resolve(),
            },
        ),
        (
            ["inspect", "why-empty", "--date", "2026-03-16"],
            "run_doctor_why_empty_command",
            {"command_name": "inspect why-empty"},
        ),
        (["run", "translate"], "run_translate_run_command", {"command_name": "run translate"}),
        (
            ["stage", "translate", "run"],
            "run_translate_run_command",
            {"command_name": "stage translate run"},
        ),
        (
            ["stage", "translate", "backfill"],
            "run_translate_backfill_command",
            {"command_name": "stage translate backfill"},
        ),
        (
            ["run", "site", "build"],
            "run_site_build_command",
            {"command_name": "run site build"},
        ),
        (
            ["stage", "site", "build"],
            "run_site_build_command",
            {"command_name": "stage site build"},
        ),
        (
            ["stage", "site", "stage"],
            "run_site_stage_command",
            {"command_name": "stage site stage"},
        ),
        (
            ["run", "site", "serve"],
            "run_site_serve_command",
            {
                "command_name": "run site serve",
                "build_command_name": "run site build",
            },
        ),
        (
            ["stage", "site", "serve"],
            "run_site_serve_command",
            {
                "command_name": "stage site serve",
                "build_command_name": "stage site build",
            },
        ),
    ],
)
def test_v2_public_routes_forward_public_command_names(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    target_name: str,
    expected: dict[str, str],
) -> None:
    runner = CliRunner()
    captured: dict[str, object] = {}

    def _fake_command(**kwargs: object) -> None:
        captured.update(kwargs)

    monkeypatch.setattr(cli_app_module, target_name, _fake_command)

    result = runner.invoke(recoleta.cli.app, argv)

    assert result.exit_code == 0, result.stdout
    for key, value in expected.items():
        assert captured[key] == value


@pytest.mark.parametrize(
    ("argv", "target_name", "expected"),
    [
        (
            ["fleet", "run", "day"],
            "execute_fleet_granularity_workflow",
            {
                "workflow_name": "day",
                "command": "fleet run day",
            },
        ),
        (
            ["fleet", "run", "week"],
            "execute_fleet_granularity_workflow",
            {
                "workflow_name": "week",
                "command": "fleet run week",
            },
        ),
        (
            ["fleet", "run", "month"],
            "execute_fleet_granularity_workflow",
            {
                "workflow_name": "month",
                "command": "fleet run month",
            },
        ),
        (
            ["fleet", "run", "deploy"],
            "execute_fleet_deploy_workflow",
            {
                "command": "fleet run deploy",
            },
        ),
        (
            ["fleet", "site", "build"],
            "run_fleet_site_build_command",
            {
                "command_name": "fleet site build",
            },
        ),
        (
            ["fleet", "site", "serve"],
            "run_fleet_site_serve_command",
            {
                "command_name": "fleet site serve",
            },
        ),
    ],
)
def test_fleet_commands_accept_manifest_path_from_env(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    target_name: str,
    expected: dict[str, object],
) -> None:
    runner = CliRunner()
    captured: dict[str, object] = {}
    monkeypatch.setenv("RECOLETA_FLEET_MANIFEST", "/tmp/fleet.yaml")

    def _fake_command(**kwargs: object) -> None:
        captured.update(kwargs)

    monkeypatch.setattr(cli_app_module, target_name, _fake_command)

    result = runner.invoke(recoleta.cli.app, argv)

    assert result.exit_code == 0, result.stdout
    assert captured["manifest_path"] == Path("/tmp/fleet.yaml").resolve()
    for key, value in expected.items():
        assert captured[key] == value
