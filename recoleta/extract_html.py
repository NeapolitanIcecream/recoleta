from __future__ import annotations

from typing import Any

from bs4 import BeautifulSoup
from bs4.element import Tag


def _has_semantic_payload(tag: Tag) -> bool:
    if tag.find(["math", "table", "pre", "code", "svg", "img"]):
        return True
    class_attr = tag.get("class")
    classes = (
        [str(c) for c in class_attr]
        if isinstance(class_attr, list)
        else [str(class_attr)]
        if class_attr
        else []
    )
    class_blob = " ".join(classes).lower()
    keep_markers = (
        "math",
        "equation",
        "eqn",
        "align",
        "matrix",
        "tabular",
        "table",
        "listing",
        "verbatim",
        "code",
        "algorithm",
        "figure",
        "caption",
    )
    return any(marker in class_blob for marker in keep_markers)


def _remove_metadata_blocks(container: Tag) -> int:
    removed_metadata = 0
    metadata_selectors = [
        ".ltx_authors",
        ".ltx_author_notes",
        ".ltx_affiliation",
        ".ltx_contact",
        ".ltx_role_orcid",
        ".ltx_role_email",
        ".ltx_role_author",
        ".ltx_creator",
        ".ltx_date",
    ]
    for selector in metadata_selectors:
        for tag in list(container.select(selector)):
            tag.decompose()
            removed_metadata += 1
    return removed_metadata


def _unwrap_contact_links(container: Tag) -> None:
    for anchor in list(container.find_all("a")):
        href = str(anchor.get("href") or "")
        if "mailto:" in href or "orcid.org" in href:
            anchor.unwrap()


def _math_subtree_ids(container: Tag) -> set[int]:
    math_subtree_ids: set[int] = set()
    for math_root in list(container.find_all("math")):
        math_subtree_ids.add(id(math_root))
        for descendant in math_root.find_all(True):
            math_subtree_ids.add(id(descendant))
    return math_subtree_ids


def _strip_non_math_attrs(container: Tag, *, math_subtree_ids: set[int]) -> int:
    allowed_attrs = {"colspan", "rowspan", "href", "src", "alt"}
    removed_attrs = 0
    for tag in container.find_all(True):
        if math_subtree_ids and id(tag) in math_subtree_ids:
            continue
        attrs = dict(getattr(tag, "attrs", {}) or {})
        if not attrs:
            continue
        new_attrs = {key: value for key, value in attrs.items() if key in allowed_attrs}
        if new_attrs != attrs:
            removed_attrs += len(attrs) - len(new_attrs)
            tag.attrs = new_attrs
    return removed_attrs


def _unwrap_presentational_wrappers(container: Tag) -> int:
    unwrapped = 0
    for tag_name in ("span", "div"):
        for tag in list(container.find_all(tag_name)):
            if _has_semantic_payload(tag):
                continue
            if tag.name in {"section", "article"}:
                continue
            try:
                tag.unwrap()
                unwrapped += 1
            except Exception:
                continue
    return unwrapped


def simplify_arxiv_html(container: Tag) -> dict[str, int]:
    removed_metadata = _remove_metadata_blocks(container)
    _unwrap_contact_links(container)
    math_subtree_ids = _math_subtree_ids(container)
    removed_attrs = _strip_non_math_attrs(
        container,
        math_subtree_ids=math_subtree_ids,
    )
    unwrapped = _unwrap_presentational_wrappers(container)
    return {
        "removed_metadata_blocks": removed_metadata,
        "unwrapped_wrappers": unwrapped,
        "removed_attrs_total": removed_attrs,
    }


def _main_container(soup: BeautifulSoup) -> Tag:
    main_container = soup.find("main")
    if main_container is None:
        main_container = soup.find("article")
    if main_container is None:
        main_container = soup.body if soup.body is not None else soup
    return main_container


def _strip_global_tags(soup: BeautifulSoup) -> None:
    for tag in soup(["script", "style", "noscript", "iframe"]):
        tag.decompose()
    for tag_name in ("nav", "header", "footer", "aside", "form"):
        for tag in soup.find_all(tag_name):
            tag.decompose()


