from __future__ import annotations

from pathlib import Path

from recoleta.app.runtime import typer
from recoleta.cli.analyze import run_analyze_command
from recoleta.cli.db import run_db_clear_command, run_db_reset_command
from recoleta.cli.ingest import run_ingest_command
from recoleta.cli.maintenance import (
    run_backup_command,
    run_doctor_command,
    run_gc_command,
    run_restore_command,
    run_stats_command,
    run_vacuum_command,
)
from recoleta.cli.publish import run_publish_command
from recoleta.cli.rag import (
    run_rag_build_index_command,
    run_rag_sync_vectors_command,
)
from recoleta.cli.run import run_scheduler_command
from recoleta.cli.site import (
    run_site_build_command,
    run_site_gh_deploy_command,
    run_site_stage_command,
)
from recoleta.cli.trends import run_trends_command, run_trends_week_command

app = typer.Typer(
    help="Recoleta research intelligence funnel CLI.", no_args_is_help=True
)
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True)
app.add_typer(db_app, name="db")
rag_app = typer.Typer(help="RAG utilities.", no_args_is_help=True)
app.add_typer(rag_app, name="rag")
site_app = typer.Typer(help="Static site utilities.", no_args_is_help=True)
app.add_typer(site_app, name="site")


@app.command()
def ingest() -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""
    run_ingest_command()


@app.command()
def analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    ),
) -> None:
    """Run LLM analysis for prepared items."""
    run_analyze_command(limit=limit)


@app.command()
def publish(
    limit: int = typer.Option(
        50, min=1, help="Max number of analyzed items published."
    ),
) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""
    run_publish_command(limit=limit)


@app.command()
def trends(
    granularity: str = typer.Option(
        "day",
        "--granularity",
        help="Trend granularity. Allowed: day, week, month.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for trend generation. Defaults to LLM_MODEL.",
    ),
    backfill: bool = typer.Option(
        False,
        "--backfill/--no-backfill",
        help="Backfill missing lower-granularity trends before generating week/month trends.",
    ),
    backfill_mode: str = typer.Option(
        "missing",
        "--backfill-mode",
        help="Backfill policy. Allowed: missing, all.",
    ),
    debug_pdf: bool = typer.Option(
        False,
        "--debug-pdf/--no-debug-pdf",
        help="Export PDF render intermediates and page previews beside the trend PDF.",
    ),
) -> None:
    """Generate trends for a period (day/week/month)."""
    run_trends_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        backfill=backfill,
        backfill_mode=backfill_mode,
        debug_pdf=debug_pdf,
    )


@app.command("trends-week")
def trends_week(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for trend generation. Defaults to LLM_MODEL.",
    ),
    backfill_mode: str = typer.Option(
        "missing",
        "--backfill-mode",
        help="Backfill policy for missing day trends. Allowed: missing, all.",
    ),
    debug_pdf: bool = typer.Option(
        False,
        "--debug-pdf/--no-debug-pdf",
        help="Export PDF render intermediates and page previews beside the trend PDF.",
    ),
) -> None:
    """Generate weekly trends and backfill missing daily trends."""
    run_trends_week_command(
        anchor_date=anchor_date,
        model=model,
        backfill_mode=backfill_mode,
        debug_pdf=debug_pdf,
    )


@site_app.command("build")
def site_build(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Destination directory for the exported static site. Defaults to MARKDOWN_OUTPUT_DIR/site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally export only the latest N trend notes.",
    ),
) -> None:
    """Build a static website from trend markdown notes."""
    run_site_build_command(input_dir=input_dir, output_dir=output_dir, limit=limit)


@site_app.command("stage")
def site_stage(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        writable=True,
        help="Repo-local directory to mirror trend markdown notes for deployment. Defaults to ./site-content/Trends, or ./site-content in topic-stream mode.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally stage only the latest N trend notes.",
    ),
) -> None:
    """Stage trend markdown notes into a repo-local directory for deployment."""
    run_site_stage_command(input_dir=input_dir, output_dir=output_dir, limit=limit)


