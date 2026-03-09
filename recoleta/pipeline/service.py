from __future__ import annotations

from typing import Any

import recoleta.pipeline as _pipeline

PipelineService: Any = _pipeline.PipelineService  # pyright: ignore[reportAttributeAccessIssue]

__all__ = ["PipelineService"]
