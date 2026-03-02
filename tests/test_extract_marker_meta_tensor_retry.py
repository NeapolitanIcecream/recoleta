from __future__ import annotations

from typing import Any

import pytest

import recoleta.extract as extract


def test_extract_pdf_text_retries_marker_on_cpu_when_meta_tensor_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Spec: meta-tensor failures should auto-retry marker on CPU once."""

    class FakeRendered:
        markdown = "cpu marker result"

    class FailingConverter:
        def __call__(self, _path: str) -> Any:
            raise RuntimeError(
                "Cannot copy out of meta tensor; no data! Please use torch.nn.Module.to_empty()"
            )

    class CpuConverter:
        def __call__(self, _path: str) -> Any:
            return FakeRendered()

    def fake_get_marker_pdf_converter(marker_device: str | None = None) -> Any:
        if str(marker_device or "").strip().lower() == "cpu":
            return CpuConverter()
        return FailingConverter()

    monkeypatch.setattr(
        extract, "_get_marker_pdf_converter", fake_get_marker_pdf_converter
    )

    diag: dict[str, Any] = {}
    out = extract._extract_pdf_text_with_marker(  # noqa: SLF001
        b"%PDF-1.4 fake", marker_device=None, diag=diag
    )

    assert out == "cpu marker result"
    assert diag.get("marker_retry_cpu") is True
