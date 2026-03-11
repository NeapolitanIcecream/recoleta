from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path

import pytest
from sqlmodel import Session, select

from recoleta.models import (
    DELIVERY_CHANNEL_TELEGRAM,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_PUBLISHED,
    Delivery,
    Item,
    Metric,
)
from recoleta.pipeline import PipelineService
from recoleta.types import ItemDraft
from tests.spec_support import (
    FakeAnalyzer,
    FakeTelegramSender,
    FlakyTelegramSender,
    _build_runtime,
)


def test_publish_writes_note_and_prevents_duplicate_delivery(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-1",
        canonical_url="https://example.com/publish-case",
        title="Publish Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish", limit=10)

    first_publish = service.publish(run_id="run-publish", limit=10)
    second_publish = service.publish(run_id="run-publish-second", limit=10)

    assert first_publish.sent == 1
    assert second_publish.sent == 0
    assert len(sender.messages) == 1
    assert first_publish.note_paths[0].exists()


def test_publish_filters_to_requested_event_window(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    service.prepare(
        run_id="run-publish-window",
        drafts=[
            ItemDraft.from_values(
                source="rss",
                source_item_id="publish-window-old",
                canonical_url="https://example.com/publish-window-old",
                title="Publish Window Old",
                authors=["Alice"],
                published_at=datetime(2025, 1, 19, 12, tzinfo=UTC),
            ),
            ItemDraft.from_values(
                source="rss",
                source_item_id="publish-window-target",
                canonical_url="https://example.com/publish-window-target",
                title="Publish Window Target",
                authors=["Bob"],
                published_at=datetime(2025, 1, 20, 12, tzinfo=UTC),
            ),
        ],
        limit=10,
    )
    service.analyze(run_id="run-publish-window", limit=10)

    result = service.publish(
        run_id="run-publish-window",
        limit=10,
        period_start=datetime(2025, 1, 20, tzinfo=UTC),
        period_end=datetime(2025, 1, 21, tzinfo=UTC),
    )

    assert result.sent == 1
    assert len(sender.messages) == 1

    with Session(repository.engine) as session:
        items = list(session.exec(select(Item)))
    by_source_item_id = {item.source_item_id: item for item in items}
    assert by_source_item_id["publish-window-target"].state == ITEM_STATE_PUBLISHED
    assert by_source_item_id["publish-window-old"].state == ITEM_STATE_ANALYZED


def test_publish_does_not_skip_markdown_when_telegram_delivery_already_sent(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: telegram idempotency must not short-circuit other publish targets."""
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)

    markdown_dir = tmp_path / "markdown-output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown,telegram")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-telegram-already-sent-1",
        canonical_url="https://example.com/publish-telegram-already-sent-case",
        title="Publish Telegram Already Sent",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(
        run_id="run-publish-telegram-already-sent", drafts=[draft], limit=10
    )
    service.analyze(run_id="run-publish-telegram-already-sent", limit=10)

    from recoleta.observability import mask_value
    from recoleta.types import utc_now

    assert settings.telegram_chat_id is not None
    destination_hash = mask_value(settings.telegram_chat_id.get_secret_value())
    with Session(repository.engine) as session:
        item = session.exec(
            select(Item).where(
                Item.source_item_id == "item-publish-telegram-already-sent-1"
            )
        ).one()
        assert item.id is not None
        session.add(
            Delivery(
                item_id=item.id,
                channel=DELIVERY_CHANNEL_TELEGRAM,
                destination=destination_hash,
                message_id="existing-message",
                status=DELIVERY_STATUS_SENT,
                sent_at=utc_now(),
            )
        )
        session.commit()
        session.refresh(item)
        assert item.state == ITEM_STATE_ANALYZED

    result = service.publish(run_id="run-publish-telegram-already-sent", limit=10)

    assert result.sent == 1
    assert result.failed == 0
    assert len(sender.messages) == 0
    assert result.note_paths and result.note_paths[0].exists()
    assert (markdown_dir / "latest.md").exists()

    with Session(repository.engine) as session:
        item = session.exec(
            select(Item).where(
                Item.source_item_id == "item-publish-telegram-already-sent-1"
            )
        ).one()
        assert item.state == ITEM_STATE_PUBLISHED


def test_publish_does_not_downgrade_sent_telegram_delivery_when_mark_item_published_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: never downgrade a SENT Telegram delivery due to a later publish error."""
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)

    monkeypatch.setenv("PUBLISH_TARGETS", "telegram")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-no-downgrade-1",
        canonical_url="https://example.com/publish-no-downgrade-case",
        title="Publish No Downgrade Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-no-downgrade", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-no-downgrade", limit=10)

    original_mark_item_published = repository.mark_item_published
    calls = {"count": 0}

    def flaky_mark_item_published(*, item_id: int) -> None:
        calls["count"] += 1
        if calls["count"] == 1:
            raise RuntimeError("simulated mark_item_published failure")
        original_mark_item_published(item_id=item_id)

    monkeypatch.setattr(repository, "mark_item_published", flaky_mark_item_published)

    first_publish = service.publish(run_id="run-publish-no-downgrade", limit=10)
    assert first_publish.sent == 0
    assert first_publish.failed == 1
    assert len(sender.messages) == 1

    with Session(repository.engine) as session:
        deliveries = list(
            session.exec(
                select(Delivery).where(
                    Delivery.channel == DELIVERY_CHANNEL_TELEGRAM,
                )
            )
        )
        assert len(deliveries) == 1
        assert deliveries[0].status == DELIVERY_STATUS_SENT
        assert deliveries[0].message_id is not None

        item = session.exec(
            select(Item).where(Item.source_item_id == "item-publish-no-downgrade-1")
        ).one()
        assert item.state == ITEM_STATE_ANALYZED

    second_publish = service.publish(run_id="run-publish-no-downgrade-2", limit=10)
    assert second_publish.sent == 1
    assert second_publish.failed == 0
    assert len(sender.messages) == 1

    with Session(repository.engine) as session:
        item = session.exec(
            select(Item).where(Item.source_item_id == "item-publish-no-downgrade-1")
        ).one()
        assert item.state == ITEM_STATE_PUBLISHED


def test_publish_writes_local_markdown_notes_without_obsidian_or_telegram(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)

    markdown_dir = tmp_path / "markdown-output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    settings, repository = _build_runtime()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-markdown-1",
        canonical_url="https://example.com/publish-markdown-case",
        title="Publish Markdown Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-markdown", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-markdown", limit=10)

    result = service.publish(run_id="run-publish-markdown", limit=10)
    assert result.sent == 1
    assert result.failed == 0
    assert result.note_paths and result.note_paths[0].exists()
    assert (markdown_dir / "latest.md").exists()

    latest = (markdown_dir / "latest.md").read_text(encoding="utf-8")
    assert "run-publish-markdown" in latest
    assert "Inbox/" in latest

    with Session(repository.engine) as session:
        assert session.exec(select(Delivery)).first() is None


def test_publish_writes_markdown_index_when_telegram_daily_cap_reached(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.delenv("OBSIDIAN_VAULT_PATH", raising=False)

    markdown_dir = tmp_path / "markdown-output"
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(markdown_dir))
    monkeypatch.setenv("PUBLISH_TARGETS", "markdown,telegram")
    monkeypatch.setenv("MAX_DELIVERIES_PER_DAY", "0")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test-bot-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "test-chat")
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-cap-1",
        canonical_url="https://example.com/publish-cap-case",
        title="Publish Cap Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-cap", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-cap", limit=10)

    result = service.publish(run_id="run-publish-cap", limit=10)
    assert result.sent == 0
    assert result.failed == 0
    assert len(sender.messages) == 0
    assert (markdown_dir / "latest.md").exists()

    latest = (markdown_dir / "latest.md").read_text(encoding="utf-8")
    assert "run-publish-cap" in latest
    assert "No items published in this run" in latest

    with Session(repository.engine) as session:
        assert (
            session.exec(select(Item).where(Item.state == ITEM_STATE_ANALYZED)).first()
            is not None
        )
        assert session.exec(select(Delivery)).first() is None


