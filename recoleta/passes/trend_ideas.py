from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from recoleta.passes.base import PassInputRef, PassOutputEnvelope, PassStatus
from recoleta.trends import TrendPayload
TREND_IDEAS_PASS_KIND = "trend_ideas"
TREND_IDEAS_SCHEMA_VERSION = 1
TREND_IDEA_KIND_VALUES = (
    "new_build",
    "revival",
    "research_gap",
    "tooling_wedge",
    "workflow_shift",
)
TREND_IDEA_TIME_HORIZON_VALUES = ("now", "near", "frontier")


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
    kind: str
    thesis: str
    anti_thesis: str | None = None
    why_now: str
    what_changed: str
    user_or_job: str
    evidence_refs: list[TrendIdeaEvidenceRef] = Field(default_factory=list)
    validation_next_step: str
    time_horizon: str

    @field_validator(
        "title",
        "kind",
        "thesis",
        "why_now",
        "what_changed",
        "user_or_job",
        "validation_next_step",
        "time_horizon",
    )
    @classmethod
    def _validate_required_text(cls, value: str) -> str:
        normalized = " ".join(str(value or "").split()).strip()
        if not normalized:
            raise ValueError("idea text fields must not be empty")
        return normalized

    @field_validator("anti_thesis")
    @classmethod
    def _validate_optional_text(cls, value: str | None) -> str | None:
        normalized = " ".join(str(value or "").split()).strip()
        return normalized or None

    @field_validator("kind")
    @classmethod
    def _validate_kind(cls, value: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in TREND_IDEA_KIND_VALUES:
            allowed = ", ".join(TREND_IDEA_KIND_VALUES)
            raise ValueError(f"kind must be one of {allowed}")
        return normalized

    @field_validator("time_horizon")
    @classmethod
    def _validate_time_horizon(cls, value: str) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in TREND_IDEA_TIME_HORIZON_VALUES:
            allowed = ", ".join(TREND_IDEA_TIME_HORIZON_VALUES)
            raise ValueError(f"time_horizon must be one of {allowed}")
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
    lines: list[str] = ["## Trend snapshot pack"]
    if upstream_pass_output_id is not None:
        lines.append(f"- upstream_pass_output_id={int(upstream_pass_output_id)}")
    lines.extend(
        [
            f"- title={str(trend_payload.title or '').strip()}",
            f"- granularity={str(trend_payload.granularity or '').strip().lower()}",
            f"- period_start={str(trend_payload.period_start or '').strip()}",
            f"- period_end={str(trend_payload.period_end or '').strip()}",
            (
                "- topics="
                + ", ".join(str(topic).strip() for topic in trend_payload.topics or [])
                if trend_payload.topics
                else "- topics=-"
            ),
            "",
            "### Overview",
            str(trend_payload.overview_md or "").strip() or "(empty)",
        ]
    )

    if trend_payload.highlights:
        lines.extend(["", "### Highlights"])
        for highlight in trend_payload.highlights:
            normalized = str(highlight or "").strip()
            if normalized:
                lines.append(f"- {normalized}")

    if trend_payload.clusters:
        lines.extend(["", "### Clusters"])
        for index, cluster in enumerate(trend_payload.clusters, start=1):
            lines.append(
                f"#### cluster {index}: {str(getattr(cluster, 'name', '') or '').strip() or '(unnamed)'}"
            )
            description = str(getattr(cluster, "description", "") or "").strip()
            if description:
                lines.append(description)
            reps = list(getattr(cluster, "representative_chunks", []) or [])
            if reps:
                lines.append("- representative_chunks")
                for rep in reps:
                    try:
                        doc_id = int(getattr(rep, "doc_id"))
                        chunk_index = int(getattr(rep, "chunk_index"))
                    except Exception:
                        continue
                    lines.append(f"  - doc_id={doc_id} chunk_index={chunk_index}")

    evolution = trend_payload.evolution
    if evolution is not None:
        lines.extend(["", "### Evolution", str(evolution.summary_md or "").strip()])
        for signal in evolution.signals or []:
            lines.append(
                (
                    "- "
                    + " | ".join(
                        part
                        for part in (
                            str(signal.theme or "").strip(),
                            str(signal.change_type.value).strip(),
                            str(signal.summary or "").strip(),
                            (
                                "history_windows="
                                + ",".join(str(window).strip() for window in signal.history_windows)
                                if signal.history_windows
                                else ""
                            ),
                        )
                        if part
                    )
                )
            )

    counter_signal = trend_payload.counter_signal
    if counter_signal is not None:
        lines.extend(
            [
                "",
                "### Counter-signal",
                f"- title={str(counter_signal.title or '').strip()}",
                str(counter_signal.summary or "").strip(),
            ]
        )
        for ref in counter_signal.evidence_refs or []:
            lines.append(
                (
                    "- evidence_ref "
                    f"doc_id={int(ref.doc_id)} chunk_index={int(ref.chunk_index)}"
                )
            )

    return "\n".join(lines).rstrip() + "\n"


def build_trend_ideas_pass_output(
    *,
    run_id: str,
    status: PassStatus,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    payload: TrendIdeasPayload,
    input_refs: list[PassInputRef] | None = None,
    diagnostics: dict[str, Any] | None = None,
) -> PassOutputEnvelope:
    normalized_diagnostics = diagnostics if isinstance(diagnostics, dict) else {}
    return PassOutputEnvelope(
        pass_kind=TREND_IDEAS_PASS_KIND,
        schema_version=TREND_IDEAS_SCHEMA_VERSION,
        status=status,
        granularity=str(granularity or "").strip().lower() or None,
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        run_id=str(run_id),
        input_refs=list(input_refs or []),
        payload=payload.model_dump(mode="json"),
        diagnostics=normalized_diagnostics,
    )


__all__ = [
    "TREND_IDEAS_PASS_KIND",
    "TREND_IDEAS_SCHEMA_VERSION",
    "TREND_IDEA_KIND_VALUES",
    "TREND_IDEA_TIME_HORIZON_VALUES",
    "TrendIdea",
    "TrendIdeaEvidenceRef",
    "TrendIdeasPayload",
    "build_empty_trend_ideas_payload",
    "build_trend_ideas_pass_output",
    "build_trend_snapshot_pack_md",
    "normalize_trend_ideas_payload",
]
