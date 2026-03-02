from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

import pytest
from sqlmodel import Session, select

from recoleta.models import (
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    Artifact,
    Content,
    Item,
    Metric,
)
from recoleta.pipeline import PipelineService
from recoleta.types import AnalysisResult, AnalyzeDebug, ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_analyze_failure_emits_failure_metric(configured_env) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(should_fail=True),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-1",
        canonical_url="https://example.com/failure-case",
        title="Failure Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-analyze-failure", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-analyze-failure", limit=10)

    metrics = repository.list_metrics(run_id="run-analyze-failure")
    failed_metric = [
        metric for metric in metrics if metric.name == "pipeline.analyze.failed_total"
    ]

    assert analyze_result.failed == 1
    assert len(failed_metric) == 1
    assert failed_metric[0].value == 1


def test_enrich_marks_retryable_failures_and_allows_retry_before_analyze(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import httpx
    import recoleta.pipeline as pipeline

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-retryable-enrich-1",
        canonical_url="https://example.com/retryable-enrich-case",
        title="Retryable Enrich Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-retryable-enrich", drafts=[draft])

    calls = 0

    def flaky_fetch_url_html(_client: httpx.Client, url: str) -> str:
        nonlocal calls
        calls += 1
        if calls == 1:
            request = httpx.Request("GET", url)
            response = httpx.Response(503, request=request, text="service unavailable")
            raise httpx.HTTPStatusError(
                "service unavailable", request=request, response=response
            )
        return "<html><body><p>mock html</p></body></html>"

    monkeypatch.setattr(pipeline, "fetch_url_html", flaky_fetch_url_html)

    service.enrich(run_id="run-retryable-enrich", limit=10)

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_RETRYABLE_FAILED

    service.enrich(run_id="run-retryable-enrich-2", limit=10)
    service.triage(run_id="run-retryable-enrich-2", limit=10)
    second = service.analyze(run_id="run-retryable-enrich-2", limit=10)
    assert second.processed == 1
    assert second.failed == 0

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_ANALYZED


def test_analyze_persists_enriched_content_and_emits_enrich_metrics(
    configured_env,
) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-enrich-1",
        canonical_url="https://example.com/enrich-case",
        title="Enrich Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-enrich", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-enrich", limit=10)

    assert analyze_result.processed == 1

    with Session(repository.engine) as session:
        content = session.exec(select(Content)).one()
        assert content.content_type == "html_maintext"
        assert content.text == "mock maintext"

    metrics = repository.list_metrics(run_id="run-enrich")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.enrich.processed_total"].value == 1
    assert by_name["pipeline.enrich.skipped_total"].value == 0
    assert by_name["pipeline.enrich.failed_total"].value == 0


def test_triage_skips_candidates_without_stored_content(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class KeywordEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            if self.calls == 1:
                return [[1.0, 0.0, 0.0]], {"kind": "query"}
            vectors: list[list[float]] = []
            for text in inputs:
                if "agents" in text.lower():
                    vectors.append([1.0, 0.0, 0.0])
                else:
                    vectors.append([0.0, 1.0, 0.0])
            return vectors, {"kind": "items"}

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        triage=SemanticTriage(embedder=KeywordEmbedder()),
        telegram_sender=FakeTelegramSender(),
    )
    service.ingest(
        run_id="run-triage-content-required",
        drafts=[
            ItemDraft.from_values(
                source="rss",
                source_item_id="triage-has-content",
                canonical_url="https://example.com/triage-has-content",
                title="Gardening Digest",
                authors=["Alice"],
                raw_metadata={"source": "test"},
            ),
            ItemDraft.from_values(
                source="rss",
                source_item_id="triage-no-content",
                canonical_url="https://example.com/triage-no-content",
                title="Agents Breakthrough",
                authors=["Bob"],
                raw_metadata={"source": "test"},
            ),
        ],
    )

    with Session(repository.engine) as session:
        items = list(session.exec(select(Item)))
    by_source_item_id = {item.source_item_id: item for item in items}
    has_content = by_source_item_id["triage-has-content"]
    assert has_content.id is not None

    repository.upsert_content(
        item_id=has_content.id,
        content_type="html_maintext",
        text="gardening details",
    )
    repository.mark_item_enriched(item_id=has_content.id)

    service.triage(run_id="run-triage-content-required", limit=1, candidate_limit=10)

    with Session(repository.engine) as session:
        refreshed = list(session.exec(select(Item)))
    refreshed_by_source_item_id = {item.source_item_id: item for item in refreshed}
    assert refreshed_by_source_item_id["triage-has-content"].state == ITEM_STATE_TRIAGED
    assert refreshed_by_source_item_id["triage-no-content"].state == ITEM_STATE_INGESTED


