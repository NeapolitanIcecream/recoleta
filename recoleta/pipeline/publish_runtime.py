from __future__ import annotations

from dataclasses import dataclass
import time
from pathlib import Path
from typing import Any

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
from recoleta.publish import (
    build_telegram_message,
    write_markdown_note,
    write_markdown_run_index,
    write_obsidian_note,
)
from recoleta.types import PublishResult, utc_now


@dataclass(frozen=True, slots=True)
class PublishTargets:
    markdown: bool
    obsidian: bool
    telegram: bool


@dataclass(frozen=True, slots=True)
class PublishItemRequest:
    service: Any
    run_id: str
    item: Any
    analysis: Any
    targets: PublishTargets
    destination_hash: str | None
    markdown_notes: list[tuple[str, Path]]
    telegram_state: dict[str, bool]


@dataclass(frozen=True, slots=True)
class PublishFailureRequest:
    service: Any
    log: Any
    run_id: str
    item: Any
    exc: Exception
    targets: PublishTargets
    destination_hash: str | None
    telegram_already_sent: bool


@dataclass(frozen=True, slots=True)
class PublishMetricsRequest:
    service: Any
    run_id: str
    publish_result: PublishResult
    filtered_total: int
    remaining_today: int | None
    started: float


@dataclass(slots=True)
class PublishStageContext:
    service: Any
    run_id: str
    log: Any
    started: float
    publish_result: PublishResult
    targets: PublishTargets
    markdown_notes: list[tuple[str, Path]]
    destination_hash: str | None


def _resolve_publish_targets(*, service: Any) -> PublishTargets:
    targets = set(service.settings.publish_targets)
    return PublishTargets(
        markdown="markdown" in targets,
        obsidian="obsidian" in targets,
        telegram="telegram" in targets,
    )


def _initialize_telegram_delivery(
    *,
    service: Any,
    log: Any,
    targets: PublishTargets,
) -> tuple[str | None, int | None]:
    if not targets.telegram:
        return None, None
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
    destination_hash, sent_today, remaining_today = service._telegram_delivery_budget()
    if remaining_today <= 0:
        log.info(
            "Publish skipped: daily delivery cap reached sent_today={} cap={}",
            sent_today,
            service.settings.max_deliveries_per_day,
        )
    return destination_hash, remaining_today


def _load_publish_candidates(
    *,
    service: Any,
    run_id: str,
    limit: int,
    period_start: Any,
    period_end: Any,
) -> tuple[list[Any], int]:
    candidate_limit = service._stage_candidate_limit(limit=limit)
    candidates = service._invoke_repository_method(
        "list_items_for_publish",
        limit=candidate_limit,
        min_relevance_score=service.settings.min_relevance_score,
        period_start=period_start,
        period_end=period_end,
    )
    candidates, candidate_counts, deferred_counts = service._rebalance_items_by_source(
        items=list(candidates),
        limit=limit,
    )
    service._record_stage_source_selection_metrics(
        run_id=run_id,
        stage="publish",
        candidate_counts=candidate_counts,
        deferred_counts=deferred_counts,
    )
    return list(candidates), candidate_limit


def _decode_topics(*, service: Any, analysis: Any) -> set[str]:
    return {
        tag.strip().lower()
        for tag in service.repository.decode_list(analysis.topics_json)
        if tag.strip()
    }


def _should_skip_publish_item(
    *,
    service: Any,
    analysis: Any,
    allow_tags: set[str],
    deny_tags: set[str],
) -> bool:
    if not allow_tags and not deny_tags:
        return False
    topics = _decode_topics(service=service, analysis=analysis)
    if deny_tags and (topics & deny_tags):
        return True
    if allow_tags and not (topics & allow_tags):
        return True
    return False


