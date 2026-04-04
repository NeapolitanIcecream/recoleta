from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
import os
import sys
import time
from typing import Any, TextIO, TypedDict

import httpx


class _ProbeAttemptRequest(TypedDict):
    url: str
    headers: dict[str, str]
    payload: dict[str, Any]
    attempt: int
    timeout_seconds: float


class _ProbeCliConfig(TypedDict):
    model: str
    url: str
    headers: dict[str, str]
    payload: dict[str, Any]
    attempts: int
    sleep_seconds: float
    timeout_seconds: float


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ping an OpenAI-compatible embeddings endpoint."
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("RECOLETA_LLM_BASE_URL", ""),
        help="Base URL for the OpenAI-compatible endpoint.",
    )
    parser.add_argument(
        "--api-key-env",
        default="RECOLETA_LLM_API_KEY",
        help="Environment variable name holding the API key.",
    )
    parser.add_argument(
        "--model",
        default="text-embedding-3-small",
        help="Embedding model name to send.",
    )
    parser.add_argument(
        "--input",
        action="append",
        default=[],
        help="Input text to embed. Repeat to send multiple inputs. Defaults to a built-in probe string.",
    )
    parser.add_argument(
        "--dimensions",
        type=int,
        default=None,
        help="Optional dimensions override for compatible models.",
    )
    parser.add_argument(
        "--attempts",
        type=int,
        default=1,
        help="How many sequential probe attempts to run.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=0.0,
        help="Delay between attempts.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds.",
    )
    return parser


def _normalize_base_url(raw: str) -> str:
    cleaned = str(raw or "").strip()
    if not cleaned:
        raise ValueError("base URL is required")
    return cleaned.rstrip("/")


def _normalize_inputs(raw_inputs: Sequence[str]) -> list[str]:
    cleaned = [str(value).strip() for value in raw_inputs if str(value).strip()]
    return cleaned or ["recoleta embedding probe"]


def _build_payload(
    *,
    model: str,
    inputs: list[str],
    dimensions: int | None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": str(model).strip(),
        "input": inputs,
        "encoding_format": "float",
    }
    if dimensions is not None:
        payload["dimensions"] = int(dimensions)
    return payload


def _extract_json_error_fields(data: Any) -> tuple[str | None, str | None, str | None]:
    if not isinstance(data, dict):
        return None, None, None
    error = data.get("error")
    if not isinstance(error, dict):
        return None, None, None
    message = str(error.get("message") or "").strip() or None
    error_type = str(error.get("type") or "").strip() or None
    error_code = str(error.get("code") or "").strip() or None
    return message, error_type, error_code


def _embedding_dimensions(data: Any) -> list[int]:
    if not isinstance(data, list):
        return []
    dimensions: list[int] = []
    for entry in data:
        if not isinstance(entry, dict):
            continue
        embedding = entry.get("embedding")
        if isinstance(embedding, list):
            dimensions.append(len(embedding))
    return dimensions


def _mark_response_validation_error(
    result: dict[str, Any],
    *,
    data: Any,
    message: str,
    code: str,
) -> dict[str, Any]:
    result["ok"] = False
    result["error_type"] = "response_validation_error"
    result["error_code"] = code
    result["error_message"] = message
    result["body_excerpt"] = json.dumps(data, ensure_ascii=False)[:1000]
    return result


def _run_probe_attempt(
    *,
    client: httpx.Client,
    request: _ProbeAttemptRequest,
) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        response = _post_probe_request(client=client, request=request)
    except httpx.HTTPError as exc:
        return _build_http_error_result(
            request=request,
            elapsed_ms=int((time.perf_counter() - started) * 1000),
            exc=exc,
        )

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    result = _build_probe_result(
        request=request,
        response=response,
        elapsed_ms=elapsed_ms,
    )
    if not _response_is_json(response):
        return _finalize_non_json_result(result=result, response=response)

    try:
        data = response.json()
    except Exception as exc:  # noqa: BLE001
        return _mark_probe_json_decode_failure(result=result, response=response, exc=exc)

    _attach_embedding_metadata(result=result, data=data)
    if response.is_success:
        return _validate_successful_probe_result(
            result=result,
            data=data,
            payload=request["payload"],
        )
    return _attach_probe_failure_details(result=result, response=response, data=data)