def test_triage_uses_latex_source_excerpt_for_arxiv_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "filter")
    monkeypatch.setenv("TRIAGE_MIN_SIMILARITY", "0.5")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class KeywordEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            if self.calls == 1:
                return [[1.0, 0.0, 0.0]], {"kind": "query"}
            vectors: list[list[float]] = []
            for text in inputs:
                if "agents" in text.lower():
                    vectors.append([1.0, 0.0, 0.0])
                else:
                    vectors.append([0.0, 1.0, 0.0])
            return vectors, {"kind": "items"}

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        triage=SemanticTriage(embedder=KeywordEmbedder()),
        telegram_sender=FakeTelegramSender(),
    )
    service.ingest(
        run_id="run-triage-latex-source",
        drafts=[
            ItemDraft.from_values(
                source="arxiv",
                source_item_id="1605.08386v1",
                canonical_url="https://arxiv.org/abs/1605.08386v1",
                title="Paper Without Keyword",
                authors=["Alice"],
                raw_metadata={"source": "test"},
            )
        ],
    )

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.id is not None
        item_id = item.id

    repository.upsert_content(
        item_id=item_id,
        content_type="latex_source",
        text="\\section{Intro}\nThis paper studies agents in production systems.",
    )
    repository.mark_item_enriched(item_id=item_id)

    service.triage(run_id="run-triage-latex-source", limit=1, candidate_limit=10)

    with Session(repository.engine) as session:
        refreshed = session.exec(select(Item)).one()
        assert refreshed.state == ITEM_STATE_TRIAGED


def test_triage_does_not_override_retryable_failed_state(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class ConstantEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            vectors = [[1.0, 0.0, 0.0] for _ in inputs]
            return vectors, {"kind": "test"}

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        triage=SemanticTriage(embedder=ConstantEmbedder()),
        telegram_sender=FakeTelegramSender(),
    )
    service.ingest(
        run_id="run-triage-preserve-retryable",
        drafts=[
            ItemDraft.from_values(
                source="rss",
                source_item_id="triage-enriched",
                canonical_url="https://example.com/triage-enriched",
                title="Enriched Candidate",
                authors=["Alice"],
                raw_metadata={"source": "test"},
            ),
            ItemDraft.from_values(
                source="rss",
                source_item_id="triage-retryable",
                canonical_url="https://example.com/triage-retryable",
                title="Retryable Candidate",
                authors=["Bob"],
                raw_metadata={"source": "test"},
            ),
        ],
    )

    with Session(repository.engine) as session:
        items = list(session.exec(select(Item)))
    by_source_item_id = {item.source_item_id: item for item in items}
    enriched = by_source_item_id["triage-enriched"]
    retryable = by_source_item_id["triage-retryable"]
    assert enriched.id is not None
    assert retryable.id is not None

    repository.upsert_content(
        item_id=enriched.id, content_type="html_maintext", text="enriched details"
    )
    repository.mark_item_enriched(item_id=enriched.id)

    repository.upsert_content(
        item_id=retryable.id, content_type="html_maintext", text="retryable details"
    )
    repository.mark_item_enriched(item_id=retryable.id)
    repository.mark_item_retryable_failed(item_id=retryable.id)

    service.triage(run_id="run-triage-preserve-retryable", limit=1, candidate_limit=10)

    with Session(repository.engine) as session:
        refreshed = list(session.exec(select(Item)))
    refreshed_by_source_item_id = {item.source_item_id: item for item in refreshed}
    assert refreshed_by_source_item_id["triage-enriched"].state == ITEM_STATE_TRIAGED
    assert (
        refreshed_by_source_item_id["triage-retryable"].state
        == ITEM_STATE_RETRYABLE_FAILED
    )


