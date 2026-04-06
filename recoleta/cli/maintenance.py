from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any, NoReturn, cast

import recoleta.cli as cli
from recoleta.cli.doctor_support import (
    GcPayloadRequest,
    StatsPayloadRequest,
    build_doctor_payload,
    build_gc_payload,
    build_llm_diagnostics_payload as _build_llm_diagnostics_payload,
    build_stats_payload,
    default_min_relevance_score as _default_min_relevance_score,
    load_gc_settings,
    log_gc_completion,
    period_bounds_for_granularity as _period_bounds_for_granularity,
    record_doctor_llm_metrics as _record_doctor_llm_metrics,
    render_doctor_output,
    render_gc_summary,
    render_stats_output,
    render_why_empty_output,
    run_llm_ping as _run_llm_ping,
    validate_latest_success_age,
)


@dataclass(frozen=True, slots=True)
class CommandFailureContext:
    console: Any
    log: Any
    failure_name: str
    message: str
    json_output: bool
    code: int = 1


@dataclass(frozen=True, slots=True)
class DoctorLlmFailureContext:
    console: Any
    log: Any
    command_name: str
    message: str
    json_output: bool
    repository: Any | None = None
    run_id: str | None = None
    billing: dict[str, Any] | None = None
    diagnostics: dict[str, Any] | None = None


@dataclass(frozen=True, slots=True)
class DoctorLlmRenderContext:
    console: Any
    command_name: str
    payload: dict[str, Any]
    ping: bool
    repository: Any | None
    run_id: str | None


@dataclass(frozen=True, slots=True)
class DoctorLlmProbeContext:
    request: DoctorLlmRequest
    settings: Any
    repository: Any | None
    run_id: str | None
    console: Any
    log: Any


@dataclass(frozen=True, slots=True)
class DoctorLlmRequest:
    ping: bool
    timeout_seconds: float
    json_output: bool
    db_path: Path | None
    config_path: Path | None
    command_name: str


def _emit_command_failure(*, context: CommandFailureContext) -> NoReturn:
    context.log.warning("{} failed error={}", context.failure_name, context.message)
    if context.json_output:
        cli._emit_json({"status": "error", "error": context.message})
    else:
        context.console.print(
            f"[red]{context.failure_name} failed[/red] {context.message}"
        )
    raise cli.typer.Exit(code=context.code)


def _load_optional_settings(
    *,
    db_path: Path | None,
    config_path: Path | None,
    resolved_db_path: Path,
    log: Any,
    warning_template: str,
) -> tuple[Any | None, str]:
    if not cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        return None, "skipped"
    try:
        return (
            cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            ),
            "ok",
        )
    except Exception as exc:  # noqa: BLE001
        log.warning(
            warning_template,
            resolved_db_path,
            type(exc).__name__,
            str(exc),
        )
        return None, "failed"


def run_gc_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    prune_caches: bool,
    dry_run: bool,
) -> None:
    console = cli._runtime_symbols()["Console"]()
    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc
    if not resolved.exists():
        console.print(
            "[green]gc completed[/green] "
            f"deleted_artifacts=0 deleted_runs=0 path={resolved}"
        )
        return

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="gc",
        log_module="cli.gc",
    )
    try:
        settings, filesystem_cache_pruning = load_gc_settings(
            db_path=db_path,
            config_path=config_path,
            resolved_db_path=resolved,
            prune_caches=prune_caches,
            log=log,
        )
        payload = build_gc_payload(
            request=GcPayloadRequest(
                repository=repository,
                settings=settings,
                prune_caches=prune_caches,
                dry_run=dry_run,
                reference_now=datetime.now(UTC),
                filesystem_cache_pruning=filesystem_cache_pruning,
            )
        )
        heartbeat_monitor.raise_if_failed()
        log_gc_completion(log=log, payload=payload, dry_run=dry_run)
        render_gc_summary(
            console=console,
            payload=payload,
            resolved_db_path=resolved,
            dry_run=dry_run,
            prune_caches=prune_caches,
        )
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_doctor_why_empty_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    anchor_date: str,
    granularity: str,
    min_relevance_score: float | None,
    json_output: bool,
    command_name: str = "doctor why-empty",
) -> None:
    symbols = cli._runtime_symbols()
    console = symbols["Console"]()
    log = symbols["logger"].bind(module="cli.doctor.why_empty", json=json_output)
    try:
        period_start, period_end = _period_bounds_for_granularity(
            anchor_date=anchor_date,
            granularity=granularity,
        )
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path,
            config_path=config_path,
        )
    except Exception as exc:  # noqa: BLE001
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=str(exc),
                json_output=json_output,
            )
        )
    if not resolved_db_path.exists():
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=f"db does not exist: {resolved_db_path}",
                json_output=json_output,
            )
        )

    settings: Any | None = None
    if cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
        except Exception as exc:  # noqa: BLE001
            log.warning(
                "{} settings load skipped error_type={} error={}",
                command_name,
                type(exc).__name__,
                str(exc),
            )

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        repository.ensure_schema_current()
    except Exception as exc:
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=str(exc),
                json_output=json_output,
            )
        )

    effective_min_relevance = (
        float(min_relevance_score)
        if min_relevance_score is not None
        else _default_min_relevance_score(settings=settings)
    )
    payload = repository.diagnose_corpus_window(
        period_start=period_start,
        period_end=period_end,
        min_relevance_score=effective_min_relevance,
    )
    payload["status"] = "ok"
    payload["granularity"] = str(granularity or "").strip().lower()

    if json_output:
        cli.typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    render_why_empty_output(console=console, payload=payload, command_name=command_name)


