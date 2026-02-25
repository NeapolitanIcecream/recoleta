from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any

import httpx
import orjson
from loguru import logger
from rich.progress import track

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.delivery import TelegramSender
from recoleta.extract import extract_html_maintext, fetch_url_html
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.observability import collect_environment_secrets, mask_value, scrub_secrets
from recoleta.ports import RepositoryPort
from recoleta.publish import build_telegram_message, write_obsidian_note
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
        self._scrub_secrets = tuple(
            dict.fromkeys(
                (
                    settings.telegram_bot_token.get_secret_value(),
                    settings.telegram_chat_id.get_secret_value(),
                    *collect_environment_secrets(),
                )
            )
        )
        self.analyzer = analyzer or LiteLLMAnalyzer(model=settings.llm_model)
        self.telegram_sender = telegram_sender or TelegramSender(
            token=settings.telegram_bot_token.get_secret_value(),
            chat_id=settings.telegram_chat_id.get_secret_value(),
        )

    def ingest(self, *, run_id: str, drafts: list[ItemDraft] | None = None) -> IngestResult:
        log = logger.bind(module="pipeline.ingest", run_id=run_id)
        started = time.perf_counter()
        ingest_result = IngestResult()
        source_drafts = drafts if drafts is not None else self._pull_source_drafts()
        for draft in track(source_drafts, description="Ingesting items"):
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
            name="pipeline.ingest.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        log.info(
            "Ingest completed with inserted={} updated={} failed={}",
            ingest_result.inserted,
            ingest_result.updated,
            ingest_result.failed,
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
            for item in track(items, description="Analyzing items"):
                try:
                    if item.id is None:
                        analyze_result.failed += 1
                        log.warning("Analyze skipped: item has no id")
                        continue

                    content_text: str | None = None
                    enrich_item_started = time.perf_counter()
                    try:
                        existing_content = self.repository.get_latest_content(
                            item_id=item.id,
                            content_type="html_maintext",
                        )
                        if existing_content is not None and existing_content.text:
                            content_text = existing_content.text
                            enrich_skipped += 1
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
                            enrich_processed += 1
                    except Exception as enrich_exc:
                        enrich_failed += 1
                        analyze_result.failed += 1
                        sanitized_error = self._sanitize_error_message(str(enrich_exc))
                        try:
                            self.repository.mark_item_failed(item_id=item.id)
                        except Exception as mark_exc:
                            log.bind(item_id=item.id).warning(
                                "Enrich mark_item_failed failed: {}",
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
                    if item.id is not None:
                        try:
                            self.repository.mark_item_failed(item_id=item.id)
                        except Exception as mark_exc:
                            log.bind(item_id=item.id).warning(
                                "Analyze mark_item_failed failed: {}",
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
            log.info("Publish skipped: daily delivery cap reached sent_today={} cap={}", sent_today, self.settings.max_deliveries_per_day)
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

        effective_limit = min(limit, remaining_today)
        candidates = self.repository.list_items_for_publish(
            limit=effective_limit,
            min_relevance_score=self.settings.min_relevance_score,
        )
        for item, analysis in track(candidates, description="Publishing items"):
            if item.id is None:
                continue
            if self.repository.has_sent_delivery(
                item_id=item.id,
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=destination_hash,
            ):
                publish_result.skipped += 1
                continue

            try:
                note_path = write_obsidian_note(
                    vault_path=self.settings.obsidian_vault_path,
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
                message_text = build_telegram_message(
                    title=item.title,
                    summary=analysis.summary,
                    insight=analysis.insight,
                    url=item.canonical_url,
                )
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
                publish_result.note_paths.append(note_path)
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
            name="pipeline.publish.failed_total",
            value=publish_result.failed,
            unit="count",
        )
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

    def _pull_source_drafts(self) -> list[ItemDraft]:
        hn_urls = list(dict.fromkeys(self.settings.sources.hn.rss_urls))
        rss_urls = list(dict.fromkeys(self.settings.sources.rss.feeds))
        arxiv_queries = list(dict.fromkeys(self.settings.sources.arxiv.queries))
        openreview_venues = list(dict.fromkeys(self.settings.sources.openreview.venues))
        drafts: list[ItemDraft] = []
        if self.settings.sources.hf_daily.enabled:
            drafts.extend(sources.fetch_hf_daily_papers_drafts(max_items=50))
        if hn_urls:
            drafts.extend(sources.fetch_rss_drafts(feed_urls=hn_urls, source="hn"))
        if rss_urls:
            drafts.extend(sources.fetch_rss_drafts(feed_urls=rss_urls, source="rss"))
        if arxiv_queries:
            drafts.extend(
                sources.fetch_arxiv_drafts(
                    queries=arxiv_queries,
                    max_results_per_run=self.settings.sources.arxiv.max_results_per_run,
                )
            )
        if openreview_venues:
            drafts.extend(sources.fetch_openreview_drafts(venues=openreview_venues, max_results_per_venue=50))
        return drafts

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
