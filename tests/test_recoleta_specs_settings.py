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
    assert settings.trends_peer_history_enabled is True
    assert settings.trends_peer_history_window_count == 3


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


def test_settings_loads_source_scale_controls(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "arxiv": {
                    "enabled": True,
                    "queries": ["cat:cs.AI"],
                    "max_results_per_run": 2,
                    "max_total_per_run": 3,
                },
                "hn": {
                    "enabled": True,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                    "max_items_per_feed": 1,
                    "max_total_per_run": 2,
                },
                "rss": {
                    "enabled": True,
                    "feeds": ["https://jack.example/"],
                    "max_items_per_feed": 3,
                    "max_total_per_run": 4,
                },
                "hf_daily": {
                    "enabled": True,
                    "max_items_per_run": 4,
                },
                "openreview": {
                    "enabled": True,
                    "venues": ["ICLR.cc/2026/Conference"],
                    "max_results_per_venue": 5,
                    "max_total_per_run": 6,
                },
            }
        ),
    )

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.sources.arxiv.max_results_per_run == 2
    assert settings.sources.arxiv.max_total_per_run == 3
    assert settings.sources.hn.max_items_per_feed == 1
    assert settings.sources.hn.max_total_per_run == 2
    assert settings.sources.rss.max_items_per_feed == 3
    assert settings.sources.rss.max_total_per_run == 4
    assert settings.sources.hf_daily.max_items_per_run == 4
    assert settings.sources.openreview.max_results_per_venue == 5
    assert settings.sources.openreview.max_total_per_run == 6


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


def test_settings_rejects_email_recipient_lists_over_resend_batch_limit(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": [f"user-{idx}@example.com" for idx in range(101)],
                "granularities": ["week"],
            }
        ),
    )

    with pytest.raises(ValueError, match="at most 100 recipients"):
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


def test_settings_loads_trends_self_similar_settings_from_env(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TRENDS_SELF_SIMILAR_ENABLED", "true")
    monkeypatch.setenv("TRENDS_RANKING_N", "42")
    monkeypatch.setenv("TRENDS_OVERVIEW_PACK_MAX_CHARS", "1234")
    monkeypatch.setenv("TRENDS_ITEM_OVERVIEW_TOP_K", "7")
    monkeypatch.setenv("TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS", "999")
    monkeypatch.setenv("TRENDS_REP_MIN_PER_CLUSTER", "3")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_ENABLED", "true")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_WINDOW_COUNT", "5")
    monkeypatch.setenv("TRENDS_PEER_HISTORY_MAX_CHARS", "4321")
    monkeypatch.setenv("TRENDS_EVOLUTION_MAX_SIGNALS", "6")

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.trends_self_similar_enabled is True
    assert settings.trends_ranking_n == 42
    assert settings.trends_overview_pack_max_chars == 1234
    assert settings.trends_item_overview_top_k == 7
    assert settings.trends_item_overview_item_max_chars == 999
    assert settings.trends_rep_min_per_cluster == 3
    assert settings.trends_peer_history_enabled is True
    assert settings.trends_peer_history_window_count == 5
    assert settings.trends_peer_history_max_chars == 4321
    assert settings.trends_evolution_max_signals == 6


