from __future__ import annotations

from collections.abc import Callable
import importlib
import json
from pathlib import Path
from typing import Any

def _import_symbol(module_name: str, *, attr_name: str | None = None) -> Any:
    module = importlib.import_module(module_name)
    if attr_name is None:
        return module
    return getattr(module, attr_name)


typer = _import_symbol("typer")
_RUNTIME_SYMBOLS: dict[str, Any] | None = None

app = typer.Typer(help="Recoleta research intelligence funnel CLI.", no_args_is_help=True)
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True)
app.add_typer(db_app, name="db")


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
    """Pull sources, enrich content, and optionally pre-rank candidates."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]

    settings, result = _execute_stage(
        stage_name="ingest",
        stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
    )
    console = console_cls(stderr=settings.log_json)
    console.print(
        f"[green]ingest completed[/green] inserted={result.inserted} updated={result.updated} failed={result.failed}"
    )


@app.command()
def analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    )
) -> None:
    """Run LLM analysis for prepared items."""

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


def _resolve_db_path(*, db_path: Path | None, config_path: Path | None) -> Path:
    if isinstance(db_path, Path):
        normalized = db_path.expanduser().resolve()
        if str(normalized).strip():
            return normalized

    env_path = str(importlib.import_module("os").getenv("RECOLETA_DB_PATH", "")).strip()
    if env_path:
        return Path(env_path).expanduser().resolve()

    resolved_config_path: Path | None = None
    if isinstance(config_path, Path):
        resolved_config_path = config_path.expanduser().resolve()
    else:
        raw = str(importlib.import_module("os").getenv("RECOLETA_CONFIG_PATH", "")).strip()
        if raw:
            resolved_config_path = Path(raw).expanduser().resolve()

    if resolved_config_path is None:
        raise ValueError("Missing db path (pass --db-path or set RECOLETA_DB_PATH / RECOLETA_CONFIG_PATH).")
    if not resolved_config_path.exists():
        raise ValueError(f"Config path does not exist: {resolved_config_path}")
    if not resolved_config_path.is_file():
        raise ValueError(f"Config path must be a file: {resolved_config_path}")

    suffix = resolved_config_path.suffix.lower()
    raw_text = resolved_config_path.read_text(encoding="utf-8")
    if suffix == ".json":
        loaded = json.loads(raw_text)
    elif suffix in {".yaml", ".yml"}:
        yaml = _import_symbol("yaml")
        loaded = yaml.safe_load(raw_text)
    else:
        raise ValueError(f"Unsupported config file type: {resolved_config_path.suffix} (expected .yaml/.yml/.json)")

    if not isinstance(loaded, dict):
        raise ValueError("Config file must contain a mapping/object at the top level")

    candidate = loaded.get("recoleta_db_path") or loaded.get("RECOLETA_DB_PATH")
    candidate_str = str(candidate or "").strip()
    if not candidate_str:
        raise ValueError("Config does not define recoleta_db_path (or RECOLETA_DB_PATH).")
    return Path(candidate_str).expanduser().resolve()


@db_app.command("clear")
def db_clear(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm deletion without prompting.",
    ),
) -> None:
    """Delete the configured SQLite DB file (and sidecar files) for a clean slate."""

    symbols = _runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]

    console = console_cls()
    if not yes:
        console.print("[red]refusing to delete db without --yes[/red]")
        raise typer.Exit(code=2)

    try:
        resolved = _resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise typer.Exit(code=2) from exc

    to_delete = [
        resolved,
        Path(f"{resolved}-wal"),
        Path(f"{resolved}-shm"),
        Path(f"{resolved}-journal"),
    ]
    deleted: list[str] = []
    for path in to_delete:
        try:
            if path.exists():
                path.unlink()
                deleted.append(str(path))
        except Exception as exc:  # noqa: BLE001
            logger.bind(module="cli.db.clear").warning("db delete failed path={} error={}", str(path), str(exc))
            console.print(f"[red]failed to delete[/red] {path}")
            raise typer.Exit(code=1) from exc

    if deleted:
        console.print(f"[green]db cleared[/green] deleted={len(deleted)} path={resolved}")
    else:
        console.print(f"[green]db already empty[/green] path={resolved}")


@db_app.command("reset")
def db_reset(
    db_path: Path | None = typer.Option(None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."),
    config_path: Path | None = typer.Option(None, "--config", help="Path to config file used to resolve recoleta_db_path."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Confirm deletion without prompting."),
) -> None:
    """Alias for `recoleta db clear`."""

    db_clear(db_path=db_path, config_path=config_path, yes=yes)


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
        _execute_stage(stage_name="ingest", stage_runner=lambda service, run_id: service.prepare(run_id=run_id))

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
