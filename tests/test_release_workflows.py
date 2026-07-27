from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import yaml


def _workflow(name: str) -> dict[str, Any]:
    workflow_path = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / name
    )
    return yaml.safe_load(workflow_path.read_text(encoding="utf-8"))


def _workflow_steps(name: str) -> list[dict[str, Any]]:
    workflow = _workflow(name)
    return workflow["jobs"]["publish" if name == "container.yml" else "build"][
        "steps"
    ]


def _workflow_events(name: str) -> dict[str, Any]:
    workflow = _workflow(name)
    raw_workflow = cast(dict[Any, Any], workflow)
    return cast(dict[str, Any], raw_workflow.get("on") or raw_workflow[True])


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


def test_manual_container_publish_replays_the_requested_tag() -> None:
    events = _workflow_events("container.yml")
    inputs = events["workflow_dispatch"]["inputs"]
    publish_steps = _workflow_steps("container.yml")
    checkout_step = next(
        step
        for step in publish_steps
        if str(step.get("uses") or "").startswith("actions/checkout@")
    )
    verify_step = next(
        step
        for step in publish_steps
        if step.get("name") == "Verify the release version"
    )
    verify_script = str(verify_step["run"])

    assert inputs["version"]["required"] is True
    assert inputs["update_latest"]["type"] == "boolean"
    assert inputs["update_latest"]["default"] is False
    assert checkout_step["with"]["ref"] == (
        "${{ github.event_name == 'release' && "
        "github.event.release.tag_name || format('v{0}', inputs.version) }}"
    )
    assert verify_step["env"]["REQUESTED_VERSION"] == "${{ inputs.version }}"
    assert 'EXPECTED_TAG="v${REQUESTED_VERSION}"' in verify_script
    assert 'CHECKED_OUT_SHA="$(git rev-parse HEAD)"' in verify_script
    assert '"$(git rev-list -n 1 "${EXPECTED_TAG}")"' in verify_script


def test_container_latest_is_only_emitted_by_the_verified_rule() -> None:
    publish_steps = _workflow_steps("container.yml")
    verify_step = next(
        step
        for step in publish_steps
        if step.get("name") == "Verify the release version"
    )
    metadata_step = next(
        step
        for step in publish_steps
        if str(step.get("uses") or "").startswith("docker/metadata-action@")
    )
    tags = str(metadata_step["with"]["tags"]).splitlines()
    verify_script = str(verify_step["run"])

    assert (
        "type=raw,value=latest,"
        "enable=${{ steps.release.outputs.publish_latest == 'true' }}"
    ) in tags
    assert metadata_step["with"]["flavor"] == "latest=false"
    assert '"${RELEASE_PRERELEASE}" == "false"' in verify_script
    assert '"${UPDATE_LATEST}" == "true"' in verify_script
    assert r"^[0-9]+\.[0-9]+\.[0-9]+$" in verify_script


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
        "${{ github.event_name == 'release' && "
        "github.event.release.tag_name || format('v{0}', inputs.version) }}"
    )
    assert verify_index < login_index < push_index
    assert any(
        str(step.get("uses") or "").startswith("astral-sh/setup-uv@")
        for step in publish_steps[:verify_index]
    )
    assert verify_step["env"]["RELEASE_TAG"] == (
        "${{ github.event.release.tag_name }}"
    )
    assert verify_step["env"]["REQUESTED_VERSION"] == "${{ inputs.version }}"
    assert 'PACKAGE_VERSION="$(uv version --short)"' in verify_script
    assert '"${EXPECTED_TAG}" != "v${PACKAGE_VERSION}"' in verify_script


def test_container_publish_targets_amd64_and_arm64() -> None:
    publish_steps = _workflow_steps("container.yml")
    qemu_index = next(
        index
        for index, step in enumerate(publish_steps)
        if str(step.get("uses") or "").startswith("docker/setup-qemu-action@")
    )
    buildx_index = next(
        index
        for index, step in enumerate(publish_steps)
        if str(step.get("uses") or "").startswith("docker/setup-buildx-action@")
    )
    push_index, push_step = next(
        (index, step)
        for index, step in enumerate(publish_steps)
        if str(step.get("uses") or "").startswith("docker/build-push-action@")
    )
    platforms = {
        value.strip()
        for value in str(push_step["with"]["platforms"]).splitlines()
        if value.strip()
    }

    assert qemu_index < buildx_index < push_index
    assert platforms == {"linux/amd64", "linux/arm64"}
