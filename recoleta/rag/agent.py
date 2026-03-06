from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from loguru import logger
from pydantic_ai import Agent, RunContext

from recoleta.rag.semantic_search import semantic_search_summaries_in_period
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.storage import Repository
from recoleta.trends import TrendCluster, TrendPayload


@dataclass(slots=True)
class TrendAgentDeps:
    repository: Repository
    vector_store: LanceVectorStore
    run_id: str
    period_start: datetime
    period_end: datetime
    rag_sources: list[dict[str, Any]] | None
    embedding_model: str
    embedding_dimensions: int | None
    embedding_batch_max_inputs: int
    embedding_batch_max_chars: int
    embedding_failure_mode: str = "continue"
    embedding_max_errors: int = 0


def _build_trend_instructions(*, output_language: str | None) -> str:
    base = (
        "You are a research trend analyst. Use tools to explore the local corpus. "
        "Prefer summary chunks (chunk_index=0) first. "
        "When ready, return a TrendPayload with grounded, readable content."
    )
    base += (
        " When available, use trend documents (doc_type=trend) for synthesis and higher-level themes, "
        "and use item documents (doc_type=item) for concrete citations and for selecting Top-N must-read items. "
        "Always include a Top-N must-read block as Markdown (either a dedicated section in overview_md or a per-cluster section). "
        "If ranking_n is provided in the prompt, use it as N."
    )
    base += (
        " Prioritize readability over compression: use short sentences, avoid long multi-clause lines, "
        "and avoid stacking many technical terms in a single sentence. "
        "Introduce acronyms once with a brief explanation in the output language, then reuse them. "
        "Avoid repetitive phrasing across overview, clusters, and highlights; each section should add new value."
    )
    base += (
        " For clusters[].representative_chunks, either omit the entry or provide an object "
        "with required integer fields doc_id and chunk_index, and optional float score. "
        "Never output null for doc_id/chunk_index."
    )
    if not output_language:
        return base
    return (
        f"{base} Use {output_language} for all natural language fields "
        "(title, overview_md, clusters[].name, clusters[].description, highlights). "
        "Keep all JSON keys in English and keep topics as concise English tags."
    )


def resolve_rag_query_sources(
    *,
    doc_type: str,
    granularity: str | None,
    rag_sources: list[dict[str, Any]] | None,
) -> list[tuple[str, str | None]]:
    normalized_type = str(doc_type or "").strip().lower()
    if normalized_type not in {"item", "trend"}:
        return []

    normalized_granularity = (
        str(granularity or "").strip().lower() if granularity is not None else ""
    )
    normalized_sources: list[tuple[str, str | None]] = []
    seen: set[tuple[str, str | None]] = set()
    for source in rag_sources or []:
        if not isinstance(source, dict):
            continue
        source_type = str(source.get("doc_type") or "").strip().lower()
        if source_type not in {"item", "trend"}:
            continue
        source_granularity = (
            str(source.get("granularity") or "").strip().lower()
            if source.get("granularity") is not None
            else ""
        )
        key = (
            source_type,
            source_granularity or None if source_type == "trend" else None,
        )
        if key in seen:
            continue
        seen.add(key)
        normalized_sources.append(key)

    if not normalized_sources:
        if normalized_type == "item":
            return [("item", None)]
        return [("trend", normalized_granularity or None)]

    allowed_sources = [
        source for source in normalized_sources if source[0] == normalized_type
    ]
    if not allowed_sources:
        return []
    if normalized_type == "item":
        return [("item", None)]
    if normalized_granularity:
        requested = ("trend", normalized_granularity)
        return [requested] if requested in allowed_sources else []
    return allowed_sources


def _doc_event_sort_key(doc: Any) -> tuple[float, int]:
    raw_event = getattr(doc, "published_at", None)
    if not isinstance(raw_event, datetime):
        raw_event = getattr(doc, "period_start", None)
    event_ts = raw_event.timestamp() if isinstance(raw_event, datetime) else 0.0
    try:
        doc_id = int(getattr(doc, "id") or 0)
    except Exception:
        doc_id = 0
    return event_ts, doc_id


