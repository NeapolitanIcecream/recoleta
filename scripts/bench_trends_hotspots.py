from __future__ import annotations

import argparse
import copy
import hashlib
import json
import statistics
import tempfile
import time
from contextlib import ExitStack
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, cast
from unittest.mock import patch

from loguru import logger
from sqlalchemy import text
from sqlmodel import Session

from recoleta.models import Document, DocumentChunk
from recoleta.rag import semantic_search as rag_semantic_search
from recoleta.storage import Repository
from recoleta.trends import (
    TrendCluster,
    TrendPayload,
    _chunk_text_segments,
    _filter_pairs_by_min_relevance,
    day_period_bounds,
    index_items_as_documents,
    semantic_search_summaries_in_period,
)
from recoleta.types import AnalysisResult, ItemDraft, sha256_hex


@dataclass(slots=True)
class _EnsureStats:
    invocations_total: int = 0
    misses_total: int = 0
    cache_hits_total: int = 0
    wall_ms_total: int = 0


def _median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def _pct_improvement(*, baseline: float, candidate: float) -> float:
    if baseline <= 0:
        return 0.0
    return ((baseline - candidate) / baseline) * 100.0


def _deterministic_vector(text_value: str, *, dimensions: int) -> list[float]:
    dims = max(4, int(dimensions))
    digest = hashlib.sha256(text_value.encode("utf-8")).digest()
    values: list[float] = []
    while len(values) < dims:
        for byte in digest:
            values.append(round((byte / 255.0) * 2.0 - 1.0, 6))
            if len(values) >= dims:
                break
        digest = hashlib.sha256(digest).digest()
    return values[:dims]


