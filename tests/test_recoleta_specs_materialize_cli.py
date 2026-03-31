from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from types import SimpleNamespace

from bs4 import BeautifulSoup
import pytest
from sqlmodel import Session, select
from typer.testing import CliRunner

import recoleta.cli
import recoleta.materialize as materialize_module
from recoleta.materialize import MaterializeTargetSpec, materialize_outputs
from recoleta.models import Document, DocumentChunk, Item
from recoleta.passes.base import PassInputRef
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.publish.item_notes import resolve_item_note_path
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, build_empty_trend_payload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft


def _seed_materialize_fixture(
    *,
    repository: Repository,
    pass_output_id: int | None = None,
) -> tuple[int, Path]:
    published_at = datetime(2026, 3, 2, 12, tzinfo=UTC)
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="robometer-1",
        canonical_url="https://example.com/robometer",
        title="Robometer: Scaling General-Purpose Robotic Reward Models",
        authors=["Alice"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.save_analysis(
        item_id=item.id,
        result=AnalysisResult(
            model="test/materialize",
            provider="test",
            summary="## Summary\n\nReward models get a stronger comparison signal.\n",
            topics=["agents", "robotics"],
            relevance_score=0.95,
            novelty_score=0.44,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    repository.mark_item_published(item_id=item.id)
    persisted_item = repository.get_item(item_id=item.id)
    assert persisted_item is not None
    item_doc = repository.upsert_document_for_item(item=persisted_item)
    assert item_doc.id is not None

    payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
            "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
            "overview_md": (
                "## Overview\n\n"
                "Start with "
                "[Robometer](https://example.com/robometer).\n"
            ),
            "topics": ["agents", "robotics"],
            "clusters": [
                {
                    "name": "Reward models",
                    "description": (
                        "Follow "
                        "[Robometer](https://example.com/robometer)."
                    ),
                    "representative_chunks": [
                        {
                            "doc_id": item_doc.id,
                            "chunk_index": 0,
                        }
                    ],
                }
            ],
            "highlights": [],
        }
    )
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        payload=payload,
        pass_output_id=pass_output_id,
    )

    output_dir = Path("/tmp/placeholder")
    item_note_path = resolve_item_note_path(
        note_dir=output_dir / "Inbox",
        item_id=item.id,
        title=persisted_item.title,
        canonical_url=persisted_item.canonical_url,
        published_at=persisted_item.published_at,
    )
    return trend_doc_id, item_note_path


def test_materialize_outputs_backfills_item_notes_rerenders_trend_links_and_keeps_db_unchanged(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"

    with Session(repository.engine) as session:
        item_before = session.exec(select(Item)).one()
        meta_before = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.chunk_index == 1,
            )
        ).one()
        item_state_before = item_before.state
        meta_text_before = meta_before.text

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    trend_note_path = output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    assert result.site_manifest_path == output_dir / "site" / "manifest.json"
    assert item_note_path.exists()
    assert trend_note_path.exists()

    trend_markdown = trend_note_path.read_text(encoding="utf-8")
    assert (
        "## Overview\nStart with "
        f"[Robometer](../Inbox/{item_note_path.name})."
    ) in trend_markdown
    assert f"[Robometer](../Inbox/{item_note_path.name})" in trend_markdown
    assert "https://example.com/robometer" not in trend_markdown
    assert "#### Representative sources" in trend_markdown
    assert "Robometer: Scaling General-Purpose Robotic Reward Models" in trend_markdown
    assert f"(../Inbox/{item_note_path.name})" in trend_markdown

    trend_html = (
        output_dir
        / "site"
        / "trends"
        / f"day--2026-03-02--trend--{trend_doc_id}.html"
    ).read_text(encoding="utf-8")
    assert f"../items/{item_note_path.stem}.html" in trend_html
    assert "https://example.com/robometer" not in trend_html

    item_html = (
        output_dir / "site" / "items" / f"{item_note_path.stem}.html"
    ).read_text(encoding="utf-8")
    assert "Open original" in item_html
    assert "https://example.com/robometer" in item_html

    with Session(repository.engine) as session:
        item_after = session.exec(select(Item)).one()
        meta_after = session.exec(
            select(DocumentChunk).where(
                DocumentChunk.doc_id == trend_doc_id,
                DocumentChunk.chunk_index == 1,
            )
        ).one()
        assert item_after.state == item_state_before
        assert meta_after.text == meta_text_before


