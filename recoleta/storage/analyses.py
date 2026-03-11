from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from sqlalchemy import and_, desc, func
from sqlalchemy.orm import aliased
from sqlmodel import Session, select

from recoleta.models import (
    Analysis,
    Item,
    ItemStreamState,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage_common import _to_json
from recoleta.types import DEFAULT_TOPIC_STREAM, AnalysisResult, utc_now


class AnalysisStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def _upsert_item_stream_state(
        self,
        *,
        session: Session,
        item_id: int,
        stream: str,
        state: str,
    ) -> ItemStreamState: ...

    def list_items_for_llm_analysis(
        self,
        *,
        limit: int,
        triage_required: bool,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[Item]:
        states = [ITEM_STATE_RETRYABLE_FAILED]
        if triage_required:
            states.append(ITEM_STATE_TRIAGED)
        else:
            states.append(ITEM_STATE_ENRICHED)

        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = select(Item).where(cast(Any, Item.state).in_(states))
            if period_start is not None and period_end is not None:
                statement = statement.where(
                    event_at >= period_start, event_at < period_end
                )
                statement = statement.order_by(
                    desc(cast(Any, event_at)),
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            else:
                statement = statement.order_by(
                    desc(cast(Any, Item.updated_at)),
                    desc(cast(Any, Item.created_at)),
                )
            statement = statement.limit(limit)
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

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        scope: str = DEFAULT_TOPIC_STREAM,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[tuple[Item, Analysis]]:
        stream_state = aliased(ItemStreamState)
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at),
                cast(Any, Item.created_at),
            )
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
            )
            if period_start is not None and period_end is not None:
                statement = statement.where(
                    event_at >= period_start,
                    event_at < period_end,
                )
            statement = statement.order_by(
                desc(cast(Any, Analysis.relevance_score)),
                desc(cast(Any, Analysis.novelty_score)),
            ).limit(limit)
            return list(session.exec(statement))

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
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
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
