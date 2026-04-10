from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
import hashlib
import html
import json
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup
from markdown_it import MarkdownIt

from recoleta.config import Settings
from recoleta.delivery import ResendBatchSender
from recoleta.models import (
    DELIVERY_CHANNEL_EMAIL,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.publish.trend_render_shared import _trend_date_token
from recoleta.site import (
    TrendSiteInputSpec,
    _discover_trend_site_input_dirs,
    _load_trend_source_documents,
    _resolve_site_local_markdown_target,
    _topic_slug,
    language_slug_from_code,
)
from recoleta.site_email_links import (
    email_links_artifact_path,
    load_email_links_artifact,
)


EMAIL_RENDERER_VERSION = "trend-email-v1"


@dataclass(frozen=True, slots=True)
class TrendEmailPreviewResult:
    preview_dir: Path
    manifest_path: Path
    html_path: Path
    text_path: Path
    content_hash: str
    primary_page_url: str
    subject: str
    instance: str | None
    trend_doc_id: int
    period_token: str


@dataclass(frozen=True, slots=True)
class TrendEmailSendResult:
    status: str
    send_dir: Path
    manifest_path: Path
    html_path: Path
    text_path: Path
    content_hash: str
    primary_page_url: str
    subject: str
    instance: str | None
    trend_doc_id: int
    period_token: str


@dataclass(frozen=True, slots=True)
class _TrendEmailCandidate:
    trend_doc_id: int
    title: str
    granularity: str
    period_start: datetime
    period_end: datetime | None
    period_token: str
    markdown_path: Path
    presentation: dict[str, Any]
    topics: list[str]
    instance: str | None
    language_code: str | None


@dataclass(frozen=True, slots=True)
class _ResolvedEvidenceEntry:
    title: str
    url: str
    reason: str | None


@dataclass(frozen=True, slots=True)
class _RenderedCluster:
    title: str
    content_markdown: str
    content_html: str
    content_text: str
    evidence: list[_ResolvedEvidenceEntry]


@dataclass(frozen=True, slots=True)
class _TrendEmailBundle:
    trend_doc_id: int
    instance: str | None
    granularity: str
    period_start: datetime
    period_end: datetime | None
    period_token: str
    language_code: str | None
    title: str
    overview_markdown: str
    overview_html: str
    overview_text: str
    topics: list[str]
    topic_links: list[dict[str, str]]
    clusters: list[_RenderedCluster]
    primary_relative_path: str
    primary_page_url: str
    source_markdown_path: Path
    subject: str
    content_hash: str


def _normalized_email_config(settings: Settings) -> Any:
    email = settings.email
    if email is None:
        raise ValueError("EMAIL config is required for trend email commands")
    return email


def _default_site_language_code(settings: Settings) -> str | None:
    localization = getattr(settings, "localization", None)
    if localization is None:
        return None
    normalized = str(
        getattr(localization, "site_default_language_code", "") or ""
    ).strip()
    return normalized or None


def _normalized_language_filter(settings: Settings) -> tuple[str | None, bool]:
    email = _normalized_email_config(settings)
    explicit = str(email.language_code or "").strip() or None
    if explicit is not None:
        return explicit, True
    return _default_site_language_code(settings), False


def _load_trend_email_links(*, site_output_dir: Path) -> dict[str, Any]:
    artifact_path = email_links_artifact_path(site_output_dir=site_output_dir)
    if not artifact_path.exists():
        raise RuntimeError(
            f"email link-map artifact not found: {artifact_path}"
        )
    return load_email_links_artifact(artifact_path=artifact_path)


def _public_url(*, settings: Settings, relative_path: str) -> str:
    email = _normalized_email_config(settings)
    normalized = str(relative_path or "").replace("\\", "/").lstrip("./")
    return f"{email.public_site_url}/{normalized}"


def _period_start_for_anchor(*, granularity: str, anchor_date: date) -> date:
    normalized = str(granularity or "").strip().lower()
    if normalized == "day":
        return anchor_date
    if normalized == "week":
        return anchor_date - timedelta(days=anchor_date.weekday())
    if normalized == "month":
        return anchor_date.replace(day=1)
    return anchor_date


def _site_input_root(settings: Settings) -> Path:
    return Path(settings.markdown_output_dir).expanduser().resolve()


def _select_trend_candidate(
    *,
    settings: Settings,
    anchor_date: date | None,
) -> _TrendEmailCandidate:
    email = _normalized_email_config(settings)
    language_filter, language_filter_is_explicit = _normalized_language_filter(settings)
    input_dirs = _discover_trend_site_input_dirs(
        [TrendSiteInputSpec(path=_site_input_root(settings))]
    )
    source_documents = _load_trend_source_documents(input_dirs=input_dirs)
    target_period_start = (
        _period_start_for_anchor(granularity=email.granularity, anchor_date=anchor_date)
        if anchor_date is not None
        else None
    )
    candidates: list[_TrendEmailCandidate] = []
    for source_document in source_documents:
        if source_document.presentation is None:
            continue
        if source_document.granularity != email.granularity:
            continue
        if source_document.period_start is None:
            continue
        trend_doc_id = int(source_document.frontmatter.get("trend_doc_id") or 0)
        if trend_doc_id <= 0:
            continue
        presentation_language = str(
            source_document.presentation.get("language_code")
            or source_document.frontmatter.get("language_code")
            or source_document.frontmatter.get("lang")
            or ""
        ).strip() or None
        if language_filter is not None:
            if language_filter_is_explicit:
                if presentation_language != language_filter:
                    continue
            elif presentation_language is not None and presentation_language != language_filter:
                continue
        period_token = _trend_date_token(
            granularity=source_document.granularity,
            period_start=source_document.period_start,
        )
        if target_period_start is not None and (
            source_document.period_start.astimezone(UTC).date() != target_period_start
        ):
            continue
        content = (
            source_document.presentation.get("content")
            if isinstance(source_document.presentation.get("content"), dict)
            else {}
        )
        assert isinstance(content, dict)
        title = str(
            content.get("title")
            or source_document.frontmatter.get("title")
            or source_document.markdown_path.stem
        ).strip() or source_document.markdown_path.stem
        candidates.append(
            _TrendEmailCandidate(
                trend_doc_id=trend_doc_id,
                title=title,
                granularity=source_document.granularity,
                period_start=source_document.period_start,
                period_end=source_document.period_end,
                period_token=period_token,
                markdown_path=source_document.markdown_path.resolve(),
                presentation=source_document.presentation,
                topics=list(source_document.topics),
                instance=str(source_document.instance or "").strip() or None,
                language_code=presentation_language,
            )
        )

    if not candidates:
        raise RuntimeError("no matching trend email candidate found")
    candidates.sort(
        key=lambda candidate: (
            candidate.period_start,
            candidate.markdown_path.name,
        ),
        reverse=True,
    )
    return candidates[0]


def _absolute_page_url_from_markdown(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    markdown_path: Path,
) -> tuple[str, str] | tuple[None, None]:
    pages_by_source_markdown = links_artifact.get("pages_by_source_markdown") or {}
    if not isinstance(pages_by_source_markdown, dict):
        return None, None
    relative_path = pages_by_source_markdown.get(str(markdown_path.resolve()))
    normalized_relative_path = str(relative_path or "").strip()
    if not normalized_relative_path:
        return None, None
    return normalized_relative_path, _public_url(
        settings=settings,
        relative_path=normalized_relative_path,
    )


def _render_markdown_html(*, markdown_text: Any) -> str:
    normalized = str(markdown_text or "").strip()
    if not normalized:
        return ""
    return MarkdownIt("commonmark", {"html": True, "typographer": True}).render(
        normalized
    )


def _render_markdown_with_site_links(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    source_markdown_path: Path,
    markdown_text: Any,
) -> tuple[str, str]:
    rendered_html = _render_markdown_html(markdown_text=markdown_text)
    if not rendered_html:
        return "", ""
    soup = BeautifulSoup(rendered_html, "html.parser")
    for anchor in soup.find_all("a", href=True):
        href = str(anchor.get("href") or "")
        target_path = _resolve_site_local_markdown_target(
            source_markdown_path=source_markdown_path,
            href=href,
        )
        if target_path is None:
            continue
        _relative_path, public_url = _absolute_page_url_from_markdown(
            settings=settings,
            links_artifact=links_artifact,
            markdown_path=target_path,
        )
        if public_url is not None:
            anchor["href"] = public_url
    normalized_html = str(soup)
    normalized_text = BeautifulSoup(normalized_html, "html.parser").get_text(
        " ",
        strip=True,
    )
    return normalized_html, normalized_text


def _resolve_evidence_entry(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    source_markdown_path: Path,
    entry: dict[str, Any],
) -> _ResolvedEvidenceEntry | None:
    title = str(entry.get("title") or "").strip() or "Evidence"
    href = str(entry.get("href") or "").strip()
    url = str(entry.get("url") or "").strip()
    resolved_url = url
    if href:
        target_path = _resolve_site_local_markdown_target(
            source_markdown_path=source_markdown_path,
            href=href,
        )
        if target_path is not None:
            _relative_path, public_url = _absolute_page_url_from_markdown(
                settings=settings,
                links_artifact=links_artifact,
                markdown_path=target_path,
            )
            if public_url is not None:
                resolved_url = public_url
        elif "://" in href:
            resolved_url = href
    resolved_url = str(resolved_url or "").strip()
    if not resolved_url:
        return None
    reason = str(entry.get("reason") or "").strip() or None
    return _ResolvedEvidenceEntry(title=title, url=resolved_url, reason=reason)


def _resolve_topic_links(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    topics: list[str],
    language_code: str | None,
) -> list[dict[str, str]]:
    language_slug = language_slug_from_code(language_code)
    topic_pages_by_language = links_artifact.get("topic_pages_by_language") or {}
    scoped_topic_pages: dict[str, Any] = {}
    if (
        language_slug
        and isinstance(topic_pages_by_language, dict)
        and isinstance(topic_pages_by_language.get(language_slug), dict)
    ):
        scoped_topic_pages = dict(topic_pages_by_language.get(language_slug) or {})
    if not scoped_topic_pages:
        raw_topic_pages = links_artifact.get("topic_pages_by_slug") or {}
        if isinstance(raw_topic_pages, dict):
            scoped_topic_pages = dict(raw_topic_pages)

    links: list[dict[str, str]] = []
    for topic in topics:
        slug = _topic_slug(topic)
        relative_path = str(scoped_topic_pages.get(slug) or "").strip()
        if not relative_path:
            continue
        links.append(
            {
                "label": topic,
                "url": _public_url(settings=settings, relative_path=relative_path),
            }
        )
    return links


def _build_email_subject(
    *,
    settings: Settings,
    granularity: str,
    period_token: str,
    instance: str | None,
) -> str:
    email = _normalized_email_config(settings)
    prefix = str(email.subject_prefix or "").strip()
    instance_segment = f"[{instance}]" if instance else ""
    parts = [prefix + instance_segment if prefix else instance_segment]
    parts.append(f"{granularity.title()} trends · {period_token}")
    return " ".join(part for part in parts if part).strip()


def _canonical_bundle_payload(bundle: _TrendEmailBundle, *, settings: Settings) -> dict[str, Any]:
    email = _normalized_email_config(settings)
    return {
        "renderer_version": EMAIL_RENDERER_VERSION,
        "trend_doc_id": bundle.trend_doc_id,
        "granularity": bundle.granularity,
        "period_start": bundle.period_start.astimezone(UTC).isoformat(),
        "period_end": (
            bundle.period_end.astimezone(UTC).isoformat()
            if bundle.period_end is not None
            else None
        ),
        "period_token": bundle.period_token,
        "language_code": bundle.language_code,
        "instance": bundle.instance,
        "title": bundle.title,
        "overview": bundle.overview_text,
        "topics": bundle.topics,
        "topic_links": bundle.topic_links,
        "primary_page_url": bundle.primary_page_url,
        "source_markdown_path": str(bundle.source_markdown_path),
        "max_clusters": int(email.max_clusters),
        "max_evidence_per_cluster": int(email.max_evidence_per_cluster),
        "clusters": [
            {
                "title": cluster.title,
                "content": cluster.content_text,
                "evidence": [
                    {
                        "title": entry.title,
                        "url": entry.url,
                        "reason": entry.reason,
                    }
                    for entry in cluster.evidence
                ],
            }
            for cluster in bundle.clusters
        ],
    }


def _hash_payload(payload: dict[str, Any]) -> str:
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _render_meta_rows(bundle: _TrendEmailBundle) -> list[tuple[str, str]]:
    period_end = (
        bundle.period_end.astimezone(UTC).date().isoformat()
        if bundle.period_end
        else None
    )
    window_value = bundle.period_start.astimezone(UTC).date().isoformat()
    if period_end is not None:
        window_value = f"{window_value} to {period_end}"
    rows = [("Window", window_value), ("Language", bundle.language_code or "default")]
    if bundle.instance:
        rows.append(("Instance", bundle.instance))
    if bundle.topics:
        rows.append(("Topics", ", ".join(bundle.topics[:4])))
    return rows


def _render_cluster_card(cluster: _RenderedCluster) -> str:
    evidence_html = ""
    if cluster.evidence:
        evidence_html = (
            "<div style='margin-top:18px'>"
            "<div style='font:600 11px/1.4 Arial,sans-serif;color:#58708a;text-transform:uppercase;letter-spacing:0.08em;margin:0 0 10px'>Evidence</div>"
            + "".join(
                (
                    "<div style='margin:0 0 8px'>"
                    f"<a href='{html.escape(entry.url, quote=True)}' style='color:#16538c;text-decoration:none;font:600 15px/1.5 Arial,sans-serif'>{html.escape(entry.title)}</a>"
                    + (
                        f"<div style='font:400 13px/1.6 Arial,sans-serif;color:#4f647a;margin-top:2px'>{html.escape(entry.reason)}</div>"
                        if entry.reason
                        else ""
                    )
                    + "</div>"
                )
                for entry in cluster.evidence
            )
            + "</div>"
        )
    return (
        "<tr><td style='padding:0 0 16px'>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse;border:1px solid #d7e2ec;border-radius:18px;background:#f7fbff'>"
        "<tr><td style='padding:22px 24px'>"
        "<div style='font:600 11px/1.4 Arial,sans-serif;color:#58708a;text-transform:uppercase;letter-spacing:0.08em;margin:0 0 10px'>Cluster</div>"
        f"<h3 style='margin:0 0 12px;font:600 22px/1.2 Georgia,Times New Roman,serif;color:#10273f'>{html.escape(cluster.title)}</h3>"
        f"<div style='font:400 16px/1.75 Arial,sans-serif;color:#18324a'>{cluster.content_html}</div>"
        f"{evidence_html}"
        "</td></tr></table></td></tr>"
    )


def _render_html_email(*, bundle: _TrendEmailBundle, settings: Settings) -> str:
    trends_index_relative_path = "trends/index.html"
    primary_parts = Path(bundle.primary_relative_path).parts
    if len(primary_parts) >= 2 and primary_parts[1] == "trends":
        trends_index_relative_path = str(Path(primary_parts[0]) / "trends" / "index.html")
    meta_html = "".join(
        (
            "<tr>"
            f"<td style='padding:0 8px 8px 0;font:600 11px/1.4 Arial,sans-serif;color:#58708a;text-transform:uppercase;letter-spacing:0.08em'>{html.escape(label)}</td>"
            f"<td style='padding:0 0 8px;font:400 14px/1.5 Arial,sans-serif;color:#18324a'>{html.escape(value)}</td>"
            "</tr>"
        )
        for label, value in _render_meta_rows(bundle)
    )
    cluster_cards = "".join(_render_cluster_card(cluster) for cluster in bundle.clusters)
    topic_cta = ""
    if bundle.topic_links:
        topic_cta = " ".join(
            f"<a href='{html.escape(topic['url'], quote=True)}' style='color:#16538c;text-decoration:none;font:600 13px/1.4 Arial,sans-serif'>{html.escape(topic['label'])}</a>"
            for topic in bundle.topic_links[:3]
        )
    return (
        "<!doctype html>"
        "<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
        f"<title>{html.escape(bundle.subject)}</title>"
        "</head>"
        "<body style='margin:0;padding:0;background:#edf3f8'>"
        "<div style='display:none;max-height:0;overflow:hidden;opacity:0;color:transparent'>"
        f"{html.escape(bundle.overview_text[:120])}"
        "</div>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse;background:#edf3f8'>"
        "<tr><td align='center' style='padding:24px'>"
        "<table role='presentation' width='640' cellspacing='0' cellpadding='0' style='width:100%;max-width:640px;border-collapse:collapse'>"
        "<tr><td style='padding:0 0 16px'>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse;background:#10273f;border-radius:28px'>"
        "<tr><td style='padding:30px 32px'>"
        f"<div style='font:600 11px/1.4 Arial,sans-serif;color:#d2e6fb;text-transform:uppercase;letter-spacing:0.08em;margin:0 0 12px'>{html.escape((bundle.instance + ' · ') if bundle.instance else '')}{html.escape(bundle.granularity.title())} trends · {html.escape(bundle.period_token)}</div>"
        f"<h1 style='margin:0 0 14px;font:600 34px/1.12 Georgia,Times New Roman,serif;color:#ffffff'>{html.escape(bundle.title)}</h1>"
        f"<div style='font:400 16px/1.7 Arial,sans-serif;color:#dbe9f6;margin:0 0 20px'>{html.escape(bundle.overview_text[:180])}</div>"
        f"<a href='{html.escape(bundle.primary_page_url, quote=True)}' style='display:inline-block;background:#f7fbff;color:#10273f;text-decoration:none;font:600 14px/1 Arial,sans-serif;padding:12px 18px;border-radius:999px'>Open on site</a>"
        "</td></tr></table></td></tr>"
        "<tr><td style='padding:0 0 16px'>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse;border:1px solid #d7e2ec;border-radius:18px;background:#ffffff'>"
        f"<tr><td style='padding:22px 24px'><table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse'>{meta_html}</table></td></tr>"
        "</table></td></tr>"
        "<tr><td style='padding:0 0 16px'>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse;border:1px solid #d7e2ec;border-radius:18px;background:#ffffff'>"
        "<tr><td style='padding:24px'>"
        "<div style='font:600 11px/1.4 Arial,sans-serif;color:#58708a;text-transform:uppercase;letter-spacing:0.08em;margin:0 0 10px'>Overview</div>"
        f"<div style='font:400 16px/1.75 Arial,sans-serif;color:#18324a'>{bundle.overview_html}</div>"
        "</td></tr></table></td></tr>"
        f"{cluster_cards}"
        "<tr><td style='padding:4px 0 0'>"
        "<table role='presentation' width='100%' cellspacing='0' cellpadding='0' style='border-collapse:collapse'>"
        "<tr><td style='padding:0 0 10px'>"
        f"<a href='{html.escape(bundle.primary_page_url, quote=True)}' style='display:inline-block;background:#16538c;color:#ffffff;text-decoration:none;font:600 14px/1 Arial,sans-serif;padding:12px 18px;border-radius:999px;margin-right:10px'>Open trend page</a>"
        "</td></tr>"
        "<tr><td style='font:400 13px/1.7 Arial,sans-serif;color:#4f647a'>"
        f"<a href='{html.escape(_public_url(settings=settings, relative_path=trends_index_relative_path), quote=True)}' style='color:#16538c;text-decoration:none'>Open trends index</a>"
        + (f" · {topic_cta}" if topic_cta else "")
        + "</td></tr>"
        "</table></td></tr>"
        "</table></td></tr></table></body></html>"
    )


def _render_text_email(bundle: _TrendEmailBundle) -> str:
    lines = [
        bundle.subject,
        bundle.primary_page_url,
        "",
        bundle.title,
        "",
        bundle.overview_text,
    ]
    for label, value in _render_meta_rows(bundle):
        lines.append(f"{label}: {value}")
    if bundle.clusters:
        lines.append("")
        lines.append("Clusters")
        for cluster in bundle.clusters:
            lines.append(f"- {cluster.title}")
            lines.append(f"  {cluster.content_text}")
            for entry in cluster.evidence:
                lines.append(f"  Evidence: {entry.title} — {entry.url}")
                if entry.reason:
                    lines.append(f"  Why: {entry.reason}")
    if bundle.topic_links:
        lines.append("")
        lines.append(
            "Topics: "
            + ", ".join(
                f"{topic['label']} ({topic['url']})" for topic in bundle.topic_links
            )
        )
    return "\n".join(lines).strip() + "\n"


def _build_email_bundle(
    *,
    settings: Settings,
    site_output_dir: Path,
    anchor_date: date | None,
) -> _TrendEmailBundle:
    email = _normalized_email_config(settings)
    links_artifact = _load_trend_email_links(site_output_dir=site_output_dir)
    candidate = _select_trend_candidate(settings=settings, anchor_date=anchor_date)
    primary_relative_path, primary_page_url = _absolute_page_url_from_markdown(
        settings=settings,
        links_artifact=links_artifact,
        markdown_path=candidate.markdown_path,
    )
    if primary_relative_path is None or primary_page_url is None:
        raise RuntimeError(
            f"site link-map does not contain trend page for {candidate.markdown_path}"
        )

    content = (
        candidate.presentation.get("content")
        if isinstance(candidate.presentation.get("content"), dict)
        else {}
    )
    assert isinstance(content, dict)
    overview_markdown = str(content.get("overview") or "").strip()
    overview_html, overview_text = _render_markdown_with_site_links(
        settings=settings,
        links_artifact=links_artifact,
        source_markdown_path=candidate.markdown_path,
        markdown_text=overview_markdown,
    )
    clusters: list[_RenderedCluster] = []
    for raw_cluster in list(content.get("clusters") or [])[: int(email.max_clusters)]:
        if not isinstance(raw_cluster, dict):
            continue
        cluster_markdown = str(raw_cluster.get("content") or "").strip()
        cluster_html, cluster_text = _render_markdown_with_site_links(
            settings=settings,
            links_artifact=links_artifact,
            source_markdown_path=candidate.markdown_path,
            markdown_text=cluster_markdown,
        )
        evidence = [
            resolved
            for resolved in (
                _resolve_evidence_entry(
                    settings=settings,
                    links_artifact=links_artifact,
                    source_markdown_path=candidate.markdown_path,
                    entry=entry,
                )
                for entry in list(raw_cluster.get("evidence") or [])[
                    : int(email.max_evidence_per_cluster)
                ]
                if isinstance(entry, dict)
            )
            if resolved is not None
        ]
        clusters.append(
            _RenderedCluster(
                title=str(raw_cluster.get("title") or "").strip() or "Cluster",
                content_markdown=cluster_markdown,
                content_html=cluster_html,
                content_text=cluster_text,
                evidence=evidence,
            )
        )

    topic_links = _resolve_topic_links(
        settings=settings,
        links_artifact=links_artifact,
        topics=candidate.topics,
        language_code=candidate.language_code,
    )
    subject = _build_email_subject(
        settings=settings,
        granularity=candidate.granularity,
        period_token=candidate.period_token,
        instance=candidate.instance,
    )
    bundle = _TrendEmailBundle(
        trend_doc_id=candidate.trend_doc_id,
        instance=candidate.instance,
        granularity=candidate.granularity,
        period_start=candidate.period_start,
        period_end=candidate.period_end,
        period_token=candidate.period_token,
        language_code=candidate.language_code,
        title=candidate.title,
        overview_markdown=overview_markdown,
        overview_html=overview_html,
        overview_text=overview_text,
        topics=candidate.topics,
        topic_links=topic_links,
        clusters=clusters,
        primary_relative_path=primary_relative_path,
        primary_page_url=primary_page_url,
        source_markdown_path=candidate.markdown_path,
        subject=subject,
        content_hash="",
    )
    content_hash = _hash_payload(_canonical_bundle_payload(bundle, settings=settings))
    return _TrendEmailBundle(
        trend_doc_id=bundle.trend_doc_id,
        instance=bundle.instance,
        granularity=bundle.granularity,
        period_start=bundle.period_start,
        period_end=bundle.period_end,
        period_token=bundle.period_token,
        language_code=bundle.language_code,
        title=bundle.title,
        overview_markdown=bundle.overview_markdown,
        overview_html=bundle.overview_html,
        overview_text=bundle.overview_text,
        topics=bundle.topics,
        topic_links=bundle.topic_links,
        clusters=bundle.clusters,
        primary_relative_path=bundle.primary_relative_path,
        primary_page_url=bundle.primary_page_url,
        source_markdown_path=bundle.source_markdown_path,
        subject=bundle.subject,
        content_hash=content_hash,
    )


def _preview_dir_for_bundle(
    *,
    settings: Settings,
    bundle: _TrendEmailBundle,
    output_dir: Path | None,
) -> Path:
    if output_dir is not None:
        return output_dir.expanduser().resolve()
    return (
        Path(settings.markdown_output_dir).expanduser().resolve()
        / ".recoleta-email"
        / "previews"
        / f"{bundle.granularity}--{bundle.period_token}--trend--{bundle.trend_doc_id}"
    )


def _send_dir_for_bundle(*, settings: Settings, bundle: _TrendEmailBundle) -> Path:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return (
        Path(settings.markdown_output_dir).expanduser().resolve()
        / ".recoleta-email"
        / "sends"
        / f"{timestamp}--{bundle.granularity}--{bundle.period_token}--trend--{bundle.trend_doc_id}"
    )


def _write_email_artifacts(
    *,
    artifact_dir: Path,
    bundle: _TrendEmailBundle,
    settings: Settings,
    provider_outcomes: list[dict[str, Any]] | None,
    kind: str,
) -> tuple[Path, Path, Path]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    html_path = artifact_dir / "body.html"
    text_path = artifact_dir / "body.txt"
    manifest_path = artifact_dir / "manifest.json"
    html_body = _render_html_email(bundle=bundle, settings=settings)
    text_body = _render_text_email(bundle)
    html_path.write_text(html_body, encoding="utf-8")
    text_path.write_text(text_body, encoding="utf-8")
    manifest_path.write_text(
        json.dumps(
            {
                "kind": kind,
                "renderer_version": EMAIL_RENDERER_VERSION,
                "trend_doc_id": bundle.trend_doc_id,
                "instance": bundle.instance,
                "granularity": bundle.granularity,
                "period_token": bundle.period_token,
                "primary_page_url": bundle.primary_page_url,
                "content_hash": bundle.content_hash,
                "subject": bundle.subject,
                "source_markdown_path": str(bundle.source_markdown_path),
                "recipients": list(_normalized_email_config(settings).to),
                "provider_outcomes": provider_outcomes or [],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return html_path, text_path, manifest_path


def build_trend_email_preview(
    *,
    settings: Settings,
    site_output_dir: Path,
    anchor_date: date | None = None,
    output_dir: Path | None = None,
) -> TrendEmailPreviewResult:
    bundle = _build_email_bundle(
        settings=settings,
        site_output_dir=site_output_dir.expanduser().resolve(),
        anchor_date=anchor_date,
    )
    preview_dir = _preview_dir_for_bundle(
        settings=settings,
        bundle=bundle,
        output_dir=output_dir,
    )
    html_path, text_path, manifest_path = _write_email_artifacts(
        artifact_dir=preview_dir,
        bundle=bundle,
        settings=settings,
        provider_outcomes=None,
        kind="preview",
    )
    return TrendEmailPreviewResult(
        preview_dir=preview_dir,
        manifest_path=manifest_path,
        html_path=html_path,
        text_path=text_path,
        content_hash=bundle.content_hash,
        primary_page_url=bundle.primary_page_url,
        subject=bundle.subject,
        instance=bundle.instance,
        trend_doc_id=bundle.trend_doc_id,
        period_token=bundle.period_token,
    )


def _default_url_checker(url: str) -> bool:
    request = Request(url, method="HEAD")
    try:
        with urlopen(request, timeout=10) as response:
            return int(getattr(response, "status", 200) or 200) < 400
    except HTTPError as exc:
        if exc.code == 405:
            with urlopen(url, timeout=10) as response:
                return int(getattr(response, "status", 200) or 200) < 400
        return False
    except (OSError, URLError):
        return False


def _email_from_header(settings: Settings) -> str:
    email = _normalized_email_config(settings)
    if str(email.from_name or "").strip():
        return f"{email.from_name} <{email.from_email}>"
    return email.from_email


def send_trend_email(
    *,
    settings: Settings,
    repository: Any,
    site_output_dir: Path,
    sender: Any | None = None,
    url_checker: Callable[[str], bool] | None = None,
    anchor_date: date | None = None,
    force_batch: bool = False,
) -> TrendEmailSendResult:
    bundle = _build_email_bundle(
        settings=settings,
        site_output_dir=site_output_dir.expanduser().resolve(),
        anchor_date=anchor_date,
    )
    check_url = url_checker or _default_url_checker
    if not check_url(bundle.primary_page_url):
        raise RuntimeError(
            f"public trend page is not reachable: {bundle.primary_page_url}"
        )

    email = _normalized_email_config(settings)
    existing_rows = repository.list_trend_deliveries(
        doc_id=bundle.trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
        destinations=list(email.to),
    )
    row_by_destination = {row.destination: row for row in existing_rows}
    current_sent = {
        destination: bool(
            destination in row_by_destination
            and row_by_destination[destination].status == DELIVERY_STATUS_SENT
            and row_by_destination[destination].content_hash == bundle.content_hash
        )
        for destination in email.to
    }
    if all(current_sent.values()) and not force_batch:
        send_dir = _send_dir_for_bundle(settings=settings, bundle=bundle)
        html_path, text_path, manifest_path = _write_email_artifacts(
            artifact_dir=send_dir,
            bundle=bundle,
            settings=settings,
            provider_outcomes=[],
            kind="send-skipped",
        )
        return TrendEmailSendResult(
            status="skipped",
            send_dir=send_dir,
            manifest_path=manifest_path,
            html_path=html_path,
            text_path=text_path,
            content_hash=bundle.content_hash,
            primary_page_url=bundle.primary_page_url,
            subject=bundle.subject,
            instance=bundle.instance,
            trend_doc_id=bundle.trend_doc_id,
            period_token=bundle.period_token,
        )
    if any(current_sent.values()) and not all(current_sent.values()) and not force_batch:
        raise RuntimeError("mixed_batch_state")

    resolved_sender = sender
    if resolved_sender is None:
        if settings.resend_api_key is None:
            raise ValueError("RECOLETA_RESEND_API_KEY is required for email send")
        resolved_sender = ResendBatchSender(
            api_key=settings.resend_api_key.get_secret_value()
        )
    emails = [
        {
            "from": _email_from_header(settings),
            "to": destination,
            "subject": bundle.subject,
            "html": _render_html_email(bundle=bundle, settings=settings),
            "text": _render_text_email(bundle),
        }
        for destination in email.to
    ]
    idempotency_key = f"trend-email:{bundle.trend_doc_id}:{bundle.content_hash}"
    if force_batch:
        idempotency_key = (
            f"{idempotency_key}:force:{datetime.now(UTC).strftime('%Y%m%dT%H%M%SZ')}"
        )
    outcomes = resolved_sender.send_batch(
        emails=emails,
        idempotency_key=idempotency_key,
    )
    for outcome in outcomes:
        destination = str(outcome.get("destination") or "").strip()
        if not destination:
            continue
        error = str(outcome.get("error") or "").strip() or None
        repository.upsert_trend_delivery(
            doc_id=bundle.trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=bundle.content_hash,
            message_id=str(outcome.get("message_id") or "").strip() or None,
            status=DELIVERY_STATUS_FAILED if error else DELIVERY_STATUS_SENT,
            error=error,
        )
    send_dir = _send_dir_for_bundle(settings=settings, bundle=bundle)
    html_path, text_path, manifest_path = _write_email_artifacts(
        artifact_dir=send_dir,
        bundle=bundle,
        settings=settings,
        provider_outcomes=outcomes,
        kind="send",
    )
    all_failed = all(str(outcome.get("error") or "").strip() for outcome in outcomes)
    status = "failed" if outcomes and all_failed else "sent"
    return TrendEmailSendResult(
        status=status,
        send_dir=send_dir,
        manifest_path=manifest_path,
        html_path=html_path,
        text_path=text_path,
        content_hash=bundle.content_hash,
        primary_page_url=bundle.primary_page_url,
        subject=bundle.subject,
        instance=bundle.instance,
        trend_doc_id=bundle.trend_doc_id,
        period_token=bundle.period_token,
    )
