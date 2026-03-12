from __future__ import annotations

import hashlib
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Any, Protocol, cast

import orjson
from loguru import logger

from recoleta.config import TopicStreamRuntime
from recoleta.delivery import TelegramSender
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.ports import RepositoryPort, TrendStageRepositoryPort
from recoleta.publish import (
    build_telegram_trend_document_caption,
    export_trend_note_pdf_debug_bundle,
    render_trend_note_pdf_result,
    write_markdown_trend_note,
    write_obsidian_trend_note,
)
from recoleta.trend_materialize import (
    materialize_trend_note_payload,
    persist_materialized_trend_payload,
)
from recoleta import trends
from recoleta.types import DEFAULT_TOPIC_STREAM, TrendResult, utc_now


def _trend_metric_stream_token(scope: str) -> str:
    normalized_scope = str(scope or "").strip().lower()
    return (
        "".join(ch if ch.isalnum() else "_" for ch in normalized_scope).strip("_")
        or "unknown"
    )


def _trend_metric_name(name: str, *, scope: str) -> str:
    normalized_name = str(name or "").strip()
    normalized_scope = str(scope or "").strip() or DEFAULT_TOPIC_STREAM
    if normalized_scope == DEFAULT_TOPIC_STREAM:
        return normalized_name
    stream_prefix = (
        f"pipeline.trends.stream.{_trend_metric_stream_token(normalized_scope)}"
    )
    if normalized_name == "pipeline.trends":
        return stream_prefix
    if not normalized_name.startswith("pipeline.trends."):
        return normalized_name
    suffix = normalized_name.removeprefix("pipeline.trends.")
    return f"{stream_prefix}.{suffix}"


class TrendStageService(Protocol):
    settings: Any
    analyzer: Any
    semantic_triage: Any
    telegram_sender: Any | None
    _topic_streams: list[TopicStreamRuntime]
    _explicit_topic_streams: bool
    _llm_connection: Any

    @property
    def repository(self) -> TrendStageRepositoryPort: ...

    def trends(
        self,
        *,
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
        backfill: bool = False,
        backfill_mode: str = "missing",
        debug_pdf: bool = False,
    ) -> TrendResult: ...

    def _settings_for_topic_stream(self, stream: TopicStreamRuntime) -> Any: ...

    def _telegram_sender_for_stream(self, stream: TopicStreamRuntime) -> Any: ...

    def _telegram_delivery_destination(self) -> str: ...

    def _telegram_delivery_budget(self) -> tuple[str, int, int]: ...

    def _sanitize_error_message(self, message: str) -> str: ...

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None: ...

    def prepare(
        self,
        *,
        run_id: str,
        period_start: Any = None,
        period_end: Any = None,
    ) -> Any: ...

    def analyze(
        self,
        *,
        run_id: str,
        period_start: Any = None,
        period_end: Any = None,
    ) -> Any: ...

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]: ...


