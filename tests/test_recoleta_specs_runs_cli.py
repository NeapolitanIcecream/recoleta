from __future__ import annotations

from datetime import UTC, datetime, timedelta
import json
from pathlib import Path

from sqlmodel import Session
from typer.testing import CliRunner

import recoleta.cli
from recoleta.models import Run
from recoleta.storage import Repository


def test_runs_show_json_aggregates_metrics_pass_outputs_and_artifacts(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-runs", run_id="run-trends")
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.llm_requests_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.llm_requests_total",
        value=2,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.estimated_cost_usd",
        value=0.0067,
        unit="usd",
    )
    repository.create_pass_output(
        run_id=run.id,
        pass_kind="trend_synthesis",
        status="succeeded",
        granularity="day",
        period_start=datetime(2026, 3, 17, tzinfo=UTC),
        period_end=datetime(2026, 3, 18, tzinfo=UTC),
        payload={"title": "Agent Systems"},
        diagnostics={"selected_total": 7},
        input_refs=[
            {"ref_kind": "document", "doc_id": 11},
            {"ref_kind": "document", "doc_id": 12},
        ],
    )
    repository.add_artifact(
        run_id=run.id,
        item_id=None,
        kind="llm_debug_bundle",
        path=str(tmp_path / "artifacts" / "debug-1.json"),
    )
    repository.add_artifact(
        run_id=run.id,
        item_id=None,
        kind="llm_debug_bundle",
        path=str(tmp_path / "artifacts" / "debug-2.json"),
    )
    repository.add_artifact(
        run_id=run.id,
        item_id=None,
        kind="trend_pdf",
        path=str(tmp_path / "artifacts" / "trend.pdf"),
    )
    repository.finish_run(run.id, success=True)

    with Session(repository.engine) as session:
        row = session.get(Run, run.id)
        assert row is not None
        row.started_at = datetime(2026, 3, 18, 10, 0, tzinfo=UTC)
        row.heartbeat_at = row.started_at + timedelta(minutes=2)
        row.finished_at = row.started_at + timedelta(minutes=2)
        session.add(row)
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        ["runs", "show", "--db-path", str(db_path), "--run-id", "run-trends", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["run"]["id"] == "run-trends"
    assert payload["run"]["status"] == "succeeded"
    assert payload["run"]["duration_seconds"] == 120
    assert payload["run"]["metrics"]["pipeline.trends.llm_requests_total"]["value"] == 3
    assert payload["run"]["billing"]["components"]["trends_llm"]["calls"] == 3
    assert payload["run"]["billing"]["total_cost_usd"] == 0.0067
    assert payload["run"]["pass_outputs_total"] == 1
    assert payload["run"]["pass_outputs"][0]["pass_kind"] == "trend_synthesis"
    assert payload["run"]["pass_outputs"][0]["diagnostics"]["selected_total"] == 7
    assert payload["run"]["pass_outputs"][0]["input_refs_total"] == 2
    assert "scope" not in payload["run"]["pass_outputs"][0]
    assert payload["run"]["artifacts_total"] == 3
    assert payload["run"]["artifacts_by_kind"]["llm_debug_bundle"] == 2
    assert payload["run"]["artifacts_by_kind"]["trend_pdf"] == 1


def test_runs_show_json_reports_run_context_and_failure_summary(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    period_start = datetime(2026, 3, 10, tzinfo=UTC)
    period_end = datetime(2026, 3, 17, tzinfo=UTC)
    run = repository.create_run("fp-context", run_id="run-context")
    repository.update_run_context(
        run_id=run.id,
        command="trends-week",
        scope="robotics",
        granularity="week",
        period_start=period_start,
        period_end=period_end,
    )
    repository.add_artifact(
        run_id=run.id,
        item_id=None,
        kind="error_context",
        path=str(tmp_path / "artifacts" / "error.json"),
        details={
            "error_type": "HTTPStatusError",
            "error_category": "auth",
            "http_status": 401,
            "retryable": True,
            "message_excerpt": "401 invalid token",
        },
    )
    repository.finish_run(run.id, success=False)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "runs",
            "show",
            "--db-path",
            str(db_path),
            "--run-id",
            "run-context",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["run"]["command"] == "trends-week"
    assert payload["run"]["scope"] == "robotics"
    assert payload["run"]["granularity"] == "week"
    assert payload["run"]["period_start"] == period_start.isoformat()
    assert payload["run"]["period_end"] == period_end.isoformat()
    assert payload["run"]["artifacts"][0]["details"]["error_category"] == "auth"
    assert payload["run"]["failure_summary"]["artifacts_total"] == 1
    assert payload["run"]["failure_summary"]["retryable_total"] == 1
    assert payload["run"]["failure_summary"]["by_category"]["auth"] == 1
    assert payload["run"]["failure_summary"]["by_type"]["HTTPStatusError"] == 1
    assert payload["run"]["failure_summary"]["http_status"]["401"] == 1


def test_inspect_runs_show_json_includes_workflow_metadata_fields(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-workflow", run_id="run-workflow")
    repository.update_run_context(
        run_id=run.id,
        command="run month --date 2026-03-16",
        operation_kind="workflow.run.month",
        scope="default",
        granularity="month",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 4, 1, tzinfo=UTC),
        target_granularity="month",
        target_period_start=datetime(2026, 3, 1, tzinfo=UTC),
        target_period_end=datetime(2026, 4, 1, tzinfo=UTC),
        requested_steps=[
            "ingest",
            "analyze",
            "publish",
            "trends:day",
            "ideas:day",
            "trends:week",
            "ideas:week",
            "trends:month",
            "ideas:month",
            "site-build",
        ],
        executed_steps=[
            "ingest",
            "analyze",
            "publish",
            "trends:day",
            "ideas:day",
            "trends:week",
            "ideas:week",
            "trends:month",
            "ideas:month",
            "site-build",
        ],
        skipped_steps=["translate"],
        billing_by_step={
            "trends:month": {
                "total_cost_usd": 0.12,
                "components": {"trends_llm": {"calls": 4}},
            }
        },
    )
    repository.finish_run(
        run.id,
        success=True,
        terminal_state="succeeded_partial",
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "inspect",
            "runs",
            "show",
            "--db-path",
            str(db_path),
            "--run-id",
            "run-workflow",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    run_payload = payload["run"]
    assert run_payload["command"] == "run month --date 2026-03-16"
    assert run_payload["operation_kind"] == "workflow.run.month"
    assert run_payload["granularity"] == "month"
    assert run_payload["target_granularity"] == "month"
    assert run_payload["target_period_start"] == "2026-03-01T00:00:00+00:00"
    assert run_payload["target_period_end"] == "2026-04-01T00:00:00+00:00"
    assert run_payload["requested_steps"] == [
        "ingest",
        "analyze",
        "publish",
        "trends:day",
        "ideas:day",
        "trends:week",
        "ideas:week",
        "trends:month",
        "ideas:month",
        "site-build",
    ]
    assert run_payload["executed_steps"] == run_payload["requested_steps"]
    assert run_payload["skipped_steps"] == ["translate"]
    assert run_payload["billing_by_step"]["trends:month"]["total_cost_usd"] == 0.12
    assert (
        run_payload["billing_by_step"]["trends:month"]["components"]["trends_llm"][
            "calls"
        ]
        == 4
    )
    assert run_payload["terminal_state"] == "succeeded_partial"


def test_runs_show_json_ignores_legacy_scope_billing_metrics(
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    run = repository.create_run("fp-stream-billing", run_id="run-stream-billing")
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.llm_requests_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.llm_input_tokens_total",
        value=72,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.llm_output_tokens_total",
        value=14,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.estimated_cost_usd",
        value=0.005,
        unit="usd",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.llm_requests_total",
        value=2,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.llm_input_tokens_total",
        value=180,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.llm_output_tokens_total",
        value=36,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.estimated_cost_usd",
        value=0.02,
        unit="usd",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.pass.ideas.llm_requests_total",
        value=1,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.pass.ideas.llm_input_tokens_total",
        value=90,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.pass.ideas.llm_output_tokens_total",
        value=18,
        unit="count",
    )
    repository.record_metric(
        run_id=run.id,
        name="pipeline.trends.scope.agents_lab.pass.ideas.estimated_cost_usd",
        value=0.007,
        unit="usd",
    )
    repository.finish_run(run.id, success=True)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "runs",
            "show",
            "--db-path",
            str(db_path),
            "--run-id",
            "run-stream-billing",
            "--json",
        ],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    billing = payload["run"]["billing"]
    assert billing["components"]["trends_llm"]["calls"] == 1
    assert billing["components"]["trends_llm"]["input_tokens"] == 72
    assert billing["components"]["trends_llm"]["output_tokens"] == 14
    assert billing["components"]["trends_llm"]["cost_usd"] == 0.005
    assert "ideas_llm" not in billing["components"]
    assert billing["total_cost_usd"] == 0.005
    assert "by_scope" not in billing


def test_runs_show_json_errors_for_missing_run(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    result = runner.invoke(
        recoleta.cli.app,
        [
            "runs",
            "show",
            "--db-path",
            str(db_path),
            "--run-id",
            "run-missing",
            "--json",
        ],
    )

    assert result.exit_code == 1
    payload = json.loads(result.stdout)
    assert payload["status"] == "error"
    assert "run not found" in payload["error"]


def test_runs_list_json_reports_recent_runs(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    repository = Repository(db_path=db_path)
    repository.init_schema()

    first = repository.create_run("fp-old", run_id="run-old")
    repository.finish_run(first.id, success=False)
    second = repository.create_run("fp-new", run_id="run-new")
    repository.update_run_context(
        run_id=second.id,
        command="ideas",
        scope="default",
        granularity="day",
        period_start=datetime(2026, 3, 18, tzinfo=UTC),
        period_end=datetime(2026, 3, 19, tzinfo=UTC),
    )
    repository.finish_run(second.id, success=True)

    with Session(repository.engine) as session:
        first_row = session.get(Run, first.id)
        second_row = session.get(Run, second.id)
        assert first_row is not None
        assert second_row is not None
        first_row.started_at = datetime(2026, 3, 18, 9, 0, tzinfo=UTC)
        first_row.heartbeat_at = first_row.started_at + timedelta(seconds=30)
        first_row.finished_at = first_row.started_at + timedelta(seconds=30)
        second_row.started_at = datetime(2026, 3, 18, 10, 0, tzinfo=UTC)
        second_row.heartbeat_at = second_row.started_at + timedelta(seconds=45)
        second_row.finished_at = second_row.started_at + timedelta(seconds=45)
        session.add(first_row)
        session.add(second_row)
        session.commit()

    result = runner.invoke(
        recoleta.cli.app,
        ["runs", "list", "--db-path", str(db_path), "--limit", "2", "--json"],
    )

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["runs"][0]["id"] == "run-new"
    assert payload["runs"][0]["status"] == "succeeded"
    assert payload["runs"][0]["command"] == "ideas"
    assert payload["runs"][0]["scope"] == "default"
    assert payload["runs"][0]["granularity"] == "day"
    assert payload["runs"][1]["id"] == "run-old"
    assert payload["runs"][1]["status"] == "failed"
