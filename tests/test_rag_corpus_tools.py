from __future__ import annotations

from recoleta.rag.corpus_tools import CorpusSpec


def test_corpus_spec_resolves_only_allowed_sources() -> None:
    spec = CorpusSpec.from_rag_sources(
        [
            {"doc_type": "item", "granularity": None},
            {"doc_type": "trend", "granularity": "day"},
        ]
    )

    assert spec.resolve_sources(doc_type="item", granularity=None) == [("item", None)]
    assert spec.resolve_sources(doc_type="trend", granularity=None) == [
        ("trend", "day")
    ]
    assert spec.resolve_sources(doc_type="trend", granularity="month") == []
