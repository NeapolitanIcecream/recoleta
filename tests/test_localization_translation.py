from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

import pytest

from recoleta import translation as translation_module
from recoleta.config import LocalizationConfig, Settings
from recoleta.materialize import MaterializeTargetSpec, materialize_outputs
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.publish import write_markdown_ideas_note, write_markdown_trend_note
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft
from tests.spec_support import _build_runtime


def _seed_item_trend_and_idea(
    *,
    repository: Repository,
) -> tuple[int, int, int, TrendPayload, TrendIdeasPayload]:
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
    repository.save_analysis(
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

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent systems",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "English canonical trend overview.",
            "topics": ["agents", "robotics"],
            "clusters": [
                {
                    "title": "Reward models",
                    "content_md": "English canonical cluster description.",
                    "evidence_refs": [
                        {
                            "doc_id": int(item_doc.id),
                            "chunk_index": 0,
                            "title": "Robotics reward model",
                            "url": "https://example.com/robotics",
                            "reason": "Grounds the cluster in the canonical corpus.",
                        }
                    ],
                }
            ],
        }
    )
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload,
    )

    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Operator wedges",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "English canonical ideas summary.",
            "ideas": [
                {
                    "title": "Prompt release gate",
                    "content_md": "Introduce a release gate before rollout.",
                    "evidence_refs": [
                        {
                            "doc_id": int(item_doc.id),
                            "chunk_index": 0,
                            "reason": "The source note ties verification to rollout control.",
                        }
                    ],
                }
            ],
        }
    )
    idea_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Operator wedges",
    )
    assert idea_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=0,
        kind="summary",
        text_value=ideas_payload.summary_md,
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(ideas_payload.model_dump(mode="json"), ensure_ascii=False),
        source_content_type="trend_ideas_payload_json",
    )
    return int(item.id), int(trend_doc_id), int(idea_doc.id), trend_payload, ideas_payload


def test_settings_loads_localization_from_env_string(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [{"code": "zh-CN", "llm_label": "Chinese (Simplified)"}],
                "site_default_language_code": "en",
            }
        ),
    )

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.localization is not None
    assert settings.localization.source_language_code == "en"
    assert settings.localization.targets[0].code == "zh-CN"


def test_settings_rejects_localization_default_language_outside_declared_languages(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [{"code": "zh-CN", "llm_label": "Chinese (Simplified)"}],
                "site_default_language_code": "fr",
            }
        ),
    )

    with pytest.raises(ValueError, match="site_default_language_code"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_candidate_context_prefers_new_trend_and_idea_presentation_sidecars(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(tmp_path / "notes"))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    settings, repository = _build_runtime()
    item_id, trend_doc_id, idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )

    write_markdown_trend_note(
        output_dir=settings.markdown_output_dir,
        trend_doc_id=trend_doc_id,
        title=trend_payload.title,
        granularity="day",
        period_start=datetime.fromisoformat(trend_payload.period_start),
        period_end=datetime.fromisoformat(trend_payload.period_end),
        run_id="run-trend-note",
        overview_md=trend_payload.overview_md,
        topics=trend_payload.topics,
        clusters=[cluster.model_dump(mode="json") for cluster in trend_payload.clusters],
    )
    write_markdown_ideas_note(
        repository=repository,
        output_dir=settings.markdown_output_dir,
        pass_output_id=7,
        upstream_pass_output_id=3,
        granularity="day",
        period_start=datetime.fromisoformat(ideas_payload.period_start),
        period_end=datetime.fromisoformat(ideas_payload.period_end),
        run_id="run-ideas-note",
        status="succeeded",
        payload=ideas_payload,
        topics=trend_payload.topics,
    )

    trend_context = translation_module._candidate_context(
        repository=repository,
        settings=settings,
        candidate=translation_module.TranslationCandidate(
            source_kind="trend_synthesis",
            source_record_id=trend_doc_id,
            payload=trend_payload.model_dump(mode="json"),
            payload_model=None,
            canonical_language_code="en",
            document_id=trend_doc_id,
            granularity="day",
            period_start=datetime.fromisoformat(trend_payload.period_start),
            period_end=datetime.fromisoformat(trend_payload.period_end),
        ),
        context_assist="direct",
        run_id="run-context",
    )
    idea_context = translation_module._candidate_context(
        repository=repository,
        settings=settings,
        candidate=translation_module.TranslationCandidate(
            source_kind="trend_ideas",
            source_record_id=idea_doc_id,
            payload=ideas_payload.model_dump(mode="json"),
            payload_model=None,
            canonical_language_code="en",
            document_id=idea_doc_id,
            granularity="day",
            period_start=datetime.fromisoformat(ideas_payload.period_start),
            period_end=datetime.fromisoformat(ideas_payload.period_end),
        ),
        context_assist="direct",
        run_id="run-context",
    )

    assert trend_context["presentation"]["content"]["overview"] == trend_payload.overview_md
    assert "ranked_shifts" not in trend_context["presentation"]["content"]
    assert trend_context["presentation"]["content"]["clusters"][0]["title"] == "Reward models"
    assert idea_context["presentation"]["content"]["summary"] == ideas_payload.summary_md
    assert "opportunities" not in idea_context["presentation"]["content"]
    assert idea_context["presentation"]["content"]["ideas"][0]["title"] == "Prompt release gate"
    assert item_id > 0


