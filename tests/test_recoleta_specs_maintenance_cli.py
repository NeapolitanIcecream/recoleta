from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast

import lancedb
import pytest
from sqlmodel import Session, select
from typer.testing import CliRunner

import recoleta.cli
from recoleta.config import Settings
from recoleta.models import (
    Artifact,
    ChunkEmbedding,
    DocumentChunk,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_RETRYABLE_FAILED,
    Item,
    ItemStreamState,
    Metric,
    Run,
)
from recoleta.rag.vector_store import embedding_table_name
from recoleta.storage import CURRENT_SCHEMA_VERSION, Repository
from recoleta.types import ItemDraft


def _seed_item_document_chunk(*, repository: Repository) -> tuple[int, int]:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="maintenance-item-1",
        canonical_url="https://example.com/maintenance-item-1",
        title="Maintenance Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime.now(UTC),
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    doc = repository.upsert_document_for_item(item=item)
    assert doc.id is not None
    chunk, _ = repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="chunk summary",
        start_char=0,
        end_char=None,
        source_content_type="analysis_summary",
    )
    assert chunk.id is not None
    repository.upsert_chunk_embedding(
        chunk_id=int(chunk.id),
        model="text-embedding-3-small",
        dimensions=3,
        text_hash=chunk.text_hash,
        vector=[0.1, 0.2, 0.3],
    )
    return int(doc.id), int(chunk.id)


def test_gc_prunes_expired_debug_artifacts_and_operational_history(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    artifacts_dir = tmp_path / "artifacts"
    artifacts_dir.mkdir()
    repository = Repository(db_path=db_path)
    repository.init_schema()

    old_artifact_path = artifacts_dir / "old.json"
    old_artifact_path.write_text("old", encoding="utf-8")
    recent_artifact_path = artifacts_dir / "recent.json"
    recent_artifact_path.write_text("recent", encoding="utf-8")

    old_run = repository.create_run("fp-old", run_id="run-old")
    recent_run = repository.create_run("fp-recent", run_id="run-recent")
    running_run = repository.create_run("fp-running", run_id="run-running")
    repository.finish_run(old_run.id, success=True)
    repository.finish_run(recent_run.id, success=True)
    repository.record_metric(run_id=old_run.id, name="metric.old", value=1.0)
    repository.record_metric(run_id=recent_run.id, name="metric.recent", value=2.0)
    repository.add_artifact(
        run_id=old_run.id,
        item_id=None,
        kind="debug",
        path=str(old_artifact_path),
    )
    repository.add_artifact(
        run_id=recent_run.id,
        item_id=None,
        kind="debug",
        path=str(recent_artifact_path),
    )

    now = datetime.now(UTC)
    old_ts = now - timedelta(days=75)
    recent_ts = now - timedelta(days=3)
    with Session(repository.engine) as session:
        old_run_row = session.get(Run, old_run.id)
        assert old_run_row is not None
        old_run_row.started_at = old_ts
        old_run_row.heartbeat_at = old_ts
        old_run_row.finished_at = old_ts

        recent_run_row = session.get(Run, recent_run.id)
        assert recent_run_row is not None
        recent_run_row.started_at = recent_ts
        recent_run_row.heartbeat_at = recent_ts
        recent_run_row.finished_at = recent_ts

        running_run_row = session.get(Run, running_run.id)
        assert running_run_row is not None
        running_run_row.started_at = recent_ts
        running_run_row.heartbeat_at = recent_ts
        running_run_row.finished_at = None

        metrics = list(session.exec(select(Metric).order_by(cast(Any, Metric.id))))
        assert len(metrics) == 2
        metrics[0].created_at = old_ts
        metrics[1].created_at = recent_ts

        artifacts = list(
            session.exec(select(Artifact).order_by(cast(Any, Artifact.id)))
        )
        assert len(artifacts) == 2
        artifacts[0].created_at = now - timedelta(days=20)
        artifacts[1].created_at = recent_ts
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        ["gc", "--db-path", str(db_path)],
    )

    assert result.exit_code == 0
    assert "deleted_artifacts=1" in result.stdout
    assert "deleted_runs=1" in result.stdout
    assert not old_artifact_path.exists()
    assert recent_artifact_path.exists()

    with Session(repository.engine) as session:
        remaining_runs = {row.id for row in session.exec(select(Run))}
        remaining_metrics = list(session.exec(select(Metric)))
        remaining_artifacts = list(session.exec(select(Artifact)))
    assert remaining_runs == {"run-recent", "run-running"}
    assert len(remaining_metrics) == 1
    assert remaining_metrics[0].run_id == "run-recent"
    assert len(remaining_artifacts) == 1
    assert remaining_artifacts[0].path == str(recent_artifact_path)


