from __future__ import annotations

from datetime import UTC, date, datetime
import json
from pathlib import Path
import re

import pytest
from sqlmodel import Session, select

from recoleta.models import Document, DocumentChunk, Metric, PassOutput
from recoleta.pipeline import PipelineService
from recoleta.types import ItemDraft
from tests.spec_support import FakeAnalyzer, FakeTelegramSender, _build_runtime


def _metric_values(*, repository, run_id: str) -> dict[str, float]:
    return {
        str(getattr(metric, "name", "")): float(getattr(metric, "value", 0.0))
        for metric in repository.list_metrics(run_id=run_id)
    }


def _seed_item_document(
    *,
    repository,
    published_at: datetime,
    source_item_id: str,
    title: str,
) -> int:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id=source_item_id,
        canonical_url=f"https://example.com/{source_item_id}",
        title=title,
        authors=["Alice"],
        published_at=published_at,
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    doc = repository.upsert_document_for_item(item=item)
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value=f"Summary for {title}.",
        source_content_type="analysis_summary",
    )
    return int(doc.id)


def test_trends_persist_canonical_pass_output_before_projection_rewrites(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("TRENDS_LLM_MODEL", "test/trends-stage-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "Chinese (Simplified)")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    repository.create_run(
        config_fingerprint="fp-run-trend-pass-output",
        run_id="run-trend-pass-output",
    )

    published_at = datetime(2026, 3, 2, 1, 0, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-pass-output-1",
        canonical_url="https://example.com/pass-output-paper",
        title="Pass Output Paper",
        authors=["Alice"],
        published_at=published_at,
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-pass-output", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-pass-output", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        assert kwargs["llm_model"] == "test/trends-stage-model"
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
            "topics": ["agents"],
            "clusters": [],
            "highlights": [f"Hit doc_id {doc_id}, chunk 0"],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-pass-output",
        granularity="day",
        anchor_date=date(2026, 3, 2),
    )

    assert result.doc_id > 0
    assert result.pass_output_id is not None

    with Session(repository.engine) as session:
        pass_output = session.get(PassOutput, result.pass_output_id)
        assert pass_output is not None
        canonical_payload = json.loads(pass_output.payload_json)
        assert "doc_id" in str(canonical_payload.get("overview_md") or "")
        diagnostics = json.loads(pass_output.diagnostics_json or "{}")
        freshness = diagnostics["workflow_freshness"]
        assert freshness["kind"] == "trend_synthesis"
        assert freshness["components"]["granularity"] == "day"
        assert freshness["components"]["llm_model"] == "test/trends-stage-model"
        assert freshness["components"]["analysis_model"] == "test/fake-model"
        assert freshness["key"]
        upstream_sources = freshness["components"]["upstream_sources"]
        assert upstream_sources["key"]
        assert upstream_sources["documents_total"] == 1
        assert upstream_sources["chunks_total"] > 0
        assert upstream_sources["source_scopes"] == [
            {"doc_type": "item", "granularity": None}
        ]
        assert "chunks" not in upstream_sources

        trend_doc = session.exec(
            select(Document).where(Document.doc_type == "trend")
        ).first()
        assert trend_doc is not None
        meta_chunk = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == int(trend_doc.id or 0),
                DocumentChunk.chunk_index == 1,
            )
        ).first()
        assert meta_chunk is not None
        projected_payload = json.loads(str(meta_chunk.text))
        assert "doc_id" in str(projected_payload.get("overview_md") or "")
        projection_meta = projected_payload.get("_projection")
        assert projection_meta == {
            "pass_output_id": result.pass_output_id,
            "pass_kind": "trend_synthesis",
        }

    trend_note = (
        settings.markdown_output_dir
        / "Trends"
        / f"day--2026-03-02--trend--{result.doc_id}.md"
    )
    markdown = trend_note.read_text(encoding="utf-8")
    assert f"pass_output_id: {result.pass_output_id}" in markdown
    assert "pass_kind: trend_synthesis" in markdown
    assert "See doc_id" not in markdown
    assert re.search(r"(?<![\w])doc_id\s*[:=#-]?\s*\d+", markdown) is None


