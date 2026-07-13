from __future__ import annotations

from recoleta.pipeline.service import PipelineService
from recoleta.storage import Repository
from tests.spec_support import FakeTelegramSender, _build_runtime


def _service() -> tuple[PipelineService, Repository]:
    settings, repository = _build_runtime()
    return (
        PipelineService(
            settings=settings,
            repository=repository,
            telegram_sender=FakeTelegramSender(),
        ),
        repository,
    )


def test_ingest_aggregate_metrics_use_one_transaction(configured_env) -> None:
    service, repository = _service()

    with repository.sql_diagnostics() as diagnostics:
        service.ingest(run_id="run-ingest-metric-batch", drafts=[])

    metrics = repository.list_metrics(run_id="run-ingest-metric-batch")
    names = {metric.name for metric in metrics}
    assert {"pipeline.ingest.items_total", "pipeline.ingest.duration_ms"} <= names
    assert diagnostics.commits_total == 1


def test_enrich_aggregate_metrics_use_one_transaction(configured_env) -> None:
    service, repository = _service()

    with repository.sql_diagnostics() as diagnostics:
        service.enrich(run_id="run-enrich-metric-batch", limit=10)

    metrics = repository.list_metrics(run_id="run-enrich-metric-batch")
    names = {metric.name for metric in metrics}
    assert {"pipeline.enrich.processed_total", "pipeline.enrich.duration_ms"} <= names
    assert diagnostics.commits_total == 1
