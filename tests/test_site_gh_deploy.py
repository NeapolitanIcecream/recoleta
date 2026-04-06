from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import shutil
import subprocess
from types import SimpleNamespace
from typing import Any

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.site_deploy as site_deploy
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
    _run_git(
        "clone", "--branch", "gh-pages", str(remote_repo), str(published), cwd=tmp_path
    )
    assert (published / "index.html").exists()
    assert (published / ".nojekyll").exists()
    assert (published / "CNAME").read_text(encoding="utf-8") == "research.example.com\n"
    assert (published / "trends" / f"{trend_note.stem}.html").exists()
    assert not (published / ".github").exists()
    deployed_manifest = json.loads(
        (published / "manifest.json").read_text(encoding="utf-8")
    )
    assert "generated_at" not in deployed_manifest
    assert "input_dir" not in deployed_manifest
    assert "output_dir" not in deployed_manifest

    assert (local_repo / "README.md").exists()
    assert not (local_repo / "index.html").exists()
    assert _run_git("rev-parse", "--abbrev-ref", "HEAD", cwd=local_repo) == "main"


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_preserves_multilingual_manifest_metadata(tmp_path: Path) -> None:
    notes_root = tmp_path / "notes"
    write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=401,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-gh-deploy-multilang-en",
        overview_md="## Overview\n\nEnglish note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=notes_root / "Localized" / "zh-cn",
        trend_doc_id=401,
        title="智能体系统",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-gh-deploy-multilang-zh",
        overview_md="## Overview\n\n中文笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

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
        input_dir=notes_root,
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
        default_language_code="en",
    )

    assert result.skipped is False
    published = tmp_path / "published"
    _run_git(
        "clone", "--branch", "gh-pages", str(remote_repo), str(published), cwd=tmp_path
    )
    deployed_manifest = json.loads(
        (published / "manifest.json").read_text(encoding="utf-8")
    )
    assert deployed_manifest["languages"] == ["en", "zh-cn"]
    assert deployed_manifest["default_language_code"] == "en"
    assert deployed_manifest["language_codes"] == {"en": "en", "zh-cn": "zh-CN"}


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_skips_push_when_multilingual_snapshot_is_unchanged(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=402,
        title="Agent Systems",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-gh-deploy-multilang-skip-en",
        overview_md="## Overview\n\nEnglish note.\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="en",
    )
    write_markdown_trend_note(
        output_dir=notes_root / "Localized" / "zh-cn",
        trend_doc_id=402,
        title="智能体系统",
        granularity="day",
        period_start=datetime(2026, 3, 1, tzinfo=UTC),
        period_end=datetime(2026, 3, 2, tzinfo=UTC),
        run_id="run-gh-deploy-multilang-skip-zh",
        overview_md="## Overview\n\n中文笔记。\n",
        topics=["agents"],
        clusters=[],
        highlights=[],
        language_code="zh-CN",
    )

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
        input_dir=notes_root,
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
        default_language_code="en",
    )
    first_head = _run_git(
        "ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path
    )

    second_result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root,
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
        default_language_code="en",
    )
    second_head = _run_git(
        "ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path
    )

    assert first_result.skipped is False
    assert second_result.skipped is True
    assert first_result.commit_sha == second_result.commit_sha
    assert first_head == second_head


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
    first_head = _run_git(
        "ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path
    )

    second_result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
    )
    second_head = _run_git(
        "ls-remote", "--heads", str(remote_repo), "gh-pages", cwd=tmp_path
    )

    assert first_result.skipped is False
    assert second_result.skipped is True
    assert first_result.commit_sha == second_result.commit_sha
    assert first_head == second_head


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_uses_best_effort_tempdir_cleanup(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    notes_root = tmp_path / "notes"
    write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=304,
        title="Cleanup Safety",
        granularity="day",
        period_start=datetime(2026, 3, 5, tzinfo=UTC),
        period_end=datetime(2026, 3, 6, tzinfo=UTC),
        run_id="run-gh-deploy-4",
        overview_md="## Overview\n\nCleanup should not fail the deploy.\n",
        topics=["deploy"],
        clusters=[],
        highlights=["Temporary checkout cleanup is best effort."],
    )

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

    real_temporary_directory = site_deploy.tempfile.TemporaryDirectory
    captured_cleanup_flags: list[bool] = []

    def _temporary_directory(*args, **kwargs):  # type: ignore[no-untyped-def]
        captured_cleanup_flags.append(bool(kwargs.get("ignore_cleanup_errors")))
        return real_temporary_directory(*args, **kwargs)

    monkeypatch.setattr(
        site_deploy.tempfile, "TemporaryDirectory", _temporary_directory
    )

    result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
    )

    assert result.skipped is False
    assert captured_cleanup_flags == [True, True]


