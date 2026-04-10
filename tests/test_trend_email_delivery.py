from __future__ import annotations

from datetime import UTC, date, datetime
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Callable, TypedDict
from unittest.mock import ANY

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.cli.email as cli_email_module
import recoleta.cli.fleet as cli_fleet_module
import recoleta.trend_email as trend_email_module
from recoleta.config import Settings
from recoleta.models import (
    DELIVERY_CHANNEL_EMAIL,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_SENT,
)
from recoleta.publish import write_markdown_note, write_markdown_trend_note
from recoleta.publish.item_note_writer import ItemNoteSpec
from recoleta.site import TrendSiteInputSpec, export_trend_static_site
from recoleta.site_email_links import email_links_artifact_path, load_email_links_artifact
from recoleta.storage import Repository
from recoleta.trend_email import (
    TrendEmailSendRequest,
    build_trend_email_preview,
    send_trend_email,
)
from recoleta.types import AnalysisResult, ItemDraft


class FakeResendBatchSender:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def send_batch(
        self,
        *,
        emails: list[dict[str, object]],
        idempotency_key: str,
    ) -> list[dict[str, str | None]]:
        self.calls.append(
            {
                "emails": emails,
                "idempotency_key": idempotency_key,
            }
        )
        return [
            {
                "destination": str(email["to"]),
                "message_id": f"msg-{idx}",
                "error": None,
            }
            for idx, email in enumerate(emails)
        ]


class PartialFailureResendBatchSender:
    def send_batch(
        self,
        *,
        emails: list[dict[str, object]],
        idempotency_key: str,
    ) -> list[dict[str, str | None]]:
        assert idempotency_key
        return [
            {
                "destination": str(emails[0]["to"]),
                "message_id": "msg-0",
                "error": None,
            },
            {
                "destination": str(emails[1]["to"]),
                "message_id": None,
                "error": "provider failed",
            },
        ]


class EmailFixture(TypedDict):
    output_dir: Path
    repository: Repository
    trend_doc_ids: dict[str, int]
    trend_note_paths: dict[str, Path]
    item_note_path: Path


def _send_request(
    *,
    site_output_dir: Path,
    sender: object | None = None,
    url_checker: Callable[[str], bool] | None = None,
    anchor_date: date | None = None,
    force_batch: bool = False,
    granularities: list[str] | None = None,
) -> TrendEmailSendRequest:
    return TrendEmailSendRequest(
        site_output_dir=site_output_dir,
        sender=sender,
        url_checker=url_checker,
        anchor_date=anchor_date,
        force_batch=force_batch,
        granularities=granularities,
    )


def _set_email_env(
    *,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    output_dir: Path,
    recipients: list[str] | None = None,
    granularities: list[str] | None = None,
) -> Settings:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv("MARKDOWN_OUTPUT_DIR", str(output_dir))
    monkeypatch.setenv("RECOLETA_RESEND_API_KEY", "re_test_secret")
    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://public.example/recoleta",
                "from_email": "updates@example.com",
                "to": recipients or ["alice@example.com", "bob@example.com"],
                "granularities": granularities or ["day"],
            }
        ),
    )
    return Settings()  # pyright: ignore[reportCallIssue]


def _seed_item_doc(*, repository: Repository, published_at: datetime) -> int:
    draft = ItemDraft.from_values(
        source="rss",
        source_item_id="trend-email-item",
        canonical_url="https://example.com/trend-email-item",
        title="Grounded runtime checks",
        authors=["Peng Wang", "Hao Wang"],
        published_at=published_at,
    )
    item, _ = repository.upsert_item(draft)
    assert item.id is not None
    repository.save_analysis(
        item_id=int(item.id),
        result=AnalysisResult(
            model="test/fake-model",
            provider="test",
            summary=(
                "## Summary\n\n"
                "Grounded runtime checks make long-horizon work auditable.\n"
            ),
            topics=["agents"],
            relevance_score=0.9,
            novelty_score=0.4,
            cost_usd=0.0,
            latency_ms=1,
        ),
    )
    persisted_item = repository.get_item(item_id=int(item.id))
    assert persisted_item is not None
    doc = repository.upsert_document_for_item(item=persisted_item)
    assert doc.id is not None
    repository.upsert_document_chunk(
        doc_id=int(doc.id),
        chunk_index=0,
        kind="summary",
        text_value="Grounded runtime checks move verification into the shipping path.",
        source_content_type="analysis_summary",
    )
    return int(doc.id)


