from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from typing import Any

from sqlalchemy import event
from sqlmodel import Session, create_engine

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
)
from recoleta.storage.analyses import AnalysisStoreMixin
from recoleta.storage.documents import DocumentStoreMixin
from recoleta.storage.deliveries import DeliveryStoreMixin
from recoleta.storage.items import ItemStoreMixin
from recoleta.storage.maintenance import MaintenanceStoreMixin
from recoleta.storage.runtime import RuntimeStoreMixin
from recoleta.storage.schema import SchemaStoreMixin

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


class Repository(
    SchemaStoreMixin,
    RuntimeStoreMixin,
    ItemStoreMixin,
    AnalysisStoreMixin,
    DeliveryStoreMixin,
    DocumentStoreMixin,
    MaintenanceStoreMixin,
):
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
