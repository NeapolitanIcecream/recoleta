from __future__ import annotations

from typing import Any

import recoleta.cli as cli
from recoleta.cli import workflow_models as _workflow_models
from recoleta.cli.workflow_models import WorkflowExecutionContext
from recoleta.cli.workflow_runner import (
    GranularityPlanRequest,
    WorkflowLoopRequest,
    WorkflowPayloadContext,
    begin_workflow_runtime,
    build_deploy_plan as _build_deploy_plan,
    build_granularity_plan as _build_granularity_plan,
    execute_workflow_loop,
    finalize_workflow_success,
    finish_workflow_failure,
    granularity_stack as _granularity_stack,
    granularity_workflow_payload,
    latest_complete_utc_day,
    parse_step_list as _parse_step_list,
    today_utc,
    validate_step_overrides as _validate_step_overrides,
    deploy_workflow_payload,
)

STEP_INGEST = _workflow_models.STEP_INGEST
STEP_ANALYZE = _workflow_models.STEP_ANALYZE
STEP_PUBLISH = _workflow_models.STEP_PUBLISH
STEP_TRENDS_DAY = _workflow_models.STEP_TRENDS_DAY
STEP_IDEAS_DAY = _workflow_models.STEP_IDEAS_DAY
STEP_TRENDS_WEEK = _workflow_models.STEP_TRENDS_WEEK
STEP_IDEAS_WEEK = _workflow_models.STEP_IDEAS_WEEK
STEP_TRENDS_MONTH = _workflow_models.STEP_TRENDS_MONTH
STEP_IDEAS_MONTH = _workflow_models.STEP_IDEAS_MONTH
STEP_TRANSLATE = _workflow_models.STEP_TRANSLATE
STEP_SITE_BUILD = _workflow_models.STEP_SITE_BUILD
STEP_SITE_DEPLOY = _workflow_models.STEP_SITE_DEPLOY


def _today_utc():
    return today_utc()


def _latest_complete_utc_day():
    return latest_complete_utc_day()


_MONKEYPATCHABLE_CLOCK_HOOKS = (_today_utc, _latest_complete_utc_day)


