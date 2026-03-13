from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import struct
from typing import Any, Callable
import zlib

import fitz
from markdown_it import MarkdownIt

from recoleta.publish.trend_render_shared import (
    _build_trend_browser_pdf_html,
    _build_trend_pdf_html,
    _decorate_trend_pdf_body_html,
    _extract_trend_pdf_sections,
    _normalize_obsidian_callouts_for_pdf,
    _split_yaml_frontmatter_text,
)


def _normalize_trend_pdf_page_mode(page_mode: str) -> str:
    normalized = str(page_mode or "").strip().lower() or "a4"
    if normalized not in {"a4", "continuous"}:
        raise ValueError("Trend PDF page_mode must be one of: a4, continuous")
    return normalized


_TREND_PDF_CSS = """
body {
  font-family: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", Arial, sans-serif;
  font-size: 10.9pt;
  line-height: 1.64;
  color: #1d2733;
  background: #f5f7fb;
}
.page-shell {
  padding: 0;
}
.hero {
  margin-bottom: 16pt;
  padding: 18pt 18pt 16pt 18pt;
  border-radius: 20pt;
  background: #eef3fa;
  border: 1pt solid #d8e2ef;
  color: #1d2d35;
}
.hero-kicker {
  margin-bottom: 7pt;
  font-size: 8.4pt;
  font-weight: bold;
  letter-spacing: 1.8pt;
  text-transform: uppercase;
  color: #4f6a8d;
}
.hero-title {
  margin: 0 0 6pt 0;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 22pt;
  line-height: 1.16;
  font-weight: bold;
  color: #112234;
}
.hero-dek {
  margin: 0 0 10pt 0;
  color: #536478;
  font-size: 9.7pt;
}
.hero-summary {
  margin: 0 0 10pt 0;
  color: #1664c0;
  font-size: 9.2pt;
  font-weight: bold;
}
.meta-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 6pt;
}
.meta-grid td {
  width: 25%;
  padding: 8pt 9pt;
  vertical-align: top;
  border: 1pt solid #d9e3ef;
  border-radius: 12pt;
  background: #f9fbfe;
}
.meta-label {
  margin-bottom: 2pt;
  font-size: 7.8pt;
  letter-spacing: 1.2pt;
  text-transform: uppercase;
  color: #6f8096;
}
.meta-value {
  font-size: 9.8pt;
  line-height: 1.4;
  color: #223243;
}
.content {
  margin: 0;
}
.brief-flow {
  margin: 0;
}
.summary-grid-wrap {
  margin: 0 0 12pt 0;
}
.summary-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 8pt;
}
.summary-panel {
  width: 50%;
  padding: 12pt 13pt;
  vertical-align: top;
  border: 1pt solid #dbe4ef;
  border-radius: 16pt;
  background: #ffffff;
}
.summary-primary {
  background: #edf5ff;
  border-color: #cfe0f7;
}
.summary-secondary {
  background: #f8fbff;
}
.summary-panel-body {
  font-size: 10pt;
}
.content-section,
.topics-section,
.clusters-section {
  margin: 0 0 12pt 0;
}
.content-section {
  padding: 0;
}
.section-compact {
  padding: 10pt 12pt;
  border: 1pt solid #dbe4ef;
  border-radius: 14pt;
  background: #fbfdff;
}
.section-label {
  margin: 0 0 7pt 0;
  font-size: 8.2pt;
  line-height: 1.2;
  color: #6a7f99;
  text-transform: uppercase;
  letter-spacing: 1.5pt;
}
.content-prose {
  margin: 0;
}
h1 {
  margin: 0 0 12pt 0;
  font-size: 23pt;
  line-height: 1.2;
  color: #102a37;
}
h2 {
  margin: 0;
  padding: 0;
  font-size: 8.9pt;
  line-height: 1.25;
  color: #7d5b42;
  text-transform: uppercase;
  letter-spacing: 1.6pt;
  border: 0;
}
h3 {
  margin: 12pt 0 5pt 0;
  font-size: 13.2pt;
  color: #15395a;
  font-family: "Songti SC", "STSong", Georgia, serif;
}
h4, h5, h6 {
  margin: 10pt 0 5pt 0;
  font-size: 8.7pt;
  color: #5d7492;
  text-transform: uppercase;
  letter-spacing: 1.1pt;
}
p {
  margin: 0 0 7pt 0;
}
ul, ol {
  margin: 0 0 8pt 14pt;
}
li {
  margin: 0 0 4pt 0;
}
blockquote {
  margin: 0 0 10pt 0;
  padding: 10pt 11pt;
  border-left: 3pt solid #3390ec;
  background: #eff7ff;
  color: #36536e;
  border-radius: 12pt;
}
pre {
  margin: 0 0 14pt 0;
  padding: 12pt;
  border-radius: 12pt;
  background: #16212b;
  color: #f8fafc;
  font-size: 9pt;
  line-height: 1.45;
  white-space: pre-wrap;
}
code {
  padding: 1pt 4pt;
  border-radius: 6pt;
  background: #eef3f8;
  border: 1pt solid #d9e3ef;
  font-size: 9.5pt;
}
a {
  color: #1d6fd3;
  text-decoration: underline;
}
hr {
  margin: 18pt 0;
  border: 0;
  border-top: 1pt solid #dbe4ef;
}
table {
  width: 100%;
  margin: 0 0 14pt 0;
  border-collapse: collapse;
}
th, td {
  padding: 6pt 8pt;
  border: 1pt solid #eadfce;
}
th {
  background: #f7f0e4;
}
strong {
  color: #162a34;
}
.topic-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 6pt;
}
.topic-grid td {
  width: 25%;
  padding: 6pt 8pt;
  border: 1pt solid #dbe4ef;
  border-radius: 999pt;
  background: #f8fbff;
  font-size: 8.9pt;
  color: #425a73;
}
.topic-grid .topic-cell-empty {
  background: transparent;
  border-color: transparent;
}
.cluster-grid {
  width: 100%;
  margin: 0;
  border-collapse: separate;
  border-spacing: 8pt;
}
.cluster-cell {
  width: 50%;
  vertical-align: top;
  border: 0;
  padding: 0;
}
.cluster-cell-empty {
  background: transparent;
}
.cluster-card {
  padding: 11pt 12pt 9pt 12pt;
  border: 1pt solid #dbe4ef;
  border-radius: 14pt;
  background: #ffffff;
  page-break-inside: avoid;
}
.cluster-title {
  margin: 0 0 7pt 0;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 12.3pt;
  line-height: 1.28;
  color: #13395f;
}
.cluster-body {
  margin: 0;
}
.content-prose ul:last-child,
.content-prose ol:last-child,
.content-prose p:last-child,
.summary-panel-body ul:last-child,
.summary-panel-body ol:last-child,
.summary-panel-body p:last-child,
.cluster-body ul:last-child,
.cluster-body ol:last-child,
.cluster-body p:last-child {
  margin-bottom: 0;
}
"""


