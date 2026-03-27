from __future__ import annotations

import json
from pathlib import Path

import pytest

from recoleta.legacy_migration import (
    legacy_explicit_topic_streams,
    load_legacy_config_document,
    load_legacy_settings,
)


def _write_legacy_yaml_config(
    *,
    path: Path,
    markdown_output_dir: Path,
    db_path: Path,
    topic_streams_payload: str,
) -> None:
    path.write_text(
        "\n".join(
            [
                f"recoleta_db_path: {db_path}",
                "llm_model: openai/gpt-4o-mini",
                f"markdown_output_dir: {markdown_output_dir}",
                'publish_targets: ["markdown"]',
                f"topic_streams: {topic_streams_payload}",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_legacy_migration_loads_explicit_topic_stream_runtimes_from_config_path(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "legacy-recoleta.yaml"
    _write_legacy_yaml_config(
        path=config_path,
        markdown_output_dir=tmp_path / "outputs",
        db_path=tmp_path / "recoleta.db",
        topic_streams_payload=(
            "["
            "{name: agents_lab, topics: [agents]}, "
            "{name: bio_watch, topics: [biology], "
            "telegram_bot_token_env: BIO_WATCH_BOT_TOKEN, "
            "telegram_chat_id_env: BIO_WATCH_CHAT_ID}"
            "]"
        ),
    )
    monkeypatch.setenv("BIO_WATCH_BOT_TOKEN", "bio-watch-bot")
    monkeypatch.setenv("BIO_WATCH_CHAT_ID", "@bio-watch")

    settings = load_legacy_settings(config_path)
    streams = legacy_explicit_topic_streams(settings)

    assert settings.topics == []
    assert [stream.name for stream in streams] == ["agents_lab", "bio_watch"]
    assert streams[0].markdown_output_dir == (
        tmp_path / "outputs" / "Streams" / "agents_lab"
    ).resolve()
    assert streams[1].markdown_output_dir == (
        tmp_path / "outputs" / "Streams" / "bio_watch"
    ).resolve()
    assert streams[1].telegram_bot_token is not None
    assert streams[1].telegram_bot_token.get_secret_value() == "bio-watch-bot"
    assert streams[1].telegram_chat_id is not None
    assert streams[1].telegram_chat_id.get_secret_value() == "@bio-watch"


def test_legacy_migration_load_config_document_supports_json_without_mutating_source(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "legacy-recoleta.json"
    payload = {
        "recoleta_db_path": str(tmp_path / "recoleta.db"),
        "llm_model": "openai/gpt-4o-mini",
        "markdown_output_dir": str(tmp_path / "outputs"),
        "publish_targets": ["markdown"],
        "topic_streams": [{"name": "agents_lab", "topics": ["agents"]}],
    }
    config_path.write_text(json.dumps(payload), encoding="utf-8")

    loaded = load_legacy_config_document(config_path)
    loaded["markdown_output_dir"] = "changed"
    reloaded = load_legacy_config_document(config_path)

    assert reloaded["markdown_output_dir"] == str(tmp_path / "outputs")
    assert reloaded["topic_streams"] == [{"name": "agents_lab", "topics": ["agents"]}]


def test_legacy_migration_rejects_colliding_topic_stream_names_after_normalization(
    tmp_path: Path,
) -> None:
    config_path = tmp_path / "legacy-recoleta.yaml"
    _write_legacy_yaml_config(
        path=config_path,
        markdown_output_dir=tmp_path / "outputs",
        db_path=tmp_path / "recoleta.db",
        topic_streams_payload=(
            "["
            "{name: agents-lab, topics: [agents]}, "
            "{name: agents_lab, topics: [biology]}"
            "]"
        ),
    )

    with pytest.raises(
        ValueError,
        match="TOPIC_STREAMS names collide after downstream normalization",
    ):
        _ = load_legacy_settings(config_path)
