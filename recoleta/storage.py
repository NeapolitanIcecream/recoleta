from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import Any, cast
from uuid import uuid4

from rapidfuzz import fuzz
from sqlalchemy import desc, event, func, text
from sqlmodel import Session, SQLModel, create_engine, select

from recoleta.models import (
    Analysis,
    Artifact,
    ChunkEmbedding,
    Content,
    Delivery,
    Document,
    DocumentChunk,
    Item,
    Metric,
    Run,
    DELIVERY_STATUS_SENT,
    ITEM_STATE_ANALYZED,
    ITEM_STATE_ENRICHED,
    ITEM_STATE_FAILED,
    ITEM_STATE_INGESTED,
    ITEM_STATE_PUBLISHED,
    ITEM_STATE_RETRYABLE_FAILED,
    ITEM_STATE_TRIAGED,
    RUN_STATUS_FAILED,
    RUN_STATUS_RUNNING,
    RUN_STATUS_SUCCEEDED,
)
from recoleta.types import AnalysisResult, ItemDraft, sha256_hex, utc_now


def _to_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _from_json_list(value: str | None) -> list[str]:
    if not value:
        return []
    loaded = json.loads(value)
    if isinstance(loaded, list):
        return [str(item) for item in loaded]
    return []


def _from_json_object(value: str | None) -> dict[str, Any]:
    if not value:
        return {}
    try:
        loaded = json.loads(value)
    except Exception:
        return {}
    return loaded if isinstance(loaded, dict) else {}


@dataclass
class SqlDiagnostics:
    queries_total: int = 0
    commits_total: int = 0


