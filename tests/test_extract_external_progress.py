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


def test_external_progress_disabled_restores_huggingface_state(monkeypatch) -> None:
    monkeypatch.delenv("HF_HUB_DISABLE_PROGRESS_BARS", raising=False)
    try:
        import huggingface_hub.utils as hf_utils
    except Exception:
        return

    are_disabled = getattr(hf_utils, "are_progress_bars_disabled", None)
    disable = getattr(hf_utils, "disable_progress_bars", None)
    enable = getattr(hf_utils, "enable_progress_bars", None)
    if not callable(are_disabled) or not callable(disable) or not callable(enable):
        return

    previous = bool(are_disabled())
    try:
        enable()
        assert are_disabled() is False

        with _external_progress_disabled():
            assert are_disabled() is True
    finally:
        if previous:
            disable()
        else:
            enable()
