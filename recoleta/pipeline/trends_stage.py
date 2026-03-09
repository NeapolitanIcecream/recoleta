from __future__ import annotations

import hashlib
import re
import time
from datetime import date, datetime, timedelta
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
from recoleta.ports import RepositoryPort
from recoleta.publish import (
    build_telegram_trend_document_caption,
    export_trend_note_pdf_debug_bundle,
    render_trend_note_pdf_result,
    write_markdown_trend_note,
    write_obsidian_trend_note,
)
from recoleta import trends
from recoleta.types import TrendResult, utc_now


class ScopedTrendsRepository:
    def __init__(self, *, repository: Any, scope: str) -> None:
        self._repository = repository
        self._scope = scope

    @property
    def engine(self) -> Any:
        return getattr(self._repository, "engine", None)

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        normalized_name = str(name or "").strip()
        if normalized_name.startswith("pipeline.trends."):
            suffix = normalized_name.removeprefix("pipeline.trends.")
            stream_token = "".join(
                ch if ch.isalnum() else "_" for ch in self._scope.lower().strip()
            ).strip("_") or "unknown"
            normalized_name = f"pipeline.trends.stream.{stream_token}.{suffix}"
        self._repository.record_metric(
            run_id=run_id,
            name=normalized_name,
            value=value,
            unit=unit,
        )

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
    ) -> list[tuple[Any, Any]]:
        return self._repository.list_analyzed_items_in_period(
            period_start=period_start,
            period_end=period_end,
            limit=limit,
            offset=offset,
            scope=self._scope,
        )

    def upsert_document_for_item(self, *, item: Any) -> Any:
        return self._repository.upsert_document_for_item(item=item, scope=self._scope)

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Any:
        return self._repository.upsert_document_for_trend(
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
            scope=self._scope,
        )

    def list_documents(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Any]:
        return self._repository.list_documents(
            doc_type=doc_type,
            period_start=period_start,
            period_end=period_end,
            granularity=granularity,
            scope=self._scope,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

    def search_chunks_text(
        self,
        *,
        query: str,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        return self._repository.search_chunks_text(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            scope=self._scope,
            limit=limit,
        )

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[Any]:
        return self._repository.list_summary_chunks_in_period(
            doc_type=doc_type,
            period_start=period_start,
            period_end=period_end,
            scope=self._scope,
            limit=limit,
            offset=offset,
        )

    def list_summary_chunk_index_rows_in_period(
        self,
        *,
        doc_type: str,
        granularity: str | None = None,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        return self._repository.list_summary_chunk_index_rows_in_period(
            doc_type=doc_type,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            scope=self._scope,
            limit=limit,
            offset=offset,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._repository, name)


class TrendStageService(Protocol):
    settings: Any
    repository: Any
    analyzer: Any
    semantic_triage: Any
    telegram_sender: Any | None
    _topic_streams: list[TopicStreamRuntime]
    _explicit_topic_streams: bool
    _llm_connection: Any

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
    started = time.perf_counter()
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity not in {"day", "week", "month"}:
        raise ValueError("granularity must be one of: day, week, month")
    anchor = anchor_date or utc_now().date()

    index_stats: dict[str, Any] = {}
    try:
        include_debug = bool(
            service.settings.write_debug_artifacts
            and service.settings.artifacts_dir is not None
        )

        def _record_index_metrics(stats: dict[str, Any], *, failed: bool) -> None:
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.index.items_total",
                value=float(stats.get("items_total") or 0),
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.index.docs_upserted_total",
                value=float(stats.get("docs_upserted") or 0),
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.index.chunks_upserted_total",
                value=float(stats.get("chunks_upserted") or 0),
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.index.duration_ms",
                value=float(stats.get("duration_ms") or 0),
                unit="ms",
            )
            service.repository.record_metric(
                run_id=run_id,
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

        if normalized_granularity == "day":
            period_start, period_end = trends.day_period_bounds(anchor)
            corpus_doc_type = "item"
            corpus_granularity: str | None = None
            index_stats = _index_items_for_period(required=True)
        elif normalized_granularity == "week":
            period_start, period_end = trends.week_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "day"
            index_stats = _index_items_for_period(required=False)
        else:
            period_start, period_end = trends.month_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "week"
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
                        _ = service.trends(
                            run_id=run_id,
                            granularity="day",
                            anchor_date=day,
                            llm_model=model,
                            backfill=False,
                            backfill_mode="missing",
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
                        _ = service.trends(
                            run_id=run_id,
                            granularity="week",
                            anchor_date=week_start.date(),
                            llm_model=model,
                            backfill=False,
                            backfill_mode="missing",
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
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.backfill.days_total",
                value=backfill_days_total,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.backfill.missing_total",
                value=backfill_missing_total,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.backfill.generated_total",
                value=backfill_generated_total,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.backfill.skipped_total",
                value=backfill_skipped_total,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.backfill.failed_total",
                value=backfill_failed_total,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
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
                order_by="event_desc",
                offset=0,
                limit=1,
            )
            corpus_docs_total = 1 if probe else 0

        service.repository.record_metric(
            run_id=run_id,
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
            service.repository.record_metric(
                run_id=run_id,
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
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.llm_requests_total",
                value=0,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.llm_input_tokens_total",
                value=0,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.llm_output_tokens_total",
                value=0,
                unit="count",
            )
            service.repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.estimated_cost_usd",
                value=0.0,
                unit="usd",
            )
        else:
            service.repository.record_metric(
                run_id=run_id,
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
                        getattr(service.settings, "trends_overview_pack_max_chars", 8000)
                        or 8000
                    ),
                    item_overview_top_k=int(
                        getattr(service.settings, "trends_item_overview_top_k", 20)
                        or 20
                    ),
                    item_overview_item_max_chars=int(
                        getattr(service.settings, "trends_item_overview_item_max_chars", 500)
                        or 500
                    ),
                )
                rag_sources = list(getattr(plan, "rag_sources", []) or [])
                ranking_n = int(getattr(service.settings, "trends_ranking_n", 10) or 10)
                rep_source_doc_type = str(
                    getattr(plan, "rep_source_doc_type", "item") or "item"
                ).strip()
                if isinstance(pack_stats, dict) and bool(pack_stats.get("truncated")):
                    service.repository.record_metric(
                        run_id=run_id,
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
                llm_connection=service._llm_connection,
            )
            if isinstance(debug, dict):
                usage = debug.get("usage")
                if isinstance(usage, dict):
                    requests = usage.get("requests")
                    input_tokens = usage.get("input_tokens")
                    output_tokens = usage.get("output_tokens")
                    if isinstance(requests, (int, float)):
                        service.repository.record_metric(
                            run_id=run_id,
                            name="pipeline.trends.llm_requests_total",
                            value=float(requests),
                            unit="count",
                        )
                    if isinstance(input_tokens, (int, float)):
                        service.repository.record_metric(
                            run_id=run_id,
                            name="pipeline.trends.llm_input_tokens_total",
                            value=float(input_tokens),
                            unit="count",
                        )
                    if isinstance(output_tokens, (int, float)):
                        service.repository.record_metric(
                            run_id=run_id,
                            name="pipeline.trends.llm_output_tokens_total",
                            value=float(output_tokens),
                            unit="count",
                        )
                cost_usd = debug.get("estimated_cost_usd")
                if isinstance(cost_usd, (int, float)):
                    service.repository.record_metric(
                        run_id=run_id,
                        name="pipeline.trends.estimated_cost_usd",
                        value=float(cost_usd),
                        unit="usd",
                    )
                else:
                    service.repository.record_metric(
                        run_id=run_id,
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
                doc = cast(Any, service.repository).get_document(doc_id=normalized_doc_id)
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
                        score=round(score_value, 6) if score_value is not None else None,
                    )
                )
                if len(reps) >= limit:
                    break
            return reps

        max_reps = 6
        for cluster in list(getattr(payload, "clusters", []) or []):
            cleaned: list[Any] = []
            for rep in list(getattr(cluster, "representative_chunks", []) or []):
                try:
                    doc_id_int = int(getattr(rep, "doc_id"))
                except Exception:
                    continue
                doc_type = _doc_type_for_doc_id(doc_id_int)
                if doc_type != "item":
                    rep_dropped_non_item_total += 1
                    continue
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

        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.rep_enforcement.dropped_non_item_total",
            value=rep_dropped_non_item_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.rep_enforcement.backfilled_total",
            value=rep_backfilled_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.rep_enforcement.failed_clusters_total",
            value=rep_failed_clusters_total,
            unit="count",
        )

        doc_id = trends.persist_trend_payload(
            repository=cast(Any, service.repository),
            granularity=normalized_granularity,
            period_start=period_start,
            period_end=period_end,
            payload=payload,
        )

        doc_cache: dict[int, Any | None] = {}
        item_cache: dict[int, Any | None] = {}

        def _get_doc(doc_id_value: int) -> Any | None:
            normalized_doc_id = int(doc_id_value)
            if normalized_doc_id <= 0:
                return None
            if normalized_doc_id not in doc_cache:
                doc_cache[normalized_doc_id] = cast(
                    Any, service.repository
                ).get_document(doc_id=normalized_doc_id)
            return doc_cache.get(normalized_doc_id)

        def _parse_authors(value: Any) -> list[str]:
            if value is None:
                return []
            if isinstance(value, list):
                return [str(a).strip() for a in value if str(a).strip()]
            if isinstance(value, str):
                raw = value.strip()
                if not raw:
                    return []
                try:
                    loaded = orjson.loads(raw)
                except Exception:
                    return []
                if isinstance(loaded, list):
                    return [str(a).strip() for a in loaded if str(a).strip()]
            return []

        def _citation_label_from_title(raw_title: str) -> str:
            normalized = " ".join(str(raw_title or "").split()).strip()
            if not normalized:
                return "Paper"
            if ":" in normalized:
                prefix = normalized.split(":", 1)[0].strip()
                if 2 <= len(prefix) <= 40:
                    normalized = prefix
            normalized = normalized.replace("[", "(").replace("]", ")")
            if len(normalized) > 60:
                normalized = normalized[:60].rstrip() + "…"
            return normalized

        def _citation_for_doc_id(doc_id_value: int) -> str | None:
            doc = _get_doc(doc_id_value)
            if doc is None:
                return None
            title = str(getattr(doc, "title", "") or "").strip()
            url = str(getattr(doc, "canonical_url", "") or "").strip()
            label = _citation_label_from_title(title)
            if url:
                return f"[{label}]({url})"
            return label

        doc_ref_pattern = re.compile(r"\bdoc_id\s*[:=]\s*([0-9][0-9,\s]*)\b")
        doc_short_pattern = re.compile(r"\bdoc\s+(\d+)\b")
        chunk_suffix_pattern = re.compile(
            r"\s*[,;，；]?\s*chunk(?:_index)?\s*[:=]\s*\d+",
            re.IGNORECASE,
        )

        rewrite_occurrences_total = 0
        rewrite_doc_ids_resolved_total = 0
        rewrite_doc_ids_unresolved_total = 0

        def _rewrite_doc_refs(value: str) -> str:
            nonlocal rewrite_occurrences_total
            nonlocal rewrite_doc_ids_resolved_total
            nonlocal rewrite_doc_ids_unresolved_total

            raw = str(value or "")
            if not raw.strip():
                return raw

            def _replace_doc_id_match(match: re.Match[str]) -> str:
                nonlocal rewrite_occurrences_total
                nonlocal rewrite_doc_ids_resolved_total
                nonlocal rewrite_doc_ids_unresolved_total

                numbers = [int(x) for x in re.findall(r"\d+", match.group(1) or "")]
                seen: set[int] = set()
                doc_ids: list[int] = []
                for n in numbers:
                    if n <= 0 or n in seen:
                        continue
                    seen.add(n)
                    doc_ids.append(n)
                if not doc_ids:
                    return match.group(0)

                rewrite_occurrences_total += 1
                citations: list[str] = []
                for doc_id_inner in doc_ids:
                    cite = _citation_for_doc_id(doc_id_inner)
                    if cite is None:
                        rewrite_doc_ids_unresolved_total += 1
                        citations.append("Paper")
                    else:
                        rewrite_doc_ids_resolved_total += 1
                        citations.append(cite)
                return "、".join(citations)

            def _replace_doc_short_match(match: re.Match[str]) -> str:
                nonlocal rewrite_occurrences_total
                nonlocal rewrite_doc_ids_resolved_total
                nonlocal rewrite_doc_ids_unresolved_total

                raw_id = match.group(1) or ""
                try:
                    doc_id_inner = int(raw_id)
                except Exception:
                    return match.group(0)
                if doc_id_inner <= 0:
                    return match.group(0)
                cite = _citation_for_doc_id(doc_id_inner)
                if cite is None:
                    rewrite_doc_ids_unresolved_total += 1
                    return match.group(0)
                rewrite_occurrences_total += 1
                rewrite_doc_ids_resolved_total += 1
                return cite

            rewritten = doc_ref_pattern.sub(_replace_doc_id_match, raw)
            rewritten = doc_short_pattern.sub(_replace_doc_short_match, rewritten)
            rewritten = chunk_suffix_pattern.sub("", rewritten)
            return rewritten

        title_for_notes = _rewrite_doc_refs(str(payload.title))
        overview_md_for_notes = _rewrite_doc_refs(str(payload.overview_md))
        highlights_for_notes = [
            _rewrite_doc_refs(str(h)) for h in (list(payload.highlights) or [])
        ]

        clusters_for_notes: list[dict[str, Any]] = []
        if payload.clusters:
            for cluster in payload.clusters:
                cluster_dict = cluster.model_dump(mode="json")
                cluster_dict["name"] = _rewrite_doc_refs(
                    str(cluster_dict.get("name") or "").strip()
                )
                cluster_dict["description"] = _rewrite_doc_refs(
                    str(cluster_dict.get("description") or "").strip()
                )
                reps = cluster_dict.get("representative_chunks") or []
                enriched_reps: list[dict[str, Any]] = []
                if isinstance(reps, list) and reps:
                    for rep in reps:
                        if not isinstance(rep, dict):
                            continue
                        raw_doc_id = rep.get("doc_id")
                        raw_chunk_index = rep.get("chunk_index")
                        if raw_doc_id is None or raw_chunk_index is None:
                            continue
                        try:
                            doc_id_int = int(raw_doc_id)
                            _ = int(raw_chunk_index)
                        except Exception:
                            continue
                        if doc_id_int <= 0:
                            continue
                        doc = _get_doc(doc_id_int)
                        if doc is None:
                            continue

                        title = str(getattr(doc, "title", "") or "").strip()
                        url = str(getattr(doc, "canonical_url", "") or "").strip()
                        if not title:
                            continue

                        authors: list[str] = []
                        doc_type = (
                            str(getattr(doc, "doc_type", "") or "").strip().lower()
                        )
                        if doc_type == "item":
                            raw_item_id = getattr(doc, "item_id", None)
                            try:
                                item_id_int = int(raw_item_id) if raw_item_id is not None else 0
                            except Exception:
                                item_id_int = 0
                            if item_id_int > 0:
                                if item_id_int not in item_cache:
                                    item_cache[item_id_int] = cast(
                                        Any, service.repository
                                    ).get_item(item_id=item_id_int)
                                item = item_cache.get(item_id_int)
                                if item is not None:
                                    authors = _parse_authors(getattr(item, "authors", None))

                        enriched = dict(rep)
                        enriched["title"] = title
                        if url:
                            enriched["url"] = url
                        if authors:
                            enriched["authors"] = authors
                        enriched_reps.append(enriched)
                cluster_dict["representative_chunks"] = enriched_reps
                clusters_for_notes.append(cluster_dict)

        if rewrite_occurrences_total or rewrite_doc_ids_unresolved_total:
            log.info(
                "Trend note doc refs rewritten occurrences={} resolved_doc_ids={} unresolved_doc_ids={}",
                rewrite_occurrences_total,
                rewrite_doc_ids_resolved_total,
                rewrite_doc_ids_unresolved_total,
            )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.note_doc_refs_rewrite_occurrences_total",
            value=rewrite_occurrences_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.note_doc_refs_resolved_total",
            value=rewrite_doc_ids_resolved_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.note_doc_refs_unresolved_total",
            value=rewrite_doc_ids_unresolved_total,
            unit="count",
        )

        trend_delivery_hash = hashlib.sha256(
            orjson.dumps(
                {
                    "title": title_for_notes,
                    "granularity": normalized_granularity,
                    "period_start": period_start.isoformat(),
                    "period_end": period_end.isoformat(),
                    "overview_md": overview_md_for_notes,
                    "topics": list(payload.topics),
                    "clusters": clusters_for_notes,
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
                    title=title_for_notes,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    run_id=run_id,
                    overview_md=overview_md_for_notes,
                    topics=list(payload.topics),
                    clusters=clusters_for_notes,
                    highlights=highlights_for_notes,
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
                    title=title_for_notes,
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    run_id=run_id,
                    overview_md=overview_md_for_notes,
                    topics=list(payload.topics),
                    clusters=clusters_for_notes,
                    highlights=highlights_for_notes,
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
                        debug_dir = markdown_note_path.parent / ".pdf-debug" / trend_pdf_path.stem
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
                            title=title_for_notes,
                            overview_md=overview_md_for_notes,
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

        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.generated_total",
            value=pdf_generated_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.failed_total",
            value=pdf_failed_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.debug.generated_total",
            value=pdf_debug_generated_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.debug.failed_total",
            value=pdf_debug_failed_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.browser.generated_total",
            value=pdf_browser_generated_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.pdf.story.generated_total",
            value=pdf_story_generated_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.telegram.sent_total",
            value=telegram_sent_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
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
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.tool_calls_total",
            value=tool_calls_total,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
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
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.trends.failed_total",
            value=1,
            unit="count",
        )
        service.repository.record_metric(
            run_id=run_id,
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
        scoped_repository = ScopedTrendsRepository(
            repository=service.repository,
            scope=stream.name,
        )
        stream_settings = service._settings_for_topic_stream(stream)
        stream_targets = set(stream.publish_targets)
        stream_sender: Any | None = None
        if "telegram" in stream_targets:
            stream_sender = service._telegram_sender_for_stream(stream)
        service_factory = cast(Any, service.__class__)
        child_service = service_factory(
            settings=stream_settings,
            repository=cast(RepositoryPort, scoped_repository),
            analyzer=service.analyzer,
            triage=service.semantic_triage,
            telegram_sender=stream_sender,
        )
        result = child_service.trends(
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
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
