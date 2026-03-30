from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import hashlib
import inspect
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, cast
from urllib.parse import parse_qs, urlparse

import httpx
from loguru import logger
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
    convert_html_document_to_markdown,
    extract_html_document_cleaned_with_references,
    extract_html_maintext,
    extract_pdf_text,
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
from recoleta.pipeline.publish_stage import run_publish_stage
from recoleta.pipeline.ideas_stage import run_ideas_stage
from recoleta.pipeline.trends_stage import run_trends_stage
from recoleta.ports import RepositoryPort
from recoleta import sources
from recoleta.triage import SemanticTriage, TriageCandidate
from recoleta.types import (
    AnalysisResult,
    AnalysisWrite,
    AnalyzeDebug,
    AnalyzeResult,
    DEFAULT_TOPIC_STREAM,
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
    scope: str
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
        self._telegram_senders: dict[str, Any] = {}
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
        items: list[Any],
        limit: int,
    ) -> tuple[list[Any], dict[str, int], dict[str, int]]:
        normalized_limit = max(0, int(limit))
        if normalized_limit <= 0 or not items:
            return [], {}, {}

        queues: dict[str, deque[Any]] = {}
        source_order: list[str] = []
        for item in items:
            source_name = (
                str(getattr(item, "source", "") or "").strip().lower() or "unknown"
            )
            queue = queues.get(source_name)
            if queue is None:
                queue = deque()
                queues[source_name] = queue
                source_order.append(source_name)
            queue.append(item)

        candidate_counts = {
            source_name: len(queue) for source_name, queue in queues.items()
        }
        selected: list[Any] = []
        while len(selected) < normalized_limit:
            progressed = False
            for source_name in source_order:
                queue = queues[source_name]
                if not queue:
                    continue
                selected.append(queue.popleft())
                progressed = True
                if len(selected) >= normalized_limit:
                    break
            if not progressed:
                break
        deferred_counts = {
            source_name: len(queue) for source_name, queue in queues.items() if queue
        }
        return selected, candidate_counts, deferred_counts

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
            MetricPoint(name=str(metric.name or "").strip(), value=metric.value, unit=metric.unit)
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
                scope=str(analysis.scope or DEFAULT_TOPIC_STREAM).strip()
                or DEFAULT_TOPIC_STREAM,
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
                scope=analysis.scope,
                mirror_item_state=analysis.mirror_item_state,
            )
        return len(normalized)

    def _update_item_states_batch(self, *, updates: list[ItemStateUpdate]) -> int:
        normalized = [
            ItemStateUpdate(
                item_id=int(update.item_id),
                state=str(update.state or "").strip(),
                stream=(
                    str(update.stream).strip()
                    if update.stream is not None and str(update.stream).strip()
                    else None
                ),
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
            if update.stream is not None:
                self.repository.mark_item_stream_state(
                    item_id=update.item_id,
                    stream=update.stream,
                    state=update.state,
                    mirror_item_state=update.mirror_item_state,
                )
            elif update.state == ITEM_STATE_RETRYABLE_FAILED:
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
        log = logger.bind(module="pipeline.ingest", run_id=run_id)
        started = time.perf_counter()
        ingest_result = IngestResult()
        source_failures_total = 0
        source_drafts = drafts
        source_stats = self._empty_source_pull_stats()
        with Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._progress_console,
        ) as progress:
            progress_task_id = progress.add_task("Ingesting items", total=None)

            if source_drafts is None:
                source_drafts, source_failures_total, source_stats = (
                    self._pull_source_drafts(
                        run_id=run_id,
                        log=log,
                        period_start=period_start,
                        period_end=period_end,
                    )
                )
            else:
                for draft in source_drafts or []:
                    source_name = str(draft.source or "").strip().lower()
                    if not source_name:
                        continue
                    bucket = source_stats.setdefault(
                        source_name,
                        {
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
                        },
                    )
                    bucket["drafts_total"] += 1

            source_drafts = source_drafts or []
            progress.update(progress_task_id, total=len(source_drafts), completed=0)
            for draft in source_drafts:
                try:
                    _, created = self.repository.upsert_item(draft)
                    source_name = str(draft.source or "").strip().lower()
                    bucket: dict[str, int] | None = None
                    if source_name:
                        bucket = source_stats.setdefault(
                            source_name,
                            self._empty_source_pull_stats().get(
                                source_name,
                                {
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
                                },
                            ),
                        )
                    if created:
                        ingest_result.inserted += 1
                        if bucket is not None:
                            bucket["inserted_total"] += 1
                    else:
                        ingest_result.updated += 1
                        if bucket is not None:
                            bucket["updated_total"] += 1
                except Exception as exc:
                    ingest_result.failed += 1
                    sanitized_error = self._sanitize_error_message(str(exc))
                    self._record_debug_artifact(
                        run_id=run_id,
                        item_id=None,
                        kind="error_context",
                        payload={
                            "stage": "ingest",
                            "error_type": type(exc).__name__,
                            "error_message": sanitized_error,
                            **self._classify_exception(exc),
                            "draft": {
                                "source": draft.source,
                                "source_item_id": draft.source_item_id,
                                "canonical_url_hash": draft.canonical_url_hash,
                            },
                        },
                        log=log,
                        failure_message="Ingest debug artifact record failed: {}",
                    )
                    log.bind(item_hash=draft.canonical_url_hash).warning(
                        "Ingest failed: {}", sanitized_error
                    )
                finally:
                    progress.advance(progress_task_id, advance=1)

        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.items_total",
            value=ingest_result.inserted + ingest_result.updated + ingest_result.failed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.inserted_total",
            value=ingest_result.inserted,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.updated_total",
            value=ingest_result.updated,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.failed_total",
            value=ingest_result.failed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.source_failures_total",
            value=source_failures_total,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        for source_name in sorted(source_stats):
            bucket = source_stats[source_name]
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.drafts_total",
                value=int(bucket.get("drafts_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.pull_failed_total",
                value=int(bucket.get("pull_failed_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.pull_duration_ms",
                value=int(bucket.get("pull_duration_ms") or 0),
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.filtered_out_total",
                value=int(bucket.get("filtered_out_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.in_window_total",
                value=int(bucket.get("in_window_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=(
                    f"pipeline.ingest.source.{source_name}.missing_published_at_total"
                ),
                value=int(bucket.get("missing_published_at_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.deduped_total",
                value=int(bucket.get("deduped_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.deferred_total",
                value=int(bucket.get("deferred_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.not_modified_total",
                value=int(bucket.get("not_modified_total") or 0),
                unit="count",
            )
            oldest_published_at_unix = int(bucket.get("oldest_published_at_unix") or 0)
            if oldest_published_at_unix > 0:
                self.repository.record_metric(
                    run_id=run_id,
                    name=f"pipeline.ingest.source.{source_name}.oldest_published_at_unix",
                    value=oldest_published_at_unix,
                    unit="unix",
                )
            newest_published_at_unix = int(bucket.get("newest_published_at_unix") or 0)
            if newest_published_at_unix > 0:
                self.repository.record_metric(
                    run_id=run_id,
                    name=f"pipeline.ingest.source.{source_name}.newest_published_at_unix",
                    value=newest_published_at_unix,
                    unit="unix",
                )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.inserted_total",
                value=int(bucket.get("inserted_total") or 0),
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.ingest.source.{source_name}.updated_total",
                value=int(bucket.get("updated_total") or 0),
                unit="count",
            )
        log.info(
            "Ingest completed with inserted={} updated={} failed={} source_failures={}",
            ingest_result.inserted,
            ingest_result.updated,
            ingest_result.failed,
            source_failures_total,
        )
        return ingest_result

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
        log = logger.bind(module="pipeline.enrich", run_id=run_id)
        enrich_started = time.perf_counter()
        include_debug = (
            self.settings.write_debug_artifacts
            and self.settings.artifacts_dir is not None
        )
        with self.repository.sql_diagnostics() as sql_diag:
            candidate_limit = self._stage_candidate_limit(limit=limit)
            items = self._invoke_repository_method(
                "list_items_for_analysis",
                limit=candidate_limit,
                period_start=period_start,
                period_end=period_end,
            )
            items, candidate_counts, deferred_counts = self._rebalance_items_by_source(
                items=list(items),
                limit=limit,
            )
            self._record_stage_source_selection_metrics(
                run_id=run_id,
                stage="enrich",
                candidate_counts=candidate_counts,
                deferred_counts=deferred_counts,
            )
            enrich_processed = 0
            enrich_failed = 0
            enrich_skipped = 0
            enrich_duration_ms_total = 0
            arxiv_items_by_method: dict[str, int] = {
                "pdf_text": 0,
                "latex_source": 0,
                "html_document": 0,
            }
            arxiv_failed_by_method: dict[str, int] = {
                "pdf_text": 0,
                "latex_source": 0,
                "html_document": 0,
            }
            html_document_items_total = 0
            html_document_fetch_ms_sum = 0
            html_document_cleanup_ms_sum = 0
            html_document_pandoc_ms_sum = 0
            html_document_pandoc_failed_total = 0
            html_document_pandoc_warning_items_total = 0
            html_document_pandoc_warning_count_sum = 0
            html_document_pandoc_warning_tex_math_convert_failed_sum = 0
            html_document_pandoc_math_replaced_sum = 0
            html_document_fallback_to_pdf_total = 0
            html_document_fallback_reason_totals: dict[str, int] = {
                bucket: 0 for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS
            }
            html_document_db_read_ms_sum = 0
            html_document_db_write_ms_sum = 0
            source_enrich_stats: dict[str, dict[str, Any]] = {
                source_name: self._new_source_enrich_bucket()
                for source_name in _SOURCE_DIAGNOSTIC_NAMES
            }

            def _source_enrich_bucket(source_name: str) -> dict[str, Any]:
                normalized = str(source_name or "").strip().lower() or "unknown"
                return source_enrich_stats.setdefault(
                    normalized,
                    self._new_source_enrich_bucket(),
                )

            def write_and_record_artifact(
                *, item_id: int | None, kind: str, payload: dict[str, Any]
            ) -> None:
                self._record_debug_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    payload=payload,
                    log=log.bind(item_id=item_id),
                    failure_message=f"Enrich {kind} artifact record failed: {{}}",
                )

            timeout = httpx.Timeout(10.0, connect=5.0)
            headers = {"User-Agent": "recoleta/0.1"}
            html_document_max_concurrency = int(
                self.settings.sources.arxiv.html_document_max_concurrency or 1
            )
            enable_parallel = (
                bool(self.settings.sources.arxiv.enrich_method == "html_document")
                and bool(self.settings.sources.arxiv.html_document_enable_parallel)
                and html_document_max_concurrency > 1
            )
            arxiv_rps = float(
                self.settings.sources.arxiv.html_document_requests_per_second or 0.0
            )

            class _RateLimiter:
                def __init__(self, *, requests_per_second: float) -> None:
                    self._interval_s = 1.0 / max(0.0001, float(requests_per_second))
                    self._lock = threading.Lock()
                    self._next_at = time.monotonic()

                def acquire(self) -> None:
                    with self._lock:
                        now = time.monotonic()
                        scheduled = self._next_at if self._next_at > now else now
                        self._next_at = scheduled + self._interval_s
                        wait_s = scheduled - now
                    if wait_s > 0:
                        time.sleep(wait_s)

            arxiv_html_throttle: Callable[[], None] | None = None
            if arxiv_rps > 0:
                limiter = _RateLimiter(requests_per_second=arxiv_rps)
                arxiv_html_throttle = limiter.acquire

            def _process_one(*, client: httpx.Client, item: Any) -> dict[str, Any]:
                raw_item_id = getattr(item, "id", None)
                source = str(getattr(item, "source", "") or "").strip().lower()
                arxiv_method: str | None = None
                if source == "arxiv":
                    arxiv_method = self.settings.sources.arxiv.enrich_method
                if raw_item_id is None:
                    return {
                        "status": "failed",
                        "item_id": None,
                        "source": source,
                        "arxiv_method": arxiv_method,
                        "error_type": "ValueError",
                        "error_message": "missing item id",
                        "classification": {"retryable": False},
                        "diag": {},
                    }
                item_id = int(raw_item_id)
                diag: dict[str, Any] = {}
                try:
                    _, stored_new_content = self._ensure_item_content(
                        client=client,
                        item=item,
                        log=log,
                        diag=diag,
                        arxiv_html_throttle=arxiv_html_throttle,
                    )
                    db_mark_started = time.perf_counter()
                    self.repository.mark_item_enriched(item_id=item_id)
                    diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                        (time.perf_counter() - db_mark_started) * 1000
                    )
                    return {
                        "status": "ok",
                        "item_id": item_id,
                        "source": source,
                        "arxiv_method": arxiv_method,
                        "stored_new": bool(stored_new_content),
                        "diag": diag,
                    }
                except Exception as enrich_exc:  # noqa: BLE001
                    sanitized_error = self._sanitize_error_message(str(enrich_exc))
                    classification = self._classify_exception(enrich_exc)
                    try:
                        db_mark_started = time.perf_counter()
                        if classification.get("retryable") is True:
                            self.repository.mark_item_retryable_failed(item_id=item_id)
                        else:
                            self.repository.mark_item_failed(item_id=item_id)
                        diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                            (time.perf_counter() - db_mark_started) * 1000
                        )
                    except Exception as mark_exc:  # noqa: BLE001
                        log.bind(item_id=item_id).warning(
                            "Enrich mark_item_state failed: {}",
                            self._sanitize_error_message(str(mark_exc)),
                        )
                    return {
                        "status": "failed",
                        "item_id": item_id,
                        "source": source,
                        "arxiv_method": arxiv_method,
                        "error_type": type(enrich_exc).__name__,
                        "error_message": sanitized_error,
                        "classification": classification,
                        "diag": diag,
                    }

            with Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self._progress_console,
            ) as progress:
                task_id = progress.add_task("Enriching items", total=len(items))

                def _consume_result(
                    result: dict[str, Any], *, item_elapsed_ms: int
                ) -> None:
                    nonlocal \
                        enrich_processed, \
                        enrich_failed, \
                        enrich_skipped, \
                        enrich_duration_ms_total
                    nonlocal html_document_items_total
                    nonlocal \
                        html_document_fetch_ms_sum, \
                        html_document_cleanup_ms_sum, \
                        html_document_pandoc_ms_sum
                    nonlocal \
                        html_document_pandoc_failed_total, \
                        html_document_pandoc_warning_items_total, \
                        html_document_pandoc_warning_count_sum, \
                        html_document_pandoc_warning_tex_math_convert_failed_sum, \
                        html_document_pandoc_math_replaced_sum
                    nonlocal html_document_fallback_to_pdf_total
                    nonlocal html_document_fallback_reason_totals
                    nonlocal html_document_db_read_ms_sum, html_document_db_write_ms_sum

                    status = result.get("status")
                    source = str(result.get("source") or "").strip().lower()
                    source_bucket = _source_enrich_bucket(source)
                    if status == "ok":
                        if result.get("stored_new"):
                            enrich_processed += 1
                            source_bucket["processed_total"] = (
                                int(source_bucket.get("processed_total") or 0) + 1
                            )
                        else:
                            enrich_skipped += 1
                            source_bucket["skipped_total"] = (
                                int(source_bucket.get("skipped_total") or 0) + 1
                            )
                    else:
                        enrich_failed += 1
                        source_bucket["failed_total"] = (
                            int(source_bucket.get("failed_total") or 0) + 1
                        )
                        item_id = result.get("item_id")
                        arxiv_method = result.get("arxiv_method")
                        if isinstance(arxiv_method, str) and arxiv_method:
                            arxiv_failed_by_method[arxiv_method] = (
                                arxiv_failed_by_method.get(arxiv_method, 0) + 1
                            )
                        classification = result.get("classification") or {}
                        if include_debug:
                            write_and_record_artifact(
                                item_id=int(item_id) if item_id is not None else None,
                                kind="error_context",
                                payload={
                                    "stage": "enrich",
                                    "error_type": result.get("error_type")
                                    or "Exception",
                                    "error_message": result.get("error_message")
                                    or "unknown",
                                    "item_id": item_id,
                                    **(
                                        classification
                                        if isinstance(classification, dict)
                                        else {}
                                    ),
                                },
                            )
                        log.bind(item_id=item_id).warning(
                            "Enrich failed: {}",
                            result.get("error_message") or "unknown",
                        )

                    diag = result.get("diag") or {}
                    arxiv_method = result.get("arxiv_method")
                    source_bucket["item_duration_ms_total"] = int(
                        source_bucket.get("item_duration_ms_total") or 0
                    ) + int(item_elapsed_ms)
                    source_bucket["fetch_ms_sum"] = int(
                        source_bucket.get("fetch_ms_sum") or 0
                    ) + int(diag.get("fetch_ms") or 0)
                    source_bucket["extract_ms_sum"] = int(
                        source_bucket.get("extract_ms_sum") or 0
                    ) + int(diag.get("extract_ms") or 0)
                    source_bucket["db_read_ms_sum"] = int(
                        source_bucket.get("db_read_ms_sum") or 0
                    ) + int(diag.get("db_read_ms") or 0)
                    source_bucket["db_write_ms_sum"] = int(
                        source_bucket.get("db_write_ms_sum") or 0
                    ) + int(diag.get("db_write_ms") or 0)
                    source_bucket["input_bytes_sum"] = int(
                        source_bucket.get("input_bytes_sum") or 0
                    ) + int(diag.get("input_bytes") or 0)
                    source_bucket["content_chars_sum"] = int(
                        source_bucket.get("content_chars_sum") or 0
                    ) + int(diag.get("content_chars") or 0)
                    source_bucket["short_content_total"] = int(
                        source_bucket.get("short_content_total") or 0
                    ) + int(diag.get("short_content") or 0)
                    content_type = str(diag.get("content_type") or "").strip().lower()
                    if content_type:
                        content_type_totals = cast(
                            dict[str, int], source_bucket["content_types"]
                        )
                        content_type_totals[content_type] = (
                            content_type_totals.get(content_type, 0) + 1
                        )
                    pdf_backend = str(diag.get("pdf_backend") or "").strip().lower()
                    if pdf_backend:
                        pdf_backend_totals = cast(
                            dict[str, int], source_bucket["pdf_backends"]
                        )
                        pdf_backend_totals[pdf_backend] = (
                            pdf_backend_totals.get(pdf_backend, 0) + 1
                        )
                    if (
                        source == "arxiv"
                        and isinstance(arxiv_method, str)
                        and arxiv_method
                    ):
                        arxiv_items_by_method[arxiv_method] = (
                            arxiv_items_by_method.get(arxiv_method, 0) + 1
                        )
                    if source == "arxiv" and arxiv_method == "html_document":
                        html_document_items_total += 1
                        html_document_fetch_ms_sum += int(diag.get("fetch_ms") or 0)
                        html_document_cleanup_ms_sum += int(diag.get("cleanup_ms") or 0)
                        html_document_pandoc_ms_sum += int(diag.get("pandoc_ms") or 0)
                        html_document_pandoc_failed_total += int(
                            diag.get("pandoc_failed") or 0
                        )
                        warning_count = int(diag.get("pandoc_warning_count") or 0)
                        html_document_pandoc_warning_count_sum += warning_count
                        if warning_count > 0:
                            html_document_pandoc_warning_items_total += 1
                        html_document_pandoc_warning_tex_math_convert_failed_sum += int(
                            diag.get("pandoc_warning_tex_math_convert_failed") or 0
                        )
                        html_document_pandoc_math_replaced_sum += int(
                            diag.get("pandoc_math_replaced_total") or 0
                        )
                        html_document_fallback_to_pdf_total += int(
                            diag.get("html_document_fallback_to_pdf") or 0
                        )
                        for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS:
                            html_document_fallback_reason_totals[bucket] += int(
                                diag.get(f"html_document_fallback_reason.{bucket}") or 0
                            )
                        html_document_db_read_ms_sum += int(diag.get("db_read_ms") or 0)
                        html_document_db_write_ms_sum += int(
                            diag.get("db_write_ms") or 0
                        )

                    enrich_duration_ms_total += int(item_elapsed_ms)
                    progress.advance(task_id, 1)

                if not enable_parallel:
                    with httpx.Client(
                        timeout=timeout, headers=headers, follow_redirects=True
                    ) as client:
                        for item in items:
                            item_started = time.perf_counter()
                            result = _process_one(client=client, item=item)
                            _consume_result(
                                result,
                                item_elapsed_ms=int(
                                    (time.perf_counter() - item_started) * 1000
                                ),
                            )
                else:
                    parallel_items: list[Any] = []
                    serial_items: list[Any] = []
                    for item in items:
                        source = str(getattr(item, "source", "") or "").strip().lower()
                        if (
                            source == "arxiv"
                            and self.settings.sources.arxiv.enrich_method
                            == "html_document"
                        ):
                            parallel_items.append(item)
                        else:
                            serial_items.append(item)

                    with httpx.Client(
                        timeout=timeout, headers=headers, follow_redirects=True
                    ) as serial_client:
                        for item in serial_items:
                            item_started = time.perf_counter()
                            result = _process_one(client=serial_client, item=item)
                            _consume_result(
                                result,
                                item_elapsed_ms=int(
                                    (time.perf_counter() - item_started) * 1000
                                ),
                            )

                    local = threading.local()
                    created_clients: list[httpx.Client] = []
                    created_lock = threading.Lock()

                    def _get_thread_client() -> httpx.Client:
                        existing = getattr(local, "client", None)
                        if isinstance(existing, httpx.Client):
                            return existing
                        client = httpx.Client(
                            timeout=timeout, headers=headers, follow_redirects=True
                        )
                        local.client = client
                        with created_lock:
                            created_clients.append(client)
                        return client

                    def _worker(item: Any) -> dict[str, Any]:
                        started = time.perf_counter()
                        client = _get_thread_client()
                        result = _process_one(client=client, item=item)
                        result["elapsed_ms"] = int(
                            (time.perf_counter() - started) * 1000
                        )
                        return result

                    executor = ThreadPoolExecutor(
                        max_workers=html_document_max_concurrency
                    )
                    futures = {
                        executor.submit(_worker, item): item for item in parallel_items
                    }
                    interrupted = False
                    try:
                        for fut in as_completed(futures):
                            try:
                                result = fut.result()
                            except Exception as exc:  # noqa: BLE001
                                result = {
                                    "status": "failed",
                                    "error_type": type(exc).__name__,
                                    "error_message": self._sanitize_error_message(
                                        str(exc)
                                    ),
                                    "classification": self._classify_exception(exc),
                                    "elapsed_ms": 0,
                                }
                            _consume_result(
                                result,
                                item_elapsed_ms=int(result.get("elapsed_ms") or 0),
                            )
                    except KeyboardInterrupt:
                        interrupted = True
                        log.warning(
                            "Interrupt received; cancelling pending enrich workers and draining in-flight tasks."
                        )
                        for fut in futures:
                            fut.cancel()
                        try:
                            executor.shutdown(wait=False, cancel_futures=True)
                        except TypeError:
                            executor.shutdown(wait=False)

                        # Drain in-flight work without letting Ctrl-C interrupt cleanup again.
                        deadline = time.monotonic() + 10.0
                        while True:
                            remaining = deadline - time.monotonic()
                            if remaining <= 0:
                                break
                            try:
                                _, not_done = wait(
                                    futures, timeout=min(0.25, remaining)
                                )
                            except KeyboardInterrupt:
                                continue
                            if not not_done:
                                break
                        raise
                    finally:
                        try:
                            executor.shutdown(wait=True, cancel_futures=True)
                        except TypeError:
                            executor.shutdown(wait=True)
                        except KeyboardInterrupt:
                            # Best-effort: keep shutdown from spewing a traceback on repeated Ctrl-C.
                            pass

                        all_done = (
                            all(fut.done() for fut in futures) if futures else True
                        )
                        if interrupted and not all_done:
                            log.warning(
                                "Interrupted before workers finished; skipping http client close to avoid mid-request failures."
                            )
                        else:
                            with created_lock:
                                to_close = list(created_clients)
                            for c in to_close:
                                try:
                                    c.close()
                                except Exception:
                                    pass

            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.processed_total",
                value=enrich_processed,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.skipped_total",
                value=enrich_skipped,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.failed_total",
                value=enrich_failed,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.item_duration_ms_total",
                value=enrich_duration_ms_total,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.duration_ms",
                value=int((time.perf_counter() - enrich_started) * 1000),
                unit="ms",
            )
            for method in ("pdf_text", "latex_source", "html_document"):
                self.repository.record_metric(
                    run_id=run_id,
                    name=f"pipeline.enrich.arxiv.method_selected.{method}_total",
                    value=arxiv_items_by_method.get(method, 0),
                    unit="count",
                )
                self.repository.record_metric(
                    run_id=run_id,
                    name=f"pipeline.enrich.arxiv.method_failed.{method}_total",
                    value=arxiv_failed_by_method.get(method, 0),
                    unit="count",
                )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.db.sql_queries_total",
                value=sql_diag.queries_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.db.sql_commits_total",
                value=sql_diag.commits_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.items_total",
                value=html_document_items_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.fetch_ms_sum",
                value=html_document_fetch_ms_sum,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.cleanup_ms_sum",
                value=html_document_cleanup_ms_sum,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_ms_sum",
                value=html_document_pandoc_ms_sum,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_failed_total",
                value=html_document_pandoc_failed_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_warning_items_total",
                value=html_document_pandoc_warning_items_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum",
                value=html_document_pandoc_warning_count_sum,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_warning_tex_math_convert_failed_sum",
                value=html_document_pandoc_warning_tex_math_convert_failed_sum,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum",
                value=html_document_pandoc_math_replaced_sum,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.fallback_to_pdf_total",
                value=html_document_fallback_to_pdf_total,
                unit="count",
            )
            for bucket, count in html_document_fallback_reason_totals.items():
                self.repository.record_metric(
                    run_id=run_id,
                    name=f"pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.{bucket}_total",
                    value=count,
                    unit="count",
                )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.db_read_ms_sum",
                value=html_document_db_read_ms_sum,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.enrich.arxiv.html_document.db_write_ms_sum",
                value=html_document_db_write_ms_sum,
                unit="ms",
            )
            for source_name in sorted(source_enrich_stats):
                source_bucket = source_enrich_stats[source_name]
                for metric_name, unit in (
                    ("processed_total", "count"),
                    ("skipped_total", "count"),
                    ("failed_total", "count"),
                    ("item_duration_ms_total", "ms"),
                    ("fetch_ms_sum", "ms"),
                    ("extract_ms_sum", "ms"),
                    ("db_read_ms_sum", "ms"),
                    ("db_write_ms_sum", "ms"),
                    ("input_bytes_sum", "bytes"),
                    ("content_chars_sum", "chars"),
                    ("short_content_total", "count"),
                ):
                    self.repository.record_metric(
                        run_id=run_id,
                        name=f"pipeline.enrich.source.{source_name}.{metric_name}",
                        value=int(source_bucket.get(metric_name) or 0),
                        unit=unit,
                    )
                for content_type, count in sorted(
                    cast(dict[str, int], source_bucket["content_types"]).items()
                ):
                    self.repository.record_metric(
                        run_id=run_id,
                        name=f"pipeline.enrich.source.{source_name}.content_type.{content_type}_total",
                        value=count,
                        unit="count",
                    )
                for pdf_backend, count in sorted(
                    cast(dict[str, int], source_bucket["pdf_backends"]).items()
                ):
                    self.repository.record_metric(
                        run_id=run_id,
                        name=f"pipeline.enrich.source.{source_name}.pdf_backend.{pdf_backend}_total",
                        value=count,
                        unit="count",
                    )
            log.info(
                "Enrich completed with processed={} skipped={} failed={}",
                enrich_processed,
                enrich_skipped,
                enrich_failed,
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
        triage_enabled = bool(self.settings.triage_enabled) and bool(
            self.settings.topics
        )
        if not triage_enabled:
            return

        normalized_limit = self._resolve_analysis_limit(limit=limit)
        normalized_candidate_limit = (
            candidate_limit
            or self._resolve_triage_candidate_limit(limit=normalized_limit)
        )
        include_debug = (
            self.settings.write_debug_artifacts
            and self.settings.artifacts_dir is not None
        )
        log = logger.bind(module="pipeline.triage", run_id=run_id)
        selection_limit = self._stage_candidate_limit(limit=normalized_candidate_limit)
        items = self._invoke_repository_method(
            "list_items_for_llm_analysis",
            limit=selection_limit,
            triage_required=False,
            period_start=period_start,
            period_end=period_end,
        )
        items, candidate_counts, deferred_counts = self._rebalance_items_by_source(
            items=list(items),
            limit=normalized_candidate_limit,
        )
        self._record_stage_source_selection_metrics(
            run_id=run_id,
            stage="triage",
            candidate_counts=candidate_counts,
            deferred_counts=deferred_counts,
        )
        triage_items = [
            item
            for item in items
            if getattr(item, "state", None) == ITEM_STATE_ENRICHED
        ]

        def write_and_record_artifact(
            *, item_id: int | None, kind: str, payload: dict[str, Any]
        ) -> None:
            self._record_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload=payload,
                log=log.bind(item_id=item_id),
                failure_message=f"Triage {kind} artifact record failed: {{}}",
            )

        triage_candidates, content_fetch_failed, content_fetch_error = (
            self._build_triage_candidates(items=triage_items)
        )
        if not triage_candidates:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.candidates_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.scored_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.selected_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.skipped_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.embedding_calls_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.embedding_errors_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.content_fetch_failed_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.failed_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.duration_ms",
                value=0,
                unit="ms",
            )
            log.info("Triage skipped: no candidates")
            return

        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.triage.content_fetch_failed_total",
            value=1 if content_fetch_failed else 0,
            unit="count",
        )
        if content_fetch_failed and include_debug and content_fetch_error is not None:
            write_and_record_artifact(
                item_id=None,
                kind="error_context",
                payload=content_fetch_error,
            )

        triage_started = time.perf_counter()
        try:
            triage_output = self.semantic_triage.select(
                run_id=run_id,
                candidates=triage_candidates,
                topics=self.settings.topics,
                limit=normalized_limit,
                mode=self.settings.triage_mode,
                query_mode=self.settings.triage_query_mode,
                embedding_model=self.settings.triage_embedding_model,
                embedding_dimensions=self.settings.triage_embedding_dimensions,
                min_similarity=self.settings.triage_min_similarity,
                exploration_rate=self.settings.triage_exploration_rate,
                recency_floor=self.settings.triage_recency_floor,
                include_debug=include_debug,
            )
            stats = triage_output.stats
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.candidates_total",
                value=stats.candidates_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.scored_total",
                value=stats.scored_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.selected_total",
                value=stats.selected_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.skipped_total",
                value=stats.skipped_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.embedding_calls_total",
                value=stats.embedding_calls_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.embedding_errors_total",
                value=stats.embedding_errors_total,
                unit="count",
            )
            if stats.embedding_prompt_tokens_total is not None:
                self.repository.record_metric(
                    run_id=run_id,
                    name="pipeline.triage.embedding_prompt_tokens_total",
                    value=stats.embedding_prompt_tokens_total,
                    unit="count",
                )
            if stats.embedding_cost_usd_total is not None:
                self.repository.record_metric(
                    run_id=run_id,
                    name="pipeline.triage.estimated_cost_usd",
                    value=stats.embedding_cost_usd_total,
                    unit="usd",
                )
            if (
                stats.embedding_cost_missing_total is not None
                and stats.embedding_cost_missing_total > 0
            ):
                self.repository.record_metric(
                    run_id=run_id,
                    name="pipeline.triage.cost_missing_total",
                    value=stats.embedding_cost_missing_total,
                    unit="count",
                )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.failed_total",
                value=0,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.duration_ms",
                value=stats.duration_ms,
                unit="ms",
            )
            for kind, payload in triage_output.artifacts.items():
                write_and_record_artifact(item_id=None, kind=kind, payload=payload)

            selected_total = 0
            for entry in triage_output.selected:
                selected_item_id = getattr(entry.candidate.item, "id", None)
                if selected_item_id is None:
                    continue
                try:
                    self.repository.mark_item_triaged(item_id=int(selected_item_id))
                    selected_total += 1
                except Exception as mark_exc:
                    log.bind(item_id=selected_item_id).warning(
                        "Triage mark_item_triaged failed: {}",
                        self._sanitize_error_message(str(mark_exc)),
                    )
            log.info(
                "Triage selected {} of {} candidates mode={} method={}",
                selected_total,
                stats.candidates_total,
                self.settings.triage_mode,
                stats.method,
            )
        except Exception as triage_exc:
            triage_duration_ms = int((time.perf_counter() - triage_started) * 1000)
            sanitized_error = self._sanitize_error_message(str(triage_exc))
            write_and_record_artifact(
                item_id=None,
                kind="error_context",
                payload={
                    "stage": "triage",
                    "error_type": type(triage_exc).__name__,
                    "error_message": sanitized_error,
                    **self._classify_exception(triage_exc),
                },
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.failed_total",
                value=1,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.duration_ms",
                value=triage_duration_ms,
                unit="ms",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.triage.candidates_total",
                value=len(triage_candidates),
                unit="count",
            )
            fallback_marked_total = 0
            for item in triage_items[:normalized_limit]:
                fallback_item_id = getattr(item, "id", None)
                if fallback_item_id is None:
                    continue
                try:
                    self.repository.mark_item_triaged(item_id=int(fallback_item_id))
                    fallback_marked_total += 1
                except Exception as mark_exc:
                    log.bind(item_id=fallback_item_id).warning(
                        "Triage fallback mark_item_triaged failed: {}",
                        self._sanitize_error_message(str(mark_exc)),
                    )
            log.warning(
                "Triage failed, falling back to recency marked={} error={}",
                fallback_marked_total,
                sanitized_error,
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
            return [], _AnalyzeParallelismStats(requested=0, effective=0, max_inflight=0)

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
                        outcomes.append(_AnalyzeCallFailure(work_item=work_item, error=exc))
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

    def _build_analyze_metric_points(
        self,
        *,
        analyze_result: AnalyzeResult,
        llm_calls_total: int,
        llm_errors_total: int,
        missing_content_total: int,
        llm_prompt_tokens_total: int,
        llm_completion_tokens_total: int,
        llm_tokens_seen: bool,
        llm_cost_usd_total: float,
        llm_cost_seen: bool,
        llm_cost_missing_total: int,
        llm_calls_by_provider_token: dict[str, int],
        llm_errors_by_provider_token: dict[str, int],
        llm_calls_by_model_token: dict[str, int],
        llm_errors_by_model_token: dict[str, int],
        duration_ms: int,
        parallelism: _AnalyzeParallelismStats,
        sql_queries_total: int,
        sql_commits_total: int,
        analysis_batches_total: int,
        analysis_rows_total: int,
        state_batches_total: int,
        state_rows_total: int,
        extra_metrics: list[MetricPoint] | None = None,
    ) -> list[MetricPoint]:
        metrics: list[MetricPoint] = []
        metrics.extend(
            [
                MetricPoint(
                    name="pipeline.analyze.parallelism.requested",
                    value=parallelism.requested,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.parallelism.effective",
                    value=parallelism.effective,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.parallelism.max_inflight",
                    value=parallelism.max_inflight,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.llm_calls_total",
                    value=llm_calls_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.llm_errors_total",
                    value=llm_errors_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.missing_content_total",
                    value=missing_content_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.sql_queries_total",
                    value=sql_queries_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.sql_commits_total",
                    value=sql_commits_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.analysis_batches_total",
                    value=analysis_batches_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.analysis_rows_total",
                    value=analysis_rows_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.state_batches_total",
                    value=state_batches_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.db.state_rows_total",
                    value=state_rows_total,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.processed_total",
                    value=analyze_result.processed,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.failed_total",
                    value=analyze_result.failed,
                    unit="count",
                ),
                MetricPoint(
                    name="pipeline.analyze.duration_ms",
                    value=duration_ms,
                    unit="ms",
                ),
            ]
        )
        if llm_tokens_seen:
            metrics.extend(
                [
                    MetricPoint(
                        name="pipeline.analyze.llm_prompt_tokens_total",
                        value=llm_prompt_tokens_total,
                        unit="count",
                    ),
                    MetricPoint(
                        name="pipeline.analyze.llm_completion_tokens_total",
                        value=llm_completion_tokens_total,
                        unit="count",
                    ),
                ]
            )
        if llm_cost_seen:
            metrics.append(
                MetricPoint(
                    name="pipeline.analyze.estimated_cost_usd",
                    value=llm_cost_usd_total,
                    unit="usd",
                )
            )
        if llm_cost_missing_total > 0:
            metrics.append(
                MetricPoint(
                    name="pipeline.analyze.cost_missing_total",
                    value=llm_cost_missing_total,
                    unit="count",
                )
            )
        for provider_token, count in llm_calls_by_provider_token.items():
            metrics.append(
                MetricPoint(
                    name=f"pipeline.analyze.llm_calls.provider.{provider_token}",
                    value=count,
                    unit="count",
                )
            )
        for provider_token, count in llm_errors_by_provider_token.items():
            metrics.append(
                MetricPoint(
                    name=f"pipeline.analyze.llm_errors.provider.{provider_token}",
                    value=count,
                    unit="count",
                )
            )
        for model_token, count in llm_calls_by_model_token.items():
            metrics.append(
                MetricPoint(
                    name=f"pipeline.analyze.llm_calls.model.{model_token}",
                    value=count,
                    unit="count",
                )
            )
        for model_token, count in llm_errors_by_model_token.items():
            metrics.append(
                MetricPoint(
                    name=f"pipeline.analyze.llm_errors.model.{model_token}",
                    value=count,
                    unit="count",
                )
            )
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
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        started = time.perf_counter()
        triage_required = bool(self.settings.triage_enabled) and bool(
            self.settings.topics
        )
        effective_limit = self._resolve_analysis_limit(limit=limit)
        analyze_result = AnalyzeResult()
        llm_calls_total = 0
        llm_errors_total = 0
        missing_content_total = 0
        llm_prompt_tokens_total = 0
        llm_completion_tokens_total = 0
        llm_tokens_seen = False
        llm_cost_usd_total = 0.0
        llm_cost_seen = False
        llm_cost_missing_total = 0
        llm_calls_by_provider_token: dict[str, int] = {}
        llm_errors_by_provider_token: dict[str, int] = {}
        llm_calls_by_model_token: dict[str, int] = {}
        llm_errors_by_model_token: dict[str, int] = {}

        def metric_token(value: str, *, max_len: int = 48) -> str:
            lowered = value.lower().strip()
            if not lowered:
                return "unknown"
            normalized = "".join(ch if ch.isalnum() else "_" for ch in lowered)
            while "__" in normalized:
                normalized = normalized.replace("__", "_")
            normalized = normalized.strip("_")
            if not normalized:
                return "unknown"
            return normalized[:max_len]

        configured_provider = (
            self.settings.llm_model.split("/", 1)[0]
            if "/" in self.settings.llm_model
            else "unknown"
        )
        configured_provider_token = metric_token(configured_provider, max_len=24)
        configured_model_token = metric_token(self.settings.llm_model)
        include_debug = (
            self.settings.write_debug_artifacts
            and self.settings.artifacts_dir is not None
        )

        def bucket_provider_token(provider: str) -> str:
            token = metric_token(provider, max_len=24)
            if token == configured_provider_token:
                return token
            return "other"

        def bucket_model_token(model: str) -> str:
            token = metric_token(model)
            if token == configured_model_token:
                return token
            return "other"

        def write_and_record_artifact(
            *, item_id: int | None, kind: str, payload: dict[str, Any]
        ) -> None:
            self._record_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload=payload,
                log=log.bind(item_id=item_id),
                failure_message=f"Analyze {kind} artifact record failed: {{}}",
            )
        with self.repository.sql_diagnostics() as sql_diag:
            candidate_limit = self._stage_candidate_limit(limit=effective_limit)
            items = self._invoke_repository_method(
                "list_items_for_llm_analysis",
                limit=candidate_limit,
                triage_required=triage_required,
                period_start=period_start,
                period_end=period_end,
            )
            items, candidate_counts, deferred_counts = self._rebalance_items_by_source(
                items=list(items),
                limit=effective_limit,
            )
            self._record_stage_source_selection_metrics(
                run_id=run_id,
                stage="analyze",
                candidate_counts=candidate_counts,
                deferred_counts=deferred_counts,
            )

            work_items: list[_AnalyzeWorkItem] = []
            state_updates: list[ItemStateUpdate] = []
            analysis_writes: list[AnalysisWrite] = []
            parallelism = _AnalyzeParallelismStats(
                requested=self._requested_analyze_parallelism(),
                effective=0,
                max_inflight=0,
            )

            for item in items:
                raw_item_id = getattr(item, "id", None)
                if raw_item_id is None:
                    analyze_result.failed += 1
                    log.warning("Analyze skipped: item has no id")
                    continue
                item_id = int(raw_item_id)
                content_text = self._load_stored_content_for_analysis(item=item)
                if not content_text:
                    missing_content_total += 1
                    analyze_result.failed += 1
                    state_updates.append(
                        ItemStateUpdate(
                            item_id=item_id,
                            state=ITEM_STATE_RETRYABLE_FAILED,
                        )
                    )
                    if include_debug:
                        write_and_record_artifact(
                            item_id=item_id,
                            kind="error_context",
                            payload={
                                "stage": "analyze",
                                "error_type": "MissingContent",
                                "error_message": "missing stored content before LLM analysis",
                                "item_id": item_id,
                                "error_category": "ordering",
                                "retryable": True,
                            },
                        )
                    log.bind(item_id=item_id).warning(
                        "Analyze failed: missing stored content"
                    )
                    continue
                work_items.append(
                    _AnalyzeWorkItem(
                        item_id=item_id,
                        title=item.title,
                        canonical_url=item.canonical_url,
                        user_topics=list(self.settings.topics),
                        content_text=content_text,
                        scope=DEFAULT_TOPIC_STREAM,
                        mirror_item_state=True,
                    )
                )

            llm_calls_total += len(work_items)
            outcomes, parallelism = self._run_analyze_calls(
                work_items=work_items,
                include_debug=include_debug,
                description="Analyzing items",
            )
            for outcome in outcomes:
                item_id = outcome.work_item.item_id
                try:
                    if isinstance(outcome, _AnalyzeCallFailure):
                        raise outcome.error

                    analysis_result_payload = outcome.result
                    debug = outcome.debug
                    if include_debug and debug is None:
                        raise RuntimeError(
                            "Analyzer did not return debug payload while include_debug is enabled"
                        )

                    provider_token = bucket_provider_token(
                        analysis_result_payload.provider
                    )
                    llm_calls_by_provider_token[provider_token] = (
                        llm_calls_by_provider_token.get(provider_token, 0) + 1
                    )
                    model_token = bucket_model_token(analysis_result_payload.model)
                    llm_calls_by_model_token[model_token] = (
                        llm_calls_by_model_token.get(model_token, 0) + 1
                    )
                    if analysis_result_payload.prompt_tokens is not None:
                        llm_prompt_tokens_total += int(
                            analysis_result_payload.prompt_tokens
                        )
                        llm_tokens_seen = True
                    if analysis_result_payload.completion_tokens is not None:
                        llm_completion_tokens_total += int(
                            analysis_result_payload.completion_tokens
                        )
                        llm_tokens_seen = True
                    if analysis_result_payload.cost_usd is not None:
                        llm_cost_usd_total += float(analysis_result_payload.cost_usd)
                        llm_cost_seen = True
                    else:
                        llm_cost_missing_total += 1

                    if include_debug and debug is not None:
                        write_and_record_artifact(
                            item_id=item_id,
                            kind="llm_request",
                            payload=debug.request,
                        )
                        write_and_record_artifact(
                            item_id=item_id,
                            kind="llm_response",
                            payload=debug.response,
                        )

                    analysis_writes.append(
                        AnalysisWrite(
                            item_id=item_id,
                            result=analysis_result_payload,
                            scope=outcome.work_item.scope,
                            mirror_item_state=outcome.work_item.mirror_item_state,
                        )
                    )
                except Exception as exc:  # noqa: BLE001
                    analyze_result.failed += 1
                    llm_errors_total += 1
                    llm_errors_by_provider_token[configured_provider_token] = (
                        llm_errors_by_provider_token.get(configured_provider_token, 0)
                        + 1
                    )
                    llm_errors_by_model_token[configured_model_token] = (
                        llm_errors_by_model_token.get(configured_model_token, 0) + 1
                    )
                    sanitized_error = self._sanitize_error_message(str(exc))
                    classification = self._classify_exception(exc)
                    state_updates.append(
                        ItemStateUpdate(
                            item_id=item_id,
                            state=(
                                ITEM_STATE_RETRYABLE_FAILED
                                if classification.get("retryable") is True
                                else ITEM_STATE_FAILED
                            ),
                        )
                    )
                    write_and_record_artifact(
                        item_id=item_id,
                        kind="error_context",
                        payload={
                            "stage": "analyze",
                            "error_type": type(exc).__name__,
                            "error_message": sanitized_error,
                            "item_id": item_id,
                            **classification,
                        },
                    )
                    log.bind(item_id=item_id).warning(
                        "Analyze failed: {}", sanitized_error
                    )

            persisted_analyses = self._persist_analysis_writes(
                analyses=analysis_writes,
            )
            analyze_result.processed += len(persisted_analyses.persisted)
            for failed_persist in persisted_analyses.failed:
                item_id = failed_persist.analysis.item_id
                analyze_result.failed += 1
                llm_errors_total += 1
                llm_errors_by_provider_token[configured_provider_token] = (
                    llm_errors_by_provider_token.get(configured_provider_token, 0) + 1
                )
                llm_errors_by_model_token[configured_model_token] = (
                    llm_errors_by_model_token.get(configured_model_token, 0) + 1
                )
                sanitized_error = self._sanitize_error_message(
                    str(failed_persist.error)
                )
                classification = self._classify_exception(failed_persist.error)
                state_updates.append(
                    ItemStateUpdate(
                        item_id=item_id,
                        state=(
                            ITEM_STATE_RETRYABLE_FAILED
                            if classification.get("retryable") is True
                            else ITEM_STATE_FAILED
                        ),
                    )
                )
                write_and_record_artifact(
                    item_id=item_id,
                    kind="error_context",
                    payload={
                        "stage": "analyze",
                        "error_type": type(failed_persist.error).__name__,
                        "error_message": sanitized_error,
                        "item_id": item_id,
                        **classification,
                    },
                )
                log.bind(item_id=item_id).warning(
                    "Analyze persistence failed: {}",
                    sanitized_error,
                )

            state_batches_total, state_rows_total = self._persist_state_updates(
                state_updates=state_updates,
            )

            metric_points = self._build_analyze_metric_points(
                analyze_result=analyze_result,
                llm_calls_total=llm_calls_total,
                llm_errors_total=llm_errors_total,
                missing_content_total=missing_content_total,
                llm_prompt_tokens_total=llm_prompt_tokens_total,
                llm_completion_tokens_total=llm_completion_tokens_total,
                llm_tokens_seen=llm_tokens_seen,
                llm_cost_usd_total=llm_cost_usd_total,
                llm_cost_seen=llm_cost_seen,
                llm_cost_missing_total=llm_cost_missing_total,
                llm_calls_by_provider_token=llm_calls_by_provider_token,
                llm_errors_by_provider_token=llm_errors_by_provider_token,
                llm_calls_by_model_token=llm_calls_by_model_token,
                llm_errors_by_model_token=llm_errors_by_model_token,
                duration_ms=int((time.perf_counter() - started) * 1000),
                parallelism=parallelism,
                sql_queries_total=sql_diag.queries_total,
                sql_commits_total=sql_diag.commits_total,
                analysis_batches_total=persisted_analyses.analysis_batches_total,
                analysis_rows_total=persisted_analyses.analysis_rows_total,
                state_batches_total=state_batches_total,
                state_rows_total=state_rows_total,
            )
            self._record_metrics_batch(run_id=run_id, metrics=metric_points)
        log.info(
            "Analyze completed with processed={} failed={} missing_content={}",
            analyze_result.processed,
            analyze_result.failed,
            missing_content_total,
        )
        return analyze_result

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
        client: httpx.Client,
        item: Any,
        log: Any,
        diag: dict[str, Any] | None = None,
        arxiv_html_throttle: Callable[[], None] | None = None,
    ) -> tuple[str, bool]:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item id is required for enrichment")
        item_id = int(raw_item_id)
        source = str(getattr(item, "source", "") or "").strip().lower()
        canonical_url = str(getattr(item, "canonical_url", "") or "")
        source_item_id = getattr(item, "source_item_id", None)

        if source == "arxiv":
            content_text, stored_new_content = self._ensure_arxiv_content(
                client=client,
                item_id=item_id,
                canonical_url=canonical_url,
                source_item_id=source_item_id,
                log=log,
                diag=diag,
                arxiv_html_throttle=arxiv_html_throttle,
            )
        elif source == "openreview":
            content_text, stored_new_content = self._ensure_pdf_content(
                client=client,
                source=source,
                item_id=item_id,
                canonical_url=canonical_url,
                source_item_id=source_item_id,
                log=log,
                diag=diag,
            )
        else:
            content_text, stored_new_content = self._ensure_html_maintext_content(
                client=client,
                item_id=item_id,
                canonical_url=canonical_url,
                diag=diag,
            )

        if not content_text.strip():
            raise RuntimeError("empty enriched content")
        return content_text, stored_new_content

    def _ensure_arxiv_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
        log: Any,
        diag: dict[str, Any] | None = None,
        arxiv_html_throttle: Callable[[], None] | None = None,
    ) -> tuple[str, bool]:
        method = self.settings.sources.arxiv.enrich_method
        failure_mode = self.settings.sources.arxiv.enrich_failure_mode
        if method == "pdf_text":
            return self._ensure_pdf_content(
                client=client,
                source="arxiv",
                item_id=item_id,
                canonical_url=canonical_url,
                source_item_id=source_item_id,
                log=log,
                diag=diag,
            )

        if method == "latex_source":
            try:
                return self._ensure_arxiv_latex_source_content(
                    client=client,
                    item_id=item_id,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
                    diag=diag,
                )
            except Exception as method_exc:
                if failure_mode == "strict":
                    raise
                log.bind(item_id=item_id).warning(
                    "arXiv enrich_method={} failed, falling back to pdf path: {}",
                    method,
                    self._sanitize_error_message(str(method_exc)),
                )
                return self._ensure_pdf_content(
                    client=client,
                    source="arxiv",
                    item_id=item_id,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
                    log=log,
                    diag=diag,
                )

        if method == "html_document":
            try:
                return self._ensure_arxiv_html_document_content(
                    client=client,
                    item_id=item_id,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
                    log=log,
                    diag=diag,
                    arxiv_html_throttle=arxiv_html_throttle,
                )
            except Exception as method_exc:
                if failure_mode == "strict":
                    raise
                reason_bucket = self._classify_arxiv_html_document_fallback_reason(
                    method_exc
                )
                if diag is not None:
                    diag["html_document_fallback_to_pdf"] = 1
                    diag[f"html_document_fallback_reason.{reason_bucket}"] = 1
                log.bind(
                    item_id=item_id,
                    html_document_fallback_reason=reason_bucket,
                ).warning(
                    "arXiv enrich_method={} failed, falling back to pdf path: {}",
                    method,
                    self._sanitize_error_message(str(method_exc)),
                )
                return self._ensure_pdf_content(
                    client=client,
                    source="arxiv",
                    item_id=item_id,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
                    log=log,
                    diag=diag,
                )

        raise ValueError(f"Unsupported arXiv enrich_method: {method}")

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
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
        log: Any,
        diag: dict[str, Any] | None = None,
        arxiv_html_throttle: Callable[[], None] | None = None,
    ) -> tuple[str, bool]:
        parallel_mode = (
            bool(self.settings.sources.arxiv.enrich_method == "html_document")
            and bool(self.settings.sources.arxiv.html_document_enable_parallel)
            and int(self.settings.sources.arxiv.html_document_max_concurrency or 1) > 1
        )
        sample_rate = float(
            self.settings.sources.arxiv.html_document_log_sample_rate or 0.0
        )
        bound_log = log.bind(item_id=item_id)

        def _should_log_info() -> bool:
            if not parallel_mode:
                return True
            if sample_rate >= 1.0:
                return True
            if sample_rate <= 0.0:
                return False
            digest = hashlib.sha256(str(item_id).encode("utf-8")).digest()
            bucket = int.from_bytes(digest[:4], "big") / (2**32)
            return bucket < sample_rate

        def _log_info_or_debug(message: str, *args: Any) -> None:
            if _should_log_info():
                bound_log.info(message, *args)
            else:
                bound_log.debug(message, *args)

        def _fetch_arxiv_html_polite(url: str) -> str:
            if callable(arxiv_html_throttle):
                arxiv_html_throttle()
            return fetch_url_html(client, url)

        db_read_started = time.perf_counter()
        existing = self.repository.get_latest_content_texts(
            item_id=item_id,
            content_types=["html_document", "html_document_md", "html_references"],
        )
        existing_document = existing.get("html_document")
        existing_md = existing.get("html_document_md")
        existing_refs = existing.get("html_references")
        if diag is not None:
            diag["db_read_ms"] = diag.get("db_read_ms", 0) + int(
                (time.perf_counter() - db_read_started) * 1000
            )
        if (
            bool(self.settings.sources.arxiv.html_document_skip_cleanup_when_complete)
            and existing_document is not None
            and existing_md is not None
            and existing_refs is not None
        ):
            self._annotate_content_diag(
                diag,
                content_type="html_document",
                content_text=existing_document,
            )
            return existing_document, False
        stored_new = False
        if existing_document is not None:
            cleanup_started = time.perf_counter()
            cleaned_document, references_html, stats = (
                extract_html_document_cleaned_with_references(existing_document)
            )
            cleanup_elapsed_ms = int((time.perf_counter() - cleanup_started) * 1000)
            if diag is not None:
                diag["cleanup_ms"] = diag.get("cleanup_ms", 0) + cleanup_elapsed_ms
                diag["extract_ms"] = diag.get("extract_ms", 0) + cleanup_elapsed_ms
            pending_upserts: dict[str, str] = {}
            if cleaned_document is not None and cleaned_document != existing_document:
                pending_upserts["html_document"] = cleaned_document
                existing_document = cleaned_document
            if existing_refs is None and references_html is not None:
                pending_upserts["html_references"] = references_html
            if existing_md is None and existing_document is not None:
                markdown, elapsed_ms, error = convert_html_document_to_markdown(
                    existing_document,
                    diag=diag,
                )
                if diag is not None:
                    diag["pandoc_ms"] = diag.get("pandoc_ms", 0) + int(elapsed_ms or 0)
                    diag["extract_ms"] = diag.get("extract_ms", 0) + int(
                        elapsed_ms or 0
                    )
                if markdown is not None:
                    pending_upserts["html_document_md"] = markdown
                    _log_info_or_debug(
                        "html_document_md created from existing html_document elapsed_ms={} chars_in={} chars_out={}",
                        elapsed_ms,
                        len(existing_document),
                        len(markdown),
                    )
                else:
                    self._log_html_document_md_conversion_skipped(
                        log=log,
                        item_id=item_id,
                        elapsed_ms=elapsed_ms,
                        error=error,
                    )
            _log_info_or_debug(
                "html_document cleanup stats removed_non_body={} removed_references_blocks={} references_chars={}",
                stats.get("removed_non_body_blocks"),
                stats.get("removed_references_blocks"),
                stats.get("references_chars"),
            )
            if pending_upserts:
                db_write_started = time.perf_counter()
                if bool(
                    self.settings.sources.arxiv.html_document_use_batched_db_writes
                ):
                    inserted = self.repository.upsert_contents_texts(
                        item_id=item_id, texts_by_type=pending_upserts
                    )
                else:
                    inserted = 0
                    for ctype, text in pending_upserts.items():
                        _, did_insert = self.repository.upsert_content_with_inserted(
                            item_id=item_id,
                            content_type=ctype,
                            text=text,
                        )
                        inserted += 1 if did_insert else 0
                if diag is not None:
                    diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                        (time.perf_counter() - db_write_started) * 1000
                    )
                stored_new = stored_new or (inserted > 0)
            self._annotate_content_diag(
                diag,
                content_type="html_document",
                content_text=existing_document,
            )
            return existing_document, stored_new
        html_url = self._build_arxiv_html_url(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if not html_url:
            raise ValueError("missing arXiv html url")
        fetch_started = time.perf_counter()
        html = _fetch_arxiv_html_polite(html_url)
        if diag is not None:
            diag["fetch_ms"] = diag.get("fetch_ms", 0) + int(
                (time.perf_counter() - fetch_started) * 1000
            )
            diag["input_bytes"] = diag.get("input_bytes", 0) + len(html.encode("utf-8"))
        cleanup_started = time.perf_counter()
        cleaned_document, references_html, stats = (
            extract_html_document_cleaned_with_references(html)
        )
        cleanup_elapsed_ms = int((time.perf_counter() - cleanup_started) * 1000)
        if diag is not None:
            diag["cleanup_ms"] = diag.get("cleanup_ms", 0) + cleanup_elapsed_ms
            diag["extract_ms"] = diag.get("extract_ms", 0) + cleanup_elapsed_ms
        if cleaned_document is None:
            raise RuntimeError("empty arXiv html document extraction")
        pending_upserts_new: dict[str, str] = {"html_document": cleaned_document}
        if references_html is not None:
            pending_upserts_new["html_references"] = references_html
        markdown, elapsed_ms, error = convert_html_document_to_markdown(
            cleaned_document,
            diag=diag,
        )
        if diag is not None:
            diag["pandoc_ms"] = diag.get("pandoc_ms", 0) + int(elapsed_ms or 0)
            diag["extract_ms"] = diag.get("extract_ms", 0) + int(elapsed_ms or 0)
        if markdown is not None:
            pending_upserts_new["html_document_md"] = markdown
            _log_info_or_debug(
                "html_document_md created elapsed_ms={} chars_in={} chars_out={}",
                elapsed_ms,
                len(cleaned_document),
                len(markdown),
            )
        else:
            self._log_html_document_md_conversion_skipped(
                log=log,
                item_id=item_id,
                elapsed_ms=elapsed_ms,
                error=error,
            )
        _log_info_or_debug(
            "html_document cleanup stats removed_non_body={} removed_references_blocks={} references_chars={}",
            stats.get("removed_non_body_blocks"),
            stats.get("removed_references_blocks"),
            stats.get("references_chars"),
        )
        extracted_maintext = extract_html_maintext(html)
        if extracted_maintext is not None:
            pending_upserts_new["html_maintext"] = extracted_maintext
        if pending_upserts_new:
            db_write_started = time.perf_counter()
            if bool(self.settings.sources.arxiv.html_document_use_batched_db_writes):
                inserted = self.repository.upsert_contents_texts(
                    item_id=item_id, texts_by_type=pending_upserts_new
                )
            else:
                inserted = 0
                for ctype, text in pending_upserts_new.items():
                    _, did_insert = self.repository.upsert_content_with_inserted(
                        item_id=item_id,
                        content_type=ctype,
                        text=text,
                    )
                    inserted += 1 if did_insert else 0
            if diag is not None:
                diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                    (time.perf_counter() - db_write_started) * 1000
                )
            stored_new = stored_new or (inserted > 0)
        self._annotate_content_diag(
            diag,
            content_type="html_document",
            content_text=cleaned_document,
        )
        return cleaned_document, bool(stored_new)

    def _ensure_pdf_content(
        self,
        *,
        client: httpx.Client,
        source: str,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
        log: Any,
        diag: dict[str, Any] | None = None,
    ) -> tuple[str, bool]:
        db_read_started = time.perf_counter()
        existing_pdf = self._get_latest_content_text(
            item_id=item_id, content_type="pdf_text"
        )
        if diag is not None:
            diag["db_read_ms"] = diag.get("db_read_ms", 0) + int(
                (time.perf_counter() - db_read_started) * 1000
            )
        if existing_pdf is not None:
            self._annotate_content_diag(
                diag,
                content_type="pdf_text",
                content_text=existing_pdf,
            )
            return existing_pdf, False
        pdf_url = self._build_pdf_url(
            source=source,
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if not pdf_url:
            raise ValueError("missing pdf url")

        fetch_started = time.perf_counter()
        pdf_bytes = fetch_url_bytes(client, pdf_url)
        if diag is not None:
            diag["fetch_ms"] = diag.get("fetch_ms", 0) + int(
                (time.perf_counter() - fetch_started) * 1000
            )
            diag["input_bytes"] = diag.get("input_bytes", 0) + len(pdf_bytes)
        extract_started = time.perf_counter()
        pdf_diag: dict[str, Any] = {}
        extracted_pdf = extract_pdf_text(pdf_bytes, diag=pdf_diag)
        if diag is not None:
            diag["extract_ms"] = diag.get("extract_ms", 0) + int(
                (time.perf_counter() - extract_started) * 1000
            )
            pdf_backend = str(pdf_diag.get("pdf_backend") or "").strip().lower()
            if pdf_backend:
                diag["pdf_backend"] = pdf_backend
        if extracted_pdf is None:
            raise RuntimeError("empty pdf text extraction")

        db_write_started = time.perf_counter()
        self.repository.upsert_content(
            item_id=item_id,
            content_type="pdf_text",
            text=extracted_pdf,
        )
        if diag is not None:
            diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                (time.perf_counter() - db_write_started) * 1000
            )
        self._annotate_content_diag(
            diag,
            content_type="pdf_text",
            content_text=extracted_pdf,
            pdf_backend=str(pdf_diag.get("pdf_backend") or "").strip().lower() or None,
        )
        return extracted_pdf, True

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
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
        backfill: bool = False,
        backfill_mode: str = "missing",
        debug_pdf: bool = False,
        reuse_existing_corpus: bool = False,
    ) -> TrendResult:
        return run_trends_stage(
            self,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
            reuse_existing_corpus=reuse_existing_corpus,
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
        run_id: str,
        log: Any,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]:
        hn_urls = (
            list(dict.fromkeys(self.settings.sources.hn.rss_urls))
            if bool(self.settings.sources.hn.enabled)
            else []
        )
        rss_urls = (
            list(dict.fromkeys(self.settings.sources.rss.feeds))
            if bool(self.settings.sources.rss.enabled)
            else []
        )
        arxiv_queries = (
            list(dict.fromkeys(self.settings.sources.arxiv.queries))
            if bool(self.settings.sources.arxiv.enabled)
            else []
        )
        openreview_venues = (
            list(dict.fromkeys(self.settings.sources.openreview.venues))
            if bool(self.settings.sources.openreview.enabled)
            else []
        )
        drafts: list[ItemDraft] = []
        source_failures_total = 0
        source_stats = self._empty_source_pull_stats()

        def pull(source_name: str, fn: Any, **call_kwargs: Any) -> None:
            nonlocal source_failures_total
            started = time.perf_counter()
            bucket = source_stats.setdefault(
                source_name,
                {
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
                },
            )
            try:
                raw_result = self._invoke_source_pull(
                    fn,
                    **call_kwargs,
                    period_start=period_start,
                    period_end=period_end,
                    pull_state_lookup=lambda scope_kind, scope_key: (
                        self._lookup_source_pull_state(
                            source=source_name,
                            scope_kind=scope_kind,
                            scope_key=scope_key,
                        )
                    ),
                    include_stats=True,
                )
                pull_result = self._normalize_source_pull_result(raw_result)
                drafts.extend(pull_result.drafts)
                bucket["drafts_total"] += len(pull_result.drafts)
                bucket["filtered_out_total"] += int(pull_result.filtered_out_total or 0)
                bucket["in_window_total"] += int(pull_result.in_window_total or 0)
                bucket["missing_published_at_total"] += int(
                    pull_result.missing_published_at_total or 0
                )
                bucket["deduped_total"] += int(pull_result.deduped_total or 0)
                bucket["deferred_total"] += int(pull_result.deferred_total or 0)
                bucket["not_modified_total"] += int(pull_result.not_modified_total or 0)
                if pull_result.oldest_published_at is not None:
                    candidate_oldest = int(pull_result.oldest_published_at.timestamp())
                    current_oldest = int(bucket.get("oldest_published_at_unix") or 0)
                    if current_oldest <= 0 or candidate_oldest < current_oldest:
                        bucket["oldest_published_at_unix"] = candidate_oldest
                if pull_result.newest_published_at is not None:
                    candidate_newest = int(pull_result.newest_published_at.timestamp())
                    current_newest = int(bucket.get("newest_published_at_unix") or 0)
                    if candidate_newest > current_newest:
                        bucket["newest_published_at_unix"] = candidate_newest
                self._persist_source_pull_state_updates(
                    source=source_name,
                    updates=list(pull_result.state_updates),
                )
            except Exception as exc:
                source_failures_total += 1
                bucket["pull_failed_total"] += 1
                sanitized_error = self._sanitize_error_message(str(exc))
                self._record_debug_artifact(
                    run_id=run_id,
                    item_id=None,
                    kind="error_context",
                    payload={
                        "stage": "ingest",
                        "source": source_name,
                        "error_type": type(exc).__name__,
                        "error_message": sanitized_error,
                        **self._classify_exception(exc),
                    },
                    log=log.bind(source=source_name),
                    failure_message="Ingest source debug artifact record failed: {}",
                )
                log.bind(source=source_name).warning(
                    "Source pull failed: {}", sanitized_error
                )
            finally:
                bucket["pull_duration_ms"] += int(
                    (time.perf_counter() - started) * 1000
                )

        if self.settings.sources.hf_daily.enabled:
            pull(
                "hf_daily",
                sources.fetch_hf_daily_papers_drafts,
                max_items=self.settings.sources.hf_daily.max_items_per_run,
            )
        if hn_urls:
            pull(
                "hn",
                sources.fetch_hn_drafts,
                feed_urls=hn_urls,
                max_items_per_feed=self.settings.sources.hn.max_items_per_feed,
                max_total_items=self.settings.sources.hn.max_total_per_run,
            )
        if rss_urls:
            pull(
                "rss",
                sources.fetch_rss_drafts,
                feed_urls=rss_urls,
                source="rss",
                max_items_per_feed=self.settings.sources.rss.max_items_per_feed,
                max_total_items=self.settings.sources.rss.max_total_per_run,
            )
        if arxiv_queries:
            pull(
                "arxiv",
                sources.fetch_arxiv_drafts,
                queries=arxiv_queries,
                max_results_per_run=self.settings.sources.arxiv.max_results_per_run,
                max_total_items=self.settings.sources.arxiv.max_total_per_run,
            )
        if openreview_venues:
            pull(
                "openreview",
                sources.fetch_openreview_drafts,
                venues=openreview_venues,
                max_results_per_venue=self.settings.sources.openreview.max_results_per_venue,
                max_total_items=self.settings.sources.openreview.max_total_per_run,
            )
        return drafts, source_failures_total, source_stats

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
        candidates_items: list[Any] = []
        item_ids: list[int] = []
        pdf_item_ids: list[int] = []
        arxiv_item_ids: list[int] = []
        for item in items:
            raw_item_id = getattr(item, "id", None)
            if raw_item_id is None:
                continue
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0:
                continue
            candidates_items.append(item)
            item_ids.append(item_id)
            source = str(getattr(item, "source", "") or "").strip().lower()
            if source in {"arxiv", "openreview"}:
                pdf_item_ids.append(item_id)
            if source == "arxiv":
                arxiv_item_ids.append(item_id)

        if not candidates_items:
            return [], False, None

        max_chars = int(
            getattr(self.settings, "triage_item_text_max_chars", 1200) or 1200
        )
        html_by_id: dict[int, Any] = {}
        pdf_by_id: dict[int, Any] = {}
        html_document_by_id: dict[int, Any] = {}
        html_document_md_by_id: dict[int, Any] = {}
        latex_by_id: dict[int, Any] = {}
        content_fetch_failed = False
        content_fetch_error: dict[str, Any] | None = None
        try:
            html_by_id = self.repository.get_latest_contents(
                item_ids=item_ids, content_type="html_maintext"
            )
            if pdf_item_ids:
                pdf_by_id = self.repository.get_latest_contents(
                    item_ids=pdf_item_ids, content_type="pdf_text"
                )
            if arxiv_item_ids:
                html_document_md_by_id = self.repository.get_latest_contents(
                    item_ids=arxiv_item_ids,
                    content_type="html_document_md",
                )
                html_document_by_id = self.repository.get_latest_contents(
                    item_ids=arxiv_item_ids,
                    content_type="html_document",
                )
                latex_by_id = self.repository.get_latest_contents(
                    item_ids=arxiv_item_ids,
                    content_type="latex_source",
                )
        except Exception as exc:  # noqa: BLE001
            content_fetch_failed = True
            sanitized_error = self._sanitize_error_message(str(exc))
            content_fetch_error = {
                "stage": "triage_content_fetch",
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                **self._classify_exception(exc),
                "content_types": [
                    "html_maintext",
                    "pdf_text",
                    "html_document_md",
                    "html_document",
                    "latex_source",
                ],
                "item_ids_total": len(item_ids),
                "pdf_item_ids_total": len(pdf_item_ids),
                "arxiv_item_ids_total": len(arxiv_item_ids),
            }
            html_by_id = {}
            pdf_by_id = {}
            html_document_by_id = {}
            html_document_md_by_id = {}
            latex_by_id = {}

        candidates: list[TriageCandidate] = []
        for item in candidates_items:
            title = str(getattr(item, "title", "") or "").strip()
            item_id = int(getattr(item, "id"))
            excerpt: str | None = None

            source = str(getattr(item, "source", "") or "").strip().lower()
            if source in {"arxiv", "openreview"}:
                existing_pdf = pdf_by_id.get(item_id)
                if existing_pdf is not None and getattr(existing_pdf, "text", None):
                    excerpt = str(getattr(existing_pdf, "text") or "")

            if excerpt is None:
                existing_html = html_by_id.get(item_id)
                if existing_html is not None and getattr(existing_html, "text", None):
                    excerpt = str(getattr(existing_html, "text") or "")
            if excerpt is None and source == "arxiv":
                existing_html_document_md = html_document_md_by_id.get(item_id)
                if existing_html_document_md is not None and getattr(
                    existing_html_document_md, "text", None
                ):
                    excerpt = str(getattr(existing_html_document_md, "text") or "")
            if excerpt is None and source == "arxiv":
                existing_html_document = html_document_by_id.get(item_id)
                if existing_html_document is not None and getattr(
                    existing_html_document, "text", None
                ):
                    excerpt = str(getattr(existing_html_document, "text") or "")
            if excerpt is None and source == "arxiv":
                existing_latex = latex_by_id.get(item_id)
                if existing_latex is not None and getattr(existing_latex, "text", None):
                    excerpt = str(getattr(existing_latex, "text") or "")

            combined = title
            if excerpt:
                trimmed_excerpt = excerpt.strip()
                if trimmed_excerpt:
                    combined = (
                        f"{title}\n\n{trimmed_excerpt}" if title else trimmed_excerpt
                    )

            if max_chars > 0 and len(combined) > max_chars:
                combined = combined[:max_chars]

            candidates.append(TriageCandidate(item=item, text=combined))
        return candidates, content_fetch_failed, content_fetch_error

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
