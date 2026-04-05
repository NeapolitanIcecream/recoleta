from __future__ import annotations

import hashlib
import math
import random
import time
from dataclasses import dataclass
from typing import Any, Sequence

from rapidfuzz import fuzz

from recoleta.llm_connection import LLMConnectionConfig
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
    embedding_cost_usd_total: float | None = None
    embedding_cost_missing_total: int | None = None


@dataclass(slots=True)
class TriageOutput:
    selected: list[TriageScoredCandidate]
    stats: TriageStats
    artifacts: dict[str, dict[str, Any]]


@dataclass(slots=True)
class _EmbeddingDebugTotals:
    calls_total: int = 0
    errors_total: int = 0
    prompt_tokens_total: int = 0
    prompt_tokens_missing_total: int = 0
    cost_usd_total: float = 0.0
    cost_missing_total: int = 0

    def record_call(self) -> None:
        self.calls_total += 1

    def record_error(self) -> None:
        self.errors_total += 1

    def absorb_debug(self, debug: Any) -> None:
        if not isinstance(debug, dict):
            self.prompt_tokens_missing_total += 1
            self.cost_missing_total += 1
            return
        raw_prompt = debug.get("prompt_tokens")
        if raw_prompt is None:
            raw_prompt = debug.get("total_tokens")
        if isinstance(raw_prompt, (int, float)):
            self.prompt_tokens_total += int(raw_prompt)
        else:
            self.prompt_tokens_missing_total += 1
        raw_cost = debug.get("cost_usd")
        if isinstance(raw_cost, (int, float)):
            self.cost_usd_total += float(raw_cost)
        else:
            self.cost_missing_total += 1


@dataclass(slots=True)
class _TriageScoringResult:
    scored: list[TriageScoredCandidate]
    method: str
    debug_totals: _EmbeddingDebugTotals
    embedding_request: dict[str, Any] | None = None
    embedding_response: dict[str, Any] | None = None


@dataclass(slots=True)
class _EmbeddingRunContext:
    run_id: str
    candidates: list[TriageCandidate]
    topics: list[str]
    query_mode: str
    embedding_model: str
    embedding_dimensions: int | None
    include_debug: bool


@dataclass(slots=True)
class _TriageSelectionConfig:
    run_id: str
    limit: int
    mode: str
    min_similarity: float
    exploration_rate: float
    recency_floor: int


@dataclass(slots=True)
class _TriageStatsContext:
    candidates_total: int
    scored_total: int
    selected_total: int
    skipped_total: int
    duration_ms: int
    method: str
    debug_totals: _EmbeddingDebugTotals


@dataclass(slots=True)
class _TriageArtifactsContext:
    run_id: str
    include_debug: bool
    scoring: _TriageScoringResult
    mode: str
    min_similarity: float
    exploration_rate: float
    recency_floor: int
    stats: TriageStats
    selected: list[TriageScoredCandidate]


@dataclass(slots=True)
class TriageSelectionRequest:
    run_id: str
    candidates: list[TriageCandidate]
    topics: list[str]
    limit: int
    mode: str
    query_mode: str
    embedding_model: str
    embedding_dimensions: int | None
    min_similarity: float
    exploration_rate: float
    recency_floor: int
    include_debug: bool