def _png_chunk(kind: bytes, data: bytes) -> bytes:
    return (
        struct.pack(">I", len(data))
        + kind
        + data
        + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )


def _build_vertical_gradient_png_data_uri(
    start_rgb: tuple[int, int, int],
    end_rgb: tuple[int, int, int],
    *,
    width: int = 8,
    height: int = 256,
) -> str:
    rows: list[bytes] = []
    for y in range(height):
        t = 0.0 if height <= 1 else y / (height - 1)
        r = round(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * t)
        g = round(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * t)
        b = round(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * t)
        pixel = bytes((r, g, b, 255))
        rows.append(b"\x00" + pixel * width)

    payload = b"".join(rows)
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + _png_chunk(b"IHDR", ihdr)
        + _png_chunk(b"IDAT", zlib.compress(payload, level=9))
        + _png_chunk(b"IEND", b"")
    )
    encoded = base64.b64encode(png).decode("ascii")
    return f"data:image/png;base64,{encoded}"


_TREND_BROWSER_BASE_CARD_GRADIENT = _build_vertical_gradient_png_data_uri(
    (255, 255, 255),
    (244, 248, 252),
)
_TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT = _build_vertical_gradient_png_data_uri(
    (235, 243, 253),
    (248, 251, 254),
)
_TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT = _build_vertical_gradient_png_data_uri(
    (247, 250, 254),
    (251, 252, 254),
)
_TREND_BROWSER_HIGHLIGHT_GRADIENT = _build_vertical_gradient_png_data_uri(
    (247, 250, 254),
    (241, 247, 253),
)
_TREND_BROWSER_CLUSTER_GRADIENT = _build_vertical_gradient_png_data_uri(
    (255, 255, 255),
    (246, 249, 253),
)