def run_trends_stage(
    service: TrendStageService,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
    backfill: bool = False,
    backfill_mode: str = "missing",
    debug_pdf: bool = False,
    scope: str = DEFAULT_TOPIC_STREAM,
) -> TrendResult:
    if service._explicit_topic_streams:
        return run_trends_topic_streams_stage(
            service,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
        )
    log = logger.bind(module="pipeline.trends", run_id=run_id)
    metric_namespace = _trend_metric_name("pipeline.trends", scope=scope)
    started = time.perf_counter()
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity not in {"day", "week", "month"}:
        raise ValueError("granularity must be one of: day, week, month")
    anchor = anchor_date or utc_now().date()

    index_stats: dict[str, Any] = {}

    def record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        service.repository.record_metric(
            run_id=run_id,
            name=_trend_metric_name(name, scope=scope),
            value=value,
            unit=unit,
        )

    try:
        include_debug = bool(
            service.settings.write_debug_artifacts
            and service.settings.artifacts_dir is not None
        )

        def _record_index_metrics(stats: dict[str, Any], *, failed: bool) -> None:
            record_metric(
                name="pipeline.trends.index.items_total",
                value=float(stats.get("items_total") or 0),
                unit="count",
            )
            record_metric(
                name="pipeline.trends.index.docs_upserted_total",
                value=float(stats.get("docs_upserted") or 0),
                unit="count",
            )
            record_metric(
                name="pipeline.trends.index.docs_deleted_total",
                value=float(stats.get("docs_deleted") or 0),
                unit="count",
            )
            record_metric(
                name="pipeline.trends.index.chunks_upserted_total",
                value=float(stats.get("chunks_upserted") or 0),
                unit="count",
            )
            record_metric(
                name="pipeline.trends.index.items_filtered_out_total",
                value=float(stats.get("items_filtered_out") or 0),
                unit="count",
            )
            record_metric(
                name="pipeline.trends.index.duration_ms",
                value=float(stats.get("duration_ms") or 0),
                unit="ms",
            )
            record_metric(
                name="pipeline.trends.index.failed_total",
                value=1 if failed else 0,
                unit="count",
            )

        def _index_items_for_period(*, required: bool) -> dict[str, Any]:
            try:
                stats = trends.index_items_as_documents(
                    repository=cast(Any, service.repository),
                    run_id=run_id,
                    period_start=period_start,
                    period_end=period_end,
                    min_relevance_score=float(
                        getattr(service.settings, "min_relevance_score", 0.0) or 0.0
                    ),
                    scope=scope,
                )
            except Exception as exc:
                failed_stats = {
                    "items_total": 0,
                    "docs_upserted": 0,
                    "chunks_upserted": 0,
                    "duration_ms": 0,
                }
                _record_index_metrics(failed_stats, failed=True)
                log.warning(
                    "Trends index failed granularity={} period_start={} period_end={} error_type={} error={}",
                    normalized_granularity,
                    period_start.isoformat(),
                    period_end.isoformat(),
                    type(exc).__name__,
                    service._sanitize_error_message(str(exc)),
                )
                if required:
                    raise
                return failed_stats
            _record_index_metrics(stats, failed=False)
            return stats

        def _prepare_period_backlog() -> None:
            service.prepare(
                run_id=run_id,
                period_start=period_start,
                period_end=period_end,
            )
            service.analyze(
                run_id=run_id,
                period_start=period_start,
                period_end=period_end,
            )

        if normalized_granularity == "day":
            period_start, period_end = trends.day_period_bounds(anchor)
            corpus_doc_type = "item"
            corpus_granularity: str | None = None
            _prepare_period_backlog()
            index_stats = _index_items_for_period(required=True)
        elif normalized_granularity == "week":
            period_start, period_end = trends.week_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "day"
            _prepare_period_backlog()
            index_stats = _index_items_for_period(required=False)
        else:
            period_start, period_end = trends.month_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "week"
            _prepare_period_backlog()
            index_stats = _index_items_for_period(required=False)

        model = llm_model or service.settings.llm_model

        normalized_backfill_mode = str(backfill_mode or "missing").strip().lower()
        if normalized_backfill_mode not in {"missing", "all"}:
            raise ValueError("backfill_mode must be one of: missing, all")

        prev_granularity = cast(Any, trends).prev_level_for_granularity(
            normalized_granularity
        )
        if bool(backfill) and prev_granularity in {"day", "week"}:
            backfill_started = time.perf_counter()
            backfill_days_total = 0
            backfill_missing_total = 0
            backfill_generated_total = 0
            backfill_skipped_total = 0
            backfill_failed_total = 0

            if prev_granularity == "day":
                backfill_days_total = 7
                week_start_day = period_start.date()
                for offset in range(backfill_days_total):
                    day = week_start_day + timedelta(days=offset)
                    day_start, day_end = trends.day_period_bounds(day)
                    existing = cast(Any, service.repository).list_documents(
                        doc_type="trend",
                        granularity="day",
                        period_start=day_start,
                        period_end=day_end,
                        scope=scope,
                        order_by="event_desc",
                        offset=0,
                        limit=1,
                    )
                    is_missing = not bool(existing)
                    if is_missing:
                        backfill_missing_total += 1
                    if normalized_backfill_mode == "missing" and not is_missing:
                        backfill_skipped_total += 1
                        continue
                    try:
                        _ = run_trends_stage(
                            service,
                            run_id=run_id,
                            granularity="day",
                            anchor_date=day,
                            llm_model=model,
                            backfill=False,
                            backfill_mode="missing",
                            scope=scope,
                        )
                        backfill_generated_total += 1
                    except Exception as day_exc:  # noqa: BLE001
                        backfill_failed_total += 1
                        log.warning(
                            "Trends week backfill failed day={} error_type={} error={}",
                            day.isoformat(),
                            type(day_exc).__name__,
                            service._sanitize_error_message(str(day_exc)),
                        )
            else:
                cursor = period_start.date()
                while True:
                    week_start, week_end = trends.week_period_bounds(cursor)
                    if week_start >= period_end:
                        break
                    backfill_days_total += 1
                    existing = cast(Any, service.repository).list_documents(
                        doc_type="trend",
                        granularity="week",
                        period_start=week_start,
                        period_end=week_end,
                        scope=scope,
                        order_by="event_desc",
                        offset=0,
                        limit=1,
                    )
                    is_missing = not bool(existing)
                    if is_missing:
                        backfill_missing_total += 1
                    if normalized_backfill_mode == "missing" and not is_missing:
                        backfill_skipped_total += 1
                        cursor = (week_start + timedelta(days=7)).date()
                        continue
                    try:
                        _ = run_trends_stage(
                            service,
                            run_id=run_id,
                            granularity="week",
                            anchor_date=week_start.date(),
                            llm_model=model,
                            backfill=False,
                            backfill_mode="missing",
                            scope=scope,
                        )
                        backfill_generated_total += 1
                    except Exception as week_exc:  # noqa: BLE001
                        backfill_failed_total += 1
                        log.warning(
                            "Trends month backfill failed week_start={} error_type={} error={}",
                            week_start.date().isoformat(),
                            type(week_exc).__name__,
                            service._sanitize_error_message(str(week_exc)),
                        )
                    cursor = (week_start + timedelta(days=7)).date()

            backfill_duration_ms = int((time.perf_counter() - backfill_started) * 1000)
            backfill_stats = {
                "days_total": backfill_days_total,
                "missing_total": backfill_missing_total,
                "generated_total": backfill_generated_total,
                "skipped_total": backfill_skipped_total,
                "failed_total": backfill_failed_total,
                "duration_ms": backfill_duration_ms,
                "mode": normalized_backfill_mode,
            }
            log_label = "week" if prev_granularity == "day" else "month"
            log.info("Trends {} backfill done stats={}", log_label, backfill_stats)
            record_metric(
                name="pipeline.trends.backfill.days_total",
                value=backfill_days_total,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.backfill.missing_total",
                value=backfill_missing_total,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.backfill.generated_total",
                value=backfill_generated_total,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.backfill.skipped_total",
                value=backfill_skipped_total,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.backfill.failed_total",
                value=backfill_failed_total,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.backfill.duration_ms",
                value=backfill_duration_ms,
                unit="ms",
            )

        corpus_docs_total = 0
        if corpus_doc_type == "item":
            corpus_docs_total = int(index_stats.get("docs_upserted") or 0)
        else:
            probe = cast(Any, service.repository).list_documents(
                doc_type="trend",
                granularity=corpus_granularity,
                period_start=period_start,
                period_end=period_end,
                scope=scope,
                order_by="event_desc",
                offset=0,
                limit=1,
            )
            corpus_docs_total = 1 if probe else 0

        record_metric(
            name="pipeline.trends.corpus.docs_total",
            value=corpus_docs_total,
            unit="count",
        )
        empty_corpus = corpus_docs_total <= 0

        if empty_corpus:
            log.info(
                "Trends corpus is empty; skipping LLM invocation granularity={} period_start={} period_end={}",
                normalized_granularity,
                period_start.isoformat(),
                period_end.isoformat(),
            )
            record_metric(
                name="pipeline.trends.corpus.empty",
                value=1.0,
                unit="bool",
            )
            payload = trends.build_empty_trend_payload(
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                output_language=service.settings.llm_output_language,
            )
            debug = {"empty_corpus": True} if include_debug else None
            record_metric(
                name="pipeline.trends.llm_requests_total",
                value=0,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.llm_input_tokens_total",
                value=0,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.llm_output_tokens_total",
                value=0,
                unit="count",
            )
            record_metric(
                name="pipeline.trends.estimated_cost_usd",
                value=0.0,
                unit="usd",
            )
        else:
            record_metric(
                name="pipeline.trends.corpus.empty",
                value=0.0,
                unit="bool",
            )
            overview_pack_md: str | None = None
            rag_sources: list[dict[str, str | None]] | None = None
            ranking_n: int | None = None
            rep_source_doc_type: str | None = None
            if bool(getattr(service.settings, "trends_self_similar_enabled", False)):
                plan = trends.TrendGenerationPlan(
                    target_granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                )
                overview_pack_md, pack_stats = trends.build_overview_pack_md(
                    cast(Any, service.repository),
                    plan,
                    overview_pack_max_chars=int(
                        getattr(
                            service.settings, "trends_overview_pack_max_chars", 8000
                        )
                        or 8000
                    ),
                    item_overview_top_k=int(
                        getattr(service.settings, "trends_item_overview_top_k", 20)
                        or 20
                    ),
                    item_overview_item_max_chars=int(
                        getattr(
                            service.settings, "trends_item_overview_item_max_chars", 500
                        )
                        or 500
                    ),
                    min_relevance_score=float(
                        getattr(service.settings, "min_relevance_score", 0.0) or 0.0
                    ),
                    scope=scope,
                )
                rag_sources = list(getattr(plan, "rag_sources", []) or [])
                ranking_n = int(getattr(service.settings, "trends_ranking_n", 10) or 10)
                rep_source_doc_type = str(
                    getattr(plan, "rep_source_doc_type", "item") or "item"
                ).strip()
                if isinstance(pack_stats, dict) and bool(pack_stats.get("truncated")):
                    record_metric(
                        name="pipeline.trends.overview_pack.truncated_total",
                        value=1,
                        unit="count",
                    )
            payload, debug = trends.generate_trend_via_tools(
                repository=cast(Any, service.repository),
                run_id=run_id,
                llm_model=model,
                output_language=service.settings.llm_output_language,
                embedding_model=service.settings.trends_embedding_model,
                embedding_dimensions=service.settings.trends_embedding_dimensions,
                embedding_batch_max_inputs=service.settings.trends_embedding_batch_max_inputs,
                embedding_batch_max_chars=service.settings.trends_embedding_batch_max_chars,
                embedding_failure_mode=getattr(
                    service.settings, "trends_embedding_failure_mode", "continue"
                ),
                embedding_max_errors=int(
                    getattr(service.settings, "trends_embedding_max_errors", 0) or 0
                ),
                lancedb_dir=service.settings.rag_lancedb_dir,
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                corpus_doc_type=corpus_doc_type,
                corpus_granularity=corpus_granularity,
                overview_pack_md=overview_pack_md,
                rag_sources=rag_sources,
                ranking_n=ranking_n,
                rep_source_doc_type=rep_source_doc_type,
                include_debug=include_debug,
                scope=scope,
                metric_namespace=metric_namespace,
                llm_connection=service._llm_connection,
            )
            if isinstance(debug, dict):
                usage = debug.get("usage")
                if isinstance(usage, dict):
                    requests = usage.get("requests")
                    input_tokens = usage.get("input_tokens")
                    output_tokens = usage.get("output_tokens")
                    if isinstance(requests, (int, float)):
                        record_metric(
                            name="pipeline.trends.llm_requests_total",
                            value=float(requests),
                            unit="count",
                        )
                    if isinstance(input_tokens, (int, float)):
                        record_metric(
                            name="pipeline.trends.llm_input_tokens_total",
                            value=float(input_tokens),
                            unit="count",
                        )
                    if isinstance(output_tokens, (int, float)):
                        record_metric(
                            name="pipeline.trends.llm_output_tokens_total",
                            value=float(output_tokens),
                            unit="count",
                        )
                prompt_chars = debug.get("prompt_chars")
                if isinstance(prompt_chars, (int, float)):
                    record_metric(
                        name="pipeline.trends.prompt_chars",
                        value=float(prompt_chars),
                        unit="chars",
                    )
                overview_pack_chars = debug.get("overview_pack_chars")
                if isinstance(overview_pack_chars, (int, float)):
                    record_metric(
                        name="pipeline.trends.overview_pack.chars",
                        value=float(overview_pack_chars),
                        unit="chars",
                    )
                cost_usd = debug.get("estimated_cost_usd")
                if isinstance(cost_usd, (int, float)):
                    record_metric(
                        name="pipeline.trends.estimated_cost_usd",
                        value=float(cost_usd),
                        unit="usd",
                    )
                else:
                    record_metric(
                        name="pipeline.trends.cost_missing_total",
                        value=1,
                        unit="count",
                    )

        rep_dropped_non_item_total = 0
        rep_backfilled_total = 0
        rep_failed_clusters_total = 0

        rep_doc_type_cache: dict[int, str | None] = {}

        def _doc_type_for_doc_id(doc_id_value: int) -> str | None:
            normalized_doc_id = int(doc_id_value)
            if normalized_doc_id <= 0:
                return None
            if normalized_doc_id not in rep_doc_type_cache:
                doc = cast(Any, service.repository).get_document(
                    doc_id=normalized_doc_id
                )
                if doc is None:
                    rep_doc_type_cache[normalized_doc_id] = None
                else:
                    rep_doc_type_cache[normalized_doc_id] = (
                        str(getattr(doc, "doc_type", "") or "").strip().lower() or None
                    )
            return rep_doc_type_cache.get(normalized_doc_id)

        def _cluster_queries(cluster: Any) -> list[str]:
            name = str(getattr(cluster, "name", "") or "").strip()
            desc = str(getattr(cluster, "description", "") or "").strip()
            candidates = [" ".join([name, desc]).strip(), name, desc]
            out: list[str] = []
            seen: set[str] = set()
            for candidate in candidates:
                normalized = " ".join(str(candidate or "").split()).strip()
                if not normalized or normalized in seen:
                    continue
                seen.add(normalized)
                out.append(normalized)
            return out

        def _backfill_item_reps_text(cluster: Any, *, limit: int) -> list[Any]:
            reps: list[Any] = []
            seen: set[tuple[int, int]] = set()
            for query in _cluster_queries(cluster):
                try:
                    rows = cast(Any, service.repository).search_chunks_text(
                        query=query,
                        doc_type="item",
                        period_start=period_start,
                        period_end=period_end,
                        scope=scope,
                        limit=limit,
                    )
                except Exception:
                    rows = []
                for row in rows or []:
                    if not isinstance(row, dict):
                        continue
                    raw_doc_id = row.get("doc_id")
                    raw_chunk_index = row.get("chunk_index")
                    if raw_doc_id is None or raw_chunk_index is None:
                        continue
                    try:
                        doc_id_int = int(raw_doc_id)
                        chunk_index_int = int(raw_chunk_index)
                    except Exception:
                        continue
                    if doc_id_int <= 0 or chunk_index_int < 0:
                        continue
                    key = (doc_id_int, chunk_index_int)
                    if key in seen:
                        continue
                    seen.add(key)
                    reps.append(
                        trends.TrendCluster.RepresentativeChunk(
                            doc_id=doc_id_int,
                            chunk_index=chunk_index_int,
                            score=None,
                        )
                    )
                    if len(reps) >= limit:
                        return reps
            return reps

        def _backfill_item_reps_semantic(cluster: Any, *, limit: int) -> list[Any]:
            queries = _cluster_queries(cluster)
            if not queries:
                return []
            query = queries[0]
            try:
                hits = trends.semantic_search_summaries_in_period(
                    repository=cast(Any, service.repository),
                    lancedb_dir=service.settings.rag_lancedb_dir,
                    run_id=run_id,
                    doc_type="item",
                    period_start=period_start,
                    period_end=period_end,
                    query=query,
                    embedding_model=service.settings.trends_embedding_model,
                    embedding_dimensions=service.settings.trends_embedding_dimensions,
                    max_batch_inputs=service.settings.trends_embedding_batch_max_inputs,
                    max_batch_chars=service.settings.trends_embedding_batch_max_chars,
                    embedding_failure_mode=getattr(
                        service.settings, "trends_embedding_failure_mode", "continue"
                    ),
                    embedding_max_errors=int(
                        getattr(service.settings, "trends_embedding_max_errors", 0) or 0
                    ),
                    limit=limit,
                    scope=scope,
                    metric_namespace=metric_namespace,
                    llm_connection=service._llm_connection,
                )
            except Exception:
                return []
            reps: list[Any] = []
            seen: set[tuple[int, int]] = set()
            for hit in hits or []:
                try:
                    doc_id_int = int(getattr(hit, "doc_id"))
                    chunk_index_int = int(getattr(hit, "chunk_index"))
                except Exception:
                    continue
                if doc_id_int <= 0 or chunk_index_int < 0:
                    continue
                key = (doc_id_int, chunk_index_int)
                if key in seen:
                    continue
                seen.add(key)
                score_raw = getattr(hit, "score", None)
                score_value: float | None
                if score_raw is None:
                    score_value = None
                else:
                    try:
                        score_value = float(score_raw)
                    except Exception:
                        score_value = None
                reps.append(
                    trends.TrendCluster.RepresentativeChunk(
                        doc_id=doc_id_int,
                        chunk_index=chunk_index_int,
                        score=round(score_value, 6)
                        if score_value is not None
                        else None,
                    )
                )
                if len(reps) >= limit:
                    break
            return reps

        def _rep_chunk_key(rep: Any) -> tuple[int, int] | None:
            try:
                doc_id_int = int(getattr(rep, "doc_id"))
                chunk_index_int = int(getattr(rep, "chunk_index"))
            except Exception:
                return None
            if doc_id_int <= 0 or chunk_index_int < 0:
                return None
            return doc_id_int, chunk_index_int

        max_reps = 6
        for cluster in list(getattr(payload, "clusters", []) or []):
            cleaned: list[Any] = []
            seen_rep_keys: set[tuple[int, int]] = set()
            for rep in list(getattr(cluster, "representative_chunks", []) or []):
                rep_key = _rep_chunk_key(rep)
                if rep_key is None:
                    continue
                doc_id_int, _chunk_index_int = rep_key
                doc_type = _doc_type_for_doc_id(doc_id_int)
                if doc_type != "item":
                    rep_dropped_non_item_total += 1
                    continue
                if rep_key in seen_rep_keys:
                    continue
                seen_rep_keys.add(rep_key)
                cleaned.append(rep)
            cluster.representative_chunks = cleaned[:max_reps]
            if cluster.representative_chunks:
                continue
            backfilled = _backfill_item_reps_text(cluster, limit=max_reps)
            if not backfilled:
                backfilled = _backfill_item_reps_semantic(cluster, limit=max_reps)
            if backfilled:
                cluster.representative_chunks = backfilled[:max_reps]
                rep_backfilled_total += 1
            else:
                cluster.representative_chunks = []
                rep_failed_clusters_total += 1

        record_metric(
            name="pipeline.trends.rep_enforcement.dropped_non_item_total",
            value=rep_dropped_non_item_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.rep_enforcement.backfilled_total",
            value=rep_backfilled_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.rep_enforcement.failed_clusters_total",
            value=rep_failed_clusters_total,
            unit="count",
        )

        materialized = materialize_trend_note_payload(
            repository=cast(Any, service.repository),
            payload=payload,
            markdown_output_dir=service.settings.markdown_output_dir,
            output_language=service.settings.llm_output_language,
        )
        payload = persist_materialized_trend_payload(
            payload=payload,
            materialized=materialized,
        )
        doc_id = trends.persist_trend_payload(
            repository=cast(Any, service.repository),
            granularity=normalized_granularity,
            period_start=period_start,
            period_end=period_end,
            payload=payload,
            scope=scope,
        )

        rewrite_occurrences_total = materialized.rewrite_stats.doc_ref_occurrences_total
        rewrite_doc_ids_resolved_total = materialized.rewrite_stats.doc_ref_resolved_total
        rewrite_doc_ids_unresolved_total = (
            materialized.rewrite_stats.doc_ref_unresolved_total
        )

        if rewrite_occurrences_total or rewrite_doc_ids_unresolved_total:
            log.info(
                "Trend note doc refs rewritten occurrences={} resolved_doc_ids={} unresolved_doc_ids={}",
                rewrite_occurrences_total,
                rewrite_doc_ids_resolved_total,
                rewrite_doc_ids_unresolved_total,
            )
        record_metric(
            name="pipeline.trends.note_doc_refs_rewrite_occurrences_total",
            value=rewrite_occurrences_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.note_doc_refs_resolved_total",
            value=rewrite_doc_ids_resolved_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.note_doc_refs_unresolved_total",
            value=rewrite_doc_ids_unresolved_total,
            unit="count",
        )

        trend_delivery_hash = hashlib.sha256(
            orjson.dumps(
                {
                    "title": materialized.title,
                    "granularity": normalized_granularity,
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "overview_md": materialized.overview_md,
                    "topics": list(payload.topics),
                    "clusters": materialized.clusters,
                },
                option=orjson.OPT_SORT_KEYS,
            )
        ).hexdigest()

        targets = set(service.settings.publish_targets or [])
        if "obsidian" in targets and service.settings.obsidian_vault_path is None:
            raise ValueError(
                "OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'"
            )
        if "telegram" in targets and service.telegram_sender is None:
            if (
                service.settings.telegram_bot_token is None
                or service.settings.telegram_chat_id is None
            ):
                raise ValueError(
                    "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required when PUBLISH_TARGETS includes 'telegram'"
                )
            service.telegram_sender = TelegramSender(
                token=service.settings.telegram_bot_token.get_secret_value(),
                chat_id=service.settings.telegram_chat_id.get_secret_value(),
            )

        repository_any = cast(Any, service.repository)
        telegram_destination = service._telegram_delivery_destination()
        telegram_remaining_today: int | None = None
        telegram_already_sent = False
        if "telegram" in targets:
            (
                _,
                _,
                telegram_remaining_today,
            ) = service._telegram_delivery_budget()
        if (
            "telegram" in targets
            and not empty_corpus
            and telegram_remaining_today is not None
            and telegram_remaining_today > 0
        ):
            telegram_already_sent = bool(
                repository_any.has_sent_trend_delivery(
                    doc_id=doc_id,
                    channel=DELIVERY_CHANNEL_TELEGRAM,
                    destination=telegram_destination,
                    content_hash=trend_delivery_hash,
                )
            )

        markdown_note_path: Path | None = None
        pdf_generated_total = 0
        pdf_failed_total = 0
        pdf_debug_generated_total = 0
        pdf_debug_failed_total = 0
        pdf_browser_generated_total = 0
        pdf_story_generated_total = 0
        telegram_sent_total = 0
        telegram_failed_total = 0

        telegram_can_attempt_delivery = (
            "telegram" in targets
            and not empty_corpus
            and telegram_remaining_today is not None
            and telegram_remaining_today > 0
            and not telegram_already_sent
        )

        if "markdown" in targets or telegram_can_attempt_delivery:
            try:
                markdown_note_path = write_markdown_trend_note(
                    output_dir=service.settings.markdown_output_dir,
                    trend_doc_id=doc_id,
                    title=materialized.title,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    run_id=run_id,
                    overview_md=materialized.overview_md,
                    topics=list(payload.topics),
                    clusters=materialized.clusters,
                    highlights=materialized.highlights,
                )
            except Exception as note_exc:  # noqa: BLE001
                log.bind(module="pipeline.trends.markdown_note").warning(
                    "Trend markdown note write failed: {}",
                    service._sanitize_error_message(str(note_exc)),
                )
        if "obsidian" in targets and service.settings.obsidian_vault_path is not None:
            try:
                write_obsidian_trend_note(
                    vault_path=service.settings.obsidian_vault_path,
                    base_folder=service.settings.obsidian_base_folder,
                    trend_doc_id=doc_id,
                    title=materialized.title,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    run_id=run_id,
                    overview_md=materialized.overview_md,
                    topics=list(payload.topics),
                    clusters=materialized.clusters,
                    highlights=materialized.highlights,
                )
            except Exception as note_exc:  # noqa: BLE001
                log.bind(module="pipeline.trends.obsidian_note").warning(
                    "Trend obsidian note write failed: {}",
                    service._sanitize_error_message(str(note_exc)),
                )

        if "telegram" in targets:
            if empty_corpus:
                log.info(
                    "Trend Telegram delivery skipped for empty corpus doc_id={} granularity={} period_start={} period_end={}",
                    doc_id,
                    normalized_granularity,
                    period_start.isoformat(),
                    period_end.isoformat(),
                )
            elif telegram_remaining_today is not None and telegram_remaining_today <= 0:
                log.info(
                    "Trend Telegram delivery skipped for daily cap doc_id={} granularity={} period_start={} period_end={}",
                    doc_id,
                    normalized_granularity,
                    period_start.isoformat(),
                    period_end.isoformat(),
                )
            elif telegram_already_sent:
                log.info(
                    "Trend Telegram delivery skipped for unchanged content doc_id={} granularity={} period_start={} period_end={}",
                    doc_id,
                    normalized_granularity,
                    period_start.isoformat(),
                    period_end.isoformat(),
                )
            else:
                trend_pdf_path: Path | None = None
                trend_pdf_result = None
                try:
                    if markdown_note_path is None:
                        raise RuntimeError(
                            "trend markdown note is unavailable for PDF delivery"
                        )
                    trend_pdf_result = render_trend_note_pdf_result(
                        markdown_path=markdown_note_path,
                        backend="auto",
                        page_mode="continuous",
                    )
                    trend_pdf_path = trend_pdf_result.path
                    pdf_generated_total = 1
                    if trend_pdf_result.prepared.renderer == "browser":
                        pdf_browser_generated_total = 1
                    else:
                        pdf_story_generated_total = 1
                except Exception as pdf_exc:  # noqa: BLE001
                    pdf_failed_total = 1
                    log.bind(module="pipeline.trends.pdf").warning(
                        "Trend PDF render failed: {}",
                        service._sanitize_error_message(str(pdf_exc)),
                    )

                if trend_pdf_path is not None and debug_pdf:
                    try:
                        if markdown_note_path is None:
                            raise RuntimeError(
                                "trend markdown note is unavailable for PDF debug export"
                            )
                        debug_dir = (
                            markdown_note_path.parent
                            / ".pdf-debug"
                            / trend_pdf_path.stem
                        )
                        export_trend_note_pdf_debug_bundle(
                            markdown_path=markdown_note_path,
                            pdf_path=trend_pdf_path,
                            debug_dir=debug_dir,
                            prepared=(
                                trend_pdf_result.prepared
                                if trend_pdf_result is not None
                                else None
                            ),
                        )
                        pdf_debug_generated_total = 1
                        log.bind(
                            module="pipeline.trends.pdf.debug",
                            debug_path=str(debug_dir),
                        ).info("Trend PDF debug export completed")
                    except Exception as debug_exc:  # noqa: BLE001
                        pdf_debug_failed_total = 1
                        log.bind(module="pipeline.trends.pdf.debug").warning(
                            "Trend PDF debug export failed: {}",
                            service._sanitize_error_message(str(debug_exc)),
                        )

                if trend_pdf_path is not None:
                    try:
                        if service.telegram_sender is None:
                            raise RuntimeError("telegram sender is not configured")
                        caption = build_telegram_trend_document_caption(
                            title=materialized.title,
                            overview_md=materialized.overview_md,
                            granularity=normalized_granularity,
                            period_start=period_start,
                        )
                        message_id = service.telegram_sender.send_document(
                            filename=trend_pdf_path.name,
                            content=trend_pdf_path.read_bytes(),
                            caption=caption,
                        )
                        repository_any.upsert_trend_delivery(
                            doc_id=doc_id,
                            channel=DELIVERY_CHANNEL_TELEGRAM,
                            destination=telegram_destination,
                            content_hash=trend_delivery_hash,
                            message_id=message_id,
                            status=DELIVERY_STATUS_SENT,
                        )
                        telegram_sent_total = 1
                    except Exception as telegram_exc:  # noqa: BLE001
                        telegram_failed_total = 1
                        sanitized_error = service._sanitize_error_message(
                            str(telegram_exc)
                        )
                        repository_any.upsert_trend_delivery(
                            doc_id=doc_id,
                            channel=DELIVERY_CHANNEL_TELEGRAM,
                            destination=telegram_destination,
                            content_hash=trend_delivery_hash,
                            message_id=None,
                            status=DELIVERY_STATUS_FAILED,
                            error=sanitized_error,
                        )
                        log.bind(module="pipeline.trends.telegram").warning(
                            "Trend Telegram delivery failed: {}",
                            sanitized_error,
                        )

        record_metric(
            name="pipeline.trends.pdf.generated_total",
            value=pdf_generated_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pdf.failed_total",
            value=pdf_failed_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pdf.debug.generated_total",
            value=pdf_debug_generated_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pdf.debug.failed_total",
            value=pdf_debug_failed_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pdf.browser.generated_total",
            value=pdf_browser_generated_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pdf.story.generated_total",
            value=pdf_story_generated_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.telegram.sent_total",
            value=telegram_sent_total,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.telegram.failed_total",
            value=telegram_failed_total,
            unit="count",
        )

        if include_debug and debug is not None:
            artifact_path = service._write_debug_artifact(
                run_id=run_id,
                item_id=None,
                kind="llm_response",
                payload={
                    "stage": "trends",
                    "granularity": normalized_granularity,
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "trend_doc_id": doc_id,
                    "debug": debug,
                },
            )
            if artifact_path is not None:
                try:
                    service.repository.add_artifact(
                        run_id=run_id,
                        item_id=None,
                        kind="llm_response",
                        path=str(artifact_path),
                    )
                except Exception as artifact_exc:  # noqa: BLE001
                    log.warning(
                        "Trends debug artifact record failed: {}",
                        service._sanitize_error_message(str(artifact_exc)),
                    )

        tool_calls_total = 0
        if isinstance(debug, dict):
            tool_calls_total = int(debug.get("tool_calls_total") or 0)
        record_metric(
            name="pipeline.trends.tool_calls_total",
            value=tool_calls_total,
            unit="count",
        )
        if isinstance(debug, dict):
            tool_call_breakdown = debug.get("tool_call_breakdown")
            if isinstance(tool_call_breakdown, dict):
                for raw_tool_name, raw_count in sorted(tool_call_breakdown.items()):
                    if not isinstance(raw_count, (int, float)):
                        continue
                    metric_tool_name = _trend_metric_stream_token(str(raw_tool_name))
                    if not metric_tool_name:
                        continue
                    record_metric(
                        name=f"pipeline.trends.tool.{metric_tool_name}.calls_total",
                        value=float(raw_count),
                        unit="count",
                    )
        record_metric(
            name="pipeline.trends.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.info(
            "Trends completed doc_id={} granularity={} period_start={} period_end={}",
            doc_id,
            normalized_granularity,
            period_start.isoformat(),
            period_end.isoformat(),
        )
        return TrendResult(
            doc_id=int(doc_id),
            granularity=normalized_granularity,
            period_start=period_start,
            period_end=period_end,
            title=str(payload.title),
        )
    except Exception as exc:
        sanitized_error = service._sanitize_error_message(str(exc))
        artifact_path = service._write_debug_artifact(
            run_id=run_id,
            item_id=None,
            kind="error_context",
            payload={
                "stage": "trends",
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                "granularity": normalized_granularity,
                "anchor_date": anchor.isoformat(),
                **service._classify_exception(exc),
            },
        )
        if artifact_path is not None:
            try:
                service.repository.add_artifact(
                    run_id=run_id,
                    item_id=None,
                    kind="error_context",
                    path=str(artifact_path),
                )
            except Exception as artifact_exc:  # noqa: BLE001
                log.warning(
                    "Trends error artifact record failed: {}",
                    service._sanitize_error_message(str(artifact_exc)),
                )
        record_metric(
            name="pipeline.trends.failed_total",
            value=1,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.warning("Trends failed: {}", sanitized_error)
        raise


def run_trends_topic_streams_stage(
    service: TrendStageService,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
    backfill: bool = False,
    backfill_mode: str = "missing",
    debug_pdf: bool = False,
) -> TrendResult:
    log = logger.bind(module="pipeline.trends", run_id=run_id)
    results: list[TrendResult] = []

    for stream in service._topic_streams:
        stream_settings = service._settings_for_topic_stream(stream)
        stream_targets = set(stream.publish_targets)
        stream_sender: Any | None = None
        if "telegram" in stream_targets:
            stream_sender = service._telegram_sender_for_stream(stream)
        service_factory = cast(Any, service.__class__)
        child_service = service_factory(
            settings=stream_settings,
            repository=cast(RepositoryPort, service.repository),
            analyzer=service.analyzer,
            triage=service.semantic_triage,
            telegram_sender=stream_sender,
        )
        result = run_trends_stage(
            child_service,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
            scope=stream.name,
        )
        result.stream = stream.name
        results.append(result)

    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.trends.streams_total",
        value=len(results),
        unit="count",
    )
    if not results:
        anchor = anchor_date or utc_now().date()
        if granularity == "week":
            period_start, period_end = trends.week_period_bounds(anchor)
        elif granularity == "month":
            period_start, period_end = trends.month_period_bounds(anchor)
        else:
            period_start, period_end = trends.day_period_bounds(anchor)
        return TrendResult(
            doc_id=0,
            granularity=str(granularity or "").strip().lower() or "day",
            period_start=period_start,
            period_end=period_end,
            title="Trend",
            stream_results=[],
        )

    first = results[0]
    log.info(
        "Topic stream trends completed streams={} granularity={} period_start={} period_end={}",
        len(results),
        first.granularity,
        first.period_start.isoformat(),
        first.period_end.isoformat(),
    )
    return TrendResult(
        doc_id=first.doc_id,
        granularity=first.granularity,
        period_start=first.period_start,
        period_end=first.period_end,
        title=first.title,
        stream=first.stream,
        stream_results=results,
    )
