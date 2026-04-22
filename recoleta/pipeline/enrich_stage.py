from __future__ import annotations

import hashlib
import threading
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Protocol, cast

import httpx
from loguru import logger
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)

from recoleta.pipeline.ingest_stage import RebalanceItemsRequest

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


@dataclass(slots=True, frozen=True)
class EnrichStageRequest:
    run_id: str
    limit: int
    period_start: datetime | None = None
    period_end: datetime | None = None


@dataclass(slots=True, frozen=True)
class ItemContentRequest:
    client: httpx.Client
    item: Any
    log: Any
    diag: dict[str, Any] | None = None
    arxiv_html_throttle: Callable[[], None] | None = None


@dataclass(slots=True, frozen=True)
class ArxivContentRequest:
    client: httpx.Client
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None = None
    arxiv_html_throttle: Callable[[], None] | None = None


@dataclass(slots=True, frozen=True)
class ArxivHtmlDocumentRequest:
    client: httpx.Client
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None = None
    arxiv_html_throttle: Callable[[], None] | None = None


@dataclass(slots=True, frozen=True)
class PdfContentRequest:
    client: httpx.Client
    source: str
    item_id: int
    canonical_url: str
    source_item_id: str | None
    log: Any
    diag: dict[str, Any] | None = None


@dataclass(slots=True, frozen=True)
class _ConsumeResultRequest:
    result: dict[str, Any]
    item_elapsed_ms: int
    include_debug: bool
    write_and_record_artifact: Callable[..., None]
    log: Any


@dataclass(slots=True)
class _ParallelRunState:
    local: threading.local
    created_clients: list[httpx.Client]
    created_lock: threading.Lock


@dataclass(slots=True, frozen=True)
class _RunnerConsumeRequest:
    stats: Any
    progress: Any
    task_id: int
    result: dict[str, Any]
    item_elapsed_ms: int


