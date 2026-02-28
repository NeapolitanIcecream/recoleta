from __future__ import annotations

import json
import os
import random
import re
import sqlite3
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import typer
from litellm.utils import token_counter
from loguru import logger
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from recoleta.analyzer import LiteLLMAnalyzer
from recoleta.config import Settings
from recoleta.observability import configure_process_logging, get_rich_console


app = typer.Typer(add_completion=False, help="Inspect recoleta benchmark SQLite DB contents.")


@dataclass(frozen=True)
class DbPaths:
    bench_dir: Path
    db_path: Path
    bench_results_path: Path | None


def _open_db(path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(str(path))
    con.row_factory = sqlite3.Row
    return con


def _median(values: list[int]) -> int | None:
    if not values:
        return None
    return int(statistics.median(values))


def _p95(values: list[int]) -> int | None:
    if not values:
        return None
    sorted_values = sorted(values)
    idx = max(0, int(round(0.95 * (len(sorted_values) - 1))))
    return int(sorted_values[idx])


def _safe_token_counter(*, model: str, messages: list[dict[str, str]]) -> tuple[int, str | None]:
    try:
        value = int(token_counter(model=model, messages=messages))
        return value, None
    except Exception as exc:
        fallback_model = "gpt-3.5-turbo"
        try:
            value = int(token_counter(model=fallback_model, messages=messages))
            return value, f"token_counter failed for model={model!r}, fell back to {fallback_model!r}: {type(exc).__name__}: {exc}"
        except Exception as fallback_exc:  # noqa: BLE001
            raise RuntimeError(
                f"token_counter failed for model={model!r} and fallback model={fallback_model!r}: {fallback_exc}"
            ) from fallback_exc


def _resolve_paths(*, bench_dir: Path, db: Path | None) -> DbPaths:
    bench_dir = bench_dir.expanduser().resolve()
    if db is not None:
        db_path = db.expanduser().resolve()
        bench_results_path = None
        return DbPaths(bench_dir=bench_dir, db_path=db_path, bench_results_path=bench_results_path)

    candidates = sorted(bench_dir.glob("recoleta-bench-*.db"))
    if not candidates:
        raise typer.BadParameter(f"No DB found under bench_dir={bench_dir}")
    if len(candidates) > 1:
        logger.bind(bench_dir=str(bench_dir)).warning(
            "Multiple DBs found under bench_dir; using the first one: {}",
            str(candidates[0]),
        )
    db_path = candidates[0]
    bench_results = bench_dir / "bench-results.json"
    bench_results_path = bench_results if bench_results.exists() else None
    return DbPaths(bench_dir=bench_dir, db_path=db_path, bench_results_path=bench_results_path)


def _maybe_load_settings(*, bench_results_path: Path | None, config: Path | None) -> Settings | None:
    config_path: Path | None = None
    if config is not None:
        config_path = config.expanduser().resolve()
    elif bench_results_path is not None:
        try:
            payload = json.loads(bench_results_path.read_text(encoding="utf-8"))
            raw = payload.get("config_path")
            if isinstance(raw, str) and raw.strip():
                config_path = Path(raw).expanduser().resolve()
        except Exception as exc:  # noqa: BLE001
            logger.bind(path=str(bench_results_path)).warning("Failed to parse bench-results.json: {}", exc)

    if config_path is None:
        return None
    os.environ["RECOLETA_CONFIG_PATH"] = str(config_path)
    try:
        return Settings()  # pyright: ignore[reportCallIssue]
    except Exception as exc:  # noqa: BLE001
        logger.bind(path=str(config_path)).warning("Failed to load Settings from config: {}", exc)
        return None


def _item_rows(con: sqlite3.Connection) -> list[sqlite3.Row]:
    cur = con.cursor()
    return cur.execute(
        "select id, source, source_item_id, canonical_url, title from items order by id",
    ).fetchall()


def _content_types(con: sqlite3.Connection) -> list[str]:
    cur = con.cursor()
    rows = cur.execute("select distinct content_type from contents order by content_type").fetchall()
    return [str(r[0]) for r in rows]


def _text_for(con: sqlite3.Connection, *, item_id: int, content_type: str) -> str:
    cur = con.cursor()
    row = cur.execute(
        "select text from contents where item_id=? and content_type=? order by id desc limit 1",
        (int(item_id), str(content_type)),
    ).fetchone()
    if row is None:
        return ""
    return str(row[0] or "")


def _excerpt(text: str, *, max_chars: int = 5000) -> str:
    trimmed = (text or "").strip()
    return trimmed[: max(0, int(max_chars))]


def _markup_stats(text: str, *, max_chars: int = 5000) -> dict[str, Any]:
    excerpt = _excerpt(text, max_chars=max_chars)
    if not excerpt:
        return {"chars": 0}
    tag_like = len(re.findall(r"<[^>]{1,200}>", excerpt))
    lt = excerpt.count("<")
    return {
        "chars": len(excerpt),
        "lt_per_1k": round(lt / max(1, len(excerpt)) * 1000, 2),
        "tag_like": tag_like,
        "ltx_": excerpt.count("ltx_"),
        "href=": excerpt.count("href="),
        "orcid": excerpt.count("orcid.org"),
    }


@app.command()
def summary(
    bench_dir: Path = typer.Option(
        Path("bench-out-html-md-v2"),
        help="Benchmark output directory containing recoleta-bench-*.db.",
    ),
    db: Path | None = typer.Option(None, help="Optional explicit path to the SQLite DB."),
) -> None:
    """Print content_type distribution and basic length stats."""
    configure_process_logging(level="INFO", log_json=False)
    console = get_rich_console()
    paths = _resolve_paths(bench_dir=bench_dir, db=db)

    con = _open_db(paths.db_path)
    try:
        types = _content_types(con)
        table = Table(title=f"DB summary: {paths.db_path.name}")
        table.add_column("content_type", style="bold")
        table.add_column("n", justify="right")
        table.add_column("min_len", justify="right")
        table.add_column("median_len", justify="right")
        table.add_column("p95_len", justify="right")
        table.add_column("max_len", justify="right")
        table.add_column("exact_200k", justify="right")

        cur = con.cursor()
        for t in types:
            rows = cur.execute("select length(text) as n from contents where content_type=?", (t,)).fetchall()
            lengths = [int(r["n"] or 0) for r in rows]
            exact_200k = sum(1 for v in lengths if v == 200_000)
            table.add_row(
                t,
                str(len(lengths)),
                str(min(lengths) if lengths else 0),
                str(_median(lengths) or 0),
                str(_p95(lengths) or 0),
                str(max(lengths) if lengths else 0),
                str(exact_200k),
            )
        console.print(table)
    finally:
        con.close()


@app.command()
def items(
    bench_dir: Path = typer.Option(Path("bench-out-html-md-v2"), help="Benchmark output directory."),
    db: Path | None = typer.Option(None, help="Optional explicit path to the SQLite DB."),
) -> None:
    """List items with per-type character lengths (quick scan for outliers)."""
    configure_process_logging(level="INFO", log_json=False)
    console = get_rich_console()
    paths = _resolve_paths(bench_dir=bench_dir, db=db)
    con = _open_db(paths.db_path)
    try:
        types = _content_types(con)
        rows = _item_rows(con)
        cur = con.cursor()

        table = Table(title=f"Items: {paths.db_path.name}")
        table.add_column("item_id", justify="right")
        table.add_column("arxiv_id")
        table.add_column("title", overflow="fold")
        for t in types:
            table.add_column(t, justify="right")

        for it in rows:
            item_id = int(it["id"])
            lengths_by_type: dict[str, int] = {}
            for t in types:
                r = cur.execute(
                    "select length(text) as n from contents where item_id=? and content_type=?",
                    (item_id, t),
                ).fetchone()
                lengths_by_type[t] = int((r["n"] if r else 0) or 0)
            title = str(it["title"] or "").strip()
            if len(title) > 80:
                title = title[:77] + "..."
            table.add_row(
                str(item_id),
                str(it["source_item_id"] or ""),
                title,
                *[str(lengths_by_type[t]) for t in types],
            )
        console.print(table)
    finally:
        con.close()


@app.command()
def sample(
    arxiv_id: str | None = typer.Option(None, help="Sample a specific arXiv id (e.g. 2602.23216v1)."),
    item_id: int | None = typer.Option(None, help="Sample a specific item id."),
    content_type: str | None = typer.Option(None, help="Optional: only show one content_type."),
    max_chars: int = typer.Option(1200, help="How many chars to show per sample (excerpt from start)."),
    bench_dir: Path = typer.Option(Path("bench-out-html-md-v2"), help="Benchmark output directory."),
    db: Path | None = typer.Option(None, help="Optional explicit path to the SQLite DB."),
) -> None:
    """Show excerpt(s) for one item, plus markup/noise counters."""
    configure_process_logging(level="INFO", log_json=False)
    console = get_rich_console()
    paths = _resolve_paths(bench_dir=bench_dir, db=db)
    con = _open_db(paths.db_path)
    try:
        cur = con.cursor()
        if item_id is None:
            if arxiv_id:
                row = cur.execute("select id from items where source_item_id=?", (arxiv_id,)).fetchone()
                if row is None:
                    raise typer.BadParameter(f"Unknown arxiv_id={arxiv_id!r}")
                item_id = int(row["id"])
            else:
                candidates = [int(r["id"]) for r in _item_rows(con)]
                if not candidates:
                    raise RuntimeError("No items in DB.")
                item_id = random.choice(candidates)

        it = cur.execute(
            "select id, source_item_id, canonical_url, title from items where id=?",
            (int(item_id),),
        ).fetchone()
        if it is None:
            raise typer.BadParameter(f"Unknown item_id={item_id}")

        types = _content_types(con)
        selected_types = [content_type] if content_type else types
        title = str(it["title"] or "").strip()
        header = Text.assemble(
            ("item_id=", "bold"),
            (str(it["id"]), "bold cyan"),
            ("  arxiv_id=", "bold"),
            (str(it["source_item_id"] or ""), "bold cyan"),
        )
        if title:
            header.append("\n")
            header.append(title, style="bold")
        console.print(Panel(header, title="Item", expand=False))

        for t in selected_types:
            raw = _text_for(con, item_id=int(item_id), content_type=str(t))
            ex = _excerpt(raw, max_chars=max_chars)
            stats = _markup_stats(raw, max_chars=5000)
            body = Text()
            body.append(json.dumps(stats, ensure_ascii=False), style="dim")
            body.append("\n\n")
            body.append(ex if ex else "<empty>")
            console.print(Panel(body, title=f"{t} (start excerpt, max_chars={max_chars})", expand=False))
    finally:
        con.close()


@app.command("prompt-cost")
def prompt_cost(
    model: str | None = typer.Option(None, help="Override model for token_counter (defaults to Settings.llm_model)."),
    config: Path | None = typer.Option(None, help="Optional recoleta.yaml; overrides bench-results.json config_path."),
    content_types: list[str] = typer.Option(
        ["html_maintext", "html_document_md", "html_document"],
        help="Which content_types to compare for prompt token cost.",
    ),
    bench_dir: Path = typer.Option(Path("bench-out-html-md-v2"), help="Benchmark output directory."),
    db: Path | None = typer.Option(None, help="Optional explicit path to the SQLite DB."),
) -> None:
    """Compare token cost of the analyzer prompt across content_types."""
    configure_process_logging(level="INFO", log_json=False)
    console = get_rich_console()
    paths = _resolve_paths(bench_dir=bench_dir, db=db)
    settings = _maybe_load_settings(bench_results_path=paths.bench_results_path, config=config)
    effective_model = (model or (settings.llm_model if settings else None) or "").strip() or "gpt-4o-mini"
    analyzer = LiteLLMAnalyzer(model=effective_model, output_language=(settings.llm_output_language if settings else None))

    con = _open_db(paths.db_path)
    try:
        items_rows = _item_rows(con)
        table = Table(title=f"Prompt token cost (model={effective_model})")
        table.add_column("arxiv_id", style="bold")
        table.add_column("title", overflow="fold")
        for ct in content_types:
            table.add_column(f"{ct}_tokens", justify="right")
            table.add_column(f"{ct}_lt/1k", justify="right")

        warnings: list[str] = []
        for it in items_rows:
            title = str(it["title"] or "").strip()
            if len(title) > 56:
                title = title[:53] + "..."

            row_values: list[str] = []
            for ct in content_types:
                text = _text_for(con, item_id=int(it["id"]), content_type=str(ct))
                prompt = analyzer._build_prompt(  # noqa: SLF001
                    title=str(it["title"] or ""),
                    canonical_url=str(it["canonical_url"] or ""),
                    user_topics=list(settings.topics) if settings else [],
                    content=text,
                )
                system_msg = analyzer._build_system_message()  # noqa: SLF001
                tok, warn = _safe_token_counter(
                    model=effective_model,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": prompt},
                    ],
                )
                if warn:
                    warnings.append(warn)
                ms = _markup_stats(text, max_chars=5000)
                row_values.extend([str(tok), str(ms.get("lt_per_1k", 0))])

            table.add_row(str(it["source_item_id"] or ""), title, *row_values)

        console.print(table)
        unique_warnings = list(dict.fromkeys(warnings))[:5]
        if unique_warnings:
            console.print(Panel("\n".join(unique_warnings), title="token_counter warnings (top)", expand=False))
    finally:
        con.close()


