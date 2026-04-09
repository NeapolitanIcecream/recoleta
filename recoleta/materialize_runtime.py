from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from loguru import logger

from recoleta.config import LocalizationConfig
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import (
    write_markdown_ideas_note,
    write_markdown_note,
    write_markdown_trend_note,
    write_obsidian_ideas_note,
    write_obsidian_note,
    write_obsidian_trend_note,
)
from recoleta.publish.item_note_writer import ItemNoteSpec
from recoleta.publish.idea_notes import resolve_ideas_note_path
from recoleta.translation import (
    localized_language_root,
    materialize_localized_languages,
)
from recoleta.trend_materialize import materialize_trend_note_payload
from recoleta.trends import TrendPayload, is_empty_trend_payload


@dataclass(slots=True)
class MaterializeTargetOutputsRequest:
    repository: Any
    target_spec: Any
    granularity: str | None
    generate_pdf: bool
    debug_pdf: bool
    output_language: str | None
    language_code: str | None


@dataclass(slots=True)
class MaterializeLocalizedOutputsRequest:
    repository: Any
    target_spec: Any
    granularity: str | None
    localization: LocalizationConfig


@dataclass(slots=True)
class MaterializeOutputsRequest:
    repository: Any
    target_spec: Any
    granularity: str | None = None
    generate_pdf: bool = False
    debug_pdf: bool = False
    output_language: str | None = None
    site_input_dir: Path | None = None
    site_output_dir: Path | None = None
    localization: LocalizationConfig | None = None
    item_export_scope: str = "linked"


@dataclass(slots=True)
class _MaterializeContext:
    repository: Any
    output_dir: Path
    obsidian_vault_path: Path | None
    obsidian_base_folder: str | None
    result: Any
    log: Any
    output_language: str | None
    language_code: str | None
    generate_pdf: bool
    debug_pdf: bool
    item_note_href_by_url: dict[str, str]


@dataclass(frozen=True, slots=True)
class _ObsidianIdeasNoteRequest:
    ctx: _MaterializeContext
    row: Any
    payload: TrendIdeasPayload
    idea_ctx: dict[str, Any]
    period_start: datetime
    period_end: datetime


@dataclass(frozen=True, slots=True)
class _LocalizedTrendNoteRequest:
    repository: Any
    language_root: Path
    language_code: str
    document: Any
    doc_id: int
    payload: TrendPayload
    trend_site_exclude: bool
    item_note_href_by_url: dict[str, str]


def _materialize_module() -> Any:
    import recoleta.materialize as materialize_module

    return materialize_module


