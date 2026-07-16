from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen
from uuid import uuid4

from bs4 import BeautifulSoup, Comment
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
)
from recoleta.site_email_links import (
    email_links_artifact_path,
    load_email_links_artifact,
)


EMAIL_RENDERER_VERSION = "trend-email-v3"
RESEND_BATCH_MAX_RECIPIENTS = 100
_EMAIL_COLOR_CANVAS = "#f5f6f8"
_EMAIL_COLOR_PAPER = "#ffffff"
_EMAIL_COLOR_INK = "#172033"
_EMAIL_COLOR_TEXT = "#354052"
_EMAIL_COLOR_MUTED = "#5f6875"
_EMAIL_COLOR_LINE = "#e2e5ea"
_EMAIL_COLOR_LINE_STRONG = "#c8ced6"
_EMAIL_COLOR_ACCENT = "#145da0"
_EMAIL_COLOR_ON_ACCENT = "#ffffff"
_EMAIL_FONT_SANS = (
    "-apple-system,BlinkMacSystemFont,Segoe UI,PingFang SC,Microsoft YaHei,"
    "Noto Sans CJK SC,Arial,Helvetica,sans-serif"
)
_EMAIL_FONT_SERIF = (
    "Songti SC,STSong,Noto Serif CJK SC,Georgia,Times New Roman,SimSun,serif"
)
_ALLOWED_EMAIL_GRANULARITIES = {"day", "week", "month"}
_EMAIL_MARKDOWN_TAGS = {
    "a",
    "blockquote",
    "br",
    "code",
    "em",
    "hr",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "ul",
}
_EMAIL_MARKDOWN_DANGEROUS_TAGS = {
    "embed",
    "iframe",
    "math",
    "object",
    "script",
    "style",
    "svg",
    "template",
}
_RTL_LANGUAGE_CODES = {"ar", "fa", "he", "ur"}
_EMAIL_COPY = {
    "en": {
        "brief": "Research brief",
        "day": "Daily brief",
        "week": "Weekly brief",
        "month": "Monthly brief",
        "findings": "Findings",
        "sources": "Sources",
        "read_full": "Read the full brief",
        "full_brief": "Full brief",
        "source": "Source",
    },
    "zh-CN": {
        "brief": "研究简报",
        "day": "日度简报",
        "week": "周度简报",
        "month": "月度简报",
        "findings": "研究发现",
        "sources": "资料来源",
        "read_full": "阅读完整报告",
        "full_brief": "完整报告",
        "source": "来源",
    },
    "zh-TW": {
        "brief": "研究簡報",
        "day": "日度簡報",
        "week": "週度簡報",
        "month": "月度簡報",
        "findings": "研究發現",
        "sources": "資料來源",
        "read_full": "閱讀完整報告",
        "full_brief": "完整報告",
        "source": "來源",
    },
    "ja": {
        "brief": "リサーチ速報",
        "day": "日次速報",
        "week": "週次速報",
        "month": "月次速報",
        "findings": "主な発見",
        "sources": "情報源",
        "read_full": "レポート全文を読む",
        "full_brief": "レポート全文",
        "source": "情報源",
    },
    "ko": {
        "brief": "리서치 브리프",
        "day": "일간 브리프",
        "week": "주간 브리프",
        "month": "월간 브리프",
        "findings": "주요 발견",
        "sources": "출처",
        "read_full": "전체 보고서 읽기",
        "full_brief": "전체 보고서",
        "source": "출처",
    },
}


@dataclass(frozen=True, slots=True)
class TrendEmailPreviewEntryResult:
    granularity: str
    preview_dir: Path
    manifest_path: Path
    html_path: Path
    text_path: Path
    content_hash: str
    primary_page_url: str
    subject: str
    trend_doc_id: int
    period_token: str


@dataclass(frozen=True, slots=True)
class TrendEmailPreviewBatchResult:
    status: str
    preview_root_dir: Path
    batch_manifest_path: Path
    instance: str | None
    results: list[TrendEmailPreviewEntryResult]


@dataclass(frozen=True, slots=True)
class TrendEmailSendEntryResult:
    status: str
    granularity: str
    send_dir: Path | None
    manifest_path: Path | None
    html_path: Path | None
    text_path: Path | None
    content_hash: str | None
    primary_page_url: str | None
    subject: str | None
    trend_doc_id: int | None
    period_token: str | None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class TrendEmailSendBatchResult:
    status: str
    send_root_dir: Path
    batch_manifest_path: Path
    instance: str | None
    results: list[TrendEmailSendEntryResult]


@dataclass(frozen=True, slots=True)
class TrendEmailSendRequest:
    site_output_dir: Path
    sender: Any | None = None
    url_checker: Callable[[str], bool] | None = None
    anchor_date: date | None = None
    force_batch: bool = False
    granularities: list[str] | None = None


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


@dataclass(frozen=True, slots=True)
class _RenderedCluster:
    title: str
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
    overview_html: str
    overview_text: str
    display_labels: dict[str, str]
    clusters: list[_RenderedCluster]
    primary_relative_path: str
    primary_page_url: str
    source_markdown_path: Path
    subject: str
    content_hash: str


@dataclass(slots=True)
class _PreparedSendBundle:
    granularity: str
    bundle: _TrendEmailBundle | None
    status: str
    current_failed: dict[str, bool] = field(default_factory=dict)
    error: str | None = None
    outcomes: list[dict[str, Any]] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class _SendPreflightContext:
    settings: Settings
    repository: Any
    destinations: list[str]
    force_batch: bool
    url_checker: Callable[[str], bool] | None


@dataclass(frozen=True, slots=True)
class _EmailArtifactWriteRequest:
    settings: Settings
    kind: str
    entry_status: str | None
    provider_outcomes: list[dict[str, Any]] | None
    error: str | None = None


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
        return _normalized_email_language_code(explicit), True
    default_language = _default_site_language_code(settings)
    return (
        _normalized_email_language_code(default_language)
        if default_language is not None
        else None,
        False,
    )


def _load_trend_email_links(*, site_output_dir: Path) -> dict[str, Any]:
    artifact_path = email_links_artifact_path(site_output_dir=site_output_dir)
    if not artifact_path.exists():
        raise RuntimeError(f"email link-map artifact not found: {artifact_path}")
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


def _presentation_content_map(presentation: dict[str, Any]) -> dict[str, Any]:
    content = (
        presentation.get("content")
        if isinstance(presentation.get("content"), dict)
        else {}
    )
    assert isinstance(content, dict)
    return content


