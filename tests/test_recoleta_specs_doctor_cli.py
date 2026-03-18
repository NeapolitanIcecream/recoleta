from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path
from typing import Any

from sqlmodel import Session
from typer.testing import CliRunner

import recoleta.cli
import recoleta.cli.maintenance as maintenance_cli
from recoleta.models import Run
from recoleta.storage import Repository


def test_doctor_healthcheck_reports_ok_without_taking_workspace_lease(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    markdown_output_dir = configured_env / "outputs"
    artifacts_dir = configured_env / "artifacts"
    lancedb_dir = configured_env / "lancedb"

    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(lancedb_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    repository.acquire_workspace_lease(
        owner_token="holder-token",
        command="holder",
        lease_timeout_seconds=600,
        run_id="holder-run",
    )

    result = runner.invoke(recoleta.cli.app, ["doctor", "--healthcheck"])

    assert result.exit_code == 0
    assert "healthcheck ok" in result.stdout
    assert "lease=held" in result.stdout
    lease = repository.get_workspace_lease()
    assert lease is not None
    assert lease.command == "holder"


def test_doctor_healthcheck_fails_when_db_is_missing(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "missing.db"

    result = runner.invoke(
        recoleta.cli.app,
        ["doctor", "--healthcheck", "--db-path", str(db_path)],
    )

    assert result.exit_code == 1
    assert "healthcheck failed" in result.stdout


def test_doctor_healthcheck_fails_when_db_uses_older_schema(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "older.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    with repository.engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA user_version = 0")

    result = runner.invoke(
        recoleta.cli.app,
        ["doctor", "--healthcheck", "--db-path", str(db_path)],
    )

    assert result.exit_code == 1
    assert "older schema version" in result.stdout


def test_doctor_healthcheck_fails_when_latest_success_is_too_old(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    markdown_output_dir = configured_env / "outputs"
    artifacts_dir = configured_env / "artifacts"
    lancedb_dir = configured_env / "lancedb"

    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(lancedb_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    run = repository.create_run("fp-old-success", run_id="run-old-success")
    repository.finish_run(run.id, success=True)

    old_success_at = datetime.now(UTC) - timedelta(hours=3)
    with Session(repository.engine) as session:
        row = session.get(Run, run.id)
        assert row is not None
        row.started_at = old_success_at
        row.heartbeat_at = old_success_at
        row.finished_at = old_success_at
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "doctor",
            "--healthcheck",
            "--max-success-age-minutes",
            "30",
        ],
    )

    assert result.exit_code == 1
    assert "latest successful run is too old" in result.stdout


def test_doctor_healthcheck_fails_when_no_successful_run_is_recorded(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    markdown_output_dir = configured_env / "outputs"
    artifacts_dir = configured_env / "artifacts"
    lancedb_dir = configured_env / "lancedb"

    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(lancedb_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))

    repository = Repository(db_path=db_path)
    repository.init_schema()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "doctor",
            "--healthcheck",
            "--max-success-age-minutes",
            "30",
        ],
    )

    assert result.exit_code == 1
    assert "latest successful run is too old" in result.stdout


class _FakeSecret:
    def __init__(self, value: str) -> None:
        self._value = value

    def get_secret_value(self) -> str:
        return self._value


class _FakeLLMSettings:
    def __init__(
        self,
        *,
        llm_model: str = "openai/gpt-4o-mini",
        llm_output_language: str | None = "Chinese (Simplified)",
        llm_api_key: str | None = "sk-recoleta-live",
        llm_base_url: str | None = "http://llm.local/v1",
        config_path: Path | None = None,
    ) -> None:
        self.llm_model = llm_model
        self.llm_output_language = llm_output_language
        self.llm_api_key = _FakeSecret(llm_api_key) if llm_api_key is not None else None
        self.llm_base_url = llm_base_url
        self.config_path = config_path


def test_doctor_llm_json_reports_effective_configuration(
    monkeypatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    settings = _FakeLLMSettings(config_path=tmp_path / "recoleta.yaml")
    monkeypatch.setenv("RECOLETA_LLM_API_KEY", "sk-recoleta-live")
    monkeypatch.setenv("RECOLETA_LLM_BASE_URL", "http://llm.local/v1")
    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda **_: settings)

    result = runner.invoke(recoleta.cli.app, ["doctor", "llm", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["ready"] is True
    assert payload["model"] == "openai/gpt-4o-mini"
    assert payload["provider"] == "openai"
    assert payload["output_language"] == "Chinese (Simplified)"
    assert payload["config_path"] == str(tmp_path / "recoleta.yaml")
    assert payload["connection"]["api_key"]["configured"] is True
    assert payload["connection"]["api_key"]["env_present"] is True
    assert payload["connection"]["api_key"]["fingerprint"] is not None
    assert payload["connection"]["base_url"]["value"] == "http://llm.local/v1"
    assert payload["connection"]["base_url"]["env_present"] is True
    assert payload["ping"]["status"] == "skipped"
    assert "sk-recoleta-live" not in result.stdout


def test_doctor_llm_json_can_run_ping_probe(
    monkeypatch,
) -> None:
    runner = CliRunner()
    settings = _FakeLLMSettings()
    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda **_: settings)

    def _fake_ping(*, settings: Any, timeout_seconds: float) -> dict[str, Any]:
        assert settings is not None
        assert timeout_seconds == 12.0
        return {
            "status": "ok",
            "elapsed_ms": 182,
            "resolved_model": "gpt-4o-mini",
            "response_excerpt": "pong",
            "prompt_tokens": 8,
            "completion_tokens": 1,
            "total_tokens": 9,
            "cost_usd": 0.00012,
        }

    monkeypatch.setattr(maintenance_cli, "_run_llm_ping", _fake_ping)

    result = runner.invoke(
        recoleta.cli.app,
        ["doctor", "llm", "--ping", "--timeout-seconds", "12", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["ping"]["status"] == "ok"
    assert payload["ping"]["elapsed_ms"] == 182
    assert payload["ping"]["resolved_model"] == "gpt-4o-mini"
    assert payload["ping"]["response_excerpt"] == "pong"
    assert payload["ping"]["total_tokens"] == 9


def test_doctor_llm_json_fails_when_ping_probe_fails(
    monkeypatch,
) -> None:
    runner = CliRunner()
    settings = _FakeLLMSettings()
    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda **_: settings)

    def _fake_ping(*, settings: Any, timeout_seconds: float) -> dict[str, Any]:
        _ = (settings, timeout_seconds)
        return {
            "status": "failed",
            "elapsed_ms": 91,
            "error_type": "AuthenticationError",
            "error_message": "invalid api key",
        }

    monkeypatch.setattr(maintenance_cli, "_run_llm_ping", _fake_ping)

    result = runner.invoke(
        recoleta.cli.app,
        ["doctor", "llm", "--ping", "--json"],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert "llm ping failed" in payload["error"]
    assert payload["diagnostics"]["ping"]["status"] == "failed"
    assert payload["diagnostics"]["ping"]["error_type"] == "AuthenticationError"
