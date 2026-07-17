from __future__ import annotations

import io
import logging
import os
from pathlib import Path
import subprocess
import sys

from loguru import logger

import recoleta.observability as observability
from recoleta.observability import configure_process_logging


_LAZY_LITELLM_LOGGING_SCRIPT = """
import logging
import os

from recoleta.observability import configure_process_logging

configure_process_logging(level=os.environ["RECOLETA_TEST_LOG_LEVEL"], log_json=False)
import litellm

_ = litellm
dependency_log = logging.getLogger("LiteLLM")
dependency_log.debug("lazy-litellm-debug-marker")
dependency_log.info("lazy-litellm-info-marker")
dependency_log.warning("lazy-litellm-warning-marker")
"""


def _run_lazy_litellm_logging(*, level: str) -> str:
    environment = dict(os.environ)
    environment.pop("LITELLM_LOG", None)
    environment["NO_COLOR"] = "1"
    environment["RECOLETA_TEST_LOG_LEVEL"] = level
    completed = subprocess.run(
        [sys.executable, "-c", _LAZY_LITELLM_LOGGING_SCRIPT],
        cwd=Path(__file__).resolve().parents[1],
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert completed.returncode == 0, completed.stderr
    return completed.stdout + completed.stderr


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


def test_default_logging_suppresses_dependency_info_but_keeps_recoleta_info(
    monkeypatch,
) -> None:
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stream)
    monkeypatch.setattr(observability, "_RICH_CONSOLE", None)

    configure_process_logging(level="INFO", log_json=False)
    try:
        logging.getLogger("LiteLLM").info("litellm request details")
        logging.getLogger("httpx").info("httpx request details")
        logging.getLogger("httpcore.connection").info("httpcore connection details")
        logging.getLogger("recoleta.test").info("recoleta stage summary")
        logging.getLogger("httpx").warning("httpx retry warning")

        output = stream.getvalue()
        assert "litellm request details" not in output
        assert "httpx request details" not in output
        assert "httpcore connection details" not in output
        assert "recoleta" in output
        assert "stage summary" in output
        assert "retry" in output
        assert "warning" in output
    finally:
        logger.remove()


def test_debug_logging_explicitly_enables_dependency_details(monkeypatch) -> None:
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stream)
    monkeypatch.setattr(observability, "_RICH_CONSOLE", None)

    configure_process_logging(level="DEBUG", log_json=False)
    try:
        logging.getLogger("LiteLLM").debug("litellm debug details")
        logging.getLogger("httpx").info("httpx verbose request")
        logging.getLogger("httpcore.connection").debug("httpcore debug details")

        output = stream.getvalue()
        assert "litellm debug" in output
        assert "details" in output
        assert "httpx verbose" in output
        assert "request" in output
        assert "httpcore debug details" in output
    finally:
        logger.remove()


def test_lazy_litellm_import_respects_default_dependency_filter() -> None:
    output = _run_lazy_litellm_logging(level="INFO")

    assert "lazy-litellm-debug-marker" not in output
    assert "lazy-litellm-info-marker" not in output
    assert output.count("lazy-litellm-warning-marker") == 1


def test_lazy_litellm_import_uses_unified_debug_logging_without_duplicates() -> None:
    output = _run_lazy_litellm_logging(level="DEBUG")

    assert output.count("lazy-litellm-debug-marker") == 1
    assert output.count("lazy-litellm-info-marker") == 1
    assert output.count("lazy-litellm-warning-marker") == 1


def test_explicit_litellm_log_setting_is_preserved(monkeypatch) -> None:
    monkeypatch.setenv("LITELLM_LOG", "ERROR")

    configure_process_logging(level="INFO", log_json=False)
    try:
        assert os.environ["LITELLM_LOG"] == "ERROR"
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
