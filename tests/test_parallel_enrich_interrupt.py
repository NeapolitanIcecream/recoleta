from __future__ import annotations

import threading
import time
from contextlib import contextmanager
from types import SimpleNamespace
from typing import Any, Iterable, Iterator, cast

import pytest

import recoleta.pipeline as pipeline
from recoleta.pipeline import PipelineService


class _FakeSqlDiag:
    queries_total = 0
    commits_total = 0


class _FakeRepository:
    def __init__(self, items: list[Any]) -> None:
        self._items = items

    @contextmanager
    def sql_diagnostics(self) -> Iterator[_FakeSqlDiag]:
        yield _FakeSqlDiag()

    def list_items_for_analysis(self, *, limit: int) -> list[Any]:  # noqa: ARG002
        return list(self._items)

    def mark_item_enriched(self, *, item_id: int) -> None:  # noqa: ARG002
        return

    def mark_item_failed(self, *, item_id: int) -> None:  # noqa: ARG002
        return

    def mark_item_retryable_failed(self, *, item_id: int) -> None:  # noqa: ARG002
        return

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:  # noqa: ARG002
        return

    def add_artifact(
        self, *, run_id: str, item_id: int | None, kind: str, path: str
    ) -> None:  # noqa: ARG002
        return


class _InterruptingExecutor(pipeline.ThreadPoolExecutor):
    """Simulate a KeyboardInterrupt that prevents executor __exit__ from waiting."""

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool | None:  # noqa: ANN401
        if exc_type is KeyboardInterrupt:
            try:
                self.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                self.shutdown(wait=False)
            return False
        return super().__exit__(exc_type, exc, tb)


def _raise_keyboard_interrupt(_: Any) -> Any:  # noqa: ANN401
    raise KeyboardInterrupt


def test_parallel_enrich_does_not_close_http_clients_while_workers_running() -> None:
    """Regression: Ctrl-C during parallel enrich must not close http clients mid-request."""

    class _FakeHttpClient:
        def __init__(self, *_: Any, **__: Any) -> None:
            self.is_closed = False

        def close(self) -> None:
            self.is_closed = True

        def __enter__(self) -> "_FakeHttpClient":
            return self

        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> None:  # noqa: ANN401
            self.close()

    item = SimpleNamespace(id=1, source="arxiv")
    repo = _FakeRepository(items=[item])
    settings = SimpleNamespace(
        telegram_bot_token=None,
        telegram_chat_id=None,
        llm_model="test/fake-model",
        llm_output_language=None,
        analyze_content_max_chars=32768,
        publish_targets=[],
        write_debug_artifacts=False,
        artifacts_dir=None,
        sources=SimpleNamespace(
            arxiv=SimpleNamespace(
                enrich_method="html_document",
                html_document_enable_parallel=True,
                html_document_max_concurrency=2,
                html_document_requests_per_second=0.0,
            )
        ),
    )

    saw_closed_client = {"value": False}
    worker_started = threading.Event()

    def _ensure_item_content(  # noqa: ANN001
        self: PipelineService,
        *,
        client: Any,
        item: Any,  # noqa: ARG001
        log: Any,  # noqa: ARG001
        diag: dict[str, int],  # noqa: ARG001
        arxiv_html_throttle: Any,  # noqa: ARG001
    ) -> tuple[Any, bool]:
        worker_started.set()
        time.sleep(0.2)
        if getattr(client, "is_closed", False):
            saw_closed_client["value"] = True
        return None, True

    def _as_completed_interrupt(_: Iterable[Any]) -> Any:  # noqa: ANN401
        def _gen() -> Any:  # noqa: ANN401
            worker_started.wait(timeout=2.0)
            raise KeyboardInterrupt
            yield  # pragma: no cover

        return _gen()

    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(
        PipelineService, "_ensure_item_content", _ensure_item_content, raising=True
    )
    monkeypatch.setattr(
        pipeline, "ThreadPoolExecutor", _InterruptingExecutor, raising=True
    )
    monkeypatch.setattr(pipeline, "as_completed", _as_completed_interrupt, raising=True)
    monkeypatch.setattr(pipeline.httpx, "Client", _FakeHttpClient, raising=True)
    try:
        dummy_triage = SimpleNamespace()
        service = PipelineService(
            settings=cast(Any, settings),
            repository=cast(Any, repo),
            analyzer=None,
            triage=cast(Any, dummy_triage),
        )
        with pytest.raises(KeyboardInterrupt):
            service.enrich(run_id="run-1", limit=1)
    finally:
        monkeypatch.undo()

    # Give any in-flight worker a chance to observe a closed client.
    time.sleep(0.4)

    assert saw_closed_client["value"] is False
