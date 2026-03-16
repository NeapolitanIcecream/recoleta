from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, cast

from loguru import logger
from sqlalchemy import and_, desc, func
from sqlalchemy.orm import aliased
from sqlmodel import Session, select

from recoleta.models import (
    Analysis,
    Document,
    PassOutput,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_PUBLISHED,
    Item,
    ItemStreamState,
)
from recoleta.publish import (
    export_trend_note_pdf_debug_bundle,
    render_trend_note_pdf_result,
    write_markdown_ideas_note,
    write_markdown_note,
    write_markdown_trend_note,
    write_obsidian_ideas_note,
    write_obsidian_note,
    write_obsidian_trend_note,
)
from recoleta.publish.idea_notes import resolve_ideas_note_path
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.provenance import (
    ProjectionProvenance,
    projection_provenance_from_mapping,
)
from recoleta.site import export_trend_static_site
from recoleta.trend_materialize import materialize_trend_note_payload
from recoleta.trends import TrendPayload, is_empty_trend_payload
from recoleta.types import DEFAULT_TOPIC_STREAM


@dataclass(slots=True)
class MaterializeScopeSpec:
    scope: str
    output_dir: Path
    obsidian_vault_path: Path | None = None
    obsidian_base_folder: str | None = None


@dataclass(slots=True)
class MaterializeScopeResult:
    scope: str
    output_dir: Path
    item_notes_total: int = 0
    trend_notes_total: int = 0
    trend_docs_total: int = 0
    trend_failures_total: int = 0
    ideas_notes_total: int = 0
    ideas_outputs_total: int = 0
    ideas_failures_total: int = 0
    obsidian_notes_total: int = 0
    obsidian_failures_total: int = 0
    trend_pdf_total: int = 0
    trend_pdf_failures_total: int = 0
    doc_ref_rewrites_total: int = 0
    doc_ref_resolved_total: int = 0
    doc_ref_unresolved_total: int = 0
    canonical_link_rewrites_total: int = 0


@dataclass(slots=True)
class MaterializeOutputsResult:
    scopes: list[MaterializeScopeResult]
    site_manifest_path: Path | None = None


