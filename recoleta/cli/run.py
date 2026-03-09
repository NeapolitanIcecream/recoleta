from __future__ import annotations

import recoleta.cli as cli


def run_scheduler_command(
    *,
    once: bool,
    analyze_limit: int | None,
    publish_limit: int,
) -> None:
    symbols = cli._runtime_symbols()
    logger = symbols["logger"]

    if once:
        run_pipeline_once(
            analyze_limit=analyze_limit,
            publish_limit=publish_limit,
        )
        return

    console_cls = symbols["Console"]
    settings, _, _ = cli._build_runtime()
    console = console_cls(stderr=settings.log_json)

    blocking_scheduler_cls = cli._import_symbol(
        "apscheduler.schedulers.blocking",
        attr_name="BlockingScheduler",
    )
    scheduler = blocking_scheduler_cls(
        timezone="UTC",
        executors={"default": {"type": "threadpool", "max_workers": 1}},
        job_defaults={"coalesce": True, "max_instances": 1},
    )

    def run_ingest_job() -> None:
        cli._execute_stage(
            stage_name="ingest",
            stage_runner=lambda service, run_id: service.prepare(run_id=run_id),
        )

    def run_analyze_job() -> None:
        cli._execute_stage(
            stage_name="analyze",
            stage_runner=lambda service, run_id: service.analyze(run_id=run_id),
        )

    def run_publish_job() -> None:
        cli._execute_stage(
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
    scheduler_log = logger.bind(module="cli.run.scheduler")
    try:
        with cli._graceful_shutdown_signals():
            scheduler.start()
    except KeyboardInterrupt as exc:
        scheduler_log.warning(
            "Scheduler stopping signal={} exit_code={} waiting_for_jobs=true",
            cli._interrupt_signal_name(exc),
            cli._interrupt_exit_code(exc),
        )
        try:
            scheduler.shutdown(wait=True)
        except KeyboardInterrupt:
            scheduler_log.warning(
                "Scheduler shutdown interrupted again; forcing stop without waiting."
            )
            try:
                scheduler.shutdown(wait=False)
            except Exception:
                scheduler_log.exception("Forced scheduler shutdown failed")
        except Exception:
            scheduler_log.exception("Scheduler shutdown failed during interrupt")
        raise cli.typer.Exit(code=cli._interrupt_exit_code(exc)) from None


def run_pipeline_once(*, analyze_limit: int | None, publish_limit: int) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = cli._begin_managed_run(
        command="run --once",
        log_module="cli.run.once",
    )

    try:
        with cli._graceful_shutdown_signals():
            ingest_result = service.prepare(run_id=run_id)
            heartbeat_monitor.raise_if_failed()
            analyze_result = service.analyze(run_id=run_id, limit=analyze_limit)
            heartbeat_monitor.raise_if_failed()
            publish_result = service.publish(run_id=run_id, limit=publish_limit)
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=True)
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="Run interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "Run stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        log.exception("Run failed")
        raise
    else:
        console.print(
            "[green]run --once completed[/green] "
            f"ingest(inserted={ingest_result.inserted} updated={ingest_result.updated} failed={ingest_result.failed}) "
            f"analyze(processed={analyze_result.processed} failed={analyze_result.failed}) "
            f"publish(sent={publish_result.sent} skipped={publish_result.skipped} failed={publish_result.failed})"
        )
        if "markdown" in settings.publish_targets:
            console.print(
                f"[cyan]markdown output[/cyan] {settings.markdown_output_dir}"
            )
            console.print(
                f"[cyan]latest index[/cyan] {settings.markdown_output_dir / 'latest.md'}"
            )
        if (
            "obsidian" in settings.publish_targets
            and settings.obsidian_vault_path is not None
        ):
            console.print(
                f"[cyan]obsidian notes[/cyan] {settings.obsidian_vault_path / settings.obsidian_base_folder / 'Inbox'}"
            )
    finally:
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )
