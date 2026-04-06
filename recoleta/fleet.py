from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

import yaml
from slugify import slugify

from recoleta.config import Settings


@dataclass(frozen=True, slots=True)
class FleetInstance:
    name: str
    config_path: Path


@dataclass(frozen=True, slots=True)
class FleetManifest:
    manifest_path: Path
    schema_version: int
    instances: list[FleetInstance]


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


def load_fleet_manifest(manifest_path: Path) -> FleetManifest:
    resolved_manifest_path = manifest_path.expanduser().resolve()
    raw = _load_document(resolved_manifest_path)
    schema_version = int(raw.get("schema_version") or 1)
    if schema_version != 1:
        raise ValueError("Unsupported fleet manifest schema_version")
    raw_instances = raw.get("instances")
    if not isinstance(raw_instances, list) or not raw_instances:
        raise ValueError("Fleet manifest must define at least one child instance")

    instances: list[FleetInstance] = []
    seen_names: set[str] = set()
    seen_slugs: dict[str, str] = {}
    for entry in raw_instances:
        if not isinstance(entry, dict):
            raise ValueError("fleet instances entries must be mappings/objects")
        name = str(entry.get("name") or "").strip()
        if not name:
            raise ValueError("fleet instances[].name is required")
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
        config_path = _resolve_config_path(
            manifest_path=resolved_manifest_path,
            value=entry.get("config_path"),
        )
        child_raw = _raw_child_config(config_path)
        if "daemon" in child_raw or "DAEMON" in child_raw:
            raise ValueError(
                f"Fleet child config must not declare DAEMON: {config_path}"
            )
        _ = load_child_settings(config_path)
        instances.append(FleetInstance(name=name, config_path=config_path))
    return FleetManifest(
        manifest_path=resolved_manifest_path,
        schema_version=schema_version,
        instances=instances,
    )
