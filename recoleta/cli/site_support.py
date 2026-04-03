from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True, slots=True)
class SiteCommandPaths:
    input_dir: Path
    output_dir: Path
    default_language_code: str | None
    item_export_scope: str
    settings: Any | None


@dataclass(frozen=True, slots=True)
class SitePathRequest:
    input_dir: Path | None
    output_dir: Path | None
    default_language_code: str | None
    item_export_scope: str
    settings: Any | None
    default_output_dir: Path


@dataclass(frozen=True, slots=True)
class FleetSitePayloadContext:
    command_name: str
    manifest: Any
    input_dirs: list[Any]
    output_dir: Path
    manifest_result_path: Path
    default_language_code: str | None
    item_export_scope: str
    site_manifest: dict[str, Any]


def site_input_dir_from_settings(settings: Any) -> Path:
    return Path(settings.markdown_output_dir).expanduser().resolve() / "Trends"


def site_output_dir_from_settings(settings: Any) -> Path:
    return Path(settings.markdown_output_dir).expanduser().resolve() / "site"


def default_language_code_from_settings(settings: Any) -> str | None:
    localization = getattr(settings, "localization", None)
    if localization is None:
        return None
    return str(getattr(localization, "site_default_language_code", "") or "").strip() or None


def normalize_item_export_scope(item_export_scope: str) -> str:
    return str(item_export_scope or "").strip().lower() or "linked"


def resolve_site_command_paths(*, request: SitePathRequest) -> SiteCommandPaths:
    resolved_default_language_code = str(request.default_language_code or "").strip() or None
    if resolved_default_language_code is None and request.settings is not None:
        resolved_default_language_code = default_language_code_from_settings(request.settings)
    return SiteCommandPaths(
        input_dir=(
            request.input_dir.expanduser().resolve()
            if request.input_dir is not None
            else site_input_dir_from_settings(request.settings)
        ),
        output_dir=(
            request.output_dir.expanduser().resolve()
            if request.output_dir is not None
            else request.default_output_dir
        ),
        default_language_code=resolved_default_language_code,
        item_export_scope=normalize_item_export_scope(request.item_export_scope),
        settings=request.settings,
    )


def site_item_count_segment(manifest: dict[str, Any]) -> str | None:
    if "items_total" not in manifest:
        return None
    items_total = int(manifest.get("items_total") or 0)
    items_available_total = manifest.get("items_available_total")
    if items_available_total is not None:
        available_total = int(items_available_total or 0)
        if available_total > items_total:
            return f"items={items_total}/{available_total}"
    return f"items={items_total}"


def load_manifest(manifest_path: Path) -> dict[str, Any]:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def site_manifest_payload(
    *,
    command_name: str,
    paths: SiteCommandPaths,
    limit: int | None,
    manifest_path: Path,
    manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "status": "ok",
        "command": command_name,
        "input_dir": str(paths.input_dir),
        "output_dir": str(paths.output_dir),
        "manifest_path": str(manifest_path),
        "default_language_code": paths.default_language_code,
        "item_export_scope": manifest.get("item_export_scope", paths.item_export_scope),
        "limit": limit,
        "manifest": manifest,
    }


def site_manifest_segments(
    *,
    manifest: dict[str, Any],
    output_dir: Path,
    include_pdfs: bool,
) -> list[str]:
    segments = [f"trends={manifest['trends_total']}"]
    if int(manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={manifest['ideas_total']}")
    if item_segment := site_item_count_segment(manifest):
        segments.append(item_segment)
    if "topics_total" in manifest:
        segments.append(f"topics={manifest['topics_total']}")
    if include_pdfs:
        segments.append(f"pdfs={manifest['pdf_total']}")
    segments.append(f"output={output_dir}")
    return segments


def fleet_input_dirs(
    *,
    manifest_path: Path,
    trend_site_input_spec_cls: Any,
    load_fleet_manifest: Callable[[Path], Any],
    child_site_input_dir: Callable[[Path], Path],
) -> tuple[Any, list[Any]]:
    manifest = load_fleet_manifest(manifest_path)
    return manifest, [
        trend_site_input_spec_cls(
            path=child_site_input_dir(instance.config_path),
            instance=instance.name,
        )
        for instance in manifest.instances
    ]


def fleet_default_language(
    *,
    manifest: Any,
    explicit: str | None,
    child_default_language_code: Callable[[Path], str | None],
) -> str | None:
    if explicit is not None and str(explicit).strip():
        return str(explicit).strip()
    for instance in manifest.instances:
        candidate = child_default_language_code(instance.config_path)
        if candidate:
            return candidate
    return None


def fleet_site_output_dir(
    *,
    manifest_path: Path,
    output_dir: Path | None,
    load_fleet_manifest: Callable[[Path], Any],
) -> Path:
    if output_dir is not None:
        return output_dir.expanduser().resolve()
    manifest = load_fleet_manifest(manifest_path)
    return manifest.manifest_path.parent / "site"


def fleet_site_payload(*, context: FleetSitePayloadContext) -> dict[str, Any]:
    return {
        "status": "ok",
        "command": context.command_name,
        "manifest_path": str(context.manifest.manifest_path),
        "input_dir": [str(input_spec.path) for input_spec in context.input_dirs],
        "output_dir": str(context.output_dir),
        "site_manifest_path": str(context.manifest_result_path),
        "default_language_code": context.default_language_code,
        "item_export_scope": context.site_manifest.get(
            "item_export_scope",
            context.item_export_scope,
        ),
        "manifest": context.site_manifest,
    }


def fleet_site_segments(*, manifest: Any, site_manifest: dict[str, Any], output_dir: Path) -> list[str]:
    segments = [
        f"instances={len(manifest.instances)}",
        f"trends={site_manifest.get('trends_total', 0)}",
    ]
    if int(site_manifest.get("ideas_total") or 0) > 0:
        segments.append(f"ideas={site_manifest['ideas_total']}")
    if item_segment := site_item_count_segment(site_manifest):
        segments.append(item_segment)
    segments.append(f"output={output_dir}")
    return segments
