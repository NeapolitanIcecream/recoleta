from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
import io
import sqlite3
from pathlib import Path
import time

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
from recoleta.types import AnalysisResult, ItemDraft


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
    assert "command" in run_columns
    assert "scope" in run_columns
    assert "granularity" in run_columns
    assert "period_start" in run_columns
    assert "period_end" in run_columns
    assert "workspace_leases" in lease_tables
    assert "pass_outputs" in lease_tables
    assert "item_stream_states" not in lease_tables


def test_init_schema_migrates_run_context_and_artifact_details_columns(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "legacy.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE runs (
                id TEXT PRIMARY KEY,
                started_at DATETIME NOT NULL,
                heartbeat_at DATETIME,
                finished_at DATETIME,
                status TEXT NOT NULL,
                config_fingerprint TEXT NOT NULL
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE artifacts (
                id INTEGER PRIMARY KEY,
                run_id TEXT NOT NULL,
                item_id INTEGER,
                kind TEXT NOT NULL,
                path TEXT NOT NULL,
                created_at DATETIME NOT NULL
            );
            """
        )
        conn.execute("PRAGMA user_version = 3")
        conn.commit()

    repository = Repository(db_path=db_path)
    repository.init_schema()

    with sqlite3.connect(db_path) as conn:
        run_columns = {
            str(row[1]) for row in conn.execute("PRAGMA table_info(runs)").fetchall()
        }
        artifact_columns = {
            str(row[1])
            for row in conn.execute("PRAGMA table_info(artifacts)").fetchall()
        }
        version = int(conn.execute("PRAGMA user_version").fetchone()[0])

    assert version == CURRENT_SCHEMA_VERSION
    assert {"command", "scope", "granularity", "period_start", "period_end"} <= run_columns
    assert "details_json" in artifact_columns


def test_init_schema_prunes_legacy_meta_rows_from_chunk_fts(tmp_path: Path) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    with sqlite3.connect(repository.db_path) as conn:
        conn.execute(
            "INSERT INTO documents(doc_type, granularity, period_start, period_end, title, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)",
            (
                "idea",
                "day",
                "2026-03-02T00:00:00+00:00",
                "2026-03-03T00:00:00+00:00",
                "Legacy idea",
            ),
        )
        doc_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        conn.execute(
            "INSERT INTO document_chunks(doc_id, chunk_index, kind, text, text_hash, source_content_type, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)",
            (
                doc_id,
                1,
                "meta",
                '{"_projection":{"pass_kind":"trend_synthesis"}}',
                "legacy-meta-hash",
                "trend_ideas_payload_json",
            ),
        )
        chunk_id = int(conn.execute("SELECT last_insert_rowid()").fetchone()[0])
        conn.execute(
            "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) VALUES (?, ?, ?, ?, ?)",
            (
                chunk_id,
                '{"_projection":{"pass_kind":"trend_synthesis"}}',
                doc_id,
                1,
                "meta",
            ),
        )
        conn.commit()

    repository.init_schema()

    with sqlite3.connect(repository.db_path) as conn:
        remaining = int(
            conn.execute("SELECT COUNT(*) FROM chunk_fts WHERE kind = 'meta'").fetchone()[0]
        )

    assert remaining == 0


def test_init_schema_rejects_legacy_shared_stream_child_tables(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "legacy-scope.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE analyses (
                id INTEGER PRIMARY KEY,
                item_id INTEGER NOT NULL,
                scope VARCHAR(64) NOT NULL DEFAULT 'default',
                model VARCHAR(128) NOT NULL,
                provider VARCHAR(64) NOT NULL,
                summary TEXT NOT NULL,
                topics_json TEXT NOT NULL DEFAULT '[]',
                relevance_score FLOAT NOT NULL DEFAULT 0.0,
                novelty_score FLOAT,
                cost_usd FLOAT,
                latency_ms INTEGER,
                created_at DATETIME NOT NULL
            );
            """
        )
        conn.execute("PRAGMA user_version = 7")
        conn.commit()

    repository = Repository(db_path=db_path)

    with pytest.raises(
        SchemaVersionError,
        match="Legacy shared-stream child tables are no longer supported",
    ):
        repository.init_schema()


def test_save_analysis_and_publish_work_with_current_schema(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="runtime-safety-item-2",
            canonical_url="https://example.com/runtime-safety-item-2",
            title="Runtime Safety Item 2",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 3, tzinfo=UTC),
        )
    )
    assert item.id is not None

    repository.save_analysis(
        item_id=item.id,
        result=AnalysisResult(
            model="test/runtime-safety",
            provider="test",
            summary="## Summary\n\nRuntime safety analysis.\n",
            topics=["systems"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    repository.mark_item_published(item_id=item.id)

    with sqlite3.connect(repository.db_path) as conn:
        current_tables = {
            str(row[0])
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

    assert "item_stream_states" not in current_tables


def test_list_items_for_publish_uses_current_item_state(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="runtime-safety-item-3",
            canonical_url="https://example.com/runtime-safety-item-3",
            title="Runtime Safety Item 3",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 4, tzinfo=UTC),
        )
    )
    assert item.id is not None

    repository.save_analysis(
        item_id=item.id,
        result=AnalysisResult(
            model="test/runtime-safety",
            provider="test",
            summary="## Summary\n\nPublish candidate.\n",
            topics=["systems"],
            relevance_score=0.95,
            novelty_score=0.5,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )

    candidates = repository.list_items_for_publish(
        limit=10,
        min_relevance_score=0.5,
    )

    assert len(candidates) == 1
    selected_item, selected_analysis = candidates[0]
    assert selected_item.id == item.id
    assert selected_analysis.item_id == item.id


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


def test_command_workspace_lease_monitor_renews_until_release(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    competing_repository = Repository(db_path=repository.db_path)
    competing_repository.init_schema()

    monkeypatch.setattr(recoleta.cli, "_WORKSPACE_LEASE_TIMEOUT_SECONDS", 2)
    monkeypatch.setattr(recoleta.cli, "_RUN_HEARTBEAT_INTERVAL_SECONDS", 1)

    owner_token, log, heartbeat_monitor = recoleta.cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=object(),
        command="gc",
        log_module="test.lease",
    )

    try:
        time.sleep(3.2)
        with pytest.raises(WorkspaceLeaseHeldError):
            competing_repository.acquire_workspace_lease(
                run_id="run-2",
                command="publish",
                owner_token="token-2",
                lease_timeout_seconds=2,
                hostname="host-b",
                pid=202,
            )
        heartbeat_monitor.raise_if_failed()
    finally:
        recoleta.cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )

    competing_repository.acquire_workspace_lease(
        run_id="run-2",
        command="publish",
        owner_token="token-2",
        lease_timeout_seconds=2,
        hostname="host-b",
        pid=202,
    )


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
        (["repair", "outputs"], "repair outputs"),
        (["site", "build"], "site build"),
        (["site", "stage"], "site stage"),
        (["site", "serve", "--port", "8765"], "site serve"),
        (["run", "deploy"], "run deploy"),
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
