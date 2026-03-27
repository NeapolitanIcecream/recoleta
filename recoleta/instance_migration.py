from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3
from typing import Any, Callable

import yaml

from recoleta.legacy_migration import (
    legacy_explicit_topic_streams,
    load_legacy_config_document,
    load_legacy_settings,
)
from recoleta.pipeline.topic_streams import telegram_destination_for_stream
from recoleta.storage import Repository
from recoleta.types import DEFAULT_TOPIC_STREAM, sha256_hex

_SOURCE_TABLES_ALWAYS_DROPPED = ("runs", "metrics", "artifacts")
_SOURCE_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")

_ITEM_COLUMNS = (
    "id",
    "source",
    "source_item_id",
    "canonical_url",
    "canonical_url_hash",
    "title",
    "authors",
    "published_at",
    "raw_metadata_json",
    "state",
    "created_at",
    "updated_at",
)
_CONTENT_COLUMNS = (
    "id",
    "item_id",
    "content_type",
    "text",
    "artifact_path",
    "content_hash",
    "created_at",
)
_ANALYSIS_COLUMNS = (
    "id",
    "item_id",
    "model",
    "provider",
    "summary",
    "topics_json",
    "relevance_score",
    "novelty_score",
    "cost_usd",
    "latency_ms",
    "created_at",
)
_DOCUMENT_COLUMNS = (
    "id",
    "doc_type",
    "item_id",
    "source",
    "canonical_url",
    "title",
    "published_at",
    "granularity",
    "period_start",
    "period_end",
    "created_at",
    "updated_at",
)
_DOCUMENT_CHUNK_COLUMNS = (
    "id",
    "doc_id",
    "chunk_index",
    "kind",
    "text",
    "start_char",
    "end_char",
    "text_hash",
    "source_content_type",
    "created_at",
)
_PASS_OUTPUT_COLUMNS = (
    "id",
    "run_id",
    "pass_kind",
    "status",
    "granularity",
    "period_start",
    "period_end",
    "schema_version",
    "content_hash",
    "payload_json",
    "diagnostics_json",
    "input_refs_json",
    "created_at",
)
_LOCALIZED_OUTPUT_COLUMNS = (
    "id",
    "source_kind",
    "source_record_id",
    "language_code",
    "status",
    "schema_version",
    "source_hash",
    "variant_role",
    "payload_json",
    "diagnostics_json",
    "created_at",
    "updated_at",
)
_SOURCE_PULL_STATE_COLUMNS = (
    "id",
    "source",
    "scope_kind",
    "scope_key",
    "etag",
    "last_modified",
    "watermark_published_at",
    "cursor_json",
    "created_at",
    "updated_at",
)
_DELIVERY_COLUMNS = (
    "id",
    "item_id",
    "channel",
    "destination",
    "message_id",
    "status",
    "error",
    "sent_at",
)
_TREND_DELIVERY_COLUMNS = (
    "id",
    "doc_id",
    "channel",
    "destination",
    "content_hash",
    "message_id",
    "status",
    "error",
    "sent_at",
)


@dataclass(slots=True)
class _ChildPlan:
    name: str
    legacy_scope: str
    config_path: Path
    db_path: Path
    output_dir: Path
    lancedb_dir: Path
    artifacts_dir: Path | None
    config_payload: dict[str, Any]
    synthetic_run_id: str
    delivery_destination: str | None
    copy_source_pull_states: bool


def _connect_sqlite(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def _table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = ? LIMIT 1",
        (table_name,),
    ).fetchone()
    return row is not None


def _table_columns(conn: sqlite3.Connection, table_name: str) -> set[str]:
    if not _table_exists(conn, table_name):
        return set()
    rows = conn.execute(f"PRAGMA table_info({table_name})").fetchall()
    return {str(row[1]) for row in rows}


def _table_has_column(conn: sqlite3.Connection, table_name: str, column: str) -> bool:
    return column in _table_columns(conn, table_name)


def _fetch_rows(
    conn: sqlite3.Connection,
    *,
    table: str,
    where_sql: str = "",
    params: tuple[Any, ...] = (),
) -> list[sqlite3.Row]:
    sql = f"SELECT * FROM {table}"
    if where_sql:
        sql += f" WHERE {where_sql}"
    sql += ";"
    return list(conn.execute(sql, params).fetchall())