def run_vacuum_command(*, db_path: Path | None, config_path: Path | None) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise cli.typer.Exit(code=2)

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="vacuum",
        log_module="cli.vacuum",
    )
    try:
        repository.vacuum()
        heartbeat_monitor.raise_if_failed()
        log.info("VACUUM completed path={}", str(resolved))
        console.print(f"[green]vacuum completed[/green] path={resolved}")
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_backup_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    output_dir: Path | None,
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[red]db does not exist[/red] path={resolved}")
        raise cli.typer.Exit(code=2)

    repository = cli._build_repository_for_db_path(db_path=resolved)
    repository.init_schema()
    owner_token, log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command="backup",
        log_module="cli.backup",
    )
    try:
        bundle_root = (
            output_dir.expanduser().resolve()
            if output_dir is not None
            else (resolved.parent / "backups").resolve()
        )
        result = repository.backup_database(output_dir=bundle_root)
        heartbeat_monitor.raise_if_failed()
        log.info(
            "Backup completed bundle_dir={} manifest_path={} schema_version={}",
            str(result.bundle_dir),
            str(result.manifest_path),
            result.schema_version,
        )
        console.print(
            "[green]backup completed[/green] "
            f"bundle={result.bundle_dir} schema_version={result.schema_version}"
        )
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_restore_command(
    *,
    bundle: Path,
    db_path: Path | None,
    config_path: Path | None,
    yes: bool,
) -> None:
    if not yes:
        cli.typer.echo("refusing to restore db without --yes")
        raise cli.typer.Exit(code=2)

    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()
    log = logger.bind(module="cli.restore")

    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    lease_repository: Any | None = None
    lease_owner_token: str | None = None
    lease_heartbeat_monitor: Any | None = None
    try:
        if resolved.exists():
            lease_repository = cli._build_repository_for_db_path(db_path=resolved)
            assert lease_repository is not None
            lease_repository.init_schema()
            lease_owner_token, _, lease_heartbeat_monitor = (
                cli._acquire_workspace_lease_for_command(
                    repository=lease_repository,
                    console=console,
                    command="restore",
                    log_module="cli.restore",
                )
            )
        result = cli._build_repository_for_db_path(db_path=resolved).restore_database(
            bundle_dir=bundle,
            db_path=resolved,
        )
        if lease_heartbeat_monitor is not None:
            lease_heartbeat_monitor.raise_if_failed()
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Restore failed bundle={} path={} error_type={} error={}",
            str(bundle),
            str(resolved),
            type(exc).__name__,
            str(exc),
        )
        console.print(f"[red]restore failed[/red] {exc}")
        raise cli.typer.Exit(code=1) from exc
    finally:
        if (
            lease_repository is not None
            and lease_owner_token is not None
            and lease_heartbeat_monitor is not None
        ):
            cli._cleanup_workspace_lease(
                repository=lease_repository,
                owner_token=lease_owner_token,
                heartbeat_monitor=lease_heartbeat_monitor,
                log=log,
            )

    log.info(
        "Restore completed bundle_dir={} path={} schema_version={}",
        str(result.bundle_dir),
        str(result.database_path),
        result.schema_version,
    )
    console.print(
        "[green]restore completed[/green] "
        f"bundle={result.bundle_dir} path={result.database_path} schema_version={result.schema_version}"
    )