def _source_document_presentation_language(source_document: Any) -> str | None:
    language_code = (
        str(
            source_document.presentation.get("language_code")
            or source_document.frontmatter.get("language_code")
            or source_document.frontmatter.get("lang")
            or ""
        ).strip()
        or None
    )
    return (
        _normalized_email_language_code(language_code)
        if language_code is not None
        else None
    )


def _matches_language_filter(
    *,
    presentation_language: str | None,
    language_filter: str | None,
    language_filter_is_explicit: bool,
) -> bool:
    if language_filter is None:
        return True
    if language_filter_is_explicit:
        return presentation_language == language_filter
    return presentation_language in {None, language_filter}


def _matches_anchor_period(
    *,
    period_start: datetime,
    target_period_start: date | None,
) -> bool:
    if target_period_start is None:
        return True
    return period_start.astimezone(UTC).date() == target_period_start


def _candidate_title(*, source_document: Any, content: dict[str, Any]) -> str:
    return (
        str(
            content.get("title")
            or source_document.frontmatter.get("title")
            or source_document.markdown_path.stem
        ).strip()
        or source_document.markdown_path.stem
    )


def _candidate_from_source_document(
    *,
    source_document: Any,
    granularity: str,
    language_filter: str | None,
    language_filter_is_explicit: bool,
    target_period_start: date | None,
) -> _TrendEmailCandidate | None:
    if source_document.presentation is None:
        return None
    if source_document.granularity != granularity or source_document.period_start is None:
        return None
    trend_doc_id = int(source_document.frontmatter.get("trend_doc_id") or 0)
    if trend_doc_id <= 0:
        return None
    presentation_language = _source_document_presentation_language(source_document)
    if not _matches_language_filter(
        presentation_language=presentation_language,
        language_filter=language_filter,
        language_filter_is_explicit=language_filter_is_explicit,
    ):
        return None
    if not _matches_anchor_period(
        period_start=source_document.period_start,
        target_period_start=target_period_start,
    ):
        return None
    content = _presentation_content_map(source_document.presentation)
    return _TrendEmailCandidate(
        trend_doc_id=trend_doc_id,
        title=_candidate_title(source_document=source_document, content=content),
        granularity=source_document.granularity,
        period_start=source_document.period_start,
        period_end=source_document.period_end,
        period_token=_trend_date_token(
            granularity=source_document.granularity,
            period_start=source_document.period_start,
        ),
        markdown_path=source_document.markdown_path.resolve(),
        presentation=source_document.presentation,
        topics=list(source_document.topics),
        instance=str(source_document.instance or "").strip() or None,
        language_code=presentation_language,
    )


def _normalize_requested_granularity(value: Any) -> str:
    normalized = str(value or "").strip().lower()
    if normalized not in _ALLOWED_EMAIL_GRANULARITIES:
        raise ValueError("--granularity must be one of: day, week, month")
    return normalized


def _resolved_email_granularities(
    *,
    settings: Settings,
    selected_granularities: list[str] | tuple[str, ...] | None,
) -> list[str]:
    email = _normalized_email_config(settings)
    configured = list(email.granularities)
    if not selected_granularities:
        return configured

    requested: list[str] = []
    seen: set[str] = set()
    for value in selected_granularities:
        normalized = _normalize_requested_granularity(value)
        if normalized in seen:
            continue
        seen.add(normalized)
        requested.append(normalized)
    missing = [value for value in requested if value not in configured]
    if missing:
        missing_display = ", ".join(missing)
        raise ValueError(
            "requested --granularity values are not configured in "
            f"EMAIL.granularities: {missing_display}"
        )
    return [value for value in configured if value in seen]


def _select_trend_candidate(
    *,
    settings: Settings,
    anchor_date: date | None,
    granularity: str,
) -> _TrendEmailCandidate:
    language_filter, language_filter_is_explicit = _normalized_language_filter(settings)
    input_dirs = _discover_trend_site_input_dirs(
        [TrendSiteInputSpec(path=_site_input_root(settings))]
    )
    source_documents = _load_trend_source_documents(input_dirs=input_dirs)
    target_period_start = (
        _period_start_for_anchor(granularity=granularity, anchor_date=anchor_date)
        if anchor_date is not None
        else None
    )
    candidates = [
        candidate
        for source_document in source_documents
        if (
            candidate := _candidate_from_source_document(
                source_document=source_document,
                granularity=granularity,
                language_filter=language_filter,
                language_filter_is_explicit=language_filter_is_explicit,
                target_period_start=target_period_start,
            )
        )
        is not None
    ]
    if not candidates:
        raise RuntimeError(
            f"no matching trend email candidate found for granularity={granularity}"
        )
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
    rendered = MarkdownIt("commonmark", {"html": True, "typographer": True}).render(
        normalized
    )
    soup = BeautifulSoup(rendered, "html.parser")
    for comment in soup.find_all(string=lambda value: isinstance(value, Comment)):
        comment.extract()
    for tag in list(soup.find_all(_EMAIL_MARKDOWN_DANGEROUS_TAGS)):
        tag.decompose()
    for tag in list(soup.find_all(True)):
        if tag.name not in _EMAIL_MARKDOWN_TAGS:
            tag.unwrap()
            continue
        if tag.name == "a":
            href = str(tag.get("href") or "").strip()
            try:
                scheme = urlsplit(href).scheme.lower()
            except ValueError:
                href = ""
                scheme = ""
            tag.attrs = (
                {"href": href}
                if href and scheme in {"", "http", "https", "mailto"}
                else {}
            )
            continue
        tag.attrs = {}
    return str(soup)


