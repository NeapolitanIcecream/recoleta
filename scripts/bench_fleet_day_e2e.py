"""Fleet day e2e benchmark harness for one-shot performance investigations.

This script is a DFX tool for controlled measurement and report generation. Its
outputs live under bench-out* and are treated as generated artifacts rather
than part of the product runtime.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

from recoleta.fleet import FleetManifest, load_fleet_manifest


_REPO_ROOT = Path(__file__).resolve().parents[1]
_TIME_LINE_RE = re.compile(r"^(real|user|sys)\s+([0-9]+(?:\.[0-9]+)?)$")
_TIME_COUNTER_RE = re.compile(r"^\s*([0-9]+)\s+(.*?)\s*$")
_STEP_LABELS = {
    "ingest": "prepare (ingest+enrich+triage)",
    "site-build": "site-build",
}


@dataclass(frozen=True, slots=True)
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True, slots=True)
class ChildSummaryRequest:
    instance_name: str
    config_path: Path
    health: dict[str, Any]
    backup: dict[str, Any]
    workflow_payload: dict[str, Any]
    run_payload: dict[str, Any]


@dataclass(frozen=True, slots=True)
class ReportRequest:
    manifest: FleetManifest
    date_token: str
    time_payload: dict[str, Any]
    children: list[dict[str, Any]]
    aggregate_steps: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]


def _run_command(
    argv: list[str],
    *,
    cwd: Path = _REPO_ROOT,
) -> CommandResult:
    completed = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    return CommandResult(
        argv=list(argv),
        returncode=int(completed.returncode),
        stdout=completed.stdout,
        stderr=completed.stderr,
    )


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    _write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _require_success(result: CommandResult, *, context: str) -> None:
    if result.returncode == 0:
        return
    raise RuntimeError(
        f"{context} failed exit_code={result.returncode}\n"
        f"argv={' '.join(result.argv)}\n"
        f"stdout={result.stdout[-4000:]}\n"
        f"stderr={result.stderr[-4000:]}"
    )


def _parse_health_output(text: str) -> dict[str, Any]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    kv: dict[str, str] = {}
    for line in lines[1:]:
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        kv[key.strip()] = value.strip()
    return {
        "ok": (
            kv.get("settings") == "ok"
            and kv.get("paths") == "ok"
            and kv.get("lease") == "free"
        ),
        "settings": kv.get("settings"),
        "paths": kv.get("paths"),
        "lease": kv.get("lease"),
        "schema_version": kv.get("schema_version"),
        "latest_run": kv.get("latest_run"),
        "raw": text,
    }


def _parse_backup_output(text: str) -> dict[str, Any]:
    bundle_match = re.search(r"bundle=(\S+)", text)
    schema_match = re.search(r"schema_version=(\d+)", text)
    return {
        "bundle_dir": bundle_match.group(1) if bundle_match is not None else None,
        "schema_version": int(schema_match.group(1))
        if schema_match is not None
        else None,
        "raw": text,
    }


def _parse_time_output(text: str) -> dict[str, Any]:
    payload: dict[str, Any] = {"raw": text}
    extra: dict[str, int] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        metric_match = _TIME_LINE_RE.match(line)
        if metric_match is not None:
            payload[f"{metric_match.group(1)}_seconds"] = float(metric_match.group(2))
            continue
        counter_match = _TIME_COUNTER_RE.match(raw_line)
        if counter_match is None:
            continue
        key = (
            counter_match.group(2)
            .strip()
            .lower()
            .replace(" ", "_")
            .replace("-", "_")
        )
        extra[key] = int(counter_match.group(1))
    payload["extra_counters"] = extra
    payload["maximum_resident_set_size"] = extra.get("maximum_resident_set_size")
    payload["peak_memory_footprint"] = extra.get("peak_memory_footprint")
    return payload


def _use_bsd_time_wrapper() -> bool:
    return sys.platform == "darwin" and Path("/usr/bin/time").exists()


def _portable_time_output(
    *,
    command_stderr: str,
    real_seconds: float,
    user_seconds: float,
    sys_seconds: float,
) -> str:
    prefix = command_stderr.rstrip()
    timing_lines = [
        f"real {real_seconds:.6f}",
        f"user {user_seconds:.6f}",
        f"sys {sys_seconds:.6f}",
        "timing_mode python_fallback",
    ]
    if prefix:
        return prefix + "\n" + "\n".join(timing_lines) + "\n"
    return "\n".join(timing_lines) + "\n"


def _run_timed_command(
    argv: list[str],
    *,
    cwd: Path = _REPO_ROOT,
) -> tuple[CommandResult, dict[str, Any]]:
    if _use_bsd_time_wrapper():
        result = _run_command(
            ["/usr/bin/time", "-lp", *argv],
            cwd=cwd,
        )
        payload = _parse_time_output(result.stderr)
        payload["timing_mode"] = "bsd_time"
        return result, payload
    started_wall = time.perf_counter()
    started_times = os.times()
    result = _run_command(argv, cwd=cwd)
    finished_times = os.times()
    raw = _portable_time_output(
        command_stderr=result.stderr,
        real_seconds=max(0.0, time.perf_counter() - started_wall),
        user_seconds=max(
            0.0,
            float(finished_times.children_user) - float(started_times.children_user),
        ),
        sys_seconds=max(
            0.0,
            float(finished_times.children_system)
            - float(started_times.children_system),
        ),
    )
    payload = _parse_time_output(raw)
    payload["timing_mode"] = "python_fallback"
    return result, payload


def _load_json_from_mixed_output(raw_text: str) -> Any:
    normalized = str(raw_text or "").strip()
    if not normalized:
        raise ValueError("expected JSON output but stdout was empty")
    try:
        return json.loads(normalized)
    except json.JSONDecodeError:
        pass
    for index, char in enumerate(raw_text):
        if char != "{":
            continue
        candidate = raw_text[index:].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"could not locate JSON object in output: {raw_text[:4000]}")


def _parse_datetime(raw: str | None) -> datetime | None:
    if not raw:
        return None
    return datetime.fromisoformat(raw)


def _wall_duration_ms(*, started_at: str | None, finished_at: str | None, heartbeat_at: str | None) -> int | None:
    started = _parse_datetime(started_at)
    if started is None:
        return None
    ended = _parse_datetime(finished_at) or _parse_datetime(heartbeat_at)
    if ended is None:
        return None
    return max(0, int((ended - started).total_seconds() * 1000))


def _float_metric(metrics: dict[str, Any], name: str) -> float:
    entry = metrics.get(name)
    if not isinstance(entry, dict):
        return 0.0
    value = entry.get("value")
    return float(value) if isinstance(value, (int, float)) else 0.0


def _collect_named_metrics(metrics: dict[str, Any], *, prefix: str, suffix: str) -> dict[str, float]:
    collected: dict[str, float] = {}
    for name, entry in metrics.items():
        if not name.startswith(prefix) or not name.endswith(suffix):
            continue
        if not isinstance(entry, dict):
            continue
        value = entry.get("value")
        if not isinstance(value, (int, float)):
            continue
        token = name[len(prefix) : -len(suffix)]
        collected[token] = float(value)
    return dict(sorted(collected.items(), key=lambda item: (-item[1], item[0])))


def _step_share(duration_ms: int, total_ms: int | None) -> float:
    if total_ms is None or total_ms <= 0:
        return 0.0
    return round((float(duration_ms) / float(total_ms)) * 100.0, 2)


def _roi_label(score_ms: float) -> str:
    if score_ms >= 120000:
        return "high"
    if score_ms >= 30000:
        return "medium"
    return "low"


def _step_label(step_id: str) -> str:
    return _STEP_LABELS.get(step_id, step_id)


def _build_prepare_hotspot(
    *,
    instance: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    ingest_stage_ms = int(_float_metric(metrics, "pipeline.ingest.duration_ms"))
    enrich_ms = int(_float_metric(metrics, "pipeline.enrich.duration_ms"))
    triage_ms = int(_float_metric(metrics, "pipeline.triage.duration_ms"))
    pulls = _collect_named_metrics(
        metrics,
        prefix="pipeline.ingest.source.",
        suffix=".pull_duration_ms",
    )
    fetch_by_source = _collect_named_metrics(
        metrics,
        prefix="pipeline.enrich.source.",
        suffix=".fetch_ms_sum",
    )
    extract_by_source = _collect_named_metrics(
        metrics,
        prefix="pipeline.enrich.source.",
        suffix=".extract_ms_sum",
    )
    top_pull = next(iter(pulls.items()), ("none", 0.0))
    top_fetch = next(iter(fetch_by_source.items()), ("none", 0.0))
    top_extract = next(iter(extract_by_source.items()), ("none", 0.0))
    return {
        "instance": instance,
        "step_id": "ingest",
        "step_label": _step_label("ingest"),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": (
            f"prepare={duration_ms}ms, ingest_stage={ingest_stage_ms}ms, "
            f"enrich_stage={enrich_ms}ms, triage_stage={triage_ms}ms, "
            f"top_pull_source={top_pull[0]}:{int(top_pull[1])}ms, "
            f"top_enrich_fetch={top_fetch[0]}:{int(top_fetch[1])}ms, "
            f"top_enrich_extract={top_extract[0]}:{int(top_extract[1])}ms"
        ),
        "mechanism": (
            "当前 workflow 的 `ingest` step 实际执行 `service.prepare()`，"
            "包含 ingest、enrich、triage 三段；本次样本里纯 ingest pull 只是小头，"
            "真正的大头是 enrich 的远端抓取、正文抽取与落库。"
        ),
        "roi": _roi_label(max(duration_ms, enrich_ms, triage_ms)),
        "details": {
            "ingest_stage_ms": ingest_stage_ms,
            "enrich_ms": enrich_ms,
            "triage_ms": triage_ms,
            "pull_duration_ms_by_source": pulls,
            "fetch_ms_by_source": fetch_by_source,
            "extract_ms_by_source": extract_by_source,
        },
    }


def _build_analyze_hotspot(
    *,
    instance: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    parallelism = int(_float_metric(metrics, "pipeline.analyze.parallelism.effective"))
    max_inflight = int(_float_metric(metrics, "pipeline.analyze.parallelism.max_inflight"))
    processed_total = int(_float_metric(metrics, "pipeline.analyze.processed_total"))
    failed_total = int(_float_metric(metrics, "pipeline.analyze.failed_total"))
    llm_calls = int(_float_metric(metrics, "pipeline.analyze.llm_calls_total"))
    prompt_tokens = int(_float_metric(metrics, "pipeline.analyze.llm_prompt_tokens_total"))
    completion_tokens = int(
        _float_metric(metrics, "pipeline.analyze.llm_completion_tokens_total")
    )
    sql_queries = int(_float_metric(metrics, "pipeline.analyze.db.sql_queries_total"))
    sql_commits = int(_float_metric(metrics, "pipeline.analyze.db.sql_commits_total"))
    return {
        "instance": instance,
        "step_id": "analyze",
        "step_label": _step_label("analyze"),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": (
            f"analyze={duration_ms}ms, llm_calls={llm_calls}, "
            f"prompt_tokens={prompt_tokens}, completion_tokens={completion_tokens}, "
            f"processed={processed_total}, failed={failed_total}, "
            f"parallelism={parallelism}/{max_inflight}, sql_queries={sql_queries}, sql_commits={sql_commits}"
        ),
        "mechanism": (
            "analyze 是独立于 prepare 的并行 LLM 分析 step；当前并发已经开到 8，"
            "所以剩余时长主要由请求总量、prompt 体积和结果落库组成。"
        ),
        "roi": _roi_label(duration_ms),
        "details": {
            "llm_calls_total": llm_calls,
            "llm_prompt_tokens_total": prompt_tokens,
            "llm_completion_tokens_total": completion_tokens,
            "processed_total": processed_total,
            "failed_total": failed_total,
            "parallelism_effective": parallelism,
            "parallelism_max_inflight": max_inflight,
            "sql_queries_total": sql_queries,
            "sql_commits_total": sql_commits,
        },
    }


def _build_trends_hotspot(
    *,
    instance: str,
    step_id: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    generate_ms = int(_float_metric(metrics, "pipeline.trends.generate.duration_ms"))
    overview_ms = int(_float_metric(metrics, "pipeline.trends.overview_pack.duration_ms"))
    history_ms = int(_float_metric(metrics, "pipeline.trends.history.pack.duration_ms"))
    semantic_metrics = {
        name: int(_float_metric(metrics, name))
        for name in (
            "pipeline.trends.semantic_index.item.duration_ms",
            "pipeline.trends.semantic_search.item.duration_ms",
            "pipeline.trends.pass.ideas.semantic_index.trend.duration_ms",
            "pipeline.trends.pass.ideas.semantic_search.trend.duration_ms",
        )
        if _float_metric(metrics, name) > 0
    }
    return {
        "instance": instance,
        "step_id": step_id,
        "step_label": _step_label(step_id),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": (
            f"{step_id}={duration_ms}ms, generate={generate_ms}ms, "
            f"overview_pack={overview_ms}ms, history_pack={history_ms}ms"
        ),
        "mechanism": "trends 慢点主要集中在 agent generation 与语义检索准备，而 overview/history pack 一般不是主瓶颈。",
        "roi": _roi_label(max(duration_ms, generate_ms)),
        "details": {"generate_ms": generate_ms, "semantic_metrics": semantic_metrics},
    }


def _build_ideas_hotspot(
    *,
    instance: str,
    step_id: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    ideas_ms = int(_float_metric(metrics, "pipeline.trends.pass.ideas.duration_ms"))
    tool_calls_total = int(_float_metric(metrics, "pipeline.trends.pass.ideas.tool_calls_total"))
    tool_breakdown = _collect_named_metrics(
        metrics,
        prefix="pipeline.trends.pass.ideas.tool.",
        suffix=".calls_total",
    )
    return {
        "instance": instance,
        "step_id": step_id,
        "step_label": _step_label(step_id),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": f"{step_id}={duration_ms}ms, ideas_pass={ideas_ms}ms, tool_calls_total={tool_calls_total}",
        "mechanism": "ideas 阶段通常由 agent tool loop 主导，工具轮次越多，LLM 往返和检索成本越高。",
        "roi": _roi_label(max(duration_ms, ideas_ms)),
        "details": {"tool_calls_total": tool_calls_total, "tool_breakdown": tool_breakdown},
    }


def _build_translate_hotspot(
    *,
    instance: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    requests_total = int(_float_metric(metrics, "pipeline.translate.llm_requests_total"))
    input_tokens = int(_float_metric(metrics, "pipeline.translate.llm_input_tokens_total"))
    output_tokens = int(_float_metric(metrics, "pipeline.translate.llm_output_tokens_total"))
    return {
        "instance": instance,
        "step_id": "translate",
        "step_label": _step_label("translate"),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": (
            f"translate={duration_ms}ms, llm_requests={requests_total}, "
            f"input_tokens={input_tokens}, output_tokens={output_tokens}"
        ),
        "mechanism": "translate 的时长主要受翻译任务数和串行 LLM 往返影响，增量跳过和任务去重的 ROI 通常很高。",
        "roi": _roi_label(duration_ms),
        "details": {
            "llm_requests_total": requests_total,
            "llm_input_tokens_total": input_tokens,
            "llm_output_tokens_total": output_tokens,
        },
    }


def _build_site_build_hotspot(
    *,
    instance: str,
    duration_ms: int,
    total_duration_ms: int | None,
) -> dict[str, Any]:
    return {
        "instance": instance,
        "step_id": "site-build",
        "step_label": _step_label("site-build"),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": f"site-build={duration_ms}ms",
        "mechanism": "site-build 当前缺少细粒度内部埋点，若时长显著，应优先做 unchanged skip 或增量导出。",
        "roi": _roi_label(duration_ms),
        "details": {},
    }


def _build_hotspot(
    *,
    instance: str,
    step_id: str,
    duration_ms: int,
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    if step_id == "ingest":
        return _build_prepare_hotspot(
            instance=instance,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
            metrics=metrics,
        )
    if step_id == "analyze":
        return _build_analyze_hotspot(
            instance=instance,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
            metrics=metrics,
        )
    if step_id.startswith("trends:"):
        return _build_trends_hotspot(
            instance=instance,
            step_id=step_id,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
            metrics=metrics,
        )
    if step_id.startswith("ideas:"):
        return _build_ideas_hotspot(
            instance=instance,
            step_id=step_id,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
            metrics=metrics,
        )
    if step_id == "translate":
        return _build_translate_hotspot(
            instance=instance,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
            metrics=metrics,
        )
    if step_id == "site-build":
        return _build_site_build_hotspot(
            instance=instance,
            duration_ms=duration_ms,
            total_duration_ms=total_duration_ms,
        )
    return {
        "instance": instance,
        "step_id": step_id,
        "step_label": _step_label(step_id),
        "duration_ms": duration_ms,
        "share_percent": _step_share(duration_ms, total_duration_ms),
        "evidence": f"{step_id}={duration_ms}ms",
        "mechanism": "该 step 没有额外 drill-down 规则。",
        "roi": _roi_label(duration_ms),
        "details": {},
    }


def _build_child_summary(
    request: ChildSummaryRequest,
) -> dict[str, Any]:
    run = request.run_payload["run"]
    metrics = run.get("metrics") or {}
    steps = _workflow_steps_with_labels(request.workflow_payload)
    ranked_steps = _ranked_steps(steps)
    total_duration_ms = _wall_duration_ms(
        started_at=run.get("started_at"),
        finished_at=run.get("finished_at"),
        heartbeat_at=run.get("heartbeat_at"),
    )
    hotspots = _top_hotspots(
        instance=request.instance_name,
        ranked_steps=ranked_steps,
        total_duration_ms=total_duration_ms,
        metrics=metrics,
    )
    return {
        "instance": request.instance_name,
        "config_path": str(request.config_path),
        "run_id": str(run.get("id") or ""),
        "terminal_state": str(run.get("terminal_state") or ""),
        "workflow_status": str(request.workflow_payload.get("status") or ""),
        "health": request.health,
        "backup": request.backup,
        "started_at": run.get("started_at"),
        "finished_at": run.get("finished_at"),
        "heartbeat_at": run.get("heartbeat_at"),
        "total_duration_ms": total_duration_ms,
        "steps": steps,
        "ranked_steps": ranked_steps,
        "hotspots": hotspots,
    }


def _workflow_steps_with_labels(workflow_payload: dict[str, Any]) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    for step in workflow_payload.get("steps") or []:
        if not isinstance(step, dict):
            continue
        step_id = str(step.get("step_id") or "")
        steps.append(
            {
                "step_id": step_id,
                "step_label": _step_label(step_id),
                "status": str(step.get("status") or ""),
                "duration_ms": int(step.get("duration_ms") or 0),
            }
        )
    return steps


def _ranked_steps(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(steps, key=lambda item: (-item["duration_ms"], item["step_id"]))


def _top_hotspots(
    *,
    instance: str,
    ranked_steps: list[dict[str, Any]],
    total_duration_ms: int | None,
    metrics: dict[str, Any],
) -> list[dict[str, Any]]:
    hotspots: list[dict[str, Any]] = []
    for step in ranked_steps[:3]:
        if step["duration_ms"] <= 0:
            continue
        hotspots.append(
            _build_hotspot(
                instance=instance,
                step_id=step["step_id"],
                duration_ms=step["duration_ms"],
                total_duration_ms=total_duration_ms,
                metrics=metrics,
            )
        )
    return hotspots


def _aggregate_step_durations(children: list[dict[str, Any]]) -> list[dict[str, Any]]:
    totals: dict[str, int] = {}
    fleet_total = 0
    for child in children:
        for step in child["steps"]:
            duration_ms = int(step["duration_ms"])
            totals[step["step_id"]] = totals.get(step["step_id"], 0) + duration_ms
            fleet_total += duration_ms
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return [
        {
            "step_id": step_id,
            "step_label": _step_label(step_id),
            "duration_ms": duration_ms,
            "share_percent": _step_share(duration_ms, fleet_total),
        }
        for step_id, duration_ms in ranked
    ]


def _build_recommendations(
    *,
    children: list[dict[str, Any]],
    aggregate_steps: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    aggregate_map = {entry["step_id"]: int(entry["duration_ms"]) for entry in aggregate_steps}
    prepare_evidence: list[str] = []
    for child in children:
        for hotspot in child["hotspots"]:
            if hotspot["step_id"] == "ingest":
                prepare_evidence.append(
                    f"{child['instance']}: {hotspot['evidence']}"
                )
    suggestions = [
        {
            "key": "prepare_enrich_io",
            "title": "优先压缩 prepare 内的 enrich 网络 I/O",
            "score_ms": float(aggregate_map.get("ingest", 0)),
            "evidence": " | ".join(prepare_evidence)
            or "prepare (ingest+enrich+triage) 是 day e2e 的主要热点。",
            "mechanism": (
                "对 HN/RSS/arXiv 内容抓取做增量跳过、失败重试分层与并发上限调优；"
                "对 arXiv html_document 路径优先优化 fetch/cleanup/pandoc，"
                "并减少重复写库。"
            ),
        },
        {
            "key": "translate_incremental",
            "title": "把 translate 变成更强的增量跳过与任务去重",
            "score_ms": float(aggregate_map.get("translate", 0)),
            "evidence": (
                f"aggregate translate={aggregate_map.get('translate', 0)}ms; "
                "历史旧指标 pipeline.translate.duration_ms / 现有累计指标 "
                "pipeline.translate.task_duration_ms_total 都是逐任务累计，"
                "本次以 step wall-time 为准。"
            ),
            "mechanism": (
                "优先跳过 unchanged 输出、按内容哈希去重翻译任务，"
                "必要时再考虑批量 materialize 或更粗粒度的翻译调度。"
            ),
        },
        {
            "key": "rag_loop_trim",
            "title": "收缩 trends/ideas 的 RAG tool loop 与上下文包",
            "score_ms": float(
                sum(
                    aggregate_map.get(step_id, 0)
                    for step_id in aggregate_map
                    if step_id.startswith("trends:") or step_id.startswith("ideas:")
                )
            ),
            "evidence": (
                f"aggregate trends+ideas="
                f"{sum(aggregate_map.get(step_id, 0) for step_id in aggregate_map if step_id.startswith('trends:') or step_id.startswith('ideas:'))}ms"
            ),
            "mechanism": (
                "减少重复 semantic search / get_doc_bundle 轮次，压缩 overview/history/trend snapshot pack，"
                "优先复用已有索引与已筛选证据。"
            ),
        },
        {
            "key": "site_build_incremental",
            "title": "给 site-build 增加 unchanged skip 或增量导出",
            "score_ms": float(aggregate_map.get("site-build", 0)),
            "evidence": f"aggregate site-build={aggregate_map.get('site-build', 0)}ms",
            "mechanism": "若站点构建时长进入前列，应按 manifest/item hash 做 unchanged skip，避免整站重导出。",
        },
    ]
    suggestions.sort(key=lambda item: (-item["score_ms"], item["key"]))
    return [
        {
            "title": suggestion["title"],
            "evidence": suggestion["evidence"],
            "mechanism": suggestion["mechanism"],
            "roi": _roi_label(float(suggestion["score_ms"])),
        }
        for suggestion in suggestions
    ]


def _report_header_lines(
    *,
    manifest: FleetManifest,
    date_token: str,
    fleet_real_seconds: Any,
    max_rss: Any,
    peak_memory: Any,
) -> list[str]:
    return [
        f"# {date_token} Fleet Day E2E 性能报告",
        "",
        "## 执行摘要",
        f"- manifest: `{manifest.manifest_path}`",
        f"- fleet 总 wall time: `{fleet_real_seconds}` 秒"
        if fleet_real_seconds is not None
        else "- fleet 总 wall time: 未解析",
        f"- 最大常驻内存: `{max_rss}`" if max_rss is not None else "- 最大常驻内存: 未解析",
        f"- 峰值内存占用: `{peak_memory}`" if peak_memory is not None else "- 峰值内存占用: 未解析",
        "- fleet 当前按 manifest 顺序串行执行，以下阶段耗时为 3 个 child 串行汇总。",
        "- 当前 workflow 的 `ingest` step 实际调用 `service.prepare()`；本报告统一将其解释为 `prepare (ingest+enrich+triage)`。",
        "",
    ]


def _report_instance_lines(children: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## 实例结果",
        "| instance | run_id | terminal_state | total_ms | top_step | top_step_ms |",
        "| --- | --- | --- | ---: | --- | ---: |",
    ]
    for child in children:
        top_step = (
            child["ranked_steps"][0]
            if child["ranked_steps"]
            else {"step_label": "-", "duration_ms": 0}
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    child["instance"],
                    child["run_id"],
                    child["terminal_state"],
                    str(child["total_duration_ms"] or 0),
                    str(top_step["step_label"]),
                    str(top_step["duration_ms"]),
                ]
            )
            + " |"
        )
    return lines + [""]


def _report_stage_lines(aggregate_steps: list[dict[str, Any]]) -> list[str]:
    lines = [
        "## 阶段排名",
        "| rank | step | total_ms | share_% |",
        "| ---: | --- | ---: | ---: |",
    ]
    for index, step in enumerate(aggregate_steps, start=1):
        lines.append(
            f"| {index} | {step['step_label']} | {step['duration_ms']} | {step['share_percent']} |"
        )
    return lines + ["", "## 热点", ""]


def _report_hotspot_lines(children: list[dict[str, Any]]) -> list[str]:
    lines: list[str] = []
    for child in children:
        lines.append(f"### {child['instance']}")
        if not child["hotspots"]:
            lines.append("- 未发现显著热点。")
            lines.append("")
            continue
        for hotspot in child["hotspots"]:
            lines.append(
                f"- `{hotspot['step_label']}` {hotspot['duration_ms']}ms ({hotspot['share_percent']}%)"
            )
            lines.append(f"  evidence: {hotspot['evidence']}")
            lines.append(f"  mechanism: {hotspot['mechanism']}")
            lines.append(f"  ROI: {hotspot['roi']}")
        lines.append("")
    return lines


def _report_recommendation_lines(recommendations: list[dict[str, Any]]) -> list[str]:
    lines = ["## 改进建议", ""]
    for index, recommendation in enumerate(recommendations, start=1):
        lines.append(f"{index}. {recommendation['title']}")
        lines.append(f"evidence: {recommendation['evidence']}")
        lines.append(f"mechanism: {recommendation['mechanism']}")
        lines.append(f"ROI: {recommendation['roi']}")
        lines.append("")
    return lines


def _report_prior_context_lines() -> list[str]:
    return [
        "## 先验对照",
        "- 历史样本显示 `embodied_ai` 的慢点偏向 HN enrich fetch。",
        "- 历史样本显示 `software_intelligence` 的慢点偏向 arXiv + HN enrich。",
        "- 历史样本中 `analyze`、`trends`、`ideas` 通常位于第二梯队；本次单样本里 `prepare` 与 `translate` 更靠前。",
        "- `pipeline.translate.duration_ms`（历史）和 `pipeline.translate.task_duration_ms_total`（现行）都是逐任务累计，不能直接当 step wall-time；本报告统一使用 workflow step duration。",
        "",
    ]


def _build_report(
    request: ReportRequest,
) -> str:
    fleet_real_seconds = request.time_payload.get("real_seconds")
    max_rss = request.time_payload.get("maximum_resident_set_size")
    peak_memory = request.time_payload.get("peak_memory_footprint")
    lines = _report_header_lines(
        manifest=request.manifest,
        date_token=request.date_token,
        fleet_real_seconds=fleet_real_seconds,
        max_rss=max_rss,
        peak_memory=peak_memory,
    )
    lines.extend(_report_instance_lines(request.children))
    lines.extend(_report_stage_lines(request.aggregate_steps))
    lines.extend(_report_hotspot_lines(request.children))
    lines.extend(_report_recommendation_lines(request.recommendations))
    lines.extend(_report_prior_context_lines())
    return "\n".join(lines).rstrip() + "\n"


def _build_summary(
    *,
    manifest: FleetManifest,
    date_token: str,
    fleet_payload: dict[str, Any],
    time_payload: dict[str, Any],
    children: list[dict[str, Any]],
) -> dict[str, Any]:
    aggregate_steps = _aggregate_step_durations(children)
    recommendations = _build_recommendations(
        children=children,
        aggregate_steps=aggregate_steps,
    )
    return {
        "manifest_path": str(manifest.manifest_path),
        "date": date_token,
        "notes": [
            "Current workflow step `ingest` invokes service.prepare() and therefore includes ingest + enrich + triage.",
            "This report renders that workflow step as `prepare (ingest+enrich+triage)` while preserving the raw step_id `ingest` in JSON.",
        ],
        "fleet": {
            "command": fleet_payload.get("command"),
            "workflow_name": fleet_payload.get("workflow_name"),
            "real_seconds": time_payload.get("real_seconds"),
            "user_seconds": time_payload.get("user_seconds"),
            "sys_seconds": time_payload.get("sys_seconds"),
            "maximum_resident_set_size": time_payload.get("maximum_resident_set_size"),
            "peak_memory_footprint": time_payload.get("peak_memory_footprint"),
        },
        "children": children,
        "aggregate_steps": aggregate_steps,
        "recommendations": recommendations,
    }


def _health_check(instance_name: str, config_path: Path, *, child_dir: Path) -> dict[str, Any]:
    result = _run_command(
        [
            "uv",
            "run",
            "recoleta",
            "inspect",
            "health",
            "--config",
            str(config_path),
        ]
    )
    _write_text(child_dir / "health.txt", result.stdout + result.stderr)
    _require_success(result, context=f"{instance_name} health check")
    health = _parse_health_output(result.stdout)
    if not health["ok"]:
        raise RuntimeError(f"{instance_name} health check failed expectations: {health}")
    return health


def _backup_instance(instance_name: str, config_path: Path, *, child_dir: Path, backup_root: Path) -> dict[str, Any]:
    result = _run_command(
        [
            "uv",
            "run",
            "recoleta",
            "admin",
            "backup",
            "--config",
            str(config_path),
            "--output-dir",
            str(backup_root),
        ]
    )
    _write_text(child_dir / "backup.txt", result.stdout + result.stderr)
    _require_success(result, context=f"{instance_name} backup")
    backup = _parse_backup_output(result.stdout)
    if backup["bundle_dir"] is None:
        raise RuntimeError(f"{instance_name} backup output missing bundle path: {result.stdout}")
    return backup


def _collect_child_run(
    *,
    instance_name: str,
    config_path: Path,
    run_id: str,
    child_dir: Path,
) -> dict[str, Any]:
    result = _run_command(
        [
            "uv",
            "run",
            "recoleta",
            "inspect",
            "runs",
            "show",
            "--config",
            str(config_path),
            "--run-id",
            run_id,
            "--json",
        ]
    )
    _write_text(child_dir / "run.raw.json", result.stdout)
    _require_success(result, context=f"{instance_name} inspect runs show")
    payload = _load_json_from_mixed_output(result.stdout)
    _write_json(child_dir / "run.json", payload)
    return payload


def _run_fleet_day(
    *,
    manifest_path: Path,
    date_token: str,
    output_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result, time_payload = _run_timed_command(
        [
            "uv",
            "run",
            "recoleta",
            "fleet",
            "run",
            "day",
            "--manifest",
            str(manifest_path),
            "--date",
            date_token,
            "--json",
        ]
    )
    _write_text(output_dir / "fleet-run.raw.json", result.stdout)
    _write_text(output_dir / "time.txt", str(time_payload.get("raw") or ""))
    _require_success(result, context="fleet run day")
    fleet_payload = _load_json_from_mixed_output(result.stdout)
    _write_json(output_dir / "fleet-run.json", fleet_payload)
    return fleet_payload, time_payload


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a single fleet day e2e replay with backups and timing."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--date", required=True, help="UTC day token, for example 20260406")
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest_path = Path(args.manifest).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_fleet_manifest(manifest_path)
    child_summaries: list[dict[str, Any]] = []

    for instance in manifest.instances:
        child_dir = output_dir / "children" / instance.name
        child_dir.mkdir(parents=True, exist_ok=True)
        preflight_path = child_dir / "preflight.json"
        if not preflight_path.exists():
            health = _health_check(
                instance.name,
                instance.config_path,
                child_dir=child_dir,
            )
            backup = _backup_instance(
                instance.name,
                instance.config_path,
                child_dir=child_dir,
                backup_root=output_dir / "backups" / instance.name,
            )
            _write_json(preflight_path, {"health": health, "backup": backup})

    fleet_payload, time_payload = _run_fleet_day(
        manifest_path=manifest.manifest_path,
        date_token=str(args.date),
        output_dir=output_dir,
    )

    children_by_name = {instance.name: instance for instance in manifest.instances}
    for child_payload in fleet_payload.get("children") or []:
        if not isinstance(child_payload, dict):
            continue
        instance_name = str(child_payload.get("instance") or "")
        if instance_name not in children_by_name:
            raise RuntimeError(f"Unknown child instance in fleet payload: {instance_name}")
        child_dir = output_dir / "children" / instance_name
        run_id = str(child_payload.get("run_id") or "")
        if not run_id:
            raise RuntimeError(f"Child payload missing run_id: {instance_name}")
        child_run_payload = _collect_child_run(
            instance_name=instance_name,
            config_path=children_by_name[instance_name].config_path,
            run_id=run_id,
            child_dir=child_dir,
        )
        _write_json(child_dir / "workflow.json", child_payload)
        preflight = json.loads((child_dir / "preflight.json").read_text(encoding="utf-8"))
        child_summary = _build_child_summary(
            ChildSummaryRequest(
                instance_name=instance_name,
                config_path=children_by_name[instance_name].config_path,
                health=preflight["health"],
                backup=preflight["backup"],
                workflow_payload=child_payload,
                run_payload=child_run_payload,
            )
        )
        _write_json(child_dir / "summary.json", child_summary)
        child_summaries.append(child_summary)

    child_summaries.sort(key=lambda item: item["instance"])
    summary = _build_summary(
        manifest=manifest,
        date_token=str(args.date),
        fleet_payload=fleet_payload,
        time_payload=time_payload,
        children=child_summaries,
    )
    _write_json(output_dir / "summary.json", summary)
    report = _build_report(
        ReportRequest(
            manifest=manifest,
            date_token=str(args.date),
            time_payload=time_payload,
            children=child_summaries,
            aggregate_steps=summary["aggregate_steps"],
            recommendations=summary["recommendations"],
        )
    )
    _write_text(output_dir / "report.md", report)
    sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
