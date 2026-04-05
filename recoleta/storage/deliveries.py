from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from sqlalchemy import func
from sqlmodel import Session, select

from recoleta.models import (
    Delivery,
    TrendDelivery,
    DELIVERY_STATUS_SENT,
)
from recoleta.types import utc_now


@dataclass(frozen=True, slots=True)
class _TrendDeliveryUpsertRequest:
    doc_id: int
    channel: str
    destination: str
    content_hash: str
    message_id: str | None
    status: str
    error: str | None = None


def _trend_delivery_for_scope(
    *,
    session: Session,
    request: _TrendDeliveryUpsertRequest,
) -> TrendDelivery | None:
    return session.exec(
        select(TrendDelivery).where(
            TrendDelivery.doc_id == request.doc_id,
            TrendDelivery.channel == request.channel,
            TrendDelivery.destination == request.destination,
        )
    ).first()


def _trend_delivery_sent_at(*, now: datetime, status: str) -> datetime | None:
    return now if status == DELIVERY_STATUS_SENT else None


def _trend_delivery_row(
    *,
    request: _TrendDeliveryUpsertRequest,
    existing: TrendDelivery | None,
    now: datetime,
) -> TrendDelivery:
    if existing is None:
        return TrendDelivery(
            doc_id=request.doc_id,
            channel=request.channel,
            destination=request.destination,
            content_hash=request.content_hash,
            message_id=request.message_id,
            status=request.status,
            error=request.error,
            sent_at=_trend_delivery_sent_at(now=now, status=request.status),
        )
    existing.content_hash = request.content_hash
    existing.message_id = request.message_id
    existing.status = request.status
    existing.error = request.error
    existing.sent_at = _trend_delivery_sent_at(now=now, status=request.status)
    return existing


def _coerce_trend_delivery_upsert_request(
    *,
    request: _TrendDeliveryUpsertRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> _TrendDeliveryUpsertRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return _TrendDeliveryUpsertRequest(
        doc_id=int(values["doc_id"]),
        channel=str(values["channel"]),
        destination=str(values["destination"]),
        content_hash=str(values["content_hash"]),
        message_id=values.get("message_id"),
        status=str(values["status"]),
        error=values.get("error"),
    )


class DeliveryStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool:
        with Session(self.engine) as session:
            statement = select(Delivery).where(
                Delivery.item_id == item_id,
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def count_sent_deliveries_since(
        self, *, channel: str, destination: str, since: datetime
    ) -> int:
        with Session(self.engine) as session:
            item_statement = select(func.count(cast(Any, Delivery.id))).where(
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
                cast(Any, Delivery.sent_at).is_not(None),
                cast(Any, Delivery.sent_at) >= since,
            )
            trend_statement = select(func.count(cast(Any, TrendDelivery.id))).where(
                TrendDelivery.channel == channel,
                TrendDelivery.destination == destination,
                TrendDelivery.status == DELIVERY_STATUS_SENT,
                cast(Any, TrendDelivery.sent_at).is_not(None),
                cast(Any, TrendDelivery.sent_at) >= since,
            )
            return int(session.exec(item_statement).one()) + int(
                session.exec(trend_statement).one()
            )

    def upsert_delivery(
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> Delivery:
        now = utc_now()
        with Session(self.engine) as session:
            existing = session.exec(
                select(Delivery).where(
                    Delivery.item_id == item_id,
                    Delivery.channel == channel,
                    Delivery.destination == destination,
                )
            ).first()
            if existing is None:
                delivery = Delivery(
                    item_id=item_id,
                    channel=channel,
                    destination=destination,
                    message_id=message_id,
                    status=status,
                    error=error,
                    sent_at=now if status == DELIVERY_STATUS_SENT else None,
                )
                session.add(delivery)
                self._commit(session)
                session.refresh(delivery)
                return delivery

            existing.message_id = message_id
            existing.status = status
            existing.error = error
            if status == DELIVERY_STATUS_SENT:
                existing.sent_at = now
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def has_sent_trend_delivery(
        self,
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
    ) -> bool:
        with Session(self.engine) as session:
            statement = select(TrendDelivery).where(
                TrendDelivery.doc_id == doc_id,
                TrendDelivery.channel == channel,
                TrendDelivery.destination == destination,
                TrendDelivery.content_hash == content_hash,
                TrendDelivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def upsert_trend_delivery(
        self,
        request: _TrendDeliveryUpsertRequest | None = None,
        **legacy_kwargs: Any,
    ) -> TrendDelivery:
        now = utc_now()
        resolved_request = _coerce_trend_delivery_upsert_request(
            request=request,
            legacy_kwargs=legacy_kwargs,
        )
        with Session(self.engine) as session:
            existing = _trend_delivery_for_scope(
                session=session,
                request=resolved_request,
            )
            delivery = _trend_delivery_row(
                request=resolved_request,
                existing=existing,
                now=now,
            )
            session.add(delivery)
            self._commit(session)
            session.refresh(delivery)
            return delivery