class Repository:
    def __init__(
        self,
        *,
        db_path: Path,
        title_dedup_threshold: float = 92.0,
        title_dedup_max_candidates: int = 500,
    ) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(
            f"sqlite:///{self.db_path}",
            echo=False,
            connect_args={"check_same_thread": False},
        )
        self.title_dedup_threshold = float(title_dedup_threshold)
        self.title_dedup_max_candidates = max(0, int(title_dedup_max_candidates))
        self._sql_diag_lock = Lock()
        self._sql_diag_active: SqlDiagnostics | None = None
        self._sql_diag_installed = False

    def _ensure_sql_diagnostics_installed(self) -> None:
        if self._sql_diag_installed:
            return

        def _before_cursor_execute(*_: Any, **__: Any) -> None:
            active = self._sql_diag_active
            if active is None:
                return
            with self._sql_diag_lock:
                active.queries_total += 1

        event.listen(self.engine, "before_cursor_execute", _before_cursor_execute)
        self._sql_diag_installed = True

    @contextmanager
    def sql_diagnostics(self) -> Any:
        """Collect coarse SQL diagnostics for a single run (aggregate counts only)."""

        self._ensure_sql_diagnostics_installed()
        diag = SqlDiagnostics()
        with self._sql_diag_lock:
            previous = self._sql_diag_active
            self._sql_diag_active = diag
        try:
            yield diag
        finally:
            with self._sql_diag_lock:
                self._sql_diag_active = previous

    def _commit(self, session: Session) -> None:
        active = self._sql_diag_active
        if active is not None:
            with self._sql_diag_lock:
                active.commits_total += 1
        session.commit()

    def init_schema(self) -> None:
        SQLModel.metadata.create_all(self.engine)
        self._ensure_chunk_fts()

    def _ensure_chunk_fts(self) -> None:
        # FTS5 is not created by SQLModel metadata.
        ddl = """
        CREATE VIRTUAL TABLE IF NOT EXISTS chunk_fts USING fts5(
            text,
            doc_id UNINDEXED,
            chunk_index UNINDEXED,
            kind UNINDEXED
        );
        """
        with self.engine.begin() as conn:
            conn.execute(text(ddl))

    def create_run(self, config_fingerprint: str, run_id: str | None = None) -> Run:
        run = Run(
            id=run_id or str(uuid4()),
            status=RUN_STATUS_RUNNING,
            config_fingerprint=config_fingerprint,
        )
        with Session(self.engine) as session:
            session.add(run)
            self._commit(session)
            session.refresh(run)
            return run

    def finish_run(self, run_id: str, success: bool) -> None:
        final_status = RUN_STATUS_SUCCEEDED if success else RUN_STATUS_FAILED
        with Session(self.engine) as session:
            run = session.get(Run, run_id)
            if run is None:
                return
            run.status = final_status
            run.finished_at = utc_now()
            session.add(run)
            self._commit(session)

    def record_metric(
        self, *, run_id: str, name: str, value: float, unit: str | None = None
    ) -> None:
        metric = Metric(run_id=run_id, name=name, value=value, unit=unit)
        with Session(self.engine) as session:
            session.add(metric)
            self._commit(session)

    def list_metrics(self, *, run_id: str) -> list[Metric]:
        with Session(self.engine) as session:
            statement = (
                select(Metric)
                .where(Metric.run_id == run_id)
                .order_by(cast(Any, Metric.id))
            )
            return list(session.exec(statement))

    def count_items(self) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Item.id)))
            return int(session.exec(statement).one())

    def _find_near_duplicate_by_title(
        self, session: Session, *, title: str
    ) -> tuple[Item, float] | None:
        normalized_title = title.strip()
        if not normalized_title:
            return None
        if self.title_dedup_max_candidates <= 0:
            return None

        statement = (
            select(Item)
            .order_by(desc(cast(Any, Item.created_at)))
            .limit(self.title_dedup_max_candidates)
        )
        candidates = list(session.exec(statement))
        best_item: Item | None = None
        best_score = -1.0
        for candidate in candidates:
            score = float(fuzz.token_set_ratio(normalized_title, candidate.title))
            if score > best_score:
                best_score = score
                best_item = candidate
                if best_score >= 100.0:
                    return candidate, best_score
        if best_item is None:
            return None
        if best_score < self.title_dedup_threshold:
            return None
        return best_item, best_score

    def upsert_item(self, draft: ItemDraft) -> tuple[Item, bool]:
        with Session(self.engine) as session:
            existing: Item | None = None
            matched_by_title = False
            title_dedup_score: float | None = None
            if draft.source_item_id:
                statement = select(Item).where(
                    Item.source == draft.source,
                    Item.source_item_id == draft.source_item_id,
                )
                existing = session.exec(statement).first()

            if existing is None:
                by_url_hash = select(Item).where(
                    Item.canonical_url_hash == draft.canonical_url_hash
                )
                existing = session.exec(by_url_hash).first()

            if existing is None and self.title_dedup_threshold > 0:
                match = self._find_near_duplicate_by_title(session, title=draft.title)
                if match is not None:
                    existing, title_dedup_score = match
                    matched_by_title = True

            if existing is None:
                created = Item(
                    source=draft.source,
                    source_item_id=draft.source_item_id,
                    canonical_url=draft.canonical_url,
                    canonical_url_hash=draft.canonical_url_hash,
                    title=draft.title,
                    authors=_to_json(draft.authors),
                    published_at=draft.published_at,
                    raw_metadata_json=_to_json(draft.raw_metadata),
                    state=ITEM_STATE_INGESTED,
                )
                session.add(created)
                self._commit(session)
                session.refresh(created)
                return created, True

            previous_state = existing.state
            if matched_by_title:
                current_metadata = _from_json_object(existing.raw_metadata_json)
                alternate_urls = current_metadata.get("alternate_urls")
                if not isinstance(alternate_urls, list):
                    alternate_urls = []
                if (
                    draft.canonical_url != existing.canonical_url
                    and draft.canonical_url not in alternate_urls
                ):
                    alternate_urls.append(draft.canonical_url)
                current_metadata["alternate_urls"] = alternate_urls

                dedup_events = current_metadata.get("dedup_events")
                if not isinstance(dedup_events, list):
                    dedup_events = []
                dedup_events.append(
                    {
                        "source": draft.source,
                        "source_item_id": draft.source_item_id,
                        "canonical_url_hash": draft.canonical_url_hash,
                        "title_similarity": round(float(title_dedup_score or 0.0), 2),
                    }
                )
                current_metadata["dedup_events"] = dedup_events[-20:]
                existing.raw_metadata_json = _to_json(current_metadata)
                if existing.published_at is None and draft.published_at is not None:
                    existing.published_at = draft.published_at
            else:
                existing.canonical_url = draft.canonical_url
                existing.canonical_url_hash = draft.canonical_url_hash
                existing.title = draft.title
                existing.authors = _to_json(draft.authors)
                existing.published_at = draft.published_at
                existing.raw_metadata_json = _to_json(draft.raw_metadata)
            if previous_state in {ITEM_STATE_FAILED, ITEM_STATE_RETRYABLE_FAILED}:
                # Allow failed items to be retried by re-ingesting.
                existing.state = ITEM_STATE_INGESTED
            existing.updated_at = utc_now()
            if (
                (not matched_by_title)
                and existing.source == draft.source
                and existing.source_item_id is None
                and draft.source_item_id is not None
            ):
                existing.source_item_id = draft.source_item_id
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing, False

    def list_items_for_analysis(self, *, limit: int) -> list[Item]:
        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(
                    cast(Any, Item.state).in_(
                        [
                            ITEM_STATE_INGESTED,
                            ITEM_STATE_ENRICHED,
                            ITEM_STATE_RETRYABLE_FAILED,
                        ]
                    )
                )
                .order_by(
                    desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at))
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def list_items_for_llm_analysis(
        self, *, limit: int, triage_required: bool
    ) -> list[Item]:
        states = [ITEM_STATE_RETRYABLE_FAILED]
        if triage_required:
            states.append(ITEM_STATE_TRIAGED)
        else:
            states.append(ITEM_STATE_ENRICHED)

        with Session(self.engine) as session:
            statement = (
                select(Item)
                .where(cast(Any, Item.state).in_(states))
                .order_by(
                    desc(cast(Any, Item.updated_at)), desc(cast(Any, Item.created_at))
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def get_latest_content(self, *, item_id: int, content_type: str) -> Content | None:
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(Content.item_id == item_id, Content.content_type == content_type)
                .order_by(desc(cast(Any, Content.id)))
            )
            return session.exec(statement).first()

    def get_latest_content_texts(
        self, *, item_id: int, content_types: list[str]
    ) -> dict[str, str | None]:
        """Fetch latest text for multiple content_types of a single item in one query."""

        normalized_item_id = int(item_id)
        types = [str(t or "").strip() for t in (content_types or [])]
        types = [t for t in types if t]
        if normalized_item_id <= 0 or not types:
            return {}

        wanted = set(types)
        out: dict[str, str | None] = {t: None for t in types}
        with Session(self.engine) as session:
            statement = (
                select(Content)
                .where(
                    Content.item_id == normalized_item_id,
                    cast(Any, Content.content_type).in_(types),
                )
                .order_by(desc(cast(Any, Content.id)))
            )
            for content in session.exec(statement):
                ctype = str(getattr(content, "content_type", "") or "").strip()
                if ctype in wanted and out.get(ctype) is None:
                    text = getattr(content, "text", None)
                    out[ctype] = (
                        text if isinstance(text, str) and text.strip() else None
                    )
                    wanted.discard(ctype)
                    if not wanted:
                        break
        return out

    def get_latest_contents(
        self, *, item_ids: list[int], content_type: str
    ) -> dict[int, Content]:
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw_item_id in item_ids:
            try:
                item_id = int(raw_item_id)
            except Exception:
                continue
            if item_id <= 0 or item_id in seen:
                continue
            seen.add(item_id)
            normalized_ids.append(item_id)
        normalized_type = str(content_type or "").strip()
        if not normalized_ids or not normalized_type:
            return {}

        with Session(self.engine) as session:
            latest_ids = (
                select(
                    cast(Any, Content.item_id),
                    func.max(cast(Any, Content.id)).label("max_id"),
                )
                .where(
                    cast(Any, Content.item_id).in_(normalized_ids),
                    Content.content_type == normalized_type,
                )
                .group_by(cast(Any, Content.item_id))
                .subquery()
            )
            statement = select(Content).join(
                latest_ids, cast(Any, Content.id) == latest_ids.c.max_id
            )
            contents = list(session.exec(statement))
            return {content.item_id: content for content in contents}

    def upsert_contents_texts(
        self, *, item_id: int, texts_by_type: dict[str, str]
    ) -> int:
        """Upsert multiple text contents for a single item with one commit."""

        normalized_item_id = int(item_id)
        if normalized_item_id <= 0:
            raise ValueError("item_id must be > 0")
        if not isinstance(texts_by_type, dict) or not texts_by_type:
            return 0

        normalized: dict[str, str] = {}
        for raw_type, raw_text in texts_by_type.items():
            content_type = str(raw_type or "").strip()
            if not content_type:
                continue
            if not isinstance(raw_text, str):
                continue
            text = raw_text.strip()
            if not text:
                continue
            normalized[content_type] = text
        if not normalized:
            return 0

        hashes_by_type: dict[str, str] = {
            ctype: sha256_hex(text) for ctype, text in normalized.items()
        }
        target_types = list(hashes_by_type.keys())
        target_hashes = list(set(hashes_by_type.values()))

        inserted = 0
        with Session(self.engine) as session:
            existing_pairs: set[tuple[str, str]] = set()
            statement = select(Content.content_type, Content.content_hash).where(
                Content.item_id == normalized_item_id,
                cast(Any, Content.content_type).in_(target_types),
                cast(Any, Content.content_hash).in_(target_hashes),
            )
            for ctype, chash in session.exec(statement):
                existing_pairs.add((str(ctype), str(chash)))

            for ctype, text in normalized.items():
                chash = hashes_by_type[ctype]
                if (ctype, chash) in existing_pairs:
                    continue
                session.add(
                    Content(
                        item_id=normalized_item_id,
                        content_type=ctype,
                        text=text,
                        artifact_path=None,
                        content_hash=chash,
                    )
                )
                inserted += 1

            if inserted > 0:
                self._commit(session)
        return inserted

    def upsert_content(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> Content:
        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content

    def upsert_content_with_inserted(
        self,
        *,
        item_id: int,
        content_type: str,
        text: str | None,
        artifact_path: str | None = None,
    ) -> tuple[Content, bool]:
        """Upsert a single content row and report whether it inserted a new record."""

        if text is None and artifact_path is None:
            raise ValueError("Either text or artifact_path must be provided")
        normalized_text = text.strip() if isinstance(text, str) else None
        if normalized_text == "":
            raise ValueError("text must not be empty")

        if normalized_text is not None:
            content_hash = sha256_hex(normalized_text)
        else:
            resolved = Path(str(artifact_path)).expanduser().resolve()
            content_hash = hashlib.sha256(resolved.read_bytes()).hexdigest()

        with Session(self.engine) as session:
            existing = session.exec(
                select(Content).where(
                    Content.item_id == item_id,
                    Content.content_type == content_type,
                    Content.content_hash == content_hash,
                )
            ).first()
            if existing is not None:
                return existing, False

            content = Content(
                item_id=item_id,
                content_type=content_type,
                text=normalized_text,
                artifact_path=artifact_path,
                content_hash=content_hash,
            )
            session.add(content)
            self._commit(session)
            session.refresh(content)
            return content, True

    def save_analysis(self, *, item_id: int, result: AnalysisResult) -> Analysis:
        with Session(self.engine) as session:
            analysis = session.exec(
                select(Analysis).where(Analysis.item_id == item_id)
            ).first()
            if analysis is None:
                analysis = Analysis(
                    item_id=item_id,
                    model=result.model,
                    provider=result.provider,
                    summary=result.summary,
                    topics_json=_to_json(result.topics),
                    relevance_score=result.relevance_score,
                    novelty_score=result.novelty_score,
                    cost_usd=result.cost_usd,
                    latency_ms=result.latency_ms,
                )
            else:
                analysis.model = result.model
                analysis.provider = result.provider
                analysis.summary = result.summary
                analysis.topics_json = _to_json(result.topics)
                analysis.relevance_score = result.relevance_score
                analysis.novelty_score = result.novelty_score
                analysis.cost_usd = result.cost_usd
                analysis.latency_ms = result.latency_ms

            item = session.get(Item, item_id)
            if item is not None:
                item.state = ITEM_STATE_ANALYZED
                item.updated_at = utc_now()
                session.add(item)

            session.add(analysis)
            self._commit(session)
            session.refresh(analysis)
            return analysis

    def mark_item_enriched(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_ENRICHED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_triaged(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_TRIAGED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def mark_item_retryable_failed(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_RETRYABLE_FAILED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def list_items_for_publish(
        self, *, limit: int, min_relevance_score: float
    ) -> list[tuple[Item, Analysis]]:
        with Session(self.engine) as session:
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(
                    Item.state == ITEM_STATE_ANALYZED,
                    Analysis.relevance_score >= min_relevance_score,
                )
                .order_by(
                    desc(cast(Any, Analysis.relevance_score)),
                    desc(cast(Any, Analysis.novelty_score)),
                )
                .limit(limit)
            )
            return list(session.exec(statement))

    def has_sent_delivery(
        self, *, item_id: int, channel: str, destination: str
    ) -> bool:
        with Session(self.engine) as session:
            statement = select(Delivery).where(
                Delivery.item_id == item_id,
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
            )
            return session.exec(statement).first() is not None

    def count_sent_deliveries_since(
        self, *, channel: str, destination: str, since: datetime
    ) -> int:
        with Session(self.engine) as session:
            statement = select(func.count(cast(Any, Delivery.id))).where(
                Delivery.channel == channel,
                Delivery.destination == destination,
                Delivery.status == DELIVERY_STATUS_SENT,
                cast(Any, Delivery.sent_at).is_not(None),
                cast(Any, Delivery.sent_at) >= since,
            )
            return int(session.exec(statement).one())

    def upsert_delivery(
        self,
        *,
        item_id: int,
        channel: str,
        destination: str,
        message_id: str | None,
        status: str,
        error: str | None = None,
    ) -> Delivery:
        now = utc_now()
        with Session(self.engine) as session:
            existing = session.exec(
                select(Delivery).where(
                    Delivery.item_id == item_id,
                    Delivery.channel == channel,
                    Delivery.destination == destination,
                )
            ).first()
            if existing is None:
                delivery = Delivery(
                    item_id=item_id,
                    channel=channel,
                    destination=destination,
                    message_id=message_id,
                    status=status,
                    error=error,
                    sent_at=now if status == DELIVERY_STATUS_SENT else None,
                )
                session.add(delivery)
                self._commit(session)
                session.refresh(delivery)
                return delivery

            existing.message_id = message_id
            existing.status = status
            existing.error = error
            if status == DELIVERY_STATUS_SENT:
                existing.sent_at = now
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def mark_item_published(self, *, item_id: int) -> None:
        with Session(self.engine) as session:
            item = session.get(Item, item_id)
            if item is None:
                return
            item.state = ITEM_STATE_PUBLISHED
            item.updated_at = utc_now()
            session.add(item)
            self._commit(session)

    def list_analyzed_items_in_period(
        self,
        *,
        period_start: datetime,
        period_end: datetime,
        limit: int,
        offset: int = 0,
    ) -> list[tuple[Item, Analysis]]:
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            event_at = func.coalesce(
                cast(Any, Item.published_at), cast(Any, Item.created_at)
            )
            statement = (
                select(Item, Analysis)
                .join(Analysis, cast(Any, Analysis.item_id) == cast(Any, Item.id))
                .where(
                    cast(Any, Item.state).in_(
                        [ITEM_STATE_ANALYZED, ITEM_STATE_PUBLISHED]
                    ),
                    event_at >= period_start,
                    event_at < period_end,
                )
                .order_by(desc(cast(Any, event_at)), desc(cast(Any, Item.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

    def upsert_document_for_item(self, *, item: Item) -> Document:
        raw_item_id = getattr(item, "id", None)
        if raw_item_id is None:
            raise ValueError("item must have an id")
        item_id = int(raw_item_id)
        if item_id <= 0:
            raise ValueError("item_id must be > 0")
        event_at = item.published_at or item.created_at
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == "item",
                    Document.item_id == item_id,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="item",
                    item_id=item_id,
                    source=str(getattr(item, "source", "") or "").strip() or None,
                    canonical_url=str(getattr(item, "canonical_url", "") or "").strip()
                    or None,
                    title=str(getattr(item, "title", "") or "").strip() or None,
                    published_at=event_at,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.source = str(getattr(item, "source", "") or "").strip() or None
            existing.canonical_url = (
                str(getattr(item, "canonical_url", "") or "").strip() or None
            )
            existing.title = str(getattr(item, "title", "") or "").strip() or None
            existing.published_at = event_at
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def upsert_document_for_trend(
        self,
        *,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
        title: str,
    ) -> Document:
        normalized_granularity = str(granularity or "").strip().lower()
        if normalized_granularity not in {"day", "week", "month"}:
            raise ValueError("unsupported granularity")
        normalized_title = str(title or "").strip() or "Trend"
        with Session(self.engine) as session:
            existing = session.exec(
                select(Document).where(
                    Document.doc_type == "trend",
                    Document.granularity == normalized_granularity,
                    Document.period_start == period_start,
                    Document.period_end == period_end,
                )
            ).first()
            if existing is None:
                doc = Document(
                    doc_type="trend",
                    granularity=normalized_granularity,
                    period_start=period_start,
                    period_end=period_end,
                    title=normalized_title,
                )
                session.add(doc)
                self._commit(session)
                session.refresh(doc)
                return doc

            existing.title = normalized_title
            existing.updated_at = utc_now()
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def upsert_document_chunk(
        self,
        *,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
        start_char: int | None = None,
        end_char: int | None = None,
        source_content_type: str | None = None,
    ) -> tuple[DocumentChunk, bool]:
        normalized_doc_id = int(doc_id)
        if normalized_doc_id <= 0:
            raise ValueError("doc_id must be > 0")
        normalized_index = int(chunk_index)
        if normalized_index < 0:
            raise ValueError("chunk_index must be >= 0")
        normalized_kind = str(kind or "").strip().lower()
        if normalized_kind not in {"summary", "content", "meta"}:
            raise ValueError("unsupported chunk kind")
        normalized_text = str(text_value or "").strip()
        if not normalized_text:
            raise ValueError("chunk text must not be empty")
        text_hash = sha256_hex(normalized_text)

        inserted = False
        with Session(self.engine) as session:
            existing = session.exec(
                select(DocumentChunk).where(
                    DocumentChunk.doc_id == normalized_doc_id,
                    DocumentChunk.chunk_index == normalized_index,
                )
            ).first()
            if existing is None:
                chunk = DocumentChunk(
                    doc_id=normalized_doc_id,
                    chunk_index=normalized_index,
                    kind=normalized_kind,
                    text=normalized_text,
                    start_char=start_char,
                    end_char=end_char,
                    text_hash=text_hash,
                    source_content_type=(
                        str(source_content_type).strip()
                        if isinstance(source_content_type, str)
                        and str(source_content_type).strip()
                        else None
                    ),
                )
                session.add(chunk)
                self._commit(session)
                session.refresh(chunk)
                inserted = True
            else:
                if str(getattr(existing, "text_hash", "") or "") == text_hash:
                    return existing, False
                existing.kind = normalized_kind
                existing.text = normalized_text
                existing.start_char = start_char
                existing.end_char = end_char
                existing.text_hash = text_hash
                existing.source_content_type = (
                    str(source_content_type).strip()
                    if isinstance(source_content_type, str)
                    and str(source_content_type).strip()
                    else None
                )
                session.add(existing)
                self._commit(session)
                session.refresh(existing)
                chunk = existing

        chunk_id = getattr(chunk, "id", None)
        if chunk_id is not None:
            self._sync_chunk_fts(
                chunk_id=int(chunk_id),
                doc_id=normalized_doc_id,
                chunk_index=normalized_index,
                kind=normalized_kind,
                text_value=normalized_text,
            )
        return chunk, inserted

    def _sync_chunk_fts(
        self,
        *,
        chunk_id: int,
        doc_id: int,
        chunk_index: int,
        kind: str,
        text_value: str,
    ) -> None:
        normalized_chunk_id = int(chunk_id)
        normalized_doc_id = int(doc_id)
        if normalized_chunk_id <= 0 or normalized_doc_id <= 0:
            return
        payload = {
            "rowid": normalized_chunk_id,
            "text": str(text_value),
            "doc_id": normalized_doc_id,
            "chunk_index": int(chunk_index),
            "kind": str(kind),
        }
        with self.engine.begin() as conn:
            conn.execute(
                text("DELETE FROM chunk_fts WHERE rowid = :rowid"),
                {"rowid": normalized_chunk_id},
            )
            conn.execute(
                text(
                    "INSERT INTO chunk_fts(rowid, text, doc_id, chunk_index, kind) "
                    "VALUES(:rowid, :text, :doc_id, :chunk_index, :kind)"
                ),
                payload,
            )

    def list_documents(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        granularity: str | None = None,
        order_by: str = "event_desc",
        offset: int = 0,
        limit: int = 50,
    ) -> list[Document]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []
        with Session(self.engine) as session:
            statement = select(Document).where(Document.doc_type == normalized_type)
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.published_at), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.published_at)),
                        desc(cast(Any, Document.id)),
                    )
            elif normalized_type == "trend":
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) >= period_start,
                    cast(Any, Document.period_end) <= period_end,
                )
                normalized_granularity = (
                    str(granularity or "").strip().lower()
                    if granularity is not None
                    else ""
                )
                if normalized_granularity:
                    statement = statement.where(
                        Document.granularity == normalized_granularity
                    )
                if order_by == "event_asc":
                    statement = statement.order_by(
                        cast(Any, Document.period_start), cast(Any, Document.id)
                    )
                else:
                    statement = statement.order_by(
                        desc(cast(Any, Document.period_start)),
                        desc(cast(Any, Document.id)),
                    )
            else:
                raise ValueError("unsupported doc_type")
            statement = statement.offset(normalized_offset).limit(normalized_limit)
            return list(session.exec(statement))

    def get_document(self, *, doc_id: int) -> Document | None:
        normalized_id = int(doc_id)
        if normalized_id <= 0:
            return None
        with Session(self.engine) as session:
            return session.get(Document, normalized_id)

    def read_document_chunk(
        self, *, doc_id: int, chunk_index: int
    ) -> DocumentChunk | None:
        normalized_doc_id = int(doc_id)
        normalized_index = int(chunk_index)
        if normalized_doc_id <= 0 or normalized_index < 0:
            return None
        with Session(self.engine) as session:
            statement = select(DocumentChunk).where(
                DocumentChunk.doc_id == normalized_doc_id,
                DocumentChunk.chunk_index == normalized_index,
            )
            return session.exec(statement).first()

    def search_chunks_text(
        self,
        *,
        query: str,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        normalized_query = str(query or "").strip()
        if not normalized_query:
            return []
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(1, min(int(limit), 50))

        if normalized_type == "item":
            period_pred = (
                "d.published_at >= :period_start AND d.published_at < :period_end"
            )
        elif normalized_type == "trend":
            period_pred = (
                "d.period_start >= :period_start AND d.period_end <= :period_end"
            )
        else:
            raise ValueError("unsupported doc_type")

        sql = f"""
        SELECT
            dc.id AS chunk_id,
            dc.doc_id AS doc_id,
            dc.chunk_index AS chunk_index,
            dc.kind AS kind,
            snippet(chunk_fts, 0, '[', ']', '…', 12) AS snippet,
            bm25(chunk_fts) AS rank
        FROM chunk_fts
        JOIN document_chunks dc ON dc.id = chunk_fts.rowid
        JOIN documents d ON d.id = dc.doc_id
        WHERE
            chunk_fts MATCH :query
            AND d.doc_type = :doc_type
            AND {period_pred}
        ORDER BY rank ASC
        LIMIT :limit
        """
        params = {
            "query": normalized_query,
            "doc_type": normalized_type,
            "period_start": period_start,
            "period_end": period_end,
            "limit": normalized_limit,
        }
        with self.engine.begin() as conn:
            rows = conn.execute(text(sql), params).mappings().all()
        out: list[dict[str, Any]] = []
        for row in rows:
            raw_chunk_id = row.get("chunk_id")
            raw_doc_id = row.get("doc_id")
            raw_chunk_index = row.get("chunk_index")
            if raw_chunk_id is None or raw_doc_id is None or raw_chunk_index is None:
                continue
            try:
                chunk_id = int(raw_chunk_id)
                doc_id = int(raw_doc_id)
                chunk_index = int(raw_chunk_index)
            except Exception:
                continue
            if chunk_id <= 0 or doc_id <= 0 or chunk_index < 0:
                continue
            out.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": doc_id,
                    "chunk_index": chunk_index,
                    "kind": str(row.get("kind") or ""),
                    "snippet": str(row.get("snippet") or ""),
                    "rank": float(row.get("rank") or 0.0),
                }
            )
        return out

    def list_summary_chunks_in_period(
        self,
        *,
        doc_type: str,
        period_start: datetime,
        period_end: datetime,
        limit: int = 500,
        offset: int = 0,
    ) -> list[DocumentChunk]:
        normalized_type = str(doc_type or "").strip().lower()
        normalized_limit = max(0, int(limit))
        normalized_offset = max(0, int(offset))
        if normalized_limit <= 0:
            return []

        with Session(self.engine) as session:
            statement = (
                select(DocumentChunk)
                .join(
                    Document, cast(Any, Document.id) == cast(Any, DocumentChunk.doc_id)
                )
                .where(
                    Document.doc_type == normalized_type,
                    DocumentChunk.kind == "summary",
                )
            )
            if normalized_type == "item":
                statement = statement.where(
                    cast(Any, Document.published_at).is_not(None),
                    cast(Any, Document.published_at) >= period_start,
                    cast(Any, Document.published_at) < period_end,
                )
            elif normalized_type == "trend":
                statement = statement.where(
                    cast(Any, Document.period_start).is_not(None),
                    cast(Any, Document.period_end).is_not(None),
                    cast(Any, Document.period_start) >= period_start,
                    cast(Any, Document.period_end) <= period_end,
                )
            else:
                raise ValueError("unsupported doc_type")

            statement = (
                statement.order_by(desc(cast(Any, DocumentChunk.id)))
                .offset(normalized_offset)
                .limit(normalized_limit)
            )
            return list(session.exec(statement))

    def get_chunk_embedding(
        self, *, chunk_id: int, model: str
    ) -> ChunkEmbedding | None:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        if normalized_chunk_id <= 0 or not normalized_model:
            return None
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.chunk_id == normalized_chunk_id,
                ChunkEmbedding.model == normalized_model,
            )
            return session.exec(statement).first()

    def list_chunk_embeddings(
        self, *, chunk_ids: list[int], model: str
    ) -> dict[int, ChunkEmbedding]:
        normalized_model = str(model or "").strip()
        if not normalized_model:
            return {}
        normalized_ids: list[int] = []
        seen: set[int] = set()
        for raw in chunk_ids or []:
            try:
                cid = int(raw)
            except Exception:
                continue
            if cid <= 0 or cid in seen:
                continue
            seen.add(cid)
            normalized_ids.append(cid)
        if not normalized_ids:
            return {}
        with Session(self.engine) as session:
            statement = select(ChunkEmbedding).where(
                ChunkEmbedding.model == normalized_model,
                cast(Any, ChunkEmbedding.chunk_id).in_(normalized_ids),
            )
            rows = list(session.exec(statement))
            return {int(row.chunk_id): row for row in rows}

    def upsert_chunk_embedding(
        self,
        *,
        chunk_id: int,
        model: str,
        dimensions: int | None,
        text_hash: str,
        vector: list[float],
    ) -> ChunkEmbedding:
        normalized_chunk_id = int(chunk_id)
        normalized_model = str(model or "").strip()
        normalized_text_hash = str(text_hash or "").strip()
        if normalized_chunk_id <= 0:
            raise ValueError("chunk_id must be > 0")
        if not normalized_model:
            raise ValueError("model must not be empty")
        if not normalized_text_hash:
            raise ValueError("text_hash must not be empty")
        if not isinstance(vector, list) or not vector:
            raise ValueError("vector must be a non-empty list")
        normalized_dims = int(dimensions) if dimensions is not None else None
        if normalized_dims is not None and normalized_dims <= 0:
            raise ValueError("dimensions must be positive")
        normalized_vector = [float(v) for v in vector]
        vector_json = _to_json(normalized_vector)

        with Session(self.engine) as session:
            existing = session.exec(
                select(ChunkEmbedding).where(
                    ChunkEmbedding.chunk_id == normalized_chunk_id,
                    ChunkEmbedding.model == normalized_model,
                )
            ).first()
            if existing is None:
                row = ChunkEmbedding(
                    chunk_id=normalized_chunk_id,
                    model=normalized_model,
                    dimensions=normalized_dims,
                    vector_json=vector_json,
                    text_hash=normalized_text_hash,
                )
                session.add(row)
                self._commit(session)
                session.refresh(row)
                return row

            if (
                str(getattr(existing, "text_hash", "") or "") == normalized_text_hash
                and str(getattr(existing, "vector_json", "") or "") == vector_json
            ):
                return existing
            existing.dimensions = normalized_dims
            existing.vector_json = vector_json
            existing.text_hash = normalized_text_hash
            session.add(existing)
            self._commit(session)
            session.refresh(existing)
            return existing

    def add_artifact(
        self, *, run_id: str, item_id: int | None, kind: str, path: str
    ) -> None:
        artifact = Artifact(run_id=run_id, item_id=item_id, kind=kind, path=path)
        with Session(self.engine) as session:
            session.add(artifact)
            self._commit(session)

    @staticmethod
    def decode_list(value: str | None) -> list[str]:
        return _from_json_list(value)
