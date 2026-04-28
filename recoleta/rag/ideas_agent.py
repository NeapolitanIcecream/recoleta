from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger
from pydantic import BaseModel, field_validator
from pydantic_ai import Agent, RunContext

from recoleta.llm_costs import (
    estimate_cost_usd_from_tokens as estimate_llm_cost_usd_from_tokens,
)
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.ports import TrendRepositoryPort
from recoleta.prompt_style import reader_facing_ai_tropes_prompt
from recoleta.rag.corpus_tools import CorpusSpec, SearchService
from recoleta.rag.agent_runtime import _extract_raw_tool_trace
from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload


class _TrendIdeasBundleTitle(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def _validate_title(cls, value: str) -> str:
        normalized = _normalize_bundle_title_value(value)
        if not normalized:
            raise ValueError("bundle title must not be empty")
        return normalized


def _normalize_bundle_title_value(value: str) -> str:
    normalized = " ".join(str(value or "").split()).strip()
    for _ in range(2):
        if not normalized:
            return ""
        if not normalized.startswith(("{", "[")):
            return normalized
        try:
            parsed = json.loads(normalized)
        except Exception:
            return normalized
        if isinstance(parsed, dict):
            candidate = parsed.get("title")
            if isinstance(candidate, str):
                normalized = " ".join(candidate.split()).strip()
                continue
            return normalized
        if isinstance(parsed, str):
            normalized = " ".join(parsed.split()).strip()
            continue
        return normalized
    return normalized


@dataclass(slots=True)
class IdeasAgentDeps:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    rag_sources: list[dict[str, Any]] | None
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    metric_namespace: str = "pipeline.trends.pass.ideas"
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    llm_connection: LLMConnectionConfig | None = None


@dataclass(frozen=True, slots=True)
class TrendIdeasGenerationRequest:
    repository: TrendRepositoryPort
    vector_store: LanceVectorStore
    run_id: str
    llm_model: str
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    granularity: str
    period_start: datetime
    period_end: datetime
    trend_payload: TrendPayload
    trend_snapshot_pack_md: str
    output_language: str | None = None
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0
    rag_sources: list[dict[str, Any]] | None = None
    include_debug: bool = False
    metric_namespace: str = "pipeline.trends.pass.ideas"
    llm_connection: LLMConnectionConfig | None = None


def _coerce_trend_ideas_generation_request(
    *,
    request: TrendIdeasGenerationRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> TrendIdeasGenerationRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return TrendIdeasGenerationRequest(
        repository=values["repository"],
        vector_store=values["vector_store"],
        run_id=str(values["run_id"]),
        llm_model=str(values["llm_model"]),
        output_language=values.get("output_language"),
        embedding_model=str(values["embedding_model"]),
        embedding_dimensions=values.get("embedding_dimensions"),
        embedding_batch_max_inputs=int(values["embedding_batch_max_inputs"]),
        embedding_batch_max_chars=int(values["embedding_batch_max_chars"]),
        embedding_failure_mode=str(values.get("embedding_failure_mode") or "continue"),
        embedding_max_errors=int(values.get("embedding_max_errors") or 0),
        granularity=str(values["granularity"]),
        period_start=values["period_start"],
        period_end=values["period_end"],
        trend_payload=values["trend_payload"],
        trend_snapshot_pack_md=str(values["trend_snapshot_pack_md"]),
        rag_sources=values.get("rag_sources"),
        include_debug=bool(values.get("include_debug", False)),
        metric_namespace=str(
            values.get("metric_namespace") or "pipeline.trends.pass.ideas"
        ),
        llm_connection=values.get("llm_connection"),
    )


def _search_service_from_deps(deps: IdeasAgentDeps) -> SearchService:
    return SearchService(
        repository=deps.repository,
        vector_store=deps.vector_store,
        run_id=deps.run_id,
        period_start=deps.period_start,
        period_end=deps.period_end,
        corpus_spec=CorpusSpec.from_rag_sources(deps.rag_sources),
        embedding_model=deps.embedding_model,
        embedding_dimensions=deps.embedding_dimensions,
        embedding_batch_max_inputs=deps.embedding_batch_max_inputs,
        embedding_batch_max_chars=deps.embedding_batch_max_chars,
        metric_namespace=deps.metric_namespace,
        embedding_failure_mode=str(deps.embedding_failure_mode or "continue"),
        embedding_max_errors=int(deps.embedding_max_errors or 0),
        llm_connection=deps.llm_connection,
    )


def _build_trend_ideas_instructions(*, output_language: str | None) -> str:
    base = (
        "You are a research editor writing short reader-facing pieces from a local"
        " evidence pack."
        " Use the pack as the primary frame, then use tools to verify and sharpen"
        " the most concrete candidate cases."
        " Return a TrendIdeasPayload."
    )
    base += (
        " Look for concrete build, workflow, evaluation, or adoption changes that"
        " the local evidence now makes credible: a buildable tool, a workflow"
        " change, a missing support layer, or a newly practical applied direction."
    )
    base += (
        " Avoid generic advice such as 'build an AI platform' or 'make an assistant'."
        " Each idea must identify a concrete build, test, or adoption change for a"
        " specific user or workflow during analysis."
    )
    base += (
        " Emit 0 to 3 ideas total, ordered by confidence and practical upside."
        " Use ordering to express priority; do not expose priority as tier labels."
    )
    base += (
        " Every emitted idea must include at least one evidence_refs entry with"
        " concrete doc_id and chunk_index values grounded in the local corpus."
    )
    base += (
        " If the evidence is too weak, return an empty ideas list and explain that"
        " briefly in summary_md instead of guessing."
    )
    base += (
        " Do not invent new umbrella terms, branded labels, or slogan-like phrasing."
        " Prefer established domain terminology."
    )
    base += (
        " If a technical term does not have a stable translation in the requested"
        " output language, prefer the original source-language term instead of forcing a translation."
    )
    base += (
        " Prefer plain, literal wording over compressed jargon, clever metaphors,"
        " or catchy headings."
    )
    base += (
        " Do not translate paper titles, framework names, product names, or acronyms"
        " unless a widely accepted translation already exists."
    )
    base += (
        " Idea titles should be factual descriptive noun phrases, not slogans,"
        " coined categories, or rhetorical questions."
    )
    base += (
        " Name the concrete operational pain, user pressure, or adoption blocker directly."
        " Do not hide the user/job behind generic platform language."
    )
    base += (
        " Use internal reasoning to judge whether a concrete case now has enough"
        " evidence, who would care first, what cheap check would validate it, and what"
        " would make it too weak to publish."
        " Do not expose those axes as separate reader-facing fields."
    )
    base += (
        " Do not use internal rubric labels in public prose. Convert those checks into"
        " ordinary prose or omit them."
    )
    base += (
        " Each idea must be a finished short piece."
        " Use ideas[].title for a literal descriptive label, ideas[].content_md for the"
        " prose body, and ideas[].evidence_refs for grounded supporting references."
    )
    base += (
        " summary_md should summarize the set directly."
        " Do not lead with counts or collection labels."
        " Do not describe the set as ideas, notes, directions, pieces, or retained"
        " items inside summary_md."
        " Idea titles should name the concrete build, test, or workflow itself."
        " Do not use task labels or collection labels in titles."
    )
    base += (
        " Use the supplied evidence pack as evidence and theme input, but do not mirror"
        " its title or summary phrasing. Write from the underlying evidence."
    )
    base += (
        " Start with search_hybrid for broad discovery, then use get_doc_bundle"
        " or read_chunk to confirm specific evidence before finalizing ideas."
    )
    base += (
        " Do not let task language leak into public prose."
        " Do not use formulas such as 'the strongest notes', 'this note',"
        " 'the evidence is publishable', 'the immediate need is not', 'not another',"
        " 'not X but Y', 'shifting from', 'turns from', 'rather than',"
        " 'instead of', 'that makes', 'the near-term job is not',"
        " 'the result does not say', 'away from X and toward Y',"
        " 'X is not Y. It is Z.',"
        " or 'a second reason to do this now'."
        " State the direction directly instead of defining it against what it is not,"
        " what it replaces, what old framing it departs from, or why the reader"
        " should act now."
        " Do not call the output publishable, grounded, retained, or strong."
    )
    base = f"{base}\n\n{reader_facing_ai_tropes_prompt()}"
    if not output_language:
        return base
    return (
        f"{base}\n\nUse {output_language} for all natural-language fields"
        " (title, summary_md, ideas[].title, ideas[].content_md, evidence reason text). Keep JSON keys"
        " and enum values in English."
    )


def build_trend_ideas_prompt_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    trend_payload: TrendPayload,
    trend_snapshot_pack_md: str,
    rag_sources: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "task": "Draft up to three concrete short pieces from the supplied evidence pack.",
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "trend_title": str(trend_payload.title or "").strip(),
        "trend_topics": list(trend_payload.topics or []),
        "trend_snapshot_pack_md": trend_snapshot_pack_md,
        "notes": _trend_ideas_prompt_notes(),
    }
    if rag_sources is not None:
        payload["rag_sources"] = rag_sources
    return payload


def _trend_ideas_prompt_notes() -> list[str]:
    return [
        "Use tools to verify and sharpen candidate ideas against the active local corpus.",
        "Prefer 0-3 ideas; omit weak ideas instead of filling the list.",
        "Use idea ordering to express priority; do not emit best-bet or alternate labels.",
        "During analysis, decide what concrete build, test, or workflow change the piece covers, who would care first, what new evidence supports it, and what cheap check would validate it.",
        "Name the concrete operational pain or adoption blocker directly instead of using generic platform language.",
        "Use evidence_refs to point to the strongest supporting documents.",
        "Do not restate the trend summary as the final output.",
        "Do not let task labels or collection labels leak into public prose.",
        "Do not coin new umbrella terms or marketing-style labels.",
        "If a technical term lacks a stable translation in the requested output language, keep the original term.",
        "Prefer direct, readable phrasing over compressed jargon.",
        "Keep paper titles, framework names, product names, and acronyms in their original form unless a widely accepted translation exists.",
        "Idea titles should read like factual descriptive labels, not slogans, coined categories, or rhetorical questions.",
        "Do not use formulas such as 'the strongest notes', 'this note', 'the evidence is publishable', 'the immediate need is not', 'not another', 'not X but Y', 'shifting from', 'turns from', 'rather than', 'instead of', 'that makes', 'the near-term job is not', 'the result does not say', 'away from X and toward Y', 'X is not Y. It is Z.', or 'a second reason to do this now'.",
        "State the direction directly instead of defining it against what it is not, what it replaces, what old framing it departs from, or why the reader should act now.",
        "Do not describe the output as publishable, grounded, retained, or strong.",
        "Return finished short prose in ideas[].content_md instead of labeled method fields.",
    ]


def _build_trend_ideas_title_instructions(*, output_language: str | None) -> str:
    base = (
        "You write bundle titles for retained sets of research directions."
        " Return an object with a single title field."
        " Write a single bundle title for the retained set."
        " The title must be a short literal noun phrase on one line."
        " Name the shared theme across the retained ideas without repeating their"
        " wording or sounding like a task label."
        " Do not use labels such as idea, ideas, notes, evidence-grounded, trend"
        " snapshot, opportunity, or why now."
        " Do not use counts, dates, colons, slogans, or rhetorical questions."
        " Do not use negative parallelism or other contrast formulas."
        " Do not serialize JSON inside the title field."
        " The title field itself must contain plain text only."
    )
    base = f"{base}\n\n{reader_facing_ai_tropes_prompt()}"
    if not output_language:
        return base
    return (
        f"{base}\n\nUse {output_language} for the title value."
        " Keep the JSON key in English."
    )


def build_trend_ideas_title_prompt_payload(
    *,
    summary_md: str,
    ideas: list[dict[str, str]],
) -> dict[str, Any]:
    return {
        "task": "Write one short bundle title for the retained set. Return plain text in the title field.",
        "summary_md": str(summary_md or "").strip(),
        "ideas": [
            {
                "title": " ".join(str(idea.get("title") or "").split()).strip(),
                "content_md": str(idea.get("content_md") or "").strip(),
            }
            for idea in list(ideas or [])
        ],
    }


def build_trend_ideas_agent(
    *,
    llm_model: str,
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> Agent[IdeasAgentDeps, TrendIdeasPayload]:
    model = build_pydantic_ai_model(llm_model, llm_connection=llm_connection)
    agent: Agent[IdeasAgentDeps, TrendIdeasPayload] = Agent(
        model,
        deps_type=IdeasAgentDeps,
        output_type=TrendIdeasPayload,
        instructions=_build_trend_ideas_instructions(output_language=output_language),
        output_retries=4,
        defer_model_check=True,
    )

    @agent.tool
    def list_docs(
        ctx: RunContext[IdeasAgentDeps],
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """List documents in the active ideas window."""
        return _search_service_from_deps(ctx.deps).list_docs(
            doc_type=doc_type,
            granularity=granularity,
            order_by=order_by,
            offset=offset,
            limit=limit,
        )

    @agent.tool
    def get_doc(ctx: RunContext[IdeasAgentDeps], doc_id: int) -> dict[str, Any]:
        """Fetch one document with metadata."""
        return _search_service_from_deps(ctx.deps).get_doc(doc_id=doc_id)

    @agent.tool
    def get_doc_bundle(
        ctx: RunContext[IdeasAgentDeps],
        doc_id: int,
        content_limit: int = 2,
        content_chars: int = 600,
    ) -> dict[str, Any]:
        """Fetch a compact evidence bundle for one document."""
        return _search_service_from_deps(ctx.deps).get_doc_bundle(
            doc_id=doc_id,
            content_limit=content_limit,
            content_chars=content_chars,
        )

    @agent.tool
    def read_chunk(
        ctx: RunContext[IdeasAgentDeps], doc_id: int, chunk_index: int
    ) -> dict[str, Any]:
        """Read one indexed chunk from a document."""
        return _search_service_from_deps(ctx.deps).read_chunk(
            doc_id=doc_id,
            chunk_index=chunk_index,
        )

    @agent.tool
    def search_text(
        ctx: RunContext[IdeasAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus lexically via FTS."""
        return _search_service_from_deps(ctx.deps).search_text(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_semantic(
        ctx: RunContext[IdeasAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Search the corpus semantically over summary chunks."""
        return _search_service_from_deps(ctx.deps).search_semantic(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    @agent.tool
    def search_hybrid(
        ctx: RunContext[IdeasAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        """Blend lexical and semantic retrieval for opportunity discovery."""
        return _search_service_from_deps(ctx.deps).search_hybrid(
            query=query,
            doc_type=doc_type,
            granularity=granularity,
            limit=limit,
        )

    return agent


def _build_trend_ideas_title_agent(
    *,
    llm_model: str,
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> Agent[None, _TrendIdeasBundleTitle]:
    model = build_pydantic_ai_model(llm_model, llm_connection=llm_connection)
    return Agent(
        model,
        output_type=_TrendIdeasBundleTitle,
        instructions=_build_trend_ideas_title_instructions(
            output_language=output_language
        ),
        output_retries=3,
        defer_model_check=True,
    )


def _summarize_tool_calls(messages: list[Any]) -> tuple[int, dict[str, int]]:
    total = 0
    breakdown: dict[str, int] = {}
    for msg in messages:
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) == "tool-call":
                total += 1
                tool_name = str(getattr(part, "tool_name", "") or "").strip()
                if tool_name:
                    breakdown[tool_name] = int(breakdown.get(tool_name, 0)) + 1
    return total, {name: breakdown[name] for name in sorted(breakdown)}


def _estimate_cost_usd_from_tokens(
    *, model: str, input_tokens: int | None, output_tokens: int | None
) -> float | None:
    return estimate_llm_cost_usd_from_tokens(
        model=model,
        prompt_tokens=input_tokens,
        completion_tokens=output_tokens,
    )


def generate_trend_ideas_payload(
    request: TrendIdeasGenerationRequest | None = None,
    **legacy_kwargs: Any,
) -> tuple[TrendIdeasPayload, dict[str, Any] | None]:
    resolved_request = _coerce_trend_ideas_generation_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    log = logger.bind(module="rag.ideas_agent", run_id=resolved_request.run_id)
    agent = build_trend_ideas_agent(
        llm_model=resolved_request.llm_model,
        output_language=resolved_request.output_language,
        llm_connection=resolved_request.llm_connection,
    )
    deps = IdeasAgentDeps(
        repository=resolved_request.repository,
        vector_store=resolved_request.vector_store,
        run_id=resolved_request.run_id,
        period_start=resolved_request.period_start,
        period_end=resolved_request.period_end,
        rag_sources=resolved_request.rag_sources,
        embedding_model=resolved_request.embedding_model,
        embedding_dimensions=resolved_request.embedding_dimensions,
        embedding_batch_max_inputs=resolved_request.embedding_batch_max_inputs,
        embedding_batch_max_chars=resolved_request.embedding_batch_max_chars,
        embedding_failure_mode=str(
            resolved_request.embedding_failure_mode or "continue"
        ),
        embedding_max_errors=int(resolved_request.embedding_max_errors or 0),
        metric_namespace=resolved_request.metric_namespace,
        llm_connection=resolved_request.llm_connection,
    )
    prompt = json.dumps(
        build_trend_ideas_prompt_payload(
            granularity=resolved_request.granularity,
            period_start=resolved_request.period_start,
            period_end=resolved_request.period_end,
            trend_payload=resolved_request.trend_payload,
            trend_snapshot_pack_md=resolved_request.trend_snapshot_pack_md,
            rag_sources=resolved_request.rag_sources,
        ),
        ensure_ascii=False,
        separators=(",", ":"),
    )

    result = agent.run_sync(prompt, deps=deps)
    payload = result.output
    usage = result.usage()
    messages_getter = getattr(result, "all_messages", None)
    raw_messages = messages_getter() if callable(messages_getter) else None
    messages: list[Any] = raw_messages if isinstance(raw_messages, list) else []
    tool_calls_total, tool_call_breakdown = _summarize_tool_calls(messages)
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=resolved_request.llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": usage_dict,
        "estimated_cost_usd": estimated_cost_usd,
        "tool_calls_total": tool_calls_total,
        "tool_call_breakdown": tool_call_breakdown,
        "raw_tool_trace": _extract_raw_tool_trace(messages),
        "prompt_chars": len(prompt),
        "trend_snapshot_pack_chars": len(
            str(resolved_request.trend_snapshot_pack_md or "")
        ),
        "include_debug": bool(resolved_request.include_debug),
    }
    log.info(
        "Ideas generation done include_debug={} cost_present={}",
        bool(resolved_request.include_debug),
        estimated_cost_usd is not None,
    )
    return payload, debug


def generate_trend_ideas_bundle_title(
    *,
    llm_model: str,
    summary_md: str,
    ideas: list[dict[str, str]],
    output_language: str | None = None,
    llm_connection: LLMConnectionConfig | None = None,
) -> tuple[str, dict[str, Any]]:
    agent = _build_trend_ideas_title_agent(
        llm_model=llm_model,
        output_language=output_language,
        llm_connection=llm_connection,
    )
    prompt = json.dumps(
        build_trend_ideas_title_prompt_payload(summary_md=summary_md, ideas=ideas),
        ensure_ascii=False,
        separators=(",", ":"),
    )
    result = agent.run_sync(prompt)
    usage = result.usage()
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": {
            "input_tokens": getattr(usage, "input_tokens", None),
            "output_tokens": getattr(usage, "output_tokens", None),
            "requests": getattr(usage, "requests", None),
        },
        "estimated_cost_usd": estimated_cost_usd,
        "prompt_chars": len(prompt),
    }
    return result.output.title, debug


__all__ = [
    "IdeasAgentDeps",
    "TrendIdeasPayload",
    "TrendIdeasGenerationRequest",
    "build_trend_ideas_title_prompt_payload",
    "build_trend_ideas_agent",
    "build_trend_ideas_prompt_payload",
    "generate_trend_ideas_bundle_title",
    "generate_trend_ideas_payload",
]
