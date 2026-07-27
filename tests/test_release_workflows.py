from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _workflow_steps(name: str) -> list[dict[str, Any]]:
    workflow_path = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / name
    )
    workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
    return workflow["jobs"]["publish" if name == "container.yml" else "build"][
        "steps"
    ]


def test_manual_publish_builds_the_requested_tag() -> None:
    build_steps = _workflow_steps("publish.yml")
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


def test_prerelease_container_does_not_update_latest() -> None:
    publish_steps = _workflow_steps("container.yml")
    metadata_step = next(
        step
        for step in publish_steps
        if str(step.get("uses") or "").startswith("docker/metadata-action@")
    )
    tags = str(metadata_step["with"]["tags"]).splitlines()

    assert (
        "type=raw,value=latest,"
        "enable=${{ github.event.release.prerelease == false }}"
    ) in tags


def test_container_release_tag_matches_package_version_before_push() -> None:
    publish_steps = _workflow_steps("container.yml")
    checkout_step = next(
        step
        for step in publish_steps
        if str(step.get("uses") or "").startswith("actions/checkout@")
    )
    verify_index, verify_step = next(
        (index, step)
        for index, step in enumerate(publish_steps)
        if step.get("name") == "Verify the release version"
    )
    login_index = next(
        index
        for index, step in enumerate(publish_steps)
        if str(step.get("uses") or "").startswith("docker/login-action@")
    )
    push_index = next(
        index
        for index, step in enumerate(publish_steps)
        if step.get("with", {}).get("push") is True
    )
    verify_script = str(verify_step["run"])

    assert checkout_step["with"]["ref"] == (
        "${{ github.event.release.tag_name }}"
    )
    assert verify_index < login_index < push_index
    assert any(
        str(step.get("uses") or "").startswith("astral-sh/setup-uv@")
        for step in publish_steps[:verify_index]
    )
    assert verify_step["env"]["RELEASE_TAG"] == (
        "${{ github.event.release.tag_name }}"
    )
    assert 'PACKAGE_VERSION="$(uv version --short)"' in verify_script
    assert '"${RELEASE_TAG}" != "v${PACKAGE_VERSION}"' in verify_script
