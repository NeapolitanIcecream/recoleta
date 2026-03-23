from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from types import SimpleNamespace
from typing import cast

import pytest
from sqlmodel import Session, select
from typer.testing import CliRunner

import recoleta.cli as recoleta_cli
from recoleta import translation as translation_module
from recoleta.cli.app import app
from recoleta.config import LocalizationConfig, Settings
from recoleta.llm_connection import LLMConnectionConfig
from recoleta.materialize import MaterializeScopeSpec, materialize_outputs
from recoleta.models import Analysis, DocumentChunk, LocalizedOutput
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish import write_markdown_trend_note
from recoleta.rag.corpus_tools import SearchService
from recoleta.site import export_trend_static_site
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft


def _seed_item_trend_and_idea(
    *,
    repository: Repository,
) -> tuple[Analysis, int, int]:
    published_at = datetime(2026, 3, 2, 12, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-1",
        canonical_url="https://example.com/robotics",
        title="Robotics reward model",
        authors=["Alice"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    analysis = repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="openai/gpt-5.4",
            provider="openai",
            summary="## Summary\n\nEnglish canonical item summary.\n",
            topics=["agents", "robotics"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    persisted_item = repository.get_item(item_id=int(item.id))
    assert persisted_item is not None
    item_doc = repository.upsert_document_for_item(item=persisted_item)
    assert item_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(item_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="English canonical item summary.",
        source_content_type="analysis_summary",
    )
    repository.upsert_content(
        item_id=int(item.id),
        content_type="html_maintext",
        text="The reward model improves robotic policy comparison.",
    )

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "overview_md": "## Overview\n\nEnglish canonical trend overview.\n",
            "topics": ["agents", "robotics"],
            "clusters": [
                {
                    "name": "Reward models",
                    "description": "English canonical cluster description.",
                    "representative_chunks": [
                        {
                            "doc_id": int(item_doc.id),
                            "chunk_index": 0,
                            "title": "Robotics reward model",
                            "url": "https://example.com/robotics",
                        }
                    ],
                }
            ],
            "highlights": ["English highlight."],
            "evolution": {
                "summary_md": "English evolution summary.",
                "signals": [
                    {
                        "theme": "Verification first",
                        "change_type": "continuing",
                        "summary": "Verification is moving earlier.",
                        "history_windows": [],
                    }
                ],
            },
        }
    )
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        payload=trend_payload,
    )

    idea_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        title="Operator wedges",
    )
    assert idea_doc.id is not None
    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Operator wedges",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "English canonical ideas summary.",
            "ideas": [
                {
                    "title": "Prompt release gate",
                    "kind": "tooling_wedge",
                    "thesis": "Introduce a release gate.",
                    "why_now": "Models are changing quickly.",
                    "what_changed": "Teams need more validation.",
                    "user_or_job": "Research ops",
                    "evidence_refs": [{"doc_id": int(item_doc.id), "chunk_index": 0}],
                    "validation_next_step": "Ship a prototype.",
                    "time_horizon": "now",
                }
            ],
        }
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="English canonical ideas summary.",
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(ideas_payload.model_dump(mode="json"), ensure_ascii=False),
        source_content_type="trend_ideas_payload_json",
    )
    return analysis, int(trend_doc_id), int(idea_doc.id)


def test_settings_loads_localization_from_env_string(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
                "legacy_backfill_source_language_code": "zh-CN",
            }
        ),
    )

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.localization is not None
    assert settings.localization.source_language_code == "en"
    assert settings.localization.targets[0].code == "zh-CN"
    assert settings.localization.site_default_language_code == "en"
    assert settings.localization.legacy_backfill_source_language_code == "zh-CN"


def test_settings_rejects_localization_default_language_outside_declared_languages(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "fr",
            }
        ),
    )

    with pytest.raises(ValueError, match="site_default_language_code"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_rejects_localization_target_code_matching_source_language(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "en",
                        "llm_label": "English",
                    }
                ],
                "site_default_language_code": "en",
            }
        ),
    )

    with pytest.raises(ValueError, match="must not duplicate source_language_code"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_require_llm_output_language_when_localization_targets_are_configured(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delenv("LLM_OUTPUT_LANGUAGE", raising=False)
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            }
        ),
    )

    with pytest.raises(ValueError, match="LLM_OUTPUT_LANGUAGE is required"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_repository_upsert_localized_output_reuses_unique_source_scope_language(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    row, created = repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=11,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="hash-1",
        payload={"summary": "第一次"},
        diagnostics={"provider": "test"},
        variant_role="translation",
    )
    updated, created_again = repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=11,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="hash-2",
        payload={"summary": "第二次"},
        diagnostics={"provider": "test"},
        variant_role="translation",
    )

    assert created is True
    assert created_again is False
    assert updated.id == row.id
    assert updated.source_hash == "hash-2"
    assert json.loads(updated.payload_json)["summary"] == "第二次"


