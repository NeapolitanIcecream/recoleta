from __future__ import annotations

import os

from recoleta.extract import _external_progress_disabled


def test_external_progress_disabled_sets_and_restores_env(monkeypatch) -> None:
    monkeypatch.setenv("HF_HUB_DISABLE_PROGRESS_BARS", "0")
    monkeypatch.delenv("TQDM_DISABLE", raising=False)

    before_hf = os.environ.get("HF_HUB_DISABLE_PROGRESS_BARS")
    before_tqdm = os.environ.get("TQDM_DISABLE")
    assert before_hf == "0"
    assert before_tqdm is None

    with _external_progress_disabled():
        assert os.environ.get("HF_HUB_DISABLE_PROGRESS_BARS") == "1"
        assert os.environ.get("TQDM_DISABLE") == "True"

    assert os.environ.get("HF_HUB_DISABLE_PROGRESS_BARS") == "0"
    assert os.environ.get("TQDM_DISABLE") is None


def test_external_progress_disabled_forces_tqdm_disable(monkeypatch) -> None:
    monkeypatch.delenv("TQDM_DISABLE", raising=False)
    try:
        from tqdm import tqdm
    except Exception:
        return

    with _external_progress_disabled():
        bar_default = tqdm(range(1))
        assert getattr(bar_default, "disable", None) is True

        bar_explicit_false = tqdm(range(1), disable=False)
        assert getattr(bar_explicit_false, "disable", None) is True