def _write_email_fixture(
    *,
    tmp_path: Path,
    instance: str | None = None,
    granularities: tuple[str, ...] = ("day",),
) -> EmailFixture:
    output_dir = tmp_path / "notes"
    repository = Repository(db_path=tmp_path / "recoleta.db")
    repository.init_schema()

    item_doc_id = _seed_item_doc(
        repository=repository,
        published_at=datetime(2026, 2, 25, 12, tzinfo=UTC),
    )
    item_note_path = write_markdown_note(
        output_dir=output_dir,
        spec=ItemNoteSpec(
            item_id=11,
            title="Grounded runtime checks",
            source="rss",
            canonical_url="https://example.com/trend-email-item",
            published_at=datetime(2026, 2, 25, 12, tzinfo=UTC),
            authors=["Peng Wang", "Hao Wang"],
            topics=["agents"],
            relevance_score=0.9,
            run_id="run-item-email",
            summary="Runtime checks keep release decisions observable.",
        ),
    )
    relative_item_href = os.path.relpath(item_note_path, start=output_dir / "Trends")

    trend_doc_ids: dict[str, int] = {}
    trend_note_paths: dict[str, Path] = {}
    period_specs = {
        "day": (
            datetime(2026, 2, 25, tzinfo=UTC),
            datetime(2026, 2, 26, tzinfo=UTC),
            "Agent systems day",
        ),
        "week": (
            datetime(2026, 2, 23, tzinfo=UTC),
            datetime(2026, 3, 2, tzinfo=UTC),
            "Agent systems week",
        ),
        "month": (
            datetime(2026, 2, 1, tzinfo=UTC),
            datetime(2026, 3, 1, tzinfo=UTC),
            "Agent systems month",
        ),
    }
    for granularity in granularities:
        period_start, period_end, title = period_specs[granularity]
        trend_doc = repository.upsert_document_for_trend(
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            title=title,
        )
        assert trend_doc.id is not None
        trend_note_path = write_markdown_trend_note(
            output_dir=output_dir,
            trend_doc_id=int(trend_doc.id),
            title=title,
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            run_id="run-trend-email",
            overview_md=(
                "Agent workflows are getting more production-ready with "
                f"[grounded notes]({relative_item_href})."
            ),
            topics=["agents", "tooling"],
            clusters=[
                {
                    "title": "Release discipline",
                    "content_md": (
                        "Verification moved into the shipping path with "
                        f"[linked evidence]({relative_item_href})."
                    ),
                    "evidence_refs": [
                        {
                            "doc_id": item_doc_id,
                            "chunk_index": 0,
                            "title": "Grounded runtime checks",
                            "href": relative_item_href,
                            "url": "https://example.com/trend-email-item",
                            "reason": "The note grounds release discipline in the corpus.",
                        }
                    ],
                }
            ],
        )
        if instance is not None:
            raw = trend_note_path.read_text(encoding="utf-8")
            trend_note_path.write_text(
                raw.replace(
                    "run_id: run-trend-email",
                    f"run_id: run-trend-email\ninstance: {instance}",
                ),
                encoding="utf-8",
            )
        trend_doc_ids[granularity] = int(trend_doc.id)
        trend_note_paths[granularity] = trend_note_path
    return {
        "output_dir": output_dir,
        "repository": repository,
        "trend_doc_ids": trend_doc_ids,
        "trend_note_paths": trend_note_paths,
        "item_note_path": item_note_path,
    }


def _preview_entry(result: object, granularity: str | None = None) -> object:
    results = list(getattr(result, "results"))
    if granularity is None:
        assert len(results) == 1
        return results[0]
    for entry in results:
        if getattr(entry, "granularity") == granularity:
            return entry
    raise AssertionError(f"missing preview entry for granularity={granularity}")


def _send_entry(result: object, granularity: str | None = None) -> object:
    results = list(getattr(result, "results"))
    if granularity is None:
        assert len(results) == 1
        return results[0]
    for entry in results:
        if getattr(entry, "granularity") == granularity:
            return entry
    raise AssertionError(f"missing send entry for granularity={granularity}")


def _fake_preview_batch_result(*, tmp_path: Path, instance: str = "default") -> object:
    preview_dir = tmp_path / "preview" / "day--2026-02-25--trend--123"
    return SimpleNamespace(
        status="succeeded",
        preview_root_dir=tmp_path / "preview",
        batch_manifest_path=tmp_path / "preview" / "batch-manifest.json",
        instance=instance,
        results=[
            SimpleNamespace(
                granularity="day",
                preview_dir=preview_dir,
                manifest_path=preview_dir / "manifest.json",
                html_path=preview_dir / "body.html",
                text_path=preview_dir / "body.txt",
                primary_page_url="https://public.example/recoleta/trends/example",
                content_hash="hash-123",
                subject="[Recoleta] Day trends · 2026-02-25",
                trend_doc_id=123,
                period_token="2026-02-25",
            )
        ],
    )


def _fake_send_batch_result(
    *,
    tmp_path: Path,
    status: str,
    entry_status: str,
    instance: str = "default",
    error: str | None = None,
    with_artifacts: bool = True,
) -> object:
    send_dir = (
        tmp_path / "send" / "day--2026-02-25--trend--123"
        if with_artifacts
        else None
    )
    return SimpleNamespace(
        status=status,
        send_root_dir=tmp_path / "send",
        batch_manifest_path=tmp_path / "send" / "batch-manifest.json",
        instance=instance,
        results=[
            SimpleNamespace(
                status=entry_status,
                granularity="day",
                send_dir=send_dir,
                manifest_path=send_dir / "manifest.json" if send_dir else None,
                html_path=send_dir / "body.html" if send_dir else None,
                text_path=send_dir / "body.txt" if send_dir else None,
                primary_page_url=(
                    "https://public.example/recoleta/trends/example"
                    if with_artifacts
                    else None
                ),
                content_hash="hash-123" if with_artifacts else None,
                subject="[Recoleta] Day trends · 2026-02-25" if with_artifacts else None,
                trend_doc_id=123 if with_artifacts else None,
                period_token="2026-02-25" if with_artifacts else None,
                error=error,
            )
        ],
    )


