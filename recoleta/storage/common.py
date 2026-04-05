from __future__ import annotations

from dataclasses import dataclass
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


CURRENT_SCHEMA_VERSION = 8
WORKSPACE_LEASE_NAME = "workspace"


class SchemaVersionError(RuntimeError):
    """Raised when the on-disk schema is incompatible with this binary."""


class WorkspaceLeaseError(RuntimeError):
    """Raised when workspace lease operations fail."""


@dataclass(frozen=True, slots=True)
class WorkspaceLeaseHeldDetails:
    lease_name: str
    holder_run_id: str | None
    holder_command: str | None
    holder_hostname: str | None
    holder_pid: int | None
    expires_at: datetime | None
    requested_run_id: str | None


def _coerce_workspace_lease_held_details(
    *,
    details: WorkspaceLeaseHeldDetails | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> WorkspaceLeaseHeldDetails:
    if details is not None:
        return details
    values = dict(legacy_kwargs or {})
    return WorkspaceLeaseHeldDetails(
        lease_name=str(values["lease_name"]),
        holder_run_id=values.get("holder_run_id"),
        holder_command=values.get("holder_command"),
        holder_hostname=values.get("holder_hostname"),
        holder_pid=values.get("holder_pid"),
        expires_at=values.get("expires_at"),
        requested_run_id=values.get("requested_run_id"),
    )


def _workspace_lease_held_message(details: WorkspaceLeaseHeldDetails) -> str:
    expires_text = (
        details.expires_at.isoformat()
        if isinstance(details.expires_at, datetime)
        else ""
    )
    message_parts = (
        f"lease={details.lease_name}",
        f"holder_run_id={details.holder_run_id}" if details.holder_run_id else "",
        f"holder_command={details.holder_command}" if details.holder_command else "",
        f"holder_hostname={details.holder_hostname}" if details.holder_hostname else "",
        f"holder_pid={details.holder_pid}" if details.holder_pid is not None else "",
        f"expires_at={expires_text}" if expires_text else "",
    )
    detail_text = " ".join(part for part in message_parts if part)
    return f"workspace lease is held {detail_text}".strip()


class WorkspaceLeaseHeldError(WorkspaceLeaseError):
    def __init__(
        self,
        details: WorkspaceLeaseHeldDetails | None = None,
        **legacy_kwargs: Any,
    ) -> None:
        resolved = _coerce_workspace_lease_held_details(
            details=details,
            legacy_kwargs=legacy_kwargs,
        )
        self.lease_name = resolved.lease_name
        self.holder_run_id = resolved.holder_run_id
        self.holder_command = resolved.holder_command
        self.holder_hostname = resolved.holder_hostname
        self.holder_pid = resolved.holder_pid
        self.expires_at = resolved.expires_at
        self.requested_run_id = resolved.requested_run_id
        super().__init__(_workspace_lease_held_message(resolved))


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
