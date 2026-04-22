"""Compare two shadow day-run benchmark outputs and render deltas."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


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


def _load_shadow_summary(root: Path) -> dict[str, Any]:
    summary = _load_json(root / "summary.json")
    children: dict[str, dict[str, Any]] = {}
    for raw_child in summary.get("children") or []:
        if not isinstance(raw_child, dict):
            continue
        instance = str(raw_child.get("instance") or "").strip()
        if not instance:
            continue
        metrics = raw_child.get("metrics") or {}
        if not isinstance(metrics, dict):
            metrics = {}
        inspect_path = root / "instances" / instance / "inspect.json"
        inspect_payload = _load_json(inspect_path) if inspect_path.exists() else {}
        run_payload = inspect_payload.get("run") if isinstance(inspect_payload, dict) else {}
        if not isinstance(run_payload, dict):
            run_payload = {}
        child_steps = list(raw_child.get("steps") or [])
        children[instance] = {
            "instance": instance,
            "terminal_state": str(raw_child.get("terminal_state") or ""),
            "real_seconds": float(
                ((raw_child.get("time") or {}).get("real_seconds") or 0.0)
            ),
            "steps": child_steps,
            "step_totals": _step_totals(child_steps),
            "total_duration_ms": sum(
                int(step.get("duration_ms") or 0) for step in child_steps
            ),
            "metrics": {
                name: _normalize_metric_value(entry)
                for name, entry in metrics.items()
            },
            "billing_by_step": (
                run_payload.get("billing_by_step")
                if isinstance(run_payload.get("billing_by_step"), dict)
                else {}
            ),
        }
    aggregate = summary.get("aggregate")
    return {
        "manifest_path": str(summary.get("manifest_path") or ""),
        "date": str(summary.get("date") or ""),
        "aggregate": aggregate if isinstance(aggregate, dict) else {},
        "children": children,
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
    baseline_metrics = (
        baseline.get("metrics") if isinstance(baseline.get("metrics"), dict) else {}
    )
    candidate_metrics = (
        candidate.get("metrics") if isinstance(candidate.get("metrics"), dict) else {}
    )
    metric_names = _selected_metric_names(
        baseline_metrics=baseline_metrics,
        candidate_metrics=candidate_metrics,
    )
    step_ids = sorted(
        set(baseline.get("step_totals") or {}) | set(candidate.get("step_totals") or {})
    )
    billing_step_ids = sorted(
        set(baseline.get("billing_by_step") or {})
        | set(candidate.get("billing_by_step") or {})
    )
    return {
        "instance": instance,
        "terminal_state": {
            "baseline": str(baseline.get("terminal_state") or ""),
            "candidate": str(candidate.get("terminal_state") or ""),
        },
        "real_seconds": _duration_delta_payload(
            baseline=float(baseline.get("real_seconds") or 0.0),
            candidate=float(candidate.get("real_seconds") or 0.0),
        ),
        "total_duration_ms": {
            "baseline": int(baseline.get("total_duration_ms") or 0),
            "candidate": int(candidate.get("total_duration_ms") or 0),
            "delta": int(candidate.get("total_duration_ms") or 0)
            - int(baseline.get("total_duration_ms") or 0),
            "improvement_pct": _duration_delta_payload(
                baseline=float(baseline.get("total_duration_ms") or 0),
                candidate=float(candidate.get("total_duration_ms") or 0),
            )["improvement_pct"],
        },
        "steps": {
            step_id: {
                "baseline_ms": int((baseline.get("step_totals") or {}).get(step_id, 0)),
                "candidate_ms": int((candidate.get("step_totals") or {}).get(step_id, 0)),
                "delta_ms": int((candidate.get("step_totals") or {}).get(step_id, 0))
                - int((baseline.get("step_totals") or {}).get(step_id, 0)),
                "improvement_pct": _duration_delta_payload(
                    baseline=float((baseline.get("step_totals") or {}).get(step_id, 0)),
                    candidate=float((candidate.get("step_totals") or {}).get(step_id, 0)),
                )["improvement_pct"],
            }
            for step_id in step_ids
        },
        "metrics": {
            metric_name: _metric_delta_payload(
                baseline=float(baseline_metrics.get(metric_name, 0.0)),
                candidate=float(candidate_metrics.get(metric_name, 0.0)),
            )
            for metric_name in metric_names
        },
        "billing_by_step": {
            step_id: {
                "baseline_usd": round(
                    _billing_total_usd((baseline.get("billing_by_step") or {}).get(step_id)),
                    6,
                ),
                "candidate_usd": round(
                    _billing_total_usd((candidate.get("billing_by_step") or {}).get(step_id)),
                    6,
                ),
                "delta_usd": round(
                    _billing_total_usd((candidate.get("billing_by_step") or {}).get(step_id))
                    - _billing_total_usd((baseline.get("billing_by_step") or {}).get(step_id)),
                    6,
                ),
            }
            for step_id in billing_step_ids
        },
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


def _render_report(comparison: dict[str, Any]) -> str:
    fleet = comparison["fleet"]["real_seconds_total"]
    lines = [
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
        "## Aggregate Steps",
        "| step | baseline_ms | candidate_ms | delta_ms | improvement_% |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for step_id, payload in comparison["aggregate_steps"].items():
        lines.append(
            f"| {step_id} | {payload['baseline_ms']} | {payload['candidate_ms']} | {payload['delta_ms']} | {payload['improvement_pct']} |"
        )
    for instance, child in comparison["children"].items():
        lines.extend(
            [
                "",
                f"## {instance}",
                (
                    "- total_duration_ms: "
                    f"`{child['total_duration_ms']['baseline']} -> {child['total_duration_ms']['candidate']}` "
                    f"(delta `{child['total_duration_ms']['delta']}`, "
                    f"improvement `{child['total_duration_ms']['improvement_pct']}%`)"
                ),
                (
                    "- terminal_state: "
                    f"`{child['terminal_state']['baseline']} -> {child['terminal_state']['candidate']}`"
                ),
                "",
                "### Top Step Deltas",
            ]
        )
        for step_id, payload in _top_changed_steps(child["steps"]):
            lines.append(
                f"- `{step_id}`: {payload['baseline_ms']} -> {payload['candidate_ms']} ms "
                f"(delta {payload['delta_ms']} ms, improvement {payload['improvement_pct']}%)"
            )
        if child["metrics"]:
            lines.extend(["", "### Top Metric Deltas"])
            for metric_name, payload in _top_changed_metrics(child["metrics"]):
                lines.append(
                    f"- `{metric_name}`: {payload['baseline']} -> {payload['candidate']} "
                    f"(delta {payload['delta']})"
                )
        if child["billing_by_step"]:
            lines.extend(["", "### Billing By Step"])
            for step_id, payload in sorted(child["billing_by_step"].items()):
                lines.append(
                    f"- `{step_id}`: {payload['baseline_usd']} -> {payload['candidate_usd']} usd "
                    f"(delta {payload['delta_usd']} usd)"
                )
    return "\n".join(lines).rstrip() + "\n"


def _build_comparison(*, baseline_dir: Path, candidate_dir: Path) -> dict[str, Any]:
    baseline = _load_shadow_summary(baseline_dir)
    candidate = _load_shadow_summary(candidate_dir)
    child_names = sorted(set(baseline["children"]) | set(candidate["children"]))
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
        "children": {
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
        },
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
