from __future__ import annotations

from bs4 import BeautifulSoup, Tag

from recoleta.markdown_render import (
    build_email_markdown_renderer,
    build_site_markdown_renderer,
    html_to_reader_text,
)


def test_site_markdown_renders_inline_and_display_math_semantically() -> None:
    rendered = build_site_markdown_renderer().render(
        "Energy follows $E=mc^2$.\n\n$$\\frac{a}{b}$$"
    )
    soup = BeautifulSoup(rendered, "html.parser")

    inline_math = soup.select_one(".math.inline math[display='inline']")
    display_math = soup.select_one(".math.block math[display='block']")

    assert inline_math is not None
    assert display_math is not None
    inline_annotation = inline_math.select_one(
        "annotation[encoding='application/x-tex']"
    )
    display_annotation = display_math.select_one(
        "annotation[encoding='application/x-tex']"
    )
    assert isinstance(inline_annotation, Tag)
    assert isinstance(display_annotation, Tag)
    assert inline_annotation.get_text() == "E=mc^2"
    assert display_annotation.get_text() == r"\frac{a}{b}"


def test_site_math_delimiters_do_not_consume_currency_code_or_escaped_dollars() -> None:
    rendered = build_site_markdown_renderer().render(
        r"A copy costs $5 and two cost $10. Keep `$z$` literal, write \$20, then use $x$."
    )
    soup = BeautifulSoup(rendered, "html.parser")

    assert len(soup.select(".math")) == 1
    annotation = soup.select_one(".math annotation")
    code = soup.select_one("code")
    assert isinstance(annotation, Tag)
    assert isinstance(code, Tag)
    assert annotation.get_text() == "x"
    assert code.get_text() == "$z$"
    assert "costs $5" in soup.get_text(" ", strip=True)
    assert "$20" in soup.get_text(" ", strip=True)


def test_site_math_delimiters_do_not_consume_cjk_currency_text() -> None:
    rendered = build_site_markdown_renderer().render("中文价格$5，公式$x$。")
    soup = BeautifulSoup(rendered, "html.parser")

    annotations = soup.select(".math annotation")
    assert [annotation.get_text() for annotation in annotations] == ["x"]
    assert "中文价格$5，公式" in soup.get_text("", strip=True)


def test_site_inline_math_allows_adjacent_cjk_prose() -> None:
    rendered = build_site_markdown_renderer().render("公式$x$满足约束。")
    soup = BeautifulSoup(rendered, "html.parser")

    annotation = soup.select_one(".math.inline annotation")
    assert isinstance(annotation, Tag)
    assert annotation.get_text() == "x"
    assert "公式" in soup.get_text("", strip=True)
    assert "满足约束。" in soup.get_text("", strip=True)


def test_site_mathml_drops_source_controlled_url_and_style_attributes() -> None:
    rendered = build_site_markdown_renderer().render(
        r"$\href{javascript:alert(1)}{x}+\style{position:fixed;color:red}{y}$"
    )
    soup = BeautifulSoup(rendered, "html.parser")

    math = soup.find("math")
    assert isinstance(math, Tag)
    assert all(
        not any(
            name in {"class", "href", "id", "src", "style"} or name.startswith("on")
            for name in tag.attrs
        )
        for tag in math.find_all(True)
    )


def test_site_mathml_drops_unbounded_dimension_attributes() -> None:
    rendered = build_site_markdown_renderer().render(
        r"$\rule{100000em}{100000em}+\hspace{100000em}x$"
    )
    soup = BeautifulSoup(rendered, "html.parser")
    math = soup.find("math")
    assert isinstance(math, Tag)
    dimension_attributes = {
        "columnspacing",
        "depth",
        "framespacing",
        "height",
        "linethickness",
        "lspace",
        "mathsize",
        "maxsize",
        "minsize",
        "rowspacing",
        "rspace",
        "voffset",
        "width",
    }
    assert all(
        dimension_attributes.isdisjoint(tag.attrs)
        for tag in [math, *math.find_all(True)]
    )


def test_invalid_tex_remains_visible_in_site_output() -> None:
    rendered = build_site_markdown_renderer().render("Before $x_$ after.")
    soup = BeautifulSoup(rendered, "html.parser")

    assert soup.select_one("math") is None
    fallback = soup.select_one(".math-source-fallback")
    assert fallback is not None
    assert fallback.get_text() == "$x_$"


def test_reader_text_contains_each_formula_source_once() -> None:
    rendered = build_site_markdown_renderer().render(
        "Energy follows $E=mc^2$.\n\n$$\\frac{a}{b}$$"
    )

    reader_text = html_to_reader_text(rendered)

    assert reader_text.count("E=mc^2") == 1
    assert reader_text.count(r"\frac{a}{b}") == 1


def test_email_markdown_keeps_tex_without_emitting_mathml_or_images() -> None:
    rendered = build_email_markdown_renderer().render(
        "Energy follows $E=mc^2$.\n\n$$\\frac{a}{b}$$"
    )
    soup = BeautifulSoup(rendered, "html.parser")

    assert soup.find("math") is None
    assert soup.find("img") is None
    inline_code = soup.select_one(".math.inline code")
    display_code = soup.select_one(".math.block pre code")
    assert isinstance(inline_code, Tag)
    assert isinstance(display_code, Tag)
    assert inline_code.get_text() == "$E=mc^2$"
    assert display_code.get_text() == r"$$\frac{a}{b}$$"
