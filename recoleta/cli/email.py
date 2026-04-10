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
from recoleta.trend_email import build_trend_email_preview, send_trend_email


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
        "status": "ok",
        "command": command_name,
        "instance": instance_name or result.instance,
        "preview_dir": str(result.preview_dir),
        "manifest_path": str(result.manifest_path),
        "html_path": str(result.html_path),
        "text_path": str(result.text_path),
        "primary_page_url": result.primary_page_url,
        "content_hash": result.content_hash,
        "subject": result.subject,
        "trend_doc_id": result.trend_doc_id,
        "period_token": result.period_token,
    }


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
        "send_dir": str(result.send_dir),
        "manifest_path": str(result.manifest_path),
        "html_path": str(result.html_path),
        "text_path": str(result.text_path),
        "primary_page_url": result.primary_page_url,
        "content_hash": result.content_hash,
        "subject": result.subject,
        "trend_doc_id": result.trend_doc_id,
        "period_token": result.period_token,
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
        f"trend={result.trend_doc_id} period={result.period_token} "
        f"output={result.preview_dir}"
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
        result = send_trend_email(
            settings=runtime.settings,
            repository=runtime.repository,
            site_output_dir=site_output_dir_from_settings(runtime.settings),
            anchor_date=parsed_anchor,
            force_batch=bool(kwargs.get("force_batch", False)),
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
    if result.status == "failed":
        emit_command_error(
            command_name=command_name,
            message=(
                "provider send failed "
                f"trend={result.trend_doc_id} period={result.period_token} "
                f"output={result.send_dir}"
            ),
            console=runtime.console,
            json_output=json_output,
            exit_code=1,
        )
    if json_output:
        cli._emit_json(payload)
        return payload
    color = "yellow" if result.status == "skipped" else "green"
    runtime.console.print(
        f"[{color}]{command_name} {result.status}[/{color}] "
        f"trend={result.trend_doc_id} period={result.period_token} "
        f"output={result.send_dir}"
    )
    return payload
