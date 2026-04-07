from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

import pytest

from pydantic_ai import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
from recoleta.rag.ideas_agent import IdeasAgentDeps, build_trend_ideas_agent
from recoleta.rag.vector_store import LanceVectorStore
from recoleta.trends import TrendPayload
from tests.spec_support import _build_runtime


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
        "overview_md": "- ok",
        "topics": ["agents"],
        "clusters": [],
        "highlights": ["agents"],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        assert info.output_tools
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
        "overview_md": "- ok",
        "topics": ["agents"],
        "clusters": [],
        "highlights": ["agents"],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        assert info.output_tools
        tool_name = info.output_tools[0].name
        attempts["count"] += 1
        payload = {"granularity": "day"} if attempts["count"] < 3 else valid_payload
        return ModelResponse(parts=[ToolCallPart(tool_name, payload)])

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
                "kind": "tooling_wedge",
                "thesis": "Build an auditable evaluation workbench.",
                "why_now": "Grounded traces are now cheap enough to keep.",
                "what_changed": "Teams can inspect long-horizon runs directly.",
                "user_or_job": "Evaluation teams debugging agent regressions.",
                "evidence_refs": [{"doc_id": 1, "chunk_index": 0}],
                "validation_next_step": "Pilot one benchmark workflow.",
                "time_horizon": "now",
            }
        ],
    }

    def model_fn(messages: list[ModelMessage], info: AgentInfo) -> ModelResponse:
        _ = messages
        assert info.output_tools
        tool_name = info.output_tools[0].name
        attempts["count"] += 1
        payload = {"granularity": "day"} if attempts["count"] < 3 else valid_payload
        return ModelResponse(parts=[ToolCallPart(tool_name, payload)])

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
