from __future__ import annotations

import builtins
from datetime import UTC, datetime
import json
from pathlib import Path
import subprocess
import sys
import textwrap
import tomllib
from typing import Any

import pytest
import yaml
from typer.testing import CliRunner

import recoleta.cli
from recoleta.arxiv_pool import (
    ArxivPoolReadinessPolicy,
    ArxivPoolWindow,
    HuldraArxivPoolBackend,
)

HULDRA_DEPENDENCY_MISSING_REASON = "huldra_dependency_missing"


def test_huldra_is_optional_project_dependency() -> None:
    """Regression: default installs must not fetch the Git-hosted Huldra package."""
    metadata = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))

    dependencies = metadata["project"]["dependencies"]
    assert all(not _dependency_names_huldra(dependency) for dependency in dependencies)

    optional_huldra = metadata["project"]["optional-dependencies"]["huldra"]
    assert any(_dependency_names_huldra(dependency) for dependency in optional_huldra)


def test_default_cli_import_and_help_do_not_import_huldra() -> None:
    script = textwrap.dedent(
        """
        import builtins
        import sys
        from typer.testing import CliRunner

        original_import = builtins.__import__

        def guarded_import(name, globals=None, locals=None, fromlist=(), level=0):
            if name == "huldra" or name.startswith("huldra."):
                raise AssertionError(f"unexpected huldra import: {name}")
            return original_import(name, globals, locals, fromlist, level)

        builtins.__import__ = guarded_import

        import recoleta.cli

        result = CliRunner().invoke(recoleta.cli.app, ["--help"])
        assert result.exit_code == 0, result.output
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", script],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr


def test_huldra_readiness_reports_missing_optional_dependency(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _block_huldra_imports(monkeypatch)
    backend = HuldraArxivPoolBackend(base_url="http://127.0.0.1:8765")

    readiness = backend.evaluate_window_readiness(
        _window(),
        readiness_policy=ArxivPoolReadinessPolicy(maturity_lag_days=1),
    )

    assert readiness.cache_status == "failed"
    assert readiness.blocked_reason == HULDRA_DEPENDENCY_MISSING_REASON
    assert readiness.diagnostic is not None
    assert readiness.diagnostic["reason"] == HULDRA_DEPENDENCY_MISSING_REASON


def test_huldra_sync_cli_reports_missing_optional_dependency_as_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _block_huldra_imports(monkeypatch)
    config_path = _write_huldra_pool_config(tmp_path)

    result = CliRunner().invoke(
        recoleta.cli.app,
        [
            "arxiv-pool",
            "sync",
            "--date",
            "2026-05-20",
            "--config",
            str(config_path),
            "--json",
        ],
    )

    assert result.exit_code == 1
    payload = json.loads(result.output)
    assert payload["status"] == "error"
    assert payload["reason"] == HULDRA_DEPENDENCY_MISSING_REASON


def _dependency_names_huldra(dependency: str) -> bool:
    return dependency.strip().lower().startswith("huldra")


def _block_huldra_imports(monkeypatch: pytest.MonkeyPatch) -> None:
    for module_name in list(sys.modules):
        if module_name == "huldra" or module_name.startswith("huldra."):
            monkeypatch.delitem(sys.modules, module_name, raising=False)
    original_import = builtins.__import__

    def blocked_import(
        name: str,
        globals: dict[str, Any] | None = None,
        locals: dict[str, Any] | None = None,
        fromlist: tuple[str, ...] = (),
        level: int = 0,
    ) -> Any:
        if name == "huldra" or name.startswith("huldra."):
            raise ModuleNotFoundError("No module named 'huldra'", name="huldra")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", blocked_import)


def _window() -> ArxivPoolWindow:
    return ArxivPoolWindow(
        query_text="cat:cs.AI",
        period_start=datetime(2026, 5, 20, tzinfo=UTC),
        period_end=datetime(2026, 5, 21, tzinfo=UTC),
        max_results=60,
    )


def _write_huldra_pool_config(tmp_path: Path) -> Path:
    config_path = tmp_path / "huldra-config.yaml"
    config_path.write_text(
        yaml.safe_dump(
            {
                "RECOLETA_DB_PATH": str(tmp_path / "recoleta.db"),
                "LLM_MODEL": "openai/gpt-4o-mini",
                "PUBLISH_TARGETS": ["markdown"],
                "ARXIV_POOL": {
                    "enabled": True,
                    "backend": "huldra",
                    "huldra_base_url": "http://127.0.0.1:8765",
                    "huldra_request_timeout_seconds": 5,
                },
                "SOURCES": {
                    "arxiv": {
                        "enabled": True,
                        "mode": "pool",
                        "queries": ["cat:cs.AI"],
                        "max_results_per_run": 60,
                    }
                },
            }
        ),
        encoding="utf-8",
    )
    return config_path
