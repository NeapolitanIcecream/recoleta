from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

import pytest

from pydantic_ai import ModelMessage, ModelResponse, ToolCallPart
from pydantic_ai.models.function import AgentInfo, FunctionModel

from recoleta.rag.agent import TrendAgentDeps, build_trend_agent
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
