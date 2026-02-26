from __future__ import annotations

from collections.abc import Callable
from typing import Any

import typer
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger
from rich.console import Console

from recoleta.config import Settings
from recoleta.observability import configure_process_logging
from recoleta.pipeline import PipelineService
from recoleta.storage import Repository

app = typer.Typer(help="Recoleta research intelligence funnel CLI.", no_args_is_help=True)


def _build_runtime() -> tuple[Settings, Repository, PipelineService]:
    settings = Settings()  # pyright: ignore[reportCallIssue]
    configure_process_logging(level=settings.log_level, log_json=settings.log_json)
    repository = Repository(
        db_path=settings.recoleta_db_path,
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = PipelineService(settings=settings, repository=repository)
    return settings, repository, service


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Callable[[PipelineService, str], Any],
) -> tuple[Settings, Any]:
    settings, repository, service = _build_runtime()
    run = repository.create_run(config_fingerprint=settings.safe_fingerprint())
    stage_log = logger.bind(module=f"cli.{stage_name}", run_id=run.id)
    try:
        result = stage_runner(service, run.id)
        repository.finish_run(run.id, success=True)
        return settings, result
    except Exception:
        repository.finish_run(run.id, success=False)
        stage_log.exception("Stage execution failed")
        raise


@app.command()
def ingest() -> None:
    """Pull sources and upsert normalized items."""

    settings, result = _execute_stage(stage_name="ingest", stage_runner=lambda service, run_id: service.ingest(run_id=run_id))
    console = Console(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )


@app.command()
def analyze(limit: int = typer.Option(100, min=1, help="Max number of items analyzed in one run.")) -> None:
    """Run LLM analysis for newly ingested items."""

    settings, result = _execute_stage(
        stage_name="analyze",
        stage_runner=lambda service, run_id: service.analyze(run_id=run_id, limit=limit),
    )
    console = Console(stderr=settings.log_json)
    console.print(f"[green]analyze completed[/green] processed={result.processed} failed={result.failed}")


@app.command()
def publish(limit: int = typer.Option(50, min=1, help="Max number of analyzed items published.")) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""

    settings, result = _execute_stage(
        stage_name="publish",
        stage_runner=lambda service, run_id: service.publish(run_id=run_id, limit=limit),
    )
    console = Console(stderr=settings.log_json)
    console.print(f"[green]publish completed[/green] sent={result.sent} skipped={result.skipped} failed={result.failed}")
    if "markdown" in settings.publish_targets:
        console.print(f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}")
        console.print(f"[cyan]latest index[/cyan] {settings.markdown_output_dir / 'latest.md'}")
    if "obsidian" in settings.publish_targets and settings.obsidian_vault_path is not None:
        console.print(
            f"[cyan]obsidian notes[/cyan] {settings.obsidian_vault_path / settings.obsidian_base_folder / 'Inbox'}"
        )


@app.command("run")
def run_scheduler() -> None:
    """Run periodic ingest/analyze/publish jobs with APScheduler."""

    settings, _, _ = _build_runtime()
    console = Console(stderr=settings.log_json)
    scheduler = BlockingScheduler(
        timezone="UTC",
        executors={"default": {"type": "threadpool", "max_workers": 1}},
        job_defaults={"coalesce": True, "max_instances": 1},
    )

    def run_ingest_job() -> None:
        _execute_stage(stage_name="ingest", stage_runner=lambda service, run_id: service.ingest(run_id=run_id))

    def run_analyze_job() -> None:
        _execute_stage(
            stage_name="analyze",
            stage_runner=lambda service, run_id: service.analyze(run_id=run_id),
        )

    def run_publish_job() -> None:
        _execute_stage(
            stage_name="publish",
            stage_runner=lambda service, run_id: service.publish(run_id=run_id),
        )

    scheduler.add_job(
        run_ingest_job,
        "interval",
        minutes=settings.ingest_interval_minutes,
        id="ingest",
        replace_existing=True,
    )
    scheduler.add_job(
        run_analyze_job,
        "interval",
        minutes=settings.analyze_interval_minutes,
        id="analyze",
        replace_existing=True,
    )
    scheduler.add_job(
        run_publish_job,
        "interval",
        minutes=settings.publish_interval_minutes,
        id="publish",
        replace_existing=True,
    )
    console.print("[cyan]scheduler started[/cyan]")
    scheduler.start()


def main() -> None:
    app()


if __name__ == "__main__":
    main()
