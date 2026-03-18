from __future__ import annotations

from click import Context
from pathlib import Path

from recoleta.app.runtime import typer
from recoleta.cli.analyze import run_analyze_command
from recoleta.cli.db import run_db_clear_command, run_db_reset_command
from recoleta.cli.ideas import run_ideas_command
from recoleta.cli.ingest import run_ingest_command
from recoleta.cli.materialize import run_materialize_outputs_command
from recoleta.cli.maintenance import (
    run_backup_command,
    run_doctor_command,
    run_doctor_llm_command,
    run_doctor_why_empty_command,
    run_gc_command,
    run_repair_streams_command,
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
from recoleta.cli.runs import run_runs_list_command, run_runs_show_command
from recoleta.cli.site import (
    run_site_build_command,
    run_site_gh_deploy_command,
    run_site_serve_command,
    run_site_stage_command,
)
from recoleta.cli.trends import run_trends_command, run_trends_week_command

app = typer.Typer(
    help="Recoleta local-first AI research radar CLI.", no_args_is_help=True
)
db_app = typer.Typer(help="Database utilities.", no_args_is_help=True)
app.add_typer(db_app, name="db")
rag_app = typer.Typer(help="RAG utilities.", no_args_is_help=True)
app.add_typer(rag_app, name="rag")
site_app = typer.Typer(help="Static site utilities.", no_args_is_help=True)
app.add_typer(site_app, name="site")
materialize_app = typer.Typer(
    help="Offline output materialization utilities.", no_args_is_help=True
)
app.add_typer(materialize_app, name="materialize")
runs_app = typer.Typer(help="Run history utilities.", no_args_is_help=True)
app.add_typer(runs_app, name="runs")
doctor_app = typer.Typer(help="Workspace diagnostics.", no_args_is_help=False)
app.add_typer(doctor_app, name="doctor")


@app.command()
def ingest(
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to prepare (YYYY-MM-DD or YYYYMMDD). Defaults to latest backlog behavior.",
    ),
) -> None:
    """Pull sources, enrich content, and optionally pre-rank candidates."""
    run_ingest_command(anchor_date=anchor_date)


@app.command()
def analyze(
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Max number of items analyzed in one run. Defaults to ANALYZE_LIMIT.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to analyze (YYYY-MM-DD or YYYYMMDD). Defaults to latest prepared backlog behavior.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Run LLM analysis for prepared items."""
    run_analyze_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


@app.command()
def publish(
    limit: int = typer.Option(
        50, min=1, help="Max number of analyzed items published."
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day to publish (YYYY-MM-DD or YYYYMMDD). Defaults to latest analyzed backlog behavior.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Publish outputs to configured targets (markdown/obsidian/telegram)."""
    run_publish_command(limit=limit, anchor_date=anchor_date, json_output=json_output)


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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
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
        json_output=json_output,
    )


@app.command()
def ideas(
    granularity: str = typer.Option(
        "day",
        "--granularity",
        help="Ideas granularity. Allowed: day, week, month.",
    ),
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD). Defaults to today (UTC).",
    ),
    model: str | None = typer.Option(
        None,
        "--model",
        help="Override LLM model for ideas generation. Defaults to LLM_MODEL.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Generate opportunity ideas from an existing trend synthesis pass output."""
    run_ideas_command(
        granularity=granularity,
        anchor_date=anchor_date,
        model=model,
        json_output=json_output,
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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Generate weekly trends and backfill missing daily trends."""
    run_trends_week_command(
        anchor_date=anchor_date,
        model=model,
        backfill_mode=backfill_mode,
        debug_pdf=debug_pdf,
        json_output=json_output,
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
        help="Directory containing trend markdown notes and sibling idea briefs. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
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
        help="Optionally export only the latest N trend notes and sibling idea briefs.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Build a static website from trend markdown notes and sibling idea briefs."""
    run_site_build_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        json_output=json_output,
    )


@site_app.command("stage")
def site_stage(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes and sibling idea briefs. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        writable=True,
        help="Repo-local directory to mirror trend markdown notes and sibling idea briefs for deployment. Defaults to ./site-content/Trends, or ./site-content in topic-stream mode.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally stage only the latest N trend notes and sibling idea briefs.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Stage trend markdown notes and sibling idea briefs for deployment."""
    run_site_stage_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        json_output=json_output,
    )


@site_app.command("serve")
def site_serve(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes and sibling idea briefs when building before serving. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Directory containing the built static site. Defaults to MARKDOWN_OUTPUT_DIR/site.",
    ),
    limit: int | None = typer.Option(
        None,
        min=1,
        help="Optionally build only the latest N trend notes and sibling idea briefs before serving.",
    ),
    host: str = typer.Option(
        "127.0.0.1",
        "--host",
        help="Host interface to bind the local preview server to.",
    ),
    port: int = typer.Option(
        8000,
        "--port",
        min=0,
        max=65535,
        help="TCP port for the local preview server. Use 0 to auto-select.",
    ),
    build: bool = typer.Option(
        True,
        "--build/--no-build",
        help="Build the static site before serving it.",
    ),
) -> None:
    """Build and serve the static site locally."""
    run_site_serve_command(
        input_dir=input_dir,
        output_dir=output_dir,
        limit=limit,
        host=host,
        port=port,
        build=build,
    )


