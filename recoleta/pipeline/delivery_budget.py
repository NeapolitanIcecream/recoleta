from __future__ import annotations

from datetime import datetime
from typing import Any

from recoleta.models import DELIVERY_CHANNEL_TELEGRAM
from recoleta.observability import mask_value
from recoleta.types import utc_now


def telegram_delivery_destination(settings: Any) -> str:
    if settings.telegram_chat_id is not None:
        return mask_value(settings.telegram_chat_id.get_secret_value())
    return "__telegram_sender__"


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