def _style_markdown_fragment(soup: BeautifulSoup, *, direction: str) -> None:
    base_text_style = (
        f"margin:0 0 16px;font-family:{_EMAIL_FONT_SANS};"
        "font-size:16px;line-height:27px;mso-line-height-rule:at-least;"
        f"color:{_EMAIL_COLOR_TEXT};word-break:break-word"
    )
    for paragraph in soup.find_all("p"):
        paragraph["style"] = base_text_style
    for anchor in soup.find_all("a"):
        anchor["style"] = (
            f"color:{_EMAIL_COLOR_ACCENT};text-decoration:underline;"
            "text-underline-offset:2px;"
            "word-break:break-word"
        )
    list_padding = "0 24px 0 0" if direction == "rtl" else "0 0 0 24px"
    for listing in soup.find_all(["ul", "ol"]):
        listing["style"] = (
            f"margin:0 0 16px;padding:{list_padding};"
            f"font-family:{_EMAIL_FONT_SANS};"
            "font-size:16px;line-height:27px;mso-line-height-rule:at-least;"
            f"color:{_EMAIL_COLOR_TEXT}"
        )
    for item in soup.find_all("li"):
        item["style"] = "margin:0 0 8px;padding:0"
    quote_edge = (
        f"padding:0 16px 0 0;border-right:3px solid {_EMAIL_COLOR_ACCENT}"
        if direction == "rtl"
        else f"padding:0 0 0 16px;border-left:3px solid {_EMAIL_COLOR_ACCENT}"
    )
    for quote in soup.find_all("blockquote"):
        quote["style"] = f"margin:0 0 16px;{quote_edge};color:{_EMAIL_COLOR_TEXT}"
    for preformatted in soup.find_all("pre"):
        preformatted["style"] = (
            f"margin:0 0 16px;padding:12px;background:{_EMAIL_COLOR_CANVAS};"
            "white-space:pre-wrap;"
            "font-family:Menlo,Consolas,monospace;font-size:14px;line-height:22px;"
            f"mso-line-height-rule:at-least;color:{_EMAIL_COLOR_TEXT};"
            "word-break:break-word"
        )
    for code in soup.find_all("code"):
        if code.parent is not None and code.parent.name == "pre":
            continue
        code["style"] = (
            "font-family:Menlo,Consolas,monospace;font-size:14px;line-height:22px;"
            f"background:{_EMAIL_COLOR_CANVAS};color:{_EMAIL_COLOR_TEXT}"
        )


