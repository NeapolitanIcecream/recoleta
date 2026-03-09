from __future__ import annotations

from contextlib import contextmanager
import json
import sqlite3
import shutil
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import event, text
from sqlmodel import Session, SQLModel, create_engine, select

from recoleta.models import (
    Artifact,
    Metric,
    Run,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_FAILED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    RUN_STATUS_FAILED,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.storage.common import (
    CURRENT_SCHEMA_VERSION,
    WORKSPACE_LEASE_NAME,
    ArtifactPruneResult,
    ChunkCachePruneResult,
    DatabaseBackupResult,
    DatabaseRestoreResult,
    OperationalPruneResult,
    SchemaVersionError,
    SqlDiagnostics,
    WorkspaceLeaseError,
    WorkspaceLeaseHeldError,
    WorkspaceLeaseLostError,
    WorkspaceStatsResult,
    _from_json_list,
)
from recoleta.storage.documents import DocumentStoreMixin
from recoleta.storage.items import ItemStoreMixin
from recoleta.storage.runtime import RuntimeStoreMixin
from recoleta.types import DEFAULT_TOPIC_STREAM, utc_now

__all__ = [
    "CURRENT_SCHEMA_VERSION",
    "WORKSPACE_LEASE_NAME",
    "SchemaVersionError",
    "WorkspaceLeaseError",
    "WorkspaceLeaseHeldError",
    "WorkspaceLeaseLostError",
    "ArtifactPruneResult",
    "OperationalPruneResult",
    "ChunkCachePruneResult",
    "DatabaseBackupResult",
    "DatabaseRestoreResult",
    "WorkspaceStatsResult",
    "SqlDiagnostics",
    "Repository",
]


class Repository(RuntimeStoreMixin, ItemStoreMixin, DocumentStoreMixin):
    def __init__(
        self,
        *,
        db_path: Path,
        title_dedup_threshold: float = 92.0,
        title_dedup_max_candidates: int = 500,
    ) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            echo=False,
            connect_args={"check_same_thread": False, "timeout": 30},
        )
        self.title_dedup_threshold = float(title_dedup_threshold)
        self.title_dedup_max_candidates = max(0, int(title_dedup_max_candidates))
        self._sql_diag_lock = Lock()
        self._sql_diag_active: SqlDiagnostics | None = None
        self._sql_diag_installed = False

    def _ensure_sql_diagnostics_installed(self) -> None:
        if self._sql_diag_installed:
            return

        def _before_cursor_execute(*_: Any, **__: Any) -> None:
            active = self._sql_diag_active
            if active is None:
                return
            with self._sql_diag_lock:
                active.queries_total += 1

        event.listen(self.engine, "before_cursor_execute", _before_cursor_execute)
        self._sql_diag_installed = True

    @contextmanager
    def sql_diagnostics(self) -> Any:
        """Collect coarse SQL diagnostics for a single run (aggregate counts only)."""

        self._ensure_sql_diagnostics_installed()
        diag = SqlDiagnostics()
        with self._sql_diag_lock:
            previous = self._sql_diag_active
            self._sql_diag_active = diag
        try:
            yield diag
        finally:
            with self._sql_diag_lock:
                self._sql_diag_active = previous

    def _commit(self, session: Session) -> None:
        active = self._sql_diag_active
        if active is not None:
            with self._sql_diag_lock:
                active.commits_total += 1
        session.commit()

    def init_schema(self) -> None:
        user_version = self._get_user_version()
        if user_version > CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Database uses newer schema version "
                f"{user_version}; current supported version is {CURRENT_SCHEMA_VERSION}."
            )
        SQLModel.metadata.create_all(self.engine)
        if user_version < CURRENT_SCHEMA_VERSION:
            self._apply_startup_safe_migrations()
        SQLModel.metadata.create_all(self.engine)
        self._backfill_default_stream_states()
        self._ensure_chunk_fts()
        if user_version < CURRENT_SCHEMA_VERSION:
            self._set_user_version(CURRENT_SCHEMA_VERSION)

    def _apply_startup_safe_migrations(self) -> None:
        self._migrate_analyses_add_scope()
        self._migrate_documents_add_scope()
        self._migrate_runs_add_heartbeat()

    def _get_user_version(self) -> int:
        with self.engine.begin() as conn:
            row = conn.execute(text("PRAGMA user_version")).fetchone()
        if not row:
            return 0
        try:
            return int(row[0])
        except Exception:
            return 0

    def _set_user_version(self, version: int) -> None:
        normalized = max(0, int(version))
        with self.engine.begin() as conn:
            conn.execute(text(f"PRAGMA user_version = {normalized}"))

    def schema_version(self) -> int:
        return self._get_user_version()

    def ensure_schema_compatible(self) -> int:
        version = self.schema_version()
        if version > CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Database uses newer schema version "
                f"{version}; current supported version is {CURRENT_SCHEMA_VERSION}."
            )
        return version

    def ensure_schema_current(self) -> int:
        version = self.ensure_schema_compatible()
        if version < CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Database uses older schema version "
                f"{version}; current supported version is {CURRENT_SCHEMA_VERSION}. "
                "Run a write-capable command to apply startup-safe migrations first."
            )
        return version

    def has_table(self, table_name: str) -> bool:
        normalized_name = str(table_name or "").strip()
        if not normalized_name:
            return False
        statement = text(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table' AND name = :name
            LIMIT 1;
            """
        )
        with self.engine.begin() as conn:
            row = conn.execute(statement, {"name": normalized_name}).fetchone()
        return row is not None

    def _table_columns(self, table_name: str) -> set[str]:
        statement = text(f"PRAGMA table_info({table_name})")
        with self.engine.begin() as conn:
            rows = conn.execute(statement).fetchall()
        columns: set[str] = set()
        for row in rows:
            if len(row) >= 2:
                columns.add(str(row[1]))
        return columns

    def _migrate_analyses_add_scope(self) -> None:
        columns = self._table_columns("analyses")
        if not columns or "scope" in columns:
            return

        ddl = [
            """
            CREATE TABLE analyses__new (
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
                created_at DATETIME NOT NULL,
                FOREIGN KEY(item_id) REFERENCES items (id)
            );
            """,
            """
            INSERT INTO analyses__new (
                id,
                item_id,
                scope,
                model,
                provider,
                summary,
                topics_json,
                relevance_score,
                novelty_score,
                cost_usd,
                latency_ms,
                created_at
            )
            SELECT
                id,
                item_id,
                'default',
                model,
                provider,
                summary,
                topics_json,
                relevance_score,
                novelty_score,
                cost_usd,
                latency_ms,
                created_at
            FROM analyses;
            """,
            "DROP TABLE analyses;",
            "ALTER TABLE analyses__new RENAME TO analyses;",
            "CREATE INDEX IF NOT EXISTS ix_analyses_item_id ON analyses (item_id);",
            "CREATE INDEX IF NOT EXISTS ix_analyses_scope ON analyses (scope);",
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_analyses_item_scope ON analyses (item_id, scope);",
        ]
        with self.engine.begin() as conn:
            for statement in ddl:
                conn.execute(text(statement))

    def _migrate_documents_add_scope(self) -> None:
        columns = self._table_columns("documents")
        if not columns or "scope" in columns:
            return

        ddl = [
            """
            CREATE TABLE documents__new (
                id INTEGER PRIMARY KEY,
                doc_type VARCHAR(16) NOT NULL,
                scope VARCHAR(64) NOT NULL DEFAULT 'default',
                item_id INTEGER,
                source VARCHAR(32),
                canonical_url TEXT,
                title TEXT,
                published_at DATETIME,
                granularity VARCHAR(16),
                period_start DATETIME,
                period_end DATETIME,
                created_at DATETIME NOT NULL,
                updated_at DATETIME NOT NULL,
                FOREIGN KEY(item_id) REFERENCES items (id)
            );
            """,
            """
            INSERT INTO documents__new (
                id,
                doc_type,
                scope,
                item_id,
                source,
                canonical_url,
                title,
                published_at,
                granularity,
                period_start,
                period_end,
                created_at,
                updated_at
            )
            SELECT
                id,
                doc_type,
                'default',
                item_id,
                source,
                canonical_url,
                title,
                published_at,
                granularity,
                period_start,
                period_end,
                created_at,
                updated_at
            FROM documents;
            """,
            "DROP TABLE documents;",
            "ALTER TABLE documents__new RENAME TO documents;",
            "CREATE INDEX IF NOT EXISTS ix_documents_doc_type ON documents (doc_type);",
            "CREATE INDEX IF NOT EXISTS ix_documents_scope ON documents (scope);",
            "CREATE INDEX IF NOT EXISTS ix_documents_item_id ON documents (item_id);",
            "CREATE INDEX IF NOT EXISTS ix_documents_published_at ON documents (published_at);",
            "CREATE INDEX IF NOT EXISTS ix_documents_granularity ON documents (granularity);",
            "CREATE INDEX IF NOT EXISTS ix_documents_period_start ON documents (period_start);",
            "CREATE INDEX IF NOT EXISTS ix_documents_period_end ON documents (period_end);",
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_documents_doc_type_item_scope ON documents (doc_type, item_id, scope);",
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_documents_doc_type_scope_granularity_period ON documents (doc_type, scope, granularity, period_start, period_end);",
        ]
        with self.engine.begin() as conn:
            for statement in ddl:
                conn.execute(text(statement))

    def _migrate_runs_add_heartbeat(self) -> None:
        columns = self._table_columns("runs")
        if not columns or "heartbeat_at" in columns:
            return

        ddl = [
            "ALTER TABLE runs ADD COLUMN heartbeat_at DATETIME;",
            """
            UPDATE runs
            SET heartbeat_at = COALESCE(finished_at, started_at)
            WHERE heartbeat_at IS NULL;
            """,
            "CREATE INDEX IF NOT EXISTS ix_runs_heartbeat_at ON runs (heartbeat_at);",
        ]
        with self.engine.begin() as conn:
            for statement in ddl:
                conn.execute(text(statement))

    def _backfill_default_stream_states(self) -> None:
        statement = """
        INSERT INTO item_stream_states (
            item_id,
            stream,
            state,
            created_at,
            updated_at
        )
        SELECT
            items.id,
            :stream,
            items.state,
            items.created_at,
            items.updated_at
        FROM items
        WHERE items.state IN (
            :triaged_state,
            :analyzed_state,
            :published_state,
            :retryable_failed_state,
            :failed_state
        )
        AND NOT EXISTS (
            SELECT 1
            FROM item_stream_states stream_states
            WHERE stream_states.item_id = items.id
              AND stream_states.stream = :stream
        );
        """
        with self.engine.begin() as conn:
            conn.execute(
                text(statement),
                {
                    "stream": DEFAULT_TOPIC_STREAM,
                    "triaged_state": ITEM_STATE_TRIAGED,
                    "analyzed_state": ITEM_STATE_ANALYZED,
                    "published_state": ITEM_STATE_PUBLISHED,
                    "retryable_failed_state": ITEM_STATE_RETRYABLE_FAILED,
                    "failed_state": ITEM_STATE_FAILED,
                },
            )

    def _ensure_chunk_fts(self) -> None:
        # FTS5 is not created by SQLModel metadata.
        ddl = """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
            text,
            doc_id UNINDEXED,
            chunk_index UNINDEXED,
            kind UNINDEXED
        );
        """
        with self.engine.begin() as conn:
            conn.execute(text(ddl))

    def add_artifact(
        self, *, run_id: str, item_id: int | None, kind: str, path: str
    ) -> None:
        artifact = Artifact(run_id=run_id, item_id=item_id, kind=kind, path=path)
        with Session(self.engine) as session:
            session.add(artifact)
            self._commit(session)

    def prune_artifacts_older_than(
        self,
        *,
        older_than: datetime,
        dry_run: bool = False,
    ) -> ArtifactPruneResult:
        with Session(self.engine) as session:
            rows = list(
                session.exec(
                    select(Artifact).where(cast(Any, Artifact.created_at) < older_than)
                )
            )
            if not rows:
                return ArtifactPruneResult()

            unique_paths: list[Path] = []
            seen_paths: set[str] = set()
            for row in rows:
                raw_path = str(getattr(row, "path", "") or "").strip()
                if not raw_path or raw_path in seen_paths:
                    continue
                seen_paths.add(raw_path)
                unique_paths.append(Path(raw_path).expanduser())

            deleted_paths = 0
            missing_paths = 0
            for path in unique_paths:
                if not path.exists():
                    missing_paths += 1
                    continue
                if dry_run:
                    deleted_paths += 1
                    continue
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
                deleted_paths += 1

            if not dry_run:
                for row in rows:
                    session.delete(row)
                self._commit(session)

        return ArtifactPruneResult(
            artifact_rows=len(rows),
            deleted_paths=deleted_paths,
            missing_paths=missing_paths,
        )

    def prune_operational_history_older_than(
        self,
        *,
        older_than: datetime,
        dry_run: bool = False,
    ) -> OperationalPruneResult:
        with Session(self.engine) as session:
            runs = list(
                session.exec(
                    select(Run).where(
                        cast(Any, Run.status).in_(
                            [RUN_STATUS_SUCCEEDED, RUN_STATUS_FAILED]
                        ),
                        cast(Any, Run.finished_at).is_not(None),
                        cast(Any, Run.finished_at) < older_than,
                    )
                )
            )
            if not runs:
                return OperationalPruneResult()

            run_ids = [str(run.id) for run in runs if str(getattr(run, "id", "") or "")]
            metrics = (
                list(
                    session.exec(
                        select(Metric).where(cast(Any, Metric.run_id).in_(run_ids))
                    )
                )
                if run_ids
                else []
            )

            if not dry_run:
                for metric in metrics:
                    session.delete(metric)
                for run in runs:
                    session.delete(run)
                self._commit(session)

        return OperationalPruneResult(
            run_rows=len(runs),
            metric_rows=len(metrics),
        )

    def clear_document_chunk_cache(
        self,
        *,
        dry_run: bool = False,
    ) -> ChunkCachePruneResult:
        chunk_count_statement = text(
            "SELECT COUNT(*) FROM document_chunks"
        )
        embedding_count_statement = text(
            "SELECT COUNT(*) FROM chunk_embeddings"
        )
        fts_count_statement = text("SELECT COUNT(*) FROM chunk_fts")
        with self.engine.begin() as conn:
            document_chunks = int(conn.execute(chunk_count_statement).scalar() or 0)
            chunk_embeddings = int(conn.execute(embedding_count_statement).scalar() or 0)
            chunk_fts_rows = int(conn.execute(fts_count_statement).scalar() or 0)
            if not dry_run:
                conn.execute(text("DELETE FROM chunk_embeddings"))
                conn.execute(text("DELETE FROM chunk_fts"))
                conn.execute(text("DELETE FROM document_chunks"))
        return ChunkCachePruneResult(
            document_chunks=document_chunks,
            chunk_embeddings=chunk_embeddings,
            chunk_fts_rows=chunk_fts_rows,
        )

    def vacuum(self) -> None:
        self.engine.dispose()
        with sqlite3.connect(str(self.db_path)) as conn:
            conn.execute("VACUUM")

    def backup_database(
        self,
        *,
        output_dir: Path,
        created_at: datetime | None = None,
    ) -> DatabaseBackupResult:
        if not self.db_path.exists():
            raise ValueError(f"Database does not exist: {self.db_path}")

        timestamp = (created_at or utc_now()).astimezone(UTC)
        resolved_output_dir = output_dir.expanduser().resolve()
        resolved_output_dir.mkdir(parents=True, exist_ok=True)

        bundle_name = f"recoleta-backup-{timestamp.strftime('%Y%m%dT%H%M%SZ')}"
        bundle_dir = resolved_output_dir / bundle_name
        suffix = 1
        while bundle_dir.exists():
            suffix += 1
            bundle_dir = resolved_output_dir / f"{bundle_name}-{suffix}"
        bundle_dir.mkdir(parents=True, exist_ok=False)

        database_path = bundle_dir / self.db_path.name
        manifest_path = bundle_dir / "manifest.json"

        self.engine.dispose()
        with sqlite3.connect(str(self.db_path)) as source_conn:
            source_conn.execute("PRAGMA wal_checkpoint(FULL)")
            with sqlite3.connect(str(database_path)) as dest_conn:
                source_conn.backup(dest_conn)

        schema_version = self.schema_version()
        manifest = {
            "kind": "recoleta-db-backup",
            "created_at": timestamp.isoformat(),
            "schema_version": schema_version,
            "database_filename": database_path.name,
            "source_db_filename": self.db_path.name,
            "database_size_bytes": database_path.stat().st_size,
        }
        manifest_path.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return DatabaseBackupResult(
            bundle_dir=bundle_dir,
            database_path=database_path,
            manifest_path=manifest_path,
            schema_version=schema_version,
            created_at=timestamp,
        )

    @staticmethod
    def restore_database(
        *,
        bundle_dir: Path,
        db_path: Path,
    ) -> DatabaseRestoreResult:
        resolved_bundle_dir = bundle_dir.expanduser().resolve()
        manifest_path = resolved_bundle_dir / "manifest.json"
        if not manifest_path.exists():
            raise ValueError(f"Backup manifest does not exist: {manifest_path}")

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("Backup manifest must contain a JSON object")

        database_filename = str(manifest.get("database_filename") or "").strip()
        if not database_filename:
            raise ValueError("Backup manifest is missing database_filename")

        source_db_path = resolved_bundle_dir / database_filename
        if not source_db_path.exists():
            raise ValueError(f"Backup database does not exist: {source_db_path}")

        manifest_schema_version = int(manifest.get("schema_version") or 0)
        if manifest_schema_version > CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Backup bundle uses newer schema version "
                f"{manifest_schema_version}; current supported version is {CURRENT_SCHEMA_VERSION}."
            )

        with sqlite3.connect(str(source_db_path)) as source_conn:
            row = source_conn.execute("PRAGMA user_version").fetchone()
            source_schema_version = int(row[0]) if row and row[0] is not None else 0
        if source_schema_version > CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Backup database uses newer schema version "
                f"{source_schema_version}; current supported version is {CURRENT_SCHEMA_VERSION}."
            )

        resolved_db_path = db_path.expanduser().resolve()
        resolved_db_path.parent.mkdir(parents=True, exist_ok=True)

        temp_target_path = resolved_db_path.with_name(
            f"{resolved_db_path.name}.restore-{uuid4().hex}.tmp"
        )
        if temp_target_path.exists():
            temp_target_path.unlink()

        with sqlite3.connect(str(source_db_path)) as source_conn:
            with sqlite3.connect(str(temp_target_path)) as dest_conn:
                source_conn.backup(dest_conn)

        for sidecar in (
            resolved_db_path,
            Path(f"{resolved_db_path}-wal"),
            Path(f"{resolved_db_path}-shm"),
            Path(f"{resolved_db_path}-journal"),
        ):
            if sidecar.exists():
                sidecar.unlink()

        temp_target_path.replace(resolved_db_path)
        return DatabaseRestoreResult(
            bundle_dir=resolved_bundle_dir,
            database_path=resolved_db_path,
            schema_version=source_schema_version,
        )

    @staticmethod
    def decode_list(value: str | None) -> list[str]:
        return _from_json_list(value)