def coerce_target_outputs_request(
    *,
    request: MaterializeTargetOutputsRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> MaterializeTargetOutputsRequest:
    if request is not None:
        return request
    return MaterializeTargetOutputsRequest(
        repository=legacy_kwargs["repository"],
        target_spec=legacy_kwargs["target_spec"],
        granularity=legacy_kwargs.get("granularity"),
        generate_pdf=bool(legacy_kwargs.get("generate_pdf", False)),
        debug_pdf=bool(legacy_kwargs.get("debug_pdf", False)),
        output_language=legacy_kwargs.get("output_language"),
        language_code=legacy_kwargs.get("language_code"),
    )


def coerce_localized_outputs_request(
    *,
    request: MaterializeLocalizedOutputsRequest | None = None,
    legacy_kwargs: dict[str, Any],
) -> MaterializeLocalizedOutputsRequest:
    if request is not None:
        return request
    return MaterializeLocalizedOutputsRequest(
        repository=legacy_kwargs["repository"],
        target_spec=legacy_kwargs["target_spec"],
        granularity=legacy_kwargs.get("granularity"),
        localization=legacy_kwargs["localization"],
    )


def coerce_outputs_request(
    *, request: MaterializeOutputsRequest | None = None, legacy_kwargs: dict[str, Any]
) -> MaterializeOutputsRequest:
    if request is not None:
        return request
    return MaterializeOutputsRequest(
        repository=legacy_kwargs["repository"],
        target_spec=legacy_kwargs["target_spec"],
        granularity=legacy_kwargs.get("granularity"),
        generate_pdf=bool(legacy_kwargs.get("generate_pdf", False)),
        debug_pdf=bool(legacy_kwargs.get("debug_pdf", False)),
        output_language=legacy_kwargs.get("output_language"),
        site_input_dir=legacy_kwargs.get("site_input_dir"),
        site_output_dir=legacy_kwargs.get("site_output_dir"),
        localization=legacy_kwargs.get("localization"),
        item_export_scope=str(
            legacy_kwargs.get("item_export_scope", "linked") or "linked"
        ),
    )


def _build_item_note_spec(
    *,
    repository: Any,
    item: Any,
    analysis: Any,
    summary_text: str,
    language_code: str | None,
) -> ItemNoteSpec:
    return ItemNoteSpec(
        item_id=int(getattr(item, "id")),
        title=str(getattr(item, "title", "") or ""),
        source=str(getattr(item, "source", "") or ""),
        canonical_url=str(getattr(item, "canonical_url", "") or ""),
        published_at=getattr(item, "published_at", None),
        authors=repository.decode_list(getattr(item, "authors", None)),
        topics=repository.decode_list(getattr(analysis, "topics_json", None)),
        relevance_score=float(getattr(analysis, "relevance_score", 0.0) or 0.0),
        run_id="materialize-outputs",
        summary=summary_text,
        language_code=language_code,
    )


def _build_materialize_context(
    *, request: MaterializeTargetOutputsRequest
) -> _MaterializeContext:
    materialize_module = _materialize_module()
    output_dir = request.target_spec.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    materialize_module._reset_managed_output_dirs(output_dir)
    obsidian_vault_path, obsidian_base_folder = (
        materialize_module._resolved_obsidian_target(target_spec=request.target_spec)
    )
    result = materialize_module.MaterializeOutputResult(output_dir=output_dir)
    log = logger.bind(module="materialize.outputs", output_dir=str(output_dir))
    return _MaterializeContext(
        repository=request.repository,
        output_dir=output_dir,
        obsidian_vault_path=obsidian_vault_path,
        obsidian_base_folder=obsidian_base_folder,
        result=result,
        log=log,
        output_language=request.output_language,
        language_code=request.language_code,
        generate_pdf=request.generate_pdf,
        debug_pdf=request.debug_pdf,
        item_note_href_by_url={},
    )


def _localized_analysis_summary(*, ctx: _MaterializeContext, analysis: Any) -> str:
    materialize_module = _materialize_module()
    analysis_id = int(getattr(analysis, "id") or 0)
    payload = materialize_module._localized_output_payload(
        repository=ctx.repository,
        source_kind="analysis",
        source_record_id=analysis_id,
        language_code=ctx.language_code,
    )
    if isinstance(payload, dict):
        return str(payload.get("summary") or "").strip()
    return str(getattr(analysis, "summary", "") or "")


def _record_item_note_href(
    *, ctx: _MaterializeContext, item: Any, note_path: Path
) -> None:
    canonical_url = str(getattr(item, "canonical_url", "") or "").strip()
    if canonical_url:
        ctx.item_note_href_by_url[canonical_url] = f"../Inbox/{note_path.name}"


def _materialize_item_notes(*, ctx: _MaterializeContext) -> None:
    materialize_module = _materialize_module()
    for item, analysis in materialize_module._materialize_item_pairs(
        repository=ctx.repository
    ):
        item_id = getattr(item, "id", None)
        if item_id is None:
            continue
        summary_text = _localized_analysis_summary(ctx=ctx, analysis=analysis)
        spec = _build_item_note_spec(
            repository=ctx.repository,
            item=item,
            analysis=analysis,
            summary_text=summary_text,
            language_code=ctx.language_code,
        )
        note_path = write_markdown_note(output_dir=ctx.output_dir, spec=spec)
        _record_item_note_href(ctx=ctx, item=item, note_path=note_path)
        ctx.result.item_notes_total += 1
        _materialize_obsidian_item_note(ctx=ctx, spec=spec, item_id=int(item_id))


def _materialize_obsidian_item_note(
    *, ctx: _MaterializeContext, spec: ItemNoteSpec, item_id: int
) -> None:
    if ctx.obsidian_vault_path is None or ctx.obsidian_base_folder is None:
        return
    try:
        write_obsidian_note(
            vault_path=ctx.obsidian_vault_path,
            base_folder=ctx.obsidian_base_folder,
            spec=spec,
        )
        ctx.result.obsidian_notes_total += 1
    except Exception as exc:  # noqa: BLE001
        ctx.result.obsidian_failures_total += 1
        ctx.log.bind(item_id=item_id).warning(
            "item obsidian materialization failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )


def _load_trend_payload_for_output(
    *, ctx: _MaterializeContext, document: Any
) -> tuple[TrendPayload, Any]:
    materialize_module = _materialize_module()
    doc_id = int(getattr(document, "id") or 0)
    payload = materialize_module._localized_output_payload(
        repository=ctx.repository,
        source_kind="trend_synthesis",
        source_record_id=doc_id,
        language_code=ctx.language_code,
    )
    if payload is not None:
        return TrendPayload.model_validate(payload), None
    return materialize_module._load_trend_payload(
        repository=ctx.repository, document=document
    )


def _trend_site_exclude(
    *, ctx: _MaterializeContext, payload: TrendPayload, trend_projection: Any
) -> bool:
    materialize_module = _materialize_module()
    trend_site_exclude = is_empty_trend_payload(payload)
    if trend_projection is None or trend_projection.pass_output_id is None:
        return trend_site_exclude
    source_pass_output = ctx.repository.get_pass_output(
        pass_output_id=int(trend_projection.pass_output_id)
    )
    if source_pass_output is None:
        return trend_site_exclude
    return materialize_module._trend_pass_output_has_empty_corpus(
        row=source_pass_output
    )


def _materialize_trend_markdown_note(
    *,
    ctx: _MaterializeContext,
    document: Any,
    payload: TrendPayload,
    trend_projection: Any,
) -> tuple[Path, Any, bool]:
    doc_id = int(getattr(document, "id") or 0)
    trend_site_exclude = _trend_site_exclude(
        ctx=ctx, payload=payload, trend_projection=trend_projection
    )
    materialized = materialize_trend_note_payload(
        repository=ctx.repository,
        payload=payload,
        markdown_output_dir=ctx.output_dir,
        output_language=ctx.output_language,
        language_code=ctx.language_code,
        item_note_href_by_url=ctx.item_note_href_by_url,
    )
    note_path = write_markdown_trend_note(
        output_dir=ctx.output_dir,
        trend_doc_id=doc_id,
        title=materialized.title,
        granularity=str(getattr(document, "granularity", "") or ""),
        period_start=getattr(document, "period_start"),
        period_end=getattr(document, "period_end"),
        run_id="materialize-outputs",
        overview_md=materialized.overview_md,
        topics=list(materialized.topics),
        clusters=materialized.clusters,
        output_language=ctx.output_language,
        pass_output_id=trend_projection.pass_output_id
        if trend_projection is not None
        else None,
        pass_kind=trend_projection.pass_kind if trend_projection is not None else None,
        site_exclude=trend_site_exclude,
        language_code=ctx.language_code,
    )
    ctx.result.trend_notes_total += 1
    ctx.result.doc_ref_rewrites_total += (
        materialized.rewrite_stats.doc_ref_occurrences_total
    )
    ctx.result.doc_ref_resolved_total += (
        materialized.rewrite_stats.doc_ref_resolved_total
    )
    ctx.result.doc_ref_unresolved_total += (
        materialized.rewrite_stats.doc_ref_unresolved_total
    )
    ctx.result.canonical_link_rewrites_total += (
        materialized.rewrite_stats.canonical_link_rewrites_total
    )
    return note_path, materialized, trend_site_exclude


def _materialize_obsidian_trend_note(
    *,
    ctx: _MaterializeContext,
    document: Any,
    materialized: Any,
    trend_projection: Any,
    trend_site_exclude: bool,
) -> None:
    if ctx.obsidian_vault_path is None or ctx.obsidian_base_folder is None:
        return
    doc_id = int(getattr(document, "id") or 0)
    try:
        write_obsidian_trend_note(
            vault_path=ctx.obsidian_vault_path,
            base_folder=ctx.obsidian_base_folder,
            trend_doc_id=doc_id,
            title=materialized.title,
            granularity=str(getattr(document, "granularity", "") or ""),
            period_start=getattr(document, "period_start"),
            period_end=getattr(document, "period_end"),
            run_id="materialize-outputs",
            overview_md=materialized.overview_md,
            topics=list(materialized.topics),
            clusters=materialized.clusters,
            output_language=ctx.output_language,
            pass_output_id=trend_projection.pass_output_id
            if trend_projection is not None
            else None,
            pass_kind=trend_projection.pass_kind
            if trend_projection is not None
            else None,
            site_exclude=trend_site_exclude,
            language_code=ctx.language_code,
        )
        ctx.result.obsidian_notes_total += 1
    except Exception as exc:  # noqa: BLE001
        ctx.result.obsidian_failures_total += 1
        ctx.log.bind(doc_id=doc_id).warning(
            "trend obsidian materialization failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )


def _materialize_trend_pdf(
    *, ctx: _MaterializeContext, document: Any, note_path: Path
) -> None:
    if not ctx.generate_pdf:
        return
    materialize_module = _materialize_module()
    doc_id = int(getattr(document, "id") or 0)
    try:
        pdf_result = materialize_module.render_trend_note_pdf_result(
            markdown_path=note_path,
            backend="auto",
            page_mode="continuous",
        )
        ctx.result.trend_pdf_total += 1
        if ctx.debug_pdf:
            debug_dir = note_path.parent / ".pdf-debug" / pdf_result.path.stem
            materialize_module.export_trend_note_pdf_debug_bundle(
                markdown_path=note_path,
                pdf_path=pdf_result.path,
                debug_dir=debug_dir,
                prepared=pdf_result.prepared,
            )
    except Exception as exc:  # noqa: BLE001
        ctx.result.trend_pdf_failures_total += 1
        ctx.log.bind(doc_id=doc_id).warning(
            "trend pdf materialization failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )


def _materialize_trend_notes(
    *, ctx: _MaterializeContext, granularity: str | None
) -> None:
    materialize_module = _materialize_module()
    trend_documents = materialize_module._materialize_trend_documents(
        repository=ctx.repository,
        granularity=granularity,
    )
    ctx.result.trend_docs_total = len(trend_documents)
    for document in trend_documents:
        doc_id = int(getattr(document, "id") or 0)
        try:
            payload, trend_projection = _load_trend_payload_for_output(
                ctx=ctx,
                document=document,
            )
            note_path, materialized, trend_site_exclude = (
                _materialize_trend_markdown_note(
                    ctx=ctx,
                    document=document,
                    payload=payload,
                    trend_projection=trend_projection,
                )
            )
        except Exception as exc:  # noqa: BLE001
            ctx.result.trend_failures_total += 1
            ctx.log.bind(doc_id=doc_id).warning(
                "trend output materialization failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            continue
        _materialize_obsidian_trend_note(
            ctx=ctx,
            document=document,
            materialized=materialized,
            trend_projection=trend_projection,
            trend_site_exclude=trend_site_exclude,
        )
        _materialize_trend_pdf(ctx=ctx, document=document, note_path=note_path)


def _ideas_note_context(
    *, ctx: _MaterializeContext, row: Any, payload: TrendIdeasPayload
) -> dict[str, Any]:
    materialize_module = _materialize_module()
    upstream_pass_output_id = materialize_module._ideas_upstream_pass_output_id(row=row)
    upstream_pass_output = (
        ctx.repository.get_pass_output(pass_output_id=int(upstream_pass_output_id))
        if upstream_pass_output_id is not None
        else None
    )
    ideas_empty_corpus = materialize_module._truthy_flag(
        materialize_module._pass_output_diagnostics(row=row).get("empty_corpus")
    )
    if (
        not ideas_empty_corpus
        and upstream_pass_output is not None
        and materialize_module._trend_pass_output_has_empty_corpus(
            row=upstream_pass_output
        )
    ):
        ideas_empty_corpus = True
    return {
        "upstream_pass_output_id": upstream_pass_output_id,
        "topics": materialize_module._ideas_topics_from_upstream_pass_output(
            repository=ctx.repository,
            pass_output_id=upstream_pass_output_id,
        ),
        "ideas_empty_corpus": ideas_empty_corpus,
        "granularity_value": str(row.granularity or payload.granularity or "day"),
    }


def _cleanup_empty_corpus_idea_outputs(
    *,
    ctx: _MaterializeContext,
    row: Any,
    granularity_value: str,
    period_start: datetime,
) -> None:
    note_path = resolve_ideas_note_path(
        note_dir=ctx.output_dir / "Ideas",
        granularity=granularity_value,
        period_start=period_start,
    )
    note_path.unlink(missing_ok=True)
    if ctx.obsidian_vault_path is None or ctx.obsidian_base_folder is None:
        return
    obsidian_note_path = resolve_ideas_note_path(
        note_dir=ctx.obsidian_vault_path / ctx.obsidian_base_folder / "Ideas",
        granularity=granularity_value,
        period_start=period_start,
    )
    obsidian_note_path.unlink(missing_ok=True)


def _log_obsidian_ideas_failure(
    *,
    ctx: _MaterializeContext,
    pass_output_id: int,
    exc: Exception,
) -> None:
    ctx.result.obsidian_failures_total += 1
    ctx.log.bind(pass_output_id=pass_output_id).warning(
        "ideas obsidian materialization failed error_type={} error={}",
        type(exc).__name__,
        str(exc),
    )


def _obsidian_ideas_note_kwargs(
    *,
    request: _ObsidianIdeasNoteRequest,
    pass_output_id: int,
) -> dict[str, Any]:
    return {
        "repository": request.ctx.repository,
        "vault_path": request.ctx.obsidian_vault_path,
        "base_folder": request.ctx.obsidian_base_folder,
        "pass_output_id": pass_output_id,
        "upstream_pass_output_id": request.idea_ctx["upstream_pass_output_id"],
        "granularity": request.idea_ctx["granularity_value"],
        "period_start": request.period_start,
        "period_end": request.period_end,
        "run_id": str(getattr(request.row, "run_id")),
        "status": str(getattr(request.row, "status")),
        "payload": request.payload,
        "topics": request.idea_ctx["topics"],
        "output_language": request.ctx.output_language,
        "language_code": request.ctx.language_code,
    }


def _materialize_obsidian_ideas_note(
    *,
    request: _ObsidianIdeasNoteRequest,
) -> None:
    if (
        request.ctx.obsidian_vault_path is None
        or request.ctx.obsidian_base_folder is None
    ):
        return
    pass_output_id = int(getattr(request.row, "id") or 0)
    try:
        write_obsidian_ideas_note(
            **_obsidian_ideas_note_kwargs(
                request=request,
                pass_output_id=pass_output_id,
            )
        )
        request.ctx.result.obsidian_notes_total += 1
    except Exception as exc:  # noqa: BLE001
        _log_obsidian_ideas_failure(
            ctx=request.ctx,
            pass_output_id=pass_output_id,
            exc=exc,
        )


def _materialize_idea_notes(
    *, ctx: _MaterializeContext, granularity: str | None
) -> None:
    materialize_module = _materialize_module()
    idea_pass_outputs = materialize_module._materialize_idea_pass_outputs(
        repository=ctx.repository,
        granularity=granularity,
    )
    ctx.result.ideas_outputs_total = len(idea_pass_outputs)
    for row in idea_pass_outputs:
        pass_output_id = int(getattr(row, "id") or 0)
        try:
            localized_idea_payload = (
                materialize_module._localized_idea_payload_for_pass_output(
                    repository=ctx.repository,
                    row=row,
                    language_code=ctx.language_code,
                )
            )
            payload = (
                TrendIdeasPayload.model_validate(localized_idea_payload)
                if localized_idea_payload is not None
                else materialize_module._load_ideas_payload(row=row)
            )
            period_start = getattr(row, "period_start")
            period_end = getattr(row, "period_end")
            if not isinstance(period_start, datetime) or not isinstance(
                period_end, datetime
            ):
                raise ValueError("ideas pass output is missing period bounds")
            idea_ctx = _ideas_note_context(ctx=ctx, row=row, payload=payload)
            if idea_ctx["ideas_empty_corpus"]:
                _cleanup_empty_corpus_idea_outputs(
                    ctx=ctx,
                    row=row,
                    granularity_value=idea_ctx["granularity_value"],
                    period_start=period_start,
                )
                continue
            write_markdown_ideas_note(
                repository=ctx.repository,
                output_dir=ctx.output_dir,
                pass_output_id=pass_output_id,
                upstream_pass_output_id=idea_ctx["upstream_pass_output_id"],
                granularity=idea_ctx["granularity_value"],
                period_start=period_start,
                period_end=period_end,
                run_id=str(getattr(row, "run_id")),
                status=str(getattr(row, "status")),
                payload=payload,
                topics=idea_ctx["topics"],
                output_language=ctx.output_language,
                language_code=ctx.language_code,
            )
            ctx.result.ideas_notes_total += 1
        except Exception as exc:  # noqa: BLE001
            ctx.result.ideas_failures_total += 1
            ctx.log.bind(pass_output_id=pass_output_id).warning(
                "ideas output materialization failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            continue
        _materialize_obsidian_ideas_note(
            request=_ObsidianIdeasNoteRequest(
                ctx=ctx,
                row=row,
                payload=payload,
                idea_ctx=idea_ctx,
                period_start=period_start,
                period_end=period_end,
            )
        )


def materialize_outputs_for_target(*, request: MaterializeTargetOutputsRequest) -> Any:
    ctx = _build_materialize_context(request=request)
    _materialize_item_notes(ctx=ctx)
    _materialize_trend_notes(ctx=ctx, granularity=request.granularity)
    _materialize_idea_notes(ctx=ctx, granularity=request.granularity)
    ctx.log.info(
        "output materialization completed stats={}",
        {
            "item_notes_total": ctx.result.item_notes_total,
            "trend_notes_total": ctx.result.trend_notes_total,
            "trend_docs_total": ctx.result.trend_docs_total,
            "trend_failures_total": ctx.result.trend_failures_total,
            "ideas_notes_total": ctx.result.ideas_notes_total,
            "ideas_outputs_total": ctx.result.ideas_outputs_total,
            "ideas_failures_total": ctx.result.ideas_failures_total,
            "obsidian_notes_total": ctx.result.obsidian_notes_total,
            "obsidian_failures_total": ctx.result.obsidian_failures_total,
            "trend_pdf_total": ctx.result.trend_pdf_total,
            "trend_pdf_failures_total": ctx.result.trend_pdf_failures_total,
            "doc_ref_rewrites_total": ctx.result.doc_ref_rewrites_total,
            "canonical_link_rewrites_total": ctx.result.canonical_link_rewrites_total,
        },
    )
    return ctx.result


def _materialize_localized_item_notes(
    *,
    repository: Any,
    language_root: Path,
    language_code: str,
    item_pairs: list[tuple[Any, Any]],
    item_note_href_by_url: dict[str, str],
) -> None:
    materialize_module = _materialize_module()
    for item, analysis in item_pairs:
        analysis_id = int(getattr(analysis, "id") or 0)
        item_id = int(getattr(item, "id") or 0)
        if analysis_id <= 0 or item_id <= 0:
            continue
        localized_output = repository.get_localized_output(
            source_kind="analysis",
            source_record_id=analysis_id,
            language_code=language_code,
        )
        if localized_output is None:
            continue
        payload = materialize_module._load_localized_payload(row=localized_output) or {}
        summary = str(payload.get("summary") or "").strip()
        if not summary:
            continue
        spec = _build_item_note_spec(
            repository=repository,
            item=item,
            analysis=analysis,
            summary_text=summary,
            language_code=language_code,
        )
        note_path = write_markdown_note(output_dir=language_root, spec=spec)
        canonical_url = str(getattr(item, "canonical_url", "") or "").strip()
        if canonical_url:
            item_note_href_by_url[canonical_url] = f"../Inbox/{note_path.name}"


def _materialize_localized_trend_notes(
    *,
    repository: Any,
    language_root: Path,
    language_code: str,
    trend_documents: list[Any],
    item_note_href_by_url: dict[str, str],
) -> None:
    for document in trend_documents:
        localized_payload = _localized_trend_payload(
            repository=repository,
            document=document,
            language_code=language_code,
        )
        if localized_payload is None:
            continue
        doc_id, payload = localized_payload
        trend_site_exclude = _localized_trend_site_exclude(
            repository=repository,
            document=document,
            payload=payload,
        )
        _write_localized_trend_note(
            request=_LocalizedTrendNoteRequest(
                repository=repository,
                language_root=language_root,
                language_code=language_code,
                document=document,
                doc_id=doc_id,
                payload=payload,
                trend_site_exclude=trend_site_exclude,
                item_note_href_by_url=item_note_href_by_url,
            )
        )


def _localized_trend_payload(
    *,
    repository: Any,
    document: Any,
    language_code: str,
) -> tuple[int, TrendPayload] | None:
    materialize_module = _materialize_module()
    doc_id = int(getattr(document, "id") or 0)
    if doc_id <= 0:
        return None
    localized_output = repository.get_localized_output(
        source_kind="trend_synthesis",
        source_record_id=doc_id,
        language_code=language_code,
    )
    if localized_output is None:
        return None
    payload_json = materialize_module._load_localized_payload(row=localized_output)
    if payload_json is None:
        return None
    try:
        return doc_id, TrendPayload.model_validate(payload_json)
    except Exception:
        return None


def _localized_trend_site_exclude(
    *,
    repository: Any,
    document: Any,
    payload: TrendPayload,
) -> bool:
    materialize_module = _materialize_module()
    trend_site_exclude = is_empty_trend_payload(payload)
    try:
        _source_payload, trend_projection = materialize_module._load_trend_payload(
            repository=repository,
            document=document,
        )
    except Exception:
        return trend_site_exclude
    if trend_projection is None or trend_projection.pass_output_id is None:
        return trend_site_exclude
    source_pass_output = repository.get_pass_output(
        pass_output_id=int(trend_projection.pass_output_id)
    )
    if source_pass_output is None:
        return trend_site_exclude
    return materialize_module._trend_pass_output_has_empty_corpus(
        row=source_pass_output
    )


def _write_localized_trend_note(
    *,
    request: _LocalizedTrendNoteRequest,
) -> None:
    materialized = materialize_trend_note_payload(
        repository=request.repository,
        payload=request.payload,
        markdown_output_dir=request.language_root,
        output_language=request.language_code,
        language_code=request.language_code,
        item_note_href_by_url=request.item_note_href_by_url,
    )
    write_markdown_trend_note(
        output_dir=request.language_root,
        trend_doc_id=request.doc_id,
        title=materialized.title,
        granularity=str(getattr(request.document, "granularity", "") or ""),
        period_start=getattr(request.document, "period_start"),
        period_end=getattr(request.document, "period_end"),
        run_id="materialize-outputs",
        overview_md=materialized.overview_md,
        topics=list(materialized.topics),
        clusters=materialized.clusters,
        output_language=request.language_code,
        site_exclude=request.trend_site_exclude,
        language_code=request.language_code,
    )


def _materialize_localized_idea_notes(
    *,
    repository: Any,
    language_root: Path,
    language_code: str,
    idea_documents: list[Any],
) -> None:
    materialize_module = _materialize_module()
    for document in idea_documents:
        doc_id = int(getattr(document, "id") or 0)
        if doc_id <= 0:
            continue
        localized_output = repository.get_localized_output(
            source_kind="trend_ideas",
            source_record_id=doc_id,
            language_code=language_code,
        )
        if localized_output is None:
            continue
        payload_json = materialize_module._load_localized_payload(row=localized_output)
        if payload_json is None:
            continue
        try:
            payload = TrendIdeasPayload.model_validate(payload_json)
        except Exception:
            continue
        period_start = getattr(document, "period_start")
        period_end = getattr(document, "period_end")
        granularity_value = str(
            getattr(document, "granularity", "") or payload.granularity or "day"
        )
        topics = materialize_module._localized_idea_topics(
            repository=repository,
            granularity=granularity_value,
            period_start=period_start,
            period_end=period_end,
        )
        write_markdown_ideas_note(
            repository=repository,
            output_dir=language_root,
            pass_output_id=None,
            upstream_pass_output_id=None,
            granularity=granularity_value,
            period_start=period_start,
            period_end=period_end,
            run_id="materialize-outputs",
            status=str(getattr(localized_output, "status", "") or "succeeded"),
            payload=payload,
            topics=topics,
            language_code=language_code,
        )


def materialize_localized_outputs(
    *, request: MaterializeLocalizedOutputsRequest
) -> None:
    materialize_module = _materialize_module()
    output_dir = request.target_spec.output_dir.expanduser().resolve()
    languages = materialize_localized_languages(
        repository=request.repository,
        localization=request.localization,
    )
    if not languages:
        return
    item_pairs, trend_documents, idea_documents = (
        materialize_module._materialize_localized_sources(
            repository=request.repository,
            granularity=request.granularity,
        )
    )
    for language_code in languages:
        language_root = localized_language_root(
            output_dir=output_dir,
            language_code=language_code,
        )
        if language_root.exists():
            materialize_module.shutil.rmtree(language_root)
        language_root.mkdir(parents=True, exist_ok=True)
        item_note_href_by_url: dict[str, str] = {}
        _materialize_localized_item_notes(
            repository=request.repository,
            language_root=language_root,
            language_code=language_code,
            item_pairs=item_pairs,
            item_note_href_by_url=item_note_href_by_url,
        )
        _materialize_localized_trend_notes(
            repository=request.repository,
            language_root=language_root,
            language_code=language_code,
            trend_documents=trend_documents,
            item_note_href_by_url=item_note_href_by_url,
        )
        _materialize_localized_idea_notes(
            repository=request.repository,
            language_root=language_root,
            language_code=language_code,
            idea_documents=idea_documents,
        )


def materialize_outputs(*, request: MaterializeOutputsRequest) -> Any:
    materialize_module = _materialize_module()
    normalized_granularity = materialize_module._normalize_granularity(
        request.granularity
    )
    canonical_language_code = materialize_module._canonical_language_code(
        localization=request.localization,
    )
    canonical_output_language = canonical_language_code or request.output_language
    output = materialize_module._materialize_outputs_for_target(
        request=MaterializeTargetOutputsRequest(
            repository=request.repository,
            target_spec=request.target_spec,
            granularity=normalized_granularity,
            generate_pdf=request.generate_pdf,
            debug_pdf=request.debug_pdf,
            output_language=canonical_output_language,
            language_code=canonical_language_code,
        )
    )
    if request.localization is not None:
        materialize_module._materialize_localized_outputs(
            request=MaterializeLocalizedOutputsRequest(
                repository=request.repository,
                target_spec=request.target_spec,
                granularity=normalized_granularity,
                localization=request.localization,
            )
        )

    site_manifest_path: Path | None = None
    if request.site_input_dir is not None and request.site_output_dir is not None:
        normalized_item_export_scope = (
            str(request.item_export_scope or "").strip().lower() or "linked"
        )
        site_export_kwargs: dict[str, Any] = {
            "input_dir": request.site_input_dir,
            "output_dir": request.site_output_dir,
            "default_language_code": (
                str(request.localization.site_default_language_code)
                if request.localization is not None
                else None
            ),
        }
        if normalized_item_export_scope != "linked":
            site_export_kwargs["item_export_scope"] = normalized_item_export_scope
        site_manifest_path = materialize_module.export_trend_static_site(
            **site_export_kwargs
        )
        logger.bind(
            module="materialize.outputs.site",
            input_dir=str(request.site_input_dir),
            output_dir=str(request.site_output_dir),
        ).info("site materialization completed")

    return materialize_module.MaterializeOutputsResult(
        output=output,
        site_manifest_path=site_manifest_path,
    )
