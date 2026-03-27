from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import sqlite3

import pytest
from sqlmodel import Session, select
from typer.testing import CliRunner
import yaml

import recoleta.cli
from recoleta.app.runtime import (
    TopicStreamsMigrationRequiredError,
    _build_settings as runtime_build_settings,
)
from recoleta.models import (
    ITEM_STATE_ANALYZED,
    ITEM_STATE_INGESTED,
    Item,
    LocalizedOutput,
    PassOutput,
    Run,
    SourcePullState,
)
from recoleta.storage import Repository


def _clear_runtime_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "RECOLETA_CONFIG_PATH",
        "RECOLETA_DB_PATH",
        "LLM_MODEL",
        "MARKDOWN_OUTPUT_DIR",
        "PUBLISH_TARGETS",
        "TOPICS",
        "TOPIC_STREAMS",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "SOURCES",
        "OBSIDIAN_VAULT_PATH",
        "OBSIDIAN_BASE_FOLDER",
        "RAG_LANCEDB_DIR",
        "ARTIFACTS_DIR",
    ):
        monkeypatch.delenv(name, raising=False)


def _write_yaml(path: Path, payload: dict[str, object]) -> Path:
    path.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return path


def _legacy_config(
    *,
    db_path: Path,
    output_dir: Path,
    stream_names: list[str],
    publish_targets: list[str] | None = None,
    daemon: dict[str, object] | None = None,
    sources: dict[str, object] | None = None,
    localization: dict[str, object] | None = None,
    llm_output_language: str | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "recoleta_db_path": str(db_path),
        "llm_model": "openai/gpt-4o-mini",
        "markdown_output_dir": str(output_dir),
        "publish_targets": list(publish_targets or ["markdown"]),
        "topic_streams": [
            {"name": name, "topics": [f"topic-{name}"]} for name in stream_names
        ],
    }
    if daemon is not None:
        payload["daemon"] = daemon
    if sources is not None:
        payload["sources"] = sources
    if localization is not None:
        payload["localization"] = localization
    if llm_output_language is not None:
        payload["llm_output_language"] = llm_output_language
    return payload


def _child_config(
    *,
    db_path: Path,
    output_dir: Path,
    daemon: dict[str, object] | None = None,
) -> dict[str, object]:
    payload: dict[str, object] = {
        "recoleta_db_path": str(db_path),
        "llm_model": "openai/gpt-4o-mini",
        "topics": ["agents"],
        "publish_targets": ["markdown"],
        "markdown_output_dir": str(output_dir),
    }
    if daemon is not None:
        payload["daemon"] = daemon
    return payload


def test_runtime_build_settings_rejects_explicit_topic_stream_configs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=tmp_path / "legacy.db",
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
        ),
    )

    with pytest.raises(
        TopicStreamsMigrationRequiredError,
        match="topic-streams-to-instances",
    ):
        runtime_build_settings(config_path=config_path)


def test_cli_rejects_legacy_topic_stream_config_with_migration_guidance(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=tmp_path / "legacy.db",
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
        ),
    )
    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    runner = CliRunner()
    result = runner.invoke(recoleta.cli.app, ["run", "day"])

    assert result.exit_code == 2
    assert "topic-streams-to-instances" in result.stdout


def test_fleet_manifest_validation_rejects_child_configs_with_daemon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    child_config_path = _write_yaml(
        tmp_path / "child.yaml",
        _child_config(
            db_path=tmp_path / "child.db",
            output_dir=tmp_path / "child-outputs",
            daemon={"schedules": [{"workflow": "day", "interval_minutes": 60}]},
        ),
    )
    manifest_path = _write_yaml(
        tmp_path / "fleet.yaml",
        {
            "schema_version": 1,
            "instances": [
                {"name": "agents_lab", "config_path": str(child_config_path)},
            ],
        },
    )

    load_fleet_manifest = recoleta.cli._import_symbol(
        "recoleta.fleet",
        attr_name="load_fleet_manifest",
    )

    with pytest.raises(ValueError, match="DAEMON"):
        load_fleet_manifest(manifest_path)


