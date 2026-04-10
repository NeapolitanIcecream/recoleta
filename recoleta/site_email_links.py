from __future__ import annotations

from collections.abc import Sequence
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any


EMAIL_LINKS_SCHEMA_VERSION = 1


def email_links_artifact_path(*, site_output_dir: Path) -> Path:
    resolved_output_dir = site_output_dir.expanduser().resolve()
    return resolved_output_dir.parent / f".{resolved_output_dir.name}-email-links.json"


def _normalize_relative_path(value: str | Path) -> str:
    return str(value).replace("\\", "/").lstrip("./")


def build_email_links_artifact_payload(
    *,
    site_output_dir: Path,
    pages_by_source_markdown: dict[str, str | Path],
    topic_pages_by_slug: dict[str, str | Path],
    topic_pages_by_language: dict[str, dict[str, str | Path]] | None = None,
) -> dict[str, Any]:
    return {
        "schema_version": EMAIL_LINKS_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).isoformat(),
        "site_output_dir": str(site_output_dir.expanduser().resolve()),
        "pages_by_source_markdown": {
            str(Path(source_markdown).expanduser().resolve()): _normalize_relative_path(
                relative_path
            )
            for source_markdown, relative_path in sorted(
                pages_by_source_markdown.items()
            )
        },
        "topic_pages_by_slug": {
            str(slug): _normalize_relative_path(relative_path)
            for slug, relative_path in sorted(topic_pages_by_slug.items())
        },
        "topic_pages_by_language": {
            str(language_slug): {
                str(slug): _normalize_relative_path(relative_path)
                for slug, relative_path in sorted(topic_pages.items())
            }
            for language_slug, topic_pages in sorted(
                (topic_pages_by_language or {}).items()
            )
        },
    }


def write_email_links_artifact(
    *,
    site_output_dir: Path,
    pages_by_source_markdown: dict[str, str | Path],
    topic_pages_by_slug: dict[str, str | Path],
    topic_pages_by_language: dict[str, dict[str, str | Path]] | None = None,
) -> Path:
    artifact_path = email_links_artifact_path(site_output_dir=site_output_dir)
    payload = build_email_links_artifact_payload(
        site_output_dir=site_output_dir,
        pages_by_source_markdown=pages_by_source_markdown,
        topic_pages_by_slug=topic_pages_by_slug,
        topic_pages_by_language=topic_pages_by_language,
    )
    artifact_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return artifact_path


def load_email_links_artifact(*, artifact_path: Path) -> dict[str, Any]:
    return json.loads(artifact_path.expanduser().resolve().read_text(encoding="utf-8"))


def _language_relative_path(*, language_slug: str, relative_path: str | Path) -> str:
    return f"{language_slug}/{_normalize_relative_path(relative_path)}"


def aggregate_multilingual_email_links(
    *,
    output_dir: Path,
    language_slugs: Sequence[str],
    default_language_slug: str,
) -> dict[str, Any]:
    resolved_output_dir = output_dir.expanduser().resolve()
    pages_by_source_markdown: dict[str, str] = {}
    topic_pages_by_slug: dict[str, str] = {}
    topic_pages_by_language: dict[str, dict[str, str]] = {}
    for language_slug in language_slugs:
        child_links = load_email_links_artifact(
            artifact_path=resolved_output_dir / f".{language_slug}-email-links.json"
        )
        child_pages = child_links.get("pages_by_source_markdown") or {}
        if isinstance(child_pages, dict):
            pages_by_source_markdown.update(
                {
                    str(source_markdown): _language_relative_path(
                        language_slug=language_slug,
                        relative_path=relative_path,
                    )
                    for source_markdown, relative_path in child_pages.items()
                }
            )
        child_topic_pages = child_links.get("topic_pages_by_slug") or {}
        if not isinstance(child_topic_pages, dict):
            continue
        namespaced_topic_pages = {
            str(slug): _language_relative_path(
                language_slug=language_slug,
                relative_path=relative_path,
            )
            for slug, relative_path in child_topic_pages.items()
        }
        topic_pages_by_language[language_slug] = namespaced_topic_pages
        if language_slug == default_language_slug:
            topic_pages_by_slug.update(namespaced_topic_pages)
    return {
        "pages_by_source_markdown": pages_by_source_markdown,
        "topic_pages_by_slug": topic_pages_by_slug,
        "topic_pages_by_language": topic_pages_by_language,
    }


def remove_child_email_links_artifacts(
    *,
    output_dir: Path,
    language_slugs: Sequence[str],
) -> None:
    resolved_output_dir = output_dir.expanduser().resolve()
    for language_slug in language_slugs:
        try:
            (resolved_output_dir / f".{language_slug}-email-links.json").unlink()
        except FileNotFoundError:
            pass
