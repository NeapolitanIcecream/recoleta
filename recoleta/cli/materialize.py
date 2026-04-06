from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import recoleta.cli as cli
from recoleta.cli.command_support import load_runtime, RuntimeLoadRequest


@dataclass(frozen=True, slots=True)
class MaterializeCommandRequest:
    db_path: Path | None
    config_path: Path | None
    output_dir: Path | None
    granularity: str | None
    pdf: bool
    site: bool
    debug_pdf: bool
    item_export_scope: str
    json_output: bool
    command_name: str


@dataclass(frozen=True, slots=True)
class MaterializeRunRequest:
    repository: Any
    settings: Any | None
    output_dir: Path | None
    granularity: str | None
    pdf: bool
    site: bool
    debug_pdf: bool
    item_export_scope: str


@dataclass(frozen=True, slots=True)
class MaterializeResultContext:
    command_name: str
    resolved_db_path: Path
    result: Any
    granularity: str | None
    json_output: bool
    console: Any


def run_materialize_outputs_command(**kwargs: Any) -> None:
    request = MaterializeCommandRequest(
        db_path=kwargs.get("db_path"),
        config_path=kwargs.get("config_path"),
        output_dir=kwargs.get("output_dir"),
        granularity=kwargs.get("granularity"),
        pdf=bool(kwargs.get("pdf", False)),
        site=bool(kwargs.get("site", False)),
        debug_pdf=bool(kwargs.get("debug_pdf", False)),
        item_export_scope=str(kwargs.get("item_export_scope", "linked")),
        json_output=bool(kwargs.get("json_output", False)),
        command_name=str(kwargs.get("command_name", "materialize outputs")),
    )
    runtime = load_runtime(
        request=RuntimeLoadRequest(
            db_path=request.db_path,
            config_path=request.config_path,
            command_name=request.command_name,
            require_settings=False,
            init_schema=True,
        ),
    )
    owner_token, lease_log, heartbeat_monitor = (
        cli._acquire_workspace_lease_for_command(
            repository=runtime.repository,
            console=runtime.console,
            command=request.command_name,
            log_module="cli.materialize.outputs",
        )
    )
    try:
        result = _materialize_outputs(
            request=MaterializeRunRequest(
                repository=runtime.repository,
                settings=runtime.settings,
                output_dir=request.output_dir,
                granularity=request.granularity,
                pdf=request.pdf,
                site=request.site,
                debug_pdf=request.debug_pdf,
                item_export_scope=request.item_export_scope,
            )
        )
        heartbeat_monitor.raise_if_failed()
    finally:
        cli._cleanup_workspace_lease(
            repository=runtime.repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=lease_log,
        )
    _emit_materialize_result(
        context=MaterializeResultContext(
            command_name=request.command_name,
            resolved_db_path=runtime.resolved_db_path,
            result=result,
            granularity=request.granularity,
            json_output=request.json_output,
            console=runtime.console,
        )
    )


def _materialize_outputs(*, request: MaterializeRunRequest) -> Any:
    materialize_outputs = cli._import_symbol(
        "recoleta.materialize",
        attr_name="materialize_outputs",
    )
    target_spec, site_input_dir, site_output_dir, output_language = (
        _materialize_target_config(
            settings=request.settings,
            output_dir=request.output_dir,
            site=request.site,
        )
    )
    materialize_kwargs: dict[str, object] = {
        "repository": request.repository,
        "target_spec": target_spec,
        "granularity": request.granularity,
        "generate_pdf": request.pdf,
        "debug_pdf": request.debug_pdf,
        "output_language": output_language,
        "site_input_dir": site_input_dir,
        "site_output_dir": site_output_dir,
        "localization": (
            getattr(request.settings, "localization", None)
            if request.settings is not None
            else None
        ),
    }
    normalized_item_export_scope = (
        str(request.item_export_scope or "").strip().lower() or "linked"
    )
    if normalized_item_export_scope != "linked":
        materialize_kwargs["item_export_scope"] = normalized_item_export_scope
    return materialize_outputs(**materialize_kwargs)


