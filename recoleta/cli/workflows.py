from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, NoReturn

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


@dataclass(slots=True)
class _ManagedWorkflowRuntime:
    settings: Any
    repository: Any
    service: Any
    console: Any
    run_id: str
    owner_token: str
    log: Any
    heartbeat_monitor: Any
    workspace_lease_lost_error: type[Exception]


@dataclass(slots=True)
class _WorkflowLoopOutcome:
    executed_steps: list[str] = field(default_factory=list)
    billing_metrics_by_step: dict[str, list[Any]] = field(default_factory=dict)
    terminal_state: str = "failed"
    step_results: list[Any] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class _WorkflowFailureMessages:
    interrupt_finish: str
    lease_finish: str
    exception_finish: str
    interrupted: str
    lease_stopped: str
    exception_log: str


@dataclass(frozen=True, slots=True)
class _ManagedWorkflowLoopRequest:
    runtime: _ManagedWorkflowRuntime
    plan: Any
    execution_context: WorkflowExecutionContext
    json_output: bool
    on_translate_failure: str
    failure_messages: _WorkflowFailureMessages


@dataclass(frozen=True, slots=True)
class _WorkflowPayloadRequest:
    payload: dict[str, Any]
    runtime: _ManagedWorkflowRuntime
    command: str
    terminal_state: str
    executed_steps: list[str]
    requested_steps: list[str]
    json_output: bool
    emit_output: bool


@dataclass(frozen=True, slots=True)
class _GranularityContextRequest:
    runtime: _ManagedWorkflowRuntime
    workflow_name: str
    command: str
    anchor_date: Any
    include_steps: list[str]
    skip_steps: list[str]


@dataclass(frozen=True, slots=True)
class _GranularityWorkflowContext:
    plan: Any
    execution_context: WorkflowExecutionContext
    on_translate_failure: str


@dataclass(frozen=True, slots=True)
class _DeployContextRequest:
    runtime: _ManagedWorkflowRuntime
    command: str
    include_steps: list[str]
    skip_steps: list[str]
    repo_dir: Any
    remote: str
    branch: str
    commit_message: Any
    cname: Any
    pages_config: str
    force: bool
    item_export_scope: str


@dataclass(frozen=True, slots=True)
class _DeployWorkflowContext:
    plan: Any
    execution_context: WorkflowExecutionContext
    on_translate_failure: str


@dataclass(frozen=True, slots=True)
class _ManagedWorkflowRunRequest:
    runtime: _ManagedWorkflowRuntime
    command: str
    kwargs: dict[str, Any]
    prepare_context: Callable[[], Any]
    payload_builder: Callable[[Any, _WorkflowLoopOutcome], dict[str, Any]]
    failure_messages: _WorkflowFailureMessages


_GRANULARITY_FAILURE_MESSAGES = _WorkflowFailureMessages(
    interrupt_finish="Workflow finish failed during interrupt",
    lease_finish="Workflow finish failed after lease loss",
    exception_finish="Workflow finish failed during exception handling",
    interrupted="Workflow interrupted",
    lease_stopped="Workflow stopped because workspace lease was lost",
    exception_log="Workflow execution failed",
)

_DEPLOY_FAILURE_MESSAGES = _WorkflowFailureMessages(
    interrupt_finish="Deploy finish failed during interrupt",
    lease_finish="Deploy finish failed after lease loss",
    exception_finish="Deploy finish failed during exception handling",
    interrupted="Workflow interrupted",
    lease_stopped="Deploy stopped because workspace lease was lost",
    exception_log="Deploy execution failed",
)


def _workflow_step_overrides(
    *,
    workflow_name: str,
    kwargs: dict[str, Any],
) -> tuple[list[str], list[str]]:
    include_steps = _parse_step_list(kwargs.get("include"))
    skip_steps = _parse_step_list(kwargs.get("skip"))
    _validate_step_overrides(
        workflow_name=workflow_name,
        include_steps=include_steps,
        skip_steps=skip_steps,
    )
    return include_steps, skip_steps


