from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
import html
import re
from urllib.parse import urlparse

from recoleta.item_summary import normalize_item_summary_markdown
from recoleta.publish.trend_render_shared import _trend_date_token


def _stash_codeblocks(text: str) -> tuple[str, list[str]]:
    codeblocks: list[str] = []

    def _stash_codeblock(match: re.Match[str]) -> str:
        code = (match.group(1) or "").strip("\n")
        token = f"\x00CB{len(codeblocks)}\x00"
        codeblocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
        return token

    return re.sub(r"```[^\n]*\n([\s\S]*?)```", _stash_codeblock, text), codeblocks


def _apply_outside_tags(value: str, transform: Callable[[str], str]) -> str:
    parts = re.split(r"(<[^>]+>)", value)
    for idx in range(0, len(parts), 2):
        parts[idx] = transform(parts[idx])
    return "".join(parts)


def _stash_codespans(line: str) -> tuple[str, list[str]]:
    codespans: list[str] = []

    def _stash_codespan(match: re.Match[str]) -> str:
        code = match.group(1) or ""
        token = f"\x00CS{len(codespans)}\x00"
        codespans.append(f"<code>{html.escape(code)}</code>")
        return token

    return re.sub(r"`([^`\n]+)`", _stash_codespan, line), codespans


def _replace_markdown_link(match: re.Match[str]) -> str:
    label = match.group(1) or ""
    url_escaped = match.group(2) or ""
    url_unescaped = html.unescape(url_escaped)
    try:
        parsed = urlparse(url_unescaped)
    except Exception:
        return match.group(0)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return f"{label} ({url_escaped})"
    safe_href = html.escape(url_unescaped, quote=True)
    return f'<a href="{safe_href}">{label}</a>'


def _apply_inline_emphasis(text: str) -> str:
    emphasized = _apply_outside_tags(
        text,
        lambda value: re.sub(r"\*\*([^\n]+?)\*\*", r"<b>\1</b>", value),
    )
    emphasized = _apply_outside_tags(
        emphasized,
        lambda value: re.sub(r"__([^\n]+?)__", r"<b>\1</b>", value),
    )
    emphasized = _apply_outside_tags(
        emphasized,
        lambda value: re.sub(r"(?<!\*)\*([^\n]+?)\*(?!\*)", r"<i>\1</i>", value),
    )
    return _apply_outside_tags(
        emphasized,
        lambda value: re.sub(r"(?<!_)_([^\n]+?)_(?!_)", r"<i>\1</i>", value),
    )


def _restore_codespans(text: str, codespans: list[str]) -> str:
    restored = text
    for idx, html_snippet in enumerate(codespans):
        restored = restored.replace(f"\x00CS{idx}\x00", html_snippet)
    return restored


def _inline_to_html(line: str) -> str:
    protected, codespans = _stash_codespans(line)
    escaped = html.escape(protected, quote=True)
    escaped = re.sub(r"\[([^\]\n]+)\]\(([^)\s\n]+)\)", _replace_markdown_link, escaped)
    return _restore_codespans(_apply_inline_emphasis(escaped), codespans)


def _render_markdownish_line(
    *,
    raw_line: str,
    codeblocks: list[str],
) -> str:
    stripped = raw_line.strip()
    codeblock_match = re.fullmatch(r"\x00CB(\d+)\x00", stripped)
    if codeblock_match:
        idx = int(codeblock_match.group(1))
        if 0 <= idx < len(codeblocks):
            return codeblocks[idx]
    if not stripped:
        return ""
    heading = re.match(r"^\s*#{1,6}\s+(.*)$", raw_line)
    if heading:
        return f"<b>{_inline_to_html(heading.group(1).strip())}</b>"
    bullet = re.match(r"^\s*[-*]\s+(.*)$", raw_line)
    if bullet:
        return f"• {_inline_to_html(bullet.group(1).strip())}"
    return _inline_to_html(raw_line.strip())


def _format_telegram_markdownish_html(text: str) -> str:
    raw = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    if not raw:
        return ""
    raw, codeblocks = _stash_codeblocks(raw)
    lines = [
        _render_markdownish_line(raw_line=raw_line, codeblocks=codeblocks)
        for raw_line in raw.splitlines()
    ]

    rendered = "\n".join(lines).strip()
    while "\n\n\n" in rendered:
        rendered = rendered.replace("\n\n\n", "\n\n")
    return rendered


def _truncate_telegram_text(
    *,
    raw_text: str,
    max_chars: int,
    render: Callable[[str], str],
) -> str:
    message = render(raw_text)
    if len(message) <= max_chars:
        return message
    if not raw_text:
        return render("…")[:max_chars]

    lo = 0
    hi = len(raw_text)
    best = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = raw_text[:mid].rstrip()
        if candidate.count("```") % 2 == 1:
            candidate = candidate.rsplit("```", 1)[0].rstrip()
        candidate_message = render(candidate + "…")
        if len(candidate_message) <= max_chars:
            best = candidate
            lo = mid + 1
        else:
            hi = mid - 1

    if best:
        boundary = max(best.rfind("\n"), best.rfind(" "))
        if boundary >= 120:
            best = best[:boundary].rstrip()
        return render(best + "…")
    return render("…")[:max_chars]


def _link_label(value: str) -> str:
    try:
        parsed = urlparse(value)
        if parsed.netloc:
            return parsed.netloc
    except Exception:
        pass
    return "Open"


def build_telegram_message(*, title: str, summary: str, url: str) -> str:
    title_raw = str(title or "").strip() or "Untitled"
    summary_raw = normalize_item_summary_markdown(summary)
    url_raw = str(url or "").strip()
    link_md = f"## Link\n[{_link_label(url_raw)}]({url_raw})" if url_raw else "## Link"

    def _render(summary_text: str) -> str:
        safe_title = html.escape(title_raw)
        safe_summary = _format_telegram_markdownish_html(
            "\n\n".join(part for part in [summary_text.strip(), link_md] if part).strip()
        )
        return "\n".join([f"<b>{safe_title}</b>", "", safe_summary]).strip()

    return _truncate_telegram_text(raw_text=summary_raw, max_chars=4096, render=_render)


def build_telegram_trend_document_caption(
    *,
    title: str,
    overview_md: str,
    granularity: str,
    period_start: datetime,
) -> str:
    title_raw = str(title or "").strip() or "Trend"
    overview_raw = str(overview_md or "").strip()
    period_token = _trend_date_token(
        granularity=granularity,
        period_start=period_start,
    )
    period_label = f"{str(granularity or '').strip().title()} · {period_token}".strip(
        " ·"
    )

    def _render(overview_text: str) -> str:
        safe_title = html.escape(title_raw)
        safe_overview = _format_telegram_markdownish_html(overview_text)
        safe_period = html.escape(period_label)
        return "\n".join(
            [
                f"<b>{safe_title}</b>",
                "",
                "<b>Overview:</b>",
                safe_overview,
                "",
                f"<b>Period:</b> {safe_period}",
            ]
        ).strip()

    return _truncate_telegram_text(raw_text=overview_raw, max_chars=1024, render=_render)