def _count_rows(
    conn: sqlite3.Connection,
    *,
    table: str,
    where_sql: str = "",
    params: tuple[Any, ...] = (),
) -> int:
    sql = f"SELECT COUNT(*) FROM {table}"
    if where_sql:
        sql += f" WHERE {where_sql}"
    row = conn.execute(sql, params).fetchone()
    return int(row[0] if row is not None else 0)


def _fetch_scope_rows(
    conn: sqlite3.Connection,
    *,
    table: str,
    scope: str,
) -> list[sqlite3.Row]:
    if not _table_exists(conn, table) or not _table_has_column(conn, table, "scope"):
        return []
    return _fetch_rows(conn, table=table, where_sql="scope = ?", params=(scope,))


def _count_scope_rows(
    conn: sqlite3.Connection,
    *,
    table: str,
    scope: str,
) -> int:
    if not _table_exists(conn, table) or not _table_has_column(conn, table, "scope"):
        return 0
    return _count_rows(conn, table=table, where_sql="scope = ?", params=(scope,))


def _insert_dict_rows(
    conn: sqlite3.Connection,
    *,
    table: str,
    columns: tuple[str, ...],
    rows: list[dict[str, Any]],
) -> int:
    if not rows:
        return 0
    placeholders = ", ".join("?" for _ in columns)
    column_sql = ", ".join(columns)
    sql = f"INSERT INTO {table} ({column_sql}) VALUES ({placeholders})"
    conn.executemany(
        sql,
        [tuple(row.get(column) for column in columns) for row in rows],
    )
    return len(rows)


def _enabled_sources(settings: Any) -> list[str]:
    enabled: list[str] = []
    sources = getattr(settings, "sources", None)
    if sources is None:
        return enabled
    for name in _SOURCE_NAMES:
        block = getattr(sources, name, None)
        if block is not None and bool(getattr(block, "enabled", False)):
            enabled.append(name)
    return enabled


def _legacy_stream_config_by_name(config_document: dict[str, Any]) -> dict[str, dict[str, Any]]:
    raw_streams = config_document.get("topic_streams") or config_document.get("TOPIC_STREAMS") or []
    by_name: dict[str, dict[str, Any]] = {}
    if not isinstance(raw_streams, list):
        return by_name
    for entry in raw_streams:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name") or "").strip()
        if not name:
            continue
        by_name[name] = deepcopy(entry)
    return by_name


def _default_scope_counts(conn: sqlite3.Connection) -> dict[str, int]:
    tables = {
        "analyses": "scope = ?",
        "documents": "scope = ?",
        "pass_outputs": "scope = ?",
        "localized_outputs": "scope = ?",
    }
    counts = {table: 0 for table in tables}
    for table, predicate in tables.items():
        if _table_exists(conn, table) and _table_has_column(conn, table, "scope"):
            counts[table] = _count_rows(
                conn,
                table=table,
                where_sql=predicate,
                params=(DEFAULT_TOPIC_STREAM,),
            )
    item_ids = {
        int(row["item_id"])
        for row in _fetch_rows(
            conn,
            table="item_stream_states",
            where_sql="stream = ?",
            params=(DEFAULT_TOPIC_STREAM,),
        )
    } if _table_exists(conn, "item_stream_states") else set()
    counts["items_only"] = len(item_ids)
    return counts


def _synthetic_run_id(name: str) -> str:
    return f"migrate-tsi-{sha256_hex(name)[:16]}"


def _child_paths(*, output_root: Path, name: str) -> tuple[Path, Path, Path, Path]:
    instance_root = output_root / "instances" / name
    return (
        instance_root / "recoleta.yaml",
        instance_root / "recoleta.db",
        instance_root / "outputs",
        instance_root / "lancedb",
    )


