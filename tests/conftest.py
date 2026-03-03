from __future__ import annotations

import json
from pathlib import Path

import pytest
import respx


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("SOURCES", raising=False)
    monkeypatch.delenv("RECOLETA_CONFIG_PATH", raising=False)
    # Avoid network fetches for model pricing in tests.
    monkeypatch.setenv("LITELLM_LOCAL_MODEL_COST_MAP", "True")


@pytest.fixture()
def configured_env(
    clean_env,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,  # noqa: ARG001
):
    vault_path = tmp_path / "vault"
    vault_path.mkdir(parents=True)

    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", str(vault_path))
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("PUBLISH_TARGETS", json.dumps(["obsidian", "telegram"]))
    monkeypatch.setenv("TOPICS", json.dumps(["agents", "ml-systems"]))
    monkeypatch.setenv(
        "SOURCES",
        json.dumps(
            {
                "hn": {
                    "enabled": True,
                    "rss_urls": ["https://news.ycombinator.com/rss"],
                },
                "rss": {"enabled": True, "feeds": ["https://example.com/feed.xml"]},
            }
        ),
    )

    return tmp_path


@pytest.fixture(autouse=True)
def mock_item_html_enrichment(
    respx_mock: respx.Router, monkeypatch: pytest.MonkeyPatch
) -> None:
    respx_mock.get(host="example.com", path__regex=r"^/(?!feed\.xml$).*").respond(
        200,
        text="<html><body><p>mock html</p></body></html>",
        headers={"Content-Type": "text/html; charset=utf-8"},
    )

    import recoleta.pipeline as pipeline

    monkeypatch.setattr(pipeline, "extract_html_maintext", lambda html: "mock maintext")  # noqa: ARG005
