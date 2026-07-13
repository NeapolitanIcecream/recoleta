from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

import pytest

from pydantic_ai import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
import recoleta.rag.ideas_agent as ideas_agent_module
from recoleta.rag.ideas_agent import IdeasAgentDeps, build_trend_ideas_agent
import recoleta.rag.pydantic_ai_model as pydantic_ai_model_module
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload
from tests.spec_support import _build_runtime


def _never_called_function_model() -> FunctionModel:
    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages, info
        raise AssertionError("agent construction test should not call the model")

    return FunctionModel(model_fn)


def _ideas_payload(*, evidence_doc_ids: list[int] | None) -> dict[str, Any]:
    ideas: list[dict[str, Any]] = []
    if evidence_doc_ids is not None:
        ideas.append(
            {
                "title": "Auditable eval workbench",
                "content_md": "Build an auditable evaluation workbench for long runs.",
                "evidence_refs": [
                    {"doc_id": doc_id, "chunk_index": index}
                    for index, doc_id in enumerate(evidence_doc_ids)
                ],
            }
        )
    return {
        "title": "Ideas",
        "granularity": "day",
        "period_start": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "period_end": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
        "summary_md": "Grounded ideas, when the evidence supports them.",
        "ideas": ideas,
    }


def _ideas_agent_deps(*, repository: Any, tmp_path: Path) -> IdeasAgentDeps:
    return IdeasAgentDeps(
        repository=repository,
        vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
        run_id="run-ideas-agent-output-contract-test",
        period_start=datetime(2026, 1, 1, tzinfo=UTC),
        period_end=datetime(2026, 1, 2, tzinfo=UTC),
        rag_sources=None,
        embedding_model="test/embed",
        embedding_dimensions=None,
        embedding_batch_max_inputs=64,
        embedding_batch_max_chars=40_000,
    )


def test_trend_agent_uses_shared_model_factory_with_llm_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connection = LLMConnectionConfig(
        api_key="sk-recoleta-test",
        base_url="http://llm.local/v1/",
    )
    calls: list[tuple[str, LLMConnectionConfig | None]] = []

    def fake_build_pydantic_ai_model(
        llm_model: str, *, llm_connection: LLMConnectionConfig | None = None
    ) -> FunctionModel:
        calls.append((llm_model, llm_connection))
        return _never_called_function_model()

    monkeypatch.setattr(
        pydantic_ai_model_module,
        "build_pydantic_ai_model",
        fake_build_pydantic_ai_model,
    )

    build_trend_agent(
        llm_model="anthropic/claude-3-5-sonnet-20241022",
        llm_connection=connection,
    )

    assert calls == [("anthropic/claude-3-5-sonnet-20241022", connection)]


