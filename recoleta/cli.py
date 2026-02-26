from __future__ import annotations

from collections.abc import Callable
import importlib
from typing import Any

def _import_symbol(module_name: str, *, attr_name: str | None = None) -> Any:
    module = importlib.import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


typer = _import_symbol("typer")
_RUNTIME_SYMBOLS: dict[str, Any] | None = None

app = typer.Typer(help="Recoleta research intelligence funnel CLI.", no_args_is_help=True)


def _runtime_symbols() -> dict[str, Any]:
    global _RUNTIME_SYMBOLS
    if _RUNTIME_SYMBOLS is not None:
        return _RUNTIME_SYMBOLS

    _RUNTIME_SYMBOLS = {
        "logger": _import_symbol("loguru", attr_name="logger"),
        "Console": _import_symbol("rich.console", attr_name="Console"),
        "Settings": _import_symbol("recoleta.config", attr_name="Settings"),
        "configure_process_logging": _import_symbol(
            "recoleta.observability",
            attr_name="configure_process_logging",
        ),
        "PipelineService": _import_symbol("recoleta.pipeline", attr_name="PipelineService"),
        "Repository": _import_symbol("recoleta.storage", attr_name="Repository"),
    }
    return _RUNTIME_SYMBOLS


def _build_runtime() -> tuple[Any, Any, Any]:
    symbols = _runtime_symbols()
    settings_cls = symbols["Settings"]
    configure_process_logging = symbols["configure_process_logging"]
    repository_cls = symbols["Repository"]
    pipeline_service_cls = symbols["PipelineService"]

    settings = settings_cls()  # pyright: ignore[reportCallIssue]
    configure_process_logging(level=settings.log_level, log_json=settings.log_json)
    repository = repository_cls(
        db_path=settings.recoleta_db_path,
        title_dedup_threshold=settings.title_dedup_threshold,
        title_dedup_max_candidates=settings.title_dedup_max_candidates,
    )
    repository.init_schema()
    service = pipeline_service_cls(settings=settings, repository=repository)
    return settings, repository, service


def _execute_stage(
    *,
    stage_name: str,
    stage_runner: Callable[[Any, str], Any],
) -> tuple[Any, Any]:
    symbols = _runtime_symbols()
    logger = symbols["logger"]

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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(stage_name="ingest", stage_runner=lambda service, run_id: service.ingest(run_id=run_id))
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )


@app.command()
def analyze(limit: int = typer.Option(100, min=1, help="Max number of items analyzed in one run.")) -> None:
    """Run LLM analysis for newly ingested items."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="analyze",
        stage_runner=lambda service, run_id: service.analyze(run_id=run_id, limit=limit),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(f"[green]analyze completed[/green] processed={result.processed} failed={result.failed}")


@app.command()
def publish(limit: int = typer.Option(50, min=1, help="Max number of analyzed items published.")) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="publish",
        stage_runner=lambda service, run_id: service.publish(run_id=run_id, limit=limit),
    )
    console = console_cls(stderr=settings.log_json)
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

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    blocking_scheduler_cls = _import_symbol(
        "apscheduler.schedulers.blocking",
        attr_name="BlockingScheduler",
    )

    settings, _, _ = _build_runtime()
    console = console_cls(stderr=settings.log_json)
    scheduler = blocking_scheduler_cls(
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
