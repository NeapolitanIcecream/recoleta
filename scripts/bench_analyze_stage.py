from __future__ import annotations

import argparse
import json
import os
import statistics
import tempfile
import threading
import time
from pathlib import Path
from typing import Any, cast

from recoleta.config import Settings
from recoleta.pipeline.service import PipelineService
from recoleta.storage import Repository
from recoleta.types import AnalysisResult, AnalyzeDebug, ItemDraft


class _BenchAnalyzer:
    def __init__(self, *, sleep_ms: int) -> None:
        self.sleep_ms = max(0, int(sleep_ms))
        self._lock = threading.Lock()
        self._active = 0
        self.max_active = 0

    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,  # noqa: ARG002
        include_debug: bool = False,  # noqa: ARG002
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        with self._lock:
            self._active += 1
            self.max_active = max(self.max_active, self._active)
        try:
            if self.sleep_ms > 0:
                time.sleep(self.sleep_ms / 1000.0)
            return (
                AnalysisResult(
                    model="bench/fake-model",
                    provider="bench",
                    summary=f"Summary for {title}",
                    topics=user_topics[:2] or ["general"],
                    relevance_score=0.91,
                    novelty_score=0.44,
                    cost_usd=0.0,
                    latency_ms=self.sleep_ms,
                ),
                None,
            )
        finally:
            with self._lock:
                self._active -= 1


def _configure_env(
    *,
    root: Path,
    max_concurrency: int,
    write_batch_size: int,
) -> None:
    os.environ["RECOLETA_DB_PATH"] = str(root / "recoleta.db")
    os.environ["LLM_MODEL"] = "openai/gpt-4o-mini"
    os.environ["PUBLISH_TARGETS"] = json.dumps(["markdown"])
    os.environ["MARKDOWN_OUTPUT_DIR"] = str(root / "outputs")
    os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"
    os.environ["TRIAGE_ENABLED"] = "false"
    os.environ["TITLE_DEDUP_THRESHOLD"] = "0"
    os.environ["ANALYZE_MAX_CONCURRENCY"] = str(max_concurrency)
    os.environ["ANALYZE_WRITE_BATCH_SIZE"] = str(write_batch_size)
    os.environ["TOPICS"] = json.dumps(["agents", "ml-systems"])


def _seed_items(repository: Repository, *, items: int) -> None:
    for idx in range(items):
        title = (
            f"Adaptive cache invalidation for rover swarms {idx}"
            if idx % 2 == 0
            else f"Genome token routing under sparse supervision {idx}"
        )
        draft = ItemDraft.from_values(
            source="rss",
            source_item_id=f"bench-item-{idx}",
            canonical_url=f"https://example.com/bench-item-{idx}",
            title=title,
            authors=["Bench"],
            raw_metadata={"bench": True},
        )
        item, _ = repository.upsert_item(draft)
        if item.id is None:
            raise RuntimeError("seed item missing id")
        repository.upsert_contents_texts(
            item_id=item.id,
            texts_by_type={
                "html_maintext": (
                    f"Bench content for item {idx}. "
                    f"This paragraph exists to make analyze deterministic. {title}"
                )
            },
        )
        repository.mark_item_enriched(item_id=item.id)


def _run_once(
    *,
    items: int,
    sleep_ms: int,
    max_concurrency: int,
    write_batch_size: int,
    limit: int | None,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="recoleta-bench-analyze-") as tmpdir:
        root = Path(tmpdir)
        _configure_env(
            root=root,
            max_concurrency=max_concurrency,
            write_batch_size=write_batch_size,
        )
        settings = Settings()  # pyright: ignore[reportCallIssue]
        repository = Repository(
            db_path=settings.recoleta_db_path,
            title_dedup_threshold=settings.title_dedup_threshold,
            title_dedup_max_candidates=settings.title_dedup_max_candidates,
        )
        repository.init_schema()
        analyzer = _BenchAnalyzer(sleep_ms=sleep_ms)
        service = PipelineService(
            settings=settings,
            repository=cast(Any, repository),
            analyzer=analyzer,
        )
        _seed_items(repository, items=items)

        run_id = "bench-analyze"
        started = time.perf_counter()
        with repository.sql_diagnostics() as sql_diag:
            result = service.analyze(run_id=run_id, limit=limit or items)
        wall_ms = int((time.perf_counter() - started) * 1000)
        metrics = {
            metric.name: metric.value for metric in repository.list_metrics(run_id=run_id)
        }
        observed_sql_queries_value = metrics.get("pipeline.analyze.db.sql_queries_total")
        observed_sql_queries_total = (
            int(observed_sql_queries_value)
            if observed_sql_queries_value is not None
            else int(sql_diag.queries_total)
        )
        observed_sql_commits_value = metrics.get("pipeline.analyze.db.sql_commits_total")
        observed_sql_commits_total = (
            int(observed_sql_commits_value)
            if observed_sql_commits_value is not None
            else int(sql_diag.commits_total)
        )
        return {
            "wall_ms": wall_ms,
            "processed": result.processed,
            "failed": result.failed,
            "sql_queries_total": sql_diag.queries_total,
            "sql_commits_total": sql_diag.commits_total,
            "observed_sql_queries_total": observed_sql_queries_total,
            "observed_sql_commits_total": observed_sql_commits_total,
            "analyzer_max_active": analyzer.max_active,
            "metrics": metrics,
        }


def _median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a controlled analyze-stage benchmark and print JSON."
    )
    parser.add_argument("--items", type=int, default=8)
    parser.add_argument("--sleep-ms", type=int, default=0)
    parser.add_argument("--max-concurrency", type=int, default=1)
    parser.add_argument("--write-batch-size", type=int, default=32)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()

    runs: list[dict[str, Any]] = [
        _run_once(
            items=args.items,
            sleep_ms=args.sleep_ms,
            max_concurrency=args.max_concurrency,
            write_batch_size=args.write_batch_size,
            limit=args.limit,
        )
        for _ in range(max(1, args.repeats))
    ]
    selected_metric_names = [
        "pipeline.analyze.parallelism.requested",
        "pipeline.analyze.parallelism.effective",
        "pipeline.analyze.parallelism.max_inflight",
        "pipeline.analyze.db.sql_queries_total",
        "pipeline.analyze.db.sql_commits_total",
        "pipeline.analyze.db.analysis_batches_total",
        "pipeline.analyze.db.state_batches_total",
        "pipeline.analyze.processed_total",
        "pipeline.analyze.failed_total",
        "pipeline.analyze.duration_ms",
    ]
    summary_metrics: dict[str, float] = {}
    for name in selected_metric_names:
        values = [
            float(cast(dict[str, float], run["metrics"])[name])
            for run in runs
            if isinstance(run.get("metrics"), dict)
            and name in cast(dict[str, float], run["metrics"])
        ]
        if values:
            summary_metrics[name] = _median(values)

    output = {
        "config": {
            "items": args.items,
            "sleep_ms": args.sleep_ms,
            "max_concurrency": args.max_concurrency,
            "write_batch_size": args.write_batch_size,
            "limit": args.limit or args.items,
            "repeats": max(1, args.repeats),
        },
        "summary": {
            "wall_ms_median": _median([float(run["wall_ms"]) for run in runs]),
            "sql_queries_total_median": _median(
                [float(run["observed_sql_queries_total"]) for run in runs]
            ),
            "sql_commits_total_median": _median(
                [float(run["observed_sql_commits_total"]) for run in runs]
            ),
            "analyzer_max_active_median": _median(
                [float(run["analyzer_max_active"]) for run in runs]
            ),
            "metrics": summary_metrics,
        },
        "runs": runs,
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
