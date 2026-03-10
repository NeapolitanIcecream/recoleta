from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any

import httpx


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Ping an OpenAI-compatible chat completions endpoint."
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
        default="openai/gpt-5.4",
        help="Model name to send.",
    )
    parser.add_argument(
        "--response-format",
        choices=("json_object", "none"),
        default="json_object",
        help="Whether to request JSON mode.",
    )
    return parser


def _normalize_base_url(raw: str) -> str:
    cleaned = str(raw or "").strip()
    if not cleaned:
        raise ValueError("base URL is required")
    return cleaned.rstrip("/")


def _build_payload(*, model: str, response_format: str) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": "Return concise JSON only."},
            {
                "role": "user",
                "content": 'Return {"ok": true, "source": "ping"} as a JSON object.',
            },
        ],
        "temperature": 0,
    }
    if response_format == "json_object":
        payload["response_format"] = {"type": "json_object"}
    return payload


def main() -> int:
    args = _build_parser().parse_args()
    try:
        base_url = _normalize_base_url(args.base_url)
    except ValueError as exc:
        print(f"invalid base url: {exc}", file=sys.stderr)
        return 2

    api_key = os.getenv(args.api_key_env, "").strip()
    if not api_key:
        print(f"missing api key env: {args.api_key_env}", file=sys.stderr)
        return 2

    url = f"{base_url}/chat/completions"
    payload = _build_payload(
        model=str(args.model).strip(),
        response_format=args.response_format,
    )
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    timeout = httpx.Timeout(30.0, connect=10.0)

    with httpx.Client(timeout=timeout) as client:
        response = client.post(url, headers=headers, json=payload)

    content_type = response.headers.get("content-type", "")
    print(json.dumps({"status_code": response.status_code, "url": url}, ensure_ascii=False))

    if "application/json" in content_type:
        try:
            data = response.json()
        except Exception as exc:  # noqa: BLE001
            print(f"json decode failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            print(response.text[:1000], file=sys.stderr)
            return 1
        print(json.dumps(data, ensure_ascii=False)[:4000])
    else:
        print(response.text[:1000])

    return 0 if response.is_success else 1


if __name__ == "__main__":
    raise SystemExit(main())
