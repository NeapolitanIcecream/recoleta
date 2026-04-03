from __future__ import annotations

import json
import time
from threading import Event, Thread
from typing import Any, Callable

from loguru import logger

from recoleta.llm_costs import estimate_cost_usd_from_tokens as estimate_llm_cost_usd_from_tokens
from recoleta.rag.agent_models import (
    RepresentativeBackfillRequest,
    TrendGenerationRequest,
    TrendPromptRequest,
)
from recoleta.rag.search_helpers import truncate_text
from recoleta.trends import TREND_EVOLUTION_CHANGE_TYPE_VALUES, TrendCluster, TrendPayload

_RAW_TOOL_TRACE_MAX_EVENTS = 64
_RAW_TOOL_TRACE_MAX_ITEMS = 12
_RAW_TOOL_TRACE_MAX_DEPTH = 4
_RAW_TOOL_TRACE_MAX_TEXT_CHARS = 600


def _heartbeat_interval_seconds() -> float:
    from recoleta.rag import agent as rag_agent

    return float(getattr(rag_agent, "_TREND_AGENT_HEARTBEAT_INTERVAL_SECONDS", 15.0))


def _prompt_notes() -> list[str]:
    return [
        "Use tools to cite representative doc_id/chunk_index in clusters.",
        "Optimize for readability: short sentences, minimal jargon pile-ups, no repetitive filler.",
        "Keep claims grounded in the local corpus.",
        "Keep the title specific and remove date/generic prefixes.",
        "Keep topics only in metadata, not in overview_md body sections.",
        "Tools only access the active target period; use history_pack_md for same-granularity historical context when present.",
        "Leave evolution null unless history_pack_md provides usable prior-window evidence.",
        (
            "If evolution is present, evolution.signals[].change_type must be one of "
            + ", ".join(TREND_EVOLUTION_CHANGE_TYPE_VALUES)
            + "."
        ),
        "If evolution is present, evolution.signals[].history_windows must use only prev_n window_id values from history_pack_md and must not repeat the current period token.",
        "Evolution must be evidence-dense: name concrete papers, benchmarks, or systems and include specific factual details or metrics whenever available.",
        "When comparing against history, ground the delta in concrete historical titles, clusters, or representative systems from history_pack_md rather than generic phrases.",
        "If you mention a historical window in prose, use the exact prev_n token so publishing can render it as a link, and do not manually repeat the linked historical title immediately next to that token.",
        "If you cannot ground an evolution signal concretely, emit fewer signals instead of generic prose.",
        "Do not repeat the overview inside evolution; explain the delta across windows.",
    ]


def _prompt_payload_extras(
    request: TrendPromptRequest,
    payload: dict[str, Any],
) -> dict[str, Any]:
    if request.overview_pack_md is not None:
        payload["overview_pack_md"] = str(request.overview_pack_md)
    if request.history_pack_md is not None:
        payload["history_pack_md"] = str(request.history_pack_md)
    if request.rag_sources is not None:
        payload["rag_sources"] = request.rag_sources
    if request.ranking_n is not None:
        payload["ranking_n"] = int(request.ranking_n)
        notes = payload.get("notes")
        if isinstance(notes, list):
            notes.append(
                "ranking_n is legacy compatibility metadata; do not force a Top-N section unless explicitly requested."
            )
    if request.rep_source_doc_type is not None:
        normalized = str(request.rep_source_doc_type).strip().lower()
        if normalized:
            payload["rep_source_doc_type"] = normalized
    if request.evolution_max_signals is not None:
        payload["evolution_max_signals"] = int(request.evolution_max_signals)
    return payload


