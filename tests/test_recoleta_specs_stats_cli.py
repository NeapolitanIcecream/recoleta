from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
import io
from pathlib import Path
from typing import cast

from loguru import logger as loguru_logger
from sqlmodel import Session
from typer.testing import CliRunner

import recoleta.cli
from recoleta.models import (
    ITEM_STATE_ANALYZED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    RUN_STATUS_FAILED,
    Run,
)
from recoleta.storage import Repository
from recoleta.types import ItemDraft


def test_stats_json_reports_backlog_stale_runs_and_lease(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    drafts = [
        ItemDraft.from_values(
            source="rss",
            source_item_id=f"stats-item-{index}",
            canonical_url=f"https://example.com/stats-item-{index}",
            title=f"Stats Item {index}",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, index + 1, tzinfo=UTC),
        )
        for index in range(4)
    ]
    items = [repository.upsert_item(draft)[0] for draft in drafts]
    item_ids = [item.id for item in items]
    assert all(item_id is not None for item_id in item_ids)
    resolved_item_ids = [cast(int, item_id) for item_id in item_ids]

    success_run = repository.create_run("fp-success", run_id="run-ok")
    stale_run = repository.create_run("fp-stale", run_id="run-stale")
    repository.create_run("fp-fresh", run_id="run-fresh")
    failed_run = repository.create_run("fp-failed", run_id="run-failed")
    repository.finish_run(success_run.id, success=True)
    repository.finish_run(failed_run.id, success=False)
    repository.acquire_workspace_lease(
        owner_token="holder-token",
        command="run",
        lease_timeout_seconds=600,
        run_id="run-fresh",
        pid=123,
    )

    reference_now = datetime.now(UTC)
    stale_ts = reference_now - timedelta(seconds=180)
    old_item_ts = reference_now - timedelta(days=2)
    with Session(repository.engine) as session:
        item_rows = {
            item_id: session.get(type(item), item_id)
            for item, item_id in zip(items, resolved_item_ids, strict=True)
        }
        assert all(row is not None for row in item_rows.values())
        item_rows[resolved_item_ids[0]].state = ITEM_STATE_INGESTED  # type: ignore[index,union-attr]
        item_rows[resolved_item_ids[0]].created_at = old_item_ts  # type: ignore[index,union-attr]
        item_rows[resolved_item_ids[1]].state = ITEM_STATE_ANALYZED  # type: ignore[index,union-attr]
        item_rows[resolved_item_ids[2]].state = ITEM_STATE_PUBLISHED  # type: ignore[index,union-attr]
        item_rows[resolved_item_ids[3]].state = ITEM_STATE_RETRYABLE_FAILED  # type: ignore[index,union-attr]

        stale_run_row = session.get(Run, stale_run.id)
        assert stale_run_row is not None
        stale_run_row.started_at = stale_ts
        stale_run_row.heartbeat_at = stale_ts

        success_row = session.get(Run, success_run.id)
        assert success_row is not None
        success_row.started_at = stale_ts
        success_row.heartbeat_at = stale_ts
        success_row.finished_at = reference_now - timedelta(seconds=30)

        failed_row = session.get(Run, failed_run.id)
        assert failed_row is not None
        failed_row.status = RUN_STATUS_FAILED
        failed_row.started_at = stale_ts
        failed_row.heartbeat_at = stale_ts
        failed_row.finished_at = stale_ts
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        ["stats", "--db-path", str(db_path), "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["items_total"] == 4
    assert payload["items_by_state"]["ingested"] == 1
    assert payload["items_by_state"]["analyzed"] == 1
    assert payload["items_by_state"]["published"] == 1
    assert payload["items_by_state"]["retryable_failed"] == 1
    assert payload["unfinished_total"] == 3
    assert payload["oldest_unfinished_age_seconds"] >= 2 * 24 * 60 * 60
    assert payload["runs_by_status"]["running"] == 2
    assert payload["runs_by_status"]["succeeded"] == 1
    assert payload["runs_by_status"]["failed"] == 1
    assert payload["stale_running_runs"] == 1
    assert payload["latest_successful_run_id"] == "run-ok"
    assert payload["latest_successful_run_at"] is not None
    assert payload["latest_successful_run_age_seconds"] >= 30
    assert payload["lease"]["state"] == "held"
    assert payload["lease"]["holder_command"] == "run"
    assert payload["lease"]["holder_run_id"] == "run-fresh"
    assert payload["lease"]["holder_pid"] == 123
    assert payload["db_bytes"] > 0


def test_stats_json_failure_emits_log_for_missing_db(tmp_path: Path) -> None:
    runner = CliRunner()
    missing_db_path = tmp_path / "missing.db"
    stream = io.StringIO()
    sink_id = loguru_logger.add(stream, level="WARNING", serialize=True)

    try:
        result = runner.invoke(
            recoleta.cli.app,
            ["stats", "--db-path", str(missing_db_path), "--json"],
        )
    finally:
        loguru_logger.remove(sink_id)

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert "db does not exist" in payload["error"]
    assert "cli.stats" in stream.getvalue()
    assert str(missing_db_path) in stream.getvalue()


def test_stats_json_reports_workspace_directory_sizes_when_settings_are_available(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    markdown_output_dir = configured_env / "outputs"
    artifacts_dir = configured_env / "artifacts"
    lancedb_dir = configured_env / "lancedb"

    markdown_output_dir.mkdir()
    artifacts_dir.mkdir()
    lancedb_dir.mkdir()
    (markdown_output_dir / "latest.md").write_text("hello", encoding="utf-8")
    (artifacts_dir / "debug.json").write_text("abc", encoding="utf-8")
    (lancedb_dir / "index.bin").write_bytes(b"1234567")

    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(lancedb_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["markdown"]))

    repository = Repository(db_path=db_path)
    repository.init_schema()

    result = runner.invoke(recoleta.cli.app, ["stats", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["settings"] == "ok"
    assert payload["workspace_bytes"]["markdown_output_dir"] == 5
    assert payload["workspace_bytes"]["artifacts_dir"] == 3
    assert payload["workspace_bytes"]["rag_lancedb_dir"] == 7
