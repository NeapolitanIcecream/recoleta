from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

import recoleta.cli


def test_db_clear_requires_yes(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    db_path.write_text("x", encoding="utf-8")
    result = runner.invoke(recoleta.cli.app, ["db", "clear", "--db-path", str(db_path)])
    assert result.exit_code == 2
    assert "refusing to delete db without --yes" in result.stdout
    assert db_path.exists()


def test_db_clear_deletes_db_and_sidecars(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    sidecars = [
        Path(f"{db_path}-wal"),
        Path(f"{db_path}-shm"),
        Path(f"{db_path}-journal"),
    ]
    db_path.write_text("db", encoding="utf-8")
    for sidecar in sidecars:
        sidecar.write_text("x", encoding="utf-8")

    result = runner.invoke(
        recoleta.cli.app, ["db", "clear", "--db-path", str(db_path), "--yes"]
    )
    assert result.exit_code == 0
    assert not db_path.exists()
    for sidecar in sidecars:
        assert not sidecar.exists()


def test_db_clear_can_resolve_db_path_from_config_file(tmp_path: Path) -> None:
    runner = CliRunner()
    db_path = tmp_path / "recoleta.db"
    db_path.write_text("db", encoding="utf-8")
    config_path = tmp_path / "recoleta.yaml"
    config_path.write_text(
        "\n".join(
            [
                "recoleta_db_path: " + repr(str(db_path)),
                "llm_model: openrouter/openai/gpt-5.2",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        recoleta.cli.app, ["db", "clear", "--config", str(config_path), "--yes"]
    )
    assert result.exit_code == 0
    assert not db_path.exists()
