from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
import orjson
from loguru import logger
from rich.progress import BarColumn, Progress, TaskProgressColumn, TextColumn, TimeElapsedColumn

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.delivery import TelegramSender
from recoleta.extract import extract_html_maintext, extract_pdf_text, fetch_url_bytes, fetch_url_html
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ENRICHED,
)
from recoleta.observability import collect_environment_secrets, get_rich_console, mask_value, scrub_secrets
from recoleta.ports import RepositoryPort
from recoleta.publish import build_telegram_message, write_markdown_note, write_markdown_run_index, write_obsidian_note
from recoleta import sources
from recoleta.triage import SemanticTriage, TriageCandidate
from recoleta.types import AnalyzeResult, IngestResult, ItemDraft, PublishResult, utc_now


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
        scrub_candidates.extend(collect_environment_secrets())
        self._scrub_secrets = tuple(dict.fromkeys(scrub_candidates))
        self._progress_console = get_rich_console()
        self.analyzer = analyzer or LiteLLMAnalyzer(
            model=settings.llm_model,
            output_language=settings.llm_output_language,
        )
        self.semantic_triage = triage or SemanticTriage(
            embedding_batch_max_inputs=settings.triage_embedding_batch_max_inputs,
            embedding_batch_max_chars=settings.triage_embedding_batch_max_chars,
        )
        self.telegram_sender = telegram_sender
        if self.telegram_sender is None and "telegram" in settings.publish_targets:
            if settings.telegram_bot_token is not None and settings.telegram_chat_id is not None:
                self.telegram_sender = TelegramSender(
                    token=settings.telegram_bot_token.get_secret_value(),
                    chat_id=settings.telegram_chat_id.get_secret_value(),
                )

    def ingest(self, *, run_id: str, drafts: list[ItemDraft] | None = None) -> IngestResult:
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
                source_drafts, source_failures_total = self._pull_source_drafts(run_id=run_id, log=log)

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
                    log.bind(item_hash=draft.canonical_url_hash).warning("Ingest failed: {}", sanitized_error)
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

    def prepare(self, *, run_id: str, drafts: list[ItemDraft] | None = None, limit: int | None = None) -> IngestResult:
        effective_limit = self._resolve_analysis_limit(limit=limit)
        candidate_limit = self._resolve_triage_candidate_limit(limit=effective_limit)
        ingest_result = self.ingest(run_id=run_id, drafts=drafts)
        self.enrich(run_id=run_id, limit=candidate_limit)
        self.triage(run_id=run_id, limit=effective_limit, candidate_limit=candidate_limit)
        return ingest_result

    def enrich(self, *, run_id: str, limit: int) -> None:
        log = logger.bind(module="pipeline.enrich", run_id=run_id)
        enrich_started = time.perf_counter()
        include_debug = self.settings.write_debug_artifacts and self.settings.artifacts_dir is not None
        items = self.repository.list_items_for_analysis(limit=limit)
        enrich_processed = 0
        enrich_failed = 0
        enrich_skipped = 0
        enrich_duration_ms_total = 0

        def write_and_record_artifact(*, item_id: int | None, kind: str, payload: dict[str, Any]) -> None:
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
        with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
            with Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self._progress_console,
            ) as progress:
                for item in progress.track(items, description="Enriching items"):
                    raw_item_id = getattr(item, "id", None)
                    if raw_item_id is None:
                        enrich_failed += 1
                        log.warning("Enrich skipped: item has no id")
                        continue
                    item_id = int(raw_item_id)
                    enrich_item_started = time.perf_counter()
                    try:
                        _, stored_new_content = self._ensure_item_content(client=client, item=item, log=log)
                        self.repository.mark_item_enriched(item_id=item_id)
                        if stored_new_content:
                            enrich_processed += 1
                        else:
                            enrich_skipped += 1
                    except Exception as enrich_exc:
                        enrich_failed += 1
                        sanitized_error = self._sanitize_error_message(str(enrich_exc))
                        classification = self._classify_exception(enrich_exc)
                        try:
                            if classification.get("retryable") is True:
                                self.repository.mark_item_retryable_failed(item_id=item_id)
                            else:
                                self.repository.mark_item_failed(item_id=item_id)
                        except Exception as mark_exc:
                            log.bind(item_id=item_id).warning(
                                "Enrich mark_item_state failed: {}",
                                self._sanitize_error_message(str(mark_exc)),
                            )
                        if include_debug:
                            write_and_record_artifact(
                                item_id=item_id,
                                kind="error_context",
                                payload={
                                    "stage": "enrich",
                                    "error_type": type(enrich_exc).__name__,
                                    "error_message": sanitized_error,
                                    "item_id": item_id,
                                    **classification,
                                },
                            )
                        log.bind(item_id=item_id).warning("Enrich failed: {}", sanitized_error)
                    finally:
                        enrich_duration_ms_total += int((time.perf_counter() - enrich_item_started) * 1000)

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
        log.info(
            "Enrich completed with processed={} skipped={} failed={}",
            enrich_processed,
            enrich_skipped,
            enrich_failed,
        )

    def triage(self, *, run_id: str, limit: int, candidate_limit: int | None = None) -> None:
        triage_enabled = bool(self.settings.triage_enabled) and bool(self.settings.topics)
        if not triage_enabled:
            return

        normalized_limit = self._resolve_analysis_limit(limit=limit)
        normalized_candidate_limit = candidate_limit or self._resolve_triage_candidate_limit(limit=normalized_limit)
        include_debug = self.settings.write_debug_artifacts and self.settings.artifacts_dir is not None
        log = logger.bind(module="pipeline.triage", run_id=run_id)
        items = self.repository.list_items_for_llm_analysis(
            limit=normalized_candidate_limit,
            triage_required=False,
        )
        triage_items = [item for item in items if getattr(item, "state", None) == ITEM_STATE_ENRICHED]

        def write_and_record_artifact(*, item_id: int | None, kind: str, payload: dict[str, Any]) -> None:
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

        triage_candidates, content_fetch_failed, content_fetch_error = self._build_triage_candidates(
            items=triage_items
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
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        started = time.perf_counter()
        triage_required = bool(self.settings.triage_enabled) and bool(self.settings.topics)
        effective_limit = self._resolve_analysis_limit(limit=limit)
        items = self.repository.list_items_for_llm_analysis(limit=effective_limit, triage_required=triage_required)
        analyze_result = AnalyzeResult()
        llm_calls_total = 0
        llm_errors_total = 0
        missing_content_total = 0
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
            self.settings.llm_model.split("/", 1)[0] if "/" in self.settings.llm_model else "unknown"
        )
        configured_provider_token = metric_token(configured_provider, max_len=24)
        configured_model_token = metric_token(self.settings.llm_model)
        include_debug = self.settings.write_debug_artifacts and self.settings.artifacts_dir is not None

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

        def write_and_record_artifact(*, item_id: int | None, kind: str, payload: dict[str, Any]) -> None:
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
                        log.bind(item_id=item_id).warning("Analyze failed: missing stored content")
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
                    llm_calls_by_model_token[model_token] = llm_calls_by_model_token.get(model_token, 0) + 1

                    if include_debug:
                        if debug is None:
                            raise RuntimeError(
                                "Analyzer did not return debug payload while include_debug is enabled"
                            )
                        write_and_record_artifact(item_id=item_id, kind="llm_request", payload=debug.request)
                        write_and_record_artifact(item_id=item_id, kind="llm_response", payload=debug.response)

                    self.repository.save_analysis(item_id=item_id, result=analysis_result)
                    analyze_result.processed += 1
                except Exception as exc:
                    analyze_result.failed += 1
                    llm_errors_total += 1
                    llm_errors_by_provider_token[configured_provider_token] = (
                        llm_errors_by_provider_token.get(configured_provider_token, 0) + 1
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
                    log.bind(item_id=item_id).warning("Analyze failed: {}", sanitized_error)

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

    def _resolve_analysis_limit(self, *, limit: int | None) -> int:
        resolved = int(self.settings.analyze_limit if limit is None else limit)
        if resolved <= 0:
            raise ValueError("limit must be > 0")
        return resolved

    def _resolve_triage_candidate_limit(self, *, limit: int) -> int:
        triage_enabled = bool(self.settings.triage_enabled) and bool(self.settings.topics)
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
        if source in {"arxiv", "openreview"}:
            existing_pdf = self.repository.get_latest_content(
                item_id=normalized_item_id,
                content_type="pdf_text",
            )
            if existing_pdf is not None and existing_pdf.text:
                return existing_pdf.text
        existing_html = self.repository.get_latest_content(
            item_id=normalized_item_id,
            content_type="html_maintext",
        )
        if existing_html is not None and existing_html.text:
            return existing_html.text
        return None

    def _ensure_item_content(self, *, client: httpx.Client, item: Any, log: Any) -> tuple[str, bool]:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item id is required for enrichment")
        item_id = int(raw_item_id)
        content_text: str | None = None
        stored_new_content = False
        source = str(getattr(item, "source", "") or "").strip().lower()
        canonical_url = str(getattr(item, "canonical_url", "") or "")
        source_item_id = getattr(item, "source_item_id", None)

        if source in {"arxiv", "openreview"}:
            existing_pdf = self.repository.get_latest_content(
                item_id=item_id,
                content_type="pdf_text",
            )
            if existing_pdf is not None and existing_pdf.text:
                content_text = existing_pdf.text
            else:
                pdf_url = self._build_pdf_url(
                    source=source,
                    canonical_url=canonical_url,
                    source_item_id=source_item_id,
                )
                if pdf_url:
                    try:
                        pdf_bytes = fetch_url_bytes(client, pdf_url)
                        extracted_pdf = extract_pdf_text(pdf_bytes)
                        if extracted_pdf is None:
                            raise RuntimeError("empty pdf text extraction")
                        self.repository.upsert_content(
                            item_id=item_id,
                            content_type="pdf_text",
                            text=extracted_pdf,
                        )
                        content_text = extracted_pdf
                        stored_new_content = True
                    except Exception as pdf_exc:
                        log.bind(item_id=item_id).warning(
                            "PDF enrich failed, falling back to HTML: {}",
                            self._sanitize_error_message(str(pdf_exc)),
                        )

        if content_text is None:
            existing_html = self.repository.get_latest_content(
                item_id=item_id,
                content_type="html_maintext",
            )
            if existing_html is not None and existing_html.text:
                content_text = existing_html.text
            else:
                html = fetch_url_html(client, canonical_url)
                extracted = extract_html_maintext(html)
                if extracted is None:
                    raise RuntimeError("empty html maintext extraction")
                self.repository.upsert_content(
                    item_id=item_id,
                    content_type="html_maintext",
                    text=extracted,
                )
                content_text = extracted
                stored_new_content = True

        if content_text is None or not content_text.strip():
            raise RuntimeError("empty enriched content")
        return content_text, stored_new_content

    def publish(self, *, run_id: str, limit: int = 50) -> PublishResult:
        log = logger.bind(module="pipeline.publish", run_id=run_id)
        started = time.perf_counter()
        publish_result = PublishResult()
        targets = set(self.settings.publish_targets)
        enable_markdown = "markdown" in targets
        enable_obsidian = "obsidian" in targets
        enable_telegram = "telegram" in targets

        markdown_notes: list[tuple[str, Path]] = []

        if enable_obsidian and self.settings.obsidian_vault_path is None:
            raise ValueError("OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'")

        destination_hash: str | None = None
        remaining_today: int | None = None
        if enable_telegram:
            if self.settings.telegram_bot_token is None or self.settings.telegram_chat_id is None:
                raise ValueError("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required when PUBLISH_TARGETS includes 'telegram'")
            if self.telegram_sender is None:
                self.telegram_sender = TelegramSender(
                    token=self.settings.telegram_bot_token.get_secret_value(),
                    chat_id=self.settings.telegram_chat_id.get_secret_value(),
                )
            destination_hash = mask_value(self.settings.telegram_chat_id.get_secret_value())
            now = utc_now()
            midnight_utc = datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                tzinfo=now.tzinfo,
            )
            sent_today = self.repository.count_sent_deliveries_since(
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=destination_hash,
                since=midnight_utc,
            )
            remaining_today = max(0, self.settings.max_deliveries_per_day - sent_today)
            if remaining_today <= 0:
                log.info(
                    "Publish skipped: daily delivery cap reached sent_today={} cap={}",
                    sent_today,
                    self.settings.max_deliveries_per_day,
                )

        effective_limit = min(limit, remaining_today) if remaining_today is not None else limit
        candidates = self.repository.list_items_for_publish(
            limit=effective_limit,
            min_relevance_score=self.settings.min_relevance_score,
        )
        allow_tags = {tag.strip().lower() for tag in self.settings.allow_tags if tag.strip()}
        deny_tags = {tag.strip().lower() for tag in self.settings.deny_tags if tag.strip()}
        filtered_total = 0
        with Progress(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self._progress_console,
        ) as progress:
            for item, analysis in progress.track(candidates, description="Publishing items"):
                if item.id is None:
                    continue
                telegram_already_sent = False
                if enable_telegram and destination_hash is not None:
                    telegram_already_sent = self.repository.has_sent_delivery(
                        item_id=item.id,
                        channel=DELIVERY_CHANNEL_TELEGRAM,
                        destination=destination_hash,
                    )
                if allow_tags or deny_tags:
                    topics = {
                        tag.strip().lower()
                        for tag in self.repository.decode_list(analysis.topics_json)
                        if tag.strip()
                    }
                    if deny_tags and (topics & deny_tags):
                        publish_result.skipped += 1
                        filtered_total += 1
                        continue
                    if allow_tags and not (topics & allow_tags):
                        publish_result.skipped += 1
                        filtered_total += 1
                        continue

                try:
                    note_paths: list[Path] = []
                    if enable_obsidian:
                        vault_path = self.settings.obsidian_vault_path
                        if vault_path is None:
                            raise RuntimeError("obsidian vault path is not configured")
                        note_paths.append(
                            write_obsidian_note(
                                vault_path=vault_path,
                                base_folder=self.settings.obsidian_base_folder,
                                item_id=item.id,
                                title=item.title,
                                source=item.source,
                                canonical_url=item.canonical_url,
                                published_at=item.published_at,
                                authors=self.repository.decode_list(item.authors),
                                topics=self.repository.decode_list(analysis.topics_json),
                                relevance_score=analysis.relevance_score,
                                run_id=run_id,
                                summary=analysis.summary,
                                insight=analysis.insight,
                                ideas=self.repository.decode_list(analysis.idea_directions_json),
                            )
                        )
                    if enable_markdown:
                        md_note_path = write_markdown_note(
                            output_dir=self.settings.markdown_output_dir,
                            item_id=item.id,
                            title=item.title,
                            source=item.source,
                            canonical_url=item.canonical_url,
                            published_at=item.published_at,
                            authors=self.repository.decode_list(item.authors),
                            topics=self.repository.decode_list(analysis.topics_json),
                            relevance_score=analysis.relevance_score,
                            run_id=run_id,
                            summary=analysis.summary,
                            insight=analysis.insight,
                            ideas=self.repository.decode_list(analysis.idea_directions_json),
                        )
                        markdown_notes.append((item.title, md_note_path))
                        note_paths.append(md_note_path)
                    if enable_telegram and destination_hash is not None and not telegram_already_sent:
                        message_text = build_telegram_message(
                            title=item.title,
                            summary=analysis.summary,
                            insight=analysis.insight,
                            url=item.canonical_url,
                        )
                        if self.telegram_sender is None:
                            raise RuntimeError("telegram sender is not configured")
                        message_id = self.telegram_sender.send(message_text)
                        self.repository.upsert_delivery(
                            item_id=item.id,
                            channel=DELIVERY_CHANNEL_TELEGRAM,
                            destination=destination_hash,
                            message_id=message_id,
                            status=DELIVERY_STATUS_SENT,
                        )
                        telegram_already_sent = True
                    self.repository.mark_item_published(item_id=item.id)
                    publish_result.sent += 1
                    publish_result.note_paths.extend(note_paths)
                except Exception as exc:
                    sanitized_error = self._sanitize_error_message(str(exc))
                    artifact_path = self._write_debug_artifact(
                        run_id=run_id,
                        item_id=item.id,
                        kind="error_context",
                        payload={
                            "stage": "publish",
                            "error_type": type(exc).__name__,
                            "error_message": sanitized_error,
                            "item_id": item.id,
                            **self._classify_exception(exc),
                        },
                    )
                    if artifact_path is not None:
                        try:
                            self.repository.add_artifact(
                                run_id=run_id,
                                item_id=item.id,
                                kind="error_context",
                                path=str(artifact_path),
                            )
                        except Exception as artifact_exc:
                            log.bind(item_id=item.id).warning(
                                "Publish debug artifact record failed: {}",
                                self._sanitize_error_message(str(artifact_exc)),
                            )
                    if enable_telegram and destination_hash is not None and not telegram_already_sent:
                        self.repository.upsert_delivery(
                            item_id=item.id,
                            channel=DELIVERY_CHANNEL_TELEGRAM,
                            destination=destination_hash,
                            message_id=None,
                            status=DELIVERY_STATUS_FAILED,
                            error=sanitized_error,
                        )
                    publish_result.failed += 1
                    log.bind(item_id=item.id).warning("Publish failed: {}", sanitized_error)

        if enable_markdown:
            try:
                write_markdown_run_index(
                    output_dir=self.settings.markdown_output_dir,
                    run_id=run_id,
                    generated_at=utc_now(),
                    notes=markdown_notes,
                )
            except Exception as exc:
                log.bind(module="pipeline.publish.markdown_index").warning(
                    "Markdown index write failed: {}",
                    self._sanitize_error_message(str(exc)),
                )

        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.sent_total",
            value=publish_result.sent,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.skipped_total",
            value=publish_result.skipped,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.filtered_total",
            value=filtered_total,
            unit="count",
        )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.failed_total",
            value=publish_result.failed,
            unit="count",
        )
        if remaining_today is not None:
            self.repository.record_metric(
                run_id=run_id,
                name="pipeline.publish.daily_cap_remaining",
                value=max(0, remaining_today - publish_result.sent),
                unit="count",
            )
        self.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.info(
            "Publish completed with sent={} skipped={} failed={}",
            publish_result.sent,
            publish_result.skipped,
            publish_result.failed,
        )
        return publish_result

    def _pull_source_drafts(self, *, run_id: str, log: Any) -> tuple[list[ItemDraft], int]:
        hn_urls = list(dict.fromkeys(self.settings.sources.hn.rss_urls))
        rss_urls = list(dict.fromkeys(self.settings.sources.rss.feeds))
        arxiv_queries = list(dict.fromkeys(self.settings.sources.arxiv.queries))
        openreview_venues = list(dict.fromkeys(self.settings.sources.openreview.venues))
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
                log.bind(source=source_name).warning("Source pull failed: {}", sanitized_error)

        if self.settings.sources.hf_daily.enabled:
            pull("hf_daily", lambda: sources.fetch_hf_daily_papers_drafts(max_items=50))
        if hn_urls:
            pull("hn", lambda: sources.fetch_rss_drafts(feed_urls=hn_urls, source="hn"))
        if rss_urls:
            pull("rss", lambda: sources.fetch_rss_drafts(feed_urls=rss_urls, source="rss"))
        if arxiv_queries:
            pull(
                "arxiv",
                lambda: sources.fetch_arxiv_drafts(
                    queries=arxiv_queries,
                    max_results_per_run=self.settings.sources.arxiv.max_results_per_run,
                ),
            )
        if openreview_venues:
            pull("openreview", lambda: sources.fetch_openreview_drafts(venues=openreview_venues, max_results_per_venue=50))
        return drafts, source_failures_total

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None:
        if not self.settings.write_debug_artifacts or self.settings.artifacts_dir is None:
            return None
        try:
            def sanitize_segment(value: str, *, max_len: int = 72, fallback: str = "unknown") -> str:
                cleaned = value.strip()
                normalized = "".join(ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned)
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

            raw_json = orjson.dumps(payload, option=orjson.OPT_INDENT_2 | orjson.OPT_SORT_KEYS)
            scrubbed = scrub_secrets(
                raw_json.decode("utf-8"),
                secrets=self._scrub_secrets,
            )
            absolute_path.write_text(scrubbed + "\n", encoding="utf-8")
            return absolute_path.relative_to(base_dir)
        except Exception as exc:
            logger.bind(module="pipeline.artifacts", run_id=run_id, item_id=item_id).warning(
                "Debug artifact write failed: {}",
                self._sanitize_error_message(str(exc)),
            )
            return None

    def _build_triage_candidates(self, *, items: list[Any]) -> tuple[list[TriageCandidate], bool, dict[str, Any] | None]:
        candidates_items: list[Any] = []
        item_ids: list[int] = []
        pdf_item_ids: list[int] = []
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

        if not candidates_items:
            return [], False, None

        max_chars = int(getattr(self.settings, "triage_item_text_max_chars", 1200) or 1200)
        html_by_id: dict[int, Any] = {}
        pdf_by_id: dict[int, Any] = {}
        content_fetch_failed = False
        content_fetch_error: dict[str, Any] | None = None
        try:
            html_by_id = self.repository.get_latest_contents(item_ids=item_ids, content_type="html_maintext")
            if pdf_item_ids:
                pdf_by_id = self.repository.get_latest_contents(item_ids=pdf_item_ids, content_type="pdf_text")
        except Exception as exc:  # noqa: BLE001
            content_fetch_failed = True
            sanitized_error = self._sanitize_error_message(str(exc))
            content_fetch_error = {
                "stage": "triage_content_fetch",
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                **self._classify_exception(exc),
                "content_types": ["html_maintext", "pdf_text"],
                "item_ids_total": len(item_ids),
                "pdf_item_ids_total": len(pdf_item_ids),
            }
            html_by_id = {}
            pdf_by_id = {}

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

            combined = title
            if excerpt:
                trimmed_excerpt = excerpt.strip()
                if trimmed_excerpt:
                    combined = f"{title}\n\n{trimmed_excerpt}" if title else trimmed_excerpt

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
    def _build_pdf_url(*, source: str, canonical_url: str, source_item_id: str | None) -> str | None:
        normalized_url = canonical_url.strip()
        if not normalized_url:
            return None

        if source == "arxiv":
            if "arxiv.org" not in normalized_url:
                return None
            if "/abs/" in normalized_url:
                base = normalized_url.replace("/abs/", "/pdf/", 1)
            elif "/pdf/" in normalized_url:
                base = normalized_url
            else:
                return None
            return base if base.endswith(".pdf") else f"{base}.pdf"

        if source == "openreview":
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