def test_materialize_outputs_renders_default_scope_items_without_legacy_stream_state_table(
    tmp_path: Path,
) -> None:
    """Regression: default-scope materialization should not depend on item_stream_states."""
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    trend_note_path = output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    assert result.site_manifest_path == output_dir / "site" / "manifest.json"
    assert item_note_path.exists()
    assert trend_note_path.exists()


def test_materialize_outputs_forwards_explicit_item_export_scope_to_site_export(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: site rebuilds during materialization must preserve the full item export override."""
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"
    captured: dict[str, object] = {}

    def _fake_export_trend_static_site(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        output_dir,
        default_language_code=None,
        item_export_scope="linked",
    ):
        captured.update(
            {
                "input_dir": input_dir,
                "output_dir": output_dir,
                "default_language_code": default_language_code,
                "item_export_scope": item_export_scope,
            }
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            '{"trends_total": 1, "topics_total": 2}\n',
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        materialize_module,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
        item_export_scope="all",
    )

    assert result.site_manifest_path == output_dir / "site" / "manifest.json"
    assert captured["item_export_scope"] == "all"


def test_default_target_spec_for_settings_uses_instance_output_roots(
    tmp_path: Path,
) -> None:
    fake_settings = SimpleNamespace(
        markdown_output_dir=tmp_path / "outputs",
        obsidian_vault_path=tmp_path / "vault",
        obsidian_base_folder="Recoleta",
    )

    target_spec = materialize_module.default_target_spec_for_settings(
        settings=fake_settings
    )

    assert target_spec.output_dir == tmp_path / "outputs"
    assert target_spec.obsidian_vault_path == tmp_path / "vault"
    assert target_spec.obsidian_base_folder == "Recoleta"


def test_materialize_outputs_preserves_trend_projection_provenance_in_note_frontmatter(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, _ = _seed_materialize_fixture(
        repository=repository,
        pass_output_id=17,
    )
    output_dir = tmp_path / "outputs"

    _ = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=None,
        site_output_dir=None,
    )

    trend_note_path = output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    note_text = trend_note_path.read_text(encoding="utf-8")
    assert "pass_output_id: 17" in note_text
    assert "pass_kind: trend_synthesis" in note_text


def test_materialize_outputs_removes_stale_managed_scope_files(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"
    stale_item_path = output_dir / "Inbox" / "stale-item.md"
    stale_trend_path = output_dir / "Trends" / "stale-trend.md"
    stale_idea_path = output_dir / "Ideas" / "stale-idea.md"
    stale_localized_path = (
        output_dir / "Localized" / "zh-cn" / "Inbox" / "stale-localized-item.md"
    )
    for path in (
        stale_item_path,
        stale_trend_path,
        stale_idea_path,
        stale_localized_path,
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("stale\n", encoding="utf-8")

    _ = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=None,
        site_output_dir=None,
    )

    assert not stale_item_path.exists()
    assert not stale_trend_path.exists()
    assert not stale_idea_path.exists()
    assert not stale_localized_path.exists()
    assert (output_dir / "Inbox" / placeholder_item_note_path.name).exists()
    assert (output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md").exists()


def test_materialize_outputs_cli_can_regenerate_pdfs_with_explicit_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, _ = _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"
    pdf_calls: list[Path] = []

    class _FakePrepared:
        renderer = "story"

    class _FakePdfResult:
        def __init__(self, path: Path) -> None:
            self.path = path
            self.prepared = _FakePrepared()

    def _fake_render_trend_note_pdf_result(*, markdown_path, **_: object):  # type: ignore[no-untyped-def]
        pdf_calls.append(markdown_path)
        pdf_path = markdown_path.with_suffix(".pdf")
        pdf_path.write_bytes(b"%PDF-1.7\n")
        return _FakePdfResult(pdf_path)

    monkeypatch.setattr(
        materialize_module,
        "render_trend_note_pdf_result",
        _fake_render_trend_note_pdf_result,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "outputs",
            "--db-path",
            str(repository.db_path),
            "--output-dir",
            str(output_dir),
            "--pdf",
        ],
    )

    assert result.exit_code == 0
    assert "repair outputs completed" in result.stdout
    assert len(pdf_calls) == 1
    assert pdf_calls[0].name == f"day--2026-03-02--trend--{trend_doc_id}.md"
    assert (output_dir / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.pdf").exists()


def test_repair_outputs_cli_forwards_explicit_item_export_scope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: repair outputs must forward the full item export override."""
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    calls: dict[str, object] = {}

    def _fake_materialize_outputs(**kwargs: object) -> materialize_module.MaterializeOutputsResult:
        calls.update(kwargs)
        output_dir = tmp_path / "outputs"
        site_dir = output_dir / "site"
        site_dir.mkdir(parents=True, exist_ok=True)
        return materialize_module.MaterializeOutputsResult(
            output=materialize_module.MaterializeOutputResult(
                output_dir=output_dir,
            ),
            site_manifest_path=site_dir / "manifest.json",
        )

    monkeypatch.setattr(
        materialize_module,
        "materialize_outputs",
        _fake_materialize_outputs,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "outputs",
            "--db-path",
            str(repository.db_path),
            "--output-dir",
            str(tmp_path / "outputs"),
            "--site",
            "--item-export-scope",
            "all",
        ],
    )

    assert result.exit_code == 0
    assert calls["item_export_scope"] == "all"


