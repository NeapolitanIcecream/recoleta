from __future__ import annotations

import json
from pathlib import Path

import pytest

from recoleta.config import Settings


def test_settings_loads_without_obsidian_or_telegram_when_markdown_only(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("RECOLETA_CONFIG_PATH", raising=False)
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.delenv("RECOLETA_CONFIG_PATH", raising=False)

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path is None
    assert settings.telegram_bot_token is None
    assert settings.telegram_chat_id is None
    assert settings.publish_targets == ["markdown"]
    assert settings.sources.arxiv.enrich_method == "html_document"
    assert settings.sources.arxiv.enrich_failure_mode == "fallback"
    assert settings.sources.hn.enabled is False
    assert settings.sources.rss.enabled is False
    assert settings.sources.arxiv.enabled is False
    assert settings.sources.openreview.enabled is False
    assert settings.sources.hf_daily.enabled is False


def test_settings_rejects_configured_source_without_enabled(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps({"rss": {"feeds": ["https://example.com/feed.xml"]}}),
    )
    with pytest.raises(ValueError, match=r"configured but disabled"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_nested_source_configuration(configured_env) -> None:
    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.sources.hn.enabled is True
    assert settings.sources.hn.rss_urls == ["https://news.ycombinator.com/rss"]
    assert settings.sources.rss.enabled is True
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]
    assert settings.topics == ["agents", "ml-systems"]


def test_settings_loads_arxiv_enrich_configuration(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "latex_source",
                    "enrich_failure_mode": "strict",
                }
            }
        ),
    )
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.sources.arxiv.queries == ["cat:cs.AI"]
    assert settings.sources.arxiv.enrich_method == "latex_source"
    assert settings.sources.arxiv.enrich_failure_mode == "strict"


def test_settings_rejects_invalid_arxiv_enrich_configuration(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "enrich_method": "unknown",
                }
            }
        ),
    )
    with pytest.raises(ValueError, match="enrich_method"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_sources_from_yaml_env_string(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        "\n".join(
            [
                "hn:",
                "  enabled: true",
                "  rss_urls:",
                "    - https://news.ycombinator.com/rss",
                "rss:",
                "  enabled: true",
                "  feeds:",
                "    - https://example.com/feed.xml",
            ]
        ),
    )
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.sources.hn.rss_urls == ["https://news.ycombinator.com/rss"]
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]


def test_settings_loads_topics_from_yaml_env_string(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TOPICS", "\n".join(["- agents", "- ml-systems"]))
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.topics == ["agents", "ml-systems"]


def test_settings_loads_allow_and_deny_tags_from_env_strings(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ALLOW_TAGS", "agents, ml-systems")
    monkeypatch.setenv("DENY_TAGS", json.dumps(["crypto"]))
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.allow_tags == ["agents", "ml-systems"]
    assert settings.deny_tags == ["crypto"]


def test_settings_loads_llm_output_language_from_env(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "  zh-CN  ")
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.llm_output_language == "zh-CN"


def test_settings_rejects_multiline_llm_output_language(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "zh\nCN")
    with pytest.raises(ValueError, match="single-line"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_from_config_file_and_env(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "TOPICS:",
                "  - agents",
                "SOURCES:",
                "  rss:",
                "    enabled: true",
                "    feeds:",
                "      - https://example.com/feed.xml",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path == vault_path.resolve()
    assert settings.recoleta_db_path == (tmp_path / "recoleta.db").resolve()
    assert settings.llm_model == "openai/gpt-4o-mini"
    assert settings.topics == ["agents"]
    assert settings.sources.rss.feeds == ["https://example.com/feed.xml"]


def test_settings_loads_llm_output_language_from_config_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'LLM_OUTPUT_LANGUAGE: "Chinese (Simplified)"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.llm_output_language == "Chinese (Simplified)"


def test_settings_loads_from_config_file_via_init_arg(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "TOPICS:",
                "  - agents",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.delenv("RECOLETA_CONFIG_PATH", raising=False)
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    settings = Settings(config_path=config_path)  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_vault_path == vault_path.resolve()
    assert settings.recoleta_db_path == (tmp_path / "recoleta.db").resolve()
    assert settings.llm_model == "openai/gpt-4o-mini"
    assert settings.topics == ["agents"]


def test_settings_env_overrides_config_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.json"
    config_path.write_text(
        json.dumps(
            {
                "OBSIDIAN_VAULT_PATH": str(vault_path),
                "RECOLETA_DB_PATH": str(tmp_path / "recoleta.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "OBSIDIAN_BASE_FOLDER": "FromConfig",
            }
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("OBSIDIAN_BASE_FOLDER", "FromEnv")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.obsidian_base_folder == "FromEnv"


def test_settings_rejects_secrets_in_config_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'OBSIDIAN_VAULT_PATH: "{vault_path}"',
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'TELEGRAM_BOT_TOKEN: "do-not-allow"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")

    with pytest.raises(
        ValueError, match="Secrets must come from environment variables only"
    ):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_requires_artifacts_dir_when_debug_artifacts_enabled(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.delenv("ARTIFACTS_DIR", raising=False)

    with pytest.raises(ValueError, match=r"ARTIFACTS_DIR.*WRITE_DEBUG_ARTIFACTS"):
        Settings()  # pyright: ignore[reportCallIssue]