def test_trends_never_backfills_evidence_and_limits_single_source_output(
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

    published_at = datetime(2026, 3, 2, 1, 0, tzinfo=UTC)
    evidence_doc_id = _seed_item_document(
        repository=repository,
        published_at=published_at,
        source_item_id="trend-evidence-backfill-1",
        title="Grounding Paper",
    )

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": "Grounded trend overview.",
            "topics": ["agents"],
            "clusters": [
                {
                    "title": "Unsupported",
                    "content_md": "This cluster has no evidence supplied by the agent.",
                    "evidence_refs": [],
                },
                {
                    "title": "Grounding",
                    "content_md": "This is explicitly grounded in the only source.",
                    "evidence_refs": [{"doc_id": evidence_doc_id, "chunk_index": 0}],
                },
                {
                    "title": "Repeated framing",
                    "content_md": "A second cluster cannot manufacture a trend.",
                    "evidence_refs": [{"doc_id": evidence_doc_id, "chunk_index": 0}],
                },
            ],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    def _fake_search_chunks_text(**kwargs):  # type: ignore[no-untyped-def]
        pytest.fail(f"post-generation evidence search must not run: {kwargs}")

    monkeypatch.setattr(repository, "search_chunks_text", _fake_search_chunks_text)

    result = service.trends(
        run_id="run-trend-evidence-backfill",
        granularity="day",
        anchor_date=date(2026, 3, 2),
        llm_model="test/fake-model",
        analysis_llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert result.pass_output_id is not None

    with Session(repository.engine) as session:
        pass_output = session.get(PassOutput, result.pass_output_id)
        assert pass_output is not None
        payload = json.loads(pass_output.payload_json)
        assert payload["clusters"] == []

        diagnostics = json.loads(pass_output.diagnostics_json or "{}")
        assert "context_packs" not in diagnostics
        assert "context_pack_stats" in diagnostics
        rep_enforcement = diagnostics["rep_enforcement"]
        assert rep_enforcement["backfilled_total"] == 0
        assert rep_enforcement["failed_clusters_total"] == 3
        assert rep_enforcement["dropped_insufficient_support_total"] == 3
        assert rep_enforcement["dropped_unread_total"] == 2
        assert rep_enforcement["dropped_single_source_excess_total"] == 0
        assert rep_enforcement["single_source_mode_total"] == 1
        assert rep_enforcement["retained_clusters_total"] == 0
        assert rep_enforcement["read_trace_enforced_total"] == 1
        assert rep_enforcement["read_trace_unavailable_total"] == 1
        assert rep_enforcement["read_trace_complete_total"] == 0

    trend_note = (
        settings.markdown_output_dir
        / "Trends"
        / f"day--2026-03-02--trend--{result.doc_id}.md"
    )
    markdown = trend_note.read_text(encoding="utf-8")
    assert "#### Evidence" not in markdown
    assert "[Grounding Paper](" not in markdown


def test_trends_keep_only_distinct_item_sources_read_by_agent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    doc_1, doc_2, doc_3 = [
        _seed_item_document(
            repository=repository,
            published_at=period_start.replace(hour=index),
            source_item_id=f"trend-evidence-{index}",
            title=title,
        )
        for index, title in enumerate(
            ("Graph verifier", "Robot world models", "Compiler fuzzing"),
            start=1,
        )
    ]
    non_item_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Discovery-only trend",
    )
    assert non_item_doc.id is not None
    non_item_doc_id = int(non_item_doc.id)
    assert len({doc_1, doc_2, doc_3}) == 3
    assert (
        len(
            repository.list_documents(
                doc_type="item",
                period_start=period_start,
                period_end=period_end,
                limit=10,
            )
        )
        == 3
    )
    from recoleta.pipeline.trends_stage import TrendStageRequest, _TrendStageRunner
    from recoleta.trends import TrendPayload

    payload = TrendPayload.model_validate(
        {
            "title": "Evidence integrity",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "Only evidence inspected by the agent can survive.",
            "topics": ["agents"],
            "clusters": [
                {
                    "title": "Duplicate chunks",
                    "content_md": "Two chunks from one paper are still one source.",
                    "evidence_refs": [
                        {"doc_id": doc_1, "chunk_index": 0},
                        {"doc_id": doc_1, "chunk_index": 1},
                    ],
                },
                {
                    "title": "Independent support",
                    "content_md": "Two inspected papers support this signal.",
                    "evidence_refs": [
                        {"doc_id": doc_1, "chunk_index": 0},
                        {"doc_id": doc_2, "chunk_index": 0},
                    ],
                },
                {
                    "title": "Unread source",
                    "content_md": "A real but unread paper cannot support the output.",
                    "evidence_refs": [
                        {"doc_id": doc_1, "chunk_index": 0},
                        {"doc_id": doc_3, "chunk_index": 0},
                    ],
                },
                {
                    "title": "Trend-document citation",
                    "content_md": "A synthesis document is not primary evidence.",
                    "evidence_refs": [
                        {"doc_id": doc_1, "chunk_index": 0},
                        {"doc_id": non_item_doc_id, "chunk_index": 0},
                    ],
                },
                {
                    "title": "No references",
                    "content_md": "Search must not attach evidence after generation.",
                    "evidence_refs": [],
                },
            ],
        }
    )
    events = [
        {
            "kind": "tool-call",
            "tool_name": "read_chunk",
            "tool_call_id": "read-1",
            "args": {"doc_id": doc_1, "chunk_index": 0},
        },
        {
            "kind": "tool-return",
            "tool_name": "read_chunk",
            "tool_call_id": "read-1",
            "content": {"chunk": {"doc_id": doc_1, "chunk_index": 0}},
        },
        {
            "kind": "tool-call",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "bundle-2",
            "args": {"doc_id": doc_2, "content_limit": 2},
        },
        {
            "kind": "tool-return",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "bundle-2",
            "content": {
                "bundle": {
                    "doc": {"doc_id": doc_2},
                    "text": "RAW_TRACE_SENTINEL" * 2000,
                }
            },
        },
        {
            "kind": "tool-call",
            "tool_name": "get_doc",
            "tool_call_id": "metadata-3",
            "args": {"doc_id": doc_3},
        },
        {
            "kind": "tool-call",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "failed-bundle-3",
            "args": {"doc_id": doc_3, "content_limit": 2},
        },
        {
            "kind": "tool-return",
            "tool_name": "get_doc_bundle",
            "tool_call_id": "failed-bundle-3",
            "content": {"error": "document read failed"},
        },
    ]
    debug = {
        "usage": {"requests": 1, "input_tokens": 100, "output_tokens": 50},
        "tool_calls_total": 4,
        "tool_call_breakdown": {
            "get_doc": 1,
            "get_doc_bundle": 2,
            "read_chunk": 1,
        },
        "raw_tool_trace": {
            "status": "captured",
            "events": events,
            "events_total": len(events),
            "tool_calls_total": 4,
            "events_truncated": False,
        },
    }
    runner = _TrendStageRunner(
        service=service,
        request=TrendStageRequest(
            run_id="run-trend-evidence-integrity",
            granularity="day",
            anchor_date=date(2026, 3, 2),
            llm_model="test/fake-model",
            reuse_existing_corpus=True,
        ),
    )
    state = runner._prepare_state()

    stats = runner._enforce_cluster_evidence_refs(
        payload=payload,
        state=state,
        debug=debug,
    )

    assert stats["item_corpus_docs_total"] == 3
    assert [cluster.title for cluster in payload.clusters] == ["Independent support"]
    assert [ref.doc_id for ref in payload.clusters[0].evidence_refs] == [doc_1, doc_2]
    assert stats["backfilled_total"] == 0
    assert stats["dropped_duplicate_doc_total"] == 1
    assert stats["dropped_unread_total"] == 1
    assert stats["dropped_non_item_total"] == 1
    assert stats["dropped_insufficient_support_total"] == 4
    assert stats["retained_clusters_total"] == 1
    assert stats["read_trace_enforced_total"] == 1

    compact_debug = runner._compact_persisted_debug(debug)
    assert compact_debug["evidence_reads"] == {
        "trace_enforced": True,
        "trace_status": "captured",
        "trace_events_truncated": False,
        "trace_complete": True,
        "item_doc_ids": [doc_1, doc_2],
        "item_docs_total": 2,
    }
    compact_json = json.dumps(compact_debug)
    assert "raw_tool_trace" not in compact_debug
    assert "RAW_TRACE_SENTINEL" not in compact_json
    assert len(compact_json) < 2_000


def test_trends_records_metric_when_pass_output_persist_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    repository.create_run(
        config_fingerprint="fp-run-pass-output-metric",
        run_id="run-pass-output-metric",
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-pass-output-2",
        canonical_url="https://example.com/pass-output-metric",
        title="Pass Output Metric",
        authors=["Alice"],
        published_at=datetime(2026, 3, 3, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-pass-output-metric", drafts=[draft], limit=10)
    service.analyze(run_id="run-pass-output-metric", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        payload = {
            "title": "Daily Trend",
            "granularity": "day",
            "period_start": pstart.isoformat(),
            "period_end": pend.isoformat(),
            "overview_md": "- metric test",
            "topics": ["agents"],
            "clusters": [],
            "highlights": [],
        }
        return TrendPayload.model_validate(payload), {"tool_calls_total": 0}

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    def _explode_create_pass_output(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("simulated pass output write failure")

    monkeypatch.setattr(repository, "create_pass_output", _explode_create_pass_output)

    result = service.trends(
        run_id="run-pass-output-metric",
        granularity="day",
        anchor_date=date(2026, 3, 3),
        llm_model="test/fake-model",
        analysis_llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert result.pass_output_id is None

    with Session(repository.engine) as session:
        metrics = list(
            session.exec(
                select(Metric).where(
                    Metric.name == "pipeline.trends.pass_outputs.persist_failed_total"
                )
            )
        )
        assert metrics
        assert metrics[-1].value == 1
        assert list(session.exec(select(PassOutput))) == []


def test_trends_records_projection_failure_metric_without_failing_stage(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    repository.create_run(
        config_fingerprint="fp-run-trend-projection-failure",
        run_id="run-trend-projection-failure",
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-projection-failure-1",
        canonical_url="https://example.com/trend-projection-failure-1",
        title="Trend Projection Failure",
        authors=["Alice"],
        published_at=datetime(2026, 3, 4, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-projection-failure", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-projection-failure", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload
    import recoleta.pipeline.trends_stage as trends_stage

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        return (
            TrendPayload.model_validate(
                {
                    "title": "Daily Trend",
                    "granularity": "day",
                    "period_start": pstart.isoformat(),
                    "period_end": pend.isoformat(),
                    "overview_md": "- projection failure test",
                    "topics": ["agents"],
                    "clusters": [],
                    "highlights": [],
                }
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    def _explode_markdown_note(**kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        raise RuntimeError("simulated markdown projection failure")

    monkeypatch.setattr(
        trends_stage, "write_markdown_trend_note", _explode_markdown_note
    )

    result = service.trends(
        run_id="run-trend-projection-failure",
        granularity="day",
        anchor_date=date(2026, 3, 4),
        llm_model="test/fake-model",
        analysis_llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert result.pass_output_id is not None
    assert not (settings.markdown_output_dir / "Trends").exists()

    metric_values = _metric_values(
        repository=repository, run_id="run-trend-projection-failure"
    )
    assert (
        metric_values["pipeline.trends.projection.trend_markdown.failed_total"] == 1.0
    )


def test_trends_records_obsidian_projection_metric_when_note_is_written(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("PUBLISH_TARGETS", "obsidian")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "md"))
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(tmp_path / "vault"))
    monkeypatch.setenv("OBSIDIAN_BASE_FOLDER", "Recoleta")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("RAG_LANCEDB_DIR", str(tmp_path / "lancedb"))

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=FakeTelegramSender(),
    )
    repository.create_run(
        config_fingerprint="fp-run-trend-obsidian-projection",
        run_id="run-trend-obsidian-projection",
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-obsidian-projection-1",
        canonical_url="https://example.com/trend-obsidian-projection-1",
        title="Trend Obsidian Projection",
        authors=["Alice"],
        published_at=datetime(2026, 3, 5, 1, 0, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-trend-obsidian-projection", drafts=[draft], limit=10)
    service.analyze(run_id="run-trend-obsidian-projection", limit=10)

    from recoleta.rag import agent as rag_agent
    from recoleta.trends import TrendPayload

    def _fake_generate(**kwargs):  # type: ignore[no-untyped-def]
        pstart = kwargs["period_start"]
        pend = kwargs["period_end"]
        return (
            TrendPayload.model_validate(
                {
                    "title": "Daily Trend",
                    "granularity": "day",
                    "period_start": pstart.isoformat(),
                    "period_end": pend.isoformat(),
                    "overview_md": "- obsidian projection test",
                    "topics": ["agents"],
                    "clusters": [],
                    "highlights": [],
                }
            ),
            {"tool_calls_total": 0},
        )

    monkeypatch.setattr(rag_agent, "generate_trend_payload", _fake_generate)

    result = service.trends(
        run_id="run-trend-obsidian-projection",
        granularity="day",
        anchor_date=date(2026, 3, 5),
        llm_model="test/fake-model",
        analysis_llm_model="test/fake-model",
    )

    assert result.doc_id > 0
    assert settings.obsidian_vault_path is not None
    obsidian_note = (
        settings.obsidian_vault_path
        / settings.obsidian_base_folder
        / "Trends"
        / f"day--2026-03-05--trend--{result.doc_id}.md"
    )
    assert obsidian_note.exists()

    metric_values = _metric_values(
        repository=repository, run_id="run-trend-obsidian-projection"
    )
    assert (
        metric_values["pipeline.trends.projection.trend_obsidian.emitted_total"] == 1.0
    )
