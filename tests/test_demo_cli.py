from __future__ import annotations

import json
from pathlib import Path

from bs4 import BeautifulSoup
from typer.testing import CliRunner

from recoleta.cli.app import app


def test_demo_builds_offline_snapshot_without_runtime_configuration(
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