_TREND_BROWSER_PDF_CSS = """
:root {
  color-scheme: light;
  --page-bg-top: #dbe7f4;
  --page-bg-mid: #eef4f8;
  --page-bg-bottom: #fafcfd;
  --line: rgba(20, 41, 67, 0.12);
  --line-strong: rgba(15, 35, 58, 0.18);
  --text: #142133;
  --muted: #5d7188;
  --accent: #1764c2;
  --accent-soft: #e7effa;
  --hero-start: #10273f;
  --hero-end: #2b5f96;
  --radius-xl: 28px;
  --radius-lg: 22px;
  --radius-md: 18px;
}
* {
  box-sizing: border-box;
}
html {
  margin: 0;
  background: linear-gradient(
    180deg,
    var(--page-bg-top) 0%,
    var(--page-bg-mid) 40%,
    var(--page-bg-bottom) 100%
  );
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
}
@page {
  margin: 0;
}
body {
  margin: 0;
  color: var(--text);
  background:
    radial-gradient(circle at top left, rgba(255, 255, 255, 0.74), transparent 34%),
    radial-gradient(circle at top right, rgba(23, 100, 194, 0.10), transparent 28%),
    linear-gradient(
      180deg,
      var(--page-bg-top) 0%,
      var(--page-bg-mid) 40%,
      var(--page-bg-bottom) 100%
    );
  font-family: "PingFang SC", "Hiragino Sans GB", "Helvetica Neue", "Segoe UI", Arial, sans-serif;
}
.page-shell {
  width: 100%;
  min-height: 100vh;
  padding: 12.5mm 12.5mm 14mm;
}
.hero {
  padding: 18px 20px 18px;
  border-radius: var(--radius-xl);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background:
    radial-gradient(circle at top right, rgba(255, 255, 255, 0.18), transparent 30%),
    linear-gradient(135deg, var(--hero-start) 0%, var(--hero-end) 100%);
  color: #f7fbff;
}
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(220px, 0.9fr);
  gap: 16px;
  align-items: end;
}
.hero-main,
.hero-meta,
.document-flow,
.summary-grid,
.cluster-columns {
  min-width: 0;
}
.hero-kicker {
  margin-bottom: 8px;
  color: rgba(233, 242, 255, 0.92);
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}
.hero-title {
  margin: 0 0 10px;
  font-size: 27px;
  line-height: 1.1;
  letter-spacing: -0.035em;
  font-weight: 760;
}
.hero-dek {
  margin: 0 0 14px;
  color: rgba(236, 243, 251, 0.82);
  font-size: 13.5px;
  line-height: 1.46;
}
.hero-summary {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.12);
  color: #eff5ff;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.04em;
}
.hero-meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}
.meta-item {
  min-height: 76px;
  padding: 12px 13px 11px;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(244, 248, 255, 0.14);
}
.meta-label {
  margin-bottom: 6px;
  color: rgba(226, 236, 248, 0.76);
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.meta-value {
  color: #f9fbff;
  font-size: 13px;
  line-height: 1.34;
  font-weight: 560;
  word-break: break-word;
}
.document-flow {
  margin-top: 12px;
}
.summary-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
.surface-card {
  margin-top: 12px;
  padding: 14px 15px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--line);
  background:
    url("__TREND_BROWSER_BASE_CARD_GRADIENT__") center/100% 100% no-repeat,
    #f7fafc;
  break-inside: avoid;
  page-break-inside: avoid;
}
.summary-grid .surface-card {
  margin-top: 0;
}
.summary-card-primary {
  border-color: rgba(28, 79, 138, 0.18);
  background:
    url("__TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT__") center/100% 100% no-repeat,
    #f3f8fd;
}
.summary-card-secondary {
  background:
    url("__TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT__") center/100% 100% no-repeat,
    #f8fbfe;
}
.highlight-card {
  background:
    url("__TREND_BROWSER_HIGHLIGHT_GRADIENT__") center/100% 100% no-repeat,
    #f5f9fd;
}
.section-label {
  margin: 0 0 10px;
  color: #6c8197;
  font-size: 10px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.prose,
.cluster-body {
  font-size: 13.4px;
  line-height: 1.58;
}
.prose > *:first-child,
.cluster-body > *:first-child {
  margin-top: 0;
}
.prose > *:last-child,
.cluster-body > *:last-child {
  margin-bottom: 0;
}
.prose p,
.cluster-body p {
  margin: 0 0 9px;
}
.prose h3,
.cluster-card h3 {
  margin: 14px 0 8px;
  color: #15395d;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 20px;
  line-height: 1.18;
  letter-spacing: -0.03em;
  font-weight: 720;
}
.cluster-card h3 {
  margin-top: 0;
  font-size: 18px;
}
.prose h4,
.cluster-body h4 {
  margin: 12px 0 7px;
  color: #6d8198;
  font-size: 10px;
  line-height: 1.2;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}
.prose ul,
.prose ol,
.cluster-body ul,
.cluster-body ol {
  margin: 7px 0 9px;
  padding-inline-start: 1.05em;
}
.prose li,
.cluster-body li {
  margin: 0 0 6px;
  padding-left: 0.12em;
}
.prose li::marker,
.cluster-body li::marker {
  color: #7a8fa7;
}
.prose a,
.cluster-body a {
  color: var(--accent);
  text-decoration: none;
}
.prose strong,
.cluster-body strong {
  color: #122238;
}
.prose blockquote,
.cluster-body blockquote {
  margin: 10px 0;
  padding: 12px 14px;
  border-left: 3px solid rgba(23, 100, 194, 0.45);
  border-radius: 14px;
  background: var(--accent-soft);
  color: #27496d;
}
.prose pre,
.cluster-body pre {
  margin: 10px 0;
  padding: 12px 14px;
  border-radius: 16px;
  background: #16212b;
  color: #f8fafc;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
}
.prose code,
.cluster-body code {
  padding: 1px 5px;
  border-radius: 8px;
  background: #eef3f8;
  border: 1px solid #d9e3ef;
  font-size: 12px;
}
.prose table,
.cluster-body table {
  width: 100%;
  margin: 10px 0 12px;
  border-collapse: collapse;
}
.prose th,
.prose td,
.cluster-body th,
.cluster-body td {
  padding: 7px 8px;
  border: 1px solid #dbe4ef;
  text-align: left;
  vertical-align: top;
}
.prose th,
.cluster-body th {
  background: #f4f7fb;
}
.topics-card {
  padding-bottom: 15px;
}
.topic-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 8px;
}
.topic-pill {
  display: block;
  min-height: 38px;
  padding: 9px 12px;
  border-radius: 999px;
  border: 1px solid #dbe4ef;
  background: rgba(248, 251, 255, 0.98);
  color: #425a74;
  font-size: 11px;
  line-height: 1.3;
  font-weight: 560;
}
.cluster-section {
  padding-bottom: 4px;
}
.cluster-columns {
  column-count: 2;
  column-gap: 12px;
}
.cluster-card {
  display: inline-block;
  width: 100%;
  margin: 0 0 12px;
  padding: 14px 14px 12px;
  border-radius: 18px;
  border: 1px solid var(--line-strong);
  background:
    url("__TREND_BROWSER_CLUSTER_GRADIENT__") center/100% 100% no-repeat,
    #f8fbfd;
  break-inside: avoid;
  page-break-inside: avoid;
}
.evolution-section {
  background:
    radial-gradient(circle at top right, rgba(23, 100, 194, 0.10), transparent 30%),
    linear-gradient(180deg, rgba(237, 244, 252, 0.98), rgba(248, 251, 255, 0.99));
}
.evolution-section-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.evolution-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.evolution-stat,
.history-pill,
.evolution-badge {
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid rgba(23, 100, 194, 0.15);
  background: rgba(23, 100, 194, 0.08);
  color: #1f5da5;
  font-size: 10.5px;
  font-weight: 700;
}
.evolution-stat.secondary,
.history-pill {
  background: rgba(255, 255, 255, 0.92);
  color: #4b647d;
}
.evolution-summary {
  margin-bottom: 12px;
}
.evolution-grid {
  display: grid;
  gap: 12px;
}
.evolution-card {
  position: relative;
  display: grid;
  gap: 10px;
  padding: 14px 14px 13px;
  border-radius: 18px;
  border: 1px solid rgba(20, 41, 67, 0.10);
  background: rgba(253, 254, 255, 0.98);
}
.evolution-card::before {
  content: "";
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  border-radius: 18px 0 0 18px;
  background: #7d94ae;
}
.evolution-change-continuing::before {
  background: #2c6bc5;
}
.evolution-change-emerging::before {
  background: #1d8b6f;
}
.evolution-change-fading::before {
  background: #b66a35;
}
.evolution-change-shifting::before {
  background: #7459c6;
}
.evolution-change-polarizing::before {
  background: #c24d6b;
}
.evolution-card-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}
.evolution-card-title {
  margin: 0;
  color: #173659;
  font-family: "Songti SC", "STSong", Georgia, serif;
  font-size: 18px;
  line-height: 1.12;
  letter-spacing: -0.02em;
  font-weight: 720;
}
.evolution-badge-continuing {
  background: rgba(29, 103, 194, 0.10);
  color: #1e5aa1;
}
.evolution-badge-emerging {
  background: rgba(29, 139, 111, 0.10);
  color: #176d58;
  border-color: rgba(29, 139, 111, 0.16);
}
.evolution-badge-fading {
  background: rgba(182, 106, 53, 0.11);
  color: #9c5a2b;
  border-color: rgba(182, 106, 53, 0.16);
}
.evolution-badge-shifting {
  background: rgba(116, 89, 198, 0.10);
  color: #654bb0;
  border-color: rgba(116, 89, 198, 0.16);
}
.evolution-badge-polarizing {
  background: rgba(194, 77, 107, 0.10);
  color: #a2415a;
  border-color: rgba(194, 77, 107, 0.16);
}
.evolution-history-block {
  display: grid;
  gap: 7px;
}
.evolution-history-label {
  color: #7589a0;
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.10em;
  text-transform: uppercase;
}
.evolution-history-track {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.evolution-copy {
  margin-top: -1px;
}
"""