def _write_publish_notes(
    request: PublishItemRequest,
) -> list[Path]:
    note_paths: list[Path] = []
    if request.targets.obsidian:
        vault_path = request.service.settings.obsidian_vault_path
        if vault_path is None:
            raise RuntimeError("obsidian vault path is not configured")
        note_paths.append(
            write_obsidian_note(
                vault_path=vault_path,
                base_folder=request.service.settings.obsidian_base_folder,
                item_id=request.item.id,
                title=request.item.title,
                source=request.item.source,
                canonical_url=request.item.canonical_url,
                published_at=request.item.published_at,
                authors=request.service.repository.decode_list(request.item.authors),
                topics=request.service.repository.decode_list(
                    request.analysis.topics_json
                ),
                relevance_score=request.analysis.relevance_score,
                run_id=request.run_id,
                summary=request.analysis.summary,
            )
        )
    if request.targets.markdown:
        md_note_path = write_markdown_note(
            output_dir=request.service.settings.markdown_output_dir,
            item_id=request.item.id,
            title=request.item.title,
            source=request.item.source,
            canonical_url=request.item.canonical_url,
            published_at=request.item.published_at,
            authors=request.service.repository.decode_list(request.item.authors),
            topics=request.service.repository.decode_list(request.analysis.topics_json),
            relevance_score=request.analysis.relevance_score,
            run_id=request.run_id,
            summary=request.analysis.summary,
        )
        request.markdown_notes.append((request.item.title, md_note_path))
        note_paths.append(md_note_path)
    return note_paths


def _send_publish_telegram(
    request: PublishItemRequest,
    telegram_already_sent: bool,
) -> bool:
    if (
        not request.targets.telegram
        or request.destination_hash is None
        or telegram_already_sent
    ):
        return telegram_already_sent
    message_text = build_telegram_message(
        title=request.item.title,
        summary=request.analysis.summary,
        url=request.item.canonical_url,
    )
    if request.service.telegram_sender is None:
        raise RuntimeError("telegram sender is not configured")
    message_id = request.service.telegram_sender.send(message_text)
    request.service.repository.upsert_delivery(
        item_id=request.item.id,
        channel=DELIVERY_CHANNEL_TELEGRAM,
        destination=request.destination_hash,
        message_id=message_id,
        status=DELIVERY_STATUS_SENT,
    )
    return True


def _record_publish_failure(request: PublishFailureRequest) -> None:
    sanitized_error = request.service._sanitize_error_message(str(request.exc))
    request.service._record_debug_artifact(
        run_id=request.run_id,
        item_id=request.item.id,
        kind="error_context",
        payload={
            "stage": "publish",
            "error_type": type(request.exc).__name__,
            "error_message": sanitized_error,
            "item_id": request.item.id,
            **request.service._classify_exception(request.exc),
        },
        log=request.log.bind(item_id=request.item.id),
        failure_message="Publish debug artifact record failed: {}",
    )
    if (
        request.targets.telegram
        and request.destination_hash is not None
        and not request.telegram_already_sent
    ):
        request.service.repository.upsert_delivery(
            item_id=request.item.id,
            channel=DELIVERY_CHANNEL_TELEGRAM,
            destination=request.destination_hash,
            message_id=None,
            status=DELIVERY_STATUS_FAILED,
            error=sanitized_error,
        )
    request.log.bind(item_id=request.item.id).warning(
        "Publish failed: {}", sanitized_error
    )


def _publish_single_item(request: PublishItemRequest) -> list[Path]:
    telegram_already_sent = bool(request.telegram_state.get("sent"))
    if request.targets.telegram and request.destination_hash is not None:
        telegram_already_sent = request.service.repository.has_sent_delivery(
            item_id=request.item.id,
            channel=DELIVERY_CHANNEL_TELEGRAM,
            destination=request.destination_hash,
        )
        request.telegram_state["sent"] = telegram_already_sent
    note_paths = _write_publish_notes(request)
    telegram_already_sent = _send_publish_telegram(request, telegram_already_sent)
    request.telegram_state["sent"] = telegram_already_sent
    request.service.repository.mark_item_published(item_id=request.item.id)
    return note_paths


def _write_markdown_index_if_enabled(
    *,
    service: Any,
    log: Any,
    enable_markdown: bool,
    run_id: str,
    markdown_notes: list[tuple[str, Path]],
) -> None:
    if not enable_markdown:
        return
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