class EnrichStageService(Protocol):
    repository: Any
    settings: Any
    _progress_console: Any

    @staticmethod
    def _new_source_enrich_bucket() -> dict[str, Any]: ...

    def _invoke_repository_method(self, method_name: str, /, **kwargs: Any) -> Any: ...

    def _stage_candidate_limit(self, *, limit: int) -> int: ...

    @staticmethod
    def _rebalance_items_by_source(
        *,
        request: RebalanceItemsRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[list[Any], dict[str, int], dict[str, int]]: ...

    def _record_stage_source_selection_metrics(
        self,
        *,
        run_id: str,
        stage: str,
        candidate_counts: dict[str, int],
        deferred_counts: dict[str, int],
    ) -> None: ...

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

    def _sanitize_error_message(self, message: str) -> str: ...

    def _ensure_item_content(
        self,
        *,
        request: ItemContentRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[str, bool]: ...

    def _ensure_arxiv_content(
        self,
        *,
        request: ArxivContentRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[str, bool]: ...

    def _ensure_pdf_content(
        self,
        *,
        request: PdfContentRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[str, bool]: ...

    def _ensure_arxiv_html_document_content(
        self,
        *,
        request: ArxivHtmlDocumentRequest | None = None,
        **legacy_kwargs: Any,
    ) -> tuple[str, bool]: ...

    def _ensure_html_maintext_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        diag: dict[str, Any] | None = None,
    ) -> tuple[str, bool]: ...

    def _ensure_arxiv_latex_source_content(
        self,
        *,
        client: httpx.Client,
        item_id: int,
        canonical_url: str,
        source_item_id: str | None,
        diag: dict[str, Any] | None = None,
    ) -> tuple[str, bool]: ...

    def _annotate_content_diag(
        self,
        diag: dict[str, Any] | None,
        *,
        content_type: str,
        content_text: str,
        pdf_backend: str | None = None,
    ) -> None: ...

    def _get_latest_content_text(
        self,
        *,
        item_id: int,
        content_type: str,
    ) -> str | None: ...

    def _log_html_document_md_conversion_skipped(
        self,
        *,
        log: Any,
        item_id: int,
        elapsed_ms: int,
        error: str | None,
    ) -> None: ...

    @staticmethod
    def _classify_arxiv_html_document_fallback_reason(exc: BaseException) -> str: ...

    @staticmethod
    def _build_pdf_url(
        *,
        source: str,
        canonical_url: str,
        source_item_id: str | None,
    ) -> str | None: ...

    @staticmethod
    def _build_arxiv_source_url(
        *,
        canonical_url: str,
        source_item_id: str | None,
    ) -> str | None: ...

    @staticmethod
    def _build_arxiv_html_url(
        *,
        canonical_url: str,
        source_item_id: str | None,
    ) -> str | None: ...


def run_enrich_stage(service: EnrichStageService, request: EnrichStageRequest) -> None:
    _EnrichStageRunner(service=service, request=request).run()


def ensure_item_content(
    service: EnrichStageService,
    request: ItemContentRequest,
) -> tuple[str, bool]:
    raw_item_id = getattr(request.item, "id", None)
    if raw_item_id is None:
        raise ValueError("item id is required for enrichment")
    item_id = int(raw_item_id)
    source = str(getattr(request.item, "source", "") or "").strip().lower()
    canonical_url = str(getattr(request.item, "canonical_url", "") or "")
    source_item_id = getattr(request.item, "source_item_id", None)

    if source == "arxiv":
        content_text, stored_new_content = service._ensure_arxiv_content(
            request=ArxivContentRequest(
                client=request.client,
                item_id=item_id,
                canonical_url=canonical_url,
                source_item_id=source_item_id,
                log=request.log,
                diag=request.diag,
                arxiv_html_throttle=request.arxiv_html_throttle,
            )
        )
    elif source == "openreview":
        content_text, stored_new_content = ensure_pdf_content(
            service,
            PdfContentRequest(
                client=request.client,
                source=source,
                item_id=item_id,
                canonical_url=canonical_url,
                source_item_id=source_item_id,
                log=request.log,
                diag=request.diag,
            ),
        )
    else:
        content_text, stored_new_content = service._ensure_html_maintext_content(
            client=request.client,
            item_id=item_id,
            canonical_url=canonical_url,
            diag=request.diag,
        )

    if not content_text.strip():
        raise RuntimeError("empty enriched content")
    return content_text, stored_new_content


def ensure_arxiv_content(
    service: EnrichStageService,
    request: ArxivContentRequest,
) -> tuple[str, bool]:
    method = service.settings.sources.arxiv.enrich_method
    if method == "pdf_text":
        return _fallback_to_arxiv_pdf(service, request)

    if method == "latex_source":
        return _ensure_arxiv_latex_mode(service, request, method)

    if method == "html_document":
        return _ensure_arxiv_html_document_mode(service, request, method)

    raise ValueError(f"Unsupported arXiv enrich_method: {method}")


def _fallback_to_arxiv_pdf(
    service: EnrichStageService,
    request: ArxivContentRequest,
) -> tuple[str, bool]:
    return service._ensure_pdf_content(
        request=PdfContentRequest(
            client=request.client,
            source="arxiv",
            item_id=request.item_id,
            canonical_url=request.canonical_url,
            source_item_id=request.source_item_id,
            log=request.log,
            diag=request.diag,
        )
    )


def _ensure_arxiv_latex_mode(
    service: EnrichStageService,
    request: ArxivContentRequest,
    method: str,
) -> tuple[str, bool]:
    try:
        return service._ensure_arxiv_latex_source_content(
            client=request.client,
            item_id=request.item_id,
            canonical_url=request.canonical_url,
            source_item_id=request.source_item_id,
            diag=request.diag,
        )
    except Exception as method_exc:
        _log_arxiv_pdf_fallback(
            service=service,
            request=request,
            method=method,
            exc=method_exc,
        )
        return _fallback_to_arxiv_pdf(service, request)


def _ensure_arxiv_html_document_mode(
    service: EnrichStageService,
    request: ArxivContentRequest,
    method: str,
) -> tuple[str, bool]:
    try:
        return service._ensure_arxiv_html_document_content(
            request=ArxivHtmlDocumentRequest(
                client=request.client,
                item_id=request.item_id,
                canonical_url=request.canonical_url,
                source_item_id=request.source_item_id,
                log=request.log,
                diag=request.diag,
                arxiv_html_throttle=request.arxiv_html_throttle,
            )
        )
    except Exception as method_exc:
        reason_bucket = _record_arxiv_html_document_fallback(
            service=service,
            request=request,
            exc=method_exc,
        )
        _log_arxiv_pdf_fallback(
            service=service,
            request=request,
            method=method,
            exc=method_exc,
            reason_bucket=reason_bucket,
        )
        return _fallback_to_arxiv_pdf(service, request)


def _record_arxiv_html_document_fallback(
    *,
    service: EnrichStageService,
    request: ArxivContentRequest,
    exc: Exception,
) -> str:
    if service.settings.sources.arxiv.enrich_failure_mode == "strict":
        raise exc
    reason_bucket = service._classify_arxiv_html_document_fallback_reason(exc)
    if request.diag is not None:
        request.diag["html_document_fallback_to_pdf"] = 1
        request.diag[f"html_document_fallback_reason.{reason_bucket}"] = 1
    return reason_bucket


def _log_arxiv_pdf_fallback(
    *,
    service: EnrichStageService,
    request: ArxivContentRequest,
    method: str,
    exc: Exception,
    reason_bucket: str | None = None,
) -> None:
    if service.settings.sources.arxiv.enrich_failure_mode == "strict":
        raise exc
    bound_log = request.log.bind(item_id=request.item_id)
    if reason_bucket:
        bound_log = bound_log.bind(html_document_fallback_reason=reason_bucket)
    bound_log.warning(
        "arXiv enrich_method={} failed, falling back to pdf path: {}",
        method,
        service._sanitize_error_message(str(exc)),
    )


def ensure_arxiv_html_document_content(
    service: EnrichStageService,
    request: ArxivHtmlDocumentRequest,
) -> tuple[str, bool]:
    context = _ArxivHtmlDocumentContext(service=service, request=request)
    existing_document, stored_new = context.existing_document_result()
    if existing_document is not None:
        return existing_document, stored_new

    html_url = service._build_arxiv_html_url(
        canonical_url=request.canonical_url,
        source_item_id=request.source_item_id,
    )
    if not html_url:
        raise ValueError("missing arXiv html url")
    html = context.fetch_html(url=html_url)
    cleaned_document, pending_upserts = context.extract_new_document(html=html)
    context.persist_pending_upserts(pending_upserts)
    service._annotate_content_diag(
        request.diag,
        content_type="html_document",
        content_text=cleaned_document,
    )
    return cleaned_document, True


def ensure_pdf_content(
    service: EnrichStageService,
    request: PdfContentRequest,
) -> tuple[str, bool]:
    db_read_started = time.perf_counter()
    existing_pdf = service._get_latest_content_text(
        item_id=request.item_id,
        content_type="pdf_text",
    )
    if request.diag is not None:
        request.diag["db_read_ms"] = request.diag.get("db_read_ms", 0) + int(
            (time.perf_counter() - db_read_started) * 1000
        )
    if existing_pdf is not None:
        service._annotate_content_diag(
            request.diag,
            content_type="pdf_text",
            content_text=existing_pdf,
        )
        return existing_pdf, False

    pdf_url = service._build_pdf_url(
        source=request.source,
        canonical_url=request.canonical_url,
        source_item_id=request.source_item_id,
    )
    if not pdf_url:
        raise ValueError("missing pdf url")

    fetch_started = time.perf_counter()
    pdf_bytes = _pipeline_fetch_url_bytes()(request.client, pdf_url)
    if request.diag is not None:
        request.diag["fetch_ms"] = request.diag.get("fetch_ms", 0) + int(
            (time.perf_counter() - fetch_started) * 1000
        )
        request.diag["input_bytes"] = request.diag.get("input_bytes", 0) + len(
            pdf_bytes
        )

    extract_started = time.perf_counter()
    pdf_diag: dict[str, Any] = {}
    extracted_pdf = _pipeline_extract_pdf_text()(pdf_bytes, diag=pdf_diag)
    if request.diag is not None:
        request.diag["extract_ms"] = request.diag.get("extract_ms", 0) + int(
            (time.perf_counter() - extract_started) * 1000
        )
        pdf_backend = str(pdf_diag.get("pdf_backend") or "").strip().lower()
        if pdf_backend:
            request.diag["pdf_backend"] = pdf_backend
    if extracted_pdf is None:
        raise RuntimeError("empty pdf text extraction")

    db_write_started = time.perf_counter()
    service.repository.upsert_content(
        item_id=request.item_id,
        content_type="pdf_text",
        text=extracted_pdf,
    )
    if request.diag is not None:
        request.diag["db_write_ms"] = request.diag.get("db_write_ms", 0) + int(
            (time.perf_counter() - db_write_started) * 1000
        )
    service._annotate_content_diag(
        request.diag,
        content_type="pdf_text",
        content_text=extracted_pdf,
        pdf_backend=str(pdf_diag.get("pdf_backend") or "").strip().lower() or None,
    )
    return extracted_pdf, True


@dataclass(slots=True)
class _EnrichStats:
    service: EnrichStageService
    processed: int = 0
    failed: int = 0
    skipped: int = 0
    duration_ms_total: int = 0
    arxiv_items_by_method: dict[str, int] = None  # type: ignore[assignment]
    arxiv_failed_by_method: dict[str, int] = None  # type: ignore[assignment]
    html_document_items_total: int = 0
    html_document_fetch_ms_sum: int = 0
    html_document_cleanup_ms_sum: int = 0
    html_document_pandoc_ms_sum: int = 0
    html_document_pandoc_failed_total: int = 0
    html_document_pandoc_warning_items_total: int = 0
    html_document_pandoc_warning_count_sum: int = 0
    html_document_pandoc_warning_tex_math_convert_failed_sum: int = 0
    html_document_pandoc_math_replaced_sum: int = 0
    html_document_fallback_to_pdf_total: int = 0
    html_document_fallback_reason_totals: dict[str, int] = None  # type: ignore[assignment]
    html_document_db_read_ms_sum: int = 0
    html_document_db_write_ms_sum: int = 0
    source_stats: dict[str, dict[str, Any]] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.arxiv_items_by_method = {
            "pdf_text": 0,
            "latex_source": 0,
            "html_document": 0,
        }
        self.arxiv_failed_by_method = {
            "pdf_text": 0,
            "latex_source": 0,
            "html_document": 0,
        }
        self.html_document_fallback_reason_totals = {
            bucket: 0 for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS
        }
        self.source_stats = {
            source_name: self.service._new_source_enrich_bucket()
            for source_name in _SOURCE_DIAGNOSTIC_NAMES
        }

    def source_bucket(self, source_name: str) -> dict[str, Any]:
        normalized = str(source_name or "").strip().lower() or "unknown"
        return self.source_stats.setdefault(
            normalized,
            self.service._new_source_enrich_bucket(),
        )

    def consume_result(self, request: _ConsumeResultRequest) -> None:
        result = request.result
        source = str(result.get("source") or "").strip().lower()
        source_bucket = self.source_bucket(source)
        self._update_status_counts(request, source_bucket)
        diag = result.get("diag") or {}
        self._accumulate_diag(
            source_bucket=source_bucket,
            item_elapsed_ms=request.item_elapsed_ms,
            diag=diag,
        )
        self._record_content_metadata(source_bucket=source_bucket, diag=diag)
        self._record_arxiv_metrics(
            source=source,
            arxiv_method=result.get("arxiv_method"),
            diag=diag,
        )
        self.duration_ms_total += int(request.item_elapsed_ms)

    def _update_status_counts(
        self,
        request: _ConsumeResultRequest,
        source_bucket: dict[str, Any],
    ) -> None:
        if request.result.get("status") == "ok":
            self._record_success_status(
                result=request.result, source_bucket=source_bucket
            )
            return
        self._record_failed_status(request, source_bucket)

    def _record_success_status(
        self,
        *,
        result: dict[str, Any],
        source_bucket: dict[str, Any],
    ) -> None:
        if result.get("stored_new"):
            self.processed += 1
            source_bucket["processed_total"] = (
                int(source_bucket.get("processed_total") or 0) + 1
            )
            return
        self.skipped += 1
        source_bucket["skipped_total"] = (
            int(source_bucket.get("skipped_total") or 0) + 1
        )

    def _record_failed_status(
        self,
        request: _ConsumeResultRequest,
        source_bucket: dict[str, Any],
    ) -> None:
        result = request.result
        self.failed += 1
        source_bucket["failed_total"] = int(source_bucket.get("failed_total") or 0) + 1
        item_id = result.get("item_id")
        arxiv_method = result.get("arxiv_method")
        if isinstance(arxiv_method, str) and arxiv_method:
            self.arxiv_failed_by_method[arxiv_method] = (
                self.arxiv_failed_by_method.get(arxiv_method, 0) + 1
            )
        classification = result.get("classification") or {}
        if request.include_debug:
            request.write_and_record_artifact(
                item_id=int(item_id) if item_id is not None else None,
                kind="error_context",
                payload={
                    "stage": "enrich",
                    "error_type": result.get("error_type") or "Exception",
                    "error_message": result.get("error_message") or "unknown",
                    "item_id": item_id,
                    **(classification if isinstance(classification, dict) else {}),
                },
            )
        request.log.bind(item_id=item_id).warning(
            "Enrich failed: {}",
            result.get("error_message") or "unknown",
        )

    def _accumulate_diag(
        self,
        *,
        source_bucket: dict[str, Any],
        item_elapsed_ms: int,
        diag: dict[str, Any],
    ) -> None:
        source_bucket["item_duration_ms_total"] = int(
            source_bucket.get("item_duration_ms_total") or 0
        ) + int(item_elapsed_ms)
        for bucket_key, diag_key in (
            ("fetch_ms_sum", "fetch_ms"),
            ("extract_ms_sum", "extract_ms"),
            ("db_read_ms_sum", "db_read_ms"),
            ("db_write_ms_sum", "db_write_ms"),
            ("input_bytes_sum", "input_bytes"),
            ("content_chars_sum", "content_chars"),
            ("short_content_total", "short_content"),
        ):
            source_bucket[bucket_key] = int(source_bucket.get(bucket_key) or 0) + int(
                diag.get(diag_key) or 0
            )

    def _record_content_metadata(
        self,
        *,
        source_bucket: dict[str, Any],
        diag: dict[str, Any],
    ) -> None:
        content_type = str(diag.get("content_type") or "").strip().lower()
        if content_type:
            content_types = cast(dict[str, int], source_bucket["content_types"])
            content_types[content_type] = content_types.get(content_type, 0) + 1
        pdf_backend = str(diag.get("pdf_backend") or "").strip().lower()
        if pdf_backend:
            pdf_backends = cast(dict[str, int], source_bucket["pdf_backends"])
            pdf_backends[pdf_backend] = pdf_backends.get(pdf_backend, 0) + 1

    def _record_arxiv_metrics(
        self,
        *,
        source: str,
        arxiv_method: Any,
        diag: dict[str, Any],
    ) -> None:
        if source == "arxiv" and isinstance(arxiv_method, str) and arxiv_method:
            self.arxiv_items_by_method[arxiv_method] = (
                self.arxiv_items_by_method.get(arxiv_method, 0) + 1
            )
        if source == "arxiv" and arxiv_method == "html_document":
            self._consume_html_document_diag(diag)

    def _consume_html_document_diag(self, diag: dict[str, Any]) -> None:
        self.html_document_items_total += 1
        self.html_document_fetch_ms_sum += int(diag.get("fetch_ms") or 0)
        self.html_document_cleanup_ms_sum += int(diag.get("cleanup_ms") or 0)
        self.html_document_pandoc_ms_sum += int(diag.get("pandoc_ms") or 0)
        self.html_document_pandoc_failed_total += int(diag.get("pandoc_failed") or 0)
        warning_count = int(diag.get("pandoc_warning_count") or 0)
        self.html_document_pandoc_warning_count_sum += warning_count
        if warning_count > 0:
            self.html_document_pandoc_warning_items_total += 1
        self.html_document_pandoc_warning_tex_math_convert_failed_sum += int(
            diag.get("pandoc_warning_tex_math_convert_failed") or 0
        )
        self.html_document_pandoc_math_replaced_sum += int(
            diag.get("pandoc_math_replaced_total") or 0
        )
        self.html_document_fallback_to_pdf_total += int(
            diag.get("html_document_fallback_to_pdf") or 0
        )
        for bucket in _ARXIV_HTML_DOCUMENT_FALLBACK_REASON_BUCKETS:
            self.html_document_fallback_reason_totals[bucket] += int(
                diag.get(f"html_document_fallback_reason.{bucket}") or 0
            )
        self.html_document_db_read_ms_sum += int(diag.get("db_read_ms") or 0)
        self.html_document_db_write_ms_sum += int(diag.get("db_write_ms") or 0)

    def record_metrics(self, *, run_id: str, sql_diag: Any, started: float) -> None:
        repository = self.service.repository
        self._record_summary_metrics(
            repository=repository,
            run_id=run_id,
            sql_diag=sql_diag,
            started=started,
        )
        self._record_html_document_metrics(repository=repository, run_id=run_id)
        for source_name in sorted(self.source_stats):
            self._record_source_metrics(
                repository=repository,
                run_id=run_id,
                source_name=source_name,
                source_bucket=self.source_stats[source_name],
            )

    def _record_summary_metrics(
        self,
        *,
        repository: Any,
        run_id: str,
        sql_diag: Any,
        started: float,
    ) -> None:
        for metric_name, value, unit in (
            ("pipeline.enrich.processed_total", self.processed, "count"),
            ("pipeline.enrich.skipped_total", self.skipped, "count"),
            ("pipeline.enrich.failed_total", self.failed, "count"),
            ("pipeline.enrich.item_duration_ms_total", self.duration_ms_total, "ms"),
            (
                "pipeline.enrich.duration_ms",
                int((time.perf_counter() - started) * 1000),
                "ms",
            ),
            ("pipeline.enrich.db.sql_queries_total", sql_diag.queries_total, "count"),
            ("pipeline.enrich.db.sql_commits_total", sql_diag.commits_total, "count"),
        ):
            repository.record_metric(
                run_id=run_id,
                name=metric_name,
                value=value,
                unit=unit,
            )
        for method in ("pdf_text", "latex_source", "html_document"):
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.arxiv.method_selected.{method}_total",
                value=self.arxiv_items_by_method.get(method, 0),
                unit="count",
            )
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.arxiv.method_failed.{method}_total",
                value=self.arxiv_failed_by_method.get(method, 0),
                unit="count",
            )

    def _record_html_document_metrics(self, *, repository: Any, run_id: str) -> None:
        for metric_name, value, unit in (
            (
                "pipeline.enrich.arxiv.html_document.items_total",
                self.html_document_items_total,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.fetch_ms_sum",
                self.html_document_fetch_ms_sum,
                "ms",
            ),
            (
                "pipeline.enrich.arxiv.html_document.cleanup_ms_sum",
                self.html_document_cleanup_ms_sum,
                "ms",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_ms_sum",
                self.html_document_pandoc_ms_sum,
                "ms",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_failed_total",
                self.html_document_pandoc_failed_total,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_warning_items_total",
                self.html_document_pandoc_warning_items_total,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_warning_count_sum",
                self.html_document_pandoc_warning_count_sum,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_warning_tex_math_convert_failed_sum",
                self.html_document_pandoc_warning_tex_math_convert_failed_sum,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.pandoc_math_replaced_sum",
                self.html_document_pandoc_math_replaced_sum,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.fallback_to_pdf_total",
                self.html_document_fallback_to_pdf_total,
                "count",
            ),
            (
                "pipeline.enrich.arxiv.html_document.db_read_ms_sum",
                self.html_document_db_read_ms_sum,
                "ms",
            ),
            (
                "pipeline.enrich.arxiv.html_document.db_write_ms_sum",
                self.html_document_db_write_ms_sum,
                "ms",
            ),
        ):
            repository.record_metric(
                run_id=run_id,
                name=metric_name,
                value=value,
                unit=unit,
            )
        for bucket, count in self.html_document_fallback_reason_totals.items():
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.arxiv.html_document.fallback_to_pdf_reason.{bucket}_total",
                value=count,
                unit="count",
            )

    def _record_source_metrics(
        self,
        *,
        repository: Any,
        run_id: str,
        source_name: str,
        source_bucket: dict[str, Any],
    ) -> None:
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
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.source.{source_name}.{metric_name}",
                value=int(source_bucket.get(metric_name) or 0),
                unit=unit,
            )
        for content_type, count in sorted(
            cast(dict[str, int], source_bucket["content_types"]).items()
        ):
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.source.{source_name}.content_type.{content_type}_total",
                value=count,
                unit="count",
            )
        for pdf_backend, count in sorted(
            cast(dict[str, int], source_bucket["pdf_backends"]).items()
        ):
            repository.record_metric(
                run_id=run_id,
                name=f"pipeline.enrich.source.{source_name}.pdf_backend.{pdf_backend}_total",
                value=count,
                unit="count",
            )


