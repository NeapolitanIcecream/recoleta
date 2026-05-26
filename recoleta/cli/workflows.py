from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, NoReturn

import recoleta.cli as cli
from recoleta.cli.arxiv_pool_readiness import (
    arxiv_pool_workflow_readiness_should_block,
    build_arxiv_pool_workflow_readiness_plan,
    evaluate_arxiv_pool_workflow_readiness,
)
from recoleta.cli import workflow_models as _workflow_models
from recoleta.cli.workflow_models import WorkflowExecutionContext
from recoleta.cli.workflow_planner import (
    decision_payloads,
    plan_workflow_execution,
    planned_expensive_steps,
)
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
from recoleta.models import RUN_TERMINAL_STATE_FAILED

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
    planner_decisions: list[Any] | None
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
    generation_force: bool = False


@dataclass(frozen=True, slots=True)
class _GranularityDryRunRequest:
    workflow_name: str
    command: str
    anchor_date: Any
    include_steps: list[str]
    skip_steps: list[str]
    generation_force: bool
    json_output: bool
    emit_output: bool
    config_path: Any


@dataclass(frozen=True, slots=True)
class _GranularityWorkflowContext:
    plan: Any
    execution_context: WorkflowExecutionContext
    on_translate_failure: str
    planner_decisions: list[Any]
    arxiv_pool_readiness: dict[str, Any] | None = None
    blocked_payload: dict[str, Any] | None = None


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


def _build_dry_run_runtime(
    *,
    config_path: Any,
) -> tuple[Any, Any, Any, Any]:
    settings, repository, service = cli._build_runtime(config_path=config_path)
    console = cli._runtime_symbols()["Console"](
        stderr=bool(getattr(settings, "log_json", False))
    )
    return settings, repository, service, console


def _workflow_loop_request(
    request: _ManagedWorkflowLoopRequest,
) -> WorkflowLoopRequest:
    return WorkflowLoopRequest(
        repository=request.runtime.repository,
        heartbeat_monitor=request.runtime.heartbeat_monitor,
        plan=request.plan,
        execution_context=request.execution_context,
        planner_decisions=request.planner_decisions,
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
        generation_force=bool(request.generation_force),
        site_deploy_force=False,
    )
    planner_decisions = plan_workflow_execution(
        plan=plan,
        repository=request.runtime.repository,
        settings=request.runtime.settings,
        generation_force=bool(request.generation_force),
        translate_include=list(policy.translate_include),
        translate_granularities=translate_granularities,
    )
    arxiv_pool_readiness = _evaluate_granularity_arxiv_pool_readiness(
        settings=request.runtime.settings,
        plan=plan,
    )
    blocked_payload = _granularity_arxiv_pool_blocked_payload(
        command=request.command,
        run_id=request.runtime.run_id,
        plan=plan,
        readiness=arxiv_pool_readiness,
    )
    return _GranularityWorkflowContext(
        plan=plan,
        execution_context=execution_context,
        on_translate_failure=str(policy.on_translate_failure or "fail"),
        planner_decisions=planner_decisions,
        arxiv_pool_readiness=arxiv_pool_readiness,
        blocked_payload=blocked_payload,
    )


def _granularity_dry_run_payload(
    *,
    command: str,
    plan: Any,
    planner_decisions: list[Any],
    arxiv_pool_readiness: dict[str, Any] | None,
) -> dict[str, Any]:
    return {
        "status": "ok",
        "mode": "dry_run",
        "command": command,
        "operation_kind": plan.operation_kind,
        "target_granularity": plan.target_granularity,
        "target_period_start": cli._isoformat_or_none(plan.target_period_start),
        "target_period_end": cli._isoformat_or_none(plan.target_period_end),
        "requested_steps": plan.requested_steps,
        "skipped_steps": plan.skipped_steps,
        "planned_expensive_steps": planned_expensive_steps(planner_decisions),
        "plan": decision_payloads(planner_decisions),
        "arxiv_pool_readiness": _public_arxiv_pool_readiness(arxiv_pool_readiness),
    }