def test_run_translation_backfill_aborts_after_repeated_provider_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    localization = LocalizationConfig.model_validate(
        {
            "source_language_code": "en",
            "targets": [
                {
                    "code": "zh-CN",
                    "llm_label": "Chinese (Simplified)",
                }
            ],
            "site_default_language_code": "en",
            "legacy_backfill_source_language_code": "zh-CN",
        }
    )
    settings = SimpleNamespace(
        localization=localization,
        llm_model="test/fake-model",
        llm_output_language="English",
        llm_connection_config=lambda: LLMConnectionConfig(),
    )
    candidates = [
        translation_module.TranslationCandidate(
            source_kind="analysis",
            source_record_id=index + 1,
            scope="default",
            payload={"summary": f"条目 {index + 1}"},
            payload_model=None,
            canonical_language_code="zh-CN",
        )
        for index in range(10)
    ]

    class APIError(Exception):
        pass

    monkeypatch.setattr(
        translation_module,
        "_incremental_candidates",
        lambda **kwargs: candidates,
    )
    monkeypatch.setattr(
        translation_module,
        "_translate_candidate_into_language",
        lambda **kwargs: (_ for _ in ()).throw(APIError("Insufficient credits")),
    )

    result = translation_module.run_translation_backfill(
        repository=repository,
        settings=cast(Settings, settings),
        include="items",
        all_history=True,
    )

    assert result.aborted is True
    assert result.failed_total == 5
    assert result.scanned_total == 5
    assert result.translated_total == 0
    assert result.abort_reason is not None
    assert "consecutive provider failures" in result.abort_reason


def test_materialize_outputs_writes_localized_note_trees_from_localized_outputs(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, trend_doc_id, idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    output_dir = tmp_path / "outputs"

    repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=int(analysis.id or 0),
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="analysis-hash",
        payload={"summary": "## Summary\n\n中文条目摘要。\n"},
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="trend-hash",
        payload={
            "title": "智能体系统",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "overview_md": "## Overview\n\n中文趋势概览。\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": ["中文亮点。"],
            "evolution": None,
        },
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="idea-hash",
        payload={
            "title": "运营切入点",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "中文 ideas 摘要。",
            "ideas": [],
        },
        diagnostics={},
        variant_role="translation",
    )

    result = materialize_outputs(
        repository=repository,
        scope_specs=[MaterializeScopeSpec(scope="default", output_dir=output_dir)],
        localization=LocalizationConfig.model_validate(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            }
        ),
    )

    assert result.site_manifest_path is None
    localized_root = output_dir / "Localized" / "zh-cn"
    item_note = next((localized_root / "Inbox").glob("*.md"))
    trend_note = localized_root / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    idea_note = localized_root / "Ideas" / "day--2026-03-02--ideas.md"
    assert item_note.exists()
    assert trend_note.exists()
    assert idea_note.exists()
    assert "中文条目摘要" in item_note.read_text(encoding="utf-8")
    assert "智能体系统" in trend_note.read_text(encoding="utf-8")
    assert "运营切入点" in idea_note.read_text(encoding="utf-8")


