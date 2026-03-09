from __future__ import annotations

import sys
from types import ModuleType

from recoleta.pipeline import service as _service


class _PipelineModule(ModuleType):
    def __getattr__(self, name: str) -> object:
        return getattr(_service, name)

    def __setattr__(self, name: str, value: object) -> None:
        super().__setattr__(name, value)
        if hasattr(_service, name):
            setattr(_service, name, value)

    def __dir__(self) -> list[str]:
        return sorted(
            set(super().__dir__()) | {name for name in dir(_service) if not name.startswith("_")}
        )


_module = sys.modules[__name__]
_module.__class__ = _PipelineModule

__all__ = [name for name in dir(_service) if not name.startswith("_")]  # pyright: ignore[reportUnsupportedDunderAll]

for _name in __all__:
    globals()[_name] = getattr(_service, _name)
