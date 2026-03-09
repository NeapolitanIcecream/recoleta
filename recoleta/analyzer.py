from __future__ import annotations

import json
import time
from collections.abc import Callable
from typing import Any, Protocol

from loguru import logger
from pydantic import BaseModel, Field
from pydantic import ValidationError
from tenacity import RetryCallState, Retrying, retry_if_exception, stop_after_attempt
from tenacity.wait import wait_base, wait_exponential_jitter

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.observability import collect_environment_secrets, scrub_secrets
from recoleta.types import AnalysisResult, AnalyzeDebug

completion: Any | None = None
_SCRUB_SECRETS: tuple[str, ...] | None = None
_retry_sleep: Callable[[float], None] = time.sleep


def _get_completion() -> Any:
    global completion  # noqa: PLW0603
    if completion is None:
        from litellm import completion as _completion

        completion = _completion
    return completion


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
    topics: list[str]
    relevance_score: float = Field(ge=0.0, le=1.0)
    novelty_score: float | None = Field(default=None, ge=0.0, le=1.0)


class _AnalyzeRetryableError(RuntimeError):
    pass


def _get_scrub_secrets() -> tuple[str, ...]:
    global _SCRUB_SECRETS  # noqa: PLW0603
    if _SCRUB_SECRETS is None:
        _SCRUB_SECRETS = collect_environment_secrets()
    return _SCRUB_SECRETS


def _sanitize_error_message(message: str, *, max_len: int = 400) -> str:
    scrubbed = scrub_secrets(message, secrets=_get_scrub_secrets())
    if len(scrubbed) <= max_len:
        return scrubbed
    return scrubbed[:max_len] + "...[truncated]"


def _should_retry_llm(exc: BaseException) -> bool:
    try:
        import litellm
    except Exception:
        return isinstance(exc, _AnalyzeRetryableError)

    candidates = (
        getattr(litellm, "RateLimitError", None),
        getattr(litellm, "ServiceUnavailableError", None),
        getattr(litellm, "Timeout", None),
        getattr(litellm, "APIError", None),
    )
    retryable_types = tuple(
        candidate for candidate in candidates if isinstance(candidate, type)
    )
    if retryable_types and isinstance(exc, retryable_types):
        return True
    return isinstance(exc, _AnalyzeRetryableError)


class _LiteLLMWait(wait_base):
    def __init__(self) -> None:
        self._fallback = wait_exponential_jitter(initial=0.5, max=8.0)

    def __call__(self, retry_state: RetryCallState) -> float:
        if retry_state.outcome is None:
            return self._fallback(retry_state)
        exc = retry_state.outcome.exception()
        retry_after = getattr(exc, "retry_after", None)
        if retry_after is None:
            return self._fallback(retry_state)
        try:
            return max(0.0, min(30.0, float(retry_after)))
        except Exception:
            return self._fallback(retry_state)


