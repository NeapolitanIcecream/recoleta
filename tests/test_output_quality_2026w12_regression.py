from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
from typing import Any

import pytest

from recoleta.config import LocalizationConfig
from recoleta.materialize import MaterializeTargetSpec, materialize_outputs
from recoleta.passes.base import PassInputRef
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.presentation import presentation_sidecar_path, validate_presentation
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft

FIXTURE_ROOT = Path(__file__).parent / "fixtures" / "output_quality" / "2026w12"
SCOPE_LABELS = {
    "embodied_ai": "具身智能",
    "software_intelligence": "软件智能",
}


def _fixture_path(*, scope: str, surface_kind: str) -> Path:
    return FIXTURE_ROOT / f"{scope}-{surface_kind}.json"


def _load_fixture(*, scope: str, surface_kind: str) -> dict[str, Any]:
    return json.loads(
        _fixture_path(scope=scope, surface_kind=surface_kind).read_text(
            encoding="utf-8"
        )
    )


def _rewrite_legacy_doc_ids(value: Any, *, mapping: dict[int, int]) -> Any:
    if isinstance(value, dict):
        rewritten = {
            key: _rewrite_legacy_doc_ids(child, mapping=mapping)
            for key, child in value.items()
        }
        if "doc_id" in rewritten:
            raw_doc_id = rewritten.get("doc_id")
            if raw_doc_id is None:
                normalized_doc_id = None
            else:
                try:
                    normalized_doc_id = int(raw_doc_id)
                except Exception:
                    normalized_doc_id = None
            if normalized_doc_id is not None and normalized_doc_id in mapping:
                rewritten["doc_id"] = mapping[normalized_doc_id]
        return rewritten
    if isinstance(value, list):
        return [_rewrite_legacy_doc_ids(item, mapping=mapping) for item in value]
    return value


def _parse_iso_datetime(value: str) -> datetime:
    return datetime.fromisoformat(str(value))


def _seed_source_documents(
    *,
    repository: Repository,
    scope: str,
    source_documents: list[dict[str, Any]],
    topics: list[str],
) -> dict[int, int]:
    doc_id_by_legacy_doc_id: dict[int, int] = {}
    for source_document in source_documents:
        legacy_doc_id = int(source_document["legacy_doc_id"])
        published_at = _parse_iso_datetime(str(source_document["published_at"]))
        draft = ItemDraft.from_values(
            source=str(source_document["source"] or "rss"),
            source_item_id=f"{scope}-{legacy_doc_id}",
            canonical_url=str(source_document["canonical_url"] or ""),
            title=str(source_document["title"] or ""),
            authors=[
                str(author).strip()
                for author in list(source_document.get("authors") or [])
                if str(author).strip()
            ],
            published_at=published_at,
        )
        item, _ = repository.upsert_item(draft)
        assert item.id is not None
        repository.save_analysis(
            item_id=int(item.id),
            result=AnalysisResult(
                model="test/output-quality",
                provider="test",
                summary=(
                    "## Summary\n\n"
                    f"{str(source_document['title']).strip()} anchors the W12 regression fixture.\n"
                ),
                topics=list(topics[:3] or ["general"]),
                relevance_score=0.93,
                novelty_score=0.41,
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
            text_value=f"W12 fixture summary for {persisted_item.title}.",
            source_content_type="analysis_summary",
        )
        repository.upsert_content(
            item_id=int(item.id),
            content_type="html_maintext",
            text=f"W12 fixture source body for {persisted_item.title}.",
        )
        doc_id_by_legacy_doc_id[legacy_doc_id] = int(item_doc.id)
    return doc_id_by_legacy_doc_id


def _seed_history_documents(
    *,
    repository: Repository,
    history_documents: list[dict[str, Any]],
    granularity: str,
    topics: list[str],
) -> None:
    for history_document in history_documents:
        period_start = _parse_iso_datetime(str(history_document["period_start"]))
        period_end = _parse_iso_datetime(str(history_document["period_end"]))
        payload = TrendPayload.model_validate(
            {
                "title": history_document["title"],
                "granularity": granularity,
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": f"Historical reference for {history_document['title']}.",
                "topics": list(topics[:3]),
                "clusters": [],
                "highlights": [],
                "evolution": None,
            }
        )
        persist_trend_payload(
            repository=repository,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            payload=payload,
        )


def _persist_ideas_document(
    *,
    repository: Repository,
    payload: TrendIdeasPayload,
    granularity: str,
    period_start: datetime,
    period_end: datetime,
) -> int:
    idea_doc = repository.upsert_document_for_idea(
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
        title=str(payload.title or "").strip() or "Ideas",
    )
    assert idea_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=0,
        kind="summary",
        text_value=str(payload.summary_md or "").strip() or "(empty)",
        source_content_type="trend_ideas_summary",
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(payload.model_dump(mode="json"), ensure_ascii=False),
        source_content_type="trend_ideas_payload_json",
    )
    return int(idea_doc.id)


