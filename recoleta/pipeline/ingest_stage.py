from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol

from loguru import logger
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta import sources
from recoleta.types import IngestResult, ItemDraft


@dataclass(slots=True, frozen=True)
class IngestStageRequest:
    run_id: str
    drafts: list[ItemDraft] | None = None
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(slots=True, frozen=True)
class SourcePullStageRequest:
    run_id: str
    log: Any
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(slots=True, frozen=True)
class RebalanceItemsRequest:
    items: list[Any]
    limit: int


class IngestStageService(Protocol):
    repository: Any
    settings: Any
    _progress_console: Any

    @staticmethod
    def _empty_source_pull_stats() -> dict[str, dict[str, int]]: ...

    @staticmethod
    def _invoke_source_pull(fn: Any, **kwargs: Any) -> Any: ...

    @staticmethod
    def _normalize_source_pull_result(raw: Any) -> sources.SourcePullResult: ...

    def _pull_source_drafts(
        self,
        *,
        request: SourcePullStageRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]: ...

    def _lookup_source_pull_state(
        self,
        *,
        source: str,
        scope_kind: str,
        scope_key: str,
    ) -> sources.SourcePullStateSnapshot | None: ...

    def _persist_source_pull_state_updates(
        self,
        *,
        source: str,
        updates: list[sources.SourcePullStateUpdate],
    ) -> None: ...

    def _sanitize_error_message(self, message: str) -> str: ...

    def _record_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
        log: Any,
        failure_message: str,
    ) -> Any: ...

    @staticmethod
    def _classify_exception(exc: BaseException) -> dict[str, Any]: ...


def run_ingest_stage(
    service: IngestStageService,
    request: IngestStageRequest,
) -> IngestResult:
    return _IngestStageRunner(service=service, request=request).run()


def pull_source_drafts(
    service: IngestStageService,
    request: SourcePullStageRequest,
) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]:
    return _SourcePullRunner(service=service, request=request).run()


def rebalance_items_by_source(
    request: RebalanceItemsRequest,
) -> tuple[list[Any], dict[str, int], dict[str, int]]:
    normalized_limit = max(0, int(request.limit))
    if normalized_limit <= 0 or not request.items:
        return [], {}, {}
    queues, source_order = _items_by_source(request.items)
    candidate_counts = {
        source_name: len(queue) for source_name, queue in queues.items()
    }
    selected = _round_robin_selection(
        queues=queues,
        source_order=source_order,
        limit=normalized_limit,
    )
    deferred_counts = {
        source_name: len(queue) for source_name, queue in queues.items() if queue
    }
    return selected, candidate_counts, deferred_counts


def _items_by_source(items: list[Any]) -> tuple[dict[str, deque[Any]], list[str]]:
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
    return queues, source_order


def _round_robin_selection(
    *,
    queues: dict[str, deque[Any]],
    source_order: list[str],
    limit: int,
) -> list[Any]:
    selected: list[Any] = []
    while len(selected) < limit:
        progressed = False
        for source_name in source_order:
            queue = queues[source_name]
            if not queue:
                continue
            selected.append(queue.popleft())
            progressed = True
            if len(selected) >= limit:
                break
        if not progressed:
            break
    return selected