def _post_probe_request(
    *,
    client: httpx.Client,
    request: _ProbeAttemptRequest,
) -> httpx.Response:
    return client.post(
        request["url"],
        headers=request["headers"],
        json=request["payload"],
        timeout=httpx.Timeout(
            request["timeout_seconds"],
            connect=min(10.0, request["timeout_seconds"]),
        ),
    )


def _build_http_error_result(
    *,
    request: _ProbeAttemptRequest,
    elapsed_ms: int,
    exc: httpx.HTTPError,
) -> dict[str, Any]:
    return {
        "attempt": request["attempt"],
        "ok": False,
        "status_code": None,
        "elapsed_ms": elapsed_ms,
        "error_type": type(exc).__name__,
        "error_code": None,
        "error_message": str(exc),
    }


def _build_probe_result(
    *,
    request: _ProbeAttemptRequest,
    response: httpx.Response,
    elapsed_ms: int,
) -> dict[str, Any]:
    return {
        "attempt": request["attempt"],
        "ok": response.is_success,
        "status_code": response.status_code,
        "elapsed_ms": elapsed_ms,
    }


def _response_is_json(response: httpx.Response) -> bool:
    content_type = response.headers.get("content-type", "")
    return "application/json" in content_type


def _finalize_non_json_result(
    *,
    result: dict[str, Any],
    response: httpx.Response,
) -> dict[str, Any]:
    text = response.text.strip()
    if text:
        result["body_excerpt"] = text[:1000]
    if not response.is_success:
        result["error_message"] = text[:1000] or f"HTTP {response.status_code}"
    return result


def _mark_probe_json_decode_failure(
    *,
    result: dict[str, Any],
    response: httpx.Response,
    exc: Exception,
) -> dict[str, Any]:
    result["error_type"] = type(exc).__name__
    result["error_message"] = f"json decode failed: {exc}"
    result["body_excerpt"] = response.text[:1000]
    result["ok"] = False
    return result


def _attach_embedding_metadata(*, result: dict[str, Any], data: Any) -> None:
    embeddings = data.get("data") if isinstance(data, dict) else None
    usage = data.get("usage") if isinstance(data, dict) else None
    dimensions = _embedding_dimensions(embeddings)
    if dimensions:
        result["embeddings_count"] = len(dimensions)
        result["embedding_dimensions"] = dimensions
    if isinstance(usage, dict):
        result["usage"] = usage


def _validate_successful_probe_result(
    *,
    result: dict[str, Any],
    data: Any,
    payload: dict[str, Any],
) -> dict[str, Any]:
    dimensions = list(result.get("embedding_dimensions") or [])
    expected_count = (
        len(payload["input"]) if isinstance(payload.get("input"), list) else 0
    )
    if not dimensions:
        return _mark_response_validation_error(
            result,
            data=data,
            message="response missing embedding vectors",
            code="missing_embeddings",
        )
    if expected_count and len(dimensions) != expected_count:
        return _mark_response_validation_error(
            result,
            data=data,
            message=(
                f"embedding count mismatch: expected {expected_count}, got {len(dimensions)}"
            ),
            code="embedding_count_mismatch",
        )
    if any(int(dimension) <= 0 for dimension in dimensions):
        return _mark_response_validation_error(
            result,
            data=data,
            message="response contained empty embedding vectors",
            code="empty_embedding_vector",
        )
    return result


def _attach_probe_failure_details(
    *,
    result: dict[str, Any],
    response: httpx.Response,
    data: Any,
) -> dict[str, Any]:
    error_message, error_type, error_code = _extract_json_error_fields(data)
    result["error_message"] = error_message or f"HTTP {response.status_code}"
    result["error_type"] = error_type
    result["error_code"] = error_code
    result["body_excerpt"] = json.dumps(data, ensure_ascii=False)[:1000]
    return result


