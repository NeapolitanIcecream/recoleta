from __future__ import annotations

from datetime import datetime, timezone
import html
from pathlib import Path
import re
from typing import Any
from urllib.parse import urlparse

import yaml
from slugify import slugify


def _read_yaml_frontmatter(path: Path) -> dict[str, Any] | None:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return None

    if not lines or lines[0].strip() != "---":
        return None

    end_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return None

    raw = "\n".join(lines[1:end_idx]).strip()
    if not raw:
        return None

    try:
        loaded = yaml.safe_load(raw)
    except Exception:
        return None
    return loaded if isinstance(loaded, dict) else None


def write_obsidian_note(
    *,
    vault_path: Path,
    base_folder: str,
    item_id: int,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
) -> Path:
    note_dir = vault_path / base_folder / "Inbox"
    note_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
    note_path = note_dir / f"{date_prefix}--{slug}.md"
    if note_path.exists():
        frontmatter = _read_yaml_frontmatter(note_path) or {}
        existing_url = str(frontmatter.get("url") or "").strip()
        if existing_url != canonical_url.strip():
            note_path = note_dir / f"{date_prefix}--{slug}--{item_id}.md"

    frontmatter = {
        "source": source,
        "url": canonical_url,
        "published_at": published_at.isoformat() if published_at else None,
        "authors": authors,
        "topics": topics,
        "relevance_score": round(relevance_score, 4),
        "run_id": run_id,
    }

    lines = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        "## Summary",
        summary.strip(),
    ]
    lines.extend(
        [
            "",
            "## Links",
            f"- Canonical: {canonical_url}",
            "",
        ]
    )
    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def write_markdown_note(
    *,
    output_dir: Path,
    item_id: int,
    title: str,
    source: str,
    canonical_url: str,
    published_at: datetime | None,
    authors: list[str],
    topics: list[str],
    relevance_score: float,
    run_id: str,
    summary: str,
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")

    note_dir = output_dir / "Inbox"
    note_dir.mkdir(parents=True, exist_ok=True)
    date_prefix = (published_at or datetime.now(timezone.utc)).strftime("%Y-%m-%d")
    slug = slugify(title, lowercase=True) or "untitled-item"
    note_path = note_dir / f"{date_prefix}--{slug}--{item_id}.md"

    frontmatter = {
        "source": source,
        "url": canonical_url,
        "published_at": published_at.isoformat() if published_at else None,
        "authors": authors,
        "topics": topics,
        "relevance_score": round(relevance_score, 4),
        "run_id": run_id,
    }

    lines = [
        "---",
        yaml.safe_dump(frontmatter, sort_keys=False).strip(),
        "---",
        "",
        f"# {title}",
        "",
        "## Summary",
        summary.strip(),
    ]
    lines.extend(
        [
            "",
            "## Links",
            f"- Canonical: {canonical_url}",
            "",
        ]
    )
    note_path.write_text("\n".join(lines), encoding="utf-8")
    return note_path


def write_markdown_run_index(
    *,
    output_dir: Path,
    run_id: str,
    generated_at: datetime,
    notes: list[tuple[str, Path]],
) -> Path:
    output_dir = output_dir.expanduser().resolve()
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError("MARKDOWN_OUTPUT_DIR must be a directory")
    output_dir.mkdir(parents=True, exist_ok=True)

    def sanitize_segment(
        value: str, *, max_len: int = 72, fallback: str = "unknown"
    ) -> str:
        cleaned = str(value).strip()
        normalized = "".join(
            ch if (ch.isalnum() or ch in {"-", "_"}) else "_" for ch in cleaned
        )
        while "__" in normalized:
            normalized = normalized.replace("__", "_")
        normalized = normalized.strip("_")
        if not normalized:
            return fallback
        return normalized[:max_len]

    safe_run_id = sanitize_segment(run_id, fallback="run")
    runs_dir = output_dir / "Runs"
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_index_path = runs_dir / f"{safe_run_id}.md"
    latest_path = output_dir / "latest.md"

    lines: list[str] = [
        "# Recoleta publish output",
        "",
        f"- Run ID: `{run_id}`",
        f"- Generated at (UTC): `{generated_at.astimezone(timezone.utc).isoformat()}`",
        "",
        "## Notes",
    ]
    if not notes:
        lines.extend(["", "_No items published in this run._", ""])
    else:
        for title, note_path in notes:
            rel: str
            try:
                rel = str(note_path.resolve().relative_to(output_dir))
            except Exception:
                rel = str(note_path)
            lines.append(f"- [{title}]({rel})")
        lines.append("")

    payload = "\n".join(lines).strip() + "\n"
    run_index_path.write_text(payload, encoding="utf-8")
    latest_path.write_text(payload, encoding="utf-8")
    return latest_path


def build_telegram_message(*, title: str, summary: str, url: str) -> str:
    max_chars = 4096

    title_raw = str(title or "").strip() or "Untitled"
    summary_raw = str(summary or "").strip()
    url_raw = str(url or "").strip()

    def _format_telegram_summary_html(text: str) -> str:
        raw = str(text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
        if not raw:
            return ""

        codeblocks: list[str] = []

        def _stash_codeblock(match: re.Match[str]) -> str:
            code = (match.group(1) or "").strip("\n")
            token = f"\x00CB{len(codeblocks)}\x00"
            codeblocks.append(f"<pre><code>{html.escape(code)}</code></pre>")
            return token

        raw = re.sub(r"```[^\n]*\n([\s\S]*?)```", _stash_codeblock, raw)

        codespans: list[str] = []

        def _inline_to_html(line: str) -> str:
            def _apply_outside_tags(value: str, transform: Any) -> str:
                parts = re.split(r"(<[^>]+>)", value)
                for idx in range(0, len(parts), 2):
                    parts[idx] = transform(parts[idx])
                return "".join(parts)

            # Protect inline code spans first so we don't interpret markdown inside them.
            def _stash_codespan(match: re.Match[str]) -> str:
                code = match.group(1) or ""
                token = f"\x00CS{len(codespans)}\x00"
                codespans.append(f"<code>{html.escape(code)}</code>")
                return token

            protected = re.sub(r"`([^`\n]+)`", _stash_codespan, line)
            escaped = html.escape(protected, quote=True)

            # Links: [label](url)
            def _replace_link(match: re.Match[str]) -> str:
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

            escaped = re.sub(r"\[([^\]\n]+)\]\(([^)\s\n]+)\)", _replace_link, escaped)

            # Bold: **text** or __text__
            escaped = _apply_outside_tags(
                escaped,
                lambda s: re.sub(r"\*\*([^\n]+?)\*\*", r"<b>\1</b>", s),
            )
            escaped = _apply_outside_tags(
                escaped,
                lambda s: re.sub(r"__([^\n]+?)__", r"<b>\1</b>", s),
            )

            # Italic: *text* or _text_ (avoid bold markers)
            escaped = _apply_outside_tags(
                escaped,
                lambda s: re.sub(
                    r"(?<!\*)\*([^\n]+?)\*(?!\*)",
                    r"<i>\1</i>",
                    s,
                ),
            )
            escaped = _apply_outside_tags(
                escaped,
                lambda s: re.sub(r"(?<!_)_([^\n]+?)_(?!_)", r"<i>\1</i>", s),
            )

            for idx, html_snippet in enumerate(codespans):
                escaped = escaped.replace(f"\x00CS{idx}\x00", html_snippet)
            return escaped

        lines: list[str] = []
        for raw_line in raw.splitlines():
            stripped = raw_line.strip()
            cb = re.fullmatch(r"\x00CB(\d+)\x00", stripped)
            if cb:
                idx = int(cb.group(1))
                if 0 <= idx < len(codeblocks):
                    lines.append(codeblocks[idx])
                    continue

            if not stripped:
                lines.append("")
                continue

            heading = re.match(r"^\s*#{1,6}\s+(.*)$", raw_line)
            if heading:
                content = heading.group(1).strip()
                lines.append(f"<b>{_inline_to_html(content)}</b>")
                continue

            bullet = re.match(r"^\s*[-*]\s+(.*)$", raw_line)
            if bullet:
                content = bullet.group(1).strip()
                lines.append(f"• {_inline_to_html(content)}")
                continue

            lines.append(_inline_to_html(raw_line.strip()))

        rendered = "\n".join(lines).strip()
        while "\n\n\n" in rendered:
            rendered = rendered.replace("\n\n\n", "\n\n")
        return rendered

    def _link_label(value: str) -> str:
        try:
            parsed = urlparse(value)
            if parsed.netloc:
                return parsed.netloc
        except Exception:
            pass
        return "Open"

    def _render(summary_text: str) -> str:
        safe_title = html.escape(title_raw)
        safe_summary = _format_telegram_summary_html(summary_text)
        safe_url_attr = html.escape(url_raw, quote=True)
        safe_label = html.escape(_link_label(url_raw))

        lines = [
            f"<b>{safe_title}</b>",
            "",
            "<b>Summary:</b>",
            safe_summary,
            "",
            f'<b>Link:</b> <a href="{safe_url_attr}">{safe_label}</a>',
        ]
        return "\n".join(lines).strip()

    message = _render(summary_raw)
    if len(message) <= max_chars:
        return message

    if not summary_raw:
        return _render("…")[:max_chars]

    # Truncate summary while keeping HTML valid (escape happens after truncation).
    lo = 0
    hi = len(summary_raw)
    best = ""
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = summary_raw[:mid].rstrip()
        if candidate.count("```") % 2 == 1:
            candidate = candidate.rsplit("```", 1)[0].rstrip()
        candidate_msg = _render(candidate + "…")
        if len(candidate_msg) <= max_chars:
            best = candidate
            lo = mid + 1
        else:
            hi = mid - 1

    if best:
        # Prefer breaking at a boundary for readability.
        boundary = max(best.rfind("\n"), best.rfind(" "))
        if boundary >= 120:
            best = best[:boundary].rstrip()
        return _render(best + "…")

    # Extremely small budget: still return a valid, short message.
    return _render("…")[:max_chars]
