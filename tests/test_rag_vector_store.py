from __future__ import annotations

from pathlib import Path

from recoleta.rag.vector_store import LanceVectorStore


def test_vector_store_search_preserves_explicit_zero_search_tuning_values(
    tmp_path: Path,
) -> None:
    """Regression: explicit zero search tuning values should not be rewritten to defaults."""

    captured: dict[str, object] = {}

    class _FakeQuery:
        def metric(self, value: str) -> "_FakeQuery":
            captured["metric"] = value
            return self

        def where(self, value: str) -> "_FakeQuery":
            captured["where"] = value
            return self

        def refine_factor(self, value: int) -> "_FakeQuery":
            captured["refine_factor"] = value
            return self

        def nprobes(self, value: int) -> "_FakeQuery":
            captured["nprobes"] = value
            return self

        def limit(self, value: int) -> "_FakeQuery":
            captured["limit"] = value
            return self

        def to_list(self) -> list[dict[str, object]]:
            return []

    class _FakeTable:
        def search(self, query_vector: list[float]) -> _FakeQuery:
            captured["query_vector"] = list(query_vector)
            return _FakeQuery()

    store = LanceVectorStore(db_dir=tmp_path / "lancedb")
    store._table = _FakeTable()

    rows = store.search(
        query_vector=[1.0, 2.0],
        where="doc_type = 'item'",
        limit=5,
        refine_factor=0,
        nprobes=0,
    )

    assert rows == []
    assert captured["query_vector"] == [1.0, 2.0]
    assert captured["metric"] == "cosine"
    assert captured["where"] == "doc_type = 'item'"
    assert captured["limit"] == 5
    assert captured["refine_factor"] == 0
    assert captured["nprobes"] == 0


def test_vector_store_build_indices_preserves_explicit_zero_index_params(
    tmp_path: Path,
) -> None:
    """Regression: explicit zero index params should reach LanceDB unchanged."""

    captured: dict[str, object] = {}

    class _FakeTable:
        def create_index(self, **kwargs: object) -> None:
            captured.update(kwargs)

        def list_indices(self) -> list[object]:
            return []

    store = LanceVectorStore(db_dir=tmp_path / "lancedb")
    store._table = _FakeTable()

    result = store.build_indices(
        build_scalar_indices=False,
        vector_m=0,
        vector_ef_construction=0,
    )

    assert result["table_exists"] is True
    assert result["errors"] == []
    assert captured["m"] == 0
    assert captured["ef_construction"] == 0
