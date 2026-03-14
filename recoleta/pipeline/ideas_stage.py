from __future__ import annotations

import json
import time
from datetime import date, datetime
from pathlib import Path
from typing import Any, Protocol, cast

from loguru import logger

from recoleta.config import TopicStreamRuntime
from recoleta.pipeline.metrics import metric_token, scoped_trends_metric_name
from recoleta.pipeline.projections import run_projection_target
from recoleta.passes import (
    PassInputRef,
    PassStatus,
    TREND_SYNTHESIS_PASS_KIND,
    TrendIdeasPayload,
    build_trend_ideas_pass_output,
    build_trend_snapshot_pack_md,
    normalize_trend_ideas_payload,
)
from recoleta.ports import RepositoryPort, TrendStageRepositoryPort
from recoleta.publish import write_markdown_ideas_note, write_obsidian_ideas_note
from recoleta.rag import ideas_agent
from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name
from recoleta import trends
from recoleta.trends import TrendPayload
from recoleta.types import DEFAULT_TOPIC_STREAM, IdeasResult, utc_now


def _trend_metric_name(name: str, *, scope: str) -> str:
    return scoped_trends_metric_name(name, scope=scope)


class IdeasStageService(Protocol):
    settings: Any
    analyzer: Any
    semantic_triage: Any
    telegram_sender: Any | None
    _topic_streams: list[TopicStreamRuntime]
    _explicit_topic_streams: bool
    _llm_connection: Any

    @property
    def repository(self) -> TrendStageRepositoryPort: ...

    def ideas(
        self,
        *,
        run_id: str,
        granularity: str = "day",
        anchor_date: date | None = None,
        llm_model: str | None = None,
    ) -> IdeasResult: ...

    def _settings_for_topic_stream(self, stream: TopicStreamRuntime) -> Any: ...

    def _sanitize_error_message(self, message: str) -> str: ...

    def _write_debug_artifact(
        self,
        *,
        run_id: str,
        item_id: int | None,
        kind: str,
        payload: dict[str, Any],
    ) -> Path | None: ...


def _period_bounds_for_granularity(
    *, granularity: str, anchor: date
) -> tuple[datetime, datetime]:
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity == "week":
        return trends.week_period_bounds(anchor)
    if normalized_granularity == "month":
        return trends.month_period_bounds(anchor)
    return trends.day_period_bounds(anchor)


def _load_trend_payload_from_pass_output(row: Any) -> TrendPayload:
    payload_json = str(getattr(row, "payload_json", "") or "{}")
    return TrendPayload.model_validate(json.loads(payload_json))


def _render_idea_document_chunk_text(idea: Any) -> str:
    evidence_reasons = [
        str(getattr(ref, "reason", "") or "").strip()
        for ref in list(getattr(idea, "evidence_refs", []) or [])
        if str(getattr(ref, "reason", "") or "").strip()
    ]
    lines = [
        f"Title: {str(getattr(idea, 'title', '') or '').strip()}",
        f"Kind: {str(getattr(idea, 'kind', '') or '').strip()}",
        f"Time horizon: {str(getattr(idea, 'time_horizon', '') or '').strip()}",
        f"User/job: {str(getattr(idea, 'user_or_job', '') or '').strip()}",
        f"Thesis: {str(getattr(idea, 'thesis', '') or '').strip()}",
        f"Why now: {str(getattr(idea, 'why_now', '') or '').strip()}",
        f"What changed: {str(getattr(idea, 'what_changed', '') or '').strip()}",
        (
            "Validation next step: "
            + str(getattr(idea, "validation_next_step", "") or "").strip()
        ),
    ]
    if evidence_reasons:
        lines.append("Evidence: " + " | ".join(evidence_reasons))
    return "\n".join(line for line in lines if str(line).strip()).strip()


