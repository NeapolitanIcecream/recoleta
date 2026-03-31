from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner
import yaml

import recoleta.cli
from recoleta.app.runtime import _build_settings as runtime_build_settings
from recoleta.site import TrendSiteInputSpec


def _clear_runtime_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "RECOLETA_CONFIG_PATH",
        "RECOLETA_DB_PATH",
        "LLM_MODEL",
        "MARKDOWN_OUTPUT_DIR",
        "PUBLISH_TARGETS",
        "TOPICS",
        "TOPIC_STREAMS",
        "topic_streams",
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


def _write_fleet_manifest(
    *,
    tmp_path: Path,
    instance_name: str = "alpha",
) -> tuple[Path, Path]:
    output_dir = tmp_path / f"{instance_name}-outputs"
    output_dir.mkdir(parents=True)
    config_path = _write_config(
        tmp_path / f"{instance_name}.yaml",
        _instance_config(
            db_path=tmp_path / f"{instance_name}.db",
            output_dir=output_dir,
        ),
    )
    manifest_path = _write_config(
        tmp_path / "fleet.yaml",
        {
            "schema_version": 1,
            "instances": [
                {"name": instance_name, "config_path": str(config_path)},
            ],
        },
    )
    return manifest_path, config_path


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


@pytest.mark.parametrize("env_key", ["TOPIC_STREAMS", "topic_streams"])
def test_runtime_build_settings_rejects_topic_streams_env_var(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    env_key: str,
) -> None:
    """Regression: topic_streams env vars must fail fast regardless of case."""
    _clear_runtime_env(monkeypatch)
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("TOPICS", "agents")
    monkeypatch.setenv(
        env_key,
        '[{"name": "agents_lab", "topics": ["agents"]}]',
    )

    with pytest.raises(ValueError, match="Unsupported config format") as exc_info:
        runtime_build_settings()

    message = str(exc_info.value)
    assert env_key in message
    assert "topic-streams-to-instances" not in message


@pytest.mark.parametrize("env_key", ["TOPIC_STREAMS", "topic_streams"])
def test_runtime_build_settings_rejects_topic_streams_in_dotenv(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    env_key: str,
) -> None:
    """Regression: topic_streams in .env must not be silently ignored."""
    _clear_runtime_env(monkeypatch)
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".env").write_text(
        "\n".join(
            [
                f"RECOLETA_DB_PATH={tmp_path / 'recoleta.db'}",
                "LLM_MODEL=openai/gpt-4o-mini",
                "TOPICS=agents",
                f"{env_key}=[]",
            ]
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Unsupported config format") as exc_info:
        runtime_build_settings()

    assert env_key in str(exc_info.value)


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


def test_fleet_site_build_reads_child_output_roots_to_include_localized_pages_pr_23(
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
        TrendSiteInputSpec(path=child_one_output, instance="alpha"),
        TrendSiteInputSpec(path=child_two_output, instance="beta"),
    ]


def test_fleet_site_build_forwards_explicit_item_export_scope_pr_23(
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
        item_export_scope="all",
        json_output=False,
        command_name="fleet site build",
    )

    assert captured["item_export_scope"] == "all"


def test_fleet_run_deploy_cli_forwards_explicit_item_export_scope_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    runner = CliRunner()
    captured: dict[str, object] = {}
    app_module = recoleta.cli._import_symbol("recoleta.cli.app")

    monkeypatch.setattr(
        app_module,
        "execute_fleet_deploy_workflow",
        lambda **kwargs: captured.update(kwargs),
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "fleet",
            "run",
            "deploy",
            "--manifest",
            str(manifest_path),
            "--item-export-scope",
            "all",
        ],
    )

    assert result.exit_code == 0
    assert captured["item_export_scope"] == "all"


@pytest.mark.parametrize(
    ("include", "skip", "match"),
    [
        ("publish", None, "only supports --include/--skip"),
        (None, "tranlsate", "unknown step id"),
    ],
)
def test_fleet_deploy_validates_step_ids_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    include: str | None,
    skip: str | None,
    match: str,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    execute_fleet_deploy_workflow = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="execute_fleet_deploy_workflow",
    )

    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.cli.fleet"),
        "run_translate_run_command",
        lambda **_: None,
    )
    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.cli.fleet"),
        "run_materialize_outputs_command",
        lambda **_: None,
    )
    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.site_deploy"),
        "deploy_trend_static_site_to_github_pages",
        lambda **_: SimpleNamespace(
            remote="origin",
            branch="gh-pages",
            remote_url="https://example.com/repo.git",
            repo_root=tmp_path,
            commit_sha="deadbeef",
            skipped=False,
            pages_source=SimpleNamespace(
                site_url="https://example.com/site",
                status="published",
            ),
        ),
    )

    with pytest.raises(ValueError, match=match):
        execute_fleet_deploy_workflow(
            manifest_path=manifest_path,
            command="fleet run deploy",
            include=include,
            skip=skip,
            repo_dir=tmp_path / "site-repo",
            json_output=False,
        )


