from __future__ import annotations

from typer.testing import CliRunner

import recoleta.cli


def test_cli_root_help_exposes_only_v2_top_level_groups() -> None:
    runner = CliRunner()

    result = runner.invoke(recoleta.cli.app, ["--help"])

    assert result.exit_code == 0
    assert "run" in result.stdout
    assert "daemon" in result.stdout
    assert "inspect" in result.stdout
    assert "repair" in result.stdout
    assert "stage" in result.stdout
    assert "admin" in result.stdout
    assert "trends-week" not in result.stdout
    assert "repair-streams" not in result.stdout
    assert "materialize" not in result.stdout


def test_removed_cli_entrypoints_show_migration_guidance() -> None:
    runner = CliRunner()

    site_result = runner.invoke(recoleta.cli.app, ["site", "gh-deploy"])
    materialize_result = runner.invoke(recoleta.cli.app, ["materialize", "outputs"])

    assert site_result.exit_code == 2
    assert "run deploy" in site_result.stdout
    assert materialize_result.exit_code == 2
    assert "repair outputs" in materialize_result.stdout