def test_settings_rejects_invalid_trends_ranking_n(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("TRENDS_RANKING_N", "0")
    with pytest.raises(ValueError, match=r"(TRENDS_RANKING_N|trends_ranking_n)"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_llm_output_language_from_env(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("LLM_OUTPUT_LANGUAGE", "  zh-CN  ")
    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.llm_output_language == "zh-CN"


def test_settings_loads_recoleta_llm_connection_from_env(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("RECOLETA_LLM_API_KEY", "  sk-recoleta-test  ")
    monkeypatch.setenv("RECOLETA_LLM_BASE_URL", "  http://llm.local/v1/  ")

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.llm_api_key is not None
    assert settings.llm_api_key.get_secret_value() == "sk-recoleta-test"
    assert settings.llm_base_url == "http://llm.local/v1/"


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


def test_settings_loads_trends_self_similar_settings_from_config_file(
    configured_env, monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                "TRENDS_SELF_SIMILAR_ENABLED: true",
                "TRENDS_RANKING_N: 33",
                "TRENDS_OVERVIEW_PACK_MAX_CHARS: 9000",
                "TRENDS_ITEM_OVERVIEW_TOP_K: 0",
                "TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS: 321",
                "TRENDS_REP_MIN_PER_CLUSTER: 4",
                "TRENDS_PEER_HISTORY_ENABLED: true",
                "TRENDS_PEER_HISTORY_WINDOW_COUNT: 2",
                "TRENDS_PEER_HISTORY_MAX_CHARS: 6789",
                "TRENDS_EVOLUTION_MAX_SIGNALS: 3",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    settings = Settings()  # pyright: ignore[reportCallIssue]
    assert settings.trends_self_similar_enabled is True
    assert settings.trends_ranking_n == 33
    assert settings.trends_overview_pack_max_chars == 9000
    assert settings.trends_item_overview_top_k == 0
    assert settings.trends_item_overview_item_max_chars == 321
    assert settings.trends_rep_min_per_cluster == 4
    assert settings.trends_peer_history_enabled is True
    assert settings.trends_peer_history_window_count == 2
    assert settings.trends_peer_history_max_chars == 6789
    assert settings.trends_evolution_max_signals == 3


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


def test_settings_rejects_recoleta_llm_api_key_in_config_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'RECOLETA_LLM_API_KEY: "do-not-allow"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    with pytest.raises(
        ValueError, match="Secrets must come from environment variables only"
    ):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_rejects_recoleta_resend_api_key_in_config_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                'RECOLETA_RESEND_API_KEY: "do-not-allow"',
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    with pytest.raises(
        ValueError, match="Secrets must come from environment variables only"
    ):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_loads_email_config_and_scrubs_resend_secret(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": ["alice@example.com", "bob@example.com"],
                "granularities": ["week", "day", "week"],
                "max_clusters": 4,
                "max_evidence_per_cluster": 3,
            }
        ),
    )
    monkeypatch.setenv("RECOLETA_RESEND_API_KEY", "re_test_secret")

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.email is not None
    assert settings.email.public_site_url == "https://example.com/recoleta"
    assert settings.email.from_name == "Recoleta"
    assert settings.email.from_email == "updates@example.com"
    assert settings.email.to == ["alice@example.com", "bob@example.com"]
    assert settings.email.granularities == ["week", "day"]
    assert settings.email.max_clusters == 4
    assert settings.email.max_evidence_per_cluster == 3
    assert settings.resend_api_key is not None
    assert settings.resend_api_key.get_secret_value() == "re_test_secret"
    assert settings.safe_model_dump()["resend_api_key"] == "***"
    assert "re_test_secret" not in settings.safe_fingerprint()


def test_settings_rejects_legacy_email_granularity_key(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": ["alice@example.com"],
                "granularity": "week",
            }
        ),
    )

    with pytest.raises(ValueError, match="EMAIL.granularity is no longer supported"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_rejects_invalid_or_empty_email_granularities(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": ["alice@example.com"],
                "granularities": [],
            }
        ),
    )
    with pytest.raises(ValueError, match="EMAIL.granularities must contain at least one"):
        Settings()  # pyright: ignore[reportCallIssue]

    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": ["alice@example.com"],
                "granularities": ["week", "quarter"],
            }
        ),
    )
    with pytest.raises(ValueError, match="EMAIL.granularities must contain only"):
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


def test_settings_loads_workflow_and_daemon_configuration_from_config_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "WORKFLOWS:",
                "  granularities:",
                "    default:",
                "      recursive_lower_levels: true",
                "      delivery_mode: all",
                "      translation: auto",
                "      translate_include: [items, trends, ideas]",
                "      site_build: true",
                "      on_translate_failure: partial_success",
                "    week:",
                "      site_build: false",
                "  deploy:",
                '    translation: "off"',
                "DAEMON:",
                "  schedules:",
                "    - workflow: day",
                "      interval_minutes: 60",
                "    - workflow: week",
                "      weekday: mon",
                "      hour_utc: 2",
                "      minute_utc: 0",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    settings = Settings()  # pyright: ignore[reportCallIssue]

    week_policy = settings.workflow_policy_for_granularity("week")
    assert week_policy.site_build is False
    assert week_policy.delivery_mode == "all"
    assert settings.workflows.deploy.translation == "off"
    assert len(settings.daemon.schedules) == 2
    assert settings.daemon.schedules[0].workflow == "day"
    assert settings.daemon.schedules[1].weekday == "mon"


def test_settings_rejects_invalid_daemon_schedule_shape(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "DAEMON:",
                "  schedules:",
                "    - workflow: day",
                "      interval_minutes: 60",
                "      weekday: mon",
                "      hour_utc: 2",
                "      minute_utc: 0",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    with pytest.raises(
        ValueError, match="either interval_minutes or weekday/hour_utc/minute_utc"
    ):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_rejects_legacy_scheduler_interval_env_vars(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: CLI v2 must fail fast when old scheduler env vars are still set."""

    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("INGEST_INTERVAL_MINUTES", "60")

    with pytest.raises(ValueError, match="INGEST_INTERVAL_MINUTES"):
        Settings()  # pyright: ignore[reportCallIssue]


def test_settings_rejects_legacy_scheduler_interval_keys_in_config_file(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: old config keys must not be silently ignored after CLI v2."""

    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                f'RECOLETA_DB_PATH: "{tmp_path / "recoleta.db"}"',
                'LLM_MODEL: "openai/gpt-4o-mini"',
                "ingest_interval_minutes: 60",
            ]
        ),
        encoding="utf-8",
    )

    monkeypatch.setenv("RECOLETA_CONFIG_PATH", str(config_path))

    with pytest.raises(ValueError, match="ingest_interval_minutes"):
        Settings()  # pyright: ignore[reportCallIssue]
