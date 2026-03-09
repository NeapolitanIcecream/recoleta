from __future__ import annotations

import hashlib
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from datetime import date, datetime
from pathlib import Path
from typing import Any, Callable, cast
from urllib.parse import parse_qs, urlparse

import httpx
import orjson
from loguru import logger
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings, TopicStreamRuntime
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
    DELIVERY_CHANNEL_TELEGRAM,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.observability import (
    collect_environment_secrets,
    get_rich_console,
    mask_value,
    scrub_secrets,
)
from recoleta.pipeline_publish_stage import (
    run_publish_stage,
    run_publish_topic_streams_stage,
)
from recoleta.pipeline_trends_stage import (
    run_trends_stage,
    run_trends_topic_streams_stage,
)
from recoleta.ports import RepositoryPort
from recoleta import sources
from recoleta.triage import SemanticTriage, TriageCandidate
from recoleta.types import (
    AnalyzeResult,
    DEFAULT_TOPIC_STREAM,
    IngestResult,
    ItemDraft,
    PublishResult,
    TrendResult,
    utc_now,
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
        runtime_builder = getattr(settings, "topic_stream_runtimes", None)
        self._topic_streams: list[TopicStreamRuntime]
        if callable(runtime_builder):
            self._topic_streams = cast(list[TopicStreamRuntime], runtime_builder())
        else:
            self._topic_streams = [
                TopicStreamRuntime(
                    name=DEFAULT_TOPIC_STREAM,
                    topics=list(getattr(settings, "topics", []) or []),
                    allow_tags=list(getattr(settings, "allow_tags", []) or []),
                    deny_tags=list(getattr(settings, "deny_tags", []) or []),
                    publish_targets=list(
                        getattr(settings, "publish_targets", []) or []
                    ),
                    markdown_output_dir=Path(
                        getattr(settings, "markdown_output_dir", ".")
                    ).expanduser(),
                    obsidian_base_folder=str(
                        getattr(settings, "obsidian_base_folder", "Recoleta")
                    ),
                    min_relevance_score=float(
                        getattr(settings, "min_relevance_score", 0.0) or 0.0
                    ),
                    max_deliveries_per_day=int(
                        getattr(settings, "max_deliveries_per_day", 0) or 0
                    ),
                    telegram_bot_token=getattr(settings, "telegram_bot_token", None),
                    telegram_chat_id=getattr(settings, "telegram_chat_id", None),
                    explicit=False,
                )
            ]
        self._explicit_topic_streams = any(
            bool(getattr(stream, "explicit", False)) for stream in self._topic_streams
        )
        self._mirror_item_states = not self._explicit_topic_streams
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
        if (
            self.telegram_sender is None
            and not self._explicit_topic_streams
            and "telegram" in settings.publish_targets
        ):
            if (
                settings.telegram_bot_token is not None
                and settings.telegram_chat_id is not None
            ):
                self.telegram_sender = TelegramSender(
                    token=settings.telegram_bot_token.get_secret_value(),
                    chat_id=settings.telegram_chat_id.get_secret_value(),
                )

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
        if self.settings.telegram_chat_id is not None:
            return mask_value(self.settings.telegram_chat_id.get_secret_value())
        return "__telegram_sender__"

    def _metric_token(self, value: str, *, max_len: int = 48) -> str:
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

    def _stream_metric_name(self, *, stage: str, stream: str, suffix: str) -> str:
        stream_token = self._metric_token(stream, max_len=32)
        return f"pipeline.{stage}.stream.{stream_token}.{suffix}"

    def _telegram_destination_for_stream(self, stream: TopicStreamRuntime) -> str:
        if stream.telegram_chat_id is not None:
            return mask_value(stream.telegram_chat_id.get_secret_value())
        return "__telegram_sender__"

    def _telegram_sender_for_stream(self, stream: TopicStreamRuntime) -> Any:
        if isinstance(self.telegram_sender, dict):
            sender = self.telegram_sender.get(stream.name)
            if sender is not None:
                return sender
            sender = self.telegram_sender.get(DEFAULT_TOPIC_STREAM)
            if sender is not None:
                return sender
        elif self.telegram_sender is not None:
            return self.telegram_sender

        if stream.name in self._telegram_senders:
            return self._telegram_senders[stream.name]
        if stream.telegram_bot_token is None or stream.telegram_chat_id is None:
            raise ValueError(
                f"Telegram credentials are required for topic stream '{stream.name}'"
            )
        sender = TelegramSender(
            token=stream.telegram_bot_token.get_secret_value(),
            chat_id=stream.telegram_chat_id.get_secret_value(),
        )
        self._telegram_senders[stream.name] = sender
        return sender

    def _telegram_delivery_budget_for_stream(
        self, stream: TopicStreamRuntime
    ) -> tuple[str, int, int]:
        destination = self._telegram_destination_for_stream(stream)
        now = utc_now()
        midnight_utc = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            tzinfo=now.tzinfo,
        )
        sent_today = self.repository.count_sent_deliveries_since(
            channel=DELIVERY_CHANNEL_TELEGRAM,
            destination=destination,
            since=midnight_utc,
        )
        remaining_today = max(0, stream.max_deliveries_per_day - sent_today)
        return destination, sent_today, remaining_today

    def _record_stream_metric(
        self, *, run_id: str, stage: str, stream: str, suffix: str, value: float, unit: str
    ) -> None:
        self.repository.record_metric(
            run_id=run_id,
            name=self._stream_metric_name(stage=stage, stream=stream, suffix=suffix),
            value=value,
            unit=unit,
        )

    def _settings_for_topic_stream(self, stream: TopicStreamRuntime) -> Settings:
        return self.settings.model_copy(
            update={
                "topics": list(stream.topics),
                "topic_streams": [],
                "allow_tags": list(stream.allow_tags),
                "deny_tags": list(stream.deny_tags),
                "publish_targets": list(stream.publish_targets),
                "markdown_output_dir": stream.markdown_output_dir,
                "obsidian_base_folder": stream.obsidian_base_folder,
                "min_relevance_score": float(stream.min_relevance_score),
                "max_deliveries_per_day": int(stream.max_deliveries_per_day),
                "telegram_bot_token": stream.telegram_bot_token,
                "telegram_chat_id": stream.telegram_chat_id,
            }
        )

    def _telegram_delivery_budget(self) -> tuple[str, int, int]:
        destination = self._telegram_delivery_destination()
        now = utc_now()
        midnight_utc = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            tzinfo=now.tzinfo,
        )
        sent_today = self.repository.count_sent_deliveries_since(
            channel=DELIVERY_CHANNEL_TELEGRAM,
            destination=destination,
            since=midnight_utc,
        )
        remaining_today = max(0, self.settings.max_deliveries_per_day - sent_today)
        return destination, sent_today, remaining_today

    def ingest(
        self, *, run_id: str, drafts: list[ItemDraft] | None = None
    ) -> IngestResult:
        log = logger.bind(module="pipeline.ingest", run_id=run_id)
        started = time.perf_counter()
        ingest_result = IngestResult()
        source_failures_total = 0
        source_drafts = drafts
        with Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._progress_console,
        ) as progress:
            progress_task_id = progress.add_task("Ingesting items", total=None)

            if source_drafts is None:
                source_drafts, source_failures_total = self._pull_source_drafts(
                    run_id=run_id, log=log
                )

            source_drafts = source_drafts or []
            progress.update(progress_task_id, total=len(source_drafts), completed=0)
            for draft in source_drafts:
                try:
                    _, created = self.repository.upsert_item(draft)
                    if created:
                        ingest_result.inserted += 1
                    else:
                        ingest_result.updated += 1
                except Exception as exc:
                    ingest_result.failed += 1
                    sanitized_error = self._sanitize_error_message(str(exc))
                    artifact_path = self._write_debug_artifact(
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
                    )
                    if artifact_path is not None:
                        try:
                            self.repository.add_artifact(
                                run_id=run_id,
                                item_id=None,
                                kind="error_context",
                                path=str(artifact_path),
                            )
                        except Exception as artifact_exc:
                            log.warning(
                                "Ingest debug artifact record failed: {}",
                                self._sanitize_error_message(str(artifact_exc)),
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
    ) -> IngestResult:
        effective_limit = self._resolve_analysis_limit(limit=limit)
        candidate_limit = self._resolve_triage_candidate_limit(limit=effective_limit)
        ingest_result = self.ingest(run_id=run_id, drafts=drafts)
        self.enrich(run_id=run_id, limit=candidate_limit)
        if not self._explicit_topic_streams:
            self.triage(
                run_id=run_id, limit=effective_limit, candidate_limit=candidate_limit
            )
        return ingest_result

    def enrich(self, *, run_id: str, limit: int) -> None:
        log = logger.bind(module="pipeline.enrich", run_id=run_id)
        enrich_started = time.perf_counter()
        include_debug = (
            self.settings.write_debug_artifacts
            and self.settings.artifacts_dir is not None
        )
        with self.repository.sql_diagnostics() as sql_diag:
            items = self.repository.list_items_for_analysis(limit=limit)
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

            def write_and_record_artifact(
                *, item_id: int | None, kind: str, payload: dict[str, Any]
            ) -> None:
                artifact_path = self._write_debug_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    payload=payload,
                )
                if artifact_path is None:
                    return
                try:
                    self.repository.add_artifact(
                        run_id=run_id,
                        item_id=item_id,
                        kind=kind,
                        path=str(artifact_path),
                    )
                except Exception as artifact_exc:
                    log.bind(item_id=item_id).warning(
                        "Enrich {} artifact record failed: {}",
                        kind,
                        self._sanitize_error_message(str(artifact_exc)),
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
                diag: dict[str, int] = {}
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
                    if status == "ok":
                        if result.get("stored_new"):
                            enrich_processed += 1
                        else:
                            enrich_skipped += 1
                    else:
                        enrich_failed += 1
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
                    source = str(result.get("source") or "").strip().lower()
                    arxiv_method = result.get("arxiv_method")
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
                                diag.get(
                                    f"html_document_fallback_reason.{bucket}"
                                )
                                or 0
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
            log.info(
                "Enrich completed with processed={} skipped={} failed={}",
                enrich_processed,
                enrich_skipped,
                enrich_failed,
            )

    def triage(
        self, *, run_id: str, limit: int, candidate_limit: int | None = None
    ) -> None:
        if self._explicit_topic_streams:
            logger.bind(module="pipeline.triage", run_id=run_id).info(
                "Triage deferred to topic-stream analyze stage streams={}",
                len(self._topic_streams),
            )
            return
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
        items = self.repository.list_items_for_llm_analysis(
            limit=normalized_candidate_limit,
            triage_required=False,
        )
        triage_items = [
            item
            for item in items
            if getattr(item, "state", None) == ITEM_STATE_ENRICHED
        ]

        def write_and_record_artifact(
            *, item_id: int | None, kind: str, payload: dict[str, Any]
        ) -> None:
            artifact_path = self._write_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload=payload,
            )
            if artifact_path is None:
                return
            try:
                self.repository.add_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    path=str(artifact_path),
                )
            except Exception as artifact_exc:
                log.bind(item_id=item_id).warning(
                    "Triage {} artifact record failed: {}",
                    kind,
                    self._sanitize_error_message(str(artifact_exc)),
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

    def analyze(self, *, run_id: str, limit: int | None = None) -> AnalyzeResult:
        if self._explicit_topic_streams:
            return self._analyze_topic_streams(run_id=run_id, limit=limit)
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        started = time.perf_counter()
        triage_required = bool(self.settings.triage_enabled) and bool(
            self.settings.topics
        )
        effective_limit = self._resolve_analysis_limit(limit=limit)
        items = self.repository.list_items_for_llm_analysis(
            limit=effective_limit, triage_required=triage_required
        )
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
            artifact_path = self._write_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload=payload,
            )
            if artifact_path is None:
                return
            try:
                self.repository.add_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    path=str(artifact_path),
                )
            except Exception as artifact_exc:
                log.bind(item_id=item_id).warning(
                    "Analyze {} artifact record failed: {}",
                    kind,
                    self._sanitize_error_message(str(artifact_exc)),
                )

        with Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._progress_console,
        ) as progress:
            for item in progress.track(items, description="Analyzing items"):
                raw_item_id = getattr(item, "id", None)
                if raw_item_id is None:
                    analyze_result.failed += 1
                    log.warning("Analyze skipped: item has no id")
                    continue
                item_id = int(raw_item_id)
                try:
                    content_text = self._load_stored_content_for_analysis(item=item)
                    if not content_text:
                        missing_content_total += 1
                        analyze_result.failed += 1
                        try:
                            self.repository.mark_item_retryable_failed(item_id=item_id)
                        except Exception as mark_exc:
                            log.bind(item_id=item_id).warning(
                                "Analyze missing content mark_item_state failed: {}",
                                self._sanitize_error_message(str(mark_exc)),
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

                    llm_calls_total += 1
                    analysis_result, debug = self.analyzer.analyze(
                        title=item.title,
                        canonical_url=item.canonical_url,
                        user_topics=self.settings.topics,
                        content=content_text,
                        include_debug=include_debug,
                    )
                    provider_token = bucket_provider_token(analysis_result.provider)
                    llm_calls_by_provider_token[provider_token] = (
                        llm_calls_by_provider_token.get(provider_token, 0) + 1
                    )
                    model_token = bucket_model_token(analysis_result.model)
                    llm_calls_by_model_token[model_token] = (
                        llm_calls_by_model_token.get(model_token, 0) + 1
                    )
                    if analysis_result.prompt_tokens is not None:
                        llm_prompt_tokens_total += int(analysis_result.prompt_tokens)
                        llm_tokens_seen = True
                    if analysis_result.completion_tokens is not None:
                        llm_completion_tokens_total += int(
                            analysis_result.completion_tokens
                        )
                        llm_tokens_seen = True
                    if analysis_result.cost_usd is not None:
                        llm_cost_usd_total += float(analysis_result.cost_usd)
                        llm_cost_seen = True
                    else:
                        llm_cost_missing_total += 1

                    if include_debug:
                        if debug is None:
                            raise RuntimeError(
                                "Analyzer did not return debug payload while include_debug is enabled"
                            )
                        write_and_record_artifact(
                            item_id=item_id, kind="llm_request", payload=debug.request
                        )
                        write_and_record_artifact(
                            item_id=item_id, kind="llm_response", payload=debug.response
                        )

                    self.repository.save_analysis(
                        item_id=item_id, result=analysis_result
                    )
                    analyze_result.processed += 1
                except Exception as exc:
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
                    try:
                        if classification.get("retryable") is True:
                            self.repository.mark_item_retryable_failed(item_id=item_id)
                        else:
                            self.repository.mark_item_failed(item_id=item_id)
                    except Exception as mark_exc:
                        log.bind(item_id=item_id).warning(
                            "Analyze mark_item_state failed: {}",
                            self._sanitize_error_message(str(mark_exc)),
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

        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.llm_calls_total",
            value=llm_calls_total,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.llm_errors_total",
            value=llm_errors_total,
            unit="count",
        )
        if llm_tokens_seen:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.llm_prompt_tokens_total",
                value=llm_prompt_tokens_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.llm_completion_tokens_total",
                value=llm_completion_tokens_total,
                unit="count",
            )
        if llm_cost_seen:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.estimated_cost_usd",
                value=llm_cost_usd_total,
                unit="usd",
            )
        if llm_cost_missing_total > 0:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.cost_missing_total",
                value=llm_cost_missing_total,
                unit="count",
            )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.missing_content_total",
            value=missing_content_total,
            unit="count",
        )
        for provider_token, count in llm_calls_by_provider_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_calls.provider.{provider_token}",
                value=count,
                unit="count",
            )
        for provider_token, count in llm_errors_by_provider_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_errors.provider.{provider_token}",
                value=count,
                unit="count",
            )
        for model_token, count in llm_calls_by_model_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_calls.model.{model_token}",
                value=count,
                unit="count",
            )
        for model_token, count in llm_errors_by_model_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_errors.model.{model_token}",
                value=count,
                unit="count",
            )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.processed_total",
            value=analyze_result.processed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.failed_total",
            value=analyze_result.failed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.info(
            "Analyze completed with processed={} failed={} missing_content={}",
            analyze_result.processed,
            analyze_result.failed,
            missing_content_total,
        )
        return analyze_result

    def _select_items_for_topic_stream_analysis(
        self,
        *,
        run_id: str,
        stream: TopicStreamRuntime,
        limit: int,
        include_debug: bool,
    ) -> list[Any]:
        triage_enabled = bool(self.settings.triage_enabled) and bool(stream.topics)
        if not triage_enabled:
            return self.repository.list_items_for_stream_analysis(
                stream=stream.name,
                limit=limit,
                selected_only=False,
            )

        log = logger.bind(module="pipeline.triage", run_id=run_id, stream=stream.name)
        candidate_limit = self._resolve_triage_candidate_limit(limit=limit)
        items = self.repository.list_items_for_stream_analysis(
            stream=stream.name,
            limit=candidate_limit,
            selected_only=False,
        )
        triage_items = [
            item
            for item in items
            if getattr(item, "state", None) == ITEM_STATE_ENRICHED
        ]
        triage_candidates, content_fetch_failed, content_fetch_error = (
            self._build_triage_candidates(items=triage_items)
        )

        def write_and_record_artifact(
            *, item_id: int | None, kind: str, payload: dict[str, Any]
        ) -> None:
            artifact_path = self._write_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload={"stream": stream.name, **payload},
            )
            if artifact_path is None:
                return
            try:
                self.repository.add_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    path=str(artifact_path),
                )
            except Exception as artifact_exc:
                log.bind(item_id=item_id).warning(
                    "Topic stream triage {} artifact record failed: {}",
                    kind,
                    self._sanitize_error_message(str(artifact_exc)),
                )

        if content_fetch_failed and include_debug and content_fetch_error is not None:
            write_and_record_artifact(
                item_id=None,
                kind="error_context",
                payload=content_fetch_error,
            )

        triage_started = time.perf_counter()
        if not triage_candidates:
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="candidates_total",
                value=0,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="selected_total",
                value=0,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="failed_total",
                value=0,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="duration_ms",
                value=0,
                unit="ms",
            )
            return []

        try:
            triage_output = self.semantic_triage.select(
                run_id=run_id,
                candidates=triage_candidates,
                topics=stream.topics,
                limit=limit,
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
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="candidates_total",
                value=stats.candidates_total,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="selected_total",
                value=stats.selected_total,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="failed_total",
                value=0,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="duration_ms",
                value=stats.duration_ms,
                unit="ms",
            )
            for kind, payload in triage_output.artifacts.items():
                write_and_record_artifact(item_id=None, kind=kind, payload=payload)

            selected_items: list[Any] = []
            for entry in triage_output.selected:
                selected_item_id = getattr(entry.candidate.item, "id", None)
                if selected_item_id is None:
                    continue
                try:
                    self.repository.mark_item_stream_state(
                        item_id=int(selected_item_id),
                        stream=stream.name,
                        state=ITEM_STATE_TRIAGED,
                        mirror_item_state=False,
                    )
                except Exception as mark_exc:
                    log.bind(item_id=selected_item_id).warning(
                        "Topic stream triage mark_item_stream_state failed: {}",
                        self._sanitize_error_message(str(mark_exc)),
                    )
                selected_items.append(entry.candidate.item)
            return selected_items
        except Exception as triage_exc:
            triage_duration_ms = int((time.perf_counter() - triage_started) * 1000)
            sanitized_error = self._sanitize_error_message(str(triage_exc))
            if include_debug:
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
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="candidates_total",
                value=len(triage_candidates),
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="selected_total",
                value=min(limit, len(items)),
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="failed_total",
                value=1,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="triage",
                stream=stream.name,
                suffix="duration_ms",
                value=triage_duration_ms,
                unit="ms",
            )
            fallback_items = items[:limit]
            for item in fallback_items:
                fallback_item_id = getattr(item, "id", None)
                if fallback_item_id is None:
                    continue
                try:
                    self.repository.mark_item_stream_state(
                        item_id=int(fallback_item_id),
                        stream=stream.name,
                        state=ITEM_STATE_TRIAGED,
                        mirror_item_state=False,
                    )
                except Exception as mark_exc:
                    log.bind(item_id=fallback_item_id).warning(
                        "Topic stream triage fallback mark_item_stream_state failed: {}",
                        self._sanitize_error_message(str(mark_exc)),
                    )
            log.warning(
                "Topic stream triage failed, falling back to recency selected={} error={}",
                len(fallback_items),
                sanitized_error,
            )
            return fallback_items

    def _analyze_topic_streams(
        self, *, run_id: str, limit: int | None = None
    ) -> AnalyzeResult:
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        started = time.perf_counter()
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
        include_debug = (
            self.settings.write_debug_artifacts
            and self.settings.artifacts_dir is not None
        )
        configured_provider = (
            self.settings.llm_model.split("/", 1)[0]
            if "/" in self.settings.llm_model
            else "unknown"
        )
        configured_provider_token = self._metric_token(
            configured_provider,
            max_len=24,
        )
        configured_model_token = self._metric_token(self.settings.llm_model)

        def bucket_provider_token(provider: str) -> str:
            token = self._metric_token(provider, max_len=24)
            if token == configured_provider_token:
                return token
            return "other"

        def bucket_model_token(model: str) -> str:
            token = self._metric_token(model)
            if token == configured_model_token:
                return token
            return "other"

        def write_and_record_artifact(
            *,
            stream_name: str,
            item_id: int | None,
            kind: str,
            payload: dict[str, Any],
        ) -> None:
            artifact_path = self._write_debug_artifact(
                run_id=run_id,
                item_id=item_id,
                kind=kind,
                payload={"stream": stream_name, **payload},
            )
            if artifact_path is None:
                return
            try:
                self.repository.add_artifact(
                    run_id=run_id,
                    item_id=item_id,
                    kind=kind,
                    path=str(artifact_path),
                )
            except Exception as artifact_exc:
                log.bind(item_id=item_id, stream=stream_name).warning(
                    "Topic stream analyze {} artifact record failed: {}",
                    kind,
                    self._sanitize_error_message(str(artifact_exc)),
                )

        for stream in self._topic_streams:
            stream_log = log.bind(stream=stream.name)
            items = self._select_items_for_topic_stream_analysis(
                run_id=run_id,
                stream=stream,
                limit=effective_limit,
                include_debug=include_debug,
            )
            stream_processed = 0
            stream_failed = 0

            with Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self._progress_console,
            ) as progress:
                for item in progress.track(
                    items,
                    description=f"Analyzing topic stream {stream.name}",
                ):
                    raw_item_id = getattr(item, "id", None)
                    if raw_item_id is None:
                        stream_failed += 1
                        analyze_result.failed += 1
                        stream_log.warning("Analyze skipped: item has no id")
                        continue
                    item_id = int(raw_item_id)
                    try:
                        content_text = self._load_stored_content_for_analysis(item=item)
                        if not content_text:
                            missing_content_total += 1
                            stream_failed += 1
                            analyze_result.failed += 1
                            try:
                                self.repository.mark_item_stream_state(
                                    item_id=item_id,
                                    stream=stream.name,
                                    state=ITEM_STATE_RETRYABLE_FAILED,
                                    mirror_item_state=False,
                                )
                            except Exception as mark_exc:
                                stream_log.bind(item_id=item_id).warning(
                                    "Topic stream analyze missing content mark_item_stream_state failed: {}",
                                    self._sanitize_error_message(str(mark_exc)),
                                )
                            if include_debug:
                                write_and_record_artifact(
                                    stream_name=stream.name,
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
                            stream_log.bind(item_id=item_id).warning(
                                "Analyze failed: missing stored content"
                            )
                            continue

                        llm_calls_total += 1
                        analysis_result, debug = self.analyzer.analyze(
                            title=item.title,
                            canonical_url=item.canonical_url,
                            user_topics=stream.topics,
                            content=content_text,
                            include_debug=include_debug,
                        )
                        provider_token = bucket_provider_token(analysis_result.provider)
                        llm_calls_by_provider_token[provider_token] = (
                            llm_calls_by_provider_token.get(provider_token, 0) + 1
                        )
                        model_token = bucket_model_token(analysis_result.model)
                        llm_calls_by_model_token[model_token] = (
                            llm_calls_by_model_token.get(model_token, 0) + 1
                        )
                        if analysis_result.prompt_tokens is not None:
                            llm_prompt_tokens_total += int(analysis_result.prompt_tokens)
                            llm_tokens_seen = True
                        if analysis_result.completion_tokens is not None:
                            llm_completion_tokens_total += int(
                                analysis_result.completion_tokens
                            )
                            llm_tokens_seen = True
                        if analysis_result.cost_usd is not None:
                            llm_cost_usd_total += float(analysis_result.cost_usd)
                            llm_cost_seen = True
                        else:
                            llm_cost_missing_total += 1

                        if include_debug:
                            if debug is None:
                                raise RuntimeError(
                                    "Analyzer did not return debug payload while include_debug is enabled"
                                )
                            write_and_record_artifact(
                                stream_name=stream.name,
                                item_id=item_id,
                                kind="llm_request",
                                payload=debug.request,
                            )
                            write_and_record_artifact(
                                stream_name=stream.name,
                                item_id=item_id,
                                kind="llm_response",
                                payload=debug.response,
                            )

                        self.repository.save_analysis(
                            item_id=item_id,
                            result=analysis_result,
                            scope=stream.name,
                            mirror_item_state=False,
                        )
                        stream_processed += 1
                        analyze_result.processed += 1
                    except Exception as exc:
                        stream_failed += 1
                        analyze_result.failed += 1
                        llm_errors_total += 1
                        llm_errors_by_provider_token[configured_provider_token] = (
                            llm_errors_by_provider_token.get(
                                configured_provider_token,
                                0,
                            )
                            + 1
                        )
                        llm_errors_by_model_token[configured_model_token] = (
                            llm_errors_by_model_token.get(
                                configured_model_token,
                                0,
                            )
                            + 1
                        )
                        sanitized_error = self._sanitize_error_message(str(exc))
                        classification = self._classify_exception(exc)
                        state = (
                            ITEM_STATE_RETRYABLE_FAILED
                            if classification.get("retryable") is True
                            else ITEM_STATE_FAILED
                        )
                        try:
                            self.repository.mark_item_stream_state(
                                item_id=item_id,
                                stream=stream.name,
                                state=state,
                                mirror_item_state=False,
                            )
                        except Exception as mark_exc:
                            stream_log.bind(item_id=item_id).warning(
                                "Topic stream analyze mark_item_stream_state failed: {}",
                                self._sanitize_error_message(str(mark_exc)),
                            )
                        write_and_record_artifact(
                            stream_name=stream.name,
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
                        stream_log.bind(item_id=item_id).warning(
                            "Analyze failed: {}",
                            sanitized_error,
                        )

            self._record_stream_metric(
                run_id=run_id,
                stage="analyze",
                stream=stream.name,
                suffix="processed_total",
                value=stream_processed,
                unit="count",
            )
            self._record_stream_metric(
                run_id=run_id,
                stage="analyze",
                stream=stream.name,
                suffix="failed_total",
                value=stream_failed,
                unit="count",
            )

        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.streams_total",
            value=len(self._topic_streams),
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.llm_calls_total",
            value=llm_calls_total,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.llm_errors_total",
            value=llm_errors_total,
            unit="count",
        )
        if llm_tokens_seen:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.llm_prompt_tokens_total",
                value=llm_prompt_tokens_total,
                unit="count",
            )
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.llm_completion_tokens_total",
                value=llm_completion_tokens_total,
                unit="count",
            )
        if llm_cost_seen:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.estimated_cost_usd",
                value=llm_cost_usd_total,
                unit="usd",
            )
        if llm_cost_missing_total > 0:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.analyze.cost_missing_total",
                value=llm_cost_missing_total,
                unit="count",
            )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.missing_content_total",
            value=missing_content_total,
            unit="count",
        )
        for provider_token, count in llm_calls_by_provider_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_calls.provider.{provider_token}",
                value=count,
                unit="count",
            )
        for provider_token, count in llm_errors_by_provider_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_errors.provider.{provider_token}",
                value=count,
                unit="count",
            )
        for model_token, count in llm_calls_by_model_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_calls.model.{model_token}",
                value=count,
                unit="count",
            )
        for model_token, count in llm_errors_by_model_token.items():
            self.repository.record_metric(
                run_id=run_id,
                name=f"pipeline.analyze.llm_errors.model.{model_token}",
                value=count,
                unit="count",
            )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.processed_total",
            value=analyze_result.processed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.failed_total",
            value=analyze_result.failed,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.analyze.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.info(
            "Topic stream analyze completed with processed={} failed={} streams={}",
            analyze_result.processed,
            analyze_result.failed,
            len(self._topic_streams),
        )
        return analyze_result

    def _resolve_analysis_limit(self, *, limit: int | None) -> int:
        resolved = int(self.settings.analyze_limit if limit is None else limit)
        if resolved <= 0:
            raise ValueError("limit must be > 0")
        return resolved

    def _resolve_triage_candidate_limit(self, *, limit: int) -> int:
        triage_enabled = bool(self.settings.triage_enabled) and (
            bool(self.settings.topics) or self._explicit_topic_streams
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
        diag: dict[str, int] | None = None,
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
            )
        else:
            content_text, stored_new_content = self._ensure_html_maintext_content(
                client=client,
                item_id=item_id,
                canonical_url=canonical_url,
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
        diag: dict[str, int] | None = None,
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
            )

        if method == "latex_source":
            try:
                return self._ensure_arxiv_latex_source_content(
                    client=client,
                    item_id=item_id,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
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
                )

        raise ValueError(f"Unsupported arXiv enrich_method: {method}")

    def _ensure_arxiv_latex_source_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
    ) -> tuple[str, bool]:
        existing_latex = self._get_latest_content_text(
            item_id=item_id, content_type="latex_source"
        )
        if existing_latex is not None:
            return existing_latex, False
        source_url = self._build_arxiv_source_url(
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if not source_url:
            raise ValueError("missing arXiv source url")
        source_bytes = fetch_url_bytes(client, source_url)
        extracted_source = extract_arxiv_latex_source(source_bytes)
        if extracted_source is None:
            raise RuntimeError("empty arXiv latex source extraction")
        self.repository.upsert_content(
            item_id=item_id,
            content_type="latex_source",
            text=extracted_source,
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
        diag: dict[str, int] | None = None,
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
            return existing_document, False
        stored_new = False
        if existing_document is not None:
            cleanup_started = time.perf_counter()
            cleaned_document, references_html, stats = (
                extract_html_document_cleaned_with_references(existing_document)
            )
            if diag is not None:
                diag["cleanup_ms"] = diag.get("cleanup_ms", 0) + int(
                    (time.perf_counter() - cleanup_started) * 1000
                )
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
        cleanup_started = time.perf_counter()
        cleaned_document, references_html, stats = (
            extract_html_document_cleaned_with_references(html)
        )
        if diag is not None:
            diag["cleanup_ms"] = diag.get("cleanup_ms", 0) + int(
                (time.perf_counter() - cleanup_started) * 1000
            )
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
    ) -> tuple[str, bool]:
        existing_pdf = self._get_latest_content_text(
            item_id=item_id, content_type="pdf_text"
        )
        if existing_pdf is not None:
            return existing_pdf, False
        pdf_url = self._build_pdf_url(
            source=source,
            canonical_url=canonical_url,
            source_item_id=source_item_id,
        )
        if not pdf_url:
            raise ValueError("missing pdf url")

        pdf_bytes = fetch_url_bytes(client, pdf_url)
        extracted_pdf = extract_pdf_text(pdf_bytes)
        if extracted_pdf is None:
            raise RuntimeError("empty pdf text extraction")

        self.repository.upsert_content(
            item_id=item_id,
            content_type="pdf_text",
            text=extracted_pdf,
        )
        return extracted_pdf, True

    def _ensure_html_maintext_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
    ) -> tuple[str, bool]:
        existing_html = self._get_latest_content_text(
            item_id=item_id, content_type="html_maintext"
        )
        if existing_html is not None:
            return existing_html, False
        html = fetch_url_html(client, canonical_url)
        extracted = extract_html_maintext(html)
        if extracted is None:
            raise RuntimeError("empty html maintext extraction")
        self.repository.upsert_content(
            item_id=item_id,
            content_type="html_maintext",
            text=extracted,
        )
        return extracted, True

    def publish(self, *, run_id: str, limit: int = 50) -> PublishResult:
        return run_publish_stage(self, run_id=run_id, limit=limit)

    def _publish_topic_streams(self, *, run_id: str, limit: int = 50) -> PublishResult:
        return run_publish_topic_streams_stage(self, run_id=run_id, limit=limit)

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
        )

    def _trends_topic_streams(
        self,
        *,
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
        backfill: bool = False,
        backfill_mode: str = "missing",
        debug_pdf: bool = False,
    ) -> TrendResult:
        return run_trends_topic_streams_stage(
            self,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            backfill=backfill,
            backfill_mode=backfill_mode,
            debug_pdf=debug_pdf,
        )

    def _pull_source_drafts(
        self, *, run_id: str, log: Any
    ) -> tuple[list[ItemDraft], int]:
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

        def pull(source_name: str, fn: Any) -> None:
            nonlocal source_failures_total
            try:
                drafts.extend(fn())
            except Exception as exc:
                source_failures_total += 1
                sanitized_error = self._sanitize_error_message(str(exc))
                artifact_path = self._write_debug_artifact(
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
                )
                if artifact_path is not None:
                    try:
                        self.repository.add_artifact(
                            run_id=run_id,
                            item_id=None,
                            kind="error_context",
                            path=str(artifact_path),
                        )
                    except Exception as artifact_exc:
                        log.bind(source=source_name).warning(
                            "Ingest source debug artifact record failed: {}",
                            self._sanitize_error_message(str(artifact_exc)),
                        )
                log.bind(source=source_name).warning(
                    "Source pull failed: {}", sanitized_error
                )

        if self.settings.sources.hf_daily.enabled:
            pull("hf_daily", lambda: sources.fetch_hf_daily_papers_drafts(max_items=50))
        if hn_urls:
            pull("hn", lambda: sources.fetch_rss_drafts(feed_urls=hn_urls, source="hn"))
        if rss_urls:
            pull(
                "rss",
                lambda: sources.fetch_rss_drafts(feed_urls=rss_urls, source="rss"),
            )
        if arxiv_queries:
            pull(
                "arxiv",
                lambda: sources.fetch_arxiv_drafts(
                    queries=arxiv_queries,
                    max_results_per_run=self.settings.sources.arxiv.max_results_per_run,
                ),
            )
        if openreview_venues:
            pull(
                "openreview",
                lambda: sources.fetch_openreview_drafts(
                    venues=openreview_venues, max_results_per_venue=50
                ),
            )
        return drafts, source_failures_total

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None:
        if (
            not self.settings.write_debug_artifacts
            or self.settings.artifacts_dir is None
        ):
            return None
        try:

            def sanitize_segment(
                value: str, *, max_len: int = 72, fallback: str = "unknown"
            ) -> str:
                cleaned = value.strip()
                normalized = "".join(
                    ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned
                )
                while "__" in normalized:
                    normalized = normalized.replace("__", "_")
                normalized = normalized.strip("_")
                if not normalized:
                    return fallback
                return normalized[:max_len]

            safe_run_id = sanitize_segment(run_id, fallback="run")
            safe_kind = sanitize_segment(kind, fallback="artifact")
            item_segment = str(item_id) if item_id is not None else "no-item"
            kind_to_name = {
                "error_context": "error-context.json",
                "llm_request": "llm-request.json",
                "llm_response": "llm-response.json",
                "embedding_request": "embedding-request.json",
                "embedding_response": "embedding-response.json",
                "triage_summary": "triage-summary.json",
            }
            file_name = kind_to_name.get(kind, f"{safe_kind.replace('_', '-')}.json")
            relative_path = Path(safe_run_id) / item_segment / file_name

            base_dir = self.settings.artifacts_dir.expanduser().resolve()
            absolute_path = (base_dir / relative_path).resolve()
            if not absolute_path.is_relative_to(base_dir):
                raise ValueError("Debug artifact path escapes artifacts_dir")
            absolute_path.parent.mkdir(parents=True, exist_ok=True)

            raw_json = orjson.dumps(
                payload, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS
            )
            scrubbed = scrub_secrets(
                raw_json.decode("utf-8"),
                secrets=self._scrub_secrets,
            )
            absolute_path.write_text(scrubbed + "\n", encoding="utf-8")
            return absolute_path.relative_to(base_dir)
        except Exception as exc:
            logger.bind(
                module="pipeline.artifacts", run_id=run_id, item_id=item_id
            ).warning(
                "Debug artifact write failed: {}",
                self._sanitize_error_message(str(exc)),
            )
            return None

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
        return scrub_secrets(
            message,
            secrets=self._scrub_secrets,
        )

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]:
        if isinstance(exc, httpx.HTTPStatusError):
            status = int(getattr(getattr(exc, "response", None), "status_code", 0) or 0)
            return {
                "error_category": "http_status",
                "retryable": status >= 500 or status == 429,
                "http_status": status,
            }
        if isinstance(exc, httpx.RequestError):
            return {"error_category": "http_request", "retryable": True}
        if isinstance(exc, ValueError):
            return {"error_category": "validation", "retryable": False}
        return {"error_category": "unknown", "retryable": False}

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