def test_ideas_agents_use_shared_model_factory_with_llm_connection(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    connection = LLMConnectionConfig(
        api_key="sk-recoleta-test",
        base_url="http://llm.local/v1/",
    )
    calls: list[tuple[str, LLMConnectionConfig | None]] = []

    def fake_build_pydantic_ai_model(
        llm_model: str, *, llm_connection: LLMConnectionConfig | None = None
    ) -> FunctionModel:
        calls.append((llm_model, llm_connection))
        return _never_called_function_model()

    monkeypatch.setattr(
        ideas_agent_module,
        "build_pydantic_ai_model",
        fake_build_pydantic_ai_model,
    )

    build_trend_ideas_agent(
        llm_model="anthropic/claude-3-5-sonnet-20241022",
        llm_connection=connection,
    )
    ideas_agent_module._build_trend_ideas_title_agent(
        llm_model="openrouter/anthropic/claude-3-5-sonnet",
        llm_connection=connection,
    )

    assert calls == [
        ("anthropic/claude-3-5-sonnet-20241022", connection),
        ("openrouter/anthropic/claude-3-5-sonnet", connection),
    ]


def test_trend_agent_validates_typed_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_agent(llm_model="openai/gpt-4o-mini")

    payload: dict[str, Any] = {
        "title": "Daily Trend",
        "granularity": "day",
        "period_start": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "period_end": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
        "overview_md": "Verification moved into the shipping path.",
        "topics": ["agents"],
        "clusters": [],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        tool_name = info.output_tools[0].name
        return ModelResponse(parts=[ToolCallPart(tool_name, payload)])

    deps = TrendAgentDeps(
        repository=repository,
        vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
        run_id="run-agent-test",
        period_start=datetime(2026, 1, 1, tzinfo=UTC),
        period_end=datetime(2026, 1, 2, tzinfo=UTC),
        rag_sources=None,
        embedding_model="test/embed",
        embedding_dimensions=None,
        embedding_batch_max_inputs=64,
        embedding_batch_max_chars=40_000,
    )

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(json.dumps({"task": "x"}), deps=deps)
        assert isinstance(result.output, TrendPayload)
        assert result.output.title == "Daily Trend"


def test_trend_agent_retries_output_validation_twice_before_accepting_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_agent(llm_model="openai/gpt-4o-mini")
    attempts = {"count": 0}
    valid_payload: dict[str, Any] = {
        "title": "Daily Trend",
        "granularity": "day",
        "period_start": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "period_end": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
        "overview_md": "Verification moved into the shipping path.",
        "topics": ["agents"],
        "clusters": [],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        attempts["count"] += 1
        payload = {"granularity": "day"} if attempts["count"] < 3 else valid_payload
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, payload)])

    deps = TrendAgentDeps(
        repository=repository,
        vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
        run_id="run-agent-retry-test",
        period_start=datetime(2026, 1, 1, tzinfo=UTC),
        period_end=datetime(2026, 1, 2, tzinfo=UTC),
        rag_sources=None,
        embedding_model="test/embed",
        embedding_dimensions=None,
        embedding_batch_max_inputs=64,
        embedding_batch_max_chars=40_000,
    )

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(json.dumps({"task": "x"}), deps=deps)

    assert isinstance(result.output, TrendPayload)
    assert result.output.title == "Daily Trend"
    assert attempts["count"] == 3


def test_ideas_agent_retries_output_validation_twice_before_accepting_output(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = {"count": 0}
    valid_payload: dict[str, Any] = {
        "title": "Ideas",
        "granularity": "day",
        "period_start": datetime(2026, 1, 1, tzinfo=UTC).isoformat(),
        "period_end": datetime(2026, 1, 2, tzinfo=UTC).isoformat(),
        "summary_md": "One grounded idea.",
        "ideas": [
            {
                "title": "Auditable eval workbench",
                "content_md": "Build an auditable evaluation workbench for long runs.",
                "evidence_refs": [
                    {"doc_id": 1, "chunk_index": 0},
                    {"doc_id": 2, "chunk_index": 0},
                ],
            }
        ],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        attempts["count"] += 1
        payload = {"granularity": "day"} if attempts["count"] < 3 else valid_payload
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, payload)])

    deps = IdeasAgentDeps(
        repository=repository,
        vector_store=LanceVectorStore(db_dir=tmp_path / "lancedb"),
        run_id="run-ideas-agent-retry-test",
        period_start=datetime(2026, 1, 1, tzinfo=UTC),
        period_end=datetime(2026, 1, 2, tzinfo=UTC),
        rag_sources=None,
        embedding_model="test/embed",
        embedding_dimensions=None,
        embedding_batch_max_inputs=64,
        embedding_batch_max_chars=40_000,
    )

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(json.dumps({"task": "x"}), deps=deps)

    assert result.output.title == "Ideas"
    assert attempts["count"] == 3


def test_ideas_agent_accepts_empty_ideas_without_retry(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = 0

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        nonlocal attempts
        _ = messages
        attempts += 1
        return ModelResponse(
            parts=[
                ToolCallPart(
                    info.output_tools[0].name,
                    _ideas_payload(evidence_doc_ids=None),
                )
            ]
        )

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(
            json.dumps({"task": "x"}),
            deps=_ideas_agent_deps(repository=repository, tmp_path=tmp_path),
        )

    assert result.output.ideas == []
    assert attempts == 1


@pytest.mark.parametrize(
    "invalid_doc_ids",
    ([], [1], [1, 1]),
    ids=("empty-references", "single-reference", "duplicate-document-references"),
)
def test_ideas_agent_retries_idea_without_two_distinct_document_refs(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    invalid_doc_ids: list[int],
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = 0
    retry_messages = ""

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        nonlocal attempts, retry_messages
        attempts += 1
        if attempts == 1:
            payload = _ideas_payload(evidence_doc_ids=invalid_doc_ids)
        else:
            retry_messages = repr(messages)
            payload = _ideas_payload(evidence_doc_ids=[1, 2])
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, payload)])

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(
            json.dumps({"task": "x"}),
            deps=_ideas_agent_deps(repository=repository, tmp_path=tmp_path),
        )

    assert [ref.doc_id for ref in result.output.ideas[0].evidence_refs] == [1, 2]
    assert attempts == 2
    assert "different positive doc_id values" in retry_messages


