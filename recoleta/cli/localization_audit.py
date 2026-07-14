from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, cast

from sqlmodel import Session, select

from recoleta.models import Analysis, Document, LocalizedOutput
from recoleta.pass_output_selection import (
    is_suppressed_pass_output,
    latest_canonical_pass_outputs_by_window,
    latest_idea_pass_output_states_by_window,
    pass_output_window_key,
)

_ISSUE_CODES = (
    "missing_localized_output",
    "orphan_localized_output",
    "unknown_localized_source_kind",
    "materialized_output_dir_missing",
    "materialized_missing_peer",
    "site_manifest_missing",
    "site_missing_peer",
    "site_manifest_language_missing",
    "site_manifest_invalid",
    "site_link_map_missing",
    "site_link_map_invalid",
    "site_link_map_mismatch",
)

_SURFACE_SPECS: dict[str, dict[str, str]] = {
    "items": {
        "source_kind": "analysis",
        "materialized_dir": "Inbox",
        "site_files_key": "item_pages",
    },
    "trends": {
        "source_kind": "trend_synthesis",
        "materialized_dir": "Trends",
        "site_files_key": "trend_pages",
    },
    "ideas": {
        "source_kind": "trend_ideas",
        "materialized_dir": "Ideas",
        "site_files_key": "idea_pages",
    },
}
_SURFACE_BY_SOURCE_KIND = {
    spec["source_kind"]: surface for surface, spec in _SURFACE_SPECS.items()
}


@dataclass(frozen=True, slots=True)
class LocalizationAuditRequest:
    repository: Any
    resolved_db_path: Path
    settings: Any | None
    settings_status: str
    materialized_output_dir: Path | None
    site_output_dir: Path | None
    sample_limit: int = 20


class _IssueCollector:
    def __init__(self, *, sample_limit: int) -> None:
        self.counts = {code: 0 for code in _ISSUE_CODES}
        self.samples = {code: [] for code in _ISSUE_CODES}
        self.sample_limit = max(0, int(sample_limit))

    def add(self, code: str, sample: dict[str, Any]) -> None:
        if code not in self.counts:
            self.counts[code] = 0
            self.samples[code] = []
        self.counts[code] += 1
        if len(self.samples[code]) < self.sample_limit:
            self.samples[code].append(sample)


def build_localization_audit_payload(
    *, request: LocalizationAuditRequest
) -> dict[str, Any]:
    issues = _IssueCollector(sample_limit=request.sample_limit)
    localization_payload = _localization_payload(settings=request.settings)
    storage_snapshot = _load_storage_snapshot(repository=request.repository)
    target_languages = _target_languages(
        localization=localization_payload,
        localized_rows=storage_snapshot["localized_rows"],
    )
    site_languages = _site_languages(
        localization=localization_payload,
        target_languages=target_languages,
    )

    surfaces_payload = _surfaces_payload(
        canonical_ids_by_surface=storage_snapshot["canonical_ids_by_surface"],
        known_ids_by_surface=storage_snapshot["known_ids_by_surface"],
        localized_rows=storage_snapshot["localized_rows"],
        target_languages=target_languages,
        issues=issues,
    )
    storage_payload = _storage_payload(
        known_ids_by_surface=storage_snapshot["known_ids_by_surface"],
        localized_rows=storage_snapshot["localized_rows"],
        issues=issues,
    )
    materialized_payload = _materialized_payload(
        output_dir=_resolve_materialized_output_dir(request=request),
        site_languages=site_languages,
        issues=issues,
    )
    site_payload = _site_payload(
        output_dir=_resolve_site_output_dir(request=request),
        site_languages=site_languages,
        issues=issues,
    )
    audit_status = (
        "warning" if any(count > 0 for count in issues.counts.values()) else "ok"
    )
    return {
        "status": "ok",
        "audit_status": audit_status,
        "db_path": str(request.resolved_db_path),
        "settings": request.settings_status,
        "localization": localization_payload,
        "expected_target_languages": target_languages,
        "expected_site_languages": site_languages,
        "surfaces": surfaces_payload,
        "storage": storage_payload,
        "materialized": materialized_payload,
        "site": site_payload,
        "issue_counts": issues.counts,
        "issue_samples": issues.samples,
    }


