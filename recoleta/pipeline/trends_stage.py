# pyright: reportGeneralTypeIssues=false
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import time
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any, Protocol, TypedDict, Unpack, cast

import orjson
from loguru import logger

from recoleta.delivery import TelegramSender
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.pipeline.metrics import metric_token
from recoleta.pipeline.pass_runner import (
    PassDefinition,
    PassPersistSpec,
    ProjectionSpec,
    run_pass_definition,
)
from recoleta.passes import TREND_SYNTHESIS_PASS_KIND, build_trend_synthesis_pass_output
from recoleta.ports import TrendStageRepositoryPort
from recoleta.publish import (
    build_telegram_trend_document_caption,
    export_trend_note_pdf_debug_bundle,
    render_trend_note_pdf_result,
    write_markdown_trend_note,
    write_obsidian_trend_note,
)
from recoleta.trend_materialize import (
    MaterializedTrendNotePayload,
    materialize_trend_note_payload,
)
from recoleta import trends
from recoleta.types import TrendResult, utc_now


def _trend_metric_name(name: str) -> str:
    return str(name or "").strip()


@dataclass(slots=True, frozen=True)
class TrendStageRequest:
    run_id: str
    granularity: str = "day"
    anchor_date: date | None = None
    llm_model: str | None = None
    backfill: bool = False
    backfill_mode: str = "missing"
    debug_pdf: bool = False
    reuse_existing_corpus: bool = False


@dataclass(slots=True)
class _TrendProjectionState:
    doc_id: int
    materialized: MaterializedTrendNotePayload
    targets: set[str]
    telegram_destination: str
    telegram_remaining_today: int | None
    telegram_already_sent: bool
    telegram_can_attempt_delivery: bool
    trend_delivery_hash: str


@dataclass(slots=True)
class _TrendStageState:
    include_debug: bool
    normalized_granularity: str
    normalized_backfill_mode: str
    anchor: date
    period_start: Any
    period_end: Any
    corpus_doc_type: str
    corpus_granularity: str | None
    model: str


@dataclass(slots=True)
class _TrendGenerationArtifacts:
    payload: Any
    debug: dict[str, Any] | None
    empty_corpus: bool
    corpus_docs_total: int
    overview_pack_md: str | None = None
    history_pack_md: str | None = None
    rag_sources: list[dict[str, str | None]] | None = None
    ranking_n: int | None = None
    rep_source_doc_type: str | None = None
    evolution_max_signals: int | None = None
    overview_pack_stats: dict[str, Any] | None = None
    history_pack_stats: dict[str, Any] | None = None
    evolution_normalization_stats: dict[str, int] | None = None
    evolution_suppressed_without_history: bool = False
    plan: trends.TrendGenerationPlan | None = None
    rep_dropped_non_item_total: int = 0
    rep_backfilled_total: int = 0
    rep_failed_clusters_total: int = 0


@dataclass(slots=True)
class _TrendDeliveryStats:
    markdown_note_path: Path | None = None
    pdf_generated_total: int = 0
    pdf_failed_total: int = 0
    pdf_debug_generated_total: int = 0
    pdf_debug_failed_total: int = 0
    pdf_browser_generated_total: int = 0
    pdf_story_generated_total: int = 0
    telegram_sent_total: int = 0
    telegram_failed_total: int = 0


@dataclass(slots=True)
class _TrendProjectionContext:
    service: TrendStageService
    request: TrendStageRequest
    state: _TrendStageState
    generation: _TrendGenerationArtifacts
    log: Any
    record_metric: Any
    pass_output_failure: dict[str, str] | None = None


@dataclass(slots=True, frozen=True)
class _TrendGenerationInputs:
    overview_pack_md: str | None
    history_pack_md: str | None
    rag_sources: list[dict[str, str | None]] | None
    ranking_n: int | None
    rep_source_doc_type: str | None
    evolution_max_signals: int | None


@dataclass(slots=True, frozen=True)
class _TrendDebugAnnotation:
    payload: Any
    overview_pack_md: str | None
    history_pack_md: str | None
    overview_pack_stats: dict[str, Any] | None
    history_pack_stats: dict[str, Any] | None
    evolution_normalization_stats: dict[str, int]
    evolution_suppressed_without_history: bool


@dataclass(slots=True, frozen=True)
class _TrendArtifactsRequest:
    payload: Any
    debug: dict[str, Any] | None
    corpus_docs_total: int
    inputs: _TrendGenerationInputs
    overview_pack_stats: dict[str, Any] | None
    history_pack_stats: dict[str, Any] | None
    evolution_normalization_stats: dict[str, int]
    evolution_suppressed_without_history: bool
    plan: trends.TrendGenerationPlan | None
    rep_stats: dict[str, int]


@dataclass(slots=True, frozen=True)
class _SourceEnsureResult:
    token: str
    doc_type: str
    granularity: str | None
    docs_total: int
    already_ready: bool = False
    materialized: bool = False
    failed: bool = False


class TrendStageService(Protocol):
    settings: Any
    analyzer: Any
    semantic_triage: Any
    telegram_sender: Any | None
    _llm_connection: Any

    @property
    def repository(self) -> TrendStageRepositoryPort: ...

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

    def _record_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
        log: Any,
        failure_message: str,
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


class _TrendStageRequestKwargs(TypedDict, total=False):
    run_id: str
    granularity: str
    anchor_date: date | None
    llm_model: str | None
    backfill: bool
    backfill_mode: str
    debug_pdf: bool
    reuse_existing_corpus: bool


def run_trends_stage(
    service: TrendStageService,
    *,
    request: TrendStageRequest | None = None,
    **legacy_kwargs: Unpack[_TrendStageRequestKwargs],
) -> TrendResult:
    normalized_request = request or TrendStageRequest(**legacy_kwargs)
    return _TrendStageRunner(service=service, request=normalized_request).run()