def _execute_granularity_dry_run(
    request: _GranularityDryRunRequest,
) -> dict[str, Any]:
    settings, repository, _service, console = _build_dry_run_runtime(
        config_path=request.config_path
    )
    plan = _build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name=request.workflow_name,
            command=request.command,
            anchor_date=request.anchor_date,
            settings=settings,
            include_steps=request.include_steps,
            skip_steps=request.skip_steps,
        )
    )
    policy = settings.workflow_policy_for_granularity(plan.target_granularity or "day")
    translate_granularities = _granularity_stack(
        target_granularity=plan.target_granularity or "day",
        recursive_lower_levels=bool(policy.recursive_lower_levels),
    )
    planner_decisions = plan_workflow_execution(
        plan=plan,
        repository=repository,
        settings=settings,
        generation_force=request.generation_force,
        translate_include=list(policy.translate_include),
        translate_granularities=translate_granularities,
    )
    arxiv_pool_readiness = _evaluate_granularity_arxiv_pool_readiness(
        settings=settings,
        plan=plan,
    )
    payload = _granularity_dry_run_payload(
        command=request.command,
        plan=plan,
        planner_decisions=planner_decisions,
        arxiv_pool_readiness=arxiv_pool_readiness,
    )
    if request.json_output:
        if request.emit_output:
            cli._emit_json(payload)
        return payload
    if request.emit_output:
        console.print(
            f"[cyan]{request.command} dry-run[/cyan] "
            f"planned_expensive_steps={payload['planned_expensive_steps']} "
            f"steps={len(planner_decisions)}"
        )
    return payload


def _granularity_workflow_payload(
    *,
    command: str,
    runtime: _ManagedWorkflowRuntime,
    plan: Any,
    outcome: _WorkflowLoopOutcome,
    planner_decisions: list[Any],
    arxiv_pool_readiness: dict[str, Any] | None,
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
            planner_decisions=planner_decisions,
            arxiv_pool_readiness=_public_arxiv_pool_readiness(
                arxiv_pool_readiness
            ),
        )
    )