def test_materialize_outputs_prefers_source_language_overrides_in_canonical_root(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, trend_doc_id, idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    output_dir = tmp_path / "outputs"

    with Session(repository.engine) as session:
        analysis_row = session.get(Analysis, int(analysis.id or 0))
        assert analysis_row is not None
        analysis_row.summary = "## Summary\n\n中文历史条目摘要。\n"
        trend_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.source_content_type == "trend_payload_json",
            )
        ).one()
        trend_payload = json.loads(trend_meta.text)
        trend_payload["title"] = "中文历史趋势"
        trend_payload["overview_md"] = "## Overview\n\n中文历史趋势概览。\n"
        trend_meta.text = json.dumps(trend_payload, ensure_ascii=False)
        idea_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == idea_doc_id,
                DocumentChunk.source_content_type == "trend_ideas_payload_json",
            )
        ).one()
        idea_payload = json.loads(idea_meta.text)
        idea_payload["title"] = "中文历史机会"
        idea_payload["summary_md"] = "中文历史 ideas 摘要。"
        idea_meta.text = json.dumps(idea_payload, ensure_ascii=False)
        session.add(analysis_row)
        session.add(trend_meta)
        session.add(idea_meta)
        session.commit()

    repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=int(analysis.id or 0),
        scope="default",
        language_code="en",
        status="succeeded",
        source_hash="analysis-en",
        payload={"summary": "## Summary\n\nHistorical item summary in English.\n"},
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=int(analysis.id or 0),
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="analysis-zh",
        payload={"summary": "## Summary\n\n中文历史条目摘要。\n"},
        diagnostics={},
        variant_role="mirror",
    )
    repository.upsert_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        scope="default",
        language_code="en",
        status="succeeded",
        source_hash="trend-en",
        payload={
            "title": "Historical trend in English",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "overview_md": "## Overview\n\nHistorical trend overview in English.\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": ["English highlight."],
            "evolution": None,
        },
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="trend-zh",
        payload={
            "title": "中文历史趋势",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "overview_md": "## Overview\n\n中文历史趋势概览。\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": ["中文亮点。"],
            "evolution": None,
        },
        diagnostics={},
        variant_role="mirror",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        scope="default",
        language_code="en",
        status="succeeded",
        source_hash="ideas-en",
        payload={
            "title": "Historical idea in English",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "Historical ideas summary in English.",
            "ideas": [],
        },
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        scope="default",
        language_code="zh-CN",
        status="succeeded",
        source_hash="ideas-zh",
        payload={
            "title": "中文历史机会",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "中文历史 ideas 摘要。",
            "ideas": [],
        },
        diagnostics={},
        variant_role="mirror",
    )
    repository.create_pass_output(
        run_id="run-ideas-source",
        pass_kind="trend_ideas",
        status="succeeded",
        scope="default",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        payload={
            "title": "中文历史机会",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "summary_md": "中文历史 ideas 摘要。",
            "ideas": [],
        },
    )

    result = materialize_outputs(
        repository=repository,
        scope_specs=[MaterializeScopeSpec(scope="default", output_dir=output_dir)],
        localization=LocalizationConfig.model_validate(
            {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
                "legacy_backfill_source_language_code": "zh-CN",
            }
        ),
    )

    assert result.site_manifest_path is None
    root_item_note = next((output_dir / "Inbox").glob("*.md"))
    root_trend_note = output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    root_idea_note = output_dir / "Ideas" / "day--2026-03-02--ideas.md"
    zh_root = output_dir / "Localized" / "zh-cn"
    assert "Historical item summary in English" in root_item_note.read_text(encoding="utf-8")
    assert "Historical trend in English" in root_trend_note.read_text(encoding="utf-8")
    assert "Historical idea in English" in root_idea_note.read_text(encoding="utf-8")
    assert "中文历史趋势" in (
        zh_root / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    ).read_text(encoding="utf-8")


def test_export_trend_static_site_builds_language_trees_and_redirect_shell(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=701,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-site-en",
        overview_md="## Overview\n\nEnglish note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        output_language="English",
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=notes_root / "Localized" / "zh-cn",
        trend_doc_id=701,
        title="智能体系统",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-site-zh",
        overview_md="## Overview\n\n中文笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        output_language="zh-CN",
        language_code="zh-CN",
    )

    site_dir = tmp_path / "site"
    manifest_path = export_trend_static_site(
        input_dir=notes_root,
        output_dir=site_dir,
        default_language_code="en",
    )

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["languages"] == ["en", "zh-cn"]
    assert manifest["default_language_code"] == "en"
    assert (site_dir / "en" / "index.html").exists()
    assert (site_dir / "zh-cn" / "index.html").exists()
    root_index = (site_dir / "index.html").read_text(encoding="utf-8")
    assert "localStorage" in root_index
    assert "en/index.html" in root_index

    en_detail = (
        site_dir / "en" / "trends" / f"{trend_note.stem}.html"
    ).read_text(encoding="utf-8")
    zh_detail = (
        site_dir / "zh-cn" / "trends" / f"{trend_note.stem}.html"
    ).read_text(encoding="utf-8")
    assert "<html lang='en'>" in en_detail
    assert "<html lang='zh-CN'>" in zh_detail
    assert "language-switcher" in en_detail
    assert "data-has-language-switcher=\"true\"" in en_detail
    assert "nav-utility-cluster" in en_detail
    assert "nav-link nav-link-external nav-link-repo" in en_detail
    assert ">Language<" in en_detail
    assert "../../zh-cn/trends/" in en_detail
    assert "Agent Systems" in en_detail
    assert "智能体系统" in zh_detail