class _IngestStageRunner:
    def __init__(
        self, *, service: IngestStageService, request: IngestStageRequest
    ) -> None:
        self.service = service
        self.request = request
        self.log = logger.bind(module="pipeline.ingest", run_id=request.run_id)
        self.started = time.perf_counter()
        self.result = IngestResult()
        self.source_failures_total = 0
        self.source_stats = service._empty_source_pull_stats()
        self.source_drafts = request.drafts

    def run(self) -> IngestResult:
        with _pipeline_progress()(
            TextColumn("{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            console=self.service._progress_console,
        ) as progress:
            task_id = progress.add_task("Ingesting items", total=None)
            self._load_source_drafts()
            drafts = self.source_drafts or []
            progress.update(task_id, total=len(drafts), completed=0)
            for draft in drafts:
                self._ingest_draft(draft)
                progress.advance(task_id, advance=1)
        self._record_metrics()
        return self.result

    def _load_source_drafts(self) -> None:
        if self.source_drafts is None:
            self.source_drafts, self.source_failures_total, self.source_stats = (
                self.service._pull_source_drafts(
                    request=SourcePullStageRequest(
                        run_id=self.request.run_id,
                        log=self.log,
                        period_start=self.request.period_start,
                        period_end=self.request.period_end,
                    )
                )
            )
            return
        for draft in self.source_drafts or []:
            bucket = _ensure_source_pull_bucket(
                self.source_stats, str(draft.source or "")
            )
            bucket["drafts_total"] += 1

    def _ingest_draft(self, draft: ItemDraft) -> None:
        try:
            _, created = self.service.repository.upsert_item(draft)
        except Exception as exc:
            self._record_ingest_failure(draft=draft, exc=exc)
            return
        bucket = _ensure_source_pull_bucket(self.source_stats, str(draft.source or ""))
        if created:
            self.result.inserted += 1
            bucket["inserted_total"] += 1
            return
        self.result.updated += 1
        bucket["updated_total"] += 1

    def _record_ingest_failure(self, *, draft: ItemDraft, exc: Exception) -> None:
        self.result.failed += 1
        sanitized_error = self.service._sanitize_error_message(str(exc))
        self.service._record_debug_artifact(
            run_id=self.request.run_id,
            item_id=None,
            kind="error_context",
            payload={
                "stage": "ingest",
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                **self.service._classify_exception(exc),
                "draft": {
                    "source": draft.source,
                    "source_item_id": draft.source_item_id,
                    "canonical_url_hash": draft.canonical_url_hash,
                },
            },
            log=self.log,
            failure_message="Ingest debug artifact record failed: {}",
        )
        self.log.bind(item_hash=draft.canonical_url_hash).warning(
            "Ingest failed: {}", sanitized_error
        )

    def _record_metrics(self) -> None:
        run_id = self.request.run_id
        repository = self.service.repository
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.items_total",
            value=self.result.inserted + self.result.updated + self.result.failed,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.inserted_total",
            value=self.result.inserted,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.updated_total",
            value=self.result.updated,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.failed_total",
            value=self.result.failed,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.source_failures_total",
            value=self.source_failures_total,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.ingest.duration_ms",
            value=int((time.perf_counter() - self.started) * 1000),
            unit="ms",
        )
        for source_name in sorted(self.source_stats):
            _record_source_pull_metrics(
                repository=repository,
                run_id=run_id,
                source_name=source_name,
                bucket=self.source_stats[source_name],
            )