def _parse_positive_int(value: Any, *, name: str) -> int:
    normalized = int(value)
    if normalized <= 0:
        raise ValueError(f"{name} must be > 0")
    return normalized


def _parse_non_negative_float(value: Any, *, name: str) -> float:
    normalized = float(value)
    if normalized < 0:
        raise ValueError(f"{name} must be >= 0")
    return normalized


def _parse_positive_float(value: Any, *, name: str) -> float:
    normalized = float(value)
    if normalized <= 0:
        raise ValueError(f"{name} must be > 0")
    return normalized


def _build_probe_headers(*, api_key: str) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }


def _build_cli_config(args: argparse.Namespace) -> _ProbeCliConfig:
    base_url = _normalize_base_url(args.base_url)
    api_key = os.getenv(args.api_key_env, "").strip()
    if not api_key:
        raise ValueError(f"missing api key env: {args.api_key_env}")
    attempts = _parse_positive_int(args.attempts, name="attempts")
    timeout_seconds = _parse_positive_float(
        args.timeout_seconds,
        name="timeout_seconds",
    )
    sleep_seconds = _parse_non_negative_float(
        args.sleep_seconds,
        name="sleep_seconds",
    )
    inputs = _normalize_inputs(args.input)
    return _ProbeCliConfig(
        model=str(args.model).strip(),
        url=f"{base_url}/embeddings",
        headers=_build_probe_headers(api_key=api_key),
        payload=_build_payload(
            model=args.model,
            inputs=inputs,
            dimensions=args.dimensions,
        ),
        attempts=attempts,
        sleep_seconds=sleep_seconds,
        timeout_seconds=timeout_seconds,
    )


def _run_probe_series(
    *,
    client: httpx.Client,
    config: _ProbeCliConfig,
    out: TextIO,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for attempt in range(1, config["attempts"] + 1):
        result = _run_probe_attempt(
            client=client,
            request=_ProbeAttemptRequest(
                url=config["url"],
                headers=config["headers"],
                payload=config["payload"],
                attempt=attempt,
                timeout_seconds=config["timeout_seconds"],
            ),
        )
        print(json.dumps(result, ensure_ascii=False), file=out)
        results.append(result)
        if attempt < config["attempts"] and config["sleep_seconds"] > 0:
            time.sleep(config["sleep_seconds"])
    return results


def _build_probe_summary(
    *,
    model: str,
    url: str,
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    elapsed_values = [int(result.get("elapsed_ms") or 0) for result in results]
    success_total = sum(1 for result in results if bool(result.get("ok")))
    return {
        "kind": "summary",
        "model": model,
        "url": url,
        "attempts_total": len(results),
        "success_total": success_total,
        "failure_total": len(results) - success_total,
        "elapsed_ms_min": min(elapsed_values) if elapsed_values else 0,
        "elapsed_ms_max": max(elapsed_values) if elapsed_values else 0,
        "elapsed_ms_avg": int(sum(elapsed_values) / len(elapsed_values))
        if elapsed_values
        else 0,
    }


def main(
    argv: Sequence[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout or sys.stdout
    err = stderr or sys.stderr
    args = _build_parser().parse_args(list(argv) if argv is not None else None)

    try:
        config = _build_cli_config(args)
    except ValueError as exc:
        message = str(exc)
        if not message.startswith("missing api key env:"):
            message = f"invalid base url: {message}" if message == "base URL is required" else message
        print(message, file=err)
        return 2

    with httpx.Client() as client:
        results = _run_probe_series(client=client, config=config, out=out)
    summary = _build_probe_summary(
        model=config["model"],
        url=config["url"],
        results=results,
    )
    print(json.dumps(summary, ensure_ascii=False), file=out)
    return 0 if summary["success_total"] == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