class _TrendStageRunner:
    def __init__(
        self, *, service: TrendStageService, request: TrendStageRequest
    ) -> None:
        self.service = service
        self.request = request
        self.log = logger.bind(module="pipeline.trends", run_id=request.run_id)
        self.started = time.perf_counter()
        self.metric_namespace = _trend_metric_name("pipeline.trends")

    def run(self) -> TrendResult:
        state: _TrendStageState | None = None
        try:
            state = self._prepare_state()
            self._run_backfill_if_requested(state)
            generation = self._build_generation_artifacts(state)
            projection_context = _TrendProjectionContext(
                service=self.service,
                request=self.request,
                state=state,
                generation=generation,
                log=self.log,
                record_metric=self.record_metric,
            )
            pass_execution = self._run_pass_execution(
                state=state,
                generation=generation,
                context=projection_context,
            )
            trend_synthesis_pass_output_id = pass_execution.pass_output_id
            trend_projection_state = pass_execution.projection_state
            if trend_projection_state is None:
                raise RuntimeError("trend projection state preparation returned empty")
            delivery_stats = self._deliver_outputs(
                state=state,
                generation=generation,
                projection_state=trend_projection_state,
                projection_results=pass_execution.projection_results,
            )
            self._record_delivery_metrics(delivery_stats)
            self._record_success_debug_artifact(
                state=state,
                generation=generation,
                doc_id=trend_projection_state.doc_id,
                pass_output_id=trend_synthesis_pass_output_id,
            )
            self._record_tool_metrics(generation.debug)
            self.record_metric(
                name="pipeline.trends.duration_ms",
                value=int((time.perf_counter() - self.started) * 1000),
                unit="ms",
            )
            self.log.info(
                "Trends completed doc_id={} granularity={} period_start={} period_end={}",
                trend_projection_state.doc_id,
                state.normalized_granularity,
                state.period_start.isoformat(),
                state.period_end.isoformat(),
            )
            return TrendResult(
                doc_id=int(trend_projection_state.doc_id),
                granularity=state.normalized_granularity,
                period_start=state.period_start,
                period_end=state.period_end,
                title=str(generation.payload.title),
                pass_output_id=trend_synthesis_pass_output_id,
            )
        except Exception as exc:
            self._handle_failure(exc=exc, state=state)
            raise

    def record_metric(
        self, *, name: str, value: float, unit: str | None = None
    ) -> None:
        self.service.repository.record_metric(
            run_id=self.request.run_id,
            name=_trend_metric_name(name),
            value=value,
            unit=unit,
        )

    def record_duration_metric(self, *, name: str, started_at: float) -> int:
        duration_ms = int((time.perf_counter() - started_at) * 1000)
        self.record_metric(name=name, value=duration_ms, unit="ms")
        return duration_ms

    def _prepare_state(self) -> _TrendStageState:
        include_debug = bool(
            self.service.settings.write_debug_artifacts
            and self.service.settings.artifacts_dir is not None
        )
        self.record_metric(
            name="pipeline.trends.corpus.reuse_existing",
            value=1.0 if self.request.reuse_existing_corpus else 0.0,
            unit="bool",
        )
        normalized_granularity = self._normalize_granularity()
        normalized_backfill_mode = self._normalize_backfill_mode()
        anchor = self.request.anchor_date or utc_now().date()
        (
            period_start,
            period_end,
            corpus_doc_type,
            corpus_granularity,
        ) = self._prepare_period_state(
            normalized_granularity=normalized_granularity,
            anchor=anchor,
        )
        model = self.request.llm_model or self.service.settings.llm_model
        return _TrendStageState(
            include_debug=include_debug,
            normalized_granularity=normalized_granularity,
            normalized_backfill_mode=normalized_backfill_mode,
            anchor=anchor,
            period_start=period_start,
            period_end=period_end,
            corpus_doc_type=corpus_doc_type,
            corpus_granularity=corpus_granularity,
            model=model,
        )

    def _normalize_granularity(self) -> str:
        normalized = str(self.request.granularity or "").strip().lower()
        if normalized not in {"day", "week", "month"}:
            raise ValueError("granularity must be one of: day, week, month")
        return normalized

    def _normalize_backfill_mode(self) -> str:
        normalized = str(self.request.backfill_mode or "missing").strip().lower()
        if normalized not in {"missing", "all"}:
            raise ValueError("backfill_mode must be one of: missing, all")
        return normalized

    def _prepare_period_state(
        self,
        *,
        normalized_granularity: str,
        anchor: date,
    ) -> tuple[Any, Any, str, str | None]:
        if normalized_granularity == "day":
            period_start, period_end = trends.day_period_bounds(anchor)
            corpus_doc_type = "item"
            corpus_granularity: str | None = None
        elif normalized_granularity == "week":
            period_start, period_end = trends.week_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "day"
        else:
            period_start, period_end = trends.month_period_bounds(anchor)
            corpus_doc_type = "trend"
            corpus_granularity = "week"

        prepare_skipped = bool(self.request.reuse_existing_corpus)
        self.record_metric(
            name="pipeline.trends.prepare.skipped_total",
            value=1 if prepare_skipped else 0,
            unit="count",
        )
        if not prepare_skipped:
            self._prepare_period_backlog(
                period_start=period_start,
                period_end=period_end,
            )
        return (
            period_start,
            period_end,
            corpus_doc_type,
            corpus_granularity,
        )

    def _prepare_period_backlog(self, *, period_start: Any, period_end: Any) -> None:
        self.service.prepare(
            run_id=self.request.run_id,
            period_start=period_start,
            period_end=period_end,
        )
        self.service.analyze(
            run_id=self.request.run_id,
            period_start=period_start,
            period_end=period_end,
        )

    def _index_items_for_period(
        self,
        *,
        period_start: Any,
        period_end: Any,
    ) -> dict[str, Any]:
        try:
            stats = trends.index_items_as_documents(
                repository=cast(Any, self.service.repository),
                run_id=self.request.run_id,
                period_start=period_start,
                period_end=period_end,
                min_relevance_score=float(
                    getattr(self.service.settings, "min_relevance_score", 0.0) or 0.0
                ),
            )
        except Exception as exc:
            failed_stats = {
                "items_total": 0,
                "docs_upserted": 0,
                "docs_deleted": 0,
                "chunks_upserted": 0,
                "items_filtered_out": 0,
                "duration_ms": 0,
            }
            self._record_index_metrics(failed_stats, failed=True)
            self.log.warning(
                "Trends index failed granularity={} period_start={} period_end={} error_type={} error={}",
                self.request.granularity,
                period_start.isoformat(),
                period_end.isoformat(),
                type(exc).__name__,
                self.service._sanitize_error_message(str(exc)),
            )
            raise
        self._record_index_metrics(stats, failed=False)
        return stats

    def _record_index_metrics(self, stats: dict[str, Any], *, failed: bool) -> None:
        for metric_name, source_key in (
            ("pipeline.trends.index.items_total", "items_total"),
            ("pipeline.trends.index.docs_upserted_total", "docs_upserted"),
            ("pipeline.trends.index.docs_deleted_total", "docs_deleted"),
            ("pipeline.trends.index.chunks_upserted_total", "chunks_upserted"),
            ("pipeline.trends.index.items_filtered_out_total", "items_filtered_out"),
            ("pipeline.trends.index.duration_ms", "duration_ms"),
        ):
            self.record_metric(
                name=metric_name,
                value=float(stats.get(source_key) or 0),
                unit="ms" if metric_name.endswith("duration_ms") else "count",
            )
        self.record_metric(
            name="pipeline.trends.index.failed_total",
            value=1 if failed else 0,
            unit="count",
        )

    def _record_source_materialization_metric(
        self,
        *,
        metric_name: str,
        token: str,
        value: float,
    ) -> None:
        self.record_metric(
            name=(
                "pipeline.trends.source_materialization."
                f"{metric_name}.{metric_token(token, max_len=24)}"
            ),
            value=value,
            unit="count",
        )

    def _source_token(self, *, doc_type: str, granularity: str | None) -> str:
        normalized_doc_type = str(doc_type or "").strip().lower()
        normalized_granularity = str(granularity or "").strip().lower()
        if normalized_doc_type == "item":
            return "item"
        if normalized_doc_type == "trend" and normalized_granularity in {"day", "week"}:
            return f"trend_{normalized_granularity}"
        raise ValueError(
            f"unsupported required source doc_type={normalized_doc_type} granularity={normalized_granularity or '-'}"
        )

    def _required_source_tokens(
        self,
        *,
        state: _TrendStageState,
        plan: trends.TrendGenerationPlan | None,
    ) -> list[str]:
        required = {
            self._source_token(
                doc_type=state.corpus_doc_type,
                granularity=state.corpus_granularity,
            ),
            "item",
        }
        if bool(getattr(self.service.settings, "trends_self_similar_enabled", False)):
            for source in list(getattr(plan, "rag_sources", []) or []):
                doc_type = str(source.get("doc_type") or "").strip().lower()
                granularity = source.get("granularity")
                try:
                    required.add(
                        self._source_token(
                            doc_type=doc_type,
                            granularity=str(granularity or "").strip().lower() or None,
                        )
                    )
                except ValueError:
                    continue
        return [
            token
            for token in ("item", "trend_day", "trend_week")
            if token in required
        ]

    def _ensure_required_sources(
        self,
        *,
        state: _TrendStageState,
        plan: trends.TrendGenerationPlan | None,
    ) -> dict[str, _SourceEnsureResult]:
        results: dict[str, _SourceEnsureResult] = {}
        for token in self._required_source_tokens(state=state, plan=plan):
            self._record_source_materialization_metric(
                metric_name="checked_total",
                token=token,
                value=1,
            )
            result = self._ensure_source(token=token, state=state)
            results[token] = result
            if result.already_ready:
                self._record_source_materialization_metric(
                    metric_name="already_ready_total",
                    token=token,
                    value=1,
                )
            if result.materialized:
                self._record_source_materialization_metric(
                    metric_name="materialized_total",
                    token=token,
                    value=1,
                )
            if result.failed:
                self._record_source_materialization_metric(
                    metric_name="failed_total",
                    token=token,
                    value=1,
                )
                raise RuntimeError(f"required source materialization failed for {token}")
            if token == "item":
                self.record_metric(
                    name="pipeline.trends.index.skipped_total",
                    value=1 if result.already_ready else 0,
                    unit="count",
                )
        return results

    def _ensure_source(
        self,
        *,
        token: str,
        state: _TrendStageState,
    ) -> _SourceEnsureResult:
        try:
            if token == "item":
                return self._ensure_item_source(state=state)
            if token == "trend_day":
                return self._ensure_trend_source(granularity="day", state=state)
            if token == "trend_week":
                return self._ensure_trend_source(granularity="week", state=state)
            raise ValueError(f"unsupported source token: {token}")
        except Exception as exc:
            self.log.warning(
                "Required source materialization failed source={} error_type={} error={}",
                token,
                type(exc).__name__,
                self.service._sanitize_error_message(str(exc)),
            )
            if token == "item":
                return _SourceEnsureResult(
                    token="item",
                    doc_type="item",
                    granularity=None,
                    docs_total=0,
                    failed=True,
                )
            granularity = token.removeprefix("trend_")
            return _SourceEnsureResult(
                token=token,
                doc_type="trend",
                granularity=granularity or None,
                docs_total=0,
                failed=True,
            )

    def _filtered_item_pairs(
        self,
        *,
        period_start: Any,
        period_end: Any,
    ) -> list[tuple[Any, Any]]:
        pairs = cast(Any, self.service.repository).list_analyzed_items_in_period(
            period_start=period_start,
            period_end=period_end,
            limit=2000,
        )
        pairs, _filtered_out_total = trends._filter_pairs_by_min_relevance(
            pairs,
            min_relevance_score=float(
                getattr(self.service.settings, "min_relevance_score", 0.0) or 0.0
            ),
        )
        return list(pairs)

    def _item_source_ready(
        self,
        *,
        period_start: Any,
        period_end: Any,
    ) -> tuple[bool, int]:
        expected_item_ids = self._expected_item_ids_for_period(
            period_start=period_start,
            period_end=period_end,
        )
        docs = self._item_documents_for_period(
            period_start=period_start,
            period_end=period_end,
            expected_total=len(expected_item_ids),
        )
        if not expected_item_ids:
            return (not bool(docs), 0)
        doc_ids_by_item_id = self._item_doc_ids_by_item_id(docs)
        if set(doc_ids_by_item_id) != expected_item_ids:
            return False, len(expected_item_ids)
        required_doc_ids = set(doc_ids_by_item_id.values())
        return (
            self._item_chunk_kinds_ready(
                required_doc_ids=required_doc_ids,
                period_start=period_start,
                period_end=period_end,
                expected_total=len(expected_item_ids),
            ),
            len(expected_item_ids),
        )

    def _expected_item_ids_for_period(
        self,
        *,
        period_start: Any,
        period_end: Any,
    ) -> set[int]:
        pairs = self._filtered_item_pairs(
            period_start=period_start,
            period_end=period_end,
        )
        item_ids: set[int] = set()
        for item, _analysis in pairs:
            raw_item_id = getattr(item, "id", None)
            if raw_item_id is None:
                continue
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id > 0:
                item_ids.add(item_id)
        return item_ids

    def _item_documents_for_period(
        self,
        *,
        period_start: Any,
        period_end: Any,
        expected_total: int,
    ) -> list[Any]:
        return cast(Any, self.service.repository).list_documents(
            doc_type="item",
            period_start=period_start,
            period_end=period_end,
            order_by="event_desc",
            limit=self._item_source_probe_limit(expected_total),
        )

    def _item_source_probe_limit(self, expected_total: int) -> int:
        return max(500, int(expected_total) * 2 + 50)

    def _item_doc_ids_by_item_id(self, docs: list[Any]) -> dict[int, int]:
        doc_ids_by_item_id: dict[int, int] = {}
        for doc in docs:
            raw_item_id = getattr(doc, "item_id", None)
            raw_doc_id = getattr(doc, "id", None)
            if raw_item_id is None or raw_doc_id is None:
                continue
            try:
                item_id = int(raw_item_id)
                doc_id = int(raw_doc_id)
            except Exception:
                continue
            if item_id > 0 and doc_id > 0:
                doc_ids_by_item_id[item_id] = doc_id
        return doc_ids_by_item_id

    def _item_chunk_kinds_ready(
        self,
        *,
        required_doc_ids: set[int],
        period_start: Any,
        period_end: Any,
        expected_total: int,
    ) -> bool:
        summary_doc_ids = self._item_chunk_doc_ids(
            kind="summary",
            period_start=period_start,
            period_end=period_end,
            expected_total=expected_total,
        )
        if not required_doc_ids <= summary_doc_ids:
            return False
        meta_doc_ids = self._item_chunk_doc_ids(
            kind="meta",
            period_start=period_start,
            period_end=period_end,
            expected_total=expected_total,
        )
        return required_doc_ids <= meta_doc_ids

    def _item_chunk_doc_ids(
        self,
        *,
        kind: str,
        period_start: Any,
        period_end: Any,
        expected_total: int,
    ) -> set[int]:
        rows = cast(Any, self.service.repository).list_document_chunk_index_rows_in_period(
            doc_type="item",
            kind=kind,
            period_start=period_start,
            period_end=period_end,
            limit=self._item_source_probe_limit(expected_total),
        )
        doc_ids: set[int] = set()
        for row in rows:
            try:
                doc_id = int(row.get("doc_id") or 0)
            except Exception:
                continue
            if doc_id > 0:
                doc_ids.add(doc_id)
        return doc_ids

    def _ensure_item_source(self, *, state: _TrendStageState) -> _SourceEnsureResult:
        if not self.request.reuse_existing_corpus:
            stats = self._index_items_for_period(
                period_start=state.period_start,
                period_end=state.period_end,
            )
            return _SourceEnsureResult(
                token="item",
                doc_type="item",
                granularity=None,
                docs_total=int(stats.get("docs_upserted") or 0),
                materialized=True,
            )
        ready, docs_total = self._item_source_ready(
            period_start=state.period_start,
            period_end=state.period_end,
        )
        if ready:
            return _SourceEnsureResult(
                token="item",
                doc_type="item",
                granularity=None,
                docs_total=docs_total,
                already_ready=True,
            )
        stats = self._index_items_for_period(
            period_start=state.period_start,
            period_end=state.period_end,
        )
        return _SourceEnsureResult(
            token="item",
            doc_type="item",
            granularity=None,
            docs_total=int(stats.get("docs_upserted") or 0),
            materialized=True,
        )

    def _trend_source_windows(
        self,
        *,
        granularity: str,
        period_start: Any,
        period_end: Any,
    ) -> list[tuple[Any, Any]]:
        windows: list[tuple[Any, Any]] = []
        if granularity == "day":
            current = period_start
            while current < period_end:
                windows.append((current, current + timedelta(days=1)))
                current += timedelta(days=1)
            return windows
        current_start, current_end = trends.week_period_bounds(period_start.date())
        while current_start < period_end:
            windows.append((current_start, current_end))
            current_start += timedelta(days=7)
            current_end += timedelta(days=7)
        return windows

    def _normalized_period_key(self, *, period_start: Any, period_end: Any) -> tuple[Any, Any]:
        return (
            self._normalized_period_datetime(period_start),
            self._normalized_period_datetime(period_end),
        )

    @staticmethod
    def _normalized_period_datetime(value: Any) -> Any:
        if not isinstance(value, datetime):
            return value
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    def _trend_docs_by_window(
        self,
        *,
        granularity: str,
        period_start: Any,
        period_end: Any,
    ) -> dict[tuple[Any, Any], Any]:
        docs = cast(Any, self.service.repository).list_documents(
            doc_type="trend",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            order_by="event_asc",
            limit=500,
        )
        docs_by_window: dict[tuple[Any, Any], Any] = {}
        for doc in docs:
            raw_start = getattr(doc, "period_start", None)
            raw_end = getattr(doc, "period_end", None)
            if raw_start is None or raw_end is None:
                continue
            docs_by_window[
                self._normalized_period_key(
                    period_start=raw_start,
                    period_end=raw_end,
                )
            ] = doc
        return docs_by_window

    def _trend_doc_contract_ready(self, *, doc: Any) -> bool:
        doc_id = int(getattr(doc, "id") or 0)
        if doc_id <= 0:
            return False
        summary_chunk = cast(Any, self.service.repository).read_document_chunk(
            doc_id=doc_id,
            chunk_index=0,
        )
        if summary_chunk is None or not str(getattr(summary_chunk, "text", "") or "").strip():
            return False
        meta_chunk = cast(Any, self.service.repository).read_document_chunk(
            doc_id=doc_id,
            chunk_index=1,
        )
        if meta_chunk is None:
            return False
        try:
            trends.TrendPayload.model_validate(
                orjson.loads(str(getattr(meta_chunk, "text", "") or "{}"))
            )
        except Exception:
            return False
        return True

    def _repair_trend_source_from_pass_output(
        self,
        *,
        granularity: str,
        period_start: Any,
        period_end: Any,
    ) -> bool:
        row = cast(Any, self.service.repository).get_latest_pass_output(
            pass_kind=TREND_SYNTHESIS_PASS_KIND,
            status="succeeded",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
        )
        if row is None or getattr(row, "id", None) is None:
            return False
        try:
            payload = trends.TrendPayload.model_validate(
                orjson.loads(str(getattr(row, "payload_json", "") or "{}"))
            )
        except Exception:
            return False
        trends.persist_trend_payload(
            repository=cast(Any, self.service.repository),
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            payload=payload,
            pass_output_id=int(getattr(row, "id") or 0),
            pass_kind=TREND_SYNTHESIS_PASS_KIND,
        )
        return True

    def _ensure_trend_source(
        self,
        *,
        granularity: str,
        state: _TrendStageState,
    ) -> _SourceEnsureResult:
        token = f"trend_{granularity}"
        windows = self._trend_source_windows(
            granularity=granularity,
            period_start=state.period_start,
            period_end=state.period_end,
        )
        docs_by_window = self._trend_docs_by_window(
            granularity=granularity,
            period_start=state.period_start,
            period_end=state.period_end,
        )
        if not windows:
            return _SourceEnsureResult(
                token=token,
                doc_type="trend",
                granularity=granularity,
                docs_total=0,
                already_ready=True,
            )
        docs_total = 0
        materialized = False
        all_ready = True
        for window_start, window_end in windows:
            doc = docs_by_window.get(
                self._normalized_period_key(
                    period_start=window_start,
                    period_end=window_end,
                )
            )
            if doc is not None and self._trend_doc_contract_ready(doc=doc):
                docs_total += 1
                continue
            all_ready = False
            repaired = self._repair_trend_source_from_pass_output(
                granularity=granularity,
                period_start=window_start,
                period_end=window_end,
            )
            if not repaired and doc is None:
                self._run_nested_trends_stage(
                    granularity=granularity,
                    anchor_date=window_start.date(),
                    model=state.model,
                )
                docs_by_window = self._trend_docs_by_window(
                    granularity=granularity,
                    period_start=state.period_start,
                    period_end=state.period_end,
                )
                doc = docs_by_window.get(
                    self._normalized_period_key(
                        period_start=window_start,
                        period_end=window_end,
                    )
                )
                repaired = doc is not None and self._trend_doc_contract_ready(doc=doc)
            if repaired:
                materialized = True
                docs_total += 1
                continue
            self.log.warning(
                "Required trend source missing structured corpus granularity={} period_start={} period_end={}",
                granularity,
                window_start.isoformat(),
                window_end.isoformat(),
            )
            return _SourceEnsureResult(
                token=token,
                doc_type="trend",
                granularity=granularity,
                docs_total=docs_total,
                failed=True,
            )
        return _SourceEnsureResult(
            token=token,
            doc_type="trend",
            granularity=granularity,
            docs_total=docs_total,
            already_ready=all_ready,
            materialized=materialized and not all_ready,
        )

    def _run_nested_trends_stage(
        self,
        *,
        granularity: str,
        anchor_date: date,
        model: str,
    ) -> None:
        run_trends_stage(
            self.service,
            request=TrendStageRequest(
                run_id=self.request.run_id,
                granularity=granularity,
                anchor_date=anchor_date,
                llm_model=model,
                backfill=False,
                backfill_mode="missing",
                reuse_existing_corpus=self.request.reuse_existing_corpus,
            ),
        )

    def _run_backfill_if_requested(self, state: _TrendStageState) -> None:
        prev_granularity = cast(Any, trends).prev_level_for_granularity(
            state.normalized_granularity
        )
        if not self.request.backfill or prev_granularity not in {"day", "week"}:
            return

        backfill_started = time.perf_counter()
        if prev_granularity == "day":
            stats = self._run_day_backfill(state)
            log_label = "week"
        else:
            stats = self._run_week_backfill(state)
            log_label = "month"
        duration_ms = int((time.perf_counter() - backfill_started) * 1000)
        log_stats = {
            **stats,
            "duration_ms": duration_ms,
            "mode": state.normalized_backfill_mode,
        }
        self.log.info("Trends {} backfill done stats={}", log_label, log_stats)
        for metric_name, value in (
            ("pipeline.trends.backfill.days_total", stats["days_total"]),
            ("pipeline.trends.backfill.missing_total", stats["missing_total"]),
            ("pipeline.trends.backfill.generated_total", stats["generated_total"]),
            ("pipeline.trends.backfill.skipped_total", stats["skipped_total"]),
            ("pipeline.trends.backfill.failed_total", stats["failed_total"]),
            ("pipeline.trends.backfill.duration_ms", duration_ms),
        ):
            self.record_metric(
                name=metric_name,
                value=value,
                unit="ms" if metric_name.endswith("duration_ms") else "count",
            )

    def _run_day_backfill(self, state: _TrendStageState) -> dict[str, int]:
        stats = {
            "days_total": 7,
            "missing_total": 0,
            "generated_total": 0,
            "skipped_total": 0,
            "failed_total": 0,
        }
        week_start_day = state.period_start.date()
        for offset in range(stats["days_total"]):
            day = week_start_day + timedelta(days=offset)
            day_start, day_end = trends.day_period_bounds(day)
            is_missing = self._trend_missing(
                granularity="day",
                period_start=day_start,
                period_end=day_end,
            )
            if is_missing:
                stats["missing_total"] += 1
            if state.normalized_backfill_mode == "missing" and not is_missing:
                stats["skipped_total"] += 1
                self.log.info(
                    "Trends backfill progress target={} current={} total={} substage={} action={}",
                    day.isoformat(),
                    offset + 1,
                    stats["days_total"],
                    "probe_existing",
                    "skip_existing",
                )
                continue
            self.log.info(
                "Trends backfill progress target={} current={} total={} substage={} action={}",
                day.isoformat(),
                offset + 1,
                stats["days_total"],
                "generate_day_trend",
                "start",
            )
            try:
                self._run_child_request(
                    granularity="day",
                    anchor_date=day,
                    model=state.model,
                )
                stats["generated_total"] += 1
                self.log.info(
                    "Trends backfill progress target={} current={} total={} substage={} action={}",
                    day.isoformat(),
                    offset + 1,
                    stats["days_total"],
                    "generate_day_trend",
                    "done",
                )
            except Exception as exc:  # noqa: BLE001
                stats["failed_total"] += 1
                self.log.warning(
                    "Trends week backfill failed day={} error_type={} error={}",
                    day.isoformat(),
                    type(exc).__name__,
                    self.service._sanitize_error_message(str(exc)),
                )
        return stats

    def _run_week_backfill(self, state: _TrendStageState) -> dict[str, int]:
        stats = {
            "days_total": 0,
            "missing_total": 0,
            "generated_total": 0,
            "skipped_total": 0,
            "failed_total": 0,
        }
        cursor = state.period_start.date()
        while True:
            week_start, week_end = trends.week_period_bounds(cursor)
            if week_start >= state.period_end:
                break
            stats["days_total"] += 1
            is_missing = self._trend_missing(
                granularity="week",
                period_start=week_start,
                period_end=week_end,
            )
            if is_missing:
                stats["missing_total"] += 1
            if state.normalized_backfill_mode == "missing" and not is_missing:
                stats["skipped_total"] += 1
                self.log.info(
                    "Trends backfill progress target={} current={} total={} substage={} action={}",
                    week_start.date().isoformat(),
                    stats["days_total"],
                    "-",
                    "probe_existing",
                    "skip_existing",
                )
                cursor = (week_start + timedelta(days=7)).date()
                continue
            self.log.info(
                "Trends backfill progress target={} current={} total={} substage={} action={}",
                week_start.date().isoformat(),
                stats["days_total"],
                "-",
                "generate_week_trend",
                "start",
            )
            try:
                self._run_child_request(
                    granularity="week",
                    anchor_date=week_start.date(),
                    model=state.model,
                )
                stats["generated_total"] += 1
                self.log.info(
                    "Trends backfill progress target={} current={} total={} substage={} action={}",
                    week_start.date().isoformat(),
                    stats["days_total"],
                    "-",
                    "generate_week_trend",
                    "done",
                )
            except Exception as exc:  # noqa: BLE001
                stats["failed_total"] += 1
                self.log.warning(
                    "Trends month backfill failed week_start={} error_type={} error={}",
                    week_start.date().isoformat(),
                    type(exc).__name__,
                    self.service._sanitize_error_message(str(exc)),
                )
            cursor = (week_start + timedelta(days=7)).date()
        return stats

    def _run_child_request(
        self,
        *,
        granularity: str,
        anchor_date: date,
        model: str,
    ) -> None:
        run_trends_stage(
            self.service,
            request=TrendStageRequest(
                run_id=self.request.run_id,
                granularity=granularity,
                anchor_date=anchor_date,
                llm_model=model,
                backfill=False,
                backfill_mode="missing",
                reuse_existing_corpus=self.request.reuse_existing_corpus,
            ),
        )

    def _trend_missing(
        self,
        *,
        granularity: str,
        period_start: Any,
        period_end: Any,
    ) -> bool:
        existing = cast(Any, self.service.repository).list_documents(
            doc_type="trend",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            order_by="event_desc",
            offset=0,
            limit=1,
        )
        return not bool(existing)

    def _build_generation_artifacts(
        self,
        state: _TrendStageState,
    ) -> _TrendGenerationArtifacts:
        plan = self._build_generation_plan(state)
        source_results = self._ensure_required_sources(state=state, plan=plan)
        corpus_docs_total = self._corpus_docs_total(
            state=state,
            source_results=source_results,
        )
        self.record_metric(
            name="pipeline.trends.corpus.docs_total",
            value=corpus_docs_total,
            unit="count",
        )
        if corpus_docs_total <= 0:
            return self._build_empty_generation(state, corpus_docs_total)
        return self._build_non_empty_generation(
            state,
            corpus_docs_total,
            plan=plan,
        )

    def _corpus_docs_total(
        self,
        *,
        state: _TrendStageState,
        source_results: dict[str, _SourceEnsureResult],
    ) -> int:
        primary_token = self._source_token(
            doc_type=state.corpus_doc_type,
            granularity=state.corpus_granularity,
        )
        report = source_results.get(primary_token)
        return int(report.docs_total) if report is not None else 0

    def _build_empty_generation(
        self,
        state: _TrendStageState,
        corpus_docs_total: int,
    ) -> _TrendGenerationArtifacts:
        self.log.info(
            "Trends corpus is empty; skipping LLM invocation granularity={} period_start={} period_end={}",
            state.normalized_granularity,
            state.period_start.isoformat(),
            state.period_end.isoformat(),
        )
        self.record_metric(
            name="pipeline.trends.corpus.empty",
            value=1.0,
            unit="bool",
        )
        payload = trends.build_empty_trend_payload(
            granularity=state.normalized_granularity,
            period_start=state.period_start,
            period_end=state.period_end,
            output_language=self.service.settings.llm_output_language,
        )
        debug = {"empty_corpus": True} if state.include_debug else None
        for metric_name, value, unit in (
            ("pipeline.trends.llm_requests_total", 0, "count"),
            ("pipeline.trends.llm_input_tokens_total", 0, "count"),
            ("pipeline.trends.llm_output_tokens_total", 0, "count"),
            ("pipeline.trends.estimated_cost_usd", 0.0, "usd"),
        ):
            self.record_metric(name=metric_name, value=value, unit=unit)
        return _TrendGenerationArtifacts(
            payload=payload,
            debug=debug,
            empty_corpus=True,
            corpus_docs_total=corpus_docs_total,
            evolution_normalization_stats={
                "history_windows_normalized_total": 0,
                "history_windows_dropped_total": 0,
                "signals_dropped_total": 0,
            },
        )

    def _build_non_empty_generation(
        self,
        state: _TrendStageState,
        corpus_docs_total: int,
        *,
        plan: trends.TrendGenerationPlan | None,
    ) -> _TrendGenerationArtifacts:
        self.record_metric(
            name="pipeline.trends.corpus.empty",
            value=0.0,
            unit="bool",
        )
        (
            overview_pack_md,
            overview_pack_stats,
            rag_sources,
            ranking_n,
            rep_source_doc_type,
        ) = self._build_overview_pack(state, plan)
        history_pack_md, history_pack_stats, evolution_max_signals = (
            self._build_history_pack(state, plan)
        )
        generation_inputs = _TrendGenerationInputs(
            overview_pack_md=overview_pack_md,
            history_pack_md=history_pack_md,
            rag_sources=rag_sources,
            ranking_n=ranking_n,
            rep_source_doc_type=rep_source_doc_type,
            evolution_max_signals=evolution_max_signals,
        )
        payload, debug = self._generate_trend_payload(
            state=state,
            corpus_docs_total=corpus_docs_total,
            inputs=generation_inputs,
        )

        evolution_normalization_stats, evolution_suppressed_without_history = (
            self._normalize_evolution(
                state=state,
                payload=payload,
                plan=plan,
                history_pack_stats=history_pack_stats,
            )
        )
        self._record_generation_debug(
            debug=debug,
            annotation=_TrendDebugAnnotation(
                payload=payload,
                overview_pack_md=overview_pack_md,
                history_pack_md=history_pack_md,
                overview_pack_stats=overview_pack_stats,
                history_pack_stats=history_pack_stats,
                evolution_normalization_stats=evolution_normalization_stats,
                evolution_suppressed_without_history=evolution_suppressed_without_history,
            ),
        )
        self._record_evolution_metrics(
            payload=payload,
            evolution_normalization_stats=evolution_normalization_stats,
            evolution_suppressed_without_history=evolution_suppressed_without_history,
        )
        rep_stats = self._record_rep_enforcement(payload=payload, state=state)
        return self._generation_artifacts_from_payload(
            _TrendArtifactsRequest(
                payload=payload,
                debug=debug,
                corpus_docs_total=corpus_docs_total,
                inputs=generation_inputs,
                overview_pack_stats=overview_pack_stats,
                history_pack_stats=history_pack_stats,
                evolution_normalization_stats=evolution_normalization_stats,
                evolution_suppressed_without_history=evolution_suppressed_without_history,
                plan=plan,
                rep_stats=rep_stats,
            )
        )

    def _record_generation_debug(
        self,
        *,
        debug: dict[str, Any] | None,
        annotation: _TrendDebugAnnotation,
    ) -> None:
        if not isinstance(debug, dict):
            return
        self._annotate_trend_debug(debug=debug, annotation=annotation)
        self._record_debug_usage_metrics(debug)

    def _record_rep_enforcement(
        self,
        *,
        payload: Any,
        state: _TrendStageState,
    ) -> dict[str, int]:
        _ = payload
        _ = state
        rep_stats = {
            "dropped_non_item_total": 0,
            "backfilled_total": 0,
            "failed_clusters_total": 0,
        }
        self._record_rep_metrics(rep_stats)
        return rep_stats

    def _generate_trend_payload(
        self,
        *,
        state: _TrendStageState,
        corpus_docs_total: int,
        inputs: _TrendGenerationInputs,
    ) -> tuple[Any, dict[str, Any] | None]:
        self.log.info(
            "Trends synthesis starting granularity={} corpus_doc_type={} corpus_docs_total={} overview_pack_chars={} history_pack_chars={}",
            state.normalized_granularity,
            state.corpus_doc_type,
            corpus_docs_total,
            len(str(inputs.overview_pack_md or "")),
            len(str(inputs.history_pack_md or "")),
        )
        generate_started = time.perf_counter()
        payload, debug = trends.generate_trend_via_tools(
            repository=cast(Any, self.service.repository),
            run_id=self.request.run_id,
            llm_model=state.model,
            output_language=self.service.settings.llm_output_language,
            embedding_model=self.service.settings.trends_embedding_model,
            embedding_dimensions=self.service.settings.trends_embedding_dimensions,
            embedding_batch_max_inputs=self.service.settings.trends_embedding_batch_max_inputs,
            embedding_batch_max_chars=self.service.settings.trends_embedding_batch_max_chars,
            embedding_failure_mode=getattr(
                self.service.settings,
                "trends_embedding_failure_mode",
                "continue",
            ),
            embedding_max_errors=int(
                getattr(self.service.settings, "trends_embedding_max_errors", 0) or 0
            ),
            lancedb_dir=self.service.settings.rag_lancedb_dir,
            granularity=state.normalized_granularity,
            period_start=state.period_start,
            period_end=state.period_end,
            corpus_doc_type=state.corpus_doc_type,
            corpus_granularity=state.corpus_granularity,
            overview_pack_md=inputs.overview_pack_md,
            history_pack_md=inputs.history_pack_md,
            rag_sources=inputs.rag_sources,
            ranking_n=inputs.ranking_n,
            rep_source_doc_type=inputs.rep_source_doc_type,
            evolution_max_signals=inputs.evolution_max_signals,
            include_debug=state.include_debug,
            metric_namespace=self.metric_namespace,
            llm_connection=self.service._llm_connection,
        )
        generate_duration_ms = self.record_duration_metric(
            name="pipeline.trends.generate.duration_ms",
            started_at=generate_started,
        )
        self.log.info(
            "Trends synthesis completed granularity={} duration_ms={} tool_calls_total={}",
            state.normalized_granularity,
            generate_duration_ms,
            int(debug.get("tool_calls_total") or 0) if isinstance(debug, dict) else 0,
        )
        return payload, debug if isinstance(debug, dict) else None

    def _annotate_trend_debug(
        self,
        *,
        debug: dict[str, Any],
        annotation: _TrendDebugAnnotation,
    ) -> None:
        debug["context_packs"] = {
            "overview_pack_md": annotation.overview_pack_md,
            "history_pack_md": annotation.history_pack_md,
        }
        if annotation.overview_pack_stats is not None:
            debug["overview_pack_stats"] = annotation.overview_pack_stats
        if annotation.history_pack_stats is not None:
            debug["history_pack_stats"] = annotation.history_pack_stats
        debug["evolution"] = {
            "present": False,
            "signals_total": 0,
            "suppressed_without_history": False,
            "normalization": annotation.evolution_normalization_stats,
        }

    def _generation_artifacts_from_payload(
        self,
        request: _TrendArtifactsRequest,
    ) -> _TrendGenerationArtifacts:
        return _TrendGenerationArtifacts(
            payload=request.payload,
            debug=request.debug,
            empty_corpus=False,
            corpus_docs_total=request.corpus_docs_total,
            overview_pack_md=request.inputs.overview_pack_md,
            history_pack_md=request.inputs.history_pack_md,
            rag_sources=request.inputs.rag_sources,
            ranking_n=request.inputs.ranking_n,
            rep_source_doc_type=request.inputs.rep_source_doc_type,
            evolution_max_signals=request.inputs.evolution_max_signals,
            overview_pack_stats=request.overview_pack_stats,
            history_pack_stats=request.history_pack_stats,
            evolution_normalization_stats=request.evolution_normalization_stats,
            evolution_suppressed_without_history=request.evolution_suppressed_without_history,
            plan=request.plan,
            rep_dropped_non_item_total=int(request.rep_stats["dropped_non_item_total"]),
            rep_backfilled_total=int(request.rep_stats["backfilled_total"]),
            rep_failed_clusters_total=int(request.rep_stats["failed_clusters_total"]),
        )

    def _build_generation_plan(
        self,
        state: _TrendStageState,
    ) -> trends.TrendGenerationPlan | None:
        self_similar_enabled = bool(
            getattr(self.service.settings, "trends_self_similar_enabled", False)
        )
        peer_history_enabled = bool(
            getattr(self.service.settings, "trends_peer_history_enabled", False)
        )
        if not self_similar_enabled and not peer_history_enabled:
            return None
        return trends.TrendGenerationPlan(
            target_granularity=state.normalized_granularity,
            period_start=state.period_start,
            period_end=state.period_end,
            peer_history_window_count=(
                int(
                    getattr(
                        self.service.settings,
                        "trends_peer_history_window_count",
                        0,
                    )
                    or 0
                )
                if peer_history_enabled
                else 0
            ),
        )

    def _build_overview_pack(
        self,
        state: _TrendStageState,
        plan: trends.TrendGenerationPlan | None,
    ) -> tuple[
        str | None,
        dict[str, Any] | None,
        list[dict[str, str | None]] | None,
        int | None,
        str | None,
    ]:
        if not bool(
            getattr(self.service.settings, "trends_self_similar_enabled", False)
        ):
            return None, None, None, None, None
        if plan is None:
            return None, None, None, None, None
        overview_pack_started = time.perf_counter()
        self.log.info(
            "Trends overview pack building granularity={} strategy={}",
            state.normalized_granularity,
            str(getattr(plan, "overview_pack_strategy", "") or "").strip() or "-",
        )
        overview_pack_md, pack_stats = trends.build_overview_pack_md(
            cast(Any, self.service.repository),
            plan,
            overview_pack_max_chars=int(
                getattr(self.service.settings, "trends_overview_pack_max_chars", 8000)
                or 8000
            ),
            item_overview_top_k=int(
                getattr(self.service.settings, "trends_item_overview_top_k", 20) or 20
            ),
            item_overview_item_max_chars=int(
                getattr(
                    self.service.settings,
                    "trends_item_overview_item_max_chars",
                    500,
                )
                or 500
            ),
            min_relevance_score=float(
                getattr(self.service.settings, "min_relevance_score", 0.0) or 0.0
            ),
        )
        overview_pack_duration_ms = self.record_duration_metric(
            name="pipeline.trends.overview_pack.duration_ms",
            started_at=overview_pack_started,
        )
        self.log.info(
            "Trends overview pack built granularity={} duration_ms={} chars={} truncated={}",
            state.normalized_granularity,
            overview_pack_duration_ms,
            len(str(overview_pack_md or "")),
            bool(isinstance(pack_stats, dict) and pack_stats.get("truncated")),
        )
        if isinstance(pack_stats, dict) and bool(pack_stats.get("truncated")):
            self.record_metric(
                name="pipeline.trends.overview_pack.truncated_total",
                value=1,
                unit="count",
            )
        rag_sources = list(getattr(plan, "rag_sources", []) or [])
        ranking_n = int(getattr(self.service.settings, "trends_ranking_n", 10) or 10)
        rep_source_doc_type = str(
            getattr(plan, "rep_source_doc_type", "item") or "item"
        ).strip()
        return overview_pack_md, pack_stats, rag_sources, ranking_n, rep_source_doc_type

    def _build_history_pack(
        self,
        state: _TrendStageState,
        plan: trends.TrendGenerationPlan | None,
    ) -> tuple[str | None, dict[str, Any] | None, int | None]:
        if not bool(
            getattr(self.service.settings, "trends_peer_history_enabled", False)
        ):
            return None, None, None
        if plan is None:
            return None, None, None
        history_pack_started = time.perf_counter()
        self.log.info(
            "Trends history pack building granularity={} window_count={}",
            state.normalized_granularity,
            int(getattr(plan, "peer_history_window_count", 0) or 0),
        )
        history_pack_md, history_pack_stats = trends.build_history_pack_md(
            cast(Any, self.service.repository),
            plan,
            history_pack_max_chars=int(
                getattr(
                    self.service.settings,
                    "trends_peer_history_max_chars",
                    6000,
                )
                or 6000
            ),
        )
        history_pack_duration_ms = self.record_duration_metric(
            name="pipeline.trends.history.pack.duration_ms",
            started_at=history_pack_started,
        )
        self.log.info(
            "Trends history pack built granularity={} duration_ms={} chars={} available_windows={} missing_windows={}",
            state.normalized_granularity,
            history_pack_duration_ms,
            len(str(history_pack_md or "")),
            int(history_pack_stats.get("available_windows") or 0),
            int(history_pack_stats.get("missing_windows") or 0),
        )
        self.record_metric(
            name="pipeline.trends.history.windows_requested",
            value=float(history_pack_stats.get("requested_windows") or 0),
            unit="count",
        )
        self.record_metric(
            name="pipeline.trends.history.windows_available",
            value=float(history_pack_stats.get("available_windows") or 0),
            unit="count",
        )
        self.record_metric(
            name="pipeline.trends.history.windows_missing",
            value=float(history_pack_stats.get("missing_windows") or 0),
            unit="count",
        )
        if bool(history_pack_stats.get("truncated")):
            self.record_metric(
                name="pipeline.trends.history.pack.truncated_total",
                value=1,
                unit="count",
            )
        evolution_max_signals = int(
            getattr(self.service.settings, "trends_evolution_max_signals", 5) or 5
        )
        return history_pack_md, history_pack_stats, evolution_max_signals

    def _normalize_evolution(
        self,
        *,
        state: _TrendStageState,
        payload: Any,
        plan: trends.TrendGenerationPlan | None,
        history_pack_stats: dict[str, Any] | None,
    ) -> tuple[dict[str, int], bool]:
        _ = state
        _ = payload
        _ = plan
        _ = history_pack_stats
        return (
            {
            "history_windows_normalized_total": 0,
            "history_windows_dropped_total": 0,
            "signals_dropped_total": 0,
            },
            False,
        )

    def _record_debug_usage_metrics(self, debug: dict[str, Any]) -> None:
        usage = debug.get("usage")
        if isinstance(usage, dict):
            if isinstance(usage.get("requests"), (int, float)):
                self.record_metric(
                    name="pipeline.trends.llm_requests_total",
                    value=float(usage["requests"]),
                    unit="count",
                )
            if isinstance(usage.get("input_tokens"), (int, float)):
                self.record_metric(
                    name="pipeline.trends.llm_input_tokens_total",
                    value=float(usage["input_tokens"]),
                    unit="count",
                )
            if isinstance(usage.get("output_tokens"), (int, float)):
                self.record_metric(
                    name="pipeline.trends.llm_output_tokens_total",
                    value=float(usage["output_tokens"]),
                    unit="count",
                )
        if isinstance(debug.get("prompt_chars"), (int, float)):
            self.record_metric(
                name="pipeline.trends.prompt_chars",
                value=float(debug["prompt_chars"]),
                unit="chars",
            )
        if isinstance(debug.get("overview_pack_chars"), (int, float)):
            self.record_metric(
                name="pipeline.trends.overview_pack.chars",
                value=float(debug["overview_pack_chars"]),
                unit="chars",
            )
        if isinstance(debug.get("history_pack_chars"), (int, float)):
            self.record_metric(
                name="pipeline.trends.history.pack.chars",
                value=float(debug["history_pack_chars"]),
                unit="chars",
            )
        if isinstance(debug.get("estimated_cost_usd"), (int, float)):
            self.record_metric(
                name="pipeline.trends.estimated_cost_usd",
                value=float(debug["estimated_cost_usd"]),
                unit="usd",
            )
        else:
            self.record_metric(
                name="pipeline.trends.cost_missing_total",
                value=1,
                unit="count",
            )

    def _record_evolution_metrics(
        self,
        *,
        payload: Any,
        evolution_normalization_stats: dict[str, int],
        evolution_suppressed_without_history: bool,
    ) -> None:
        _ = payload
        self.record_metric(
            name="pipeline.trends.evolution.emitted_total",
            value=0,
            unit="count",
        )
        self.record_metric(
            name="pipeline.trends.evolution.signals_total",
            value=0,
            unit="count",
        )
        self.record_metric(
            name="pipeline.trends.evolution.suppressed_without_history_total",
            value=1 if evolution_suppressed_without_history else 0,
            unit="count",
        )
        for metric_name, key in (
            (
                "pipeline.trends.evolution.history_windows_normalized_total",
                "history_windows_normalized_total",
            ),
            (
                "pipeline.trends.evolution.history_windows_dropped_total",
                "history_windows_dropped_total",
            ),
            (
                "pipeline.trends.evolution.signals_dropped_total",
                "signals_dropped_total",
            ),
        ):
            self.record_metric(
                name=metric_name,
                value=float(evolution_normalization_stats.get(key, 0)),
                unit="count",
            )

    def _record_rep_metrics(self, rep_stats: dict[str, int]) -> None:
        for metric_name, key in (
            (
                "pipeline.trends.rep_enforcement.dropped_non_item_total",
                "dropped_non_item_total",
            ),
            (
                "pipeline.trends.rep_enforcement.backfilled_total",
                "backfilled_total",
            ),
            (
                "pipeline.trends.rep_enforcement.failed_clusters_total",
                "failed_clusters_total",
            ),
        ):
            self.record_metric(
                name=metric_name,
                value=rep_stats[key],
                unit="count",
            )

    def _run_pass_execution(
        self,
        *,
        state: _TrendStageState,
        generation: _TrendGenerationArtifacts,
        context: _TrendProjectionContext,
    ) -> Any:
        trend_synthesis_diagnostics: dict[str, Any] = {
            "context_packs": {
                "overview_pack_md": generation.overview_pack_md,
                "history_pack_md": generation.history_pack_md,
            },
            "overview_pack_stats": generation.overview_pack_stats,
            "history_pack_stats": generation.history_pack_stats,
            "evolution": {
                "present": False,
                "signals_total": 0,
                "suppressed_without_history": False,
                "normalization": generation.evolution_normalization_stats or {},
            },
            "rep_enforcement": {
                "dropped_non_item_total": generation.rep_dropped_non_item_total,
                "backfilled_total": generation.rep_backfilled_total,
                "failed_clusters_total": generation.rep_failed_clusters_total,
            },
        }
        if isinstance(generation.debug, dict):
            trend_synthesis_diagnostics["debug"] = generation.debug
        trend_synthesis_envelope = build_trend_synthesis_pass_output(
            run_id=self.request.run_id,
            granularity=state.normalized_granularity,
            period_start=state.period_start,
            period_end=state.period_end,
            payload=generation.payload,
            diagnostics=trend_synthesis_diagnostics,
        )

        def _capture_pass_output_failure(exc: BaseException) -> None:
            context.pass_output_failure = {
                "error_type": type(exc).__name__,
                "error_message": self.service._sanitize_error_message(str(exc)),
            }

        return run_pass_definition(
            repository=self.service.repository,
            record_metric=self.record_metric,
            definition=PassDefinition(
                persist=PassPersistSpec(
                    envelope=trend_synthesis_envelope,
                    period_start=state.period_start,
                    period_end=state.period_end,
                    log=self.log.bind(module="pipeline.trends.pass.synthesis"),
                    failure_message=(
                        "Trend synthesis pass output persist failed pass_kind={pass_kind} "
                        "granularity={granularity} period_start={period_start} "
                        "period_end={period_end} error_type={error_type} error={error}"
                    ),
                    warning_context={
                        "granularity": state.normalized_granularity,
                        "period_start": state.period_start.isoformat(),
                        "period_end": state.period_end.isoformat(),
                    },
                    sanitize_error=self.service._sanitize_error_message,
                    on_failure=_capture_pass_output_failure,
                    persisted_metric_name="pipeline.trends.pass.synthesis.persisted_total",
                    reraise=False,
                ),
                prepare_projection_state=lambda pass_output_id: (
                    _prepare_trend_projection_state(
                        context,
                        pass_output_id,
                    )
                ),
                build_projection_specs=lambda pass_output_id, projection_state: (
                    _build_trend_projection_specs(
                        context,
                        pass_output_id,
                        projection_state,
                    )
                ),
                allow_projection_without_pass_output=True,
            ),
        )

    def _deliver_outputs(
        self,
        *,
        state: _TrendStageState,
        generation: _TrendGenerationArtifacts,
        projection_state: _TrendProjectionState,
        projection_results: dict[str, Any],
    ) -> _TrendDeliveryStats:
        delivery = _TrendDeliveryStats()
        raw_markdown_note_path = projection_results.get("markdown")
        delivery.markdown_note_path = (
            raw_markdown_note_path if isinstance(raw_markdown_note_path, Path) else None
        )
        skip_reason = self._telegram_skip_reason(
            state=state,
            generation=generation,
            projection_state=projection_state,
        )
        if skip_reason is not None:
            self._log_telegram_skip(
                reason=skip_reason,
                state=state,
                projection_state=projection_state,
            )
            return delivery

        trend_pdf_path, trend_pdf_result = self._render_trend_pdf(
            delivery=delivery,
            markdown_note_path=delivery.markdown_note_path,
        )

        if trend_pdf_path is not None and self.request.debug_pdf:
            self._export_trend_pdf_debug(
                delivery=delivery,
                markdown_note_path=delivery.markdown_note_path,
                trend_pdf_path=trend_pdf_path,
                trend_pdf_result=trend_pdf_result,
            )

        if trend_pdf_path is None:
            return delivery
        self._deliver_pdf_to_telegram(
            delivery=delivery,
            state=state,
            projection_state=projection_state,
            trend_pdf_path=trend_pdf_path,
        )
        return delivery

    def _telegram_skip_reason(
        self,
        *,
        state: _TrendStageState,
        generation: _TrendGenerationArtifacts,
        projection_state: _TrendProjectionState,
    ) -> str | None:
        if "telegram" not in projection_state.targets:
            return "target_disabled"
        if generation.empty_corpus:
            return "empty_corpus"
        if (
            projection_state.telegram_remaining_today is not None
            and projection_state.telegram_remaining_today <= 0
        ):
            return "daily_cap"
        if projection_state.telegram_already_sent:
            return "unchanged"
        return None

    def _log_telegram_skip(
        self,
        *,
        reason: str,
        state: _TrendStageState,
        projection_state: _TrendProjectionState,
    ) -> None:
        if reason == "target_disabled":
            return
        reason_labels = {
            "empty_corpus": "empty corpus",
            "daily_cap": "daily cap",
            "unchanged": "unchanged content",
        }
        self.log.info(
            "Trend Telegram delivery skipped for {} doc_id={} granularity={} period_start={} period_end={}",
            reason_labels.get(reason, reason),
            projection_state.doc_id,
            state.normalized_granularity,
            state.period_start.isoformat(),
            state.period_end.isoformat(),
        )

    def _render_trend_pdf(
        self,
        *,
        delivery: _TrendDeliveryStats,
        markdown_note_path: Path | None,
    ) -> tuple[Path | None, Any]:
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
            if trend_pdf_result.prepared.renderer == "browser":
                delivery.pdf_browser_generated_total = 1
            else:
                delivery.pdf_story_generated_total = 1
            delivery.pdf_generated_total = 1
            return trend_pdf_result.path, trend_pdf_result
        except Exception as pdf_exc:  # noqa: BLE001
            delivery.pdf_failed_total = 1
            self.log.bind(module="pipeline.trends.pdf").warning(
                "Trend PDF render failed: {}",
                self.service._sanitize_error_message(str(pdf_exc)),
            )
            return None, trend_pdf_result

    def _export_trend_pdf_debug(
        self,
        *,
        delivery: _TrendDeliveryStats,
        markdown_note_path: Path | None,
        trend_pdf_path: Path,
        trend_pdf_result: Any,
    ) -> None:
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
                prepared=trend_pdf_result.prepared
                if trend_pdf_result is not None
                else None,
            )
            delivery.pdf_debug_generated_total = 1
            self.log.bind(
                module="pipeline.trends.pdf.debug",
                debug_path=str(debug_dir),
            ).info("Trend PDF debug export completed")
        except Exception as debug_exc:  # noqa: BLE001
            delivery.pdf_debug_failed_total = 1
            self.log.bind(module="pipeline.trends.pdf.debug").warning(
                "Trend PDF debug export failed: {}",
                self.service._sanitize_error_message(str(debug_exc)),
            )

    def _deliver_pdf_to_telegram(
        self,
        *,
        delivery: _TrendDeliveryStats,
        state: _TrendStageState,
        projection_state: _TrendProjectionState,
        trend_pdf_path: Path,
    ) -> None:
        repository_any = cast(Any, self.service.repository)
        try:
            if self.service.telegram_sender is None:
                raise RuntimeError("telegram sender is not configured")
            caption = build_telegram_trend_document_caption(
                title=projection_state.materialized.title,
                overview_md=projection_state.materialized.overview_md,
                granularity=state.normalized_granularity,
                period_start=state.period_start,
            )
            message_id = self.service.telegram_sender.send_document(
                filename=trend_pdf_path.name,
                content=trend_pdf_path.read_bytes(),
                caption=caption,
            )
            repository_any.upsert_trend_delivery(
                doc_id=projection_state.doc_id,
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=projection_state.telegram_destination,
                content_hash=projection_state.trend_delivery_hash,
                message_id=message_id,
                status=DELIVERY_STATUS_SENT,
            )
            delivery.telegram_sent_total = 1
        except Exception as telegram_exc:  # noqa: BLE001
            delivery.telegram_failed_total = 1
            sanitized_error = self.service._sanitize_error_message(str(telegram_exc))
            repository_any.upsert_trend_delivery(
                doc_id=projection_state.doc_id,
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=projection_state.telegram_destination,
                content_hash=projection_state.trend_delivery_hash,
                message_id=None,
                status=DELIVERY_STATUS_FAILED,
                error=sanitized_error,
            )
            self.log.bind(module="pipeline.trends.telegram").warning(
                "Trend Telegram delivery failed: {}",
                sanitized_error,
            )

    def _record_delivery_metrics(self, delivery: _TrendDeliveryStats) -> None:
        for metric_name, value in (
            ("pipeline.trends.pdf.generated_total", delivery.pdf_generated_total),
            ("pipeline.trends.pdf.failed_total", delivery.pdf_failed_total),
            (
                "pipeline.trends.pdf.debug.generated_total",
                delivery.pdf_debug_generated_total,
            ),
            ("pipeline.trends.pdf.debug.failed_total", delivery.pdf_debug_failed_total),
            (
                "pipeline.trends.pdf.browser.generated_total",
                delivery.pdf_browser_generated_total,
            ),
            (
                "pipeline.trends.pdf.story.generated_total",
                delivery.pdf_story_generated_total,
            ),
            ("pipeline.trends.telegram.sent_total", delivery.telegram_sent_total),
            ("pipeline.trends.telegram.failed_total", delivery.telegram_failed_total),
        ):
            self.record_metric(name=metric_name, value=value, unit="count")

    def _record_success_debug_artifact(
        self,
        *,
        state: _TrendStageState,
        generation: _TrendGenerationArtifacts,
        doc_id: int,
        pass_output_id: int | None,
    ) -> None:
        if not state.include_debug or generation.debug is None:
            return
        self.service._record_debug_artifact(
            run_id=self.request.run_id,
            item_id=None,
            kind="llm_response",
            payload={
                "stage": "trends",
                "granularity": state.normalized_granularity,
                "period_start": state.period_start.isoformat(),
                "period_end": state.period_end.isoformat(),
                "trend_doc_id": doc_id,
                "trend_synthesis_pass_output_id": pass_output_id,
                "debug": generation.debug,
            },
            log=self.log,
            failure_message="Trends debug artifact record failed: {}",
        )

    def _record_tool_metrics(self, debug: dict[str, Any] | None) -> None:
        tool_calls_total = (
            int(debug.get("tool_calls_total") or 0) if isinstance(debug, dict) else 0
        )
        self.record_metric(
            name="pipeline.trends.tool_calls_total",
            value=tool_calls_total,
            unit="count",
        )
        if not isinstance(debug, dict):
            return
        tool_call_breakdown = debug.get("tool_call_breakdown")
        if not isinstance(tool_call_breakdown, dict):
            return
        for raw_tool_name, raw_count in sorted(tool_call_breakdown.items()):
            if not isinstance(raw_count, (int, float)):
                continue
            metric_tool_name = metric_token(str(raw_tool_name), max_len=32)
            if not metric_tool_name:
                continue
            self.record_metric(
                name=f"pipeline.trends.tool.{metric_tool_name}.calls_total",
                value=float(raw_count),
                unit="count",
            )

    def _handle_failure(
        self,
        *,
        exc: BaseException,
        state: _TrendStageState | None,
    ) -> None:
        sanitized_error = self.service._sanitize_error_message(str(exc))
        anchor = (
            state.anchor
            if state is not None
            else (self.request.anchor_date or utc_now().date())
        )
        granularity = (
            state.normalized_granularity
            if state is not None
            else str(self.request.granularity or "").strip().lower()
        )
        self.service._record_debug_artifact(
            run_id=self.request.run_id,
            item_id=None,
            kind="error_context",
            payload={
                "stage": "trends",
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                "granularity": granularity,
                "anchor_date": anchor.isoformat(),
                **self.service._classify_exception(exc),
            },
            log=self.log,
            failure_message="Trends error artifact record failed: {}",
        )
        self.record_metric(
            name="pipeline.trends.failed_total",
            value=1,
            unit="count",
        )
        self.record_metric(
            name="pipeline.trends.duration_ms",
            value=int((time.perf_counter() - self.started) * 1000),
            unit="ms",
        )
        self.log.warning("Trends failed: {}", sanitized_error)


