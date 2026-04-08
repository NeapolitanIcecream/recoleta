from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from recoleta.passes.base import PassInputRef, PassOutputEnvelope, PassStatus
from recoleta.trends import TrendPayload

TREND_IDEAS_PASS_KIND = "trend_ideas"
TREND_IDEAS_SCHEMA_VERSION = 1
@dataclass(frozen=True, slots=True)
class _TrendIdeasPassOutputRequest:
    run_id: str
    status: PassStatus
    granularity: str
    period_start: datetime
    period_end: datetime
    payload: TrendIdeasPayload
    input_refs: list[PassInputRef] | None = None
    diagnostics: dict[str, Any] | None = None


def _coerce_trend_ideas_pass_output_request(
    *,
    request: _TrendIdeasPassOutputRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _TrendIdeasPassOutputRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return _TrendIdeasPassOutputRequest(
        run_id=str(values["run_id"]),
        status=values["status"],
        granularity=str(values["granularity"]),
        period_start=values["period_start"],
        period_end=values["period_end"],
        payload=values["payload"],
        input_refs=list(values.get("input_refs") or []),
        diagnostics=values.get("diagnostics"),
    )


def _is_chinese_output_language(output_language: str | None) -> bool:
    normalized = str(output_language or "").strip()
    if not normalized:
        return False
    lowered = normalized.lower()
    return lowered.startswith("zh") or "chinese" in lowered or "中文" in normalized


class TrendIdeaEvidenceRef(BaseModel):
    doc_id: int
    chunk_index: int = 0
    reason: str | None = None

    @field_validator("doc_id")
    @classmethod
    def _validate_doc_id(cls, value: int) -> int:
        normalized = int(value)
        if normalized <= 0:
            raise ValueError("doc_id must be > 0")
        return normalized

    @field_validator("chunk_index")
    @classmethod
    def _validate_chunk_index(cls, value: int) -> int:
        normalized = int(value)
        if normalized < 0:
            raise ValueError("chunk_index must be >= 0")
        return normalized


class TrendIdea(BaseModel):
    title: str
    content_md: str
    evidence_refs: list[TrendIdeaEvidenceRef] = Field(default_factory=list)

    @field_validator("title", "content_md")
    @classmethod
    def _validate_required_text(cls, value: str) -> str:
        normalized = " ".join(str(value or "").split()).strip()
        if not normalized:
            raise ValueError("idea text fields must not be empty")
        return normalized


class TrendIdeasPayload(BaseModel):
    title: str
    granularity: str
    period_start: str
    period_end: str
    summary_md: str
    ideas: list[TrendIdea] = Field(default_factory=list)

    @field_validator("title", "granularity", "period_start", "period_end", "summary_md")
    @classmethod
    def _validate_required_text(cls, value: str) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            raise ValueError("payload text fields must not be empty")
        return normalized


def build_empty_trend_ideas_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    output_language: str | None = None,
) -> TrendIdeasPayload:
    normalized_granularity = str(granularity or "").strip().lower() or "day"
    if _is_chinese_output_language(output_language):
        title = "本期暂无可发布研究趋势"
        summary_md = "该周期没有可用文档，因此不输出机会想法。"
    else:
        title = "No publishable ideas for this period"
        summary_md = "No documents are available for this period, so no opportunity ideas are emitted."
    return TrendIdeasPayload(
        title=title,
        granularity=normalized_granularity,
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        summary_md=summary_md,
        ideas=[],
    )


def normalize_trend_ideas_payload(
    payload: TrendIdeasPayload,
    *,
    max_ideas: int = 3,
) -> TrendIdeasPayload:
    seen_titles: set[str] = set()
    normalized_ideas: list[TrendIdea] = []
    for idea in payload.ideas or []:
        title_key = " ".join(str(idea.title or "").split()).strip().lower()
        if not title_key or title_key in seen_titles:
            continue
        seen_titles.add(title_key)
        seen_refs: set[tuple[int, int]] = set()
        evidence_refs: list[TrendIdeaEvidenceRef] = []
        for ref in idea.evidence_refs or []:
            key = (int(ref.doc_id), int(ref.chunk_index))
            if key in seen_refs:
                continue
            seen_refs.add(key)
            evidence_refs.append(ref)
        if not evidence_refs:
            continue
        normalized_ideas.append(
            idea.model_copy(update={"evidence_refs": evidence_refs})
        )
        if len(normalized_ideas) >= max(0, int(max_ideas or 0)):
            break
    return payload.model_copy(update={"ideas": normalized_ideas})