@site_app.command("gh-deploy")
def site_gh_deploy(
    input_dir: Path | None = typer.Option(
        None,
        "--input-dir",
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
        help="Directory containing trend markdown notes and sibling idea briefs. Defaults to MARKDOWN_OUTPUT_DIR/Trends, or MARKDOWN_OUTPUT_DIR in topic-stream mode.",
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
        help="Optionally deploy only the latest N trend notes and sibling idea briefs.",
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
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
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
        json_output=json_output,
    )


@materialize_app.command("outputs")
def materialize_outputs(
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="SQLite database path. Defaults to RECOLETA_DB_PATH or the configured settings file.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config-path",
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        help="Optional YAML/JSON config path used to resolve the database and default output directories.",
    ),
    output_dir: Path | None = typer.Option(
        None,
        "--output-dir",
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
        help="Markdown output root to rewrite in single-stream mode. Defaults to MARKDOWN_OUTPUT_DIR or per-stream settings output roots.",
    ),
    scope: str = typer.Option(
        "default",
        "--scope",
        help="Scope/stream name for single-stream materialization. When settings define explicit topic streams, the default rewrites every configured stream.",
    ),
    granularity: str | None = typer.Option(
        None,
        "--granularity",
        help="Optionally rerender only day, week, or month trend notes.",
    ),
    pdf: bool = typer.Option(
        False,
        "--pdf/--no-pdf",
        help="Regenerate trend PDFs from the rerendered markdown notes.",
    ),
    site: bool = typer.Option(
        False,
        "--site/--no-site",
        help="Rebuild the static site after markdown outputs are materialized.",
    ),
    debug_pdf: bool = typer.Option(
        False,
        "--debug-pdf/--no-debug-pdf",
        help="Export PDF render debug bundles beside regenerated PDFs.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON output.",
    ),
) -> None:
    """Backfill item pages and rerender trend outputs without rerunning ingest/analyze."""
    run_materialize_outputs_command(
        db_path=db_path,
        config_path=config_path,
        output_dir=output_dir,
        scope=scope,
        granularity=granularity,
        pdf=pdf,
        site=site,
        debug_pdf=debug_pdf,
        json_output=json_output,
    )


@runs_app.command("show")
def runs_show(
    run_id: str | None = typer.Option(
        None,
        "--run-id",
        help="Run id to inspect. Defaults to the most recent run.",
    ),
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
    """Inspect a single recorded run with aggregated metrics and pass outputs."""
    run_runs_show_command(
        run_id=run_id,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@runs_app.command("list")
def runs_list(
    limit: int = typer.Option(
        10,
        "--limit",
        min=1,
        help="Max number of recent runs to return.",
    ),
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
    """List recent runs with compact status and output counts."""
    run_runs_list_command(
        limit=limit,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
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


@doctor_app.callback(invoke_without_command=True)
def doctor(
    ctx: Context,
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
    if getattr(ctx, "invoked_subcommand", None) is not None:
        return
    run_doctor_command(
        healthcheck=healthcheck,
        db_path=db_path,
        config_path=config_path,
        max_success_age_minutes=max_success_age_minutes,
    )


@doctor_app.command("why-empty")
def doctor_why_empty(
    anchor_date: str = typer.Option(
        ...,
        "--date",
        help="Anchor date in UTC (YYYY-MM-DD or YYYYMMDD).",
    ),
    granularity: str = typer.Option(
        "day",
        "--granularity",
        help="Corpus window granularity. Allowed: day, week, month.",
    ),
    stream: str = typer.Option(
        "default",
        "--stream",
        help="Topic stream / scope to inspect. Use default for the default corpus.",
    ),
    min_relevance_score: float | None = typer.Option(
        None,
        "--min-relevance-score",
        help="Override the relevance threshold used when explaining corpus selection.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of human-readable text.",
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
    """Explain why a trend corpus window is empty or smaller than expected."""
    run_doctor_why_empty_command(
        db_path=db_path,
        config_path=config_path,
        anchor_date=anchor_date,
        granularity=granularity,
        stream=stream,
        min_relevance_score=min_relevance_score,
        json_output=json_output,
    )


@doctor_app.command("llm")
def doctor_llm(
    ping: bool = typer.Option(
        False,
        "--ping/--no-ping",
        help="Run a lightweight connectivity probe against the configured LLM model.",
    ),
    timeout_seconds: float = typer.Option(
        20.0,
        "--timeout-seconds",
        min=1.0,
        help="Per-request timeout for the optional LLM ping probe.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of human-readable text.",
    ),
    db_path: Path | None = typer.Option(
        None,
        "--db-path",
        help="Path to the SQLite DB file. Used only to help load settings when needed.",
    ),
    config_path: Path | None = typer.Option(
        None,
        "--config",
        help="Path to config file used to resolve settings.",
    ),
) -> None:
    """Inspect effective LLM configuration and optionally probe the configured provider."""
    run_doctor_llm_command(
        ping=ping,
        timeout_seconds=timeout_seconds,
        json_output=json_output,
        db_path=db_path,
        config_path=config_path,
    )


@app.command("repair-streams")
def repair_streams(
    anchor_date: str = typer.Option(
        ...,
        "--date",
        help="Target UTC day to repair (YYYY-MM-DD or YYYYMMDD).",
    ),
    streams: str = typer.Option(
        ...,
        "--streams",
        help="Comma-separated topic stream names to requeue for analysis.",
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        help="Emit machine-readable JSON instead of human-readable text.",
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
    """Requeue stream-analysis state for a day window without touching items directly."""
    run_repair_streams_command(
        db_path=db_path,
        config_path=config_path,
        anchor_date=anchor_date,
        streams=streams,
        json_output=json_output,
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
    anchor_date: str | None = typer.Option(
        None,
        "--date",
        help="Target UTC day for a one-off run (YYYY-MM-DD or YYYYMMDD). Requires --once.",
    ),
) -> None:
    """Run periodic ingest/analyze/publish jobs with APScheduler (or run once)."""
    run_scheduler_command(
        once=once,
        analyze_limit=analyze_limit,
        publish_limit=publish_limit,
        anchor_date=anchor_date,
    )


def main() -> None:
    app()
