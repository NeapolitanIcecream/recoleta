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
) -> None:
    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    console = console_cls()

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
        command="materialize outputs",
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

        normalized_scope = str(scope or "").strip() or "default"
        resolved_output_dir = (
            output_dir.expanduser().resolve() if output_dir is not None else None
        )

        if resolved_output_dir is not None:
            scope_specs = [
                materialize_scope_spec_cls(
                    scope=normalized_scope,
                    output_dir=resolved_output_dir,
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
                if cli._has_explicit_topic_streams(settings):
                    site_input_dir = Path(settings.markdown_output_dir)
                    site_output_dir = Path(settings.markdown_output_dir) / "site"
                else:
                    site_input_dir = Path(scope_specs[0].output_dir)
                    site_output_dir = Path(scope_specs[0].output_dir) / "site"
            output_language = settings.llm_output_language

        result = materialize_outputs(
            repository=repository,
            scope_specs=list(scope_specs),
            granularity=granularity,
            generate_pdf=pdf,
            debug_pdf=debug_pdf,
            output_language=output_language,
            site_input_dir=site_input_dir,
            site_output_dir=site_output_dir,
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
    trend_pdf_total = sum(scope_result.trend_pdf_total for scope_result in result.scopes)
    trend_pdf_failures_total = sum(
        scope_result.trend_pdf_failures_total for scope_result in result.scopes
    )
    canonical_link_rewrites_total = sum(
        scope_result.canonical_link_rewrites_total for scope_result in result.scopes
    )
    console.print(
        "[green]materialize outputs completed[/green] "
        f"scopes={len(result.scopes)} "
        f"items={item_notes_total} "
        f"trends={trend_notes_total}/{trend_docs_total} "
        f"trend_failures={trend_failures_total} "
        f"canonical_link_rewrites={canonical_link_rewrites_total} "
        f"pdfs={trend_pdf_total} "
        f"pdf_failures={trend_pdf_failures_total}"
    )
    for scope_result in result.scopes:
        console.print(
            f"[cyan]{scope_result.scope}[/cyan] "
            f"output={scope_result.output_dir} "
            f"items={scope_result.item_notes_total} "
            f"trends={scope_result.trend_notes_total}/{scope_result.trend_docs_total}"
        )
    if result.site_manifest_path is not None:
        console.print(f"[cyan]site manifest[/cyan] {result.site_manifest_path}")
