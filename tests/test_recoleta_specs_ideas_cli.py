from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

import recoleta.cli


class _FakeRun:
    def __init__(self, run_id: str) -> None:
        self.id = run_id


@dataclass
class _FakeIdeasStreamResult:
    stream: str
    status: str
    pass_output_id: int
    note_path: Path | None


class _FakeRepo:
    def __init__(self) -> None:
        self.finished: list[tuple[str, bool]] = []

    def acquire_workspace_lease(self, **_: object) -> None:
        return None

    def mark_stale_runs_failed(self, **_: object) -> int:
        return 0

    def create_run(
        self, *, config_fingerprint: str, run_id: str | None = None
    ) -> _FakeRun:  # noqa: ARG002
        _ = run_id
        return _FakeRun("run-ideas")

    def heartbeat_run(self, run_id: str) -> None:
        _ = run_id

    def renew_workspace_lease(self, **_: object) -> None:
        return None

    def release_workspace_lease(self, **_: object) -> bool:
        return True

    def finish_run(self, run_id: str, *, success: bool) -> None:
        self.finished.append((run_id, bool(success)))

    def list_metrics(self, *, run_id: str):  # type: ignore[no-untyped-def]
        _ = run_id
        return []


class _FakeSettings:
    log_json = False

    def safe_fingerprint(self) -> str:
        return "fp-ideas"


class _FakeService:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def ideas(  # type: ignore[no-untyped-def]
        self,
        *,
        run_id: str,
        granularity: str,
        anchor_date=None,
        llm_model=None,
    ):
        self.calls.append(
            {
                "run_id": run_id,
                "granularity": granularity,
                "anchor_date": anchor_date,
                "llm_model": llm_model,
            }
        )
        return type(
            "IdeasResult",
            (),
            {
                "pass_output_id": 7,
                "granularity": str(granularity),
                "period_start": datetime(2026, 3, 2, tzinfo=UTC),
                "period_end": datetime(2026, 3, 3, tzinfo=UTC),
                "title": "Why now ideas",
                "status": "succeeded",
                "note_path": Path("/tmp/recoleta/Ideas/day--2026-03-02--ideas.md"),
            },
        )()


def test_ideas_cli_accepts_yyyymmdd_date_and_prints_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()
    fake_service = _FakeService()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, fake_service),
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["ideas", "--granularity", "day", "--date", "20260302"],
    )

    assert result.exit_code == 0
    assert "ideas completed" in result.stdout
    assert "status=succeeded" in result.stdout
    assert "pass_output_id=7" in result.stdout
    assert fake_repo.finished == [("run-ideas", True)]
    assert fake_service.calls
    assert fake_service.calls[0]["anchor_date"] == date(2026, 3, 2)


def test_ideas_cli_ignores_legacy_stream_results_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()

    class _FakeTopicStreamService:
        def ideas(  # type: ignore[no-untyped-def]
            self,
            *,
            run_id: str,
            granularity: str,
            anchor_date=None,
            llm_model=None,
        ):
            _ = (run_id, granularity, anchor_date, llm_model)
            stream_results = [
                _FakeIdeasStreamResult(
                    stream="embodied_ai",
                    status="succeeded",
                    pass_output_id=5,
                    note_path=Path(
                        "/tmp/recoleta/Streams/embodied_ai/Ideas/day--2026-03-09--ideas.md"
                    ),
                ),
                _FakeIdeasStreamResult(
                    stream="software_intelligence",
                    status="suppressed",
                    pass_output_id=6,
                    note_path=None,
                ),
            ]
            return type(
                "IdeasResult",
                (),
                {
                    "pass_output_id": 5,
                    "granularity": "day",
                    "period_start": datetime(2026, 3, 9, tzinfo=UTC),
                    "period_end": datetime(2026, 3, 10, tzinfo=UTC),
                    "title": "Ideas",
                    "status": "succeeded",
                    "note_path": stream_results[0].note_path,
                    "stream_results": stream_results,
                },
            )()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, _FakeTopicStreamService()),
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["ideas", "--granularity", "day", "--date", "20260309"],
    )

    assert result.exit_code == 0
    assert "ideas completed" in result.stdout
    assert "streams=2" not in result.stdout
    assert "status=succeeded" in result.stdout
    assert "pass_output_id=5" in result.stdout
    assert "software_intelligence" not in result.stdout
    assert "status=suppressed" not in result.stdout
    assert "pass_output_id=6" not in result.stdout
    assert (
        "note_path=/tmp/recoleta/Streams/embodied_ai/Ideas/day--2026-03-09--ideas.md"
        in result.stdout
    )


def test_ideas_cli_json_ignores_legacy_stream_results_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings()
    fake_repo = _FakeRepo()

    class _FakeTopicStreamService:
        def ideas(  # type: ignore[no-untyped-def]
            self,
            *,
            run_id: str,
            granularity: str,
            anchor_date=None,
            llm_model=None,
        ):
            _ = (run_id, granularity, anchor_date, llm_model)
            stream_results = [
                _FakeIdeasStreamResult(
                    stream="embodied_ai",
                    status="succeeded",
                    pass_output_id=5,
                    note_path=Path(
                        "/tmp/recoleta/Streams/embodied_ai/Ideas/day--2026-03-09--ideas.md"
                    ),
                ),
                _FakeIdeasStreamResult(
                    stream="software_intelligence",
                    status="suppressed",
                    pass_output_id=6,
                    note_path=None,
                ),
            ]
            return type(
                "IdeasResult",
                (),
                {
                    "pass_output_id": 5,
                    "granularity": "day",
                    "period_start": datetime(2026, 3, 9, tzinfo=UTC),
                    "period_end": datetime(2026, 3, 10, tzinfo=UTC),
                    "title": "Ideas",
                    "status": "succeeded",
                    "note_path": stream_results[0].note_path,
                    "upstream_pass_output_id": 4,
                    "stream_results": stream_results,
                },
            )()

    monkeypatch.setattr(
        recoleta.cli,
        "_build_runtime",
        lambda: (fake_settings, fake_repo, _FakeTopicStreamService()),
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["ideas", "--granularity", "day", "--date", "20260309", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "ideas"
    assert payload["run_id"] == "run-ideas"
    assert payload["pass_output_id"] == 5
    assert payload["upstream_pass_output_id"] == 4
    assert payload["note_path"] == (
        "/tmp/recoleta/Streams/embodied_ai/Ideas/day--2026-03-09--ideas.md"
    )
    assert "stream_results_total" not in payload
    assert "stream_results" not in payload