class _SourcePullRunner:
    def __init__(
        self, *, service: IngestStageService, request: SourcePullStageRequest
    ) -> None:
        self.service = service
        self.request = request
        self.drafts: list[ItemDraft] = []
        self.source_failures_total = 0
        self.source_stats = service._empty_source_pull_stats()

    def run(self) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]:
        for source_name, fn, source_request, legacy_kwargs in self._configured_pulls():
            self._pull_source(
                source_name=source_name,
                fn=fn,
                source_request=source_request,
                legacy_kwargs=legacy_kwargs,
            )
        return self.drafts, self.source_failures_total, self.source_stats

    def _configured_pulls(self) -> list[tuple[str, Any, Any, dict[str, Any]]]:
        configured: list[tuple[str, Any, Any, dict[str, Any]]] = []
        for configured_pull in (
            self._hf_daily_pull(),
            self._hn_pull(),
            self._rss_pull(),
            self._arxiv_pull(),
            self._openreview_pull(),
        ):
            if configured_pull is not None:
                configured.append(configured_pull)
        return configured

    def _hf_daily_pull(self) -> tuple[str, Any, Any, dict[str, Any]] | None:
        settings = self.service.settings.sources.hf_daily
        if not settings.enabled:
            return None
        source_request = sources.HFDailyPapersPullRequest(
            max_items=settings.max_items_per_run,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            pull_state_lookup=self._pull_state_lookup("hf_daily"),
            include_stats=True,
        )
        return (
            "hf_daily",
            sources.fetch_hf_daily_papers_drafts,
            source_request,
            {
                "max_items": source_request.max_items,
                "period_start": source_request.period_start,
                "period_end": source_request.period_end,
                "pull_state_lookup": source_request.pull_state_lookup,
                "include_stats": source_request.include_stats,
            },
        )

    def _hn_pull(self) -> tuple[str, Any, Any, dict[str, Any]] | None:
        settings = self.service.settings.sources.hn
        hn_urls = _deduped_values(settings.rss_urls) if settings.enabled else []
        if not hn_urls:
            return None
        source_request = sources.HNPullRequest(
            feed_urls=hn_urls,
            max_items_per_feed=settings.max_items_per_feed,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            max_total_items=settings.max_total_per_run,
            pull_state_lookup=self._pull_state_lookup("hn"),
            include_stats=True,
        )
        return (
            "hn",
            sources.fetch_hn_drafts,
            source_request,
            {
                "feed_urls": source_request.feed_urls,
                "max_items_per_feed": source_request.max_items_per_feed,
                "period_start": source_request.period_start,
                "period_end": source_request.period_end,
                "max_total_items": source_request.max_total_items,
                "pull_state_lookup": source_request.pull_state_lookup,
                "include_stats": source_request.include_stats,
            },
        )

    def _rss_pull(self) -> tuple[str, Any, Any, dict[str, Any]] | None:
        settings = self.service.settings.sources.rss
        rss_urls = _deduped_values(settings.feeds) if settings.enabled else []
        if not rss_urls:
            return None
        source_request = sources.FeedPullRequest(
            feed_urls=rss_urls,
            source="rss",
            max_items_per_feed=settings.max_items_per_feed,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            max_total_items=settings.max_total_per_run,
            pull_state_lookup=self._pull_state_lookup("rss"),
            include_stats=True,
        )
        return (
            "rss",
            sources.fetch_rss_drafts,
            source_request,
            {
                "feed_urls": source_request.feed_urls,
                "source": source_request.source,
                "max_items_per_feed": source_request.max_items_per_feed,
                "period_start": source_request.period_start,
                "period_end": source_request.period_end,
                "max_total_items": source_request.max_total_items,
                "pull_state_lookup": source_request.pull_state_lookup,
                "include_stats": source_request.include_stats,
            },
        )

    def _arxiv_pull(self) -> tuple[str, Any, Any, dict[str, Any]] | None:
        settings = self.service.settings.sources.arxiv
        arxiv_queries = _deduped_values(settings.queries) if settings.enabled else []
        if not arxiv_queries:
            return None
        source_request = sources.ArxivPullRequest(
            queries=arxiv_queries,
            max_results_per_run=settings.max_results_per_run,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            max_total_items=settings.max_total_per_run,
            pull_state_lookup=self._pull_state_lookup("arxiv"),
            include_stats=True,
        )
        return (
            "arxiv",
            sources.fetch_arxiv_drafts,
            source_request,
            {
                "queries": source_request.queries,
                "max_results_per_run": source_request.max_results_per_run,
                "period_start": source_request.period_start,
                "period_end": source_request.period_end,
                "max_total_items": source_request.max_total_items,
                "pull_state_lookup": source_request.pull_state_lookup,
                "include_stats": source_request.include_stats,
            },
        )

    def _openreview_pull(self) -> tuple[str, Any, Any, dict[str, Any]] | None:
        settings = self.service.settings.sources.openreview
        openreview_venues = _deduped_values(settings.venues) if settings.enabled else []
        if not openreview_venues:
            return None
        source_request = sources.OpenReviewPullRequest(
            venues=openreview_venues,
            max_results_per_venue=settings.max_results_per_venue,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            max_total_items=settings.max_total_per_run,
            pull_state_lookup=self._pull_state_lookup("openreview"),
            include_stats=True,
        )
        return (
            "openreview",
            sources.fetch_openreview_drafts,
            source_request,
            {
                "venues": source_request.venues,
                "max_results_per_venue": source_request.max_results_per_venue,
                "period_start": source_request.period_start,
                "period_end": source_request.period_end,
                "max_total_items": source_request.max_total_items,
                "pull_state_lookup": source_request.pull_state_lookup,
                "include_stats": source_request.include_stats,
            },
        )

    def _pull_source(
        self,
        *,
        source_name: str,
        fn: Any,
        source_request: Any,
        legacy_kwargs: dict[str, Any],
    ) -> None:
        started = time.perf_counter()
        bucket = _ensure_source_pull_bucket(self.source_stats, source_name)
        try:
            raw_result = self.service._invoke_source_pull(
                fn,
                request=source_request,
                **legacy_kwargs,
            )
            pull_result = self.service._normalize_source_pull_result(raw_result)
            self._merge_pull_result(
                source_name=source_name, bucket=bucket, pull_result=pull_result
            )
        except Exception as exc:
            self._record_pull_failure(source_name=source_name, bucket=bucket, exc=exc)
        finally:
            bucket["pull_duration_ms"] += int((time.perf_counter() - started) * 1000)

    def _merge_pull_result(
        self,
        *,
        source_name: str,
        bucket: dict[str, int],
        pull_result: sources.SourcePullResult,
    ) -> None:
        self.drafts.extend(pull_result.drafts)
        bucket["drafts_total"] += len(pull_result.drafts)
        bucket["filtered_out_total"] += int(pull_result.filtered_out_total or 0)
        bucket["in_window_total"] += int(pull_result.in_window_total or 0)
        bucket["missing_published_at_total"] += int(
            pull_result.missing_published_at_total or 0
        )
        bucket["deduped_total"] += int(pull_result.deduped_total or 0)
        bucket["deferred_total"] += int(pull_result.deferred_total or 0)
        bucket["not_modified_total"] += int(pull_result.not_modified_total or 0)
        _merge_published_at_bucket(
            bucket=bucket,
            oldest=pull_result.oldest_published_at,
            newest=pull_result.newest_published_at,
        )
        self.service._persist_source_pull_state_updates(
            source=source_name,
            updates=list(pull_result.state_updates),
        )

    def _record_pull_failure(
        self,
        *,
        source_name: str,
        bucket: dict[str, int],
        exc: Exception,
    ) -> None:
        self.source_failures_total += 1
        bucket["pull_failed_total"] += 1
        sanitized_error = self.service._sanitize_error_message(str(exc))
        self.service._record_debug_artifact(
            run_id=self.request.run_id,
            item_id=None,
            kind="error_context",
            payload={
                "stage": "ingest",
                "source": source_name,
                "error_type": type(exc).__name__,
                "error_message": sanitized_error,
                **self.service._classify_exception(exc),
            },
            log=self.request.log.bind(source=source_name),
            failure_message="Ingest source debug artifact record failed: {}",
        )
        self.request.log.bind(source=source_name).warning(
            "Source pull failed: {}", sanitized_error
        )

    def _pull_state_lookup(self, source_name: str) -> sources.PullStateLookup:
        return lambda scope_kind, scope_key: self.service._lookup_source_pull_state(
            source=source_name,
            scope_kind=scope_kind,
            scope_key=scope_key,
        )