def test_translate_run_cli_writes_incremental_localized_outputs_for_all_surfaces(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, trend_doc_id, idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    config_path = tmp_path / "recoleta.yaml"
    output_dir = tmp_path / "outputs"
    config_path.write_text(
        "\n".join(
            [
                f'recoleta_db_path: "{repository.db_path}"',
                'llm_model: "openai/gpt-5.4"',
                'publish_targets: ["markdown"]',
                f'markdown_output_dir: "{output_dir}"',
                'llm_output_language: "English"',
                "localization:",
                "  source_language_code: en",
                "  targets:",
                '    - code: "zh-CN"',
                '      llm_label: "Chinese (Simplified)"',
                "  site_default_language_code: en",
                "",
            ]
        ),
        encoding="utf-8",
    )

    import recoleta.translation as translation_module

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            (
                kwargs["payload"]
                | (
                    {"summary": "## Summary\n\n中文条目摘要。\n"}
                    if kwargs["source_kind"] == "analysis"
                    else {}
                )
                | (
                    {"title": "智能体系统"}
                    if kwargs["source_kind"] == "trend_synthesis"
                    else {}
                )
                | (
                    {"title": "运营切入点"}
                    if kwargs["source_kind"] == "trend_ideas"
                    else {}
                )
            ),
            {
                "usage": {"requests": 1, "input_tokens": 80, "output_tokens": 24},
                "estimated_cost_usd": 0.0016,
            },
        )
        if kwargs.get("return_debug")
        else (
            kwargs["payload"]
            | (
                {"summary": "## Summary\n\n中文条目摘要。\n"}
                if kwargs["source_kind"] == "analysis"
                else {}
            )
            | (
                {"title": "智能体系统"}
                if kwargs["source_kind"] == "trend_synthesis"
                else {}
            )
            | (
                {"title": "运营切入点"}
                if kwargs["source_kind"] == "trend_ideas"
                else {}
            )
        ),
    )

    result = runner.invoke(
        app,
        [
            "translate",
            "run",
            "--config-path",
            str(config_path),
            "--include",
            "items,trends,ideas",
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert "Billing report" in result.stdout

    second = runner.invoke(
        app,
        [
            "translate",
            "run",
            "--config-path",
            str(config_path),
            "--include",
            "items,trends,ideas",
        ],
    )
    assert second.exit_code == 0, second.stdout
    assert "Billing report" in second.stdout

    with Session(repository.engine) as session:
        rows = list(
            session.exec(
                select(LocalizedOutput).order_by(LocalizedOutput.source_kind)
            )
        )
    assert [(row.source_kind, row.source_record_id) for row in rows] == [
        ("analysis", int(analysis.id or 0)),
        ("trend_ideas", idea_doc_id),
        ("trend_synthesis", trend_doc_id),
    ]
    assert all(row.language_code == "zh-CN" for row in rows)
    recent_runs = repository.list_recent_runs(limit=2)
    assert len(recent_runs) == 2
    assert all(run.command == "translate run" for run in recent_runs)
    recent_metric_names = [
        {
            str(getattr(metric, "name", "") or "")
            for metric in repository.list_metrics(run_id=run.id)
        }
        for run in recent_runs
    ]
    assert any(
        "pipeline.translate.llm_requests_total" in metric_names
        for metric_names in recent_metric_names
    )


def test_translate_run_cli_json_includes_run_id_and_billing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, _trend_doc_id, _idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    config_path = tmp_path / "recoleta-json.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'recoleta_db_path: "{repository.db_path}"',
                'llm_model: "openai/gpt-5.4"',
                'publish_targets: ["markdown"]',
                f'markdown_output_dir: "{tmp_path / "outputs"}"',
                'llm_output_language: "English"',
                "localization:",
                "  source_language_code: en",
                "  targets:",
                '    - code: "zh-CN"',
                '      llm_label: "Chinese (Simplified)"',
                "  site_default_language_code: en",
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            kwargs["payload"],
            {
                "usage": {"requests": 1, "input_tokens": 64, "output_tokens": 16},
                "estimated_cost_usd": 0.0011,
            },
        )
        if kwargs.get("return_debug")
        else kwargs["payload"],
    )

    result = runner.invoke(
        app,
        [
            "translate",
            "run",
            "--config-path",
            str(config_path),
            "--include",
            "items",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "translate run"
    assert payload["run_id"]
    assert payload["billing"]["components"]["translation_llm"]["calls"] == 1
    assert payload["billing"]["components"]["translation_llm"]["input_tokens"] == 64
    assert payload["billing"]["components"]["translation_llm"]["output_tokens"] == 16
    assert payload["billing"]["total_cost_usd"] == 0.0011
    row = repository.get_localized_output(
        source_kind="analysis",
        source_record_id=int(analysis.id or 0),
        scope="default",
        language_code="zh-CN",
    )
    assert row is not None


def test_translate_run_hybrid_uses_search_service_without_auto_syncing_vectors(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _analysis, _trend_doc_id, _idea_doc_id = _seed_item_trend_and_idea(
        repository=repository
    )
    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "rag_lancedb_dir": tmp_path / "lancedb",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            },
        }
    )

    import recoleta.rag.semantic_search as semantic_search_module
    import recoleta.translation as translation_module

    hybrid_calls: list[dict[str, object]] = []
    captured_contexts: list[dict[str, object]] = []
    original_search_hybrid = SearchService.search_hybrid

    def _recording_search_hybrid(self, **kwargs):  # type: ignore[no-untyped-def]
        hybrid_calls.append(dict(kwargs))
        return original_search_hybrid(self, **kwargs)

    monkeypatch.setattr(SearchService, "search_hybrid", _recording_search_hybrid)
    monkeypatch.setattr(
        semantic_search_module,
        "ensure_summary_vectors_for_period",
        lambda **_: (_ for _ in ()).throw(
            AssertionError("translation hybrid search must not auto-sync vectors")
        ),
    )
    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            captured_contexts.append(dict(kwargs["context"] or {}))
            or kwargs["payload"]
        ),
    )

    result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include="items",
        context_assist="hybrid",
        force=True,
    )

    assert result.failed_total == 0
    assert result.translated_total == 1
    assert len(hybrid_calls) == 1
    assert hybrid_calls[0]["doc_type"] == "item"
    assert captured_contexts
    assert captured_contexts[0]["assist_mode"] == "hybrid"
    assert captured_contexts[0]["hybrid_status"] == "ok"
    assert captured_contexts[0]["hybrid_matches"]
    assert repository.list_metrics(run_id="translation-context") == []