def _prepare_trend_projection_state(
    context: _TrendProjectionContext,
    pass_output_id: int | None,
) -> _TrendProjectionState:
    state = context.state
    generation = context.generation
    service = context.service
    if pass_output_id is None:
        service._record_debug_artifact(
            run_id=context.request.run_id,
            item_id=None,
            kind="pass_output_failure",
            payload={
                "stage": "trends",
                "pass_kind": "trend_synthesis",
                "granularity": state.normalized_granularity,
                "period_start": state.period_start.isoformat(),
                "period_end": state.period_end.isoformat(),
                "failure": context.pass_output_failure or {},
            },
            log=context.log,
            failure_message="Trends pass output failure artifact record failed: {}",
        )

    doc_id = trends.persist_trend_payload(
        repository=cast(Any, service.repository),
        granularity=state.normalized_granularity,
        period_start=state.period_start,
        period_end=state.period_end,
        payload=generation.payload,
        pass_output_id=pass_output_id,
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
    )
    materialized = materialize_trend_note_payload(
        repository=cast(Any, service.repository),
        payload=generation.payload,
        markdown_output_dir=service.settings.markdown_output_dir,
        output_language=service.settings.llm_output_language,
    )
    _record_note_doc_ref_metrics(context, materialized)
    targets = set(service.settings.publish_targets or [])
    _validate_projection_targets(context, targets)
    trend_delivery_hash = _build_trend_delivery_hash(
        normalized_granularity=state.normalized_granularity,
        period_start=state.period_start,
        period_end=state.period_end,
        materialized=materialized,
    )
    (
        telegram_destination,
        telegram_remaining_today,
        telegram_already_sent,
        telegram_can_attempt_delivery,
    ) = _resolve_telegram_delivery_state(
        context=context,
        doc_id=doc_id,
        targets=targets,
        trend_delivery_hash=trend_delivery_hash,
    )
    return _TrendProjectionState(
        doc_id=doc_id,
        materialized=materialized,
        targets=targets,
        telegram_destination=telegram_destination,
        telegram_remaining_today=telegram_remaining_today,
        telegram_already_sent=telegram_already_sent,
        telegram_can_attempt_delivery=telegram_can_attempt_delivery,
        trend_delivery_hash=trend_delivery_hash,
    )