def build_trend_agent(
    *, llm_model: str, output_language: str | None = None
) -> Agent[TrendAgentDeps, TrendPayload]:
    from recoleta.rag.pydantic_ai_model import build_pydantic_ai_model

    model = build_pydantic_ai_model(llm_model)
    agent: Agent[TrendAgentDeps, TrendPayload] = Agent(
        model,
        deps_type=TrendAgentDeps,
        output_type=TrendPayload,
        instructions=_build_trend_instructions(output_language=output_language),
        defer_model_check=True,
    )

    @agent.tool
    def list_docs(
        ctx: RunContext[TrendAgentDeps],
        doc_type: str,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        deps = ctx.deps
        requested_sources = resolve_rag_query_sources(
            doc_type=doc_type,
            granularity=granularity,
            rag_sources=deps.rag_sources,
        )
        normalized_order = str(order_by or "event_desc").strip()
        normalized_offset = max(0, int(offset or 0))
        normalized_limit = max(0, int(limit or 50))
        if not requested_sources or normalized_limit <= 0:
            return {"docs": [], "returned": 0}

        docs: list[Any] = []
        seen_doc_ids: set[int] = set()
        for source_doc_type, source_granularity in requested_sources:
            rows = deps.repository.list_documents(
                doc_type=source_doc_type,
                period_start=deps.period_start,
                period_end=deps.period_end,
                granularity=source_granularity,
                order_by=normalized_order,
                offset=0,
                limit=normalized_limit,
            )
            for doc in rows:
                try:
                    doc_id = int(getattr(doc, "id") or 0)
                except Exception:
                    continue
                if doc_id <= 0 or doc_id in seen_doc_ids:
                    continue
                seen_doc_ids.add(doc_id)
                docs.append(doc)

        docs.sort(key=_doc_event_sort_key, reverse=normalized_order != "event_asc")
        docs = docs[normalized_offset : normalized_offset + normalized_limit]
        out: list[dict[str, Any]] = []
        for doc in docs:
            published_at = getattr(doc, "published_at", None)
            period_start_value = getattr(doc, "period_start", None)
            period_end_value = getattr(doc, "period_end", None)
            out.append(
                {
                    "doc_id": int(getattr(doc, "id")),
                    "doc_type": str(getattr(doc, "doc_type") or ""),
                    "title": str(getattr(doc, "title") or ""),
                    "item_id": getattr(doc, "item_id", None),
                    "source": str(getattr(doc, "source") or ""),
                    "canonical_url": str(getattr(doc, "canonical_url") or ""),
                    "published_at": published_at.isoformat()
                    if isinstance(published_at, datetime)
                    else None,
                    "granularity": str(getattr(doc, "granularity") or ""),
                    "period_start": period_start_value.isoformat()
                    if isinstance(period_start_value, datetime)
                    else None,
                    "period_end": period_end_value.isoformat()
                    if isinstance(period_end_value, datetime)
                    else None,
                }
            )
        return {"docs": out, "returned": len(out)}

    @agent.tool
    def get_doc(ctx: RunContext[TrendAgentDeps], doc_id: int) -> dict[str, Any]:
        deps = ctx.deps
        doc = deps.repository.get_document(doc_id=int(doc_id or 0))
        if doc is None:
            return {"doc": None}
        published_at = getattr(doc, "published_at", None)
        period_start_value = getattr(doc, "period_start", None)
        period_end_value = getattr(doc, "period_end", None)
        return {
            "doc": {
                "doc_id": int(getattr(doc, "id")),
                "doc_type": str(getattr(doc, "doc_type") or ""),
                "title": str(getattr(doc, "title") or ""),
                "item_id": getattr(doc, "item_id", None),
                "source": str(getattr(doc, "source") or ""),
                "canonical_url": str(getattr(doc, "canonical_url") or ""),
                "published_at": published_at.isoformat()
                if isinstance(published_at, datetime)
                else None,
                "granularity": str(getattr(doc, "granularity") or ""),
                "period_start": period_start_value.isoformat()
                if isinstance(period_start_value, datetime)
                else None,
                "period_end": period_end_value.isoformat()
                if isinstance(period_end_value, datetime)
                else None,
            }
        }

    @agent.tool
    def read_chunk(
        ctx: RunContext[TrendAgentDeps], doc_id: int, chunk_index: int
    ) -> dict[str, Any]:
        deps = ctx.deps
        chunk = deps.repository.read_document_chunk(
            doc_id=int(doc_id or 0), chunk_index=int(chunk_index or 0)
        )
        if chunk is None:
            return {"chunk": None}
        return {
            "chunk": {
                "chunk_id": int(getattr(chunk, "id")),
                "doc_id": int(getattr(chunk, "doc_id")),
                "chunk_index": int(getattr(chunk, "chunk_index")),
                "kind": str(getattr(chunk, "kind") or ""),
                "start_char": getattr(chunk, "start_char", None),
                "end_char": getattr(chunk, "end_char", None),
                "source_content_type": str(getattr(chunk, "source_content_type") or ""),
                "text": str(getattr(chunk, "text") or ""),
            }
        }

    @agent.tool
    def search_text(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        deps = ctx.deps
        requested_sources = resolve_rag_query_sources(
            doc_type=doc_type,
            granularity=granularity,
            rag_sources=deps.rag_sources,
        )
        normalized_limit = max(1, int(limit or 10))
        if not requested_sources:
            return {"hits": [], "returned": 0}

        hits: list[dict[str, Any]] = []
        seen_hits: set[tuple[int, int]] = set()
        for source_doc_type, source_granularity in requested_sources:
            rows = deps.repository.search_chunks_text(
                query=str(query or ""),
                doc_type=source_doc_type,
                granularity=source_granularity,
                period_start=deps.period_start,
                period_end=deps.period_end,
                limit=normalized_limit,
            )
            for row in rows:
                if not isinstance(row, dict):
                    continue
                try:
                    key = (
                        int(row.get("doc_id") or 0),
                        int(row.get("chunk_index") or -1),
                    )
                except Exception:
                    continue
                if key[0] <= 0 or key[1] < 0 or key in seen_hits:
                    continue
                seen_hits.add(key)
                hits.append(row)
        hits.sort(
            key=lambda row: (
                float(row.get("rank") or 0.0),
                int(row.get("doc_id") or 0),
                int(row.get("chunk_index") or 0),
            )
        )
        hits = hits[:normalized_limit]
        return {"hits": hits, "returned": len(hits)}

    @agent.tool
    def search_semantic(
        ctx: RunContext[TrendAgentDeps],
        query: str,
        doc_type: str,
        granularity: str | None = None,
        limit: int = 10,
    ) -> dict[str, Any]:
        deps = ctx.deps
        requested_sources = resolve_rag_query_sources(
            doc_type=doc_type,
            granularity=granularity,
            rag_sources=deps.rag_sources,
        )
        normalized_limit = max(1, int(limit or 10))
        if not requested_sources:
            return {"hits": [], "returned": 0}

        hits: list[Any] = []
        seen_hits: set[tuple[int, int]] = set()
        for source_doc_type, source_granularity in requested_sources:
            rows = semantic_search_summaries_in_period(
                repository=deps.repository,
                vector_store=deps.vector_store,
                run_id=deps.run_id,
                doc_type=source_doc_type,
                granularity=source_granularity,
                period_start=deps.period_start,
                period_end=deps.period_end,
                query=str(query or ""),
                embedding_model=deps.embedding_model,
                embedding_dimensions=deps.embedding_dimensions,
                max_batch_inputs=deps.embedding_batch_max_inputs,
                max_batch_chars=deps.embedding_batch_max_chars,
                embedding_failure_mode=str(deps.embedding_failure_mode or "continue"),
                embedding_max_errors=int(deps.embedding_max_errors or 0),
                limit=normalized_limit,
                metric_namespace="pipeline.trends",
            )
            for hit in rows:
                try:
                    key = (
                        int(getattr(hit, "doc_id")),
                        int(getattr(hit, "chunk_index")),
                    )
                except Exception:
                    continue
                if key[0] <= 0 or key[1] < 0 or key in seen_hits:
                    continue
                seen_hits.add(key)
                hits.append(hit)
        hits.sort(
            key=lambda hit: (
                -float(getattr(hit, "score", 0.0) or 0.0),
                int(getattr(hit, "doc_id") or 0),
                int(getattr(hit, "chunk_index") or 0),
            )
        )
        hits = hits[:normalized_limit]
        rows = [
            {
                "chunk_id": h.chunk_id,
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
                "text_preview": h.text_preview,
            }
            for h in hits
        ]
        return {"hits": rows, "returned": len(rows)}

    return agent


def ensure_trend_cluster_representatives(
    *,
    payload: TrendPayload,
    search,
    max_reps: int = 6,
) -> dict[str, int]:
    clusters_total = len(payload.clusters or [])
    clusters_backfilled_total = 0
    invalid_reps_dropped_total = 0
    reps_backfilled_total = 0

    normalized_max_reps = max(0, int(max_reps or 0))
    if normalized_max_reps <= 0 or not payload.clusters:
        return {
            "clusters_total": clusters_total,
            "clusters_backfilled_total": 0,
            "invalid_reps_dropped_total": 0,
            "reps_backfilled_total": 0,
        }

    for cluster in payload.clusters:
        raw_reps = cluster.representative_chunks or []
        cleaned: list[TrendCluster.RepresentativeChunk] = []
        for rep in raw_reps:
            try:
                doc_id = int(getattr(rep, "doc_id"))
                chunk_index = int(getattr(rep, "chunk_index"))
            except Exception:
                invalid_reps_dropped_total += 1
                continue
            if doc_id <= 0 or chunk_index < 0:
                invalid_reps_dropped_total += 1
                continue
            score_raw = getattr(rep, "score", None)
            rep_score: float | None = None
            if score_raw is not None:
                try:
                    rep_score = float(score_raw)  # type: ignore[arg-type]
                except Exception:
                    rep_score = None
            cleaned.append(
                TrendCluster.RepresentativeChunk(
                    doc_id=doc_id,
                    chunk_index=chunk_index,
                    score=round(rep_score, 6) if rep_score is not None else None,
                )
            )

        if cleaned:
            cluster.representative_chunks = cleaned[:normalized_max_reps]
            continue

        query = " ".join(
            [
                str(getattr(cluster, "name", "") or "").strip(),
                str(getattr(cluster, "description", "") or "").strip(),
            ]
        ).strip()
        backfilled: list[TrendCluster.RepresentativeChunk] = []
        if query:
            try:
                rows = search(query, normalized_max_reps) or []
            except Exception:
                rows = []
            for r in rows:
                if not isinstance(r, dict):
                    continue
                doc_id_raw = r.get("doc_id")
                chunk_index_raw = r.get("chunk_index")
                if doc_id_raw is None or chunk_index_raw is None:
                    continue
                try:
                    doc_id = int(doc_id_raw)
                    chunk_index = int(chunk_index_raw)
                except Exception:
                    continue
                if doc_id <= 0 or chunk_index < 0:
                    continue
                score_raw = r.get("score")
                hit_score: float | None
                if score_raw is None:
                    hit_score = None
                else:
                    try:
                        hit_score = float(score_raw)  # type: ignore[arg-type]
                    except Exception:
                        hit_score = None
                backfilled.append(
                    TrendCluster.RepresentativeChunk(
                        doc_id=doc_id,
                        chunk_index=chunk_index,
                        score=round(hit_score, 6) if hit_score is not None else None,
                    )
                )
                if len(backfilled) >= normalized_max_reps:
                    break

        if not backfilled:
            doc_ids = list(getattr(cluster, "representative_doc_ids", []) or [])
            for raw_doc_id in doc_ids:
                try:
                    doc_id = int(raw_doc_id)
                except Exception:
                    continue
                if doc_id <= 0:
                    continue
                backfilled.append(
                    TrendCluster.RepresentativeChunk(
                        doc_id=doc_id, chunk_index=0, score=None
                    )
                )
                if len(backfilled) >= normalized_max_reps:
                    break

        if backfilled:
            cluster.representative_chunks = backfilled
            clusters_backfilled_total += 1
            reps_backfilled_total += len(backfilled)
        else:
            cluster.representative_chunks = []

    return {
        "clusters_total": clusters_total,
        "clusters_backfilled_total": clusters_backfilled_total,
        "invalid_reps_dropped_total": invalid_reps_dropped_total,
        "reps_backfilled_total": reps_backfilled_total,
    }


def _count_tool_calls(messages: list[Any]) -> int:
    total = 0
    for msg in messages:
        parts = getattr(msg, "parts", None)
        if not isinstance(parts, list):
            continue
        for part in parts:
            if getattr(part, "part_kind", None) == "tool-call":
                total += 1
    return total


def _estimate_cost_usd_from_tokens(
    *, model: str, input_tokens: int | None, output_tokens: int | None
) -> float | None:
    if input_tokens is None and output_tokens is None:
        return None
    prompt_tokens = int(input_tokens or 0)
    completion_tokens = int(output_tokens or 0)
    if prompt_tokens <= 0 and completion_tokens <= 0:
        return 0.0
    try:
        from litellm.cost_calculator import cost_per_token
    except Exception:
        return None

    candidates: list[str] = []
    raw = str(model or "").strip()
    if raw:
        candidates.append(raw)
        # pydantic-ai normalized form: provider:model
        if "/" in raw and ":" not in raw:
            provider, rest = raw.split("/", 1)
            provider = provider.strip()
            rest = rest.strip()
            if provider and rest:
                candidates.append(f"{provider}:{rest}")
                candidates.append(rest)
        if ":" in raw:
            _, rest = raw.split(":", 1)
            rest = rest.strip()
            if rest:
                candidates.append(rest)

    seen: set[str] = set()
    for candidate in candidates:
        normalized = str(candidate).strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        try:
            prompt_cost, completion_cost = cost_per_token(
                model=normalized,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
            )
            return float(prompt_cost) + float(completion_cost)
        except Exception:
            continue
    return None


def build_trend_prompt_payload(
    *,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    overview_pack_md: str | None = None,
    rag_sources: list[dict[str, Any]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "task": "Generate research trends for the period.",
        "granularity": granularity,
        "period_start": period_start.isoformat(),
        "period_end": period_end.isoformat(),
        "corpus": {"doc_type": corpus_doc_type, "granularity": corpus_granularity},
        "notes": [
            "Use tools to cite representative doc_id/chunk_index in clusters.",
            "Optimize for readability: short sentences, minimal jargon pile-ups, no repetitive filler.",
            "Keep claims grounded in the local corpus.",
        ],
    }
    if overview_pack_md is not None:
        payload["overview_pack_md"] = str(overview_pack_md)
    if rag_sources is not None:
        payload["rag_sources"] = rag_sources
    if ranking_n is not None:
        payload["ranking_n"] = int(ranking_n)
    if rep_source_doc_type is not None:
        normalized = str(rep_source_doc_type).strip().lower()
        if normalized:
            payload["rep_source_doc_type"] = normalized
    return payload


def generate_trend_payload(
    *,
    repository: Repository,
    vector_store: LanceVectorStore,
    run_id: str,
    llm_model: str,
    output_language: str | None = None,
    embedding_model: str,
    embedding_dimensions: int | None,
    embedding_batch_max_inputs: int,
    embedding_batch_max_chars: int,
    embedding_failure_mode: str = "continue",
    embedding_max_errors: int = 0,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
    corpus_doc_type: str,
    corpus_granularity: str | None = None,
    overview_pack_md: str | None = None,
    rag_sources: list[dict[str, Any]] | None = None,
    ranking_n: int | None = None,
    rep_source_doc_type: str | None = None,
    include_debug: bool = False,
) -> tuple[TrendPayload, dict[str, Any] | None]:
    log = logger.bind(module="rag.trend_agent", run_id=run_id)
    agent = build_trend_agent(llm_model=llm_model, output_language=output_language)
    deps = TrendAgentDeps(
        repository=repository,
        vector_store=vector_store,
        run_id=run_id,
        period_start=period_start,
        period_end=period_end,
        rag_sources=rag_sources,
        embedding_model=embedding_model,
        embedding_dimensions=embedding_dimensions,
        embedding_batch_max_inputs=embedding_batch_max_inputs,
        embedding_batch_max_chars=embedding_batch_max_chars,
        embedding_failure_mode=str(embedding_failure_mode or "continue"),
        embedding_max_errors=int(embedding_max_errors or 0),
    )

    prompt = json.dumps(
        build_trend_prompt_payload(
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            corpus_doc_type=corpus_doc_type,
            corpus_granularity=corpus_granularity,
            overview_pack_md=overview_pack_md,
            rag_sources=rag_sources,
            ranking_n=ranking_n,
            rep_source_doc_type=rep_source_doc_type,
        ),
        ensure_ascii=False,
        separators=(",", ":"),
    )

    result = agent.run_sync(prompt, deps=deps)
    payload = result.output
    rep_doc_type_candidate = str(rep_source_doc_type or "").strip().lower()
    rep_doc_type = (
        rep_doc_type_candidate
        if rep_doc_type_candidate in {"item", "trend"}
        else "item"
    )
    rep_stats = ensure_trend_cluster_representatives(
        payload=payload,
        search=lambda q, n: [
            {
                "doc_id": h.doc_id,
                "chunk_index": h.chunk_index,
                "score": round(float(h.score), 6),
            }
            for h in semantic_search_summaries_in_period(
                repository=repository,
                vector_store=vector_store,
                run_id=run_id,
                doc_type=rep_doc_type,
                period_start=period_start,
                period_end=period_end,
                query=q,
                embedding_model=embedding_model,
                embedding_dimensions=embedding_dimensions,
                max_batch_inputs=embedding_batch_max_inputs,
                max_batch_chars=embedding_batch_max_chars,
                embedding_failure_mode=str(embedding_failure_mode or "continue"),
                embedding_max_errors=int(embedding_max_errors or 0),
                limit=int(n),
                metric_namespace="pipeline.trends",
            )
        ],
        max_reps=6,
    )
    if rep_stats.get("invalid_reps_dropped_total", 0) or rep_stats.get(
        "clusters_backfilled_total", 0
    ):
        log.warning("Trend cluster representatives normalized stats={}", rep_stats)
        try:
            repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.cluster_representatives_backfilled_total",
                value=int(rep_stats.get("clusters_backfilled_total") or 0),
                unit="count",
            )
            repository.record_metric(
                run_id=run_id,
                name="pipeline.trends.cluster_representatives_invalid_dropped_total",
                value=int(rep_stats.get("invalid_reps_dropped_total") or 0),
                unit="count",
            )
        except Exception as metric_exc:  # noqa: BLE001
            log.warning(
                "Trend representative metrics failed error_type={} error={}",
                type(metric_exc).__name__,
                str(metric_exc),
            )
    usage = result.usage()
    usage_dict = {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
        "requests": getattr(usage, "requests", None),
    }
    estimated_cost_usd = _estimate_cost_usd_from_tokens(
        model=llm_model,
        input_tokens=getattr(usage, "input_tokens", None),
        output_tokens=getattr(usage, "output_tokens", None),
    )
    debug: dict[str, Any] = {
        "usage": usage_dict,
        "estimated_cost_usd": estimated_cost_usd,
    }
    if include_debug:
        messages = result.all_messages()
        debug["tool_calls_total"] = _count_tool_calls(messages)
    log.info(
        "Trend generation done include_debug={} cost_present={}",
        bool(include_debug),
        estimated_cost_usd is not None,
    )
    return payload, debug