def build_trend_prompt_payload(request: TrendPromptRequest) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "task": "Generate research trends for the period.",
        "granularity": request.granularity,
        "period_start": request.period_start.isoformat(),
        "period_end": request.period_end.isoformat(),
        "corpus": {
            "doc_type": request.corpus_doc_type,
            "granularity": request.corpus_granularity,
        },
        "notes": _prompt_notes(),
        "evolution_change_types": list(TREND_EVOLUTION_CHANGE_TYPE_VALUES),
        "evolution_requirements": {
            "avoid_generic_summary": True,
            "prefer_concrete_titles": True,
            "prefer_named_history_anchors": True,
            "prefer_quantitative_details": True,
            "render_history_window_mentions": True,
            "use_fewer_signals_if_evidence_is_thin": True,
        },
    }
    return _prompt_payload_extras(request, payload)


def _normalized_representative(
    rep: Any,
) -> TrendCluster.RepresentativeChunk | None:
    try:
        doc_id = int(getattr(rep, "doc_id"))
        chunk_index = int(getattr(rep, "chunk_index"))
    except Exception:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    score_raw = getattr(rep, "score", None)
    try:
        score = float(score_raw) if score_raw is not None else None
    except Exception:
        score = None
    return TrendCluster.RepresentativeChunk(
        doc_id=doc_id,
        chunk_index=chunk_index,
        score=round(score, 6) if score is not None else None,
    )


def _backfilled_chunks_from_doc_ids(
    cluster: TrendCluster,
    *,
    max_reps: int,
) -> list[TrendCluster.RepresentativeChunk]:
    out: list[TrendCluster.RepresentativeChunk] = []
    for raw_doc_id in list(getattr(cluster, "representative_doc_ids", []) or []):
        try:
            doc_id = int(raw_doc_id)
        except Exception:
            continue
        if doc_id <= 0:
            continue
        out.append(TrendCluster.RepresentativeChunk(doc_id=doc_id, chunk_index=0, score=None))
        if len(out) >= max_reps:
            break
    return out


def _cluster_search_query(cluster: TrendCluster) -> str:
    return " ".join(
        [
            str(getattr(cluster, "name", "") or "").strip(),
            str(getattr(cluster, "description", "") or "").strip(),
        ]
    ).strip()


def _clean_representatives(
    cluster: TrendCluster,
    *,
    max_reps: int,
) -> tuple[list[TrendCluster.RepresentativeChunk], int]:
    raw_reps = list(cluster.representative_chunks or [])
    cleaned = [
        normalized
        for rep in raw_reps
        if (normalized := _normalized_representative(rep)) is not None
    ]
    return cleaned[:max_reps], max(0, len(raw_reps) - len(cleaned))


def _backfilled_chunks_from_search_rows(
    rows: list[Any],
    *,
    max_reps: int,
) -> list[TrendCluster.RepresentativeChunk]:
    backfilled: list[TrendCluster.RepresentativeChunk] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        normalized = _normalized_representative(type("Row", (), row)())
        if normalized is None:
            continue
        backfilled.append(normalized)
        if len(backfilled) >= max_reps:
            break
    return backfilled


def _backfilled_chunks(
    *,
    cluster: TrendCluster,
    search: Callable[[str, int], list[dict[str, Any]]],
    max_reps: int,
) -> list[TrendCluster.RepresentativeChunk]:
    query = _cluster_search_query(cluster)
    if query:
        try:
            rows = search(query, max_reps) or []
        except Exception as exc:
            logger.warning(
                "Representative search failed query={} error_type={} error={}",
                query,
                type(exc).__name__,
                str(exc),
            )
            rows = []
        backfilled = _backfilled_chunks_from_search_rows(
            rows,
            max_reps=max_reps,
        )
        if backfilled:
            return backfilled
    return _backfilled_chunks_from_doc_ids(cluster, max_reps=max_reps)