def _materialize_child_config_payload(
    *,
    base_document: dict[str, Any],
    name: str,
    topics: list[str],
    allow_tags: list[str],
    deny_tags: list[str],
    publish_targets: list[str],
    min_relevance_score: float,
    max_deliveries_per_day: int,
    obsidian_base_folder: str,
    config_path: Path,
    db_path: Path,
    output_dir: Path,
    lancedb_dir: Path,
    artifacts_dir: Path | None,
    sources_payload: dict[str, Any] | None,
) -> dict[str, Any]:
    payload = deepcopy(base_document)
    payload.pop("topic_streams", None)
    payload.pop("TOPIC_STREAMS", None)
    payload.pop("daemon", None)
    payload.pop("DAEMON", None)
    payload["topics"] = list(topics)
    payload["allow_tags"] = list(allow_tags)
    payload["deny_tags"] = list(deny_tags)
    payload["publish_targets"] = list(publish_targets)
    payload["min_relevance_score"] = float(min_relevance_score)
    payload["max_deliveries_per_day"] = int(max_deliveries_per_day)
    payload["recoleta_db_path"] = str(db_path)
    payload["markdown_output_dir"] = str(output_dir)
    payload["rag_lancedb_dir"] = str(lancedb_dir)
    payload["obsidian_base_folder"] = str(obsidian_base_folder)
    if artifacts_dir is not None:
        payload["artifacts_dir"] = str(artifacts_dir)
    else:
        payload.pop("artifacts_dir", None)
        payload.pop("ARTIFACTS_DIR", None)
    if sources_payload is not None:
        payload["sources"] = deepcopy(sources_payload)
    else:
        payload["sources"] = {}
    return payload