def _normalize_granularity(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip().lower()
    if not normalized:
        return None
    if normalized not in {"day", "week", "month"}:
        raise ValueError("granularity must be one of: day, week, month")
    return normalized


def _materialize_item_pairs(*, repository: Any, scope: str) -> list[tuple[Any, Any]]:
    stream_state = aliased(ItemStreamState)
    with Session(repository.engine) as session:
        event_at = func.coalesce(
            cast(Any, Item.published_at), cast(Any, Item.created_at)
        )
        statement = (
            select(Item, Analysis)
            .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
            .join(
                stream_state,
                and_(
                    cast(Any, stream_state.item_id) == cast(Any, Item.id),
                    cast(Any, stream_state.stream) == scope,
                ),
            )
            .where(
                cast(Any, Analysis.scope) == scope,
                cast(Any, stream_state.state).in_(
                    [ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]
                ),
            )
            .order_by(desc(cast(Any, event_at)), desc(cast(Any, Item.id)))
        )
        return list(session.exec(statement))


def _materialize_trend_documents(
    *,
    repository: Any,
    scope: str,
    granularity: str | None,
) -> list[Document]:
    with Session(repository.engine) as session:
        statement = select(Document).where(
            Document.doc_type == "trend",
            cast(Any, Document.scope) == scope,
        )
        if granularity is not None:
            statement = statement.where(Document.granularity == granularity)
        statement = statement.order_by(
            cast(Any, Document.period_start),
            cast(Any, Document.id),
        )
        return list(session.exec(statement))


def _load_trend_payload(
    *,
    repository: Any,
    document: Any,
) -> tuple[TrendPayload, ProjectionProvenance | None]:
    doc_id = int(getattr(document, "id") or 0)
    if doc_id > 0:
        meta_chunk = repository.read_document_chunk(doc_id=doc_id, chunk_index=1)
        if meta_chunk is not None:
            try:
                loaded = json.loads(str(getattr(meta_chunk, "text", "") or ""))
                return (
                    TrendPayload.model_validate(loaded),
                    projection_provenance_from_mapping(loaded),
                )
            except Exception:
                pass

    summary_chunk = (
        repository.read_document_chunk(doc_id=doc_id, chunk_index=0)
        if doc_id > 0
        else None
    )
    overview_md = str(getattr(summary_chunk, "text", "") or "").strip() or "(empty)"
    period_start = getattr(document, "period_start", None)
    period_end = getattr(document, "period_end", None)
    if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
        raise ValueError(f"trend document {doc_id} is missing period bounds")
    granularity = str(getattr(document, "granularity", "") or "").strip().lower()
    if granularity not in {"day", "week", "month"}:
        raise ValueError(f"trend document {doc_id} has invalid granularity")
    return (
        TrendPayload(
            title=str(getattr(document, "title", "") or "Trend").strip() or "Trend",
            granularity=granularity,
            period_start=period_start.astimezone(UTC).isoformat(),
            period_end=period_end.astimezone(UTC).isoformat(),
            overview_md=overview_md,
            topics=[],
            clusters=[],
            highlights=[],
        ),
        None,
    )


def _materialize_idea_pass_outputs(
    *,
    repository: Any,
    scope: str,
    granularity: str | None,
) -> list[PassOutput]:
    with Session(repository.engine) as session:
        statement = select(PassOutput).where(
            PassOutput.pass_kind == "trend_ideas",
            cast(Any, PassOutput.status).in_(("succeeded", "suppressed")),
            cast(Any, PassOutput.scope) == scope,
        )
        if granularity is not None:
            statement = statement.where(PassOutput.granularity == granularity)
        statement = statement.order_by(
            desc(cast(Any, PassOutput.created_at)),
            desc(cast(Any, PassOutput.id)),
        )
        rows = list(session.exec(statement))

    selected: list[PassOutput] = []
    seen_windows: set[tuple[str | None, datetime | None, datetime | None]] = set()
    for row in rows:
        key = (row.granularity, row.period_start, row.period_end)
        if key in seen_windows:
            continue
        seen_windows.add(key)
        selected.append(row)
    selected.sort(
        key=lambda row: (
            row.period_start or datetime.min.replace(tzinfo=UTC),
            row.period_end or datetime.min.replace(tzinfo=UTC),
            row.id or 0,
        )
    )
    return selected


def _load_ideas_payload(*, row: PassOutput) -> TrendIdeasPayload:
    return TrendIdeasPayload.model_validate(json.loads(str(row.payload_json or "{}")))


def _truthy_flag(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    normalized = str(value or "").strip().lower()
    return normalized in {"1", "true", "yes", "on"}


def _trend_pass_output_has_empty_corpus(*, row: Any) -> bool:
    diagnostics = _pass_output_diagnostics(row=row)
    if isinstance(diagnostics, dict):
        if _truthy_flag(diagnostics.get("empty_corpus")):
            return True
        debug = diagnostics.get("debug")
        if isinstance(debug, dict) and _truthy_flag(debug.get("empty_corpus")):
            return True
    try:
        payload = TrendPayload.model_validate(json.loads(str(getattr(row, "payload_json", "") or "{}")))
    except Exception:
        return False
    return is_empty_trend_payload(payload)


def _pass_output_diagnostics(*, row: Any) -> dict[str, Any]:
    try:
        loaded = json.loads(str(getattr(row, "diagnostics_json", "") or "{}"))
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


def _ideas_upstream_pass_output_id(*, row: PassOutput) -> int | None:
    try:
        input_refs = json.loads(str(row.input_refs_json or "[]"))
    except Exception:
        return None
    if not isinstance(input_refs, list):
        return None
    for ref in input_refs:
        if not isinstance(ref, dict):
            continue
        raw_pass_output_id = ref.get("pass_output_id")
        if raw_pass_output_id is None:
            continue
        try:
            pass_output_id = int(raw_pass_output_id)
        except Exception:
            continue
        if pass_output_id > 0:
            return pass_output_id
    return None


def _ideas_topics_from_upstream_pass_output(
    *,
    repository: Any,
    pass_output_id: int | None,
) -> list[str]:
    if pass_output_id is None:
        return []
    row = repository.get_pass_output(pass_output_id=pass_output_id)
    if row is None:
        return []
    try:
        payload = TrendPayload.model_validate(json.loads(str(row.payload_json or "{}")))
    except Exception:
        return []
    return [str(topic).strip() for topic in payload.topics or [] if str(topic).strip()]


def _materialize_scope_outputs(
    *,
    repository: Any,
    scope_spec: MaterializeScopeSpec,
    granularity: str | None,
    generate_pdf: bool,
    debug_pdf: bool,
    output_language: str | None,
) -> MaterializeScopeResult:
    output_dir = scope_spec.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    obsidian_vault_path = (
        scope_spec.obsidian_vault_path.expanduser().resolve()
        if scope_spec.obsidian_vault_path is not None
        else None
    )
    obsidian_base_folder = str(scope_spec.obsidian_base_folder or "").strip() or None
    result = MaterializeScopeResult(
        scope=scope_spec.scope,
        output_dir=output_dir,
    )
    log = logger.bind(
        module="materialize.outputs.scope",
        scope=scope_spec.scope,
        output_dir=str(output_dir),
    )

    item_note_href_by_url: dict[str, str] = {}
    for item, analysis in _materialize_item_pairs(
        repository=repository,
        scope=scope_spec.scope,
    ):
        item_id = getattr(item, "id", None)
        if item_id is None:
            continue
        note_path = write_markdown_note(
            output_dir=output_dir,
            item_id=int(item_id),
            title=str(getattr(item, "title", "") or ""),
            source=str(getattr(item, "source", "") or ""),
            canonical_url=str(getattr(item, "canonical_url", "") or ""),
            published_at=getattr(item, "published_at", None),
            authors=repository.decode_list(getattr(item, "authors", None)),
            topics=repository.decode_list(getattr(analysis, "topics_json", None)),
            relevance_score=float(getattr(analysis, "relevance_score", 0.0) or 0.0),
            run_id="materialize-outputs",
            summary=str(getattr(analysis, "summary", "") or ""),
        )
        canonical_url = str(getattr(item, "canonical_url", "") or "").strip()
        if canonical_url:
            item_note_href_by_url[canonical_url] = (
                f"../Inbox/{note_path.name}"
            )
        result.item_notes_total += 1
        if obsidian_vault_path is not None and obsidian_base_folder is not None:
            try:
                write_obsidian_note(
                    vault_path=obsidian_vault_path,
                    base_folder=obsidian_base_folder,
                    item_id=int(item_id),
                    title=str(getattr(item, "title", "") or ""),
                    source=str(getattr(item, "source", "") or ""),
                    canonical_url=canonical_url,
                    published_at=getattr(item, "published_at", None),
                    authors=repository.decode_list(getattr(item, "authors", None)),
                    topics=repository.decode_list(getattr(analysis, "topics_json", None)),
                    relevance_score=float(
                        getattr(analysis, "relevance_score", 0.0) or 0.0
                    ),
                    run_id="materialize-outputs",
                    summary=str(getattr(analysis, "summary", "") or ""),
                )
                result.obsidian_notes_total += 1
            except Exception as exc:  # noqa: BLE001
                result.obsidian_failures_total += 1
                log.bind(item_id=int(item_id)).warning(
                    "item obsidian materialization failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )

    trend_documents = _materialize_trend_documents(
        repository=repository,
        scope=scope_spec.scope,
        granularity=granularity,
    )
    result.trend_docs_total = len(trend_documents)
    for document in trend_documents:
        doc_id = int(getattr(document, "id") or 0)
        try:
            payload, trend_projection = _load_trend_payload(
                repository=repository,
                document=document,
            )
            trend_site_exclude = is_empty_trend_payload(payload)
            if trend_projection is not None and trend_projection.pass_output_id is not None:
                source_pass_output = repository.get_pass_output(
                    pass_output_id=int(trend_projection.pass_output_id)
                )
                if source_pass_output is not None:
                    trend_site_exclude = _trend_pass_output_has_empty_corpus(
                        row=source_pass_output
                    )
            materialized = materialize_trend_note_payload(
                repository=repository,
                payload=payload,
                markdown_output_dir=output_dir,
                output_language=output_language,
                item_note_href_by_url=item_note_href_by_url,
                scope=scope_spec.scope,
            )
            note_path = write_markdown_trend_note(
                output_dir=output_dir,
                trend_doc_id=doc_id,
                title=materialized.title,
                granularity=str(getattr(document, "granularity", "") or ""),
                period_start=cast(datetime, getattr(document, "period_start")),
                period_end=cast(datetime, getattr(document, "period_end")),
                run_id="materialize-outputs",
                overview_md=materialized.overview_md,
                topics=list(materialized.topics),
                evolution=materialized.evolution,
                history_window_refs=materialized.history_window_refs,
                clusters=materialized.clusters,
                highlights=materialized.highlights,
                output_language=output_language,
                pass_output_id=(
                    trend_projection.pass_output_id
                    if trend_projection is not None
                    else None
                ),
                pass_kind=(
                    trend_projection.pass_kind if trend_projection is not None else None
                ),
                site_exclude=trend_site_exclude,
            )
            result.trend_notes_total += 1
            result.doc_ref_rewrites_total += (
                materialized.rewrite_stats.doc_ref_occurrences_total
            )
            result.doc_ref_resolved_total += (
                materialized.rewrite_stats.doc_ref_resolved_total
            )
            result.doc_ref_unresolved_total += (
                materialized.rewrite_stats.doc_ref_unresolved_total
            )
            result.canonical_link_rewrites_total += (
                materialized.rewrite_stats.canonical_link_rewrites_total
            )
        except Exception as exc:  # noqa: BLE001
            result.trend_failures_total += 1
            log.bind(doc_id=doc_id).warning(
                "trend output materialization failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            continue
        if obsidian_vault_path is not None and obsidian_base_folder is not None:
            try:
                write_obsidian_trend_note(
                    vault_path=obsidian_vault_path,
                    base_folder=obsidian_base_folder,
                    trend_doc_id=doc_id,
                    title=materialized.title,
                    granularity=str(getattr(document, "granularity", "") or ""),
                    period_start=cast(datetime, getattr(document, "period_start")),
                    period_end=cast(datetime, getattr(document, "period_end")),
                    run_id="materialize-outputs",
                    overview_md=materialized.overview_md,
                    topics=list(materialized.topics),
                    evolution=materialized.evolution,
                    history_window_refs=materialized.history_window_refs,
                    clusters=materialized.clusters,
                    highlights=materialized.highlights,
                    output_language=output_language,
                    pass_output_id=(
                        trend_projection.pass_output_id
                        if trend_projection is not None
                        else None
                    ),
                    pass_kind=(
                        trend_projection.pass_kind
                        if trend_projection is not None
                        else None
                    ),
                    site_exclude=trend_site_exclude,
                )
                result.obsidian_notes_total += 1
            except Exception as exc:  # noqa: BLE001
                result.obsidian_failures_total += 1
                log.bind(doc_id=doc_id).warning(
                    "trend obsidian materialization failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )

        if not generate_pdf:
            continue
        try:
            pdf_result = render_trend_note_pdf_result(
                markdown_path=note_path,
                backend="auto",
                page_mode="continuous",
            )
            result.trend_pdf_total += 1
            if debug_pdf:
                debug_dir = note_path.parent / ".pdf-debug" / pdf_result.path.stem
                export_trend_note_pdf_debug_bundle(
                    markdown_path=note_path,
                    pdf_path=pdf_result.path,
                    debug_dir=debug_dir,
                    prepared=pdf_result.prepared,
                )
        except Exception as exc:  # noqa: BLE001
            result.trend_pdf_failures_total += 1
            log.bind(doc_id=doc_id).warning(
                "trend pdf materialization failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )

    idea_pass_outputs = _materialize_idea_pass_outputs(
        repository=repository,
        scope=scope_spec.scope,
        granularity=granularity,
    )
    result.ideas_outputs_total = len(idea_pass_outputs)
    for row in idea_pass_outputs:
        pass_output_id = int(getattr(row, "id") or 0)
        try:
            payload = _load_ideas_payload(row=row)
            upstream_pass_output_id = _ideas_upstream_pass_output_id(row=row)
            upstream_pass_output = (
                repository.get_pass_output(pass_output_id=int(upstream_pass_output_id))
                if upstream_pass_output_id is not None
                else None
            )
            ideas_empty_corpus = _truthy_flag(
                _pass_output_diagnostics(row=row).get("empty_corpus")
            )
            if (
                not ideas_empty_corpus
                and upstream_pass_output is not None
                and _trend_pass_output_has_empty_corpus(row=upstream_pass_output)
            ):
                ideas_empty_corpus = True
            topics = _ideas_topics_from_upstream_pass_output(
                repository=repository,
                pass_output_id=upstream_pass_output_id,
            )
            period_start = row.period_start
            period_end = row.period_end
            if not isinstance(period_start, datetime) or not isinstance(period_end, datetime):
                raise ValueError("ideas pass output is missing period bounds")
            if ideas_empty_corpus:
                note_path = resolve_ideas_note_path(
                    note_dir=output_dir / "Ideas",
                    granularity=str(row.granularity or payload.granularity or "day"),
                    period_start=period_start,
                )
                note_path.unlink(missing_ok=True)
                if obsidian_vault_path is not None and obsidian_base_folder is not None:
                    obsidian_note_path = resolve_ideas_note_path(
                        note_dir=obsidian_vault_path / obsidian_base_folder / "Ideas",
                        granularity=str(row.granularity or payload.granularity or "day"),
                        period_start=period_start,
                    )
                    obsidian_note_path.unlink(missing_ok=True)
                continue
            _ = write_markdown_ideas_note(
                repository=repository,
                output_dir=output_dir,
                pass_output_id=pass_output_id,
                upstream_pass_output_id=upstream_pass_output_id,
                granularity=str(row.granularity or payload.granularity or "day"),
                period_start=period_start,
                period_end=period_end,
                run_id=str(row.run_id),
                status=str(row.status),
                payload=payload,
                scope=scope_spec.scope,
                topics=topics,
            )
            result.ideas_notes_total += 1
        except Exception as exc:  # noqa: BLE001
            result.ideas_failures_total += 1
            log.bind(pass_output_id=pass_output_id).warning(
                "ideas output materialization failed error_type={} error={}",
                type(exc).__name__,
                str(exc),
            )
            continue
        if obsidian_vault_path is not None and obsidian_base_folder is not None:
            try:
                write_obsidian_ideas_note(
                    repository=repository,
                    vault_path=obsidian_vault_path,
                    base_folder=obsidian_base_folder,
                    pass_output_id=pass_output_id,
                    upstream_pass_output_id=upstream_pass_output_id,
                    granularity=str(row.granularity or payload.granularity or "day"),
                    period_start=period_start,
                    period_end=period_end,
                    run_id=str(row.run_id),
                    status=str(row.status),
                    payload=payload,
                    scope=scope_spec.scope,
                    topics=topics,
                )
                result.obsidian_notes_total += 1
            except Exception as exc:  # noqa: BLE001
                result.obsidian_failures_total += 1
                log.bind(pass_output_id=pass_output_id).warning(
                    "ideas obsidian materialization failed error_type={} error={}",
                    type(exc).__name__,
                    str(exc),
                )

    log.info(
        "scope materialization completed stats={}",
        {
            "scope": result.scope,
            "item_notes_total": result.item_notes_total,
            "trend_notes_total": result.trend_notes_total,
            "trend_docs_total": result.trend_docs_total,
            "trend_failures_total": result.trend_failures_total,
            "ideas_notes_total": result.ideas_notes_total,
            "ideas_outputs_total": result.ideas_outputs_total,
            "ideas_failures_total": result.ideas_failures_total,
            "obsidian_notes_total": result.obsidian_notes_total,
            "obsidian_failures_total": result.obsidian_failures_total,
            "trend_pdf_total": result.trend_pdf_total,
            "trend_pdf_failures_total": result.trend_pdf_failures_total,
            "doc_ref_rewrites_total": result.doc_ref_rewrites_total,
            "canonical_link_rewrites_total": result.canonical_link_rewrites_total,
        },
    )
    return result


def materialize_outputs(
    *,
    repository: Any,
    scope_specs: list[MaterializeScopeSpec],
    granularity: str | None = None,
    generate_pdf: bool = False,
    debug_pdf: bool = False,
    output_language: str | None = None,
    site_input_dir: Path | None = None,
    site_output_dir: Path | None = None,
) -> MaterializeOutputsResult:
    normalized_granularity = _normalize_granularity(granularity)
    results = [
        _materialize_scope_outputs(
            repository=repository,
            scope_spec=scope_spec,
            granularity=normalized_granularity,
            generate_pdf=generate_pdf,
            debug_pdf=debug_pdf,
            output_language=output_language,
        )
        for scope_spec in scope_specs
    ]

    site_manifest_path: Path | None = None
    if site_input_dir is not None and site_output_dir is not None:
        site_manifest_path = export_trend_static_site(
            input_dir=site_input_dir,
            output_dir=site_output_dir,
        )
        logger.bind(
            module="materialize.outputs.site",
            input_dir=str(site_input_dir),
            output_dir=str(site_output_dir),
        ).info("site materialization completed")

    return MaterializeOutputsResult(
        scopes=results,
        site_manifest_path=site_manifest_path,
    )


def default_scope_specs_for_settings(*, settings: Any) -> list[MaterializeScopeSpec]:
    topic_stream_runtimes = getattr(settings, "topic_stream_runtimes", None)
    if callable(topic_stream_runtimes):
        runtimes = cast(list[Any], topic_stream_runtimes())
        if any(bool(getattr(runtime, "explicit", False)) for runtime in runtimes):
            return [
                MaterializeScopeSpec(
                    scope=str(getattr(runtime, "name", "") or DEFAULT_TOPIC_STREAM),
                    output_dir=Path(getattr(runtime, "markdown_output_dir")),
                    obsidian_vault_path=getattr(settings, "obsidian_vault_path", None),
                    obsidian_base_folder=str(
                        getattr(runtime, "obsidian_base_folder", "") or ""
                    )
                    or None,
                )
                for runtime in runtimes
            ]
    return [
        MaterializeScopeSpec(
            scope=DEFAULT_TOPIC_STREAM,
            output_dir=Path(settings.markdown_output_dir),
            obsidian_vault_path=getattr(settings, "obsidian_vault_path", None),
            obsidian_base_folder=str(
                getattr(settings, "obsidian_base_folder", "") or ""
            )
            or None,
        )
    ]
