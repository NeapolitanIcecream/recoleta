from __future__ import annotations

import json
import time
from typing import Protocol

from litellm import completion
from pydantic import BaseModel, Field

from recoleta.types import AnalysisResult


class Analyzer(Protocol):
    def analyze(self, *, title: str, canonical_url: str, user_topics: list[str]) -> AnalysisResult: ...


class _AnalysisPayload(BaseModel):
    summary: str
    insight: str
    idea_directions: list[str]
    topics: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    novelty_score: float | None = Field(default=None, ge=0.0, le=1.0)


class LiteLLMAnalyzer:
    def __init__(self, *, model: str) -> None:
        self.model = model

    def analyze(self, *, title: str, canonical_url: str, user_topics: list[str]) -> AnalysisResult:
        prompt = self._build_prompt(title=title, canonical_url=canonical_url, user_topics=user_topics)
        started = time.perf_counter()
        response = completion(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a research signal analyst. Return strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        raw_content = _extract_content(response)
        payload = _AnalysisPayload.model_validate(json.loads(raw_content))
        provider = self.model.split("/", 1)[0] if "/" in self.model else "unknown"
        return AnalysisResult(
            model=self.model,
            provider=provider,
            summary=payload.summary,
            insight=payload.insight,
            idea_directions=payload.idea_directions,
            topics=payload.topics,
            relevance_score=payload.relevance_score,
            novelty_score=payload.novelty_score,
            cost_usd=None,
            latency_ms=elapsed_ms,
        )

    @staticmethod
    def _build_prompt(*, title: str, canonical_url: str, user_topics: list[str]) -> str:
        serialized_topics = ", ".join(user_topics) if user_topics else "general technology"
        return (
            "Analyze one research item and return a JSON object with keys: "
            "summary, insight, idea_directions, topics, relevance_score, novelty_score.\n"
            "Constraints:\n"
            "- summary: <= 120 words\n"
            "- insight: <= 80 words\n"
            "- idea_directions: 2 to 4 short bullet-like strings\n"
            "- topics: up to 5 concise tags\n"
            "- relevance_score and novelty_score in [0,1]\n"
            f"User topics: {serialized_topics}\n"
            f"Title: {title}\n"
            f"URL: {canonical_url}\n"
        )


def _extract_content(response: object) -> str:
    if isinstance(response, dict):
        return str(response["choices"][0]["message"]["content"])
    choices = getattr(response, "choices")
    first_choice = choices[0]
    return str(first_choice.message.content)
