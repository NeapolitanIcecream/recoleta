from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import sqlite3
import re
import shutil
from datetime import UTC, datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Any, cast
from uuid import uuid4

from rapidfuzz import fuzz
from sqlalchemy import desc, event, func, text
from sqlalchemy import and_, or_
from sqlalchemy.orm import aliased
from sqlmodel import Session, SQLModel, create_engine, select

from recoleta.models import (
    Analysis,
    Artifact,
    ChunkEmbedding,
    Content,
    Delivery,
    Document,
    DocumentChunk,
    ItemStreamState,
    Item,
    Metric,
    Run,
    TrendDelivery,
    WorkspaceLease,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.types import (
    AnalysisResult,
    DEFAULT_TOPIC_STREAM,
    ItemDraft,
    sha256_hex,
    utc_now,
)


CURRENT_SCHEMA_VERSION = 1
WORKSPACE_LEASE_NAME = "workspace"


class SchemaVersionError(RuntimeError):
    """Raised when the on-disk schema is incompatible with this binary."""


class WorkspaceLeaseError(RuntimeError):
    """Raised when workspace lease operations fail."""


class WorkspaceLeaseHeldError(WorkspaceLeaseError):
    def __init__(
        self,
        *,
        lease_name: str,
        holder_run_id: str | None,
        holder_command: str | None,
        holder_hostname: str | None,
        holder_pid: int | None,
        expires_at: datetime | None,
        requested_run_id: str | None,
    ) -> None:
        self.lease_name = lease_name
        self.holder_run_id = holder_run_id
        self.holder_command = holder_command
        self.holder_hostname = holder_hostname
        self.holder_pid = holder_pid
        self.expires_at = expires_at
        self.requested_run_id = requested_run_id
        expires_text = expires_at.isoformat() if isinstance(expires_at, datetime) else ""
        details = " ".join(
            part
            for part in (
                f"lease={lease_name}",
                f"holder_run_id={holder_run_id}" if holder_run_id else "",
                f"holder_command={holder_command}" if holder_command else "",
                f"holder_hostname={holder_hostname}" if holder_hostname else "",
                f"holder_pid={holder_pid}" if holder_pid is not None else "",
                f"expires_at={expires_text}" if expires_text else "",
            )
            if part
        )
        super().__init__(f"workspace lease is held {details}".strip())


class WorkspaceLeaseLostError(WorkspaceLeaseError):
    def __init__(self, *, lease_name: str, owner_token: str) -> None:
        self.lease_name = lease_name
        self.owner_token = owner_token
        super().__init__(f"workspace lease lost lease={lease_name}")


def _to_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _from_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    loaded = json.loads(value)
    if isinstance(loaded, list):
        return [str(item) for item in loaded]
    return []


def _from_json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        loaded = json.loads(value)
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


_FTS5_QUERY_TOKEN_RE = re.compile(r"\w+", flags=re.UNICODE)


def _to_fts5_query(value: str) -> str:
    """Convert plain text into a safe FTS5 query (no operators, no column filters)."""

    tokens = _FTS5_QUERY_TOKEN_RE.findall(value)
    if not tokens:
        return ""
    escaped_tokens = [token.replace('"', '""') for token in tokens]
    return " ".join(f'"{token}"' for token in escaped_tokens)


@dataclass
class SqlDiagnostics:
    queries_total: int = 0
    commits_total: int = 0


@dataclass(frozen=True, slots=True)
class ArtifactPruneResult:
    artifact_rows: int = 0
    deleted_paths: int = 0
    missing_paths: int = 0


@dataclass(frozen=True, slots=True)
class OperationalPruneResult:
    run_rows: int = 0
    metric_rows: int = 0


@dataclass(frozen=True, slots=True)
class ChunkCachePruneResult:
    document_chunks: int = 0
    chunk_embeddings: int = 0
    chunk_fts_rows: int = 0


@dataclass(frozen=True, slots=True)
class DatabaseBackupResult:
    bundle_dir: Path
    database_path: Path
    manifest_path: Path
    schema_version: int
    created_at: datetime


@dataclass(frozen=True, slots=True)
class DatabaseRestoreResult:
    bundle_dir: Path
    database_path: Path
    schema_version: int


@dataclass(frozen=True, slots=True)
class WorkspaceStatsResult:
    item_state_counts: dict[str, int]
    unfinished_total: int
    oldest_unfinished_at: datetime | None
    run_status_counts: dict[str, int]
    stale_running_runs: int
    latest_successful_run_id: str | None
    latest_successful_run_at: datetime | None


class Repository:
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

    def create_run(self, config_fingerprint: str, run_id: str | None = None) -> Run:
        now = utc_now()
        run = Run(
            id=run_id or str(uuid4()),
            started_at=now,
            heartbeat_at=now,
            status=RUN_STATUS_RUNNING,
            config_fingerprint=config_fingerprint,
        )
        with Session(self.engine) as session:
            session.add(run)
            self._commit(session)
            session.refresh(run)
            return run

    def finish_run(self, run_id: str, success: bool) -> None:
        final_status = RUN_STATUS_SUCCEEDED if success else RUN_STATUS_FAILED
        finished_at = utc_now()
        with Session(self.engine) as session:
            run = session.get(Run, run_id)
            if run is None:
                return
            run.status = final_status
            run.finished_at = finished_at
            run.heartbeat_at = finished_at
            session.add(run)
            self._commit(session)

    def heartbeat_run(self, run_id: str, *, now: datetime | None = None) -> None:
        heartbeat_at = now or utc_now()
        statement = text(
            """
            UPDATE runs
            SET heartbeat_at = :heartbeat_at
            WHERE id = :run_id
              AND status = :running_status;
            """
        )
        with self.engine.begin() as conn:
            conn.execute(
                statement,
                {
                    "heartbeat_at": heartbeat_at,
                    "run_id": run_id,
                    "running_status": RUN_STATUS_RUNNING,
                },
            )

    def mark_stale_runs_failed(
        self,
        *,
        stale_after_seconds: int,
        now: datetime | None = None,
    ) -> int:
        reference_now = now or utc_now()
        cutoff = reference_now - timedelta(seconds=max(1, int(stale_after_seconds)))
        statement = text(
            """
            UPDATE runs
            SET status = :failed_status,
                finished_at = :finished_at,
                heartbeat_at = :finished_at
            WHERE status = :running_status
              AND COALESCE(heartbeat_at, started_at) < :cutoff;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "failed_status": RUN_STATUS_FAILED,
                    "finished_at": reference_now,
                    "running_status": RUN_STATUS_RUNNING,
                    "cutoff": cutoff,
                },
            )
        return int(result.rowcount or 0)

    def acquire_workspace_lease(
        self,
        *,
        owner_token: str,
        command: str,
        lease_timeout_seconds: int,
        run_id: str | None = None,
        hostname: str | None = None,
        pid: int | None = None,
        name: str = WORKSPACE_LEASE_NAME,
        now: datetime | None = None,
    ) -> WorkspaceLease:
        acquired_at = now or utc_now()
        expires_at = acquired_at + timedelta(
            seconds=max(1, int(lease_timeout_seconds))
        )
        statement = text(
            """
            INSERT INTO workspace_leases (
                name,
                owner_token,
                run_id,
                pid,
                hostname,
                command,
                acquired_at,
                heartbeat_at,
                expires_at
            )
            VALUES (
                :name,
                :owner_token,
                :run_id,
                :pid,
                :hostname,
                :command,
                :acquired_at,
                :heartbeat_at,
                :expires_at
            )
            ON CONFLICT(name) DO UPDATE SET
                owner_token = excluded.owner_token,
                run_id = excluded.run_id,
                pid = excluded.pid,
                hostname = excluded.hostname,
                command = excluded.command,
                acquired_at = excluded.acquired_at,
                heartbeat_at = excluded.heartbeat_at,
                expires_at = excluded.expires_at
            WHERE workspace_leases.expires_at <= :acquired_at
               OR workspace_leases.owner_token = :owner_token;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "name": name,
                    "owner_token": owner_token,
                    "run_id": run_id,
                    "pid": pid,
                    "hostname": hostname,
                    "command": command,
                    "acquired_at": acquired_at,
                    "heartbeat_at": acquired_at,
                    "expires_at": expires_at,
                },
            )
        lease = self.get_workspace_lease(name=name)
        if int(result.rowcount or 0) <= 0 or lease is None:
            raise self._workspace_lease_held_error(
                name=name,
                requested_run_id=run_id,
            )
        return lease

    def renew_workspace_lease(
        self,
        *,
        owner_token: str,
        lease_timeout_seconds: int,
        name: str = WORKSPACE_LEASE_NAME,
        now: datetime | None = None,
    ) -> WorkspaceLease:
        heartbeat_at = now or utc_now()
        expires_at = heartbeat_at + timedelta(
            seconds=max(1, int(lease_timeout_seconds))
        )
        statement = text(
            """
            UPDATE workspace_leases
            SET heartbeat_at = :heartbeat_at,
                expires_at = :expires_at
            WHERE name = :name
              AND owner_token = :owner_token;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "heartbeat_at": heartbeat_at,
                    "expires_at": expires_at,
                    "name": name,
                    "owner_token": owner_token,
                },
            )
        if int(result.rowcount or 0) <= 0:
            raise WorkspaceLeaseLostError(
                lease_name=name,
                owner_token=owner_token,
            )
        lease = self.get_workspace_lease(name=name)
        if lease is None:
            raise WorkspaceLeaseLostError(
                lease_name=name,
                owner_token=owner_token,
            )
        return lease

    def release_workspace_lease(
        self,
        *,
        owner_token: str,
        name: str = WORKSPACE_LEASE_NAME,
    ) -> bool:
        statement = text(
            """
            DELETE FROM workspace_leases
            WHERE name = :name
              AND owner_token = :owner_token;
            """
        )
        with self.engine.begin() as conn:
            result = conn.execute(
                statement,
                {
                    "name": name,
                    "owner_token": owner_token,
                },
            )
        return int(result.rowcount or 0) > 0

    def get_workspace_lease(
        self, *, name: str = WORKSPACE_LEASE_NAME
    ) -> WorkspaceLease | None:
        with Session(self.engine) as session:
            return session.get(WorkspaceLease, name)

    def list_recent_runs(self, *, limit: int = 5) -> list[Run]:
        normalized_limit = max(0, int(limit))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = (
                select(Run)
                .order_by(
                    desc(cast(Any, Run.started_at)),
                    desc(cast(Any, Run.id)),
                )
                .limit(normalized_limit)
                )
            return list(session.exec(statement))

    def collect_workspace_stats(
        self,
        *,
        stale_after_seconds: int,
        now: datetime | None = None,
    ) -> WorkspaceStatsResult:
        reference_now = now or utc_now()
        cutoff = reference_now - timedelta(seconds=max(1, int(stale_after_seconds)))
        item_state_counts = {
            ITEM_STATE_INGESTED: 0,
            ITEM_STATE_ENRICHED: 0,
            ITEM_STATE_TRIAGED: 0,
            ITEM_STATE_ANALYZED: 0,
            ITEM_STATE_PUBLISHED: 0,
            ITEM_STATE_RETRYABLE_FAILED: 0,
            ITEM_STATE_FAILED: 0,
        }
        run_status_counts = {
            RUN_STATUS_RUNNING: 0,
            RUN_STATUS_SUCCEEDED: 0,
            RUN_STATUS_FAILED: 0,
        }

        with Session(self.engine) as session:
            item_counts_statement = select(
                Item.state,
                func.count(cast(Any, Item.id)),
            ).group_by(Item.state)
            for state, count in session.exec(item_counts_statement):
                normalized_state = str(state or "").strip()
                if not normalized_state:
                    continue
                item_state_counts[normalized_state] = int(count or 0)

            oldest_unfinished_statement = select(
                func.min(cast(Any, Item.created_at))
            ).where(
                ~cast(Any, Item.state).in_(
                    [
                        ITEM_STATE_PUBLISHED,
                        ITEM_STATE_FAILED,
                    ]
                )
            )
            oldest_unfinished_at = session.exec(oldest_unfinished_statement).one()

            run_counts_statement = select(
                Run.status,
                func.count(cast(Any, Run.id)),
            ).group_by(Run.status)
            for status, count in session.exec(run_counts_statement):
                normalized_status = str(status or "").strip()
                if not normalized_status:
                    continue
                run_status_counts[normalized_status] = int(count or 0)

            stale_running_statement = select(func.count(cast(Any, Run.id))).where(
                Run.status == RUN_STATUS_RUNNING,
                func.coalesce(Run.heartbeat_at, Run.started_at) < cutoff,
            )
            stale_running_runs = int(session.exec(stale_running_statement).one())

            latest_successful_statement = (
                select(Run)
                .where(Run.status == RUN_STATUS_SUCCEEDED)
                .order_by(
                    desc(cast(Any, Run.finished_at)),
                    desc(cast(Any, Run.started_at)),
                    desc(cast(Any, Run.id)),
                )
                .limit(1)
            )
            latest_successful_run = session.exec(latest_successful_statement).first()

        unfinished_total = sum(
            count
            for state, count in item_state_counts.items()
            if state not in {ITEM_STATE_PUBLISHED, ITEM_STATE_FAILED}
        )
        latest_successful_run_at = None
        latest_successful_run_id = None
        if latest_successful_run is not None:
            latest_successful_run_id = latest_successful_run.id
            latest_successful_run_at = (
                latest_successful_run.finished_at
                or latest_successful_run.heartbeat_at
                or latest_successful_run.started_at
            )

        return WorkspaceStatsResult(
            item_state_counts=item_state_counts,
            unfinished_total=unfinished_total,
            oldest_unfinished_at=oldest_unfinished_at,
            run_status_counts=run_status_counts,
            stale_running_runs=stale_running_runs,
            latest_successful_run_id=latest_successful_run_id,
            latest_successful_run_at=latest_successful_run_at,
        )

    def _workspace_lease_held_error(
        self,
        *,
        name: str,
        requested_run_id: str | None,
    ) -> WorkspaceLeaseHeldError:
        lease = self.get_workspace_lease(name=name)
        return WorkspaceLeaseHeldError(
            lease_name=name,
            holder_run_id=(lease.run_id if lease is not None else None),
            holder_command=(lease.command if lease is not None else None),
            holder_hostname=(lease.hostname if lease is not None else None),
            holder_pid=(lease.pid if lease is not None else None),
            expires_at=(lease.expires_at if lease is not None else None),
            requested_run_id=requested_run_id,
        )

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        metric = Metric(run_id=run_id, name=name, value=value, unit=unit)
        with Session(self.engine) as session:
            session.add(metric)
            self._commit(session)

    def list_metrics(self, *, run_id: str) -> list[Metric]:
        with Session(self.engine) as session:
            statement = (
                select(Metric)
                .where(Metric.run_id == run_id)
                .order_by(cast(Any, Metric.id))
            )
            return list(session.exec(statement))

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def _find_near_duplicate_by_title(
        self, session: Session, *, title: str
    ) -> tuple[Item, float] | None:
        normalized_title = title.strip()
        if not normalized_title:
            return None
        if self.title_dedup_max_candidates <= 0:
            return None

        statement = (
            select(Item)
            .order_by(desc(cast(Any, Item.created_at)))
            .limit(self.title_dedup_max_candidates)
        )
        candidates = list(session.exec(statement))
        best_item: Item | None = None
        best_score = -1.0
        for candidate in candidates:
            score = float(fuzz.token_set_ratio(normalized_title, candidate.title))
            if score > best_score:
                best_score = score
                best_item = candidate
                if best_score >= 100.0:
                    return candidate, best_score
        if best_item is None:
            return None
        if best_score < self.title_dedup_threshold:
            return None
        return best_item, best_score

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing: Item | None = None
            matched_by_title = False
            title_dedup_score: float | None = None
            if draft.source_item_id:
                statement = select(Item).where(
                    Item.source == draft.source,
                    Item.source_item_id == draft.source_item_id,
                )
                existing = session.exec(statement).first()

            if existing is None:
                by_url_hash = select(Item).where(
                    Item.canonical_url_hash == draft.canonical_url_hash
                )
                existing = session.exec(by_url_hash).first()

            if existing is None and self.title_dedup_threshold > 0:
                match = self._find_near_duplicate_by_title(session, title=draft.title)
                if match is not None:
                    existing, title_dedup_score = match
                    matched_by_title = True

            if existing is None:
                created = Item(
                    source=draft.source,
                    source_item_id=draft.source_item_id,
                    canonical_url=draft.canonical_url,
                    canonical_url_hash=draft.canonical_url_hash,
                    title=draft.title,
                    authors=_to_json(draft.authors),
                    published_at=draft.published_at,
                    raw_metadata_json=_to_json(draft.raw_metadata),
                    state=ITEM_STATE_INGESTED,
                )
                session.add(created)
                self._commit(session)
                session.refresh(created)
                return created, True

            previous_state = existing.state
            if matched_by_title:
                current_metadata = _from_json_object(existing.raw_metadata_json)
                alternate_urls = current_metadata.get("alternate_urls")
                if not isinstance(alternate_urls, list):
                    alternate_urls = []
                if (
                    draft.canonical_url != existing.canonical_url
                    and draft.canonical_url not in alternate_urls
                ):
                    alternate_urls.append(draft.canonical_url)
                current_metadata["alternate_urls"] = alternate_urls

                dedup_events = current_metadata.get("dedup_events")
                if not isinstance(dedup_events, list):
                    dedup_events = []
                dedup_events.append(
                    {
                        "source": draft.source,
                        "source_item_id": draft.source_item_id,
                        "canonical_url_hash": draft.canonical_url_hash,
                        "title_similarity": round(float(title_dedup_score or 0.0), 2),
                    }
                )
                current_metadata["dedup_events"] = dedup_events[-20:]
                existing.raw_metadata_json = _to_json(current_metadata)
                if existing.published_at is None and draft.published_at is not None:
                    existing.published_at = draft.published_at
            else:
                existing.canonical_url = draft.canonical_url
                existing.canonical_url_hash = draft.canonical_url_hash
                existing.title = draft.title
                existing.authors = _to_json(draft.authors)
                existing.published_at = draft.published_at
                existing.raw_metadata_json = _to_json(draft.raw_metadata)
            if previous_state in {ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED}:
                # Allow failed items to be retried by re-ingesting.
                existing.state = ITEM_STATE_INGESTED
            existing.updated_at = utc_now()
            if (
                (not matched_by_title)
                and existing.source == draft.source
                and existing.source_item_id is None
                and draft.source_item_id is not None
            ):
                existing.source_item_id = draft.source_item_id
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing, False

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(
                    cast(Any, Item.state).in_(
                        [
                            ITEM_STATE_INGESTED,
                            ITEM_STATE_ENRICHED,
                            ITEM_STATE_RETRYABLE_FAILED,
                        ]
                    )
                )
                .order_by(
                    desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at))
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def list_items_for_llm_analysis(
        self, *, limit: int, triage_required: bool
    ) -> list[Item]:
        states = [ITEM_STATE_RETRYABLE_FAILED]
        if triage_required:
            states.append(ITEM_STATE_TRIAGED)
        else:
            states.append(ITEM_STATE_ENRICHED)

        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(cast(Any, Item.state).in_(states))
                .order_by(
                    desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at))
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(Content.item_id == item_id, Content.content_type == content_type)
                .order_by(desc(cast(Any, Content.id)))
            )
            return session.exec(statement).first()

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]:
        """Fetch latest text for multiple content_types of a single item in one query."""

        normalized_item_id = int(item_id)
        types = [str(t or "").strip() for t in (content_types or [])]
        types = [t for t in types if t]
        if normalized_item_id <= 0 or not types:
            return {}

        wanted = set(types)
        out: dict[str, str | None] = {t: None for t in types}
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(
                    Content.item_id == normalized_item_id,
                    cast(Any, Content.content_type).in_(types),
                )
                .order_by(desc(cast(Any, Content.id)))
            )
            for content in session.exec(statement):
                ctype = str(getattr(content, "content_type", "") or "").strip()
                if ctype in wanted and out.get(ctype) is None:
                    text = getattr(content, "text", None)
                    out[ctype] = (
                        text if isinstance(text, str) and text.strip() else None
                    )
                    wanted.discard(ctype)
                    if not wanted:
                        break
        return out

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]:
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw_item_id in item_ids:
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0 or item_id in seen:
                continue
            seen.add(item_id)
            normalized_ids.append(item_id)
        normalized_type = str(content_type or "").strip()
        if not normalized_ids or not normalized_type:
            return {}

        with Session(self.engine) as session:
            latest_ids = (
                select(
                    cast(Any, Content.item_id),
                    func.max(cast(Any, Content.id)).label("max_id"),
                )
                .where(
                    cast(Any, Content.item_id).in_(normalized_ids),
                    Content.content_type == normalized_type,
                )
                .group_by(cast(Any, Content.item_id))
                .subquery()
            )
            statement = select(Content).join(
                latest_ids, cast(Any, Content.id) == latest_ids.c.max_id
            )
            contents = list(session.exec(statement))
            return {content.item_id: content for content in contents}

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int:
        """Upsert multiple text contents for a single item with one commit."""

        normalized_item_id = int(item_id)
        if normalized_item_id <= 0:
            raise ValueError("item_id must be > 0")
        if not isinstance(texts_by_type, dict) or not texts_by_type:
            return 0

        normalized: dict[str, str] = {}
        for raw_type, raw_text in texts_by_type.items():
            content_type = str(raw_type or "").strip()
            if not content_type:
                continue
            if not isinstance(raw_text, str):
                continue
            text = raw_text.strip()
            if not text:
                continue
            normalized[content_type] = text
        if not normalized:
            return 0

        hashes_by_type: dict[str, str] = {
            ctype: sha256_hex(text) for ctype, text in normalized.items()
        }
        target_types = list(hashes_by_type.keys())
        target_hashes = list(set(hashes_by_type.values()))

        inserted = 0
        with Session(self.engine) as session:
            existing_pairs: set[tuple[str, str]] = set()
            statement = select(Content.content_type, Content.content_hash).where(
                Content.item_id == normalized_item_id,
                cast(Any, Content.content_type).in_(target_types),
                cast(Any, Content.content_hash).in_(target_hashes),
            )
            for ctype, chash in session.exec(statement):
                existing_pairs.add((str(ctype), str(chash)))

            for ctype, text in normalized.items():
                chash = hashes_by_type[ctype]
                if (ctype, chash) in existing_pairs:
                    continue
                session.add(
                    Content(
                        item_id=normalized_item_id,
                        content_type=ctype,
                        text=text,
                        artifact_path=None,
                        content_hash=chash,
                    )
                )
                inserted += 1

            if inserted > 0:
                self._commit(session)
        return inserted

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content:
        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]:
        """Upsert a single content row and report whether it inserted a new record."""

        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing, False

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content, True

    def _upsert_item_stream_state(
        self,
        *,
        session: Session,
        item_id: int,
        stream: str,
        state: str,
    ) -> ItemStreamState:
        existing = session.exec(
            select(ItemStreamState).where(
                ItemStreamState.item_id == item_id,
                ItemStreamState.stream == stream,
            )
        ).first()
        now = utc_now()
        if existing is None:
            existing = ItemStreamState(
                item_id=item_id,
                stream=stream,
                state=state,
                created_at=now,
                updated_at=now,
            )
        else:
            existing.state = state
            existing.updated_at = now
        session.add(existing)
        return existing

    def list_items_for_stream_analysis(
        self,
        *,
        stream: str,
        limit: int,
        selected_only: bool = False,
    ) -> list[Item]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .outerjoin(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == stream,
                    ),
                )
                .where(
                    cast(Any, Item.state).in_(
                        [ITEM_STATE_ENRICHED, ITEM_STATE_RETRYABLE_FAILED]
                    )
                )
                .order_by(
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
                .limit(limit)
            )
            if selected_only:
                statement = statement.where(
                    cast(Any, stream_state.state).in_(
                        [ITEM_STATE_TRIAGED, ITEM_STATE_RETRYABLE_FAILED]
                    )
                )
            else:
                statement = statement.where(
                    or_(
                        cast(Any, stream_state.id).is_(None),
                        cast(Any, stream_state.state) == ITEM_STATE_RETRYABLE_FAILED,
                    )
                )
            return list(session.exec(statement))

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        scope: str = DEFAULT_TOPIC_STREAM,
        mirror_item_state: bool = True,
    ) -> Analysis:
        with Session(self.engine) as session:
            analysis = session.exec(
                select(Analysis).where(
                    Analysis.item_id == item_id,
                    Analysis.scope == scope,
                )
            ).first()
            if analysis is None:
                analysis = Analysis(
                    item_id=item_id,
                    scope=scope,
                    model=result.model,
                    provider=result.provider,
                    summary=result.summary,
                    topics_json=_to_json(result.topics),
                    relevance_score=result.relevance_score,
                    novelty_score=result.novelty_score,
                    cost_usd=result.cost_usd,
                    latency_ms=result.latency_ms,
                )
            else:
                analysis.model = result.model
                analysis.provider = result.provider
                analysis.summary = result.summary
                analysis.topics_json = _to_json(result.topics)
                analysis.relevance_score = result.relevance_score
                analysis.novelty_score = result.novelty_score
                analysis.cost_usd = result.cost_usd
                analysis.latency_ms = result.latency_ms

            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=scope,
                state=ITEM_STATE_ANALYZED,
            )
            if mirror_item_state:
                item = session.get(Item, item_id)
                if item is not None:
                    item.state = ITEM_STATE_ANALYZED
                    item.updated_at = utc_now()
                    session.add(item)

            session.add(analysis)
            self._commit(session)
            session.refresh(analysis)
            return analysis

    def mark_item_enriched(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_ENRICHED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_triaged(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_TRIAGED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_stream_state(
        self,
        *,
        item_id: int,
        stream: str,
        state: str,
        mirror_item_state: bool = False,
    ) -> None:
        with Session(self.engine) as session:
            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=stream,
                state=state,
            )
            if mirror_item_state:
                item = session.get(Item, item_id)
                if item is not None:
                    item.state = state
                    item.updated_at = utc_now()
                    session.add(item)
            self._commit(session)

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_RETRYABLE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> list[tuple[Item, Analysis]]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .join(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == scope,
                    ),
                )
                .where(
                    cast(Any, Analysis.scope) == scope,
                    cast(Any, stream_state.state) == ITEM_STATE_ANALYZED,
                    cast(Any, Analysis.relevance_score) >= min_relevance_score,
                )
                .order_by(
                    desc(cast(Any, Analysis.relevance_score)),
                    desc(cast(Any, Analysis.novelty_score)),
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool:
        with Session(self.engine) as session:
            statement = select(Delivery).where(
                Delivery.item_id == item_id,
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def count_sent_deliveries_since(
        self, *, channel: str, destination: str, since: datetime
    ) -> int:
        with Session(self.engine) as session:
            item_statement = select(func.count(cast(Any, Delivery.id))).where(
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
                cast(Any, Delivery.sent_at).is_not(None),
                cast(Any, Delivery.sent_at) >= since,
            )
            trend_statement = select(func.count(cast(Any, TrendDelivery.id))).where(
                TrendDelivery.channel == channel,
                TrendDelivery.destination == destination,
                TrendDelivery.status == DELIVERY_STATUS_SENT,
                cast(Any, TrendDelivery.sent_at).is_not(None),
                cast(Any, TrendDelivery.sent_at) >= since,
            )
            return int(session.exec(item_statement).one()) + int(
                session.exec(trend_statement).one()
            )

    def upsert_delivery(
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> Delivery:
        now = utc_now()
        with Session(self.engine) as session:
            existing = session.exec(
                select(Delivery).where(
                    Delivery.item_id == item_id,
                    Delivery.channel == channel,
                    Delivery.destination == destination,
                )
            ).first()
            if existing is None:
                delivery = Delivery(
                    item_id=item_id,
                    channel=channel,
                    destination=destination,
                    message_id=message_id,
                    status=status,
                    error=error,
                    sent_at=now if status == DELIVERY_STATUS_SENT else None,
                )
                session.add(delivery)
                self._commit(session)
                session.refresh(delivery)
                return delivery

            existing.message_id = message_id
            existing.status = status
            existing.error = error
            if status == DELIVERY_STATUS_SENT:
                existing.sent_at = now
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def has_sent_trend_delivery(
        self,
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
    ) -> bool:
        with Session(self.engine) as session:
            statement = select(TrendDelivery).where(
                TrendDelivery.doc_id == doc_id,
                TrendDelivery.channel == channel,
                TrendDelivery.destination == destination,
                TrendDelivery.content_hash == content_hash,
                TrendDelivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def upsert_trend_delivery(
        self,
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> TrendDelivery:
        now = utc_now()
        with Session(self.engine) as session:
            existing = session.exec(
                select(TrendDelivery).where(
                    TrendDelivery.doc_id == doc_id,
                    TrendDelivery.channel == channel,
                    TrendDelivery.destination == destination,
                )
            ).first()
            if existing is None:
                delivery = TrendDelivery(
                    doc_id=doc_id,
                    channel=channel,
                    destination=destination,
                    content_hash=content_hash,
                    message_id=message_id,
                    status=status,
                    error=error,
                    sent_at=now if status == DELIVERY_STATUS_SENT else None,
                )
                session.add(delivery)
                self._commit(session)
                session.refresh(delivery)
                return delivery

            existing.content_hash = content_hash
            existing.message_id = message_id
            existing.status = status
            existing.error = error
            existing.sent_at = now if status == DELIVERY_STATUS_SENT else None
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def mark_item_published(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_PUBLISHED
            item.updated_at = utc_now()
            session.add(item)
            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=DEFAULT_TOPIC_STREAM,
                state=ITEM_STATE_PUBLISHED,
            )
            self._commit(session)

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> list[tuple[Item, Analysis]]:
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .join(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == scope,
                    ),
                )
                .where(
                    cast(Any, Analysis.scope) == scope,
                    cast(Any, stream_state.state).in_(
                        [ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]
                    ),
                    event_at >= period_start,
                    event_at < period_end,
                )
                .order_by(desc(cast(Any, event_at)), desc(cast(Any, Item.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

    def upsert_document_for_item(
        self, *, item: Item, scope: str = DEFAULT_TOPIC_STREAM
    ) -> Document:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item must have an id")
        item_id = int(raw_item_id)
        if item_id <= 0:
            raise ValueError("item_id must be > 0")
        event_at = item.published_at or item.created_at
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    Document.item_id == item_id,
                    cast(Any, Document.scope) == scope,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="item",
                    scope=scope,
                    item_id=item_id,
                    source=str(getattr(item, "source", "") or "").strip() or None,
                    canonical_url=str(getattr(item, "canonical_url", "") or "").strip()
                    or None,
                    title=str(getattr(item, "title", "") or "").strip() or None,
                    published_at=event_at,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.source = str(getattr(item, "source", "") or "").strip() or None
            existing.canonical_url = (
                str(getattr(item, "canonical_url", "") or "").strip() or None
            )
            existing.title = str(getattr(item, "title", "") or "").strip() or None
            existing.published_at = event_at
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> Document:
        normalized_granularity = str(granularity or "").strip().lower()
        if normalized_granularity not in {"day", "week", "month"}:
            raise ValueError("unsupported granularity")
        normalized_title = str(title or "").strip() or "Trend"
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == "trend",
                    cast(Any, Document.scope) == scope,
                    Document.granularity == normalized_granularity,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="trend",
                    scope=scope,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    title=normalized_title,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.title = normalized_title
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def upsert_document_chunk(
        self,
        *,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
        start_char: int | None = None,
        end_char: int | None = None,
        source_content_type: str | None = None,
    ) -> tuple[DocumentChunk, bool]:
        normalized_doc_id = int(doc_id)
        if normalized_doc_id <= 0:
            raise ValueError("doc_id must be > 0")
        normalized_index = int(chunk_index)
        if normalized_index < 0:
            raise ValueError("chunk_index must be >= 0")
        normalized_kind = str(kind or "").strip().lower()
        if normalized_kind not in {"summary", "content", "meta"}:
            raise ValueError("unsupported chunk kind")
        normalized_text = str(text_value or "").strip()
        if not normalized_text:
            raise ValueError("chunk text must not be empty")
        text_hash = sha256_hex(normalized_text)

        inserted = False
        with Session(self.engine) as session:
            existing = session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == normalized_doc_id,
                    DocumentChunk.chunk_index == normalized_index,
                )
            ).first()
            if existing is None:
                chunk = DocumentChunk(
                    doc_id=normalized_doc_id,
                    chunk_index=normalized_index,
                    kind=normalized_kind,
                    text=normalized_text,
                    start_char=start_char,
                    end_char=end_char,
                    text_hash=text_hash,
                    source_content_type=(
                        str(source_content_type).strip()
                        if isinstance(source_content_type, str)
                        and str(source_content_type).strip()
                        else None
                    ),
                )
                session.add(chunk)
                self._commit(session)
                session.refresh(chunk)
                inserted = True
            else:
                if str(getattr(existing, "text_hash", "") or "") == text_hash:
                    return existing, False
                existing.kind = normalized_kind
                existing.text = normalized_text
                existing.start_char = start_char
                existing.end_char = end_char
                existing.text_hash = text_hash
                existing.source_content_type = (
                    str(source_content_type).strip()
                    if isinstance(source_content_type, str)
                    and str(source_content_type).strip()
                    else None
                )
                session.add(existing)
                self._commit(session)
                session.refresh(existing)
                chunk = existing

        chunk_id = getattr(chunk, "id", None)
        if chunk_id is not None:
            self._sync_chunk_fts(
                chunk_id=int(chunk_id),
                doc_id=normalized_doc_id,
                chunk_index=normalized_index,
                kind=normalized_kind,
                text_value=normalized_text,
            )
        return chunk, inserted

    def delete_document_chunks(
        self,
        *,
        doc_id: int,
        kind: str | None = None,
        chunk_index_gte: int | None = None,
    ) -> int:
        normalized_doc_id = int(doc_id)
        if normalized_doc_id <= 0:
            raise ValueError("doc_id must be > 0")

        normalized_kind: str | None = None
        if kind is not None:
            candidate = str(kind or "").strip().lower()
            if not candidate:
                normalized_kind = None
            elif candidate not in {"summary", "content", "meta"}:
                raise ValueError("unsupported chunk kind")
            else:
                normalized_kind = candidate

        normalized_index_gte: int | None = None
        if chunk_index_gte is not None:
            normalized_index_gte = int(chunk_index_gte)
            if normalized_index_gte < 0:
                raise ValueError("chunk_index_gte must be >= 0")

        with Session(self.engine) as session:
            statement = select(DocumentChunk).where(
                DocumentChunk.doc_id == normalized_doc_id
            )
            if normalized_kind is not None:
                statement = statement.where(DocumentChunk.kind == normalized_kind)
            if normalized_index_gte is not None:
                statement = statement.where(
                    DocumentChunk.chunk_index >= normalized_index_gte
                )
            rows = list(session.exec(statement))
            if not rows:
                return 0

            chunk_ids: list[int] = []
            for row in rows:
                raw_id = getattr(row, "id", None)
                if raw_id is None:
                    continue
                try:
                    cid = int(raw_id)
                except Exception:
                    continue
                if cid > 0:
                    chunk_ids.append(cid)

            if chunk_ids:
                with self.engine.begin() as conn:
                    for cid in chunk_ids:
                        conn.execute(
                            text(
                                "DELETE FROM chunk_embeddings WHERE chunk_id = :chunk_id"
                            ),
                            {"chunk_id": cid},
                        )
                        conn.execute(
                            text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                            {"rowid": cid},
                        )

            for row in rows:
                session.delete(row)
            self._commit(session)
            return len(rows)

    def _sync_chunk_fts(
        self,
        *,
        chunk_id: int,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
    ) -> None:
        normalized_chunk_id = int(chunk_id)
        normalized_doc_id = int(doc_id)
        if normalized_chunk_id <= 0 or normalized_doc_id <= 0:
            return
        payload = {
            "rowid": normalized_chunk_id,
            "text": str(text_value),
            "doc_id": normalized_doc_id,
            "chunk_index": int(chunk_index),
            "kind": str(kind),
        }
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                {"rowid": normalized_chunk_id},
            )
            conn.execute(
                text(
                    "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
                    "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
                ),
                payload,
            )

    def list_documents(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        scope: str = DEFAULT_TOPIC_STREAM,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = select(Document).where(
                Document.doc_type == normalized_type,
                cast(Any, Document.scope) == scope,
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.published_at), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.published_at)),
                        desc(cast(Any, Document.id)),
                    )
            elif normalized_type == "trend":
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    # Overlap predicate: include trends intersecting the window.
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
                )
                normalized_granularity = (
                    str(granularity or "").strip().lower()
                    if granularity is not None
                    else ""
                )
                if normalized_granularity:
                    statement = statement.where(
                        Document.granularity == normalized_granularity
                    )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.period_start), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.period_start)),
                        desc(cast(Any, Document.id)),
                    )
            else:
                raise ValueError("unsupported doc_type")
            statement = statement.offset(normalized_offset).limit(normalized_limit)
            return list(session.exec(statement))

    def get_document(self, *, doc_id: int) -> Document | None:
        normalized_id = int(doc_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(Document, normalized_id)

    def get_item(self, *, item_id: int) -> Item | None:
        normalized_id = int(item_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(Item, normalized_id)

    def read_document_chunk(
        self, *, doc_id: int, chunk_index: int
    ) -> DocumentChunk | None:
        normalized_doc_id = int(doc_id)
        normalized_index = int(chunk_index)
        if normalized_doc_id <= 0 or normalized_index < 0:
            return None
        with Session(self.engine) as session:
            statement = select(DocumentChunk).where(
                DocumentChunk.doc_id == normalized_doc_id,
                DocumentChunk.chunk_index == normalized_index,
            )
            return session.exec(statement).first()

    def search_chunks_text(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        scope: str = DEFAULT_TOPIC_STREAM,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        normalized_query = str(query or "").strip()
        if not normalized_query:
            return []
        fts_query = _to_fts5_query(normalized_query)
        if not fts_query:
            return []
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(1, min(int(limit), 50))

        if normalized_type == "item":
            period_pred = (
                "d.published_at >= :period_start AND d.published_at < :period_end"
            )
        elif normalized_type == "trend":
            period_pred = (
                "d.period_start < :period_end AND d.period_end > :period_start"
            )
        else:
            raise ValueError("unsupported doc_type")

        extra_predicates: list[str] = []
        params = {
            "query": fts_query,
            "doc_type": normalized_type,
            "scope": scope,
            "period_start": period_start,
            "period_end": period_end,
            "limit": normalized_limit,
        }
        if normalized_type == "trend":
            normalized_granularity = (
                str(granularity or "").strip().lower() if granularity is not None else ""
            )
            if normalized_granularity:
                extra_predicates.append("d.granularity = :granularity")
                params["granularity"] = normalized_granularity

        sql = f"""
        SELECT
            dc.id AS chunk_id,
            dc.doc_id AS doc_id,
            dc.chunk_index AS chunk_index,
            dc.kind AS kind,
            snippet(chunk_fts, 0, '[', ']', '…', 12) AS snippet,
            bm25(chunk_fts) AS rank
        FROM chunk_fts
        JOIN document_chunks dc ON dc.id = chunk_fts.rowid
        JOIN documents d ON d.id = dc.doc_id
        WHERE
            chunk_fts MATCH :query
            AND d.doc_type = :doc_type
            AND d.scope = :scope
            AND {period_pred}
            {"AND " + " AND ".join(extra_predicates) if extra_predicates else ""}
        ORDER BY rank ASC
        LIMIT :limit
        """
        with self.engine.begin() as conn:
            rows = conn.execute(text(sql), params).mappings().all()
        out: list[dict[str, Any]] = []
        for row in rows:
            raw_chunk_id = row.get("chunk_id")
            raw_doc_id = row.get("doc_id")
            raw_chunk_index = row.get("chunk_index")
            if raw_chunk_id is None or raw_doc_id is None or raw_chunk_index is None:
                continue
            try:
                chunk_id = int(raw_chunk_id)
                doc_id = int(raw_doc_id)
                chunk_index = int(raw_chunk_index)
            except Exception:
                continue
            if chunk_id <= 0 or doc_id <= 0 or chunk_index < 0:
                continue
            out.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_index": chunk_index,
                    "kind": str(row.get("kind") or ""),
                    "snippet": str(row.get("snippet") or ""),
                    "rank": float(row.get("rank") or 0.0),
                }
            )
        return out

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        scope: str = DEFAULT_TOPIC_STREAM,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = (
                select(DocumentChunk)
                .join(
                    Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id)
                )
                .where(
                    Document.doc_type == normalized_type,
                    cast(Any, Document.scope) == scope,
                    DocumentChunk.kind == "summary",
                )
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
            elif normalized_type == "trend":
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
                )
            else:
                raise ValueError("unsupported doc_type")

            statement = (
                statement.order_by(desc(cast(Any, DocumentChunk.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

    def list_summary_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        scope: str = DEFAULT_TOPIC_STREAM,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        """Return summary chunk rows with document time window metadata for vector sync."""

        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = (
                select(DocumentChunk, Document)
                .join(
                    Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id)
                )
                .where(
                    Document.doc_type == normalized_type,
                    cast(Any, Document.scope) == scope,
                    DocumentChunk.kind == "summary",
                )
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
                statement = statement.order_by(desc(cast(Any, DocumentChunk.id)))
            elif normalized_type == "trend":
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) < period_end,
                    cast(Any, Document.period_end) > period_start,
                )
                normalized_granularity = (
                    str(granularity or "").strip().lower()
                    if granularity is not None
                    else ""
                )
                if normalized_granularity:
                    statement = statement.where(
                        Document.granularity == normalized_granularity
                    )
                statement = statement.order_by(desc(cast(Any, DocumentChunk.id)))
            else:
                raise ValueError("unsupported doc_type")

            statement = statement.offset(normalized_offset).limit(normalized_limit)
            rows = list(session.exec(statement))

        out: list[dict[str, Any]] = []
        for chunk, doc in rows:
            chunk_id = getattr(chunk, "id", None)
            doc_id = getattr(doc, "id", None)
            if chunk_id is None or doc_id is None:
                continue
            if normalized_type == "item":
                published_at = getattr(doc, "published_at", None)
                if not isinstance(published_at, datetime):
                    continue
                if published_at.tzinfo is None:
                    published_at = published_at.replace(tzinfo=UTC)
                event_start_ts = float(published_at.timestamp())
                event_end_ts = float(published_at.timestamp())
            else:
                dstart = getattr(doc, "period_start", None)
                dend = getattr(doc, "period_end", None)
                if not isinstance(dstart, datetime) or not isinstance(dend, datetime):
                    continue
                if dstart.tzinfo is None:
                    dstart = dstart.replace(tzinfo=UTC)
                if dend.tzinfo is None:
                    dend = dend.replace(tzinfo=UTC)
                event_start_ts = float(dstart.timestamp())
                event_end_ts = float(dend.timestamp())

            text_value = str(getattr(chunk, "text", "") or "")
            preview = text_value[:240] + ("..." if len(text_value) > 240 else "")
            out.append(
                {
                    "chunk_id": int(chunk_id),
                    "doc_id": int(doc_id),
                    "doc_type": normalized_type,
                    "granularity": str(getattr(doc, "granularity", "") or "") or None,
                    "chunk_index": int(getattr(chunk, "chunk_index")),
                    "kind": str(getattr(chunk, "kind") or ""),
                    "text": text_value,
                    "text_hash": str(getattr(chunk, "text_hash") or ""),
                    "text_preview": preview,
                    "event_start_ts": event_start_ts,
                    "event_end_ts": event_end_ts,
                }
            )
        return out

    def get_chunk_embedding(
        self, *, chunk_id: int, model: str
    ) -> ChunkEmbedding | None:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        if normalized_chunk_id <= 0 or not normalized_model:
            return None
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.chunk_id == normalized_chunk_id,
                ChunkEmbedding.model == normalized_model,
            )
            return session.exec(statement).first()

    def list_chunk_embeddings(
        self, *, chunk_ids: list[int], model: str
    ) -> dict[int, ChunkEmbedding]:
        normalized_model = str(model or "").strip()
        if not normalized_model:
            return {}
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw in chunk_ids or []:
            try:
                cid = int(raw)
            except Exception:
                continue
            if cid <= 0 or cid in seen:
                continue
            seen.add(cid)
            normalized_ids.append(cid)
        if not normalized_ids:
            return {}
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.model == normalized_model,
                cast(Any, ChunkEmbedding.chunk_id).in_(normalized_ids),
            )
            rows = list(session.exec(statement))
            return {int(row.chunk_id): row for row in rows}

    def upsert_chunk_embedding(
        self,
        *,
        chunk_id: int,
        model: str,
        dimensions: int | None,
        text_hash: str,
        vector: list[float],
    ) -> ChunkEmbedding:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        normalized_text_hash = str(text_hash or "").strip()
        if normalized_chunk_id <= 0:
            raise ValueError("chunk_id must be > 0")
        if not normalized_model:
            raise ValueError("model must not be empty")
        if not normalized_text_hash:
            raise ValueError("text_hash must not be empty")
        if not isinstance(vector, list) or not vector:
            raise ValueError("vector must be a non-empty list")
        normalized_dims = int(dimensions) if dimensions is not None else None
        if normalized_dims is not None and normalized_dims <= 0:
            raise ValueError("dimensions must be positive")
        normalized_vector = [float(v) for v in vector]
        vector_json = _to_json(normalized_vector)

        with Session(self.engine) as session:
            existing = session.exec(
                select(ChunkEmbedding).where(
                    ChunkEmbedding.chunk_id == normalized_chunk_id,
                    ChunkEmbedding.model == normalized_model,
                )
            ).first()
            if existing is None:
                row = ChunkEmbedding(
                    chunk_id=normalized_chunk_id,
                    model=normalized_model,
                    dimensions=normalized_dims,
                    vector_json=vector_json,
                    text_hash=normalized_text_hash,
                )
                session.add(row)
                self._commit(session)
                session.refresh(row)
                return row

            if (
                str(getattr(existing, "text_hash", "") or "") == normalized_text_hash
                and str(getattr(existing, "vector_json", "") or "") == vector_json
            ):
                return existing
            existing.dimensions = normalized_dims
            existing.vector_json = vector_json
            existing.text_hash = normalized_text_hash
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

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

        schema_version = int(manifest.get("schema_version") or 0)
        if schema_version > CURRENT_SCHEMA_VERSION:
            raise SchemaVersionError(
                "Backup bundle uses newer schema version "
                f"{schema_version}; current supported version is {CURRENT_SCHEMA_VERSION}."
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
            schema_version=schema_version,
        )

    @staticmethod
    def decode_list(value: str | None) -> list[str]:
        return _from_json_list(value)