def _coerce_triage_selection_request(
    *,
    request: TriageSelectionRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> TriageSelectionRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return TriageSelectionRequest(
        run_id=str(values["run_id"]),
        candidates=list(values["candidates"]),
        topics=list(values["topics"]),
        limit=int(values["limit"]),
        mode=str(values["mode"]),
        query_mode=str(values["query_mode"]),
        embedding_model=str(values["embedding_model"]),
        embedding_dimensions=values.get("embedding_dimensions"),
        min_similarity=float(values["min_similarity"]),
        exploration_rate=float(values["exploration_rate"]),
        recency_floor=int(values["recency_floor"]),
        include_debug=bool(values["include_debug"]),
    )


class SemanticTriage:
    def __init__(
        self,
        *,
        embedder: Embedder | None = None,
        embedding_batch_max_inputs: int = _DEFAULT_EMBEDDING_BATCH_MAX_INPUTS,
        embedding_batch_max_chars: int = _DEFAULT_EMBEDDING_BATCH_MAX_CHARS,
        llm_connection: LLMConnectionConfig | None = None,
    ) -> None:
        self.embedder = embedder or LiteLLMEmbedder(llm_connection=llm_connection)
        self.embedding_batch_max_inputs = max(1, int(embedding_batch_max_inputs))
        self.embedding_batch_max_chars = max(1, int(embedding_batch_max_chars))

    def select(
        self,
        request: TriageSelectionRequest | None = None,
        **legacy_kwargs: Any,
    ) -> TriageOutput:
        resolved_request = _coerce_triage_selection_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        started = time.perf_counter()
        if resolved_request.limit <= 0 or not resolved_request.candidates:
            return _build_early_triage_output(
                candidates=resolved_request.candidates,
                duration_ms=int((time.perf_counter() - started) * 1000),
                method="noop",
                selected=[],
            )

        normalized_topics = _normalize_topics(resolved_request.topics)
        if not normalized_topics:
            return _build_early_triage_output(
                candidates=resolved_request.candidates,
                duration_ms=int((time.perf_counter() - started) * 1000),
                method="topics_empty_fallback",
                selected=[
                    TriageScoredCandidate(candidate=candidate, score=0.0)
                    for candidate in resolved_request.candidates[: resolved_request.limit]
                ],
            )
        scoring = self._score_candidates(
            context=_EmbeddingRunContext(
                run_id=resolved_request.run_id,
                candidates=resolved_request.candidates,
                topics=normalized_topics,
                query_mode=resolved_request.query_mode,
                embedding_model=resolved_request.embedding_model,
                embedding_dimensions=resolved_request.embedding_dimensions,
                include_debug=resolved_request.include_debug,
            )
        )

        selected, skipped_total = self._select_from_scored(
            scored=scoring.scored,
            config=_TriageSelectionConfig(
                run_id=resolved_request.run_id,
                limit=resolved_request.limit,
                mode=resolved_request.mode,
                min_similarity=resolved_request.min_similarity,
                exploration_rate=resolved_request.exploration_rate,
                recency_floor=resolved_request.recency_floor,
            ),
        )

        duration_ms = int((time.perf_counter() - started) * 1000)
        stats = _build_triage_stats(
            context=_TriageStatsContext(
                candidates_total=len(resolved_request.candidates),
                scored_total=len(scoring.scored),
                selected_total=len(selected),
                skipped_total=skipped_total,
                duration_ms=duration_ms,
                method=scoring.method,
                debug_totals=scoring.debug_totals,
            )
        )
        artifacts = _build_triage_artifacts(
            context=_TriageArtifactsContext(
                run_id=resolved_request.run_id,
                include_debug=resolved_request.include_debug,
                scoring=scoring,
                mode=resolved_request.mode,
                min_similarity=resolved_request.min_similarity,
                exploration_rate=resolved_request.exploration_rate,
                recency_floor=resolved_request.recency_floor,
                stats=stats,
                selected=selected,
            )
        )
        return TriageOutput(selected=selected, stats=stats, artifacts=artifacts)

    def _score_candidates(
        self,
        *,
        context: _EmbeddingRunContext,
    ) -> _TriageScoringResult:
        debug_totals = _EmbeddingDebugTotals()
        embedding_request = _build_embedding_request_artifact(
            context=context,
            max_inputs=self.embedding_batch_max_inputs,
            max_chars=self.embedding_batch_max_chars,
        )
        try:
            scored, embedding_response = self._score_candidates_with_embeddings(
                context=context,
                debug_totals=debug_totals,
            )
            return _TriageScoringResult(
                scored=scored,
                method="embedding_cosine",
                debug_totals=debug_totals,
                embedding_request=embedding_request,
                embedding_response=(
                    embedding_response if context.include_debug else None
                ),
            )
        except Exception as exc:  # noqa: BLE001
            debug_totals.record_error()
            return _TriageScoringResult(
                scored=self._score_with_rapidfuzz(
                    candidates=context.candidates,
                    topics=context.topics,
                ),
                method="fuzz_title",
                debug_totals=debug_totals,
                embedding_request=embedding_request,
                embedding_response=_build_embedding_error_artifact(
                    exc=exc,
                    embedding_response=None,
                )
                if context.include_debug
                else None,
            )

    def _score_candidates_with_embeddings(
        self,
        *,
        context: _EmbeddingRunContext,
        debug_totals: _EmbeddingDebugTotals,
    ) -> tuple[list[TriageScoredCandidate], dict[str, Any]]:
        query_vectors, query_debug = self._embed_query_vectors(
            context=context,
            debug_totals=debug_totals,
        )
        item_vectors, items_debug = self._embed_candidate_vectors(
            context=context,
            debug_totals=debug_totals,
        )
        return (
            self._score_with_vectors(
                candidates=context.candidates,
                query_vectors=query_vectors,
                item_vectors=item_vectors,
            ),
            {"query": query_debug, "items": items_debug},
        )

    def _embed_query_vectors(
        self,
        *,
        context: _EmbeddingRunContext,
        debug_totals: _EmbeddingDebugTotals,
    ) -> tuple[list[list[float]], dict[str, Any]]:
        debug_totals.record_call()
        query_vectors, query_debug = self._embed_query(
            topics=context.topics,
            query_mode=context.query_mode,
            model=context.embedding_model,
            dimensions=context.embedding_dimensions,
        )
        debug_totals.absorb_debug(query_debug)
        return query_vectors, query_debug

    def _embed_candidate_vectors(
        self,
        *,
        context: _EmbeddingRunContext,
        debug_totals: _EmbeddingDebugTotals,
    ) -> tuple[list[list[float]], dict[str, Any]]:
        item_texts = [candidate.text for candidate in context.candidates]
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
                items_batch_chars_max,
                sum(len(text) for text in batch),
            )
            batch_vectors, batch_debug = self._embed_candidate_batch(
                batch=batch,
                embedding_model=context.embedding_model,
                embedding_dimensions=context.embedding_dimensions,
                debug_totals=debug_totals,
            )
            item_vectors.extend(batch_vectors)
            if not items_sample_head and batch_vectors and batch_vectors[0]:
                items_sample_head = [float(value) for value in batch_vectors[0][:8]]
            if isinstance(batch_debug, dict):
                raw_elapsed_ms = batch_debug.get("elapsed_ms")
                if isinstance(raw_elapsed_ms, (int, float)):
                    items_elapsed_ms_total += int(raw_elapsed_ms)
                _merge_usage_totals(items_usage_totals, batch_debug.get("usage"))

        if len(item_vectors) != len(context.candidates):
            raise ValueError("embedding output size mismatch")
        return item_vectors, {
            "model": context.embedding_model,
            "inputs_total": len(item_texts),
            "dimensions": context.embedding_dimensions,
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

    def _embed_candidate_batch(
        self,
        *,
        batch: list[str],
        embedding_model: str,
        embedding_dimensions: int | None,
        debug_totals: _EmbeddingDebugTotals,
    ) -> tuple[list[list[float]], Any]:
        debug_totals.record_call()
        batch_vectors, batch_debug = self.embedder.embed(
            model=embedding_model,
            inputs=batch,
            dimensions=embedding_dimensions,
        )
        debug_totals.absorb_debug(batch_debug)
        if len(batch_vectors) != len(batch):
            raise ValueError("embedding output size mismatch")
        return batch_vectors, batch_debug

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
    def _selection_sort_key(entry: TriageScoredCandidate) -> tuple[float, float]:
        created_ts = 0.0
        created_at = getattr(entry.candidate.item, "created_at", None)
        if created_at is not None:
            created_ts = float(getattr(created_at, "timestamp")())
        return (entry.score, created_ts)

    @staticmethod
    def _normalize_selection_mode(mode: str) -> str:
        normalized_mode = str(mode or "").strip().lower()
        return normalized_mode if normalized_mode in {"prioritize", "filter"} else "prioritize"

    @classmethod
    def _recency_items(
        cls,
        *,
        scored: list[TriageScoredCandidate],
        config: _TriageSelectionConfig,
    ) -> tuple[list[TriageScoredCandidate], set[int]]:
        recency_n = max(0, min(int(config.recency_floor), config.limit, len(scored)))
        recency_items = scored[:recency_n]
        recency_ids = {
            item.candidate.item.id
            for item in recency_items
            if item.candidate.item.id is not None
        }
        return recency_items, recency_ids

    @classmethod
    def _eligible_entries(
        cls,
        *,
        scored: list[TriageScoredCandidate],
        normalized_mode: str,
        min_similarity: float,
    ) -> tuple[list[TriageScoredCandidate], int]:
        if normalized_mode != "filter":
            return scored, 0
        threshold = max(0.0, min(1.0, float(min_similarity)))
        eligible = [entry for entry in scored if entry.score >= threshold]
        skipped_total = sum(1 for entry in scored if entry.score < threshold)
        return eligible, skipped_total

    @classmethod
    def _sample_exploration_entries(
        cls,
        *,
        eligible_sorted: list[TriageScoredCandidate],
        selected_ids: set[int],
        remaining_slots: int,
        config: _TriageSelectionConfig,
    ) -> list[TriageScoredCandidate]:
        exploration_slots = max(
            0,
            min(
                remaining_slots,
                int(
                    math.floor(
                        config.limit * max(0.0, float(config.exploration_rate))
                    )
                ),
            ),
        )
        exploitation_slots = max(0, remaining_slots - exploration_slots)
        exploration_pool = [
            entry
            for entry in eligible_sorted[exploitation_slots:]
            if entry.candidate.item.id not in selected_ids
        ]
        if exploration_slots <= 0 or not exploration_pool:
            return []
        rng = random.Random(_stable_seed(config.run_id))
        return rng.sample(exploration_pool, k=min(exploration_slots, len(exploration_pool)))

    @staticmethod
    def _select_from_scored(
        *,
        scored: list[TriageScoredCandidate],
        config: _TriageSelectionConfig,
    ) -> tuple[list[TriageScoredCandidate], int]:
        if config.limit <= 0 or not scored:
            return [], 0

        normalized_mode = SemanticTriage._normalize_selection_mode(config.mode)
        recency_items, recency_ids = SemanticTriage._recency_items(
            scored=scored,
            config=config,
        )
        remaining = [
            entry for entry in scored if entry.candidate.item.id not in recency_ids
        ]
        eligible, skipped_total = SemanticTriage._eligible_entries(
            scored=remaining,
            normalized_mode=normalized_mode,
            min_similarity=config.min_similarity,
        )
        eligible_sorted = sorted(
            eligible,
            key=SemanticTriage._selection_sort_key,
            reverse=True,
        )

        remaining_slots = max(0, config.limit - len(recency_items))
        exploration_slots = max(
            0,
            min(
                remaining_slots,
                int(math.floor(config.limit * max(0.0, float(config.exploration_rate)))),
            ),
        )
        exploitation_slots = max(0, remaining_slots - exploration_slots)

        exploitation = eligible_sorted[:exploitation_slots]
        selected_ids = {
            entry.candidate.item.id
            for entry in recency_items + exploitation
            if entry.candidate.item.id is not None
        }
        exploration = SemanticTriage._sample_exploration_entries(
            eligible_sorted=eligible_sorted,
            selected_ids=selected_ids,
            remaining_slots=remaining_slots,
            config=config,
        )

        selected = recency_items + exploitation + exploration
        selected = sorted(
            selected,
            key=SemanticTriage._selection_sort_key,
            reverse=True,
        )
        return selected[: config.limit], skipped_total


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
    context: _TriageArtifactsContext,
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

    scored_sorted = sorted(context.scoring.scored, key=lambda e: e.score, reverse=True)
    return {
        "run_id_fingerprint": _fingerprint(context.run_id),
        "mode": context.mode,
        "method": context.scoring.method,
        "min_similarity": float(context.min_similarity),
        "exploration_rate": float(context.exploration_rate),
        "recency_floor": int(context.recency_floor),
        "stats": {
            "candidates_total": context.stats.candidates_total,
            "scored_total": context.stats.scored_total,
            "selected_total": context.stats.selected_total,
            "skipped_total": context.stats.skipped_total,
            "embedding_calls_total": context.stats.embedding_calls_total,
            "embedding_errors_total": context.stats.embedding_errors_total,
            "duration_ms": context.stats.duration_ms,
        },
        "selected_preview": preview(context.selected, limit=20),
        "top_scores_preview": preview(scored_sorted, limit=20),
    }


def _normalize_topics(topics: list[str]) -> list[str]:
    return [str(topic).strip() for topic in topics if str(topic).strip()]


def _build_early_triage_output(
    *,
    candidates: list[TriageCandidate],
    duration_ms: int,
    method: str,
    selected: list[TriageScoredCandidate],
) -> TriageOutput:
    return TriageOutput(
        selected=selected,
        stats=TriageStats(
            candidates_total=len(candidates),
            scored_total=0,
            selected_total=len(selected),
            skipped_total=0,
            embedding_calls_total=0,
            embedding_errors_total=0,
            duration_ms=duration_ms,
            method=method,
        ),
        artifacts={},
    )


def _build_embedding_request_artifact(
    *,
    context: _EmbeddingRunContext,
    max_inputs: int,
    max_chars: int,
) -> dict[str, Any] | None:
    if not context.include_debug:
        return None
    return {
        "run_id_fingerprint": _fingerprint(context.run_id),
        "model": context.embedding_model,
        "dimensions": context.embedding_dimensions,
        "query_mode": context.query_mode,
        "topics_total": len(context.topics),
        "candidates_total": len(context.candidates),
        "batching": {"max_inputs": max_inputs, "max_chars": max_chars},
    }


def _build_embedding_error_artifact(
    *,
    exc: BaseException,
    embedding_response: dict[str, Any] | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "error_type": type(exc).__name__,
        "error_message": str(exc),
    }
    if embedding_response is not None:
        payload["debug"] = embedding_response
    return payload


def _build_triage_stats(
    *,
    context: _TriageStatsContext,
) -> TriageStats:
    return TriageStats(
        candidates_total=context.candidates_total,
        scored_total=context.scored_total,
        selected_total=context.selected_total,
        skipped_total=context.skipped_total,
        embedding_calls_total=context.debug_totals.calls_total,
        embedding_errors_total=context.debug_totals.errors_total,
        duration_ms=context.duration_ms,
        method=context.method,
        embedding_prompt_tokens_total=_optional_prompt_tokens(context.debug_totals),
        embedding_cost_usd_total=_optional_cost_total(context.debug_totals),
        embedding_cost_missing_total=(
            context.debug_totals.cost_missing_total
            if context.debug_totals.calls_total > 0
            else 0
        ),
    )


def _optional_prompt_tokens(debug_totals: _EmbeddingDebugTotals) -> int | None:
    if debug_totals.calls_total <= 0:
        return 0
    if debug_totals.prompt_tokens_total > 0:
        return debug_totals.prompt_tokens_total
    return None


def _optional_cost_total(debug_totals: _EmbeddingDebugTotals) -> float | None:
    if debug_totals.calls_total <= 0:
        return 0.0
    if debug_totals.cost_usd_total > 0.0:
        return debug_totals.cost_usd_total
    return None


def _build_triage_artifacts(
    *,
    context: _TriageArtifactsContext,
) -> dict[str, dict[str, Any]]:
    if not context.include_debug:
        return {}
    artifacts: dict[str, dict[str, Any]] = {}
    if context.scoring.embedding_request is not None:
        artifacts["embedding_request"] = context.scoring.embedding_request
    if context.scoring.embedding_response is not None:
        artifacts["embedding_response"] = context.scoring.embedding_response
    artifacts["triage_summary"] = _build_triage_summary(context=context)
    return artifacts