def _fake_embed(
    self: Any,
    *,
    model: str,
    inputs: list[str],
    dimensions: int | None = None,
) -> tuple[list[list[float]], dict[str, Any]]:
    del self
    dims = int(dimensions or 16)
    vectors = [
        _deterministic_vector(f"{model}:{idx}:{value}", dimensions=dims)
        for idx, value in enumerate(inputs)
    ]
    prompt_tokens = sum(max(1, len(value) // 4) for value in inputs)
    return (
        vectors,
        {
            "model": model,
            "prompt_tokens": prompt_tokens,
            "total_tokens": prompt_tokens,
            "cost_usd": 0.0,
            "elapsed_ms": 0,
        },
    )


def _copy_index_stats(stats: dict[str, Any]) -> dict[str, Any]:
    copied: dict[str, Any] = {}
    for key, value in stats.items():
        if isinstance(value, list):
            copied[key] = list(value)
        elif isinstance(value, dict):
            copied[key] = dict(value)
        else:
            copied[key] = value
    return copied


def _with_fake_embeddings(stack: ExitStack) -> None:
    stack.enter_context(
        patch.object(rag_semantic_search.LiteLLMEmbedder, "embed", _fake_embed)
    )


def _wrap_ensure_summary_vectors(
    *,
    cached: bool,
    ensure_stats: _EnsureStats,
) -> Any:
    original = rag_semantic_search.ensure_summary_vectors_for_period
    cache: dict[tuple[Any, ...], dict[str, Any]] = {}

    def _cache_key(kwargs: dict[str, Any]) -> tuple[Any, ...]:
        return (
            str(kwargs.get("doc_type") or "").strip(),
            str(kwargs.get("granularity") or "").strip() or None,
            cast(datetime, kwargs["period_start"]).isoformat(),
            cast(datetime, kwargs["period_end"]).isoformat(),
            str(kwargs.get("embedding_model") or "").strip(),
            int(kwargs.get("embedding_dimensions") or 0)
            if kwargs.get("embedding_dimensions") is not None
            else None,
            int(kwargs.get("limit") or 0),
            int(kwargs.get("offset") or 0),
        )

    def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
        del args
        ensure_stats.invocations_total += 1
        key = _cache_key(kwargs)
        if cached and key in cache:
            ensure_stats.cache_hits_total += 1
            return _copy_index_stats(cache[key])
        started = time.perf_counter()
        result = original(**kwargs)
        ensure_stats.wall_ms_total += int((time.perf_counter() - started) * 1000)
        ensure_stats.misses_total += 1
        if cached:
            cache[key] = _copy_index_stats(result)
        return result

    return wrapped


def _build_repository(*, root: Path) -> Repository:
    repository = Repository(
        db_path=root / "recoleta.db",
        title_dedup_threshold=0.0,
        title_dedup_max_candidates=0,
    )
    repository.init_schema()
    return repository


def _seed_analyzed_items(
    repository: Repository,
    *,
    period_start: datetime,
    items: int,
    content_chars: int,
) -> None:
    dense_chars = max(1200, int(content_chars))
    for idx in range(max(1, items)):
        published_at = period_start + timedelta(minutes=idx)
        title = (
            f"Agent memory routing for rover swarms {idx}"
            if idx % 2 == 0
            else f"Genome alignment cache for bio labs {idx}"
        )
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=f"bench-trends-item-{idx}",
            canonical_url=f"https://example.com/trends-item-{idx}",
            title=title,
            authors=["Bench"],
            published_at=published_at,
            raw_metadata={"bench": True},
        )
        item, _ = repository.upsert_item(draft)
        if item.id is None:
            raise RuntimeError("seeded item missing id")
        repeated = (
            f"{title}. Agents, memory, retrieval, ranking, benchmarks. " * 64
        )
        content = repeated[:dense_chars]
        repository.upsert_contents_texts(
            item_id=item.id,
            texts_by_type={"html_maintext": content},
        )
        repository.mark_item_enriched(item_id=item.id)
        repository.save_analysis(
            item_id=item.id,
            result=AnalysisResult(
                model="bench/fake-model",
                provider="bench",
                summary=(
                    f"Summary: {title}. "
                    f"Problem: multi-agent memory retrieval. "
                    f"Approach: vector ranking with caches. "
                    f"Results: lower latency and better recall."
                ),
                topics=["agents", "retrieval"],
                relevance_score=0.9,
                novelty_score=0.45,
                cost_usd=0.0,
                latency_ms=1,
            ),
            mirror_item_state=True,
        )


def _index_items_current(
    repository: Repository,
    *,
    run_id: str,
    period_start: datetime,
    period_end: datetime,
) -> dict[str, Any]:
    with repository.sql_diagnostics() as sql_diag:
        started = time.perf_counter()
        stats = index_items_as_documents(
            repository=repository,
            run_id=run_id,
            period_start=period_start,
            period_end=period_end,
        )
        wall_ms = int((time.perf_counter() - started) * 1000)
    return {
        "wall_ms": wall_ms,
        "sql_queries_total": int(sql_diag.queries_total),
        "sql_commits_total": int(sql_diag.commits_total),
        "stats": stats,
    }


def _index_items_batched(
    repository: Repository,
    *,
    period_start: datetime,
    period_end: datetime,
    content_chunk_chars: int = 1200,
    max_content_chunks_per_item: int = 8,
    min_relevance_score: float = 0.0,
) -> dict[str, Any]:
    started = time.perf_counter()
    pairs = repository.list_analyzed_items_in_period(
        period_start=period_start,
        period_end=period_end,
        limit=2000,
    )
    pairs, filtered_out_total = _filter_pairs_by_min_relevance(
        pairs,
        min_relevance_score=min_relevance_score,
    )
    docs_upserted = 0
    chunks_upserted = 0
    with repository.sql_diagnostics() as sql_diag:
        with Session(repository.engine) as session:
            docs_by_item_id: dict[int, Document] = {}
            for item, _analysis in pairs:
                raw_item_id = getattr(item, "id", None)
                if raw_item_id is None:
                    continue
                item_id = int(raw_item_id)
                doc = Document(
                    doc_type="item",
                    item_id=item_id,
                    source=str(getattr(item, "source", "") or "").strip() or None,
                    canonical_url=str(getattr(item, "canonical_url", "") or "").strip()
                    or None,
                    title=str(getattr(item, "title", "") or "").strip() or None,
                    published_at=getattr(item, "published_at", None)
                    or getattr(item, "created_at", None),
                )
                session.add(doc)
                docs_by_item_id[item_id] = doc
            session.flush()
            docs_upserted = len(docs_by_item_id)

            chunk_rows: list[DocumentChunk] = []
            for item, analysis in pairs:
                raw_item_id = getattr(item, "id", None)
                if raw_item_id is None:
                    continue
                item_id = int(raw_item_id)
                doc = docs_by_item_id.get(item_id)
                if doc is None or doc.id is None:
                    continue
                summary_text = str(getattr(analysis, "summary", "") or "").strip()
                if summary_text:
                    chunk_rows.append(
                        DocumentChunk(
                            doc_id=int(doc.id),
                            chunk_index=0,
                            kind="summary",
                            text=summary_text,
                            start_char=0,
                            end_char=None,
                            text_hash=sha256_hex(summary_text),
                            source_content_type="analysis_summary",
                        )
                    )
                texts = repository.get_latest_content_texts(
                    item_id=item_id,
                    content_types=[
                        "pdf_text",
                        "html_maintext",
                        "html_document_md",
                        "html_document",
                        "latex_source",
                    ],
                )
                chosen_text: str | None = None
                chosen_type: str | None = None
                for content_type in (
                    "pdf_text",
                    "html_maintext",
                    "html_document_md",
                    "html_document",
                    "latex_source",
                ):
                    candidate = texts.get(content_type)
                    if isinstance(candidate, str) and candidate.strip():
                        chosen_text = candidate
                        chosen_type = content_type
                        break
                if not chosen_text or chosen_type is None:
                    continue
                for chunk_index, (start_char, end_char, segment) in enumerate(
                    _chunk_text_segments(
                        chosen_text,
                        chunk_chars=content_chunk_chars,
                    )[: max(0, int(max_content_chunks_per_item))],
                    start=1,
                ):
                    chunk_rows.append(
                        DocumentChunk(
                            doc_id=int(doc.id),
                            chunk_index=chunk_index,
                            kind="content",
                            text=segment,
                            start_char=start_char,
                            end_char=end_char,
                            text_hash=sha256_hex(segment),
                            source_content_type=chosen_type,
                        )
                    )
            session.add_all(chunk_rows)
            session.flush()
            chunks_upserted = len(chunk_rows)
            fts_rows = [
                {
                    "rowid": int(chunk.id),
                    "text": str(chunk.text),
                    "doc_id": int(chunk.doc_id),
                    "chunk_index": int(chunk.chunk_index),
                    "kind": str(chunk.kind),
                }
                for chunk in chunk_rows
                if chunk.id is not None
            ]
            if fts_rows:
                session.connection().execute(
                    text(
                        "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
                        "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
                    ),
                    fts_rows,
                )
            repository._commit(session)
        wall_ms = int((time.perf_counter() - started) * 1000)
    return {
        "wall_ms": wall_ms,
        "sql_queries_total": int(sql_diag.queries_total),
        "sql_commits_total": int(sql_diag.commits_total),
        "stats": {
            "items_total": len(pairs),
            "items_filtered_out": filtered_out_total,
            "docs_upserted": docs_upserted,
            "docs_deleted": 0,
            "chunks_upserted": chunks_upserted,
            "content_chunks_upserted": max(0, chunks_upserted - docs_upserted),
            "content_chunks_deleted": 0,
            "duration_ms": wall_ms,
            "benchmark_mode": "cold_path_batch_insert",
        },
    }


def _list_item_documents(
    repository: Repository,
    *,
    period_start: datetime,
    period_end: datetime,
) -> list[Document]:
    return repository.list_documents(
        doc_type="item",
        period_start=period_start,
        period_end=period_end,
        order_by="event_desc",
        limit=5000,
    )


def _seed_trend_documents(
    repository: Repository,
    *,
    period_start: datetime,
    trend_docs: int,
) -> list[int]:
    doc_ids: list[int] = []
    for idx in range(max(1, trend_docs)):
        trend_start = period_start + timedelta(hours=idx)
        trend_end = trend_start + timedelta(hours=1)
        doc = repository.upsert_document_for_trend(
            granularity="day",
            period_start=trend_start,
            period_end=trend_end,
            title=f"Trend bench cluster {idx}",
        )
        if doc.id is None:
            raise RuntimeError("trend doc missing id")
        repository.upsert_document_chunk(
            doc_id=doc.id,
            chunk_index=0,
            kind="summary",
            text_value=f"Trend summary {idx}",
            start_char=0,
            end_char=None,
            source_content_type="trend_overview",
        )
        repository.upsert_document_chunk(
            doc_id=doc.id,
            chunk_index=1,
            kind="meta",
            text_value=json.dumps(
                {
                    "title": f"Trend bench cluster {idx}",
                    "overview_md": f"Overview {idx}",
                    "clusters": [],
                },
                ensure_ascii=False,
                separators=(",", ":"),
            ),
            start_char=0,
            end_char=None,
            source_content_type="trend_payload_json",
        )
        doc_ids.append(int(doc.id))
    return doc_ids


def _build_rep_payload(
    *,
    item_doc_ids: list[int],
    trend_doc_ids: list[int],
    clusters: int,
    scenario: str,
) -> TrendPayload:
    payload_clusters: list[TrendCluster] = []
    for idx in range(max(1, clusters)):
        if scenario == "pass_through":
            representatives = [
                TrendCluster.RepresentativeChunk(
                    doc_id=item_doc_ids[(idx + offset) % len(item_doc_ids)],
                    chunk_index=0,
                    score=0.95,
                )
                for offset in range(3)
            ]
            name = f"agents cluster {idx}"
            description = f"retrieval cache cluster {idx}"
        else:
            representatives = [
                TrendCluster.RepresentativeChunk(
                    doc_id=trend_doc_ids[(idx + offset) % len(trend_doc_ids)],
                    chunk_index=0,
                    score=0.81,
                )
                for offset in range(2)
            ]
            name = f"zxqv semantic fallback {idx}"
            description = f"unmatched representative fallback {idx}"
        payload_clusters.append(
            TrendCluster(
                name=name,
                description=description,
                representative_doc_ids=[],
                representative_chunks=representatives,
            )
        )
    return TrendPayload(
        title="Bench Trends",
        granularity="day",
        period_start=datetime.now(tz=UTC).isoformat(),
        period_end=(datetime.now(tz=UTC) + timedelta(days=1)).isoformat(),
        overview_md="- Bench overview",
        topics=["agents"],
        clusters=payload_clusters,
        highlights=[],
    )


def _run_stage_rep_enforcement_like_current(
    *,
    repository: Repository,
    payload: TrendPayload,
    lancedb_dir: Path,
    run_id: str,
    period_start: datetime,
    period_end: datetime,
    embedding_model: str,
    embedding_dimensions: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    rep_dropped_non_item_total = 0
    rep_backfilled_total = 0
    rep_failed_clusters_total = 0
    get_document_calls = 0
    text_search_calls = 0
    semantic_search_calls = 0
    rep_doc_type_cache: dict[int, str | None] = {}

    def _doc_type_for_doc_id(doc_id_value: int) -> str | None:
        nonlocal get_document_calls
        normalized_doc_id = int(doc_id_value)
        if normalized_doc_id <= 0:
            return None
        if normalized_doc_id not in rep_doc_type_cache:
            get_document_calls += 1
            doc = repository.get_document(doc_id=normalized_doc_id)
            if doc is None:
                rep_doc_type_cache[normalized_doc_id] = None
            else:
                rep_doc_type_cache[normalized_doc_id] = (
                    str(getattr(doc, "doc_type", "") or "").strip().lower() or None
                )
        return rep_doc_type_cache.get(normalized_doc_id)

    def _cluster_queries(cluster: Any) -> list[str]:
        candidates = [
            " ".join(
                [
                    str(getattr(cluster, "name", "") or "").strip(),
                    str(getattr(cluster, "description", "") or "").strip(),
                ]
            ).strip(),
            str(getattr(cluster, "name", "") or "").strip(),
            str(getattr(cluster, "description", "") or "").strip(),
        ]
        out: list[str] = []
        seen: set[str] = set()
        for candidate in candidates:
            normalized = " ".join(str(candidate or "").split()).strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            out.append(normalized)
        return out

    def _backfill_item_reps_text(cluster: Any, *, limit: int) -> list[TrendCluster.RepresentativeChunk]:
        nonlocal text_search_calls
        reps: list[TrendCluster.RepresentativeChunk] = []
        seen: set[tuple[int, int]] = set()
        for query in _cluster_queries(cluster):
            text_search_calls += 1
            rows = repository.search_chunks_text(
                query=query,
                doc_type="item",
                period_start=period_start,
                period_end=period_end,
                limit=limit,
            )
            for row in rows or []:
                if not isinstance(row, dict):
                    continue
                try:
                    doc_id_int = int(row.get("doc_id") or 0)
                    chunk_index_int = int(row.get("chunk_index") or -1)
                except Exception:
                    continue
                if doc_id_int <= 0 or chunk_index_int < 0:
                    continue
                key = (doc_id_int, chunk_index_int)
                if key in seen:
                    continue
                seen.add(key)
                reps.append(
                    TrendCluster.RepresentativeChunk(
                        doc_id=doc_id_int,
                        chunk_index=chunk_index_int,
                        score=None,
                    )
                )
                if len(reps) >= limit:
                    return reps
        return reps

    def _backfill_item_reps_semantic(
        cluster: Any,
        *,
        limit: int,
    ) -> list[TrendCluster.RepresentativeChunk]:
        nonlocal semantic_search_calls
        queries = _cluster_queries(cluster)
        if not queries:
            return []
        semantic_search_calls += 1
        hits = semantic_search_summaries_in_period(
            repository=repository,
            lancedb_dir=lancedb_dir,
            run_id=run_id,
            doc_type="item",
            period_start=period_start,
            period_end=period_end,
            query=queries[0],
            embedding_model=embedding_model,
            embedding_dimensions=embedding_dimensions,
            max_batch_inputs=64,
            max_batch_chars=24000,
            limit=limit,
            metric_namespace=None,
            llm_connection=None,
        )
        reps: list[TrendCluster.RepresentativeChunk] = []
        seen: set[tuple[int, int]] = set()
        for hit in hits:
            key = (int(hit.doc_id), int(hit.chunk_index))
            if key[0] <= 0 or key[1] < 0 or key in seen:
                continue
            seen.add(key)
            reps.append(
                TrendCluster.RepresentativeChunk(
                    doc_id=key[0],
                    chunk_index=key[1],
                    score=round(float(hit.score), 6),
                )
            )
            if len(reps) >= limit:
                break
        return reps

    max_reps = 6
    with repository.sql_diagnostics() as sql_diag:
        for cluster in list(payload.clusters or []):
            cleaned: list[TrendCluster.RepresentativeChunk] = []
            seen_rep_keys: set[tuple[int, int]] = set()
            for rep in list(cluster.representative_chunks or []):
                try:
                    rep_key = (int(getattr(rep, "doc_id")), int(getattr(rep, "chunk_index")))
                except Exception:
                    continue
                if rep_key[0] <= 0 or rep_key[1] < 0:
                    continue
                doc_type = _doc_type_for_doc_id(rep_key[0])
                if doc_type != "item":
                    rep_dropped_non_item_total += 1
                    continue
                if rep_key in seen_rep_keys:
                    continue
                seen_rep_keys.add(rep_key)
                cleaned.append(rep)
            cluster.representative_chunks = cleaned[:max_reps]
            if cluster.representative_chunks:
                continue
            backfilled = _backfill_item_reps_text(cluster, limit=max_reps)
            if not backfilled:
                backfilled = _backfill_item_reps_semantic(cluster, limit=max_reps)
            if backfilled:
                cluster.representative_chunks = backfilled[:max_reps]
                rep_backfilled_total += 1
            else:
                cluster.representative_chunks = []
                rep_failed_clusters_total += 1
        wall_ms = int((time.perf_counter() - started) * 1000)
    return {
        "wall_ms": wall_ms,
        "sql_queries_total": int(sql_diag.queries_total),
        "sql_commits_total": int(sql_diag.commits_total),
        "get_document_calls": get_document_calls,
        "text_search_calls": text_search_calls,
        "semantic_search_calls": semantic_search_calls,
        "dropped_non_item_total": rep_dropped_non_item_total,
        "backfilled_total": rep_backfilled_total,
        "failed_clusters_total": rep_failed_clusters_total,
    }


def _run_semantic_cache_benchmark(
    *,
    items: int,
    queries: int,
    repeats: int,
) -> dict[str, Any]:
    def _one_run(*, cached: bool) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="recoleta-bench-trends-cache-") as tmpdir:
            root = Path(tmpdir)
            repository = _build_repository(root=root)
            period_start, period_end = day_period_bounds(datetime.now(tz=UTC).date())
            _seed_analyzed_items(
                repository,
                period_start=period_start,
                items=items,
                content_chars=3200,
            )
            _ = _index_items_current(
                repository,
                run_id="bench-index",
                period_start=period_start,
                period_end=period_end,
            )
            ensure_stats = _EnsureStats()
            wrapped = _wrap_ensure_summary_vectors(
                cached=cached,
                ensure_stats=ensure_stats,
            )
            with ExitStack() as stack:
                _with_fake_embeddings(stack)
                stack.enter_context(
                    patch.object(
                        rag_semantic_search,
                        "ensure_summary_vectors_for_period",
                        wrapped,
                    )
                )
                search_queries = [
                    f"agents retrieval benchmark query {idx}"
                    for idx in range(max(1, queries))
                ]
                with repository.sql_diagnostics() as sql_diag:
                    started = time.perf_counter()
                    returned_total = 0
                    for idx, query in enumerate(search_queries):
                        hits = semantic_search_summaries_in_period(
                            repository=repository,
                            lancedb_dir=root / "lancedb",
                            run_id=f"bench-cache-{idx}",
                            doc_type="item",
                            period_start=period_start,
                            period_end=period_end,
                            query=query,
                            embedding_model="bench/embedding",
                            embedding_dimensions=16,
                            max_batch_inputs=64,
                            max_batch_chars=24000,
                            limit=12,
                            metric_namespace=None,
                            llm_connection=None,
                        )
                        returned_total += len(hits)
                    wall_ms = int((time.perf_counter() - started) * 1000)
                return {
                    "wall_ms": wall_ms,
                    "sql_queries_total": int(sql_diag.queries_total),
                    "sql_commits_total": int(sql_diag.commits_total),
                    "ensure_invocations_total": ensure_stats.invocations_total,
                    "ensure_misses_total": ensure_stats.misses_total,
                    "ensure_cache_hits_total": ensure_stats.cache_hits_total,
                    "ensure_wall_ms_total": ensure_stats.wall_ms_total,
                    "returned_hits_total": returned_total,
                }

    baseline_runs = [_one_run(cached=False) for _ in range(max(1, repeats))]
    cached_runs = [_one_run(cached=True) for _ in range(max(1, repeats))]
    baseline = {
        "wall_ms_median": _median([float(run["wall_ms"]) for run in baseline_runs]),
        "sql_queries_total_median": _median(
            [float(run["sql_queries_total"]) for run in baseline_runs]
        ),
        "ensure_misses_total_median": _median(
            [float(run["ensure_misses_total"]) for run in baseline_runs]
        ),
        "ensure_wall_ms_total_median": _median(
            [float(run["ensure_wall_ms_total"]) for run in baseline_runs]
        ),
    }
    cached = {
        "wall_ms_median": _median([float(run["wall_ms"]) for run in cached_runs]),
        "sql_queries_total_median": _median(
            [float(run["sql_queries_total"]) for run in cached_runs]
        ),
        "ensure_misses_total_median": _median(
            [float(run["ensure_misses_total"]) for run in cached_runs]
        ),
        "ensure_cache_hits_total_median": _median(
            [float(run["ensure_cache_hits_total"]) for run in cached_runs]
        ),
        "ensure_wall_ms_total_median": _median(
            [float(run["ensure_wall_ms_total"]) for run in cached_runs]
        ),
    }
    return {
        "config": {"items": items, "queries": queries, "repeats": repeats},
        "baseline": baseline,
        "cached": cached,
        "delta": {
            "wall_ms_improvement_pct": _pct_improvement(
                baseline=baseline["wall_ms_median"],
                candidate=cached["wall_ms_median"],
            ),
            "sql_queries_reduction_pct": _pct_improvement(
                baseline=baseline["sql_queries_total_median"],
                candidate=cached["sql_queries_total_median"],
            ),
        },
    }


def _run_index_batch_benchmark(
    *,
    items: int,
    repeats: int,
) -> dict[str, Any]:
    def _one_run(*, batched: bool) -> dict[str, Any]:
        with tempfile.TemporaryDirectory(prefix="recoleta-bench-trends-index-") as tmpdir:
            root = Path(tmpdir)
            repository = _build_repository(root=root)
            period_start, period_end = day_period_bounds(datetime.now(tz=UTC).date())
            _seed_analyzed_items(
                repository,
                period_start=period_start,
                items=items,
                content_chars=7200,
            )
            if batched:
                return _index_items_batched(
                    repository,
                    period_start=period_start,
                    period_end=period_end,
                )
            return _index_items_current(
                repository,
                run_id="bench-index",
                period_start=period_start,
                period_end=period_end,
            )

    baseline_runs = [_one_run(batched=False) for _ in range(max(1, repeats))]
    batched_runs = [_one_run(batched=True) for _ in range(max(1, repeats))]
    baseline = {
        "wall_ms_median": _median([float(run["wall_ms"]) for run in baseline_runs]),
        "sql_queries_total_median": _median(
            [float(run["sql_queries_total"]) for run in baseline_runs]
        ),
        "sql_commits_total_median": _median(
            [float(run["sql_commits_total"]) for run in baseline_runs]
        ),
    }
    batched = {
        "wall_ms_median": _median([float(run["wall_ms"]) for run in batched_runs]),
        "sql_queries_total_median": _median(
            [float(run["sql_queries_total"]) for run in batched_runs]
        ),
        "sql_commits_total_median": _median(
            [float(run["sql_commits_total"]) for run in batched_runs]
        ),
    }
    return {
        "config": {
            "items": items,
            "repeats": repeats,
            "benchmark_mode": "cold_path",
        },
        "baseline": baseline,
        "batched": batched,
        "delta": {
            "wall_ms_improvement_pct": _pct_improvement(
                baseline=baseline["wall_ms_median"],
                candidate=batched["wall_ms_median"],
            ),
            "sql_queries_reduction_pct": _pct_improvement(
                baseline=baseline["sql_queries_total_median"],
                candidate=batched["sql_queries_total_median"],
            ),
            "sql_commits_reduction_pct": _pct_improvement(
                baseline=baseline["sql_commits_total_median"],
                candidate=batched["sql_commits_total_median"],
            ),
        },
    }


def _run_rep_enforcement_benchmark(
    *,
    items: int,
    clusters: int,
    repeats: int,
) -> dict[str, Any]:
    def _scenario_runs(scenario: str) -> list[dict[str, Any]]:
        runs: list[dict[str, Any]] = []
        for _ in range(max(1, repeats)):
            with tempfile.TemporaryDirectory(prefix="recoleta-bench-trends-reps-") as tmpdir:
                root = Path(tmpdir)
                repository = _build_repository(root=root)
                period_start, period_end = day_period_bounds(datetime.now(tz=UTC).date())
                _seed_analyzed_items(
                    repository,
                    period_start=period_start,
                    items=items,
                    content_chars=2800,
                )
                _ = _index_items_current(
                    repository,
                    run_id="bench-index",
                    period_start=period_start,
                    period_end=period_end,
                )
                item_docs = _list_item_documents(
                    repository,
                    period_start=period_start,
                    period_end=period_end,
                )
                item_doc_ids = [int(doc.id) for doc in item_docs if doc.id is not None]
                if not item_doc_ids:
                    raise RuntimeError("item document seeding failed")
                trend_doc_ids = _seed_trend_documents(
                    repository,
                    period_start=period_start,
                    trend_docs=max(6, clusters),
                )
                payload = _build_rep_payload(
                    item_doc_ids=item_doc_ids,
                    trend_doc_ids=trend_doc_ids,
                    clusters=clusters,
                    scenario=scenario,
                )
                with ExitStack() as stack:
                    _with_fake_embeddings(stack)
                    current = _run_stage_rep_enforcement_like_current(
                        repository=repository,
                        payload=copy.deepcopy(payload),
                        lancedb_dir=root / "lancedb",
                        run_id=f"bench-reps-{scenario}",
                        period_start=period_start,
                        period_end=period_end,
                        embedding_model="bench/embedding",
                        embedding_dimensions=16,
                    )
                runs.append(current)
        return runs

    pass_through_runs = _scenario_runs("pass_through")
    forced_rebackfill_runs = _scenario_runs("forced_rebackfill")

    def _summarize(runs: list[dict[str, Any]]) -> dict[str, float]:
        return {
            "wall_ms_median": _median([float(run["wall_ms"]) for run in runs]),
            "sql_queries_total_median": _median(
                [float(run["sql_queries_total"]) for run in runs]
            ),
            "get_document_calls_median": _median(
                [float(run["get_document_calls"]) for run in runs]
            ),
            "text_search_calls_median": _median(
                [float(run["text_search_calls"]) for run in runs]
            ),
            "semantic_search_calls_median": _median(
                [float(run["semantic_search_calls"]) for run in runs]
            ),
            "backfilled_total_median": _median(
                [float(run["backfilled_total"]) for run in runs]
            ),
        }

    pass_through = _summarize(pass_through_runs)
    forced_rebackfill = _summarize(forced_rebackfill_runs)
    return {
        "config": {"items": items, "clusters": clusters, "repeats": repeats},
        "pass_through_item_reps": pass_through,
        "forced_rebackfill_upper_bound": forced_rebackfill,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run controlled trends hotspot benchmarks and print JSON."
    )
    parser.add_argument("--items", type=int, default=96)
    parser.add_argument("--queries", type=int, default=6)
    parser.add_argument("--clusters", type=int, default=24)
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    if not args.verbose:
        logger.remove()

    output = {
        "config": {
            "items": max(1, args.items),
            "queries": max(1, args.queries),
            "clusters": max(1, args.clusters),
            "repeats": max(1, args.repeats),
            "verbose": bool(args.verbose),
        },
        "semantic_corpus_cache": _run_semantic_cache_benchmark(
            items=max(1, args.items),
            queries=max(1, args.queries),
            repeats=max(1, args.repeats),
        ),
        "index_batching": _run_index_batch_benchmark(
            items=max(1, args.items),
            repeats=max(1, args.repeats),
        ),
        "rep_enforcement": _run_rep_enforcement_benchmark(
            items=max(1, args.items),
            clusters=max(1, args.clusters),
            repeats=max(1, args.repeats),
        ),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