def _seed_scope_from_w12_fixtures(
    *,
    repository: Repository,
    scope: str,
) -> tuple[dict[str, Any], dict[str, Any], int, int]:
    trend_fixture = _load_fixture(scope=scope, surface_kind="trend")
    ideas_fixture = _load_fixture(scope=scope, surface_kind="ideas")
    combined_sources = {
        int(source_document["legacy_doc_id"]): source_document
        for source_document in [
            *list(trend_fixture.get("source_documents") or []),
            *list(ideas_fixture.get("source_documents") or []),
        ]
    }
    topics = list(trend_fixture["canonical_payload"].get("topics") or [])
    doc_id_mapping = _seed_source_documents(
        repository=repository,
        scope=scope,
        source_documents=list(combined_sources.values()),
        topics=topics,
    )
    _seed_history_documents(
        repository=repository,
        history_documents=list(trend_fixture.get("history_documents") or []),
        granularity=str(trend_fixture["canonical_payload"]["granularity"]),
        topics=topics,
    )

    rewritten_trend_payload = TrendPayload.model_validate(
        _rewrite_legacy_doc_ids(
            deepcopy(trend_fixture["canonical_payload"]),
            mapping=doc_id_mapping,
        )
    )
    period_start = _parse_iso_datetime(str(rewritten_trend_payload.period_start))
    period_end = _parse_iso_datetime(str(rewritten_trend_payload.period_end))
    trend_row = repository.create_pass_output(
        run_id=f"run-{scope}-w12-trend",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity=rewritten_trend_payload.granularity,
        period_start=period_start,
        period_end=period_end,
        payload=rewritten_trend_payload.model_dump(mode="json"),
    )
    assert trend_row.id is not None
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity=rewritten_trend_payload.granularity,
        period_start=period_start,
        period_end=period_end,
        payload=rewritten_trend_payload,
        pass_output_id=int(trend_row.id),
    )

    rewritten_ideas_payload = TrendIdeasPayload.model_validate(
        _rewrite_legacy_doc_ids(
            deepcopy(ideas_fixture["canonical_payload"]),
            mapping=doc_id_mapping,
        )
    )
    ideas_row = repository.create_pass_output(
        run_id=f"run-{scope}-w12-ideas",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity=rewritten_ideas_payload.granularity,
        period_start=period_start,
        period_end=period_end,
        payload=rewritten_ideas_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity=rewritten_trend_payload.granularity,
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=int(trend_row.id),
            ).model_dump(mode="json")
        ],
    )
    assert ideas_row.id is not None
    idea_doc_id = _persist_ideas_document(
        repository=repository,
        payload=rewritten_ideas_payload,
        granularity=rewritten_ideas_payload.granularity,
        period_start=period_start,
        period_end=period_end,
    )
    return trend_fixture, ideas_fixture, int(trend_doc_id), int(idea_doc_id)


def _localized_trend_payload(
    payload: dict[str, Any],
    *,
    scope: str,
) -> dict[str, Any]:
    localized = deepcopy(payload)
    scope_label = SCOPE_LABELS[scope]
    localized["title"] = f"{scope_label} W12 本地化趋势"
    localized["overview_md"] = f"{scope_label} W12 本地化趋势概览。"
    localized["highlights"] = [
        f"{scope_label} 本地化亮点 {index}。"
        for index, _ in enumerate(localized.get("highlights") or [None], start=1)
    ]
    for index, cluster in enumerate(localized.get("clusters") or [], start=1):
        cluster["name"] = f"{scope_label} 主题 {index}"
        cluster["description"] = f"{scope_label} 本地化聚类说明 {index}。"
    evolution = localized.get("evolution")
    if isinstance(evolution, dict):
        evolution["summary_md"] = f"{scope_label} 本地化变化摘要。"
        for index, signal in enumerate(evolution.get("signals") or [], start=1):
            signal["theme"] = f"{scope_label} 变化 {index}"
            signal["summary"] = f"{scope_label} 本地化变化说明 {index}。"
    return localized


