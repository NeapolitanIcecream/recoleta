from __future__ import annotations

from recoleta import translation as translation_module


def test_translation_system_message_includes_shared_ai_tropes_prompt() -> None:
    system_message = translation_module._build_translation_system_message()

    assert "Return strict JSON only." in system_message
    assert "The goal is not to ban every phrase once." in system_message
    assert "Avoid negative parallelism" in system_message
    assert "Avoid false suspense" in system_message
    assert "Avoid fractal summaries" in system_message
    assert "When multiple target-language phrasings are equally faithful" in system_message
