from __future__ import annotations

from dataclasses import dataclass, field
import inspect
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait  # noqa: F401
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, TypedDict, Unpack, cast
from urllib.parse import parse_qs, urlparse

import httpx
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.delivery import TelegramSender
from recoleta.extract import (
    extract_arxiv_latex_source,
    convert_html_document_to_markdown,  # noqa: F401
    extract_html_document_cleaned_with_references,  # noqa: F401
    extract_html_maintext,
    extract_pdf_text,  # noqa: F401
    fetch_url_bytes,
    fetch_url_html,
)
from recoleta.llm_connection import llm_connection_from_settings
from recoleta.models import (
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.observability import (
    collect_environment_secrets,
    get_rich_console,
)
from recoleta.pipeline import artifacts as pipeline_artifacts
from recoleta.pipeline import delivery_budget as pipeline_delivery_budget
from recoleta.pipeline import metrics as pipeline_metrics
from recoleta.pipeline.ingest_stage import (
    IngestStageRequest,
    RebalanceItemsRequest,
    SourcePullStageRequest,
    pull_source_drafts as run_source_pull_stage,
    rebalance_items_by_source as rebalance_stage_items_by_source,
    run_ingest_stage,
)
from recoleta.pipeline.enrich_stage import (
    ArxivContentRequest,
    ArxivHtmlDocumentRequest,
    EnrichStageRequest,
    ItemContentRequest,
    PdfContentRequest,
    ensure_arxiv_content,
    ensure_arxiv_html_document_content,
    ensure_item_content,
    ensure_pdf_content,
    run_enrich_stage,
)
from recoleta.pipeline.analyze_runtime import execute_analyze
from recoleta.pipeline.triage_runtime import (
    build_triage_candidates as build_stage_triage_candidates,
    TriageStageRequest,
    execute_triage,
)
from recoleta.pipeline.publish_stage import run_publish_stage
from recoleta.pipeline.ideas_stage import run_ideas_stage
from recoleta.pipeline.trends_stage import TrendStageRequest, run_trends_stage
from recoleta.ports import RepositoryPort
from recoleta import sources
from recoleta.triage import SemanticTriage, TriageCandidate
from recoleta.types import (
    AnalysisResult,
    AnalysisWrite,
    AnalyzeDebug,
    AnalyzeResult,
    IngestResult,
    ItemDraft,
    ItemStateUpdate,
    MetricPoint,
    PublishResult,
    IdeasResult,
    TrendResult,
)

_ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS = (
    "http_404",
    "http_429",
    "http_5xx",
    "http_other",
    "timeout",
    "request_error",
    "missing_url",
    "empty_document",
    "other",
)
_SOURCE_DIAGNOSTIC_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")
_SHORT_CONTENT_DENSE_CHAR_THRESHOLD = 200


@dataclass(slots=True)
class _AnalyzeWorkItem:
    item_id: int
    title: str
    canonical_url: str
    user_topics: list[str]
    content_text: str
    mirror_item_state: bool


@dataclass(slots=True)
class _AnalyzeCallSuccess:
    work_item: _AnalyzeWorkItem
    result: AnalysisResult
    debug: AnalyzeDebug | None


@dataclass(slots=True)
class _AnalyzeCallFailure:
    work_item: _AnalyzeWorkItem
    error: Exception


@dataclass(slots=True)
class _AnalyzeParallelismStats:
    requested: int
    effective: int
    max_inflight: int


@dataclass(slots=True)
class _AnalyzePersistFailure:
    analysis: AnalysisWrite
    error: Exception


@dataclass(slots=True)
class _AnalyzePersistResult:
    persisted: list[AnalysisWrite] = field(default_factory=list)
    failed: list[_AnalyzePersistFailure] = field(default_factory=list)
    analysis_batches_total: int = 0
    analysis_rows_total: int = 0


@dataclass(slots=True)
class _AnalyzeMetricBuildRequest:
    analyze_result: AnalyzeResult
    llm_calls_total: int
    llm_errors_total: int
    missing_content_total: int
    llm_prompt_tokens_total: int
    llm_completion_tokens_total: int
    llm_tokens_seen: bool
    llm_cost_usd_total: float
    llm_cost_seen: bool
    llm_cost_missing_total: int
    llm_calls_by_provider_token: dict[str, int]
    llm_errors_by_provider_token: dict[str, int]
    llm_calls_by_model_token: dict[str, int]
    llm_errors_by_model_token: dict[str, int]
    duration_ms: int
    parallelism: _AnalyzeParallelismStats
    sql_queries_total: int
    sql_commits_total: int
    analysis_batches_total: int
    analysis_rows_total: int
    state_batches_total: int
    state_rows_total: int
    extra_metrics: list[MetricPoint] | None = None


class _EnsureItemContentKwargs(TypedDict, total=False):
    client: httpx.Client
    item: Any
    log: Any
    diag: dict[str, Any] | None
    arxiv_html_throttle: Callable[[], None] | None


class _EnsureArxivContentKwargs(TypedDict, total=False):
    client: httpx.Client
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None
    arxiv_html_throttle: Callable[[], None] | None


class _EnsureArxivHtmlDocumentContentKwargs(TypedDict, total=False):
    client: httpx.Client
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None
    arxiv_html_throttle: Callable[[], None] | None


class _EnsurePdfContentKwargs(TypedDict, total=False):
    client: httpx.Client
    source: str
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None


class _TrendStageRequestKwargs(TypedDict, total=False):
    run_id: str
    granularity: str
    anchor_date: date | None
    llm_model: str | None
    backfill: bool
    backfill_mode: str
    debug_pdf: bool
    reuse_existing_corpus: bool


class PipelineService:
    def __init__(
        self,
        *,
        settings: Settings,
        repository: RepositoryPort,
        analyzer: Analyzer | None = None,
        triage: SemanticTriage | None = None,
        telegram_sender: Any | None = None,
    ) -> None:
        self.settings = settings
        self.repository = repository
        scrub_candidates: list[str] = []
        if settings.telegram_bot_token is not None:
            scrub_candidates.append(settings.telegram_bot_token.get_secret_value())
        if settings.telegram_chat_id is not None:
            scrub_candidates.append(settings.telegram_chat_id.get_secret_value())
        llm_api_key = getattr(settings, "llm_api_key", None)
        if llm_api_key is not None:
            scrub_candidates.append(llm_api_key.get_secret_value())
        resend_api_key = getattr(settings, "resend_api_key", None)
        if resend_api_key is not None:
            scrub_candidates.append(resend_api_key.get_secret_value())
        scrub_candidates.extend(collect_environment_secrets())
        self._scrub_secrets = tuple(dict.fromkeys(scrub_candidates))
        self._llm_connection = llm_connection_from_settings(settings)
        self._progress_console = get_rich_console()
        self.analyzer = analyzer or LiteLLMAnalyzer(
            model=settings.llm_model,
            output_language=settings.llm_output_language,
            content_max_chars=settings.analyze_content_max_chars,
            llm_connection=self._llm_connection,
        )
        self.semantic_triage = triage or SemanticTriage(
            embedding_batch_max_inputs=settings.triage_embedding_batch_max_inputs,
            embedding_batch_max_chars=settings.triage_embedding_batch_max_chars,
            llm_connection=self._llm_connection,
        )
        self.telegram_sender = telegram_sender
        self._pandoc_unavailable_warned = False
        if self.telegram_sender is None and "telegram" in settings.publish_targets:
            if (
                settings.telegram_bot_token is not None
                and settings.telegram_chat_id is not None
            ):
                self.telegram_sender = TelegramSender(
                    token=settings.telegram_bot_token.get_secret_value(),
                    chat_id=settings.telegram_chat_id.get_secret_value(),
                )

    @staticmethod
    def _dense_char_count(text: str) -> int:
        return len("".join(str(text or "").split()))

    @staticmethod
    def _empty_source_pull_stats() -> dict[str, dict[str, int]]:
        return {
            source_name: {
                "drafts_total": 0,
                "pull_failed_total": 0,
                "pull_duration_ms": 0,
                "filtered_out_total": 0,
                "in_window_total": 0,
                "missing_published_at_total": 0,
                "deduped_total": 0,
                "deferred_total": 0,
                "not_modified_total": 0,
                "oldest_published_at_unix": 0,
                "newest_published_at_unix": 0,
                "inserted_total": 0,
                "updated_total": 0,
            }
            for source_name in _SOURCE_DIAGNOSTIC_NAMES
        }

    @staticmethod
    def _invoke_callable_with_supported_kwargs(fn: Any, **kwargs: Any) -> Any:
        try:
            signature = inspect.signature(fn)
        except Exception:
            return fn(**kwargs)
        accepts_var_kwargs = any(
            parameter.kind is inspect.Parameter.VAR_KEYWORD
            for parameter in signature.parameters.values()
        )
        filtered_kwargs = (
            kwargs
            if accepts_var_kwargs
            else {
                key: value
                for key, value in kwargs.items()
                if key in signature.parameters
            }
        )
        return fn(**filtered_kwargs)

    @staticmethod
    def _invoke_source_pull(fn: Any, **kwargs: Any) -> Any:
        return PipelineService._invoke_callable_with_supported_kwargs(fn, **kwargs)

    def _invoke_repository_method(self, method_name: str, /, **kwargs: Any) -> Any:
        method = getattr(self.repository, method_name)
        return self._invoke_callable_with_supported_kwargs(method, **kwargs)

    def _lookup_source_pull_state(
        self,
        *,
        source: str,
        scope_kind: str,
        scope_key: str,
    ) -> sources.SourcePullStateSnapshot | None:
        getter = getattr(self.repository, "get_source_pull_state", None)
        if not callable(getter):
            return None
        result = self._invoke_callable_with_supported_kwargs(
            getter,
            source=source,
            scope_kind=scope_kind,
            scope_key=scope_key,
        )
        return result if isinstance(result, sources.SourcePullStateSnapshot) else None

    def _persist_source_pull_state_updates(
        self,
        *,
        source: str,
        updates: list[sources.SourcePullStateUpdate],
    ) -> None:
        upsert = getattr(self.repository, "upsert_source_pull_state", None)
        if not callable(upsert):
            return
        for update in updates:
            if not isinstance(update, sources.SourcePullStateUpdate):
                continue
            self._invoke_callable_with_supported_kwargs(
                upsert,
                source=source,
                update=update,
            )

    @staticmethod
    def _normalize_source_pull_result(raw: Any) -> sources.SourcePullResult:
        if isinstance(raw, sources.SourcePullResult):
            return raw
        if raw is None:
            return sources.SourcePullResult()
        return sources.SourcePullResult(drafts=list(raw or []))

    @staticmethod
    def _new_source_enrich_bucket() -> dict[str, Any]:
        return {
            "processed_total": 0,
            "skipped_total": 0,
            "failed_total": 0,
            "item_duration_ms_total": 0,
            "fetch_ms_sum": 0,
            "extract_ms_sum": 0,
            "db_read_ms_sum": 0,
            "db_write_ms_sum": 0,
            "input_bytes_sum": 0,
            "content_chars_sum": 0,
            "short_content_total": 0,
            "content_types": {},
            "pdf_backends": {},
        }

    def _configured_source_names(self) -> list[str]:
        settings_sources = getattr(self.settings, "sources", None)
        if settings_sources is None:
            return []
        configured: list[str] = []
        for source_name in _SOURCE_DIAGNOSTIC_NAMES:
            source_settings = getattr(settings_sources, source_name, None)
            if source_settings is None:
                continue
            enabled = getattr(source_settings, "enabled", None)
            if enabled is None or bool(enabled):
                configured.append(source_name)
        return configured

    def _stage_candidate_limit(self, *, limit: int) -> int:
        normalized_limit = max(1, int(limit))
        enabled_sources = self._configured_source_names()
        if len(enabled_sources) <= 1:
            return normalized_limit
        return min(normalized_limit * len(enabled_sources), normalized_limit * 5)

    @staticmethod
    def _rebalance_items_by_source(
        *,
        request: RebalanceItemsRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[list[Any], dict[str, int], dict[str, int]]:
        normalized_request = request or RebalanceItemsRequest(**legacy_kwargs)
        return rebalance_stage_items_by_source(normalized_request)

    def _record_stage_source_selection_metrics(
        self,
        *,
        run_id: str,
        stage: str,
        candidate_counts: dict[str, int],
        deferred_counts: dict[str, int],
    ) -> None:
        sources = sorted(set(candidate_counts) | set(deferred_counts))
        metrics: list[MetricPoint] = []
        for source_name in sources:
            candidate_total = int(candidate_counts.get(source_name) or 0)
            deferred_total = int(deferred_counts.get(source_name) or 0)
            selected_total = max(0, candidate_total - deferred_total)
            metrics.extend(
                [
                    MetricPoint(
                        name=f"pipeline.{stage}.source.{source_name}.candidate_total",
                        value=candidate_total,
                        unit="count",
                    ),
                    MetricPoint(
                        name=f"pipeline.{stage}.source.{source_name}.selected_total",
                        value=selected_total,
                        unit="count",
                    ),
                    MetricPoint(
                        name=f"pipeline.{stage}.source.{source_name}.deferred_total",
                        value=deferred_total,
                        unit="count",
                    ),
                ]
            )
        self._record_metrics_batch(run_id=run_id, metrics=metrics)

    def _record_metrics_batch(
        self,
        *,
        run_id: str,
        metrics: list[MetricPoint],
    ) -> int:
        normalized = [
            MetricPoint(
                name=str(metric.name or "").strip(),
                value=metric.value,
                unit=metric.unit,
            )
            for metric in metrics
            if str(metric.name or "").strip()
        ]
        if not normalized:
            return 0
        batch_recorder = getattr(self.repository, "record_metrics_batch", None)
        if callable(batch_recorder):
            try:
                return cast(int, batch_recorder(run_id=run_id, metrics=normalized))
            except TypeError:
                pass
        for metric in normalized:
            self.repository.record_metric(
                run_id=run_id,
                name=metric.name,
                value=metric.value,
                unit=metric.unit,
            )
        return len(normalized)

    def _save_analyses_batch(self, *, analyses: list[AnalysisWrite]) -> int:
        normalized = [
            AnalysisWrite(
                item_id=int(analysis.item_id),
                result=analysis.result,
                mirror_item_state=bool(analysis.mirror_item_state),
            )
            for analysis in analyses
            if int(getattr(analysis, "item_id", 0) or 0) > 0
        ]
        if not normalized:
            return 0
        batch_saver = getattr(self.repository, "save_analyses_batch", None)
        if callable(batch_saver):
            try:
                return cast(int, batch_saver(analyses=normalized))
            except TypeError:
                pass
        for analysis in normalized:
            self.repository.save_analysis(
                item_id=analysis.item_id,
                result=analysis.result,
                mirror_item_state=analysis.mirror_item_state,
            )
        return len(normalized)

    def _update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int:
        normalized = [
            ItemStateUpdate(
                item_id=int(update.item_id),
                state=str(update.state or "").strip(),
                mirror_item_state=bool(update.mirror_item_state),
            )
            for update in updates
            if int(getattr(update, "item_id", 0) or 0) > 0
            and str(getattr(update, "state", "") or "").strip()
        ]
        if not normalized:
            return 0
        batch_updater = getattr(self.repository, "update_item_states_batch", None)
        if callable(batch_updater):
            try:
                return cast(int, batch_updater(updates=normalized))
            except TypeError:
                pass
        for update in normalized:
            if update.state == ITEM_STATE_RETRYABLE_FAILED:
                self.repository.mark_item_retryable_failed(item_id=update.item_id)
            elif update.state == ITEM_STATE_FAILED:
                self.repository.mark_item_failed(item_id=update.item_id)
            elif update.state == ITEM_STATE_TRIAGED:
                self.repository.mark_item_triaged(item_id=update.item_id)
            elif update.state == ITEM_STATE_ENRICHED:
                self.repository.mark_item_enriched(item_id=update.item_id)
            else:
                self.repository.mark_item_failed(item_id=update.item_id)
        return len(normalized)

    def _requested_analyze_parallelism(self) -> int:
        return max(1, int(self.settings.analyze_max_concurrency))

    def _analyze_write_batch_size(self) -> int:
        return max(1, int(self.settings.analyze_write_batch_size))

    @staticmethod
    def _chunked_batch_ranges(total: int, batch_size: int) -> list[tuple[int, int]]:
        normalized_total = max(0, int(total))
        normalized_batch_size = max(1, int(batch_size))
        return [
            (start, min(start + normalized_batch_size, normalized_total))
            for start in range(0, normalized_total, normalized_batch_size)
        ]

    @classmethod
    def _annotate_content_diag(
        cls,
        diag: dict[str, Any] | None,
        *,
        content_type: str,
        content_text: str,
        pdf_backend: str | None = None,
    ) -> None:
        if diag is None:
            return
        diag["content_type"] = str(content_type).strip().lower()
        diag["content_chars"] = len(content_text)
        diag["short_content"] = (
            1
            if cls._dense_char_count(content_text) < _SHORT_CONTENT_DENSE_CHAR_THRESHOLD
            else 0
        )
        if pdf_backend:
            diag["pdf_backend"] = str(pdf_backend).strip().lower()

    def _log_html_document_md_conversion_skipped(
        self,
        *,
        log: Any,
        item_id: int,
        elapsed_ms: int,
        error: str | None,
    ) -> None:
        error_text = str(error or "").strip()
        is_unavailable = error_text.startswith(
            "pandoc_unavailable"
        ) or error_text.startswith("pypandoc_import_failed")
        if is_unavailable:
            # Avoid spamming logs when pandoc isn't installed in the environment.
            if not self._pandoc_unavailable_warned:
                self._pandoc_unavailable_warned = True
                log.bind(item_id=item_id).warning(
                    "html_document_md conversion skipped (pandoc unavailable) elapsed_ms={} error={}",
                    elapsed_ms,
                    error_text or None,
                )
            else:
                log.bind(item_id=item_id).debug(
                    "html_document_md conversion skipped (pandoc unavailable) elapsed_ms={} error={}",
                    elapsed_ms,
                    error_text or None,
                )
            return

        log.bind(item_id=item_id).warning(
            "html_document_md conversion skipped elapsed_ms={} error={}",
            elapsed_ms,
            error_text or None,
        )

    def _telegram_delivery_destination(self) -> str:
        return pipeline_delivery_budget.telegram_delivery_destination(self.settings)

    def _metric_token(self, value: str, *, max_len: int = 48) -> str:
        return pipeline_metrics.metric_token(value, max_len=max_len)

    def _telegram_delivery_budget(self) -> tuple[str, int, int]:
        return pipeline_delivery_budget.telegram_delivery_budget(
            repository=self.repository,
            settings=self.settings,
        )

    def ingest(
        self,
        *,
        run_id: str,
        drafts: list[ItemDraft] | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> IngestResult:
        return run_ingest_stage(
            self,
            IngestStageRequest(
                run_id=run_id,
                drafts=drafts,
                period_start=period_start,
                period_end=period_end,
            ),
        )

    def prepare(
        self,
        *,
        run_id: str,
        drafts: list[ItemDraft] | None = None,
        limit: int | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> IngestResult:
        effective_limit = self._resolve_analysis_limit(limit=limit)
        candidate_limit = self._resolve_triage_candidate_limit(limit=effective_limit)
        ingest_result = self.ingest(
            run_id=run_id,
            drafts=drafts,
            period_start=period_start,
            period_end=period_end,
        )
        self.enrich(
            run_id=run_id,
            limit=candidate_limit,
            period_start=period_start,
            period_end=period_end,
        )
        self.triage(
            run_id=run_id,
            limit=effective_limit,
            candidate_limit=candidate_limit,
            period_start=period_start,
            period_end=period_end,
        )
        return ingest_result

    def enrich(
        self,
        *,
        run_id: str,
        limit: int,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> None:
        run_enrich_stage(
            self,
            EnrichStageRequest(
                run_id=run_id,
                limit=limit,
                period_start=period_start,
                period_end=period_end,
            ),
        )

    def triage(
        self,
        *,
        run_id: str,
        limit: int,
        candidate_limit: int | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> None:
        return execute_triage(
            TriageStageRequest(
                service=self,
                run_id=run_id,
                limit=limit,
                candidate_limit=candidate_limit,
                period_start=period_start,
                period_end=period_end,
            )
        )

    def _run_analyze_calls(
        self,
        *,
        work_items: list[_AnalyzeWorkItem],
        include_debug: bool,
        description: str,
    ) -> tuple[
        list[_AnalyzeCallSuccess | _AnalyzeCallFailure],
        _AnalyzeParallelismStats,
    ]:
        if not work_items:
            return [], _AnalyzeParallelismStats(
                requested=0, effective=0, max_inflight=0
            )

        requested = self._requested_analyze_parallelism()
        effective = min(requested, len(work_items))
        outcomes: list[_AnalyzeCallSuccess | _AnalyzeCallFailure] = []
        active = 0
        max_inflight = 0
        lock = threading.Lock()

        def _invoke(
            work_item: _AnalyzeWorkItem,
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            nonlocal active, max_inflight
            with lock:
                active += 1
                max_inflight = max(max_inflight, active)
            try:
                return self.analyzer.analyze(
                    title=work_item.title,
                    canonical_url=work_item.canonical_url,
                    user_topics=work_item.user_topics,
                    content=work_item.content_text,
                    include_debug=include_debug,
                )
            finally:
                with lock:
                    active -= 1

        with Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._progress_console,
        ) as progress:
            task_id = progress.add_task(description, total=len(work_items))
            if effective <= 1:
                for work_item in work_items:
                    try:
                        result, debug = _invoke(work_item)
                    except Exception as exc:  # noqa: BLE001
                        outcomes.append(
                            _AnalyzeCallFailure(work_item=work_item, error=exc)
                        )
                    else:
                        outcomes.append(
                            _AnalyzeCallSuccess(
                                work_item=work_item,
                                result=result,
                                debug=debug,
                            )
                        )
                    progress.advance(task_id, 1)
            else:
                with ThreadPoolExecutor(
                    max_workers=effective,
                    thread_name_prefix="recoleta-analyze",
                ) as executor:
                    futures = {
                        executor.submit(_invoke, work_item): work_item
                        for work_item in work_items
                    }
                    for future in as_completed(futures):
                        work_item = futures[future]
                        try:
                            result, debug = future.result()
                        except Exception as exc:  # noqa: BLE001
                            outcomes.append(
                                _AnalyzeCallFailure(work_item=work_item, error=exc)
                            )
                        else:
                            outcomes.append(
                                _AnalyzeCallSuccess(
                                    work_item=work_item,
                                    result=result,
                                    debug=debug,
                                )
                            )
                        progress.advance(task_id, 1)

        return outcomes, _AnalyzeParallelismStats(
            requested=requested,
            effective=effective,
            max_inflight=max_inflight,
        )

    def _persist_analysis_writes(
        self,
        *,
        analyses: list[AnalysisWrite],
    ) -> _AnalyzePersistResult:
        batch_size = self._analyze_write_batch_size()
        result = _AnalyzePersistResult()

        for start, end in self._chunked_batch_ranges(len(analyses), batch_size):
            batch = analyses[start:end]
            try:
                written = self._save_analyses_batch(analyses=batch)
            except Exception as batch_exc:
                if len(batch) == 1:
                    result.failed.append(
                        _AnalyzePersistFailure(
                            analysis=batch[0],
                            error=batch_exc,
                        )
                    )
                    continue
                for analysis in batch:
                    try:
                        written = self._save_analyses_batch(analyses=[analysis])
                    except Exception as item_exc:
                        result.failed.append(
                            _AnalyzePersistFailure(
                                analysis=analysis,
                                error=item_exc,
                            )
                        )
                        continue
                    if written > 0:
                        result.persisted.append(analysis)
                        result.analysis_batches_total += 1
                        result.analysis_rows_total += written
                continue
            if written > 0:
                result.persisted.extend(batch)
                result.analysis_batches_total += 1
                result.analysis_rows_total += written

        return result

    def _persist_state_updates(
        self,
        *,
        state_updates: list[ItemStateUpdate],
    ) -> tuple[int, int]:
        batch_size = self._analyze_write_batch_size()
        state_batches_total = 0
        state_rows_total = 0
        for start, end in self._chunked_batch_ranges(len(state_updates), batch_size):
            updated = self._update_item_states_batch(updates=state_updates[start:end])
            if updated > 0:
                state_batches_total += 1
                state_rows_total += updated

        return state_batches_total, state_rows_total

    def _analyze_parallelism_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        return [
            MetricPoint(
                name="pipeline.analyze.parallelism.requested",
                value=request.parallelism.requested,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.parallelism.effective",
                value=request.parallelism.effective,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.parallelism.max_inflight",
                value=request.parallelism.max_inflight,
                unit="count",
            ),
        ]

    def _analyze_db_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        return [
            MetricPoint(
                name="pipeline.analyze.db.sql_queries_total",
                value=request.sql_queries_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.db.sql_commits_total",
                value=request.sql_commits_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.db.analysis_batches_total",
                value=request.analysis_batches_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.db.analysis_rows_total",
                value=request.analysis_rows_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.db.state_batches_total",
                value=request.state_batches_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.db.state_rows_total",
                value=request.state_rows_total,
                unit="count",
            ),
        ]

    def _analyze_result_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        return [
            MetricPoint(
                name="pipeline.analyze.llm_calls_total",
                value=request.llm_calls_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.llm_errors_total",
                value=request.llm_errors_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.missing_content_total",
                value=request.missing_content_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.processed_total",
                value=request.analyze_result.processed,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.failed_total",
                value=request.analyze_result.failed,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.duration_ms",
                value=request.duration_ms,
                unit="ms",
            ),
        ]

    def _base_analyze_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        return (
            self._analyze_parallelism_metric_points(request=request)
            + self._analyze_result_metric_points(request=request)
            + self._analyze_db_metric_points(request=request)
        )

    def _analyze_token_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        if not request.llm_tokens_seen:
            return []
        return [
            MetricPoint(
                name="pipeline.analyze.llm_prompt_tokens_total",
                value=request.llm_prompt_tokens_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.analyze.llm_completion_tokens_total",
                value=request.llm_completion_tokens_total,
                unit="count",
            ),
        ]

    def _analyze_cost_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        metrics: list[MetricPoint] = []
        if request.llm_cost_seen:
            metrics.append(
                MetricPoint(
                    name="pipeline.analyze.estimated_cost_usd",
                    value=request.llm_cost_usd_total,
                    unit="usd",
                )
            )
        if request.llm_cost_missing_total > 0:
            metrics.append(
                MetricPoint(
                    name="pipeline.analyze.cost_missing_total",
                    value=request.llm_cost_missing_total,
                    unit="count",
                )
            )
        return metrics

    def _analyze_counter_metric_points(
        self,
        *,
        metric_prefix: str,
        values: dict[str, int],
    ) -> list[MetricPoint]:
        return [
            MetricPoint(
                name=f"pipeline.analyze.{metric_prefix}.{token}",
                value=count,
                unit="count",
            )
            for token, count in values.items()
        ]

    def _build_analyze_metric_points(
        self,
        *,
        request: _AnalyzeMetricBuildRequest,
    ) -> list[MetricPoint]:
        metrics = self._base_analyze_metric_points(request=request)
        metrics.extend(self._analyze_token_metric_points(request=request))
        metrics.extend(self._analyze_cost_metric_points(request=request))
        metrics.extend(
            self._analyze_counter_metric_points(
                metric_prefix="llm_calls.provider",
                values=request.llm_calls_by_provider_token,
            )
        )
        metrics.extend(
            self._analyze_counter_metric_points(
                metric_prefix="llm_errors.provider",
                values=request.llm_errors_by_provider_token,
            )
        )
        metrics.extend(
            self._analyze_counter_metric_points(
                metric_prefix="llm_calls.model",
                values=request.llm_calls_by_model_token,
            )
        )
        metrics.extend(
            self._analyze_counter_metric_points(
                metric_prefix="llm_errors.model",
                values=request.llm_errors_by_model_token,
            )
        )
        extra_metrics = getattr(request, "extra_metrics", None)
        if extra_metrics:
            metrics.extend(extra_metrics)
        return metrics

    def analyze(
        self,
        *,
        run_id: str,
        limit: int | None = None,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> AnalyzeResult:
        return execute_analyze(
            self,
            run_id=run_id,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
        )

    def _resolve_analysis_limit(self, *, limit: int | None) -> int:
        resolved = int(self.settings.analyze_limit if limit is None else limit)
        if resolved <= 0:
            raise ValueError("limit must be > 0")
        return resolved

    def _resolve_triage_candidate_limit(self, *, limit: int) -> int:
        triage_enabled = bool(self.settings.triage_enabled) and bool(
            self.settings.topics
        )
        if not triage_enabled:
            return limit
        return min(
            int(self.settings.triage_max_candidates),
            int(limit) * int(self.settings.triage_candidate_factor),
        )

    def _load_stored_content_for_analysis(self, *, item: Any) -> str | None:
        item_id = getattr(item, "id", None)
        if item_id is None:
            return None
        normalized_item_id = int(item_id)
        source = str(getattr(item, "source", "") or "").strip().lower()
        if source == "arxiv":
            return self._load_arxiv_content_for_analysis(item_id=normalized_item_id)
        if source == "openreview":
            existing_pdf = self._get_latest_content_text(
                item_id=normalized_item_id,
                content_type="pdf_text",
            )
            if existing_pdf is not None:
                return existing_pdf
        return self._get_latest_content_text(
            item_id=normalized_item_id,
            content_type="html_maintext",
        )

    def _get_latest_content_text(
        self, *, item_id: int, content_type: str
    ) -> str | None:
        existing_content = self.repository.get_latest_content(
            item_id=item_id, content_type=content_type
        )
        if existing_content is None or not existing_content.text:
            return None
        return existing_content.text

    def _load_arxiv_content_for_analysis(self, *, item_id: int) -> str | None:
        method = self.settings.sources.arxiv.enrich_method
        failure_mode = self.settings.sources.arxiv.enrich_failure_mode
        primary_by_method = {
            "pdf_text": "pdf_text",
            "latex_source": "latex_source",
            "html_document": "html_document_md",
        }
        content_types: list[str] = [primary_by_method.get(method, "pdf_text")]
        if failure_mode == "fallback":
            for candidate_type in (
                "pdf_text",
                "html_maintext",
                "html_document_md",
                "html_document",
                "latex_source",
            ):
                if candidate_type not in content_types:
                    content_types.append(candidate_type)
        for content_type in content_types:
            loaded = self._get_latest_content_text(
                item_id=item_id, content_type=content_type
            )
            if loaded is not None:
                return loaded
        return None

    def _ensure_item_content(
        self,
        *,
        request: ItemContentRequest | None = None,
        **legacy_kwargs: Unpack[_EnsureItemContentKwargs],
    ) -> tuple[str, bool]:
        normalized_request = request or ItemContentRequest(**legacy_kwargs)
        return ensure_item_content(self, normalized_request)

    def _ensure_arxiv_content(
        self,
        *,
        request: ArxivContentRequest | None = None,
        **legacy_kwargs: Unpack[_EnsureArxivContentKwargs],
    ) -> tuple[str, bool]:
        normalized_request = request or ArxivContentRequest(**legacy_kwargs)
        return ensure_arxiv_content(self, normalized_request)

    def _ensure_arxiv_latex_source_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
        diag: dict[str, Any] | None = None,
    ) -> tuple[str, bool]:
        db_read_started = time.perf_counter()
        existing_latex = self._get_latest_content_text(
            item_id=item_id, content_type="latex_source"
        )
        if diag is not None:
            diag["db_read_ms"] = diag.get("db_read_ms", 0) + int(
                (time.perf_counter() - db_read_started) * 1000
            )
        if existing_latex is not None:
            self._annotate_content_diag(
                diag,
                content_type="latex_source",
                content_text=existing_latex,
            )
            return existing_latex, False
        source_url = self._build_arxiv_source_url(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if not source_url:
            raise ValueError("missing arXiv source url")
        fetch_started = time.perf_counter()
        source_bytes = fetch_url_bytes(client, source_url)
        if diag is not None:
            diag["fetch_ms"] = diag.get("fetch_ms", 0) + int(
                (time.perf_counter() - fetch_started) * 1000
            )
            diag["input_bytes"] = diag.get("input_bytes", 0) + len(source_bytes)
        extract_started = time.perf_counter()
        extracted_source = extract_arxiv_latex_source(source_bytes)
        if diag is not None:
            diag["extract_ms"] = diag.get("extract_ms", 0) + int(
                (time.perf_counter() - extract_started) * 1000
            )
        if extracted_source is None:
            raise RuntimeError("empty arXiv latex source extraction")
        db_write_started = time.perf_counter()
        self.repository.upsert_content(
            item_id=item_id,
            content_type="latex_source",
            text=extracted_source,
        )
        if diag is not None:
            diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                (time.perf_counter() - db_write_started) * 1000
            )
        self._annotate_content_diag(
            diag,
            content_type="latex_source",
            content_text=extracted_source,
        )
        return extracted_source, True

    def _ensure_arxiv_html_document_content(
        self,
        *,
        request: ArxivHtmlDocumentRequest | None = None,
        **legacy_kwargs: Unpack[_EnsureArxivHtmlDocumentContentKwargs],
    ) -> tuple[str, bool]:
        normalized_request = request or ArxivHtmlDocumentRequest(**legacy_kwargs)
        return ensure_arxiv_html_document_content(self, normalized_request)

    def _ensure_pdf_content(
        self,
        *,
        request: PdfContentRequest | None = None,
        **legacy_kwargs: Unpack[_EnsurePdfContentKwargs],
    ) -> tuple[str, bool]:
        normalized_request = request or PdfContentRequest(**legacy_kwargs)
        return ensure_pdf_content(self, normalized_request)

    def _ensure_html_maintext_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        diag: dict[str, Any] | None = None,
    ) -> tuple[str, bool]:
        db_read_started = time.perf_counter()
        existing_html = self._get_latest_content_text(
            item_id=item_id, content_type="html_maintext"
        )
        if diag is not None:
            diag["db_read_ms"] = diag.get("db_read_ms", 0) + int(
                (time.perf_counter() - db_read_started) * 1000
            )
        if existing_html is not None:
            self._annotate_content_diag(
                diag,
                content_type="html_maintext",
                content_text=existing_html,
            )
            return existing_html, False
        fetch_started = time.perf_counter()
        html = fetch_url_html(client, canonical_url)
        if diag is not None:
            diag["fetch_ms"] = diag.get("fetch_ms", 0) + int(
                (time.perf_counter() - fetch_started) * 1000
            )
            diag["input_bytes"] = diag.get("input_bytes", 0) + len(html.encode("utf-8"))
        extract_started = time.perf_counter()
        extracted = extract_html_maintext(html)
        if diag is not None:
            diag["extract_ms"] = diag.get("extract_ms", 0) + int(
                (time.perf_counter() - extract_started) * 1000
            )
        if extracted is None:
            raise RuntimeError("empty html maintext extraction")
        db_write_started = time.perf_counter()
        self.repository.upsert_content(
            item_id=item_id,
            content_type="html_maintext",
            text=extracted,
        )
        if diag is not None:
            diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                (time.perf_counter() - db_write_started) * 1000
            )
        self._annotate_content_diag(
            diag,
            content_type="html_maintext",
            content_text=extracted,
        )
        return extracted, True

    def publish(
        self,
        *,
        run_id: str,
        limit: int = 50,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> PublishResult:
        return run_publish_stage(
            self,
            run_id=run_id,
            limit=limit,
            period_start=period_start,
            period_end=period_end,
        )

    def trends(
        self,
        *,
        request: TrendStageRequest | None = None,
        **legacy_kwargs: Unpack[_TrendStageRequestKwargs],
    ) -> TrendResult:
        normalized_request = request or TrendStageRequest(**legacy_kwargs)
        return run_trends_stage(
            self,
            request=normalized_request,
        )

    def ideas(
        self,
        *,
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
    ) -> IdeasResult:
        return run_ideas_stage(
            self,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
        )

    def _pull_source_drafts(
        self,
        *,
        request: SourcePullStageRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]:
        normalized_request = request or SourcePullStageRequest(**legacy_kwargs)
        return run_source_pull_stage(self, normalized_request)

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None:
        return pipeline_artifacts.write_debug_artifact(
            settings=self.settings,
            scrub_secrets_values=self._scrub_secrets,
            run_id=run_id,
            item_id=item_id,
            kind=kind,
            payload=payload,
        )

    def _record_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
        log: Any,
        failure_message: str,
    ) -> Path | None:
        artifact_path = self._write_debug_artifact(
            run_id=run_id,
            item_id=item_id,
            kind=kind,
            payload=payload,
        )
        if artifact_path is None:
            return None
        try:
            self._invoke_repository_method(
                "add_artifact",
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                path=str(artifact_path),
                details=pipeline_artifacts.summarize_artifact_payload(
                    kind=kind,
                    payload=payload,
                ),
            )
        except Exception as artifact_exc:
            log.warning(
                failure_message,
                self._sanitize_error_message(str(artifact_exc)),
            )
        return artifact_path

    def _build_triage_candidates(
        self, *, items: list[Any]
    ) -> tuple[list[TriageCandidate], bool, dict[str, Any] | None]:
        return build_stage_triage_candidates(self, items=items)

    def _sanitize_error_message(self, message: str) -> str:
        return pipeline_artifacts.sanitize_error_message(
            message=message,
            secrets=self._scrub_secrets,
        )

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]:
        return pipeline_artifacts.classify_exception(exc)

    @staticmethod
    def _classify_arxiv_html_document_fallback_reason(exc: BaseException) -> str:
        if isinstance(exc, httpx.HTTPStatusError):
            status = int(getattr(getattr(exc, "response", None), "status_code", 0) or 0)
            if status == 404:
                return "http_404"
            if status == 429:
                return "http_429"
            if 500 <= status <= 599:
                return "http_5xx"
            return "http_other"
        if isinstance(exc, httpx.TimeoutException):
            return "timeout"
        if isinstance(exc, httpx.RequestError):
            return "request_error"
        message = str(exc or "").strip().lower()
        if "missing arxiv html url" in message:
            return "missing_url"
        if "empty arxiv html document extraction" in message:
            return "empty_document"
        return "other"

    @staticmethod
    def _build_pdf_url(
        *, source: str, canonical_url: str, source_item_id: str | None
    ) -> str | None:
        if source == "arxiv":
            return PipelineService._build_arxiv_pdf_url(
                canonical_url=canonical_url,
                source_item_id=source_item_id,
            )

        if source == "openreview":
            normalized_url = canonical_url.strip()
            if not normalized_url:
                return None
            if "openreview.net/pdf" in normalized_url:
                return normalized_url
            note_id = (source_item_id or "").strip()
            if not note_id:
                try:
                    parsed = urlparse(normalized_url)
                    note_id = (parse_qs(parsed.query).get("id") or [""])[0].strip()
                except Exception:
                    note_id = ""
            if not note_id:
                return None
            return f"https://openreview.net/pdf?id={note_id}"

        return None

    @staticmethod
    def _build_arxiv_pdf_url(
        *, canonical_url: str, source_item_id: str | None
    ) -> str | None:
        arxiv_id = PipelineService._extract_arxiv_identifier(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if arxiv_id is None:
            return None
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    @staticmethod
    def _build_arxiv_source_url(
        *, canonical_url: str, source_item_id: str | None
    ) -> str | None:
        arxiv_id = PipelineService._extract_arxiv_identifier(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if arxiv_id is None:
            return None
        return f"https://arxiv.org/e-print/{arxiv_id}"

    @staticmethod
    def _build_arxiv_html_url(
        *, canonical_url: str, source_item_id: str | None
    ) -> str | None:
        arxiv_id = PipelineService._extract_arxiv_identifier(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if arxiv_id is None:
            return None
        return f"https://arxiv.org/html/{arxiv_id}"

    @staticmethod
    def _extract_arxiv_identifier(
        *, canonical_url: str, source_item_id: str | None
    ) -> str | None:
        for raw_value in (source_item_id or "", canonical_url or ""):
            normalized = PipelineService._normalize_arxiv_identifier(raw_value)
            if normalized is not None:
                return normalized
        return None

    @staticmethod
    def _normalize_arxiv_identifier(raw_value: str) -> str | None:
        candidate = str(raw_value or "").strip()
        if not candidate:
            return None
        if "://" in candidate:
            try:
                parsed = urlparse(candidate)
                candidate = parsed.path.strip("/")
            except Exception:
                return None
        for prefix in ("abs/", "pdf/", "html/", "e-print/", "src/", "format/"):
            if candidate.startswith(prefix):
                candidate = candidate[len(prefix) :]
                break
        candidate = (
            candidate.replace("arXiv:", "").replace("arxiv:", "").strip().strip("/")
        )
        if candidate.endswith(".pdf"):
            candidate = candidate[:-4]
        candidate = candidate.strip()
        if not candidate:
            return None
        if any(ch.isspace() for ch in candidate):
            return None
        return candidate


_VULTURE_USED_PIPELINE_SERVICE_APIS = (
    PipelineService._build_triage_candidates,
    PipelineService._metric_token,
    PipelineService.publish,
)