def test_repository_analysis_selection_prioritizes_recently_updated_retryables(
    configured_env,
) -> None:
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    service.ingest(
        run_id="run-selection-order",
        drafts=[
            ItemDraft.from_values(
                source="rss",
                source_item_id="order-older",
                canonical_url="https://example.com/order-older",
                title="Older by Created At",
                authors=["Alice"],
                raw_metadata={"source": "test"},
            ),
            ItemDraft.from_values(
                source="rss",
                source_item_id="order-newer",
                canonical_url="https://example.com/order-newer",
                title="Newer by Created At",
                authors=["Bob"],
                raw_metadata={"source": "test"},
            ),
        ],
    )

    with Session(repository.engine) as session:
        items = list(session.exec(select(Item)))
        by_source_item_id = {item.source_item_id: item for item in items}
        older = by_source_item_id["order-older"]
        newer = by_source_item_id["order-newer"]
        older.state = ITEM_STATE_RETRYABLE_FAILED
        newer.state = ITEM_STATE_RETRYABLE_FAILED
        older.created_at = datetime(2024, 1, 1, tzinfo=UTC)
        older.updated_at = datetime(2024, 1, 3, tzinfo=UTC)
        newer.created_at = datetime(2024, 1, 2, tzinfo=UTC)
        newer.updated_at = datetime(2024, 1, 2, tzinfo=UTC)
        session.add(older)
        session.add(newer)
        session.commit()

    selection = repository.list_items_for_analysis(limit=1)
    llm_selection = repository.list_items_for_llm_analysis(
        limit=1, triage_required=False
    )
    assert selection[0].source_item_id == "order-older"
    assert llm_selection[0].source_item_id == "order-older"


def test_analyze_with_semantic_triage_prioritizes_high_similarity_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.titles: list[str] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,  # noqa: ARG002
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.titles.append(title)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="Matters because it matches user topics.",
                    idea_directions=["Try it."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    class KeywordEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            if self.calls == 1:
                return [[1.0, 0.0, 0.0]], {"kind": "query"}
            vectors: list[list[float]] = []
            for text in inputs:
                if "agents" in text.lower():
                    vectors.append([1.0, 0.0, 0.0])
                else:
                    vectors.append([0.0, 1.0, 0.0])
            return vectors, {"kind": "items"}

    analyzer = CapturingAnalyzer()
    triage = SemanticTriage(embedder=KeywordEmbedder())
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        triage=triage,
        telegram_sender=FakeTelegramSender(),
    )

    draft_relevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-relevant",
        canonical_url="https://example.com/triage-relevant",
        title="Agents for Good",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    draft_irrelevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-irrelevant",
        canonical_url="https://example.com/triage-irrelevant",
        title="Gardening Tips",
        authors=["Bob"],
        raw_metadata={"source": "test"},
    )

    run_id = "run-triage"
    service.prepare(run_id=run_id, drafts=[draft_relevant, draft_irrelevant], limit=1)
    result = service.analyze(run_id=run_id, limit=1)
    assert result.processed == 1
    assert analyzer.titles == ["Agents for Good"]

    with Session(repository.engine) as session:
        items = list(session.exec(select(Item).order_by(cast(Any, Item.id))))
        assert len(items) == 2
        by_title = {item.title: item for item in items}
        assert by_title["Agents for Good"].state == ITEM_STATE_ANALYZED
        assert by_title["Gardening Tips"].state == ITEM_STATE_ENRICHED

    metrics = repository.list_metrics(run_id=run_id)
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.triage.candidates_total"].value == 2
    assert by_name["pipeline.triage.selected_total"].value == 1