def test_translate_run_records_llm_and_context_metrics_when_run_id_is_present(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _analysis, _trend_doc_id, _idea_doc_id = _seed_item_trend_and_idea(
        repository=repository
    )
    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "rag_lancedb_dir": tmp_path / "lancedb",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            },
        }
    )
    run = repository.create_run("fp-translate-metrics", run_id="run-translate-metrics")

    def _recording_search_hybrid(self, **kwargs):  # type: ignore[no-untyped-def]
        _ = kwargs
        if str(getattr(self, "metric_namespace", "") or "").strip():
            self.repository.record_metric(
                run_id=self.run_id,
                name=f"{self.metric_namespace}.embedding_calls_total",
                value=1,
                unit="count",
            )
        return {
            "hits": [],
            "returned": 0,
            "source_returned": {"text": 0, "semantic": 0},
        }

    monkeypatch.setattr(SearchService, "search_hybrid", _recording_search_hybrid)
    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            kwargs["payload"],
            {
                "usage": {"requests": 1, "input_tokens": 72, "output_tokens": 18},
                "estimated_cost_usd": 0.0013,
            },
        )
        if kwargs.get("return_debug")
        else kwargs["payload"],
    )

    result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include="items",
        context_assist="hybrid",
        force=True,
        run_id=run.id,
    )

    assert result.failed_total == 0
    assert result.translated_total == 1
    metric_values = {
        str(metric.name): float(metric.value)
        for metric in repository.list_metrics(run_id=run.id)
    }
    assert metric_values["pipeline.translate.llm_requests_total"] == 1.0
    assert metric_values["pipeline.translate.llm_input_tokens_total"] == 72.0
    assert metric_values["pipeline.translate.llm_output_tokens_total"] == 18.0
    assert metric_values["pipeline.translate.estimated_cost_usd"] == 0.0013
    assert metric_values["pipeline.translate.context.embedding_calls_total"] == 1.0


def test_translate_run_hybrid_fails_open_when_search_service_raises(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, _trend_doc_id, _idea_doc_id = _seed_item_trend_and_idea(
        repository=repository
    )
    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "rag_lancedb_dir": tmp_path / "lancedb",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            },
        }
    )

    import recoleta.translation as translation_module

    calls: list[str] = []
    captured_contexts: list[dict[str, object]] = []

    def _raising_search_hybrid(self, **kwargs):  # type: ignore[no-untyped-def]
        _ = self
        calls.append(str(kwargs.get("doc_type") or ""))
        raise RuntimeError("search backend unavailable")

    monkeypatch.setattr(SearchService, "search_hybrid", _raising_search_hybrid)
    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            captured_contexts.append(dict(kwargs["context"] or {}))
            or kwargs["payload"]
        ),
    )

    result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include="items",
        context_assist="hybrid",
        force=True,
    )

    assert calls == ["item"]
    assert result.failed_total == 0
    assert result.translated_total == 1
    assert captured_contexts[0]["hybrid_status"] == "failed_open"

    row = repository.get_localized_output(
        source_kind="analysis",
        source_record_id=int(analysis.id or 0),
        scope="default",
        language_code="zh-CN",
    )
    assert row is not None


