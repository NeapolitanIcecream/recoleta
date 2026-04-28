"""Compare two shadow day-run benchmark outputs and render deltas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, cast


_METRIC_PREFIXES = (
    "pipeline.workflow.step.",
    "pipeline.ingest.",
    "pipeline.enrich.",
    "pipeline.site_build.",
    "pipeline.triage.",
    "pipeline.analyze.",
    "pipeline.trends.",
    "pipeline.translate.",
)

_WORKLOAD_COMPARABILITY_METRICS = (
    "pipeline.ingest.source.arxiv.in_window_total",
    "pipeline.ingest.source.arxiv.inserted_total",
    "pipeline.ingest.source.arxiv.pull_failed_total",
    "pipeline.enrich.source.arxiv.processed_total",
    "pipeline.enrich.source.arxiv.content_chars_sum",
    "pipeline.enrich.source.hn.content_chars_sum",
    "pipeline.translate.scanned_total",
    "pipeline.translate.translated_total",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _write_json(path: Path, payload: Any) -> None:
    _write_text(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def _normalize_metric_value(raw: Any) -> float:
    if isinstance(raw, dict):
        value = raw.get("value")
        return float(value) if isinstance(value, (int, float)) else 0.0
    return float(raw) if isinstance(raw, (int, float)) else 0.0


def _duration_delta_payload(*, baseline: float, candidate: float) -> dict[str, float]:
    improvement_pct = 0.0
    if baseline > 0:
        improvement_pct = round(((baseline - candidate) / baseline) * 100.0, 2)
    return {
        "baseline": round(baseline, 2),
        "candidate": round(candidate, 2),
        "delta": round(candidate - baseline, 2),
        "improvement_pct": improvement_pct,
    }


def _metric_delta_payload(*, baseline: float, candidate: float) -> dict[str, float]:
    return {
        "baseline": round(baseline, 2),
        "candidate": round(candidate, 2),
        "delta": round(candidate - baseline, 2),
    }


def _step_totals(steps: list[dict[str, Any]]) -> dict[str, int]:
    totals: dict[str, int] = {}
    for step in steps:
        step_id = str(step.get("step_id") or "").strip()
        if not step_id:
            continue
        totals[step_id] = totals.get(step_id, 0) + int(step.get("duration_ms") or 0)
    return totals


def _selected_metric_names(
    baseline_metrics: dict[str, float],
    candidate_metrics: dict[str, float],
) -> list[str]:
    names = {
        name
        for name in set(baseline_metrics) | set(candidate_metrics)
        if name.startswith(_METRIC_PREFIXES)
    }
    return sorted(names)


def _billing_total_usd(entry: Any) -> float:
    if not isinstance(entry, dict):
        return 0.0
    value = entry.get("total_cost_usd")
    return float(value) if isinstance(value, (int, float)) else 0.0


def _dict_value(payload: dict[str, Any], key: str) -> dict[str, Any]:
    value = payload.get(key)
    return value if isinstance(value, dict) else {}


def _metric_values(raw_metrics: Any) -> dict[str, float]:
    metrics = raw_metrics if isinstance(raw_metrics, dict) else {}
    return {
        str(name): _normalize_metric_value(entry)
        for name, entry in metrics.items()
    }


def _child_steps(raw_child: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        step
        for step in raw_child.get("steps") or []
        if isinstance(step, dict)
    ]


def _run_payload(root: Path, instance: str) -> dict[str, Any]:
    inspect_path = root / "instances" / instance / "inspect.json"
    inspect_payload = _load_json(inspect_path) if inspect_path.exists() else {}
    return _dict_value(inspect_payload, "run") if isinstance(inspect_payload, dict) else {}


def _billing_by_step(root: Path, instance: str) -> dict[str, Any]:
    billing = _run_payload(root, instance).get("billing_by_step")
    return billing if isinstance(billing, dict) else {}


def _load_child_summary(root: Path, raw_child: dict[str, Any]) -> tuple[str, dict[str, Any]] | None:
    instance = str(raw_child.get("instance") or "").strip()
    if not instance:
        return None
    child_steps = _child_steps(raw_child)
    time_payload = _dict_value(raw_child, "time")
    return instance, {
        "instance": instance,
        "terminal_state": str(raw_child.get("terminal_state") or ""),
        "real_seconds": float(time_payload.get("real_seconds") or 0.0),
        "steps": child_steps,
        "step_totals": _step_totals(child_steps),
        "total_duration_ms": sum(
            int(step.get("duration_ms") or 0) for step in child_steps
        ),
        "metrics": _metric_values(raw_child.get("metrics")),
        "billing_by_step": _billing_by_step(root, instance),
    }


def _load_children(root: Path, summary: dict[str, Any]) -> dict[str, dict[str, Any]]:
    children: dict[str, dict[str, Any]] = {}
    for raw_child in summary.get("children") or []:
        if not isinstance(raw_child, dict):
            continue
        child_summary = _load_child_summary(root, raw_child)
        if child_summary is None:
            continue
        instance, payload = child_summary
        children[instance] = payload
    return children


def _load_shadow_summary(root: Path) -> dict[str, Any]:
    summary = _load_json(root / "summary.json")
    if not isinstance(summary, dict):
        summary = {}
    return {
        "manifest_path": str(summary.get("manifest_path") or ""),
        "date": str(summary.get("date") or ""),
        "aggregate": _dict_value(summary, "aggregate"),
        "children": _load_children(root, summary),
    }


def _aggregate_step_delta(
    baseline_aggregate: dict[str, Any],
    candidate_aggregate: dict[str, Any],
) -> dict[str, dict[str, float | int]]:
    baseline_steps = {
        str(step.get("step_id") or ""): int(step.get("duration_ms") or 0)
        for step in baseline_aggregate.get("step_totals") or []
        if isinstance(step, dict)
    }
    candidate_steps = {
        str(step.get("step_id") or ""): int(step.get("duration_ms") or 0)
        for step in candidate_aggregate.get("step_totals") or []
        if isinstance(step, dict)
    }
    payload: dict[str, dict[str, float | int]] = {}
    for step_id in sorted(set(baseline_steps) | set(candidate_steps)):
        baseline_ms = int(baseline_steps.get(step_id, 0))
        candidate_ms = int(candidate_steps.get(step_id, 0))
        payload[step_id] = {
            "baseline_ms": baseline_ms,
            "candidate_ms": candidate_ms,
            "delta_ms": candidate_ms - baseline_ms,
            "improvement_pct": _duration_delta_payload(
                baseline=float(baseline_ms),
                candidate=float(candidate_ms),
            )["improvement_pct"],
        }
    return payload


def _child_delta(
    *,
    instance: str,
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, Any]:
    baseline_metrics = _child_metrics(baseline)
    candidate_metrics = _child_metrics(candidate)
    return {
        "instance": instance,
        "terminal_state": _terminal_state_delta(baseline, candidate),
        "real_seconds": _duration_delta_payload(
            baseline=float(baseline.get("real_seconds") or 0.0),
            candidate=float(candidate.get("real_seconds") or 0.0),
        ),
        "total_duration_ms": _total_duration_delta(baseline, candidate),
        "steps": _step_deltas(baseline, candidate),
        "metrics": _metric_deltas(baseline_metrics, candidate_metrics),
        "billing_by_step": _billing_deltas(baseline, candidate),
    }


def _child_metrics(child: dict[str, Any]) -> dict[str, float]:
    return (
        cast(dict[str, float], child.get("metrics"))
        if isinstance(child.get("metrics"), dict)
        else {}
    )


def _terminal_state_delta(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, str]:
    return {
        "baseline": str(baseline.get("terminal_state") or ""),
        "candidate": str(candidate.get("terminal_state") or ""),
    }


def _total_duration_delta(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, float | int]:
    baseline_ms = int(baseline.get("total_duration_ms") or 0)
    candidate_ms = int(candidate.get("total_duration_ms") or 0)
    return {
        "baseline": baseline_ms,
        "candidate": candidate_ms,
        "delta": candidate_ms - baseline_ms,
        "improvement_pct": _duration_delta_payload(
            baseline=float(baseline_ms),
            candidate=float(candidate_ms),
        )["improvement_pct"],
    }


def _step_deltas(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, dict[str, float | int]]:
    baseline_steps = _dict_value(baseline, "step_totals")
    candidate_steps = _dict_value(candidate, "step_totals")
    return {
        step_id: _step_delta(
            baseline_ms=int(baseline_steps.get(step_id, 0)),
            candidate_ms=int(candidate_steps.get(step_id, 0)),
        )
        for step_id in sorted(set(baseline_steps) | set(candidate_steps))
    }


def _step_delta(*, baseline_ms: int, candidate_ms: int) -> dict[str, float | int]:
    return {
        "baseline_ms": baseline_ms,
        "candidate_ms": candidate_ms,
        "delta_ms": candidate_ms - baseline_ms,
        "improvement_pct": _duration_delta_payload(
            baseline=float(baseline_ms),
            candidate=float(candidate_ms),
        )["improvement_pct"],
    }


def _metric_deltas(
    baseline_metrics: dict[str, float],
    candidate_metrics: dict[str, float],
) -> dict[str, dict[str, float]]:
    metric_names = _selected_metric_names(
        baseline_metrics=baseline_metrics,
        candidate_metrics=candidate_metrics,
    )
    return {
        metric_name: _metric_delta_payload(
            baseline=float(baseline_metrics.get(metric_name, 0.0)),
            candidate=float(candidate_metrics.get(metric_name, 0.0)),
        )
        for metric_name in metric_names
    }


def _billing_deltas(
    baseline: dict[str, Any],
    candidate: dict[str, Any],
) -> dict[str, dict[str, float]]:
    baseline_billing = _dict_value(baseline, "billing_by_step")
    candidate_billing = _dict_value(candidate, "billing_by_step")
    return {
        step_id: _billing_delta(
            baseline_billing.get(step_id),
            candidate_billing.get(step_id),
        )
        for step_id in sorted(set(baseline_billing) | set(candidate_billing))
    }


def _billing_delta(baseline_entry: Any, candidate_entry: Any) -> dict[str, float]:
    baseline_usd = _billing_total_usd(baseline_entry)
    candidate_usd = _billing_total_usd(candidate_entry)
    return {
        "baseline_usd": round(baseline_usd, 6),
        "candidate_usd": round(candidate_usd, 6),
        "delta_usd": round(candidate_usd - baseline_usd, 6),
    }


def _top_changed_steps(steps: dict[str, Any], *, limit: int = 5) -> list[tuple[str, dict[str, Any]]]:
    return sorted(
        steps.items(),
        key=lambda item: (-abs(int(item[1]["delta_ms"])), item[0]),
    )[:limit]


def _top_changed_metrics(
    metrics: dict[str, Any],
    *,
    limit: int = 8,
) -> list[tuple[str, dict[str, Any]]]:
    return sorted(
        metrics.items(),
        key=lambda item: (-abs(float(item[1]["delta"])), item[0]),
    )[:limit]


def _workload_warning_reason(metric_name: str, *, baseline: float, candidate: float) -> str | None:
    if baseline == candidate:
        return None
    delta = candidate - baseline
    if metric_name.endswith("_chars_sum"):
        if baseline <= 0.0 or abs(delta) / baseline >= 0.02:
            return "content workload changed"
        return None
    if abs(delta) >= 1.0:
        return "count workload changed"
    return None


def _workload_comparability_warnings(children: dict[str, Any]) -> list[dict[str, Any]]:
    warnings: list[dict[str, Any]] = []
    for instance, child in sorted(children.items()):
        metrics = child.get("metrics") if isinstance(child.get("metrics"), dict) else {}
        for metric_name in _WORKLOAD_COMPARABILITY_METRICS:
            payload = metrics.get(metric_name)
            if not isinstance(payload, dict):
                continue
            baseline = float(payload.get("baseline") or 0.0)
            candidate = float(payload.get("candidate") or 0.0)
            reason = _workload_warning_reason(
                metric_name,
                baseline=baseline,
                candidate=candidate,
            )
            if reason is None:
                continue
            warnings.append(
                {
                    "instance": instance,
                    "metric": metric_name,
                    "baseline": round(baseline, 2),
                    "candidate": round(candidate, 2),
                    "delta": round(candidate - baseline, 2),
                    "reason": reason,
                }
            )
    return warnings


def _render_report(comparison: dict[str, Any]) -> str:
    lines = [
        *_render_report_header(comparison),
        *_render_aggregate_steps(comparison["aggregate_steps"]),
        *_render_workload_warnings(
            comparison.get("workload_comparability_warnings") or []
        ),
    ]
    for instance, child in comparison["children"].items():
        lines.extend(_render_child_report(instance, child))
    return "\n".join(lines).rstrip() + "\n"


def _render_report_header(comparison: dict[str, Any]) -> list[str]:
    fleet = comparison["fleet"]["real_seconds_total"]
    return [
        "# Shadow Day Run Comparison",
        "",
        f"- baseline: `{comparison['baseline_dir']}`",
        f"- candidate: `{comparison['candidate_dir']}`",
        f"- date: `{comparison['date']}`",
        f"- manifest: `{comparison['manifest_path']}`",
        (
            "- fleet wall time: "
            f"`{fleet['baseline']}s -> {fleet['candidate']}s` "
            f"(delta `{fleet['delta']}s`, improvement `{fleet['improvement_pct']}%`)"
        ),
        "",
    ]


def _render_aggregate_steps(aggregate_steps: dict[str, Any]) -> list[str]:
    lines = [
        "## Aggregate Steps",
        "| step | baseline_ms | candidate_ms | delta_ms | improvement_% |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for step_id, payload in aggregate_steps.items():
        lines.append(
            f"| {step_id} | {payload['baseline_ms']} | {payload['candidate_ms']} | {payload['delta_ms']} | {payload['improvement_pct']} |"
        )
    return lines


def _render_workload_warnings(workload_warnings: list[dict[str, Any]]) -> list[str]:
    lines = ["", "## Workload Comparability Warnings"]
    if workload_warnings:
        lines.append(
            "Treat wall-time deltas as non-comparable until these source workload differences are explained."
        )
        for warning in workload_warnings:
            lines.append(
                f"- `{warning['instance']}` `{warning['metric']}`: "
                f"{warning['baseline']} -> {warning['candidate']} "
                f"(delta {warning['delta']}; {warning['reason']})"
            )
    else:
        lines.append("- none")
    return lines


def _render_child_report(instance: str, child: dict[str, Any]) -> list[str]:
    lines = [
        "",
        f"## {instance}",
        _render_child_total_duration(child),
        _render_child_terminal_state(child),
        "",
        "### Top Step Deltas",
    ]
    lines.extend(_render_top_step_deltas(child["steps"]))
    lines.extend(_render_top_metric_deltas(child["metrics"]))
    lines.extend(_render_billing_deltas(child["billing_by_step"]))
    return lines


def _render_child_total_duration(child: dict[str, Any]) -> str:
    total = child["total_duration_ms"]
    return (
        "- total_duration_ms: "
        f"`{total['baseline']} -> {total['candidate']}` "
        f"(delta `{total['delta']}`, improvement `{total['improvement_pct']}%`)"
    )


def _render_child_terminal_state(child: dict[str, Any]) -> str:
    state = child["terminal_state"]
    return f"- terminal_state: `{state['baseline']} -> {state['candidate']}`"


def _render_top_step_deltas(steps: dict[str, Any]) -> list[str]:
    return [
        (
            f"- `{step_id}`: {payload['baseline_ms']} -> {payload['candidate_ms']} ms "
            f"(delta {payload['delta_ms']} ms, improvement {payload['improvement_pct']}%)"
        )
        for step_id, payload in _top_changed_steps(steps)
    ]


def _render_top_metric_deltas(metrics: dict[str, Any]) -> list[str]:
    if not metrics:
        return []
    lines = ["", "### Top Metric Deltas"]
    for metric_name, payload in _top_changed_metrics(metrics):
        lines.append(
            f"- `{metric_name}`: {payload['baseline']} -> {payload['candidate']} "
            f"(delta {payload['delta']})"
        )
    return lines


def _render_billing_deltas(billing_by_step: dict[str, Any]) -> list[str]:
    if not billing_by_step:
        return []
    lines = ["", "### Billing By Step"]
    for step_id, payload in sorted(billing_by_step.items()):
        lines.append(
            f"- `{step_id}`: {payload['baseline_usd']} -> {payload['candidate_usd']} usd "
            f"(delta {payload['delta_usd']} usd)"
        )
    return lines


def _build_comparison(*, baseline_dir: Path, candidate_dir: Path) -> dict[str, Any]:
    baseline = _load_shadow_summary(baseline_dir)
    candidate = _load_shadow_summary(candidate_dir)
    child_names = sorted(set(baseline["children"]) | set(candidate["children"]))
    children = {
        instance: _child_delta(
            instance=instance,
            baseline=(
                baseline["children"].get(instance)
                if isinstance(baseline["children"].get(instance), dict)
                else {}
            ),
            candidate=(
                candidate["children"].get(instance)
                if isinstance(candidate["children"].get(instance), dict)
                else {}
            ),
        )
        for instance in child_names
    }
    return {
        "baseline_dir": str(baseline_dir),
        "candidate_dir": str(candidate_dir),
        "manifest_path": baseline["manifest_path"] or candidate["manifest_path"],
        "date": baseline["date"] or candidate["date"],
        "fleet": {
            "real_seconds_total": _duration_delta_payload(
                baseline=float((baseline["aggregate"].get("real_seconds_total") or 0.0)),
                candidate=float((candidate["aggregate"].get("real_seconds_total") or 0.0)),
            )
        },
        "aggregate_steps": _aggregate_step_delta(
            baseline_aggregate=baseline["aggregate"],
            candidate_aggregate=candidate["aggregate"],
        ),
        "workload_comparability_warnings": _workload_comparability_warnings(children),
        "children": children,
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare two shadow day-run benchmark outputs and render deltas."
    )
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    baseline_dir = Path(args.baseline).expanduser().resolve()
    candidate_dir = Path(args.candidate).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    comparison = _build_comparison(
        baseline_dir=baseline_dir,
        candidate_dir=candidate_dir,
    )
    _write_json(output_dir / "delta.json", comparison)
    _write_text(output_dir / "report.md", _render_report(comparison))
    print(json.dumps(comparison, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
