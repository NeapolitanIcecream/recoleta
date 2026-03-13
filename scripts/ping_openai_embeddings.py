from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
import os
import sys
import time
from typing import Any, TextIO

import httpx


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
    url: str,
    headers: dict[str, str],
    payload: dict[str, Any],
    attempt: int,
    timeout_seconds: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    try:
        response = client.post(
            url,
            headers=headers,
            json=payload,
            timeout=httpx.Timeout(timeout_seconds, connect=min(10.0, timeout_seconds)),
        )
    except httpx.HTTPError as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return {
            "attempt": attempt,
            "ok": False,
            "status_code": None,
            "elapsed_ms": elapsed_ms,
            "error_type": type(exc).__name__,
            "error_code": None,
            "error_message": str(exc),
        }

    elapsed_ms = int((time.perf_counter() - started) * 1000)
    result: dict[str, Any] = {
        "attempt": attempt,
        "ok": response.is_success,
        "status_code": response.status_code,
        "elapsed_ms": elapsed_ms,
    }

    content_type = response.headers.get("content-type", "")
    if "application/json" not in content_type:
        text = response.text.strip()
        if text:
            result["body_excerpt"] = text[:1000]
        if not response.is_success:
            result["error_message"] = text[:1000] or f"HTTP {response.status_code}"
        return result

    try:
        data = response.json()
    except Exception as exc:  # noqa: BLE001
        result["error_type"] = type(exc).__name__
        result["error_message"] = f"json decode failed: {exc}"
        result["body_excerpt"] = response.text[:1000]
        result["ok"] = False
        return result

    embeddings = data.get("data") if isinstance(data, dict) else None
    usage = data.get("usage") if isinstance(data, dict) else None
    dimensions = _embedding_dimensions(embeddings)
    if dimensions:
        result["embeddings_count"] = len(dimensions)
        result["embedding_dimensions"] = dimensions
    if isinstance(usage, dict):
        result["usage"] = usage

    expected_count = len(payload["input"]) if isinstance(payload.get("input"), list) else 0
    if response.is_success and not dimensions:
        return _mark_response_validation_error(
            result,
            data=data,
            message="response missing embedding vectors",
            code="missing_embeddings",
        )
    if response.is_success and expected_count and len(dimensions) != expected_count:
        return _mark_response_validation_error(
            result,
            data=data,
            message=(
                f"embedding count mismatch: expected {expected_count}, got {len(dimensions)}"
            ),
            code="embedding_count_mismatch",
        )
    if response.is_success and any(dimension <= 0 for dimension in dimensions):
        return _mark_response_validation_error(
            result,
            data=data,
            message="response contained empty embedding vectors",
            code="empty_embedding_vector",
        )

    if not response.is_success:
        error_message, error_type, error_code = _extract_json_error_fields(data)
        result["error_message"] = error_message or f"HTTP {response.status_code}"
        result["error_type"] = error_type
        result["error_code"] = error_code
        result["body_excerpt"] = json.dumps(data, ensure_ascii=False)[:1000]

    return result


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
        base_url = _normalize_base_url(args.base_url)
    except ValueError as exc:
        print(f"invalid base url: {exc}", file=err)
        return 2

    api_key = os.getenv(args.api_key_env, "").strip()
    if not api_key:
        print(f"missing api key env: {args.api_key_env}", file=err)
        return 2

    attempts = int(args.attempts)
    if attempts <= 0:
        print("attempts must be > 0", file=err)
        return 2

    timeout_seconds = float(args.timeout_seconds)
    if timeout_seconds <= 0:
        print("timeout_seconds must be > 0", file=err)
        return 2

    sleep_seconds = float(args.sleep_seconds)
    if sleep_seconds < 0:
        print("sleep_seconds must be >= 0", file=err)
        return 2

    inputs = _normalize_inputs(args.input)
    payload = _build_payload(
        model=args.model,
        inputs=inputs,
        dimensions=args.dimensions,
    )
    url = f"{base_url}/embeddings"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    results: list[dict[str, Any]] = []
    with httpx.Client() as client:
        for attempt in range(1, attempts + 1):
            result = _run_probe_attempt(
                client=client,
                url=url,
                headers=headers,
                payload=payload,
                attempt=attempt,
                timeout_seconds=timeout_seconds,
            )
            print(json.dumps(result, ensure_ascii=False), file=out)
            results.append(result)
            if attempt < attempts and sleep_seconds > 0:
                time.sleep(sleep_seconds)

    elapsed_values = [int(result.get("elapsed_ms") or 0) for result in results]
    success_total = sum(1 for result in results if bool(result.get("ok")))
    summary = {
        "kind": "summary",
        "model": str(args.model).strip(),
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
    print(json.dumps(summary, ensure_ascii=False), file=out)
    return 0 if success_total == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
