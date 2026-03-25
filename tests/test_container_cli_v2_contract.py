from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_runtime_dockerfile_defaults_to_v2_daemon_and_healthcheck() -> None:
    """Regression: the published image should default to the CLI v2 daemon contract."""
    dockerfile = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")

    assert 'CMD ["daemon", "start"]' in dockerfile
    assert 'CMD ["recoleta", "inspect", "health", "--healthcheck"]' in dockerfile
    assert 'CMD ["run"]' not in dockerfile
    assert 'CMD ["recoleta", "doctor", "--healthcheck"]' not in dockerfile


def test_cli_v2_migration_guide_marks_run_week_as_broader_replacement() -> None:
    """Regression: the migration guide should warn that `run week` is broader than `trends-week`."""
    guide = (REPO_ROOT / "docs" / "guides" / "cli-v2-migration.md").read_text(
        encoding="utf-8"
    )

    assert "`recoleta trends-week --date 2026-03-16`" in guide
    assert "`recoleta run week --date 2026-03-16`" in guide
    assert "broader end-to-end replacement" in guide