def test_fleet_site_build_reads_child_outputs_only(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    child_one_output = tmp_path / "alpha-outputs"
    child_two_output = tmp_path / "beta-outputs"
    child_one_output.mkdir(parents=True)
    child_two_output.mkdir(parents=True)
    child_one_config = _write_yaml(
        tmp_path / "alpha.yaml",
        _child_config(
            db_path=tmp_path / "alpha.db",
            output_dir=child_one_output,
        ),
    )
    child_two_config = _write_yaml(
        tmp_path / "beta.yaml",
        _child_config(
            db_path=tmp_path / "beta.db",
            output_dir=child_two_output,
        ),
    )
    manifest_path = _write_yaml(
        tmp_path / "fleet.yaml",
        {
            "schema_version": 1,
            "instances": [
                {"name": "alpha", "config_path": str(child_one_config)},
                {"name": "beta", "config_path": str(child_two_config)},
            ],
        },
    )
    captured: dict[str, object] = {}

    def _fake_export_trend_static_site(**kwargs: object) -> Path:
        captured.update(kwargs)
        manifest = tmp_path / "site-manifest.json"
        manifest.write_text(
            json.dumps(
                {
                    "trends_total": 0,
                    "ideas_total": 0,
                    "topics_total": 0,
                    "streams_total": 2,
                }
            ),
            encoding="utf-8",
        )
        return manifest

    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.site"),
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )
    run_fleet_site_build_command = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="run_fleet_site_build_command",
    )

    run_fleet_site_build_command(
        manifest_path=manifest_path,
        output_dir=tmp_path / "site",
        limit=None,
        default_language_code=None,
        json_output=False,
        command_name="fleet site build",
    )

    input_dirs = captured["input_dir"]
    assert input_dirs == [
        child_one_output / "Trends",
        child_two_output / "Trends",
    ]


def test_topic_streams_migration_fails_closed_for_shared_telegram_destinations(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "@shared-destination")
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=tmp_path / "legacy.db",
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["alpha", "beta"],
            publish_targets=["telegram"],
            sources={
                "hn": {
                    "enabled": True,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                }
            },
        ),
    )
    migrate = recoleta.cli._import_symbol(
        "recoleta.instance_migration",
        attr_name="migrate_topic_streams_to_instances",
    )

    with pytest.raises(ValueError, match="shared Telegram destination"):
        migrate(
            config_path=config_path,
            db_path=tmp_path / "legacy.db",
            output_dir=tmp_path / "fleet",
            ambiguous_source_mode="copy_all",
            shared_delivery_mode="fail",
            default_scope_mode="archive",
        )


def test_topic_streams_migration_dry_run_returns_manifest_preview_without_writing(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    legacy_db = tmp_path / "legacy.db"
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=legacy_db,
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
            publish_targets=["markdown"],
        ),
    )
    Repository(db_path=legacy_db).init_schema()
    migrate = recoleta.cli._import_symbol(
        "recoleta.instance_migration",
        attr_name="migrate_topic_streams_to_instances",
    )

    result = migrate(
        config_path=config_path,
        db_path=legacy_db,
        output_dir=tmp_path / "fleet",
        ambiguous_source_mode="disable",
        shared_delivery_mode="fail",
        default_scope_mode="archive",
        dry_run=True,
    )

    assert result["dry_run"] is True
    assert result["children"][0]["name"] == "agents_lab"
    assert result["migration_manifest"]["dry_run"] is True
    assert not (tmp_path / "fleet").exists()
    assert not Path(result["fleet_manifest_path"]).exists()
    assert not Path(result["migration_manifest_path"]).exists()


