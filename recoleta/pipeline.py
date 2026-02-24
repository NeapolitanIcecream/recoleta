from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from loguru import logger
from rich.progress import track

from recoleta.analyzer import Analyzer, LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.delivery import TelegramSender
from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.observability import mask_value
from recoleta.publish import build_telegram_message, write_obsidian_note
from recoleta.sources import fetch_rss_drafts
from recoleta.storage import Repository
from recoleta.types import AnalyzeResult, IngestResult, ItemDraft, PublishResult


class PipelineService:
    def __init__(
        self,
        *,
        settings: Settings,
        repository: Repository,
        analyzer: Analyzer | None = None,
        telegram_sender: Any | None = None,
    ) -> None:
        self.settings = settings
        self.repository = repository
        self.analyzer = analyzer or LiteLLMAnalyzer(model=settings.llm_model)
        self.telegram_sender = telegram_sender or TelegramSender(
            token=settings.telegram_bot_token.get_secret_value(),
            chat_id=settings.telegram_chat_id.get_secret_value(),
        )

    def ingest(self, *, run_id: str, drafts: list[ItemDraft] | None = None) -> IngestResult:
        log = logger.bind(module="pipeline.ingest", run_id=run_id)
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
                log.bind(item_hash=draft.canonical_url_hash).warning("Ingest failed: {}", str(exc))

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
        log.info(
            "Ingest completed with inserted={} updated={} failed={}",
            ingest_result.inserted,
            ingest_result.updated,
            ingest_result.failed,
        )
        return ingest_result

    def analyze(self, *, run_id: str, limit: int = 100) -> AnalyzeResult:
        log = logger.bind(module="pipeline.analyze", run_id=run_id)
        items = self.repository.list_items_for_analysis(limit=limit)
        analyze_result = AnalyzeResult()
        for item in track(items, description="Analyzing items"):
            try:
                if item.id is None:
                    analyze_result.failed += 1
                    log.warning("Analyze skipped: item has no id")
                    continue
                analysis_result = self.analyzer.analyze(
                    title=item.title,
                    canonical_url=item.canonical_url,
                    user_topics=self.settings.topics,
                )
                self.repository.save_analysis(item_id=item.id, result=analysis_result)
                analyze_result.processed += 1
            except Exception as exc:
                analyze_result.failed += 1
                if item.id is not None:
                    self.repository.mark_item_failed(item_id=item.id)
                artifact_path = self._write_debug_artifact(
                    run_id=run_id,
                    item_id=item.id,
                    kind="error_context",
                    payload={
                        "stage": "analyze",
                        "error_type": type(exc).__name__,
                        "error_message": str(exc),
                        "item_id": item.id,
                    },
                )
                if artifact_path is not None:
                    self.repository.add_artifact(
                        run_id=run_id,
                        item_id=item.id,
                        kind="error_context",
                        path=str(artifact_path),
                    )
                log.bind(item_id=item.id).warning("Analyze failed: {}", str(exc))

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
        log.info(
            "Analyze completed with processed={} failed={}",
            analyze_result.processed,
            analyze_result.failed,
        )
        return analyze_result

    def publish(self, *, run_id: str, limit: int = 50) -> PublishResult:
        log = logger.bind(module="pipeline.publish", run_id=run_id)
        publish_result = PublishResult()
        destination_hash = mask_value(self.settings.telegram_chat_id.get_secret_value())
        candidates = self.repository.list_items_for_publish(
            limit=limit,
            min_relevance_score=self.settings.min_relevance_score,
        )
        for item, analysis in track(candidates, description="Publishing items"):
            if item.id is None:
                continue
            if self.repository.delivery_exists(
                item_id=item.id,
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=destination_hash,
            ):
                publish_result.skipped += 1
                continue

            note_path = write_obsidian_note(
                vault_path=self.settings.obsidian_vault_path,
                base_folder=self.settings.obsidian_base_folder,
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
            try:
                message_id = self.telegram_sender.send(message_text)
                self.repository.add_delivery(
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
                self.repository.add_delivery(
                    item_id=item.id,
                    channel=DELIVERY_CHANNEL_TELEGRAM,
                    destination=destination_hash,
                    message_id=None,
                    status=DELIVERY_STATUS_FAILED,
                    error=str(exc),
                )
                publish_result.failed += 1
                log.bind(item_id=item.id).warning("Publish failed: {}", str(exc))

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
        drafts: list[ItemDraft] = []
        if hn_urls:
            drafts.extend(fetch_rss_drafts(feed_urls=hn_urls, source="hn"))
        if rss_urls:
            drafts.extend(fetch_rss_drafts(feed_urls=rss_urls, source="rss"))
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
        artifact_dir = self.settings.artifacts_dir / run_id
        artifact_dir.mkdir(parents=True, exist_ok=True)
        file_name = f"{item_id or 'no-item'}-{kind}-debug.json"
        path = artifact_dir / file_name
        path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")
        return path