def _render_markdown_with_site_links(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    source_markdown_path: Path,
    markdown_text: Any,
    direction: str,
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
    _style_markdown_fragment(soup, direction=direction)
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
    return _ResolvedEvidenceEntry(title=title, url=resolved_url)


def _source_url_dedup_key(url: str) -> str:
    normalized = str(url or "").strip()
    try:
        parts = urlsplit(normalized)
        hostname = parts.hostname
        normalized_netloc = parts.netloc
        if hostname is not None:
            userinfo = ""
            if "@" in parts.netloc:
                userinfo = parts.netloc.rsplit("@", 1)[0] + "@"
            normalized_host = hostname.casefold()
            if ":" in normalized_host:
                normalized_host = f"[{normalized_host}]"
            port = parts.port
            normalized_netloc = (
                f"{userinfo}{normalized_host}"
                + (f":{port}" if port is not None else "")
            )
        return urlunsplit(
            (
                parts.scheme.casefold(),
                normalized_netloc,
                parts.path,
                parts.query,
                "",
            )
        )
    except ValueError:
        return normalized.split("#", 1)[0]


def _build_email_subject(
    *,
    settings: Settings,
    title: str,
    instance: str | None,
) -> str:
    email = _normalized_email_config(settings)
    prefix = str(email.subject_prefix or "").strip()
    normalized_title = " ".join(str(title or "").split()).strip()
    _ = instance
    parts = [prefix, normalized_title]
    return " ".join(part for part in parts if part).strip()


def _canonical_bundle_payload(
    bundle: _TrendEmailBundle, *, settings: Settings
) -> dict[str, Any]:
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
        "subject": bundle.subject,
        "overview_html": bundle.overview_html,
        "display_labels": bundle.display_labels,
        "primary_page_url": bundle.primary_page_url,
        "max_findings": min(int(email.max_clusters), 3),
        "max_sources_per_finding": min(int(email.max_evidence_per_cluster), 2),
        "clusters": [
            {
                "title": cluster.title,
                "content_html": cluster.content_html,
                "evidence": [
                    {
                        "title": entry.title,
                        "url": entry.url,
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


def _normalized_email_language_code(language_code: str | None) -> str:
    normalized = str(language_code or "").strip().replace("_", "-")
    if not re.fullmatch(r"[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*", normalized):
        return "en"
    parts = normalized.split("-")
    canonical = [parts[0].lower()]
    for part in parts[1:]:
        if len(part) == 4 and part.isalpha():
            canonical.append(part.title())
        elif (len(part) == 2 and part.isalpha()) or (
            len(part) == 3 and part.isdigit()
        ):
            canonical.append(part.upper())
        else:
            canonical.append(part.lower())
    return "-".join(canonical)


def _email_locale_key(language_code: str | None) -> str:
    normalized = _normalized_email_language_code(language_code)
    parts = normalized.casefold().split("-")
    primary = parts[0]
    if primary == "zh" and (
        "hant" in parts or any(region in parts for region in {"hk", "mo", "tw"})
    ):
        return "zh-TW"
    if primary == "zh":
        return "zh-CN"
    if primary == "ja":
        return "ja"
    if primary == "ko":
        return "ko"
    return "en"


def _email_language_code(language_code: str | None) -> str:
    return _normalized_email_language_code(language_code)


def _email_direction(language_code: str | None) -> str:
    language = _email_language_code(language_code).split("-", 1)[0].lower()
    return "rtl" if language in _RTL_LANGUAGE_CODES else "ltr"


def _email_copy_for(bundle: _TrendEmailBundle) -> dict[str, str]:
    copy = dict(_EMAIL_COPY[_email_locale_key(bundle.language_code)])
    legacy_english = {
        "clusters": {"Clusters", "Findings"},
        "evidence": {"Evidence", "Sources"},
    }
    for source_key, copy_key in (("clusters", "findings"), ("evidence", "sources")):
        label = str(bundle.display_labels.get(source_key) or "").strip()
        if not label:
            continue
        if label in legacy_english[source_key]:
            continue
        copy[copy_key] = label
    return copy


def _email_period_line(bundle: _TrendEmailBundle, copy: dict[str, str]) -> str:
    granularity_label = copy.get(bundle.granularity, copy["brief"])
    parts = [bundle.instance, granularity_label, bundle.period_token]
    return " · ".join(str(part).strip() for part in parts if str(part or "").strip())


def _email_preheader(bundle: _TrendEmailBundle, copy: dict[str, str]) -> str:
    finding_count = len(bundle.clusters)
    first_title = bundle.clusters[0].title if bundle.clusters else bundle.title
    if finding_count == 0:
        separator = "：" if _email_locale_key(bundle.language_code) in {
            "zh-CN",
            "zh-TW",
            "ja",
        } else ": "
        return f"{copy['brief']}{separator}{bundle.title}"
    if _email_locale_key(bundle.language_code) == "zh-CN":
        return f"本期{finding_count}项研究发现：{first_title}"
    if _email_locale_key(bundle.language_code) == "zh-TW":
        return f"本期 {finding_count} 項研究發現：{first_title}"
    if _email_locale_key(bundle.language_code) == "ja":
        return f"{finding_count}件の発見：{first_title}"
    if _email_locale_key(bundle.language_code) == "ko":
        return f"주요 발견 {finding_count}건: {first_title}"
    noun = "finding" if finding_count == 1 else "findings"
    return f"{finding_count} {noun}: {first_title}"


def _render_email_button(
    *,
    url: str,
    label: str,
) -> str:
    height = 44
    width = 200
    horizontal_padding = 20
    html_content_width = width - (horizontal_padding * 2)
    background = _EMAIL_COLOR_ACCENT
    foreground = _EMAIL_COLOR_ON_ACCENT
    url_attr = html.escape(url, quote=True)
    label_html = html.escape(label)
    anchor_style = (
        f"display:inline-block;background:{background};color:{foreground};"
        f"text-decoration:none;font-family:{_EMAIL_FONT_SANS};"
        f"width:{html_content_width}px;text-align:center;"
        "font-size:16px;font-weight:700;line-height:44px;"
        f"padding:0 {horizontal_padding}px;border-radius:4px;mso-hide:all"
    )
    return (
        "<!--[if mso]>"
        '<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" '
        'xmlns:w="urn:schemas-microsoft-com:office:word" '
        f'href="{url_attr}" '
        f'style="height:{height}px;v-text-anchor:middle;width:{width}px;" '
        f'arcsize="18%" stroke="f" fillcolor="{background}">'
        "<w:anchorlock/>"
        f"<center style='color:{foreground};font-family:{_EMAIL_FONT_SANS};"
        f"font-size:16px;font-weight:700'>{label_html}</center>"
        "</v:roundrect>"
        "<![endif]-->"
        "<!--[if !mso]><!-->"
        f"<a href='{url_attr}' style='{anchor_style}'>{label_html}</a>"
        "<!--<![endif]-->"
    )


def _render_finding(
    cluster: _RenderedCluster,
    *,
    index: int,
    copy: dict[str, str],
) -> str:
    sources_html = ""
    if cluster.evidence:
        sources_html = (
            "<div data-section='sources' style='margin:18px 0 0'>"
            f"<h4 style='margin:0 0 8px;font-family:{_EMAIL_FONT_SANS};font-size:16px;line-height:24px;mso-line-height-rule:at-least;font-weight:700;color:{_EMAIL_COLOR_TEXT}'>{html.escape(copy['sources'])}</h4>"
            + "".join(
                (
                    f"<div style='margin:0 0 7px;font-family:{_EMAIL_FONT_SANS};font-size:16px;line-height:24px;mso-line-height-rule:at-least'>"
                    f"<a href='{html.escape(entry.url, quote=True)}' style='color:{_EMAIL_COLOR_ACCENT};text-decoration:underline;text-underline-offset:2px;word-break:break-word'>{html.escape(entry.title)}</a>"
                    "</div>"
                )
                for entry in cluster.evidence
            )
            + "</div>"
        )
    section_style = "margin:0;padding:0 0 28px"
    if index > 0:
        section_style += f";border-top:1px solid {_EMAIL_COLOR_LINE};padding-top:28px"
    return (
        f"<div style='{section_style}'>"
        f"<h3 style='margin:0 0 12px;font-family:{_EMAIL_FONT_SERIF};font-size:22px;line-height:29px;mso-line-height-rule:at-least;font-weight:700;color:{_EMAIL_COLOR_INK}'>{html.escape(cluster.title)}</h3>"
        f"<div>{cluster.content_html}</div>"
        f"{sources_html}"
        "</div>"
    )


def _render_html_email(*, bundle: _TrendEmailBundle) -> str:
    copy = _email_copy_for(bundle)
    language_code = _email_language_code(bundle.language_code)
    direction = _email_direction(bundle.language_code)
    period_line = _email_period_line(bundle, copy)
    preheader = _email_preheader(bundle, copy)
    findings_html = "".join(
        _render_finding(cluster, index=index, copy=copy)
        for index, cluster in enumerate(bundle.clusters)
    )
    findings_section = ""
    if findings_html:
        findings_section = (
            "<div style='margin:26px 0 0'>"
            f"<h2 style='margin:0 0 22px;font-family:{_EMAIL_FONT_SANS};font-size:18px;line-height:26px;mso-line-height-rule:at-least;font-weight:700;color:{_EMAIL_COLOR_INK}'>{html.escape(copy['findings'])}</h2>"
            f"{findings_html}"
            "</div>"
        )
    return (
        "<!doctype html>"
        f"<html lang='{html.escape(language_code, quote=True)}' dir='{direction}'><head>"
        "<meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<meta name='x-apple-disable-message-reformatting'>"
        f"<title>{html.escape(bundle.subject)}</title>"
        "<style>"
        "body,table,td,a{-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%}"
        "table,td{mso-table-lspace:0pt;mso-table-rspace:0pt}"
        "table{border-collapse:collapse!important}"
        "a[x-apple-data-detectors]{color:inherit!important;text-decoration:none!important}"
        "@media only screen and (max-width:480px){"
        ".email-gutter{padding:0!important}.email-shell{width:100%!important}"
        ".email-content{padding:28px 22px!important}"
        ".email-title{font-size:28px!important;line-height:35px!important}"
        "}"
        "</style>"
        "</head>"
        f"<body style='margin:0;padding:0;background:{_EMAIL_COLOR_CANVAS}'>"
        "<div class='preheader' aria-hidden='true' style='display:none!important;max-height:0;max-width:0;overflow:hidden;opacity:0;color:transparent;font-size:1px;line-height:1px'>"
        f"{html.escape(preheader)}"
        "</div>"
        f"<table role='presentation' width='100%' cellspacing='0' cellpadding='0' bgcolor='{_EMAIL_COLOR_CANVAS}' style='width:100%;background:{_EMAIL_COLOR_CANVAS};border-collapse:collapse'>"
        "<tr><td class='email-gutter' align='center' style='padding:24px 12px'>"
        f"<table class='email-shell' role='presentation' width='600' cellspacing='0' cellpadding='0' bgcolor='{_EMAIL_COLOR_PAPER}' style='width:100%;max-width:600px;background:{_EMAIL_COLOR_PAPER};border:1px solid {_EMAIL_COLOR_LINE_STRONG};border-collapse:collapse'>"
        "<tr><td class='email-content' style='padding:42px 48px'>"
        "<div role='article' aria-roledescription='email'>"
        f"<div style='margin:0 0 12px;font-family:{_EMAIL_FONT_SANS};font-size:14px;line-height:21px;mso-line-height-rule:at-least;font-weight:600;color:{_EMAIL_COLOR_MUTED}'>{html.escape(period_line)}</div>"
        f"<h1 class='email-title' style='margin:0 0 22px;font-family:{_EMAIL_FONT_SERIF};font-size:32px;line-height:41px;mso-line-height-rule:at-least;font-weight:700;color:{_EMAIL_COLOR_INK}'>{html.escape(bundle.title)}</h1>"
        f"<div>{bundle.overview_html}</div>"
        f"{findings_section}"
        f"<div style='margin:4px 0 0;padding:28px 0 0;border-top:1px solid {_EMAIL_COLOR_LINE_STRONG}'>"
        f"{_render_email_button(url=bundle.primary_page_url, label=copy['read_full'])}"
        "</div>"
        "</div></td></tr>"
        "</table></td></tr></table></body></html>"
    )


def _render_text_email(bundle: _TrendEmailBundle) -> str:
    copy = _email_copy_for(bundle)
    label_separator = (
        "："
        if _email_locale_key(bundle.language_code) in {"zh-CN", "zh-TW", "ja"}
        else ": "
    )
    lines = [
        bundle.title,
        _email_period_line(bundle, copy),
        "",
        bundle.overview_text,
    ]
    if bundle.clusters:
        lines.append("")
        lines.append(copy["findings"])
        for index, cluster in enumerate(bundle.clusters, start=1):
            lines.append("")
            lines.append(f"{index}. {cluster.title}")
            lines.append(cluster.content_text)
            for entry in cluster.evidence:
                lines.append(
                    f"{copy['source']}{label_separator}{entry.title} — {entry.url}"
                )
    lines.extend(
        ["", f"{copy['full_brief']}{label_separator}{bundle.primary_page_url}"]
    )
    return "\n".join(lines).strip() + "\n"


def _primary_trend_page(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    candidate: _TrendEmailCandidate,
) -> tuple[str, str]:
    primary_relative_path, primary_page_url = _absolute_page_url_from_markdown(
        settings=settings,
        links_artifact=links_artifact,
        markdown_path=candidate.markdown_path,
    )
    if primary_relative_path is None or primary_page_url is None:
        raise RuntimeError(
            f"site link-map does not contain trend page for {candidate.markdown_path}"
        )
    return primary_relative_path, primary_page_url


def _render_overview_section(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    candidate: _TrendEmailCandidate,
    content: dict[str, Any],
) -> tuple[str, str]:
    return _render_markdown_with_site_links(
        settings=settings,
        links_artifact=links_artifact,
        source_markdown_path=candidate.markdown_path,
        markdown_text=str(content.get("overview") or "").strip(),
        direction=_email_direction(candidate.language_code),
    )


def _render_cluster(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    source_markdown_path: Path,
    raw_cluster: dict[str, Any],
    direction: str,
) -> _RenderedCluster:
    cluster_markdown = str(raw_cluster.get("content") or "").strip()
    cluster_html, cluster_text = _render_markdown_with_site_links(
        settings=settings,
        links_artifact=links_artifact,
        source_markdown_path=source_markdown_path,
        markdown_text=cluster_markdown,
        direction=direction,
    )
    evidence = [
        resolved
        for resolved in (
            _resolve_evidence_entry(
                settings=settings,
                links_artifact=links_artifact,
                source_markdown_path=source_markdown_path,
                entry=entry,
            )
            for entry in list(raw_cluster.get("evidence") or [])
            if isinstance(entry, dict)
        )
        if resolved is not None
    ]
    return _RenderedCluster(
        title=str(raw_cluster.get("title") or "").strip() or "Cluster",
        content_html=cluster_html,
        content_text=cluster_text,
        evidence=evidence,
    )


def _render_clusters(
    *,
    settings: Settings,
    links_artifact: dict[str, Any],
    candidate: _TrendEmailCandidate,
    content: dict[str, Any],
) -> list[_RenderedCluster]:
    email = _normalized_email_config(settings)
    max_clusters = min(int(email.max_clusters), 3)
    max_evidence = min(int(email.max_evidence_per_cluster), 2)
    direction = _email_direction(candidate.language_code)
    rendered_clusters = [
        _render_cluster(
            settings=settings,
            links_artifact=links_artifact,
            source_markdown_path=candidate.markdown_path,
            raw_cluster=raw_cluster,
            direction=direction,
        )
        for raw_cluster in list(content.get("clusters") or [])[:max_clusters]
        if isinstance(raw_cluster, dict)
    ]
    seen_source_urls: set[str] = set()
    deduplicated: list[_RenderedCluster] = []
    for cluster in rendered_clusters:
        unique_evidence: list[_ResolvedEvidenceEntry] = []
        for entry in cluster.evidence:
            source_key = _source_url_dedup_key(entry.url)
            if source_key in seen_source_urls:
                continue
            seen_source_urls.add(source_key)
            unique_evidence.append(entry)
            if len(unique_evidence) >= max_evidence:
                break
        deduplicated.append(
            _RenderedCluster(
                title=cluster.title,
                content_html=cluster.content_html,
                content_text=cluster.content_text,
                evidence=unique_evidence,
            )
        )
    return deduplicated


def _presentation_display_labels(presentation: dict[str, Any]) -> dict[str, str]:
    raw_labels = presentation.get("display_labels")
    if not isinstance(raw_labels, dict):
        return {}
    return {
        str(key): str(value).strip()
        for key, value in raw_labels.items()
        if str(key).strip() and str(value).strip()
    }


def _bundle_with_hash(
    *,
    settings: Settings,
    bundle: _TrendEmailBundle,
) -> _TrendEmailBundle:
    return _TrendEmailBundle(
        trend_doc_id=bundle.trend_doc_id,
        instance=bundle.instance,
        granularity=bundle.granularity,
        period_start=bundle.period_start,
        period_end=bundle.period_end,
        period_token=bundle.period_token,
        language_code=bundle.language_code,
        title=bundle.title,
        overview_html=bundle.overview_html,
        overview_text=bundle.overview_text,
        display_labels=bundle.display_labels,
        clusters=bundle.clusters,
        primary_relative_path=bundle.primary_relative_path,
        primary_page_url=bundle.primary_page_url,
        source_markdown_path=bundle.source_markdown_path,
        subject=bundle.subject,
        content_hash=_hash_payload(
            _canonical_bundle_payload(bundle, settings=settings)
        ),
    )


def _build_email_bundle(
    *,
    settings: Settings,
    site_output_dir: Path,
    anchor_date: date | None,
    granularity: str,
) -> _TrendEmailBundle:
    links_artifact = _load_trend_email_links(site_output_dir=site_output_dir)
    candidate = _select_trend_candidate(
        settings=settings,
        anchor_date=anchor_date,
        granularity=granularity,
    )
    primary_relative_path, primary_page_url = _primary_trend_page(
        settings=settings,
        links_artifact=links_artifact,
        candidate=candidate,
    )
    content = _presentation_content_map(candidate.presentation)
    overview_html, overview_text = _render_overview_section(
        settings=settings,
        links_artifact=links_artifact,
        candidate=candidate,
        content=content,
    )
    subject = _build_email_subject(
        settings=settings,
        title=candidate.title,
        instance=candidate.instance,
    )
    return _bundle_with_hash(
        settings=settings,
        bundle=_TrendEmailBundle(
            trend_doc_id=candidate.trend_doc_id,
            instance=candidate.instance,
            granularity=candidate.granularity,
            period_start=candidate.period_start,
            period_end=candidate.period_end,
            period_token=candidate.period_token,
            language_code=candidate.language_code,
            title=candidate.title,
            overview_html=overview_html,
            overview_text=overview_text,
            display_labels=_presentation_display_labels(candidate.presentation),
            clusters=_render_clusters(
                settings=settings,
                links_artifact=links_artifact,
                candidate=candidate,
                content=content,
            ),
            primary_relative_path=primary_relative_path,
            primary_page_url=primary_page_url,
            source_markdown_path=candidate.markdown_path,
            subject=subject,
            content_hash="",
        ),
    )


def _bundle_artifact_dir_name(bundle: _TrendEmailBundle) -> str:
    return f"{bundle.granularity}--{bundle.period_token}--trend--{bundle.trend_doc_id}"


def _unique_invocation_token() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    nonce = uuid4().hex[:8]
    return f"{timestamp}-{nonce}"


def _preview_root_dir(*, settings: Settings, output_dir: Path | None) -> Path:
    if output_dir is not None:
        return output_dir.expanduser().resolve()
    return (
        Path(settings.markdown_output_dir).expanduser().resolve()
        / ".recoleta-email"
        / "previews"
        / _unique_invocation_token()
    )


def _send_root_dir(*, settings: Settings) -> Path:
    return (
        Path(settings.markdown_output_dir).expanduser().resolve()
        / ".recoleta-email"
        / "sends"
        / _unique_invocation_token()
    )


def _write_email_artifacts(
    *,
    artifact_dir: Path,
    bundle: _TrendEmailBundle,
    request: _EmailArtifactWriteRequest,
) -> tuple[Path, Path, Path]:
    artifact_dir.mkdir(parents=True, exist_ok=True)
    html_path = artifact_dir / "body.html"
    text_path = artifact_dir / "body.txt"
    manifest_path = artifact_dir / "manifest.json"
    html_body = _render_html_email(bundle=bundle)
    text_body = _render_text_email(bundle)
    html_path.write_text(html_body, encoding="utf-8")
    text_path.write_text(text_body, encoding="utf-8")
    manifest_payload: dict[str, Any] = {
        "kind": request.kind,
        "renderer_version": EMAIL_RENDERER_VERSION,
        "entry_status": request.entry_status,
        "trend_doc_id": bundle.trend_doc_id,
        "instance": bundle.instance,
        "granularity": bundle.granularity,
        "period_token": bundle.period_token,
        "primary_page_url": bundle.primary_page_url,
        "content_hash": bundle.content_hash,
        "subject": bundle.subject,
        "source_markdown_path": str(bundle.source_markdown_path),
        "recipients": list(_normalized_email_config(request.settings).to),
        "provider_outcomes": request.provider_outcomes or [],
    }
    if request.error is not None:
        manifest_payload["error"] = request.error
    manifest_path.write_text(
        json.dumps(
            manifest_payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return html_path, text_path, manifest_path


def _write_batch_manifest(*, root_dir: Path, payload: dict[str, Any]) -> Path:
    root_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = root_dir / "batch-manifest.json"
    manifest_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def _preview_entry_payload(entry: TrendEmailPreviewEntryResult) -> dict[str, Any]:
    return {
        "granularity": entry.granularity,
        "preview_dir": str(entry.preview_dir),
        "manifest_path": str(entry.manifest_path),
        "html_path": str(entry.html_path),
        "text_path": str(entry.text_path),
        "primary_page_url": entry.primary_page_url,
        "content_hash": entry.content_hash,
        "subject": entry.subject,
        "trend_doc_id": entry.trend_doc_id,
        "period_token": entry.period_token,
    }


def _send_entry_payload(entry: TrendEmailSendEntryResult) -> dict[str, Any]:
    payload = {
        "status": entry.status,
        "granularity": entry.granularity,
        "send_dir": _optional_path_payload(entry.send_dir),
        "manifest_path": _optional_path_payload(entry.manifest_path),
        "html_path": _optional_path_payload(entry.html_path),
        "text_path": _optional_path_payload(entry.text_path),
        "primary_page_url": entry.primary_page_url,
        "content_hash": entry.content_hash,
        "subject": entry.subject,
        "trend_doc_id": entry.trend_doc_id,
        "period_token": entry.period_token,
    }
    if entry.error is not None:
        payload["error"] = entry.error
    return payload


def _instance_for_bundles(bundles: list[_TrendEmailBundle]) -> str | None:
    if not bundles:
        return None
    return bundles[0].instance


def _optional_path_payload(path: Path | None) -> str | None:
    if path is None:
        return None
    return str(path)


def build_trend_email_preview(
    *,
    settings: Settings,
    site_output_dir: Path,
    anchor_date: date | None = None,
    output_dir: Path | None = None,
    granularities: list[str] | tuple[str, ...] | None = None,
) -> TrendEmailPreviewBatchResult:
    selected_granularities = _resolved_email_granularities(
        settings=settings,
        selected_granularities=granularities,
    )
    bundles = [
        _build_email_bundle(
            settings=settings,
            site_output_dir=site_output_dir.expanduser().resolve(),
            anchor_date=anchor_date,
            granularity=granularity,
        )
        for granularity in selected_granularities
    ]

    preview_root_dir = _preview_root_dir(settings=settings, output_dir=output_dir)
    results: list[TrendEmailPreviewEntryResult] = []
    for bundle in bundles:
        preview_dir = preview_root_dir / _bundle_artifact_dir_name(bundle)
        html_path, text_path, manifest_path = _write_email_artifacts(
            artifact_dir=preview_dir,
            bundle=bundle,
            request=_EmailArtifactWriteRequest(
                settings=settings,
                kind="preview",
                entry_status="succeeded",
                provider_outcomes=None,
            ),
        )
        results.append(
            TrendEmailPreviewEntryResult(
                granularity=bundle.granularity,
                preview_dir=preview_dir,
                manifest_path=manifest_path,
                html_path=html_path,
                text_path=text_path,
                content_hash=bundle.content_hash,
                primary_page_url=bundle.primary_page_url,
                subject=bundle.subject,
                trend_doc_id=bundle.trend_doc_id,
                period_token=bundle.period_token,
            )
        )
    batch_manifest_path = _write_batch_manifest(
        root_dir=preview_root_dir,
        payload={
            "kind": "preview-batch",
            "renderer_version": EMAIL_RENDERER_VERSION,
            "status": "succeeded",
            "instance": _instance_for_bundles(bundles),
            "results": [_preview_entry_payload(entry) for entry in results],
        },
    )
    return TrendEmailPreviewBatchResult(
        status="succeeded",
        preview_root_dir=preview_root_dir,
        batch_manifest_path=batch_manifest_path,
        instance=_instance_for_bundles(bundles),
        results=results,
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


def _delivery_status_maps(
    *,
    existing_rows: list[Any],
    destinations: list[str],
    content_hash: str,
) -> tuple[dict[str, bool], dict[str, bool]]:
    row_by_destination = {row.destination: row for row in existing_rows}
    current_sent = {
        destination: bool(
            destination in row_by_destination
            and row_by_destination[destination].status == DELIVERY_STATUS_SENT
            and row_by_destination[destination].content_hash == content_hash
        )
        for destination in destinations
    }
    current_failed = {
        destination: bool(
            destination in row_by_destination
            and row_by_destination[destination].status == DELIVERY_STATUS_FAILED
            and row_by_destination[destination].content_hash == content_hash
        )
        for destination in destinations
    }
    return current_sent, current_failed


def _email_batch_payloads(
    *,
    settings: Settings,
    bundle: _TrendEmailBundle,
    destinations: list[str],
) -> list[dict[str, object]]:
    if len(destinations) > RESEND_BATCH_MAX_RECIPIENTS:
        raise ValueError("EMAIL.to supports at most 100 recipients per Resend batch")
    html_body = _render_html_email(bundle=bundle)
    text_body = _render_text_email(bundle)
    return [
        {
            "from": _email_from_header(settings),
            "to": destination,
            "subject": bundle.subject,
            "html": html_body,
            "text": text_body,
        }
        for destination in destinations
    ]


def _recipient_batch_fingerprint(destinations: list[str]) -> str:
    payload = json.dumps(destinations, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _idempotency_key_for_send(
    *,
    bundle: _TrendEmailBundle,
    destinations: list[str],
    current_failed: dict[str, bool],
    force_batch: bool,
) -> str:
    recipients_token = _recipient_batch_fingerprint(destinations)
    key = (
        f"trend-email:{bundle.trend_doc_id}:{bundle.content_hash}:"
        f"recipients:{recipients_token}"
    )
    if force_batch:
        return f"{key}:force:{_unique_invocation_token()}"
    if current_failed and all(current_failed.values()):
        return f"{key}:retry:{_unique_invocation_token()}"
    return key


def _persist_send_outcomes(
    *,
    repository: Any,
    doc_id: int,
    content_hash: str,
    outcomes: list[dict[str, Any]],
) -> None:
    for outcome in outcomes:
        destination = str(outcome.get("destination") or "").strip()
        if not destination:
            continue
        error = str(outcome.get("error") or "").strip() or None
        repository.upsert_trend_delivery(
            doc_id=doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=content_hash,
            message_id=str(outcome.get("message_id") or "").strip() or None,
            status=DELIVERY_STATUS_FAILED if error else DELIVERY_STATUS_SENT,
            error=error,
        )


def _batch_send_action(
    *,
    current_sent: dict[str, bool],
    force_batch: bool,
) -> str:
    if all(current_sent.values()) and not force_batch:
        return "skip"
    if any(current_sent.values()) and not all(current_sent.values()) and not force_batch:
        raise RuntimeError("mixed_batch_state")
    return "send"


def _ensure_reachable_public_page(
    *,
    bundle: _TrendEmailBundle,
    url_checker: Callable[[str], bool] | None,
) -> None:
    check_url = url_checker or _default_url_checker
    if not check_url(bundle.primary_page_url):
        raise RuntimeError(
            f"public trend page is not reachable: {bundle.primary_page_url}"
        )


def _resolved_email_sender(*, settings: Settings, sender: Any | None) -> Any:
    if sender is not None:
        return sender
    if settings.resend_api_key is None:
        raise ValueError("RECOLETA_RESEND_API_KEY is required for email send")
    return ResendBatchSender(api_key=settings.resend_api_key.get_secret_value())


def _preflight_send_bundle(
    *,
    context: _SendPreflightContext,
    bundle: _TrendEmailBundle,
) -> _PreparedSendBundle:
    existing_rows = context.repository.list_trend_deliveries(
        doc_id=bundle.trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
        destinations=context.destinations,
    )
    current_sent, current_failed = _delivery_status_maps(
        existing_rows=existing_rows,
        destinations=context.destinations,
        content_hash=bundle.content_hash,
    )
    try:
        action = _batch_send_action(
            current_sent=current_sent,
            force_batch=context.force_batch,
        )
    except RuntimeError as exc:
        return _PreparedSendBundle(
            granularity=bundle.granularity,
            bundle=bundle,
            status="preflight_failed",
            current_failed=current_failed,
            error=str(exc),
        )
    if action == "skip":
        return _PreparedSendBundle(
            granularity=bundle.granularity,
            bundle=bundle,
            status="skipped",
            current_failed=current_failed,
        )
    try:
        _email_batch_payloads(
            settings=context.settings,
            bundle=bundle,
            destinations=context.destinations,
        )
        _ensure_reachable_public_page(bundle=bundle, url_checker=context.url_checker)
    except Exception as exc:  # noqa: BLE001
        return _PreparedSendBundle(
            granularity=bundle.granularity,
            bundle=bundle,
            status="preflight_failed",
            current_failed=current_failed,
            error=str(exc),
        )
    return _PreparedSendBundle(
        granularity=bundle.granularity,
        bundle=bundle,
        status="ready_to_send",
        current_failed=current_failed,
    )


def _resolve_send_bundle(
    *,
    context: _SendPreflightContext,
    request: TrendEmailSendRequest,
    granularity: str,
) -> _PreparedSendBundle:
    try:
        bundle = _build_email_bundle(
            settings=context.settings,
            site_output_dir=request.site_output_dir.expanduser().resolve(),
            anchor_date=request.anchor_date,
            granularity=granularity,
        )
    except Exception as exc:  # noqa: BLE001
        return _PreparedSendBundle(
            granularity=granularity,
            bundle=None,
            status="preflight_failed",
            error=str(exc),
        )
    return _preflight_send_bundle(
        context=context,
        bundle=bundle,
    )


def _send_error_from_outcomes(outcomes: list[dict[str, Any]]) -> str:
    for outcome in outcomes:
        error = str(outcome.get("error") or "").strip()
        if error:
            return error
    return "provider send failed"


def _write_send_entry_results(
    *,
    root_dir: Path,
    settings: Settings,
    prepared_bundles: list[_PreparedSendBundle],
) -> list[TrendEmailSendEntryResult]:
    results: list[TrendEmailSendEntryResult] = []
    for prepared in prepared_bundles:
        if prepared.bundle is None:
            results.append(
                TrendEmailSendEntryResult(
                    status=prepared.status,
                    granularity=prepared.granularity,
                    send_dir=None,
                    manifest_path=None,
                    html_path=None,
                    text_path=None,
                    content_hash=None,
                    primary_page_url=None,
                    subject=None,
                    trend_doc_id=None,
                    period_token=None,
                    error=prepared.error,
                )
            )
            continue
        entry_dir = root_dir / _bundle_artifact_dir_name(prepared.bundle)
        html_path, text_path, manifest_path = _write_email_artifacts(
            artifact_dir=entry_dir,
            bundle=prepared.bundle,
            request=_EmailArtifactWriteRequest(
                settings=settings,
                kind="send",
                entry_status=prepared.status,
                provider_outcomes=prepared.outcomes,
                error=prepared.error,
            ),
        )
        results.append(
            TrendEmailSendEntryResult(
                status=prepared.status,
                granularity=prepared.bundle.granularity,
                send_dir=entry_dir,
                manifest_path=manifest_path,
                html_path=html_path,
                text_path=text_path,
                content_hash=prepared.bundle.content_hash,
                primary_page_url=prepared.bundle.primary_page_url,
                subject=prepared.bundle.subject,
                trend_doc_id=prepared.bundle.trend_doc_id,
                period_token=prepared.bundle.period_token,
                error=prepared.error,
            )
        )
    return results


def _send_batch_result(
    *,
    status: str,
    settings: Settings,
    send_root_dir: Path,
    bundles: list[_TrendEmailBundle],
    prepared_bundles: list[_PreparedSendBundle],
) -> TrendEmailSendBatchResult:
    results = _write_send_entry_results(
        root_dir=send_root_dir,
        settings=settings,
        prepared_bundles=prepared_bundles,
    )
    batch_manifest_path = _write_batch_manifest(
        root_dir=send_root_dir,
        payload={
            "kind": "send-batch",
            "renderer_version": EMAIL_RENDERER_VERSION,
            "status": status,
            "instance": _instance_for_bundles(bundles),
            "results": [_send_entry_payload(entry) for entry in results],
        },
    )
    return TrendEmailSendBatchResult(
        status=status,
        send_root_dir=send_root_dir,
        batch_manifest_path=batch_manifest_path,
        instance=_instance_for_bundles(bundles),
        results=results,
    )


def _execute_send_batch(
    *,
    settings: Settings,
    repository: Any,
    request: TrendEmailSendRequest,
    prepared_bundles: list[_PreparedSendBundle],
) -> bool:
    sender = None
    if any(prepared.status == "ready_to_send" for prepared in prepared_bundles):
        sender = _resolved_email_sender(settings=settings, sender=request.sender)
    email = _normalized_email_config(settings)
    for index, prepared in enumerate(prepared_bundles):
        if prepared.status != "ready_to_send":
            continue
        assert prepared.bundle is not None
        assert sender is not None
        emails = _email_batch_payloads(
            settings=settings,
            bundle=prepared.bundle,
            destinations=list(email.to),
        )
        outcomes = sender.send_batch(
            emails=emails,
            idempotency_key=_idempotency_key_for_send(
                bundle=prepared.bundle,
                destinations=list(email.to),
                current_failed=prepared.current_failed,
                force_batch=request.force_batch,
            ),
        )
        prepared.outcomes = outcomes
        _persist_send_outcomes(
            repository=repository,
            doc_id=prepared.bundle.trend_doc_id,
            content_hash=prepared.bundle.content_hash,
            outcomes=outcomes,
        )
        if any(str(outcome.get("error") or "").strip() for outcome in outcomes):
            prepared.status = "send_failed"
            prepared.error = _send_error_from_outcomes(outcomes)
            for later in prepared_bundles[index + 1 :]:
                if later.status == "ready_to_send":
                    later.status = "not_attempted"
            return True
        prepared.status = "sent"
    return False


def send_trend_email(
    *,
    settings: Settings,
    repository: Any,
    request: TrendEmailSendRequest,
) -> TrendEmailSendBatchResult:
    selected_granularities = _resolved_email_granularities(
        settings=settings,
        selected_granularities=request.granularities,
    )
    email = _normalized_email_config(settings)
    context = _SendPreflightContext(
        settings=settings,
        repository=repository,
        destinations=list(email.to),
        force_batch=request.force_batch,
        url_checker=request.url_checker,
    )
    prepared_bundles = [
        _resolve_send_bundle(
            context=context,
            request=request,
            granularity=granularity,
        )
        for granularity in selected_granularities
    ]
    bundles = [
        prepared.bundle
        for prepared in prepared_bundles
        if prepared.bundle is not None
    ]

    send_root_dir = _send_root_dir(settings=settings)
    if any(prepared.status == "preflight_failed" for prepared in prepared_bundles):
        return _send_batch_result(
            status="preflight_failed",
            settings=settings,
            send_root_dir=send_root_dir,
            bundles=bundles,
            prepared_bundles=prepared_bundles,
        )
    send_failed = _execute_send_batch(
        settings=settings,
        repository=repository,
        request=request,
        prepared_bundles=prepared_bundles,
    )
    return _send_batch_result(
        status="send_failed" if send_failed else "succeeded",
        settings=settings,
        send_root_dir=send_root_dir,
        bundles=bundles,
        prepared_bundles=prepared_bundles,
    )