def run_stats_command(
    *,
    json_output: bool,
    db_path: Path | None,
    config_path: Path | None,
    command_name: str = "stats",
) -> None:
    symbols = cli._runtime_symbols()
    console = symbols["Console"]()
    log = symbols["logger"].bind(module="cli.stats", json=json_output)
    try:
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path, config_path=config_path
        )
    except Exception as exc:  # noqa: BLE001
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=f"db path resolution failed: {exc}",
                json_output=json_output,
            )
        )
    if not resolved_db_path.exists():
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=f"db does not exist: {resolved_db_path}",
                json_output=json_output,
            )
        )
    settings, settings_status = _load_optional_settings(
        db_path=db_path,
        config_path=config_path,
        resolved_db_path=resolved_db_path,
        log=log,
        warning_template="Stats settings load failed db_path={} error_type={} error={}",
    )
    workspace_bytes = (
        cli._workspace_bytes_from_settings(settings) if settings is not None else {}
    )
    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        payload = build_stats_payload(
            request=StatsPayloadRequest(
                repository=repository,
                resolved_db_path=resolved_db_path,
                settings=settings,
                settings_status=settings_status,
                workspace_bytes=workspace_bytes,
                reference_now=datetime.now(UTC),
            )
        )
    except Exception as exc:
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=command_name,
                message=str(exc),
                json_output=json_output,
            )
        )
    if json_output:
        cli.typer.echo(json.dumps(payload, ensure_ascii=False, sort_keys=True))
        return
    render_stats_output(console=console, payload=payload, command_name=command_name)


def run_doctor_command(
    *,
    healthcheck: bool,
    db_path: Path | None,
    config_path: Path | None,
    max_success_age_minutes: int | None,
    command_name: str = "doctor",
) -> None:
    symbols = cli._runtime_symbols()
    console = symbols["Console"]()
    log = symbols["logger"].bind(module="cli.doctor", healthcheck=healthcheck)
    failure_name = "healthcheck" if healthcheck else command_name
    try:
        resolved_db_path = cli._resolve_db_path(
            db_path=db_path, config_path=config_path
        )
    except Exception as exc:  # noqa: BLE001
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=failure_name,
                message=f"db path resolution failed: {exc}",
                json_output=False,
            )
        )
    settings: Any | None = None
    settings_status = "skipped"
    if cli._should_attempt_settings_load(
        db_path_option=db_path,
        config_path_option=config_path,
    ):
        try:
            settings = cli._build_settings(
                config_path=config_path,
                db_path=resolved_db_path,
            )
            settings_status = "ok"
        except Exception as exc:  # noqa: BLE001
            _emit_command_failure(
                context=CommandFailureContext(
                    console=console,
                    log=log,
                    failure_name=failure_name,
                    message=f"settings load failed: {exc}",
                    json_output=False,
                )
            )
    if not resolved_db_path.exists():
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=failure_name,
                message=f"db does not exist: {resolved_db_path}",
                json_output=False,
            )
        )
    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    try:
        payload = build_doctor_payload(
            repository=repository,
            resolved_db_path=resolved_db_path,
            settings=settings,
            settings_status=settings_status,
            reference_now=datetime.now(UTC),
        )
    except Exception as exc:
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=failure_name,
                message=str(exc),
                json_output=False,
            )
        )
    try:
        validate_latest_success_age(
            payload=payload,
            max_success_age_minutes=max_success_age_minutes,
            reference_now=datetime.now(UTC),
        )
    except ValueError as exc:
        _emit_command_failure(
            context=CommandFailureContext(
                console=console,
                log=log,
                failure_name=failure_name,
                message=str(exc),
                json_output=False,
            )
        )
    render_doctor_output(
        console=console,
        payload=payload,
        command_name=command_name,
        healthcheck=healthcheck,
    )


