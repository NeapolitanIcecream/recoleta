from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import io
import sqlite3
from pathlib import Path

from loguru import logger as loguru_logger
import pytest
from sqlmodel import Session
from typer.testing import CliRunner

import recoleta.cli
from recoleta.models import RUN_STATUS_FAILED, Run
from recoleta.storage import (
    CURRENT_SCHEMA_VERSION,
    Repository,
    SchemaVersionError,
    WorkspaceLeaseHeldError,
)


def test_init_schema_sets_user_version_and_runtime_tables(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")

    repository.init_schema()

    with sqlite3.connect(repository.db_path) as conn:
        version = int(conn.execute("PRAGMA user_version").fetchone()[0])
        run_columns = {
            str(row[1]) for row in conn.execute("PRAGMA table_info(runs)").fetchall()
        }
        lease_tables = {
            str(row[0])
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

    assert version == CURRENT_SCHEMA_VERSION
    assert "heartbeat_at" in run_columns
    assert "workspace_leases" in lease_tables


def test_init_schema_rejects_newer_schema_version(tmp_path: Path) -> None:
    db_path = tmp_path / "future.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(f"PRAGMA user_version = {CURRENT_SCHEMA_VERSION + 1}")
        conn.commit()

    repository = Repository(db_path=db_path)

    with pytest.raises(SchemaVersionError, match="newer schema version"):
        repository.init_schema()


def test_workspace_lease_blocks_second_owner_until_release(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    repository.acquire_workspace_lease(
        run_id="run-1",
        command="ingest",
        owner_token="token-1",
        lease_timeout_seconds=90,
        hostname="host-a",
        pid=101,
    )

    with pytest.raises(WorkspaceLeaseHeldError) as exc:
        repository.acquire_workspace_lease(
            run_id="run-2",
            command="publish",
            owner_token="token-2",
            lease_timeout_seconds=90,
            hostname="host-b",
            pid=202,
        )

    assert exc.value.holder_run_id == "run-1"
    assert exc.value.holder_command == "ingest"

    assert repository.release_workspace_lease(owner_token="token-1") is True

    repository.acquire_workspace_lease(
        run_id="run-2",
        command="publish",
        owner_token="token-2",
        lease_timeout_seconds=90,
        hostname="host-b",
        pid=202,
    )


def test_mark_stale_runs_failed_marks_expired_running_run(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    run = repository.create_run(config_fingerprint="fp-stale", run_id="run-stale")

    stale_at = datetime(2026, 3, 1, tzinfo=UTC)
    now = stale_at + timedelta(seconds=120)

    with Session(repository.engine) as session:
        row = session.get(Run, run.id)
        assert row is not None
        row.started_at = stale_at
        row.heartbeat_at = stale_at
        session.add(row)
        session.commit()

    recovered = repository.mark_stale_runs_failed(
        stale_after_seconds=90,
        now=now,
    )

    assert recovered == 1

    with Session(repository.engine) as session:
        row = session.get(Run, run.id)
        assert row is not None
        assert row.status == RUN_STATUS_FAILED
        assert row.finished_at == now


@dataclass(slots=True)
class _FakeRun:
    id: str


class _LockingRepo:
    def __init__(self) -> None:
        self.created: list[tuple[str, str | None]] = []

    def acquire_workspace_lease(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id,
        command,
        owner_token,
        lease_timeout_seconds,
        hostname=None,
        pid=None,
    ) -> None:
        _ = (command, owner_token, lease_timeout_seconds, hostname, pid)
        raise WorkspaceLeaseHeldError(
            lease_name="workspace",
            holder_run_id="run-active",
            holder_command="publish",
            holder_hostname="host-b",
            holder_pid=202,
            expires_at=datetime(2026, 3, 9, 12, 0, tzinfo=UTC),
            requested_run_id=run_id,
        )

    def mark_stale_runs_failed(  # type: ignore[no-untyped-def]
        self, *, stale_after_seconds, now=None
    ) -> int:
        _ = (stale_after_seconds, now)
        return 0

    def create_run(  # type: ignore[no-untyped-def]
        self, *, config_fingerprint, run_id=None
    ) -> _FakeRun:
        self.created.append((str(config_fingerprint), run_id))
        return _FakeRun(id=str(run_id or "run-1"))

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(  # type: ignore[no-untyped-def]
        self, *, owner_token, lease_timeout_seconds
    ) -> None:
        _ = (owner_token, lease_timeout_seconds)

    def release_workspace_lease(self, *, owner_token: str) -> bool:
        _ = owner_token
        return False

    def finish_run(self, run_id: str, *, success: bool) -> None:
        _ = (run_id, success)


class _FakeSettings:
    log_json = False
    publish_targets: list[str] = []

    def safe_fingerprint(self) -> str:
        return "fp-lock"


def test_ingest_cli_exits_when_workspace_lock_is_held(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: a second writer should fail fast instead of creating another run."""

    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _LockingRepo()
    fake_service = object()
    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="WARNING", serialize=True)

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    try:
        result = runner.invoke(recoleta.cli.app, ["ingest"])
    finally:
        loguru_logger.remove(sink_id)

    assert result.exit_code == 1
    assert "workspace is locked" in result.stdout
    assert fake_repo.created == []
    assert "cli.runtime.lock" in stream.getvalue()


@pytest.mark.parametrize(
    ("argv", "command_name"),
    [
        (["site", "build"], "site build"),
        (["site", "stage"], "site stage"),
    ],
)
def test_site_cli_defaults_exit_when_workspace_lock_is_held(
    configured_env: Path,
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    command_name: str,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    markdown_output_dir = configured_env / "output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    repository = Repository(db_path=db_path)
    repository.init_schema()
    repository.acquire_workspace_lease(
        owner_token="holder-token",
        command="holder",
        lease_timeout_seconds=600,
        run_id="holder-run",
    )

    result = runner.invoke(recoleta.cli.app, argv)

    assert result.exit_code == 1
    assert "workspace is locked" in result.stdout
    lease = repository.get_workspace_lease()
    assert lease is not None
    assert lease.command == "holder"