class _EnrichStageRunner:
    def __init__(
        self, *, service: EnrichStageService, request: EnrichStageRequest
    ) -> None:
        self.service = service
        self.request = request
        self.log = logger.bind(module="pipeline.enrich", run_id=request.run_id)
        self.started = time.perf_counter()
        self.include_debug = bool(service.settings.write_debug_artifacts) and bool(
            service.settings.artifacts_dir is not None
        )
        self.timeout = httpx.Timeout(10.0, connect=5.0)
        self.headers = {"User-Agent": "recoleta/0.1"}
        self.html_document_max_concurrency = int(
            service.settings.sources.arxiv.html_document_max_concurrency or 1
        )
        self.enable_parallel = (
            bool(service.settings.sources.arxiv.enrich_method == "html_document")
            and bool(service.settings.sources.arxiv.html_document_enable_parallel)
            and self.html_document_max_concurrency > 1
        )
        self.arxiv_html_throttle = _build_arxiv_html_throttle(service)

    def run(self) -> None:
        with self.service.repository.sql_diagnostics() as sql_diag:
            items = self._load_items()
            stats = _EnrichStats(service=self.service)
            with _pipeline_progress()(
                TextColumn("{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
                console=self.service._progress_console,
            ) as progress:
                task_id = progress.add_task("Enriching items", total=len(items))
                if not self.enable_parallel:
                    self._run_serial_items(
                        items=items, progress=progress, task_id=task_id, stats=stats
                    )
                else:
                    parallel_items, serial_items = self._partition_items(items)
                    self._run_serial_items(
                        items=serial_items,
                        progress=progress,
                        task_id=task_id,
                        stats=stats,
                    )
                    self._run_parallel_items(
                        items=parallel_items,
                        progress=progress,
                        task_id=task_id,
                        stats=stats,
                    )
            stats.record_metrics(
                run_id=self.request.run_id,
                sql_diag=sql_diag,
                started=self.started,
            )
            self.log.info(
                "Enrich completed with processed={} skipped={} failed={}",
                stats.processed,
                stats.skipped,
                stats.failed,
            )

    def _load_items(self) -> list[Any]:
        candidate_limit = self.service._stage_candidate_limit(limit=self.request.limit)
        items = self.service._invoke_repository_method(
            "list_items_for_analysis",
            limit=candidate_limit,
            period_start=self.request.period_start,
            period_end=self.request.period_end,
        )
        rebalanced_items, candidate_counts, deferred_counts = (
            self.service._rebalance_items_by_source(
                request=RebalanceItemsRequest(
                    items=list(items),
                    limit=self.request.limit,
                )
            )
        )
        self.service._record_stage_source_selection_metrics(
            run_id=self.request.run_id,
            stage="enrich",
            candidate_counts=candidate_counts,
            deferred_counts=deferred_counts,
        )
        return rebalanced_items

    def _run_serial_items(
        self,
        *,
        items: list[Any],
        progress: Any,
        task_id: int,
        stats: _EnrichStats,
    ) -> None:
        with httpx.Client(
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        ) as client:
            for item in items:
                item_started = time.perf_counter()
                result = self._process_one(client=client, item=item)
                self._consume_result(
                    _RunnerConsumeRequest(
                        stats=stats,
                        progress=progress,
                        task_id=task_id,
                        result=result,
                        item_elapsed_ms=int(
                            (time.perf_counter() - item_started) * 1000
                        ),
                    )
                )

    def _run_parallel_items(
        self,
        *,
        items: list[Any],
        progress: Any,
        task_id: int,
        stats: _EnrichStats,
    ) -> None:
        parallel_state = _ParallelRunState(
            local=threading.local(),
            created_clients=[],
            created_lock=threading.Lock(),
        )
        executor = _pipeline_thread_pool_executor()(
            max_workers=self.html_document_max_concurrency
        )
        futures = {
            executor.submit(self._parallel_worker, parallel_state, item): item
            for item in items
        }
        interrupted = False
        try:
            for future in _pipeline_as_completed()(futures):
                result = self._parallel_result(future)
                self._consume_result(
                    _RunnerConsumeRequest(
                        stats=stats,
                        progress=progress,
                        task_id=task_id,
                        result=result,
                        item_elapsed_ms=int(result.get("elapsed_ms") or 0),
                    )
                )
        except KeyboardInterrupt:
            interrupted = True
            self.log.warning(
                "Interrupt received; cancelling pending enrich workers and draining in-flight tasks."
            )
            self._cancel_parallel_executor(executor=executor, futures=futures)
            self._drain_parallel_futures(futures)
            raise
        finally:
            self._shutdown_parallel_executor(executor)
            self._close_parallel_clients(
                parallel_state=parallel_state,
                futures=futures,
                interrupted=interrupted,
            )

    def _partition_items(self, items: list[Any]) -> tuple[list[Any], list[Any]]:
        parallel_items: list[Any] = []
        serial_items: list[Any] = []
        for item in items:
            source = str(getattr(item, "source", "") or "").strip().lower()
            if (
                source == "arxiv"
                and self.service.settings.sources.arxiv.enrich_method == "html_document"
            ):
                parallel_items.append(item)
            else:
                serial_items.append(item)
        return parallel_items, serial_items

    def _process_one(self, *, client: httpx.Client, item: Any) -> dict[str, Any]:
        raw_item_id = getattr(item, "id", None)
        source = str(getattr(item, "source", "") or "").strip().lower()
        arxiv_method: str | None = None
        if source == "arxiv":
            arxiv_method = self.service.settings.sources.arxiv.enrich_method
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
            _, stored_new_content = self.service._ensure_item_content(
                client=client,
                item=item,
                log=self.log,
                diag=diag,
                arxiv_html_throttle=self.arxiv_html_throttle,
            )
            db_mark_started = time.perf_counter()
            self.service.repository.mark_item_enriched(item_id=item_id)
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
            sanitized_error = self.service._sanitize_error_message(str(enrich_exc))
            classification = self.service._classify_exception(enrich_exc)
            try:
                db_mark_started = time.perf_counter()
                if classification.get("retryable") is True:
                    self.service.repository.mark_item_retryable_failed(item_id=item_id)
                else:
                    self.service.repository.mark_item_failed(item_id=item_id)
                diag["db_write_ms"] = diag.get("db_write_ms", 0) + int(
                    (time.perf_counter() - db_mark_started) * 1000
                )
            except Exception as mark_exc:  # noqa: BLE001
                self.log.bind(item_id=item_id).warning(
                    "Enrich mark_item_state failed: {}",
                    self.service._sanitize_error_message(str(mark_exc)),
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

    def _consume_result(self, request: _RunnerConsumeRequest) -> None:
        request.stats.consume_result(
            _ConsumeResultRequest(
                result=request.result,
                item_elapsed_ms=request.item_elapsed_ms,
                include_debug=self.include_debug,
                write_and_record_artifact=self._write_and_record_artifact,
                log=self.log,
            )
        )
        request.progress.advance(request.task_id, 1)

    def _parallel_worker(
        self,
        parallel_state: _ParallelRunState,
        item: Any,
    ) -> dict[str, Any]:
        started = time.perf_counter()
        result = self._process_one(
            client=self._thread_client(parallel_state),
            item=item,
        )
        result["elapsed_ms"] = int((time.perf_counter() - started) * 1000)
        return result

    def _thread_client(self, parallel_state: _ParallelRunState) -> httpx.Client:
        existing = getattr(parallel_state.local, "client", None)
        if isinstance(existing, httpx.Client):
            return existing
        client = httpx.Client(
            timeout=self.timeout,
            headers=self.headers,
            follow_redirects=True,
        )
        parallel_state.local.client = client
        with parallel_state.created_lock:
            parallel_state.created_clients.append(client)
        return client

    def _parallel_result(self, future: Any) -> dict[str, Any]:
        try:
            return future.result()
        except Exception as exc:  # noqa: BLE001
            return {
                "status": "failed",
                "error_type": type(exc).__name__,
                "error_message": self.service._sanitize_error_message(str(exc)),
                "classification": self.service._classify_exception(exc),
                "elapsed_ms": 0,
            }

    def _cancel_parallel_executor(
        self, *, executor: Any, futures: dict[Any, Any]
    ) -> None:
        for future in futures:
            future.cancel()
        try:
            executor.shutdown(wait=False, cancel_futures=True)
        except TypeError:
            executor.shutdown(wait=False)

    def _drain_parallel_futures(self, futures: dict[Any, Any]) -> None:
        deadline = time.monotonic() + 10.0
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            try:
                _, not_done = _pipeline_wait()(futures, timeout=min(0.25, remaining))
            except KeyboardInterrupt:
                continue
            if not not_done:
                break

    def _shutdown_parallel_executor(self, executor: Any) -> None:
        try:
            executor.shutdown(wait=True, cancel_futures=True)
        except TypeError:
            executor.shutdown(wait=True)
        except KeyboardInterrupt:
            pass

    def _close_parallel_clients(
        self,
        *,
        parallel_state: _ParallelRunState,
        futures: dict[Any, Any],
        interrupted: bool,
    ) -> None:
        all_done = all(future.done() for future in futures) if futures else True
        if interrupted and not all_done:
            self.log.warning(
                "Interrupted before workers finished; skipping http client close to avoid mid-request failures."
            )
            return
        with parallel_state.created_lock:
            to_close = list(parallel_state.created_clients)
        for client in to_close:
            try:
                client.close()
            except Exception:
                pass

    def _write_and_record_artifact(
        self,
        *,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> None:
        self.service._record_debug_artifact(
            run_id=self.request.run_id,
            item_id=item_id,
            kind=kind,
            payload=payload,
            log=self.log.bind(item_id=item_id),
            failure_message=f"Enrich {kind} artifact record failed: {{}}",
        )


class _ArxivHtmlDocumentContext:
    def __init__(
        self,
        *,
        service: EnrichStageService,
        request: ArxivHtmlDocumentRequest,
    ) -> None:
        self.service = service
        self.request = request
        self.parallel_mode = (
            bool(service.settings.sources.arxiv.enrich_method == "html_document")
            and bool(service.settings.sources.arxiv.html_document_enable_parallel)
            and int(service.settings.sources.arxiv.html_document_max_concurrency or 1)
            > 1
        )
        self.sample_rate = float(
            service.settings.sources.arxiv.html_document_log_sample_rate or 0.0
        )
        self.bound_log = request.log.bind(item_id=request.item_id)

    def existing_document_result(self) -> tuple[str | None, bool]:
        existing_document, existing_md, existing_refs = self._load_existing_content()
        if (
            bool(
                self.service.settings.sources.arxiv.html_document_skip_cleanup_when_complete
            )
            and existing_document is not None
            and existing_md is not None
        ):
            self.service._annotate_content_diag(
                self.request.diag,
                content_type="html_document",
                content_text=existing_document,
            )
            return existing_document, False
        if existing_document is None:
            return None, False

        cleaned_document, references_html, stats = self._clean_document(
            existing_document
        )
        pending_upserts: dict[str, str] = {}
        if cleaned_document is not None and cleaned_document != existing_document:
            pending_upserts["html_document"] = cleaned_document
            existing_document = cleaned_document
        if existing_refs is None and references_html is not None:
            pending_upserts["html_references"] = references_html
        if existing_md is None and existing_document is not None:
            markdown = self._populate_markdown(
                html_document=existing_document,
                pending_upserts=pending_upserts,
                existing_document=True,
            )
            if markdown is not None:
                pending_upserts["html_document_md"] = markdown

        self._log_cleanup_stats(stats=stats)
        stored_new = self.persist_pending_upserts(pending_upserts)
        self.service._annotate_content_diag(
            self.request.diag,
            content_type="html_document",
            content_text=existing_document,
        )
        return existing_document, stored_new

    def fetch_html(self, *, url: str) -> str:
        if callable(self.request.arxiv_html_throttle):
            self.request.arxiv_html_throttle()
        fetch_started = time.perf_counter()
        html = _pipeline_fetch_url_html()(self.request.client, url)
        if self.request.diag is not None:
            self.request.diag["fetch_ms"] = self.request.diag.get("fetch_ms", 0) + int(
                (time.perf_counter() - fetch_started) * 1000
            )
            self.request.diag["input_bytes"] = self.request.diag.get(
                "input_bytes", 0
            ) + len(html.encode("utf-8"))
        return html

    def extract_new_document(self, *, html: str) -> tuple[str, dict[str, str]]:
        cleaned_document, references_html, stats = self._clean_document(html)
        if cleaned_document is None:
            raise RuntimeError("empty arXiv html document extraction")
        pending_upserts: dict[str, str] = {"html_document": cleaned_document}
        if references_html is not None:
            pending_upserts["html_references"] = references_html
        markdown = self._populate_markdown(
            html_document=cleaned_document,
            pending_upserts=pending_upserts,
            existing_document=False,
        )
        if markdown is not None:
            pending_upserts["html_document_md"] = markdown
        extracted_maintext = _pipeline_extract_html_maintext()(html)
        if extracted_maintext is not None:
            pending_upserts["html_maintext"] = extracted_maintext
        self._log_cleanup_stats(stats=stats)
        return cleaned_document, pending_upserts

    def persist_pending_upserts(self, pending_upserts: dict[str, str]) -> bool:
        if not pending_upserts:
            return False
        db_write_started = time.perf_counter()
        if bool(
            self.service.settings.sources.arxiv.html_document_use_batched_db_writes
        ):
            inserted = self.service.repository.upsert_contents_texts(
                item_id=self.request.item_id,
                texts_by_type=pending_upserts,
            )
        else:
            inserted = 0
            for content_type, text in pending_upserts.items():
                _, did_insert = self.service.repository.upsert_content_with_inserted(
                    item_id=self.request.item_id,
                    content_type=content_type,
                    text=text,
                )
                inserted += 1 if did_insert else 0
        if self.request.diag is not None:
            self.request.diag["db_write_ms"] = self.request.diag.get(
                "db_write_ms", 0
            ) + int((time.perf_counter() - db_write_started) * 1000)
        return inserted > 0

    def _load_existing_content(self) -> tuple[str | None, str | None, str | None]:
        db_read_started = time.perf_counter()
        existing = self.service.repository.get_latest_content_texts(
            item_id=self.request.item_id,
            content_types=["html_document", "html_document_md", "html_references"],
        )
        if self.request.diag is not None:
            self.request.diag["db_read_ms"] = self.request.diag.get(
                "db_read_ms", 0
            ) + int((time.perf_counter() - db_read_started) * 1000)
        return (
            existing.get("html_document"),
            existing.get("html_document_md"),
            existing.get("html_references"),
        )

    def _clean_document(
        self, html: str
    ) -> tuple[str | None, str | None, dict[str, Any]]:
        cleanup_started = time.perf_counter()
        cleaned_document, references_html, stats = (
            _pipeline_extract_html_document_cleaned_with_references()(html)
        )
        cleanup_elapsed_ms = int((time.perf_counter() - cleanup_started) * 1000)
        if self.request.diag is not None:
            self.request.diag["cleanup_ms"] = (
                self.request.diag.get("cleanup_ms", 0) + cleanup_elapsed_ms
            )
            self.request.diag["extract_ms"] = (
                self.request.diag.get("extract_ms", 0) + cleanup_elapsed_ms
            )
        return cleaned_document, references_html, stats

    def _populate_markdown(
        self,
        *,
        html_document: str,
        pending_upserts: dict[str, str],
        existing_document: bool,
    ) -> str | None:
        markdown, elapsed_ms, error = _pipeline_convert_html_document_to_markdown()(
            html_document,
            diag=self.request.diag,
        )
        if self.request.diag is not None:
            self.request.diag["pandoc_ms"] = self.request.diag.get(
                "pandoc_ms", 0
            ) + int(elapsed_ms or 0)
            self.request.diag["extract_ms"] = self.request.diag.get(
                "extract_ms", 0
            ) + int(elapsed_ms or 0)
        if markdown is not None:
            message = (
                "html_document_md created from existing html_document elapsed_ms={} chars_in={} chars_out={}"
                if existing_document
                else "html_document_md created elapsed_ms={} chars_in={} chars_out={}"
            )
            self._log_info_or_debug(
                message, elapsed_ms, len(html_document), len(markdown)
            )
            return markdown
        self.service._log_html_document_md_conversion_skipped(
            log=self.request.log,
            item_id=self.request.item_id,
            elapsed_ms=elapsed_ms,
            error=error,
        )
        return None

    def _log_cleanup_stats(self, *, stats: dict[str, Any]) -> None:
        self._log_info_or_debug(
            "html_document cleanup stats removed_non_body={} removed_references_blocks={} references_chars={}",
            stats.get("removed_non_body_blocks"),
            stats.get("removed_references_blocks"),
            stats.get("references_chars"),
        )

    def _log_info_or_debug(self, message: str, *args: Any) -> None:
        if self._should_log_info():
            self.bound_log.info(message, *args)
        else:
            self.bound_log.debug(message, *args)

    def _should_log_info(self) -> bool:
        if not self.parallel_mode:
            return True
        if self.sample_rate >= 1.0:
            return True
        if self.sample_rate <= 0.0:
            return False
        digest = hashlib.sha256(str(self.request.item_id).encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:4], "big") / (2**32)
        return bucket < self.sample_rate


class _ArxivHtmlRateLimiter:
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


def _build_arxiv_html_throttle(
    service: EnrichStageService,
) -> Callable[[], None] | None:
    arxiv_rps = float(
        service.settings.sources.arxiv.html_document_requests_per_second or 0.0
    )
    if arxiv_rps <= 0:
        return None
    return _ArxivHtmlRateLimiter(requests_per_second=arxiv_rps).acquire


def _pipeline_progress() -> type[Progress]:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.Progress


def _pipeline_thread_pool_executor() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.ThreadPoolExecutor


def _pipeline_as_completed() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.as_completed


def _pipeline_wait() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.wait


def _pipeline_fetch_url_bytes() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.fetch_url_bytes


def _pipeline_fetch_url_html() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.fetch_url_html


def _pipeline_extract_pdf_text() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.extract_pdf_text


def _pipeline_extract_html_maintext() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.extract_html_maintext


def _pipeline_convert_html_document_to_markdown() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.convert_html_document_to_markdown


def _pipeline_extract_html_document_cleaned_with_references() -> Any:
    from recoleta import pipeline as pipeline_module

    return pipeline_module.extract_html_document_cleaned_with_references
