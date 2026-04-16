from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

from scripts import bench_shadow_day_run as bench


def test_run_day_once_uses_portable_timing_when_bsd_time_is_unavailable(
    tmp_path: Path,
    monkeypatch,
) -> None:
    instance_dir = tmp_path / "instance"
    instance_dir.mkdir()
    calls: list[tuple[list[str], dict[str, str] | None]] = []
    timer_samples = iter([20.0, 21.25])
    cpu_samples = iter(
        [
            SimpleNamespace(children_user=1.0, children_system=0.25),
            SimpleNamespace(children_user=1.6, children_system=0.5),
        ]
    )

    def _run_command(  # type: ignore[no-untyped-def]
        argv,
        *,
        cwd=None,
        extra_env=None,
    ):
        _ = cwd
        calls.append((list(argv), extra_env))
        return bench.CommandResult(
            argv=list(argv),
            returncode=0,
            stdout=json.dumps({"run_id": "run-1", "steps": []}),
            stderr="shadow stderr\n",
        )

    monkeypatch.setattr(bench, "_run_command", _run_command)
    monkeypatch.setattr(bench, "_use_bsd_time_wrapper", lambda: False)
    monkeypatch.setattr(bench.time, "perf_counter", lambda: next(timer_samples))
    monkeypatch.setattr(bench.os, "times", lambda: next(cpu_samples))

    payload, time_payload = bench._run_day_once(
        shadow_config=Path("/tmp/recoleta.shadow.yaml"),
        date_token="20260406",
        instance_dir=instance_dir,
    )

    assert payload == {"run_id": "run-1", "steps": []}
    assert len(calls) == 1
    assert calls[0][0][:4] == ["uv", "run", "recoleta", "run"]
    assert calls[0][1] == {"RECOLETA_CONFIG_PATH": "/tmp/recoleta.shadow.yaml"}
    assert time_payload["real_seconds"] == 1.25
    assert time_payload["user_seconds"] == 0.6
    assert time_payload["sys_seconds"] == 0.25
    assert time_payload["maximum_resident_set_size"] is None
    assert "timing_mode python_fallback" in (instance_dir / "time.txt").read_text(
        encoding="utf-8"
    )