def _record_note_doc_ref_metrics(
    context: _TrendProjectionContext,
    materialized: MaterializedTrendNotePayload,
) -> None:
    rewrite_occurrences_total = materialized.rewrite_stats.doc_ref_occurrences_total
    rewrite_doc_ids_resolved_total = materialized.rewrite_stats.doc_ref_resolved_total
    rewrite_doc_ids_unresolved_total = (
        materialized.rewrite_stats.doc_ref_unresolved_total
    )
    if rewrite_occurrences_total or rewrite_doc_ids_unresolved_total:
        context.log.info(
            "Trend note doc refs rewritten occurrences={} resolved_doc_ids={} unresolved_doc_ids={}",
            rewrite_occurrences_total,
            rewrite_doc_ids_resolved_total,
            rewrite_doc_ids_unresolved_total,
        )
    for metric_name, value in (
        (
            "pipeline.trends.note_doc_refs_rewrite_occurrences_total",
            rewrite_occurrences_total,
        ),
        (
            "pipeline.trends.note_doc_refs_resolved_total",
            rewrite_doc_ids_resolved_total,
        ),
        (
            "pipeline.trends.note_doc_refs_unresolved_total",
            rewrite_doc_ids_unresolved_total,
        ),
    ):
        context.record_metric(name=metric_name, value=value, unit="count")


