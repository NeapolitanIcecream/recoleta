from __future__ import annotations


def is_retryable_llm_error(exc: BaseException) -> bool:
    """Return whether an exhausted provider error is safe to retry in a later run."""

    try:
        import litellm
    except Exception:
        return False

    candidates = (
        getattr(litellm, "RateLimitError", None),
        getattr(litellm, "ServiceUnavailableError", None),
        getattr(litellm, "Timeout", None),
        getattr(litellm, "APIError", None),
    )
    retryable_types = tuple(
        candidate for candidate in candidates if isinstance(candidate, type)
    )
    return bool(retryable_types and isinstance(exc, retryable_types))