_TREND_BROWSER_PDF_CSS = (
    _TREND_BROWSER_PDF_CSS.replace(
        "__TREND_BROWSER_BASE_CARD_GRADIENT__",
        _TREND_BROWSER_BASE_CARD_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT__",
        _TREND_BROWSER_SUMMARY_PRIMARY_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT__",
        _TREND_BROWSER_SUMMARY_SECONDARY_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_HIGHLIGHT_GRADIENT__",
        _TREND_BROWSER_HIGHLIGHT_GRADIENT,
    )
    .replace(
        "__TREND_BROWSER_CLUSTER_GRADIENT__",
        _TREND_BROWSER_CLUSTER_GRADIENT,
    )
)


@dataclass(slots=True)
class TrendPdfRenderInputs:
    markdown_path: Path
    output_path: Path
    frontmatter: dict[str, Any]
    raw_markdown: str
    normalized_markdown: str
    title: str
    document_html: str
    css: str
    renderer: str
    page_mode: str


@dataclass(slots=True)
class TrendPdfRenderResult:
    path: Path
    prepared: TrendPdfRenderInputs


def _prepare_trend_pdf_render_inputs(
    *,
    markdown_path: Path,
    output_path: Path | None = None,
    backend: str = "story",
    page_mode: str = "a4",
) -> TrendPdfRenderInputs:
    resolved_markdown_path = markdown_path.expanduser().resolve()
    if not resolved_markdown_path.exists():
        raise ValueError(
            f"Trend markdown note does not exist: {resolved_markdown_path}"
        )
    if not resolved_markdown_path.is_file():
        raise ValueError(
            f"Trend markdown note must be a file: {resolved_markdown_path}"
        )

    resolved_output_path = (
        output_path.expanduser().resolve()
        if output_path is not None
        else resolved_markdown_path.with_suffix(".pdf")
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    raw_markdown = resolved_markdown_path.read_text(encoding="utf-8")
    frontmatter, markdown_body = _split_yaml_frontmatter_text(raw_markdown)
    normalized_markdown = _normalize_obsidian_callouts_for_pdf(markdown_body).strip()
    if not normalized_markdown:
        normalized_markdown = "# Trend\n"

    normalized_backend = str(backend or "").strip().lower() or "story"
    normalized_page_mode = _normalize_trend_pdf_page_mode(page_mode)
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True})
    body_html = markdown.render(normalized_markdown)
    title, sections = _extract_trend_pdf_sections(body_html=body_html)

    if normalized_backend == "browser":
        document_html = _build_trend_browser_pdf_html(
            frontmatter=frontmatter,
            title=title,
            sections=sections,
        )
        css = _TREND_BROWSER_PDF_CSS
        actual_page_mode = normalized_page_mode
    else:
        decorated_body_html, decorated_title = _decorate_trend_pdf_body_html(
            body_html=body_html
        )
        title = decorated_title
        document_html = _build_trend_pdf_html(
            body_html=decorated_body_html,
            frontmatter=frontmatter,
            title=title,
        )
        css = _TREND_PDF_CSS
        actual_page_mode = "a4"

    return TrendPdfRenderInputs(
        markdown_path=resolved_markdown_path,
        output_path=resolved_output_path,
        frontmatter=frontmatter,
        raw_markdown=raw_markdown,
        normalized_markdown=normalized_markdown,
        title=title,
        document_html=document_html,
        css=css,
        renderer=normalized_backend,
        page_mode=actual_page_mode,
    )