@site_app.command("gh-deploy")
def site_gh_deploy(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    repo_dir: Path | None = typer.Option(
        None,
        "--repo-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Git repository used to resolve the deployment remote. Defaults to the current working directory.",
    ),
    remote: str = typer.Option(
        "origin",
        "--remote",
        help="Git remote that will receive the deployment branch.",
    ),
    branch: str = typer.Option(
        "gh-pages",
        "--branch",
        help="Deployment branch used by GitHub Pages.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally deploy only the latest N trend notes.",
    ),
    commit_message: str | None = typer.Option(
        None,
        "--message",
        help="Optional git commit message for the deployment branch update.",
    ),
    cname: str | None = typer.Option(
        None,
        "--cname",
        help="Optional custom domain written to the deployment branch CNAME file.",
    ),
    pages_config: str = typer.Option(
        "auto",
        "--pages-config",
        help="How to configure the GitHub Pages source after pushing. Allowed: auto, always, never.",
    ),
    force: bool = typer.Option(
        True,
        "--force/--no-force",
        help="Force-push the deployment branch. Defaults to force for derived site output.",
    ),
) -> None:
    """Build the static site and push it to a dedicated GitHub Pages branch."""
    run_site_gh_deploy_command(
        input_dir=input_dir,
        repo_dir=repo_dir,
        remote=remote,
        branch=branch,
        limit=limit,
        commit_message=commit_message,
        cname=cname,
        pages_config=pages_config,
        force=force,
    )


@rag_app.command("sync-vectors")
def rag_sync_vectors(
    doc_type: str = typer.Option(
        "item",
        "--doc-type",
        help="Corpus doc_type for summary vector sync. Allowed: item, trend.",
    ),
    period_start: str = typer.Option(
        ...,
        "--period-start",
        help="Inclusive start time (ISO 8601, UTC recommended).",
    ),
    period_end: str = typer.Option(
        ...,
        "--period-end",
        help="Exclusive end time (ISO 8601, UTC recommended).",
    ),
    page_size: int = typer.Option(
        500, "--page-size", min=1, max=5000, help="SQLite paging size per batch."
    ),
) -> None:
    """Sync/rebuild summary vectors from SQLite corpus into LanceDB."""
    run_rag_sync_vectors_command(
        doc_type=doc_type,
        period_start=period_start,
        period_end=period_end,
        page_size=page_size,
    )


@rag_app.command("build-index")
def rag_build_index(
    vector: bool = typer.Option(
        True, "--vector/--no-vector", help="Build a vector index (ANN)."
    ),
    scalar: bool = typer.Option(
        True,
        "--scalar/--no-scalar",
        help="Build scalar indices for filter columns.",
    ),
    vector_index_type: str = typer.Option(
        "IVF_HNSW_SQ",
        "--vector-index-type",
        help="Vector index type. Examples: IVF_FLAT, IVF_SQ, IVF_HNSW_SQ, IVF_PQ (requires enough rows).",
    ),
    vector_metric: str = typer.Option(
        "cosine",
        "--vector-metric",
        help="Vector distance metric. Examples: cosine, l2, dot.",
    ),
    vector_num_partitions: int | None = typer.Option(
        None,
        "--vector-num-partitions",
        min=1,
        help="Optional IVF partition count. If omitted, LanceDB chooses defaults.",
    ),
    vector_num_sub_vectors: int | None = typer.Option(
        None,
        "--vector-num-sub-vectors",
        min=1,
        help="Optional PQ sub-vector count (PQ variants only).",
    ),
    strict: bool = typer.Option(
        False,
        "--strict",
        help="Exit non-zero if any index build fails.",
    ),
) -> None:
    """Build/rebuild indices for the current embedding table in LanceDB."""
    run_rag_build_index_command(
        vector=vector,
        scalar=scalar,
        vector_index_type=vector_index_type,
        vector_metric=vector_metric,
        vector_num_partitions=vector_num_partitions,
        vector_num_sub_vectors=vector_num_sub_vectors,
        strict=strict,
    )


