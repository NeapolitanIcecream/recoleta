from __future__ import annotations

from datetime import UTC, datetime, timedelta
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
        text_value=json.dumps(
            ideas_payload.model_dump(mode="json"), ensure_ascii=False
        ),
        source_content_type="trend_ideas_payload_json",
    )
    return (
        int(item.id),
        int(trend_doc_id),
        int(idea_doc.id),
        trend_payload,
        ideas_payload,
    )


def _seed_suppressed_generation_windows(
    *,
    repository: Repository,
    trend_payload: TrendPayload,
    ideas_payload: TrendIdeasPayload,
) -> None:
    period_start = datetime.fromisoformat(trend_payload.period_start)
    period_end = datetime.fromisoformat(trend_payload.period_end)
    repository.create_pass_output(
        run_id="run-older-trend-success",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    repository.create_pass_output(
        run_id="run-latest-trend-suppression",
        pass_kind="trend_synthesis",
        status="suppressed",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    repository.create_pass_output(
        run_id="run-older-ideas-success",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
    )
    repository.create_pass_output(
        run_id="run-latest-ideas-suppression",
        pass_kind="trend_ideas",
        status="suppressed",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
    )


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
        clusters=[
            cluster.model_dump(mode="json") for cluster in trend_payload.clusters
        ],
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

    assert (
        trend_context["presentation"]["content"]["overview"]
        == trend_payload.overview_md
    )
    assert "ranked_shifts" not in trend_context["presentation"]["content"]
    assert (
        trend_context["presentation"]["content"]["clusters"][0]["title"]
        == "Reward models"
    )
    assert (
        idea_context["presentation"]["content"]["summary"] == ideas_payload.summary_md
    )
    assert "opportunities" not in idea_context["presentation"]["content"]
    assert (
        idea_context["presentation"]["content"]["ideas"][0]["title"]
        == "Prompt release gate"
    )
    assert item_id > 0


def test_suppressed_generation_windows_are_not_translation_candidates(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, _trend_doc_id, _idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    _seed_suppressed_generation_windows(
        repository=repository,
        trend_payload=trend_payload,
        ideas_payload=ideas_payload,
    )

    candidates = translation_module._incremental_candidates(
        repository=repository,
        granularity="day",
        include={"trends", "ideas"},
        limit=10,
        source_language_code="en",
        all_history=True,
    )

    assert candidates == []


@pytest.mark.parametrize("new_trend_status", ["succeeded", "suppressed"])
def test_ideas_translation_requires_the_current_succeeded_trend(
    tmp_path: Path,
    new_trend_status: str,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, _trend_doc_id, _idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    period_start = datetime.fromisoformat(trend_payload.period_start)
    period_end = datetime.fromisoformat(trend_payload.period_end)
    prior_trend = repository.create_pass_output(
        run_id="run-prior-currentness-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert prior_trend.id is not None
    repository.create_pass_output(
        run_id="run-stale-currentness-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            {
                "ref_kind": "pass_output",
                "pass_kind": "trend_synthesis",
                "pass_output_id": prior_trend.id,
            }
        ],
    )
    repository.create_pass_output(
        run_id=f"run-new-currentness-trend-{new_trend_status}",
        pass_kind="trend_synthesis",
        status=new_trend_status,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )

    candidates = translation_module._incremental_candidates(
        repository=repository,
        granularity="day",
        include={"ideas"},
        limit=10,
        source_language_code="en",
        all_history=True,
    )

    assert candidates == []


def test_translation_limit_is_applied_after_suppressed_windows_are_filtered(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, _trend_doc_id, _idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    older_start = datetime(2026, 3, 1, tzinfo=UTC)
    older_end = datetime(2026, 3, 2, tzinfo=UTC)
    older_trend = trend_payload.model_copy(
        update={
            "period_start": older_start.isoformat(),
            "period_end": older_end.isoformat(),
            "title": "Older valid trend",
        }
    )
    persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=older_start,
        period_end=older_end,
        payload=older_trend,
    )
    older_trend_row = repository.create_pass_output(
        run_id="run-older-valid-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=older_start,
        period_end=older_end,
        payload=older_trend.model_dump(mode="json"),
    )
    assert older_trend_row.id is not None
    older_ideas = ideas_payload.model_copy(
        update={
            "period_start": older_start.isoformat(),
            "period_end": older_end.isoformat(),
            "title": "Older valid ideas",
        }
    )
    repository.create_pass_output(
        run_id="run-older-valid-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=older_start,
        period_end=older_end,
        payload=older_ideas.model_dump(mode="json"),
        input_refs=[
            {
                "ref_kind": "pass_output",
                "pass_kind": "trend_synthesis",
                "pass_output_id": older_trend_row.id,
            }
        ],
    )
    _seed_suppressed_generation_windows(
        repository=repository,
        trend_payload=trend_payload,
        ideas_payload=ideas_payload,
    )

    candidates = translation_module._incremental_candidates(
        repository=repository,
        granularity="day",
        include={"trends", "ideas"},
        limit=1,
        source_language_code="en",
        all_history=True,
    )

    assert {candidate.source_kind for candidate in candidates} == {
        "trend_synthesis",
        "trend_ideas",
    }
    candidate_period_starts = {candidate.period_start for candidate in candidates}
    assert len(candidate_period_starts) == 1
    candidate_period_start = candidate_period_starts.pop()
    assert candidate_period_start is not None
    assert candidate_period_start.replace(tzinfo=UTC) == older_start


def test_idea_translation_limit_prefers_newer_missing_projection_backfill(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, _trend_doc_id, _idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    existing_start = datetime.fromisoformat(trend_payload.period_start)
    existing_end = datetime.fromisoformat(trend_payload.period_end)
    existing_trend = repository.create_pass_output(
        run_id="run-existing-backfill-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=existing_start,
        period_end=existing_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert existing_trend.id is not None
    repository.create_pass_output(
        run_id="run-existing-backfill-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=existing_start,
        period_end=existing_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            {
                "ref_kind": "pass_output",
                "pass_kind": "trend_synthesis",
                "pass_output_id": existing_trend.id,
            }
        ],
    )
    newer_start = existing_start + timedelta(days=1)
    newer_end = existing_end + timedelta(days=1)
    newer_trend_payload = trend_payload.model_copy(
        update={
            "period_start": newer_start.isoformat(),
            "period_end": newer_end.isoformat(),
            "title": "Newer trend without an Idea document",
        }
    )
    newer_trend = repository.create_pass_output(
        run_id="run-newer-backfill-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=newer_start,
        period_end=newer_end,
        payload=newer_trend_payload.model_dump(mode="json"),
    )
    assert newer_trend.id is not None
    newer_ideas = ideas_payload.model_copy(
        update={
            "period_start": newer_start.isoformat(),
            "period_end": newer_end.isoformat(),
            "title": "Newer backfilled ideas",
        }
    )
    repository.create_pass_output(
        run_id="run-newer-backfill-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=newer_start,
        period_end=newer_end,
        payload=newer_ideas.model_dump(mode="json"),
        input_refs=[
            {
                "ref_kind": "pass_output",
                "pass_kind": "trend_synthesis",
                "pass_output_id": newer_trend.id,
            }
        ],
    )

    candidates = translation_module._incremental_candidates(
        repository=repository,
        granularity="day",
        include={"ideas"},
        limit=1,
        source_language_code="en",
        all_history=True,
    )

    assert len(candidates) == 1
    assert candidates[0].period_start is not None
    assert candidates[0].period_start.replace(tzinfo=UTC) == newer_start


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
    assert "## 概览" in trend_note.read_text(encoding="utf-8")
    assert "## 摘要" in idea_note.read_text(encoding="utf-8")
    assert "提示词发布闸门" in idea_note.read_text(encoding="utf-8")
    assert (
        validate_presentation(
            json.loads(
                presentation_sidecar_path(note_path=trend_note).read_text(
                    encoding="utf-8"
                )
            )
        )
        == []
    )
    assert (
        validate_presentation(
            json.loads(
                presentation_sidecar_path(note_path=idea_note).read_text(
                    encoding="utf-8"
                )
            )
        )
        == []
    )


def test_materialize_omits_suppressed_windows_from_all_generated_surfaces(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _item_id, trend_doc_id, idea_doc_id, trend_payload, ideas_payload = (
        _seed_item_trend_and_idea(repository=repository)
    )
    _seed_suppressed_generation_windows(
        repository=repository,
        trend_payload=trend_payload,
        ideas_payload=ideas_payload,
    )
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
        source_hash="stale-trend-translation",
        payload=trend_payload.model_dump(mode="json"),
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        language_code="zh-CN",
        status="succeeded",
        source_hash="stale-ideas-translation",
        payload=ideas_payload.model_dump(mode="json"),
        diagnostics={},
        variant_role="translation",
    )

    output_dir = tmp_path / "outputs"
    vault_path = tmp_path / "vault"
    obsidian_trend_note = (
        vault_path
        / "Recoleta"
        / "Trends"
        / f"day--2026-03-02--trend--{trend_doc_id}.md"
    )
    obsidian_idea_note = vault_path / "Recoleta" / "Ideas" / "day--2026-03-02--ideas.md"
    for note_path in (obsidian_trend_note, obsidian_idea_note):
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text("stale projection\n", encoding="utf-8")
        presentation_sidecar_path(note_path=note_path).write_text(
            '{"stale": true}\n', encoding="utf-8"
        )

    pdf_calls: list[Path] = []

    def _unexpected_pdf_render(*, markdown_path: Path, **_kwargs: Any) -> None:
        pdf_calls.append(markdown_path)
        raise AssertionError("suppressed trends must not be rendered")

    monkeypatch.setattr(
        "recoleta.materialize.render_trend_note_pdf_result",
        _unexpected_pdf_render,
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(
            output_dir=output_dir,
            obsidian_vault_path=vault_path,
            obsidian_base_folder="Recoleta",
        ),
        generate_pdf=True,
        localization=localization,
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    assert not list((output_dir / "Trends").glob("*.md"))
    assert not list((output_dir / "Ideas").glob("*.md"))
    assert not list((output_dir / "Trends").glob("*.pdf"))
    assert not list((output_dir / "Localized" / "zh-cn" / "Trends").glob("*.md"))
    assert not list((output_dir / "Localized" / "zh-cn" / "Ideas").glob("*.md"))
    assert not obsidian_trend_note.exists()
    assert not obsidian_idea_note.exists()
    assert not presentation_sidecar_path(note_path=obsidian_trend_note).exists()
    assert not presentation_sidecar_path(note_path=obsidian_idea_note).exists()
    assert pdf_calls == []
    assert result.output.trend_pdf_failures_total == 0
    assert result.site_manifest_path is not None
    manifest = json.loads(result.site_manifest_path.read_text(encoding="utf-8"))
    assert manifest["trends_total"] == 0
    assert manifest["ideas_total"] == 0


def test_run_translation_creates_localized_outputs_for_all_surfaces(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "test/fake-model")
    monkeypatch.setenv("TRANSLATION_LLM_MODEL", "test/translation-stage-model")
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
    models_seen: list[str] = []

    def _fake_translate(*, request=None, **kwargs: Any) -> dict[str, Any]:
        normalized = translation_module.coerce_translate_structured_payload_request(
            request=request,
            legacy_kwargs=kwargs,
        )
        models_seen.append(normalized.model)
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

    monkeypatch.setattr(
        translation_module, "translate_structured_payload", _fake_translate
    )

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
    assert (
        repository.get_localized_output(
            source_kind="analysis",
            source_record_id=item_id,
            language_code="zh-CN",
        )
        is not None
    )
    assert (
        repository.get_localized_output(
            source_kind="trend_synthesis",
            source_record_id=trend_doc_id,
            language_code="zh-CN",
        )
        is not None
    )
    assert (
        repository.get_localized_output(
            source_kind="trend_ideas",
            source_record_id=idea_doc_id,
            language_code="zh-CN",
        )
        is not None
    )
    metric_names = {
        metric.name for metric in repository.list_metrics(run_id="run-translation")
    }
    assert "pipeline.translate.task_duration_ms_total" in metric_names
    assert "pipeline.translate.duration_ms" not in metric_names
    assert trend_payload.title == "Agent systems"
    assert ideas_payload.title == "Operator wedges"
    assert models_seen == ["test/translation-stage-model"] * 3

    models_seen.clear()
    rerun_result = translation_module.run_translation(
        repository=repository,
        settings=settings,
        include=["items"],
        limit=1,
        llm_model="test/translation-override",
        context_assist="direct",
        force=False,
        run_id="run-translation-override",
    )

    assert rerun_result.translated_total == 1
    assert models_seen == ["test/translation-override"]