def test_gc_prune_caches_clears_rebuildable_cache_material(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    markdown_output_dir = tmp_path / "outputs"
    trends_dir = markdown_output_dir / "Trends"
    trends_dir.mkdir(parents=True)
    lancedb_dir = tmp_path / "lancedb"

    monkeypatch.setenv("RECOLETA_DB_PATH", str(db_path))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("SOURCES", json.dumps({}))
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_output_dir))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(lancedb_dir))

    settings = Settings()  # pyright: ignore[reportCallIssue]
    repository = Repository(db_path=db_path)
    repository.init_schema()
    doc_id, chunk_id = _seed_item_document_chunk(repository=repository)

    trend_markdown_path = trends_dir / "2026-03-01--trend.md"
    trend_markdown_path.write_text("# Trend\n", encoding="utf-8")
    trend_pdf_path = trend_markdown_path.with_suffix(".pdf")
    trend_pdf_path.write_bytes(b"%PDF-1.4\n")
    pdf_debug_dir = trends_dir / ".pdf-debug" / "2026-03-01--trend"
    pdf_debug_dir.mkdir(parents=True)
    (pdf_debug_dir / "debug.txt").write_text("debug", encoding="utf-8")
    site_output_dir = markdown_output_dir / "site"
    site_output_dir.mkdir()
    (site_output_dir / "index.html").write_text("<html></html>", encoding="utf-8")

    active_table = embedding_table_name(
        embedding_model=settings.trends_embedding_model,
        embedding_dimensions=settings.trends_embedding_dimensions,
    )
    db = lancedb.connect(str(lancedb_dir))
    row = {
        "chunk_id": 1,
        "doc_id": doc_id,
        "doc_type": "item",
        "chunk_index": 0,
        "kind": "summary",
        "text_hash": "abc",
        "text_preview": "preview",
        "event_start_ts": 1.0,
        "event_end_ts": 2.0,
        "vector": [0.1, 0.2, 0.3],
    }
    db.create_table(active_table, [row], exist_ok=True)
    inactive_table = "chunk_vectors_olddeadbeef"
    db.create_table(inactive_table, [row], exist_ok=True)

    result = runner.invoke(recoleta.cli.app, ["gc", "--prune-caches"])

    assert result.exit_code == 0
    assert "deleted_document_chunks=1" in result.stdout
    assert "deleted_lancedb_tables=1" in result.stdout
    assert "deleted_trend_pdfs=1" in result.stdout
    assert "deleted_pdf_debug_dirs=1" in result.stdout
    assert "deleted_site_outputs=1" in result.stdout
    assert not trend_pdf_path.exists()
    assert not pdf_debug_dir.exists()
    assert not site_output_dir.exists()

    with Session(repository.engine) as session:
        assert session.get(Item, 1) is not None
        assert session.exec(select(DocumentChunk)).all() == []
        assert session.exec(select(ChunkEmbedding)).all() == []
    assert repository.read_document_chunk(doc_id=doc_id, chunk_index=0) is None
    table_names = set(db.list_tables(limit=20).tables or [])
    assert active_table in table_names
    assert inactive_table not in table_names
    assert repository.get_document(doc_id=doc_id) is not None
    assert chunk_id > 0