def test_export_trend_static_site_writes_email_link_map_artifact(tmp_path: Path) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = fixture["output_dir"]
    trend_note_path = fixture["trend_note_paths"]["day"]
    item_note_path = fixture["item_note_path"]
    assert isinstance(output_dir, Path)
    assert isinstance(trend_note_path, Path)
    assert isinstance(item_note_path, Path)

    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    artifact_path = email_links_artifact_path(site_output_dir=site_dir)
    assert artifact_path.exists()
    payload = load_email_links_artifact(artifact_path=artifact_path)
    assert payload["pages_by_source_markdown"][str(trend_note_path.resolve())].startswith(
        "trends/"
    )
    assert payload["pages_by_source_markdown"][str(item_note_path.resolve())].startswith(
        "items/"
    )
    manifest = json.loads((site_dir / "manifest.json").read_text(encoding="utf-8"))
    assert "email_links" not in (manifest.get("files") or {})


def test_export_trend_static_site_aggregate_instance_build_writes_email_link_map(
    tmp_path: Path,
) -> None:
    alpha_root = tmp_path / "alpha"
    beta_root = tmp_path / "beta"
    alpha_fixture = _write_email_fixture(tmp_path=alpha_root, instance="Alpha")
    beta_fixture = _write_email_fixture(tmp_path=beta_root, instance="Beta")

    site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=[
            TrendSiteInputSpec(path=alpha_root / "notes", instance="Alpha"),
            TrendSiteInputSpec(path=beta_root / "notes", instance="Beta"),
        ],
        output_dir=site_dir,
    )

    artifact_path = email_links_artifact_path(site_output_dir=site_dir)
    payload = load_email_links_artifact(artifact_path=artifact_path)
    alpha_trend = Path(alpha_fixture["trend_note_paths"]["day"])
    beta_trend = Path(beta_fixture["trend_note_paths"]["day"])
    assert "alpha--" in payload["pages_by_source_markdown"][str(alpha_trend.resolve())]
    assert "beta--" in payload["pages_by_source_markdown"][str(beta_trend.resolve())]


