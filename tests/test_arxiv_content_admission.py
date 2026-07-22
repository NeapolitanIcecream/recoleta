from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from recoleta.arxiv_content_admission import ArxivContentAdmission


@dataclass
class _FakeClock:
    value: float = 1_000.0

    def now(self) -> float:
        return self.value

    def sleep(self, seconds: float) -> None:
        self.value += seconds


def _rate_limited_response(*, retry_after: str | None = None) -> httpx.Response:
    request = httpx.Request("GET", "https://arxiv.org/html/1706.03762")
    headers = {"Retry-After": retry_after} if retry_after is not None else {}
    return httpx.Response(429, request=request, headers=headers)


def _admission(path: Path, clock: _FakeClock) -> ArxivContentAdmission:
    return ArxivContentAdmission(
        db_path=path,
        requests_per_second=1 / 15,
        cooldown_seconds=3_600,
        clock=clock.now,
        sleeper=clock.sleep,
    )


def test_content_admission_persists_cooldown_across_process_owners(
    tmp_path: Path,
) -> None:
    clock = _FakeClock()
    path = tmp_path / "arxiv-content-admission.sqlite3"
    first = _admission(path, clock)
    second = _admission(path, clock)

    assert first.acquire() == 0.0
    first.record_rate_limited(_rate_limited_response(retry_after="120"))

    waited = second.acquire()

    assert waited == 3_600.0


def test_content_admission_uses_retry_after_as_a_hard_lower_bound(
    tmp_path: Path,
) -> None:
    clock = _FakeClock()
    admission = _admission(tmp_path / "admission.sqlite3", clock)
    admission.record_rate_limited(_rate_limited_response(retry_after="7200"))

    waited = admission.acquire()

    assert waited == 7_200.0


def test_content_admission_serializes_request_slots_across_instances(
    tmp_path: Path,
) -> None:
    clock = _FakeClock()
    path = tmp_path / "admission.sqlite3"

    assert _admission(path, clock).acquire() == 0.0
    assert _admission(path, clock).acquire() == 15.0


def test_content_admission_samples_slot_time_after_winning_sqlite_lock(
    tmp_path: Path,
    monkeypatch: Any,
) -> None:
    clock = _FakeClock(value=1_020.0)
    admission = _admission(tmp_path / "admission.sqlite3", clock)

    class _LockWaitingConnection:
        next_allowed_at: float | None = None

        def __enter__(self) -> "_LockWaitingConnection":
            return self

        def __exit__(self, *_args: object) -> None:
            return None

        def execute(
            self,
            statement: str,
            parameters: tuple[float, float, float] | None = None,
        ) -> "_LockWaitingConnection":
            if statement == "BEGIN IMMEDIATE":
                # Model time spent waiting for another process's write lock.
                clock.value = 1_100.0
            elif "INSERT INTO arxiv_content_rate_state" in statement:
                assert parameters is not None
                self.next_allowed_at = parameters[0]
            return self

        def fetchone(self) -> tuple[float, float]:
            return (0.0, 0.0)

        def commit(self) -> None:
            return None

    connection = _LockWaitingConnection()
    monkeypatch.setattr(admission, "_connect", lambda: connection)

    assert admission.acquire() == 0.0
    assert connection.next_allowed_at == 1_115.0