def _doctor_llm_billing(
    *, repository: Any, run_id: str, log: Any
) -> dict[str, Any] | None:
    try:
        return cli._billing_summary_payload(repository.list_metrics(run_id=run_id))
    except Exception as exc:  # noqa: BLE001
        log.warning(
            "Doctor llm billing metrics load failed error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        return None


def _emit_doctor_llm_failure(*, context: DoctorLlmFailureContext) -> NoReturn:
    context.log.warning(context.message)
    if context.json_output:
        payload: dict[str, Any] = {"status": "error", "error": context.message}
        if context.run_id is not None:
            payload["run_id"] = context.run_id
        if context.billing is not None or context.run_id is not None:
            payload["billing"] = context.billing
        if context.diagnostics is not None:
            payload["diagnostics"] = context.diagnostics
        cli._emit_json(payload)
    else:
        context.console.print(
            f"[red]{context.command_name} failed[/red] {context.message}"
        )
        if context.repository is not None and context.run_id is not None:
            cli._print_billing_report(
                console=context.console,
                repository=context.repository,
                run_id=context.run_id,
            )
    raise cli.typer.Exit(code=1)


def _render_doctor_llm_output(*, context: DoctorLlmRenderContext) -> None:
    context.console.print(
        f"[green]{context.command_name} ok[/green] "
        f"ready={str(context.payload['ready']).lower()} "
        f"provider={context.payload['provider']} model={context.payload['model']}"
    )
    context.console.print(_doctor_llm_api_key_line(context.payload))
    context.console.print(_doctor_llm_base_url_line(context.payload))
    _render_doctor_llm_metadata(context=context)
    if context.ping:
        context.console.print("ping=" + _doctor_llm_ping_line(context.payload))
    if context.repository is not None and context.run_id is not None:
        cli._print_billing_report(
            console=context.console,
            repository=context.repository,
            run_id=context.run_id,
        )


def _doctor_llm_api_key_line(payload: dict[str, Any]) -> str:
    return (
        "api_key="
        + (
            f"configured fingerprint={payload['connection']['api_key']['fingerprint']}"
            if payload["connection"]["api_key"]["configured"]
            else "missing"
        )
        + (
            " env_present=true"
            if payload["connection"]["api_key"]["env_present"]
            else " env_present=false"
        )
    )


def _doctor_llm_base_url_line(payload: dict[str, Any]) -> str:
    return (
        "base_url="
        + (
            str(payload["connection"]["base_url"]["value"])
            if payload["connection"]["base_url"]["configured"]
            else "default"
        )
        + (
            " env_present=true"
            if payload["connection"]["base_url"]["env_present"]
            else " env_present=false"
        )
    )


def _render_doctor_llm_metadata(*, context: DoctorLlmRenderContext) -> None:
    if context.payload["output_language"] is not None:
        context.console.print(f"output_language={context.payload['output_language']}")
    if context.payload["config_path"] is not None:
        context.console.print(f"config_path={context.payload['config_path']}")
    if context.payload["issues"]:
        context.console.print("issues=" + " ".join(context.payload["issues"]))


def _doctor_llm_ping_line(payload: dict[str, Any]) -> str:
    return " ".join(
        part
        for part in (
            payload["ping"]["status"],
            _doctor_llm_ping_part(
                name="elapsed_ms",
                value=payload["ping"].get("elapsed_ms"),
            ),
            _doctor_llm_ping_part(
                name="resolved_model",
                value=payload["ping"].get("resolved_model"),
            ),
            _doctor_llm_ping_part(
                name="prompt_tokens",
                value=payload["ping"].get("prompt_tokens"),
            ),
            _doctor_llm_ping_part(
                name="completion_tokens",
                value=payload["ping"].get("completion_tokens"),
            ),
        )
        if part
    )


def _doctor_llm_ping_part(*, name: str, value: Any) -> str:
    if value is None or value == "":
        return ""
    return f"{name}={value}"


def _load_doctor_llm_settings(
    *,
    request: DoctorLlmRequest,
    console: Any,
    log: Any,
) -> Any:
    try:
        return cli._build_settings(
            config_path=request.config_path,
            db_path=request.db_path,
        )
    except Exception as exc:  # noqa: BLE001
        _emit_doctor_llm_failure(
            context=DoctorLlmFailureContext(
                console=console,
                log=log,
                command_name=request.command_name,
                message=f"settings load failed: {exc}",
                json_output=request.json_output,
            )
        )


def _setup_doctor_llm_run(
    *,
    request: DoctorLlmRequest,
    settings: Any,
    console: Any,
    log: Any,
) -> tuple[Any | None, str | None, Any]:
    if not request.ping:
        return None, None, log
    raw_db_path = getattr(settings, "recoleta_db_path", None)
    if raw_db_path is None:
        _emit_doctor_llm_failure(
            context=DoctorLlmFailureContext(
                console=console,
                log=log,
                command_name=request.command_name,
                message="settings do not expose recoleta_db_path",
                json_output=request.json_output,
            )
        )
    try:
        repository = cast(
            Any, cli._build_repository_for_db_path(db_path=Path(raw_db_path))
        )
        repository.init_schema()
        run_id, observed_log = cli._begin_observed_run_for_settings(
            settings=settings,
            repository=repository,
            command=request.command_name,
            log_module="cli.doctor.llm",
        )
        return repository, run_id, observed_log
    except Exception as exc:  # noqa: BLE001
        _emit_doctor_llm_failure(
            context=DoctorLlmFailureContext(
                console=console,
                log=log,
                command_name=request.command_name,
                message=f"{request.command_name} run setup failed: {exc}",
                json_output=request.json_output,
            )
        )


def _run_doctor_llm_probe(
    *,
    context: DoctorLlmProbeContext,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    billing: dict[str, Any] | None = None
    try:
        ping_payload = (
            _run_llm_ping(
                settings=context.settings,
                timeout_seconds=context.request.timeout_seconds,
            )
            if context.request.ping
            else {"status": "skipped"}
        )
        if context.repository is not None and context.run_id is not None:
            _record_doctor_llm_metrics(
                repository=context.repository,
                run_id=context.run_id,
                ping_payload=ping_payload,
            )
            context.repository.finish_run(
                context.run_id,
                success=str(ping_payload.get("status", "") or "") == "ok",
            )
            billing = _doctor_llm_billing(
                repository=context.repository,
                run_id=context.run_id,
                log=context.log,
            )
        return ping_payload, billing
    except Exception as exc:  # noqa: BLE001
        if context.repository is not None and context.run_id is not None:
            try:
                context.repository.finish_run(context.run_id, success=False)
            except Exception:
                context.log.exception(
                    "Doctor llm run finish failed during error handling"
                )
        _emit_doctor_llm_failure(
            context=DoctorLlmFailureContext(
                console=context.console,
                log=context.log,
                command_name=context.request.command_name,
                message=f"llm ping failed: {exc}",
                json_output=context.request.json_output,
                repository=context.repository,
                run_id=context.run_id,
                billing=billing,
            )
        )


def _doctor_llm_success_payload(
    *,
    request: DoctorLlmRequest,
    payload: dict[str, Any],
    run_id: str | None,
    billing: dict[str, Any] | None,
) -> dict[str, Any]:
    output_payload: dict[str, Any] = {"status": "ok", **payload}
    if request.ping:
        output_payload["run_id"] = run_id
        output_payload["billing"] = billing
    return output_payload


def run_doctor_llm_command(**kwargs: Any) -> None:
    request = DoctorLlmRequest(
        ping=bool(kwargs.get("ping", False)),
        timeout_seconds=float(kwargs.get("timeout_seconds", 30.0)),
        json_output=bool(kwargs.get("json_output", False)),
        db_path=kwargs.get("db_path"),
        config_path=kwargs.get("config_path"),
        command_name=str(kwargs.get("command_name", "doctor llm")),
    )
    symbols = cli._runtime_symbols()
    console = symbols["Console"]()
    log = symbols["logger"].bind(
        module="cli.doctor.llm",
        ping=request.ping,
        json=request.json_output,
    )
    settings = _load_doctor_llm_settings(request=request, console=console, log=log)
    repository, run_id, log = _setup_doctor_llm_run(
        request=request,
        settings=settings,
        console=console,
        log=log,
    )
    ping_payload, billing = _run_doctor_llm_probe(
        context=DoctorLlmProbeContext(
            request=request,
            settings=settings,
            repository=repository,
            run_id=run_id,
            console=console,
            log=log,
        )
    )
    payload = _build_llm_diagnostics_payload(
        settings=settings, ping_payload=ping_payload
    )
    if request.ping and str(ping_payload.get("status", "") or "") != "ok":
        log.warning(
            "LLM ping failed model={} provider={} error_type={} error={}",
            payload["model"],
            payload["provider"],
            ping_payload.get("error_type"),
            ping_payload.get("error_message"),
        )
        _emit_doctor_llm_failure(
            context=DoctorLlmFailureContext(
                console=console,
                log=log,
                command_name=request.command_name,
                message="llm ping failed",
                json_output=request.json_output,
                repository=repository,
                run_id=run_id,
                billing=billing,
                diagnostics=payload,
            )
        )

    if request.json_output:
        cli._emit_json(
            _doctor_llm_success_payload(
                request=request,
                payload=payload,
                run_id=run_id,
                billing=billing,
            )
        )
        return
    _render_doctor_llm_output(
        context=DoctorLlmRenderContext(
            console=console,
            command_name=request.command_name,
            payload=payload,
            ping=request.ping,
            repository=repository,
            run_id=run_id,
        )
    )
