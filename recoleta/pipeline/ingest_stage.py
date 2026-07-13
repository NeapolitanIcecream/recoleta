from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Protocol

from loguru import logger
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta import sources
from recoleta.types import IngestResult, ItemDraft, MetricPoint


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


_SourcePullRequest = (
    sources.HFDailyPapersPullRequest
    | sources.HNPullRequest
    | sources.FeedPullRequest
    | sources.ArxivPullRequest
    | sources.OpenReviewPullRequest
)
_SourcePullFetcher = Callable[..., list[ItemDraft] | sources.SourcePullResult]
_NO_POOL_BACKEND = object()
_SOURCE_NAMES = ("arxiv", "hn", "hf_daily", "openreview", "rss")


@dataclass(slots=True, frozen=True)
class _ConfiguredSourcePull:
    source_name: str
    fetcher: _SourcePullFetcher
    request: _SourcePullRequest
    pool_backend: Any = _NO_POOL_BACKEND


class IngestStageService(Protocol):
    repository: Any
    settings: Any
    _progress_console: Any

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

    def _merge_run_source_diagnostics(
        self,
        *,
        run_id: str,
        diagnostics: list[dict[str, Any]],
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

    def _record_metrics_batch(
        self, *, run_id: str, metrics: list[MetricPoint]
    ) -> int: ...


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
        self.source_stats = _empty_source_pull_stats()
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
                pull_source_drafts(
                    self.service,
                    SourcePullStageRequest(
                        run_id=self.request.run_id,
                        log=self.log,
                        period_start=self.request.period_start,
                        period_end=self.request.period_end,
                    ),
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
        metrics = [
            MetricPoint(
                name="pipeline.ingest.items_total",
                value=self.result.inserted + self.result.updated + self.result.failed,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.ingest.inserted_total",
                value=self.result.inserted,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.ingest.updated_total",
                value=self.result.updated,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.ingest.failed_total",
                value=self.result.failed,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.ingest.source_failures_total",
                value=self.source_failures_total,
                unit="count",
            ),
            MetricPoint(
                name="pipeline.ingest.duration_ms",
                value=int((time.perf_counter() - self.started) * 1000),
                unit="ms",
            ),
        ]
        for source_name in sorted(self.source_stats):
            metrics.extend(
                _source_pull_metric_points(
                    source_name=source_name,
                    bucket=self.source_stats[source_name],
                )
            )
        self.service._record_metrics_batch(run_id=run_id, metrics=metrics)


class _SourcePullRunner:
    def __init__(
        self, *, service: IngestStageService, request: SourcePullStageRequest
    ) -> None:
        self.service = service
        self.request = request
        self.drafts: list[ItemDraft] = []
        self.source_failures_total = 0
        self.source_stats = _empty_source_pull_stats()

    def run(self) -> tuple[list[ItemDraft], int, dict[str, dict[str, int]]]:
        for configured_pull in self._configured_pulls():
            self._pull_source(configured_pull)
        return self.drafts, self.source_failures_total, self.source_stats

    def _configured_pulls(self) -> list[_ConfiguredSourcePull]:
        configured: list[_ConfiguredSourcePull] = []
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

    def _hf_daily_pull(self) -> _ConfiguredSourcePull | None:
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
        return _ConfiguredSourcePull(
            source_name="hf_daily",
            fetcher=sources.fetch_hf_daily_papers_drafts,
            request=source_request,
        )

    def _hn_pull(self) -> _ConfiguredSourcePull | None:
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
        return _ConfiguredSourcePull(
            source_name="hn",
            fetcher=sources.fetch_hn_drafts,
            request=source_request,
        )

    def _rss_pull(self) -> _ConfiguredSourcePull | None:
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
        return _ConfiguredSourcePull(
            source_name="rss",
            fetcher=sources.fetch_rss_drafts,
            request=source_request,
        )

    def _arxiv_pull(self) -> _ConfiguredSourcePull | None:
        settings = self.service.settings.sources.arxiv
        arxiv_queries = _deduped_values(settings.queries) if settings.enabled else []
        if not arxiv_queries:
            return None
        mode = str(getattr(settings, "mode", "direct") or "direct").strip().lower()
        pool_db_path = None
        pool_backend = None
        if mode == "pool":
            from recoleta.arxiv_pool import (
                arxiv_pool_backend_descriptor_from_settings,
                build_arxiv_pool_backend_from_settings,
                resolve_arxiv_pool_db_path,
            )

            pool_backend = build_arxiv_pool_backend_from_settings(self.service.settings)
            if (
                arxiv_pool_backend_descriptor_from_settings(self.service.settings).kind
                == "local_sqlite"
            ):
                pool_db_path = resolve_arxiv_pool_db_path(self.service.settings)
        pool_settings = self.service.settings.arxiv_pool
        source_request = sources.ArxivPullRequest(
            queries=arxiv_queries,
            max_results_per_run=settings.max_results_per_run,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
            max_total_items=settings.max_total_per_run,
            pull_state_lookup=self._pull_state_lookup("arxiv"),
            include_stats=True,
            mode=mode,
            pool_db_path=pool_db_path,
            pool_maturity_lag_days=int(pool_settings.maturity_lag_days),
            pool_readiness_gate=str(pool_settings.readiness_gate),
            pool_allow_immature_windows=bool(pool_settings.allow_immature_windows),
        )
        return _ConfiguredSourcePull(
            source_name="arxiv",
            fetcher=sources.fetch_arxiv_drafts,
            request=source_request,
            pool_backend=pool_backend,
        )

    def _openreview_pull(self) -> _ConfiguredSourcePull | None:
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
        return _ConfiguredSourcePull(
            source_name="openreview",
            fetcher=sources.fetch_openreview_drafts,
            request=source_request,
        )

    def _pull_source(self, configured_pull: _ConfiguredSourcePull) -> None:
        source_name = configured_pull.source_name
        started = time.perf_counter()
        bucket = _ensure_source_pull_bucket(self.source_stats, source_name)
        try:
            if configured_pull.pool_backend is _NO_POOL_BACKEND:
                raw_result = configured_pull.fetcher(request=configured_pull.request)
            else:
                raw_result = configured_pull.fetcher(
                    request=configured_pull.request,
                    pool_backend=configured_pull.pool_backend,
                )
            pull_result = _normalize_source_pull_result(raw_result)
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
        for key, value in pull_result.extra_metrics.items():
            if _safe_source_metric_key(key):
                bucket[key] = int(bucket.get(key) or 0) + int(value or 0)
        if pull_result.diagnostics:
            self.service._merge_run_source_diagnostics(
                run_id=self.request.run_id,
                diagnostics=list(pull_result.diagnostics),
            )
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


def _empty_source_pull_stats() -> dict[str, dict[str, int]]:
    return {source_name: _new_source_pull_bucket() for source_name in _SOURCE_NAMES}


def _normalize_source_pull_result(raw: Any) -> sources.SourcePullResult:
    if isinstance(raw, sources.SourcePullResult):
        return raw
    if raw is None:
        return sources.SourcePullResult()
    return sources.SourcePullResult(drafts=list(raw))


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
        bucket = _new_source_pull_bucket()
        source_stats[normalized] = bucket
    return bucket


def _new_source_pull_bucket() -> dict[str, int]:
    return {
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
        "pool_drafts_total": 0,
        "pool_window_unavailable_total": 0,
        "pool_window_immature_total": 0,
        "pool_window_immature_allowed_total": 0,
        "pool_window_analysis_ready_total": 0,
    }


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


def _source_pull_metric_points(
    *,
    source_name: str,
    bucket: dict[str, int],
) -> list[MetricPoint]:
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
        ("pool_drafts_total", "count"),
        ("pool_window_unavailable_total", "count"),
        ("pool_window_immature_total", "count"),
        ("pool_window_immature_allowed_total", "count"),
        ("pool_window_analysis_ready_total", "count"),
    )
    metrics = [
        MetricPoint(
            name=f"pipeline.ingest.source.{source_name}.{key}",
            value=int(bucket.get(key) or 0),
            unit=unit,
        )
        for key, unit in metric_names
    ]
    for key in ("oldest_published_at_unix", "newest_published_at_unix"):
        value = int(bucket.get(key) or 0)
        if value > 0:
            metrics.append(
                MetricPoint(
                    name=f"pipeline.ingest.source.{source_name}.{key}",
                    value=value,
                    unit="unix",
                )
            )
    return metrics


def _safe_source_metric_key(value: str) -> bool:
    normalized = str(value or "").strip()
    if not normalized:
        return False
    return all(ch.islower() or ch.isdigit() or ch == "_" for ch in normalized)
