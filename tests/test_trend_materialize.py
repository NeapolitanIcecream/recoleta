from __future__ import annotations

from datetime import UTC, datetime
import re

from recoleta.trend_materialize import materialize_trend_note_payload
from recoleta.trends import TrendPayload
from recoleta.types import ItemDraft
from tests.spec_support import _build_runtime


def _seed_item_doc(*, repository, source_item_id: str, title: str, canonical_url: str) -> int:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id=source_item_id,
        canonical_url=canonical_url,
        title=title,
        authors=["Alice"],
        published_at=datetime(2026, 3, 2, tzinfo=UTC),
        raw_metadata={"source": "test"},
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    doc = repository.upsert_document_for_item(item=item)
    assert doc.id is not None
    return int(doc.id)


def test_materialize_trend_note_payload_rewrites_doc_refs_and_canonical_links(
    configured_env, tmp_path
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    doc_id = _seed_item_doc(
        repository=repository,
        source_item_id="robometer-1",
        title="Robometer: Scaling General-Purpose Robotic Reward Models",
        canonical_url="https://example.com/robometer",
    )

    materialized = materialize_trend_note_payload(
        repository=repository,
        payload=TrendPayload.model_validate(
            {
                "title": "Daily Trend",
                "granularity": "day",
                "period_start": datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 3, 3, tzinfo=UTC).isoformat(),
                "overview_md": (
                    f"See doc_id: {doc_id}, chunk 0 and "
                    "[Robometer](https://example.com/robometer)."
                ),
                "topics": ["agents"],
                "clusters": [
                    {
                        "title": "Reward loops",
                        "content_md": f"Follow doc_id {doc_id}, chunk 0 in the item note.",
                        "evidence_refs": [
                            {
                                "doc_id": doc_id,
                                "chunk_index": 0,
                                "reason": f"doc_id {doc_id}, chunk 0 anchors the example.",
                            }
                        ],
                    }
                ],
            }
        ),
        markdown_output_dir=tmp_path,
        output_language="English",
    )

    assert "../Inbox/" in materialized.overview_md
    assert "https://example.com/robometer" not in materialized.overview_md
    assert "doc_id" not in materialized.overview_md
    assert re.search(r"\bchunk(?:_index)?\b", materialized.overview_md, flags=re.I) is None

    cluster = materialized.clusters[0]
    assert "../Inbox/" in cluster["content_md"]
    assert "doc_id" not in cluster["content_md"]
    assert "anchors the example." in cluster["evidence_refs"][0]["reason"]
    assert "doc_id" not in cluster["evidence_refs"][0]["reason"]
    assert cluster["evidence_refs"][0]["title"].startswith("Robometer")
    assert cluster["evidence_refs"][0]["note_href"].startswith("../Inbox/")


def test_materialize_trend_note_payload_deduplicates_cluster_evidence_by_document(
    configured_env, tmp_path
) -> None:
    _ = configured_env
    _, repository = _build_runtime()

    doc_id = _seed_item_doc(
        repository=repository,
        source_item_id="paper-1",
        title="Representative Paper Should Appear Once",
        canonical_url="https://example.com/paper-1",
    )

    materialized = materialize_trend_note_payload(
        repository=repository,
        payload=TrendPayload.model_validate(
            {
                "title": "Daily Trend",
                "granularity": "day",
                "period_start": datetime(2026, 3, 9, tzinfo=UTC).isoformat(),
                "period_end": datetime(2026, 3, 10, tzinfo=UTC).isoformat(),
                "overview_md": "A short trend overview.",
                "topics": ["agents"],
                "clusters": [
                    {
                        "title": "Evidence consolidation",
                        "content_md": "One item should appear once even if multiple chunks matched.",
                        "evidence_refs": [
                            {
                                "doc_id": doc_id,
                                "chunk_index": 0,
                                "reason": "The summary chunk anchors the point.",
                            },
                            {
                                "doc_id": doc_id,
                                "chunk_index": 1,
                                "reason": "A later chunk repeats the same paper.",
                            },
                        ],
                    }
                ],
            }
        ),
        markdown_output_dir=tmp_path,
        output_language="English",
    )

    cluster = materialized.clusters[0]
    assert len(cluster["evidence_refs"]) == 1
    assert cluster["evidence_refs"][0]["doc_id"] == doc_id
    assert cluster["evidence_refs"][0]["chunk_index"] == 0
    assert cluster["evidence_refs"][0]["reason"] == "The summary chunk anchors the point."
