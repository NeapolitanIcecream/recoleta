from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import quote

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
from recoleta.storage.localized_outputs import LocalizedOutputStoreMixin
from recoleta.storage.maintenance import MaintenanceStoreMixin
from recoleta.storage.pass_outputs import PassOutputStoreMixin
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
    PassOutputStoreMixin,
    LocalizedOutputStoreMixin,
    MaintenanceStoreMixin,
):
    def __init__(
        self,
        *,
        db_path: Path,
        title_dedup_threshold: float = 92.0,
        title_dedup_max_candidates: int = 500,
        read_only: bool = False,
    ) -> None:
        self.db_path = db_path
        self.read_only = bool(read_only)
        if self.read_only:
            resolved_path = self.db_path.expanduser().resolve()
            encoded_path = quote(resolved_path.as_posix(), safe="/:")
            database_url = (
                f"sqlite:///file:{encoded_path}?mode=ro&uri=true"
            )
        else:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            database_url = f"sqlite:///{self.db_path}"
        self.engine = create_engine(
            database_url,
            echo=False,
            connect_args={"check_same_thread": False, "timeout": 30},
        )
        self.title_dedup_threshold = float(title_dedup_threshold)
        self.title_dedup_max_candidates = max(0, int(title_dedup_max_candidates))
        self._sql_diag_lock = Lock()
        self._sql_diag_active: list[SqlDiagnostics] = []
        self._sql_diag_installed = False

    def _ensure_sql_diagnostics_installed(self) -> None:
        if self._sql_diag_installed:
            return

        def _before_cursor_execute(*_: Any, **__: Any) -> None:
            with self._sql_diag_lock:
                for active in self._sql_diag_active:
                    active.queries_total += 1

        event.listen(self.engine, "before_cursor_execute", _before_cursor_execute)
        self._sql_diag_installed = True

    @contextmanager
    def sql_diagnostics(self) -> Any:
        """Collect coarse SQL diagnostics for a single run (aggregate counts only)."""

        self._ensure_sql_diagnostics_installed()
        diag = SqlDiagnostics()
        with self._sql_diag_lock:
            self._sql_diag_active.append(diag)
        try:
            yield diag
        finally:
            with self._sql_diag_lock:
                if self._sql_diag_active and self._sql_diag_active[-1] is diag:
                    self._sql_diag_active.pop()
                elif diag in self._sql_diag_active:
                    self._sql_diag_active.remove(diag)

    def _commit(self, session: Session) -> None:
        with self._sql_diag_lock:
            for active in self._sql_diag_active:
                active.commits_total += 1
        session.commit()
