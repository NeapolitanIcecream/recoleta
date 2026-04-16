"""Shadow benchmark harness for controlled day-run replay experiments.

This script is a DFX tool, not a production execution path. It restores a
backup into a shadow workspace, deletes derived outputs before each replay, and
collects comparable timing artifacts so idempotent reuse is not misread as a
performance win.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import yaml

from recoleta.fleet import FleetManifest, FleetInstance, load_fleet_manifest


_REPO_ROOT = Path(__file__).resolve().parents[1]
_TIME_LINE_RE = re.compile(r"^(real|user|sys)\s+([0-9]+(?:\.[0-9]+)?)$")
_TIME_COUNTER_RE = re.compile(r"^\s*([0-9]+)\s+(.*?)\s*$")


@dataclass(frozen=True, slots=True)
class CommandResult:
    argv: list[str]
    returncode: int
    stdout: str
    stderr: str


@dataclass(frozen=True, slots=True)
class InstanceSummaryRequest:
    instance: FleetInstance
    bundle_dir: Path
    run_payload: dict[str, Any]
    inspect_payload: dict[str, Any]
    time_payload: dict[str, Any]
    shadow_config: Path


def _run_command(
    argv: list[str],
    *,
    cwd: Path = _REPO_ROOT,
    extra_env: dict[str, str] | None = None,
) -> CommandResult:
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    completed = subprocess.run(
        argv,
        cwd=str(cwd),
        env=env,
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
    extra_env: dict[str, str] | None = None,
) -> tuple[CommandResult, dict[str, Any]]:
    if _use_bsd_time_wrapper():
        result = _run_command(
            ["/usr/bin/time", "-lp", *argv],
            cwd=cwd,
            extra_env=extra_env,
        )
        payload = _parse_time_output(result.stderr)
        payload["timing_mode"] = "bsd_time"
        return result, payload
    started_wall = time.perf_counter()
    started_times = os.times()
    result = _run_command(argv, cwd=cwd, extra_env=extra_env)
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


def _selected_instances(
    *,
    manifest: FleetManifest,
    names: list[str],
) -> list[FleetInstance]:
    if not names:
        return list(manifest.instances)
    wanted = {name.strip() for name in names if name.strip()}
    by_name = {instance.name: instance for instance in manifest.instances}
    missing = sorted(wanted - set(by_name))
    if missing:
        raise ValueError(f"unknown instance name(s): {', '.join(missing)}")
    return [by_name[name] for name in sorted(wanted)]


def _latest_backup_bundle(*, backup_root: Path, instance_name: str) -> Path:
    instance_root = backup_root / instance_name
    bundles = sorted(
        path for path in instance_root.iterdir() if path.is_dir() and path.name.startswith("recoleta-backup-")
    )
    if not bundles:
        raise FileNotFoundError(f"no backup bundle found for {instance_name} under {instance_root}")
    return bundles[-1]


def _shadow_config_payload(*, source_config: Path, shadow_root: Path) -> dict[str, Any]:
    payload = yaml.safe_load(source_config.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"config must contain a mapping: {source_config}")
    payload = dict(payload)
    payload["recoleta_db_path"] = str(shadow_root / "recoleta.db")
    payload["markdown_output_dir"] = str(shadow_root / "outputs")
    payload["rag_lancedb_dir"] = str(shadow_root / "lancedb")
    if "artifacts_dir" in payload or bool(payload.get("write_debug_artifacts")):
        payload["artifacts_dir"] = str(shadow_root / "artifacts")
    if "obsidian_vault_path" in payload:
        payload["obsidian_vault_path"] = str(shadow_root / "obsidian")
    return payload


def _reset_shadow_workspace(*, shadow_root: Path) -> None:
    for name in ("recoleta.db", "outputs", "lancedb", "artifacts", "obsidian"):
        path = shadow_root / name
        if path.is_dir():
            shutil.rmtree(path)
        elif path.exists():
            path.unlink()


def _restore_shadow_db(*, bundle_dir: Path, shadow_config: Path, instance_dir: Path) -> None:
    result = _run_command(
        [
            "uv",
            "run",
            "recoleta",
            "admin",
            "restore",
            "--bundle",
            str(bundle_dir),
            "--yes",
        ],
        extra_env={"RECOLETA_CONFIG_PATH": str(shadow_config)},
    )
    _write_text(instance_dir / "restore.txt", result.stdout + result.stderr)
    _require_success(result, context="shadow restore")


def _run_day_once(*, shadow_config: Path, date_token: str, instance_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    result, time_payload = _run_timed_command(
        [
            "uv",
            "run",
            "recoleta",
            "run",
            "day",
            "--date",
            date_token,
            "--json",
        ],
        extra_env={"RECOLETA_CONFIG_PATH": str(shadow_config)},
    )
    _write_text(instance_dir / "run.raw.json", result.stdout)
    _write_text(instance_dir / "time.txt", str(time_payload.get("raw") or ""))
    _require_success(result, context="shadow run day")
    payload = _load_json_from_mixed_output(result.stdout)
    _write_json(instance_dir / "run.json", payload)
    return payload, time_payload


def _inspect_run(*, shadow_config: Path, run_id: str, instance_dir: Path) -> dict[str, Any]:
    result = _run_command(
        [
            "uv",
            "run",
            "recoleta",
            "inspect",
            "runs",
            "show",
            "--run-id",
            run_id,
            "--json",
        ],
        extra_env={"RECOLETA_CONFIG_PATH": str(shadow_config)},
    )
    _write_text(instance_dir / "inspect.raw.json", result.stdout)
    _require_success(result, context="inspect run")
    payload = _load_json_from_mixed_output(result.stdout)
    _write_json(instance_dir / "inspect.json", payload)
    return payload


def _workflow_step_payloads(run_payload: dict[str, Any]) -> list[dict[str, Any]]:
    steps: list[dict[str, Any]] = []
    for step in run_payload.get("steps") or []:
        if not isinstance(step, dict):
            continue
        steps.append(
            {
                "step_id": str(step.get("step_id") or ""),
                "status": str(step.get("status") or ""),
                "duration_ms": int(step.get("duration_ms") or 0),
            }
        )
    return steps


def _ranked_step_payloads(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(steps, key=lambda item: (-item["duration_ms"], item["step_id"]))


def _instance_metadata(
    *,
    instance: FleetInstance,
    bundle_dir: Path,
    shadow_config: Path,
    run_payload: dict[str, Any],
    time_payload: dict[str, Any],
) -> dict[str, Any]:
    return {
        "instance": instance.name,
        "source_config_path": str(instance.config_path),
        "shadow_config_path": str(shadow_config),
        "bundle_dir": str(bundle_dir),
        "time": time_payload,
        "run_id": str(run_payload.get("run_id") or ""),
        "terminal_state": str(run_payload.get("terminal_state") or ""),
        "executed_steps": list(run_payload.get("executed_steps") or []),
    }


def _instance_summary(
    request: InstanceSummaryRequest,
) -> dict[str, Any]:
    metrics = ((request.inspect_payload.get("run") or {}).get("metrics") or {})
    steps = _workflow_step_payloads(request.run_payload)
    return {
        **_instance_metadata(
            instance=request.instance,
            bundle_dir=request.bundle_dir,
            shadow_config=request.shadow_config,
            run_payload=request.run_payload,
            time_payload=request.time_payload,
        ),
        "steps": steps,
        "ranked_steps": _ranked_step_payloads(steps),
        "metrics": metrics,
    }


def _aggregate(children: list[dict[str, Any]]) -> dict[str, Any]:
    step_totals: dict[str, int] = {}
    real_seconds_total = 0.0
    for child in children:
        real_seconds_total += float((child.get("time") or {}).get("real_seconds") or 0.0)
        for step in child.get("steps") or []:
            step_id = str(step.get("step_id") or "")
            step_totals[step_id] = step_totals.get(step_id, 0) + int(step.get("duration_ms") or 0)
    ranked_steps = sorted(step_totals.items(), key=lambda item: (-item[1], item[0]))
    return {
        "real_seconds_total": round(real_seconds_total, 2),
        "step_totals": [
            {"step_id": step_id, "duration_ms": duration_ms}
            for step_id, duration_ms in ranked_steps
        ],
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a day workflow on restored shadow instances to benchmark code changes."
    )
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--backup-root", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument(
        "--instances",
        default="",
        help="Comma-separated instance names. Defaults to every instance in the manifest.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    manifest = load_fleet_manifest(Path(args.manifest).expanduser().resolve())
    backup_root = Path(args.backup_root).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    children: list[dict[str, Any]] = []
    instance_names = [token.strip() for token in str(args.instances or "").split(",") if token.strip()]
    for instance in _selected_instances(manifest=manifest, names=instance_names):
        instance_dir = output_dir / "instances" / instance.name
        shadow_root = instance_dir / "shadow"
        shadow_root.mkdir(parents=True, exist_ok=True)
        bundle_dir = _latest_backup_bundle(backup_root=backup_root, instance_name=instance.name)
        shadow_config_payload = _shadow_config_payload(
            source_config=instance.config_path,
            shadow_root=shadow_root,
        )
        shadow_config = instance_dir / "recoleta.shadow.yaml"
        _write_text(shadow_config, yaml.safe_dump(shadow_config_payload, sort_keys=False))
        _reset_shadow_workspace(shadow_root=shadow_root)
        _restore_shadow_db(
            bundle_dir=bundle_dir,
            shadow_config=shadow_config,
            instance_dir=instance_dir,
        )
        run_payload, time_payload = _run_day_once(
            shadow_config=shadow_config,
            date_token=str(args.date),
            instance_dir=instance_dir,
        )
        run_id = str(run_payload.get("run_id") or "")
        if not run_id:
            raise RuntimeError(f"missing run_id in run payload for {instance.name}")
        inspect_payload = _inspect_run(
            shadow_config=shadow_config,
            run_id=run_id,
            instance_dir=instance_dir,
        )
        summary = _instance_summary(
            InstanceSummaryRequest(
                instance=instance,
                bundle_dir=bundle_dir,
                run_payload=run_payload,
                inspect_payload=inspect_payload,
                time_payload=time_payload,
                shadow_config=shadow_config,
            )
        )
        _write_json(instance_dir / "summary.json", summary)
        children.append(summary)

    children.sort(key=lambda item: item["instance"])
    summary = {
        "manifest_path": str(manifest.manifest_path),
        "date": str(args.date),
        "children": children,
        "aggregate": _aggregate(children),
    }
    _write_json(output_dir / "summary.json", summary)
    sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
