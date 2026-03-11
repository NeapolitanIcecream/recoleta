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
from recoleta.types import (
    DEFAULT_TOPIC_STREAM,
    AnalysisResult,
    AnalysisWrite,
    utc_now,
)


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
        existing_states: dict[tuple[int, str], ItemStreamState] | None = None,
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

    def save_analyses_batch(self, *, analyses: list[AnalysisWrite]) -> int:
        normalized: list[AnalysisWrite] = []
        seen: dict[tuple[int, str], int] = {}
        for analysis in analyses:
            try:
                item_id = int(analysis.item_id)
            except Exception:
                continue
            if item_id <= 0:
                continue
            scope = str(analysis.scope or DEFAULT_TOPIC_STREAM).strip() or DEFAULT_TOPIC_STREAM
            key = (item_id, scope)
            normalized_write = AnalysisWrite(
                item_id=item_id,
                result=analysis.result,
                scope=scope,
                mirror_item_state=bool(analysis.mirror_item_state),
            )
            existing_index = seen.get(key)
            if existing_index is None:
                seen[key] = len(normalized)
                normalized.append(normalized_write)
            else:
                normalized[existing_index] = normalized_write
        if not normalized:
            return 0

        item_ids = sorted({analysis.item_id for analysis in normalized})
        scopes = sorted({analysis.scope for analysis in normalized})
        mirror_item_ids = sorted(
            {
                analysis.item_id
                for analysis in normalized
                if analysis.mirror_item_state
            }
        )
        with Session(self.engine) as session:
            existing_by_key: dict[tuple[int, str], Analysis] = {}
            statement = select(Analysis).where(
                cast(Any, Analysis.item_id).in_(item_ids),
                cast(Any, Analysis.scope).in_(scopes),
            )
            for analysis in session.exec(statement):
                existing_by_key[(analysis.item_id, analysis.scope)] = analysis

            existing_states: dict[tuple[int, str], ItemStreamState] = {}
            stream_state_statement = select(ItemStreamState).where(
                cast(Any, ItemStreamState.item_id).in_(item_ids),
                cast(Any, ItemStreamState.stream).in_(scopes),
            )
            for stream_state in session.exec(stream_state_statement):
                existing_states[(stream_state.item_id, stream_state.stream)] = (
                    stream_state
                )

            items_by_id: dict[int, Item] = {}
            if mirror_item_ids:
                item_statement = select(Item).where(cast(Any, Item.id).in_(mirror_item_ids))
                items_by_id = {
                    int(item.id): item
                    for item in session.exec(item_statement)
                    if item.id is not None
                }

            applied = 0
            for analysis_write in normalized:
                key = (analysis_write.item_id, analysis_write.scope)
                existing = existing_by_key.get(key)
                result = analysis_write.result
                if existing is None:
                    existing = Analysis(
                        item_id=analysis_write.item_id,
                        scope=analysis_write.scope,
                        model=result.model,
                        provider=result.provider,
                        summary=result.summary,
                        topics_json=_to_json(result.topics),
                        relevance_score=result.relevance_score,
                        novelty_score=result.novelty_score,
                        cost_usd=result.cost_usd,
                        latency_ms=result.latency_ms,
                    )
                    existing_by_key[key] = existing
                else:
                    existing.model = result.model
                    existing.provider = result.provider
                    existing.summary = result.summary
                    existing.topics_json = _to_json(result.topics)
                    existing.relevance_score = result.relevance_score
                    existing.novelty_score = result.novelty_score
                    existing.cost_usd = result.cost_usd
                    existing.latency_ms = result.latency_ms

                self._upsert_item_stream_state(
                    session=session,
                    item_id=analysis_write.item_id,
                    stream=analysis_write.scope,
                    state=ITEM_STATE_ANALYZED,
                    existing_states=existing_states,
                )
                if analysis_write.mirror_item_state:
                    item = items_by_id.get(analysis_write.item_id)
                    if item is not None:
                        item.state = ITEM_STATE_ANALYZED
                        item.updated_at = utc_now()
                        session.add(item)

                session.add(existing)
                applied += 1

            if applied > 0:
                self._commit(session)
            return applied

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
