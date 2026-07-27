from __future__ import annotations

from pathlib import Path

import yaml


def test_manual_publish_builds_the_requested_tag() -> None:
    workflow_path = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / "publish.yml"
    )
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    build_steps = workflow["jobs"]["build"]["steps"]
    checkout_step = next(
        step
        for step in build_steps
        if str(step.get("uses") or "").startswith("actions/checkout@")
    )
    verify_step = next(
        step
        for step in build_steps
        if step.get("name") == "Verify the version and tag"
    )

    assert checkout_step["with"]["ref"] == (
        "${{ github.event_name == 'release' && "
        "github.event.release.tag_name || format('v{0}', inputs.version) }}"
    )
    assert 'CHECKED_OUT_SHA="$(git rev-parse HEAD)"' in verify_step["run"]
    assert '"${CHECKED_OUT_SHA}"' in verify_step["run"]