def _persist_ideas_document_projection(
    *,
    repository: TrendStageRepositoryPort,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendIdeasPayload,
    scope: str,
) -> int:
    doc = repository.upsert_document_for_idea(
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        title=str(payload.title or "").strip() or "Ideas",
        scope=scope,
    )
    doc_id = int(getattr(doc, "id") or 0)
    if doc_id <= 0:
        raise RuntimeError("idea document projection did not return a document id")

    repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=0,
        kind="summary",
        text_value=str(payload.summary_md or "").strip() or "(empty)",
        start_char=0,
        end_char=None,
        source_content_type="trend_ideas_summary",
    )

    next_chunk_index = 1
    for idea in list(payload.ideas or []):
        text_value = _render_idea_document_chunk_text(idea)
        if not text_value:
            continue
        repository.upsert_document_chunk(
            doc_id=doc_id,
            chunk_index=next_chunk_index,
            kind="content",
            text_value=text_value,
            start_char=0,
            end_char=None,
            source_content_type="trend_idea",
        )
        next_chunk_index += 1

    repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=next_chunk_index,
        kind="meta",
        text_value=json.dumps(
            payload.model_dump(mode="json"), ensure_ascii=False, separators=(",", ":")
        ),
        start_char=0,
        end_char=None,
        source_content_type="trend_ideas_payload_json",
    )
    repository.delete_document_chunks(doc_id=doc_id, chunk_index_gte=next_chunk_index + 1)
    return doc_id


def _record_ideas_debug_artifact(
    *,
    service: IdeasStageService,
    run_id: str,
    upstream_pass_output_id: int,
    status: PassStatus,
    trend_snapshot_pack_md: str,
    ideas_payload: TrendIdeasPayload,
    debug: dict[str, Any] | None,
) -> None:
    if not (
        bool(service.settings.write_debug_artifacts)
        and service.settings.artifacts_dir is not None
    ):
        return
    try:
        artifact_path = service._write_debug_artifact(
            run_id=run_id,
            item_id=None,
            kind="ideas_llm_response",
            payload={
                "upstream_pass_output_id": upstream_pass_output_id,
                "status": status.value,
                "trend_snapshot_pack_md": trend_snapshot_pack_md,
                "payload": ideas_payload.model_dump(mode="json"),
                "debug": debug or {},
            },
        )
    except Exception:
        return
    if artifact_path is None:
        return
    try:
        service.repository.add_artifact(
            run_id=run_id,
            item_id=None,
            kind="ideas_llm_response",
            path=artifact_path.name,
        )
    except Exception:
        return