def _remove_non_body_blocks(main_container: Tag) -> int:
    removed_non_body = 0
    non_body_selectors = [
        '[role="navigation"]',
        '[aria-label="navigation"]',
        ".toc",
        ".ltx_toc",
        ".ltx_role_toc",
        ".ltx_page_header",
        ".ltx_page_footer",
        ".ltx_sidebar",
        ".sidebar",
    ]
    for selector in non_body_selectors:
        for tag in list(main_container.select(selector)):
            tag.decompose()
            removed_non_body += 1
    return removed_non_body


def _is_reference_heading(text: str) -> bool:
    normalized = " ".join(text.strip().lower().split())
    return normalized in {"references", "bibliography"}


def _extract_reference_selector_blocks(main_container: Tag) -> tuple[list[str], int]:
    references_blocks: list[str] = []
    removed_references = 0
    for tag in list(
        main_container.select(
            ".ltx_bibliography, .ltx_biblist, .ltx_references, #references, #bibliography, .references, .bibliography"
        )
    ):
        references_blocks.append(str(tag))
        tag.decompose()
        removed_references += 1
    return references_blocks, removed_references


def _heading_level(tag: Any) -> int:
    try:
        return int(str(getattr(tag, "name"))[1])
    except Exception:
        return 6


def _collect_reference_heading_block(heading: Tag) -> str:
    level = _heading_level(heading)
    collected: list[str] = [str(heading)]
    current = heading.next_sibling
    while current is not None:
        next_node = getattr(current, "next_sibling", None)
        if getattr(current, "name", None) in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            if _heading_level(current) <= level:
                break
        try:
            collected.append(str(current))
            current.extract()
        except Exception:
            pass
        current = next_node
    try:
        heading.decompose()
    except Exception:
        pass
    return "\n".join(collected)


def _extract_reference_heading_blocks(main_container: Tag) -> tuple[list[str], int]:
    references_blocks: list[str] = []
    removed_references = 0
    for heading in list(main_container.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])):
        heading_text = heading.get_text(" ", strip=True)
        if not heading_text or not _is_reference_heading(heading_text):
            continue
        parent = heading.parent
        if parent is None:
            continue
        if parent.name in {"section", "div"} and parent.get_text(" ", strip=True):
            references_blocks.append(str(parent))
            parent.decompose()
            removed_references += 1
            continue
        references_blocks.append(_collect_reference_heading_block(heading))
        removed_references += 1
    return references_blocks, removed_references


def _extract_reference_blocks(main_container: Tag) -> tuple[list[str], int]:
    selector_blocks, selector_removed = _extract_reference_selector_blocks(
        main_container
    )
    heading_blocks, heading_removed = _extract_reference_heading_blocks(main_container)
    return selector_blocks + heading_blocks, selector_removed + heading_removed


def _normalize_html_fragment(fragment: str, *, limit: int) -> str | None:
    normalized_lines = [line.strip() for line in fragment.splitlines() if line.strip()]
    combined = "\n".join(normalized_lines).strip()
    if not combined:
        return None
    if limit > 0 and len(combined) > limit:
        combined = combined[:limit].rstrip()
    return combined or None


def extract_html_document_cleaned_with_references_impl(
    html: str,
    *,
    max_chars: int,
    references_max_chars: int,
) -> tuple[str | None, str | None, dict[str, Any]]:
    stripped = html.strip()
    if not stripped:
        return None, None, {"error": "empty_input"}
    soup = BeautifulSoup(stripped, "html.parser")
    _strip_global_tags(soup)
    main_container = _main_container(soup)
    if not main_container.get_text(" ", strip=True):
        return None, None, {"error": "empty_main_container"}
    removed_non_body = _remove_non_body_blocks(main_container)
    references_blocks, removed_references = _extract_reference_blocks(main_container)
    simplify_stats = simplify_arxiv_html(main_container)
    cleaned_html = _normalize_html_fragment(str(main_container), limit=max_chars)
    references_html = (
        _normalize_html_fragment(
            "\n\n".join(references_blocks), limit=references_max_chars
        )
        if references_blocks
        else None
    )
    stats: dict[str, Any] = {
        "removed_non_body_blocks": removed_non_body,
        "removed_references_blocks": removed_references,
        "references_blocks_collected": len(references_blocks),
        "cleaned_chars": len(cleaned_html or ""),
        "references_chars": len(references_html or ""),
        **simplify_stats,
    }
    return cleaned_html, references_html, stats