def _localized_ideas_payload(
    payload: dict[str, Any],
    *,
    scope: str,
) -> dict[str, Any]:
    localized = deepcopy(payload)
    scope_label = SCOPE_LABELS[scope]
    localized["title"] = f"{scope_label} W12 本地化机会"
    localized["summary_md"] = f"{scope_label} W12 本地化机会摘要。"
    for index, idea in enumerate(localized.get("ideas") or [], start=1):
        idea["title"] = f"{scope_label} 机会 {index}"
        idea["user_or_job"] = f"{scope_label} 角色 {index}"
        idea["thesis"] = f"{scope_label} 本地化判断 {index}。"
        idea["why_now"] = f"{scope_label} 本地化为什么是现在 {index}。"
        idea["what_changed"] = f"{scope_label} 本地化变化说明 {index}。"
        idea["validation_next_step"] = f"{scope_label} 本地化验证步骤 {index}。"
        if "anti_thesis" in idea:
            idea["anti_thesis"] = f"{scope_label} 本地化反论点 {index}。"
    return localized


@pytest.mark.parametrize("scope", ["embodied_ai", "software_intelligence"])
def test_materialize_outputs_replays_w12_output_quality_regressions(
    scope: str,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / f"{scope}.db")
    repository.init_schema()
    trend_fixture, ideas_fixture, trend_doc_id, _idea_doc_id = (
        _seed_scope_from_w12_fixtures(
            repository=repository,
            scope=scope,
        )
    )
    output_dir = tmp_path / scope / "outputs"

    assert "Kind:" in ideas_fixture["legacy_excerpt"]
    assert "Time horizon:" in ideas_fixture["legacy_excerpt"]
    assert "User/job:" in ideas_fixture["legacy_excerpt"]
    if scope == "embodied_ai":
        assert "Prev_1" in trend_fixture["legacy_excerpt"]

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    assert result.site_manifest_path is not None

    trend_note = output_dir / "Trends" / f"week--2026-W12--trend--{trend_doc_id}.md"
    idea_note = output_dir / "Ideas" / "week--2026-W12--ideas.md"
    trend_sidecar_path = presentation_sidecar_path(note_path=trend_note)
    idea_sidecar_path = presentation_sidecar_path(note_path=idea_note)
    trend_text = trend_note.read_text(encoding="utf-8")
    idea_text = idea_note.read_text(encoding="utf-8")
    trend_sidecar = json.loads(trend_sidecar_path.read_text(encoding="utf-8"))
    idea_sidecar = json.loads(idea_sidecar_path.read_text(encoding="utf-8"))
    trend_html = (output_dir / "site" / "trends" / f"{trend_note.stem}.html").read_text(
        encoding="utf-8"
    )
    idea_html = (output_dir / "site" / "ideas" / f"{idea_note.stem}.html").read_text(
        encoding="utf-8"
    )

    assert trend_sidecar["presentation_schema_version"] == 2
    assert idea_sidecar["presentation_schema_version"] == 2
    assert validate_presentation(trend_sidecar) == []
    assert validate_presentation(idea_sidecar) == []

    assert "Prev_1" not in trend_text
    assert "Kind:" not in idea_text
    assert "Time horizon:" not in idea_text
    assert "User/job:" not in idea_text
    assert "raw enum" not in idea_text.lower()

    assert 1 <= len(trend_sidecar["content"]["ranked_shifts"]) <= 3
    assert [
        shift["rank"] for shift in trend_sidecar["content"]["ranked_shifts"]
    ] == list(range(1, len(trend_sidecar["content"]["ranked_shifts"]) + 1))
    assert [
        opportunity["tier"] for opportunity in idea_sidecar["content"]["opportunities"]
    ] == [
        "best_bet",
        "alternate",
        "alternate",
    ]
    assert len(idea_sidecar["content"]["opportunities"]) == 3

    assert "### Best bet:" in idea_text
    assert idea_text.count("\n### ") == 3
    assert "#### Evidence" in idea_text
    assert (
        "Shared semantic state layer for indoor robot and IoT coordination"
        not in idea_text
    )
    assert "Bug-witness generation workflow for autonomous debugging" not in idea_text

    assert trend_html.count("detail-shift-card") == len(
        trend_sidecar["content"]["ranked_shifts"]
    )
    assert idea_html.count("idea-opportunity-card") == 3
    assert "Kind:" not in idea_html
    assert "Time horizon:" not in idea_html
    assert "User/job:" not in idea_html