class LiteLLMAnalyzer:
    def __init__(
        self,
        *,
        model: str,
        output_language: str | None = None,
        content_max_chars: int = 5000,
        llm_connection: LLMConnectionConfig | None = None,
    ) -> None:
        self.model = model
        self.output_language = output_language
        self.content_max_chars = max(0, int(content_max_chars))
        self.llm_connection = llm_connection or LLMConnectionConfig()

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
            content_max_chars=self.content_max_chars,
        )
        started = time.perf_counter()
        messages = [
            {"role": "system", "content": self._build_system_message()},
            {"role": "user", "content": prompt},
        ]

        log = logger.bind(module="analyzer.llm", model=self.model)
        retry_attempts: list[dict[str, Any]] = []

        def _before_sleep(retry_state: RetryCallState) -> None:
            if retry_state.outcome is None:
                return
            exc = retry_state.outcome.exception()
            if exc is None:
                return
            sleep_s = 0.0
            next_action = getattr(retry_state, "next_action", None)
            if next_action is not None:
                sleep_s = float(getattr(next_action, "sleep", 0.0) or 0.0)

            retry_attempts.append(
                {
                    "attempt": int(retry_state.attempt_number),
                    "error_type": type(exc).__name__,
                    "error_message": _sanitize_error_message(str(exc)),
                    "retryable": bool(_should_retry_llm(exc)),
                    "sleep_s": sleep_s,
                }
            )
            log.opt(exception=False).warning(
                "Analyze LLM call retrying attempt={} sleep_s={} error_type={} error={}",
                retry_state.attempt_number,
                round(sleep_s, 3),
                type(exc).__name__,
                _sanitize_error_message(str(exc)),
            )

        def _call_and_parse() -> tuple[_AnalysisPayload, str, object]:
            response = _get_completion()(
                model=self.model,
                messages=messages,
                response_format={"type": "json_object"},
                **self.llm_connection.litellm_completion_kwargs(),
            )
            raw_content = _extract_content(response)
            try:
                decoded = json.loads(raw_content)
            except json.JSONDecodeError as exc:
                raise _AnalyzeRetryableError(
                    f"LLM returned invalid JSON: {exc.msg}"
                ) from exc
            try:
                payload = _AnalysisPayload.model_validate(decoded)
            except ValidationError as exc:
                raise _AnalyzeRetryableError(
                    f"LLM returned JSON with invalid schema: {type(exc).__name__}"
                ) from exc
            return payload, raw_content, response

        retrying = Retrying(
            retry=retry_if_exception(_should_retry_llm),
            stop=stop_after_attempt(4),
            wait=_LiteLLMWait(),
            sleep=_retry_sleep,
            before_sleep=_before_sleep,
            reraise=True,
        )
        payload, raw_content, response = retrying(_call_and_parse)

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        provider = self.model.split("/", 1)[0] if "/" in self.model else "unknown"
        usage = _extract_usage_dict(response)
        prompt_tokens, completion_tokens, total_tokens = _extract_token_counts(usage)
        cost_usd = _extract_response_cost_usd(response)
        if cost_usd is None:
            try:
                from litellm.cost_calculator import completion_cost

                cost_usd = float(completion_cost(completion_response=response))
            except Exception:
                cost_usd = None
        result = AnalysisResult(
            model=self.model,
            provider=provider,
            summary=payload.summary,
            topics=payload.topics,
            relevance_score=payload.relevance_score,
            novelty_score=payload.novelty_score,
            cost_usd=cost_usd,
            latency_ms=elapsed_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
        )
        if not include_debug:
            return result, None

        request_debug: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"},
        }
        connection_overrides = self.llm_connection.debug_payload()
        if connection_overrides:
            request_debug["connection_overrides"] = connection_overrides
        response_debug: dict[str, Any] = {
            "elapsed_ms": elapsed_ms,
            "content": raw_content,
            "parsed": payload.model_dump(mode="json"),
            "usage": usage,
            "cost_usd": cost_usd,
            "retry": {
                "attempts": retry_attempts,
                "attempts_total": len(retry_attempts) + 1,
            },
        }
        return result, AnalyzeDebug(request=request_debug, response=response_debug)

    @staticmethod
    def _build_prompt(
        *,
        title: str,
        canonical_url: str,
        user_topics: list[str],
        content: str | None,
        content_max_chars: int = 5000,
    ) -> str:
        serialized_topics = (
            ", ".join(user_topics) if user_topics else "general technology"
        )
        trimmed_content = (content or "").strip()
        max_chars = max(0, int(content_max_chars))
        if max_chars > 0 and len(trimmed_content) > max_chars:
            trimmed_content = trimmed_content[:max_chars] + "\n...[truncated]..."
        return (
            "Read the following research paper and return a single JSON object with keys: "
            "summary, topics, relevance_score, novelty_score.\n"
            "\n"
            "Hard requirements (must follow):\n"
            "- Output MUST be strict JSON only. No markdown outside JSON, no extra keys, no code fences.\n"
            "- summary: a high-signal TL;DR in Markdown (inside the string).\n"
            "  - Answer these questions explicitly:\n"
            "    1) What problem does it solve, and why does it matter?\n"
            "    2) What is the core method/mechanism? Explain in the simplest possible terms.\n"
            "    3) What breakthrough results does it claim? Include numbers when available (metric/dataset/baseline/comparison).\n"
            "  - Use this structure:\n"
            "    - TL;DR: one sentence\n"
            "    - Problem: 1-3 bullets\n"
            "    - Approach: 2-5 bullets\n"
            "    - Results: 2-6 bullets with numbers; if the provided text has no quantitative results, say so and list the strongest concrete claims.\n"
            "- topics: 3 to 6 concise English tags in lower-kebab-case. No spaces.\n"
            "- relevance_score and novelty_score in [0,1].\n"
            "\n"
            f"User topics (for relevance scoring only): {serialized_topics}\n"
            f"Title: {title}\n"
            f"URL: {canonical_url}\n"
            + (
                f"Paper content (excerpt):\n{trimmed_content}\n"
                if trimmed_content
                else ""
            )
        )

    def _build_system_message(self) -> str:
        base_message = "You are a research signal analyst. Return strict JSON only."
        if not self.output_language:
            return base_message
        return (
            f"{base_message} Use {self.output_language} for the summary value. "
            "Keep all JSON keys in English and keep topics as concise English tags."
        )


def _extract_content(response: object) -> str:
    if isinstance(response, dict):
        return str(response["choices"][0]["message"]["content"])
    choices = getattr(response, "choices")
    first_choice = choices[0]
    return str(first_choice.message.content)


def _extract_usage_dict(response: object) -> dict[str, Any] | None:
    usage: Any
    if isinstance(response, dict):
        usage = response.get("usage")
    else:
        usage = getattr(response, "usage", None)
    if isinstance(usage, dict):
        return usage
    if usage is None:
        return None
    prompt_tokens = getattr(usage, "prompt_tokens", None)
    completion_tokens = getattr(usage, "completion_tokens", None)
    total_tokens = getattr(usage, "total_tokens", None)
    out: dict[str, Any] = {}
    if prompt_tokens is not None:
        out["prompt_tokens"] = prompt_tokens
    if completion_tokens is not None:
        out["completion_tokens"] = completion_tokens
    if total_tokens is not None:
        out["total_tokens"] = total_tokens
    return out or None


def _extract_response_cost_usd(response: object) -> float | None:
    hidden: Any | None
    if isinstance(response, dict):
        hidden = response.get("_hidden_params")
    else:
        hidden = getattr(response, "_hidden_params", None)
    if not isinstance(hidden, dict):
        return None
    raw = hidden.get("response_cost")
    if isinstance(raw, (int, float)):
        return float(raw)
    if raw is None:
        return None
    try:
        return float(raw)
    except Exception:
        return None


def _get_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return None


def _extract_token_counts(
    usage: dict[str, Any] | None,
) -> tuple[int | None, int | None, int | None]:
    if not isinstance(usage, dict):
        return None, None, None
    prompt_tokens = _get_int(usage.get("prompt_tokens"))
    completion_tokens = _get_int(usage.get("completion_tokens"))
    total_tokens = _get_int(usage.get("total_tokens"))
    if prompt_tokens is None:
        prompt_tokens = _get_int(usage.get("input_tokens"))
    if completion_tokens is None:
        completion_tokens = _get_int(usage.get("output_tokens"))
    if (
        total_tokens is None
        and prompt_tokens is not None
        and completion_tokens is not None
    ):
        total_tokens = prompt_tokens + completion_tokens
    return prompt_tokens, completion_tokens, total_tokens
