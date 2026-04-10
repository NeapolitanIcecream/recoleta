from __future__ import annotations

from datetime import date
from typing import Any

import recoleta.cli as cli
from recoleta.cli.command_support import (
    RuntimeLoadRequest,
    emit_command_error,
    load_runtime,
)
from recoleta.cli.site_support import site_output_dir_from_settings
from recoleta.trend_email import (
    TrendEmailSendRequest,
    build_trend_email_preview,
    send_trend_email,
)


def _parse_anchor_or_exit(
    *,
    anchor_date: str | None,
    command_name: str,
    console: Any,
    json_output: bool,
) -> date | None:
    if anchor_date is None or not str(anchor_date).strip():
        return None
    try:
        return cli._parse_anchor_date_option(str(anchor_date).strip())
    except Exception as exc:  # noqa: BLE001
        emit_command_error(
            command_name=command_name,
            message=f"invalid --date: {exc}",
            console=console,
            json_output=json_output,
            exit_code=2,
        )


def _preview_payload(
    *,
    command_name: str,
    result: Any,
    instance_name: str | None = None,
) -> dict[str, Any]:
    return {
        "status": result.status,
        "command": command_name,
        "instance": instance_name or result.instance,
        "preview_root_dir": str(result.preview_root_dir),
        "batch_manifest_path": str(result.batch_manifest_path),
        "results": [
            {
                "granularity": entry.granularity,
                "preview_dir": str(entry.preview_dir),
                "manifest_path": str(entry.manifest_path),
                "html_path": str(entry.html_path),
                "text_path": str(entry.text_path),
                "primary_page_url": entry.primary_page_url,
                "content_hash": entry.content_hash,
                "subject": entry.subject,
                "trend_doc_id": entry.trend_doc_id,
                "period_token": entry.period_token,
            }
            for entry in result.results
        ],
    }


def _path_payload(path: object) -> str | None:
    if path is None:
        return None
    return str(path)


def _send_payload(
    *,
    command_name: str,
    result: Any,
    instance_name: str | None = None,
) -> dict[str, Any]:
    return {
        "status": result.status,
        "command": command_name,
        "instance": instance_name or result.instance,
        "send_root_dir": str(result.send_root_dir),
        "batch_manifest_path": str(result.batch_manifest_path),
        "results": [
            {
                "status": entry.status,
                "granularity": entry.granularity,
                "send_dir": _path_payload(entry.send_dir),
                "manifest_path": _path_payload(entry.manifest_path),
                "html_path": _path_payload(entry.html_path),
                "text_path": _path_payload(entry.text_path),
                "primary_page_url": entry.primary_page_url,
                "content_hash": entry.content_hash,
                "subject": entry.subject,
                "trend_doc_id": entry.trend_doc_id,
                "period_token": entry.period_token,
                **({"error": entry.error} if entry.error is not None else {}),
            }
            for entry in result.results
        ],
    }


def run_email_preview_command(**kwargs: Any) -> dict[str, Any]:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "run email preview"))
    runtime = load_runtime(
        request=RuntimeLoadRequest(
            db_path=kwargs.get("db_path"),
            config_path=kwargs.get("config_path"),
            command_name=command_name,
            require_settings=True,
            init_schema=False,
        )
    )
    assert runtime.settings is not None
    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=kwargs.get("anchor_date"),
        command_name=command_name,
        console=runtime.console,
        json_output=json_output,
    )
    try:
        result = build_trend_email_preview(
            settings=runtime.settings,
            site_output_dir=site_output_dir_from_settings(runtime.settings),
            anchor_date=parsed_anchor,
            output_dir=kwargs.get("output_dir"),
            granularities=kwargs.get("granularities"),
        )
    except Exception as exc:  # noqa: BLE001
        emit_command_error(
            command_name=command_name,
            message=str(exc),
            console=runtime.console,
            json_output=json_output,
            exit_code=1,
        )
    payload = _preview_payload(command_name=command_name, result=result)
    if json_output:
        cli._emit_json(payload)
        return payload
    runtime.console.print(
        f"[green]{command_name} completed[/green] "
        f"bundles={len(result.results)} output={result.preview_root_dir}"
    )
    return payload


def run_email_send_command(**kwargs: Any) -> dict[str, Any]:
    json_output = bool(kwargs.get("json_output", False))
    command_name = str(kwargs.get("command_name", "run email send"))
    runtime = load_runtime(
        request=RuntimeLoadRequest(
            db_path=kwargs.get("db_path"),
            config_path=kwargs.get("config_path"),
            command_name=command_name,
            require_settings=True,
            init_schema=True,
        )
    )
    assert runtime.settings is not None
    parsed_anchor = _parse_anchor_or_exit(
        anchor_date=kwargs.get("anchor_date"),
        command_name=command_name,
        console=runtime.console,
        json_output=json_output,
    )
    try:
        result = send_trend_email(
            settings=runtime.settings,
            repository=runtime.repository,
            request=TrendEmailSendRequest(
                site_output_dir=site_output_dir_from_settings(runtime.settings),
                anchor_date=parsed_anchor,
                force_batch=bool(kwargs.get("force_batch", False)),
                granularities=kwargs.get("granularities"),
            ),
        )
    except Exception as exc:  # noqa: BLE001
        emit_command_error(
            command_name=command_name,
            message=str(exc),
            console=runtime.console,
            json_output=json_output,
            exit_code=1,
        )
    payload = _send_payload(command_name=command_name, result=result)
    if json_output:
        cli._emit_json(payload)
        if result.status in {"preflight_failed", "send_failed"}:
            raise cli.typer.Exit(code=1)
        return payload
    all_skipped = bool(result.results) and all(
        entry.status == "skipped" for entry in result.results
    )
    color = (
        "red"
        if result.status in {"preflight_failed", "send_failed"}
        else ("yellow" if all_skipped else "green")
    )
    runtime.console.print(
        f"[{color}]{command_name} {result.status}[/{color}] "
        f"bundles={len(result.results)} output={result.send_root_dir}"
    )
    if result.status in {"preflight_failed", "send_failed"}:
        raise cli.typer.Exit(code=1)
    return payload
