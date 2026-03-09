from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path

from sqlmodel import Session
from typer.testing import CliRunner

import recoleta.cli
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
