from __future__ import annotations

import json

import pytest

from recoleta.passes.trend_ideas import TrendIdeasPayload
from recoleta.translation_llm import (
    TranslationLLMDeps,
    TranslationLLMOutputError,
    TranslationLLMRequest,
    translate_structured_payload_with_debug,
)


def _ideas_payload() -> dict[str, object]:
    return {
        "title": "Ideas",
        "granularity": "day",
        "period_start": "2026-03-30T00:00:00+00:00",
        "period_end": "2026-03-31T00:00:00+00:00",
        "summary_md": "One grounded idea.",
        "ideas": [
            {
                "title": "Auditable eval workbench",
                "kind": "tooling_wedge",
                "thesis": "Build an auditable evaluation workbench.",
                "why_now": "Grounded traces are now cheap enough to keep.",
                "what_changed": "Teams can inspect long-horizon runs directly.",
                "user_or_job": "Evaluation teams debugging agent regressions.",
                "evidence_refs": [{"doc_id": 1, "chunk_index": 0}],
                "validation_next_step": "Pilot the workbench with one benchmark.",
                "time_horizon": "now",
            }
        ],
    }


def test_translate_structured_payload_retries_after_invalid_json() -> None:
    attempts = {"count": 0}
    raw_responses = [
        '{"title":"Ideas"',
        json.dumps(_ideas_payload(), ensure_ascii=False),
    ]

    def _completion(**_: object) -> object:
        response = {"raw": raw_responses[attempts["count"]]}
        attempts["count"] += 1
        return response

    translated, debug = translate_structured_payload_with_debug(
        TranslationLLMRequest(
            model="test/fake-model",
            source_kind="trend_ideas",
            payload=_ideas_payload(),
            source_language_code="en",
            target_language_code="zh-CN",
            payload_model=TrendIdeasPayload,
        ),
        TranslationLLMDeps(
            completion_factory=lambda: _completion,
            extract_usage_dict_fn=lambda response: {"requests": 1, "cost": response},
            extract_token_counts_fn=lambda usage: (10, 5, 15),
            extract_content_fn=lambda response: response["raw"],
            resolve_response_cost_usd_fn=lambda **_: 0.01,
        ),
    )

    assert attempts["count"] == 2
    assert translated["title"] == "Ideas"
    assert debug["usage"]["requests"] == 2
    assert debug["estimated_cost_usd"] == 0.02
    assert debug["retry"]["attempts_total"] == 2


def test_translate_structured_payload_retries_after_schema_validation_error() -> None:
    attempts = {"count": 0}
    raw_responses = [
        json.dumps({"title": "Ideas"}, ensure_ascii=False),
        json.dumps(_ideas_payload(), ensure_ascii=False),
    ]

    def _completion(**_: object) -> object:
        response = {"raw": raw_responses[attempts["count"]]}
        attempts["count"] += 1
        return response

    translated, debug = translate_structured_payload_with_debug(
        TranslationLLMRequest(
            model="test/fake-model",
            source_kind="trend_ideas",
            payload=_ideas_payload(),
            source_language_code="en",
            target_language_code="zh-CN",
            payload_model=TrendIdeasPayload,
        ),
        TranslationLLMDeps(
            completion_factory=lambda: _completion,
            extract_usage_dict_fn=lambda response: {"requests": 1, "cost": response},
            extract_token_counts_fn=lambda usage: (12, 6, 18),
            extract_content_fn=lambda response: response["raw"],
            resolve_response_cost_usd_fn=lambda **_: 0.02,
        ),
    )

    assert attempts["count"] == 2
    assert translated["summary_md"] == "One grounded idea."
    assert debug["usage"]["requests"] == 2
    assert debug["estimated_cost_usd"] == 0.04
    assert debug["retry"]["attempts_total"] == 2


def test_translate_structured_payload_retries_after_missing_content() -> None:
    attempts = {"count": 0}
    raw_responses = [
        None,
        json.dumps(_ideas_payload(), ensure_ascii=False),
    ]

    def _completion(**_: object) -> object:
        response = {"raw": raw_responses[attempts["count"]]}
        attempts["count"] += 1
        return response

    translated, debug = translate_structured_payload_with_debug(
        TranslationLLMRequest(
            model="test/fake-model",
            source_kind="trend_ideas",
            payload=_ideas_payload(),
            source_language_code="en",
            target_language_code="zh-CN",
            payload_model=TrendIdeasPayload,
        ),
        TranslationLLMDeps(
            completion_factory=lambda: _completion,
            extract_usage_dict_fn=lambda response: {"requests": 1, "cost": response},
            extract_token_counts_fn=lambda usage: (10, 5, 15),
            extract_content_fn=lambda response: response["raw"],
            resolve_response_cost_usd_fn=lambda **_: 0.01,
        ),
    )

    assert attempts["count"] == 2
    assert translated["title"] == "Ideas"
    assert debug["retry"]["attempts_total"] == 2
    assert debug["retry"]["attempts"][0]["reason"] == "empty_content"


def test_translate_structured_payload_classifies_content_filter_responses() -> None:
    attempts = {"count": 0}

    def _completion(**_: object) -> object:
        attempts["count"] += 1
        return {
            "choices": [
                {
                    "finish_reason": "content_filter",
                    "message": {
                        "content": "I'm sorry, but I cannot assist with that request."
                    },
                }
            ],
            "usage": {"prompt_tokens": 10, "completion_tokens": 1, "total_tokens": 11},
        }

    with pytest.raises(TranslationLLMOutputError) as excinfo:
        translate_structured_payload_with_debug(
            TranslationLLMRequest(
                model="test/fake-model",
                source_kind="trend_ideas",
                payload=_ideas_payload(),
                source_language_code="en",
                target_language_code="zh-CN",
                payload_model=TrendIdeasPayload,
            ),
            TranslationLLMDeps(
                completion_factory=lambda: _completion,
                resolve_response_cost_usd_fn=lambda **_: 0.01,
            ),
        )

    assert attempts["count"] == 3
    assert excinfo.value.reason == "content_filter"
    assert excinfo.value.finish_reason == "content_filter"


def test_translate_structured_payload_ignores_non_output_text_parts() -> None:
    translated, debug = translate_structured_payload_with_debug(
        TranslationLLMRequest(
            model="test/fake-model",
            source_kind="trend_ideas",
            payload=_ideas_payload(),
            source_language_code="en",
            target_language_code="zh-CN",
            payload_model=TrendIdeasPayload,
        ),
        TranslationLLMDeps(
            completion_factory=lambda: (
                lambda **_: {
                    "choices": [
                        {
                            "finish_reason": "stop",
                            "message": {
                                "content": [
                                    {
                                        "type": "reasoning",
                                        "text": "internal reasoning that is not JSON",
                                    },
                                    {
                                        "type": "output_text",
                                        "text": json.dumps(_ideas_payload(), ensure_ascii=False),
                                    },
                                ]
                            },
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 10,
                        "completion_tokens": 5,
                        "total_tokens": 15,
                    },
                }
            ),
            resolve_response_cost_usd_fn=lambda **_: 0.01,
        ),
    )

    assert translated["title"] == "Ideas"
    assert debug["usage"]["requests"] == 1