@pytest.mark.skipif(shutil.which("git") is None, reason="git is required")
def test_gh_deploy_prefers_push_url_when_remote_endpoints_diverge(
    tmp_path: Path,
) -> None:
    notes_root = tmp_path / "notes"
    trend_note = write_markdown_trend_note(
        output_dir=notes_root,
        trend_doc_id=303,
        title="Push URL Deploy",
        granularity="day",
        period_start=datetime(2026, 3, 3, tzinfo=UTC),
        period_end=datetime(2026, 3, 4, tzinfo=UTC),
        run_id="run-gh-deploy-3",
        overview_md="## Overview\n\nDeployment should use the push remote.\n",
        topics=["git"],
        clusters=[],
        highlights=["Push URLs may differ from fetch URLs."],
    )
    trend_note.with_suffix(".pdf").write_bytes(b"%PDF-1.7\n")

    push_remote_repo = tmp_path / "push-remote.git"
    _run_git("init", "--bare", str(push_remote_repo), cwd=tmp_path)

    local_repo = tmp_path / "repo"
    local_repo.mkdir(parents=True, exist_ok=True)
    _run_git("init", "-b", "main", cwd=local_repo)
    _run_git("config", "user.name", "Recoleta Tester", cwd=local_repo)
    _run_git("config", "user.email", "tester@example.com", cwd=local_repo)
    (local_repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _run_git("add", "README.md", cwd=local_repo)
    _run_git("commit", "-m", "init", cwd=local_repo)
    _run_git(
        "remote",
        "add",
        "origin",
        str(tmp_path / "fetch-remote-does-not-exist.git"),
        cwd=local_repo,
    )
    _run_git(
        "remote", "set-url", "--push", "origin", str(push_remote_repo), cwd=local_repo
    )

    result = deploy_trend_static_site_to_github_pages(
        input_dir=notes_root / "Trends",
        repo_dir=local_repo,
        remote="origin",
        branch="gh-pages",
        pages_config_mode="never",
        force=True,
    )

    assert result.skipped is False
    assert Path(result.remote_url) == push_remote_repo.resolve()

    published = tmp_path / "published"
    _run_git(
        "clone",
        "--branch",
        "gh-pages",
        str(push_remote_repo),
        str(published),
        cwd=tmp_path,
    )
    assert (published / "trends" / f"{trend_note.stem}.html").exists()


def test_gh_deploy_forwards_explicit_item_export_scope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: gh deploy must preserve the explicit full item export override."""
    captured: dict[str, object] = {}
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(
        site_deploy, "_resolve_git_repo_root", lambda repo_root: repo_root
    )
    monkeypatch.setattr(
        site_deploy,
        "_resolve_git_remote",
        lambda *, repo_root, remote_name: SimpleNamespace(  # noqa: ARG005
            name=remote_name,
            url="https://example.com/recoleta.git",
        ),
    )

    def _fake_export_trend_static_site(  # type: ignore[no-untyped-def]
        *,
        input_dir,
        output_dir,
        limit=None,
        default_language_code=None,
        item_export_scope="linked",
    ):
        captured.update(
            {
                "input_dir": input_dir,
                "output_dir": output_dir,
                "limit": limit,
                "default_language_code": default_language_code,
                "item_export_scope": item_export_scope,
            }
        )
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "index.html").write_text("site\n", encoding="utf-8")
        manifest_path = output_dir / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "trends_total": 1,
                    "topics_total": 2,
                    "items_total": 3,
                    "item_export_scope": item_export_scope,
                }
            ),
            encoding="utf-8",
        )
        return manifest_path

    monkeypatch.setattr(
        site_deploy,
        "export_trend_static_site",
        _fake_export_trend_static_site,
    )
    monkeypatch.setattr(
        site_deploy,
        "_sanitize_public_manifests",
        lambda *, site_dir: {"trends_total": 1, "topics_total": 2},
    )
    monkeypatch.setattr(site_deploy, "_write_cname", lambda **_: None)
    monkeypatch.setattr(site_deploy, "_ensure_no_symlinks", lambda *_: None)
    monkeypatch.setattr(
        site_deploy,
        "_publish_site_snapshot",
        lambda **_: ("deadbeef", False),
    )
    monkeypatch.setattr(
        site_deploy,
        "_configure_pages_source",
        lambda **_: PagesSourceConfigResult(
            status="skipped",
            method=None,
            detail="pages config disabled",
            site_url=None,
        ),
    )

    result = deploy_trend_static_site_to_github_pages(
        input_dir=tmp_path / "notes" / "Trends",
        repo_dir=repo_dir,
        pages_config_mode="never",
        item_export_scope="all",
    )

    assert result.skipped is False
    assert captured["item_export_scope"] == "all"


@dataclass(slots=True)
class _FakeSettings:
    log_json: bool = False
    markdown_output_dir: Path = Path("/tmp/recoleta-output")
    recoleta_db_path: Path = Path("/tmp/recoleta.db")
    localization: object | None = None
    workflows: object | None = None

    def safe_fingerprint(self) -> str:
        return "fp-gh-deploy"

    def localization_target_codes(self) -> list[str]:
        if self.localization is None:
            return []
        return [
            str(getattr(target, "code", "") or "")
            for target in getattr(self.localization, "targets", [])
        ]


class _FakeRepo:
    def __init__(self) -> None:
        self.updated: list[dict[str, object]] = []
        self.finished: list[tuple[str, bool, str | None]] = []

    def update_run_context(self, **kwargs: object) -> None:
        self.updated.append(dict(kwargs))

    def finish_run(
        self,
        run_id: str,
        *,
        success: bool,
        terminal_state: str | None = None,
    ) -> None:
        self.finished.append((run_id, bool(success), terminal_state))

    def list_metrics(self, *, run_id: str) -> list[object]:
        _ = run_id
        return []


class _FakeHeartbeatMonitor:
    def raise_if_failed(self) -> None:
        return None

    def stop(self) -> None:
        return None


class _FakeConsole:
    def __init__(self) -> None:
        self.lines: list[str] = []

    def print(self, *parts: object) -> None:
        self.lines.append(" ".join(str(part) for part in parts))


class _FakeLog:
    def exception(self, *_: object, **__: object) -> None:
        return None

    def warning(self, *_: object, **__: object) -> None:
        return None


def _install_deploy_runtime(
    monkeypatch: pytest.MonkeyPatch,
    *,
    settings: _FakeSettings,
    repository: _FakeRepo,
    import_symbol_override,
) -> _FakeConsole:
    console = _FakeConsole()
    monkeypatch.setattr(
        recoleta.cli,
        "_begin_managed_run",
        lambda *, command, log_module: (  # noqa: ARG005
            settings,
            repository,
            object(),
            console,
            "run-deploy-1",
            "owner-1",
            _FakeLog(),
            _FakeHeartbeatMonitor(),
        ),
    )
    monkeypatch.setattr(recoleta.cli, "_cleanup_managed_run", lambda **_: None)
    original_import_symbol = recoleta.cli._import_symbol

    def _fake_import_symbol(module_name: str, *, attr_name: str | None = None):
        override = import_symbol_override(module_name, attr_name)
        if override is not None:
            return override
        return original_import_symbol(module_name, attr_name=attr_name)

    monkeypatch.setattr(recoleta.cli, "_import_symbol", _fake_import_symbol)
    return console


def test_run_deploy_cli_uses_default_paths_and_prints_summary(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings(
        markdown_output_dir=tmp_path / "output",
        recoleta_db_path=tmp_path / "recoleta.db",
    )
    fake_settings.localization = SimpleNamespace(
        targets=[], site_default_language_code="en"
    )
    fake_settings.workflows = SimpleNamespace(
        deploy=SimpleNamespace(
            translation="auto",
            translate_include=["items", "trends", "ideas"],
            site_build=True,
            on_translate_failure="partial_success",
        )
    )
    calls: dict[str, Any] = {}

    monkeypatch.chdir(tmp_path)

    def _override(module_name: str, attr_name: str | None):
        if module_name == "recoleta.site" and attr_name == "export_trend_static_site":

            def _fake_site_build(
                *, input_dir, output_dir, default_language_code=None, limit=None
            ):  # type: ignore[no-untyped-def]
                calls.setdefault("site_build", []).append(
                    (input_dir, output_dir, default_language_code, limit)
                )
                manifest_path = Path(output_dir) / "manifest.json"
                manifest_path.parent.mkdir(parents=True, exist_ok=True)
                manifest_path.write_text(
                    '{"trends_total": 4, "ideas_total": 4, "topics_total": 7}',
                    encoding="utf-8",
                )
                return manifest_path

            return _fake_site_build
        if (
            module_name == "recoleta.site_deploy"
            and attr_name == "deploy_trend_static_site_to_github_pages"
        ):

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
                default_language_code=None,
            ):
                calls.update(
                    {
                        "input_dir": input_dir,
                        "repo_dir": repo_dir,
                        "remote": remote,
                        "branch": branch,
                        "limit": limit,
                        "commit_message": commit_message,
                        "cname": cname,
                        "pages_config_mode": pages_config_mode,
                        "force": force,
                        "default_language_code": default_language_code,
                    }
                )
                return GitHubPagesDeployResult(
                    branch=str(branch),
                    remote=str(remote),
                    remote_url="git@github.com:example/recoleta.git",
                    repo_root=Path(repo_dir),
                    commit_sha="abcdef1234567890",
                    skipped=False,
                    trends_total=4,
                    topics_total=7,
                    files_total=18,
                    pages_source=PagesSourceConfigResult(
                        status="configured",
                        method="gh",
                        detail="configured via gh",
                        site_url="https://example.github.io/recoleta/",
                    ),
                )

            return _fake_deploy
        return None

    _install_deploy_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=_FakeRepo(),
        import_symbol_override=_override,
    )

    result = runner.invoke(recoleta.cli.app, ["run", "deploy"])

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["repo_dir"] == tmp_path.resolve()
    assert calls["remote"] == "origin"
    assert calls["branch"] == "gh-pages"
    assert calls["pages_config_mode"] == "auto"
    assert calls["force"] is True
    assert calls["default_language_code"] == "en"


def test_run_deploy_cli_passes_repo_dir_and_pages_config(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    calls: dict[str, object] = {}
    fake_settings = _FakeSettings(
        markdown_output_dir=tmp_path / "output",
        recoleta_db_path=tmp_path / "recoleta.db",
        workflows=SimpleNamespace(
            deploy=SimpleNamespace(
                translation="off",
                translate_include=["items", "trends", "ideas"],
                site_build=False,
                on_translate_failure="partial_success",
            )
        ),
    )

    def _override(module_name: str, attr_name: str | None):
        if (
            module_name == "recoleta.site_deploy"
            and attr_name == "deploy_trend_static_site_to_github_pages"
        ):

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
                default_language_code=None,
            ):
                _ = (remote, branch, limit, commit_message, cname, force)
                calls.update(
                    {
                        "input_dir": input_dir,
                        "repo_dir": repo_dir,
                        "pages_config_mode": pages_config_mode,
                        "default_language_code": default_language_code,
                    }
                )
                return GitHubPagesDeployResult(
                    branch="gh-pages",
                    remote="origin",
                    remote_url="git@github.com:example/recoleta.git",
                    repo_root=Path(repo_dir),
                    commit_sha="abcdef1234567890",
                    skipped=True,
                    trends_total=1,
                    topics_total=2,
                    files_total=5,
                    pages_source=PagesSourceConfigResult(
                        status="skipped",
                        method=None,
                        detail="pages config disabled",
                        site_url=None,
                    ),
                )

            return _fake_deploy
        return None

    _install_deploy_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=_FakeRepo(),
        import_symbol_override=_override,
    )
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir(parents=True, exist_ok=True)

    result = runner.invoke(
        recoleta.cli.app,
        [
            "run",
            "deploy",
            "--repo-dir",
            str(repo_dir),
            "--pages-config",
            "never",
        ],
    )

    assert result.exit_code == 0
    assert calls["input_dir"] == fake_settings.markdown_output_dir / "Trends"
    assert calls["repo_dir"] == repo_dir.resolve()
    assert calls["pages_config_mode"] == "never"
    assert calls["default_language_code"] is None


def test_run_deploy_cli_emits_json_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    fake_settings = _FakeSettings(
        markdown_output_dir=tmp_path / "output",
        recoleta_db_path=tmp_path / "recoleta.db",
    )
    fake_settings.workflows = SimpleNamespace(
        deploy=SimpleNamespace(
            translation="off",
            translate_include=["items", "trends", "ideas"],
            site_build=False,
            on_translate_failure="partial_success",
        )
    )

    def _override(module_name: str, attr_name: str | None):
        if (
            module_name == "recoleta.site_deploy"
            and attr_name == "deploy_trend_static_site_to_github_pages"
        ):

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
                default_language_code=None,
            ):
                _ = (
                    input_dir,
                    repo_dir,
                    remote,
                    branch,
                    limit,
                    commit_message,
                    cname,
                    pages_config_mode,
                    force,
                    default_language_code,
                )
                return GitHubPagesDeployResult(
                    branch="gh-pages",
                    remote="origin",
                    remote_url="git@github.com:example/recoleta.git",
                    repo_root=tmp_path,
                    commit_sha="abcdef1234567890",
                    skipped=False,
                    trends_total=4,
                    topics_total=7,
                    files_total=18,
                    pages_source=PagesSourceConfigResult(
                        status="configured",
                        method="gh",
                        detail="configured via gh",
                        site_url="https://example.github.io/recoleta/",
                    ),
                )

            return _fake_deploy
        return None

    _install_deploy_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=_FakeRepo(),
        import_symbol_override=_override,
    )

    result = runner.invoke(recoleta.cli.app, ["run", "deploy", "--json"])

    assert result.exit_code == 0
    payload = json.loads(result.stdout)
    assert payload["status"] == "ok"
    assert payload["command"] == "run deploy"
    assert payload["branch"] == "gh-pages"
    assert payload["remote"] == "origin"
    assert payload["commit_sha"] == "abcdef1234567890"
    assert payload["pages_source"]["site_url"] == "https://example.github.io/recoleta/"


def test_run_deploy_cli_forwards_explicit_item_export_scope(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """Regression: run deploy must forward the full item export override."""
    runner = CliRunner()
    calls: dict[str, object] = {}
    fake_settings = _FakeSettings(
        markdown_output_dir=tmp_path / "output",
        recoleta_db_path=tmp_path / "recoleta.db",
        workflows=SimpleNamespace(
            deploy=SimpleNamespace(
                translation="off",
                translate_include=["items", "trends", "ideas"],
                site_build=False,
                on_translate_failure="partial_success",
            )
        ),
    )

    def _override(module_name: str, attr_name: str | None):
        if (
            module_name == "recoleta.site_deploy"
            and attr_name == "deploy_trend_static_site_to_github_pages"
        ):

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
                default_language_code=None,
                item_export_scope="linked",
            ):
                _ = (
                    input_dir,
                    repo_dir,
                    remote,
                    branch,
                    limit,
                    commit_message,
                    cname,
                    pages_config_mode,
                    force,
                    default_language_code,
                )
                calls["item_export_scope"] = item_export_scope
                return GitHubPagesDeployResult(
                    branch="gh-pages",
                    remote="origin",
                    remote_url="git@github.com:example/recoleta.git",
                    repo_root=tmp_path,
                    commit_sha="deadbeef",
                    skipped=False,
                    trends_total=1,
                    topics_total=2,
                    files_total=5,
                    pages_source=PagesSourceConfigResult(
                        status="configured",
                        method="gh",
                        detail="configured via gh",
                        site_url="https://example.github.io/recoleta/",
                    ),
                )

            return _fake_deploy
        return None

    _install_deploy_runtime(
        monkeypatch,
        settings=fake_settings,
        repository=_FakeRepo(),
        import_symbol_override=_override,
    )

    result = runner.invoke(
        recoleta.cli.app,
        ["run", "deploy", "--item-export-scope", "all"],
    )

    assert result.exit_code == 0
    assert calls["item_export_scope"] == "all"
