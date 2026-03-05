from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path

import pytest
import re

from recoleta.pipeline import PipelineService
from recoleta.publish import write_obsidian_trend_note
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def test_write_obsidian_trend_note_renders_clusters_as_headings_and_papers(
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    base_folder = "Recoleta"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    note_path = write_obsidian_trend_note(
        vault_path=vault_path,
        base_folder=base_folder,
        trend_doc_id=17,
        title="T",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        run_id="run-1",
        overview_md="Overview",
        topics=["VLA", "robotics"],
        clusters=[
            {
                "name": "Cluster A",
                "description": "Para 1.\n\nPara 2.",
                "representative_chunks": [
                    {
                        "doc_id": 1,
                        "chunk_index": 0,
                        "title": "Robometer: Scaling ...",
                        "url": "http://arxiv.org/abs/2603.02115v1",
                        "authors": ["A", "B", "C", "D", "E", "F", "G"],
                    }
                ],
            }
        ],
        highlights=["H1", "H2", "H3", "H4"],
    )

    expected = (
        vault_path / base_folder / "Trends" / "day--2026-03-02--trend--17.md"
    ).resolve()
    assert note_path.resolve() == expected
    text = note_path.read_text(encoding="utf-8")
    assert "> [!summary] TL;DR" in text
    assert "aliases:" in text
    assert "tags:" in text
    assert "## Clusters" in text
    assert "### Cluster A" in text
    assert "#### Representative papers" in text
    assert "- [Robometer: Scaling ...](http://arxiv.org/abs/2603.02115v1)" in text
    assert " — A; B; C; D; E; F; …" in text
    assert "doc_id=" not in text


def test_trends_day_rewrites_doc_id_refs_and_enriches_representatives(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Spec: published trend notes should not expose raw doc_id references."""

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

    published_at = datetime(2026, 3, 2, 1, 0, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-regression-1",
        canonical_url="https://example.com/robometer",
        title="Robometer: Scaling General-Purpose Robotic Reward Models via Trajectory Comparisons",
        authors=["Alice"],
        published_at=published_at,
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
                    "name": "C",
                    "description": f"Ref doc_id:{doc_id}",
                    "representative_doc_ids": [],
                    "representative_chunks": [{"doc_id": doc_id, "chunk_index": 0}],
                }
            ],
            "highlights": [f"Hit doc_id: {doc_id}"],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-regression",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
    )
    trends_dir = (settings.markdown_output_dir / "Trends").resolve()
    matches = list(trends_dir.glob("day--2026-03-02--trend--*.md"))
    assert len(matches) == 1

    md = matches[0].read_text(encoding="utf-8")
    assert re.search(r"(?<![\\w])doc_id\\s*:", md) is None
    assert "[Robometer](" in md
    assert "Robometer: Scaling General-Purpose Robotic Reward Models" in md
    assert "— Alice" in md
    assert result.doc_id > 0
