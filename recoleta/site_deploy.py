from __future__ import annotations

from collections.abc import Sequence
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

from recoleta.site import TrendSiteInputSpec, export_trend_static_site

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


@dataclass(frozen=True, slots=True)
class GitHubPagesDeployRequest:
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec]
    repo_dir: Path
    remote: str = "origin"
    branch: str = _DEFAULT_DEPLOY_BRANCH
    limit: int | None = None
    commit_message: str | None = None
    cname: str | None = None
    pages_config_mode: str = "auto"
    force: bool = True
    default_language_code: str | None = None
    item_export_scope: str = "linked"


def _coerce_github_pages_deploy_request(
    *,
    request: GitHubPagesDeployRequest | None = None,
    legacy_kwargs: dict[str, Any] | None = None,
) -> GitHubPagesDeployRequest:
    if request is not None:
        return request
    values = dict(legacy_kwargs or {})
    return GitHubPagesDeployRequest(
        input_dir=values["input_dir"],
        repo_dir=values["repo_dir"],
        remote=str(values.get("remote") or "origin"),
        branch=str(values.get("branch") or _DEFAULT_DEPLOY_BRANCH),
        limit=values.get("limit"),
        commit_message=values.get("commit_message"),
        cname=values.get("cname"),
        pages_config_mode=str(values.get("pages_config_mode") or "auto"),
        force=bool(values.get("force", True)),
        default_language_code=values.get("default_language_code"),
        item_export_scope=str(values.get("item_export_scope") or "linked"),
    )


@dataclass(frozen=True, slots=True)
class _DeployPreparationRequest:
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec]
    site_dir: Path
    limit: int | None
    default_language_code: str | None
    item_export_scope: str
    cname: str | None


@dataclass(frozen=True, slots=True)
class _DeployContext:
    normalized_mode: str
    repo_root: Path
    branch: str
    remote_info: GitRemoteInfo


@dataclass(frozen=True, slots=True)
class _PreparedDeploySite:
    manifest: dict[str, Any]
    commit_sha: str | None
    skipped: bool
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

    endpoint = _gh_pages_endpoint(remote_info=remote_info)
    payload_args = _gh_pages_payload_args(branch=branch)
    failure = _gh_pages_update_or_create(
        base_args=base_args,
        endpoint=endpoint,
        payload_args=payload_args,
    )
    if failure is not None:
        return failure
    site_url = _gh_pages_site_url(base_args=base_args, endpoint=endpoint)
    return _pages_success_result(
        method="gh",
        detail=f"configured GitHub Pages to publish from {branch}",
        site_url=site_url,
    )


def _gh_pages_endpoint(*, remote_info: GitRemoteInfo) -> str:
    return f"repos/{remote_info.owner}/{remote_info.repo}/pages"


def _gh_pages_payload_args(*, branch: str) -> list[str]:
    return ["-f", f"source[branch]={branch}", "-f", "source[path]=/"]


def _pages_failure_detail(*, completed: subprocess.CompletedProcess[str]) -> str:
    return (
        completed.stderr.strip()
        or completed.stdout.strip()
        or "Pages source configuration failed"
    )


def _gh_pages_update_or_create(
    *,
    base_args: list[str],
    endpoint: str,
    payload_args: list[str],
) -> PagesSourceConfigResult | None:
    update = _run_command(
        [*base_args, "-X", "PUT", endpoint, *payload_args],
        cwd=Path.cwd(),
        check=False,
    )
    if update.returncode == 0:
        return None
    stderr = update.stderr.strip()
    if "404" not in stderr and "Not Found" not in stderr:
        return _pages_failed_result(method="gh", detail=_pages_failure_detail(completed=update))
    create = _run_command(
        [*base_args, "-X", "POST", endpoint, *payload_args],
        cwd=Path.cwd(),
        check=False,
    )
    if create.returncode == 0:
        return None
    return _pages_failed_result(method="gh", detail=_pages_failure_detail(completed=create))


def _gh_pages_site_url(*, base_args: list[str], endpoint: str) -> str | None:
    info = _run_command(
        [*base_args, endpoint],
        cwd=Path.cwd(),
        check=False,
    )
    if info.returncode != 0:
        return None
    try:
        payload = json.loads(info.stdout or "{}")
    except Exception:
        return None
    candidate = str(payload.get("html_url") or "").strip()
    return candidate or None


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
    request: GitHubPagesDeployRequest | None = None,
    **legacy_kwargs: Any,
) -> GitHubPagesDeployResult:
    resolved_request = _coerce_github_pages_deploy_request(
        request=request,
        legacy_kwargs=legacy_kwargs,
    )
    context = _resolved_deploy_context(
        repo_dir=resolved_request.repo_dir,
        remote=resolved_request.remote,
        branch=resolved_request.branch,
        pages_config_mode=resolved_request.pages_config_mode,
    )
    prepared = _prepare_deploy_site(
        context=context,
        request=_deploy_preparation_request(
            input_dir=resolved_request.input_dir,
            limit=resolved_request.limit,
            default_language_code=resolved_request.default_language_code,
            item_export_scope=resolved_request.item_export_scope,
            cname=resolved_request.cname,
        ),
        commit_message=resolved_request.commit_message,
        force=resolved_request.force,
    )
    result = _deploy_result(context=context, prepared=prepared)
    _log_deploy_result(result=result)
    return result


