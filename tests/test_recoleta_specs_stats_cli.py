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


def _seed_freshness_regression_scenario(
    *,
    repository: Repository,
    backup_root: Path,
) -> None:
    latest_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="freshness-item-latest",
            canonical_url="https://example.com/freshness-item-latest",
            title="Freshness Latest Item",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 4, 12, 12, tzinfo=UTC),
        )
    )
    published_item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="freshness-item-published",
            canonical_url="https://example.com/freshness-item-published",
            title="Freshness Published Item",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 4, 11, 12, tzinfo=UTC),
        )
    )
    assert latest_item.id is not None
    assert published_item.id is not None

    day_run = repository.create_run("fp-freshness-day", run_id="run-freshness-day")
    repository.update_run_context(
        run_id=day_run.id,
        command="run day --date 2026-04-06",
        operation_kind="workflow.run.day",
        scope="default",
        granularity="day",
        period_start=datetime(2026, 4, 6, tzinfo=UTC),
        period_end=datetime(2026, 4, 7, tzinfo=UTC),
    )
    repository.finish_run(day_run.id, success=True)

    week_run = repository.create_run("fp-freshness-week", run_id="run-freshness-week")
    repository.update_run_context(
        run_id=week_run.id,
        command="run week --date 2026-03-30",
        operation_kind="workflow.run.week",
        scope="default",
        granularity="week",
        period_start=datetime(2026, 3, 30, tzinfo=UTC),
        period_end=datetime(2026, 4, 6, tzinfo=UTC),
    )
    repository.finish_run(week_run.id, success=True)

    source_run = repository.create_run(
        "fp-freshness-source",
        run_id="run-freshness-source",
    )
    repository.record_metric(
        run_id=source_run.id,
        name="pipeline.ingest.source.rss.drafts_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=source_run.id,
        name="pipeline.ingest.source.rss.newest_published_at_unix",
        value=datetime(2026, 4, 12, 23, 55, tzinfo=UTC).timestamp(),
        unit="unix",
    )
    repository.finish_run(source_run.id, success=True)

    derived_run = repository.create_run(
        "fp-freshness-derived",
        run_id="run-freshness-derived",
    )
    for pass_kind in ("trend_synthesis", "trend_ideas"):
        for granularity in ("day", "week"):
            repository.create_pass_output(
                run_id=derived_run.id,
                pass_kind=pass_kind,
                status="succeeded",
                granularity=granularity,
                period_start=datetime(2026, 4, 6, tzinfo=UTC),
                period_end=datetime(2026, 4, 13, tzinfo=UTC),
                payload={"title": f"{pass_kind}-{granularity}"},
                diagnostics={},
                input_refs=[],
            )
    repository.finish_run(derived_run.id, success=True)

    with Session(repository.engine) as session:
        latest_item_row = session.get(type(latest_item), int(latest_item.id))
        published_item_row = session.get(type(published_item), int(published_item.id))
        assert latest_item_row is not None
        assert published_item_row is not None
        latest_item_row.state = ITEM_STATE_ANALYZED
        published_item_row.state = ITEM_STATE_PUBLISHED

        day_run_row = session.get(Run, day_run.id)
        week_run_row = session.get(Run, week_run.id)
        source_run_row = session.get(Run, source_run.id)
        derived_run_row = session.get(Run, derived_run.id)
        assert day_run_row is not None
        assert week_run_row is not None
        assert source_run_row is not None
        assert derived_run_row is not None

        day_run_row.started_at = datetime(2026, 4, 11, 4, 30, tzinfo=UTC)
        day_run_row.heartbeat_at = datetime(2026, 4, 11, 4, 35, tzinfo=UTC)
        day_run_row.finished_at = datetime(2026, 4, 11, 4, 42, tzinfo=UTC)

        week_run_row.started_at = datetime(2026, 4, 16, 10, 0, tzinfo=UTC)
        week_run_row.heartbeat_at = datetime(2026, 4, 16, 10, 15, tzinfo=UTC)
        week_run_row.finished_at = datetime(2026, 4, 16, 10, 22, tzinfo=UTC)

        source_run_row.started_at = datetime(2026, 4, 17, 10, 30, tzinfo=UTC)
        source_run_row.heartbeat_at = datetime(2026, 4, 17, 10, 31, tzinfo=UTC)
        source_run_row.finished_at = datetime(2026, 4, 17, 10, 32, tzinfo=UTC)

        derived_run_row.started_at = datetime(2026, 4, 17, 11, 0, tzinfo=UTC)
        derived_run_row.heartbeat_at = datetime(2026, 4, 17, 11, 10, tzinfo=UTC)
        derived_run_row.finished_at = datetime(2026, 4, 17, 11, 13, tzinfo=UTC)
        session.commit()

    bundle_dir = backup_root / "recoleta-backup-20260407T012620Z"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / "manifest.json").write_text(
        json.dumps(
            {
                "kind": "recoleta-db-backup",
                "created_at": "2026-04-07T01:26:20.361189+00:00",
                "schema_version": 8,
                "database_filename": "recoleta.db",
                "source_db_filename": "recoleta.db",
                "database_size_bytes": 1024,
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


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


def test_stats_json_fails_when_db_uses_older_schema(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "older.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    with repository.engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA user_version = 0")

    result = runner.invoke(
        recoleta.cli.app,
        ["stats", "--db-path", str(db_path), "--json"],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert "older schema version" in payload["error"]


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


def test_stats_json_reports_latest_source_diagnostics(
    configured_env: Path,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-source-diag", run_id="run-source-diag")
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.drafts_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.pull_failed_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.hn.drafts_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.hn.pull_failed_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.processed_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.skipped_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.failed_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.content_chars_sum",
        value=1234,
        unit="chars",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.content_type.html_maintext_total",
        value=1,
        unit="count",
    )
    repository.finish_run(run.id, success=False)

    result = runner.invoke(recoleta.cli.app, ["stats", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    diagnostics = payload["source_diagnostics"]
    assert diagnostics["run_id"] == "run-source-diag"
    assert diagnostics["run_status"] == "failed"
    assert diagnostics["sources"]["rss"]["status"] == "ok"
    assert diagnostics["sources"]["rss"]["pipeline_completed"] is True
    assert diagnostics["sources"]["rss"]["ingest"]["drafts_total"] == 1
    assert diagnostics["sources"]["rss"]["enrich"]["processed_total"] == 1
    assert diagnostics["sources"]["rss"]["enrich"]["content_types"] == {
        "html_maintext": 1
    }
    assert diagnostics["sources"]["hn"]["status"] == "pull_failed"
    assert diagnostics["sources"]["hn"]["pipeline_completed"] is False
    assert diagnostics["sources"]["hn"]["ingest"]["pull_failed_total"] == 1


def test_stats_json_reports_pull_failed_when_backlog_enrich_succeeds(
    configured_env: Path,
) -> None:
    """Regression: backlog enrich must not hide an active source pull failure."""
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-source-diag", run_id="run-source-diag-backlog")
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.drafts_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.pull_failed_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.processed_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.skipped_total",
        value=0,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.enrich.source.rss.failed_total",
        value=0,
        unit="count",
    )
    repository.finish_run(run.id, success=False)

    result = runner.invoke(recoleta.cli.app, ["stats", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    diagnostics = payload["source_diagnostics"]
    assert diagnostics["run_id"] == "run-source-diag-backlog"
    assert diagnostics["sources"]["rss"]["status"] == "pull_failed"
    assert diagnostics["sources"]["rss"]["pipeline_completed"] is False


def test_stats_json_reports_extended_ingest_source_diagnostics(
    configured_env: Path,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-source-diag", run_id="run-source-diag-extended")
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.filtered_out_total",
        value=2,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.deduped_total",
        value=3,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.deferred_total",
        value=4,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.not_modified_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.oldest_published_at_unix",
        value=datetime(2025, 1, 20, 10, tzinfo=UTC).timestamp(),
        unit="unix",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.ingest.source.rss.newest_published_at_unix",
        value=datetime(2025, 1, 21, 11, tzinfo=UTC).timestamp(),
        unit="unix",
    )
    repository.finish_run(run.id, success=True)

    result = runner.invoke(recoleta.cli.app, ["stats", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    ingest_payload = payload["source_diagnostics"]["sources"]["rss"]["ingest"]
    assert ingest_payload["filtered_out_total"] == 2
    assert ingest_payload["deduped_total"] == 3
    assert ingest_payload["deferred_total"] == 4
    assert ingest_payload["not_modified_total"] == 1
    assert ingest_payload["oldest_published_at"] == "2025-01-20T10:00:00+00:00"
    assert ingest_payload["newest_published_at"] == "2025-01-21T11:00:00+00:00"


def test_inspect_freshness_json_reports_split_freshness_axes(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    backup_root = configured_env / "configured-backups"
    monkeypatch.setenv("BACKUP_OUTPUT_DIR", str(backup_root))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_freshness_regression_scenario(repository=repository, backup_root=backup_root)

    result = runner.invoke(recoleta.cli.app, ["inspect", "freshness", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["freshness"]["run"]["latest_successful_by_granularity"]["day"] == {
        "finished_at": "2026-04-11T04:42:00+00:00",
        "period_end": "2026-04-07T00:00:00+00:00",
        "period_start": "2026-04-06T00:00:00+00:00",
        "run_id": "run-freshness-day",
    }
    assert payload["freshness"]["run"]["latest_successful_by_granularity"]["week"] == {
        "finished_at": "2026-04-16T10:22:00+00:00",
        "period_end": "2026-04-06T00:00:00+00:00",
        "period_start": "2026-03-30T00:00:00+00:00",
        "run_id": "run-freshness-week",
    }
    assert (
        payload["freshness"]["data"]["latest_item_published_at"]
        == "2026-04-12T12:00:00+00:00"
    )
    assert (
        payload["freshness"]["data"]["latest_published_item_at"]
        == "2026-04-11T12:00:00+00:00"
    )
    assert (
        payload["freshness"]["data"]["source_observation"]["sources"]["rss"]["ingest"][
            "newest_published_at"
        ]
        == "2026-04-12T23:55:00+00:00"
    )
    assert (
        payload["freshness"]["derived_windows"]["trends"]["day"]["latest_period_end"]
        == "2026-04-13T00:00:00+00:00"
    )
    assert (
        payload["freshness"]["derived_windows"]["ideas"]["week"]["latest_period_end"]
        == "2026-04-13T00:00:00+00:00"
    )
    assert payload["freshness"]["backup"]["scope"] == "db_only"
    assert payload["freshness"]["backup"]["root_dir"] == str(backup_root.resolve())
    assert (
        payload["freshness"]["backup"]["latest_created_at"]
        == "2026-04-07T01:26:20.361189+00:00"
    )
    mismatch_codes = {
        mismatch["code"] for mismatch in payload["freshness"]["mismatches"]
    }
    assert mismatch_codes == {
        "backup_behind_data",
        "workflow_day_behind_derived_day",
        "workflow_week_behind_derived_week",
    }


def test_inspect_freshness_uses_env_backup_output_dir_when_settings_are_skipped(
    tmp_path: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "env-backups"
    monkeypatch.setenv("BACKUP_OUTPUT_DIR", str(backup_root))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_freshness_regression_scenario(repository=repository, backup_root=backup_root)

    result = runner.invoke(
        recoleta.cli.app,
        ["inspect", "freshness", "--db-path", str(db_path), "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["freshness"]["backup"]["root_dir"] == str(backup_root.resolve())
    assert (
        payload["freshness"]["backup"]["latest_created_at"]
        == "2026-04-07T01:26:20.361189+00:00"
    )


def test_inspect_freshness_uses_config_backup_output_dir_when_settings_load_fails(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "config-backups"
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{db_path}"',
                f'BACKUP_OUTPUT_DIR: "{backup_root}"',
            ]
        ),
        encoding="utf-8",
    )

    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_freshness_regression_scenario(repository=repository, backup_root=backup_root)

    result = runner.invoke(
        recoleta.cli.app,
        ["inspect", "freshness", "--config", str(config_path), "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["settings"] == "failed"
    assert payload["freshness"]["backup"]["root_dir"] == str(backup_root.resolve())
    assert (
        payload["freshness"]["backup"]["latest_created_at"]
        == "2026-04-07T01:26:20.361189+00:00"
    )


def test_stats_json_includes_freshness_snapshot(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    backup_root = configured_env / "configured-backups"
    monkeypatch.setenv("BACKUP_OUTPUT_DIR", str(backup_root))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_freshness_regression_scenario(repository=repository, backup_root=backup_root)

    result = runner.invoke(recoleta.cli.app, ["stats", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["latest_successful_run_id"] == "run-freshness-derived"
    assert payload["freshness"]["run"]["latest_successful_run_id"] == "run-freshness-derived"
    assert (
        payload["freshness"]["data"]["latest_item_published_at"]
        == "2026-04-12T12:00:00+00:00"
    )
    assert (
        payload["freshness"]["backup"]["latest_created_at"]
        == "2026-04-07T01:26:20.361189+00:00"
    )


def test_stats_text_distinguishes_run_data_derived_and_backup_freshness(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    backup_root = configured_env / "configured-backups"
    monkeypatch.setenv("BACKUP_OUTPUT_DIR", str(backup_root))

    repository = Repository(db_path=db_path)
    repository.init_schema()
    _seed_freshness_regression_scenario(repository=repository, backup_root=backup_root)

    result = runner.invoke(recoleta.cli.app, ["stats"])

    assert result.exit_code == 0
    assert "run_freshness=" in result.stdout
    assert "data_freshness=" in result.stdout
    assert "derived_day_window=" in result.stdout
    assert "derived_week_window=" in result.stdout
    assert "backup_recovery_point=" in result.stdout