def _record_publish_metrics(request: PublishMetricsRequest) -> None:
    request.service.repository.record_metric(
        run_id=request.run_id,
        name="pipeline.publish.sent_total",
        value=request.publish_result.sent,
        unit="count",
    )
    request.service.repository.record_metric(
        run_id=request.run_id,
        name="pipeline.publish.skipped_total",
        value=request.publish_result.skipped,
        unit="count",
    )
    request.service.repository.record_metric(
        run_id=request.run_id,
        name="pipeline.publish.filtered_total",
        value=request.filtered_total,
        unit="count",
    )
    request.service.repository.record_metric(
        run_id=request.run_id,
        name="pipeline.publish.failed_total",
        value=request.publish_result.failed,
        unit="count",
    )
    if request.remaining_today is not None:
        request.service.repository.record_metric(
            run_id=request.run_id,
            name="pipeline.publish.daily_cap_remaining",
            value=max(0, request.remaining_today - request.publish_result.sent),
            unit="count",
        )
    request.service.repository.record_metric(
        run_id=request.run_id,
        name="pipeline.publish.duration_ms",
        value=int((time.perf_counter() - request.started) * 1000),
        unit="ms",
    )


def execute_publish_stage(
    service: Any,
    *,
    run_id: str,
    limit: int = 50,
    period_start: Any = None,
    period_end: Any = None,
) -> PublishResult:
    targets = _resolve_publish_targets(service=service)
    if targets.obsidian and service.settings.obsidian_vault_path is None:
        raise ValueError(
            "OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'"
        )
    context = PublishStageContext(
        service=service,
        run_id=run_id,
        log=logger.bind(module="pipeline.publish", run_id=run_id),
        started=time.perf_counter(),
        publish_result=PublishResult(),
        targets=targets,
        markdown_notes=[],
        destination_hash=None,
    )
    destination_hash, remaining_today = _initialize_telegram_delivery(
        service=service,
        log=context.log,
        targets=targets,
    )
    context.destination_hash = destination_hash
    effective_limit = (
        min(limit, remaining_today) if remaining_today is not None else limit
    )
    candidates, _ = _load_publish_candidates(
        service=service,
        run_id=run_id,
        limit=effective_limit,
        period_start=period_start,
        period_end=period_end,
    )
    allow_tags = {
        tag.strip().lower() for tag in service.settings.allow_tags if tag.strip()
    }
    deny_tags = {
        tag.strip().lower() for tag in service.settings.deny_tags if tag.strip()
    }
    filtered_total = _publish_candidate_loop(
        context=context,
        candidates=candidates,
        allow_tags=allow_tags,
        deny_tags=deny_tags,
    )
    _write_markdown_index_if_enabled(
        service=service,
        log=context.log,
        enable_markdown=targets.markdown,
        run_id=run_id,
        markdown_notes=context.markdown_notes,
    )
    _record_publish_metrics(
        PublishMetricsRequest(
            service=service,
            run_id=run_id,
            publish_result=context.publish_result,
            filtered_total=filtered_total,
            remaining_today=remaining_today,
            started=context.started,
        )
    )
    context.log.info(
        "Publish completed with sent={} skipped={} failed={}",
        context.publish_result.sent,
        context.publish_result.skipped,
        context.publish_result.failed,
    )
    return context.publish_result


def _publish_candidate_loop(
    *,
    context: PublishStageContext,
    candidates: list[Any],
    allow_tags: set[str],
    deny_tags: set[str],
) -> int:
    filtered_total = 0
    with Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        console=context.service._progress_console,
    ) as progress:
        for item, analysis in progress.track(
            candidates, description="Publishing items"
        ):
            if item.id is None:
                continue
            if _should_skip_publish_item(
                service=context.service,
                analysis=analysis,
                allow_tags=allow_tags,
                deny_tags=deny_tags,
            ):
                context.publish_result.skipped += 1
                filtered_total += 1
                continue
            telegram_state = {"sent": False}
            try:
                note_paths = _publish_single_item(
                    PublishItemRequest(
                        service=context.service,
                        run_id=context.run_id,
                        item=item,
                        analysis=analysis,
                        targets=context.targets,
                        destination_hash=context.destination_hash,
                        markdown_notes=context.markdown_notes,
                        telegram_state=telegram_state,
                    )
                )
                context.publish_result.sent += 1
                context.publish_result.note_paths.extend(note_paths)
            except Exception as exc:  # noqa: BLE001
                context.publish_result.failed += 1
                _record_publish_failure(
                    PublishFailureRequest(
                        service=context.service,
                        log=context.log,
                        run_id=context.run_id,
                        item=item,
                        exc=exc,
                        targets=context.targets,
                        destination_hash=context.destination_hash,
                        telegram_already_sent=bool(telegram_state.get("sent")),
                    )
                )
    return filtered_total
