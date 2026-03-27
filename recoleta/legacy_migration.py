from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any

import yaml

from recoleta.config import Settings, TopicStreamRuntime


def load_legacy_config_document(config_path: Path) -> dict[str, Any]:
    resolved = config_path.expanduser().resolve()
    raw_text = resolved.read_text(encoding="utf-8")
    suffix = resolved.suffix.lower()
    if suffix == ".json":
        loaded = json.loads(raw_text)
    elif suffix in {".yaml", ".yml"}:
        loaded = yaml.safe_load(raw_text)
    else:
        raise ValueError(
            f"Unsupported config file type: {resolved.suffix} (expected .yaml/.yml/.json)"
        )
    if not isinstance(loaded, dict):
        raise ValueError("Legacy config file must contain a mapping/object")
    return deepcopy(loaded)


def load_legacy_settings(config_path: Path) -> Settings:
    return Settings(config_path=config_path.expanduser().resolve())  # pyright: ignore[reportCallIssue]


def legacy_explicit_topic_streams(settings: Settings) -> list[TopicStreamRuntime]:
    return [
        stream
        for stream in settings.topic_stream_runtimes()
        if bool(getattr(stream, "explicit", False))
    ]