def test_analyze_triage_embedding_failure_emits_metric_and_falls_back(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class ExplodingEmbedder:
        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            raise RuntimeError("boom")

    analyzer = FakeAnalyzer()
    triage = SemanticTriage(embedder=ExplodingEmbedder())
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        triage=triage,
        telegram_sender=FakeTelegramSender(),
    )

    draft_relevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-fallback-relevant",
        canonical_url="https://example.com/triage-fallback-relevant",
        title="Agents are great",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    draft_irrelevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-fallback-irrelevant",
        canonical_url="https://example.com/triage-fallback-irrelevant",
        title="Cooking recipes",
        authors=["Bob"],
        raw_metadata={"source": "test"},
    )

    run_id = "run-triage-fallback"
    service.prepare(run_id=run_id, drafts=[draft_relevant, draft_irrelevant], limit=1)
    result = service.analyze(run_id=run_id, limit=1)
    assert result.processed == 1

    metrics = repository.list_metrics(run_id=run_id)
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.triage.embedding_errors_total"].value == 1
    assert by_name["pipeline.triage.failed_total"].value == 0


def test_analyze_triage_content_fetch_failure_emits_metric_and_still_runs(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class KeywordEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            if self.calls == 1:
                return [[1.0, 0.0, 0.0]], {"kind": "query"}
            vectors: list[list[float]] = []
            for text in inputs:
                if "agents" in text.lower():
                    vectors.append([1.0, 0.0, 0.0])
                else:
                    vectors.append([0.0, 1.0, 0.0])
            return vectors, {"kind": "items"}

    def explode_latest_contents(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("boom")

    monkeypatch.setattr(repository, "get_latest_contents", explode_latest_contents)

    triage = SemanticTriage(embedder=KeywordEmbedder())
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        triage=triage,
        telegram_sender=FakeTelegramSender(),
    )

    draft_relevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-content-fetch-relevant",
        canonical_url="https://example.com/triage-content-fetch-relevant",
        title="Agents for Good",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    draft_irrelevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-content-fetch-irrelevant",
        canonical_url="https://example.com/triage-content-fetch-irrelevant",
        title="Gardening Tips",
        authors=["Bob"],
        raw_metadata={"source": "test"},
    )

    run_id = "run-triage-content-fetch"
    service.prepare(run_id=run_id, drafts=[draft_relevant, draft_irrelevant], limit=1)
    result = service.analyze(run_id=run_id, limit=1)
    assert result.processed == 1

    metrics = repository.list_metrics(run_id=run_id)
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.triage.content_fetch_failed_total"].value == 1


