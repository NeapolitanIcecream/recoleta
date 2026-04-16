from __future__ import annotations

import json
from pathlib import Path

from scripts import bench_fleet_day_e2e as bench


def test_run_fleet_day_reruns_when_output_dir_already_contains_prior_artifacts(
    tmp_path: Path,
    monkeypatch,
) -> None:
    output_dir = tmp_path / "bench"
    output_dir.mkdir()
    (output_dir / "fleet-run.raw.json").write_text(
        json.dumps({"status": "stale"}),
        encoding="utf-8",
    )
    (output_dir / "time.txt").write_text(
        "real 0.10\n1 maximum resident set size\n",
        encoding="utf-8",
    )
    calls: list[list[str]] = []

    def _run_command(argv, *, cwd=None, env=None):  # type: ignore[no-untyped-def]
        _ = (cwd, env)
        calls.append(list(argv))
        return bench.CommandResult(
            argv=list(argv),
            returncode=0,
            stdout=json.dumps({"status": "fresh", "children": []}),
            stderr="real 1.50\n123 maximum resident set size\n",
        )

    monkeypatch.setattr(bench, "_run_command", _run_command)

    payload, time_payload = bench._run_fleet_day(
        manifest_path=Path("/tmp/fleet.yaml"),
        date_token="20260406",
        output_dir=output_dir,
    )

    assert len(calls) == 1
    assert payload == {"status": "fresh", "children": []}
    assert time_payload["real_seconds"] == 1.5
    assert time_payload["maximum_resident_set_size"] == 123
    assert json.loads((output_dir / "fleet-run.raw.json").read_text(encoding="utf-8")) == payload
    assert json.loads((output_dir / "fleet-run.json").read_text(encoding="utf-8")) == payload