def test_fleet_deploy_stops_when_child_translation_aborts_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    execute_fleet_deploy_workflow = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="execute_fleet_deploy_workflow",
    )
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    captured_translate_calls: list[dict[str, object]] = []

    def _aborting_translate(**kwargs: object) -> None:
        captured_translate_calls.append(dict(kwargs))
        raise RuntimeError("translation aborted")

    monkeypatch.setattr(
        fleet_cli_module,
        "run_translate_run_command",
        _aborting_translate,
    )
    monkeypatch.setattr(
        fleet_cli_module,
        "run_materialize_outputs_command",
        lambda **_: (_ for _ in ()).throw(
            AssertionError("materialize must not run after translation abort")
        ),
    )
    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.site_deploy"),
        "deploy_trend_static_site_to_github_pages",
        lambda **_: (_ for _ in ()).throw(
            AssertionError("deploy must not run after translation abort")
        ),
    )

    with pytest.raises(RuntimeError, match="translation aborted"):
        execute_fleet_deploy_workflow(
            manifest_path=manifest_path,
            command="fleet run deploy",
            include="translate",
            skip=None,
            repo_dir=tmp_path / "site-repo",
            json_output=False,
        )

    assert captured_translate_calls
    assert captured_translate_calls[0]["raise_on_abort"] is True


def test_fleet_deploy_forwards_child_instance_input_specs_pr_23(
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
    execute_fleet_deploy_workflow = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="execute_fleet_deploy_workflow",
    )
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    captured: dict[str, object] = {}

    monkeypatch.setattr(fleet_cli_module, "run_translate_run_command", lambda **_: None)
    monkeypatch.setattr(fleet_cli_module, "run_materialize_outputs_command", lambda **_: None)

    def _fake_deploy(**kwargs: object) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(
            remote="origin",
            branch="gh-pages",
            remote_url="https://example.com/repo.git",
            repo_root=tmp_path,
            commit_sha="deadbeef",
            skipped=False,
            pages_source=SimpleNamespace(
                site_url="https://example.com/site",
                status="published",
            ),
        )

    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.site_deploy"),
        "deploy_trend_static_site_to_github_pages",
        _fake_deploy,
    )

    execute_fleet_deploy_workflow(
        manifest_path=manifest_path,
        command="fleet run deploy",
        include=None,
        skip=None,
        repo_dir=tmp_path / "site-repo",
        json_output=False,
    )

    assert captured["input_dir"] == [
        TrendSiteInputSpec(path=child_one_output, instance="alpha"),
        TrendSiteInputSpec(path=child_two_output, instance="beta"),
    ]


