from __future__ import annotations

from datetime import datetime
from typing import Any, cast

from sqlalchemy import desc, func
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
from recoleta.storage_common import _to_json
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


def _existing_analyses_by_item_id(
    *,
    session: Session,
    item_ids: list[int],
) -> dict[int, Analysis]:
    statement = select(Analysis).where(cast(Any, Analysis.item_id).in_(item_ids))
    return {int(analysis.item_id): analysis for analysis in session.exec(statement)}


def _mirror_items_by_id(
    *,
    session: Session,
    mirror_item_ids: list[int],
) -> dict[int, Item]:
    if not mirror_item_ids:
        return {}
    item_statement = select(Item).where(cast(Any, Item.id).in_(mirror_item_ids))
    return {
        int(item.id): item
        for item in session.exec(item_statement)
        if item.id is not None
    }


def _analysis_row(
    *,
    analysis_write: AnalysisWrite,
    existing: Analysis | None,
) -> Analysis:
    result = analysis_write.result
    if existing is None:
        return Analysis(
            item_id=analysis_write.item_id,
            model=result.model,
            provider=result.provider,
            summary=result.summary,
            topics_json=_to_json(result.topics),
            relevance_score=result.relevance_score,
            novelty_score=result.novelty_score,
            cost_usd=result.cost_usd,
            latency_ms=result.latency_ms,
        )
    existing.model = result.model
    existing.provider = result.provider
    existing.summary = result.summary
    existing.topics_json = _to_json(result.topics)
    existing.relevance_score = result.relevance_score
    existing.novelty_score = result.novelty_score
    existing.cost_usd = result.cost_usd
    existing.latency_ms = result.latency_ms
    return existing


def _mirror_analyzed_item(
    *,
    session: Session,
    items_by_id: dict[int, Item],
    analysis_write: AnalysisWrite,
) -> None:
    if not analysis_write.mirror_item_state:
        return
    item = items_by_id.get(analysis_write.item_id)
    if item is None:
        return
    item.state = ITEM_STATE_ANALYZED
    item.updated_at = utc_now()
    session.add(item)


class AnalysisStoreMixin:
    engine: Any

    def _commit(self, session: Session) -> None: ...

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

        item_ids = sorted({analysis.item_id for analysis in normalized})
        mirror_item_ids = sorted(
            {
                analysis.item_id
                for analysis in normalized
                if analysis.mirror_item_state
            }
        )
        with Session(self.engine) as session:
            existing_by_key = _existing_analyses_by_item_id(
                session=session,
                item_ids=item_ids,
            )
            items_by_id = _mirror_items_by_id(
                session=session,
                mirror_item_ids=mirror_item_ids,
            )

            applied = 0
            for analysis_write in normalized:
                analysis_row = _analysis_row(
                    analysis_write=analysis_write,
                    existing=existing_by_key.get(analysis_write.item_id),
                )
                existing_by_key[analysis_write.item_id] = analysis_row
                _mirror_analyzed_item(
                    session=session,
                    items_by_id=items_by_id,
                    analysis_write=analysis_write,
                )

                session.add(analysis_row)
                applied += 1

            if applied > 0:
                self._commit(session)
            return applied

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
            statement = statement.order_by(
                desc(cast(Any, event_at)), desc(cast(Any, Item.id))
            ).offset(normalized_offset).limit(normalized_limit)
            return list(session.exec(statement))