def run_ideas_stage(
    service: IdeasStageService,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
    scope: str = DEFAULT_TOPIC_STREAM,
) -> IdeasResult:
    if service._explicit_topic_streams:
        return run_ideas_topic_streams_stage(
            service,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
        )

    log = logger.bind(module="pipeline.trends.pass.ideas", run_id=run_id, scope=scope)
    started = time.perf_counter()
    normalized_granularity = str(granularity or "").strip().lower()
    if normalized_granularity not in {"day", "week", "month"}:
        raise ValueError("granularity must be one of: day, week, month")
    anchor = anchor_date or utc_now().date()
    period_start, period_end = _period_bounds_for_granularity(
        granularity=normalized_granularity,
        anchor=anchor,
    )

    def record_metric(*, name: str, value: float, unit: str | None = None) -> None:
        service.repository.record_metric(
            run_id=run_id,
            name=_trend_metric_name(name, scope=scope),
            value=value,
            unit=unit,
        )

    upstream = service.repository.get_latest_pass_output(
        pass_kind=TREND_SYNTHESIS_PASS_KIND,
        scope=scope,
        status=PassStatus.SUCCEEDED.value,
        granularity=normalized_granularity,
        period_start=period_start,
        period_end=period_end,
    )
    if upstream is None or getattr(upstream, "id", None) is None:
        record_metric(
            name="pipeline.trends.pass.ideas.upstream_missing_total",
            value=1,
            unit="count",
        )
        record_metric(
            name="pipeline.trends.pass.ideas.duration_ms",
            value=int((time.perf_counter() - started) * 1000),
            unit="ms",
        )
        raise RuntimeError(
            "Missing trend_synthesis pass output for "
            f"granularity={normalized_granularity} "
            f"period_start={period_start.isoformat()} period_end={period_end.isoformat()}"
        )

    upstream_pass_output_id = int(getattr(upstream, "id"))
    trend_payload = _load_trend_payload_from_pass_output(upstream)
    trend_snapshot_pack_md = build_trend_snapshot_pack_md(
        trend_payload=trend_payload,
        upstream_pass_output_id=upstream_pass_output_id,
    )
    include_debug = bool(
        service.settings.write_debug_artifacts
        and service.settings.artifacts_dir is not None
    )
    model = str(llm_model or service.settings.llm_model or "").strip()
    if not model:
        raise ValueError("llm_model must not be empty")
    targets = set(service.settings.publish_targets or [])
    if "obsidian" in targets and service.settings.obsidian_vault_path is None:
        raise ValueError(
            "OBSIDIAN_VAULT_PATH is required when PUBLISH_TARGETS includes 'obsidian'"
        )
    if "telegram" in targets:
        record_metric(
            name="pipeline.trends.projection.ideas_telegram.skipped_total",
            value=1,
            unit="count",
        )
        log.info("Ideas telegram projection is not implemented; target ignored")

    store = LanceVectorStore(
        db_dir=Path(service.settings.rag_lancedb_dir),
        table_name=embedding_table_name(
            embedding_model=service.settings.trends_embedding_model,
            embedding_dimensions=service.settings.trends_embedding_dimensions,
        ),
    )
    payload, debug = ideas_agent.generate_trend_ideas_payload(
        repository=cast(Any, service.repository),
        vector_store=store,
        run_id=run_id,
        llm_model=model,
        output_language=service.settings.llm_output_language,
        embedding_model=service.settings.trends_embedding_model,
        embedding_dimensions=service.settings.trends_embedding_dimensions,
        embedding_batch_max_inputs=service.settings.trends_embedding_batch_max_inputs,
        embedding_batch_max_chars=service.settings.trends_embedding_batch_max_chars,
        embedding_failure_mode=getattr(
            service.settings, "trends_embedding_failure_mode", "continue"
        ),
        embedding_max_errors=int(
            getattr(service.settings, "trends_embedding_max_errors", 0) or 0
        ),
        granularity=normalized_granularity,
        period_start=period_start,
        period_end=period_end,
        trend_payload=trend_payload,
        trend_snapshot_pack_md=trend_snapshot_pack_md,
        rag_sources=trends.rag_sources_for_granularity(normalized_granularity),
        include_debug=include_debug,
        scope=scope,
        metric_namespace=_trend_metric_name("pipeline.trends.pass.ideas", scope=scope),
        llm_connection=service._llm_connection,
    )
    payload = normalize_trend_ideas_payload(payload)
    status = (
        PassStatus.SUPPRESSED
        if not list(payload.ideas or [])
        else PassStatus.SUCCEEDED
    )

    input_refs = [
        PassInputRef(
            ref_kind="pass_output",
            pass_kind=TREND_SYNTHESIS_PASS_KIND,
            scope=scope,
            granularity=normalized_granularity,
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            pass_output_id=upstream_pass_output_id,
        )
    ]
    diagnostics = debug if isinstance(debug, dict) else {}
    envelope = build_trend_ideas_pass_output(
        run_id=run_id,
        status=status,
        scope=scope,
        granularity=normalized_granularity,
        period_start=period_start,
        period_end=period_end,
        payload=payload,
        input_refs=input_refs,
        diagnostics=diagnostics,
    )

    try:
        row = service.repository.create_pass_output(
            run_id=envelope.run_id,
            pass_kind=envelope.pass_kind,
            status=envelope.status.value,
            scope=envelope.scope,
            granularity=envelope.granularity,
            period_start=period_start,
            period_end=period_end,
            schema_version=envelope.schema_version,
            payload=envelope.payload,
            diagnostics=envelope.diagnostics,
            input_refs=[ref.model_dump(mode="json") for ref in envelope.input_refs],
        )
        pass_output_id = int(getattr(row, "id") or 0) or None
    except Exception as exc:  # noqa: BLE001
        record_metric(
            name="pipeline.trends.pass_outputs.persist_failed_total",
            value=1,
            unit="count",
        )
        log.warning(
            "Ideas pass output persist failed granularity={} period_start={} period_end={} error_type={} error={}",
            normalized_granularity,
            period_start.isoformat(),
            period_end.isoformat(),
            type(exc).__name__,
            service._sanitize_error_message(str(exc)),
        )
        raise

    record_metric(
        name="pipeline.trends.pass.ideas.persisted_total",
        value=1,
        unit="count",
    )

    note_path: Path | None = None
    if status == PassStatus.SUPPRESSED:
        record_metric(
            name="pipeline.trends.pass.ideas.suppressed_total",
            value=1,
            unit="count",
        )
    else:
        _ = run_projection_target(
            enabled=True,
            metric_base="pipeline.trends.projection.ideas_documents",
            record_metric=record_metric,
            log=log.bind(module="pipeline.trends.projection.ideas_documents"),
            failure_message=(
                "Ideas document projection failed pass_output_id={pass_output_id} "
                "error_type={error_type} error={error}"
            ),
            execute=lambda: _persist_ideas_document_projection(
                repository=service.repository,
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                payload=payload,
                scope=scope,
            ),
            warning_context={"pass_output_id": pass_output_id},
            sanitize_error=service._sanitize_error_message,
        )
        note_path = run_projection_target(
            enabled="markdown" in targets,
            metric_base="pipeline.trends.projection.ideas_markdown",
            record_metric=record_metric,
            log=log.bind(module="pipeline.trends.projection.ideas_markdown"),
            failure_message=(
                "Ideas markdown projection failed pass_output_id={pass_output_id} "
                "error_type={error_type} error={error}"
            ),
            execute=lambda: write_markdown_ideas_note(
                repository=cast(Any, service.repository),
                output_dir=Path(service.settings.markdown_output_dir),
                pass_output_id=cast(int, pass_output_id),
                upstream_pass_output_id=upstream_pass_output_id,
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                run_id=run_id,
                status=status.value,
                payload=payload,
                scope=scope,
                topics=list(trend_payload.topics or []),
            ),
            warning_context={"pass_output_id": pass_output_id},
            sanitize_error=service._sanitize_error_message,
        )
        _ = run_projection_target(
            enabled="obsidian" in targets and service.settings.obsidian_vault_path is not None,
            metric_base="pipeline.trends.projection.ideas_obsidian",
            record_metric=record_metric,
            log=log.bind(module="pipeline.trends.projection.ideas_obsidian"),
            failure_message=(
                "Ideas obsidian projection failed pass_output_id={pass_output_id} "
                "error_type={error_type} error={error}"
            ),
            execute=lambda: write_obsidian_ideas_note(
                repository=cast(Any, service.repository),
                vault_path=service.settings.obsidian_vault_path,
                base_folder=service.settings.obsidian_base_folder,
                pass_output_id=cast(int, pass_output_id),
                upstream_pass_output_id=upstream_pass_output_id,
                granularity=normalized_granularity,
                period_start=period_start,
                period_end=period_end,
                run_id=run_id,
                status=status.value,
                payload=payload,
                scope=scope,
                topics=list(trend_payload.topics or []),
            ),
            warning_context={"pass_output_id": pass_output_id},
            sanitize_error=service._sanitize_error_message,
        )

    if isinstance(debug, dict):
        usage = debug.get("usage")
        if isinstance(usage, dict):
            requests = usage.get("requests")
            input_tokens = usage.get("input_tokens")
            output_tokens = usage.get("output_tokens")
            if isinstance(requests, (int, float)):
                record_metric(
                    name="pipeline.trends.pass.ideas.llm_requests_total",
                    value=float(requests),
                    unit="count",
                )
            if isinstance(input_tokens, (int, float)):
                record_metric(
                    name="pipeline.trends.pass.ideas.llm_input_tokens_total",
                    value=float(input_tokens),
                    unit="count",
                )
            if isinstance(output_tokens, (int, float)):
                record_metric(
                    name="pipeline.trends.pass.ideas.llm_output_tokens_total",
                    value=float(output_tokens),
                    unit="count",
                )
        prompt_chars = debug.get("prompt_chars")
        if isinstance(prompt_chars, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.prompt_chars",
                value=float(prompt_chars),
                unit="chars",
            )
        snapshot_pack_chars = debug.get("trend_snapshot_pack_chars")
        if isinstance(snapshot_pack_chars, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.snapshot_pack.chars",
                value=float(snapshot_pack_chars),
                unit="chars",
            )
        cost_usd = debug.get("estimated_cost_usd")
        if isinstance(cost_usd, (int, float)):
            record_metric(
                name="pipeline.trends.pass.ideas.estimated_cost_usd",
                value=float(cost_usd),
                unit="usd",
            )

    tool_calls_total = int(debug.get("tool_calls_total") or 0) if isinstance(debug, dict) else 0
    record_metric(
        name="pipeline.trends.pass.ideas.tool_calls_total",
        value=tool_calls_total,
        unit="count",
    )
    if isinstance(debug, dict):
        tool_call_breakdown = debug.get("tool_call_breakdown")
        if isinstance(tool_call_breakdown, dict):
            for raw_tool_name, raw_count in sorted(tool_call_breakdown.items()):
                if not isinstance(raw_count, (int, float)):
                    continue
                metric_tool_name = metric_token(str(raw_tool_name), max_len=32)
                if not metric_tool_name:
                    continue
                record_metric(
                    name=f"pipeline.trends.pass.ideas.tool.{metric_tool_name}.calls_total",
                    value=float(raw_count),
                    unit="count",
                )

    _record_ideas_debug_artifact(
        service=service,
        run_id=run_id,
        upstream_pass_output_id=upstream_pass_output_id,
        status=status,
        trend_snapshot_pack_md=trend_snapshot_pack_md,
        ideas_payload=payload,
        debug=debug,
    )
    record_metric(
        name="pipeline.trends.pass.ideas.duration_ms",
        value=int((time.perf_counter() - started) * 1000),
        unit="ms",
    )
    return IdeasResult(
        pass_output_id=pass_output_id,
        granularity=normalized_granularity,
        period_start=period_start,
        period_end=period_end,
        title=payload.title,
        status=status.value,
        note_path=note_path,
        upstream_pass_output_id=upstream_pass_output_id,
    )