def _apply_cluster_representatives(
    cluster: TrendCluster,
    *,
    search: Callable[[str, int], list[dict[str, Any]]],
    max_reps: int,
) -> dict[str, int]:
    cleaned, invalid_reps_dropped_total = _clean_representatives(
        cluster,
        max_reps=max_reps,
    )
    if cleaned:
        cluster.representative_chunks = cleaned
        return {
            "clusters_backfilled_total": 0,
            "invalid_reps_dropped_total": invalid_reps_dropped_total,
            "reps_backfilled_total": 0,
        }
    backfilled = _backfilled_chunks(cluster=cluster, search=search, max_reps=max_reps)
    cluster.representative_chunks = backfilled
    return {
        "clusters_backfilled_total": 1 if backfilled else 0,
        "invalid_reps_dropped_total": invalid_reps_dropped_total,
        "reps_backfilled_total": len(backfilled),
    }


def ensure_trend_cluster_representatives_with_search(
    *,
    payload: TrendPayload,
    search: Callable[[str, int], list[dict[str, Any]]],
    max_reps: int = 6,
) -> dict[str, int]:
    clusters_total = len(payload.clusters or [])
    normalized_max_reps = max(0, int(max_reps or 0))
    if normalized_max_reps <= 0 or not payload.clusters:
        return {
            "clusters_total": clusters_total,
            "clusters_backfilled_total": 0,
            "invalid_reps_dropped_total": 0,
            "reps_backfilled_total": 0,
        }
    clusters_backfilled_total = 0
    invalid_reps_dropped_total = 0
    reps_backfilled_total = 0
    for cluster in payload.clusters:
        cluster_stats = _apply_cluster_representatives(
            cluster,
            search=search,
            max_reps=normalized_max_reps,
        )
        clusters_backfilled_total += int(cluster_stats["clusters_backfilled_total"])
        invalid_reps_dropped_total += int(cluster_stats["invalid_reps_dropped_total"])
        reps_backfilled_total += int(cluster_stats["reps_backfilled_total"])
    return {
        "clusters_total": clusters_total,
        "clusters_backfilled_total": clusters_backfilled_total,
        "invalid_reps_dropped_total": invalid_reps_dropped_total,
        "reps_backfilled_total": reps_backfilled_total,
    }


def ensure_trend_cluster_representatives(
    request: RepresentativeBackfillRequest,
) -> dict[str, int]:
    from recoleta.rag import agent as rag_agent

    return ensure_trend_cluster_representatives_with_search(
        payload=request.payload,
        search=lambda query, limit: [
            {
                "doc_id": hit.doc_id,
                "chunk_index": hit.chunk_index,
                "score": round(float(hit.score), 6),
            }
            for hit in rag_agent.semantic_search_summaries_in_period(
                repository=request.repository,
                vector_store=request.vector_store,
                run_id=request.run_id,
                doc_type=request.search_request(query=query, limit=limit).window.doc_type,
                granularity=request.search_request(query=query, limit=limit).window.granularity,
                period_start=request.period_start,
                period_end=request.period_end,
                query=query,
                embedding_model=request.embedding_model,
                embedding_dimensions=request.embedding_dimensions,
                max_batch_inputs=request.embedding_batch_max_inputs,
                max_batch_chars=request.embedding_batch_max_chars,
                embedding_failure_mode=request.embedding_failure_mode,
                embedding_max_errors=request.embedding_max_errors,
                limit=limit,
                metric_namespace=request.metric_namespace,
                llm_connection=request.llm_connection,
            )
        ],
        max_reps=request.max_reps,
    )


def _compact_mapping_value(value: dict[Any, Any], *, depth: int) -> dict[str, Any]:
    compacted_dict: dict[str, Any] = {}
    items = list(value.items())
    for key, item_value in items[:_RAW_TOOL_TRACE_MAX_ITEMS]:
        compacted_dict[str(key)] = _compact_tool_trace_value(item_value, depth=depth + 1)
    if len(items) > _RAW_TOOL_TRACE_MAX_ITEMS:
        compacted_dict["__truncated_items__"] = len(items) - _RAW_TOOL_TRACE_MAX_ITEMS
    return compacted_dict


