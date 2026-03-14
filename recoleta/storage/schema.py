from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlmodel import SQLModel

from recoleta.models import (
    ITEM_STATE_ANALYZED,
    ITEM_STATE_FAILED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage_common import CURRENT_SCHEMA_VERSION, SchemaVersionError
from recoleta.types import DEFAULT_TOPIC_STREAM


class SchemaStoreMixin:
    engine: Any

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
        self._prune_chunk_fts_meta_rows()
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

    def _prune_chunk_fts_meta_rows(self) -> None:
        if not self.has_table("chunk_fts"):
            return
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM chunk_fts WHERE kind = 'meta'"))