def _begin_managed_workflow(
    *,
    command: str,
    log_module: str,
    config_path: Any,
) -> _ManagedWorkflowRuntime:
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
        log_module=log_module,
        config_path=config_path,
    )
    return _ManagedWorkflowRuntime(
        settings=settings,
        repository=repository,
        service=service,
        console=console,
        run_id=run_id,
        owner_token=owner_token,
        log=log,
        heartbeat_monitor=heartbeat_monitor,
        workspace_lease_lost_error=workspace_lease_lost_error,
    )


def _workflow_loop_request(
    request: _ManagedWorkflowLoopRequest,
) -> WorkflowLoopRequest:
    return WorkflowLoopRequest(
        repository=request.runtime.repository,
        heartbeat_monitor=request.runtime.heartbeat_monitor,
        plan=request.plan,
        execution_context=request.execution_context,
        json_output=request.json_output,
        on_translate_failure=request.on_translate_failure,
    )


def _workflow_loop_outcome(
    result: tuple[list[str], dict[str, list[Any]], str, list[Any]],
) -> _WorkflowLoopOutcome:
    return _WorkflowLoopOutcome(
        executed_steps=result[0],
        billing_metrics_by_step=result[1],
        terminal_state=result[2],
        step_results=result[3],
    )


def _finalize_managed_workflow_loop(
    *,
    request: _ManagedWorkflowLoopRequest,
    outcome: _WorkflowLoopOutcome,
) -> None:
    finalize_workflow_success(
        repository=request.runtime.repository,
        run_id=request.runtime.run_id,
        executed_steps=outcome.executed_steps,
        billing_metrics_by_step=outcome.billing_metrics_by_step,
        terminal_state=outcome.terminal_state,
    )


def _handle_managed_loop_interrupt(
    *,
    request: _ManagedWorkflowLoopRequest,
    exc: KeyboardInterrupt,
) -> NoReturn:
    finish_workflow_failure(
        repository=request.runtime.repository,
        run_id=request.runtime.run_id,
        log=request.runtime.log,
        message=request.failure_messages.interrupt_finish,
    )
    cli._raise_typer_exit_for_interrupt(
        log=request.runtime.log,
        message=request.failure_messages.interrupted,
        exc=exc,
    )


def _handle_managed_loop_lease_loss(
    *,
    request: _ManagedWorkflowLoopRequest,
    exc: Exception,
) -> NoReturn:
    finish_workflow_failure(
        repository=request.runtime.repository,
        run_id=request.runtime.run_id,
        log=request.runtime.log,
        message=request.failure_messages.lease_finish,
    )
    request.runtime.log.warning(
        "{} error_type={} error={}",
        request.failure_messages.lease_stopped,
        type(exc).__name__,
        str(exc),
    )
    raise cli.typer.Exit(code=1) from None


def _handle_managed_loop_exception(
    *,
    request: _ManagedWorkflowLoopRequest,
) -> None:
    finish_workflow_failure(
        repository=request.runtime.repository,
        run_id=request.runtime.run_id,
        log=request.runtime.log,
        message=request.failure_messages.exception_finish,
    )
    request.runtime.log.exception(request.failure_messages.exception_log)


def _execute_managed_workflow_loop(
    *,
    request: _ManagedWorkflowLoopRequest,
) -> _WorkflowLoopOutcome:
    try:
        outcome = _workflow_loop_outcome(
            execute_workflow_loop(request=_workflow_loop_request(request))
        )
        request.runtime.heartbeat_monitor.raise_if_failed()
        _finalize_managed_workflow_loop(request=request, outcome=outcome)
        return outcome
    except KeyboardInterrupt as exc:
        _handle_managed_loop_interrupt(
            request=request,
            exc=exc,
        )
    except request.runtime.workspace_lease_lost_error as exc:
        _handle_managed_loop_lease_loss(
            request=request,
            exc=exc,
        )
    except Exception:
        _handle_managed_loop_exception(request=request)
        raise


