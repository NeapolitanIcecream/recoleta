from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from sqlalchemy import and_, desc, func, or_, update
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlmodel import Session, select

from recoleta.models import (
    Analysis,
    Item,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
)
from recoleta.storage.common import _to_json
from recoleta.types import (
    AnalysisResult,
    AnalysisWrite,
    utc_now,
)


def _normalized_analysis_write(analysis: AnalysisWrite) -> AnalysisWrite | None:
    try:
        item_id = int(analysis.item_id)
    except Exception:
        return None
    if item_id <= 0:
        return None
    return AnalysisWrite(
        item_id=item_id,
        result=analysis.result,
        mirror_item_state=bool(analysis.mirror_item_state),
    )


def _normalized_analysis_writes(analyses: list[AnalysisWrite]) -> list[AnalysisWrite]:
    normalized: list[AnalysisWrite] = []
    seen: dict[int, int] = {}
    for analysis in analyses:
        normalized_write = _normalized_analysis_write(analysis)
        if normalized_write is None:
            continue
        existing_index = seen.get(normalized_write.item_id)
        if existing_index is None:
            seen[normalized_write.item_id] = len(normalized)
            normalized.append(normalized_write)
        else:
            normalized[existing_index] = normalized_write
    return normalized


def _analysis_upsert_rows(analyses: list[AnalysisWrite]) -> list[dict[str, Any]]:
    created_at = utc_now()
    return [
        {
            "item_id": analysis.item_id,
            "model": analysis.result.model,
            "provider": analysis.result.provider,
            "summary": analysis.result.summary,
            "topics_json": _to_json(analysis.result.topics),
            "relevance_score": analysis.result.relevance_score,
            "novelty_score": analysis.result.novelty_score,
            "cost_usd": analysis.result.cost_usd,
            "latency_ms": analysis.result.latency_ms,
            "created_at": created_at,
        }
        for analysis in analyses
    ]


def _bulk_upsert_analyses(*, session: Session, analyses: list[AnalysisWrite]) -> None:
    table = cast(Any, Analysis).__table__
    statement = sqlite_insert(table).values(_analysis_upsert_rows(analyses))
    excluded = statement.excluded
    session.execute(
        statement.on_conflict_do_update(
            index_elements=[table.c.item_id],
            set_={
                "model": excluded.model,
                "provider": excluded.provider,
                "summary": excluded.summary,
                "topics_json": excluded.topics_json,
                "relevance_score": excluded.relevance_score,
                "novelty_score": excluded.novelty_score,
                "cost_usd": excluded.cost_usd,
                "latency_ms": excluded.latency_ms,
            },
        )
    )


def _bulk_mirror_analyzed_items(
    *, session: Session, mirror_item_ids: list[int]
) -> None:
    if not mirror_item_ids:
        return
    session.execute(
        update(cast(Any, Item).__table__)
        .where(cast(Any, Item).__table__.c.id.in_(mirror_item_ids))
        .values(state=ITEM_STATE_ANALYZED, updated_at=utc_now())
    )


def _llm_analysis_candidate_states(*, triage_required: bool) -> list[str]:
    states = [ITEM_STATE_RETRYABLE_FAILED]
    if triage_required:
        states.append(ITEM_STATE_TRIAGED)
    else:
        states.append(ITEM_STATE_ENRICHED)
    return states


def _llm_analysis_candidate_filter(
    *,
    triage_required: bool,
    llm_model: str | None,
) -> tuple[Any, bool]:
    states = _llm_analysis_candidate_states(triage_required=triage_required)
    state_candidate = cast(Any, Item.state).in_(states)
    normalized_model = str(llm_model or "").strip()
    if not normalized_model:
        return state_candidate, False
    stale_model_candidate = and_(
        cast(Any, Item.state).in_([ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]),
        cast(Any, Analysis.model) != normalized_model,
    )
    return or_(state_candidate, stale_model_candidate), True


class AnalysisStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

    def count_items_for_llm_analysis_by_state(
        self,
        *,
        triage_required: bool,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        llm_model: str | None = None,
    ) -> dict[str, int]:
        candidate_filter, requires_analysis_join = _llm_analysis_candidate_filter(
            triage_required=triage_required,
            llm_model=llm_model,
        )
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = select(Item.state, func.count())
            if requires_analysis_join:
                statement = statement.outerjoin(
                    Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id)
                )
            statement = statement.where(candidate_filter)
            if period_start is not None and period_end is not None:
                statement = statement.where(
                    event_at >= period_start, event_at < period_end
                )
            statement = statement.group_by(cast(Any, Item.state))
            return {
                str(state): int(total or 0)
                for state, total in session.exec(statement).all()
            }

    def list_items_for_llm_analysis(
        self,
        *,
        limit: int,
        triage_required: bool,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
        llm_model: str | None = None,
    ) -> list[Item]:
        candidate_filter, requires_analysis_join = _llm_analysis_candidate_filter(
            triage_required=triage_required,
            llm_model=llm_model,
        )

        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = select(Item)
            if requires_analysis_join:
                statement = statement.outerjoin(
                    Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id)
                )
            statement = statement.where(candidate_filter)
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
        mirror_item_state: bool = True,
    ) -> Analysis:
        with Session(self.engine) as session:
            analysis = session.exec(
                select(Analysis).where(Analysis.item_id == item_id)
            ).first()
            if analysis is None:
                analysis = Analysis(
                    item_id=item_id,
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
        normalized = _normalized_analysis_writes(analyses)
        if not normalized:
            return 0

        mirror_item_ids = sorted(
            {analysis.item_id for analysis in normalized if analysis.mirror_item_state}
        )
        with Session(self.engine) as session:
            _bulk_upsert_analyses(session=session, analyses=normalized)
            _bulk_mirror_analyzed_items(
                session=session,
                mirror_item_ids=mirror_item_ids,
            )
            self._commit(session)
        return len(normalized)

    def list_items_for_publish(
        self,
        *,
        limit: int,
        min_relevance_score: float,
        period_start: datetime | None = None,
        period_end: datetime | None = None,
    ) -> list[tuple[Item, Analysis]]:
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at),
                cast(Any, Item.created_at),
            )
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(
                    cast(Any, Analysis.relevance_score) >= min_relevance_score,
                    cast(Any, Item.state) == ITEM_STATE_ANALYZED,
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
            self._commit(session)

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
        llm_model: str | None = None,
    ) -> list[tuple[Item, Analysis]]:
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(
                    event_at >= period_start,
                    event_at < period_end,
                    cast(Any, Item.state).in_(
                        [ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]
                    ),
                )
            )
            normalized_model = str(llm_model or "").strip()
            if normalized_model:
                statement = statement.where(Analysis.model == normalized_model)
            statement = (
                statement.order_by(desc(cast(Any, event_at)), desc(cast(Any, Item.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))
