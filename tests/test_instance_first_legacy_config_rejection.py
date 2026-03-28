from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner
import yaml

import recoleta.cli
from recoleta.app.runtime import _build_settings as runtime_build_settings


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


def _write_config(path: Path, payload: dict[str, object]) -> Path:
    if path.suffix == ".json":
        path.write_text(
            json.dumps(payload, ensure_ascii=False, sort_keys=True),
            encoding="utf-8",
        )
    else:
        path.write_text(
            yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
    return path


def _instance_config(*, db_path: Path, output_dir: Path) -> dict[str, object]:
    return {
        "recoleta_db_path": str(db_path),
        "llm_model": "openai/gpt-4o-mini",
        "topics": ["agents"],
        "publish_targets": ["markdown"],
        "markdown_output_dir": str(output_dir),
    }


@pytest.mark.parametrize(
    ("suffix", "legacy_key"),
    [
        (".yaml", "topic_streams"),
        (".yaml", "TOPIC_STREAMS"),
        (".json", "topic_streams"),
        (".json", "TOPIC_STREAMS"),
    ],
)
def test_runtime_build_settings_rejects_topic_stream_keys_in_config_files(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    suffix: str,
    legacy_key: str,
) -> None:
    """Regression: old topic stream keys must fail fast instead of being ignored."""
    _clear_runtime_env(monkeypatch)
    config_path = _write_config(
        tmp_path / f"legacy{suffix}",
        {
            **_instance_config(
                db_path=tmp_path / "recoleta.db",
                output_dir=tmp_path / "outputs",
            ),
            legacy_key: [{"name": "agents_lab", "topics": ["agents"]}],
        },
    )

    with pytest.raises(ValueError, match="Unsupported config format") as exc_info:
        runtime_build_settings(config_path=config_path)

    message = str(exc_info.value)
    assert legacy_key in message
    assert "topic-streams-to-instances" not in message


def test_runtime_build_settings_rejects_topic_streams_env_var(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: TOPIC_STREAMS in the environment must fail fast too."""
    _clear_runtime_env(monkeypatch)
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", "agents")
    monkeypatch.setenv(
        "TOPIC_STREAMS",
        '[{"name": "agents_lab", "topics": ["agents"]}]',
    )

    with pytest.raises(ValueError, match="Unsupported config format") as exc_info:
        runtime_build_settings()

    message = str(exc_info.value)
    assert "TOPIC_STREAMS" in message
    assert "topic-streams-to-instances" not in message


def test_runtime_build_settings_rejects_topic_streams_in_dotenv(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: TOPIC_STREAMS in .env must not be silently ignored."""
    _clear_runtime_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "\n".join(
            [
                f"RECOLETA_DB_PATH={tmp_path / 'recoleta.db'}",
                "LLM_MODEL=openai/gpt-4o-mini",
                "TOPICS=agents",
                "TOPIC_STREAMS=[]",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported config format") as exc_info:
        runtime_build_settings()

    assert "TOPIC_STREAMS" in str(exc_info.value)


def test_cli_run_day_reports_generic_unsupported_config_format(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    config_path = _write_config(
        tmp_path / "legacy.yaml",
        {
            **_instance_config(
                db_path=tmp_path / "legacy.db",
                output_dir=tmp_path / "legacy-outputs",
            ),
            "topic_streams": [{"name": "agents_lab", "topics": ["agents"]}],
        },
    )
    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    runner = CliRunner()
    result = runner.invoke(recoleta.cli.app, ["run", "day"])

    assert result.exit_code == 2
    assert "Unsupported config format" in result.stdout
    assert "topic_streams" in result.stdout
    assert "topic-streams-to-instances" not in result.stdout


def test_fleet_manifest_validation_rejects_child_configs_with_daemon(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    child_config_path = _write_config(
        tmp_path / "child.yaml",
        {
            **_instance_config(
                db_path=tmp_path / "child.db",
                output_dir=tmp_path / "child-outputs",
            ),
            "daemon": {"schedules": [{"workflow": "day", "interval_minutes": 60}]},
        },
    )
    manifest_path = _write_config(
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
    child_one_config = _write_config(
        tmp_path / "alpha.yaml",
        _instance_config(
            db_path=tmp_path / "alpha.db",
            output_dir=child_one_output,
        ),
    )
    child_two_config = _write_config(
        tmp_path / "beta.yaml",
        _instance_config(
            db_path=tmp_path / "beta.db",
            output_dir=child_two_output,
        ),
    )
    manifest_path = _write_config(
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

    assert captured["input_dir"] == [
        child_one_output / "Trends",
        child_two_output / "Trends",
    ]