def build_trend_snapshot_pack_md(
    *,
    trend_payload: TrendPayload,
    upstream_pass_output_id: int | None = None,
) -> str:
    lines = _snapshot_pack_header_lines(
        trend_payload=trend_payload,
        upstream_pass_output_id=upstream_pass_output_id,
    )
    lines.extend(_snapshot_pack_cluster_lines(clusters=trend_payload.clusters))

    return "\n".join(lines).rstrip() + "\n"


def _snapshot_pack_header_lines(
    *,
    trend_payload: TrendPayload,
    upstream_pass_output_id: int | None,
) -> list[str]:
    lines = ["## Trend snapshot pack"]
    if upstream_pass_output_id is not None:
        lines.append(f"- upstream_pass_output_id={int(upstream_pass_output_id)}")
    topics = (
        "- topics="
        + ", ".join(str(topic).strip() for topic in trend_payload.topics or [])
        if trend_payload.topics
        else "- topics=-"
    )
    lines.extend(
        [
            f"- title={str(trend_payload.title or '').strip()}",
            f"- granularity={str(trend_payload.granularity or '').strip().lower()}",
            f"- period_start={str(trend_payload.period_start or '').strip()}",
            f"- period_end={str(trend_payload.period_end or '').strip()}",
            topics,
            "",
            "### Overview",
            str(trend_payload.overview_md or "").strip() or "(empty)",
        ]
    )
    return lines


def _snapshot_pack_cluster_lines(*, clusters: Any) -> list[str]:
    if not clusters:
        return []
    lines = ["", "### Clusters"]
    for index, cluster in enumerate(clusters, start=1):
        lines.extend(_snapshot_pack_cluster_entry_lines(index=index, cluster=cluster))
    return lines


def _snapshot_pack_cluster_entry_lines(*, index: int, cluster: Any) -> list[str]:
    lines = [
        f"#### cluster {index}: {str(getattr(cluster, 'title', '') or '').strip() or '(untitled)'}"
    ]
    content_md = str(getattr(cluster, "content_md", "") or "").strip()
    if content_md:
        lines.append(content_md)
    evidence = _snapshot_pack_evidence_ref_lines(
        evidence_refs=list(getattr(cluster, "evidence_refs", []) or [])
    )
    if evidence:
        lines.append("- evidence_refs")
        lines.extend(evidence)
    return lines


def _snapshot_pack_evidence_ref_lines(
    *, evidence_refs: list[Any]
) -> list[str]:
    lines: list[str] = []
    for rep in evidence_refs:
        try:
            doc_id = int(getattr(rep, "doc_id"))
            chunk_index = int(getattr(rep, "chunk_index"))
        except Exception:
            continue
        lines.append(f"  - doc_id={doc_id} chunk_index={chunk_index}")
    return lines


def build_trend_ideas_pass_output(
    *,
    request: _TrendIdeasPassOutputRequest | None = None,
    **legacy_kwargs: Any,
) -> PassOutputEnvelope:
    normalized_request = _coerce_trend_ideas_pass_output_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    normalized_diagnostics = (
        normalized_request.diagnostics
        if isinstance(normalized_request.diagnostics, dict)
        else {}
    )
    return PassOutputEnvelope(
        pass_kind=TREND_IDEAS_PASS_KIND,
        schema_version=TREND_IDEAS_SCHEMA_VERSION,
        status=normalized_request.status,
        granularity=str(normalized_request.granularity or "").strip().lower() or None,
        period_start=normalized_request.period_start.isoformat(),
        period_end=normalized_request.period_end.isoformat(),
        run_id=str(normalized_request.run_id),
        input_refs=list(normalized_request.input_refs or []),
        payload=normalized_request.payload.model_dump(mode="json"),
        diagnostics=normalized_diagnostics,
    )


__all__ = [
    "TREND_IDEAS_PASS_KIND",
    "TREND_IDEAS_SCHEMA_VERSION",
    "TrendIdea",
    "TrendIdeaEvidenceRef",
    "TrendIdeasPayload",
    "build_empty_trend_ideas_payload",
    "build_trend_ideas_pass_output",
    "build_trend_snapshot_pack_md",
    "normalize_trend_ideas_payload",
]
