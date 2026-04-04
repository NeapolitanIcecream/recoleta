from __future__ import annotations

import importlib.util
import io
from pathlib import Path

import httpx


def _load_script_module():
    script_path = (
        Path(__file__).resolve().parents[1] / "scripts" / "ping_openai_embeddings.py"
    )
    spec = importlib.util.spec_from_file_location(
        "ping_openai_embeddings", script_path
    )
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_embedding_probe_reports_success_metadata() -> None:
    """Spec: successful probes should summarize embedding count, shape, and usage."""

    script = _load_script_module()

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == httpx.URL("http://llm.local/v1/embeddings")
        assert request.headers["authorization"] == "Bearer sk-test"
        assert request.headers["content-type"] == "application/json"
        assert request.read() == (
            b'{"model":"text-embedding-3-small","input":["probe text","probe text 2"],"encoding_format":"float"}'
        )
        return httpx.Response(
            200,
            json={
                "data": [
                    {"embedding": [0.1, 0.2, 0.3], "index": 0},
                    {"embedding": [0.4, 0.5, 0.6], "index": 1},
                ],
                "usage": {"prompt_tokens": 8, "total_tokens": 8},
            },
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        result = script._run_probe_attempt(
            client=client,
            request=script._ProbeAttemptRequest(
                url="http://llm.local/v1/embeddings",
                headers={
                    "Authorization": "Bearer sk-test",
                    "Content-Type": "application/json",
                },
                payload=script._build_payload(
                    model="text-embedding-3-small",
                    inputs=["probe text", "probe text 2"],
                    dimensions=None,
                ),
                attempt=1,
                timeout_seconds=12.0,
            ),
        )

    assert result["ok"] is True
    assert result["status_code"] == 200
    assert result["embeddings_count"] == 2
    assert result["embedding_dimensions"] == [3, 3]
    assert result["usage"] == {"prompt_tokens": 8, "total_tokens": 8}


def test_embedding_probe_surfaces_gateway_timeout_payload() -> None:
    """Spec: failed probes should preserve upstream timeout details in structured output."""

    script = _load_script_module()

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            504,
            json={
                "error": {
                    "message": "bad response status code 504",
                    "type": "gateway_timeout",
                    "code": "upstream_504",
                }
            },
        )

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        result = script._run_probe_attempt(
            client=client,
            request=script._ProbeAttemptRequest(
                url="http://llm.local/v1/embeddings",
                headers={
                    "Authorization": "Bearer sk-test",
                    "Content-Type": "application/json",
                },
                payload=script._build_payload(
                    model="text-embedding-3-small",
                    inputs=["probe text"],
                    dimensions=1536,
                ),
                attempt=2,
                timeout_seconds=12.0,
            ),
        )

    assert result["ok"] is False
    assert result["status_code"] == 504
    assert result["error_type"] == "gateway_timeout"
    assert result["error_code"] == "upstream_504"
    assert result["error_message"] == "bad response status code 504"


def test_embedding_probe_rejects_success_payload_without_vectors() -> None:
    """Regression: a 200 response without embeddings should still fail the probe."""

    script = _load_script_module()

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    with httpx.Client(transport=transport) as client:
        result = script._run_probe_attempt(
            client=client,
            request=script._ProbeAttemptRequest(
                url="http://llm.local/v1/embeddings",
                headers={
                    "Authorization": "Bearer sk-test",
                    "Content-Type": "application/json",
                },
                payload=script._build_payload(
                    model="text-embedding-3-small",
                    inputs=["probe text"],
                    dimensions=None,
                ),
                attempt=3,
                timeout_seconds=12.0,
            ),
        )

    assert result["ok"] is False
    assert result["status_code"] == 200
    assert result["error_type"] == "response_validation_error"
    assert result["error_code"] == "missing_embeddings"
    assert result["error_message"] == "response missing embedding vectors"


def test_embedding_probe_main_requires_api_key_env(monkeypatch) -> None:
    """Spec: missing credentials should fail fast before any network call."""

    script = _load_script_module()
    stdout = io.StringIO()
    stderr = io.StringIO()

    monkeypatch.delenv("RECOLETA_LLM_API_KEY", raising=False)

    exit_code = script.main(
        ["--base-url", "http://llm.local/v1"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == 2
    assert stdout.getvalue() == ""
    assert "missing api key env: RECOLETA_LLM_API_KEY" in stderr.getvalue()
