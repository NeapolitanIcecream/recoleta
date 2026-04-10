from __future__ import annotations

from types import SimpleNamespace

import recoleta.delivery as delivery_module
from recoleta.delivery import ResendBatchSender


def test_resend_batch_sender_requests_permissive_batch_validation(
    monkeypatch,
) -> None:
    captured: dict[str, object] = {}
    response = SimpleNamespace(data=[{"id": "msg-0"}], errors=[])

    class _FakeBatch:
        @staticmethod
        def send(emails: object, options: object) -> object:
            captured["emails"] = emails
            captured["options"] = options
            return response

    fake_resend = SimpleNamespace(api_key=None, Batch=_FakeBatch)
    monkeypatch.setattr(delivery_module, "resend", fake_resend)

    sender = ResendBatchSender(api_key="re_test_secret")
    sender.send_batch(
        emails=[{"to": "alice@example.com"}],
        idempotency_key="trend-email:test",
    )

    assert captured["options"] == {
        "idempotency_key": "trend-email:test",
        "batch_validation": "permissive",
    }


def test_resend_batch_sender_maps_sparse_errors_by_reported_index(
    monkeypatch,
) -> None:
    response = SimpleNamespace(
        data=[{"id": "msg-0"}],
        errors=[
            {
                "index": 1,
                "message": "invalid recipient",
            }
        ],
    )

    class _FakeBatch:
        @staticmethod
        def send(emails: object, options: object) -> object:
            return response

    fake_resend = SimpleNamespace(api_key=None, Batch=_FakeBatch)
    monkeypatch.setattr(delivery_module, "resend", fake_resend)

    sender = ResendBatchSender(api_key="re_test_secret")
    outcomes = sender.send_batch(
        emails=[
            {"to": "alice@example.com"},
            {"to": "bob@example.com"},
        ],
        idempotency_key="trend-email:test",
    )

    assert outcomes == [
        {
            "destination": "alice@example.com",
            "message_id": "msg-0",
            "error": None,
        },
        {
            "destination": "bob@example.com",
            "message_id": None,
            "error": "invalid recipient",
        },
    ]


def test_resend_batch_sender_consumes_success_results_sequentially_after_errors(
    monkeypatch,
) -> None:
    response = SimpleNamespace(
        data=[{"id": "msg-1"}],
        errors=[
            {
                "index": 0,
                "message": "invalid recipient",
            }
        ],
    )

    class _FakeBatch:
        @staticmethod
        def send(emails: object, options: object) -> object:
            return response

    fake_resend = SimpleNamespace(api_key=None, Batch=_FakeBatch)
    monkeypatch.setattr(delivery_module, "resend", fake_resend)

    sender = ResendBatchSender(api_key="re_test_secret")
    outcomes = sender.send_batch(
        emails=[
            {"to": "alice@example.com"},
            {"to": "bob@example.com"},
        ],
        idempotency_key="trend-email:test",
    )

    assert outcomes == [
        {
            "destination": "alice@example.com",
            "message_id": None,
            "error": "invalid recipient",
        },
        {
            "destination": "bob@example.com",
            "message_id": "msg-1",
            "error": None,
        },
    ]