@pytest.mark.parametrize("scope", ["embodied_ai", "software_intelligence"])
def test_materialize_outputs_repair_w12_sidecars_and_localized_reprojections(
    scope: str,
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / f"{scope}.db")
    repository.init_schema()
    trend_fixture, ideas_fixture, trend_doc_id, idea_doc_id = (
        _seed_scope_from_w12_fixtures(
            repository=repository,
            scope=scope,
        )
    )
    output_dir = tmp_path / scope / "outputs"
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
        source_hash=f"{scope}-trend-zh",
        payload=_localized_trend_payload(
            trend_fixture["canonical_payload"],
            scope=scope,
        ),
        diagnostics={},
        variant_role="translation",
    )
    repository.upsert_localized_output(
        source_kind="trend_ideas",
        source_record_id=idea_doc_id,
        language_code="zh-CN",
        status="succeeded",
        source_hash=f"{scope}-ideas-zh",
        payload=_localized_ideas_payload(
            ideas_fixture["canonical_payload"],
            scope=scope,
        ),
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
    trend_note = zh_root / "Trends" / f"week--2026-W12--trend--{trend_doc_id}.md"
    idea_note = zh_root / "Ideas" / "week--2026-W12--ideas.md"
    trend_sidecar_path = presentation_sidecar_path(note_path=trend_note)
    idea_sidecar_path = presentation_sidecar_path(note_path=idea_note)

    trend_text = trend_note.read_text(encoding="utf-8")
    idea_text = idea_note.read_text(encoding="utf-8")
    assert "## 概览" in trend_text
    assert "## Overview" not in trend_text
    assert "## 摘要" in idea_text
    assert "## 机会" in idea_text
    assert "Kind:" not in idea_text
    assert "Time horizon:" not in idea_text
    assert "User/job:" not in idea_text

    zh_trend_html = (
        output_dir / "site" / "zh-cn" / "trends" / f"{trend_note.stem}.html"
    ).read_text(encoding="utf-8")
    zh_idea_html = (
        output_dir / "site" / "zh-cn" / "ideas" / f"{idea_note.stem}.html"
    ).read_text(encoding="utf-8")
    assert ">Overview<" in zh_trend_html
    assert ">Top shifts<" in zh_trend_html
    assert ">Summary<" in zh_idea_html
    assert ">Opportunities<" in zh_idea_html

    trend_sidecar_path.unlink()
    idea_sidecar_path.write_text('{"stale": true}\n', encoding="utf-8")
    presentation_sidecar_path(
        note_path=output_dir / "Trends" / f"week--2026-W12--trend--{trend_doc_id}.md"
    ).write_text('{"broken": true}\n', encoding="utf-8")
    presentation_sidecar_path(
        note_path=output_dir / "Ideas" / "week--2026-W12--ideas.md"
    ).unlink()

    _ = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        localization=localization,
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    repaired_paths = [
        presentation_sidecar_path(
            note_path=output_dir
            / "Trends"
            / f"week--2026-W12--trend--{trend_doc_id}.md"
        ),
        presentation_sidecar_path(
            note_path=output_dir / "Ideas" / "week--2026-W12--ideas.md"
        ),
        trend_sidecar_path,
        idea_sidecar_path,
    ]
    for repaired_path in repaired_paths:
        payload = json.loads(repaired_path.read_text(encoding="utf-8"))
        assert payload["presentation_schema_version"] == 2
        assert validate_presentation(payload) == []
