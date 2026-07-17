from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import json
import sqlite3
import shutil
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import and_, desc, func, text
from sqlmodel import Session, select

from recoleta.models import (
    Analysis,
    Artifact,
    Document,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_PUBLISHED,
    Item,
    Metric,
    PassOutput,
    Run,
    RUN_STATUS_FAILED,
    RUN_STATUS_SUCCEEDED,
    WorkflowStepReceipt,
)
from recoleta.storage.common import (
    CURRENT_SCHEMA_VERSION,
    ArtifactPruneResult,
    ChunkCachePruneResult,
    DatabaseBackupResult,
    DatabaseRestoreResult,
    OperationalPruneResult,
    SchemaVersionError,
    _from_json_list,
    _to_json,
)
from recoleta.types import utc_now


def _resolve_artifact_prune_path(
    *,
    raw_path: str,
    artifacts_root: Path | None,
) -> Path | None:
    candidate = Path(raw_path).expanduser()
    if artifacts_root is None:
        return candidate if candidate.is_absolute() else None

    root = artifacts_root.expanduser().resolve()
    resolved = (
        candidate.resolve()
        if candidate.is_absolute()
        else (root / candidate).resolve()
    )
    if resolved == root or not resolved.is_relative_to(root):
        return None
    return resolved


@dataclass(frozen=True, slots=True)
class _ArtifactPrunePlan:
    eligible_rows: tuple[Artifact, ...]
    unique_paths: tuple[Path, ...]
    skipped_path_values: frozenset[str]
    skipped_run_ids: tuple[str, ...]
    skipped_rows: int


def _build_artifact_prune_plan(
    *,
    rows: list[Artifact],
    artifacts_root: Path | None,
) -> _ArtifactPrunePlan:
    eligible_rows: list[Artifact] = []
    unique_paths: list[Path] = []
    seen_paths: set[str] = set()
    skipped_path_values: set[str] = set()
    skipped_run_ids: set[str] = set()
    skipped_rows = 0
    for row in rows:
        raw_path = str(getattr(row, "path", "") or "").strip()
        resolved_path = (
            _resolve_artifact_prune_path(
                raw_path=raw_path,
                artifacts_root=artifacts_root,
            )
            if raw_path
            else None
        )
        if resolved_path is None:
            skipped_rows += 1
            if raw_path:
                skipped_path_values.add(raw_path)
            skipped_run_ids.add(str(row.run_id))
            continue
        eligible_rows.append(row)
        resolved_path_value = str(resolved_path)
        if resolved_path_value in seen_paths:
            continue
        seen_paths.add(resolved_path_value)
        unique_paths.append(resolved_path)
    return _ArtifactPrunePlan(
        eligible_rows=tuple(eligible_rows),
        unique_paths=tuple(unique_paths),
        skipped_path_values=frozenset(skipped_path_values),
        skipped_run_ids=tuple(sorted(skipped_run_ids)),
        skipped_rows=skipped_rows,
    )


def _prune_artifact_paths(
    *,
    paths: tuple[Path, ...],
    dry_run: bool,
) -> tuple[int, int]:
    deleted_paths = 0
    missing_paths = 0
    for path in paths:
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
    return deleted_paths, missing_paths


