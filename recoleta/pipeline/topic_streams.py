from __future__ import annotations

from datetime import datetime
from typing import Any

from recoleta.config import Settings, TopicStreamRuntime
from recoleta.delivery import TelegramSender
from recoleta.models import DELIVERY_CHANNEL_TELEGRAM
from recoleta.observability import mask_value
from recoleta.types import DEFAULT_TOPIC_STREAM, utc_now


def telegram_delivery_destination(settings: Any) -> str:
    if settings.telegram_chat_id is not None:
        return mask_value(settings.telegram_chat_id.get_secret_value())
    return "__telegram_sender__"


def telegram_destination_for_stream(stream: TopicStreamRuntime) -> str:
    if stream.telegram_chat_id is not None:
        return mask_value(stream.telegram_chat_id.get_secret_value())
    return "__telegram_sender__"


def telegram_sender_for_stream(service: Any, stream: TopicStreamRuntime) -> Any:
    if isinstance(service.telegram_sender, dict):
        sender = service.telegram_sender.get(stream.name)
        if sender is not None:
            return sender
        sender = service.telegram_sender.get(DEFAULT_TOPIC_STREAM)
        if sender is not None:
            return sender
    elif service.telegram_sender is not None:
        return service.telegram_sender

    if stream.name in service._telegram_senders:
        return service._telegram_senders[stream.name]
    if stream.telegram_bot_token is None or stream.telegram_chat_id is None:
        raise ValueError(
            f"Telegram credentials are required for topic stream '{stream.name}'"
        )
    sender = TelegramSender(
        token=stream.telegram_bot_token.get_secret_value(),
        chat_id=stream.telegram_chat_id.get_secret_value(),
    )
    service._telegram_senders[stream.name] = sender
    return sender


def telegram_delivery_budget_for_stream(
    *, repository: Any, stream: TopicStreamRuntime
) -> tuple[str, int, int]:
    destination = telegram_destination_for_stream(stream)
    now = utc_now()
    midnight_utc = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        tzinfo=now.tzinfo,
    )
    sent_today = repository.count_sent_deliveries_since(
        channel=DELIVERY_CHANNEL_TELEGRAM,
        destination=destination,
        since=midnight_utc,
    )
    remaining_today = max(0, stream.max_deliveries_per_day - sent_today)
    return destination, sent_today, remaining_today


def settings_for_topic_stream(
    *, settings: Settings, stream: TopicStreamRuntime
) -> Settings:
    return settings.model_copy(
        update={
            "topics": list(stream.topics),
            "topic_streams": [],
            "allow_tags": list(stream.allow_tags),
            "deny_tags": list(stream.deny_tags),
            "publish_targets": list(stream.publish_targets),
            "markdown_output_dir": stream.markdown_output_dir,
            "obsidian_base_folder": stream.obsidian_base_folder,
            "min_relevance_score": float(stream.min_relevance_score),
            "max_deliveries_per_day": int(stream.max_deliveries_per_day),
            "telegram_bot_token": stream.telegram_bot_token,
            "telegram_chat_id": stream.telegram_chat_id,
        }
    )


def telegram_delivery_budget(*, repository: Any, settings: Any) -> tuple[str, int, int]:
    destination = telegram_delivery_destination(settings)
    now = utc_now()
    midnight_utc = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        tzinfo=now.tzinfo,
    )
    sent_today = repository.count_sent_deliveries_since(
        channel=DELIVERY_CHANNEL_TELEGRAM,
        destination=destination,
        since=midnight_utc,
    )
    remaining_today = max(0, settings.max_deliveries_per_day - sent_today)
    return destination, sent_today, remaining_today
