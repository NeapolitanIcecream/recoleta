from __future__ import annotations

from pathlib import Path

from sqlmodel import Session, select

from recoleta.models import Analysis, ITEM_STATE_ANALYZED, Item
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, AnalysisWrite, ItemDraft


def _analysis_write(*, item_id: int, index: int) -> AnalysisWrite:
    return AnalysisWrite(
        item_id=item_id,
        result=AnalysisResult(
            model="test/model",
            provider="test",
            summary=f"summary-{index}",
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )


def test_save_analyses_batch_uses_constant_sql_statements(tmp_path: Path) -> None:
    repository = Repository(
        db_path=tmp_path / "recoleta.db",
        title_dedup_max_candidates=0,
    )
    repository.init_schema()
    item_ids: list[int] = []
    for index in range(100):
        item, _inserted = repository.upsert_item(
            ItemDraft.from_values(
                source="rss",
                source_item_id=f"item-{index}",
                canonical_url=f"https://example.com/{index}",
                title=f"Item {index}",
                authors=[],
                raw_metadata={},
            )
        )
        assert item.id is not None
        item_ids.append(item.id)

    with repository.sql_diagnostics() as diagnostics:
        applied = repository.save_analyses_batch(
            analyses=[
                _analysis_write(item_id=item_id, index=index)
                for index, item_id in enumerate(item_ids)
            ]
        )

    assert applied == 100
    assert diagnostics.queries_total == 2
    assert diagnostics.commits_total == 1
    with Session(repository.engine) as session:
        analyses = list(session.exec(select(Analysis)))
        items = list(session.exec(select(Item)))
    assert len(analyses) == 100
    assert {item.state for item in items} == {ITEM_STATE_ANALYZED}
