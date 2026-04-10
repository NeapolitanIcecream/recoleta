from __future__ import annotations

from datetime import UTC, datetime
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import TypedDict
from unittest.mock import ANY

import pytest
from typer.testing import CliRunner

import recoleta.cli
import recoleta.cli.email as cli_email_module
import recoleta.cli.fleet as cli_fleet_module
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
    trend_doc_id: int
    trend_note_path: Path
    item_note_path: Path


def _set_email_env(
    *,
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    output_dir: Path,
    recipients: list[str] | None = None,
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
                "granularity": "day",
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

    trend_doc = repository.upsert_document_for_trend(
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
        title="Agent systems",
    )
    assert trend_doc.id is not None
    trend_note_path = write_markdown_trend_note(
        output_dir=output_dir,
        trend_doc_id=int(trend_doc.id),
        title="Agent systems",
        granularity="day",
        period_start=datetime(2026, 2, 25, tzinfo=UTC),
        period_end=datetime(2026, 2, 26, tzinfo=UTC),
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
            raw.replace("run_id: run-trend-email", f"run_id: run-trend-email\ninstance: {instance}"),
            encoding="utf-8",
        )
    return {
        "output_dir": output_dir,
        "repository": repository,
        "trend_doc_id": int(trend_doc.id),
        "trend_note_path": trend_note_path,
        "item_note_path": item_note_path,
    }


def test_export_trend_static_site_writes_email_link_map_artifact(tmp_path: Path) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = fixture["output_dir"]
    trend_note_path = fixture["trend_note_path"]
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
    alpha_trend = Path(alpha_fixture["trend_note_path"])
    beta_trend = Path(beta_fixture["trend_note_path"])
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

    assert result.preview_dir.exists()
    assert result.manifest_path.exists()
    html_body = result.html_path.read_text(encoding="utf-8")
    text_body = result.text_path.read_text(encoding="utf-8")
    assert "https://public.example/recoleta/trends/" in html_body
    assert "https://public.example/recoleta/items/" in html_body
    assert "Open on site" in html_body
    assert "Agent systems" in text_body
    manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
    assert manifest["content_hash"] == result.content_hash
    assert manifest["primary_page_url"] == result.primary_page_url


def test_send_trend_email_blocks_when_primary_page_is_not_publicly_reachable(
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

    with pytest.raises(RuntimeError, match="public trend page is not reachable"):
        send_trend_email(
            settings=settings,
            repository=repository,
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: False,
        )


def test_send_trend_email_skips_duplicate_batch_for_unchanged_content(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_id"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    sender = FakeResendBatchSender()

    first = send_trend_email(
        settings=settings,
        repository=repository,
        site_output_dir=site_dir,
        sender=sender,
        url_checker=lambda _url: True,
    )
    second = send_trend_email(
        settings=settings,
        repository=repository,
        site_output_dir=site_dir,
        sender=sender,
        url_checker=lambda _url: True,
    )

    assert first.status == "sent"
    assert second.status == "skipped"
    assert len(sender.calls) == 1
    rows = repository.list_trend_deliveries(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
    )
    assert len(rows) == 2
    assert {row.status for row in rows} == {DELIVERY_STATUS_SENT}


def test_send_trend_email_allows_retry_after_failed_batch_and_force_for_mixed_state(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_id"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)
    preview = build_trend_email_preview(settings=settings, site_output_dir=site_dir)
    retry_sender = FakeResendBatchSender()

    assert settings.email is not None
    for destination in settings.email.to:
        repository.upsert_trend_delivery(
            doc_id=trend_doc_id,
            channel=DELIVERY_CHANNEL_EMAIL,
            destination=destination,
            content_hash=preview.content_hash,
            message_id=None,
            status=DELIVERY_STATUS_FAILED,
            error="provider failed",
        )

    retry_result = send_trend_email(
        settings=settings,
        repository=repository,
        site_output_dir=site_dir,
        sender=retry_sender,
        url_checker=lambda _url: True,
    )
    assert retry_result.status == "sent"
    assert retry_sender.calls == [
        {
            "emails": ANY,
            "idempotency_key": ANY,
        }
    ]
    assert retry_sender.calls[0]["idempotency_key"] != (
        f"trend-email:{trend_doc_id}:{preview.content_hash}"
    )

    repository.upsert_trend_delivery(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
        destination=settings.email.to[0],
        content_hash=preview.content_hash,
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

    with pytest.raises(RuntimeError, match="mixed_batch_state"):
        send_trend_email(
            settings=settings,
            repository=repository,
            site_output_dir=site_dir,
            sender=FakeResendBatchSender(),
            url_checker=lambda _url: True,
        )

    forced = send_trend_email(
        settings=settings,
        repository=repository,
        site_output_dir=site_dir,
        sender=FakeResendBatchSender(),
        url_checker=lambda _url: True,
        force_batch=True,
    )
    assert forced.status == "sent"


def test_send_trend_email_returns_failed_when_any_recipient_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    fixture = _write_email_fixture(tmp_path=tmp_path)
    output_dir = Path(fixture["output_dir"])
    repository = fixture["repository"]
    trend_doc_id = int(fixture["trend_doc_id"])
    settings = _set_email_env(monkeypatch=monkeypatch, tmp_path=tmp_path, output_dir=output_dir)
    site_dir = tmp_path / "site"
    export_trend_static_site(input_dir=output_dir, output_dir=site_dir)

    result = send_trend_email(
        settings=settings,
        repository=repository,
        site_output_dir=site_dir,
        sender=PartialFailureResendBatchSender(),
        url_checker=lambda _url: True,
    )

    assert result.status == "failed"
    rows = repository.list_trend_deliveries(
        doc_id=trend_doc_id,
        channel=DELIVERY_CHANNEL_EMAIL,
    )
    assert len(rows) == 2
    assert {row.status for row in rows} == {DELIVERY_STATUS_SENT, DELIVERY_STATUS_FAILED}


def test_run_email_send_command_exits_non_zero_when_batch_fails(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runtime = SimpleNamespace(
        settings=object(),
        repository=object(),
        console=SimpleNamespace(print=lambda *args, **kwargs: None),
    )
    failed_result = SimpleNamespace(
        status="failed",
        send_dir=tmp_path / "send",
        manifest_path=tmp_path / "send" / "manifest.json",
        html_path=tmp_path / "send" / "body.html",
        text_path=tmp_path / "send" / "body.txt",
        primary_page_url="https://public.example/recoleta/trends/example",
        content_hash="hash-123",
        subject="[Recoleta] Day trends · 2026-02-25",
        instance="default",
        trend_doc_id=123,
        period_token="2026-02-25",
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
                "granularity": "week",
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
    failed_result = SimpleNamespace(
        status="failed",
        send_dir=tmp_path / "send",
        manifest_path=tmp_path / "send" / "manifest.json",
        html_path=tmp_path / "send" / "body.html",
        text_path=tmp_path / "send" / "body.txt",
        primary_page_url="https://public.example/recoleta/trends/example",
        content_hash="hash-123",
        subject="[Recoleta][Beta] Day trends · 2026-02-25",
        instance="Beta",
        trend_doc_id=123,
        period_token="2026-02-25",
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
                    '  granularity: "day"',
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
    assert payload["primary_page_url"].startswith("https://public.example/recoleta/trends/beta--")