def test_materialize_outputs_cli_emits_json_summary(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "outputs",
            "--db-path",
            str(repository.db_path),
            "--output-dir",
            str(output_dir),
            "--site",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "repair outputs"
    assert payload["totals"]["items"] == 1
    assert payload["totals"]["trends"] == 1
    assert payload["site_manifest_path"] == str(output_dir / "site" / "manifest.json")
    assert payload["output"]["output_dir"] == str(output_dir)
    assert payload["output"]["trend_notes_total"] == 1


def test_stage_materialize_cli_forwards_explicit_item_export_scope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: stage materialize must forward the full item export override."""
    runner = CliRunner()
    calls: dict[str, object] = {}
    app_module = recoleta.cli._import_symbol("recoleta.cli.app")

    monkeypatch.setattr(
        app_module,
        "run_materialize_outputs_command",
        lambda **kwargs: calls.update(kwargs),
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "stage",
            "materialize",
            "--item-export-scope",
            "all",
        ],
    )

    assert result.exit_code == 0
    assert calls["item_export_scope"] == "all"


def test_materialize_outputs_cli_rejects_non_default_scope_in_instance_first_runtime(
    tmp_path: Path,
) -> None:
    """Regression: instance-first output repair must target the default scope only."""
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "outputs",
            "--db-path",
            str(repository.db_path),
            "--output-dir",
            str(output_dir),
            "--scope",
            "agents_lab",
        ],
    )

    assert result.exit_code == 2


def test_materialize_outputs_rebuilds_ideas_notes_from_pass_outputs_and_exports_site(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    with Session(repository.engine) as session:
        item_doc = session.exec(
            select(Document).where(Document.doc_type == "item").limit(1)
        ).one()
    assert item_doc.id is not None

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "## Overview\n\nAgent workflows are getting more production-ready.\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": [],
        }
    )
    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-trend-pass",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert trend_pass_output.id is not None

    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Verification-first agent rollout",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Use a prompt release gate before shipping changes.",
            "ideas": [
                {
                    "title": "Prompt CI gate",
                    "kind": "tooling_wedge",
                    "thesis": "Ship a prompt release gate before production rollout.",
                    "why_now": "Prompt changes now behave like deployable releases.",
                    "what_changed": "Agent teams now manage prompt/tool changes continuously.",
                    "user_or_job": "Platform engineers shipping agent changes.",
                    "evidence_refs": [
                        {
                            "doc_id": trend_doc_id,
                            "chunk_index": 0,
                            "reason": "Trend note captures the operational shift.",
                        },
                        {
                            "doc_id": item_doc.id,
                            "chunk_index": 0,
                            "reason": "Item note anchors the paper-level evidence.",
                        },
                    ],
                    "validation_next_step": "Replay 20 prompt changes through the gate.",
                    "time_horizon": "now",
                }
            ],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-ideas-pass",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    idea_note_path = output_dir / "Ideas" / "day--2026-03-02--ideas.md"
    assert idea_note_path.exists()
    assert result.site_manifest_path == output_dir / "site" / "manifest.json"

    idea_markdown = idea_note_path.read_text(encoding="utf-8")
    assert f"[Agent Systems](../Trends/day--2026-03-02--trend--{trend_doc_id}.md)" in idea_markdown
    assert f"[Robometer: Scaling General-Purpose Robotic Reward Models](../Inbox/{item_note_path.name})" in idea_markdown

    idea_html = (
        output_dir / "site" / "ideas" / "day--2026-03-02--ideas.html"
    ).read_text(encoding="utf-8")
    assert f"../trends/day--2026-03-02--trend--{trend_doc_id}.html" in idea_html
    assert f"../items/{item_note_path.stem}.html" in idea_html


def test_materialize_outputs_deduplicates_idea_evidence_by_document(
    tmp_path: Path,
) -> None:
    """Regression: ideas output should not expose duplicate article citations for different chunks."""

    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    with Session(repository.engine) as session:
        item_doc = session.exec(
            select(Document).where(Document.doc_type == "item").limit(1)
        ).one()
    assert item_doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(item_doc.id),
        chunk_index=1,
        kind="content",
        text_value="Verifier loops inspect long traces in the body chunk.",
        source_content_type="analysis_body",
    )

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "## Overview\n\nAgent workflows are getting more production-ready.\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": [],
        }
    )
    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-trend-pass-dedup",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert trend_pass_output.id is not None

    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Verification-first agent rollout",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Use a prompt release gate before shipping changes.",
            "ideas": [
                {
                    "title": "Prompt CI gate",
                    "kind": "tooling_wedge",
                    "thesis": "Ship a prompt release gate before production rollout.",
                    "why_now": "Prompt changes now behave like deployable releases.",
                    "what_changed": "Agent teams now manage prompt/tool changes continuously.",
                    "user_or_job": "Platform engineers shipping agent changes.",
                    "evidence_refs": [
                        {
                            "doc_id": item_doc.id,
                            "chunk_index": 0,
                            "reason": "The summary chunk anchors the paper-level evidence.",
                        },
                        {
                            "doc_id": item_doc.id,
                            "chunk_index": 1,
                            "reason": "The body chunk shows the verifier loop details.",
                        },
                    ],
                    "validation_next_step": "Replay 20 prompt changes through the gate.",
                    "time_horizon": "now",
                }
            ],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-ideas-pass-dedup",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    _ = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    idea_note_path = output_dir / "Ideas" / "day--2026-03-02--ideas.md"
    idea_markdown = idea_note_path.read_text(encoding="utf-8")
    item_link = (
        f"[Robometer: Scaling General-Purpose Robotic Reward Models]"
        f"(../Inbox/{item_note_path.name})"
    )
    assert idea_markdown.count(item_link) == 1
    assert (
        f"- {item_link}\n"
        "  - The summary chunk anchors the paper-level evidence.\n"
        "  - The body chunk shows the verifier loop details."
    ) in idea_markdown
    assert "The summary chunk anchors the paper-level evidence." in idea_markdown
    assert "The body chunk shows the verifier loop details." in idea_markdown
    assert "; The body chunk shows the verifier loop details." not in idea_markdown
    assert "(chunk 1)" not in idea_markdown

    idea_html = (
        output_dir / "site" / "ideas" / "day--2026-03-02--ideas.html"
    ).read_text(encoding="utf-8")
    soup = BeautifulSoup(idea_html, "html.parser")
    meta_panels = {
        label.get_text(" ", strip=True): value.get_text(" ", strip=True)
        for panel in soup.select(".meta-panel")
        for label in [panel.select_one(".meta-panel-label")]
        for value in [panel.select_one(".meta-panel-value")]
        if label is not None and value is not None
    }
    assert idea_html.count(f"../items/{item_note_path.stem}.html") == 1
    assert meta_panels.get("Evidence") == "1"
    assert "(chunk 1)" not in idea_html


def test_materialize_outputs_repairs_obsidian_notes_for_trends_and_ideas(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, placeholder_item_note_path = _seed_materialize_fixture(
        repository=repository
    )
    output_dir = tmp_path / "outputs"
    vault_path = tmp_path / "vault"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    with Session(repository.engine) as session:
        item_doc = session.exec(
            select(Document).where(Document.doc_type == "item").limit(1)
        ).one()
    assert item_doc.id is not None

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "## Overview\n\nAgent workflows are getting more production-ready.\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": [],
        }
    )
    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-trend-pass-obsidian",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert trend_pass_output.id is not None

    ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Verification-first agent rollout",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Use a prompt release gate before shipping changes.",
            "ideas": [
                {
                    "title": "Prompt CI gate",
                    "kind": "tooling_wedge",
                    "thesis": "Ship a prompt release gate before production rollout.",
                    "why_now": "Prompt changes now behave like deployable releases.",
                    "what_changed": "Agent teams now manage prompt/tool changes continuously.",
                    "user_or_job": "Platform engineers shipping agent changes.",
                    "evidence_refs": [
                        {
                            "doc_id": trend_doc_id,
                            "chunk_index": 0,
                            "reason": "Trend note captures the operational shift.",
                        },
                        {
                            "doc_id": item_doc.id,
                            "chunk_index": 0,
                            "reason": "Item note anchors the paper-level evidence.",
                        },
                    ],
                    "validation_next_step": "Replay 20 prompt changes through the gate.",
                    "time_horizon": "now",
                }
            ],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-ideas-pass-obsidian",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=ideas_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(
            output_dir=output_dir,
            obsidian_vault_path=vault_path,
            obsidian_base_folder="Recoleta",
        ),
    )

    item_note_path = output_dir / "Inbox" / placeholder_item_note_path.name
    obsidian_item_note = vault_path / "Recoleta" / "Inbox" / item_note_path.name
    obsidian_trend_note = (
        vault_path / "Recoleta" / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md"
    )
    obsidian_idea_note = (
        vault_path / "Recoleta" / "Ideas" / "day--2026-03-02--ideas.md"
    )

    assert obsidian_item_note.exists()
    assert obsidian_trend_note.exists()
    assert obsidian_idea_note.exists()
    assert result.output.obsidian_notes_total == 3
    assert result.output.obsidian_failures_total == 0

    idea_markdown = obsidian_idea_note.read_text(encoding="utf-8")
    assert f"[Agent Systems](../Trends/day--2026-03-02--trend--{trend_doc_id}.md)" in idea_markdown
    assert f"[Robometer: Scaling General-Purpose Robotic Reward Models](../Inbox/{item_note_path.name})" in idea_markdown


def test_materialize_outputs_prefers_latest_ideas_pass_output_even_when_suppressed(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    _trend_doc_id, _ = _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)

    trend_payload = TrendPayload.model_validate(
        {
            "title": "Agent Systems",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "overview_md": "## Overview\n\nAgent workflows are getting more production-ready.\n",
            "topics": ["agents", "robotics"],
            "clusters": [],
            "highlights": [],
        }
    )
    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-trend-pass-latest-window",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=trend_payload.model_dump(mode="json"),
    )
    assert trend_pass_output.id is not None

    older_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Older succeeded ideas",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "An older ideas run emitted one opportunity.",
            "ideas": [
                {
                    "title": "Stale idea that should disappear",
                    "kind": "tooling_wedge",
                    "thesis": "This should not survive materialization.",
                    "why_now": "It came from an older pass output.",
                    "what_changed": "Nothing relevant anymore.",
                    "user_or_job": "Nobody after suppression.",
                    "evidence_refs": [],
                    "validation_next_step": "Do not run this.",
                    "time_horizon": "now",
                }
            ],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-ideas-pass-older-success",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=older_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    suppressed_payload = TrendIdeasPayload.model_validate(
        {
            "title": "Latest suppressed ideas",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "Evidence is too thin for a durable opportunity brief.",
            "ideas": [],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-ideas-pass-latest-suppressed",
        pass_kind="trend_ideas",
        status="suppressed",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=suppressed_payload.model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
    )

    idea_note_path = output_dir / "Ideas" / "day--2026-03-02--ideas.md"
    note_text = idea_note_path.read_text(encoding="utf-8")

    assert result.output.ideas_outputs_total == 1
    assert "status: suppressed" in note_text
    assert "# Latest suppressed ideas" in note_text
    assert "Evidence is too thin for a durable opportunity brief." in note_text
    assert "Stale idea that should disappear" not in note_text


def test_materialize_outputs_skips_empty_corpus_ideas_and_site_excludes_empty_trends(
    tmp_path: Path,
) -> None:
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    output_dir = tmp_path / "outputs"
    period_start = datetime(2026, 3, 13, tzinfo=UTC)
    period_end = datetime(2026, 3, 14, tzinfo=UTC)

    empty_trend_payload = build_empty_trend_payload(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        output_language="Chinese (Simplified)",
    )
    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-empty-trend-pass",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=empty_trend_payload.model_dump(mode="json"),
        diagnostics={"empty_corpus": True},
    )
    assert trend_pass_output.id is not None
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=empty_trend_payload,
        pass_output_id=int(trend_pass_output.id),
    )

    empty_ideas_payload = TrendIdeasPayload.model_validate(
        {
            "title": "本期暂无可发布研究趋势",
            "granularity": "day",
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "summary_md": "该周期没有可用文档，因此不输出机会想法。",
            "ideas": [],
        }
    )
    repository.create_pass_output(
        run_id="run-materialize-empty-ideas-pass",
        pass_kind="trend_ideas",
        status="suppressed",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=empty_ideas_payload.model_dump(mode="json"),
        diagnostics={"empty_corpus": True},
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    result = materialize_outputs(
        repository=repository,
        target_spec=MaterializeTargetSpec(output_dir=output_dir),
        site_input_dir=output_dir,
        site_output_dir=output_dir / "site",
    )

    trend_note_path = output_dir / "Trends" / f"day--2026-03-13--trend--{trend_doc_id}.md"
    idea_note_path = output_dir / "Ideas" / "day--2026-03-13--ideas.md"
    trend_note_text = trend_note_path.read_text(encoding="utf-8")
    assert result.site_manifest_path is not None
    manifest = json.loads(result.site_manifest_path.read_text(encoding="utf-8"))

    assert "site_exclude: true" in trend_note_text
    assert not idea_note_path.exists()
    assert manifest["trends_total"] == 0
    assert manifest["ideas_total"] == 0
    assert manifest["files"]["trend_pages"] == []
    assert manifest["files"]["idea_pages"] == []
    assert not (output_dir / "site" / "trends" / f"{trend_note_path.stem}.html").exists()
    assert not (output_dir / "site" / "ideas" / "day--2026-03-13--ideas.html").exists()


def test_materialize_outputs_cli_reports_obsidian_repairs_when_settings_are_available(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()
    trend_doc_id, _ = _seed_materialize_fixture(repository=repository)
    output_dir = tmp_path / "outputs"
    vault_path = tmp_path / "vault"
    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    with Session(repository.engine) as session:
        item_doc = session.exec(
            select(Document).where(Document.doc_type == "item").limit(1)
        ).one()
    assert item_doc.id is not None

    trend_pass_output = repository.create_pass_output(
        run_id="run-materialize-cli-trend-pass",
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload.model_validate(
            {
                "title": "Agent Systems",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "overview_md": "## Overview\n\nAgent workflows are getting more production-ready.\n",
                "topics": ["agents", "robotics"],
                "clusters": [],
                "highlights": [],
            }
        ).model_dump(mode="json"),
    )
    assert trend_pass_output.id is not None
    repository.create_pass_output(
        run_id="run-materialize-cli-ideas-pass",
        pass_kind="trend_ideas",
        status="succeeded",
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendIdeasPayload.model_validate(
            {
                "title": "Verification-first agent rollout",
                "granularity": "day",
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
                "summary_md": "Use a prompt release gate before shipping changes.",
                "ideas": [
                    {
                        "title": "Prompt CI gate",
                        "kind": "tooling_wedge",
                        "thesis": "Ship a prompt release gate before production rollout.",
                        "why_now": "Prompt changes now behave like deployable releases.",
                        "what_changed": "Agent teams now manage prompt/tool changes continuously.",
                        "user_or_job": "Platform engineers shipping agent changes.",
                        "evidence_refs": [
                            {
                                "doc_id": trend_doc_id,
                                "chunk_index": 0,
                                "reason": "Trend note captures the operational shift.",
                            },
                            {
                                "doc_id": item_doc.id,
                                "chunk_index": 0,
                                "reason": "Item note anchors the paper-level evidence.",
                            },
                        ],
                        "validation_next_step": "Replay 20 prompt changes through the gate.",
                        "time_horizon": "now",
                    }
                ],
            }
        ).model_dump(mode="json"),
        input_refs=[
            PassInputRef(
                ref_kind="pass_output",
                pass_kind="trend_synthesis",
                granularity="day",
                period_start=period_start.isoformat(),
                period_end=period_end.isoformat(),
                pass_output_id=trend_pass_output.id,
            ).model_dump(mode="json")
        ],
    )

    config_path = tmp_path / "recoleta.yml"
    config_path.write_text(
        "\n".join(
                [
                    f"recoleta_db_path: {repository.db_path}",
                    f"markdown_output_dir: {output_dir}",
                    f"obsidian_vault_path: {vault_path}",
                "obsidian_base_folder: Recoleta",
                "publish_targets: [markdown, obsidian]",
                "llm_model: test/fake-model",
                "llm_output_language: Chinese (Simplified)",
                "",
            ]
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "repair",
            "outputs",
            "--config-path",
            str(config_path),
            "--output-dir",
            str(output_dir),
        ],
    )

    assert result.exit_code == 0
    assert "repair outputs completed" in result.stdout
    assert "obsidian=3" in result.stdout
    assert (vault_path / "Recoleta" / "Ideas" / "day--2026-03-02--ideas.md").exists()