def _build_trend_delivery_hash(
    *,
    normalized_granularity: str,
    period_start: Any,
    period_end: Any,
    materialized: MaterializedTrendNotePayload,
) -> str:
    return hashlib.sha256(
        orjson.dumps(
            {
                "title": materialized.title,
                "granularity": normalized_granularity,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": materialized.overview_md,
                "topics": list(materialized.topics),
                "clusters": materialized.clusters,
            },
            option=orjson.OPT_SORT_KEYS,
        )
    ).hexdigest()


def _validate_projection_targets(
    context: _TrendProjectionContext,
    targets: set[str],
) -> None:
    service = context.service
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


def _resolve_telegram_delivery_state(
    *,
    context: _TrendProjectionContext,
    doc_id: int,
    targets: set[str],
    trend_delivery_hash: str,
) -> tuple[str, int | None, bool, bool]:
    service = context.service
    repository_any = cast(Any, service.repository)
    telegram_destination = service._telegram_delivery_destination()
    telegram_remaining_today: int | None = None
    telegram_already_sent = False
    if "telegram" in targets:
        _, _, telegram_remaining_today = service._telegram_delivery_budget()
    if (
        "telegram" in targets
        and not context.generation.empty_corpus
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
    telegram_can_attempt_delivery = (
        "telegram" in targets
        and not context.generation.empty_corpus
        and telegram_remaining_today is not None
        and telegram_remaining_today > 0
        and not telegram_already_sent
    )
    return (
        telegram_destination,
        telegram_remaining_today,
        telegram_already_sent,
        telegram_can_attempt_delivery,
    )


def _build_trend_projection_specs(
    context: _TrendProjectionContext,
    pass_output_id: int | None,
    state: _TrendProjectionState | None,
) -> list[ProjectionSpec]:
    if state is None:
        raise RuntimeError("trend projection state is required")
    warning_context = {
        "doc_id": state.doc_id,
        "granularity": context.state.normalized_granularity,
        "period_start": context.state.period_start.isoformat(),
        "period_end": context.state.period_end.isoformat(),
    }
    return [
        _trend_markdown_projection_spec(
            context=context,
            pass_output_id=pass_output_id,
            projection_state=state,
            warning_context=warning_context,
        ),
        _trend_obsidian_projection_spec(
            context=context,
            pass_output_id=pass_output_id,
            projection_state=state,
            warning_context=warning_context,
        ),
    ]


def _trend_markdown_projection_spec(
    *,
    context: _TrendProjectionContext,
    pass_output_id: int | None,
    projection_state: _TrendProjectionState,
    warning_context: dict[str, Any],
) -> ProjectionSpec:
    service = context.service
    stage_state = context.state
    materialized = projection_state.materialized
    return ProjectionSpec(
        name="markdown",
        enabled="markdown" in projection_state.targets
        or projection_state.telegram_can_attempt_delivery,
        metric_base="pipeline.trends.projection.trend_markdown",
        log=context.log.bind(module="pipeline.trends.projection.trend_markdown"),
        failure_message=(
            "Trend markdown projection failed doc_id={doc_id} "
            "granularity={granularity} period_start={period_start} "
            "period_end={period_end} error_type={error_type} error={error}"
        ),
        execute=lambda: write_markdown_trend_note(
            output_dir=service.settings.markdown_output_dir,
            trend_doc_id=projection_state.doc_id,
            title=materialized.title,
            granularity=stage_state.normalized_granularity,
            period_start=stage_state.period_start,
            period_end=stage_state.period_end,
            run_id=context.request.run_id,
            overview_md=materialized.overview_md,
            topics=list(materialized.topics),
            clusters=materialized.clusters,
            output_language=service.settings.llm_output_language,
            pass_output_id=pass_output_id,
            pass_kind=TREND_SYNTHESIS_PASS_KIND,
            site_exclude=context.generation.empty_corpus,
        ),
        warning_context=warning_context,
        sanitize_error=service._sanitize_error_message,
        reraise=False,
    )


def _trend_obsidian_projection_spec(
    *,
    context: _TrendProjectionContext,
    pass_output_id: int | None,
    projection_state: _TrendProjectionState,
    warning_context: dict[str, Any],
) -> ProjectionSpec:
    service = context.service
    stage_state = context.state
    materialized = projection_state.materialized
    return ProjectionSpec(
        name="obsidian",
        enabled="obsidian" in projection_state.targets
        and service.settings.obsidian_vault_path is not None,
        metric_base="pipeline.trends.projection.trend_obsidian",
        log=context.log.bind(module="pipeline.trends.projection.trend_obsidian"),
        failure_message=(
            "Trend obsidian projection failed doc_id={doc_id} "
            "granularity={granularity} period_start={period_start} "
            "period_end={period_end} error_type={error_type} error={error}"
        ),
        execute=lambda: write_obsidian_trend_note(
            vault_path=service.settings.obsidian_vault_path,
            base_folder=service.settings.obsidian_base_folder,
            trend_doc_id=projection_state.doc_id,
            title=materialized.title,
            granularity=stage_state.normalized_granularity,
            period_start=stage_state.period_start,
            period_end=stage_state.period_end,
            run_id=context.request.run_id,
            overview_md=materialized.overview_md,
            topics=list(materialized.topics),
            clusters=materialized.clusters,
            output_language=service.settings.llm_output_language,
            pass_output_id=pass_output_id,
            pass_kind=TREND_SYNTHESIS_PASS_KIND,
            site_exclude=context.generation.empty_corpus,
        ),
        warning_context=warning_context,
        sanitize_error=service._sanitize_error_message,
        reraise=False,
    )
