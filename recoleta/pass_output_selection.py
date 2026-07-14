from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Iterable, cast

from sqlalchemy import desc, or_
from sqlmodel import Session, select

from recoleta.models import PassOutput
from recoleta.passes.base import (
    SUPPRESSION_PROJECTION_COMPLETE_KEY,
    PassStatus,
)


CANONICAL_PASS_OUTPUT_STATUSES = (
    PassStatus.SUCCEEDED.value,
    PassStatus.SUPPRESSED.value,
)
type PassOutputWindowKey = tuple[str | None, datetime | None, datetime | None]


@dataclass(frozen=True, slots=True)
class IdeaPassOutputWindowState:
    row: Any
    active: bool


def pass_output_window_key(row: Any) -> PassOutputWindowKey:
    return (
        str(getattr(row, "granularity", "") or "").strip().lower() or None,
        _normalized_window_datetime(getattr(row, "period_start", None)),
        _normalized_window_datetime(getattr(row, "period_end", None)),
    )


def _normalized_window_datetime(value: Any) -> datetime | None:
    if not isinstance(value, datetime):
        return None
    if value.tzinfo is None or value.tzinfo.utcoffset(value) is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


def latest_canonical_pass_outputs_by_window(
    *,
    repository: Any,
    pass_kind: str,
    windows: Iterable[PassOutputWindowKey],
) -> dict[PassOutputWindowKey, Any]:
    """Load canonical outputs for many exact windows with bounded SQL queries."""
    requested = _normalized_window_keys(windows)
    if not requested:
        return {}
    engine = getattr(repository, "engine", None)
    if engine is None:
        return _canonical_outputs_without_engine(
            repository=repository,
            pass_kind=pass_kind,
            requested=requested,
        )
    rows = _canonical_pass_output_rows(
        engine=engine,
        pass_kind=pass_kind,
        requested=requested,
    )
    return _select_latest_requested_outputs(rows=rows, requested=requested)


def latest_idea_pass_output_states_by_window(
    *,
    repository: Any,
    windows: Iterable[PassOutputWindowKey],
) -> dict[PassOutputWindowKey, IdeaPassOutputWindowState]:
    """Resolve Ideas currentness against each window's canonical Trend output."""
    requested = _normalized_window_keys(windows)
    ideas_by_window = latest_canonical_pass_outputs_by_window(
        repository=repository,
        pass_kind="trend_ideas",
        windows=requested,
    )
    if not ideas_by_window:
        return {}
    trends_by_window = latest_canonical_pass_outputs_by_window(
        repository=repository,
        pass_kind="trend_synthesis",
        windows=requested,
    )
    return {
        key: IdeaPassOutputWindowState(
            row=row,
            active=_idea_output_matches_current_trend(
                row=row,
                trend_row=trends_by_window.get(key),
            ),
        )
        for key, row in ideas_by_window.items()
    }


def _idea_output_matches_current_trend(*, row: Any, trend_row: Any | None) -> bool:
    return bool(
        _pass_output_status(row) == PassStatus.SUCCEEDED.value
        and _pass_output_status(trend_row) == PassStatus.SUCCEEDED.value
        and _referenced_pass_output_id(row, pass_kind="trend_synthesis")
        == _positive_row_id(trend_row)
    )


