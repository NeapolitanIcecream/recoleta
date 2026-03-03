from __future__ import annotations

import hashlib
import math
import random
import time
from dataclasses import dataclass
from typing import Any, Sequence

from rapidfuzz import fuzz

from recoleta.models import Item
from recoleta.rag.embeddings import Embedder, LiteLLMEmbedder, iter_embedding_batches

_DEFAULT_EMBEDDING_BATCH_MAX_INPUTS = 64
_DEFAULT_EMBEDDING_BATCH_MAX_CHARS = 40_000


def _merge_usage_totals(totals: dict[str, float], usage: Any) -> None:
    if not isinstance(usage, dict):
        return
    for key, value in usage.items():
        if isinstance(value, (int, float)):
            totals[str(key)] = float(totals.get(str(key), 0.0)) + float(value)


@dataclass(slots=True)
class TriageCandidate:
    item: Item
    text: str


@dataclass(slots=True)
class TriageScoredCandidate:
    candidate: TriageCandidate
    score: float


@dataclass(slots=True)
class TriageStats:
    candidates_total: int
    scored_total: int
    selected_total: int
    skipped_total: int
    embedding_calls_total: int
    embedding_errors_total: int
    duration_ms: int
    method: str
    embedding_prompt_tokens_total: int | None = None
    embedding_prompt_tokens_missing_total: int | None = None
    embedding_cost_usd_total: float | None = None
    embedding_cost_missing_total: int | None = None


@dataclass(slots=True)
class TriageOutput:
    selected: list[TriageScoredCandidate]
    stats: TriageStats
    artifacts: dict[str, dict[str, Any]]


