from __future__ import annotations
from pathlib import Path

import recoleta.cli as cli


def run_db_clear_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    yes: bool,
) -> None:
    if not yes:
        cli.typer.echo("refusing to delete db without --yes")
        raise cli.typer.Exit(code=2)

    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    console = console_cls()

    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    to_delete = [
        resolved,
        Path(f"{resolved}-wal"),
        Path(f"{resolved}-shm"),
        Path(f"{resolved}-journal"),
    ]
    deleted: list[str] = []
    for path in to_delete:
        try:
            if path.exists():
                path.unlink()
                deleted.append(str(path))
        except Exception as exc:  # noqa: BLE001
            logger.bind(module="cli.db.clear").warning(
                "db delete failed path={} error={}", str(path), str(exc)
            )
            console.print(f"[red]failed to delete[/red] {path}")
            raise cli.typer.Exit(code=1) from exc

    if deleted:
        console.print(
            f"[green]db cleared[/green] deleted={len(deleted)} path={resolved}"
        )
    else:
        console.print(f"[green]db already empty[/green] path={resolved}")


def run_db_reset_command(
    *,
    db_path: Path | None,
    config_path: Path | None,
    trends_only: bool,
    yes: bool,
) -> None:
    if not trends_only:
        run_db_clear_command(db_path=db_path, config_path=config_path, yes=yes)
        return

    if not yes:
        cli.typer.echo("refusing to reset trends without --yes")
        raise cli.typer.Exit(code=2)

    symbols = cli._runtime_symbols()
    console_cls = symbols["Console"]
    logger = symbols["logger"]
    repository_cls = symbols["Repository"]
    console = console_cls()
    log = logger.bind(module="cli.db.reset")

    try:
        resolved = cli._resolve_db_path(db_path=db_path, config_path=config_path)
    except Exception as exc:  # noqa: BLE001
        console.print(f"[red]db path resolution failed[/red] {exc}")
        raise cli.typer.Exit(code=2) from exc

    if not resolved.exists():
        console.print(f"[green]db already empty[/green] path={resolved}")
        return

    repository = repository_cls(db_path=resolved)
    repository.init_schema()

    sqlmodel_session = cli._import_symbol("sqlmodel", attr_name="Session")
    sqlmodel_select = cli._import_symbol("sqlmodel", attr_name="select")
    document_model = cli._import_symbol("recoleta.models", attr_name="Document")

    with sqlmodel_session(repository.engine) as session:  # type: ignore[operator]
        statement = sqlmodel_select(document_model).where(
            document_model.doc_type.in_(["item", "trend"])
        )
        docs = list(session.exec(statement))
        doc_ids = [int(getattr(d, "id") or 0) for d in docs if getattr(d, "id", None)]

    chunks_deleted_total = 0
    for doc_id in doc_ids:
        chunks_deleted_total += int(repository.delete_document_chunks(doc_id=doc_id))

    docs_deleted_total = 0
    with sqlmodel_session(repository.engine) as session:  # type: ignore[operator]
        statement = sqlmodel_select(document_model).where(
            document_model.id.in_(doc_ids)
        )
        for doc in session.exec(statement):
            session.delete(doc)
            docs_deleted_total += 1
        session.commit()

    log.info(
        "Trends reset done deleted_docs={} deleted_chunks={} path={}",
        docs_deleted_total,
        chunks_deleted_total,
        str(resolved),
    )
    console.print(
        "[green]db trends reset[/green] "
        f"deleted_docs={docs_deleted_total} deleted_chunks={chunks_deleted_total} path={resolved}"
    )