def test_translate_run_prefers_canonical_pass_outputs_for_trends_and_ideas(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _analysis, trend_doc_id, idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    repository.create_pass_output(
        run_id="run-trend-pass",
        pass_kind="trend_synthesis",
        status="succeeded",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Canonical trend payload",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "## Overview\n\nCanonical overview from pass output.\n",
                "topics": ["agents", "robotics"],
                "clusters": [],
                "highlights": ["Canonical highlight."],
                "evolution": None,
            }
        ).model_dump(mode="json"),
    )
    repository.create_pass_output(
        run_id="run-idea-pass",
        pass_kind="trend_ideas",
        status="succeeded",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Canonical ideas payload",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "Canonical ideas summary from pass output.",
                "ideas": [],
            }
        ).model_dump(mode="json"),
    )
    with Session(repository.engine) as session:
        trend_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.source_content_type == "trend_payload_json",
            )
        ).one()
        idea_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == idea_doc_id,
                DocumentChunk.source_content_type == "trend_ideas_payload_json",
            )
        ).one()
        trend_payload = json.loads(trend_meta.text)
        trend_payload["title"] = "Projection trend snapshot"
        idea_payload = json.loads(idea_meta.text)
        idea_payload["title"] = "Projection ideas snapshot"
        trend_meta.text = json.dumps(trend_payload, ensure_ascii=False)
        idea_meta.text = json.dumps(idea_payload, ensure_ascii=False)
        session.add(trend_meta)
        session.add(idea_meta)
        session.commit()

    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
            },
        }
    )

    import recoleta.translation as translation_module

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: kwargs["payload"],
    )

    result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include="trends,ideas",
        force=True,
    )

    assert result.failed_total == 0
    assert result.translated_total == 2
    trend_row = repository.get_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        scope="default",
        language_code="zh-CN",
    )
    idea_row = repository.get_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        scope="default",
        language_code="zh-CN",
    )
    assert trend_row is not None
    assert idea_row is not None
    assert json.loads(trend_row.payload_json)["title"] == "Canonical trend payload"
    assert json.loads(idea_row.payload_json)["title"] == "Canonical ideas payload"


