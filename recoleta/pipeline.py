from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import httpx
import orjson
from loguru import logger
from rich.console import Console
from rich.progress import track

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.delivery import TelegramSender
from recoleta.extract import extract_html_maintext, extract_pdf_text, fetch_url_bytes, fetch_url_html
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.observability import collect_environment_secrets, mask_value, scrub_secrets
from recoleta.ports import RepositoryPort
from recoleta.publish import build_telegram_message, write_markdown_note, write_markdown_run_index, write_obsidian_note
from recoleta import sources
from recoleta.types import AnalyzeResult, IngestResult, ItemDraft, PublishResult, utc_now


class PipelineService:
    def __init__(
        self,
        *,
        settings: Settings,
        repository: RepositoryPort,
        analyzer: Analyzer | None = None,
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
        self._progress_console = Console(stderr=True)
        self.analyzer = analyzer or LiteLLMAnalyzer(
            model=settings.llm_model,
            output_language=settings.llm_output_language,
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
        if source_drafts is None:
            source_drafts, source_failures_total = self._pull_source_drafts(run_id=run_id, log=log)

        for draft in track(source_drafts, description="Ingesting items", console=self._progress_console):
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

    def analyze(self, *, run_id: str, limit: int = 100) -> AnalyzeResult:
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        started = time.perf_counter()
        items = self.repository.list_items_for_analysis(limit=limit)
        analyze_result = AnalyzeResult()
        llm_calls_total = 0
        llm_errors_total = 0
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
        enrich_processed = 0
        enrich_failed = 0
        enrich_skipped = 0
        enrich_duration_ms_total = 0

        timeout = httpx.Timeout(10.0, connect=5.0)
        headers = {"User-Agent": "recoleta/0.1"}
        with httpx.Client(timeout=timeout, headers=headers, follow_redirects=True) as client:
            for item in track(items, description="Analyzing items", console=self._progress_console):
                try:
                    if item.id is None:
                        analyze_result.failed += 1
                        log.warning("Analyze skipped: item has no id")
                        continue

                    content_text: str | None = None
                    enrich_item_started = time.perf_counter()
                    try:
                        stored_new_content = False
                        if item.source in {"arxiv", "openreview"}:
                            existing_pdf = self.repository.get_latest_content(
                                item_id=item.id,
                                content_type="pdf_text",
                            )
                            if existing_pdf is not None and existing_pdf.text:
                                content_text = existing_pdf.text
                            else:
                                pdf_url = self._build_pdf_url(
                                    source=item.source,
                                    canonical_url=item.canonical_url,
                                    source_item_id=item.source_item_id,
                                )
                                if pdf_url:
                                    try:
                                        pdf_bytes = fetch_url_bytes(client, pdf_url)
                                        extracted_pdf = extract_pdf_text(pdf_bytes)
                                        if extracted_pdf is None:
                                            raise RuntimeError("empty pdf text extraction")
                                        self.repository.upsert_content(
                                            item_id=item.id,
                                            content_type="pdf_text",
                                            text=extracted_pdf,
                                        )
                                        self.repository.mark_item_enriched(item_id=item.id)
                                        content_text = extracted_pdf
                                        stored_new_content = True
                                    except Exception as pdf_exc:
                                        log.bind(item_id=item.id).warning(
                                            "PDF enrich failed, falling back to HTML: {}",
                                            self._sanitize_error_message(str(pdf_exc)),
                                        )

                        if content_text is None:
                            existing_html = self.repository.get_latest_content(
                                item_id=item.id,
                                content_type="html_maintext",
                            )
                            if existing_html is not None and existing_html.text:
                                content_text = existing_html.text
                            else:
                                html = fetch_url_html(client, item.canonical_url)
                                extracted = extract_html_maintext(html)
                                if extracted is None:
                                    raise RuntimeError("empty html maintext extraction")
                                self.repository.upsert_content(
                                    item_id=item.id,
                                    content_type="html_maintext",
                                    text=extracted,
                                )
                                self.repository.mark_item_enriched(item_id=item.id)
                                content_text = extracted
                                stored_new_content = True

                        if stored_new_content:
                            enrich_processed += 1
                        else:
                            enrich_skipped += 1
                    except Exception as enrich_exc:
                        enrich_failed += 1
                        analyze_result.failed += 1
                        sanitized_error = self._sanitize_error_message(str(enrich_exc))
                        classification = self._classify_exception(enrich_exc)
                        try:
                            if classification.get("retryable") is True:
                                self.repository.mark_item_retryable_failed(item_id=item.id)
                            else:
                                self.repository.mark_item_failed(item_id=item.id)
                        except Exception as mark_exc:
                            log.bind(item_id=item.id).warning(
                                "Enrich mark_item_state failed: {}",
                                self._sanitize_error_message(str(mark_exc)),
                            )
                        write_and_record_artifact(
                            item_id=item.id,
                            kind="error_context",
                            payload={
                                "stage": "enrich",
                                "error_type": type(enrich_exc).__name__,
                                "error_message": sanitized_error,
                                "item_id": item.id,
                                **classification,
                            },
                        )
                        log.bind(item_id=item.id).warning("Enrich failed: {}", sanitized_error)
                        continue
                    finally:
                        enrich_duration_ms_total += int((time.perf_counter() - enrich_item_started) * 1000)

                    llm_calls_total += 1
                    analysis_result, debug = self.analyzer.analyze(
                        title=item.title,
                        canonical_url=item.canonical_url,
                        user_topics=self.settings.topics,
                        content=content_text,
                        include_debug=include_debug,
                    )
                    provider_token = bucket_provider_token(analysis_result.provider)
                    llm_calls_by_provider_token[provider_token] = llm_calls_by_provider_token.get(provider_token, 0) + 1

                    model_token = bucket_model_token(analysis_result.model)
                    llm_calls_by_model_token[model_token] = llm_calls_by_model_token.get(model_token, 0) + 1

                    if include_debug:
                        if debug is None:
                            raise RuntimeError("Analyzer did not return debug payload while include_debug is enabled")
                        write_and_record_artifact(item_id=item.id, kind="llm_request", payload=debug.request)
                        write_and_record_artifact(item_id=item.id, kind="llm_response", payload=debug.response)

                    self.repository.save_analysis(item_id=item.id, result=analysis_result)
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
                    if item.id is not None:
                        try:
                            if classification.get("retryable") is True:
                                self.repository.mark_item_retryable_failed(item_id=item.id)
                            else:
                                self.repository.mark_item_failed(item_id=item.id)
                        except Exception as mark_exc:
                            log.bind(item_id=item.id).warning(
                                "Analyze mark_item_state failed: {}",
                                self._sanitize_error_message(str(mark_exc)),
                            )
                    write_and_record_artifact(
                        item_id=item.id,
                        kind="error_context",
                        payload={
                            "stage": "analyze",
                            "error_type": type(exc).__name__,
                            "error_message": sanitized_error,
                            "item_id": item.id,
                            **classification,
                        },
                    )
                    log.bind(item_id=item.id).warning("Analyze failed: {}", sanitized_error)

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
            name="pipeline.enrich.duration_ms_total",
            value=enrich_duration_ms_total,
            unit="ms",
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
            "Analyze completed with processed={} failed={}",
            analyze_result.processed,
            analyze_result.failed,
        )
        return analyze_result

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
                self.repository.record_metric(
                    run_id=run_id,
                    name="pipeline.publish.daily_cap_remaining",
                    value=0,
                    unit="count",
                )
                self.repository.record_metric(
                    run_id=run_id,
                    name="pipeline.publish.duration_ms",
                    value=int((time.perf_counter() - started) * 1000),
                    unit="ms",
                )
                return publish_result

        effective_limit = min(limit, remaining_today) if remaining_today is not None else limit
        candidates = self.repository.list_items_for_publish(
            limit=effective_limit,
            min_relevance_score=self.settings.min_relevance_score,
        )
        allow_tags = {tag.strip().lower() for tag in self.settings.allow_tags if tag.strip()}
        deny_tags = {tag.strip().lower() for tag in self.settings.deny_tags if tag.strip()}
        filtered_total = 0
        for item, analysis in track(candidates, description="Publishing items", console=self._progress_console):
            if item.id is None:
                continue
            if enable_telegram and destination_hash is not None:
                if self.repository.has_sent_delivery(
                    item_id=item.id,
                    channel=DELIVERY_CHANNEL_TELEGRAM,
                    destination=destination_hash,
                ):
                    publish_result.skipped += 1
                    continue
            if allow_tags or deny_tags:
                topics = {tag.strip().lower() for tag in self.repository.decode_list(analysis.topics_json) if tag.strip()}
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
                if enable_telegram and destination_hash is not None:
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
                if enable_telegram and destination_hash is not None:
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