def _resolved_deploy_context(
    *,
    repo_dir: Path,
    remote: str,
    branch: str,
    pages_config_mode: str,
) -> _DeployContext:
    repo_root = _resolve_git_repo_root(repo_dir.expanduser().resolve())
    return _DeployContext(
        normalized_mode=_normalize_pages_config_mode(pages_config_mode),
        repo_root=repo_root,
        branch=_resolved_deploy_branch(branch=branch),
        remote_info=_resolve_git_remote(
            repo_root=repo_root,
            remote_name=str(remote or "origin").strip() or "origin",
        ),
    )


def _deploy_preparation_request(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    limit: int | None,
    default_language_code: str | None,
    item_export_scope: str,
    cname: str | None,
) -> _DeployPreparationRequest:
    return _DeployPreparationRequest(
        input_dir=input_dir,
        site_dir=Path(),
        limit=limit,
        default_language_code=default_language_code,
        item_export_scope=item_export_scope,
        cname=cname,
    )


def _prepare_deploy_site(
    *,
    context: _DeployContext,
    request: _DeployPreparationRequest,
    commit_message: str | None,
    force: bool,
) -> _PreparedDeploySite:
    with tempfile.TemporaryDirectory(
        prefix="recoleta-gh-pages-site-",
        ignore_cleanup_errors=True,
    ) as tmp_dir:
        site_dir = Path(tmp_dir).resolve() / "site"
        manifest = _prepare_site_dir(
            request=_DeployPreparationRequest(
                input_dir=request.input_dir,
                site_dir=site_dir,
                limit=request.limit,
                default_language_code=request.default_language_code,
                item_export_scope=request.item_export_scope,
                cname=request.cname,
            )
        )
        commit_sha, skipped = _publish_site_snapshot(
            site_dir=site_dir,
            repo_root=context.repo_root,
            remote_info=context.remote_info,
            branch=context.branch,
            commit_message=_resolved_deploy_message(commit_message=commit_message),
            force=force,
        )
        return _PreparedDeploySite(
            manifest=manifest,
            commit_sha=commit_sha or None,
            skipped=skipped,
            files_total=_site_files_total(site_dir=site_dir),
            pages_source=_configure_pages_source(
                remote_info=context.remote_info,
                branch=context.branch,
                mode=context.normalized_mode,
            ),
        )


def _deploy_result(
    *,
    context: _DeployContext,
    prepared: _PreparedDeploySite,
) -> GitHubPagesDeployResult:
    return GitHubPagesDeployResult(
        branch=context.branch,
        remote=context.remote_info.name,
        remote_url=context.remote_info.url,
        repo_root=context.repo_root,
        commit_sha=prepared.commit_sha,
        skipped=prepared.skipped,
        trends_total=int(prepared.manifest.get("trends_total") or 0),
        topics_total=int(prepared.manifest.get("topics_total") or 0),
        files_total=prepared.files_total,
        pages_source=prepared.pages_source,
    )


def _log_deploy_result(*, result: GitHubPagesDeployResult) -> None:
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


def _resolved_deploy_branch(*, branch: str) -> str:
    return str(branch or _DEFAULT_DEPLOY_BRANCH).strip() or _DEFAULT_DEPLOY_BRANCH


def _resolved_deploy_message(*, commit_message: str | None) -> str:
    return (str(commit_message).strip() if commit_message is not None else "") or _DEFAULT_DEPLOY_MESSAGE


def _site_export_kwargs(
    *,
    input_dir: Path | TrendSiteInputSpec | Sequence[Path | TrendSiteInputSpec],
    site_dir: Path,
    limit: int | None,
    default_language_code: str | None,
    item_export_scope: str,
) -> dict[str, Any]:
    normalized_item_export_scope = str(item_export_scope or "").strip().lower() or "linked"
    export_kwargs: dict[str, Any] = {
        "input_dir": input_dir,
        "output_dir": site_dir,
        "limit": limit,
        "default_language_code": default_language_code,
    }
    if normalized_item_export_scope != "linked":
        export_kwargs["item_export_scope"] = normalized_item_export_scope
    return export_kwargs


def _prepare_site_dir(
    *,
    request: _DeployPreparationRequest,
) -> dict[str, Any]:
    export_trend_static_site(
        **_site_export_kwargs(
            input_dir=request.input_dir,
            site_dir=request.site_dir,
            limit=request.limit,
            default_language_code=request.default_language_code,
            item_export_scope=request.item_export_scope,
        )
    )
    manifest = _sanitize_public_manifests(site_dir=request.site_dir)
    if request.cname is not None:
        _write_cname(site_dir=request.site_dir, cname=request.cname)
    _ensure_no_symlinks(request.site_dir)
    return manifest


def _site_files_total(*, site_dir: Path) -> int:
    return sum(1 for child in site_dir.rglob("*") if child.is_file())
