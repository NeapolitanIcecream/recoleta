from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from filelock import FileLock, Timeout
import yaml
from slugify import slugify

from recoleta.config import DaemonConfig, Settings


class FleetSequenceBusyError(RuntimeError):
    """Raised when another process owns the fleet workflow sequence lease."""


@dataclass(frozen=True, slots=True)
class FleetInstance:
    name: str
    config_path: Path


@dataclass(frozen=True, slots=True)
class FleetManifest:
    manifest_path: Path
    schema_version: int
    instances: list[FleetInstance]
    daemon: DaemonConfig


def fleet_sequence_lock_path(manifest_path: Path) -> Path:
    resolved = manifest_path.expanduser().resolve()
    digest = hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()
    user_id = getattr(os, "getuid", lambda: "user")()
    lock_root = Path(tempfile.gettempdir()) / f"recoleta-fleet-locks-{user_id}"
    lock_root.mkdir(mode=0o700, parents=True, exist_ok=True)
    return lock_root / f"{digest}.lock"


@contextmanager
def fleet_sequence_lease(manifest_path: Path) -> Iterator[None]:
    """Hold a crash-safe, host-local lease for one complete fleet sequence."""

    resolved = manifest_path.expanduser().resolve()
    lock_path = fleet_sequence_lock_path(resolved)
    lock = FileLock(lock_path)
    try:
        lock.acquire(timeout=0)
    except Timeout as exc:
        raise FleetSequenceBusyError(
            f"Fleet workflow is already running for manifest: {resolved.name}"
        ) from exc
    try:
        yield
    finally:
        lock.release()


def _load_document(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    raw_text = resolved.read_text(encoding="utf-8")
    suffix = resolved.suffix.lower()
    if suffix == ".json":
        loaded = json.loads(raw_text)
    elif suffix in {".yaml", ".yml"}:
        loaded = yaml.safe_load(raw_text)
    else:
        raise ValueError(
            f"Unsupported manifest file type: {resolved.suffix} (expected .yaml/.yml/.json)"
        )
    if not isinstance(loaded, dict):
        raise ValueError("Fleet manifest must contain a mapping/object")
    return loaded


def _resolve_config_path(*, manifest_path: Path, value: Any) -> Path:
    raw = str(value or "").strip()
    if not raw:
        raise ValueError("fleet instances[].config_path is required")
    candidate = Path(raw).expanduser()
    if not candidate.is_absolute():
        candidate = (manifest_path.parent / candidate).resolve()
    else:
        candidate = candidate.resolve()
    if not candidate.exists() or not candidate.is_file():
        raise ValueError(f"Fleet child config does not exist: {candidate}")
    return candidate


def _raw_child_config(config_path: Path) -> dict[str, Any]:
    suffix = config_path.suffix.lower()
    raw_text = config_path.read_text(encoding="utf-8")
    if suffix == ".json":
        loaded = json.loads(raw_text)
    elif suffix in {".yaml", ".yml"}:
        loaded = yaml.safe_load(raw_text)
    else:
        raise ValueError(
            f"Unsupported child config type: {config_path.suffix} (expected .yaml/.yml/.json)"
        )
    if not isinstance(loaded, dict):
        raise ValueError(f"Child config must contain a mapping/object: {config_path}")
    return loaded


def load_child_settings(config_path: Path) -> Settings:
    return Settings(config_path=config_path.expanduser().resolve())  # pyright: ignore[reportCallIssue]


def child_site_input_dir(config_path: Path) -> Path:
    settings = load_child_settings(config_path)
    return Path(settings.markdown_output_dir).expanduser().resolve()


def child_default_language_code(config_path: Path) -> str | None:
    settings = load_child_settings(config_path)
    localization = getattr(settings, "localization", None)
    if localization is None:
        return None
    return (
        str(getattr(localization, "site_default_language_code", "") or "").strip()
        or None
    )


def _fleet_instance_slug(name: str) -> str:
    return slugify(str(name or "").strip(), lowercase=True) or "instance"


def _load_fleet_daemon(raw: dict[str, Any]) -> DaemonConfig:
    raw_daemon = raw.get("daemon", raw.get("DAEMON", {}))
    if raw_daemon is None:
        raw_daemon = {}
    if not isinstance(raw_daemon, dict):
        raise ValueError("fleet daemon must be a mapping/object")
    return DaemonConfig.model_validate(raw_daemon)


def _claim_fleet_instance_name(
    name: str,
    *,
    seen_names: set[str],
    seen_slugs: dict[str, str],
) -> None:
    if name in seen_names:
        raise ValueError(f"Duplicate fleet instance name: {name}")
    seen_names.add(name)
    name_slug = _fleet_instance_slug(name)
    if name_slug in seen_slugs and seen_slugs[name_slug] != name:
        raise ValueError(
            "Fleet instance names must produce unique public slugs: "
            f"slug '{name_slug}' is shared by {seen_slugs[name_slug]}, {name}"
        )
    seen_slugs[name_slug] = name


def _load_fleet_instance(
    entry: Any,
    *,
    manifest_path: Path,
    seen_names: set[str],
    seen_slugs: dict[str, str],
) -> FleetInstance:
    if not isinstance(entry, dict):
        raise ValueError("fleet instances entries must be mappings/objects")
    name = str(entry.get("name") or "").strip()
    if not name:
        raise ValueError("fleet instances[].name is required")
    _claim_fleet_instance_name(
        name,
        seen_names=seen_names,
        seen_slugs=seen_slugs,
    )
    config_path = _resolve_config_path(
        manifest_path=manifest_path,
        value=entry.get("config_path"),
    )
    child_raw = _raw_child_config(config_path)
    if "daemon" in child_raw or "DAEMON" in child_raw:
        raise ValueError(f"Fleet child config must not declare DAEMON: {config_path}")
    _ = load_child_settings(config_path)
    return FleetInstance(name=name, config_path=config_path)


def _load_fleet_instances(raw: Any, *, manifest_path: Path) -> list[FleetInstance]:
    if not isinstance(raw, list) or not raw:
        raise ValueError("Fleet manifest must define at least one child instance")
    instances: list[FleetInstance] = []
    seen_names: set[str] = set()
    seen_slugs: dict[str, str] = {}
    for entry in raw:
        instances.append(
            _load_fleet_instance(
                entry,
                manifest_path=manifest_path,
                seen_names=seen_names,
                seen_slugs=seen_slugs,
            )
        )
    return instances


def load_fleet_manifest(manifest_path: Path) -> FleetManifest:
    resolved_manifest_path = manifest_path.expanduser().resolve()
    raw = _load_document(resolved_manifest_path)
    schema_version = int(raw.get("schema_version") or 1)
    if schema_version != 1:
        raise ValueError("Unsupported fleet manifest schema_version")
    return FleetManifest(
        manifest_path=resolved_manifest_path,
        schema_version=schema_version,
        instances=_load_fleet_instances(
            raw.get("instances"),
            manifest_path=resolved_manifest_path,
        ),
        daemon=_load_fleet_daemon(raw),
    )
