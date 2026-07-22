from __future__ import annotations

from typing import Any, cast

import httpx
import pytest

from recoleta.extract import fetch_url_html


class _RetryAfterClient:
    def __init__(self, *, retry_after: str = "2") -> None:
        self.calls = 0
        self.retry_after = retry_after

    def get(self, url: str, **_: Any) -> httpx.Response:
        self.calls += 1
        request = httpx.Request("GET", url)
        if self.calls == 1:
            return httpx.Response(
                status_code=429,
                headers={"Retry-After": self.retry_after},
                request=request,
                text="too many requests",
            )
        return httpx.Response(
            status_code=200,
            request=request,
            text="<html><body>ok</body></html>",
        )


def test_fetch_url_html_waits_retry_after_before_retrying_429() -> None:
    """Regression: 429 responses with Retry-After must not retry immediately."""

    slept: list[float] = []
    retrying = cast(Any, fetch_url_html).retry
    previous_sleep = retrying.sleep
    retrying.sleep = lambda seconds: slept.append(float(seconds))
    try:
        client = _RetryAfterClient()

        html = fetch_url_html(
            client,  # type: ignore[arg-type]
            "https://arxiv.org/html/1706.03762",
        )
    finally:
        retrying.sleep = previous_sleep

    assert html == "<html><body>ok</body></html>"
    assert client.calls == 2
    assert slept == [2.0]


def test_fetch_url_html_honors_long_retry_after_before_retrying_429() -> None:
    """Regression: 429 Retry-After values above one minute must not be shortened."""

    slept: list[float] = []
    retrying = cast(Any, fetch_url_html).retry
    previous_sleep = retrying.sleep
    retrying.sleep = lambda seconds: slept.append(float(seconds))
    try:
        client = _RetryAfterClient(retry_after="120")

        html = fetch_url_html(
            client,  # type: ignore[arg-type]
            "https://arxiv.org/html/1706.03762",
        )
    finally:
        retrying.sleep = previous_sleep

    assert html == "<html><body>ok</body></html>"
    assert client.calls == 2
    assert slept == [120.0]


def test_fetch_url_html_acquires_admission_before_every_attempt() -> None:
    attempts: list[int] = []
    client = _RetryAfterClient()
    retrying = cast(Any, fetch_url_html).retry
    previous_sleep = retrying.sleep
    retrying.sleep = lambda _seconds: None
    try:
        html = fetch_url_html(
            client,  # type: ignore[arg-type]
            "https://arxiv.org/html/1706.03762",
            before_attempt=lambda: attempts.append(len(attempts) + 1),
        )
    finally:
        retrying.sleep = previous_sleep

    assert html == "<html><body>ok</body></html>"
    assert attempts == [1, 2]


def test_fetch_url_html_can_defer_429_without_retrying_or_falling_through() -> None:
    rate_limited: list[int] = []
    client = _RetryAfterClient(retry_after="120")

    with pytest.raises(httpx.HTTPStatusError) as caught:
        fetch_url_html(
            client,  # type: ignore[arg-type]
            "https://arxiv.org/html/1706.03762",
            retry_on_429=False,
            on_rate_limited=lambda response: rate_limited.append(
                response.status_code
            ),
        )

    assert caught.value.response.status_code == 429
    assert client.calls == 1
    assert rate_limited == [429]
