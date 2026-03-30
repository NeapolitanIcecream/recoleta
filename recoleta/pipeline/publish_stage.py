from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Protocol

from loguru import logger
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.ports import PublishRepositoryPort
from recoleta.publish import (
    build_telegram_message,
    write_markdown_note,
    write_markdown_run_index,
    write_obsidian_note,
)
from recoleta.types import PublishResult, utc_now


class PublishStageService(Protocol):
    settings: Any
    telegram_sender: Any | None
    _progress_console: Any

    @property
    def repository(self) -> PublishRepositoryPort: ...

    def _invoke_repository_method(self, method_name: str, /, **kwargs: Any) -> Any: ...

    def _stage_candidate_limit(self, *, limit: int) -> int: ...

    @staticmethod
    def _rebalance_items_by_source(
        *,
        items: list[Any],
        limit: int,
    ) -> tuple[list[Any], dict[str, int], dict[str, int]]: ...

    def _record_stage_source_selection_metrics(
        self,
        *,
        run_id: str,
        stage: str,
        candidate_counts: dict[str, int],
        deferred_counts: dict[str, int],
    ) -> None: ...

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

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]: ...


def run_publish_stage(
    service: PublishStageService,
    *,
    run_id: str,
    limit: int = 50,
    period_start: Any = None,
    period_end: Any = None,
) -> PublishResult:
    log = logger.bind(module="pipeline.publish", run_id=run_id)
    started = time.perf_counter()
    publish_result = PublishResult()
    targets = set(service.settings.publish_targets)
    enable_markdown = "markdown" in targets
    enable_obsidian = "obsidian" in targets
    enable_telegram = "telegram" in targets

    markdown_notes: list[tuple[str, Path]] = []

    if enable_obsidian and service.settings.obsidian_vault_path is None:
        raise ValueError(
            "OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'"
        )

    destination_hash: str | None = None
    remaining_today: int | None = None
    if enable_telegram:
        if (
            service.settings.telegram_bot_token is None
            or service.settings.telegram_chat_id is None
        ):
            raise ValueError(
                "TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are required when PUBLISH_TARGETS includes 'telegram'"
            )
        if service.telegram_sender is None:
            from recoleta.delivery import TelegramSender

            service.telegram_sender = TelegramSender(
                token=service.settings.telegram_bot_token.get_secret_value(),
                chat_id=service.settings.telegram_chat_id.get_secret_value(),
            )
        (
            destination_hash,
            sent_today,
            remaining_today,
        ) = service._telegram_delivery_budget()
        if remaining_today <= 0:
            log.info(
                "Publish skipped: daily delivery cap reached sent_today={} cap={}",
                sent_today,
                service.settings.max_deliveries_per_day,
            )

    effective_limit = (
        min(limit, remaining_today) if remaining_today is not None else limit
    )
    candidate_limit = service._stage_candidate_limit(limit=effective_limit)
    candidates = service._invoke_repository_method(
        "list_items_for_publish",
        limit=candidate_limit,
        min_relevance_score=service.settings.min_relevance_score,
        period_start=period_start,
        period_end=period_end,
    )
    candidates, candidate_counts, deferred_counts = service._rebalance_items_by_source(
        items=list(candidates),
        limit=effective_limit,
    )
    service._record_stage_source_selection_metrics(
        run_id=run_id,
        stage="publish",
        candidate_counts=candidate_counts,
        deferred_counts=deferred_counts,
    )
    allow_tags = {
        tag.strip().lower() for tag in service.settings.allow_tags if tag.strip()
    }
    deny_tags = {
        tag.strip().lower() for tag in service.settings.deny_tags if tag.strip()
    }
    filtered_total = 0
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=service._progress_console,
    ) as progress:
        for item, analysis in progress.track(
            candidates, description="Publishing items"
        ):
            if item.id is None:
                continue
            telegram_already_sent = False
            if enable_telegram and destination_hash is not None:
                telegram_already_sent = service.repository.has_sent_delivery(
                    item_id=item.id,
                    channel=DELIVERY_CHANNEL_TELEGRAM,
                    destination=destination_hash,
                )
            if allow_tags or deny_tags:
                topics = {
                    tag.strip().lower()
                    for tag in service.repository.decode_list(analysis.topics_json)
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
                    vault_path = service.settings.obsidian_vault_path
                    if vault_path is None:
                        raise RuntimeError("obsidian vault path is not configured")
                    note_paths.append(
                        write_obsidian_note(
                            vault_path=vault_path,
                            base_folder=service.settings.obsidian_base_folder,
                            item_id=item.id,
                            title=item.title,
                            source=item.source,
                            canonical_url=item.canonical_url,
                            published_at=item.published_at,
                            authors=service.repository.decode_list(item.authors),
                            topics=service.repository.decode_list(analysis.topics_json),
                            relevance_score=analysis.relevance_score,
                            run_id=run_id,
                            summary=analysis.summary,
                        )
                    )
                if enable_markdown:
                    md_note_path = write_markdown_note(
                        output_dir=service.settings.markdown_output_dir,
                        item_id=item.id,
                        title=item.title,
                        source=item.source,
                        canonical_url=item.canonical_url,
                        published_at=item.published_at,
                        authors=service.repository.decode_list(item.authors),
                        topics=service.repository.decode_list(analysis.topics_json),
                        relevance_score=analysis.relevance_score,
                        run_id=run_id,
                        summary=analysis.summary,
                    )
                    markdown_notes.append((item.title, md_note_path))
                    note_paths.append(md_note_path)
                if (
                    enable_telegram
                    and destination_hash is not None
                    and not telegram_already_sent
                ):
                    message_text = build_telegram_message(
                        title=item.title,
                        summary=analysis.summary,
                        url=item.canonical_url,
                    )
                    if service.telegram_sender is None:
                        raise RuntimeError("telegram sender is not configured")
                    message_id = service.telegram_sender.send(message_text)
                    service.repository.upsert_delivery(
                        item_id=item.id,
                        channel=DELIVERY_CHANNEL_TELEGRAM,
                        destination=destination_hash,
                        message_id=message_id,
                        status=DELIVERY_STATUS_SENT,
                    )
                    telegram_already_sent = True
                service.repository.mark_item_published(item_id=item.id)
                publish_result.sent += 1
                publish_result.note_paths.extend(note_paths)
            except Exception as exc:
                sanitized_error = service._sanitize_error_message(str(exc))
                service._record_debug_artifact(
                    run_id=run_id,
                    item_id=item.id,
                    kind="error_context",
                    payload={
                        "stage": "publish",
                        "error_type": type(exc).__name__,
                        "error_message": sanitized_error,
                        "item_id": item.id,
                        **service._classify_exception(exc),
                    },
                    log=log.bind(item_id=item.id),
                    failure_message="Publish debug artifact record failed: {}",
                )
                if (
                    enable_telegram
                    and destination_hash is not None
                    and not telegram_already_sent
                ):
                    service.repository.upsert_delivery(
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
                output_dir=service.settings.markdown_output_dir,
                run_id=run_id,
                generated_at=utc_now(),
                notes=markdown_notes,
            )
        except Exception as exc:
            log.bind(module="pipeline.publish.markdown_index").warning(
                "Markdown index write failed: {}",
                service._sanitize_error_message(str(exc)),
            )

    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.publish.sent_total",
        value=publish_result.sent,
        unit="count",
    )
    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.publish.skipped_total",
        value=publish_result.skipped,
        unit="count",
    )
    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.publish.filtered_total",
        value=filtered_total,
        unit="count",
    )
    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.publish.failed_total",
        value=publish_result.failed,
        unit="count",
    )
    if remaining_today is not None:
        service.repository.record_metric(
            run_id=run_id,
            name="pipeline.publish.daily_cap_remaining",
            value=max(0, remaining_today - publish_result.sent),
            unit="count",
        )
    service.repository.record_metric(
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
