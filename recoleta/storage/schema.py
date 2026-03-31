from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlmodel import SQLModel

from recoleta.storage_common import CURRENT_SCHEMA_VERSION, SchemaVersionError


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
        self._assert_no_legacy_shared_stream_tables()
        if user_version < CURRENT_SCHEMA_VERSION:
            self._apply_startup_safe_migrations()
        SQLModel.metadata.create_all(self.engine)
        self._ensure_chunk_fts()
        self._prune_chunk_fts_meta_rows()
        if user_version < CURRENT_SCHEMA_VERSION:
            self._set_user_version(CURRENT_SCHEMA_VERSION)

    def _apply_startup_safe_migrations(self) -> None:
        self._migrate_runs_add_heartbeat()
        self._migrate_runs_add_context()
        self._migrate_runs_add_workflow_metadata()
        self._migrate_artifacts_add_details_json()

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

    def _conn_has_table(self, conn: Any, table_name: str) -> bool:
        row = conn.execute(
            text(
                """
                SELECT 1
                FROM sqlite_master
                WHERE type = 'table' AND name = :name
                LIMIT 1;
                """
            ),
            {"name": str(table_name or "").strip()},
        ).fetchone()
        return row is not None

    def _fetch_rows(self, conn: Any, statement: str) -> list[dict[str, Any]]:
        return [dict(row) for row in conn.execute(text(statement)).mappings()]

    def _assert_no_legacy_shared_stream_tables(self) -> None:
        legacy_scope_tables = [
            table_name
            for table_name in ("analyses", "documents", "pass_outputs", "localized_outputs")
            if "scope" in self._table_columns(table_name)
        ]
        if not legacy_scope_tables:
            return
        joined = ", ".join(sorted(legacy_scope_tables))
        raise SchemaVersionError(
            "Legacy shared-stream child tables are no longer supported by this runtime. "
            f"Unsupported tables with a scope column: {joined}."
        )

    def _migrate_runs_add_workflow_metadata(self) -> None:
        columns = self._table_columns("runs")
        if not columns:
            return

        ddl: list[str] = []
        index_ddl: list[str] = []
        if "operation_kind" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN operation_kind VARCHAR(64);"
            )
            index_ddl.append(
                "CREATE INDEX IF NOT EXISTS ix_runs_operation_kind ON runs (operation_kind);"
            )
        if "target_granularity" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN target_granularity VARCHAR(16);"
            )
            index_ddl.append(
                "CREATE INDEX IF NOT EXISTS ix_runs_target_granularity ON runs (target_granularity);"
            )
        if "target_period_start" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN target_period_start DATETIME;")
            index_ddl.append(
                "CREATE INDEX IF NOT EXISTS ix_runs_target_period_start ON runs (target_period_start);"
            )
        if "target_period_end" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN target_period_end DATETIME;")
            index_ddl.append(
                "CREATE INDEX IF NOT EXISTS ix_runs_target_period_end ON runs (target_period_end);"
            )
        if "requested_steps_json" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN requested_steps_json TEXT NOT NULL DEFAULT '[]';"
            )
        if "executed_steps_json" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN executed_steps_json TEXT NOT NULL DEFAULT '[]';"
            )
        if "skipped_steps_json" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN skipped_steps_json TEXT NOT NULL DEFAULT '[]';"
            )
        if "billing_by_step_json" not in columns:
            ddl.append(
                "ALTER TABLE runs ADD COLUMN billing_by_step_json TEXT NOT NULL DEFAULT '{}';"
            )
        if "terminal_state" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN terminal_state VARCHAR(32);")
            index_ddl.append(
                "CREATE INDEX IF NOT EXISTS ix_runs_terminal_state ON runs (terminal_state);"
            )

        if not ddl and not index_ddl:
            return

        with self.engine.begin() as conn:
            for statement in ddl + index_ddl:
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

    def _migrate_runs_add_context(self) -> None:
        columns = self._table_columns("runs")
        if not columns:
            return

        ddl: list[str] = []
        if "command" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN command VARCHAR(128);")
        if "scope" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN scope VARCHAR(64);")
        if "granularity" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN granularity VARCHAR(16);")
        if "period_start" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN period_start DATETIME;")
        if "period_end" not in columns:
            ddl.append("ALTER TABLE runs ADD COLUMN period_end DATETIME;")
        ddl.extend(
            [
                "CREATE INDEX IF NOT EXISTS ix_runs_command ON runs (command);",
                "CREATE INDEX IF NOT EXISTS ix_runs_scope ON runs (scope);",
                "CREATE INDEX IF NOT EXISTS ix_runs_granularity ON runs (granularity);",
                "CREATE INDEX IF NOT EXISTS ix_runs_period_start ON runs (period_start);",
                "CREATE INDEX IF NOT EXISTS ix_runs_period_end ON runs (period_end);",
            ]
        )
        with self.engine.begin() as conn:
            for statement in ddl:
                conn.execute(text(statement))

    def _migrate_artifacts_add_details_json(self) -> None:
        columns = self._table_columns("artifacts")
        if not columns or "details_json" in columns:
            return

        with self.engine.begin() as conn:
            conn.execute(
                text(
                    "ALTER TABLE artifacts ADD COLUMN details_json TEXT NOT NULL DEFAULT '{}';"
                )
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

    def _rebuild_chunk_fts_from_chunks(self, conn: Any) -> None:
        if not self._conn_has_table(conn, "chunk_fts") or not self._conn_has_table(
            conn, "document_chunks"
        ):
            return
        conn.execute(text("DELETE FROM chunk_fts;"))
        conn.execute(
            text(
                """
                INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind)
                SELECT id, text, doc_id, chunk_index, kind
                FROM document_chunks;
                """
            )
        )

    def _prune_chunk_fts_meta_rows(self) -> None:
        if not self.has_table("chunk_fts"):
            return
        with self.engine.begin() as conn:
            conn.execute(text("DELETE FROM chunk_fts WHERE kind = 'meta'"))