def export_trend_note_pdf_debug_bundle(
    *,
    markdown_path: Path,
    pdf_path: Path,
    debug_dir: Path,
    prepared: TrendPdfRenderInputs | None = None,
) -> Path:
    inputs = prepared or _prepare_trend_pdf_render_inputs(
        markdown_path=markdown_path,
        output_path=pdf_path,
    )
    resolved_debug_dir = debug_dir.expanduser().resolve()
    resolved_debug_dir.mkdir(parents=True, exist_ok=True)

    files = {
        "source": "source.md",
        "normalized": "normalized.md",
        "html": "document.html",
        "css": "styles.css",
    }
    (resolved_debug_dir / files["source"]).write_text(
        inputs.raw_markdown, encoding="utf-8"
    )
    (resolved_debug_dir / files["normalized"]).write_text(
        inputs.normalized_markdown + "\n", encoding="utf-8"
    )
    (resolved_debug_dir / files["html"]).write_text(
        inputs.document_html, encoding="utf-8"
    )
    (resolved_debug_dir / files["css"]).write_text(inputs.css, encoding="utf-8")

    previews: list[str] = []
    page_count = 0
    with fitz.open(pdf_path) as document:
        page_count = len(document)
        for page_number in range(page_count):
            preview_name = f"page-{page_number + 1}.png"
            page = document.load_page(page_number)
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(
                resolved_debug_dir / preview_name
            )
            previews.append(preview_name)

    manifest = {
        "title": inputs.title,
        "renderer": inputs.renderer,
        "page_mode": inputs.page_mode,
        "markdown_path": str(inputs.markdown_path),
        "pdf_path": str(pdf_path.expanduser().resolve()),
        "page_count": page_count,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "frontmatter": inputs.frontmatter,
        "files": {
            "source_markdown": files["source"],
            "normalized_markdown": files["normalized"],
            "document_html": files["html"],
            "styles_css": files["css"],
            "page_previews": previews,
        },
    }
    manifest_path = resolved_debug_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest_path


