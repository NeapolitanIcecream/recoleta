from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from recoleta.config import LLM_MODEL_CONFIG_FIELDS, resolve_stage_llm_model
from recoleta.types import sha256_hex

WORKFLOW_FRESHNESS_SCHEMA_VERSION = 1
_SOURCE_CHUNK_BATCH_LIMIT = 1000


@dataclass(frozen=True, slots=True)
class _SourceChunkQuery:
    doc_type: str
    granularity: str | None
    kind: str
    period_start: datetime
    period_end: datetime


@dataclass(frozen=True, slots=True)
class _SourceChunkBatch:
    rows: list[Any]
    outcome: str = "ok"


def workflow_freshness_key(freshness: dict[str, Any] | None) -> str | None:
    if not isinstance(freshness, dict):
        return None
    normalized = str(freshness.get("key") or "").strip()
    return normalized or None


def analyze_budget_config_fingerprint(
    settings: Any,
    *,
    llm_model: str | None = None,
) -> str:
    effective_model = resolve_stage_llm_model(
        settings,
        stage="analyze",
        override=llm_model,
    )
    payload = _safe_settings_payload(settings)
    if payload is None:
        return _legacy_analyze_budget_config_fingerprint(
            settings,
            llm_model=llm_model,
        )
    for field_name in LLM_MODEL_CONFIG_FIELDS:
        payload.pop(field_name, None)
    payload["effective_analyze_llm_model"] = effective_model
    return sha256_hex(
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def analyze_budget_config_fingerprint_candidates(
    settings: Any,
    *,
    llm_model: str | None = None,
) -> tuple[str, ...]:
    fingerprints = (
        analyze_budget_config_fingerprint(settings, llm_model=llm_model),
        _legacy_analyze_budget_config_fingerprint(settings, llm_model=llm_model),
        _pre_stage_model_analyze_budget_config_fingerprint(
            settings,
            llm_model=llm_model,
        ),
    )
    return tuple(dict.fromkeys(value for value in fingerprints if value))


def _legacy_analyze_budget_config_fingerprint(
    settings: Any,
    *,
    llm_model: str | None,
) -> str:
    base_fingerprint = _settings_fingerprint(settings)
    if not base_fingerprint:
        return ""
    configured_model = resolve_stage_llm_model(settings, stage="analyze")
    effective_model = resolve_stage_llm_model(
        settings,
        stage="analyze",
        override=llm_model,
    )
    if effective_model == configured_model:
        return base_fingerprint
    return sha256_hex(
        json.dumps(
            {
                "settings_fingerprint": base_fingerprint,
                "analyze_llm_model": effective_model,
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def _pre_stage_model_analyze_budget_config_fingerprint(
    settings: Any,
    *,
    llm_model: str | None,
) -> str:
    global_model = str(getattr(settings, "llm_model", "") or "").strip()
    effective_model = resolve_stage_llm_model(
        settings,
        stage="analyze",
        override=llm_model,
    )
    if not global_model or effective_model != global_model:
        return ""
    payload = _safe_settings_payload(settings)
    if payload is None:
        return ""
    for field_name in LLM_MODEL_CONFIG_FIELDS - {"llm_model"}:
        payload.pop(field_name, None)
    return sha256_hex(
        json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
        )
    )


def build_trend_synthesis_freshness(
    *,
    settings: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    llm_model: str | None = None,
    **options: Any,
) -> dict[str, Any]:
    repository = options.get("repository")
    source_fingerprint = options.get("source_fingerprint")
    analysis_model = options.get("analysis_model")
    components = _base_generation_components(
        kind="trend_synthesis",
        settings=settings,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        llm_model=llm_model,
    )
    components["analysis_model"] = (
        str(analysis_model or "").strip()
        or resolve_stage_llm_model(settings, stage="analyze")
    )
    if source_fingerprint is None and repository is not None:
        source_fingerprint = build_trend_source_fingerprint(
            repository=repository,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
        )
    if source_fingerprint is not None:
        components["upstream_sources"] = source_fingerprint
    return _freshness_payload(components)


def build_trend_source_fingerprint(
    *,
    repository: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> dict[str, Any]:
    source_scopes = _trend_source_scopes(granularity)
    chunks: list[dict[str, Any]] = []
    for scope in source_scopes:
        for kind in ("summary", "content", "meta"):
            chunks.extend(
                _source_chunk_rows(
                    repository=repository,
                    query=_SourceChunkQuery(
                        doc_type=str(scope["doc_type"]),
                        granularity=scope["granularity"],
                        kind=kind,
                        period_start=period_start,
                        period_end=period_end,
                    ),
                )
            )
    chunks.sort(key=_source_chunk_sort_key)
    document_keys = {
        (
            str(chunk.get("doc_type") or ""),
            chunk.get("granularity"),
            int(chunk.get("doc_id") or 0),
        )
        for chunk in chunks
    }
    components = {
        "schema_version": WORKFLOW_FRESHNESS_SCHEMA_VERSION,
        "granularity": str(granularity or "").strip().lower(),
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "source_scopes": source_scopes,
        "chunks": chunks,
    }
    serialized = json.dumps(components, ensure_ascii=False, sort_keys=True)
    return {
        "schema_version": WORKFLOW_FRESHNESS_SCHEMA_VERSION,
        "key": sha256_hex(serialized),
        "documents_total": len(document_keys),
        "chunks_total": len(chunks),
        "source_scopes": source_scopes,
        "chunks": chunks,
    }


def build_trend_ideas_freshness(
    *,
    settings: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    upstream_pass_output_id: int,
    llm_model: str | None = None,
) -> dict[str, Any]:
    components = _base_generation_components(
        kind="trend_ideas",
        settings=settings,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        llm_model=llm_model,
    )
    components["upstream_pass_output_id"] = int(upstream_pass_output_id)
    return _freshness_payload(components)


def _base_generation_components(
    *,
    kind: str,
    settings: Any,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    llm_model: str | None,
) -> dict[str, Any]:
    return {
        "schema_version": WORKFLOW_FRESHNESS_SCHEMA_VERSION,
        "kind": kind,
        "granularity": str(granularity or "").strip().lower(),
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "settings_fingerprint": _settings_generation_fingerprint(settings),
        "llm_model": resolve_stage_llm_model(
            settings,
            stage=_stage_for_generation_kind(kind),
            override=llm_model,
        ),
        "llm_output_language": str(
            getattr(settings, "llm_output_language", "") or ""
        ).strip(),
    }


def _stage_for_generation_kind(kind: str) -> str:
    normalized = str(kind or "").strip()
    if normalized == "trend_synthesis":
        return "trends"
    if normalized == "trend_ideas":
        return "ideas"
    raise ValueError("generation kind must be one of: trend_synthesis, trend_ideas")


def _settings_generation_fingerprint(settings: Any) -> str:
    payload = _safe_settings_payload(settings)
    if payload is not None:
        for field_name in LLM_MODEL_CONFIG_FIELDS:
            payload.pop(field_name, None)
        serialized = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return sha256_hex(serialized)
    return _settings_fingerprint(settings)


def _safe_settings_payload(settings: Any) -> dict[str, Any] | None:
    dumper = getattr(settings, "safe_model_dump", None)
    if not callable(dumper):
        return None
    try:
        payload = dumper()
    except Exception:
        return None
    return dict(payload) if isinstance(payload, dict) else None


def _settings_fingerprint(settings: Any) -> str:
    builder = getattr(settings, "safe_fingerprint", None)
    if not callable(builder):
        return ""
    try:
        return str(builder() or "").strip()
    except Exception:
        return ""


def _trend_source_scopes(granularity: str) -> list[dict[str, str | None]]:
    normalized = str(granularity or "").strip().lower()
    if normalized == "week":
        return [{"doc_type": "trend", "granularity": "day"}]
    if normalized == "month":
        return [{"doc_type": "trend", "granularity": "week"}]
    return [{"doc_type": "item", "granularity": None}]


def _source_chunk_rows(
    *,
    repository: Any,
    query: _SourceChunkQuery,
) -> list[dict[str, Any]]:
    lister = getattr(repository, "list_document_chunk_index_rows_in_period", None)
    if not callable(lister):
        return []
    rows: list[dict[str, Any]] = []
    offset = 0
    while True:
        batch = _source_chunk_batch(
            lister=lister,
            query=query,
            offset=offset,
        )
        if batch.outcome == "stop":
            return rows
        if batch.outcome == "failed":
            return []
        for row in batch.rows:
            normalized = _normalize_source_chunk_row(row)
            if normalized is not None:
                rows.append(normalized)
        if len(batch.rows) < _SOURCE_CHUNK_BATCH_LIMIT:
            return rows
        offset += _SOURCE_CHUNK_BATCH_LIMIT


def _source_chunk_batch(
    *,
    lister: Any,
    query: _SourceChunkQuery,
    offset: int,
) -> _SourceChunkBatch:
    try:
        batch = _call_source_chunk_lister(
            lister=lister,
            query=query,
            offset=offset,
        )
    except TypeError:
        if offset > 0:
            return _SourceChunkBatch(rows=[], outcome="stop")
        return _source_chunk_first_batch_without_offset(
            lister=lister,
            query=query,
        )
    except Exception:
        return _SourceChunkBatch(rows=[], outcome="failed")
    return _SourceChunkBatch(rows=list(batch) if batch is not None else [])


def _source_chunk_first_batch_without_offset(
    *,
    lister: Any,
    query: _SourceChunkQuery,
) -> _SourceChunkBatch:
    try:
        batch = lister(
            doc_type=query.doc_type,
            kind=query.kind,
            granularity=query.granularity,
            period_start=query.period_start,
            period_end=query.period_end,
            limit=_SOURCE_CHUNK_BATCH_LIMIT,
        )
    except Exception:
        return _SourceChunkBatch(rows=[], outcome="failed")
    return _SourceChunkBatch(rows=list(batch) if batch is not None else [])


def _call_source_chunk_lister(
    *,
    lister: Any,
    query: _SourceChunkQuery,
    offset: int,
) -> Any:
    return lister(
        doc_type=query.doc_type,
        kind=query.kind,
        granularity=query.granularity,
        period_start=query.period_start,
        period_end=query.period_end,
        limit=_SOURCE_CHUNK_BATCH_LIMIT,
        offset=offset,
    )


def _normalize_source_chunk_row(row: Any) -> dict[str, Any] | None:
    doc_id = _positive_int(_row_value(row, "doc_id"))
    chunk_index = _non_negative_int(_row_value(row, "chunk_index"))
    kind = str(_row_value(row, "kind") or "").strip().lower()
    text_hash = str(_row_value(row, "text_hash") or "").strip()
    if doc_id is None or chunk_index is None or kind not in {"summary", "content", "meta"}:
        return None
    return {
        "doc_id": doc_id,
        "doc_type": str(_row_value(row, "doc_type") or "").strip().lower(),
        "granularity": str(_row_value(row, "granularity") or "").strip().lower()
        or None,
        "chunk_index": chunk_index,
        "kind": kind,
        "text_hash": text_hash,
        "event_start": _iso_component(_row_value(row, "event_start_ts")),
        "event_end": _iso_component(_row_value(row, "event_end_ts")),
    }


def _source_chunk_sort_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row.get("doc_type") or "",
        row.get("granularity") or "",
        row.get("event_start") or "",
        row.get("event_end") or "",
        int(row.get("doc_id") or 0),
        row.get("kind") or "",
        int(row.get("chunk_index") or 0),
        row.get("text_hash") or "",
    )


def _row_value(row: Any, key: str) -> Any:
    if isinstance(row, dict):
        return row.get(key)
    return getattr(row, key, None)


def _positive_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except Exception:
        return None
    return parsed if parsed > 0 else None


def _non_negative_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except Exception:
        return None
    return parsed if parsed >= 0 else None


def _iso_component(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    normalized = str(value or "").strip()
    return normalized or None


def _freshness_payload(components: dict[str, Any]) -> dict[str, Any]:
    serialized = json.dumps(components, ensure_ascii=False, sort_keys=True)
    return {
        "schema_version": WORKFLOW_FRESHNESS_SCHEMA_VERSION,
        "kind": components.get("kind"),
        "key": sha256_hex(serialized),
        "components": components,
    }


__all__ = [
    "WORKFLOW_FRESHNESS_SCHEMA_VERSION",
    "build_trend_ideas_freshness",
    "build_trend_source_fingerprint",
    "build_trend_synthesis_freshness",
    "workflow_freshness_key",
]
