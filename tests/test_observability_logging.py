from __future__ import annotations

import io
import sys

from loguru import logger

import recoleta.observability as observability
from recoleta.observability import configure_process_logging


def test_configure_process_logging_strips_raw_ansi_sequences_from_sink_output(
    monkeypatch,
) -> None:
    """Regression: custom rich sink must not leak ANSI control sequences as text."""

    class _CapturingStderr(io.StringIO):
        def isatty(self) -> bool:
            return True

    stream = _CapturingStderr()
    monkeypatch.setattr(sys, "stderr", stream)

    configure_process_logging(level="INFO", log_json=False)
    try:
        logger.bind(module="pipeline.ingest", run_id="run-observability-test").info(
            "Ingest completed"
        )

        output = stream.getvalue()
        assert "Ingest" in output
        assert "completed" in output
        assert "\x1b[" not in output
        assert "[32m" not in output
        assert "[0m" not in output
    finally:
        logger.remove()


def test_get_rich_console_rebuilds_when_cached_stderr_is_closed(
    monkeypatch,
) -> None:
    """Regression: cached Console must not keep writing to a closed pytest capture stream."""

    class _CapturingStderr(io.StringIO):
        def isatty(self) -> bool:
            return False

    first_stream = _CapturingStderr()
    second_stream = _CapturingStderr()
    monkeypatch.setattr(sys, "stderr", first_stream)
    monkeypatch.setattr(observability, "_RICH_CONSOLE", None)

    first_console = observability.get_rich_console()
    first_stream.close()

    monkeypatch.setattr(sys, "stderr", second_stream)
    second_console = observability.get_rich_console()
    second_console.print("hello")

    assert second_console is not first_console
    assert second_console.file is second_stream
    assert "hello" in second_stream.getvalue()


def test_configured_rich_sink_rebuilds_console_after_stderr_changes(
    monkeypatch,
) -> None:
    """Regression: configured rich sink must not keep a closed pytest capture stream."""

    class _CapturingStderr(io.StringIO):
        def isatty(self) -> bool:
            return False

    first_stream = _CapturingStderr()
    second_stream = _CapturingStderr()
    monkeypatch.setattr(sys, "stderr", first_stream)
    monkeypatch.setattr(observability, "_RICH_CONSOLE", None)

    configure_process_logging(level="INFO", log_json=False)
    try:
        first_stream.close()
        monkeypatch.setattr(sys, "stderr", second_stream)
        logger.bind(module="pipeline.trends", run_id="run-after-close").info(
            "after-close log"
        )

        output = second_stream.getvalue()
        assert "after-close log" in output
        assert "Logging error" not in output
    finally:
        logger.remove()