def _render_trend_note_pdf_story(inputs: TrendPdfRenderInputs) -> None:
    page_rect = fitz.paper_rect("a4")
    content_rect = fitz.Rect(34, 38, page_rect.width - 34, page_rect.height - 38)

    def _rect_fn(
        rect_num: int,
        _filled: fitz.Rect,
    ) -> tuple[fitz.Rect, fitz.Rect, None]:
        _ = rect_num
        return page_rect, content_rect, None

    if inputs.output_path.exists():
        inputs.output_path.unlink()
    writer = fitz.DocumentWriter(str(inputs.output_path), "compress")
    try:
        fitz.Story(inputs.document_html, user_css=inputs.css, em=11).write(
            writer, _rect_fn
        )
    finally:
        writer.close()


def _compose_trend_pdf_browser_html(*, inputs: TrendPdfRenderInputs) -> str:
    return inputs.document_html.replace(
        "</head>",
        f"<style>{inputs.css}</style></head>",
        1,
    )


def _render_trend_note_pdf_browser_with_dependencies(
    *,
    inputs: TrendPdfRenderInputs,
    sync_playwright: Callable[[], Any],
    launch_options_list: list[dict[str, Any]],
) -> None:
    viewport = {"width": 794, "height": 1123}
    last_error: Exception | None = None
    if inputs.output_path.exists():
        inputs.output_path.unlink()

    with sync_playwright() as playwright:
        for launch_kwargs in launch_options_list:
            browser = None
            try:
                browser = playwright.chromium.launch(**launch_kwargs)
                page = browser.new_page(
                    viewport=viewport,
                    device_scale_factor=1,
                    color_scheme="light",
                )
                page.set_content(
                    _compose_trend_pdf_browser_html(inputs=inputs),
                    wait_until="load",
                )
                page.emulate_media(media="screen")
                if inputs.page_mode == "continuous":
                    height_px = int(
                        page.evaluate(
                            """async () => {
                              if (document.fonts && document.fonts.ready) {
                                await document.fonts.ready;
                              }
                              const root = document.documentElement;
                              const body = document.body;
                              return Math.ceil(Math.max(
                                root.scrollHeight,
                                root.offsetHeight,
                                body.scrollHeight,
                                body.offsetHeight,
                              ));
                            }"""
                        )
                    )
                    pdf_kwargs: dict[str, Any] = {
                        "path": str(inputs.output_path),
                        "width": "210mm",
                        "height": f"{max(height_px, viewport['height'])}px",
                        "print_background": True,
                        "margin": {
                            "top": "0",
                            "right": "0",
                            "bottom": "0",
                            "left": "0",
                        },
                    }
                else:
                    pdf_kwargs = {
                        "path": str(inputs.output_path),
                        "format": "A4",
                        "print_background": True,
                        "margin": {
                            "top": "0",
                            "right": "0",
                            "bottom": "0",
                            "left": "0",
                        },
                    }
                page.pdf(**pdf_kwargs)
                return
            except Exception as exc:  # noqa: BLE001
                last_error = exc
            finally:
                if browser is not None:
                    browser.close()

    raise RuntimeError("Browser-based trend PDF rendering failed.") from last_error
