from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any, cast
from uuid import uuid4

from rapidfuzz import fuzz
from sqlalchemy import desc, func
from sqlmodel import Session, SQLModel, create_engine, select

from recoleta.models import (
    Analysis,
    Artifact,
    Content,
    Delivery,
    Item,
    Metric,
    Run,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.types import AnalysisResult, ItemDraft, sha256_hex, utc_now


def _to_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _from_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    loaded = json.loads(value)
    if isinstance(loaded, list):
        return [str(item) for item in loaded]
    return []


def _from_json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        loaded = json.loads(value)
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


class Repository:
    def __init__(
        self,
        *,
        db_path: Path,
        title_dedup_threshold: float = 92.0,
        title_dedup_max_candidates: int = 500,
    ) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{self.db_path}", echo=False)
        self.title_dedup_threshold = float(title_dedup_threshold)
        self.title_dedup_max_candidates = max(0, int(title_dedup_max_candidates))

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

    def _find_near_duplicate_by_title(self, session: Session, *, title: str) -> tuple[Item, float] | None:
        normalized_title = title.strip()
        if not normalized_title:
            return None
        if self.title_dedup_max_candidates <= 0:
            return None

        statement = (
            select(Item)
            .order_by(desc(cast(Any, Item.created_at)))
            .limit(self.title_dedup_max_candidates)
        )
        candidates = list(session.exec(statement))
        best_item: Item | None = None
        best_score = -1.0
        for candidate in candidates:
            score = float(fuzz.token_set_ratio(normalized_title, candidate.title))
            if score > best_score:
                best_score = score
                best_item = candidate
                if best_score >= 100.0:
                    return candidate, best_score
        if best_item is None:
            return None
        if best_score < self.title_dedup_threshold:
            return None
        return best_item, best_score

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing: Item | None = None
            matched_by_title = False
            title_dedup_score: float | None = None
            if draft.source_item_id:
                statement = select(Item).where(
                    Item.source == draft.source,
                    Item.source_item_id == draft.source_item_id,
                )
                existing = session.exec(statement).first()

            if existing is None:
                by_url_hash = select(Item).where(Item.canonical_url_hash == draft.canonical_url_hash)
                existing = session.exec(by_url_hash).first()

            if existing is None and self.title_dedup_threshold > 0:
                match = self._find_near_duplicate_by_title(session, title=draft.title)
                if match is not None:
                    existing, title_dedup_score = match
                    matched_by_title = True

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

            previous_state = existing.state
            if matched_by_title:
                current_metadata = _from_json_object(existing.raw_metadata_json)
                alternate_urls = current_metadata.get("alternate_urls")
                if not isinstance(alternate_urls, list):
                    alternate_urls = []
                if draft.canonical_url != existing.canonical_url and draft.canonical_url not in alternate_urls:
                    alternate_urls.append(draft.canonical_url)
                current_metadata["alternate_urls"] = alternate_urls

                dedup_events = current_metadata.get("dedup_events")
                if not isinstance(dedup_events, list):
                    dedup_events = []
                dedup_events.append(
                    {
                        "source": draft.source,
                        "source_item_id": draft.source_item_id,
                        "canonical_url_hash": draft.canonical_url_hash,
                        "title_similarity": round(float(title_dedup_score or 0.0), 2),
                    }
                )
                current_metadata["dedup_events"] = dedup_events[-20:]
                existing.raw_metadata_json = _to_json(current_metadata)
                if existing.published_at is None and draft.published_at is not None:
                    existing.published_at = draft.published_at
            else:
                existing.canonical_url = draft.canonical_url
                existing.canonical_url_hash = draft.canonical_url_hash
                existing.title = draft.title
                existing.authors = _to_json(draft.authors)
                existing.published_at = draft.published_at
                existing.raw_metadata_json = _to_json(draft.raw_metadata)
            if previous_state in {ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED}:
                # Allow failed items to be retried by re-ingesting.
                existing.state = ITEM_STATE_INGESTED
            existing.updated_at = utc_now()
            if (
                (not matched_by_title)
                and existing.source == draft.source
                and existing.source_item_id is None
                and draft.source_item_id is not None
            ):
                existing.source_item_id = draft.source_item_id
            session.add(existing)
            session.commit()
            session.refresh(existing)
            return existing, False

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(
                    cast(Any, Item.state).in_(
                        [
                            ITEM_STATE_INGESTED,
                            ITEM_STATE_ENRICHED,
                            ITEM_STATE_RETRYABLE_FAILED,
                        ]
                    )
                )
                .order_by(desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at)))
                .limit(limit)
            )
            return list(session.exec(statement))

    def list_items_for_llm_analysis(self, *, limit: int, triage_required: bool) -> list[Item]:
        states = [ITEM_STATE_RETRYABLE_FAILED]
        if triage_required:
            states.append(ITEM_STATE_TRIAGED)
        else:
            states.append(ITEM_STATE_ENRICHED)

        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(cast(Any, Item.state).in_(states))
                .order_by(desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at)))
                .limit(limit)
            )
            return list(session.exec(statement))

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(Content.item_id == item_id, Content.content_type == content_type)
                .order_by(desc(cast(Any, Content.id)))
            )
            return session.exec(statement).first()

    def get_latest_contents(self, *, item_ids: list[int], content_type: str) -> dict[int, Content]:
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw_item_id in item_ids:
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0 or item_id in seen:
                continue
            seen.add(item_id)
            normalized_ids.append(item_id)
        normalized_type = str(content_type or "").strip()
        if not normalized_ids or not normalized_type:
            return {}

        with Session(self.engine) as session:
            latest_ids = (
                select(
                    cast(Any, Content.item_id),
                    func.max(cast(Any, Content.id)).label("max_id"),
                )
                .where(
                    cast(Any, Content.item_id).in_(normalized_ids),
                    Content.content_type == normalized_type,
                )
                .group_by(cast(Any, Content.item_id))
                .subquery()
            )
            statement = select(Content).join(latest_ids, cast(Any, Content.id) == latest_ids.c.max_id)
            contents = list(session.exec(statement))
            return {content.item_id: content for content in contents}

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content:
        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            session.commit()
            session.refresh(content)
            return content

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

    def mark_item_enriched(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_ENRICHED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def mark_item_triaged(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_TRIAGED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_RETRYABLE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            session.commit()

    def list_items_for_publish(self, *, limit: int, min_relevance_score: float) -> list[tuple[Item, Analysis]]:
        with Session(self.engine) as session:
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(Item.state == ITEM_STATE_ANALYZED, Analysis.relevance_score >= min_relevance_score)
                .order_by(
                    desc(cast(Any, Analysis.relevance_score)),
                    desc(cast(Any, Analysis.novelty_score)),
                )
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
                session.commit()
                session.refresh(delivery)
                return delivery

            existing.message_id = message_id
            existing.status = status
            existing.error = error
            if status == DELIVERY_STATUS_SENT:
                existing.sent_at = now
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