class SemanticTriage:
    def __init__(
        self,
        *,
        embedder: Embedder | None = None,
        embedding_batch_max_inputs: int = _DEFAULT_EMBEDDING_BATCH_MAX_INPUTS,
        embedding_batch_max_chars: int = _DEFAULT_EMBEDDING_BATCH_MAX_CHARS,
    ) -> None:
        self.embedder = embedder or LiteLLMEmbedder()
        self.embedding_batch_max_inputs = max(1, int(embedding_batch_max_inputs))
        self.embedding_batch_max_chars = max(1, int(embedding_batch_max_chars))

    def select(
        self,
        *,
        run_id: str,
        candidates: list[TriageCandidate],
        topics: list[str],
        limit: int,
        mode: str,
        query_mode: str,
        embedding_model: str,
        embedding_dimensions: int | None,
        min_similarity: float,
        exploration_rate: float,
        recency_floor: int,
        include_debug: bool,
    ) -> TriageOutput:
        started = time.perf_counter()
        artifacts: dict[str, dict[str, Any]] = {}

        if limit <= 0 or not candidates:
            duration_ms = int((time.perf_counter() - started) * 1000)
            stats = TriageStats(
                candidates_total=len(candidates),
                scored_total=0,
                selected_total=0,
                skipped_total=0,
                embedding_calls_total=0,
                embedding_errors_total=0,
                duration_ms=duration_ms,
                method="noop",
            )
            return TriageOutput(selected=[], stats=stats, artifacts={})

        normalized_topics = [
            str(topic).strip() for topic in topics if str(topic).strip()
        ]
        if not normalized_topics:
            duration_ms = int((time.perf_counter() - started) * 1000)
            selected = [
                TriageScoredCandidate(candidate=candidate, score=0.0)
                for candidate in candidates[:limit]
            ]
            stats = TriageStats(
                candidates_total=len(candidates),
                scored_total=0,
                selected_total=len(selected),
                skipped_total=0,
                embedding_calls_total=0,
                embedding_errors_total=0,
                duration_ms=duration_ms,
                method="topics_empty_fallback",
            )
            return TriageOutput(selected=selected, stats=stats, artifacts={})

        embedding_calls_total = 0
        embedding_errors_total = 0
        method = "embedding_cosine"
        embedding_prompt_tokens_total = 0
        embedding_prompt_tokens_missing_total = 0
        embedding_cost_usd_total = 0.0
        embedding_cost_missing_total = 0

        def _accumulate_embedding_debug(debug: Any) -> None:
            nonlocal embedding_prompt_tokens_total
            nonlocal embedding_prompt_tokens_missing_total
            nonlocal embedding_cost_usd_total
            nonlocal embedding_cost_missing_total

            if not isinstance(debug, dict):
                embedding_prompt_tokens_missing_total += 1
                embedding_cost_missing_total += 1
                return

            raw_prompt = debug.get("prompt_tokens")
            if raw_prompt is None:
                raw_prompt = debug.get("total_tokens")
            if isinstance(raw_prompt, (int, float)):
                embedding_prompt_tokens_total += int(raw_prompt)
            else:
                embedding_prompt_tokens_missing_total += 1

            raw_cost = debug.get("cost_usd")
            if isinstance(raw_cost, (int, float)):
                embedding_cost_usd_total += float(raw_cost)
            else:
                embedding_cost_missing_total += 1

        embedding_request: dict[str, Any] | None = None
        if include_debug:
            embedding_request = {
                "run_id_fingerprint": _fingerprint(run_id),
                "model": embedding_model,
                "dimensions": embedding_dimensions,
                "query_mode": query_mode,
                "topics_total": len(normalized_topics),
                "candidates_total": len(candidates),
                "batching": {
                    "max_inputs": self.embedding_batch_max_inputs,
                    "max_chars": self.embedding_batch_max_chars,
                },
            }

        embedding_debug: dict[str, Any] | None = None
        try:
            embedding_calls_total += 1
            query_vectors, query_debug = self._embed_query(
                topics=normalized_topics,
                query_mode=query_mode,
                model=embedding_model,
                dimensions=embedding_dimensions,
            )
            _accumulate_embedding_debug(query_debug)
            embedding_debug = {"query": query_debug}

            item_texts = [candidate.text for candidate in candidates]
            item_vectors: list[list[float]] = []
            items_usage_totals: dict[str, float] = {}
            items_elapsed_ms_total = 0
            items_batches_total = 0
            items_batch_inputs_max = 0
            items_batch_chars_max = 0
            items_sample_head: list[float] = []

            for batch in iter_embedding_batches(
                item_texts,
                max_batch_inputs=self.embedding_batch_max_inputs,
                max_batch_chars=self.embedding_batch_max_chars,
            ):
                items_batches_total += 1
                items_batch_inputs_max = max(items_batch_inputs_max, len(batch))
                items_batch_chars_max = max(
                    items_batch_chars_max, sum(len(text) for text in batch)
                )

                embedding_calls_total += 1
                batch_vectors, batch_debug = self.embedder.embed(
                    model=embedding_model,
                    inputs=batch,
                    dimensions=embedding_dimensions,
                )
                _accumulate_embedding_debug(batch_debug)
                if len(batch_vectors) != len(batch):
                    raise ValueError("embedding output size mismatch")
                item_vectors.extend(batch_vectors)

                if not items_sample_head and batch_vectors and batch_vectors[0]:
                    items_sample_head = [float(value) for value in batch_vectors[0][:8]]
                if isinstance(batch_debug, dict):
                    raw_elapsed_ms = batch_debug.get("elapsed_ms")
                    if isinstance(raw_elapsed_ms, (int, float)):
                        items_elapsed_ms_total += int(raw_elapsed_ms)
                    _merge_usage_totals(items_usage_totals, batch_debug.get("usage"))

            if len(item_vectors) != len(candidates):
                raise ValueError("embedding output size mismatch")

            items_debug: dict[str, Any] = {
                "model": embedding_model,
                "inputs_total": len(item_texts),
                "dimensions": embedding_dimensions,
                "batching": {
                    "max_inputs": self.embedding_batch_max_inputs,
                    "max_chars": self.embedding_batch_max_chars,
                },
                "batches_total": items_batches_total,
                "batch_inputs_max": items_batch_inputs_max,
                "batch_chars_max": items_batch_chars_max,
                "elapsed_ms_total": items_elapsed_ms_total,
                "usage_total": items_usage_totals or None,
                "sample_embedding_head": items_sample_head,
            }
            embedding_debug["items"] = items_debug
            scored = self._score_with_vectors(
                candidates=candidates,
                query_vectors=query_vectors,
                item_vectors=item_vectors,
            )
        except Exception as exc:  # noqa: BLE001
            embedding_errors_total += 1
            method = "fuzz_title"
            scored = self._score_with_rapidfuzz(
                candidates=candidates, topics=normalized_topics
            )
            if include_debug:
                payload: dict[str, Any] = {
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
                if embedding_debug is not None:
                    payload["debug"] = embedding_debug
                artifacts["embedding_response"] = payload

        if include_debug and embedding_request is not None:
            artifacts.setdefault("embedding_request", embedding_request)
            if embedding_debug is not None:
                artifacts.setdefault("embedding_response", embedding_debug)

        selected, skipped_total = self._select_from_scored(
            run_id=run_id,
            scored=scored,
            limit=limit,
            mode=mode,
            min_similarity=min_similarity,
            exploration_rate=exploration_rate,
            recency_floor=recency_floor,
        )

        duration_ms = int((time.perf_counter() - started) * 1000)
        prompt_tokens_total: int | None = None
        if embedding_calls_total <= 0:
            prompt_tokens_total = 0
        elif embedding_prompt_tokens_total > 0:
            prompt_tokens_total = embedding_prompt_tokens_total
        cost_usd_total: float | None = None
        if embedding_calls_total <= 0:
            cost_usd_total = 0.0
        elif embedding_cost_usd_total > 0.0:
            cost_usd_total = embedding_cost_usd_total
        stats = TriageStats(
            candidates_total=len(candidates),
            scored_total=len(scored),
            selected_total=len(selected),
            skipped_total=skipped_total,
            embedding_calls_total=embedding_calls_total,
            embedding_errors_total=embedding_errors_total,
            duration_ms=duration_ms,
            method=method,
            embedding_prompt_tokens_total=prompt_tokens_total,
            embedding_prompt_tokens_missing_total=embedding_prompt_tokens_missing_total
            if embedding_calls_total > 0
            else 0,
            embedding_cost_usd_total=cost_usd_total,
            embedding_cost_missing_total=embedding_cost_missing_total
            if embedding_calls_total > 0
            else 0,
        )

        if include_debug:
            artifacts["triage_summary"] = _build_triage_summary(
                run_id=run_id,
                mode=mode,
                method=method,
                min_similarity=min_similarity,
                exploration_rate=exploration_rate,
                recency_floor=recency_floor,
                stats=stats,
                scored=scored,
                selected=selected,
            )

        return TriageOutput(selected=selected, stats=stats, artifacts=artifacts)

    def _embed_query(
        self,
        *,
        topics: list[str],
        query_mode: str,
        model: str,
        dimensions: int | None,
    ) -> tuple[list[list[float]], dict[str, Any]]:
        if query_mode == "joined":
            query = "User topics: " + ", ".join(topics)
            vectors, debug = self.embedder.embed(
                model=model, inputs=[query], dimensions=dimensions
            )
            if len(vectors) != 1:
                raise ValueError("query embedding output size mismatch")
            return vectors, debug
        if query_mode == "max_per_topic":
            vectors, debug = self.embedder.embed(
                model=model, inputs=topics, dimensions=dimensions
            )
            if len(vectors) != len(topics):
                raise ValueError("topic embeddings output size mismatch")
            return vectors, debug
        raise ValueError("unsupported triage query_mode")

    @staticmethod
    def _score_with_vectors(
        *,
        candidates: list[TriageCandidate],
        query_vectors: list[list[float]],
        item_vectors: list[list[float]],
    ) -> list[TriageScoredCandidate]:
        scored: list[TriageScoredCandidate] = []
        for candidate, item_vec in zip(candidates, item_vectors, strict=True):
            best = 0.0
            for query_vec in query_vectors:
                best = max(best, _bounded_cosine_similarity(query_vec, item_vec))
            scored.append(TriageScoredCandidate(candidate=candidate, score=best))
        return scored

    @staticmethod
    def _score_with_rapidfuzz(
        *, candidates: list[TriageCandidate], topics: list[str]
    ) -> list[TriageScoredCandidate]:
        query = ", ".join(topics)
        scored: list[TriageScoredCandidate] = []
        for candidate in candidates:
            title = str(getattr(candidate.item, "title", "") or "").strip()
            ratio = (
                float(fuzz.token_set_ratio(title, query)) if title and query else 0.0
            )
            scored.append(
                TriageScoredCandidate(
                    candidate=candidate, score=max(0.0, min(1.0, ratio / 100.0))
                )
            )
        return scored

    @staticmethod
    def _select_from_scored(
        *,
        run_id: str,
        scored: list[TriageScoredCandidate],
        limit: int,
        mode: str,
        min_similarity: float,
        exploration_rate: float,
        recency_floor: int,
    ) -> tuple[list[TriageScoredCandidate], int]:
        if limit <= 0 or not scored:
            return [], 0

        normalized_mode = str(mode or "").strip().lower()
        if normalized_mode not in {"prioritize", "filter"}:
            normalized_mode = "prioritize"

        recency_n = max(0, min(int(recency_floor), limit, len(scored)))
        recency_items = scored[:recency_n]
        recency_ids = {
            item.candidate.item.id
            for item in recency_items
            if item.candidate.item.id is not None
        }

        remaining = [
            entry for entry in scored if entry.candidate.item.id not in recency_ids
        ]

        eligible = remaining
        skipped_total = 0
        if normalized_mode == "filter":
            threshold = max(0.0, min(1.0, float(min_similarity)))
            eligible = [entry for entry in remaining if entry.score >= threshold]
            skipped_total = sum(1 for entry in remaining if entry.score < threshold)

        def sort_key(entry: TriageScoredCandidate) -> tuple[float, float]:
            created_ts = 0.0
            created_at = getattr(entry.candidate.item, "created_at", None)
            if created_at is not None:
                created_ts = float(getattr(created_at, "timestamp")())
            return (entry.score, created_ts)

        eligible_sorted = sorted(eligible, key=sort_key, reverse=True)

        remaining_slots = max(0, limit - len(recency_items))
        exploration_slots = max(
            0,
            min(
                remaining_slots,
                int(math.floor(limit * max(0.0, float(exploration_rate)))),
            ),
        )
        exploitation_slots = max(0, remaining_slots - exploration_slots)

        exploitation = eligible_sorted[:exploitation_slots]
        selected_ids = {
            entry.candidate.item.id
            for entry in recency_items + exploitation
            if entry.candidate.item.id is not None
        }

        exploration_pool = [
            entry
            for entry in eligible_sorted[exploitation_slots:]
            if entry.candidate.item.id not in selected_ids
        ]
        exploration: list[TriageScoredCandidate] = []
        if exploration_slots > 0 and exploration_pool:
            rng = random.Random(_stable_seed(run_id))
            exploration = rng.sample(
                exploration_pool, k=min(exploration_slots, len(exploration_pool))
            )

        selected = recency_items + exploitation + exploration
        selected = sorted(selected, key=sort_key, reverse=True)
        return selected[:limit], skipped_total


def _bounded_cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    cosine = _cosine_similarity(a, b)
    if not math.isfinite(cosine):
        return 0.0
    return max(0.0, min(1.0, cosine))


def _cosine_similarity(a: Sequence[float], b: Sequence[float]) -> float:
    dot = 0.0
    norm_a = 0.0
    norm_b = 0.0
    for x, y in zip(a, b, strict=True):
        fx = float(x)
        fy = float(y)
        dot += fx * fy
        norm_a += fx * fx
        norm_b += fy * fy
    if norm_a <= 0.0 or norm_b <= 0.0:
        return 0.0
    return dot / (math.sqrt(norm_a) * math.sqrt(norm_b))


def _stable_seed(value: str) -> int:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def _build_triage_summary(
    *,
    run_id: str,
    mode: str,
    method: str,
    min_similarity: float,
    exploration_rate: float,
    recency_floor: int,
    stats: TriageStats,
    scored: list[TriageScoredCandidate],
    selected: list[TriageScoredCandidate],
) -> dict[str, Any]:
    def preview(
        entries: list[TriageScoredCandidate], *, limit: int
    ) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for entry in entries[:limit]:
            item = entry.candidate.item
            title = str(getattr(item, "title", "") or "").strip()
            if len(title) > 140:
                title = title[:140] + "..."
            rows.append(
                {
                    "item_id": item.id,
                    "source": getattr(item, "source", None),
                    "score": round(float(entry.score), 4),
                    "title": title,
                }
            )
        return rows

    scored_sorted = sorted(scored, key=lambda e: e.score, reverse=True)
    return {
        "run_id_fingerprint": _fingerprint(run_id),
        "mode": mode,
        "method": method,
        "min_similarity": float(min_similarity),
        "exploration_rate": float(exploration_rate),
        "recency_floor": int(recency_floor),
        "stats": {
            "candidates_total": stats.candidates_total,
            "scored_total": stats.scored_total,
            "selected_total": stats.selected_total,
            "skipped_total": stats.skipped_total,
            "embedding_calls_total": stats.embedding_calls_total,
            "embedding_errors_total": stats.embedding_errors_total,
            "duration_ms": stats.duration_ms,
        },
        "selected_preview": preview(selected, limit=20),
        "top_scores_preview": preview(scored_sorted, limit=20),
    }
