from __future__ import annotations

from recoleta import translation as translation_module


def test_translation_system_message_includes_shared_ai_tropes_prompt() -> None:
    system_message = translation_module._build_translation_system_message()

    assert "Return strict JSON only." in system_message
    assert (
        "Write reader-facing prose as an editor working from specific evidence."
        in system_message
    )
    assert "Do not use negative parallelism" in system_message
    assert "Do not use suspense, rhetorical questions" in system_message
    assert "Do not preview, restate, and conclude the same point" in system_message
    assert (
        "When multiple target-language phrasings are equally faithful" in system_message
    )
