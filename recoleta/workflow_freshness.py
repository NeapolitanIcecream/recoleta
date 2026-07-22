from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from recoleta.config import LLM_MODEL_CONFIG_FIELDS, Settings, resolve_stage_llm_model
from recoleta.types import sha256_hex

WORKFLOW_FRESHNESS_SCHEMA_VERSION = 1
_ANALYZE_BUDGET_CONFIG_SCHEMA_VERSION = 2
_ANALYZE_SOURCE_PROBE_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")
_MISSING_SETTING = object()
_SOURCE_CHUNK_BATCH_LIMIT = 1000
_PERSISTED_SOURCE_FINGERPRINT_FIELDS = (
    "schema_version",
    "key",
    "documents_total",
    "chunks_total",
    "source_scopes",
)


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


def workflow_freshness_diagnostics_view(
    freshness: dict[str, Any],
) -> dict[str, Any]:
    """Return a compact persisted view without changing the full fingerprint key."""
    view = dict(freshness)
    components = freshness.get("components")
    if not isinstance(components, dict):
        return view

    persisted_components = dict(components)
    upstream_sources = components.get("upstream_sources")
    if isinstance(upstream_sources, dict):
        persisted_components["upstream_sources"] = {
            field: upstream_sources[field]
            for field in _PERSISTED_SOURCE_FINGERPRINT_FIELDS
            if field in upstream_sources
        }
    view["components"] = persisted_components
    return view


def analyze_budget_config_fingerprint(
    settings: Any,
    *,
    llm_model: str | None = None,
) -> str:
    """Fingerprint Stage 4 semantics; the numeric budget is compared separately."""
    effective_model = resolve_stage_llm_model(
        settings,
        stage="analyze",
        override=llm_model,
    )
    identity = _analyze_budget_config_identity(
        settings,
        effective_model=effective_model,
    )
    return sha256_hex(
        json.dumps(
            identity,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            default=repr,
        )
    )


def _analyze_budget_config_identity(
    settings: Any,
    *,
    effective_model: str,
) -> dict[str, Any]:
    stage4_fields, missing_stage4_fields = _analyze_budget_stage4_fields(settings)
    return {
        "kind": "analyze_budget_config",
        "schema_version": _ANALYZE_BUDGET_CONFIG_SCHEMA_VERSION,
        "effective_analyze_llm_model": effective_model,
        **stage4_fields,
        "missing_stage4_fields": missing_stage4_fields,
    }


def _analyze_source_probe_multiplier(sources: Any) -> int:
    enabled_total = 0
    for source_name in _ANALYZE_SOURCE_PROBE_NAMES:
        source = getattr(sources, source_name, None)
        if source is None:
            continue
        enabled = getattr(source, "enabled", None)
        if enabled is None or bool(enabled):
            enabled_total += 1
    return 1 if enabled_total <= 1 else min(enabled_total, 5)


def _analyze_budget_stage4_fields(
    settings: Any,
) -> tuple[dict[str, Any], list[str]]:
    available: dict[str, Any] = {}
    missing: list[str] = []

    for field_name in (
        "llm_base_url",
        "llm_output_language",
        "analyze_content_max_chars",
    ):
        value = _identity_attribute(
            settings,
            field_name,
            path=field_name,
            missing=missing,
        )
        if value is not _MISSING_SETTING:
            available[field_name] = value

    topics = _identity_attribute(
        settings,
        "topics",
        path="topics",
        missing=missing,
    )
    if topics is not _MISSING_SETTING:
        available["topics"] = list(topics) if isinstance(topics, list) else topics
    triage_enabled = _identity_attribute(
        settings,
        "triage_enabled",
        path="triage_enabled",
        missing=missing,
    )
    if topics is not _MISSING_SETTING and triage_enabled is not _MISSING_SETTING:
        available["triage_required"] = bool(triage_enabled) and bool(topics)
    elif triage_enabled is not _MISSING_SETTING:
        available["triage_enabled"] = triage_enabled

    sources = _identity_attribute(
        settings,
        "sources",
        path="sources",
        missing=missing,
    )
    if sources is not _MISSING_SETTING:
        available["source_probe_multiplier"] = _analyze_source_probe_multiplier(
            sources
        )
        arxiv = _identity_attribute(
            sources,
            "arxiv",
            path="sources.arxiv",
            missing=missing,
        )
        if arxiv is not _MISSING_SETTING:
            arxiv_content: dict[str, Any] = {}
            for field_name in ("enrich_method", "enrich_failure_mode"):
                value = _identity_attribute(
                    arxiv,
                    field_name,
                    path=f"sources.arxiv.{field_name}",
                    missing=missing,
                )
                if value is not _MISSING_SETTING:
                    arxiv_content[field_name] = value
            if arxiv_content:
                available["arxiv_content"] = arxiv_content

    return available, sorted(missing)


def _identity_attribute(
    owner: Any,
    field_name: str,
    *,
    path: str,
    missing: list[str],
) -> Any:
    value = getattr(owner, field_name, _MISSING_SETTING)
    if value is _MISSING_SETTING:
        missing.append(path)
    return value


def _model_isolated_analyze_budget_config_fingerprint(
    settings: Any,
    *,
    llm_model: str | None,
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
    fingerprints = [
        analyze_budget_config_fingerprint(settings, llm_model=llm_model)
    ]
    if _supports_legacy_analyze_budget_fingerprints(settings):
        fingerprints.extend(
            (
                _model_isolated_analyze_budget_config_fingerprint(
                    settings,
                    llm_model=llm_model,
                ),
                _legacy_analyze_budget_config_fingerprint(
                    settings,
                    llm_model=llm_model,
                ),
                _pre_stage_model_analyze_budget_config_fingerprint(
                    settings,
                    llm_model=llm_model,
                ),
            )
        )
    return tuple(dict.fromkeys(value for value in fingerprints if value))


def _supports_legacy_analyze_budget_fingerprints(settings: Any) -> bool:
    settings_type = type(settings)
    return (
        isinstance(settings, Settings)
        and getattr(settings_type, "safe_model_dump", None)
        is Settings.safe_model_dump
        and getattr(settings_type, "safe_fingerprint", None)
        is Settings.safe_fingerprint
    )


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
    "workflow_freshness_diagnostics_view",
    "workflow_freshness_key",
]