def _materialize_target_config(
    *,
    settings: Any | None,
    output_dir: Path | None,
    site: bool,
) -> tuple[Any, Path | None, Path | None, Any]:
    materialize_module = cli._import_symbol("recoleta.materialize")
    materialize_target_spec_cls = getattr(materialize_module, "MaterializeTargetSpec")
    default_target_spec_for_settings = getattr(
        materialize_module,
        "default_target_spec_for_settings",
    )
    if output_dir is not None:
        resolved_output_dir = output_dir.expanduser().resolve()
        target_spec = materialize_target_spec_cls(
            output_dir=resolved_output_dir,
            obsidian_vault_path=(
                getattr(settings, "obsidian_vault_path", None)
                if settings is not None
                else None
            ),
            obsidian_base_folder=(
                str(getattr(settings, "obsidian_base_folder", "") or "").strip() or None
                if settings is not None
                else None
            ),
        )
        return (
            target_spec,
            resolved_output_dir if site else None,
            resolved_output_dir / "site" if site else None,
            getattr(settings, "llm_output_language", None),
        )
    if settings is None:
        raise ValueError("output_dir is required when settings are unavailable")
    target_spec = default_target_spec_for_settings(settings=settings)
    return (
        target_spec,
        Path(target_spec.output_dir) if site else None,
        Path(target_spec.output_dir) / "site" if site else None,
        settings.llm_output_language,
    )


def _emit_materialize_result(*, context: MaterializeResultContext) -> None:
    output = context.result.output
    if context.json_output:
        cli._emit_json(
            {
                "status": "ok",
                "command": context.command_name,
                "db_path": str(context.resolved_db_path),
                "granularity": context.granularity,
                "site_manifest_path": cli._path_or_none(
                    context.result.site_manifest_path
                ),
                "totals": {
                    "items": output.item_notes_total,
                    "trends": output.trend_notes_total,
                    "trend_docs": output.trend_docs_total,
                    "trend_failures": output.trend_failures_total,
                    "ideas": output.ideas_notes_total,
                    "idea_outputs": output.ideas_outputs_total,
                    "idea_failures": output.ideas_failures_total,
                    "obsidian": output.obsidian_notes_total,
                    "obsidian_failures": output.obsidian_failures_total,
                    "canonical_link_rewrites": output.canonical_link_rewrites_total,
                    "pdfs": output.trend_pdf_total,
                    "pdf_failures": output.trend_pdf_failures_total,
                },
                "output": {
                    "output_dir": str(output.output_dir),
                    "item_notes_total": output.item_notes_total,
                    "trend_notes_total": output.trend_notes_total,
                    "trend_docs_total": output.trend_docs_total,
                    "trend_failures_total": output.trend_failures_total,
                    "ideas_notes_total": output.ideas_notes_total,
                    "ideas_outputs_total": output.ideas_outputs_total,
                    "ideas_failures_total": output.ideas_failures_total,
                    "obsidian_notes_total": output.obsidian_notes_total,
                    "obsidian_failures_total": output.obsidian_failures_total,
                    "trend_pdf_total": output.trend_pdf_total,
                    "trend_pdf_failures_total": output.trend_pdf_failures_total,
                    "doc_ref_rewrites_total": output.doc_ref_rewrites_total,
                    "doc_ref_resolved_total": output.doc_ref_resolved_total,
                    "doc_ref_unresolved_total": output.doc_ref_unresolved_total,
                    "canonical_link_rewrites_total": output.canonical_link_rewrites_total,
                },
            }
        )
        return
    context.console.print(
        f"[green]{context.command_name} completed[/green] "
        f"output={output.output_dir} "
        f"items={output.item_notes_total} "
        f"trends={output.trend_notes_total}/{output.trend_docs_total} "
        f"trend_failures={output.trend_failures_total} "
        f"ideas={output.ideas_notes_total}/{output.ideas_outputs_total} "
        f"idea_failures={output.ideas_failures_total} "
        f"obsidian={output.obsidian_notes_total} "
        f"obsidian_failures={output.obsidian_failures_total} "
        f"canonical_link_rewrites={output.canonical_link_rewrites_total} "
        f"pdfs={output.trend_pdf_total} "
        f"pdf_failures={output.trend_pdf_failures_total}"
    )
    if context.result.site_manifest_path is not None:
        context.console.print(
            f"[cyan]site manifest[/cyan] {context.result.site_manifest_path}"
        )