def execute_granularity_workflow(**kwargs: Any) -> dict[str, Any]:
    workflow_name = str(kwargs["workflow_name"])
    command = str(kwargs["command"])
    include_steps = _parse_step_list(kwargs.get("include"))
    skip_steps = _parse_step_list(kwargs.get("skip"))
    _validate_step_overrides(
        workflow_name=workflow_name,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
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
    ) = begin_workflow_runtime(
        command=command,
        log_module=f"cli.workflow.{workflow_name}",
        config_path=kwargs.get("config_path"),
    )
    plan = None
    executed_steps: list[str] = []
    billing_metrics_by_step: dict[str, list[Any]] = {}
    terminal_state = "failed"
    step_results = []
    try:
        plan = _build_granularity_plan(
            request=GranularityPlanRequest(
                workflow_name=workflow_name,
                command=command,
                anchor_date=kwargs.get("anchor_date"),
                settings=settings,
                include_steps=include_steps,
                skip_steps=skip_steps,
            )
        )
        policy = settings.workflow_policy_for_granularity(plan.target_granularity or "day")
        translate_granularities = _granularity_stack(
            target_granularity=plan.target_granularity or "day",
            recursive_lower_levels=bool(policy.recursive_lower_levels),
        )
        cli._update_run_context(
            repository,
            run_id=run_id,
            command=command,
            operation_kind=plan.operation_kind,
            scope="default",
            granularity=plan.target_granularity,
            period_start=plan.target_period_start,
            period_end=plan.target_period_end,
            target_granularity=plan.target_granularity,
            target_period_start=plan.target_period_start,
            target_period_end=plan.target_period_end,
            requested_steps=plan.requested_steps,
            skipped_steps=plan.skipped_steps,
        )
        execution_context = WorkflowExecutionContext(
            repository=repository,
            service=service,
            settings=settings,
            run_id=run_id,
            target_granularity=plan.target_granularity,
            target_period_start=plan.target_period_start,
            target_period_end=plan.target_period_end,
            translate_include=list(policy.translate_include),
            translate_granularities=translate_granularities,
            delivery_mode=policy.delivery_mode,
            publish_requested_explicitly=STEP_PUBLISH in include_steps,
            analyze_limit=int(getattr(settings, "analyze_limit", 100) or 100),
            publish_limit=max(50, int(getattr(settings, "analyze_limit", 100) or 100)),
            repo_dir=None,
            remote="origin",
            branch="gh-pages",
            commit_message=None,
            cname=None,
            pages_config="auto",
            force=True,
        )
        executed_steps, billing_metrics_by_step, terminal_state, step_results = (
            execute_workflow_loop(
                request=WorkflowLoopRequest(
                    repository=repository,
                    heartbeat_monitor=heartbeat_monitor,
                    plan=plan,
                    execution_context=execution_context,
                    json_output=bool(kwargs.get("json_output", False)),
                    on_translate_failure=str(policy.on_translate_failure or "fail"),
                )
            )
        )
        heartbeat_monitor.raise_if_failed()
        finalize_workflow_success(
            repository=repository,
            run_id=run_id,
            executed_steps=executed_steps,
            billing_metrics_by_step=billing_metrics_by_step,
            terminal_state=terminal_state,
        )
    except KeyboardInterrupt as exc:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Workflow finish failed during interrupt",
        )
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="Workflow interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Workflow finish failed after lease loss",
        )
        log.warning(
            "Workflow stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Workflow finish failed during exception handling",
        )
        log.exception("Workflow execution failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )
    assert plan is not None
    payload = granularity_workflow_payload(
        context=WorkflowPayloadContext(
            command=command,
            run_id=run_id,
            plan=plan,
            metrics=repository.list_metrics(run_id=run_id),
            executed_steps=executed_steps,
            billing_metrics_by_step=billing_metrics_by_step,
            terminal_state=terminal_state,
            step_results=step_results,
        )
    )
    if bool(kwargs.get("json_output", False)):
        if bool(kwargs.get("emit_output", True)):
            cli._emit_json(payload)
        return payload
    if bool(kwargs.get("emit_output", True)):
        console.print(
            f"[green]{command} completed[/green] "
            f"run_id={run_id} terminal_state={terminal_state} "
            f"steps={len(executed_steps)}/{len(plan.requested_steps)}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
    return payload


def execute_deploy_workflow(**kwargs: Any) -> dict[str, Any]:
    command = str(kwargs["command"])
    include_steps = _parse_step_list(kwargs.get("include"))
    skip_steps = _parse_step_list(kwargs.get("skip"))
    _validate_step_overrides(
        workflow_name="deploy",
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
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
    ) = begin_workflow_runtime(
        command=command,
        log_module="cli.workflow.deploy",
        config_path=kwargs.get("config_path"),
    )
    _ = service
    plan = None
    executed_steps: list[str] = []
    billing_metrics_by_step: dict[str, list[Any]] = {}
    terminal_state = "failed"
    step_results = []
    try:
        plan = _build_deploy_plan(
            command=command,
            settings=settings,
            include_steps=include_steps,
            skip_steps=skip_steps,
        )
        cli._update_run_context(
            repository,
            run_id=run_id,
            command=command,
            operation_kind=plan.operation_kind,
            requested_steps=plan.requested_steps,
            skipped_steps=plan.skipped_steps,
        )
        execution_context = WorkflowExecutionContext(
            repository=repository,
            service=service,
            settings=settings,
            run_id=run_id,
            target_granularity=None,
            target_period_start=None,
            target_period_end=None,
            translate_include=list(settings.workflows.deploy.translate_include),
            translate_granularities=None,
            delivery_mode=None,
            publish_requested_explicitly=False,
                analyze_limit=None,
                publish_limit=0,
            repo_dir=kwargs.get("repo_dir"),
            remote=str(kwargs.get("remote", "origin")),
            branch=str(kwargs.get("branch", "gh-pages")),
            commit_message=kwargs.get("commit_message"),
            cname=kwargs.get("cname"),
            pages_config=str(kwargs.get("pages_config", "auto")),
            force=bool(kwargs.get("force", True)),
            item_export_scope=str(kwargs.get("item_export_scope", "linked")),
        )
        executed_steps, billing_metrics_by_step, terminal_state, step_results = (
            execute_workflow_loop(
                request=WorkflowLoopRequest(
                    repository=repository,
                    heartbeat_monitor=heartbeat_monitor,
                    plan=plan,
                    execution_context=execution_context,
                    json_output=bool(kwargs.get("json_output", False)),
                    on_translate_failure=str(
                        settings.workflows.deploy.on_translate_failure or "fail"
                    ),
                )
            )
        )
        heartbeat_monitor.raise_if_failed()
        finalize_workflow_success(
            repository=repository,
            run_id=run_id,
            executed_steps=executed_steps,
            billing_metrics_by_step=billing_metrics_by_step,
            terminal_state=terminal_state,
        )
    except KeyboardInterrupt as exc:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Deploy finish failed during interrupt",
        )
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="Workflow interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Deploy finish failed after lease loss",
        )
        log.warning(
            "Deploy stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        finish_workflow_failure(
            repository=repository,
            run_id=run_id,
            log=log,
            message="Deploy finish failed during exception handling",
        )
        log.exception("Deploy execution failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )
    assert plan is not None
    payload = deploy_workflow_payload(
        context=WorkflowPayloadContext(
            command=command,
            run_id=run_id,
            plan=plan,
            metrics=repository.list_metrics(run_id=run_id),
            executed_steps=executed_steps,
            billing_metrics_by_step=billing_metrics_by_step,
            terminal_state=terminal_state,
            step_results=step_results,
        )
    )
    if bool(kwargs.get("json_output", False)):
        if bool(kwargs.get("emit_output", True)):
            cli._emit_json(payload)
        return payload
    if bool(kwargs.get("emit_output", True)):
        console.print(
            f"[green]{command} completed[/green] "
            f"run_id={run_id} terminal_state={terminal_state} "
            f"steps={len(executed_steps)}/{len(plan.requested_steps)}"
        )
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
    return payload


def run_daemon_start_command() -> None:
    settings = cli._build_settings()
    console = cli._runtime_symbols()["Console"](stderr=bool(getattr(settings, "log_json", False)))
    scheduler = _build_scheduler()
    _register_daemon_schedules(scheduler=scheduler, settings=settings)
    console.print("[cyan]daemon started[/cyan]")
    _run_scheduler(scheduler=scheduler)


def _build_scheduler() -> Any:
    blocking_scheduler_cls = cli._import_symbol(
        "apscheduler.schedulers.blocking",
        attr_name="BlockingScheduler",
    )
    return blocking_scheduler_cls(
        timezone="UTC",
        executors={"default": {"type": "threadpool", "max_workers": 1}},
        job_defaults={"coalesce": True, "max_instances": 1},
    )


def _register_daemon_schedules(*, scheduler: Any, settings: Any) -> None:
    schedules = list(getattr(settings.daemon, "schedules", []) or [])
    for schedule_index, schedule in enumerate(schedules):
        workflow_name = str(getattr(schedule, "workflow", "") or "").strip().lower()
        trigger, trigger_kwargs = _schedule_trigger_args(schedule=schedule)
        scheduler.add_job(
            _scheduled_workflow_runner(workflow_name),
            trigger,
            **trigger_kwargs,
            id=_schedule_job_id(
                workflow_name=workflow_name,
                schedule=schedule,
                schedule_index=schedule_index,
            ),
            replace_existing=True,
        )


def _schedule_job_id(*, workflow_name: str, schedule: Any, schedule_index: int) -> str:
    if getattr(schedule, "interval_minutes", None) is not None:
        return f"workflow:{workflow_name}:interval:{int(schedule.interval_minutes)}:{schedule_index}"
    return (
        "workflow:"
        f"{workflow_name}:cron:{str(schedule.weekday)}:"
        f"{int(schedule.hour_utc)}:{int(schedule.minute_utc)}:{schedule_index}"
    )


def _schedule_trigger_args(*, schedule: Any) -> tuple[str, dict[str, Any]]:
    if getattr(schedule, "interval_minutes", None) is not None:
        return "interval", {"minutes": int(schedule.interval_minutes)}
    return (
        "cron",
        {
            "day_of_week": str(schedule.weekday),
            "hour": int(schedule.hour_utc),
            "minute": int(schedule.minute_utc),
        },
    )


def _scheduled_workflow_runner(workflow_name: str) -> Any:
    def _run() -> None:
        if workflow_name in {"now", "day", "week", "month"}:
            execute_granularity_workflow(
                workflow_name=workflow_name,
                command=f"daemon {workflow_name}",
            )
            return
        if workflow_name == "deploy":
            execute_deploy_workflow(command="daemon deploy")
            return
        raise ValueError(f"unsupported daemon workflow: {workflow_name}")

    return _run


def _run_scheduler(*, scheduler: Any) -> None:
    scheduler_log = cli._runtime_symbols()["logger"].bind(module="cli.daemon.start")
    try:
        with cli._graceful_shutdown_signals():
            scheduler.start()
    except KeyboardInterrupt as exc:
        scheduler_log.warning(
            "Daemon stopping signal={} exit_code={} waiting_for_jobs=true",
            cli._interrupt_signal_name(exc),
            cli._interrupt_exit_code(exc),
        )
        try:
            scheduler.shutdown(wait=True)
        except KeyboardInterrupt:
            scheduler_log.warning(
                "Daemon shutdown interrupted again; forcing stop without waiting."
            )
            try:
                scheduler.shutdown(wait=False)
            except Exception:
                scheduler_log.exception("Forced daemon shutdown failed")
        except Exception:
            scheduler_log.exception("Daemon shutdown failed during interrupt")
        raise cli.typer.Exit(code=cli._interrupt_exit_code(exc)) from None