def _compact_sequence_value(value: list[Any] | tuple[Any, ...], *, depth: int) -> list[Any]:
    compacted_list = [
        _compact_tool_trace_value(item, depth=depth + 1)
        for item in list(value)[:_RAW_TOOL_TRACE_MAX_ITEMS]
    ]
    if len(value) > _RAW_TOOL_TRACE_MAX_ITEMS:
        compacted_list.append({"__truncated_items__": len(value) - _RAW_TOOL_TRACE_MAX_ITEMS})
    return compacted_list


def _compact_model_dump(value: Any, *, depth: int) -> Any | None:
    model_dump = getattr(value, "model_dump", None)
    if not callable(model_dump):
        return None
    try:
        return _compact_tool_trace_value(model_dump(mode="json"), depth=depth + 1)
    except Exception:
        return None


def _compact_tool_trace_value(value: Any, *, depth: int = 0) -> Any:
    if value is None or isinstance(value, (bool, int, float)):
        return value
    if isinstance(value, str):
        return truncate_text(value, max_chars=_RAW_TOOL_TRACE_MAX_TEXT_CHARS)
    if depth >= _RAW_TOOL_TRACE_MAX_DEPTH:
        return truncate_text(str(value), max_chars=_RAW_TOOL_TRACE_MAX_TEXT_CHARS)
    if isinstance(value, dict):
        return _compact_mapping_value(value, depth=depth)
    if isinstance(value, (list, tuple)):
        return _compact_sequence_value(value, depth=depth)
    compacted = _compact_model_dump(value, depth=depth)
    if compacted is not None:
        return compacted
    return truncate_text(str(value), max_chars=_RAW_TOOL_TRACE_MAX_TEXT_CHARS)


def _tool_call_event(
    *,
    message_index: int,
    message_kind: str,
    part_index: int,
    part: Any,
    event_index: int,
) -> dict[str, Any]:
    return {
        "event_index": event_index,
        "message_index": message_index,
        "message_kind": message_kind,
        "part_index": part_index,
        "kind": "tool-call",
        "tool_name": str(getattr(part, "tool_name", "") or ""),
        "tool_call_id": str(getattr(part, "tool_call_id", "") or ""),
        "args": _compact_tool_trace_value(getattr(part, "args", None)),
    }


def _tool_return_content(part: Any) -> Any:
    raw_content = getattr(part, "content", None)
    model_response_object = getattr(part, "model_response_object", None)
    if callable(model_response_object) and not isinstance(raw_content, str):
        try:
            return model_response_object()
        except Exception:
            return getattr(part, "content", None)
    return raw_content


def _tool_return_event(
    *,
    message_index: int,
    message_kind: str,
    part_index: int,
    part: Any,
    event_index: int,
) -> dict[str, Any]:
    return {
        "event_index": event_index,
        "message_index": message_index,
        "message_kind": message_kind,
        "part_index": part_index,
        "kind": "tool-return",
        "tool_name": str(getattr(part, "tool_name", "") or ""),
        "tool_call_id": str(getattr(part, "tool_call_id", "") or ""),
        "content": _compact_tool_trace_value(_tool_return_content(part)),
    }


def _message_tool_trace_events(
    *,
    message_index: int,
    message_kind: str,
    parts: list[Any] | tuple[Any, ...],
    event_offset: int,
) -> tuple[list[dict[str, Any]], int]:
    events: list[dict[str, Any]] = []
    tool_calls_total = 0
    for part_index, part in enumerate(parts):
        part_kind = str(getattr(part, "part_kind", "") or "").strip()
        if part_kind == "tool-call":
            tool_calls_total += 1
            events.append(
                _tool_call_event(
                    message_index=message_index,
                    message_kind=message_kind,
                    part_index=part_index,
                    part=part,
                    event_index=event_offset + len(events),
                )
            )
            continue
        if part_kind == "tool-return":
            events.append(
                _tool_return_event(
                    message_index=message_index,
                    message_kind=message_kind,
                    part_index=part_index,
                    part=part,
                    event_index=event_offset + len(events),
                )
            )
    return events, tool_calls_total


def _extract_raw_tool_trace(messages: list[Any]) -> dict[str, Any]:
    if not messages:
        return {
            "status": "unavailable",
            "events": [],
            "events_total": 0,
            "tool_calls_total": 0,
            "events_truncated": False,
        }
    events: list[dict[str, Any]] = []
    tool_calls_total = 0
    for message_index, message in enumerate(messages):
        parts = getattr(message, "parts", None)
        if not isinstance(parts, (list, tuple)):
            continue
        message_events, message_tool_calls = _message_tool_trace_events(
            message_index=message_index,
            message_kind=str(getattr(message, "kind", "") or ""),
            parts=parts,
            event_offset=len(events),
        )
        events.extend(message_events)
        tool_calls_total += message_tool_calls
    events_total = len(events)
    return {
        "status": "captured",
        "events": events[:_RAW_TOOL_TRACE_MAX_EVENTS],
        "events_total": events_total,
        "tool_calls_total": tool_calls_total,
        "events_truncated": events_total > _RAW_TOOL_TRACE_MAX_EVENTS,
    }


def _summarize_tool_calls(messages: list[Any]) -> tuple[int, dict[str, int]]:
    total = 0
    breakdown: dict[str, int] = {}
    for message in messages:
        parts = getattr(message, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) != "tool-call":
                continue
            total += 1
            tool_name = str(getattr(part, "tool_name", "") or "").strip()
            if tool_name:
                breakdown[tool_name] = int(breakdown.get(tool_name, 0)) + 1
    return total, {name: breakdown[name] for name in sorted(breakdown)}


def _estimate_cost_usd_from_tokens(
    *,
    model: str,
    input_tokens: int | None,
    output_tokens: int | None,
) -> float | None:
    return estimate_llm_cost_usd_from_tokens(
        model=model,
        prompt_tokens=input_tokens,
        completion_tokens=output_tokens,
    )


def _record_metric(
    request: TrendGenerationRequest,
    *,
    name: str,
    value: float,
    unit: str | None = None,
) -> None:
    request.repository.record_metric(
        run_id=request.run_id,
        name=f"{request.metric_namespace}.{name}",
        value=value,
        unit=unit,
    )


def _start_trend_generation_heartbeat(
    *,
    log: Any,
    granularity: str,
    prompt_chars: int,
) -> tuple[Event, Thread]:
    stop_event = Event()
    started = time.perf_counter()
    interval_seconds = max(0.01, _heartbeat_interval_seconds())

    def _heartbeat() -> None:
        while not stop_event.wait(timeout=interval_seconds):
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            log.info(
                "Trend generation heartbeat granularity={} elapsed_ms={} prompt_chars={} tool_calls_observed_total={}",
                granularity,
                elapsed_ms,
                prompt_chars,
                0,
            )

    thread = Thread(
        target=_heartbeat,
        name=f"recoleta-trend-heartbeat-{granularity}",
        daemon=True,
    )
    thread.start()
    return stop_event, thread


def _agent_runtime_objects(
    request: TrendGenerationRequest,
) -> tuple[Any, Any]:
    from recoleta.rag.agent import TrendAgentDeps, build_trend_agent

    agent_kwargs: dict[str, Any] = {
        "llm_model": request.llm_model,
        "output_language": request.output_language,
    }
    if request.llm_connection is not None:
        agent_kwargs["llm_connection"] = request.llm_connection
    agent = build_trend_agent(**agent_kwargs)
    deps = TrendAgentDeps(
        repository=request.repository,
        vector_store=request.vector_store,
        run_id=request.run_id,
        metric_namespace=request.metric_namespace,
        period_start=request.period_start,
        period_end=request.period_end,
        rag_sources=request.rag_sources,
        embedding_model=request.embedding_model,
        embedding_dimensions=request.embedding_dimensions,
        embedding_batch_max_inputs=request.embedding_batch_max_inputs,
        embedding_batch_max_chars=request.embedding_batch_max_chars,
        embedding_failure_mode=str(request.embedding_failure_mode or "continue"),
        embedding_max_errors=int(request.embedding_max_errors or 0),
        llm_connection=request.llm_connection,
    )
    return agent, deps