def test_build_trend_email_preview_writes_preview_artifacts_and_site_first_links(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    entry = _preview_entry(result)

    assert result.preview_root_dir.exists()
    assert result.batch_manifest_path.exists()
    assert entry.preview_dir.exists()
    assert entry.manifest_path.exists()
    html_body = entry.html_path.read_text(encoding="utf-8")
    text_body = entry.text_path.read_text(encoding="utf-8")
    assert "https://public.example/recoleta/trends/" in html_body
    assert "https://public.example/recoleta/items/" in html_body
    assert "Open on site" in html_body
    assert "Agent systems" in text_body
    manifest = json.loads(entry.manifest_path.read_text(encoding="utf-8"))
    assert manifest["content_hash"] == entry.content_hash
    assert manifest["primary_page_url"] == entry.primary_page_url


def test_build_trend_email_preview_writes_multi_granularity_batch_in_config_order(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day", "week"))
    output_dir = Path(fixture["output_dir"])
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = build_trend_email_preview(settings=settings, site_output_dir=site_dir)

    assert result.status == "succeeded"
    assert [entry.granularity for entry in result.results] == ["day", "week"]
    assert result.preview_root_dir.exists()
    assert result.batch_manifest_path.exists()
    batch_manifest = json.loads(result.batch_manifest_path.read_text(encoding="utf-8"))
    assert batch_manifest["status"] == "succeeded"
    assert len(batch_manifest["results"]) == 2


def test_build_trend_email_preview_is_all_or_nothing_on_multi_granularity_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day",))
    output_dir = Path(fixture["output_dir"])
    preview_root = tmp_path / "preview-root"
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    with pytest.raises(RuntimeError, match="granularity=week"):
        build_trend_email_preview(
            settings=settings,
            site_output_dir=site_dir,
            output_dir=preview_root,
        )

    assert not preview_root.exists()


def test_build_trend_email_preview_filters_selected_granularities_in_config_order(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(
        tmp_path=tmp_path,
        granularities=("day", "week", "month"),
    )
    output_dir = Path(fixture["output_dir"])
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["week", "day", "month"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = build_trend_email_preview(
        settings=settings,
        site_output_dir=site_dir,
        granularities=["month", "week"],
    )

    assert [entry.granularity for entry in result.results] == ["week", "month"]


def test_send_trend_email_marks_preflight_failed_when_primary_page_is_not_publicly_reachable(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    assert isinstance(repository, Repository)
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: False,
        ),
    )

    assert result.status == "preflight_failed"
    entry = _send_entry(result)
    assert entry.status == "preflight_failed"
    assert "public trend page is not reachable" in str(entry.error)


def test_send_trend_email_preflight_failure_keeps_ready_entries_and_skips_provider_calls(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("week", "month"))
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["week", "month"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    preview = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    blocked_url = _preview_entry(preview, "week").primary_page_url
    sender = FakeResendBatchSender()

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda url: url != blocked_url,
        ),
    )

    assert result.status == "preflight_failed"
    assert [entry.granularity for entry in result.results] == ["week", "month"]
    assert _send_entry(result, "week").status == "preflight_failed"
    assert _send_entry(result, "month").status == "ready_to_send"
    assert sender.calls == []


def test_send_trend_email_converts_bundle_build_failures_into_preflight_failed_results(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day",))
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )

    assert result.status == "preflight_failed"
    assert [entry.granularity for entry in result.results] == ["day", "week"]
    ready = _send_entry(result, "day")
    assert ready.status == "ready_to_send"
    assert ready.send_dir is not None and ready.send_dir.exists()
    blocked = _send_entry(result, "week")
    assert blocked.status == "preflight_failed"
    assert blocked.error == "no matching trend email candidate found for granularity=week"
    assert blocked.send_dir is None
    assert blocked.manifest_path is None
    assert blocked.html_path is None
    assert blocked.text_path is None
    assert sender.calls == []
    batch_manifest = json.loads(result.batch_manifest_path.read_text(encoding="utf-8"))
    assert batch_manifest["status"] == "preflight_failed"
    assert batch_manifest["results"][1]["granularity"] == "week"
    assert batch_manifest["results"][1]["send_dir"] is None


def test_send_trend_email_skips_duplicate_batch_for_unchanged_content(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_ids"]["day"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    first = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )
    second = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )

    assert first.status == "succeeded"
    assert _send_entry(first).status == "sent"
    assert second.status == "succeeded"
    assert _send_entry(second).status == "skipped"
    assert len(sender.calls) == 1
    rows = repository.list_trend_deliveries(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
    )
    assert len(rows) == 2
    assert {row.status for row in rows} == {DELIVERY_STATUS_SENT}


def test_send_trend_email_skips_without_requiring_public_url_reachability(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_ids"]["day"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    preview = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    preview_entry = _preview_entry(preview)

    assert settings.email is not None
    for destination in settings.email.to:
        repository.upsert_trend_delivery(
            doc_id=trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=preview_entry.content_hash,
            message_id=f"msg-{destination}",
            status=DELIVERY_STATUS_SENT,
            error=None,
        )

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            url_checker=lambda _url: False,
        ),
    )

    assert result.status == "succeeded"
    assert _send_entry(result).status == "skipped"


def test_send_trend_email_allows_retry_after_failed_batch_and_force_for_mixed_state(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_ids"]["day"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    preview = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    preview_entry = _preview_entry(preview)
    retry_sender = FakeResendBatchSender()

    assert settings.email is not None
    for destination in settings.email.to:
        repository.upsert_trend_delivery(
            doc_id=trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=preview_entry.content_hash,
            message_id=None,
            status=DELIVERY_STATUS_FAILED,
            error="provider failed",
        )

    retry_result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=retry_sender,
            url_checker=lambda _url: True,
        ),
    )
    assert retry_result.status == "succeeded"
    assert _send_entry(retry_result).status == "sent"
    assert retry_sender.calls == [
        {
            "emails": ANY,
            "idempotency_key": ANY,
        }
    ]
    assert retry_sender.calls[0]["idempotency_key"] != (
        f"trend-email:{trend_doc_id}:{preview_entry.content_hash}"
    )

    repository.upsert_trend_delivery(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
        destination=settings.email.to[0],
        content_hash=preview_entry.content_hash,
        message_id="msg-existing",
        status=DELIVERY_STATUS_SENT,
        error=None,
    )
    repository.upsert_trend_delivery(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
        destination=settings.email.to[1],
        content_hash="different-hash",
        message_id=None,
        status=DELIVERY_STATUS_FAILED,
        error="old failure",
    )

    blocked = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: True,
        ),
    )
    assert blocked.status == "preflight_failed"
    assert _send_entry(blocked).status == "preflight_failed"
    assert _send_entry(blocked).error == "mixed_batch_state"

    forced = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: True,
            force_batch=True,
        ),
    )
    assert forced.status == "succeeded"
    assert _send_entry(forced).status == "sent"