def _deduped_values(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _pipeline_progress() -> type[Progress]:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.Progress


def _ensure_source_pull_bucket(
    source_stats: dict[str, dict[str, int]],
    source_name: str,
) -> dict[str, int]:
    normalized = str(source_name or "").strip().lower()
    if not normalized:
        normalized = "unknown"
    bucket = source_stats.get(normalized)
    if bucket is None:
        bucket = {
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
        source_stats[normalized] = bucket
    return bucket


def _merge_published_at_bucket(
    *,
    bucket: dict[str, int],
    oldest: datetime | None,
    newest: datetime | None,
) -> None:
    if oldest is not None:
        candidate_oldest = int(oldest.timestamp())
        current_oldest = int(bucket.get("oldest_published_at_unix") or 0)
        if current_oldest <= 0 or candidate_oldest < current_oldest:
            bucket["oldest_published_at_unix"] = candidate_oldest
    if newest is not None:
        candidate_newest = int(newest.timestamp())
        current_newest = int(bucket.get("newest_published_at_unix") or 0)
        if candidate_newest > current_newest:
            bucket["newest_published_at_unix"] = candidate_newest


def _record_source_pull_metrics(
    *,
    repository: Any,
    run_id: str,
    source_name: str,
    bucket: dict[str, int],
) -> None:
    metric_names = (
        ("drafts_total", "count"),
        ("pull_failed_total", "count"),
        ("pull_duration_ms", "ms"),
        ("filtered_out_total", "count"),
        ("in_window_total", "count"),
        ("missing_published_at_total", "count"),
        ("deduped_total", "count"),
        ("deferred_total", "count"),
        ("not_modified_total", "count"),
        ("inserted_total", "count"),
        ("updated_total", "count"),
    )
    for key, unit in metric_names:
        repository.record_metric(
            run_id=run_id,
            name=f"pipeline.ingest.source.{source_name}.{key}",
            value=int(bucket.get(key) or 0),
            unit=unit,
        )
    _record_source_published_at_metric(
        repository=repository,
        run_id=run_id,
        source_name=source_name,
        bucket=bucket,
        key="oldest_published_at_unix",
    )
    _record_source_published_at_metric(
        repository=repository,
        run_id=run_id,
        source_name=source_name,
        bucket=bucket,
        key="newest_published_at_unix",
    )


def _record_source_published_at_metric(
    *,
    repository: Any,
    run_id: str,
    source_name: str,
    bucket: dict[str, int],
    key: str,
) -> None:
    value = int(bucket.get(key) or 0)
    if value <= 0:
        return
    repository.record_metric(
        run_id=run_id,
        name=f"pipeline.ingest.source.{source_name}.{key}",
        value=value,
        unit="unix",
    )