def render_localization_audit_output(
    *, console: Any, payload: dict[str, Any], command_name: str
) -> None:
    color = "green" if payload["audit_status"] == "ok" else "yellow"
    console.print(
        f"[{color}]{command_name} {payload['audit_status']}[/{color}] "
        f"db={payload['db_path']} settings={payload['settings']}"
    )
    console.print(
        "targets="
        + ",".join(payload["expected_target_languages"])
        + f" localized_outputs={payload['storage']['localized_outputs_total']} "
        + f"orphans={payload['storage']['orphan_total']}"
    )
    for surface, surface_payload in payload["surfaces"].items():
        language_segments = [
            f"{language}={stats['stored_total']}/{surface_payload['canonical_total']} "
            f"missing={stats['missing_total']}"
            for language, stats in surface_payload["languages"].items()
        ]
        console.print(
            f"surface={surface} canonical={surface_payload['canonical_total']} "
            + " ".join(language_segments)
        )
    console.print(
        f"materialized={payload['materialized']['status']} "
        f"missing_peer={payload['materialized']['missing_peer_total']} "
        f"site={payload['site']['status']} "
        f"site_missing_peer={payload['site']['missing_peer_total']} "
        f"link_map={payload['site'].get('link_map', {}).get('status', 'skipped')}"
    )
    issue_segments = [
        f"{code}={count}"
        for code, count in payload["issue_counts"].items()
        if int(count) > 0
    ]
    if issue_segments:
        console.print("issues=" + " ".join(issue_segments))
    for code, samples in payload["issue_samples"].items():
        for sample in samples:
            console.print(
                f"issue_sample code={code} "
                + " ".join(f"{key}={value}" for key, value in sample.items())
            )


def _language_slug(value: str | None) -> str:
    return str(value or "").strip().lower().replace("_", "-")


