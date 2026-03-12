from __future__ import annotations

from recoleta.publish.trend_render_shared import clamp_trend_overview_markdown


def test_clamp_trend_overview_markdown_preserves_short_markdown_links() -> None:
    overview = (
        "## Overview\n\n"
        "Start with [Robometer](../Inbox/2026-03-02--robometer.md).\n"
    )

    clamped = clamp_trend_overview_markdown(overview)

    assert clamped == "Start with [Robometer](../Inbox/2026-03-02--robometer.md)."


def test_clamp_trend_overview_markdown_preserves_short_markdown_links_in_chinese_mode() -> None:
    overview = (
        "## Overview\n\n"
        "Start with [Robometer](../Inbox/2026-03-02--robometer.md).\n"
    )

    clamped = clamp_trend_overview_markdown(overview, output_language="zh-CN")

    assert clamped == "Start with [Robometer](../Inbox/2026-03-02--robometer.md)."
