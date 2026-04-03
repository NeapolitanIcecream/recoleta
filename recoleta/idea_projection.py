from __future__ import annotations

from dataclasses import dataclass
import json
from datetime import datetime
from typing import Any

from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.provenance import build_projection_provenance, inject_projection_provenance


@dataclass(frozen=True, slots=True)
class IdeaProjectionRequest:
    repository: Any
    pass_output_id: int
    upstream_pass_output_id: int | None
    granularity: str
    period_start: datetime
    period_end: datetime
    payload: TrendIdeasPayload
    pass_kind: str = "trend_ideas"
    upstream_pass_kind: str | None = "trend_synthesis"


def render_idea_document_chunk_text(idea: Any) -> str:
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
        "Anti-thesis: " + str(getattr(idea, "anti_thesis", "") or "").strip(),
        f"Why now: {str(getattr(idea, 'why_now', '') or '').strip()}",
        f"What changed: {str(getattr(idea, 'what_changed', '') or '').strip()}",
        "Validation next step: "
        + str(getattr(idea, "validation_next_step", "") or "").strip(),
    ]
    if evidence_reasons:
        lines.append("Evidence: " + " | ".join(evidence_reasons))
    return "\n".join(line for line in lines if str(line).strip()).strip()


def persist_idea_document_projection(request: IdeaProjectionRequest) -> int:
    doc = request.repository.upsert_document_for_idea(
        granularity=request.granularity,
        period_start=request.period_start,
        period_end=request.period_end,
        title=str(request.payload.title or "").strip() or "Ideas",
    )
    doc_id = int(getattr(doc, "id") or 0)
    if doc_id <= 0:
        raise RuntimeError("idea document projection did not return a document id")

    request.repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=0,
        kind="summary",
        text_value=str(request.payload.summary_md or "").strip() or "(empty)",
        start_char=0,
        end_char=None,
        source_content_type="trend_ideas_summary",
    )

    next_chunk_index = 1
    for idea in list(request.payload.ideas or []):
        text_value = render_idea_document_chunk_text(idea)
        if not text_value:
            continue
        request.repository.upsert_document_chunk(
            doc_id=doc_id,
            chunk_index=next_chunk_index,
            kind="content",
            text_value=text_value,
            start_char=0,
            end_char=None,
            source_content_type="trend_idea",
        )
        next_chunk_index += 1

    request.repository.upsert_document_chunk(
        doc_id=doc_id,
        chunk_index=next_chunk_index,
        kind="meta",
        text_value=json.dumps(
            inject_projection_provenance(
                payload=request.payload.model_dump(mode="json"),
                provenance=build_projection_provenance(
                    pass_output_id=request.pass_output_id,
                    pass_kind=request.pass_kind,
                    upstream_pass_output_id=request.upstream_pass_output_id,
                    upstream_pass_kind=(
                        request.upstream_pass_kind
                        if request.upstream_pass_output_id is not None
                        else None
                    ),
                ),
            ),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        start_char=0,
        end_char=None,
        source_content_type="trend_ideas_payload_json",
    )
    request.repository.delete_document_chunks(
        doc_id=doc_id,
        chunk_index_gte=next_chunk_index + 1,
    )
    return doc_id
