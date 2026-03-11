from __future__ import annotations

import json
import re
import socket
from datetime import date, timedelta
from pathlib import Path

import pytest

from recoleta.pipeline import PipelineService
from recoleta.trends import (
    TrendPayload,
    day_period_bounds,
    index_items_as_documents,
    persist_trend_payload,
    week_period_bounds,
)
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_trends_week_published_markdown_locks_quality_signals(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: weekly trend notes should include must-read + reps + hide raw doc_id refs."""

    # Guard against accidental network calls in this regression test.
    def _no_network(*_args, **_kwargs):  # type: ignore[no-untyped-def]
        raise RuntimeError("network disabled")

    monkeypatch.setattr(
        socket,
        "create_connection",
        _no_network,
    )
    monkeypatch.setattr(socket.socket, "connect", _no_network, raising=True)
    monkeypatch.setattr(socket.socket, "connect_ex", _no_network, raising=True)

    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("TOPICS", json.dumps(["agents"]))
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    anchor = date(2026, 3, 5)
    week_start, week_end = week_period_bounds(anchor)

    # Ensure weekly corpus isn't empty (weekly trends read daily trend docs by default).
    day_start, day_end = day_period_bounds(week_start.date())
    _ = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=day_start,
        period_end=day_end,
        payload=TrendPayload(
            title="Daily Trend",
            granularity="day",
            period_start=day_start.isoformat(),
            period_end=day_end.isoformat(),
            overview_md="- daily",
            topics=["agents"],
            clusters=[],
            highlights=[],
        ),
    )

    # Create multiple analyzed items in the weekly window and index them as item documents.
    titles = [
        "Robometer: Scaling reward models via trajectory comparisons",
        "Diffusion Policy: A unified view of planning and control",
        "VLA Agents: Tool-using robots in the wild",
        "RAG Systems: Retrieval and grounding for long-context LLMs",
    ]
    for idx, paper_title in enumerate(titles, start=1):
        paper_url = f"https://example.com/paper-{idx}"
        published_at = week_start + timedelta(days=idx)
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=f"paper-{idx}",
            canonical_url=paper_url,
            title=paper_title,
            authors=["Alice", "Bob"],
            published_at=published_at,
            raw_metadata={"source": "test"},
        )
        item, _ = repository.upsert_item(draft)
        assert item.id is not None
        analysis, _ = service.analyzer.analyze(
            title=paper_title,
            canonical_url=paper_url,
            user_topics=["agents"],
            include_debug=False,
        )
        _ = repository.save_analysis(item_id=int(item.id), result=analysis)

    _ = index_items_as_documents(
        repository=repository,
        run_id="run-week-quality-regression",
        period_start=week_start,
        period_end=week_end,
    )

    from recoleta.rag import agent as rag_agent

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        repo = kwargs["repository"]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        docs = repo.list_documents(
            doc_type="item",
            period_start=pstart,
            period_end=pend,
            granularity=None,
            order_by="event_desc",
            offset=0,
            limit=10,
        )
        assert docs and len(docs) >= 3
        doc_ids = [int(getattr(d, "id")) for d in docs[:3]]
        payload = {
            "title": f"Weekly Trend doc_id={doc_ids[0]}, chunk: 0",
            "granularity": "week",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": f"See doc_id: {doc_ids[0]}, chunk: 0.",
            "topics": ["agents"],
            "clusters": [
                {
                    "name": f"Top-10 must-read doc_id={doc_ids[1]}, chunk_index: 0",
                    "description": f"Curated from doc_id={doc_ids[1]}, chunk_index: 0.",
                    "representative_doc_ids": [],
                    "representative_chunks": [
                        {"doc_id": doc_id, "chunk_index": 0} for doc_id in doc_ids
                    ],
                }
            ],
            "highlights": [f"Must read doc_id: {doc_ids[2]}"],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-week-quality-regression",
        granularity="week",
        anchor_date=anchor,
        llm_model="test/fake-model",
    )

    trends_dir = (settings.markdown_output_dir / "Trends").resolve()
    matches = sorted(trends_dir.glob(f"week--*--trend--{result.doc_id}.md"))
    assert len(matches) == 1
    note_path = matches[0]
    md = note_path.read_text(encoding="utf-8")

    # Ensure internal doc references do not leak into published notes.
    assert re.search(r"\bdoc_id\b", md) is None
    assert re.search(r"\bdoc\b\s*[:=#-]?\s*\d+\b", md, flags=re.I) is None
    assert re.search(r"\bchunk(?:_index)?\s*[:=]\s*\d+\b", md, flags=re.I) is None
    assert re.search(r"\b\d+\s*[,;，；]?\s*chunk(?:_index)?\b", md, flags=re.I) is None
    assert (
        re.search(r"^#{2,6}\s+Top-\d+\s+must-?read\b", md, flags=re.M | re.I)
        is not None
    )
    title_match = re.search(r"^#\s+(.+)$", md, flags=re.M)
    assert title_match is not None
    title_line = title_match.group(1)
    assert "Weekly Trend" not in title_line
    assert "doc_id" not in title_line
    assert "chunk" not in title_line
    assert "[" not in title_line
    assert "]" not in title_line
    assert re.search(r"^#{2,6}\s+Representative\b", md, flags=re.M | re.I) is not None
    link_total = len(re.findall(r"\[[^\]]+\]\(https?://", md)) + len(
        re.findall(r"<https?://", md)
    )
    assert link_total >= 3
