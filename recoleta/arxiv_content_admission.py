from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
import sqlite3
import time

import httpx

_Clock = Callable[[], float]
_Sleeper = Callable[[float], None]


class ArxivContentAdmission:
    """Process-safe admission and cooldown for requests to arxiv.org content."""

    def __init__(
        self,
        *,
        db_path: Path,
        requests_per_second: float,
        cooldown_seconds: int,
        clock: _Clock = time.time,
        sleeper: _Sleeper = time.sleep,
    ) -> None:
        self.db_path = Path(db_path).expanduser()
        self.interval_seconds = 1.0 / max(0.0001, float(requests_per_second))
        self.cooldown_seconds = max(1, int(cooldown_seconds))
        self._clock = clock
        self._sleep = sleeper
        self._initialize()

    def acquire(self) -> float:
        waited_total = 0.0
        while True:
            with self._connect() as connection:
                connection.execute("BEGIN IMMEDIATE")
                # Sample after winning the write lock. Otherwise time spent
                # waiting for another process can make the newly reserved slot
                # already expired when this transaction commits.
                now = float(self._clock())
                row = connection.execute(
                    """
                    SELECT next_allowed_at, cooldown_until
                    FROM arxiv_content_rate_state
                    WHERE rate_domain = 'arxiv_content'
                    """
                ).fetchone()
                next_allowed_at = float(row[0]) if row is not None else 0.0
                cooldown_until = float(row[1]) if row is not None else 0.0
                allowed_at = max(next_allowed_at, cooldown_until)
                if allowed_at <= now:
                    connection.execute(
                        """
                        INSERT INTO arxiv_content_rate_state (
                            rate_domain,
                            next_allowed_at,
                            cooldown_until,
                            last_status,
                            updated_at
                        ) VALUES ('arxiv_content', ?, ?, NULL, ?)
                        ON CONFLICT(rate_domain) DO UPDATE SET
                            next_allowed_at = excluded.next_allowed_at,
                            updated_at = excluded.updated_at
                        """,
                        (now + self.interval_seconds, cooldown_until, now),
                    )
                    connection.commit()
                    return waited_total
                wait_seconds = max(0.0, allowed_at - now)
                connection.commit()
            self._sleep(wait_seconds)
            waited_total += wait_seconds

    def record_rate_limited(self, response: httpx.Response) -> float:
        now = float(self._clock())
        retry_after = _retry_after_seconds(response=response, now_epoch=now)
        cooldown_seconds = max(
            float(self.cooldown_seconds),
            float(retry_after or 0.0),
        )
        proposed_until = now + cooldown_seconds
        with self._connect() as connection:
            connection.execute("BEGIN IMMEDIATE")
            row = connection.execute(
                """
                SELECT next_allowed_at, cooldown_until
                FROM arxiv_content_rate_state
                WHERE rate_domain = 'arxiv_content'
                """
            ).fetchone()
            next_allowed_at = float(row[0]) if row is not None else now
            current_cooldown = float(row[1]) if row is not None else 0.0
            cooldown_until = max(current_cooldown, proposed_until)
            connection.execute(
                """
                INSERT INTO arxiv_content_rate_state (
                    rate_domain,
                    next_allowed_at,
                    cooldown_until,
                    last_status,
                    updated_at
                ) VALUES ('arxiv_content', ?, ?, 429, ?)
                ON CONFLICT(rate_domain) DO UPDATE SET
                    next_allowed_at = excluded.next_allowed_at,
                    cooldown_until = excluded.cooldown_until,
                    last_status = excluded.last_status,
                    updated_at = excluded.updated_at
                """,
                (max(next_allowed_at, cooldown_until), cooldown_until, now),
            )
            connection.commit()
        return cooldown_until

    def _initialize(self) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS arxiv_content_rate_state (
                    rate_domain TEXT PRIMARY KEY,
                    next_allowed_at REAL NOT NULL,
                    cooldown_until REAL NOT NULL,
                    last_status INTEGER,
                    updated_at REAL NOT NULL
                )
                """
            )

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path, timeout=30.0)
        connection.execute("PRAGMA busy_timeout = 30000")
        return connection


def _retry_after_seconds(*, response: httpx.Response, now_epoch: float) -> float | None:
    raw_value = str(response.headers.get("Retry-After") or "").strip()
    if not raw_value:
        return None
    try:
        return max(0.0, float(raw_value))
    except ValueError:
        try:
            retry_at = parsedate_to_datetime(raw_value)
        except (TypeError, ValueError):
            return None
        if retry_at.tzinfo is None:
            retry_at = retry_at.replace(tzinfo=UTC)
        now = datetime.fromtimestamp(now_epoch, tz=UTC)
        return max(0.0, (retry_at - now).total_seconds())
