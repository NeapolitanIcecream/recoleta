from __future__ import annotations

from dataclasses import dataclass
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


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