def test_ideas_agent_accepts_two_distinct_document_refs_without_retry(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = 0

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        nonlocal attempts
        _ = messages
        attempts += 1
        return ModelResponse(
            parts=[
                ToolCallPart(
                    info.output_tools[0].name,
                    _ideas_payload(evidence_doc_ids=[1, 2]),
                )
            ]
        )

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(
            json.dumps({"task": "x"}),
            deps=_ideas_agent_deps(repository=repository, tmp_path=tmp_path),
        )

    assert [ref.doc_id for ref in result.output.ideas[0].evidence_refs] == [1, 2]
    assert attempts == 1


@pytest.mark.parametrize(
    "oversized_content",
    (
        " ".join(["evidence"] * 281),
        "あ" * 551,
        "한" * 551,
        "🧪 " * 551,
        "中" * 400 + " AI" * 275,
        " ".join(["исследование"] * 281),
        "a" * 1_201,
        "! " * 3_201,
    ),
    ids=(
        "english-words",
        "japanese-kana",
        "korean-hangul",
        "emoji",
        "mixed-cjk-ascii",
        "russian-words",
        "unbroken-ascii",
        "universal-character-ceiling",
    ),
)
def test_ideas_agent_retries_oversized_idea_before_accepting_compact_prose(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    oversized_content: str,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = 0
    retry_messages = ""

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        nonlocal attempts, retry_messages
        attempts += 1
        payload = _ideas_payload(evidence_doc_ids=[1, 2])
        if attempts == 1:
            payload["ideas"][0]["content_md"] = oversized_content
        else:
            retry_messages = repr(messages)
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, payload)])

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(
            json.dumps({"task": "x"}),
            deps=_ideas_agent_deps(repository=repository, tmp_path=tmp_path),
        )

    assert result.output.ideas[0].content_md.startswith("Build an auditable")
    assert attempts == 2
    assert "280 whitespace-delimited words" in retry_messages


@pytest.mark.parametrize(
    "content_md",
    (
        " ".join(["evidence"] * 280),
        "あ" * 550,
        "한" * 550,
        "🧪 " * 550,
        " ".join(["исследование"] * 100),
        " ".join(["تجربة"] * 100),
        "a" * 1_200,
        (
            "Inspect https://example.com/runs/42?q=agent and compare "
            "`result = score / 100` before changing the pilot threshold."
        ),
    ),
    ids=(
        "english-word-boundary",
        "japanese-character-boundary",
        "korean-character-boundary",
        "emoji-character-boundary",
        "russian-spaced-prose",
        "arabic-spaced-prose",
        "unbroken-run-boundary",
        "normal-url-and-inline-code",
    ),
)
def test_ideas_agent_accepts_length_boundaries_and_normal_markup_without_retry(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    content_md: str,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")

    _, repository = _build_runtime()
    agent = build_trend_ideas_agent(llm_model="openai/gpt-4o-mini")
    attempts = 0

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        nonlocal attempts
        _ = messages
        attempts += 1
        payload = _ideas_payload(evidence_doc_ids=[1, 2])
        payload["ideas"][0]["content_md"] = content_md
        return ModelResponse(parts=[ToolCallPart(info.output_tools[0].name, payload)])

    with agent.override(model=FunctionModel(model_fn)):
        result = agent.run_sync(
            json.dumps({"task": "x"}),
            deps=_ideas_agent_deps(repository=repository, tmp_path=tmp_path),
        )

    assert result.output.ideas[0].content_md == content_md.strip()
    assert attempts == 1