def _print_workflow_completion(
    *,
    request: _WorkflowPayloadRequest,
) -> None:
    request.runtime.console.print(
        f"[green]{request.command} completed[/green] "
        f"run_id={request.runtime.run_id} terminal_state={request.terminal_state} "
        f"steps={len(request.executed_steps)}/{len(request.requested_steps)}"
    )
    cli._print_billing_report(
        console=request.runtime.console,
        repository=request.runtime.repository,
        run_id=request.runtime.run_id,
    )


def _emit_workflow_payload(
    *,
    request: _WorkflowPayloadRequest,
) -> dict[str, Any]:
    if request.json_output:
        if request.emit_output:
            cli._emit_json(request.payload)
        return request.payload
    if request.emit_output:
        _print_workflow_completion(request=request)
    return request.payload


def _granularity_analyze_limit(*, settings: Any) -> int:
    return int(getattr(settings, "analyze_limit", 100) or 100)


def _granularity_workflow_context(
    request: _GranularityContextRequest,
) -> _GranularityWorkflowContext:
    plan = _build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name=request.workflow_name,
            command=request.command,
            anchor_date=request.anchor_date,
            settings=request.runtime.settings,
            include_steps=request.include_steps,
            skip_steps=request.skip_steps,
        )
    )
    policy = request.runtime.settings.workflow_policy_for_granularity(
        plan.target_granularity or "day"
    )
    translate_granularities = _granularity_stack(
        target_granularity=plan.target_granularity or "day",
        recursive_lower_levels=bool(policy.recursive_lower_levels),
    )
    cli._update_run_context(
        request.runtime.repository,
        run_id=request.runtime.run_id,
        command=request.command,
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
    analyze_limit = _granularity_analyze_limit(settings=request.runtime.settings)
    execution_context = WorkflowExecutionContext(
        repository=request.runtime.repository,
        service=request.runtime.service,
        settings=request.runtime.settings,
        run_id=request.runtime.run_id,
        target_granularity=plan.target_granularity,
        target_period_start=plan.target_period_start,
        target_period_end=plan.target_period_end,
        on_translate_failure=str(policy.on_translate_failure or "fail"),
        translate_include=list(policy.translate_include),
        translate_granularities=translate_granularities,
        delivery_mode=policy.delivery_mode,
        publish_requested_explicitly=STEP_PUBLISH in request.include_steps,
        analyze_limit=analyze_limit,
        publish_limit=max(50, analyze_limit),
        repo_dir=None,
        remote="origin",
        branch="gh-pages",
        commit_message=None,
        cname=None,
        pages_config="auto",
        force=True,
    )
    return _GranularityWorkflowContext(
        plan=plan,
        execution_context=execution_context,
        on_translate_failure=str(policy.on_translate_failure or "fail"),
    )


def _granularity_workflow_payload(
    *,
    command: str,
    runtime: _ManagedWorkflowRuntime,
    plan: Any,
    outcome: _WorkflowLoopOutcome,
) -> dict[str, Any]:
    return granularity_workflow_payload(
        context=WorkflowPayloadContext(
            command=command,
            run_id=runtime.run_id,
            plan=plan,
            metrics=runtime.repository.list_metrics(run_id=runtime.run_id),
            executed_steps=outcome.executed_steps,
            billing_metrics_by_step=outcome.billing_metrics_by_step,
            terminal_state=outcome.terminal_state,
            step_results=outcome.step_results,
        )
    )


def _deploy_workflow_context(
    request: _DeployContextRequest,
) -> _DeployWorkflowContext:
    plan = _build_deploy_plan(
        command=request.command,
        settings=request.runtime.settings,
        include_steps=request.include_steps,
        skip_steps=request.skip_steps,
    )
    cli._update_run_context(
        request.runtime.repository,
        run_id=request.runtime.run_id,
        command=request.command,
        operation_kind=plan.operation_kind,
        requested_steps=plan.requested_steps,
        skipped_steps=plan.skipped_steps,
    )
    return _DeployWorkflowContext(
        plan=plan,
        execution_context=WorkflowExecutionContext(
            repository=request.runtime.repository,
            service=request.runtime.service,
            settings=request.runtime.settings,
            run_id=request.runtime.run_id,
            target_granularity=None,
            target_period_start=None,
            target_period_end=None,
            on_translate_failure=str(
                request.runtime.settings.workflows.deploy.on_translate_failure
                or "fail"
            ),
            translate_include=list(
                request.runtime.settings.workflows.deploy.translate_include
            ),
            translate_granularities=None,
            delivery_mode=None,
            publish_requested_explicitly=False,
            analyze_limit=None,
            publish_limit=0,
            repo_dir=request.repo_dir,
            remote=request.remote,
            branch=request.branch,
            commit_message=request.commit_message,
            cname=request.cname,
            pages_config=request.pages_config,
            force=request.force,
            item_export_scope=request.item_export_scope,
        ),
        on_translate_failure=str(
            request.runtime.settings.workflows.deploy.on_translate_failure or "fail"
        ),
    )


def _deploy_workflow_payload(
    *,
    command: str,
    runtime: _ManagedWorkflowRuntime,
    plan: Any,
    outcome: _WorkflowLoopOutcome,
) -> dict[str, Any]:
    return deploy_workflow_payload(
        context=WorkflowPayloadContext(
            command=command,
            run_id=runtime.run_id,
            plan=plan,
            metrics=runtime.repository.list_metrics(run_id=runtime.run_id),
            executed_steps=outcome.executed_steps,
            billing_metrics_by_step=outcome.billing_metrics_by_step,
            terminal_state=outcome.terminal_state,
            step_results=outcome.step_results,
        )
    )


def _run_managed_workflow(
    request: _ManagedWorkflowRunRequest,
) -> dict[str, Any]:
    loop_started = False
    try:
        context = request.prepare_context()
        loop_started = True
        outcome = _execute_managed_workflow_loop(
            request=_ManagedWorkflowLoopRequest(
                runtime=request.runtime,
                plan=context.plan,
                execution_context=context.execution_context,
                json_output=bool(request.kwargs.get("json_output", False)),
                on_translate_failure=context.on_translate_failure,
                failure_messages=request.failure_messages,
            )
        )
        return _emit_workflow_payload(
            request=_WorkflowPayloadRequest(
                payload=request.payload_builder(context, outcome),
                runtime=request.runtime,
                command=request.command,
                terminal_state=outcome.terminal_state,
                executed_steps=outcome.executed_steps,
                requested_steps=context.plan.requested_steps,
                json_output=bool(request.kwargs.get("json_output", False)),
                emit_output=bool(request.kwargs.get("emit_output", True)),
            )
        )
    except KeyboardInterrupt as exc:
        if not loop_started:
            _handle_preloop_interrupt(
                runtime=request.runtime,
                exc=exc,
                finish_message=request.failure_messages.interrupt_finish,
                interrupt_message=request.failure_messages.interrupted,
            )
        raise
    except request.runtime.workspace_lease_lost_error as exc:
        if not loop_started:
            _handle_preloop_lease_loss(
                runtime=request.runtime,
                exc=exc,
                finish_message=request.failure_messages.lease_finish,
                warning_message=request.failure_messages.lease_stopped,
            )
        raise
    except Exception:
        if not loop_started:
            _handle_preloop_exception(
                runtime=request.runtime,
                finish_message=request.failure_messages.exception_finish,
                exception_message=request.failure_messages.exception_log,
            )
        raise
    finally:
        cli._cleanup_managed_run(
            repository=request.runtime.repository,
            owner_token=request.runtime.owner_token,
            heartbeat_monitor=request.runtime.heartbeat_monitor,
            log=request.runtime.log,
        )


def _handle_preloop_interrupt(
    *,
    runtime: _ManagedWorkflowRuntime,
    exc: KeyboardInterrupt,
    finish_message: str,
    interrupt_message: str,
) -> None:
    finish_workflow_failure(
        repository=runtime.repository,
        run_id=runtime.run_id,
        log=runtime.log,
        message=finish_message,
    )
    cli._raise_typer_exit_for_interrupt(
        log=runtime.log,
        message=interrupt_message,
        exc=exc,
    )


def _handle_preloop_lease_loss(
    *,
    runtime: _ManagedWorkflowRuntime,
    exc: Exception,
    finish_message: str,
    warning_message: str,
) -> None:
    finish_workflow_failure(
        repository=runtime.repository,
        run_id=runtime.run_id,
        log=runtime.log,
        message=finish_message,
    )
    runtime.log.warning(
        "{} error_type={} error={}",
        warning_message,
        type(exc).__name__,
        str(exc),
    )
    raise cli.typer.Exit(code=1) from None


def _handle_preloop_exception(
    *,
    runtime: _ManagedWorkflowRuntime,
    finish_message: str,
    exception_message: str,
) -> None:
    finish_workflow_failure(
        repository=runtime.repository,
        run_id=runtime.run_id,
        log=runtime.log,
        message=finish_message,
    )
    runtime.log.exception(exception_message)


def execute_granularity_workflow(**kwargs: Any) -> dict[str, Any]:
    workflow_name = str(kwargs["workflow_name"])
    command = str(kwargs["command"])
    include_steps, skip_steps = _workflow_step_overrides(
        workflow_name=workflow_name,
        kwargs=kwargs,
    )
    runtime = _begin_managed_workflow(
        command=command,
        log_module=f"cli.workflow.{workflow_name}",
        config_path=kwargs.get("config_path"),
    )
    return _run_managed_workflow(
        request=_ManagedWorkflowRunRequest(
            runtime=runtime,
            command=command,
            kwargs=kwargs,
            prepare_context=lambda: _granularity_workflow_context(
                _GranularityContextRequest(
                    runtime=runtime,
                    workflow_name=workflow_name,
                    command=command,
                    anchor_date=kwargs.get("anchor_date"),
                    include_steps=include_steps,
                    skip_steps=skip_steps,
                )
            ),
            payload_builder=lambda context, outcome: _granularity_workflow_payload(
                command=command,
                runtime=runtime,
                plan=context.plan,
                outcome=outcome,
            ),
            failure_messages=_GRANULARITY_FAILURE_MESSAGES,
        )
    )


def execute_deploy_workflow(**kwargs: Any) -> dict[str, Any]:
    command = str(kwargs["command"])
    include_steps, skip_steps = _workflow_step_overrides(
        workflow_name="deploy",
        kwargs=kwargs,
    )
    runtime = _begin_managed_workflow(
        command=command,
        log_module="cli.workflow.deploy",
        config_path=kwargs.get("config_path"),
    )
    return _run_managed_workflow(
        request=_ManagedWorkflowRunRequest(
            runtime=runtime,
            command=command,
            kwargs=kwargs,
            prepare_context=lambda: _deploy_workflow_context(
                _DeployContextRequest(
                    runtime=runtime,
                    command=command,
                    include_steps=include_steps,
                    skip_steps=skip_steps,
                    repo_dir=kwargs.get("repo_dir"),
                    remote=str(kwargs.get("remote", "origin")),
                    branch=str(kwargs.get("branch", "gh-pages")),
                    commit_message=kwargs.get("commit_message"),
                    cname=kwargs.get("cname"),
                    pages_config=str(kwargs.get("pages_config", "auto")),
                    force=bool(kwargs.get("force", True)),
                    item_export_scope=str(kwargs.get("item_export_scope", "linked")),
                )
            ),
            payload_builder=lambda context, outcome: _deploy_workflow_payload(
                command=command,
                runtime=runtime,
                plan=context.plan,
                outcome=outcome,
            ),
            failure_messages=_DEPLOY_FAILURE_MESSAGES,
        )
    )


def run_daemon_start_command() -> None:
    settings = cli._build_settings()
    console = cli._runtime_symbols()["Console"](
        stderr=bool(getattr(settings, "log_json", False))
    )
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
