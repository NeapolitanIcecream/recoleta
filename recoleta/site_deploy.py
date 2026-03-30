from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Any
from urllib.parse import urlparse

from loguru import logger

from recoleta.site import export_trend_static_site

_DEFAULT_DEPLOY_BRANCH = "gh-pages"
_DEFAULT_DEPLOY_MESSAGE = "Deploy Recoleta static site"
_ALLOWED_PAGES_CONFIG_MODES = {"auto", "always", "never"}
_SCP_REMOTE_RE = re.compile(r"^(?:(?P<user>[^@]+)@)?(?P<host>[^:/]+):(?P<path>.+)$")


@dataclass(slots=True)
class GitRemoteInfo:
    name: str
    url: str
    host: str | None
    owner: str | None
    repo: str | None


@dataclass(slots=True)
class PagesSourceConfigResult:
    status: str
    method: str | None
    detail: str
    site_url: str | None


@dataclass(slots=True)
class GitHubPagesDeployResult:
    branch: str
    remote: str
    remote_url: str
    repo_root: Path
    commit_sha: str | None
    skipped: bool
    trends_total: int
    topics_total: int
    files_total: int
    pages_source: PagesSourceConfigResult


def _run_command(
    args: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        args,
        cwd=cwd,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    if check and completed.returncode != 0:
        stderr = completed.stderr.strip()
        stdout = completed.stdout.strip()
        detail = stderr or stdout or f"exit_code={completed.returncode}"
        raise RuntimeError(f"Command failed: {' '.join(args)} ({detail})")
    return completed


def _run_git(
    args: list[str],
    *,
    cwd: Path,
    check: bool = True,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    git_executable = shutil.which("git")
    if git_executable is None:
        raise RuntimeError("git executable was not found in PATH")
    return _run_command([git_executable, *args], cwd=cwd, env=env, check=check)


def _normalize_pages_config_mode(value: str) -> str:
    normalized = str(value or "").strip().lower() or "auto"
    if normalized not in _ALLOWED_PAGES_CONFIG_MODES:
        raise ValueError(
            "pages_config_mode must be one of: auto, always, never"
        )
    return normalized


def _resolve_git_repo_root(repo_dir: Path) -> Path:
    completed = _run_git(
        ["rev-parse", "--show-toplevel"],
        cwd=repo_dir.expanduser().resolve(),
    )
    return Path(completed.stdout.strip()).expanduser().resolve()


def _parse_git_remote(url: str, *, name: str) -> GitRemoteInfo:
    raw = str(url or "").strip()
    host: str | None = None
    owner: str | None = None
    repo: str | None = None
    path = ""

    if raw.startswith(("http://", "https://", "ssh://", "git://")):
        parsed = urlparse(raw)
        host = parsed.hostname
        path = parsed.path or ""
    else:
        matched = _SCP_REMOTE_RE.fullmatch(raw)
        if matched is not None:
            host = matched.group("host")
            path = matched.group("path") or ""

    normalized_path = path.strip().lstrip("/").removesuffix(".git")
    parts = [part for part in normalized_path.split("/") if part]
    if len(parts) >= 2:
        owner = parts[-2]
        repo = parts[-1]

    return GitRemoteInfo(
        name=name,
        url=raw,
        host=host.lower() if host is not None else None,
        owner=owner,
        repo=repo,
    )


def _git_remote_url(*, repo_root: Path, remote_name: str, push: bool) -> str | None:
    args = ["remote", "get-url"]
    if push:
        args.append("--push")
    args.append(remote_name)
    completed = _run_git(
        args,
        cwd=repo_root,
        check=False,
    )
    normalized = completed.stdout.strip()
    if completed.returncode != 0 or not normalized:
        return None
    return normalized


def _resolve_git_remote(*, repo_root: Path, remote_name: str) -> GitRemoteInfo:
    remote_url = _git_remote_url(
        repo_root=repo_root,
        remote_name=remote_name,
        push=True,
    )
    if remote_url is None:
        completed = _run_git(
            ["remote", "get-url", remote_name],
            cwd=repo_root,
        )
        remote_url = completed.stdout.strip()
    return _parse_git_remote(remote_url, name=remote_name)


def _git_config_value(*, repo_root: Path, key: str) -> str | None:
    completed = _run_git(
        ["config", "--get", key],
        cwd=repo_root,
        check=False,
    )
    normalized = completed.stdout.strip()
    return normalized or None


def _deployment_identity(*, repo_root: Path) -> tuple[str, str]:
    name = _git_config_value(repo_root=repo_root, key="user.name") or "Recoleta"
    email = _git_config_value(repo_root=repo_root, key="user.email") or "recoleta@localhost"
    return name, email


def _clear_directory_contents(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.name == ".git":
            continue
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def _copy_tree_contents(*, source_dir: Path, target_dir: Path) -> None:
    for child in source_dir.iterdir():
        destination = target_dir / child.name
        if child.is_dir():
            shutil.copytree(child, destination, dirs_exist_ok=True)
        else:
            shutil.copy2(child, destination)


def _write_cname(*, site_dir: Path, cname: str) -> None:
    normalized = str(cname or "").strip()
    if not normalized:
        raise ValueError("cname must not be empty")
    if "\n" in normalized or "\r" in normalized:
        raise ValueError("cname must be a single-line value")
    (site_dir / "CNAME").write_text(normalized + "\n", encoding="utf-8")


def _sanitize_public_manifest(*, manifest_path: Path) -> dict[str, Any]:
    loaded = json.loads(manifest_path.read_text(encoding="utf-8"))
    sanitized = {
        "files": loaded.get("files") or {},
        "topics_total": int(loaded.get("topics_total") or 0),
        "trends_total": int(loaded.get("trends_total") or 0),
    }
    for key in (
        "ideas_total",
        "items_total",
        "items_available_total",
        "items_unreferenced_total",
        "item_export_scope",
        "languages",
        "language_codes",
        "default_language_code",
    ):
        if key in loaded:
            sanitized[key] = loaded.get(key)
    manifest_path.write_text(
        json.dumps(sanitized, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return sanitized


def _sanitize_public_manifests(*, site_dir: Path) -> dict[str, Any]:
    root_manifest_path = site_dir / "manifest.json"
    root_manifest = _sanitize_public_manifest(manifest_path=root_manifest_path)
    for manifest_path in sorted(site_dir.rglob("manifest.json")):
        if manifest_path == root_manifest_path:
            continue
        _sanitize_public_manifest(manifest_path=manifest_path)
    return root_manifest


def _ensure_no_symlinks(path: Path) -> None:
    for child in path.rglob("*"):
        if child.is_symlink():
            raise ValueError(
                "GitHub Pages branch publishing does not support symbolic links; "
                "use `recoleta run site build` for manual hosting or a custom workflow instead."
            )


def _remote_branch_exists(*, remote_name: str, branch: str, cwd: Path) -> bool:
    completed = _run_git(
        ["ls-remote", "--exit-code", "--heads", remote_name, branch],
        cwd=cwd,
        check=False,
    )
    return completed.returncode == 0


def _prepare_deploy_checkout(
    *,
    deploy_root: Path,
    remote_name: str,
    remote_url: str,
    branch: str,
) -> bool:
    _run_git(["init"], cwd=deploy_root)
    _run_git(["remote", "add", remote_name, remote_url], cwd=deploy_root)

    branch_exists = _remote_branch_exists(
        remote_name=remote_name,
        branch=branch,
        cwd=deploy_root,
    )
    if branch_exists:
        _run_git(["fetch", "--depth", "1", remote_name, branch], cwd=deploy_root)
        _run_git(["checkout", "-B", branch, "FETCH_HEAD"], cwd=deploy_root)
    else:
        _run_git(["checkout", "--orphan", branch], cwd=deploy_root)
    return branch_exists


def _publish_site_snapshot(
    *,
    site_dir: Path,
    repo_root: Path,
    remote_info: GitRemoteInfo,
    branch: str,
    commit_message: str,
    force: bool,
) -> tuple[str, bool]:
    author_name, author_email = _deployment_identity(repo_root=repo_root)

    # Git housekeeping or filesystem indexing can leave transient entries in the
    # temporary checkout during teardown on macOS. Treat cleanup as best-effort so
    # a completed publish is not reported as failed after the push succeeded.
    with tempfile.TemporaryDirectory(
        prefix="recoleta-gh-pages-branch-",
        ignore_cleanup_errors=True,
    ) as tmp_dir:
        deploy_root = Path(tmp_dir).resolve()
        branch_exists = _prepare_deploy_checkout(
            deploy_root=deploy_root,
            remote_name=remote_info.name,
            remote_url=remote_info.url,
            branch=branch,
        )
        _clear_directory_contents(deploy_root)
        _copy_tree_contents(source_dir=site_dir, target_dir=deploy_root)
        _run_git(["add", "--all"], cwd=deploy_root)

        status_output = _run_git(["status", "--short"], cwd=deploy_root).stdout.strip()
        if branch_exists and not status_output:
            commit_sha = _run_git(["rev-parse", "HEAD"], cwd=deploy_root).stdout.strip()
            return commit_sha, True

        commit_env = os.environ.copy()
        commit_env["GIT_AUTHOR_NAME"] = author_name
        commit_env["GIT_AUTHOR_EMAIL"] = author_email
        commit_env["GIT_COMMITTER_NAME"] = author_name
        commit_env["GIT_COMMITTER_EMAIL"] = author_email
        _run_git(["commit", "-m", commit_message], cwd=deploy_root, env=commit_env)

        push_args = ["push"]
        if force:
            push_args.append("--force")
        push_args.extend(
            [remote_info.name, f"HEAD:refs/heads/{branch}"]
        )
        _run_git(push_args, cwd=deploy_root)
        commit_sha = _run_git(["rev-parse", "HEAD"], cwd=deploy_root).stdout.strip()
        return commit_sha, False


def _pages_skip_result(*, detail: str) -> PagesSourceConfigResult:
    return PagesSourceConfigResult(
        status="skipped",
        method=None,
        detail=detail,
        site_url=None,
    )


def _pages_failed_result(*, method: str, detail: str) -> PagesSourceConfigResult:
    return PagesSourceConfigResult(
        status="failed",
        method=method,
        detail=detail,
        site_url=None,
    )


def _pages_success_result(
    *,
    method: str,
    detail: str,
    site_url: str | None,
) -> PagesSourceConfigResult:
    return PagesSourceConfigResult(
        status="configured",
        method=method,
        detail=detail,
        site_url=site_url,
    )


def _gh_api_base_args(*, host: str | None) -> list[str] | None:
    gh_executable = shutil.which("gh")
    if gh_executable is None:
        return None
    base_args = [gh_executable, "api"]
    if host and host != "github.com":
        base_args.extend(["--hostname", host])
    return base_args


def _gh_api_configure_pages_source(
    *,
    remote_info: GitRemoteInfo,
    branch: str,
) -> PagesSourceConfigResult:
    if remote_info.host is None or remote_info.owner is None or remote_info.repo is None:
        return _pages_skip_result(detail="remote is not a GitHub repository")

    base_args = _gh_api_base_args(host=remote_info.host)
    if base_args is None:
        return _pages_skip_result(detail="gh CLI was not found in PATH")

    endpoint = f"repos/{remote_info.owner}/{remote_info.repo}/pages"
    payload_args = [
        "-f",
        f"source[branch]={branch}",
        "-f",
        "source[path]=/",
    ]

    update = _run_command(
        [*base_args, "-X", "PUT", endpoint, *payload_args],
        cwd=Path.cwd(),
        check=False,
    )
    if update.returncode != 0:
        stderr = update.stderr.strip()
        if "404" in stderr or "Not Found" in stderr:
            create = _run_command(
                [*base_args, "-X", "POST", endpoint, *payload_args],
                cwd=Path.cwd(),
                check=False,
            )
            if create.returncode != 0:
                detail = create.stderr.strip() or create.stdout.strip() or "Pages source configuration failed"
                return _pages_failed_result(method="gh", detail=detail)
        else:
            detail = stderr or update.stdout.strip() or "Pages source configuration failed"
            return _pages_failed_result(method="gh", detail=detail)

    info = _run_command(
        [*base_args, endpoint],
        cwd=Path.cwd(),
        check=False,
    )
    site_url: str | None = None
    if info.returncode == 0:
        try:
            payload = json.loads(info.stdout or "{}")
            candidate = str(payload.get("html_url") or "").strip()
            site_url = candidate or None
        except Exception:
            site_url = None
    return _pages_success_result(
        method="gh",
        detail=f"configured GitHub Pages to publish from {branch}",
        site_url=site_url,
    )


def _github_token() -> str | None:
    for key in ("GH_TOKEN", "GITHUB_TOKEN"):
        value = os.getenv(key, "").strip()
        if value:
            return value
    return None


def _http_api_configure_pages_source(
    *,
    remote_info: GitRemoteInfo,
    branch: str,
) -> PagesSourceConfigResult:
    token = _github_token()
    if token is None:
        return _pages_skip_result(detail="no GH_TOKEN or GITHUB_TOKEN was set")
    if remote_info.host != "github.com" or remote_info.owner is None or remote_info.repo is None:
        return _pages_skip_result(
            detail="token-based Pages auto-configuration currently supports github.com remotes only"
        )

    import httpx

    endpoint = f"https://api.github.com/repos/{remote_info.owner}/{remote_info.repo}/pages"
    payload: dict[str, Any] = {"source": {"branch": branch, "path": "/"}}
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    with httpx.Client(timeout=20.0, headers=headers) as client:
        response = client.put(endpoint, json=payload)
        if response.status_code == 404:
            response = client.post(endpoint, json=payload)
        if response.status_code not in {200, 201, 204}:
            detail = response.text.strip() or f"GitHub API returned {response.status_code}"
            return _pages_failed_result(method="token", detail=detail)
        info = client.get(endpoint)
        site_url: str | None = None
        if info.status_code == 200:
            try:
                payload_json = info.json()
            except Exception:
                payload_json = {}
            candidate = str(payload_json.get("html_url") or "").strip()
            site_url = candidate or None

    return _pages_success_result(
        method="token",
        detail=f"configured GitHub Pages to publish from {branch}",
        site_url=site_url,
    )


def _configure_pages_source(
    *,
    remote_info: GitRemoteInfo,
    branch: str,
    mode: str,
) -> PagesSourceConfigResult:
    normalized_mode = _normalize_pages_config_mode(mode)
    if normalized_mode == "never":
        return _pages_skip_result(detail="pages source configuration was disabled")

    gh_result = _gh_api_configure_pages_source(
        remote_info=remote_info,
        branch=branch,
    )
    if gh_result.status == "configured":
        return gh_result
    if gh_result.status == "failed":
        if normalized_mode == "always":
            raise RuntimeError(gh_result.detail)
        return gh_result

    token_result = _http_api_configure_pages_source(
        remote_info=remote_info,
        branch=branch,
    )
    if token_result.status == "configured":
        return token_result
    if token_result.status == "failed":
        if normalized_mode == "always":
            raise RuntimeError(token_result.detail)
        return token_result

    if normalized_mode == "always":
        raise RuntimeError(token_result.detail)
    return token_result


def deploy_trend_static_site_to_github_pages(
    *,
    input_dir: Path | list[Path],
    repo_dir: Path,
    remote: str = "origin",
    branch: str = _DEFAULT_DEPLOY_BRANCH,
    limit: int | None = None,
    commit_message: str | None = None,
    cname: str | None = None,
    pages_config_mode: str = "auto",
    force: bool = True,
    default_language_code: str | None = None,
    item_export_scope: str = "linked",
) -> GitHubPagesDeployResult:
    normalized_mode = _normalize_pages_config_mode(pages_config_mode)
    resolved_repo_root = _resolve_git_repo_root(repo_dir.expanduser().resolve())
    remote_info = _resolve_git_remote(
        repo_root=resolved_repo_root,
        remote_name=str(remote or "origin").strip() or "origin",
    )

    with tempfile.TemporaryDirectory(
        prefix="recoleta-gh-pages-site-",
        ignore_cleanup_errors=True,
    ) as tmp_dir:
        site_dir = Path(tmp_dir).resolve() / "site"
        normalized_item_export_scope = (
            str(item_export_scope or "").strip().lower() or "linked"
        )
        export_kwargs: dict[str, Any] = {
            "input_dir": input_dir,
            "output_dir": site_dir,
            "limit": limit,
            "default_language_code": default_language_code,
        }
        if normalized_item_export_scope != "linked":
            export_kwargs["item_export_scope"] = normalized_item_export_scope
        manifest_path = export_trend_static_site(
            **export_kwargs,
        )
        _ = manifest_path
        manifest = _sanitize_public_manifests(site_dir=site_dir)
        if cname is not None:
            _write_cname(site_dir=site_dir, cname=cname)
        _ensure_no_symlinks(site_dir)

        commit_sha, skipped = _publish_site_snapshot(
            site_dir=site_dir,
            repo_root=resolved_repo_root,
            remote_info=remote_info,
            branch=str(branch or _DEFAULT_DEPLOY_BRANCH).strip() or _DEFAULT_DEPLOY_BRANCH,
            commit_message=(str(commit_message).strip() if commit_message is not None else "")
            or _DEFAULT_DEPLOY_MESSAGE,
            force=force,
        )

        pages_source = _configure_pages_source(
            remote_info=remote_info,
            branch=str(branch or _DEFAULT_DEPLOY_BRANCH).strip() or _DEFAULT_DEPLOY_BRANCH,
            mode=normalized_mode,
        )

        files_total = sum(1 for child in site_dir.rglob("*") if child.is_file())

    result = GitHubPagesDeployResult(
        branch=str(branch or _DEFAULT_DEPLOY_BRANCH).strip() or _DEFAULT_DEPLOY_BRANCH,
        remote=remote_info.name,
        remote_url=remote_info.url,
        repo_root=resolved_repo_root,
        commit_sha=commit_sha or None,
        skipped=skipped,
        trends_total=int(manifest.get("trends_total") or 0),
        topics_total=int(manifest.get("topics_total") or 0),
        files_total=files_total,
        pages_source=pages_source,
    )
    logger.bind(
        module="site.gh_deploy",
        repo_root=str(result.repo_root),
        remote=result.remote,
        branch=result.branch,
        skipped=result.skipped,
        trends_total=result.trends_total,
        topics_total=result.topics_total,
        pages_source_status=result.pages_source.status,
    ).info("GitHub Pages branch deployment completed")
    return result
