from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

from typer.testing import CliRunner

import recoleta.cli
from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.storage import Repository
from recoleta.trends import TrendPayload, persist_trend_payload
from recoleta.types import AnalysisResult, ItemDraft


def _configure_localization_env(monkeypatch, root: Path, db_path: Path) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(db_path))
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(root / "notes"))
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


def _write_empty_site_manifest(site_root: Path) -> None:
    site_root.mkdir(parents=True, exist_ok=True)
    (site_root / "manifest.json").write_text(
        json.dumps(
            {
                "languages": ["en", "zh-cn"],
                "language_codes": {"en": "en", "zh-cn": "zh-CN"},
                "default_language_code": "en",
                "files": {
                    "by_language": {
                        "en": {
                            "trend_pages": [],
                            "idea_pages": [],
                            "item_pages": [],
                        },
                        "zh-cn": {
                            "trend_pages": [],
                            "idea_pages": [],
                            "item_pages": [],
                        },
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_site_link_map(
    site_root: Path, *, recorded_site_output_dir: Path | None = None
) -> None:
    artifact_path = site_root.parent / f".{site_root.name}-email-links.json"
    artifact_path.write_text(
        json.dumps(
            {
                "site_output_dir": str(recorded_site_output_dir or site_root),
                "pages_by_source_markdown": {},
                "topic_pages_by_language": {},
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def _seed_localizable_surfaces(
    *,
    repository: Repository,
) -> tuple[int, int, int]:
    published_at = datetime(2026, 3, 2, 12, tzinfo=UTC)
    item, _ = repository.upsert_item(
        ItemDraft.from_values(
            source="rss",
            source_item_id="localization-audit-item",
            canonical_url="https://example.com/localization-audit-item",
            title="Localization audit item",
            authors=["Alice"],
            published_at=published_at,
        )
    )
    assert item.id is not None
    analysis = repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="openai/gpt-5.4",
            provider="openai",
            summary="English canonical item summary.",
            topics=["agents"],
            relevance_score=0.8,
            novelty_score=0.2,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    assert analysis.id is not None

    period_start = datetime(2026, 3, 2, tzinfo=UTC)
    period_end = datetime(2026, 3, 3, tzinfo=UTC)
    trend_doc_id = persist_trend_payload(
        repository=repository,
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        payload=TrendPayload(
            title="Localization audit trend",
            granularity="day",
            period_start=period_start.isoformat(),
            period_end=period_end.isoformat(),
            overview_md="English canonical trend overview.",
            topics=["agents"],
            clusters=[],
        ),
    )

    idea_doc = repository.upsert_document_for_idea(
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        title="Localization audit ideas",
    )
    assert idea_doc.id is not None
    ideas_payload = TrendIdeasPayload(
        title="Localization audit ideas",
        granularity="day",
        period_start=period_start.isoformat(),
        period_end=period_end.isoformat(),
        summary_md="English canonical idea summary.",
        ideas=[],
    )
    repository.upsert_document_chunk(
        doc_id=int(idea_doc.id),
        chunk_index=1,
        kind="meta",
        text_value=json.dumps(ideas_payload.model_dump(mode="json")),
        source_content_type="trend_ideas_payload_json",
    )
    return int(analysis.id), int(trend_doc_id), int(idea_doc.id)


def test_inspect_localization_json_reports_storage_coverage(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()
    analysis_id, _trend_doc_id, _idea_doc_id = _seed_localizable_surfaces(
        repository=repository
    )
    repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=analysis_id,
        language_code="zh-CN",
        status="succeeded",
        source_hash="analysis-zh",
        payload={"summary": "中文摘要。"},
        diagnostics={},
    )

    result = runner.invoke(recoleta.cli.app, ["inspect", "localization", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["audit_status"] == "warning"
    assert payload["localization"]["source_language_code"] == "en"
    assert payload["expected_target_languages"] == ["zh-CN"]
    assert payload["surfaces"]["items"]["canonical_total"] == 1
    assert payload["surfaces"]["items"]["languages"]["zh-CN"] == {
        "stored_total": 1,
        "succeeded_total": 1,
        "missing_total": 0,
        "orphan_total": 0,
    }
    assert payload["surfaces"]["trends"]["languages"]["zh-CN"]["missing_total"] == 1
    assert payload["surfaces"]["ideas"]["languages"]["zh-CN"]["missing_total"] == 1
    assert payload["issue_counts"]["missing_localized_output"] == 2
    assert {
        sample["surface"] for sample in payload["issue_samples"]["missing_localized_output"]
    } == {"trends", "ideas"}


def test_inspect_localization_json_warns_when_requested_artifacts_are_missing(
    configured_env: Path,
    monkeypatch,
) -> None:
    """Regression: missing requested artifact checks previously left audit_status ok."""
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "inspect",
            "localization",
            "--materialized-output-dir",
            str(configured_env / "missing-notes"),
            "--site-output-dir",
            str(configured_env / "missing-site"),
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["audit_status"] == "warning"
    assert payload["materialized"]["status"] == "missing"
    assert payload["materialized"]["reason"] == "materialized_output_dir_missing"
    assert payload["site"]["status"] == "missing"
    assert payload["site"]["reason"] == "site_manifest_missing"
    assert payload["issue_counts"]["materialized_output_dir_missing"] == 1
    assert payload["issue_counts"]["site_manifest_missing"] == 1


def test_inspect_localization_json_reports_unexpected_language_orphans(
    configured_env: Path,
    monkeypatch,
) -> None:
    """Regression: deconfigured-language orphans counted in storage without issues."""
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()
    repository.upsert_localized_output(
        source_kind="analysis",
        source_record_id=9999,
        language_code="fr",
        status="succeeded",
        source_hash="analysis-fr",
        payload={"summary": "Résumé orphelin."},
        diagnostics={},
    )
    notes_root = configured_env / "notes"
    notes_root.mkdir(parents=True)
    site_root = notes_root / "site"
    _write_empty_site_manifest(site_root)
    _write_site_link_map(site_root)

    result = runner.invoke(recoleta.cli.app, ["inspect", "localization", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["audit_status"] == "warning"
    assert payload["expected_target_languages"] == ["zh-CN"]
    assert payload["storage"]["orphan_total"] == 1
    assert payload["issue_counts"]["orphan_localized_output"] == 1
    assert payload["issue_samples"]["orphan_localized_output"] == [
        {
            "surface": "items",
            "source_kind": "analysis",
            "source_record_id": 9999,
            "language_code": "fr",
        }
    ]


def test_inspect_localization_json_orders_capped_storage_issue_samples(
    configured_env: Path,
    monkeypatch,
) -> None:
    """Regression: capped storage samples previously followed SQLite scan order."""
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()
    orphan_rows = [
        ("trend_synthesis", 20, "zh-CN"),
        ("analysis", 30, "fr"),
        ("analysis", 10, "ja"),
        ("analysis", 10, "de"),
        ("trend_ideas", 5, "es"),
    ]
    unknown_rows = [
        ("zz_unknown", 30, "fr"),
        ("aa_unknown", 40, "ja"),
        ("aa_unknown", 10, "es"),
        ("aa_unknown", 10, "de"),
    ]
    for index, (source_kind, source_record_id, language_code) in enumerate(
        [*orphan_rows, *unknown_rows],
        start=1,
    ):
        repository.upsert_localized_output(
            source_kind=source_kind,
            source_record_id=source_record_id,
            language_code=language_code,
            status="succeeded",
            source_hash=f"localized-storage-sample-{index}",
            payload={"summary": "localized sample"},
            diagnostics={},
        )
    notes_root = configured_env / "notes"
    notes_root.mkdir(parents=True)
    site_root = notes_root / "site"
    _write_empty_site_manifest(site_root)
    _write_site_link_map(site_root)

    def run_payload() -> dict[str, object]:
        result = runner.invoke(
            recoleta.cli.app,
            ["inspect", "localization", "--sample-limit", "3", "--json"],
        )
        assert result.exit_code == 0
        return json.loads(result.stdout)

    first_payload = run_payload()
    second_payload = run_payload()

    assert first_payload["issue_counts"]["orphan_localized_output"] == len(orphan_rows)
    assert first_payload["issue_counts"]["unknown_localized_source_kind"] == len(
        unknown_rows
    )
    assert first_payload["issue_samples"]["orphan_localized_output"] == second_payload[
        "issue_samples"
    ]["orphan_localized_output"]
    assert first_payload["issue_samples"][
        "unknown_localized_source_kind"
    ] == second_payload["issue_samples"]["unknown_localized_source_kind"]
    assert first_payload["issue_samples"]["orphan_localized_output"] == [
        {
            "surface": "items",
            "source_kind": "analysis",
            "source_record_id": 10,
            "language_code": "de",
        },
        {
            "surface": "items",
            "source_kind": "analysis",
            "source_record_id": 10,
            "language_code": "ja",
        },
        {
            "surface": "items",
            "source_kind": "analysis",
            "source_record_id": 30,
            "language_code": "fr",
        },
    ]
    assert first_payload["issue_samples"]["unknown_localized_source_kind"] == [
        {
            "source_kind": "aa_unknown",
            "source_record_id": 10,
            "language_code": "de",
        },
        {
            "source_kind": "aa_unknown",
            "source_record_id": 10,
            "language_code": "es",
        },
        {
            "source_kind": "aa_unknown",
            "source_record_id": 40,
            "language_code": "ja",
        },
    ]


def test_inspect_localization_json_reports_materialized_and_site_peer_mismatches(
    configured_env: Path,
    monkeypatch,
) -> None:
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()
    _analysis_id, trend_doc_id, _idea_doc_id = _seed_localizable_surfaces(
        repository=repository
    )
    notes_root = configured_env / "notes"
    site_root = notes_root / "site"
    (notes_root / "Trends").mkdir(parents=True)
    (notes_root / "Localized" / "zh-cn" / "Trends").mkdir(parents=True)
    (notes_root / "Trends" / f"day--2026-03-02--trend--{trend_doc_id}.md").write_text(
        "# English trend\n",
        encoding="utf-8",
    )
    site_root.mkdir(parents=True)
    (site_root / "manifest.json").write_text(
        json.dumps(
            {
                "languages": ["en", "zh-cn"],
                "language_codes": {"en": "en", "zh-cn": "zh-CN"},
                "default_language_code": "en",
                "files": {
                    "by_language": {
                        "en": {
                            "trend_pages": ["trends/day--2026-03-02--trend.html"],
                            "idea_pages": [],
                            "item_pages": [],
                        },
                        "zh-cn": {
                            "trend_pages": [],
                            "idea_pages": [],
                            "item_pages": [],
                        },
                    }
                },
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "inspect",
            "localization",
            "--materialized-output-dir",
            str(notes_root),
            "--site-output-dir",
            str(site_root),
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["audit_status"] == "warning"
    assert payload["materialized"]["status"] == "ok"
    assert payload["materialized"]["missing_peer_total"] == 1
    assert payload["site"]["status"] == "ok"
    assert payload["site"]["link_map"]["status"] == "missing"
    assert payload["site"]["missing_peer_total"] == 1
    assert payload["issue_counts"]["materialized_missing_peer"] == 1
    assert payload["issue_counts"]["site_missing_peer"] == 1
    assert payload["issue_counts"]["site_link_map_missing"] == 1
    assert payload["issue_samples"]["materialized_missing_peer"][0]["language_slug"] == "zh-cn"
    assert payload["issue_samples"]["site_missing_peer"][0]["language_slug"] == "zh-cn"


def test_inspect_localization_reports_link_map_output_dir_mismatch(
    configured_env: Path,
    monkeypatch,
) -> None:
    """Regression: mismatched link maps were reported as link_map=ok in text output."""
    runner = CliRunner()
    db_path = configured_env / "recoleta.db"
    _configure_localization_env(monkeypatch, configured_env, db_path)
    repository = Repository(db_path=db_path)
    repository.init_schema()
    notes_root = configured_env / "notes"
    notes_root.mkdir(parents=True)
    site_root = notes_root / "site"
    _write_empty_site_manifest(site_root)
    other_site_root = configured_env / "other-site"
    _write_site_link_map(site_root, recorded_site_output_dir=other_site_root)

    json_result = runner.invoke(
        recoleta.cli.app,
        [
            "inspect",
            "localization",
            "--materialized-output-dir",
            str(notes_root),
            "--site-output-dir",
            str(site_root),
            "--json",
        ],
    )
    text_result = runner.invoke(
        recoleta.cli.app,
        [
            "inspect",
            "localization",
            "--materialized-output-dir",
            str(notes_root),
            "--site-output-dir",
            str(site_root),
        ],
    )

    assert json_result.exit_code == 0
    payload = json.loads(json_result.stdout)
    assert payload["audit_status"] == "warning"
    assert payload["site"]["link_map"]["status"] == "mismatch"
    assert payload["site"]["link_map"]["matches_site_output_dir"] is False
    assert payload["site"]["link_map"]["recorded_output_dir"] == str(other_site_root)
    assert payload["issue_counts"]["site_link_map_mismatch"] == 1
    assert text_result.exit_code == 0
    assert "link_map=mismatch" in text_result.stdout
    assert "link_map=ok" not in text_result.stdout