class MaintenanceStoreMixin:
    engine: Any
    db_path: Path

    def _commit(self, session: Session) -> None: ...

    def schema_version(self) -> int: ...

    def add_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        path: str,
        details: dict[str, Any] | None = None,
    ) -> None:
        normalized_details = details if isinstance(details, dict) else {}
        artifact = Artifact(
            run_id=run_id,
            item_id=item_id,
            kind=kind,
            path=path,
            details_json=_to_json(normalized_details),
        )
        with Session(self.engine) as session:
            session.add(artifact)
            self._commit(session)

    def list_artifacts_for_run(self, *, run_id: str) -> list[Artifact]:
        normalized_run_id = str(run_id or "").strip()
        if not normalized_run_id:
            return []
        with Session(self.engine) as session:
            statement = (
                select(Artifact)
                .where(Artifact.run_id == normalized_run_id)
                .order_by(
                    desc(cast(Any, Artifact.created_at)),
                    desc(cast(Any, Artifact.id)),
                )
            )
            return list(session.exec(statement))

    def diagnose_corpus_window(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        min_relevance_score: float = 0.0,
    ) -> dict[str, Any]:
        min_relevance = float(min_relevance_score or 0.0)
        selected_item_states = {ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED}

        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            rows = list(
                session.exec(
                    select(Item, Analysis)
                    .outerjoin(
                        Analysis,
                        and_(
                            cast(Any, Analysis.item_id) == cast(Any, Item.id),
                        ),
                    )
                    .where(event_at >= period_start, event_at < period_end)
                    .order_by(
                        desc(cast(Any, event_at)),
                        desc(cast(Any, Item.updated_at)),
                        desc(cast(Any, Item.created_at)),
                    )
                )
            )
            indexed_item_docs_total = int(
                session.exec(
                    select(func.count())
                    .select_from(Document)
                    .where(
                        Document.doc_type == "item",
                        cast(Any, Document.published_at).is_not(None),
                        cast(Any, Document.published_at) >= period_start,
                        cast(Any, Document.published_at) < period_end,
                    )
                ).one()
                or 0
            )

        item_states: dict[str, int] = {}
        eligible_item_states: dict[str, int] = {}
        exclusion_reasons: dict[str, int] = {}
        selected_total = 0
        filtered_out_total = 0
        analysis_present_total = 0
        eligible_item_state_present_total = 0
        excluded_samples: list[dict[str, Any]] = []

        for item, analysis in rows:
            item_state = str(getattr(item, "state", "") or "unknown")
            item_states[item_state] = item_states.get(item_state, 0) + 1
            if analysis is not None:
                analysis_present_total += 1

            blockers: set[str] = set()
            if analysis is None:
                blockers.add("missing_analysis")

            eligible_item_state_present_total += 1
            eligible_item_states[item_state] = (
                eligible_item_states.get(item_state, 0) + 1
            )
            if item_state not in selected_item_states:
                blockers.add(f"item_state_{item_state}")

            if (
                analysis is not None
                and float(getattr(analysis, "relevance_score", 0.0) or 0.0)
                < min_relevance
            ):
                blockers.add("relevance_below_threshold")

            if blockers:
                filtered_out_total += 1
                for reason in sorted(blockers):
                    exclusion_reasons[reason] = exclusion_reasons.get(reason, 0) + 1
                if len(excluded_samples) < 5:
                    excluded_samples.append(
                        {
                            "item_id": int(getattr(item, "id", 0) or 0),
                            "title": str(getattr(item, "title", "") or ""),
                            "reasons": sorted(blockers),
                        }
                    )
                continue

            selected_total += 1

        return {
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "scope": "default",
            "min_relevance_score": min_relevance,
            "candidate_total": len(rows),
            "selected_total": selected_total,
            "filtered_out_total": filtered_out_total,
            "analysis_present_total": analysis_present_total,
            "eligible_item_state_present_total": eligible_item_state_present_total,
            "indexed_item_docs_total": indexed_item_docs_total,
            "item_states": dict(sorted(item_states.items())),
            "eligible_item_states": dict(sorted(eligible_item_states.items())),
            "exclusion_reasons": dict(
                sorted(
                    exclusion_reasons.items(), key=lambda entry: (-entry[1], entry[0])
                )
            ),
            "excluded_samples": excluded_samples,
        }

    def prune_artifacts_older_than(
        self,
        *,
        older_than: datetime,
        dry_run: bool = False,
        artifacts_root: Path | None = None,
    ) -> ArtifactPruneResult:
        with Session(self.engine) as session:
            rows = list(
                session.exec(
                    select(Artifact).where(cast(Any, Artifact.created_at) < older_than)
                )
            )
            if not rows:
                return ArtifactPruneResult()

            plan = _build_artifact_prune_plan(
                rows=rows,
                artifacts_root=artifacts_root,
            )
            deleted_paths, missing_paths = _prune_artifact_paths(
                paths=plan.unique_paths,
                dry_run=dry_run,
            )

            if not dry_run:
                for row in plan.eligible_rows:
                    session.delete(row)
                self._commit(session)

        return ArtifactPruneResult(
            artifact_rows=len(plan.eligible_rows),
            deleted_paths=deleted_paths,
            missing_paths=missing_paths,
            skipped_paths=len(plan.skipped_path_values),
            candidate_rows=len(rows),
            skipped_rows=plan.skipped_rows,
            skipped_run_ids=plan.skipped_run_ids,
        )

    def prune_operational_history_older_than(
        self,
        *,
        older_than: datetime,
        dry_run: bool = False,
        artifact_older_than: datetime | None = None,
        protected_artifact_run_ids: Iterable[str] = (),
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
            canonical_run_ids = self._canonical_reference_run_ids(
                session=session,
                run_ids=run_ids,
            )
            artifact_run_ids = self._retained_artifact_run_ids(
                session=session,
                run_ids=run_ids,
                artifact_older_than=artifact_older_than,
                protected_run_ids=protected_artifact_run_ids,
            )
            retained_run_ids = canonical_run_ids | artifact_run_ids
            deletable_runs = [
                run for run in runs if str(run.id) not in retained_run_ids
            ]

            if not dry_run:
                for metric in metrics:
                    session.delete(metric)
                for run in deletable_runs:
                    session.delete(run)
                self._commit(session)

        return OperationalPruneResult(
            run_rows=len(deletable_runs),
            metric_rows=len(metrics),
            retained_run_rows=len(retained_run_ids),
            retained_canonical_run_rows=len(canonical_run_ids),
            retained_artifact_run_rows=len(artifact_run_ids),
        )

    @staticmethod
    def _canonical_reference_run_ids(
        *,
        session: Session,
        run_ids: list[str],
    ) -> set[str]:
        if not run_ids:
            return set()
        pass_output_ids = session.exec(
            select(PassOutput.run_id).where(cast(Any, PassOutput.run_id).in_(run_ids))
        )
        receipt_ids = session.exec(
            select(WorkflowStepReceipt.run_id).where(
                cast(Any, WorkflowStepReceipt.run_id).in_(run_ids)
            )
        )
        return {str(run_id) for run_id in [*pass_output_ids, *receipt_ids]}

    @staticmethod
    def _retained_artifact_run_ids(
        *,
        session: Session,
        run_ids: list[str],
        artifact_older_than: datetime | None,
        protected_run_ids: Iterable[str] = (),
    ) -> set[str]:
        if not run_ids:
            return set()
        statement = select(Artifact.run_id).where(
            cast(Any, Artifact.run_id).in_(run_ids)
        )
        if artifact_older_than is not None:
            statement = statement.where(
                cast(Any, Artifact.created_at) >= artifact_older_than
            )
        recent_run_ids = {str(run_id) for run_id in session.exec(statement)}
        protected = {str(run_id) for run_id in protected_run_ids}
        return recent_run_ids | (set(run_ids) & protected)

    def clear_document_chunk_cache(
        self,
        *,
        dry_run: bool = False,
    ) -> ChunkCachePruneResult:
        chunk_count_statement = text("SELECT COUNT(*) FROM document_chunks")
        embedding_count_statement = text("SELECT COUNT(*) FROM chunk_embeddings")
        fts_count_statement = text("SELECT COUNT(*) FROM chunk_fts")
        with self.engine.begin() as conn:
            document_chunks = int(conn.execute(chunk_count_statement).scalar() or 0)
            chunk_embeddings = int(
                conn.execute(embedding_count_statement).scalar() or 0
            )
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