def test_materialize_outputs_writes_localized_note_trees_from_localized_outputs(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, trend_doc_id, idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    output_dir = tmp_path / "outputs"
    localization = LocalizationConfig.model_validate(
        {
            "source_language_code": "en",
            "targets": [{"code": "zh-CN", "llm_label": "Chinese (Simplified)"}],
            "site_default_language_code": "en",
        }
    )

    repository.upsert_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        language_code="zh-CN",
        status="succeeded",
        source_hash="trend-zh",
        payload={
            **trend_payload.model_dump(mode="json"),
            "title": "智能体系统",
            "overview_md": "中文趋势概览。",
                "clusters": [
                    {
                        "title": "奖励模型",
                        "content_md": "中文聚类说明。",
                        "evidence_refs": [
                            ref.model_dump(mode="json")
                            for ref in trend_payload.clusters[0].evidence_refs
                        ],
                    }
                ],
            },
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        language_code="zh-CN",
        status="succeeded",
        source_hash="ideas-zh",
        payload={
            **ideas_payload.model_dump(mode="json"),
            "title": "运营机会",
            "summary_md": "中文机会摘要。",
            "ideas": [
                {
                    "title": "提示词发布闸门",
                    "content_md": "先加发布闸门，再扩大 rollout。",
                    "evidence_refs": [
                        ref.model_dump(mode="json")
                        for ref in ideas_payload.ideas[0].evidence_refs
                    ],
                }
            ],
        },
        diagnostics={},
        variant_role="translation",
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        localization=localization,
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    assert result.site_manifest_path is not None
    zh_root = output_dir / "Localized" / "zh-cn"
    trend_note = zh_root / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    idea_note = zh_root / "Ideas" / "day--2026-03-02--ideas.md"
    assert trend_note.exists()
    assert idea_note.exists()
    assert "智能体系统" in trend_note.read_text(encoding="utf-8")
    assert "## Overview" in trend_note.read_text(encoding="utf-8")
    assert "## Summary" in idea_note.read_text(encoding="utf-8")
    assert "提示词发布闸门" in idea_note.read_text(encoding="utf-8")
    assert validate_presentation(
        json.loads(presentation_sidecar_path(note_path=trend_note).read_text(encoding="utf-8"))
    ) == []
    assert validate_presentation(
        json.loads(presentation_sidecar_path(note_path=idea_note).read_text(encoding="utf-8"))
    ) == []


def test_run_translation_creates_localized_outputs_for_all_surfaces(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "English")
    monkeypatch.setenv(
        "LOCALIZATION",
        json.dumps(
            {
                "source_language_code": "en",
                "targets": [{"code": "zh-CN", "llm_label": "Chinese (Simplified)"}],
                "site_default_language_code": "en",
            }
        ),
    )
    settings, repository = _build_runtime()
    item_id, trend_doc_id, idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )

    def _fake_translate(*, request=None, **kwargs: Any) -> dict[str, Any]:
        normalized = translation_module.coerce_translate_structured_payload_request(
            request=request,
            legacy_kwargs=kwargs,
        )
        payload = dict(normalized.payload)
        payload["title"] = f"ZH {payload.get('title', '')}".strip()
        if "summary" in payload:
            payload["summary"] = "ZH item summary."
        if "overview_md" in payload:
            payload["overview_md"] = "ZH trend overview."
        if "summary_md" in payload:
            payload["summary_md"] = "ZH ideas summary."
        if "ideas" in payload and payload["ideas"]:
            payload["ideas"][0]["title"] = "ZH Prompt release gate"
            payload["ideas"][0]["content_md"] = "ZH idea body."
        return payload

    monkeypatch.setattr(translation_module, "translate_structured_payload", _fake_translate)

    result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include=["items", "trends", "ideas"],
        limit=10,
        context_assist="direct",
        force=True,
        run_id="run-translation",
    )

    outputs = repository.list_localized_outputs(language_code="zh-CN")
    assert result.translated_total == 3
    assert {output.source_kind for output in outputs} == {
        "analysis",
        "trend_ideas",
        "trend_synthesis",
    }
    assert repository.get_localized_output(
        source_kind="analysis",
        source_record_id=item_id,
        language_code="zh-CN",
    ) is not None
    assert repository.get_localized_output(
        source_kind="trend_synthesis",
        source_record_id=trend_doc_id,
        language_code="zh-CN",
    ) is not None
    assert repository.get_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        language_code="zh-CN",
    ) is not None
    metric_names = {
        metric.name for metric in repository.list_metrics(run_id="run-translation")
    }
    assert "pipeline.translate.task_duration_ms_total" in metric_names
    assert "pipeline.translate.duration_ms" not in metric_names
    assert trend_payload.title == "Agent systems"
    assert ideas_payload.title == "Operator wedges"