def _localization_payload(*, settings: Any | None) -> dict[str, Any]:
    localization = getattr(settings, "localization", None)
    if localization is None:
        return {
            "source_language_code": None,
            "target_languages": [],
            "site_default_language_code": None,
        }
    source_language_code = (
        str(getattr(localization, "source_language_code", "") or "").strip() or None
    )
    target_languages = [
        code
        for target in getattr(localization, "targets", []) or []
        if (code := str(getattr(target, "code", "") or "").strip())
    ]
    site_default_language_code = (
        str(getattr(localization, "site_default_language_code", "") or "").strip()
        or None
    )
    return {
        "source_language_code": source_language_code,
        "target_languages": _dedupe(target_languages),
        "site_default_language_code": site_default_language_code,
    }


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    deduped: list[str] = []
    for value in values:
        normalized = str(value or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        deduped.append(normalized)
    return deduped


def _load_storage_snapshot(*, repository: Any) -> dict[str, Any]:
    with Session(repository.engine) as session:
        analysis_ids = _id_set(session.exec(select(Analysis.id)))
        trend_documents = list(
            session.exec(select(Document).where(Document.doc_type == "trend"))
        )
        idea_documents = list(
            session.exec(select(Document).where(Document.doc_type == "idea"))
        )
        localized_rows = list(
            session.exec(
                select(LocalizedOutput).order_by(
                    cast(Any, LocalizedOutput.source_kind),
                    cast(Any, LocalizedOutput.source_record_id),
                    cast(Any, LocalizedOutput.language_code),
                    cast(Any, LocalizedOutput.id),
                )
            )
        )
    trend_ids = _document_ids(trend_documents)
    idea_ids = _document_ids(idea_documents)
    return {
        "canonical_ids_by_surface": {
            "items": analysis_ids,
            "trends": _canonical_document_ids(
                repository=repository,
                documents=trend_documents,
                pass_kind="trend_synthesis",
            ),
            "ideas": _canonical_document_ids(
                repository=repository,
                documents=idea_documents,
                pass_kind="trend_ideas",
            ),
        },
        "known_ids_by_surface": {
            "items": analysis_ids,
            "trends": trend_ids,
            "ideas": idea_ids,
        },
        "localized_rows": localized_rows,
    }


def _document_ids(documents: list[Document]) -> set[int]:
    return _id_set(getattr(document, "id", None) for document in documents)


def _canonical_document_ids(
    *, repository: Any, documents: list[Document], pass_kind: str
) -> set[int]:
    if pass_kind == "trend_ideas":
        return _canonical_idea_document_ids(
            repository=repository,
            documents=documents,
        )
    canonical_by_window = latest_canonical_pass_outputs_by_window(
        repository=repository,
        pass_kind=pass_kind,
        windows=(pass_output_window_key(document) for document in documents),
    )
    return {
        document_id
        for document in documents
        if (document_id := int(getattr(document, "id", 0) or 0)) > 0
        and not is_suppressed_pass_output(
            canonical_by_window.get(pass_output_window_key(document))
        )
    }


def _canonical_idea_document_ids(
    *, repository: Any, documents: list[Document]
) -> set[int]:
    states_by_window = latest_idea_pass_output_states_by_window(
        repository=repository,
        windows=(pass_output_window_key(document) for document in documents),
    )
    return {
        document_id
        for document in documents
        if (document_id := int(getattr(document, "id", 0) or 0)) > 0
        and (
            (state := states_by_window.get(pass_output_window_key(document))) is None
            or state.active
        )
    }


def _id_set(values: Any) -> set[int]:
    ids: set[int] = set()
    for value in values:
        if value is None:
            continue
        try:
            normalized = int(value)
        except Exception:
            continue
        if normalized > 0:
            ids.add(normalized)
    return ids


def _target_languages(
    *, localization: dict[str, Any], localized_rows: list[LocalizedOutput]
) -> list[str]:
    configured = list(localization.get("target_languages") or [])
    if configured:
        return configured
    return sorted(
        {
            language
            for row in localized_rows
            if (language := str(row.language_code or "").strip())
        }
    )


def _site_languages(
    *, localization: dict[str, Any], target_languages: list[str]
) -> list[dict[str, str]]:
    languages: list[dict[str, str]] = []
    source_language_code = localization.get("source_language_code")
    if source_language_code:
        languages.append(
            {
                "code": str(source_language_code),
                "slug": _language_slug(str(source_language_code)),
                "role": "source",
            }
        )
    for language_code in target_languages:
        slug = _language_slug(language_code)
        if not slug:
            continue
        languages.append(
            {"code": language_code, "slug": slug, "role": "target"}
        )
    seen: set[str] = set()
    deduped: list[dict[str, str]] = []
    for language in languages:
        slug = language["slug"]
        if slug in seen:
            continue
        seen.add(slug)
        deduped.append(language)
    return deduped


def _surfaces_payload(
    *,
    canonical_ids_by_surface: dict[str, set[int]],
    known_ids_by_surface: dict[str, set[int]],
    localized_rows: list[LocalizedOutput],
    target_languages: list[str],
    issues: _IssueCollector,
) -> dict[str, Any]:
    rows_by_kind_language = _rows_by_kind_language(localized_rows=localized_rows)
    payload: dict[str, Any] = {}
    for surface, spec in _SURFACE_SPECS.items():
        source_kind = spec["source_kind"]
        canonical_ids = canonical_ids_by_surface[surface]
        known_ids = known_ids_by_surface[surface]
        language_payload: dict[str, Any] = {}
        for language_code in target_languages:
            rows = rows_by_kind_language.get((source_kind, language_code), [])
            stored_ids = _row_source_ids(rows)
            active_stored_ids = stored_ids & canonical_ids
            inactive_ids = (stored_ids & known_ids) - canonical_ids
            orphan_ids = sorted(stored_ids - known_ids)
            missing_ids = sorted(canonical_ids - active_stored_ids)
            for source_record_id in missing_ids:
                issues.add(
                    "missing_localized_output",
                    {
                        "surface": surface,
                        "source_kind": source_kind,
                        "source_record_id": source_record_id,
                        "language_code": language_code,
                    },
                )
            language_payload[language_code] = {
                "stored_total": len(active_stored_ids),
                "succeeded_total": sum(
                    1
                    for row in rows
                    if str(row.status or "") == "succeeded"
                    and int(row.source_record_id) in canonical_ids
                ),
                "inactive_total": len(inactive_ids),
                "missing_total": len(missing_ids),
                "orphan_total": len(orphan_ids),
            }
        payload[surface] = {
            "source_kind": source_kind,
            "canonical_total": len(canonical_ids),
            "languages": language_payload,
        }
    return payload


def _rows_by_kind_language(
    *, localized_rows: list[LocalizedOutput]
) -> dict[tuple[str, str], list[LocalizedOutput]]:
    grouped: dict[tuple[str, str], list[LocalizedOutput]] = {}
    for row in localized_rows:
        source_kind = str(row.source_kind or "").strip()
        language_code = str(row.language_code or "").strip()
        grouped.setdefault((source_kind, language_code), []).append(row)
    return grouped


def _row_source_ids(rows: list[LocalizedOutput]) -> set[int]:
    ids: set[int] = set()
    for row in rows:
        try:
            source_record_id = int(row.source_record_id)
        except Exception:
            continue
        if source_record_id > 0:
            ids.add(source_record_id)
    return ids


def _storage_payload(
    *,
    known_ids_by_surface: dict[str, set[int]],
    localized_rows: list[LocalizedOutput],
    issues: _IssueCollector,
) -> dict[str, Any]:
    orphan_total = 0
    unknown_total = 0
    for row in localized_rows:
        source_kind = str(row.source_kind or "").strip()
        surface = _SURFACE_BY_SOURCE_KIND.get(source_kind)
        source_record_id = int(row.source_record_id or 0)
        if surface is None:
            unknown_total += 1
            issues.add(
                "unknown_localized_source_kind",
                {
                    "source_kind": str(row.source_kind or ""),
                    "source_record_id": source_record_id,
                    "language_code": str(row.language_code or ""),
                },
            )
            continue
        if source_record_id not in known_ids_by_surface[surface]:
            orphan_total += 1
            issues.add(
                "orphan_localized_output",
                {
                    "surface": surface,
                    "source_kind": source_kind,
                    "source_record_id": source_record_id,
                    "language_code": str(row.language_code or ""),
                },
            )
    return {
        "localized_outputs_total": len(localized_rows),
        "orphan_total": orphan_total,
        "unknown_source_kind_total": unknown_total,
    }


def _resolve_materialized_output_dir(
    *, request: LocalizationAuditRequest
) -> Path | None:
    if request.materialized_output_dir is not None:
        return request.materialized_output_dir.expanduser().resolve()
    if request.settings is None:
        return None
    markdown_output_dir = getattr(request.settings, "markdown_output_dir", None)
    return Path(markdown_output_dir).expanduser().resolve() if markdown_output_dir else None


def _resolve_site_output_dir(*, request: LocalizationAuditRequest) -> Path | None:
    if request.site_output_dir is not None:
        return request.site_output_dir.expanduser().resolve()
    materialized_output_dir = _resolve_materialized_output_dir(request=request)
    return materialized_output_dir / "site" if materialized_output_dir is not None else None


def _materialized_payload(
    *,
    output_dir: Path | None,
    site_languages: list[dict[str, str]],
    issues: _IssueCollector,
) -> dict[str, Any]:
    if output_dir is None:
        return _skipped_peer_payload(reason="no_materialized_output_dir")
    if not output_dir.exists():
        issues.add(
            "materialized_output_dir_missing",
            {"output_dir": str(output_dir)},
        )
        return _skipped_peer_payload(
            status="missing",
            output_dir=output_dir,
            reason="materialized_output_dir_missing",
        )
    surfaces: dict[str, Any] = {}
    missing_peer_total = 0
    for surface, spec in _SURFACE_SPECS.items():
        files_by_slug: dict[str, set[str]] = {}
        surface_payload: dict[str, Any] = {}
        for language in site_languages:
            root = _materialized_language_root(
                output_dir=output_dir,
                language=language,
            )
            relative_files = _materialized_relative_files(
                root=root,
                directory_name=spec["materialized_dir"],
            )
            files_by_slug[language["slug"]] = relative_files
            surface_payload[language["code"]] = {
                "language_slug": language["slug"],
                "files_total": len(relative_files),
                "root": str(root),
            }
        missing_peer_total += _record_peer_missing_issues(
            issue_code="materialized_missing_peer",
            surface=surface,
            files_by_slug=files_by_slug,
            languages=site_languages,
            issues=issues,
        )
        surfaces[surface] = surface_payload
    return {
        "status": "ok",
        "output_dir": str(output_dir),
        "surfaces": surfaces,
        "missing_peer_total": missing_peer_total,
    }


def _skipped_peer_payload(
    *, reason: str, status: str = "skipped", output_dir: Path | None = None
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "status": status,
        "reason": reason,
        "surfaces": {},
        "missing_peer_total": 0,
    }
    if output_dir is not None:
        payload["output_dir"] = str(output_dir)
    return payload


def _materialized_language_root(
    *, output_dir: Path, language: dict[str, str]
) -> Path:
    if language.get("role") == "source":
        return output_dir
    return output_dir / "Localized" / language["slug"]


def _materialized_relative_files(*, root: Path, directory_name: str) -> set[str]:
    surface_dir = root / directory_name
    if not surface_dir.exists() or not surface_dir.is_dir():
        return set()
    return {
        f"{directory_name}/{path.name}"
        for path in surface_dir.glob("*.md")
        if path.is_file()
    }


def _record_peer_missing_issues(
    *,
    issue_code: str,
    surface: str,
    files_by_slug: dict[str, set[str]],
    languages: list[dict[str, str]],
    issues: _IssueCollector,
) -> int:
    if len(languages) < 2:
        return 0
    peer_universe: set[str] = set()
    for relative_files in files_by_slug.values():
        peer_universe.update(relative_files)
    missing_total = 0
    for language in languages:
        language_slug = language["slug"]
        for relative_path in sorted(peer_universe - files_by_slug.get(language_slug, set())):
            missing_total += 1
            issues.add(
                issue_code,
                {
                    "surface": surface,
                    "language_code": language["code"],
                    "language_slug": language_slug,
                    "relative_path": relative_path,
                },
            )
    return missing_total


def _site_payload(
    *,
    output_dir: Path | None,
    site_languages: list[dict[str, str]],
    issues: _IssueCollector,
) -> dict[str, Any]:
    if output_dir is None:
        return _skipped_peer_payload(reason="no_site_output_dir")
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.exists():
        issues.add(
            "site_manifest_missing",
            {"output_dir": str(output_dir), "manifest_path": str(manifest_path)},
        )
        return _skipped_peer_payload(
            status="missing",
            output_dir=output_dir,
            reason="site_manifest_missing",
        )
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.add(
            "site_manifest_invalid",
            {"manifest_path": str(manifest_path), "error_type": type(exc).__name__},
        )
        return _skipped_peer_payload(
            status="invalid",
            output_dir=output_dir,
            reason="site_manifest_invalid",
        )
    if not isinstance(manifest, dict):
        issues.add("site_manifest_invalid", {"manifest_path": str(manifest_path)})
        return _skipped_peer_payload(
            status="invalid",
            output_dir=output_dir,
            reason="site_manifest_invalid",
        )

    manifest_languages = [
        str(language_slug)
        for language_slug in manifest.get("languages", [])
        if str(language_slug).strip()
    ]
    for language in site_languages:
        if manifest_languages and language["slug"] not in manifest_languages:
            issues.add(
                "site_manifest_language_missing",
                {
                    "language_code": language["code"],
                    "language_slug": language["slug"],
                },
            )
    files_by_language = _site_files_by_language(
        manifest=manifest,
        site_languages=site_languages,
    )
    surfaces: dict[str, Any] = {}
    missing_peer_total = 0
    for surface, spec in _SURFACE_SPECS.items():
        files_by_slug = {
            language["slug"]: _site_relative_files(
                files_by_language=files_by_language,
                language_slug=language["slug"],
                files_key=spec["site_files_key"],
            )
            for language in site_languages
        }
        missing_peer_total += _record_peer_missing_issues(
            issue_code="site_missing_peer",
            surface=surface,
            files_by_slug=files_by_slug,
            languages=site_languages,
            issues=issues,
        )
        surfaces[surface] = {
            language["code"]: {
                "language_slug": language["slug"],
                "pages_total": len(files_by_slug[language["slug"]]),
            }
            for language in site_languages
        }
    return {
        "status": "ok",
        "output_dir": str(output_dir),
        "manifest_path": str(manifest_path),
        "languages": manifest_languages,
        "surfaces": surfaces,
        "link_map": _site_link_map_payload(output_dir=output_dir, issues=issues),
        "missing_peer_total": missing_peer_total,
    }


def _site_link_map_payload(
    *, output_dir: Path, issues: _IssueCollector
) -> dict[str, Any]:
    artifact_path = output_dir.parent / f".{output_dir.name}-email-links.json"
    if not artifact_path.exists():
        issues.add(
            "site_link_map_missing",
            {"artifact_path": str(artifact_path)},
        )
        return {"status": "missing", "artifact_path": str(artifact_path)}
    try:
        payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues.add(
            "site_link_map_invalid",
            {"artifact_path": str(artifact_path), "error_type": type(exc).__name__},
        )
        return {"status": "invalid", "artifact_path": str(artifact_path)}
    if not isinstance(payload, dict):
        issues.add(
            "site_link_map_invalid",
            {"artifact_path": str(artifact_path)},
        )
        return {"status": "invalid", "artifact_path": str(artifact_path)}

    recorded_output_dir = str(payload.get("site_output_dir") or "").strip()
    matches_site_output_dir = True
    if recorded_output_dir and recorded_output_dir != str(output_dir):
        matches_site_output_dir = False
        issues.add(
            "site_link_map_mismatch",
            {
                "artifact_path": str(artifact_path),
                "recorded_output_dir": recorded_output_dir,
                "site_output_dir": str(output_dir),
            },
        )
    pages_by_source = payload.get("pages_by_source_markdown") or {}
    topic_pages_by_language = payload.get("topic_pages_by_language") or {}
    return {
        "status": "ok" if matches_site_output_dir else "mismatch",
        "artifact_path": str(artifact_path),
        "matches_site_output_dir": matches_site_output_dir,
        "recorded_output_dir": recorded_output_dir or None,
        "site_output_dir": str(output_dir),
        "pages_by_source_markdown_total": len(pages_by_source)
        if isinstance(pages_by_source, dict)
        else 0,
        "topic_pages_by_language_total": len(topic_pages_by_language)
        if isinstance(topic_pages_by_language, dict)
        else 0,
    }


def _site_files_by_language(
    *, manifest: dict[str, Any], site_languages: list[dict[str, str]]
) -> dict[str, dict[str, Any]]:
    files = manifest.get("files")
    files_by_language = files.get("by_language") if isinstance(files, dict) else None
    if isinstance(files_by_language, dict):
        return {
            str(language_slug): dict(language_files)
            for language_slug, language_files in files_by_language.items()
            if isinstance(language_files, dict)
        }
    default_slug = _default_manifest_language_slug(
        manifest=manifest,
        site_languages=site_languages,
    )
    return {default_slug: dict(files)} if isinstance(files, dict) else {}


def _default_manifest_language_slug(
    *, manifest: dict[str, Any], site_languages: list[dict[str, str]]
) -> str:
    raw_default = str(manifest.get("default_language_code") or "").strip()
    if raw_default:
        return _language_slug(raw_default)
    if site_languages:
        return site_languages[0]["slug"]
    return "default"


def _site_relative_files(
    *, files_by_language: dict[str, dict[str, Any]], language_slug: str, files_key: str
) -> set[str]:
    language_files = files_by_language.get(language_slug) or {}
    raw_files = language_files.get(files_key) or []
    if not isinstance(raw_files, list):
        return set()
    return {str(value).replace("\\", "/").lstrip("./") for value in raw_files}
