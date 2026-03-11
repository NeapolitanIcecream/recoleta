from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import shutil
import subprocess

import pytest
from typer.testing import CliRunner

import recoleta.cli
from recoleta.publish import write_markdown_trend_note
from recoleta.site_deploy import (
    GitHubPagesDeployResult,
    PagesSourceConfigResult,
    deploy_trend_static_site_to_github_pages,
)


def _run_git(*args: str, cwd: Path) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip()


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_creates_branch_snapshot_without_touching_main_worktree(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=301,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-gh-deploy-1",
        overview_md="## TL;DR\n\n- Agent workflows are getting productionized.\n",
        topics=["agents", "tooling"],
        clusters=[],
        highlights=["Agent stacks are stabilizing."],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    remote_repo = tmp_path / "remote.git"
    _run_git("init", "--bare", str(remote_repo), cwd=tmp_path)

    local_repo = tmp_path / "repo"
    local_repo.mkdir(parents=True, exist_ok=True)
    _run_git("init", "-b", "main", cwd=local_repo)
    _run_git("config", "user.name", "Recoleta Tester", cwd=local_repo)
    _run_git("config", "user.email", "tester@example.com", cwd=local_repo)
    (local_repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _run_git("add", "README.md", cwd=local_repo)
    _run_git("commit", "-m", "init", cwd=local_repo)
    _run_git("remote", "add", "origin", str(remote_repo), cwd=local_repo)
    _run_git("push", "-u", "origin", "main", cwd=local_repo)

    result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        commit_message="Deploy Recoleta site",
        cname="research.example.com",
        pages_config_mode="never",
        force=True,
    )

    assert result.skipped is False
    assert result.branch == "gh-pages"
    assert result.trends_total == 1
    assert result.pages_source.status == "skipped"
    assert result.commit_sha

    published = tmp_path / "published"
    _run_git("clone", "--branch", "gh-pages", str(remote_repo), str(published), cwd=tmp_path)
    assert (published / "index.html").exists()
    assert (published / ".nojekyll").exists()
    assert (published / "CNAME").read_text(encoding="utf-8") == "research.example.com\n"
    assert (published / "trends" / f"{trend_note.stem}.html").exists()
    assert not (published / ".github").exists()
    deployed_manifest = json.loads((published / "manifest.json").read_text(encoding="utf-8"))
    assert "generated_at" not in deployed_manifest
    assert "input_dir" not in deployed_manifest
    assert "output_dir" not in deployed_manifest

    assert (local_repo / "README.md").exists()
    assert not (local_repo / "index.html").exists()
    assert _run_git("rev-parse", "--abbrev-ref", "HEAD", cwd=local_repo) == "main"


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_skips_push_when_snapshot_is_unchanged(tmp_path: Path) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=302,
        title="Embodied Systems",
        granularity="day",
        period_start=datetime(2026, 3, 2, tzinfo=UTC),
        period_end=datetime(2026, 3, 3, tzinfo=UTC),
        run_id="run-gh-deploy-2",
        overview_md="## Overview\n\nEmbodied systems are becoming more modular.\n",
        topics=["robotics"],
        clusters=[],
        highlights=["Embodied models are easier to steer."],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    remote_repo = tmp_path / "remote.git"
    _run_git("init", "--bare", str(remote_repo), cwd=tmp_path)

    local_repo = tmp_path / "repo"
    local_repo.mkdir(parents=True, exist_ok=True)
    _run_git("init", "-b", "main", cwd=local_repo)
    _run_git("config", "user.name", "Recoleta Tester", cwd=local_repo)
    _run_git("config", "user.email", "tester@example.com", cwd=local_repo)
    (local_repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _run_git("add", "README.md", cwd=local_repo)
    _run_git("commit", "-m", "init", cwd=local_repo)
    _run_git("remote", "add", "origin", str(remote_repo), cwd=local_repo)
    _run_git("push", "-u", "origin", "main", cwd=local_repo)

    first_result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
    )
    first_head = _run_git("ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path)

    second_result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
    )
    second_head = _run_git("ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path)

    assert first_result.skipped is False
    assert second_result.skipped is True
    assert first_result.commit_sha == second_result.commit_sha
    assert first_head == second_head


@dataclass(slots=True)
class _FakeSettings:
    log_json: bool = False
    markdown_output_dir: Path = Path("/tmp/recoleta-output")
    recoleta_db_path: Path = Path("/tmp/recoleta.db")

    def safe_fingerprint(self) -> str:
        return "fp-gh-deploy"


def test_site_gh_deploy_cli_uses_default_paths_and_prints_summary(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings(
        markdown_output_dir=tmp_path / "output",
        recoleta_db_path=tmp_path / "recoleta.db",
    )
    calls: dict[str, object] = {}

    monkeypatch.setattr(recoleta.cli, "_build_settings", lambda: fake_settings)
    monkeypatch.setattr(
        recoleta.cli,
        "_maybe_acquire_workspace_lease_for_settings",
        lambda **_: (None, None, None, None),
    )

    def _fake_deploy(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        repo_dir,
        remote,
        branch,
        limit=None,
        commit_message=None,
        cname=None,
        pages_config_mode="auto",
        force=True,
    ):
        calls["input_dir"] = input_dir
        calls["repo_dir"] = repo_dir
        calls["remote"] = remote
        calls["branch"] = branch
        calls["limit"] = limit
        calls["commit_message"] = commit_message
        calls["cname"] = cname
        calls["pages_config_mode"] = pages_config_mode
        calls["force"] = force
        return GitHubPagesDeployResult(
            branch=str(branch),
            remote=str(remote),
            remote_url="git@github.com:example/recoleta.git",
            repo_root=Path(repo_dir),
            commit_sha="abcdef1234567890",
            skipped=False,
            trends_total=4,
            topics_total=7,
            streams_total=2,
            files_total=18,
            pages_source=PagesSourceConfigResult(
                status="configured",
                method="gh",
                detail="configured via gh",
                site_url="https://example.github.io/recoleta/",
            ),
        )

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(
        "recoleta.site_deploy.deploy_trend_static_site_to_github_pages",
        _fake_deploy,
    )

    result = runner.invoke(recoleta.cli.app, ["site", "gh-deploy"])

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["repo_dir"] == tmp_path.resolve()
    assert calls["remote"] == "origin"
    assert calls["branch"] == "gh-pages"
    assert calls["pages_config_mode"] == "auto"
    assert calls["force"] is True
    assert "site gh-deploy completed" in result.stdout
    assert "branch=gh-pages" in result.stdout
    assert "https://example.github.io/recoleta/" in result.stdout


def test_site_gh_deploy_cli_with_explicit_input_dir_does_not_require_settings(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}

    def _fail_build_settings():  # type: ignore[no-untyped-def]
        raise AssertionError("settings should not be loaded")

    def _fake_deploy(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        repo_dir,
        remote,
        branch,
        limit=None,
        commit_message=None,
        cname=None,
        pages_config_mode="auto",
        force=True,
    ):
        _ = (remote, branch, limit, commit_message, cname, force)
        calls["input_dir"] = input_dir
        calls["repo_dir"] = repo_dir
        calls["pages_config_mode"] = pages_config_mode
        return GitHubPagesDeployResult(
            branch="gh-pages",
            remote="origin",
            remote_url="git@github.com:example/recoleta.git",
            repo_root=Path(repo_dir),
            commit_sha="abcdef1234567890",
            skipped=True,
            trends_total=1,
            topics_total=2,
            streams_total=0,
            files_total=5,
            pages_source=PagesSourceConfigResult(
                status="skipped",
                method=None,
                detail="pages config disabled",
                site_url=None,
            ),
        )

    input_dir = tmp_path / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(recoleta.cli, "_build_settings", _fail_build_settings)
    monkeypatch.setattr(
        "recoleta.site_deploy.deploy_trend_static_site_to_github_pages",
        _fake_deploy,
    )

    result = runner.invoke(
        recoleta.cli.app,
        [
            "site",
            "gh-deploy",
            "--input-dir",
            str(input_dir),
            "--pages-config",
            "never",
        ],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == input_dir.resolve()
    assert calls["repo_dir"] == Path.cwd().resolve()
    assert calls["pages_config_mode"] == "never"
    assert "no changes" in result.stdout
