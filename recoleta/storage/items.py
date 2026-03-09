from __future__ import annotations

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from rapidfuzz import fuzz
from sqlalchemy import and_, desc, func, or_
from sqlalchemy.orm import aliased
from sqlmodel import Session, select

from recoleta.models import (
    Analysis,
    Content,
    Delivery,
    Item,
    ItemStreamState,
    TrendDelivery,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage_common import _from_json_object, _to_json
from recoleta.types import DEFAULT_TOPIC_STREAM, AnalysisResult, ItemDraft, sha256_hex, utc_now


class ItemStoreMixin:
    engine: Any
    title_dedup_threshold: float
    title_dedup_max_candidates: int

    def _commit(self, session: Session) -> None: ...

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def _find_near_duplicate_by_title(
        self, session: Session, *, title: str
    ) -> tuple[Item, float] | None:
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
                by_url_hash = select(Item).where(
                    Item.canonical_url_hash == draft.canonical_url_hash
                )
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
                self._commit(session)
                session.refresh(created)
                return created, True

            previous_state = existing.state
            if matched_by_title:
                current_metadata = _from_json_object(existing.raw_metadata_json)
                alternate_urls = current_metadata.get("alternate_urls")
                if not isinstance(alternate_urls, list):
                    alternate_urls = []
                if (
                    draft.canonical_url != existing.canonical_url
                    and draft.canonical_url not in alternate_urls
                ):
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
            self._commit(session)
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

    def list_items_for_llm_analysis(
        self, *, limit: int, triage_required: bool
    ) -> list[Item]:
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

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]:
        normalized_item_id = int(item_id)
        types = [str(t or "").strip() for t in (content_types or [])]
        types = [t for t in types if t]
        if normalized_item_id <= 0 or not types:
            return {}

        wanted = set(types)
        out: dict[str, str | None] = {t: None for t in types}
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(
                    Content.item_id == normalized_item_id,
                    cast(Any, Content.content_type).in_(types),
                )
                .order_by(desc(cast(Any, Content.id)))
            )
            for content in session.exec(statement):
                ctype = str(getattr(content, "content_type", "") or "").strip()
                if ctype in wanted and out.get(ctype) is None:
                    text = getattr(content, "text", None)
                    out[ctype] = text if isinstance(text, str) and text.strip() else None
                    wanted.discard(ctype)
                    if not wanted:
                        break
        return out

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]:
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
            statement = select(Content).join(
                latest_ids, cast(Any, Content.id) == latest_ids.c.max_id
            )
            contents = list(session.exec(statement))
            return {content.item_id: content for content in contents}

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int:
        normalized_item_id = int(item_id)
        if normalized_item_id <= 0:
            raise ValueError("item_id must be > 0")
        if not isinstance(texts_by_type, dict) or not texts_by_type:
            return 0

        normalized: dict[str, str] = {}
        for raw_type, raw_text in texts_by_type.items():
            content_type = str(raw_type or "").strip()
            if not content_type:
                continue
            if not isinstance(raw_text, str):
                continue
            text_value = raw_text.strip()
            if not text_value:
                continue
            normalized[content_type] = text_value
        if not normalized:
            return 0

        hashes_by_type: dict[str, str] = {
            ctype: sha256_hex(text_value) for ctype, text_value in normalized.items()
        }
        target_types = list(hashes_by_type.keys())
        target_hashes = list(set(hashes_by_type.values()))

        inserted = 0
        with Session(self.engine) as session:
            existing_pairs: set[tuple[str, str]] = set()
            statement = select(Content.content_type, Content.content_hash).where(
                Content.item_id == normalized_item_id,
                cast(Any, Content.content_type).in_(target_types),
                cast(Any, Content.content_hash).in_(target_hashes),
            )
            for ctype, chash in session.exec(statement):
                existing_pairs.add((str(ctype), str(chash)))

            for ctype, text_value in normalized.items():
                chash = hashes_by_type[ctype]
                if (ctype, chash) in existing_pairs:
                    continue
                session.add(
                    Content(
                        item_id=normalized_item_id,
                        content_type=ctype,
                        text=text_value,
                        artifact_path=None,
                        content_hash=chash,
                    )
                )
                inserted += 1

            if inserted > 0:
                self._commit(session)
        return inserted

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
            self._commit(session)
            session.refresh(content)
            return content

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]:
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
                return existing, False

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content, True

    def _upsert_item_stream_state(
        self,
        *,
        session: Session,
        item_id: int,
        stream: str,
        state: str,
    ) -> ItemStreamState:
        existing = session.exec(
            select(ItemStreamState).where(
                ItemStreamState.item_id == item_id,
                ItemStreamState.stream == stream,
            )
        ).first()
        now = utc_now()
        if existing is None:
            existing = ItemStreamState(
                item_id=item_id,
                stream=stream,
                state=state,
                created_at=now,
                updated_at=now,
            )
        else:
            existing.state = state
            existing.updated_at = now
        session.add(existing)
        return existing

    def list_items_for_stream_analysis(
        self,
        *,
        stream: str,
        limit: int,
        selected_only: bool = False,
    ) -> list[Item]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .outerjoin(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == stream,
                    ),
                )
                .where(
                    cast(Any, Item.state).in_(
                        [ITEM_STATE_ENRICHED, ITEM_STATE_RETRYABLE_FAILED]
                    )
                )
                .order_by(
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
                .limit(limit)
            )
            if selected_only:
                statement = statement.where(
                    cast(Any, stream_state.state).in_(
                        [ITEM_STATE_TRIAGED, ITEM_STATE_RETRYABLE_FAILED]
                    )
                )
            else:
                statement = statement.where(
                    or_(
                        cast(Any, stream_state.id).is_(None),
                        cast(Any, stream_state.state) == ITEM_STATE_RETRYABLE_FAILED,
                    )
                )
            return list(session.exec(statement))

    def save_analysis(
        self,
        *,
        item_id: int,
        result: AnalysisResult,
        scope: str = DEFAULT_TOPIC_STREAM,
        mirror_item_state: bool = True,
    ) -> Analysis:
        with Session(self.engine) as session:
            analysis = session.exec(
                select(Analysis).where(
                    Analysis.item_id == item_id,
                    Analysis.scope == scope,
                )
            ).first()
            if analysis is None:
                analysis = Analysis(
                    item_id=item_id,
                    scope=scope,
                    model=result.model,
                    provider=result.provider,
                    summary=result.summary,
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
                analysis.topics_json = _to_json(result.topics)
                analysis.relevance_score = result.relevance_score
                analysis.novelty_score = result.novelty_score
                analysis.cost_usd = result.cost_usd
                analysis.latency_ms = result.latency_ms

            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=scope,
                state=ITEM_STATE_ANALYZED,
            )
            if mirror_item_state:
                item = session.get(Item, item_id)
                if item is not None:
                    item.state = ITEM_STATE_ANALYZED
                    item.updated_at = utc_now()
                    session.add(item)

            session.add(analysis)
            self._commit(session)
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
            self._commit(session)

    def mark_item_triaged(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_TRIAGED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_stream_state(
        self,
        *,
        item_id: int,
        stream: str,
        state: str,
        mirror_item_state: bool = False,
    ) -> None:
        with Session(self.engine) as session:
            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=stream,
                state=state,
            )
            if mirror_item_state:
                item = session.get(Item, item_id)
                if item is not None:
                    item.state = state
                    item.updated_at = utc_now()
                    session.add(item)
            self._commit(session)

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_RETRYABLE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> list[tuple[Item, Analysis]]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .join(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == scope,
                    ),
                )
                .where(
                    cast(Any, Analysis.scope) == scope,
                    cast(Any, stream_state.state) == ITEM_STATE_ANALYZED,
                    cast(Any, Analysis.relevance_score) >= min_relevance_score,
                )
                .order_by(
                    desc(cast(Any, Analysis.relevance_score)),
                    desc(cast(Any, Analysis.novelty_score)),
                )
                .limit(limit)
            )
            return list(session.exec(statement))

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
        *,
        doc_id: int,
        channel: str,
        destination: str,
        content_hash: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> TrendDelivery:
        now = utc_now()
        with Session(self.engine) as session:
            existing = session.exec(
                select(TrendDelivery).where(
                    TrendDelivery.doc_id == doc_id,
                    TrendDelivery.channel == channel,
                    TrendDelivery.destination == destination,
                )
            ).first()
            if existing is None:
                delivery = TrendDelivery(
                    doc_id=doc_id,
                    channel=channel,
                    destination=destination,
                    content_hash=content_hash,
                    message_id=message_id,
                    status=status,
                    error=error,
                    sent_at=now if status == DELIVERY_STATUS_SENT else None,
                )
                session.add(delivery)
                self._commit(session)
                session.refresh(delivery)
                return delivery

            existing.content_hash = content_hash
            existing.message_id = message_id
            existing.status = status
            existing.error = error
            existing.sent_at = now if status == DELIVERY_STATUS_SENT else None
            session.add(existing)
            self._commit(session)
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
            self._upsert_item_stream_state(
                session=session,
                item_id=item_id,
                stream=DEFAULT_TOPIC_STREAM,
                state=ITEM_STATE_PUBLISHED,
            )
            self._commit(session)

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
        scope: str = DEFAULT_TOPIC_STREAM,
    ) -> list[tuple[Item, Analysis]]:
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            event_at = func.coalesce(cast(Any, Item.published_at), cast(Any, Item.created_at))
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .join(
                    stream_state,
                    and_(
                        cast(Any, stream_state.item_id) == cast(Any, Item.id),
                        cast(Any, stream_state.stream) == scope,
                    ),
                )
                .where(
                    cast(Any, Analysis.scope) == scope,
                    cast(Any, stream_state.state).in_(
                        [ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]
                    ),
                    event_at >= period_start,
                    event_at < period_end,
                )
                .order_by(desc(cast(Any, event_at)), desc(cast(Any, Item.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))