@app.command()
def pattern(
    regex: str = typer.Argument(..., help="Regex pattern to count in the excerpt window."),
    content_type: str = typer.Option("html_document_md", help="Which content_type to scan."),
    max_chars: int = typer.Option(5000, help="Scan only the first N chars (matches prompt excerpt window)."),
    bench_dir: Path = typer.Option(Path("bench-out-html-md-v2"), help="Benchmark output directory."),
    db: Path | None = typer.Option(None, help="Optional explicit path to the SQLite DB."),
) -> None:
    """Count a regex across items to spot systematic noise."""
    configure_process_logging(level="INFO", log_json=False)
    console = get_rich_console()
    paths = _resolve_paths(bench_dir=bench_dir, db=db)
    compiled = re.compile(regex)

    con = _open_db(paths.db_path)
    try:
        items_rows = _item_rows(con)
        table = Table(title=f"Pattern counts: /{regex}/ in {content_type} (first {max_chars} chars)")
        table.add_column("arxiv_id", style="bold")
        table.add_column("count", justify="right")
        table.add_column("first_hit", overflow="fold")

        totals = 0
        ranked: list[tuple[int, str, str]] = []
        for it in items_rows:
            text = _text_for(con, item_id=int(it["id"]), content_type=str(content_type))
            window = _excerpt(text, max_chars=max_chars)
            matches = list(compiled.finditer(window))
            cnt = len(matches)
            totals += cnt
            snippet = ""
            if matches:
                m0 = matches[0]
                start = max(0, m0.start() - 40)
                end = min(len(window), m0.end() + 80)
                snippet = window[start:end].replace("\n", "\\n")
            ranked.append((cnt, str(it["source_item_id"] or ""), snippet))

        for cnt, arxiv_id, snippet in sorted(ranked, key=lambda x: (-x[0], x[1])):
            table.add_row(arxiv_id, str(cnt), snippet)
        console.print(table)
        console.print(Panel(f"total_matches={totals}", title="Totals", expand=False))
    finally:
        con.close()


def main() -> None:
    app()


if __name__ == "__main__":
    main()

