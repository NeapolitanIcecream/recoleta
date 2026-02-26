from __future__ import annotations

import io
import sys

from loguru import logger

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
    logger.bind(module="pipeline.ingest", run_id="run-observability-test").info("Ingest completed")

    output = stream.getvalue()
    assert "Ingest" in output
    assert "completed" in output
    assert "\x1b[" not in output
    assert "[32m" not in output
    assert "[0m" not in output