def _public_arxiv_pool_readiness(
    readiness: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if readiness is None:
        return None
    return {
        key: value
        for key, value in readiness.items()
        if key != "_workflow_readiness_plan"
    }


def _evaluate_granularity_arxiv_pool_readiness(
    *,
    settings: Any,
    plan: Any,
) -> dict[str, Any] | None:
    readiness_plan = build_arxiv_pool_workflow_readiness_plan(
        settings_list=[settings],
        target_period_start=plan.target_period_start,
        target_period_end=plan.target_period_end,
        requested_steps=list(plan.requested_steps),
    )
    if readiness_plan.status != "planned":
        return None
    readiness = evaluate_arxiv_pool_workflow_readiness(readiness_plan)
    return {
        **readiness,
        "_workflow_readiness_plan": readiness_plan,
    }


def _granularity_arxiv_pool_blocked_payload(
    *,
    command: str,
    run_id: str,
    plan: Any,
    readiness: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if readiness is None:
        return None
    readiness_plan = readiness.get("_workflow_readiness_plan")
    if readiness_plan is None:
        return None
    if not arxiv_pool_workflow_readiness_should_block(readiness_plan, readiness):
        return None
    payload_readiness = _public_arxiv_pool_readiness(readiness) or {}
    return {
        "status": "blocked",
        "command": command,
        "run_id": run_id,
        "operation_kind": plan.operation_kind,
        "target_granularity": plan.target_granularity,
        "target_period_start": cli._isoformat_or_none(plan.target_period_start),
        "target_period_end": cli._isoformat_or_none(plan.target_period_end),
        "requested_steps": plan.requested_steps,
        "skipped_steps": plan.skipped_steps,
        "arxiv_pool_readiness": payload_readiness,
    }


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
            generation_force=False,
            site_deploy_force=request.force,
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


def _managed_workflow_blocked_payload(context: Any) -> dict[str, Any] | None:
    blocked_payload = getattr(context, "blocked_payload", None)
    return blocked_payload if isinstance(blocked_payload, dict) else None


def _raise_blocked_managed_workflow(
    *,
    request: _ManagedWorkflowRunRequest,
    blocked_payload: dict[str, Any],
) -> NoReturn:
    cli._finish_run(
        request.runtime.repository,
        run_id=request.runtime.run_id,
        success=False,
        terminal_state=RUN_TERMINAL_STATE_FAILED,
    )
    _emit_blocked_managed_workflow(
        request=request,
        blocked_payload=blocked_payload,
    )
    raise cli.typer.Exit(code=1)


def _emit_blocked_managed_workflow(
    *,
    request: _ManagedWorkflowRunRequest,
    blocked_payload: dict[str, Any],
) -> None:
    if bool(request.kwargs.get("json_output", False)):
        if bool(request.kwargs.get("emit_output", True)):
            cli._emit_json(blocked_payload)
        return
    if not bool(request.kwargs.get("emit_output", True)):
        return
    readiness = blocked_payload.get("arxiv_pool_readiness") or {}
    request.runtime.console.print(
        f"[yellow]{request.command} blocked[/yellow] "
        f"arxiv_pool_windows={readiness.get('blocked_windows_total')}"
    )


def _execute_and_emit_managed_workflow(
    *,
    request: _ManagedWorkflowRunRequest,
    context: Any,
) -> dict[str, Any]:
    outcome = _execute_managed_workflow_loop(
        request=_ManagedWorkflowLoopRequest(
            runtime=request.runtime,
            plan=context.plan,
            execution_context=context.execution_context,
            planner_decisions=getattr(context, "planner_decisions", None),
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


def _handle_preloop_start_failure(
    *,
    request: _ManagedWorkflowRunRequest,
    loop_started: bool,
    exc: BaseException,
) -> None:
    if loop_started:
        return
    if isinstance(exc, KeyboardInterrupt):
        _handle_preloop_interrupt(
            runtime=request.runtime,
            exc=exc,
            finish_message=request.failure_messages.interrupt_finish,
            interrupt_message=request.failure_messages.interrupted,
        )
        return
    if isinstance(exc, request.runtime.workspace_lease_lost_error):
        _handle_preloop_lease_loss(
            runtime=request.runtime,
            exc=exc,
            finish_message=request.failure_messages.lease_finish,
            warning_message=request.failure_messages.lease_stopped,
        )
        return
    if isinstance(exc, Exception):
        _handle_preloop_exception(
            runtime=request.runtime,
            finish_message=request.failure_messages.exception_finish,
            exception_message=request.failure_messages.exception_log,
        )


def _run_managed_workflow(
    request: _ManagedWorkflowRunRequest,
) -> dict[str, Any]:
    loop_started = False
    try:
        context = request.prepare_context()
        blocked_payload = _managed_workflow_blocked_payload(context)
        if blocked_payload is not None:
            loop_started = True
            _raise_blocked_managed_workflow(
                request=request,
                blocked_payload=blocked_payload,
            )
        loop_started = True
        return _execute_and_emit_managed_workflow(
            request=request,
            context=context,
        )
    except (KeyboardInterrupt, Exception) as exc:
        _handle_preloop_start_failure(
            request=request,
            loop_started=loop_started,
            exc=exc,
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
    if bool(kwargs.get("dry_run", False)):
        return _execute_granularity_dry_run(
            _GranularityDryRunRequest(
                workflow_name=workflow_name,
                command=command,
                anchor_date=kwargs.get("anchor_date"),
                include_steps=include_steps,
                skip_steps=skip_steps,
                generation_force=bool(kwargs.get("force", False)),
                json_output=bool(kwargs.get("json_output", False)),
                emit_output=bool(kwargs.get("emit_output", True)),
                config_path=kwargs.get("config_path"),
            )
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
                    generation_force=bool(kwargs.get("force", False)),
                )
            ),
            payload_builder=lambda context, outcome: _granularity_workflow_payload(
                command=command,
                runtime=runtime,
                plan=context.plan,
                outcome=outcome,
                planner_decisions=context.planner_decisions,
                arxiv_pool_readiness=context.arxiv_pool_readiness,
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
