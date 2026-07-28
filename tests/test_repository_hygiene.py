from __future__ import annotations

import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


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


def test_repository_does_not_track_local_agent_state() -> None:
    forbidden_prefixes = (".codex-workflows/", ".cursor/")
    tracked = [path.as_posix() for path in _tracked_paths()]

    violations = [
        path
        for path in tracked
        if any(path.startswith(prefix) for prefix in forbidden_prefixes)
    ]

    assert violations == []


def test_tracked_text_does_not_contain_user_home_paths() -> None:
    unix_prefixes = ("/" + "Users" + "/", "/" + "home" + "/")
    windows_prefix = "\\" + "Users" + "\\"
    path_patterns = [
        re.compile(
            rf"(?:^|[\s`'\"=(]){re.escape(prefix)}[^/\s`'\"<>]+(?:/|$)"
        )
        for prefix in unix_prefixes
    ]
    path_patterns.append(
        re.compile(
            rf"(?:^|[\s`'\"=(])[A-Za-z]:{re.escape(windows_prefix)}"
            r"[^\\\s`'\"<>]+(?:\\|$)"
        )
    )
    file_uri = "file" + "://"
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
            if file_uri in line or any(
                pattern.search(line) for pattern in path_patterns
            ):
                violations.append(f"{relative_path.as_posix()}:{line_number}")

    assert violations == []
