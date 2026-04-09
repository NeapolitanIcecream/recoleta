from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
import re

import pytest

from recoleta.pipeline import PipelineService
from recoleta.publish import write_obsidian_trend_note
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_write_obsidian_trend_note_renders_clusters_and_evidence_blocks(
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    note_path = write_obsidian_trend_note(
        vault_path=vault_path,
        base_folder="Recoleta",
        trend_doc_id=17,
        title="T",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-1",
        overview_md="Overview",
        topics=["vla", "robotics"],
        clusters=[
            {
                "title": "Cluster A",
                "content_md": "Para 1.\n\nPara 2.",
                "evidence_refs": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "Robometer: Scaling ...",
                        "url": "http://arxiv.org/abs/2603.02115v1",
                    }
                ],
            }
        ],
    )

    text = note_path.read_text(encoding="utf-8")
    assert "## Clusters" in text
    assert "### Cluster A" in text
    assert "#### Evidence" in text
    assert "- [Robometer: Scaling ...](http://arxiv.org/abs/2603.02115v1)" in text
    assert "Representative sources" not in text
    assert "## Highlights" not in text


def test_trends_day_rewrites_doc_id_refs_and_enriches_evidence_links(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-regression-1",
        canonical_url="https://example.com/robometer",
        title="Robometer: Scaling General-Purpose Robotic Reward Models via Trajectory Comparisons",
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-regression", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-regression", limit=10)

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
            limit=1,
        )
        assert docs and docs[0].id is not None
        doc_id = int(docs[0].id)
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": f"See doc_id: {doc_id}, chunk: 0.",
            "topics": ["vla"],
            "clusters": [
                {
                    "title": "Grounding",
                    "content_md": f"Ref doc_id:{doc_id}",
                    "evidence_refs": [
                        {
                            "doc_id": doc_id,
                            "chunk_index": 0,
                            "reason": f"Hit doc_id: {doc_id}",
                        }
                    ],
                }
            ],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-regression",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )
    matches = list((settings.markdown_output_dir / "Trends").glob("day--2026-03-02--trend--*.md"))
    assert len(matches) == 1

    md = matches[0].read_text(encoding="utf-8")
    assert re.search(r"(?<![\w])doc_id\s*[:=#-]?", md) is None
    assert re.search(r"\bchunk(?:_index)?\b", md, flags=re.I) is None
    assert "../Inbox/" in md
    assert "https://example.com/robometer" not in md
    assert "[Robometer](" in md
    assert "#### Evidence" in md
    assert result.doc_id > 0


def test_trends_day_deduplicates_evidence_from_same_doc_across_chunks(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-regression-2",
        canonical_url="https://example.com/deduped-paper",
        title="Representative Paper Should Appear Once",
        authors=["Alice"],
        published_at=datetime(2026, 3, 9, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-regression-2", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-regression-2", limit=10)

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
            limit=1,
        )
        assert docs and docs[0].id is not None
        doc_id = int(docs[0].id)
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": "- ok",
            "topics": ["agents"],
            "clusters": [
                {
                    "title": "Evidence consolidation",
                    "content_md": "Repeated evidence refs should collapse to one reader-facing citation.",
                    "evidence_refs": [
                        {"doc_id": doc_id, "chunk_index": 1, "reason": "First match."},
                        {"doc_id": doc_id, "chunk_index": 2, "reason": "Second match."},
                    ],
                }
            ],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-regression-2",
        granularity="day",
        anchor_date=date(2026, 3, 9),
        llm_model="test/fake-model",
    )
    matches = list((settings.markdown_output_dir / "Trends").glob("day--2026-03-09--trend--*.md"))
    assert len(matches) == 1

    md = matches[0].read_text(encoding="utf-8")
    assert "../Inbox/" in md
    assert "https://example.com/deduped-paper" not in md
    assert md.count("[Representative Paper Should Appear Once](") == 1
    assert result.doc_id > 0