def _write_yaml(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def _maybe_unique_obsidian_base_folder(value: str, *, child_name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        return child_name
    return normalized


def _copy_all_rows(
    source_conn: sqlite3.Connection,
    target_conn: sqlite3.Connection,
    *,
    table: str,
    columns: tuple[str, ...],
    where_sql: str = "",
    params: tuple[Any, ...] = (),
    mutate: Callable[[dict[str, Any]], dict[str, Any] | None] | None = None,
) -> list[dict[str, Any]]:
    rows = _fetch_rows(source_conn, table=table, where_sql=where_sql, params=params)
    payload: list[dict[str, Any]] = []
    for row in rows:
        record = {column: row[column] for column in columns}
        if mutate is not None:
            record = mutate(record)
            if record is None:
                continue
        payload.append(record)
    _insert_dict_rows(target_conn, table=table, columns=columns, rows=payload)
    return payload


def _rebuild_chunk_fts(target_conn: sqlite3.Connection) -> int:
    target_conn.execute("DELETE FROM chunk_fts")
    inserted = target_conn.execute(
        """
        INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind)
        SELECT id, text, doc_id, chunk_index, kind
        FROM document_chunks
        WHERE kind != 'meta'
        """
    ).rowcount
    return int(inserted or 0)


def _site_input_dir_for_child_output(output_dir: Path) -> Path:
    return output_dir / "Trends"


def _count_document_chunks_for_doc_ids(
    conn: sqlite3.Connection,
    *,
    doc_ids: set[int],
    include_meta: bool,
) -> int:
    if not doc_ids or not _table_exists(conn, "document_chunks"):
        return 0
    placeholders = ", ".join("?" for _ in doc_ids)
    where_sql = f"doc_id IN ({placeholders})"
    params: tuple[Any, ...] = tuple(sorted(doc_ids))
    if not include_meta:
        where_sql += " AND kind != ?"
        params = params + ("meta",)
    return _count_rows(conn, table="document_chunks", where_sql=where_sql, params=params)


def _planned_child_manifest_entry(
    source_conn: sqlite3.Connection,
    *,
    plan: _ChildPlan,
    delivery_destination_to_child: dict[str, str],
    child_plan_count: int,
) -> dict[str, Any]:
    doc_rows = _fetch_scope_rows(source_conn, table="documents", scope=plan.legacy_scope)
    doc_ids = {int(row["id"]) for row in doc_rows}
    pass_rows = _fetch_scope_rows(
        source_conn,
        table="pass_outputs",
        scope=plan.legacy_scope,
    )
    pass_output_legacy_run_ids = {
        str(int(row["id"])): str(row["run_id"]) for row in pass_rows
    }

    migrated_delivery_total = 0
    dropped_delivery_total = 0
    if _table_exists(source_conn, "deliveries"):
        for row in _fetch_rows(source_conn, table="deliveries"):
            destination = str(row["destination"] or "")
            owner = delivery_destination_to_child.get(destination)
            if child_plan_count == 1 or owner == plan.name:
                migrated_delivery_total += 1
            else:
                dropped_delivery_total += 1

    migrated_trend_delivery_total = 0
    dropped_trend_delivery_total = 0
    if _table_exists(source_conn, "trend_deliveries"):
        for row in _fetch_rows(source_conn, table="trend_deliveries"):
            if int(row["doc_id"]) in doc_ids:
                migrated_trend_delivery_total += 1
            else:
                dropped_trend_delivery_total += 1

    return {
        "name": plan.name,
        "legacy_scope": plan.legacy_scope,
        "config_path": str(plan.config_path),
        "db_path": str(plan.db_path),
        "output_dir": str(plan.output_dir),
        "rag_lancedb_dir": str(plan.lancedb_dir),
        "artifacts_dir": str(plan.artifacts_dir) if plan.artifacts_dir is not None else None,
        "synthetic_run_id": plan.synthetic_run_id,
        "copied_source_pull_states": bool(plan.copy_source_pull_states),
        "item_total": _count_rows(source_conn, table="items") if _table_exists(source_conn, "items") else 0,
        "content_total": _count_rows(source_conn, table="contents") if _table_exists(source_conn, "contents") else 0,
        "analysis_total": _count_scope_rows(
            source_conn,
            table="analyses",
            scope=plan.legacy_scope,
        ),
        "document_total": len(doc_rows),
        "document_chunk_total": _count_document_chunks_for_doc_ids(
            source_conn,
            doc_ids=doc_ids,
            include_meta=True,
        ),
        "localized_output_total": _count_scope_rows(
            source_conn,
            table="localized_outputs",
            scope=plan.legacy_scope,
        ),
        "pass_output_total": len(pass_rows),
        "pass_output_legacy_run_ids": pass_output_legacy_run_ids,
        "chunk_fts_rows": _count_document_chunks_for_doc_ids(
            source_conn,
            doc_ids=doc_ids,
            include_meta=False,
        ),
        "deliveries": {
            "migrated": migrated_delivery_total,
            "dropped": dropped_delivery_total,
        },
        "trend_deliveries": {
            "migrated": migrated_trend_delivery_total,
            "dropped": dropped_trend_delivery_total,
        },
    }


def _build_migration_manifest_payload(
    *,
    resolved_config_path: Path,
    resolved_db_path: Path,
    fleet_manifest_path: Path,
    normalized_ambiguous_source_mode: str,
    normalized_shared_delivery_mode: str,
    normalized_default_scope_mode: str,
    manifest_children: list[dict[str, Any]],
    archived_default_scope: dict[str, int],
    warnings: list[str],
    source_conn: sqlite3.Connection,
    dry_run: bool,
) -> dict[str, Any]:
    return {
        "source_config_path": str(resolved_config_path),
        "source_db_path": str(resolved_db_path),
        "fleet_manifest_path": str(fleet_manifest_path),
        "dry_run": dry_run,
        "flags": {
            "ambiguous_source_mode": normalized_ambiguous_source_mode,
            "shared_delivery_mode": normalized_shared_delivery_mode,
            "default_scope_mode": normalized_default_scope_mode,
        },
        "children": manifest_children,
        "archived_default_scope": archived_default_scope if normalized_default_scope_mode == "archive" else {},
        "intentionally_dropped_history": {
            table: _count_rows(source_conn, table=table)
            for table in _SOURCE_TABLES_ALWAYS_DROPPED
            if _table_exists(source_conn, table)
        },
        "warnings": warnings,
    }


def migrate_topic_streams_to_instances(
    *,
    config_path: Path,
    db_path: Path,
    output_dir: Path,
    ambiguous_source_mode: str = "fail",
    shared_delivery_mode: str = "fail",
    default_scope_mode: str = "archive",
    dry_run: bool = False,
) -> dict[str, Any]:
    resolved_config_path = config_path.expanduser().resolve()
    resolved_db_path = db_path.expanduser().resolve()
    resolved_output_dir = output_dir.expanduser().resolve()

    legacy_document = load_legacy_config_document(resolved_config_path)
    legacy_settings = load_legacy_settings(resolved_config_path)
    explicit_streams = legacy_explicit_topic_streams(legacy_settings)
    if not explicit_streams:
        raise ValueError("Legacy config does not define explicit TOPIC_STREAMS")

    normalized_ambiguous_source_mode = (
        str(ambiguous_source_mode or "").strip().lower() or "fail"
    )
    normalized_shared_delivery_mode = (
        str(shared_delivery_mode or "").strip().lower() or "fail"
    )
    normalized_default_scope_mode = (
        str(default_scope_mode or "").strip().lower() or "archive"
    )
    if normalized_ambiguous_source_mode not in {"fail", "copy_all", "disable"}:
        raise ValueError("ambiguous_source_mode must be one of: fail, copy_all, disable")
    if normalized_shared_delivery_mode not in {"fail", "allow"}:
        raise ValueError("shared_delivery_mode must be one of: fail, allow")
    if normalized_default_scope_mode not in {"archive", "child-instance"}:
        raise ValueError("default_scope_mode must be one of: archive, child-instance")

    enabled_sources = _enabled_sources(legacy_settings)
    source_must_be_disambiguated = len(explicit_streams) > 1 and bool(enabled_sources)
    if source_must_be_disambiguated and normalized_ambiguous_source_mode == "fail":
        raise ValueError(
            "Legacy sources are shared across multiple topic streams; "
            "set --ambiguous-source-mode copy_all or disable."
        )

    legacy_stream_configs = _legacy_stream_config_by_name(legacy_document)
    child_plans: list[_ChildPlan] = []
    for stream in explicit_streams:
        raw_stream = legacy_stream_configs.get(stream.name, {})
        if (
            "telegram_bot_token_env" in raw_stream
            or "telegram_chat_id_env" in raw_stream
        ):
            raise ValueError(
                "Per-stream telegram env overrides are not yet supported by child config materialization"
            )
        child_config_path, child_db_path, child_output_dir, child_lancedb_dir = _child_paths(
            output_root=resolved_output_dir,
            name=stream.name,
        )
        artifacts_dir: Path | None = None
        if (
            legacy_document.get("artifacts_dir") is not None
            or legacy_document.get("ARTIFACTS_DIR") is not None
            or bool(legacy_document.get("write_debug_artifacts"))
            or bool(legacy_document.get("WRITE_DEBUG_ARTIFACTS"))
        ):
            artifacts_dir = child_config_path.parent / "artifacts"
        sources_payload = (
            legacy_document.get("sources")
            if normalized_ambiguous_source_mode == "copy_all" or not source_must_be_disambiguated
            else None
        )
        child_payload = _materialize_child_config_payload(
            base_document=legacy_document,
            name=stream.name,
            topics=list(stream.topics),
            allow_tags=list(stream.allow_tags),
            deny_tags=list(stream.deny_tags),
            publish_targets=list(stream.publish_targets),
            min_relevance_score=float(stream.min_relevance_score),
            max_deliveries_per_day=int(stream.max_deliveries_per_day),
            obsidian_base_folder=_maybe_unique_obsidian_base_folder(
                stream.obsidian_base_folder,
                child_name=stream.name,
            ),
            config_path=child_config_path,
            db_path=child_db_path,
            output_dir=child_output_dir,
            lancedb_dir=child_lancedb_dir,
            artifacts_dir=artifacts_dir,
            sources_payload=sources_payload,
        )
        child_plans.append(
            _ChildPlan(
                name=stream.name,
                legacy_scope=stream.name,
                config_path=child_config_path,
                db_path=child_db_path,
                output_dir=child_output_dir,
                lancedb_dir=child_lancedb_dir,
                artifacts_dir=artifacts_dir,
                config_payload=child_payload,
                synthetic_run_id=_synthetic_run_id(stream.name),
                delivery_destination=(
                    telegram_destination_for_stream(stream)
                    if "telegram" in list(stream.publish_targets)
                    else None
                ),
                copy_source_pull_states=(
                    normalized_ambiguous_source_mode == "copy_all"
                    or not source_must_be_disambiguated
                ),
            )
        )

    with _connect_sqlite(resolved_db_path) as source_conn:
        archived_default_scope = _default_scope_counts(source_conn)
        if (
            normalized_default_scope_mode == "child-instance"
            and any(value > 0 for value in archived_default_scope.values())
        ):
            child_config_path, child_db_path, child_output_dir, child_lancedb_dir = _child_paths(
                output_root=resolved_output_dir,
                name="legacy_default",
            )
            default_artifacts_dir: Path | None = None
            if (
                legacy_document.get("artifacts_dir") is not None
                or legacy_document.get("ARTIFACTS_DIR") is not None
                or bool(legacy_document.get("write_debug_artifacts"))
                or bool(legacy_document.get("WRITE_DEBUG_ARTIFACTS"))
            ):
                default_artifacts_dir = child_config_path.parent / "artifacts"
            child_plans.append(
                _ChildPlan(
                    name="legacy_default",
                    legacy_scope=DEFAULT_TOPIC_STREAM,
                    config_path=child_config_path,
                    db_path=child_db_path,
                    output_dir=child_output_dir,
                    lancedb_dir=child_lancedb_dir,
                    artifacts_dir=default_artifacts_dir,
                    config_payload=_materialize_child_config_payload(
                        base_document=legacy_document,
                        name="legacy_default",
                        topics=list(getattr(legacy_settings, "topics", []) or []),
                        allow_tags=list(getattr(legacy_settings, "allow_tags", []) or []),
                        deny_tags=list(getattr(legacy_settings, "deny_tags", []) or []),
                        publish_targets=list(getattr(legacy_settings, "publish_targets", []) or []),
                        min_relevance_score=float(getattr(legacy_settings, "min_relevance_score", 0.6)),
                        max_deliveries_per_day=int(getattr(legacy_settings, "max_deliveries_per_day", 10)),
                        obsidian_base_folder=_maybe_unique_obsidian_base_folder(
                            f"{getattr(legacy_settings, 'obsidian_base_folder', '')}/legacy_default",
                            child_name="legacy_default",
                        ),
                        config_path=child_config_path,
                        db_path=child_db_path,
                        output_dir=child_output_dir,
                        lancedb_dir=child_lancedb_dir,
                        artifacts_dir=default_artifacts_dir,
                        sources_payload=(
                            legacy_document.get("sources")
                            if normalized_ambiguous_source_mode == "copy_all" or not source_must_be_disambiguated
                            else None
                        ),
                    ),
                    synthetic_run_id=_synthetic_run_id("legacy_default"),
                    delivery_destination=None,
                    copy_source_pull_states=(
                        normalized_ambiguous_source_mode == "copy_all"
                        or not source_must_be_disambiguated
                    ),
                )
            )

    shared_destinations: dict[str, list[str]] = {}
    for plan in child_plans:
        if plan.delivery_destination is None:
            continue
        shared_destinations.setdefault(plan.delivery_destination, []).append(plan.name)
    overlapping_destinations = {
        destination: names
        for destination, names in shared_destinations.items()
        if len(names) > 1
    }
    if (
        normalized_ambiguous_source_mode == "copy_all"
        and overlapping_destinations
        and normalized_shared_delivery_mode == "fail"
    ):
        examples = ", ".join(
            f"{destination} -> {', '.join(sorted(names))}"
            for destination, names in sorted(overlapping_destinations.items())
        )
        raise ValueError(
            "copy_all would preserve a shared Telegram destination across child instances; "
            f"shared Telegram destination(s): {examples}"
        )

    fleet_manifest_path = resolved_output_dir / "fleet.yaml"
    migration_manifest_path = resolved_output_dir / "migration-manifest.json"
    fleet_manifest = {
        "schema_version": 1,
        "instances": [
            {"name": plan.name, "config_path": str(plan.config_path)}
            for plan in child_plans
        ],
    }

    warnings: list[str] = []
    if overlapping_destinations and normalized_shared_delivery_mode == "allow":
        warnings.append(
            "copy_all preserved shared Telegram destinations; overlapping source coverage may duplicate deliveries and max_deliveries_per_day is now enforced per instance"
        )

    with _connect_sqlite(resolved_db_path) as source_conn:
        delivery_destination_to_child = {
            plan.delivery_destination: plan.name
            for plan in child_plans
            if plan.delivery_destination is not None
            and plan.delivery_destination not in overlapping_destinations
        }
        manifest_children: list[dict[str, Any]] = []
        if dry_run:
            manifest_children = [
                _planned_child_manifest_entry(
                    source_conn,
                    plan=plan,
                    delivery_destination_to_child=delivery_destination_to_child,
                    child_plan_count=len(child_plans),
                )
                for plan in child_plans
            ]
            migration_manifest = _build_migration_manifest_payload(
                resolved_config_path=resolved_config_path,
                resolved_db_path=resolved_db_path,
                fleet_manifest_path=fleet_manifest_path,
                normalized_ambiguous_source_mode=normalized_ambiguous_source_mode,
                normalized_shared_delivery_mode=normalized_shared_delivery_mode,
                normalized_default_scope_mode=normalized_default_scope_mode,
                manifest_children=manifest_children,
                archived_default_scope=archived_default_scope,
                warnings=warnings,
                source_conn=source_conn,
                dry_run=True,
            )
            return {
                "dry_run": True,
                "fleet_manifest_path": str(fleet_manifest_path),
                "fleet_manifest": fleet_manifest,
                "migration_manifest_path": str(migration_manifest_path),
                "migration_manifest": migration_manifest,
                "children": manifest_children,
                "warnings": warnings,
            }

        resolved_output_dir.mkdir(parents=True, exist_ok=True)
        for plan in child_plans:
            plan.config_path.parent.mkdir(parents=True, exist_ok=True)
            _write_yaml(plan.config_path, plan.config_payload)
            child_repository = Repository(db_path=plan.db_path)
            child_repository.init_schema()
            created_run = child_repository.create_run(
                config_fingerprint="topic-streams-to-instances-migration",
                run_id=plan.synthetic_run_id,
            )
            child_repository.update_run_context(
                run_id=created_run.id,
                command="admin migrate topic-streams-to-instances",
                operation_kind="admin.migrate.topic_streams_to_instances",
                scope=DEFAULT_TOPIC_STREAM,
            )
            child_repository.finish_run(created_run.id, success=True)

            item_states = {
                int(row["item_id"]): str(row["state"])
                for row in _fetch_rows(
                    source_conn,
                    table="item_stream_states",
                    where_sql="stream = ?",
                    params=(plan.legacy_scope,),
                )
            } if _table_exists(source_conn, "item_stream_states") else {}

            doc_rows = _fetch_scope_rows(
                source_conn,
                table="documents",
                scope=plan.legacy_scope,
            )
            doc_ids = {int(row["id"]) for row in doc_rows}

            pass_rows = _fetch_scope_rows(
                source_conn,
                table="pass_outputs",
                scope=plan.legacy_scope,
            )
            pass_output_legacy_run_ids = {
                str(int(row["id"])): str(row["run_id"]) for row in pass_rows
            }

            localized_rows = _fetch_scope_rows(
                source_conn,
                table="localized_outputs",
                scope=plan.legacy_scope,
            )

            with _connect_sqlite(plan.db_path) as child_conn:
                child_conn.execute("PRAGMA foreign_keys = ON")

                item_payload = []
                for row in _fetch_rows(source_conn, table="items"):
                    record = {column: row[column] for column in _ITEM_COLUMNS}
                    record["state"] = item_states.get(int(row["id"]), row["state"])
                    item_payload.append(record)
                _insert_dict_rows(
                    child_conn,
                    table="items",
                    columns=_ITEM_COLUMNS,
                    rows=item_payload,
                )

                _copy_all_rows(
                    source_conn,
                    child_conn,
                    table="contents",
                    columns=_CONTENT_COLUMNS,
                )
                if _table_has_column(source_conn, "analyses", "scope"):
                    _copy_all_rows(
                        source_conn,
                        child_conn,
                        table="analyses",
                        columns=_ANALYSIS_COLUMNS,
                        where_sql="scope = ?",
                        params=(plan.legacy_scope,),
                    )
                if _table_has_column(source_conn, "documents", "scope"):
                    _copy_all_rows(
                        source_conn,
                        child_conn,
                        table="documents",
                        columns=_DOCUMENT_COLUMNS,
                        where_sql="scope = ?",
                        params=(plan.legacy_scope,),
                    )
                if doc_ids:
                    placeholders = ", ".join("?" for _ in doc_ids)
                    _copy_all_rows(
                        source_conn,
                        child_conn,
                        table="document_chunks",
                        columns=_DOCUMENT_CHUNK_COLUMNS,
                        where_sql=f"doc_id IN ({placeholders})",
                        params=tuple(sorted(doc_ids)),
                    )
                if _table_has_column(source_conn, "pass_outputs", "scope"):
                    _copy_all_rows(
                        source_conn,
                        child_conn,
                        table="pass_outputs",
                        columns=_PASS_OUTPUT_COLUMNS,
                        where_sql="scope = ?",
                        params=(plan.legacy_scope,),
                        mutate=lambda record: {
                            **record,
                            "run_id": plan.synthetic_run_id,
                        },
                    )
                if localized_rows:
                    localized_payload = []
                    for row in localized_rows:
                        record = {column: row[column] for column in _LOCALIZED_OUTPUT_COLUMNS}
                        localized_payload.append(record)
                    _insert_dict_rows(
                        child_conn,
                        table="localized_outputs",
                        columns=_LOCALIZED_OUTPUT_COLUMNS,
                        rows=localized_payload,
                    )
                if plan.copy_source_pull_states and _table_exists(source_conn, "source_pull_states"):
                    _copy_all_rows(
                        source_conn,
                        child_conn,
                        table="source_pull_states",
                        columns=_SOURCE_PULL_STATE_COLUMNS,
                    )

                migrated_delivery_total = 0
                dropped_delivery_total = 0
                if _table_exists(source_conn, "deliveries"):
                    for row in _fetch_rows(source_conn, table="deliveries"):
                        destination = str(row["destination"] or "")
                        owner = delivery_destination_to_child.get(destination)
                        if len(child_plans) == 1 or owner == plan.name:
                            migrated_delivery_total += _insert_dict_rows(
                                child_conn,
                                table="deliveries",
                                columns=_DELIVERY_COLUMNS,
                                rows=[
                                    {
                                        column: row[column]
                                        for column in _DELIVERY_COLUMNS
                                    }
                                ],
                            )
                        else:
                            dropped_delivery_total += 1
                migrated_trend_delivery_total = 0
                dropped_trend_delivery_total = 0
                if _table_exists(source_conn, "trend_deliveries"):
                    for row in _fetch_rows(source_conn, table="trend_deliveries"):
                        if int(row["doc_id"]) in doc_ids:
                            migrated_trend_delivery_total += _insert_dict_rows(
                                child_conn,
                                table="trend_deliveries",
                                columns=_TREND_DELIVERY_COLUMNS,
                                rows=[
                                    {
                                        column: row[column]
                                        for column in _TREND_DELIVERY_COLUMNS
                                    }
                                ],
                            )
                        else:
                            dropped_trend_delivery_total += 1

                rebuilt_chunk_fts_total = _rebuild_chunk_fts(child_conn)
                child_conn.commit()

            from recoleta.cli.materialize import run_materialize_outputs_command

            run_materialize_outputs_command(
                db_path=None,
                config_path=plan.config_path,
                output_dir=None,
                scope=DEFAULT_TOPIC_STREAM,
                granularity=None,
                pdf=False,
                site=False,
                debug_pdf=False,
                json_output=False,
                command_name=f"admin migrate materialize --instance {plan.name}",
            )
            from recoleta.site import export_trend_static_site
            from recoleta.fleet import child_default_language_code

            site_input_dir = _site_input_dir_for_child_output(plan.output_dir)
            if site_input_dir.exists():
                export_trend_static_site(
                    input_dir=site_input_dir,
                    output_dir=plan.output_dir / "site",
                    default_language_code=child_default_language_code(plan.config_path),
                )

            manifest_children.append(
                {
                    "name": plan.name,
                    "legacy_scope": plan.legacy_scope,
                    "config_path": str(plan.config_path),
                    "db_path": str(plan.db_path),
                    "output_dir": str(plan.output_dir),
                    "rag_lancedb_dir": str(plan.lancedb_dir),
                    "artifacts_dir": str(plan.artifacts_dir) if plan.artifacts_dir is not None else None,
                    "synthetic_run_id": plan.synthetic_run_id,
                    "copied_source_pull_states": bool(plan.copy_source_pull_states),
                    "pass_output_legacy_run_ids": pass_output_legacy_run_ids,
                    "chunk_fts_rows": rebuilt_chunk_fts_total,
                    "deliveries": {
                        "migrated": migrated_delivery_total,
                        "dropped": dropped_delivery_total,
                    },
                    "trend_deliveries": {
                        "migrated": migrated_trend_delivery_total,
                        "dropped": dropped_trend_delivery_total,
                    },
                }
            )

    _write_yaml(fleet_manifest_path, fleet_manifest)

    with _connect_sqlite(resolved_db_path) as source_conn:
        migration_manifest = _build_migration_manifest_payload(
            resolved_config_path=resolved_config_path,
            resolved_db_path=resolved_db_path,
            fleet_manifest_path=fleet_manifest_path,
            normalized_ambiguous_source_mode=normalized_ambiguous_source_mode,
            normalized_shared_delivery_mode=normalized_shared_delivery_mode,
            normalized_default_scope_mode=normalized_default_scope_mode,
            manifest_children=manifest_children,
            archived_default_scope=archived_default_scope,
            warnings=warnings,
            source_conn=source_conn,
            dry_run=False,
        )
    migration_manifest_path.write_text(
        json.dumps(migration_manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    return {
        "dry_run": False,
        "fleet_manifest_path": str(fleet_manifest_path),
        "migration_manifest_path": str(migration_manifest_path),
        "children": manifest_children,
        "warnings": warnings,
    }
