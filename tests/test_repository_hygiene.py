from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlsplit


REPO_ROOT = Path(__file__).resolve().parents[1]
PLAIN_USER_HOME_PATTERN = re.compile(
    r"(?:^|[\s`'\"=(])"
    r"(?:/(?:Users|home)/[^/\s`'\"<>]+(?:/|$)"
    r"|[A-Za-z]:/Users/[^/\s`'\"<>]+(?:/|$))",
    flags=re.IGNORECASE,
)
FILE_URI_PATTERN = re.compile(
    "file" + r"://[^\s`'\"<>]+",
    flags=re.IGNORECASE,
)
ABSOLUTE_USER_HOME_PATTERNS = (
    re.compile(
        r"^/(?:Users|home)/[^/\s`'\"<>]+(?:/|$)",
        flags=re.IGNORECASE,
    ),
    re.compile(
        r"^[A-Za-z]:/Users/[^/\s`'\"<>]+(?:/|$)",
        flags=re.IGNORECASE,
    ),
)


def _tracked_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
    )
    return [
        Path(raw_path.decode())
        for raw_path in result.stdout.split(b"\0")
        if raw_path
    ]


def _is_absolute_user_home(path: str) -> bool:
    normalized = unquote(path).replace("\\", "/")
    return any(pattern.search(normalized) for pattern in ABSOLUTE_USER_HOME_PATTERNS)


def _contains_user_home_path(line: str) -> bool:
    normalized = line.replace("\\", "/")
    if PLAIN_USER_HOME_PATTERN.search(normalized):
        return True

    for match in FILE_URI_PATTERN.finditer(normalized):
        parsed = urlsplit(match.group())
        uri_path = parsed.path
        candidates = [uri_path]
        if re.match(r"^/[A-Za-z]:/", uri_path):
            candidates.append(uri_path[1:])
        if re.fullmatch(r"[A-Za-z]:", parsed.netloc):
            candidates.append(f"{parsed.netloc}{uri_path}")
        if any(_is_absolute_user_home(candidate) for candidate in candidates):
            return True

    return False


def test_repository_does_not_track_local_agent_state() -> None:
    forbidden_prefixes = (".codex-workflows/", ".cursor/")
    tracked = [path.as_posix() for path in _tracked_paths()]

    violations = [
        path
        for path in tracked
        if any(path.startswith(prefix) for prefix in forbidden_prefixes)
    ]

    assert violations == []


def test_user_home_path_detection_covers_platform_and_uri_variants() -> None:
    macos_home = "/" + "Users" + "/alice/recoleta"
    linux_home = "/" + "home" + "/alice/recoleta"
    windows_home = "C:" + "\\" + "Users" + "\\alice\\recoleta"
    normalized_windows_home = "C:" + "/" + "Users" + "/alice/recoleta"
    file_uri = "file" + "://"

    examples = (
        macos_home,
        linux_home,
        windows_home,
        normalized_windows_home,
        f"{file_uri}{macos_home}",
        f"{file_uri}{linux_home}",
        f"{file_uri}/{normalized_windows_home}",
        f"{file_uri}localhost/{normalized_windows_home}",
    )

    assert all(_contains_user_home_path(f"path={example}") for example in examples)


def test_user_home_path_detection_allows_unrelated_uris() -> None:
    file_uri = "file" + "://"

    examples = (
        f"{file_uri}/tmp/recoleta/report.json",
        f"{file_uri}server/shared/recoleta.db",
        "https://example.com/home/research",
    )

    assert not any(_contains_user_home_path(example) for example in examples)


def test_tracked_text_does_not_contain_user_home_paths() -> None:
    violations: list[str] = []

    for relative_path in _tracked_paths():
        path = REPO_ROOT / relative_path
        if not path.is_file():
            continue
        contents = path.read_bytes()
        if b"\0" in contents:
            continue
        text = contents.decode("utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if _contains_user_home_path(line):
                violations.append(f"{relative_path.as_posix()}:{line_number}")

    assert violations == []
