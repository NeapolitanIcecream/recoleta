from __future__ import annotations

import html
from collections.abc import Callable
import re
from typing import TYPE_CHECKING, Any
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from latex2mathml.converter import convert as latex_to_mathml
from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin

if TYPE_CHECKING:
    from markdown_it.rules_inline import StateInline


_MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"
_MATHML_ALLOWED_ATTRIBUTES = frozenset(
    {
        "accent",
        "accentunder",
        "align",
        "bevelled",
        "close",
        "columnalign",
        "columnlines",
        "columnspan",
        "dir",
        "display",
        "displaystyle",
        "fence",
        "form",
        "frame",
        "largeop",
        "linebreak",
        "mathvariant",
        "movablelimits",
        "notation",
        "open",
        "rowalign",
        "rowlines",
        "rowspan",
        "separator",
        "separators",
        "stretchy",
        "symmetric",
    }
)
_CJK_OR_FULLWIDTH_TEXT_RE = re.compile(
    r"[\u3000-\u30ff\u3400-\u9fff\uf900-\ufaff\uff00-\uffef]"
)
ElementTree.register_namespace("", _MATHML_NAMESPACE)


def _tex_with_delimiters(source: str, *, display_mode: bool) -> str:
    delimiter = "$$" if display_mode else "$"
    return f"{delimiter}{source}{delimiter}"


def _mathml_with_source_annotation(*, source: str, display_mode: bool) -> str:
    rendered = latex_to_mathml(
        source,
        display="block" if display_mode else "inline",
    )
    root = ElementTree.fromstring(rendered)
    for element in root.iter():
        element.attrib = {
            name: value
            for name, value in element.attrib.items()
            if name.rsplit("}", 1)[-1].lower() in _MATHML_ALLOWED_ATTRIBUTES
        }
    semantics = ElementTree.Element(f"{{{_MATHML_NAMESPACE}}}semantics")
    semantics.text = root.text
    root.text = None
    for child in tuple(root):
        root.remove(child)
        semantics.append(child)
    annotation = ElementTree.SubElement(
        semantics,
        f"{{{_MATHML_NAMESPACE}}}annotation",
        {"encoding": "application/x-tex"},
    )
    annotation.text = source
    root.append(semantics)
    return ElementTree.tostring(root, encoding="unicode")


def _render_site_math(source: str, options: dict[str, Any]) -> str:
    display_mode = bool(options.get("display_mode"))
    try:
        return _mathml_with_source_annotation(
            source=source,
            display_mode=display_mode,
        )
    except Exception:
        fallback = _tex_with_delimiters(source, display_mode=display_mode)
        return f'<code class="math-source-fallback">{html.escape(fallback)}</code>'


def _render_email_math(source: str, options: dict[str, Any]) -> str:
    display_mode = bool(options.get("display_mode"))
    escaped_source = html.escape(
        _tex_with_delimiters(source, display_mode=display_mode)
    )
    if display_mode:
        return f"<pre><code>{escaped_source}</code></pre>"
    return f"<code>{escaped_source}</code>"


def _is_escaped(source: str, position: int) -> bool:
    backslashes = 0
    cursor = position - 1
    while cursor >= 0 and source[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def _is_inline_math_opener(source: str, start: int) -> bool:
    if source[start] != "$" or _is_escaped(source, start):
        return False
    if (start + 1 < len(source) and source[start + 1] == "$") or (
        start > 0 and source[start - 1] == "$"
    ):
        return False
    if start + 1 >= len(source) or source[start + 1].isspace():
        return False
    if start > 0 and source[start - 1].isdigit():
        return False
    return True


def _find_inline_math_end(source: str, start: int) -> int | None:
    cursor = start + 1
    while True:
        end = source.find("$", cursor)
        if end < 0:
            return None
        if not _is_escaped(source, end):
            return end
        cursor = end + 1


def _inline_math_content_is_valid(content: str) -> bool:
    if not content or content[-1].isspace() or "`" in content or "\n" in content:
        return False
    if content[0].isdigit() and _CJK_OR_FULLWIDTH_TEXT_RE.search(content):
        return False
    return True


def _inline_math_trailing_context_is_valid(source: str, end: int) -> bool:
    if end + 1 < len(source):
        trailing = source[end + 1]
        if trailing.isascii() and trailing.isalnum():
            return False
    return True


def _safe_inline_math(state: StateInline, silent: bool) -> bool:
    source = state.src
    start = state.pos
    if not _is_inline_math_opener(source, start):
        return False
    end = _find_inline_math_end(source, start)
    if end is None:
        return False
    content = source[start + 1 : end]
    if not _inline_math_content_is_valid(content):
        return False
    if not _inline_math_trailing_context_is_valid(source, end):
        return False

    if not silent:
        token = state.push("math_inline", "math", 0)
        token.content = content
        token.markup = "$"
    state.pos = end + 1
    return True


def _build_math_markdown_renderer(
    *,
    renderer: Callable[[str, dict[str, Any]], str],
) -> MarkdownIt:
    markdown = MarkdownIt("commonmark", {"html": True, "typographer": True}).use(
        dollarmath_plugin,
        allow_labels=False,
        allow_space=False,
        allow_digits=False,
        allow_blank_lines=False,
        renderer=renderer,
    )
    markdown.inline.ruler.at("math_inline", _safe_inline_math)
    return markdown


def build_site_markdown_renderer() -> MarkdownIt:
    return _build_math_markdown_renderer(renderer=_render_site_math)


def render_site_math_fragment(*, source: str, display_mode: bool) -> str:
    rendered_math = _render_site_math(
        str(source or ""),
        {"display_mode": display_mode},
    )
    tag = "div" if display_mode else "span"
    mode_class = "block" if display_mode else "inline"
    return f'<{tag} class="math {mode_class}">{rendered_math}</{tag}>'


def build_email_markdown_renderer() -> MarkdownIt:
    return _build_math_markdown_renderer(renderer=_render_email_math)


def html_to_reader_text(html_text: str, *, separator: str = " ") -> str:
    soup = BeautifulSoup(str(html_text or ""), "html.parser")
    for math in soup.find_all("math"):
        annotation = math.find("annotation", attrs={"encoding": "application/x-tex"})
        source = (
            annotation.get_text("", strip=False)
            if annotation is not None
            else math.get_text(separator, strip=True)
        )
        math.replace_with(source)
    return soup.get_text(separator, strip=True)
