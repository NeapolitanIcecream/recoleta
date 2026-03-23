from __future__ import annotations

from datetime import UTC, datetime

import recoleta.cli as cli


def run_rag_sync_vectors_command(
    *,
    doc_type: str,
    period_start: str,
    period_end: str,
    page_size: int,
) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        _service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = cli._begin_managed_run(
        command="rag sync-vectors",
        log_module="cli.rag.sync_vectors",
    )

    try:
        start_dt = datetime.fromisoformat(str(period_start).strip())
        end_dt = datetime.fromisoformat(str(period_end).strip())
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]invalid datetime[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc
    if start_dt.tzinfo is None:
        start_dt = start_dt.replace(tzinfo=UTC)
    else:
        start_dt = start_dt.astimezone(UTC)
    if end_dt.tzinfo is None:
        end_dt = end_dt.replace(tzinfo=UTC)
    else:
        end_dt = end_dt.astimezone(UTC)
    if end_dt <= start_dt:
        console.print(
            "[red]invalid datetime range[/red] period_end must be > period_start"
        )
        raise cli.typer.Exit(code=2)
    try:
        with cli._graceful_shutdown_signals():
            from recoleta.rag.sync import sync_summary_vectors_in_period
            from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

            store = LanceVectorStore(
                db_dir=settings.rag_lancedb_dir,
                table_name=embedding_table_name(
                    embedding_model=settings.trends_embedding_model,
                    embedding_dimensions=settings.trends_embedding_dimensions,
                ),
            )
            stats = sync_summary_vectors_in_period(
                repository=repository,
                vector_store=store,
                run_id=run_id,
                doc_type=str(doc_type).strip().lower(),
                period_start=start_dt,
                period_end=end_dt,
                embedding_model=settings.trends_embedding_model,
                embedding_dimensions=settings.trends_embedding_dimensions,
                max_batch_inputs=settings.trends_embedding_batch_max_inputs,
                max_batch_chars=settings.trends_embedding_batch_max_chars,
                embedding_failure_mode=getattr(
                    settings, "trends_embedding_failure_mode", "continue"
                ),
                embedding_max_errors=int(
                    getattr(settings, "trends_embedding_max_errors", 0) or 0
                ),
                page_size=page_size,
                llm_connection=settings.llm_connection_config(),
            )
        heartbeat_monitor.raise_if_failed()
        repository.finish_run(run_id, success=True)
        console.print(f"[green]rag sync completed[/green] stats={stats}")
        cli._print_billing_report(console=console, repository=repository, run_id=run_id)
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="RAG sync interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "RAG sync stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except Exception:
        repository.finish_run(run_id, success=False)
        log.exception("RAG sync failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )


def run_rag_build_index_command(
    *,
    vector: bool,
    scalar: bool,
    vector_index_type: str,
    vector_metric: str,
    vector_num_partitions: int | None,
    vector_num_sub_vectors: int | None,
    strict: bool,
) -> None:
    symbols = cli._runtime_symbols()
    workspace_lease_lost_error = symbols["WorkspaceLeaseLostError"]

    (
        settings,
        repository,
        _service,
        console,
        run_id,
        owner_token,
        log,
        heartbeat_monitor,
    ) = cli._begin_managed_run(
        command="rag build-index",
        log_module="cli.rag.build_index",
    )
    try:
        with cli._graceful_shutdown_signals():
            from recoleta.rag.vector_store import LanceVectorStore, embedding_table_name

            store = LanceVectorStore(
                db_dir=settings.rag_lancedb_dir,
                table_name=embedding_table_name(
                    embedding_model=settings.trends_embedding_model,
                    embedding_dimensions=settings.trends_embedding_dimensions,
                ),
            )
            stats = store.build_indices(
                build_vector_index=bool(vector),
                vector_index_type=str(vector_index_type),
                vector_metric=str(vector_metric),
                vector_num_partitions=vector_num_partitions,
                vector_num_sub_vectors=vector_num_sub_vectors,
                build_scalar_indices=bool(scalar),
                replace=True,
                strict=bool(strict),
            )
        heartbeat_monitor.raise_if_failed()
        errors = stats.get("errors") or []
        table_exists = bool(stats.get("table_exists"))

        if not table_exists:
            repository.finish_run(run_id, success=True)
            console.print(
                "[yellow]rag build-index skipped[/yellow] table not found (run `recoleta rag sync-vectors` first)"
            )
            return

        if strict and errors:
            repository.finish_run(run_id, success=False)
            console.print(f"[red]rag build-index failed[/red] stats={stats}")
            raise cli.typer.Exit(code=1)

        repository.finish_run(run_id, success=True)
        if errors:
            console.print(
                f"[yellow]rag build-index completed with errors[/yellow] stats={stats}"
            )
        else:
            console.print(f"[green]rag build-index completed[/green] stats={stats}")
    except KeyboardInterrupt as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed during interrupt")
        cli._raise_typer_exit_for_interrupt(
            log=log,
            message="RAG build-index interrupted",
            exc=exc,
        )
    except workspace_lease_lost_error as exc:
        try:
            repository.finish_run(run_id, success=False)
        except Exception:
            log.exception("Run finish failed after lease loss")
        log.warning(
            "RAG build-index stopped because workspace lease was lost error_type={} error={}",
            type(exc).__name__,
            str(exc),
        )
        raise cli.typer.Exit(code=1) from None
    except cli.typer.Exit:
        raise
    except Exception:
        repository.finish_run(run_id, success=False)
        log.exception("RAG build-index failed")
        raise
    finally:
        cli._cleanup_managed_run(
            repository=repository,
            owner_token=owner_token,
            heartbeat_monitor=heartbeat_monitor,
            log=log,
        )