def _referenced_pass_output_id(row: Any, *, pass_kind: str) -> int | None:
    raw = getattr(row, "input_refs_json", None)
    try:
        refs = json.loads(str(raw or "[]"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    for ref in refs if isinstance(refs, list) else []:
        if not isinstance(ref, dict) or str(ref.get("pass_kind") or "") != pass_kind:
            continue
        try:
            value = int(ref.get("pass_output_id") or 0)
        except (TypeError, ValueError):
            return None
        return value if value > 0 else None
    return None


def _positive_row_id(row: Any | None) -> int | None:
    try:
        value = int(getattr(row, "id", 0) or 0)
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


def _pass_output_status(row: Any | None) -> str:
    return str(getattr(row, "status", "") or "").strip().lower()


def _normalized_window_keys(
    windows: Iterable[PassOutputWindowKey],
) -> set[PassOutputWindowKey]:
    return {
        (
            str(granularity or "").strip().lower() or None,
            _normalized_window_datetime(period_start),
            _normalized_window_datetime(period_end),
        )
        for granularity, period_start, period_end in windows
    }


def _canonical_outputs_without_engine(
    *,
    repository: Any,
    pass_kind: str,
    requested: set[PassOutputWindowKey],
) -> dict[PassOutputWindowKey, Any]:
    selected: dict[PassOutputWindowKey, Any] = {}
    for key in requested:
        row = latest_canonical_pass_output(
            repository=repository,
            pass_kind=pass_kind,
            granularity=key[0],
            period_start=key[1],
            period_end=key[2],
        )
        if row is not None:
            selected[key] = row
    return selected


def _canonical_pass_output_rows(
    *,
    engine: Any,
    pass_kind: str,
    requested: set[PassOutputWindowKey],
) -> list[PassOutput]:
    with Session(engine) as session:
        statement = select(PassOutput).where(
            PassOutput.pass_kind == str(pass_kind or "").strip(),
            cast(Any, PassOutput.status).in_(CANONICAL_PASS_OUTPUT_STATUSES),
            _requested_values_condition(
                PassOutput.granularity,
                {key[0] for key in requested},
            ),
            _requested_values_condition(
                PassOutput.period_start,
                {key[1] for key in requested},
            ),
            _requested_values_condition(
                PassOutput.period_end,
                {key[2] for key in requested},
            ),
        )
        rows = session.exec(
            statement.order_by(
                desc(cast(Any, PassOutput.created_at)),
                desc(cast(Any, PassOutput.id)),
            )
        )
        return list(rows)


def _requested_values_condition(column: Any, values: set[Any]) -> Any:
    non_null_values = [value for value in values if value is not None]
    conditions: list[Any] = []
    if non_null_values:
        conditions.append(cast(Any, column).in_(non_null_values))
    if None in values:
        conditions.append(cast(Any, column).is_(None))
    return or_(*conditions)


def _select_latest_requested_outputs(
    *,
    rows: Iterable[PassOutput],
    requested: set[PassOutputWindowKey],
) -> dict[PassOutputWindowKey, Any]:
    selected: dict[PassOutputWindowKey, Any] = {}
    for row in rows:
        key = pass_output_window_key(row)
        if key in requested and key not in selected:
            selected[key] = row
    return selected


def latest_pass_output_for_statuses(
    *,
    repository: Any,
    pass_kind: str,
    statuses: Iterable[str],
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> Any | None:
    """Return the newest terminal output for one logical pass window."""
    normalized_statuses = tuple(
        dict.fromkeys(
            token
            for status in statuses
            if (token := str(status or "").strip().lower())
        )
    )
    normalized_status_set = set(normalized_statuses)
    if normalized_status_set == set(CANONICAL_PASS_OUTPUT_STATUSES):
        latest = repository.get_latest_pass_output(
            pass_kind=pass_kind,
            status=None,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
        )
        if (
            str(getattr(latest, "status", "") or "").strip().lower()
            in normalized_status_set
        ):
            return latest
    rows: list[Any] = []
    for status in normalized_statuses:
        row = repository.get_latest_pass_output(
            pass_kind=pass_kind,
            status=status,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
        )
        if row is not None:
            rows.append(row)
    return max(rows, key=_pass_output_recency_key) if rows else None


def latest_canonical_pass_output(
    *,
    repository: Any,
    pass_kind: str,
    granularity: str | None,
    period_start: datetime | None,
    period_end: datetime | None,
) -> Any | None:
    return latest_pass_output_for_statuses(
        repository=repository,
        pass_kind=pass_kind,
        statuses=CANONICAL_PASS_OUTPUT_STATUSES,
        granularity=granularity,
        period_start=period_start,
        period_end=period_end,
    )


def is_suppressed_pass_output(row: Any | None) -> bool:
    return str(getattr(row, "status", "") or "").strip().lower() == (
        PassStatus.SUPPRESSED.value
    )


def suppression_projection_incomplete(row: Any | None) -> bool:
    """Return whether a new suppressed output still needs projection cleanup.

    Historical rows predate this diagnostic and remain complete by default.
    """
    if not is_suppressed_pass_output(row):
        return False
    raw = getattr(row, "diagnostics_json", None)
    try:
        diagnostics = json.loads(str(raw or "{}"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return False
    return bool(
        isinstance(diagnostics, dict)
        and diagnostics.get(SUPPRESSION_PROJECTION_COMPLETE_KEY) is False
    )


def _pass_output_recency_key(row: Any) -> tuple[float, int]:
    created_at = getattr(row, "created_at", None)
    timestamp = created_at.timestamp() if isinstance(created_at, datetime) else 0.0
    try:
        row_id = int(getattr(row, "id", 0) or 0)
    except TypeError, ValueError:
        row_id = 0
    return timestamp, row_id
