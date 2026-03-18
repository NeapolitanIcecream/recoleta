from __future__ import annotations

import httpx

from recoleta.pipeline.artifacts import classify_exception, summarize_artifact_payload


def test_classify_exception_marks_http_401_as_retryable_auth_failure() -> None:
    """Regression: run-scoped auth failures must not poison stream state forever."""

    request = httpx.Request("POST", "https://api.example.com/v1/chat/completions")
    response = httpx.Response(status_code=401, request=request)
    exc = httpx.HTTPStatusError("401 invalid token", request=request, response=response)

    classification = classify_exception(exc)

    assert classification == {
        "error_category": "auth",
        "retryable": True,
        "http_status": 401,
    }


def test_summarize_artifact_payload_extracts_error_context_details() -> None:
    summary = summarize_artifact_payload(
        kind="error_context",
        payload={
            "stage": "publish",
            "error_type": "HTTPStatusError",
            "error_message": "401 invalid token for upstream provider",
            "error_category": "auth",
            "retryable": True,
            "http_status": 401,
        },
    )

    assert summary == {
        "error_type": "HTTPStatusError",
        "error_category": "auth",
        "http_status": 401,
        "retryable": True,
        "message_excerpt": "401 invalid token for upstream provider",
    }


def test_summarize_artifact_payload_extracts_pass_output_failure_details() -> None:
    summary = summarize_artifact_payload(
        kind="pass_output_failure",
        payload={
            "stage": "trends",
            "failure": {
                "error_type": "IntegrityError",
                "error_message": "UNIQUE constraint failed: pass_outputs.content_hash",
            },
        },
    )

    assert summary == {
        "error_type": "IntegrityError",
        "message_excerpt": "UNIQUE constraint failed: pass_outputs.content_hash",
    }