def _run_agent_sync(
    request: TrendGenerationRequest,
    *,
    prompt: str,
    log: Any,
) -> tuple[Any, int]:
    agent, deps = _agent_runtime_objects(request)
    agent_started = time.perf_counter()
    stop_event, heartbeat_thread = _start_trend_generation_heartbeat(
        log=log,
        granularity=request.granularity,
        prompt_chars=len(prompt),
    )
    try:
        result = agent.run_sync(prompt, deps=deps)
    except Exception as exc:
        agent_duration_ms = int((time.perf_counter() - agent_started) * 1000)
        _record_metric(
            request,
            name="agent_run_sync.duration_ms",
            value=agent_duration_ms,
            unit="ms",
        )
        _record_metric(
            request,
            name="agent_run_sync.failed_total",
            value=1,
            unit="count",
        )
        log.warning(
            "Trend generation failed granularity={} elapsed_ms={} prompt_chars={} error_type={} error={}",
            request.granularity,
            agent_duration_ms,
            len(prompt),
            type(exc).__name__,
            str(exc),
        )
        raise
    finally:
        stop_event.set()
        heartbeat_thread.join(timeout=1.0)
    return result, int((time.perf_counter() - agent_started) * 1000)


def _record_backfill_metrics(
    *,
    request: TrendGenerationRequest,
    rep_stats: dict[str, int],
) -> None:
    if not rep_stats.get("invalid_reps_dropped_total", 0) and not rep_stats.get(
        "clusters_backfilled_total", 0
    ):
        return
    request.repository.record_metric(
        run_id=request.run_id,
        name=f"{request.metric_namespace}.cluster_representatives_backfilled_total",
        value=int(rep_stats.get("clusters_backfilled_total") or 0),
        unit="count",
    )
    request.repository.record_metric(
        run_id=request.run_id,
        name=f"{request.metric_namespace}.cluster_representatives_invalid_dropped_total",
        value=int(rep_stats.get("invalid_reps_dropped_total") or 0),
        unit="count",
    )


