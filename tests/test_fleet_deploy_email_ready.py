from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
import yaml

import recoleta.cli
import recoleta.site_deploy as site_deploy
from recoleta.publish import write_markdown_trend_note
from recoleta.site_email_links import (
    email_links_artifact_path,
    load_email_links_artifact,
)


def _clear_runtime_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "RECOLETA_CONFIG_PATH",
        "RECOLETA_DB_PATH",
        "LLM_MODEL",
        "MARKDOWN_OUTPUT_DIR",
        "PUBLISH_TARGETS",
        "TOPICS",
        "EMAIL",
        "RECOLETA_RESEND_API_KEY",
        "LOCALIZATION",
        "WORKFLOWS",
    ):
        monkeypatch.delenv(name, raising=False)


def _write_config(path: Path, payload: dict[str, Any]) -> Path:
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def _write_email_enabled_fleet(tmp_path: Path) -> tuple[Path, Path]:
    output_dir = tmp_path / "alpha-output"
    trend_note_path = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=527,
        title="Agent delivery systems",
        granularity="day",
        period_start=datetime(2026, 5, 26, tzinfo=UTC),
        period_end=datetime(2026, 5, 27, tzinfo=UTC),
        run_id="run-fleet-email-ready",
        overview_md="## Overview\n\nAgent delivery systems now rely on deploy-ready artifacts.\n",
        topics=["agents", "delivery"],
        clusters=[],
    )
    config_path = _write_config(
        tmp_path / "alpha.yaml",
        {
            "recoleta_db_path": str(tmp_path / "alpha.db"),
            "llm_model": "openai/gpt-4o-mini",
            "topics": ["agents"],
            "publish_targets": ["markdown"],
            "markdown_output_dir": str(output_dir),
            "workflows": {"deploy": {"translation": "off"}},
            "email": {
                "public_site_url": "https://public.example/recoleta",
                "from_email": "updates@example.com",
                "to": ["reader@example.com"],
                "granularities": ["day"],
            },
        },
    )
    manifest_path = _write_config(
        tmp_path / "fleet.yaml",
        {
            "schema_version": 1,
            "instances": [{"name": "alpha", "config_path": str(config_path)}],
        },
    )
    return manifest_path, trend_note_path


def _fake_successful_deploy(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    def _deploy(**_: object) -> SimpleNamespace:
        return SimpleNamespace(
            remote="origin",
            branch="gh-pages",
            remote_url="https://example.com/repo.git",
            repo_root=tmp_path,
            commit_sha="deadbeef",
            skipped=False,
            pages_source=SimpleNamespace(
                site_url="https://public.example/recoleta",
                status="configured",
            ),
        )

    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    monkeypatch.setattr(fleet_cli_module, "run_translate_run_command", lambda **_: None)
    monkeypatch.setattr(
        fleet_cli_module,
        "run_materialize_outputs_command",
        lambda **_: None,
    )
    monkeypatch.setattr(
        site_deploy,
        "deploy_trend_static_site_to_github_pages",
        _deploy,
    )


def test_fleet_run_deploy_refreshes_canonical_site_and_email_link_map(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, trend_note_path = _write_email_enabled_fleet(tmp_path)
    _fake_successful_deploy(monkeypatch, tmp_path)
    execute_fleet_deploy_workflow = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="execute_fleet_deploy_workflow",
    )

    payload = execute_fleet_deploy_workflow(
        manifest_path=manifest_path,
        command="fleet run deploy",
        include=None,
        skip=None,
        repo_dir=tmp_path / "site-repo",
        json_output=True,
    )

    site_dir = manifest_path.parent / "site"
    artifact_path = email_links_artifact_path(site_output_dir=site_dir)
    assert (site_dir / "manifest.json").exists()
    assert artifact_path.exists()
    links = load_email_links_artifact(artifact_path=artifact_path)
    assert (
        str(trend_note_path.resolve()) in links["pages_by_source_markdown"]
    )
    assert payload["site"]["output_dir"] == str(site_dir)


def test_fleet_email_preview_resolves_page_after_deploy_without_manual_site_build(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _trend_note_path = _write_email_enabled_fleet(tmp_path)
    _fake_successful_deploy(monkeypatch, tmp_path)
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    execute_fleet_deploy_workflow = getattr(
        fleet_cli_module,
        "execute_fleet_deploy_workflow",
    )
    run_fleet_email_preview_command = getattr(
        fleet_cli_module,
        "run_fleet_email_preview_command",
    )

    execute_fleet_deploy_workflow(
        manifest_path=manifest_path,
        command="fleet run deploy",
        include=None,
        skip=None,
        repo_dir=tmp_path / "site-repo",
        json_output=True,
    )

    payload = run_fleet_email_preview_command(
        manifest_path=manifest_path,
        instance="alpha",
        anchor_date="2026-05-26",
        output_dir=tmp_path / "preview",
        granularities=["day"],
        json_output=True,
        command_name="fleet run email preview",
    )

    assert payload["status"] == "succeeded"
    assert payload["results"][0]["primary_page_url"].startswith(
        "https://public.example/recoleta/trends/"
    )