def test_translate_backfill_cli_writes_translation_and_mirror_variants(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    analysis, trend_doc_id, idea_doc_id = _seed_item_trend_and_idea(repository=repository)

    repository.save_analysis(
        item_id=int(repository.get_item(item_id=1).id or 1),  # type: ignore[union-attr]
        result=AnalysisResult(
            model="openai/gpt-5.4",
            provider="openai",
            summary="## Summary\n\n中文历史条目摘要。\n",
            topics=["agents", "robotics"],
            relevance_score=0.9,
            novelty_score=0.3,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    with Session(repository.engine) as session:
        trend_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.chunk_index == 1,
            )
        ).one()
        trend_payload = json.loads(trend_meta.text)
        trend_payload["title"] = "中文历史趋势"
        trend_payload["overview_md"] = "## Overview\n\n中文历史趋势概览。\n"
        trend_meta.text = json.dumps(trend_payload, ensure_ascii=False)
        session.add(trend_meta)

        idea_meta = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == idea_doc_id,
                DocumentChunk.kind == "meta",
            )
        ).one()
        idea_payload = json.loads(idea_meta.text)
        idea_payload["title"] = "中文历史机会"
        idea_payload["summary_md"] = "中文历史 ideas 摘要。"
        idea_meta.text = json.dumps(idea_payload, ensure_ascii=False)
        session.add(idea_meta)
        session.commit()

    config_path = tmp_path / "recoleta-backfill.yaml"
    output_dir = tmp_path / "outputs"
    config_path.write_text(
        "\n".join(
            [
                f'recoleta_db_path: "{repository.db_path}"',
                'llm_model: "openai/gpt-5.4"',
                'publish_targets: ["markdown"]',
                f'markdown_output_dir: "{output_dir}"',
                'llm_output_language: "English"',
                "localization:",
                "  source_language_code: en",
                "  targets:",
                '    - code: "zh-CN"',
                '      llm_label: "Chinese (Simplified)"',
                "  site_default_language_code: en",
                '  legacy_backfill_source_language_code: "zh-CN"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    import recoleta.translation as translation_module

    def _fake_translate(**kwargs):  # type: ignore[no-untyped-def]
        payload = dict(kwargs["payload"])
        if kwargs["target_language_code"] == "en":
            payload["title"] = {
                "trend_synthesis": "Historical trend in English",
                "trend_ideas": "Historical idea in English",
            }.get(kwargs["source_kind"], payload.get("title"))
            if kwargs["source_kind"] == "analysis":
                payload["summary"] = "## Summary\n\nHistorical item summary in English.\n"
        if kwargs.get("return_debug"):
            return (
                payload,
                {
                    "usage": {"requests": 1, "input_tokens": 70, "output_tokens": 20},
                    "estimated_cost_usd": 0.0015,
                },
            )
        return payload

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        _fake_translate,
    )

    result = runner.invoke(
        app,
        [
            "translate",
            "backfill",
            "--config-path",
            str(config_path),
            "--all-history",
            "--include",
            "items,trends,ideas",
            "--emit-mirror-targets",
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert "Billing report" in result.stdout

    with Session(repository.engine) as session:
        rows = list(session.exec(select(LocalizedOutput)))
    by_key = {
        (row.source_kind, row.source_record_id, row.language_code): row
        for row in rows
    }
    assert ("analysis", int(analysis.id or 0), "en") in by_key
    assert ("analysis", int(analysis.id or 0), "zh-CN") in by_key
    assert ("trend_synthesis", trend_doc_id, "en") in by_key
    assert ("trend_synthesis", trend_doc_id, "zh-CN") in by_key
    assert ("trend_ideas", idea_doc_id, "en") in by_key
    assert ("trend_ideas", idea_doc_id, "zh-CN") in by_key
    assert by_key[("analysis", int(analysis.id or 0), "zh-CN")].variant_role == "mirror"
    assert by_key[("analysis", int(analysis.id or 0), "en")].variant_role == "translation"
    recent_run = repository.list_recent_runs(limit=1)[0]
    assert recent_run.command == "translate backfill"


def test_translate_backfill_cli_json_includes_run_id_and_billing(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _analysis, _trend_doc_id, _idea_doc_id = _seed_item_trend_and_idea(repository=repository)
    config_path = tmp_path / "recoleta-backfill-json.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'recoleta_db_path: "{repository.db_path}"',
                'llm_model: "openai/gpt-5.4"',
                'publish_targets: ["markdown"]',
                f'markdown_output_dir: "{tmp_path / "outputs"}"',
                'llm_output_language: "English"',
                "localization:",
                "  source_language_code: en",
                "  targets:",
                '    - code: "zh-CN"',
                '      llm_label: "Chinese (Simplified)"',
                "  site_default_language_code: en",
                '  legacy_backfill_source_language_code: "zh-CN"',
                "",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: (
            kwargs["payload"],
            {
                "usage": {"requests": 1, "input_tokens": 88, "output_tokens": 22},
                "estimated_cost_usd": 0.0019,
            },
        )
        if kwargs.get("return_debug")
        else kwargs["payload"],
    )

    result = runner.invoke(
        app,
        [
            "translate",
            "backfill",
            "--config-path",
            str(config_path),
            "--include",
            "items",
            "--all-history",
            "--json",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "translate backfill"
    assert payload["run_id"]
    assert payload["billing"]["components"]["translation_llm"]["calls"] == 1
    assert payload["billing"]["components"]["translation_llm"]["input_tokens"] == 88
    assert payload["billing"]["components"]["translation_llm"]["output_tokens"] == 22
    assert payload["billing"]["total_cost_usd"] == 0.0019


def test_translate_run_preserves_success_when_billing_metrics_lookup_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import recoleta.cli.translate as translate_cli

    class _FakeConsole:
        def __init__(self) -> None:
            self.lines: list[str] = []

        def print(self, message: str) -> None:
            self.lines.append(str(message))

    class _FakeHeartbeat:
        def raise_if_failed(self) -> None:
            return None

    class _FakeLog:
        def __init__(self) -> None:
            self.warning_calls: list[str] = []

        def warning(self, message: str, *args: object) -> None:
            self.warning_calls.append(message.format(*args))

        def exception(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("unexpected exception log")

    class _FakeRepository:
        def __init__(self) -> None:
            self.finished: list[tuple[str, bool]] = []

        def finish_run(self, run_id: str, *, success: bool) -> None:
            self.finished.append((run_id, bool(success)))

        def list_metrics(self, *, run_id: str):  # type: ignore[no-untyped-def]
            _ = run_id
            raise RuntimeError("metrics unavailable")

    fake_repo = _FakeRepository()
    fake_console = _FakeConsole()
    fake_log = _FakeLog()
    fake_settings = SimpleNamespace(log_json=False)

    monkeypatch.setattr(
        translate_cli,
        "_load_settings_for_translate",
        lambda **_: (Path("/tmp/recoleta.db"), fake_settings, fake_repo, fake_console),
    )
    monkeypatch.setattr(
        recoleta_cli,
        "_begin_managed_run_for_settings",
        lambda **_: ("run-translate", "owner", fake_log, _FakeHeartbeat()),
    )
    monkeypatch.setattr(
        recoleta_cli,
        "_cleanup_managed_run",
        lambda **_: None,
    )
    monkeypatch.setattr(
        recoleta_cli,
        "_print_billing_report",
        lambda **_: None,
    )
    monkeypatch.setattr(
        recoleta_cli,
        "_update_run_context",
        lambda *args, **kwargs: None,
    )
    monkeypatch.setattr(
        translation_module,
        "run_translation",
        lambda **_: translation_module.TranslationRunResult(translated_total=1),
    )

    translate_cli.run_translate_run_command(
        db_path=None,
        config_path=None,
        scope="default",
        granularity=None,
        include="items",
        limit=None,
        force=False,
        context_assist="direct",
        json_output=False,
    )

    assert fake_repo.finished == [("run-translate", True)]
    assert any("translate run completed" in line for line in fake_console.lines)
    assert fake_log.warning_calls


def test_translate_backfill_latest_only_limits_trends_and_ideas_to_latest_window(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _analysis, latest_trend_doc_id, latest_idea_doc_id = _seed_item_trend_and_idea(
        repository=repository
    )
    older_start = datetime(2026, 3, 1, tzinfo=UTC)
    older_end = datetime(2026, 3, 2, tzinfo=UTC)
    older_trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=older_start,
        period_end=older_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Older trend",
                "granularity": "day",
                "period_start": older_start.isoformat(),
                "period_end": older_end.isoformat(),
                "overview_md": "## Overview\n\nOlder trend overview.\n",
                "topics": ["agents"],
                "clusters": [],
                "highlights": [],
                "evolution": None,
            }
        ),
    )
    older_idea_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=older_start,
        period_end=older_end,
        title="Older ideas",
    )
    assert older_idea_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(older_idea_doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Older ideas summary.",
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(older_idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(
            TrendIdeasPayload.model_validate(
                {
                    "title": "Older ideas",
                    "granularity": "day",
                    "period_start": older_start.isoformat(),
                    "period_end": older_end.isoformat(),
                    "summary_md": "Older ideas summary.",
                    "ideas": [],
                }
            ).model_dump(mode="json"),
            ensure_ascii=False,
        ),
        source_content_type="trend_ideas_payload_json",
    )

    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
                "legacy_backfill_source_language_code": "zh-CN",
            },
        }
    )

    import recoleta.translation as translation_module

    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: kwargs["payload"],
    )

    latest_only_result = translation_module.run_translation_backfill(
        repository=repository,
        settings=settings,
        include="trends,ideas",
        all_history=False,
        force=True,
    )
    assert latest_only_result.failed_total == 0
    latest_only_rows = repository.list_localized_outputs(
        scope="default",
        language_code="en",
    )
    latest_only_keys = {
        (row.source_kind, row.source_record_id)
        for row in latest_only_rows
    }
    assert latest_only_keys == {
        ("trend_synthesis", latest_trend_doc_id),
        ("trend_ideas", latest_idea_doc_id),
    }

    all_history_result = translation_module.run_translation_backfill(
        repository=repository,
        settings=settings,
        include="trends,ideas",
        all_history=True,
        force=True,
    )
    assert all_history_result.failed_total == 0
    history_rows = repository.list_localized_outputs(
        scope="default",
        language_code="en",
    )
    history_keys = {
        (row.source_kind, row.source_record_id)
        for row in history_rows
    }
    assert history_keys == {
        ("trend_synthesis", int(older_trend_doc_id)),
        ("trend_synthesis", latest_trend_doc_id),
        ("trend_ideas", int(older_idea_doc.id)),
        ("trend_ideas", latest_idea_doc_id),
    }


def test_run_translation_backfill_creates_missing_idea_documents_from_pass_outputs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    row = repository.create_pass_output(
        run_id="run-ideas-backfill-doc",
        pass_kind="trend_ideas",
        status="succeeded",
        scope="default",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Operator wedges",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "English canonical ideas summary.",
                "ideas": [
                    {
                        "title": "Prompt release gate",
                        "kind": "tooling_wedge",
                        "thesis": "Introduce a release gate.",
                        "why_now": "Models are changing quickly.",
                        "what_changed": "Teams need more validation.",
                        "user_or_job": "Research ops",
                        "evidence_refs": [],
                        "validation_next_step": "Ship a prototype.",
                        "time_horizon": "now",
                    }
                ],
            }
        ).model_dump(mode="json"),
    )
    settings = Settings.model_validate(
        {
            "recoleta_db_path": repository.db_path,
            "llm_model": "openai/gpt-5.4",
            "llm_output_language": "English",
            "localization": {
                "source_language_code": "en",
                "targets": [
                    {
                        "code": "zh-CN",
                        "llm_label": "Chinese (Simplified)",
                    }
                ],
                "site_default_language_code": "en",
                "legacy_backfill_source_language_code": "zh-CN",
            },
        }
    )
    monkeypatch.setattr(
        translation_module,
        "translate_structured_payload",
        lambda **kwargs: kwargs["payload"],
    )

    result = translation_module.run_translation_backfill(
        repository=repository,
        settings=settings,
        include="ideas",
        all_history=True,
        force=True,
    )

    assert result.failed_total == 0
    with Session(repository.engine) as session:
        idea_doc = session.exec(
            select(translation_module.Document)
            .where(
                translation_module.Document.doc_type == "idea",
                translation_module.Document.scope == "default",
                translation_module.Document.granularity == "day",
                translation_module.Document.period_start == period_start,
                translation_module.Document.period_end == period_end,
            )
        ).first()
    assert idea_doc is not None
    rows = repository.list_localized_outputs(scope="default", language_code="en")
    keys = {(row.source_kind, row.source_record_id) for row in rows}
    assert ("trend_ideas", int(idea_doc.id or 0)) in keys
    meta_chunk = repository.read_document_chunk(doc_id=int(idea_doc.id or 0), chunk_index=2)
    assert meta_chunk is not None
    assert meta_chunk.source_content_type == "trend_ideas_payload_json"
    assert int(row.id or 0) > 0