def test_backup_and_restore_roundtrip(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "backups"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="backup-item-1",
        canonical_url="https://example.com/backup-item-1",
        title="Backup Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime(2026, 3, 1, tzinfo=UTC),
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None

    backup_result = runner.invoke(
        recoleta.cli.app,
        ["backup", "--db-path", str(db_path), "--output-dir", str(backup_root)],
    )
    assert backup_result.exit_code == 0
    bundle_dirs = [path for path in backup_root.iterdir() if path.is_dir()]
    assert len(bundle_dirs) == 1
    bundle_dir = bundle_dirs[0]
    manifest_path = bundle_dir / "manifest.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert int(manifest["schema_version"]) == CURRENT_SCHEMA_VERSION

    with Session(repository.engine) as session:
        for row in session.exec(select(Item)):
            session.delete(row)
        session.commit()

    restore_result = runner.invoke(
        recoleta.cli.app,
        [
            "restore",
            "--db-path",
            str(db_path),
            "--bundle",
            str(bundle_dir),
            "--yes",
        ],
    )
    assert restore_result.exit_code == 0

    restored_repository = Repository(db_path=db_path)
    restored_repository.init_schema()
    with Session(restored_repository.engine) as session:
        restored_items = list(session.exec(select(Item)))
    assert len(restored_items) == 1
    assert restored_items[0].canonical_url == "https://example.com/backup-item-1"


def test_restore_exits_when_workspace_lock_is_held(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "backups"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="restore-lock-item-1",
        canonical_url="https://example.com/restore-lock-item-1",
        title="Restore Lock Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime(2026, 3, 1, tzinfo=UTC),
    )
    repository.upsert_item(draft)

    backup_result = runner.invoke(
        recoleta.cli.app,
        ["backup", "--db-path", str(db_path), "--output-dir", str(backup_root)],
    )
    assert backup_result.exit_code == 0
    bundle_dir = next(path for path in backup_root.iterdir() if path.is_dir())

    repository.acquire_workspace_lease(
        owner_token="holder-token",
        command="holder",
        lease_timeout_seconds=600,
        run_id="holder-run",
    )

    restore_result = runner.invoke(
        recoleta.cli.app,
        [
            "restore",
            "--db-path",
            str(db_path),
            "--bundle",
            str(bundle_dir),
            "--yes",
        ],
    )

    assert restore_result.exit_code == 1
    assert "workspace is locked" in restore_result.stdout


def test_restore_rejects_bundle_with_newer_schema_version(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "backups"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="restore-newer-schema-item-1",
        canonical_url="https://example.com/restore-newer-schema-item-1",
        title="Restore Newer Schema Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime(2026, 3, 1, tzinfo=UTC),
    )
    repository.upsert_item(draft)

    backup_result = runner.invoke(
        recoleta.cli.app,
        ["backup", "--db-path", str(db_path), "--output-dir", str(backup_root)],
    )
    assert backup_result.exit_code == 0
    bundle_dir = next(path for path in backup_root.iterdir() if path.is_dir())
    manifest_path = bundle_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["schema_version"] = CURRENT_SCHEMA_VERSION + 1
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    restore_result = runner.invoke(
        recoleta.cli.app,
        [
            "restore",
            "--db-path",
            str(db_path),
            "--bundle",
            str(bundle_dir),
            "--yes",
        ],
    )

    assert restore_result.exit_code == 1
    assert "newer schema version" in restore_result.stdout


def test_restore_rejects_bundle_when_database_file_uses_newer_schema(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    backup_root = tmp_path / "backups"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="restore-db-schema-item-1",
        canonical_url="https://example.com/restore-db-schema-item-1",
        title="Restore DB Schema Item",
        authors=["Alice"],
        raw_metadata={"source": "test"},
        published_at=datetime(2026, 3, 1, tzinfo=UTC),
    )
    repository.upsert_item(draft)

    backup_result = runner.invoke(
        recoleta.cli.app,
        ["backup", "--db-path", str(db_path), "--output-dir", str(backup_root)],
    )
    assert backup_result.exit_code == 0
    bundle_dir = next(path for path in backup_root.iterdir() if path.is_dir())
    manifest_path = bundle_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    bundle_db_path = bundle_dir / str(manifest["database_filename"])

    with sqlite3.connect(bundle_db_path) as conn:
        conn.execute(f"PRAGMA user_version = {CURRENT_SCHEMA_VERSION + 1}")
        conn.commit()

    restore_result = runner.invoke(
        recoleta.cli.app,
        [
            "restore",
            "--db-path",
            str(db_path),
            "--bundle",
            str(bundle_dir),
            "--yes",
        ],
    )

    assert restore_result.exit_code == 1
    assert "newer schema version" in restore_result.stdout


def test_vacuum_exits_when_workspace_lock_is_held(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    repository.acquire_workspace_lease(
        owner_token="holder-token",
        command="holder",
        lease_timeout_seconds=600,
        run_id="holder-run",
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["vacuum", "--db-path", str(db_path)],
    )

    assert result.exit_code == 1
    assert "workspace is locked" in result.stdout


def test_gc_prune_caches_with_db_path_only_skips_filesystem_cache_pruning(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    doc_id, _ = _seed_item_document_chunk(repository=repository)

    result = runner.invoke(
        recoleta.cli.app,
        ["gc", "--db-path", str(db_path), "--prune-caches"],
    )

    assert result.exit_code == 0
    assert "deleted_document_chunks=1" in result.stdout
    assert "filesystem_cache_pruning=skipped" in result.stdout
    assert repository.read_document_chunk(doc_id=doc_id, chunk_index=0) is None


def test_repair_streams_requeues_existing_and_missing_stream_rows(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    first, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="repair-stream-1",
            canonical_url="https://example.com/repair-stream-1",
            title="Repair Stream Existing State",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 15, 10, tzinfo=UTC),
        )
    )
    second, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="repair-stream-2",
            canonical_url="https://example.com/repair-stream-2",
            title="Repair Stream Missing State",
            authors=["Bob"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 15, 11, tzinfo=UTC),
        )
    )
    assert first.id is not None
    assert second.id is not None
    repository.mark_item_enriched(item_id=int(first.id))
    repository.mark_item_enriched(item_id=int(second.id))
    repository.mark_item_stream_state(
        item_id=int(first.id),
        stream="agents_lab",
        state=ITEM_STATE_ANALYZED,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "streams",
            "--db-path",
            str(db_path),
            "--date",
            "2026-03-15",
            "--streams",
            "agents_lab",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["candidate_total"] == 2
    assert payload["updated_total"] == 1
    assert payload["inserted_total"] == 1
    assert payload["streams"] == ["agents_lab"]

    with Session(repository.engine) as session:
        rows = list(
            session.exec(
                select(ItemStreamState).where(ItemStreamState.stream == "agents_lab")
            )
        )

    assert len(rows) == 2
    assert {int(row.item_id): row.state for row in rows} == {
        int(first.id): ITEM_STATE_RETRYABLE_FAILED,
        int(second.id): ITEM_STATE_RETRYABLE_FAILED,
    }


def test_doctor_why_empty_reports_stream_blockers_as_json(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="doctor-why-empty-1",
            canonical_url="https://example.com/doctor-why-empty-1",
            title="Doctor Why Empty",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 15, 12, tzinfo=UTC),
        )
    )
    assert item.id is not None
    repository.mark_item_enriched(item_id=int(item.id))
    repository.mark_item_stream_state(
        item_id=int(item.id),
        stream="agents_lab",
        state=ITEM_STATE_RETRYABLE_FAILED,
    )
    with Session(repository.engine) as session:
        row = session.get(Item, int(item.id))
        assert row is not None
        row.state = ITEM_STATE_ANALYZED
        session.add(row)
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "doctor",
            "why-empty",
            "--db-path",
            str(db_path),
            "--date",
            "2026-03-15",
            "--granularity",
            "day",
            "--stream",
            "agents_lab",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["scope"] == "agents_lab"
    assert payload["candidate_total"] == 1
    assert payload["selected_total"] == 0
    assert payload["filtered_out_total"] == 1
    assert payload["item_states"]["analyzed"] == 1
    assert payload["exclusion_reasons"]["missing_analysis"] == 1
    assert payload["exclusion_reasons"]["stream_state_retryable_failed"] == 1


def test_repair_streams_applies_startup_safe_migrations_before_repair(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="repair-stream-migration",
            canonical_url="https://example.com/repair-stream-migration",
            title="Repair Streams Migrates First",
            authors=["Alice"],
            raw_metadata={"source": "test"},
            published_at=datetime(2026, 3, 15, 12, tzinfo=UTC),
        )
    )
    assert item.id is not None
    repository.mark_item_enriched(item_id=int(item.id))

    with repository.engine.begin() as conn:
        conn.exec_driver_sql("PRAGMA user_version = 3")

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "streams",
            "--db-path",
            str(db_path),
            "--date",
            "2026-03-15",
            "--streams",
            "agents_lab",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["inserted_total"] == 1

    with sqlite3.connect(db_path) as conn:
        version = int(conn.execute("PRAGMA user_version").fetchone()[0])

    assert version == CURRENT_SCHEMA_VERSION
