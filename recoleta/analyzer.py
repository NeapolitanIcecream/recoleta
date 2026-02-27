from __future__ import annotations

import json
import time
from typing import Any, Protocol

from litellm import completion
from pydantic import BaseModel, Field

from recoleta.types import AnalysisResult, AnalyzeDebug


class Analyzer(Protocol):
    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]: ...


class _AnalysisPayload(BaseModel):
    summary: str
    insight: str
    idea_directions: list[str]
    topics: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    novelty_score: float | None = Field(default=None, ge=0.0, le=1.0)


class LiteLLMAnalyzer:
    def __init__(self, *, model: str, output_language: str | None = None) -> None:
        self.model = model
        self.output_language = output_language

    def analyze(
        self,
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None = None,
        include_debug: bool = False,
    ) -> tuple[AnalysisResult, AnalyzeDebug | None]:
        prompt = self._build_prompt(
            title=title,
            canonical_url=canonical_url,
            user_topics=user_topics,
            content=content,
        )
        started = time.perf_counter()
        messages = [
            {"role": "system", "content": self._build_system_message()},
            {"role": "user", "content": prompt},
        ]
        response = completion(
            model=self.model,
            messages=messages,
            response_format={"type": "json_object"},
        )
        elapsed_ms = int((time.perf_counter() - started) * 1000)
        raw_content = _extract_content(response)
        payload = _AnalysisPayload.model_validate(json.loads(raw_content))
        provider = self.model.split("/", 1)[0] if "/" in self.model else "unknown"
        result = AnalysisResult(
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
        if not include_debug:
            return result, None

        request_debug: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
        }
        response_debug: dict[str, Any] = {
            "elapsed_ms": elapsed_ms,
            "content": raw_content,
            "parsed": payload.model_dump(mode="json"),
        }
        return result, AnalyzeDebug(request=request_debug, response=response_debug)

    @staticmethod
    def _build_prompt(*, title: str, canonical_url: str, user_topics: list[str], content: str | None) -> str:
        serialized_topics = ", ".join(user_topics) if user_topics else "general technology"
        trimmed_content = (content or "").strip()
        if len(trimmed_content) > 5000:
            trimmed_content = trimmed_content[:5000] + "\n...[truncated]..."
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
            + (f"Content excerpt:\n{trimmed_content}\n" if trimmed_content else "")
        )

    def _build_system_message(self) -> str:
        base_message = "You are a research signal analyst. Return strict JSON only."
        if not self.output_language:
            return base_message
        return (
            f"{base_message} Use {self.output_language} for summary, insight, and idea_directions values. "
            "Keep all JSON keys in English and keep topics as concise English tags."
        )


def _extract_content(response: object) -> str:
    if isinstance(response, dict):
        return str(response["choices"][0]["message"]["content"])
    choices = getattr(response, "choices")
    first_choice = choices[0]
    return str(first_choice.message.content)