def test_fleet_deploy_forwards_explicit_item_export_scope_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    execute_fleet_deploy_workflow = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="execute_fleet_deploy_workflow",
    )
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    captured: dict[str, object] = {}

    monkeypatch.setattr(
        fleet_cli_module,
        "run_translate_run_command",
        lambda **_: None,
    )
    monkeypatch.setattr(
        fleet_cli_module,
        "run_materialize_outputs_command",
        lambda **_: None,
    )

    def _fake_deploy(**kwargs: object) -> SimpleNamespace:
        captured.update(kwargs)
        return SimpleNamespace(
            remote="origin",
            branch="gh-pages",
            remote_url="https://example.com/repo.git",
            repo_root=tmp_path,
            commit_sha="deadbeef",
            skipped=False,
            pages_source=SimpleNamespace(
                site_url="https://example.com/site",
                status="published",
            ),
        )

    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.site_deploy"),
        "deploy_trend_static_site_to_github_pages",
        _fake_deploy,
    )

    payload = execute_fleet_deploy_workflow(
        manifest_path=manifest_path,
        command="fleet run deploy",
        include=None,
        skip=None,
        repo_dir=tmp_path / "site-repo",
        item_export_scope="all",
        json_output=True,
    )

    assert payload["status"] == "ok"
    assert captured["item_export_scope"] == "all"


def test_fleet_site_serve_builds_then_serves_explicit_output_dir_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    run_fleet_site_serve_command = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="run_fleet_site_serve_command",
    )
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    captured: dict[str, list[dict[str, object]]] = {
        "build": [],
        "serve": [],
    }

    monkeypatch.setattr(
        fleet_cli_module,
        "run_fleet_site_build_command",
        lambda **kwargs: captured["build"].append(dict(kwargs)),
    )
    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.cli.site"),
        "run_site_serve_command",
        lambda **kwargs: captured["serve"].append(dict(kwargs)),
    )

    output_dir = tmp_path / "preview-site"
    run_fleet_site_serve_command(
        manifest_path=manifest_path,
        output_dir=output_dir,
        limit=3,
        host="0.0.0.0",
        port=4173,
        build=True,
        default_language_code="en",
        item_export_scope="all",
        command_name="fleet site serve",
        build_command_name="fleet site build",
    )

    assert captured["build"] == [
        {
            "manifest_path": manifest_path,
            "output_dir": output_dir,
            "limit": 3,
            "default_language_code": "en",
            "item_export_scope": "all",
            "json_output": False,
            "command_name": "fleet site build",
        }
    ]
    assert captured["serve"] == [
        {
            "input_dir": None,
            "output_dir": output_dir,
            "limit": 3,
            "host": "0.0.0.0",
            "port": 4173,
            "build": False,
            "default_language_code": "en",
            "item_export_scope": "all",
            "command_name": "fleet site serve",
            "build_command_name": "fleet site build",
        }
    ]


def test_fleet_site_serve_skips_build_and_uses_manifest_site_dir_by_default_pr_23(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _clear_runtime_env(monkeypatch)
    manifest_path, _config_path = _write_fleet_manifest(tmp_path=tmp_path)
    run_fleet_site_serve_command = recoleta.cli._import_symbol(
        "recoleta.cli.fleet",
        attr_name="run_fleet_site_serve_command",
    )
    fleet_cli_module = recoleta.cli._import_symbol("recoleta.cli.fleet")
    captured_serve_calls: list[dict[str, object]] = []

    monkeypatch.setattr(
        fleet_cli_module,
        "run_fleet_site_build_command",
        lambda **_: (_ for _ in ()).throw(
            AssertionError("fleet build must not run when build=False")
        ),
    )
    monkeypatch.setattr(
        recoleta.cli._import_symbol("recoleta.cli.site"),
        "run_site_serve_command",
        lambda **kwargs: captured_serve_calls.append(dict(kwargs)),
    )

    run_fleet_site_serve_command(
        manifest_path=manifest_path,
        output_dir=None,
        limit=5,
        host="127.0.0.1",
        port=8000,
        build=False,
        default_language_code="zh-cn",
        item_export_scope="all",
        command_name="fleet site serve",
        build_command_name="fleet site build",
    )

    assert captured_serve_calls == [
        {
            "input_dir": None,
            "output_dir": manifest_path.parent / "site",
            "limit": 5,
            "host": "127.0.0.1",
            "port": 8000,
            "build": False,
            "default_language_code": "zh-cn",
            "item_export_scope": "all",
            "command_name": "fleet site serve",
            "build_command_name": "fleet site build",
        }
    ]
