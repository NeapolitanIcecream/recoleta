from __future__ import annotations


def metric_token(value: str, *, max_len: int = 48) -> str:
    lowered = value.lower().strip()
    if not lowered:
        return "unknown"
    normalized = "".join(ch if ch.isalnum() else "_" for ch in lowered)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    if not normalized:
        return "unknown"
    return normalized[:max_len]