def test_publish_filters_by_allow_tags_and_records_metric(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("ALLOW_TAGS", json.dumps(["non-matching-tag"]))

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-filter-allow-1",
        canonical_url="https://example.com/publish-filter-allow-case",
        title="Publish Filter Allow Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-filter-allow", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-filter-allow", limit=10)
    result = service.publish(run_id="run-publish-filter-allow", limit=10)

    assert result.sent == 0
    assert result.skipped == 1
    assert len(sender.messages) == 0

    metrics = repository.list_metrics(run_id="run-publish-filter-allow")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.publish.filtered_total"].value == 1


def test_publish_filters_by_deny_tags_and_records_metric(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DENY_TAGS", json.dumps(["agents"]))

    settings, repository = _build_runtime()
    sender = FakeTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-filter-deny-1",
        canonical_url="https://example.com/publish-filter-deny-case",
        title="Publish Filter Deny Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-filter-deny", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-filter-deny", limit=10)
    result = service.publish(run_id="run-publish-filter-deny", limit=10)

    assert result.sent == 0
    assert result.skipped == 1
    assert len(sender.messages) == 0

    metrics = repository.list_metrics(run_id="run-publish-filter-deny")
    by_name: dict[str, Metric] = {metric.name: metric for metric in metrics}
    assert by_name["pipeline.publish.filtered_total"].value == 1


def test_publish_retries_after_failed_delivery(configured_env) -> None:
    settings, repository = _build_runtime()
    sender = FlakyTelegramSender()
    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=sender,
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-retry-1",
        canonical_url="https://example.com/publish-retry-case",
        title="Publish Retry Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-retry", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-retry", limit=10)

    first_publish = service.publish(run_id="run-publish-retry", limit=10)
    assert settings.obsidian_vault_path is not None
    note_dir = settings.obsidian_vault_path / settings.obsidian_base_folder / "Inbox"
    note_paths_after_first = list(note_dir.glob("*.md"))
    assert len(note_paths_after_first) == 1
    first_note_path = note_paths_after_first[0]
    assert first_note_path.exists()
    second_publish = service.publish(run_id="run-publish-retry-2", limit=10)
    note_paths_after_second = list(note_dir.glob("*.md"))
    assert len(note_paths_after_second) == 1
    assert second_publish.note_paths and second_publish.note_paths[0] == first_note_path

    assert first_publish.sent == 0
    assert first_publish.failed == 1
    assert second_publish.sent == 1
    assert second_publish.failed == 0
    assert len(sender.messages) == 1

    with Session(repository.engine) as session:
        deliveries = list(
            session.exec(
                select(Delivery).where(
                    Delivery.channel == DELIVERY_CHANNEL_TELEGRAM,
                )
            )
        )
        assert len(deliveries) == 1
        assert deliveries[0].status == DELIVERY_STATUS_SENT
        assert deliveries[0].message_id is not None


def test_publish_sanitizes_secrets_in_delivery_error(
    configured_env, monkeypatch: pytest.MonkeyPatch
) -> None:
    from urllib.parse import quote

    from recoleta.observability import mask_value

    settings, repository = _build_runtime()
    assert settings.telegram_bot_token is not None
    assert settings.telegram_chat_id is not None
    token = settings.telegram_bot_token.get_secret_value()
    chat = settings.telegram_chat_id.get_secret_value()
    token_encoded = quote(token, safe="")
    chat_encoded = quote(chat, safe="")
    recoleta_llm_key = "sk-test-recoleta-llm-key"
    monkeypatch.setenv("RECOLETA_LLM_API_KEY", recoleta_llm_key)
    recoleta_llm_key_encoded = quote(recoleta_llm_key, safe="")

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(
                " ".join(
                    [
                        f"token={token}",
                        f"token_encoded={token_encoded}",
                        f"chat={chat}",
                        f"chat_encoded={chat_encoded}",
                        f"recoleta_llm_key={recoleta_llm_key}",
                        f"recoleta_llm_key_encoded={recoleta_llm_key_encoded}",
                    ]
                )
            )

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=ExplodingTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-sanitize-1",
        canonical_url="https://example.com/publish-sanitize-case",
        title="Publish Sanitize Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-sanitize", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-sanitize", limit=10)
    publish_result = service.publish(run_id="run-publish-sanitize", limit=10)

    assert publish_result.failed == 1

    with Session(repository.engine) as session:
        delivery = session.exec(select(Delivery)).one()
        assert token not in (delivery.error or "")
        assert token_encoded not in (delivery.error or "")
        assert chat not in (delivery.error or "")
        assert chat_encoded not in (delivery.error or "")
        assert recoleta_llm_key not in (delivery.error or "")
        assert recoleta_llm_key_encoded not in (delivery.error or "")
        assert mask_value(token) in (delivery.error or "")
        assert mask_value(chat) in (delivery.error or "")
        assert mask_value(recoleta_llm_key) in (delivery.error or "")


def test_publish_does_not_crash_when_debug_artifact_write_fails(
    configured_env,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from recoleta.observability import mask_value

    tmp_path = configured_env
    bad_artifacts_dir = tmp_path / "bad-artifacts"
    bad_artifacts_dir.write_text("not-a-dir", encoding="utf-8")

    monkeypatch.setenv("WRITE_DEBUG_ARTIFACTS", "true")
    monkeypatch.setenv("ARTIFACTS_DIR", str(bad_artifacts_dir))

    settings, repository = _build_runtime()
    assert settings.telegram_bot_token is not None
    assert settings.telegram_chat_id is not None
    token = settings.telegram_bot_token.get_secret_value()
    chat = settings.telegram_chat_id.get_secret_value()

    class ExplodingTelegramSender:
        def send(self, text: str) -> str:  # noqa: ARG002
            raise RuntimeError(f"token={token} chat={chat}")

    service = PipelineService(
        settings=settings,
        repository=repository,
        analyzer=FakeAnalyzer(),
        telegram_sender=ExplodingTelegramSender(),
    )

    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="item-publish-artifact-failure-1",
        canonical_url="https://example.com/publish-artifact-failure-case",
        title="Publish Artifact Failure Case",
        authors=["Alice"],
        raw_metadata={"source": "test"},
    )
    service.prepare(run_id="run-publish-artifact-failure", drafts=[draft], limit=10)
    service.analyze(run_id="run-publish-artifact-failure", limit=10)
    publish_result = service.publish(run_id="run-publish-artifact-failure", limit=10)

    assert publish_result.failed == 1

    with Session(repository.engine) as session:
        delivery = session.exec(select(Delivery)).one()
        assert token not in (delivery.error or "")
        assert chat not in (delivery.error or "")
        assert mask_value(token) in (delivery.error or "")
        assert mask_value(chat) in (delivery.error or "")