def test_analyze_triage_dimension_mismatch_falls_back_to_rapidfuzz(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.triage import SemanticTriage

    monkeypatch.setenv("TRIAGE_ENABLED", "true")
    monkeypatch.setenv("TRIAGE_MODE", "prioritize")
    monkeypatch.setenv("TRIAGE_RECENCY_FLOOR", "0")
    monkeypatch.setenv("TRIAGE_EXPLORATION_RATE", "0")

    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.titles: list[str] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,  # noqa: ARG002
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.titles.append(title)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="Matters because it matches user topics.",
                    idea_directions=["Try it."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    class MismatchedDimsEmbedder:
        def __init__(self) -> None:
            self.calls = 0

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            if self.calls == 1:
                return [[1.0, 0.0, 0.0]], {"kind": "query"}
            return [[1.0, 0.0] for _ in inputs], {"kind": "items"}

    analyzer = CapturingAnalyzer()
    triage = SemanticTriage(embedder=MismatchedDimsEmbedder())
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        triage=triage,
        telegram_sender=FakeTelegramSender(),
    )

    draft_relevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-dim-mismatch-relevant",
        canonical_url="https://example.com/triage-dim-mismatch-relevant",
        title="Agents for Good",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    draft_irrelevant = ItemDraft.from_values(
        source="rss",
        source_item_id="triage-dim-mismatch-irrelevant",
        canonical_url="https://example.com/triage-dim-mismatch-irrelevant",
        title="Gardening Tips",
        authors=["Bob"],
        raw_metadata={"source": "test"},
    )

    run_id = "run-triage-dim-mismatch"
    service.prepare(run_id=run_id, drafts=[draft_relevant, draft_irrelevant], limit=1)
    result = service.analyze(run_id=run_id, limit=1)
    assert result.processed == 1
    assert analyzer.titles == ["Agents for Good"]

    metrics = repository.list_metrics(run_id=run_id)
    by_name = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.triage.embedding_errors_total"].value == 1
    assert by_name["pipeline.triage.failed_total"].value == 0


def test_semantic_triage_batches_item_embeddings_for_large_candidate_pool() -> None:
    from recoleta.triage import SemanticTriage, TriageCandidate
    from recoleta.types import sha256_hex

    class CountingEmbedder:
        def __init__(self) -> None:
            self.calls = 0
            self.batch_sizes: list[int] = []

        def embed(
            self, *, model: str, inputs: list[str], dimensions: int | None = None
        ):  # type: ignore[no-untyped-def]
            assert model
            assert dimensions is None or dimensions > 0
            self.calls += 1
            self.batch_sizes.append(len(inputs))
            vectors = [[1.0, 0.0, 0.0] for _ in inputs]
            return vectors, {}

    embedder = CountingEmbedder()
    triage = SemanticTriage(embedder=embedder)

    candidates: list[TriageCandidate] = []
    for i in range(200):
        url = f"https://example.com/triage-batch-{i}"
        item = Item(
            id=i + 1,
            source="rss",
            source_item_id=f"triage-batch-{i}",
            canonical_url=url,
            canonical_url_hash=sha256_hex(url),
            title=f"Item {i}",
        )
        candidates.append(TriageCandidate(item=item, text="Agents\n\n" + ("x" * 1200)))

    output = triage.select(
        run_id="run-triage-batch",
        candidates=candidates,
        topics=["agents"],
        limit=10,
        mode="prioritize",
        query_mode="joined",
        embedding_model="test/embedding-model",
        embedding_dimensions=None,
        min_similarity=0.0,
        exploration_rate=0.0,
        recency_floor=0,
        include_debug=False,
    )

    assert output.stats.method == "embedding_cosine"
    assert output.stats.embedding_errors_total == 0
    assert output.stats.candidates_total == 200
    assert output.stats.scored_total == 200
    assert output.stats.selected_total == 10
    assert output.stats.embedding_calls_total == embedder.calls
    assert embedder.calls >= 3
    assert embedder.batch_sizes[0] == 1
    assert max(embedder.batch_sizes[1:]) < len(candidates)


def test_analyze_prefers_pdf_enrichment_for_arxiv_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.pipeline as pipeline

    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.contents: list[str | None] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.contents.append(content)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="This matters because it aligns with user interests.",
                    idea_directions=["Try reproducing the approach."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    analyzer = CapturingAnalyzer()

    expected_pdf_url = "https://arxiv.org/pdf/1605.08386v1.pdf"

    def fake_fetch_url_bytes(_client, url: str) -> bytes:  # noqa: ARG001
        assert url == expected_pdf_url
        return b"%PDF-mock"

    def fail_fetch_url_html(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("html fetch should not be used")

    monkeypatch.setattr(pipeline, "fetch_url_bytes", fake_fetch_url_bytes)
    monkeypatch.setattr(
        pipeline,
        "extract_pdf_text",
        lambda _bytes, **_: "mock pdf text",  # noqa: ARG005
    )
    monkeypatch.setattr(pipeline, "fetch_url_html", fail_fetch_url_html)

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1605.08386v1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv PDF Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-pdf-enrich", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-pdf-enrich", limit=10)
    assert analyze_result.processed == 1

    assert analyzer.contents == ["mock pdf text"]

    with Session(repository.engine) as session:
        contents = list(session.exec(select(Content).order_by(cast(Any, Content.id))))
        assert contents
        assert any(
            content.content_type == "pdf_text" and content.text == "mock pdf text"
            for content in contents
        )


def test_analyze_uses_latex_source_enrichment_for_arxiv_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.pipeline as pipeline

    monkeypatch.setenv(
        "SOURCES",
        '{"arxiv":{"enabled":true,"queries":["cat:cs.AI"],"enrich_method":"latex_source","enrich_failure_mode":"strict"}}',
    )
    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.contents: list[str | None] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.contents.append(content)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="This matters because it aligns with user interests.",
                    idea_directions=["Try reproducing the approach."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    analyzer = CapturingAnalyzer()

    expected_source_url = "https://arxiv.org/e-print/1605.08386v1"

    def fake_fetch_url_bytes(_client, url: str) -> bytes:  # noqa: ARG001
        assert url == expected_source_url
        return b"mock source archive"

    def fail_fetch_url_html(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("html fetch should not be used")

    monkeypatch.setattr(pipeline, "fetch_url_bytes", fake_fetch_url_bytes)
    monkeypatch.setattr(
        pipeline,
        "extract_arxiv_latex_source",
        lambda _bytes: "\\section{Intro}\nAgents are useful.",  # noqa: ARG005
    )
    monkeypatch.setattr(pipeline, "fetch_url_html", fail_fetch_url_html)

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1605.08386v1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv LaTeX Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-latex-enrich", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-latex-enrich", limit=10)
    assert analyze_result.processed == 1

    assert analyzer.contents == ["\\section{Intro}\nAgents are useful."]

    with Session(repository.engine) as session:
        contents = list(session.exec(select(Content).order_by(cast(Any, Content.id))))
        assert contents
        assert any(
            content.content_type == "latex_source"
            and content.text == "\\section{Intro}\nAgents are useful."
            for content in contents
        )


def test_analyze_uses_html_document_enrichment_for_arxiv_items(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.pipeline as pipeline

    monkeypatch.setenv(
        "SOURCES",
        '{"arxiv":{"enabled":true,"queries":["cat:cs.AI"],"enrich_method":"html_document","enrich_failure_mode":"strict"}}',
    )
    settings, repository = _build_runtime()

    class CapturingAnalyzer:
        def __init__(self) -> None:
            self.contents: list[str | None] = []

        def analyze(
            self,
            *,
            title: str,
            canonical_url: str,  # noqa: ARG002
            user_topics: list[str],
            content: str | None = None,
            include_debug: bool = False,  # noqa: ARG002
        ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
            self.contents.append(content)
            return (
                AnalysisResult(
                    model="test/fake-model",
                    provider="test",
                    summary=f"Summary for {title}",
                    insight="This matters because it aligns with user interests.",
                    idea_directions=["Try reproducing the approach."],
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.9,
                    novelty_score=0.4,
                    cost_usd=0.0,
                    latency_ms=1,
                ),
                None,
            )

    analyzer = CapturingAnalyzer()

    expected_html_url = "https://arxiv.org/html/1605.08386v1"

    def fake_fetch_url_html(_client, url: str) -> str:  # noqa: ARG001
        assert url == expected_html_url
        return "<html><body><main><p>raw html body</p></main></body></html>"

    def fail_fetch_url_bytes(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("binary fetch should not be used")

    monkeypatch.setattr(pipeline, "fetch_url_html", fake_fetch_url_html)
    monkeypatch.setattr(pipeline, "fetch_url_bytes", fail_fetch_url_bytes)
    monkeypatch.setattr(
        pipeline,
        "extract_html_document_cleaned_with_references",
        lambda _html, **_: ("<main><p>clean html body</p></main>", None, {}),  # noqa: ARG005
    )
    monkeypatch.setattr(
        pipeline, "extract_html_maintext", lambda _html: "clean text body"
    )  # noqa: ARG005
    monkeypatch.setattr(
        pipeline,
        "convert_html_document_to_markdown",
        lambda _html, **_: ("clean html body", 3, None),  # noqa: ARG005
    )

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=analyzer,
        telegram_sender=FakeTelegramSender(),
    )
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1605.08386v1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv HTML Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-html-document-enrich", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-html-document-enrich", limit=10)
    assert analyze_result.processed == 1

    assert analyzer.contents == ["clean html body"]

    with Session(repository.engine) as session:
        contents = list(session.exec(select(Content).order_by(cast(Any, Content.id))))
        assert any(
            content.content_type == "html_document"
            and content.text == "<main><p>clean html body</p></main>"
            for content in contents
        )
        assert any(
            content.content_type == "html_maintext"
            and content.text == "clean text body"
            for content in contents
        )


def test_arxiv_strict_enrich_does_not_fallback_when_method_fails(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import httpx
    import recoleta.pipeline as pipeline

    monkeypatch.setenv(
        "SOURCES",
        '{"arxiv":{"enabled":true,"queries":["cat:cs.AI"],"enrich_method":"html_document","enrich_failure_mode":"strict"}}',
    )
    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    draft = ItemDraft.from_values(
        source="arxiv",
        source_item_id="1605.08386v1",
        canonical_url="https://arxiv.org/abs/1605.08386v1",
        title="Arxiv Strict Failure",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.ingest(run_id="run-arxiv-strict-failure", drafts=[draft])

    def fail_fetch_url_html(_client, url: str) -> str:  # noqa: ARG001
        request = httpx.Request("GET", url)
        response = httpx.Response(503, request=request, text="service unavailable")
        raise httpx.HTTPStatusError(
            "service unavailable", request=request, response=response
        )

    def fail_if_binary_fetch_used(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise AssertionError("strict mode must not fallback to binary/pdf fetch")

    monkeypatch.setattr(pipeline, "fetch_url_html", fail_fetch_url_html)
    monkeypatch.setattr(pipeline, "fetch_url_bytes", fail_if_binary_fetch_used)

    service.enrich(run_id="run-arxiv-strict-failure", limit=10)

    with Session(repository.engine) as session:
        item = session.exec(select(Item)).one()
        assert item.state == ITEM_STATE_RETRYABLE_FAILED

    metrics = repository.list_metrics(run_id="run-arxiv-strict-failure")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.enrich.failed_total"].value == 1
    assert by_name["pipeline.enrich.arxiv.method_failed.html_document_total"].value == 1


def test_analyze_writes_llm_request_and_response_artifacts(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tmp_path = configured_env
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-llm-artifacts-1",
        canonical_url="https://example.com/llm-artifacts-case",
        title="LLM Artifacts Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-llm-artifacts", drafts=[draft], limit=10)
    analyze_result = service.analyze(run_id="run-llm-artifacts", limit=10)
    assert analyze_result.processed == 1

    with Session(repository.engine) as session:
        artifacts = list(
            session.exec(
                select(Artifact)
                .where(Artifact.run_id == "run-llm-artifacts")
                .order_by(cast(Any, Artifact.id))
            )
        )
        kinds = {artifact.kind for artifact in artifacts}
        assert {"llm_request", "llm_response"}.issubset(kinds)
        for artifact in artifacts:
            assert not Path(artifact.path).is_absolute()
            assert (artifacts_dir / artifact.path).exists()


def test_analyze_sanitizes_debug_artifact_paths(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tmp_path = configured_env
    artifacts_dir = tmp_path / "artifacts"

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(artifacts_dir))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-llm-artifacts-2",
        canonical_url="https://example.com/llm-artifacts-case-2",
        title="LLM Artifacts Case 2",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-llm-artifacts-2", drafts=[draft], limit=10)

    malicious_run_id = "../run-llm-artifacts-2"
    analyze_result = service.analyze(run_id=malicious_run_id, limit=10)
    assert analyze_result.processed == 1

    base_dir = artifacts_dir.resolve()
    with Session(repository.engine) as session:
        artifacts = list(
            session.exec(
                select(Artifact)
                .where(Artifact.run_id == malicious_run_id)
                .order_by(cast(Any, Artifact.id))
            )
        )
        assert artifacts
        for artifact in artifacts:
            artifact_rel = Path(artifact.path)
            assert ".." not in artifact_rel.parts
            assert not artifact_rel.is_absolute()
            artifact_abs = (artifacts_dir / artifact_rel).resolve()
            assert artifact_abs.is_relative_to(base_dir)
            assert artifact_abs.exists()


def test_pipeline_records_duration_metrics_for_each_stage(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-durations-1",
        canonical_url="https://example.com/durations-case",
        title="Durations Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-durations", drafts=[draft], limit=10)
    service.analyze(run_id="run-durations", limit=10)
    service.publish(run_id="run-durations", limit=10)

    metrics = repository.list_metrics(run_id="run-durations")
    metric_names = {metric.name for metric in metrics}
    assert "pipeline.ingest.duration_ms" in metric_names
    assert "pipeline.enrich.item_duration_ms_total" in metric_names
    assert "pipeline.enrich.duration_ms" in metric_names
    assert "pipeline.analyze.duration_ms" in metric_names
    assert "pipeline.publish.duration_ms" in metric_names