def test_send_trend_email_uses_unique_force_and_retry_idempotency_keys(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_ids"]["day"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    preview = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    preview_entry = _preview_entry(preview)
    sender = FakeResendBatchSender()
    frozen_now = datetime(2026, 4, 10, 4, 55, 0, tzinfo=UTC)

    class _FrozenDateTime:
        @classmethod
        def now(cls, tz: object | None = None) -> datetime:
            assert tz is not None
            return frozen_now

    uuid_values = iter(
        [
            "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
            "cccccccccccccccccccccccccccccccc",
            "dddddddddddddddddddddddddddddddd",
            "eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
            "ffffffffffffffffffffffffffffffff",
            "11111111111111111111111111111111",
            "22222222222222222222222222222222",
        ]
    )

    monkeypatch.setattr(trend_email_module, "datetime", _FrozenDateTime)
    monkeypatch.setattr(
        trend_email_module,
        "uuid4",
        lambda: SimpleNamespace(hex=next(uuid_values)),
    )

    first_force = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
            force_batch=True,
        ),
    )
    second_force = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
            force_batch=True,
        ),
    )

    assert first_force.status == "succeeded"
    assert _send_entry(first_force).status == "sent"
    assert second_force.status == "succeeded"
    assert _send_entry(second_force).status == "sent"
    assert sender.calls[0]["idempotency_key"] != sender.calls[1]["idempotency_key"]
    assert ":force:" in str(sender.calls[0]["idempotency_key"])
    assert ":force:" in str(sender.calls[1]["idempotency_key"])

    assert settings.email is not None
    for destination in settings.email.to:
        repository.upsert_trend_delivery(
            doc_id=trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=preview_entry.content_hash,
            message_id=None,
            status=DELIVERY_STATUS_FAILED,
            error="provider failed",
        )

    first_retry = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )
    for destination in settings.email.to:
        repository.upsert_trend_delivery(
            doc_id=trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=preview_entry.content_hash,
            message_id=None,
            status=DELIVERY_STATUS_FAILED,
            error="provider failed",
        )
    second_retry = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )

    assert first_retry.status == "succeeded"
    assert _send_entry(first_retry).status == "sent"
    assert second_retry.status == "succeeded"
    assert _send_entry(second_retry).status == "sent"
    assert sender.calls[2]["idempotency_key"] != sender.calls[3]["idempotency_key"]
    assert ":retry:" in str(sender.calls[2]["idempotency_key"])
    assert ":retry:" in str(sender.calls[3]["idempotency_key"])


def test_send_trend_email_changes_non_force_idempotency_key_when_recipient_batch_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        recipients=["alice@example.com", "bob@example.com"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    first = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )
    assert first.status == "succeeded"
    assert _send_entry(first).status == "sent"

    assert settings.email is not None
    settings.email.to = ["carol@example.com", "dave@example.com"]

    second = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )

    assert second.status == "succeeded"
    assert _send_entry(second).status == "sent"
    assert len(sender.calls) == 2
    assert sender.calls[0]["idempotency_key"] != sender.calls[1]["idempotency_key"]
    assert ":force:" not in str(sender.calls[1]["idempotency_key"])
    assert ":retry:" not in str(sender.calls[1]["idempotency_key"])


def test_send_trend_email_returns_failed_when_any_recipient_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_ids"]["day"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=PartialFailureResendBatchSender(),
            url_checker=lambda _url: True,
        ),
    )

    assert result.status == "send_failed"
    assert _send_entry(result).status == "send_failed"
    rows = repository.list_trend_deliveries(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
    )
    assert len(rows) == 2
    assert {row.status for row in rows} == {DELIVERY_STATUS_SENT, DELIVERY_STATUS_FAILED}


def test_send_trend_email_marks_later_bundles_not_attempted_after_send_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day", "week"))
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=PartialFailureResendBatchSender(),
            url_checker=lambda _url: True,
        ),
    )

    assert result.status == "send_failed"
    assert _send_entry(result, "day").status == "send_failed"
    assert _send_entry(result, "week").status == "not_attempted"


def test_send_trend_email_rejects_recipient_lists_over_resend_batch_limit(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
    )
    assert settings.email is not None
    settings.email.to = [f"user-{idx}@example.com" for idx in range(101)]
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: True,
        ),
    )

    assert result.status == "preflight_failed"
    assert _send_entry(result).status == "preflight_failed"
    assert "at most 100 recipients" in str(_send_entry(result).error)


def test_send_trend_email_force_batch_applies_only_to_selected_granularity(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day", "week"))
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    first = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )
    forced_week = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
            force_batch=True,
            granularities=["week"],
        ),
    )

    assert first.status == "succeeded"
    assert forced_week.status == "succeeded"
    assert [entry.granularity for entry in forced_week.results] == ["week"]
    assert _send_entry(forced_week, "week").status == "sent"
    assert len(sender.calls) == 3


def test_send_trend_email_returns_succeeded_when_all_selected_bundles_are_skipped(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path, granularities=("day", "week"))
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    settings = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path,
        output_dir=output_dir,
        granularities=["day", "week"],
    )
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    initial = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: True,
        ),
    )
    result = send_trend_email(
        settings=settings,
        repository=repository,
        request=_send_request(
            site_output_dir=site_dir,
            sender=sender,
            url_checker=lambda _url: False,
        ),
    )

    assert initial.status == "succeeded"
    assert result.status == "succeeded"
    assert [entry.status for entry in result.results] == ["skipped", "skipped"]
    assert len(sender.calls) == 2


