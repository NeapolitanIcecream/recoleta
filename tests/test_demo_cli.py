from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup
from typer.testing import CliRunner

from recoleta.cli.app import app


def test_demo_builds_bundled_snapshot_without_runtime_configuration(
    tmp_path: Path,
) -> None:
    output_dir = tmp_path / "evaluation"
    result = CliRunner().invoke(
        app,
        ["demo", "--output-dir", str(output_dir), "--json"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert payload["source"] == "bundled-production-fleet-snapshot"
    assert payload["network_calls"] is False
    assert payload["model_calls"] is False
    assert payload["qualified_activation"] is False
    assert payload["manifest"]["trends_total"] == 1
    assert (output_dir / ".recoleta-demo").is_file()
    assert (output_dir / "EVALUATION.md").is_file()

    soup = BeautifulSoup(
        (output_dir / "index.html").read_text(encoding="utf-8"),
        "html.parser",
    )
    assert soup.select_one("h1").get_text(" ", strip=True) == "Notes"  # type: ignore[union-attr]
    assert (
        "Agent evaluation reaches ambiguous projects"
        in soup.select_one(".home-feature-title").get_text(" ", strip=True)  # type: ignore[union-attr]
    )


def test_demo_human_output_scopes_its_network_claim(tmp_path: Path) -> None:
    output_dir = tmp_path / "evaluation"
    result = CliRunner().invoke(
        app,
        ["demo", "--output-dir", str(output_dir)],
    )

    assert result.exit_code == 0, result.output
    assert (
        "Recoleta fetched no sources and made no model or embedding calls."
        in result.stdout
    )
    assert "No network or model calls were made" not in result.stdout


def test_demo_manifest_paths_refer_to_final_snapshot(tmp_path: Path) -> None:
    output_dir = tmp_path / "evaluation"
    result = CliRunner().invoke(
        app,
        ["demo", "--output-dir", str(output_dir), "--json"],
    )

    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    manifest = payload["manifest"]
    persisted_manifest = json.loads(
        (output_dir / "manifest.json").read_text(encoding="utf-8")
    )
    artifacts_dir = output_dir.resolve() / "artifacts"

    assert persisted_manifest == manifest
    assert Path(manifest["output_dir"]) == output_dir.resolve()
    assert Path(manifest["output_dir"]).is_dir()
    assert Path(manifest["input_dir"]) == artifacts_dir
    assert Path(manifest["input_dir"]).is_dir()
    assert manifest["input_dirs"]
    assert all(
        Path(input_entry["path"]) == artifacts_dir
        and Path(input_entry["path"]).is_dir()
        for input_entry in manifest["input_dirs"]
    )


def test_demo_force_only_replaces_a_prior_demo(tmp_path: Path) -> None:
    output_dir = tmp_path / "existing"
    output_dir.mkdir()
    (output_dir / "user-data.txt").write_text("keep", encoding="utf-8")

    result = CliRunner().invoke(
        app,
        ["demo", "--output-dir", str(output_dir), "--force"],
    )

    assert result.exit_code == 2
    assert "Refusing to replace an unmarked directory" in result.stdout
    assert (output_dir / "user-data.txt").read_text(encoding="utf-8") == "keep"