def test_admin_migrate_cli_forwards_dry_run_flag(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    legacy_db = tmp_path / "legacy.db"
    Repository(db_path=legacy_db).init_schema()
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=legacy_db,
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
        ),
    )
    output_dir = tmp_path / "fleet"
    captured: dict[str, object] = {}
    migration_module = recoleta.cli._import_symbol("recoleta.instance_migration")

    def _fake_migrate(**kwargs: object) -> dict[str, object]:
        captured.update(kwargs)
        return {
            "dry_run": True,
            "fleet_manifest_path": str(output_dir / "fleet.yaml"),
            "migration_manifest_path": str(output_dir / "migration-manifest.json"),
            "children": [],
            "warnings": [],
        }

    monkeypatch.setattr(
        migration_module,
        "migrate_topic_streams_to_instances",
        _fake_migrate,
    )

    runner = CliRunner()
    result = runner.invoke(
        recoleta.cli.app,
        [
            "admin",
            "migrate",
            "topic-streams-to-instances",
            "--config",
            str(config_path),
            "--db",
            str(legacy_db),
            "--out",
            str(output_dir),
            "--dry-run",
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert captured["dry_run"] is True


def test_topic_streams_migration_rewrites_pass_output_runs_and_rebuilds_chunk_fts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    legacy_db = tmp_path / "legacy.db"
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=legacy_db,
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
            publish_targets=["markdown"],
        ),
    )
    repository = Repository(db_path=legacy_db)
    repository.init_schema()

    item_published_at = datetime(2026, 3, 20, 12, 0, tzinfo=UTC)
    with Session(repository.engine) as session:
        session.add(
            Run(
                id="legacy-run",
                config_fingerprint="legacy-fingerprint",
            )
        )
        session.add(
            Item(
                id=1,
                source="rss",
                source_item_id="item-1",
                canonical_url="https://example.com/item-1",
                canonical_url_hash="canonical-hash-1",
                title="Agents Lab Item",
                published_at=item_published_at,
                raw_metadata_json="{}",
                state=ITEM_STATE_INGESTED,
            )
        )
        session.add(
            SourcePullState(
                id=1,
                source="rss",
                scope_kind="feed",
                scope_key="https://example.com/feed.xml",
                cursor_json='{"etag":"123"}',
            )
        )
        session.commit()
    with sqlite3.connect(legacy_db) as conn:
        conn.execute("ALTER TABLE analyses ADD COLUMN scope VARCHAR(64);")
        conn.execute("ALTER TABLE documents ADD COLUMN scope VARCHAR(64);")
        conn.execute("ALTER TABLE pass_outputs ADD COLUMN scope VARCHAR(64);")
        conn.execute("ALTER TABLE localized_outputs ADD COLUMN scope VARCHAR(64);")
        conn.execute(
            """
            INSERT INTO analyses (
                id, item_id, model, provider, summary, topics_json,
                relevance_score, novelty_score, cost_usd, latency_ms, created_at, scope
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?);
            """,
            (
                1,
                1,
                "openai/gpt-4o-mini",
                "openai",
                "summary",
                '["agents"]',
                0.91,
                0.5,
                0.0,
                1,
                "agents_lab",
            ),
        )
        conn.execute(
            """
            INSERT INTO documents (
                id, doc_type, item_id, source, canonical_url, title, published_at,
                created_at, updated_at, scope
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?);
            """,
            (
                1,
                "item",
                1,
                "rss",
                "https://example.com/item-1",
                "Agents Lab Item",
                item_published_at.isoformat(),
                "agents_lab",
            ),
        )
        conn.execute(
            """
            INSERT INTO document_chunks (
                id, doc_id, chunk_index, kind, text, text_hash, source_content_type, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP);
            """,
            (
                1,
                1,
                0,
                "content",
                "lexical migration token",
                "chunk-hash-1",
                "markdown",
            ),
        )
        conn.execute(
            """
            INSERT INTO pass_outputs (
                id, run_id, pass_kind, status, schema_version, content_hash,
                payload_json, diagnostics_json, input_refs_json, created_at, scope
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, ?);
            """,
            (
                1,
                "legacy-run",
                "trend_synthesis",
                "succeeded",
                1,
                "pass-output-hash",
                '{"title":"Agents Lab Trend"}',
                "{}",
                "[]",
                "agents_lab",
            ),
        )
        conn.execute(
            """
            INSERT INTO localized_outputs (
                id, source_kind, source_record_id, language_code, status,
                schema_version, source_hash, variant_role,
                payload_json, diagnostics_json, created_at, updated_at, scope
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?);
            """,
            (
                1,
                "pass_output",
                1,
                "zh-CN",
                "succeeded",
                1,
                "localized-hash",
                "translation",
                '{"title":"智能体实验室趋势"}',
                "{}",
                "agents_lab",
            ),
        )
        conn.execute(
            """
            CREATE TABLE item_stream_states (
                id INTEGER PRIMARY KEY,
                item_id INTEGER NOT NULL,
                stream VARCHAR(64) NOT NULL,
                state VARCHAR(24) NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.execute(
            """
            INSERT INTO item_stream_states (id, item_id, stream, state)
            VALUES (1, 1, 'agents_lab', ?);
            """,
            (ITEM_STATE_ANALYZED,),
        )
        conn.commit()

    migrate = recoleta.cli._import_symbol(
        "recoleta.instance_migration",
        attr_name="migrate_topic_streams_to_instances",
    )
    result = migrate(
        config_path=config_path,
        db_path=legacy_db,
        output_dir=tmp_path / "fleet",
        ambiguous_source_mode="disable",
        shared_delivery_mode="fail",
        default_scope_mode="archive",
    )

    child_db = Path(result["children"][0]["db_path"])
    child_repository = Repository(db_path=child_db)
    child_repository.init_schema()

    with Session(child_repository.engine) as session:
        item = session.exec(select(Item).where(Item.id == 1)).one()
        pass_output = session.exec(select(PassOutput).where(PassOutput.id == 1)).one()
        localized = session.exec(
            select(LocalizedOutput).where(LocalizedOutput.id == 1)
        ).one()
        runs = list(session.exec(select(Run)))

    assert item.state == ITEM_STATE_ANALYZED
    assert len(runs) == 1
    assert runs[0].id == pass_output.run_id
    assert localized.source_record_id == pass_output.id

    with sqlite3.connect(child_db) as conn:
        chunk_fts_total = int(
            conn.execute("SELECT COUNT(*) FROM chunk_fts").fetchone()[0]
        )
    assert chunk_fts_total == 1

    matches = child_repository.search_chunks_text(
        query="lexical migration",
        doc_type="item",
        period_start=datetime(2026, 3, 20, 0, 0, tzinfo=UTC),
        period_end=datetime(2026, 3, 21, 0, 0, tzinfo=UTC),
    )
    assert matches

    manifest_path = Path(result["migration_manifest_path"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["children"][0]["pass_output_legacy_run_ids"] == {
        "1": "legacy-run"
    }


def test_topic_streams_migration_uses_child_default_language_for_site_export(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    legacy_db = tmp_path / "legacy.db"
    Repository(db_path=legacy_db).init_schema()
    config_path = _write_yaml(
        tmp_path / "legacy.yaml",
        _legacy_config(
            db_path=legacy_db,
            output_dir=tmp_path / "legacy-outputs",
            stream_names=["agents_lab"],
            publish_targets=["markdown"],
            localization={
                "source_language_code": "en",
                "targets": [{"code": "zh-CN", "llm_label": "Chinese (Simplified)"}],
                "site_default_language_code": "en",
            },
            llm_output_language="English",
        ),
    )
    materialize_module = recoleta.cli._import_symbol("recoleta.cli.materialize")
    site_module = recoleta.cli._import_symbol("recoleta.site")
    captured: dict[str, object] = {}

    def _fake_materialize_outputs_command(**kwargs: object) -> None:
        config_value = kwargs["config_path"]
        assert isinstance(config_value, Path)
        output_dir = config_value.parent / "outputs" / "Trends"
        (output_dir / "en").mkdir(parents=True, exist_ok=True)
        (output_dir / "zh-cn").mkdir(parents=True, exist_ok=True)

    def _fake_export_trend_static_site(**kwargs: object) -> Path:
        captured.update(kwargs)
        output_dir = kwargs["output_dir"]
        assert isinstance(output_dir, Path)
        output_dir.mkdir(parents=True, exist_ok=True)
        manifest_path = output_dir / "site-manifest.json"
        manifest_path.write_text("{}", encoding="utf-8")
        return manifest_path

    monkeypatch.setattr(
        materialize_module,
        "run_materialize_outputs_command",
        _fake_materialize_outputs_command,
    )
    monkeypatch.setattr(
        site_module,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )

    migrate = recoleta.cli._import_symbol(
        "recoleta.instance_migration",
        attr_name="migrate_topic_streams_to_instances",
    )
    migrate(
        config_path=config_path,
        db_path=legacy_db,
        output_dir=tmp_path / "fleet",
        ambiguous_source_mode="disable",
        shared_delivery_mode="fail",
        default_scope_mode="archive",
    )

    assert captured["default_language_code"] == "en"