def test_preview_content_hash_is_stable_across_workspace_paths(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture_one = _write_email_fixture(tmp_path=tmp_path / "one")
    fixture_two = _write_email_fixture(tmp_path=tmp_path / "two")

    output_dir_one = Path(fixture_one["output_dir"])
    output_dir_two = Path(fixture_two["output_dir"])

    settings_one = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path / "one",
        output_dir=output_dir_one,
    )
    site_dir_one = tmp_path / "site-one"
    export_trend_static_site(input_dir=output_dir_one, output_dir=site_dir_one)
    preview_one = build_trend_email_preview(
        settings=settings_one,
        site_output_dir=site_dir_one,
    )

    settings_two = _set_email_env(
        monkeypatch=monkeypatch,
        tmp_path=tmp_path / "two",
        output_dir=output_dir_two,
    )
    site_dir_two = tmp_path / "site-two"
    export_trend_static_site(input_dir=output_dir_two, output_dir=site_dir_two)
    preview_two = build_trend_email_preview(
        settings=settings_two,
        site_output_dir=site_dir_two,
    )

    assert _preview_entry(preview_one).content_hash == _preview_entry(preview_two).content_hash


def test_preview_content_hash_changes_when_rewritten_internal_link_changes(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    item_note_path = Path(fixture["item_note_path"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    preview_one = build_trend_email_preview(
        settings=settings,
        site_output_dir=site_dir,
    )

    artifact_path = email_links_artifact_path(site_output_dir=site_dir)
    payload = json.loads(artifact_path.read_text(encoding="utf-8"))
    payload["pages_by_source_markdown"][str(item_note_path.resolve())] = (
        "items/alternate-grounded-runtime-checks/index.html"
    )
    artifact_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    preview_two = build_trend_email_preview(
        settings=settings,
        site_output_dir=site_dir,
    )

    assert _preview_entry(preview_one).content_hash != _preview_entry(preview_two).content_hash


def test_send_root_dir_is_unique_even_with_same_timestamp(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    frozen_now = datetime(2026, 4, 10, 4, 25, 6, tzinfo=UTC)

    class _FrozenDateTime:
        @classmethod
        def now(cls, tz: object | None = None) -> datetime:
            assert tz is not None
            return frozen_now

    monkeypatch.setattr(trend_email_module, "datetime", _FrozenDateTime)

    first = trend_email_module._send_root_dir(settings=settings)
    second = trend_email_module._send_root_dir(settings=settings)

    assert first != second


def test_run_email_send_command_exits_non_zero_when_batch_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime = SimpleNamespace(
        settings=object(),
        repository=object(),
        console=SimpleNamespace(print=lambda *args, **kwargs: None),
    )
    failed_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="send_failed",
        entry_status="send_failed",
        error="provider failed",
    )

    monkeypatch.setattr(cli_email_module, "load_runtime", lambda request: runtime)
    monkeypatch.setattr(
        cli_email_module,
        "site_output_dir_from_settings",
        lambda _settings: tmp_path / "site",
    )
    monkeypatch.setattr(
        cli_email_module,
        "send_trend_email",
        lambda **kwargs: failed_result,
    )

    with pytest.raises(recoleta.cli.typer.Exit) as exc:
        cli_email_module.run_email_send_command()

    assert exc.value.exit_code == 1


def test_run_email_send_command_requests_runtime_schema_init(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    captured: dict[str, object] = {}
    runtime = SimpleNamespace(
        settings=object(),
        repository=object(),
        console=SimpleNamespace(print=lambda *args, **kwargs: None),
    )
    sent_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="succeeded",
        entry_status="sent",
    )

    def _fake_load_runtime(*, request: object) -> object:
        captured["init_schema"] = getattr(request, "init_schema")
        return runtime

    monkeypatch.setattr(cli_email_module, "load_runtime", _fake_load_runtime)
    monkeypatch.setattr(
        cli_email_module,
        "site_output_dir_from_settings",
        lambda _settings: tmp_path / "site",
    )
    monkeypatch.setattr(
        cli_email_module,
        "send_trend_email",
        lambda **kwargs: sent_result,
    )

    cli_email_module.run_email_send_command()

    assert captured["init_schema"] is True


def test_run_email_send_command_json_emits_batch_payload_and_non_zero_exit_on_preflight_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime = SimpleNamespace(
        settings=object(),
        repository=object(),
        console=SimpleNamespace(print=lambda *args, **kwargs: None),
    )
    failed_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="preflight_failed",
        entry_status="preflight_failed",
        error="mixed_batch_state",
        with_artifacts=False,
    )
    captured_payload: dict[str, object] = {}

    monkeypatch.setattr(cli_email_module, "load_runtime", lambda request: runtime)
    monkeypatch.setattr(
        cli_email_module,
        "site_output_dir_from_settings",
        lambda _settings: tmp_path / "site",
    )
    monkeypatch.setattr(
        cli_email_module,
        "send_trend_email",
        lambda **kwargs: failed_result,
    )
    monkeypatch.setattr(
        cli_email_module.cli,
        "_emit_json",
        lambda payload: captured_payload.update(payload),
    )

    with pytest.raises(recoleta.cli.typer.Exit) as exc:
        cli_email_module.run_email_send_command(json_output=True)

    assert exc.value.exit_code == 1
    assert captured_payload["status"] == "preflight_failed"
    assert "send_root_dir" in captured_payload
    assert "batch_manifest_path" in captured_payload
    assert captured_payload["results"][0]["status"] == "preflight_failed"
    assert captured_payload["results"][0]["send_dir"] is None
    assert captured_payload["results"][0]["manifest_path"] is None
    assert captured_payload["results"][0]["html_path"] is None
    assert captured_payload["results"][0]["text_path"] is None


def test_run_email_preview_command_passes_selected_granularities(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime = SimpleNamespace(
        settings=object(),
        repository=object(),
        console=SimpleNamespace(print=lambda *args, **kwargs: None),
    )
    captured: dict[str, object] = {}

    monkeypatch.setattr(cli_email_module, "load_runtime", lambda request: runtime)
    monkeypatch.setattr(
        cli_email_module,
        "site_output_dir_from_settings",
        lambda _settings: tmp_path / "site",
    )

    def _fake_build_trend_email_preview(**kwargs: object) -> object:
        captured["granularities"] = kwargs["granularities"]
        return _fake_preview_batch_result(tmp_path=tmp_path)

    monkeypatch.setattr(
        cli_email_module,
        "build_trend_email_preview",
        _fake_build_trend_email_preview,
    )

    cli_email_module.run_email_preview_command(granularities=["week", "day"])

    assert captured["granularities"] == ["week", "day"]


def test_settings_email_recipients_are_deduplicated(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setenv("RECOLETA_DB_PATH", str(tmp_path / "recoleta.db"))
    monkeypatch.setenv("LLM_MODEL", "openai/gpt-4o-mini")
    monkeypatch.setenv(
        "EMAIL",
        json.dumps(
            {
                "public_site_url": "https://example.com/recoleta",
                "from_email": "updates@example.com",
                "to": [
                    " alice@example.com ",
                    "bob@example.com",
                    "alice@example.com",
                    "bob@example.com ",
                ],
                "granularities": ["week"],
            }
        ),
    )

    settings = Settings()  # pyright: ignore[reportCallIssue]

    assert settings.email is not None
    assert settings.email.to == ["alice@example.com", "bob@example.com"]


def test_run_fleet_email_send_command_exits_non_zero_when_batch_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    failed_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="send_failed",
        entry_status="send_failed",
        instance="Beta",
        error="provider failed",
    )
    resolved_instance = SimpleNamespace(name="Beta", config_path=tmp_path / "beta.yaml")
    manifest = SimpleNamespace(manifest_path=tmp_path / "fleet.yaml")
    settings = SimpleNamespace(recoleta_db_path=tmp_path / "beta.db")

    monkeypatch.setattr(cli_fleet_module, "load_fleet_manifest", lambda _path: manifest)
    monkeypatch.setattr(
        cli_fleet_module,
        "_resolve_fleet_instance",
        lambda manifest, value: resolved_instance,
    )
    monkeypatch.setattr(cli_fleet_module, "load_child_settings", lambda _path: settings)
    monkeypatch.setattr(
        cli_fleet_module,
        "Repository",
        lambda db_path: SimpleNamespace(db_path=db_path),
    )
    monkeypatch.setattr(
        cli_fleet_module,
        "_fleet_site_output_dir",
        lambda manifest_path, _output_dir: tmp_path / "site",
    )
    monkeypatch.setattr(
        cli_fleet_module,
        "send_trend_email",
        lambda **kwargs: failed_result,
    )

    with pytest.raises(recoleta.cli.typer.Exit) as exc:
        cli_fleet_module.run_fleet_email_send_command(
            manifest_path=tmp_path / "fleet.yaml",
            instance="beta",
        )

    assert exc.value.exit_code == 1


def test_run_fleet_email_send_command_initializes_repository_schema(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sent_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="succeeded",
        entry_status="sent",
        instance="Beta",
    )
    resolved_instance = SimpleNamespace(name="Beta", config_path=tmp_path / "beta.yaml")
    manifest = SimpleNamespace(manifest_path=tmp_path / "fleet.yaml")
    settings = SimpleNamespace(recoleta_db_path=tmp_path / "beta.db")
    repository = SimpleNamespace(
        initialized=False,
        init_schema=lambda: None,
    )

    def _fake_init_schema() -> None:
        repository.initialized = True

    repository.init_schema = _fake_init_schema

    monkeypatch.setattr(cli_fleet_module, "load_fleet_manifest", lambda _path: manifest)
    monkeypatch.setattr(
        cli_fleet_module,
        "_resolve_fleet_instance",
        lambda manifest, value: resolved_instance,
    )
    monkeypatch.setattr(cli_fleet_module, "load_child_settings", lambda _path: settings)
    monkeypatch.setattr(
        cli_fleet_module,
        "Repository",
        lambda db_path: repository,
    )
    monkeypatch.setattr(
        cli_fleet_module,
        "_fleet_site_output_dir",
        lambda manifest_path, _output_dir: tmp_path / "site",
    )

    def _fake_send_trend_email(**kwargs: object) -> object:
        assert getattr(kwargs["repository"], "initialized") is True
        return sent_result

    monkeypatch.setattr(
        cli_fleet_module,
        "send_trend_email",
        _fake_send_trend_email,
    )

    cli_fleet_module.run_fleet_email_send_command(
        manifest_path=tmp_path / "fleet.yaml",
        instance="beta",
    )

    assert repository.initialized is True


def test_run_fleet_email_send_command_uses_explicit_site_output_dir(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    sent_result = _fake_send_batch_result(
        tmp_path=tmp_path,
        status="succeeded",
        entry_status="sent",
        instance="Beta",
    )
    resolved_instance = SimpleNamespace(name="Beta", config_path=tmp_path / "beta.yaml")
    manifest = SimpleNamespace(manifest_path=tmp_path / "fleet.yaml")
    settings = SimpleNamespace(recoleta_db_path=tmp_path / "beta.db")
    repository = SimpleNamespace(init_schema=lambda: None)
    captured: dict[str, object] = {}

    monkeypatch.setattr(cli_fleet_module, "load_fleet_manifest", lambda _path: manifest)
    monkeypatch.setattr(
        cli_fleet_module,
        "_resolve_fleet_instance",
        lambda manifest, value: resolved_instance,
    )
    monkeypatch.setattr(cli_fleet_module, "load_child_settings", lambda _path: settings)
    monkeypatch.setattr(cli_fleet_module, "Repository", lambda db_path: repository)

    def _fake_fleet_site_output_dir(manifest_path: Path, output_dir: Path | None) -> Path:
        captured["site_output_dir_arg"] = output_dir
        return Path(output_dir or tmp_path / "site")

    monkeypatch.setattr(
        cli_fleet_module,
        "_fleet_site_output_dir",
        _fake_fleet_site_output_dir,
    )

    def _fake_send_trend_email(**kwargs: object) -> object:
        captured["request_site_output_dir"] = getattr(
            kwargs["request"], "site_output_dir"
        )
        return sent_result

    monkeypatch.setattr(
        cli_fleet_module,
        "send_trend_email",
        _fake_send_trend_email,
    )

    explicit_site_dir = tmp_path / "custom-site"
    cli_fleet_module.run_fleet_email_send_command(
        manifest_path=tmp_path / "fleet.yaml",
        instance="beta",
        site_output_dir=explicit_site_dir,
    )

    assert captured["site_output_dir_arg"] == explicit_site_dir
    assert captured["request_site_output_dir"] == explicit_site_dir


def test_fleet_run_email_preview_uses_selected_child_instance(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = CliRunner()
    alpha_root = tmp_path / "alpha"
    beta_root = tmp_path / "beta"
    alpha_fixture = _write_email_fixture(tmp_path=alpha_root, instance="Alpha")
    beta_fixture = _write_email_fixture(tmp_path=beta_root, instance="Beta")
    alpha_output = Path(alpha_fixture["output_dir"])
    beta_output = Path(beta_fixture["output_dir"])
    aggregate_site_dir = tmp_path / "site"
    export_trend_static_site(
        input_dir=[
            TrendSiteInputSpec(path=alpha_output, instance="Alpha"),
            TrendSiteInputSpec(path=beta_output, instance="Beta"),
        ],
        output_dir=aggregate_site_dir,
    )

    alpha_config = tmp_path / "alpha.yaml"
    beta_config = tmp_path / "beta.yaml"
    for config_path, db_name, output_dir in (
        (alpha_config, "alpha.db", alpha_output),
        (beta_config, "beta.db", beta_output),
    ):
        config_path.write_text(
            "\n".join(
                [
                    f'RECOLETA_DB_PATH: "{config_path.parent / db_name}"',
                    'LLM_MODEL: "openai/gpt-4o-mini"',
                    f'MARKDOWN_OUTPUT_DIR: "{output_dir}"',
                    "EMAIL:",
                    '  public_site_url: "https://public.example/recoleta"',
                    '  from_email: "updates@example.com"',
                    '  to: ["alice@example.com"]',
                    '  granularities: ["day"]',
                ]
            )
            + "\n",
            encoding="utf-8",
        )
    manifest_path = tmp_path / "fleet.yaml"
    manifest_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "instances": [
                    {"name": "Alpha", "config_path": str(alpha_config)},
                    {"name": "Beta", "config_path": str(beta_config)},
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("RECOLETA_RESEND_API_KEY", "re_test_secret")

    result = runner.invoke(
        recoleta.cli.app,
        [
            "fleet",
            "run",
            "email",
            "preview",
            "--manifest",
            str(manifest_path),
            "--instance",
            "beta",
            "--output-dir",
            str(tmp_path / "preview"),
            "--json",
        ],
    )

    assert result.exit_code == 0, result.stdout
    payload = json.loads(result.stdout)
    assert payload["instance"] == "Beta"
    assert payload["results"][0]["primary_page_url"].startswith(
        "https://public.example/recoleta/trends/beta--"
    )
