from __future__ import annotations

from collections.abc import Callable
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
        if user_version < CURRENT_SCHEMA_VERSION:
            self._apply_startup_safe_migrations()
        SQLModel.metadata.create_all(self.engine)
        self._ensure_chunk_fts()
        self._prune_chunk_fts_meta_rows()
        if user_version < CURRENT_SCHEMA_VERSION:
            self._set_user_version(CURRENT_SCHEMA_VERSION)

    def _apply_startup_safe_migrations(self) -> None:
        self._migrate_analyses_drop_scope()
        self._migrate_documents_drop_scope()
        self._migrate_pass_outputs_drop_scope()
        self._migrate_localized_outputs_drop_scope()
        self._migrate_runs_add_heartbeat()
        self._migrate_runs_add_context()
        self._migrate_runs_add_workflow_metadata()
        self._migrate_artifacts_add_details_json()
        self._migrate_drop_item_stream_states()

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

    def _dedupe_rows(
        self,
        rows: list[dict[str, Any]],
        *,
        key_builder: Callable[[dict[str, Any]], tuple[Any, ...]],
        id_field: str = "id",
    ) -> tuple[list[dict[str, Any]], dict[int, int]]:
        winners: list[dict[str, Any]] = []
        winner_by_key: dict[tuple[Any, ...], dict[str, Any]] = {}
        id_map: dict[int, int] = {}
        for row in rows:
            try:
                row_id = int(row.get(id_field) or 0)
            except Exception:
                continue
            if row_id <= 0:
                continue
            key = key_builder(row)
            winner = winner_by_key.get(key)
            if winner is None:
                winner_by_key[key] = row
                winners.append(row)
                id_map[row_id] = row_id
                continue
            id_map[row_id] = int(winner[id_field])
        return winners, id_map

    def _migrate_analyses_drop_scope(self) -> None:
        columns = self._table_columns("analyses")
        if not columns or "scope" not in columns:
            return

        with self.engine.begin() as conn:
            rows = self._fetch_rows(
                conn,
                """
                SELECT
                    id,
                    item_id,
                    model,
                    provider,
                    summary,
                    topics_json,
                    relevance_score,
                    novelty_score,
                    cost_usd,
                    latency_ms,
                    created_at
                FROM analyses
                ORDER BY created_at DESC, id DESC;
                """,
            )
            winners, _ = self._dedupe_rows(
                rows,
                key_builder=lambda row: (int(row.get("item_id") or 0),),
            )
            conn.execute(
                text(
                    """
                    CREATE TABLE analyses__new (
                        id INTEGER PRIMARY KEY,
                        item_id INTEGER NOT NULL,
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
                    """
                )
            )
            if winners:
                conn.execute(
                    text(
                        """
                        INSERT INTO analyses__new (
                            id,
                            item_id,
                            model,
                            provider,
                            summary,
                            topics_json,
                            relevance_score,
                            novelty_score,
                            cost_usd,
                            latency_ms,
                            created_at
                        ) VALUES (
                            :id,
                            :item_id,
                            :model,
                            :provider,
                            :summary,
                            :topics_json,
                            :relevance_score,
                            :novelty_score,
                            :cost_usd,
                            :latency_ms,
                            :created_at
                        );
                        """
                    ),
                    winners,
                )
            conn.execute(text("DROP TABLE analyses;"))
            conn.execute(text("ALTER TABLE analyses__new RENAME TO analyses;"))
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_analyses_item_id ON analyses (item_id);")
            )
            conn.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS uq_analyses_item ON analyses (item_id);")
            )

    def _migrate_documents_drop_scope(self) -> None:
        columns = self._table_columns("documents")
        if not columns or "scope" not in columns:
            return

        with self.engine.begin() as conn:
            document_rows = self._fetch_rows(
                conn,
                """
                SELECT
                    id,
                    doc_type,
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
                FROM documents
                ORDER BY updated_at DESC, created_at DESC, id DESC;
                """,
            )

            def document_key(row: dict[str, Any]) -> tuple[Any, ...]:
                doc_type = str(row.get("doc_type") or "").strip()
                item_id = row.get("item_id")
                if item_id is not None:
                    try:
                        normalized_item_id: Any = int(item_id)
                    except Exception:
                        normalized_item_id = item_id
                    return ("item", doc_type, normalized_item_id)
                return (
                    "period",
                    doc_type,
                    str(row.get("granularity") or "").strip(),
                    row.get("period_start"),
                    row.get("period_end"),
                )

            document_winners, document_id_map = self._dedupe_rows(
                document_rows,
                key_builder=document_key,
            )

            conn.execute(
                text(
                    """
                    CREATE TABLE documents__new (
                        id INTEGER PRIMARY KEY,
                        doc_type VARCHAR(16) NOT NULL,
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
                    """
                )
            )
            if document_winners:
                conn.execute(
                    text(
                        """
                        INSERT INTO documents__new (
                            id,
                            doc_type,
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
                        ) VALUES (
                            :id,
                            :doc_type,
                            :item_id,
                            :source,
                            :canonical_url,
                            :title,
                            :published_at,
                            :granularity,
                            :period_start,
                            :period_end,
                            :created_at,
                            :updated_at
                        );
                        """
                    ),
                    document_winners,
                )

            if self._conn_has_table(conn, "localized_outputs"):
                localized_updates = [
                    {"old_id": old_id, "new_id": new_id}
                    for old_id, new_id in document_id_map.items()
                    if old_id != new_id
                ]
                if localized_updates:
                    conn.execute(
                        text(
                            """
                            UPDATE localized_outputs
                            SET source_record_id = :new_id
                            WHERE source_kind IN ('trend_synthesis', 'trend_ideas')
                              AND source_record_id = :old_id;
                            """
                        ),
                        localized_updates,
                    )

            chunk_id_map: dict[int, int] = {}
            rewrite_document_chunks = self._conn_has_table(conn, "document_chunks")
            rewrite_chunk_embeddings = self._conn_has_table(conn, "chunk_embeddings")
            rewrite_trend_deliveries = self._conn_has_table(conn, "trend_deliveries")

            if rewrite_document_chunks:
                chunk_rows = self._fetch_rows(
                    conn,
                    """
                    SELECT
                        id,
                        doc_id,
                        chunk_index,
                        kind,
                        text,
                        start_char,
                        end_char,
                        text_hash,
                        source_content_type,
                        created_at
                    FROM document_chunks
                    ORDER BY created_at DESC, id DESC;
                    """,
                )
                remapped_chunk_rows: list[dict[str, Any]] = []
                for row in chunk_rows:
                    try:
                        old_doc_id = int(row.get("doc_id") or 0)
                    except Exception:
                        continue
                    new_doc_id = document_id_map.get(old_doc_id)
                    if new_doc_id is None:
                        continue
                    remapped = dict(row)
                    remapped["doc_id"] = new_doc_id
                    remapped_chunk_rows.append(remapped)
                chunk_winners, chunk_id_map = self._dedupe_rows(
                    remapped_chunk_rows,
                    key_builder=lambda row: (
                        int(row.get("doc_id") or 0),
                        int(row.get("chunk_index") or 0),
                    ),
                )
                conn.execute(
                    text(
                        """
                        CREATE TABLE document_chunks__new (
                            id INTEGER PRIMARY KEY,
                            doc_id INTEGER NOT NULL,
                            chunk_index INTEGER NOT NULL,
                            kind VARCHAR(16) NOT NULL,
                            text TEXT NOT NULL,
                            start_char INTEGER,
                            end_char INTEGER,
                            text_hash VARCHAR(64) NOT NULL,
                            source_content_type VARCHAR(32),
                            created_at DATETIME NOT NULL,
                            FOREIGN KEY(doc_id) REFERENCES documents (id)
                        );
                        """
                    )
                )
                if chunk_winners:
                    conn.execute(
                        text(
                            """
                            INSERT INTO document_chunks__new (
                                id,
                                doc_id,
                                chunk_index,
                                kind,
                                text,
                                start_char,
                                end_char,
                                text_hash,
                                source_content_type,
                                created_at
                            ) VALUES (
                                :id,
                                :doc_id,
                                :chunk_index,
                                :kind,
                                :text,
                                :start_char,
                                :end_char,
                                :text_hash,
                                :source_content_type,
                                :created_at
                            );
                            """
                        ),
                        chunk_winners,
                    )

            if rewrite_chunk_embeddings:
                embedding_rows = self._fetch_rows(
                    conn,
                    """
                    SELECT
                        id,
                        chunk_id,
                        model,
                        dimensions,
                        vector_json,
                        text_hash,
                        created_at
                    FROM chunk_embeddings
                    ORDER BY created_at DESC, id DESC;
                    """,
                )
                remapped_embedding_rows: list[dict[str, Any]] = []
                for row in embedding_rows:
                    try:
                        old_chunk_id = int(row.get("chunk_id") or 0)
                    except Exception:
                        continue
                    if rewrite_document_chunks:
                        new_chunk_id = chunk_id_map.get(old_chunk_id)
                        if new_chunk_id is None:
                            continue
                    else:
                        new_chunk_id = old_chunk_id
                    remapped = dict(row)
                    remapped["chunk_id"] = new_chunk_id
                    remapped_embedding_rows.append(remapped)
                embedding_winners, _ = self._dedupe_rows(
                    remapped_embedding_rows,
                    key_builder=lambda row: (
                        int(row.get("chunk_id") or 0),
                        str(row.get("model") or "").strip(),
                    ),
                )
                conn.execute(
                    text(
                        """
                        CREATE TABLE chunk_embeddings__new (
                            id INTEGER PRIMARY KEY,
                            chunk_id INTEGER NOT NULL,
                            model VARCHAR(128) NOT NULL,
                            dimensions INTEGER,
                            vector_json TEXT NOT NULL,
                            text_hash VARCHAR(64) NOT NULL,
                            created_at DATETIME NOT NULL,
                            FOREIGN KEY(chunk_id) REFERENCES document_chunks (id)
                        );
                        """
                    )
                )
                if embedding_winners:
                    conn.execute(
                        text(
                            """
                            INSERT INTO chunk_embeddings__new (
                                id,
                                chunk_id,
                                model,
                                dimensions,
                                vector_json,
                                text_hash,
                                created_at
                            ) VALUES (
                                :id,
                                :chunk_id,
                                :model,
                                :dimensions,
                                :vector_json,
                                :text_hash,
                                :created_at
                            );
                            """
                        ),
                        embedding_winners,
                    )

            if rewrite_trend_deliveries:
                delivery_rows = self._fetch_rows(
                    conn,
                    """
                    SELECT
                        id,
                        doc_id,
                        channel,
                        destination,
                        content_hash,
                        message_id,
                        status,
                        error,
                        sent_at
                    FROM trend_deliveries
                    ORDER BY
                        CASE WHEN sent_at IS NULL THEN 0 ELSE 1 END DESC,
                        sent_at DESC,
                        id DESC;
                    """,
                )
                remapped_delivery_rows: list[dict[str, Any]] = []
                for row in delivery_rows:
                    try:
                        old_doc_id = int(row.get("doc_id") or 0)
                    except Exception:
                        continue
                    new_doc_id = document_id_map.get(old_doc_id)
                    if new_doc_id is None:
                        continue
                    remapped = dict(row)
                    remapped["doc_id"] = new_doc_id
                    remapped_delivery_rows.append(remapped)
                delivery_winners, _ = self._dedupe_rows(
                    remapped_delivery_rows,
                    key_builder=lambda row: (
                        int(row.get("doc_id") or 0),
                        str(row.get("channel") or "").strip(),
                        str(row.get("destination") or "").strip(),
                    ),
                )
                conn.execute(
                    text(
                        """
                        CREATE TABLE trend_deliveries__new (
                            id INTEGER PRIMARY KEY,
                            doc_id INTEGER NOT NULL,
                            channel VARCHAR(32) NOT NULL,
                            destination VARCHAR(128) NOT NULL,
                            content_hash VARCHAR(64) NOT NULL,
                            message_id VARCHAR(128),
                            status VARCHAR(24) NOT NULL,
                            error TEXT,
                            sent_at DATETIME,
                            FOREIGN KEY(doc_id) REFERENCES documents (id)
                        );
                        """
                    )
                )
                if delivery_winners:
                    conn.execute(
                        text(
                            """
                            INSERT INTO trend_deliveries__new (
                                id,
                                doc_id,
                                channel,
                                destination,
                                content_hash,
                                message_id,
                                status,
                                error,
                                sent_at
                            ) VALUES (
                                :id,
                                :doc_id,
                                :channel,
                                :destination,
                                :content_hash,
                                :message_id,
                                :status,
                                :error,
                                :sent_at
                            );
                            """
                        ),
                        delivery_winners,
                    )

            if rewrite_chunk_embeddings:
                conn.execute(text("DROP TABLE chunk_embeddings;"))
                conn.execute(text("ALTER TABLE chunk_embeddings__new RENAME TO chunk_embeddings;"))
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_chunk_embeddings_chunk_id ON chunk_embeddings (chunk_id);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_chunk_embeddings_model ON chunk_embeddings (model);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_chunk_embeddings_text_hash ON chunk_embeddings (text_hash);")
                )
                conn.execute(
                    text("CREATE UNIQUE INDEX IF NOT EXISTS uq_chunk_embeddings_chunk_model ON chunk_embeddings (chunk_id, model);")
                )

            if rewrite_document_chunks:
                conn.execute(text("DROP TABLE document_chunks;"))
                conn.execute(text("ALTER TABLE document_chunks__new RENAME TO document_chunks;"))
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_document_chunks_doc_id ON document_chunks (doc_id);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_document_chunks_chunk_index ON document_chunks (chunk_index);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_document_chunks_kind ON document_chunks (kind);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_document_chunks_text_hash ON document_chunks (text_hash);")
                )
                conn.execute(
                    text("CREATE UNIQUE INDEX IF NOT EXISTS uq_document_chunks_doc_chunk ON document_chunks (doc_id, chunk_index);")
                )

            if rewrite_trend_deliveries:
                conn.execute(text("DROP TABLE trend_deliveries;"))
                conn.execute(text("ALTER TABLE trend_deliveries__new RENAME TO trend_deliveries;"))
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_trend_deliveries_doc_id ON trend_deliveries (doc_id);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_trend_deliveries_destination ON trend_deliveries (destination);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_trend_deliveries_content_hash ON trend_deliveries (content_hash);")
                )
                conn.execute(
                    text("CREATE INDEX IF NOT EXISTS ix_trend_deliveries_status ON trend_deliveries (status);")
                )
                conn.execute(
                    text("CREATE UNIQUE INDEX IF NOT EXISTS uq_trend_deliveries_doc_channel_destination ON trend_deliveries (doc_id, channel, destination);")
                )

            conn.execute(text("DROP TABLE documents;"))
            conn.execute(text("ALTER TABLE documents__new RENAME TO documents;"))
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_doc_type ON documents (doc_type);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_item_id ON documents (item_id);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_published_at ON documents (published_at);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_granularity ON documents (granularity);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_period_start ON documents (period_start);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_documents_period_end ON documents (period_end);")
            )
            conn.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS uq_documents_doc_type_item ON documents (doc_type, item_id);")
            )
            conn.execute(
                text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_documents_doc_type_granularity_period ON documents (doc_type, granularity, period_start, period_end);"
                )
            )

            if rewrite_document_chunks:
                self._rebuild_chunk_fts_from_chunks(conn)

    def _migrate_pass_outputs_drop_scope(self) -> None:
        columns = self._table_columns("pass_outputs")
        if not columns or "scope" not in columns:
            return

        ddl = [
            """
            CREATE TABLE pass_outputs__new (
                id INTEGER PRIMARY KEY,
                run_id VARCHAR NOT NULL,
                pass_kind VARCHAR(64) NOT NULL,
                status VARCHAR(24) NOT NULL,
                granularity VARCHAR(16),
                period_start DATETIME,
                period_end DATETIME,
                schema_version INTEGER NOT NULL DEFAULT 1,
                content_hash VARCHAR(64) NOT NULL,
                payload_json TEXT NOT NULL DEFAULT '{}',
                diagnostics_json TEXT NOT NULL DEFAULT '{}',
                input_refs_json TEXT NOT NULL DEFAULT '[]',
                created_at DATETIME NOT NULL,
                FOREIGN KEY(run_id) REFERENCES runs (id)
            );
            """,
            """
            INSERT INTO pass_outputs__new (
                id,
                run_id,
                pass_kind,
                status,
                granularity,
                period_start,
                period_end,
                schema_version,
                content_hash,
                payload_json,
                diagnostics_json,
                input_refs_json,
                created_at
            )
            SELECT
                id,
                run_id,
                pass_kind,
                status,
                granularity,
                period_start,
                period_end,
                schema_version,
                content_hash,
                payload_json,
                diagnostics_json,
                input_refs_json,
                created_at
            FROM pass_outputs;
            """,
            "DROP TABLE pass_outputs;",
            "ALTER TABLE pass_outputs__new RENAME TO pass_outputs;",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_run_id ON pass_outputs (run_id);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_pass_kind ON pass_outputs (pass_kind);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_status ON pass_outputs (status);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_granularity ON pass_outputs (granularity);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_period_start ON pass_outputs (period_start);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_period_end ON pass_outputs (period_end);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_content_hash ON pass_outputs (content_hash);",
            "CREATE INDEX IF NOT EXISTS ix_pass_outputs_created_at ON pass_outputs (created_at);",
        ]
        with self.engine.begin() as conn:
            for statement in ddl:
                conn.execute(text(statement))

    def _migrate_localized_outputs_drop_scope(self) -> None:
        columns = self._table_columns("localized_outputs")
        if not columns or "scope" not in columns:
            return

        with self.engine.begin() as conn:
            rows = self._fetch_rows(
                conn,
                """
                SELECT
                    id,
                    source_kind,
                    source_record_id,
                    language_code,
                    status,
                    schema_version,
                    source_hash,
                    variant_role,
                    payload_json,
                    diagnostics_json,
                    created_at,
                    updated_at
                FROM localized_outputs
                ORDER BY updated_at DESC, created_at DESC, id DESC;
                """,
            )
            winners, _ = self._dedupe_rows(
                rows,
                key_builder=lambda row: (
                    str(row.get("source_kind") or "").strip(),
                    int(row.get("source_record_id") or 0),
                    str(row.get("language_code") or "").strip(),
                ),
            )
            conn.execute(
                text(
                    """
                    CREATE TABLE localized_outputs__new (
                        id INTEGER PRIMARY KEY,
                        source_kind VARCHAR(32) NOT NULL,
                        source_record_id INTEGER NOT NULL,
                        language_code VARCHAR(32) NOT NULL,
                        status VARCHAR(24) NOT NULL DEFAULT 'succeeded',
                        schema_version INTEGER NOT NULL DEFAULT 1,
                        source_hash VARCHAR(64) NOT NULL,
                        variant_role VARCHAR(16) NOT NULL DEFAULT 'translation',
                        payload_json TEXT NOT NULL DEFAULT '{}',
                        diagnostics_json TEXT NOT NULL DEFAULT '{}',
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL
                    );
                    """
                )
            )
            if winners:
                conn.execute(
                    text(
                        """
                        INSERT INTO localized_outputs__new (
                            id,
                            source_kind,
                            source_record_id,
                            language_code,
                            status,
                            schema_version,
                            source_hash,
                            variant_role,
                            payload_json,
                            diagnostics_json,
                            created_at,
                            updated_at
                        ) VALUES (
                            :id,
                            :source_kind,
                            :source_record_id,
                            :language_code,
                            :status,
                            :schema_version,
                            :source_hash,
                            :variant_role,
                            :payload_json,
                            :diagnostics_json,
                            :created_at,
                            :updated_at
                        );
                        """
                    ),
                    winners,
                )
            conn.execute(text("DROP TABLE localized_outputs;"))
            conn.execute(text("ALTER TABLE localized_outputs__new RENAME TO localized_outputs;"))
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_source_kind ON localized_outputs (source_kind);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_source_record_id ON localized_outputs (source_record_id);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_language_code ON localized_outputs (language_code);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_status ON localized_outputs (status);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_source_hash ON localized_outputs (source_hash);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_variant_role ON localized_outputs (variant_role);")
            )
            conn.execute(
                text("CREATE INDEX IF NOT EXISTS ix_localized_outputs_updated_at ON localized_outputs (updated_at);")
            )
            conn.execute(
                text("CREATE UNIQUE INDEX IF NOT EXISTS uq_localized_outputs_source_language ON localized_outputs (source_kind, source_record_id, language_code);")
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

    def _migrate_drop_item_stream_states(self) -> None:
        if not self.has_table("item_stream_states"):
            return
        with self.engine.begin() as conn:
            conn.execute(text("DROP TABLE item_stream_states;"))

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
