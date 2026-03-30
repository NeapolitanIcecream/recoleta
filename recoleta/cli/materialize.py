from __future__ import annotations

from pathlib import Path

import recoleta.cli as cli


def run_materialize_outputs_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    output_dir: Path | None,
    scope: str,
    granularity: str | None,
    pdf: bool,
    site: bool,
    debug_pdf: bool,
    item_export_scope: str = "linked",
    json_output: bool = False,
    command_name: str = "materialize outputs",
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()
    normalized_scope = cli._require_default_scope(scope)

    try:
        resolved_db_path = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    repository = cli._build_repository_for_db_path(db_path=resolved_db_path)
    repository.init_schema()
    owner_token, lease_log, heartbeat_monitor = cli._acquire_workspace_lease_for_command(
        repository=repository,
        console=console,
        command=command_name,
        log_module="cli.materialize.outputs",
    )
    try:
        settings = cli._maybe_load_settings(
            db_path_option=db_path,
            config_path_option=config_path,
            resolved_db_path=resolved_db_path,
        )
        console = (
            console_cls(stderr=settings.log_json) if settings is not None else console_cls()
        )

        materialize_outputs = cli._import_symbol(
            "recoleta.materialize",
            attr_name="materialize_outputs",
        )
        materialize_scope_spec_cls = cli._import_symbol(
            "recoleta.materialize",
            attr_name="MaterializeScopeSpec",
        )
        default_scope_specs_for_settings = cli._import_symbol(
            "recoleta.materialize",
            attr_name="default_scope_specs_for_settings",
        )

        resolved_output_dir = (
            output_dir.expanduser().resolve() if output_dir is not None else None
        )

        if resolved_output_dir is not None:
            resolved_obsidian_vault_path = None
            resolved_obsidian_base_folder = None
            if settings is not None:
                resolved_obsidian_vault_path = getattr(
                    settings, "obsidian_vault_path", None
                )
                resolved_obsidian_base_folder = str(
                    getattr(settings, "obsidian_base_folder", "") or ""
                ).strip() or None
            scope_specs = [
                materialize_scope_spec_cls(
                    scope=normalized_scope,
                    output_dir=resolved_output_dir,
                    obsidian_vault_path=resolved_obsidian_vault_path,
                    obsidian_base_folder=resolved_obsidian_base_folder,
                )
            ]
            site_input_dir = resolved_output_dir if site else None
            site_output_dir = resolved_output_dir / "site" if site else None
            output_language = getattr(settings, "llm_output_language", None)
        else:
            if settings is None:
                raise ValueError(
                    "output_dir is required when settings are unavailable"
                )
            default_specs = list(default_scope_specs_for_settings(settings=settings))
            if (
                normalized_scope != "default"
                and any(spec.scope == normalized_scope for spec in default_specs)
            ):
                scope_specs = [
                    spec for spec in default_specs if spec.scope == normalized_scope
                ]
            elif normalized_scope != "default" and len(default_specs) == 1:
                scope_specs = [
                    materialize_scope_spec_cls(
                        scope=normalized_scope,
                        output_dir=Path(default_specs[0].output_dir),
                    )
                ]
            elif normalized_scope == "default":
                scope_specs = default_specs
            else:
                available = ", ".join(sorted(spec.scope for spec in default_specs))
                raise ValueError(
                    f"unknown scope '{normalized_scope}' (available: {available})"
                )

            site_input_dir = None
            site_output_dir = None
            if site:
                site_input_dir = Path(scope_specs[0].output_dir)
                site_output_dir = Path(scope_specs[0].output_dir) / "site"
            output_language = settings.llm_output_language

        normalized_item_export_scope = (
            str(item_export_scope or "").strip().lower() or "linked"
        )
        materialize_kwargs: dict[str, object] = {
            "repository": repository,
            "scope_specs": list(scope_specs),
            "granularity": granularity,
            "generate_pdf": pdf,
            "debug_pdf": debug_pdf,
            "output_language": output_language,
            "site_input_dir": site_input_dir,
            "site_output_dir": site_output_dir,
            "localization": (
                getattr(settings, "localization", None) if settings is not None else None
            ),
        }
        if normalized_item_export_scope != "linked":
            materialize_kwargs["item_export_scope"] = normalized_item_export_scope
        result = materialize_outputs(
            **materialize_kwargs,
        )
        heartbeat_monitor.raise_if_failed()
    finally:
        cli._cleanup_workspace_lease(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=lease_log,
        )

    item_notes_total = sum(scope_result.item_notes_total for scope_result in result.scopes)
    trend_notes_total = sum(
        scope_result.trend_notes_total for scope_result in result.scopes
    )
    trend_docs_total = sum(scope_result.trend_docs_total for scope_result in result.scopes)
    trend_failures_total = sum(
        scope_result.trend_failures_total for scope_result in result.scopes
    )
    ideas_notes_total = sum(scope_result.ideas_notes_total for scope_result in result.scopes)
    ideas_outputs_total = sum(
        scope_result.ideas_outputs_total for scope_result in result.scopes
    )
    ideas_failures_total = sum(
        scope_result.ideas_failures_total for scope_result in result.scopes
    )
    obsidian_notes_total = sum(
        scope_result.obsidian_notes_total for scope_result in result.scopes
    )
    obsidian_failures_total = sum(
        scope_result.obsidian_failures_total for scope_result in result.scopes
    )
    trend_pdf_total = sum(scope_result.trend_pdf_total for scope_result in result.scopes)
    trend_pdf_failures_total = sum(
        scope_result.trend_pdf_failures_total for scope_result in result.scopes
    )
    canonical_link_rewrites_total = sum(
        scope_result.canonical_link_rewrites_total for scope_result in result.scopes
    )
    if json_output:
        cli._emit_json(
            {
                "status": "ok",
                "command": command_name,
                "db_path": str(resolved_db_path),
                "scope": normalized_scope,
                "granularity": granularity,
                "site_manifest_path": cli._path_or_none(result.site_manifest_path),
                "totals": {
                    "scopes": len(result.scopes),
                    "items": item_notes_total,
                    "trends": trend_notes_total,
                    "trend_docs": trend_docs_total,
                    "trend_failures": trend_failures_total,
                    "ideas": ideas_notes_total,
                    "idea_outputs": ideas_outputs_total,
                    "idea_failures": ideas_failures_total,
                    "obsidian": obsidian_notes_total,
                    "obsidian_failures": obsidian_failures_total,
                    "canonical_link_rewrites": canonical_link_rewrites_total,
                    "pdfs": trend_pdf_total,
                    "pdf_failures": trend_pdf_failures_total,
                },
                "scopes": [
                    {
                        "scope": scope_result.scope,
                        "output_dir": str(scope_result.output_dir),
                        "item_notes_total": scope_result.item_notes_total,
                        "trend_notes_total": scope_result.trend_notes_total,
                        "trend_docs_total": scope_result.trend_docs_total,
                        "trend_failures_total": scope_result.trend_failures_total,
                        "ideas_notes_total": scope_result.ideas_notes_total,
                        "ideas_outputs_total": scope_result.ideas_outputs_total,
                        "ideas_failures_total": scope_result.ideas_failures_total,
                        "obsidian_notes_total": scope_result.obsidian_notes_total,
                        "obsidian_failures_total": scope_result.obsidian_failures_total,
                        "trend_pdf_total": scope_result.trend_pdf_total,
                        "trend_pdf_failures_total": scope_result.trend_pdf_failures_total,
                        "doc_ref_rewrites_total": scope_result.doc_ref_rewrites_total,
                        "doc_ref_resolved_total": scope_result.doc_ref_resolved_total,
                        "doc_ref_unresolved_total": scope_result.doc_ref_unresolved_total,
                        "canonical_link_rewrites_total": scope_result.canonical_link_rewrites_total,
                    }
                    for scope_result in result.scopes
                ],
            }
        )
        return
    console.print(
        f"[green]{command_name} completed[/green] "
        f"scopes={len(result.scopes)} "
        f"items={item_notes_total} "
        f"trends={trend_notes_total}/{trend_docs_total} "
        f"trend_failures={trend_failures_total} "
        f"ideas={ideas_notes_total}/{ideas_outputs_total} "
        f"idea_failures={ideas_failures_total} "
        f"obsidian={obsidian_notes_total} "
        f"obsidian_failures={obsidian_failures_total} "
        f"canonical_link_rewrites={canonical_link_rewrites_total} "
        f"pdfs={trend_pdf_total} "
        f"pdf_failures={trend_pdf_failures_total}"
    )
    for scope_result in result.scopes:
        console.print(
            f"[cyan]{scope_result.scope}[/cyan] "
            f"output={scope_result.output_dir} "
            f"items={scope_result.item_notes_total} "
            f"trends={scope_result.trend_notes_total}/{scope_result.trend_docs_total} "
            f"ideas={scope_result.ideas_notes_total}/{scope_result.ideas_outputs_total} "
            f"obsidian={scope_result.obsidian_notes_total}"
        )
    if result.site_manifest_path is not None:
        console.print(f"[cyan]site manifest[/cyan] {result.site_manifest_path}")