def run_ideas_topic_streams_stage(
    service: IdeasStageService,
    *,
    run_id: str,
    granularity: str = "day",
    anchor_date: date | None = None,
    llm_model: str | None = None,
) -> IdeasResult:
    results: list[IdeasResult] = []
    for stream in service._topic_streams:
        stream_settings = service._settings_for_topic_stream(stream)
        service_factory = cast(Any, service.__class__)
        child_service = service_factory(
            settings=stream_settings,
            repository=cast(RepositoryPort, service.repository),
            analyzer=service.analyzer,
            triage=service.semantic_triage,
            telegram_sender=service.telegram_sender,
        )
        result = run_ideas_stage(
            child_service,
            run_id=run_id,
            granularity=granularity,
            anchor_date=anchor_date,
            llm_model=llm_model,
            scope=stream.name,
        )
        result.stream = stream.name
        results.append(result)

    service.repository.record_metric(
        run_id=run_id,
        name="pipeline.trends.pass.ideas.streams_total",
        value=len(results),
        unit="count",
    )
    anchor = anchor_date or utc_now().date()
    period_start, period_end = _period_bounds_for_granularity(
        granularity=granularity,
        anchor=anchor,
    )
    if not results:
        return IdeasResult(
            pass_output_id=None,
            granularity=str(granularity or "").strip().lower() or "day",
            period_start=period_start,
            period_end=period_end,
            title="Ideas",
            status=PassStatus.SUPPRESSED.value,
            note_path=None,
            stream_results=[],
        )
    first = results[0]
    return IdeasResult(
        pass_output_id=first.pass_output_id,
        granularity=first.granularity,
        period_start=first.period_start,
        period_end=first.period_end,
        title=first.title,
        status=first.status,
        note_path=first.note_path,
        upstream_pass_output_id=first.upstream_pass_output_id,
        stream=first.stream,
        stream_results=results,
    )
