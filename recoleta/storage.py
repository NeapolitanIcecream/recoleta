from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from sqlalchemy import desc, func
from sqlmodel import Session, SQLModel, create_engine, select

from recoleta.models import (
    Analysis,
    Artifact,
    Delivery,
    Item,
    Metric,
    Run,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.types import AnalysisResult, ItemDraft, utc_now


def _to_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _from_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    loaded = json.loads(value)
    if isinstance(loaded, list):
        return [str(item) for item in loaded]
    return []


class Repository:
    def __init__(self, *, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)

    def init_schema(self) -> None:
        SQLModel.metadata.create_all(self.engine)

    def create_run(self, config_fingerprint: str, run_id: str | None = None) -> Run:
        run = Run(
            id=run_id or str(uuid4()),
            status=RUN_STATUS_RUNNING,
            config_fingerprint=config_fingerprint,
        )
        with Session(self.engine) as session:
            session.add(run)
            session.commit()
            session.refresh(run)
            return run

    def finish_run(self, run_id: str, success: bool) -> None:
        final_status = RUN_STATUS_SUCCEEDED if success else RUN_STATUS_FAILED
        with Session(self.engine) as session:
            run = session.get(Run, run_id)
            if run is None:
                return
            run.status = final_status
            run.finished_at = utc_now()
            session.add(run)
            session.commit()

    def record_metric(self, *, run_id: str, name: str, value: float, unit: str | None = None) -> None:
        metric = Metric(run_id=run_id, name=name, value=value, unit=unit)
        with Session(self.engine) as session:
            session.add(metric)
            session.commit()

    def list_metrics(self, *, run_id: str) -> list[Metric]:
        with Session(self.engine) as session:
            statement = (
                select(Metric).where(Metric.run_id == run_id).order_by(cast(Any, Metric.id))
            )
            return list(session.exec(statement))

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing: Item | None = None
            if draft.source_item_id:
                statement = select(Item).where(
                    Item.source == draft.source,
                    Item.source_item_id == draft.source_item_id,
                )
                existing = session.exec(statement).first()

            if existing is None:
                by_url_hash = select(Item).where(Item.canonical_url_hash == draft.canonical_url_hash)
                existing = session.exec(by_url_hash).first()

            if existing is None:
                created = Item(
                    source=draft.source,
                    source_item_id=draft.source_item_id,
                    canonical_url=draft.canonical_url,
                    canonical_url_hash=draft.canonical_url_hash,
                    title=draft.title,
                    authors=_to_json(draft.authors),
                    published_at=draft.published_at,
                    raw_metadata_json=_to_json(draft.raw_metadata),
                    state=ITEM_STATE_INGESTED,
                )
                session.add(created)
                session.commit()
                session.refresh(created)
                return created, True

            existing.canonical_url = draft.canonical_url
            existing.canonical_url_hash = draft.canonical_url_hash
            existing.title = draft.title
            existing.authors = _to_json(draft.authors)
            existing.published_at = draft.published_at
            existing.raw_metadata_json = _to_json(draft.raw_metadata)
            existing.state = ITEM_STATE_INGESTED
            existing.updated_at = utc_now()
            if existing.source_item_id is None and draft.source_item_id is not None:
                existing.source_item_id = draft.source_item_id
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing, False

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(Item.state == ITEM_STATE_INGESTED)
                .order_by(desc(cast(Any, Item.created_at)))
                .limit(limit)
            )
            return list(session.exec(statement))

    def save_analysis(self, *, item_id: int, result: AnalysisResult) -> Analysis:
        with Session(self.engine) as session:
            analysis = session.exec(select(Analysis).where(Analysis.item_id == item_id)).first()
            if analysis is None:
                analysis = Analysis(
                    item_id=item_id,
                    model=result.model,
                    provider=result.provider,
                    summary=result.summary,
                    insight=result.insight,
                    idea_directions_json=_to_json(result.idea_directions),
                    topics_json=_to_json(result.topics),
                    relevance_score=result.relevance_score,
                    novelty_score=result.novelty_score,
                    cost_usd=result.cost_usd,
                    latency_ms=result.latency_ms,
                )
            else:
                analysis.model = result.model
                analysis.provider = result.provider
                analysis.summary = result.summary
                analysis.insight = result.insight
                analysis.idea_directions_json = _to_json(result.idea_directions)
                analysis.topics_json = _to_json(result.topics)
                analysis.relevance_score = result.relevance_score
                analysis.novelty_score = result.novelty_score
                analysis.cost_usd = result.cost_usd
                analysis.latency_ms = result.latency_ms

            item = session.get(Item, item_id)
            if item is not None:
                item.state = ITEM_STATE_ANALYZED
                item.updated_at = utc_now()
                session.add(item)

            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            return analysis

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def list_items_for_publish(self, *, limit: int, min_relevance_score: float) -> list[tuple[Item, Analysis]]:
        with Session(self.engine) as session:
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(Item.state == ITEM_STATE_ANALYZED, Analysis.relevance_score >= min_relevance_score)
                .order_by(desc(cast(Any, Analysis.relevance_score)))
                .limit(limit)
            )
            return list(session.exec(statement))

    def has_sent_delivery(self, *, item_id: int, channel: str, destination: str) -> bool:
        with Session(self.engine) as session:
            statement = select(Delivery).where(
                Delivery.item_id == item_id,
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def count_sent_deliveries_since(self, *, channel: str, destination: str, since: datetime) -> int:
        with Session(self.engine) as session:
            statement = (
                select(func.count(cast(Any, Delivery.id)))
                .where(
                    Delivery.channel == channel,
                    Delivery.destination == destination,
                    Delivery.status == DELIVERY_STATUS_SENT,
                    cast(Any, Delivery.sent_at).is_not(None),
                    cast(Any, Delivery.sent_at) >= since,
                )
            )
            return int(session.exec(statement).one())

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
                    sent_at=utc_now(),
                )
                session.add(delivery)
                session.commit()
                session.refresh(delivery)
                return delivery

            existing.message_id = message_id
            existing.status = status
            existing.error = error
            existing.sent_at = utc_now()
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing

    def mark_item_published(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_PUBLISHED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def add_artifact(self, *, run_id: str, item_id: int | None, kind: str, path: str) -> None:
        artifact = Artifact(run_id=run_id, item_id=item_id, kind=kind, path=path)
        with Session(self.engine) as session:
            session.add(artifact)
            session.commit()

    @staticmethod
    def decode_list(value: str | None) -> list[str]:
        return _from_json_list(value)