@db_app.command("clear")
def db_clear(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm deletion without prompting.",
    ),
) -> None:
    """Delete the configured SQLite DB file (and sidecar files) for a clean slate."""
    run_db_clear_command(
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@app.command("gc")
def gc(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    prune_caches: bool = typer.Option(
        False,
        "--prune-caches",
        help="Also prune rebuildable caches such as chunk indices, inactive LanceDB tables, trend PDFs, and managed site output.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Report what would be deleted without mutating the workspace.",
    ),
) -> None:
    """Prune expired debug material and operational history."""
    run_gc_command(
        db_path=db_path,
        config_path=config_path,
        prune_caches=prune_caches,
        dry_run=dry_run,
    )


@app.command("vacuum")
def vacuum(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
) -> None:
    """Run SQLite VACUUM on the configured database."""
    run_vacuum_command(db_path=db_path, config_path=config_path)


@app.command("backup")
def backup(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Directory where timestamped backup bundles should be created. Defaults to <db-dir>/backups.",
    ),
) -> None:
    """Create a DB-scoped backup bundle with manifest metadata."""
    run_backup_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
    )


@app.command("restore")
def restore(
    bundle: Path = typer.Option(
        ...,
        "--bundle",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Path to a backup bundle directory created by `recoleta backup`.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    yes: bool = typer.Option(
        False,
        "--yes",
        "-y",
        help="Confirm replacing the target DB.",
    ),
) -> None:
    """Restore the SQLite DB from a backup bundle."""
    run_restore_command(
        bundle=bundle,
        db_path=db_path,
        config_path=config_path,
        yes=yes,
    )


@app.command("stats")
def stats(
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
) -> None:
    """Summarize read-only workspace operational state."""
    run_stats_command(
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@app.command("doctor")
def doctor(
    healthcheck: bool = typer.Option(
        False,
        "--healthcheck",
        help="Run a read-only healthcheck suitable for supervisors and containers.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Overrides config/env.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve recoleta_db_path.",
    ),
    max_success_age_minutes: int | None = typer.Option(
        None,
        "--max-success-age-minutes",
        min=1,
        help="Fail if the latest successful run is older than this many minutes.",
    ),
) -> None:
    """Run read-only diagnostics for the current workspace."""
    run_doctor_command(
        healthcheck=healthcheck,
        db_path=db_path,
        config_path=config_path,
        max_success_age_minutes=max_success_age_minutes,
    )


@db_app.command("reset")
def db_reset(
    db_path: Path | None = typer.Option(
        None, "--db-path", help="Path to the SQLite DB file. Overrides config/env."
    ),
    config_path: Path | None = typer.Option(
        None, "--config", help="Path to config file used to resolve recoleta_db_path."
    ),
    trends_only: bool = typer.Option(
        False,
        "--trends-only",
        help="Only reset trend-related documents/chunks (keeps items, analyses, contents).",
    ),
    yes: bool = typer.Option(
        False, "--yes", "-y", help="Confirm deletion without prompting."
    ),
) -> None:
    """Reset the SQLite DB (full reset) or only trend-related content."""
    run_db_reset_command(
        db_path=db_path,
        config_path=config_path,
        trends_only=trends_only,
        yes=yes,
    )


@app.command("run")
def run_scheduler(
    once: bool = typer.Option(
        False,
        "--once",
        help="Run ingest/analyze/publish once and exit (no scheduler).",
    ),
    analyze_limit: int | None = typer.Option(
        None,
        "--analyze-limit",
        min=1,
        help="Max number of items analyzed in the one-off run. Defaults to ANALYZE_LIMIT.",
    ),
    publish_limit: int = typer.Option(
        50,
        "--publish-limit",
        min=1,
        help="Max number of analyzed items published in the one-off run.",
    ),
) -> None:
    """Run periodic ingest/analyze/publish jobs with APScheduler (or run once)."""
    run_scheduler_command(
        once=once,
        analyze_limit=analyze_limit,
        publish_limit=publish_limit,
    )


def main() -> None:
    app()