def _trend_prompt(request: TrendGenerationRequest) -> tuple[str, int]:
    prompt = json.dumps(
        build_trend_prompt_payload(request.prompt_request()),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    return prompt, len(prompt)


def _log_generation_start(
    *,
    log: Any,
    request: TrendGenerationRequest,
    prompt_chars: int,
) -> None:
    log.info(
        "Trend generation started granularity={} prompt_chars={} corpus_doc_type={} corpus_granularity={}",
        request.granularity,
        prompt_chars,
        request.corpus_doc_type,
        request.corpus_granularity or "-",
    )


def _record_agent_run_metrics(
    request: TrendGenerationRequest,
    *,
    agent_duration_ms: int,
) -> None:
    _record_metric(
        request,
        name="agent_run_sync.duration_ms",
        value=agent_duration_ms,
        unit="ms",
    )
    _record_metric(
        request,
        name="agent_run_sync.failed_total",
        value=0,
        unit="count",
    )


def _representative_backfill_request(
    request: TrendGenerationRequest,
    *,
    payload: TrendPayload,
) -> RepresentativeBackfillRequest:
    return RepresentativeBackfillRequest(
        payload=payload,
        repository=request.repository,
        vector_store=request.vector_store,
        run_id=request.run_id,
        period_start=request.period_start,
        period_end=request.period_end,
        rep_source_doc_type=request.rep_source_doc_type,
        embedding_model=request.embedding_model,
        embedding_dimensions=request.embedding_dimensions,
        embedding_batch_max_inputs=request.embedding_batch_max_inputs,
        embedding_batch_max_chars=request.embedding_batch_max_chars,
        embedding_failure_mode=request.embedding_failure_mode,
        embedding_max_errors=request.embedding_max_errors,
        metric_namespace=request.metric_namespace,
        llm_connection=request.llm_connection,
    )


def _run_representative_backfill(
    request: TrendGenerationRequest,
    *,
    payload: TrendPayload,
    log: Any,
) -> dict[str, int]:
    from recoleta.rag import agent as rag_agent

    rep_backfill_started = time.perf_counter()
    rep_stats = rag_agent.ensure_trend_cluster_representatives(
        request=_representative_backfill_request(request, payload=payload)
    )
    rep_backfill_duration_ms = int((time.perf_counter() - rep_backfill_started) * 1000)
    _record_metric(
        request,
        name="rep_backfill.duration_ms",
        value=rep_backfill_duration_ms,
        unit="ms",
    )
    log.info(
        "Trend representative backfill done granularity={} duration_ms={} clusters_backfilled_total={} invalid_reps_dropped_total={} reps_backfilled_total={}",
        request.granularity,
        rep_backfill_duration_ms,
        int(rep_stats.get("clusters_backfilled_total") or 0),
        int(rep_stats.get("invalid_reps_dropped_total") or 0),
        int(rep_stats.get("reps_backfilled_total") or 0),
    )
    return rep_stats


def _log_generation_done(
    *,
    log: Any,
    request: TrendGenerationRequest,
    agent_duration_ms: int,
    debug: dict[str, Any],
) -> None:
    log.info(
        "Trend generation done granularity={} elapsed_ms={} include_debug={} cost_present={} tool_calls_total={}",
        request.granularity,
        agent_duration_ms,
        bool(request.include_debug),
        debug.get("estimated_cost_usd") is not None,
        debug.get("tool_calls_total"),
    )


def _generation_debug_payload(
    *,
    request: TrendGenerationRequest,
    result: Any,
    prompt_chars: int,
) -> dict[str, Any]:
    usage = result.usage()
    messages_getter = getattr(result, "all_messages", None)
    raw_messages = messages_getter() if callable(messages_getter) else None
    messages: list[Any] = raw_messages if isinstance(raw_messages, list) else []
    tool_calls_total, tool_call_breakdown = _summarize_tool_calls(messages)
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    return {
        "usage": usage_dict,
        "estimated_cost_usd": _estimate_cost_usd_from_tokens(
            model=request.llm_model,
            input_tokens=getattr(usage, "input_tokens", None),
            output_tokens=getattr(usage, "output_tokens", None),
        ),
        "tool_calls_total": tool_calls_total,
        "tool_call_breakdown": tool_call_breakdown,
        "raw_tool_trace": _extract_raw_tool_trace(messages),
        "prompt_chars": prompt_chars,
        "overview_pack_chars": len(str(request.overview_pack_md or "")),
        "history_pack_chars": len(str(request.history_pack_md or "")),
    }


def generate_trend_payload(
    request: TrendGenerationRequest,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    log = logger.bind(module="rag.trend_agent", run_id=request.run_id)
    prompt, prompt_chars = _trend_prompt(request)
    _log_generation_start(log=log, request=request, prompt_chars=prompt_chars)
    result, agent_duration_ms = _run_agent_sync(request, prompt=prompt, log=log)
    _record_agent_run_metrics(request, agent_duration_ms=agent_duration_ms)
    payload = result.output
    rep_stats = _run_representative_backfill(request, payload=payload, log=log)
    try:
        _record_backfill_metrics(request=request, rep_stats=rep_stats)
    except Exception as metric_exc:
        log.warning(
            "Trend representative metrics failed error_type={} error={}",
            type(metric_exc).__name__,
            str(metric_exc),
        )
    debug = _generation_debug_payload(request=request, result=result, prompt_chars=prompt_chars)
    _log_generation_done(
        log=log,
        request=request,
        agent_duration_ms=agent_duration_ms,
        debug=debug,
    )
    return payload, debug
