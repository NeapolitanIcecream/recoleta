from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.rag.sync as rag_sync_module
import recoleta.rag.vector_store as vector_store_module


class _FakeHeartbeatMonitor:
    def raise_if_failed(self) -> None:
        return None


class _FakeRepo:
    def __init__(self) -> None:
        self.finished: list[tuple[str, bool]] = []
        self.metrics: list[SimpleNamespace] = []

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))

    def record_metric(
        self,
        *,
        run_id: str,
        name: str,
        value: float,
        unit: str | None = None,
    ) -> None:
        _ = run_id
        self.metrics.append(SimpleNamespace(name=name, value=value, unit=unit))

    def list_metrics(self, *, run_id: str):  # type: ignore[no-untyped-def]
        _ = run_id
        return list(self.metrics)


class _FakeSettings:
    log_json = False
    rag_lancedb_dir = "/tmp/recoleta-rag"
    trends_embedding_model = "openai/text-embedding-3-small"
    trends_embedding_dimensions = 1536
    trends_embedding_batch_max_inputs = 16
    trends_embedding_batch_max_chars = 8000
    trends_embedding_failure_mode = "continue"
    trends_embedding_max_errors = 0

    @staticmethod
    def llm_connection_config() -> object:
        return SimpleNamespace()


def test_rag_sync_vectors_prints_billing_report(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()
    console = recoleta.cli._runtime_symbols()["Console"]()
    fake_log = SimpleNamespace(
        exception=lambda *args, **kwargs: None,
        warning=lambda *args, **kwargs: None,
    )

    monkeypatch.setattr(
        recoleta.cli,
        "_begin_managed_run",
        lambda **_: (
            fake_settings,
            fake_repo,
            None,
            console,
            "run-rag-sync",
            "owner-token",
            fake_log,
            _FakeHeartbeatMonitor(),
        ),
    )
    monkeypatch.setattr(
        recoleta.cli,
        "_cleanup_managed_run",
        lambda **_: None,
    )

    class _FakeVectorStore:
        def __init__(self, **kwargs) -> None:  # type: ignore[no-untyped-def]
            self.kwargs = dict(kwargs)

    monkeypatch.setattr(vector_store_module, "LanceVectorStore", _FakeVectorStore)
    monkeypatch.setattr(
        vector_store_module,
        "embedding_table_name",
        lambda **_: "embeddings_test",
    )

    def _fake_sync_summary_vectors_in_period(**kwargs):  # type: ignore[no-untyped-def]
        repository = kwargs["repository"]
        run_id = kwargs["run_id"]
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_calls_total",
            value=3,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_prompt_tokens_total",
            value=240,
            unit="count",
        )
        repository.record_metric(
            run_id=run_id,
            name="pipeline.rag.sync.embedding_estimated_cost_usd",
            value=0.0024,
            unit="usd",
        )
        return {
            "chunks_total": 10,
            "embedded_total": 7,
            "skipped_total": 3,
            "embedding_calls_total": 3,
            "embedding_prompt_tokens_total": 240,
            "embedding_cost_usd_total": 0.0024,
        }

    monkeypatch.setattr(
        rag_sync_module,
        "sync_summary_vectors_in_period",
        _fake_sync_summary_vectors_in_period,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "rag",
            "sync-vectors",
            "--doc-type",
            "item",
            "--period-start",
            datetime(2026, 3, 1, tzinfo=UTC).isoformat(),
            "--period-end",
            datetime(2026, 3, 2, tzinfo=UTC).isoformat(),
        ],
    )

    assert result.exit_code == 0
    assert "rag sync completed" in result.stdout
    assert "Billing report" in result.stdout
    assert fake_repo.finished == [("run-rag-sync", True)]


def test_sync_summary_vectors_preserves_explicit_zero_limits_for_normalization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Regression: explicit zero limits should normalize to 1, not reset to broad defaults."""

    captured_limits: list[tuple[int, int]] = []

    class _MetricRepo:
        def record_metric(self, **_: object) -> None:
            return None

    def _fake_ensure_summary_vectors_for_period(*, request):  # type: ignore[no-untyped-def]
        captured_limits.append((int(request.limit), int(request.offset)))
        return {"chunks_total": 0}

    monkeypatch.setattr(
        rag_sync_module,
        "ensure_summary_vectors_for_period",
        _fake_ensure_summary_vectors_for_period,
    )

    stats = rag_sync_module.sync_summary_vectors_in_period(
        repository=_MetricRepo(),
        vector_store=SimpleNamespace(),
        run_id="run-rag-zero-limits",
        doc_type="item",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        embedding_model="openai/text-embedding-3-small",
        embedding_dimensions=1536,
        max_batch_inputs=16,
        max_batch_chars=8000,
        page_size=0,
        max_pages=0,
    )

    assert stats["page_size"] == 1
    assert captured_limits == [(1, 0)]
