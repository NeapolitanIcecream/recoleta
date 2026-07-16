from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import re
import sqlite3
from typing import Any


_PASS_KIND_TO_ARTIFACT = {
    "trend_synthesis": "trend",
    "trend_ideas": "idea",
}
_CANONICAL_TERMINAL_STATUSES = frozenset({"succeeded", "suppressed"})
_UNIT_FIELD = {"trend": "clusters", "idea": "ideas"}
_DEFAULT_NEAR_DUPLICATE_THRESHOLD = 0.5
_LEXICAL_SHINGLE_SIZE = 3
_TITLE_FRAME_LATIN_TOKENS = 2
_TITLE_FRAME_DENSE_TOKENS = 5
_OPENING_LATIN_TOKENS = 5
_OPENING_DENSE_TOKENS = 8
_BOILERPLATE_LATIN_TOKENS = 5
_BOILERPLATE_DENSE_TOKENS = 8
_SERIES_CANDIDATE_LIMIT = 20
_MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_TOKEN_RE = re.compile(r"[a-z0-9]+|[\u3400-\u9fff]|[^\W\d_]", re.IGNORECASE)
_DENSE_SCRIPT_TOKEN_RE = re.compile(
    r"^["
    r"\u1100-\u11ff"  # Hangul Jamo
    r"\u3040-\u30ff"  # Hiragana and Katakana
    r"\u3130-\u318f"  # Hangul Compatibility Jamo
    r"\u31f0-\u31ff"  # Katakana Phonetic Extensions
    r"\u3400-\u9fff"  # CJK ideographs
    r"\ua960-\ua97f"  # Hangul Jamo Extended-A
    r"\uac00-\ud7af"  # Hangul syllables
    r"\ud7b0-\ud7ff"  # Hangul Jamo Extended-B
    r"\uff66-\uff9f"  # Halfwidth Katakana
    r"]$"
)
_GENERIC_REASON_ZH_RE = re.compile(
    r"^(?:该|这)?(?:论文|来源|研究|文档|笔记|摘要)?"
    r"(?:报告|显示|描述|支持|说明)(?:了)?(?:该|这|本)?"
    r"(?:观点|结论|趋势|方向|假设|论点|证据|结果|内容)[。.]?$"
)
_GENERIC_REASON_WORDS = frozenset(
    {
        "a",
        "an",
        "anchors",
        "claim",
        "cluster",
        "context",
        "describes",
        "direction",
        "document",
        "evidence",
        "example",
        "finding",
        "grounds",
        "hypothesis",
        "illustrates",
        "item",
        "note",
        "paper",
        "point",
        "provides",
        "rationale",
        "reports",
        "result",
        "results",
        "shows",
        "source",
        "study",
        "summary",
        "supports",
        "supplies",
        "the",
        "this",
        "trend",
    }
)


@dataclass(frozen=True, slots=True)
class _PassOutputRow:
    database: str
    scope: str
    pass_output_id: int
    pass_kind: str
    status: str
    granularity: str
    period_start: str
    period_end: str
    payload_json: str


@dataclass(frozen=True, slots=True)
class _EvidenceRef:
    doc_id: int
    chunk_index: int
    reason: str


@dataclass(frozen=True, slots=True)
class _ArtifactUnit:
    database: str
    scope: str
    artifact_kind: str
    pass_output_id: int
    granularity: str
    period_start: str
    period_end: str
    unit_index: int
    title: str
    content: str
    evidence_refs_total: int
    exact_duplicate_refs: int
    distinct_doc_ids: tuple[int, ...]
    same_doc_multi_chunk_doc_ids: tuple[int, ...]
    same_doc_multi_chunk_extra_refs: int
    evidence_reasons: tuple[str, ...]

    @property
    def unit_id(self) -> str:
        return f"{self.artifact_kind}:{self.pass_output_id}:{self.unit_index}"

    def report_dict(self) -> dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "pass_output_id": self.pass_output_id,
            "granularity": self.granularity,
            "period_start": self.period_start,
            "period_end": self.period_end,
            "unit_index": self.unit_index,
            "title": self.title,
            "evidence_refs_total": self.evidence_refs_total,
            "exact_duplicate_refs": self.exact_duplicate_refs,
            "distinct_doc_ids": list(self.distinct_doc_ids),
            "distinct_doc_support_count": len(self.distinct_doc_ids),
            "same_doc_multi_chunk_doc_ids": list(self.same_doc_multi_chunk_doc_ids),
            "same_doc_multi_chunk_extra_refs": (self.same_doc_multi_chunk_extra_refs),
        }


@dataclass(frozen=True, slots=True)
class _ArtifactRecord:
    database: str
    scope: str
    artifact_kind: str
    pass_output_id: int
    granularity: str
    period_start: str
    period_end: str
    title: str
    summary: str


@dataclass(slots=True)
class _GroupEvaluation:
    report: dict[str, Any]
    trend_units: list[_ArtifactUnit]
    idea_units: list[_ArtifactUnit]
    records: list[_ArtifactRecord]


def _empty_diagnostics() -> Counter[str]:
    return Counter(
        {
            "relevant_pass_outputs_seen": 0,
            "terminal_pass_outputs": 0,
            "suppressed_pass_outputs": 0,
            "non_terminal_filtered": 0,
            "non_succeeded_filtered": 0,
            "succeeded_pass_outputs": 0,
            "canonical_pass_outputs": 0,
            "canonical_succeeded_outputs": 0,
            "canonical_suppressed_outputs": 0,
            "superseded_terminal_outputs": 0,
            "superseded_succeeded_outputs": 0,
            "superseded_suppressed_outputs": 0,
            "suppressed_units_ignored": 0,
            "malformed_payloads": 0,
            "non_object_payloads": 0,
            "missing_units_list": 0,
            "skipped_non_object_units": 0,
            "invalid_evidence_refs": 0,
            "legacy_ref_fields_used": 0,
        }
    )


def _read_database(
    database: Path,
) -> tuple[dict[str, list[_PassOutputRow]], dict[str, Counter[str]]]:
    resolved = database.expanduser().resolve()
    if not resolved.is_file():
        raise ValueError(f"database does not exist: {resolved}")
    connection = sqlite3.connect(f"{resolved.as_uri()}?mode=ro", uri=True)
    setattr(connection, "row_factory", sqlite3.Row)
    try:
        placeholders = ", ".join("?" for _ in _PASS_KIND_TO_ARTIFACT)
        rows = connection.execute(
            f"""
            select
                po.id,
                po.pass_kind,
                po.status,
                coalesce(po.granularity, '') as granularity,
                coalesce(cast(po.period_start as text), '') as period_start,
                coalesce(cast(po.period_end as text), '') as period_end,
                po.payload_json,
                coalesce(nullif(trim(r.scope), ''), 'default') as scope
            from pass_outputs po
            left join runs r on r.id = po.run_id
            where po.pass_kind in ({placeholders})
            order by po.created_at desc, po.id desc
            """,
            tuple(_PASS_KIND_TO_ARTIFACT),
        ).fetchall()
    finally:
        connection.close()

    records_by_scope: dict[str, list[_PassOutputRow]] = defaultdict(list)
    diagnostics_by_scope: dict[str, Counter[str]] = defaultdict(_empty_diagnostics)
    seen_keys: set[tuple[str, str, str, str, str]] = set()
    for row in rows:
        scope = str(row["scope"] or "default").strip() or "default"
        diagnostics = diagnostics_by_scope[scope]
        diagnostics["relevant_pass_outputs_seen"] += 1
        status = str(row["status"] or "").strip().lower()
        if status not in _CANONICAL_TERMINAL_STATUSES:
            diagnostics["non_terminal_filtered"] += 1
            # Compatibility alias retained for existing report consumers. It now
            # means a row whose status is ineligible for canonical selection.
            diagnostics["non_succeeded_filtered"] += 1
            continue
        diagnostics["terminal_pass_outputs"] += 1
        diagnostics[f"{status}_pass_outputs"] += 1
        key = (
            scope,
            str(row["pass_kind"]),
            str(row["granularity"] or "").strip().lower(),
            str(row["period_start"] or ""),
            str(row["period_end"] or ""),
        )
        if key in seen_keys:
            diagnostics["superseded_terminal_outputs"] += 1
            diagnostics[f"superseded_{status}_outputs"] += 1
            continue
        seen_keys.add(key)
        diagnostics["canonical_pass_outputs"] += 1
        diagnostics[f"canonical_{status}_outputs"] += 1
        records_by_scope[scope].append(
            _PassOutputRow(
                database=str(resolved),
                scope=scope,
                pass_output_id=int(row["id"]),
                pass_kind=str(row["pass_kind"]),
                status=status,
                granularity=key[2],
                period_start=key[3],
                period_end=key[4],
                payload_json=str(row["payload_json"] or ""),
            )
        )
    return dict(records_by_scope), dict(diagnostics_by_scope)


def _coerce_evidence_ref(raw_ref: Any) -> _EvidenceRef | None:
    raw_doc_id: Any
    raw_chunk_index: Any
    reason = ""
    if isinstance(raw_ref, bool):
        return None
    if isinstance(raw_ref, int | str):
        raw_doc_id = raw_ref
        raw_chunk_index = 0
    elif isinstance(raw_ref, dict):
        raw_doc_id = raw_ref.get("doc_id")
        raw_chunk_index = raw_ref.get("chunk_index", 0)
        reason = " ".join(str(raw_ref.get("reason") or "").split()).strip()
    else:
        return None
    try:
        doc_id = int(raw_doc_id)
        chunk_index = int(raw_chunk_index)
    except TypeError, ValueError:
        return None
    if doc_id <= 0 or chunk_index < 0:
        return None
    return _EvidenceRef(doc_id=doc_id, chunk_index=chunk_index, reason=reason)


def _unit_evidence_refs(
    unit: dict[str, Any], *, diagnostics: Counter[str]
) -> list[_EvidenceRef]:
    if "evidence_refs" in unit:
        raw_refs = unit.get("evidence_refs")
    elif "representative_chunks" in unit:
        raw_refs = unit.get("representative_chunks")
        diagnostics["legacy_ref_fields_used"] += 1
    elif "representative_doc_ids" in unit:
        raw_refs = unit.get("representative_doc_ids")
        diagnostics["legacy_ref_fields_used"] += 1
    else:
        raw_refs = []
    if not isinstance(raw_refs, list):
        diagnostics["invalid_evidence_refs"] += 1
        return []
    refs: list[_EvidenceRef] = []
    for raw_ref in raw_refs:
        ref = _coerce_evidence_ref(raw_ref)
        if ref is None:
            diagnostics["invalid_evidence_refs"] += 1
            continue
        refs.append(ref)
    return refs


def _unit_text(unit: dict[str, Any], *fields: str) -> str:
    for field in fields:
        value = unit.get(field)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _build_unit(
    *,
    row: _PassOutputRow,
    artifact_kind: str,
    unit_index: int,
    raw_unit: dict[str, Any],
    diagnostics: Counter[str],
) -> _ArtifactUnit:
    refs = _unit_evidence_refs(raw_unit, diagnostics=diagnostics)
    unique_ref_pairs = {(ref.doc_id, ref.chunk_index) for ref in refs}
    chunks_by_doc: dict[int, set[int]] = defaultdict(set)
    for doc_id, chunk_index in unique_ref_pairs:
        chunks_by_doc[doc_id].add(chunk_index)
    same_doc_multi_chunk_doc_ids = tuple(
        sorted(doc_id for doc_id, chunks in chunks_by_doc.items() if len(chunks) > 1)
    )
    return _ArtifactUnit(
        database=row.database,
        scope=row.scope,
        artifact_kind=artifact_kind,
        pass_output_id=row.pass_output_id,
        granularity=row.granularity,
        period_start=row.period_start,
        period_end=row.period_end,
        unit_index=unit_index,
        title=_unit_text(raw_unit, "title", "name") or f"{artifact_kind} {unit_index}",
        content=_unit_text(raw_unit, "content_md", "description", "summary"),
        evidence_refs_total=len(refs),
        exact_duplicate_refs=len(refs) - len(unique_ref_pairs),
        distinct_doc_ids=tuple(sorted(chunks_by_doc)),
        same_doc_multi_chunk_doc_ids=same_doc_multi_chunk_doc_ids,
        same_doc_multi_chunk_extra_refs=sum(
            len(chunks_by_doc[doc_id]) - 1 for doc_id in same_doc_multi_chunk_doc_ids
        ),
        evidence_reasons=tuple(ref.reason for ref in refs if ref.reason),
    )


def _parse_artifact_row(
    *, row: _PassOutputRow, diagnostics: Counter[str]
) -> tuple[str, bool, list[_ArtifactUnit], _ArtifactRecord | None]:
    artifact_kind = _PASS_KIND_TO_ARTIFACT[row.pass_kind]
    try:
        payload = json.loads(row.payload_json)
    except TypeError, json.JSONDecodeError:
        diagnostics["malformed_payloads"] += 1
        return artifact_kind, False, [], None
    if not isinstance(payload, dict):
        diagnostics["non_object_payloads"] += 1
        return artifact_kind, False, [], None
    raw_units = payload.get(_UNIT_FIELD[artifact_kind])
    if not isinstance(raw_units, list):
        diagnostics["missing_units_list"] += 1
        return artifact_kind, True, [], None
    if row.status == "suppressed":
        diagnostics["suppressed_units_ignored"] += len(raw_units)
        return artifact_kind, True, [], None
    units: list[_ArtifactUnit] = []
    for unit_index, raw_unit in enumerate(raw_units, start=1):
        if not isinstance(raw_unit, dict):
            diagnostics["skipped_non_object_units"] += 1
            continue
        units.append(
            _build_unit(
                row=row,
                artifact_kind=artifact_kind,
                unit_index=unit_index,
                raw_unit=raw_unit,
                diagnostics=diagnostics,
            )
        )
    summary_field = "overview_md" if artifact_kind == "trend" else "summary_md"
    record = _ArtifactRecord(
        database=row.database,
        scope=row.scope,
        artifact_kind=artifact_kind,
        pass_output_id=row.pass_output_id,
        granularity=row.granularity,
        period_start=row.period_start,
        period_end=row.period_end,
        title=_unit_text(payload, "title"),
        summary=_unit_text(payload, summary_field),
    )
    return artifact_kind, True, units, record


def _ratio(numerator: int, denominator: int) -> float:
    return round(numerator / denominator, 6) if denominator else 0.0


def _support_summary(units: Sequence[_ArtifactUnit]) -> dict[str, Any]:
    support_counts = [len(unit.distinct_doc_ids) for unit in units]
    total = len(units)
    zero = sum(count == 0 for count in support_counts)
    single = sum(count == 1 for count in support_counts)
    multi = sum(count >= 2 for count in support_counts)
    multi_chunk_units = sum(bool(unit.same_doc_multi_chunk_doc_ids) for unit in units)
    histogram = Counter(support_counts)
    return {
        "units_total": total,
        "zero_source_units": zero,
        "single_source_units": single,
        "multi_source_units": multi,
        "zero_source_ratio": _ratio(zero, total),
        "single_source_ratio": _ratio(single, total),
        "multi_source_ratio": _ratio(multi, total),
        "mean_distinct_doc_support": (
            round(sum(support_counts) / total, 6) if total else 0.0
        ),
        "min_distinct_doc_support": min(support_counts, default=0),
        "max_distinct_doc_support": max(support_counts, default=0),
        "distinct_doc_support_histogram": {
            str(count): histogram[count] for count in sorted(histogram)
        },
        "evidence_refs_total": sum(unit.evidence_refs_total for unit in units),
        "exact_duplicate_refs_total": sum(unit.exact_duplicate_refs for unit in units),
        "same_doc_multi_chunk_units": multi_chunk_units,
        "same_doc_multi_chunk_unit_ratio": _ratio(multi_chunk_units, total),
        "same_doc_multi_chunk_extra_refs_total": sum(
            unit.same_doc_multi_chunk_extra_refs for unit in units
        ),
    }


def _repeated_support_sets(units: Sequence[_ArtifactUnit]) -> list[dict[str, Any]]:
    grouped: dict[tuple[int, tuple[int, ...]], list[_ArtifactUnit]] = defaultdict(list)
    for unit in units:
        if unit.distinct_doc_ids:
            grouped[(unit.pass_output_id, unit.distinct_doc_ids)].append(unit)
    candidates: list[dict[str, Any]] = []
    for (pass_output_id, doc_ids), matches in grouped.items():
        if len(matches) < 2:
            continue
        first = matches[0]
        candidates.append(
            {
                "artifact_kind": first.artifact_kind,
                "pass_output_id": pass_output_id,
                "granularity": first.granularity,
                "period_start": first.period_start,
                "distinct_doc_ids": list(doc_ids),
                "unit_ids": [match.unit_id for match in matches],
                "unit_titles": [match.title for match in matches],
            }
        )
    return sorted(
        candidates,
        key=lambda candidate: (
            candidate["artifact_kind"],
            candidate["period_start"],
            candidate["pass_output_id"],
            candidate["distinct_doc_ids"],
        ),
    )


def _lexical_features(text: str, *, shingle_size: int) -> set[tuple[str, ...]]:
    normalized = _MARKDOWN_LINK_RE.sub(r"\1", str(text or "")).casefold()
    tokens = _TOKEN_RE.findall(normalized)
    if not tokens:
        return set()
    if len(tokens) < shingle_size:
        return {(token,) for token in tokens}
    return {
        tuple(tokens[index : index + shingle_size])
        for index in range(len(tokens) - shingle_size + 1)
    }


def _dice_similarity(left: str, right: str, *, shingle_size: int) -> float:
    left_features = _lexical_features(left, shingle_size=shingle_size)
    right_features = _lexical_features(right, shingle_size=shingle_size)
    if not left_features or not right_features:
        return 0.0
    return round(
        2
        * len(left_features & right_features)
        / (len(left_features) + len(right_features)),
        6,
    )


def _parse_datetime(value: str) -> datetime | None:
    normalized = str(value or "").strip()
    if not normalized:
        return None
    try:
        parsed = datetime.fromisoformat(normalized.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _excerpt(value: str, *, limit: int = 280) -> str:
    normalized = " ".join(str(value or "").split())
    return normalized if len(normalized) <= limit else normalized[: limit - 1] + "…"


def _parsed_unit_period(
    unit: _ArtifactUnit,
) -> tuple[_ArtifactUnit, datetime, datetime] | None:
    period_start = _parse_datetime(unit.period_start)
    period_end = _parse_datetime(unit.period_end)
    if period_start is None or period_end is None:
        return None
    return unit, period_start, period_end


def _near_duplicate_candidate(
    *, week_unit: _ArtifactUnit, day_unit: _ArtifactUnit, threshold: float
) -> dict[str, Any] | None:
    title_score = _dice_similarity(week_unit.title, day_unit.title, shingle_size=1)
    content_score = _dice_similarity(
        week_unit.content,
        day_unit.content,
        shingle_size=_LEXICAL_SHINGLE_SIZE,
    )
    score = max(title_score, content_score)
    if score < threshold:
        return None
    return {
        "score": score,
        "title_score": title_score,
        "content_score": content_score,
        "week_unit_id": week_unit.unit_id,
        "week_title": week_unit.title,
        "week_content_excerpt": _excerpt(week_unit.content),
        "week_period_start": week_unit.period_start,
        "day_unit_id": day_unit.unit_id,
        "day_title": day_unit.title,
        "day_content_excerpt": _excerpt(day_unit.content),
        "day_period_start": day_unit.period_start,
    }


def _units_with_period(
    units: Sequence[_ArtifactUnit], *, granularity: str
) -> list[tuple[_ArtifactUnit, datetime, datetime]]:
    parsed: list[tuple[_ArtifactUnit, datetime, datetime]] = []
    for unit in units:
        period = _parsed_unit_period(unit)
        if unit.granularity == granularity and period is not None:
            parsed.append(period)
    return parsed


def _weekly_day_near_duplicates(
    units: Sequence[_ArtifactUnit], *, threshold: float
) -> tuple[int, list[dict[str, Any]]]:
    weekly = _units_with_period(units, granularity="week")
    daily = _units_with_period(units, granularity="day")
    pairs_compared = 0
    candidates: list[dict[str, Any]] = []
    for week_unit, week_start, week_end in weekly:
        for day_unit, day_start, day_end in daily:
            if day_start < week_start or day_end > week_end:
                continue
            pairs_compared += 1
            candidate = _near_duplicate_candidate(
                week_unit=week_unit,
                day_unit=day_unit,
                threshold=threshold,
            )
            if candidate is not None:
                candidates.append(candidate)
    candidates.sort(
        key=lambda candidate: (
            -candidate["score"],
            candidate["week_unit_id"],
            candidate["day_unit_id"],
        )
    )
    return pairs_compared, candidates


def _tokens(value: str) -> list[str]:
    normalized = _MARKDOWN_LINK_RE.sub(r"\1", str(value or "")).casefold()
    return _TOKEN_RE.findall(normalized)


def _uses_dense_script(tokens: Sequence[str]) -> bool:
    if not tokens:
        return False
    dense_tokens = sum(
        bool(_DENSE_SCRIPT_TOKEN_RE.fullmatch(token)) for token in tokens
    )
    return dense_tokens * 2 >= len(tokens)


def _stem_title_frame_token(token: str) -> str:
    normalized = token.casefold()
    if not normalized.isascii() or not normalized.isalpha():
        return normalized
    if normalized.endswith("ing") and len(normalized) > 5:
        normalized = normalized[:-3]
    elif normalized.endswith("ed") and len(normalized) > 4:
        normalized = normalized[:-2]
    elif normalized.endswith("s") and len(normalized) > 4:
        normalized = normalized[:-1]
    if normalized.endswith("e") and len(normalized) > 3:
        normalized = normalized[:-1]
    return normalized


def _title_frame(value: str) -> str:
    tokens = _tokens(value)
    if _uses_dense_script(tokens):
        return "".join(tokens[:_TITLE_FRAME_DENSE_TOKENS])
    return " ".join(
        _stem_title_frame_token(token)
        for token in tokens[:_TITLE_FRAME_LATIN_TOKENS]
    )


def _opening_ngram(value: str) -> str:
    tokens = _tokens(value)
    if _uses_dense_script(tokens):
        return "".join(tokens[:_OPENING_DENSE_TOKENS])
    return " ".join(tokens[:_OPENING_LATIN_TOKENS])


def _record_sort_key(record: _ArtifactRecord) -> tuple[datetime, str, int]:
    period = _parse_datetime(record.period_start)
    return (
        period or datetime.max.replace(tzinfo=UTC),
        record.period_start,
        record.pass_output_id,
    )


def _adjacent_signature_repetition(
    records: Sequence[_ArtifactRecord],
    *,
    value_name: str,
    signature_name: str,
) -> dict[str, Any]:
    grouped: dict[tuple[str, str], list[_ArtifactRecord]] = defaultdict(list)
    for record in records:
        grouped[(record.artifact_kind, record.granularity)].append(record)
    compared = 0
    candidates: list[dict[str, Any]] = []
    for (artifact_kind, granularity), series in sorted(grouped.items()):
        ordered = sorted(series, key=_record_sort_key)
        for previous, current in zip(ordered, ordered[1:], strict=False):
            previous_value = str(getattr(previous, value_name) or "")
            current_value = str(getattr(current, value_name) or "")
            previous_signature = (
                _title_frame(previous_value)
                if signature_name == "frame"
                else _opening_ngram(previous_value)
            )
            current_signature = (
                _title_frame(current_value)
                if signature_name == "frame"
                else _opening_ngram(current_value)
            )
            if not previous_signature or not current_signature:
                continue
            compared += 1
            if previous_signature != current_signature:
                continue
            candidates.append(
                {
                    "artifact_kind": artifact_kind,
                    "granularity": granularity,
                    signature_name: current_signature,
                    "previous_pass_output_id": previous.pass_output_id,
                    "previous_period_start": previous.period_start,
                    "previous_value": _excerpt(previous_value),
                    "current_pass_output_id": current.pass_output_id,
                    "current_period_start": current.period_start,
                    "current_value": _excerpt(current_value),
                }
            )
    return {
        "adjacent_pairs_compared": compared,
        "repeated_pairs": len(candidates),
        "repeated_pair_ratio": _ratio(len(candidates), compared),
        "candidates": candidates[:_SERIES_CANDIDATE_LIMIT],
    }


def _boilerplate_features(value: str) -> set[tuple[str, ...]]:
    tokens = _tokens(value)
    size = (
        _BOILERPLATE_DENSE_TOKENS
        if _uses_dense_script(tokens)
        else _BOILERPLATE_LATIN_TOKENS
    )
    if len(tokens) < size:
        return set()
    return {
        tuple(tokens[index : index + size])
        for index in range(len(tokens) - size + 1)
    }


def _render_phrase(tokens: tuple[str, ...]) -> str:
    return "".join(tokens) if _uses_dense_script(tokens) else " ".join(tokens)


def _boilerplate_report(units: Sequence[_ArtifactUnit]) -> dict[str, Any]:
    feature_units: dict[
        tuple[str, str, tuple[str, ...]], list[_ArtifactUnit]
    ] = defaultdict(list)
    for unit in units:
        for feature in _boilerplate_features(unit.content):
            feature_units[(unit.artifact_kind, unit.granularity, feature)].append(
                unit
            )
    candidates: list[dict[str, Any]] = []
    units_with_shared_phrases: set[str] = set()
    for (artifact_kind, granularity, feature), matches in feature_units.items():
        pass_output_ids = {match.pass_output_id for match in matches}
        if len(pass_output_ids) < 2:
            continue
        unit_ids = sorted({match.unit_id for match in matches})
        units_with_shared_phrases.update(unit_ids)
        candidates.append(
            {
                "phrase": _render_phrase(feature),
                "artifact_kind": artifact_kind,
                "granularity": granularity,
                "pass_outputs_total": len(pass_output_ids),
                "units_total": len(unit_ids),
                "unit_ids": unit_ids,
            }
        )
    candidates.sort(
        key=lambda candidate: (
            -candidate["pass_outputs_total"],
            -candidate["units_total"],
            candidate["artifact_kind"],
            candidate["phrase"],
        )
    )
    return {
        "units_total": len(units),
        "units_with_shared_phrases": len(units_with_shared_phrases),
        "unit_ratio": _ratio(len(units_with_shared_phrases), len(units)),
        "candidate_phrases_total": len(candidates),
        "candidates": candidates[:_SERIES_CANDIDATE_LIMIT],
    }


def _summary_overlap_report(
    records: Sequence[_ArtifactRecord], units: Sequence[_ArtifactUnit]
) -> dict[str, Any]:
    units_by_output: dict[tuple[str, int], list[_ArtifactUnit]] = defaultdict(list)
    for unit in units:
        units_by_output[(unit.artifact_kind, unit.pass_output_id)].append(unit)
    candidates: list[dict[str, Any]] = []
    for record in records:
        if not record.summary:
            continue
        matches = units_by_output.get((record.artifact_kind, record.pass_output_id), [])
        if not matches:
            continue
        scored = [
            (
                _dice_similarity(
                    record.summary,
                    unit.content,
                    shingle_size=_LEXICAL_SHINGLE_SIZE,
                ),
                unit,
            )
            for unit in matches
        ]
        score, closest = max(scored, key=lambda item: (item[0], item[1].unit_id))
        candidates.append(
            {
                "score": score,
                "artifact_kind": record.artifact_kind,
                "pass_output_id": record.pass_output_id,
                "granularity": record.granularity,
                "period_start": record.period_start,
                "title": record.title,
                "closest_unit_id": closest.unit_id,
                "closest_unit_title": closest.title,
                "summary_excerpt": _excerpt(record.summary),
                "unit_excerpt": _excerpt(closest.content),
            }
        )
    candidates.sort(
        key=lambda candidate: (
            -candidate["score"],
            candidate["artifact_kind"],
            candidate["period_start"],
            candidate["pass_output_id"],
        )
    )
    scores = [float(candidate["score"]) for candidate in candidates]
    return {
        "artifacts_compared": len(candidates),
        "mean_max_unit_overlap": round(sum(scores) / len(scores), 6) if scores else 0.0,
        "max_unit_overlap": max(scores, default=0.0),
        "candidates": candidates[:_SERIES_CANDIDATE_LIMIT],
    }


def _evidence_reason_is_generic(reason: str) -> bool:
    normalized = " ".join(str(reason or "").split()).strip()
    if not normalized or re.search(r"\d", normalized):
        return False
    if _GENERIC_REASON_ZH_RE.fullmatch(normalized):
        return True
    words = re.findall(r"[a-z]+", normalized.casefold())
    return bool(words) and all(word in _GENERIC_REASON_WORDS for word in words)


def _generic_source_annotations_report(
    units: Sequence[_ArtifactUnit],
) -> dict[str, Any]:
    annotations: list[tuple[_ArtifactUnit, str]] = [
        (unit, reason)
        for unit in units
        for reason in unit.evidence_reasons
        if reason
    ]
    generic = [
        {
            "unit_id": unit.unit_id,
            "artifact_kind": unit.artifact_kind,
            "pass_output_id": unit.pass_output_id,
            "period_start": unit.period_start,
            "unit_title": unit.title,
            "reason": reason,
        }
        for unit, reason in annotations
        if _evidence_reason_is_generic(reason)
    ]
    return {
        "annotations_total": len(annotations),
        "generic_annotations": len(generic),
        "generic_annotation_ratio": _ratio(len(generic), len(annotations)),
        "candidates": generic[:_SERIES_CANDIDATE_LIMIT],
    }


def _series_quality_report(
    *, records: Sequence[_ArtifactRecord], units: Sequence[_ArtifactUnit]
) -> dict[str, Any]:
    return {
        "title_frame_repetition": _adjacent_signature_repetition(
            records,
            value_name="title",
            signature_name="frame",
        ),
        "opening_repetition": _adjacent_signature_repetition(
            records,
            value_name="summary",
            signature_name="opening_ngram",
        ),
        "boilerplate": _boilerplate_report(units),
        "summary_overlap": _summary_overlap_report(records, units),
        "generic_source_annotations": _generic_source_annotations_report(units),
    }


def _evaluate_group(
    *,
    database: str,
    scope: str,
    rows: Sequence[_PassOutputRow],
    diagnostics: Counter[str],
    near_duplicate_threshold: float,
) -> _GroupEvaluation:
    trend_units: list[_ArtifactUnit] = []
    idea_units: list[_ArtifactUnit] = []
    records: list[_ArtifactRecord] = []
    artifact_counts = Counter(
        {
            "trend_payloads": 0,
            "idea_payloads": 0,
            "valid_trend_payloads": 0,
            "valid_idea_payloads": 0,
        }
    )
    for row in rows:
        artifact_kind, valid_payload, units, record = _parse_artifact_row(
            row=row, diagnostics=diagnostics
        )
        artifact_counts[f"{artifact_kind}_payloads"] += 1
        if valid_payload:
            artifact_counts[f"valid_{artifact_kind}_payloads"] += 1
        if artifact_kind == "trend":
            trend_units.extend(units)
        else:
            idea_units.extend(units)
        if record is not None:
            records.append(record)

    all_units = [*trend_units, *idea_units]
    repeated = _repeated_support_sets(all_units)
    repeated_units = sum(len(candidate["unit_ids"]) for candidate in repeated)
    pairs_compared, near_duplicates = _weekly_day_near_duplicates(
        idea_units, threshold=near_duplicate_threshold
    )
    report = {
        "database": database,
        "scope": scope,
        "artifact_counts": {
            name: artifact_counts[name]
            for name in (
                "idea_payloads",
                "trend_payloads",
                "valid_idea_payloads",
                "valid_trend_payloads",
            )
        },
        "row_diagnostics": dict(sorted(diagnostics.items())),
        "trend_support": _support_summary(trend_units),
        "idea_support": _support_summary(idea_units),
        "support_set_repetition": {
            "groups_total": len(repeated),
            "units_total": repeated_units,
            "unit_ratio": _ratio(repeated_units, len(all_units)),
        },
        "repeated_support_sets": repeated,
        "weekly_day_near_duplicate_pairs_compared": pairs_compared,
        "weekly_day_near_duplicate_candidates": near_duplicates,
        "series_quality": _series_quality_report(
            records=records,
            units=all_units,
        ),
        "trend_units": [unit.report_dict() for unit in trend_units],
        "idea_units": [unit.report_dict() for unit in idea_units],
    }
    return _GroupEvaluation(
        report=report,
        trend_units=trend_units,
        idea_units=idea_units,
        records=records,
    )


def _sum_named_values(
    groups: Sequence[_GroupEvaluation], *, section: str
) -> dict[str, int]:
    totals: Counter[str] = Counter()
    for group in groups:
        for name, value in group.report[section].items():
            if isinstance(value, int):
                totals[name] += value
    return dict(sorted(totals.items()))


def _aggregate_series_quality(groups: Sequence[_GroupEvaluation]) -> dict[str, Any]:
    title_pairs = sum(
        group.report["series_quality"]["title_frame_repetition"][
            "adjacent_pairs_compared"
        ]
        for group in groups
    )
    title_repeated = sum(
        group.report["series_quality"]["title_frame_repetition"]["repeated_pairs"]
        for group in groups
    )
    opening_pairs = sum(
        group.report["series_quality"]["opening_repetition"][
            "adjacent_pairs_compared"
        ]
        for group in groups
    )
    opening_repeated = sum(
        group.report["series_quality"]["opening_repetition"]["repeated_pairs"]
        for group in groups
    )
    boilerplate_units = sum(
        group.report["series_quality"]["boilerplate"]["units_total"]
        for group in groups
    )
    boilerplate_shared = sum(
        group.report["series_quality"]["boilerplate"][
            "units_with_shared_phrases"
        ]
        for group in groups
    )
    overlap_compared = sum(
        group.report["series_quality"]["summary_overlap"]["artifacts_compared"]
        for group in groups
    )
    overlap_weighted_sum = sum(
        group.report["series_quality"]["summary_overlap"][
            "mean_max_unit_overlap"
        ]
        * group.report["series_quality"]["summary_overlap"]["artifacts_compared"]
        for group in groups
    )
    annotations_total = sum(
        group.report["series_quality"]["generic_source_annotations"][
            "annotations_total"
        ]
        for group in groups
    )
    generic_annotations = sum(
        group.report["series_quality"]["generic_source_annotations"][
            "generic_annotations"
        ]
        for group in groups
    )
    return {
        "title_frame_adjacent_pairs_compared": title_pairs,
        "title_frame_repeated_pairs": title_repeated,
        "title_frame_repeated_pair_ratio": _ratio(title_repeated, title_pairs),
        "opening_adjacent_pairs_compared": opening_pairs,
        "opening_repeated_pairs": opening_repeated,
        "opening_repeated_pair_ratio": _ratio(opening_repeated, opening_pairs),
        "boilerplate_units_total": boilerplate_units,
        "boilerplate_units_with_shared_phrases": boilerplate_shared,
        "boilerplate_unit_ratio": _ratio(boilerplate_shared, boilerplate_units),
        "summary_overlap_artifacts_compared": overlap_compared,
        "summary_overlap_mean_max_unit_overlap": (
            round(overlap_weighted_sum / overlap_compared, 6)
            if overlap_compared
            else 0.0
        ),
        "summary_overlap_max_unit_overlap": max(
            (
                group.report["series_quality"]["summary_overlap"][
                    "max_unit_overlap"
                ]
                for group in groups
            ),
            default=0.0,
        ),
        "source_annotations_total": annotations_total,
        "generic_source_annotations": generic_annotations,
        "generic_source_annotation_ratio": _ratio(
            generic_annotations, annotations_total
        ),
    }


def _aggregate_report(
    *, databases_total: int, groups: Sequence[_GroupEvaluation]
) -> dict[str, Any]:
    trend_units = [unit for group in groups for unit in group.trend_units]
    idea_units = [unit for group in groups for unit in group.idea_units]
    row_diagnostics = _sum_named_values(groups, section="row_diagnostics")
    artifact_counts = _sum_named_values(groups, section="artifact_counts")
    repeated_groups = sum(
        group.report["support_set_repetition"]["groups_total"] for group in groups
    )
    repeated_units = sum(
        group.report["support_set_repetition"]["units_total"] for group in groups
    )
    all_units_total = len(trend_units) + len(idea_units)
    return {
        "databases_total": databases_total,
        "groups_total": len(groups),
        "canonical_pass_outputs": row_diagnostics.get("canonical_pass_outputs", 0),
        "artifact_counts": artifact_counts,
        "row_diagnostics": row_diagnostics,
        "trend_support": _support_summary(trend_units),
        "idea_support": _support_summary(idea_units),
        "support_set_repetition": {
            "groups_total": repeated_groups,
            "units_total": repeated_units,
            "unit_ratio": _ratio(repeated_units, all_units_total),
        },
        "weekly_day_near_duplicate_pairs_compared": sum(
            group.report["weekly_day_near_duplicate_pairs_compared"] for group in groups
        ),
        "weekly_day_near_duplicate_candidates_total": sum(
            len(group.report["weekly_day_near_duplicate_candidates"])
            for group in groups
        ),
        "series_quality": _aggregate_series_quality(groups),
    }


def evaluate_databases(
    *,
    db_paths: Sequence[Path],
    near_duplicate_threshold: float = _DEFAULT_NEAR_DUPLICATE_THRESHOLD,
) -> dict[str, Any]:
    threshold = float(near_duplicate_threshold)
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("near_duplicate_threshold must be between 0 and 1")
    resolved_paths = list(
        dict.fromkeys(str(path.expanduser().resolve()) for path in db_paths)
    )
    if not resolved_paths:
        raise ValueError("at least one database is required")

    evaluations: list[_GroupEvaluation] = []
    for database in resolved_paths:
        records_by_scope, diagnostics_by_scope = _read_database(Path(database))
        scopes = sorted(set(records_by_scope) | set(diagnostics_by_scope))
        for scope in scopes:
            evaluations.append(
                _evaluate_group(
                    database=database,
                    scope=scope,
                    rows=records_by_scope.get(scope, []),
                    diagnostics=diagnostics_by_scope.get(scope, _empty_diagnostics()),
                    near_duplicate_threshold=threshold,
                )
            )

    return {
        "schema_version": 2,
        "inputs": resolved_paths,
        "methodology": {
            "canonical_selection": (
                "Latest succeeded or suppressed pass_output per database, scope, "
                "pass_kind, granularity, period_start, and period_end. Newer eligible "
                "terminal rows supersede reruns; failed, started, and unknown statuses "
                "are filtered before selection and cannot shadow an older terminal row."
            ),
            "status_semantics": {
                "canonical_terminal_statuses": sorted(_CANONICAL_TERMINAL_STATUSES),
                "suppressed_artifact": (
                    "A suppressed row contributes one valid canonical payload and zero "
                    "artifact units, even if its stored units list is unexpectedly non-empty."
                ),
                "filtered_statuses": (
                    "Every status other than succeeded or suppressed is ineligible for "
                    "canonical selection."
                ),
                "compatibility_diagnostic": (
                    "non_succeeded_filtered is retained as an alias of "
                    "non_terminal_filtered; suppressed rows are not filtered."
                ),
            },
            "source_unit": (
                "A source is one distinct positive doc_id. Multiple chunks from the "
                "same document never increase source breadth."
            ),
            "support_set_repetition": (
                "Exact repeated non-empty doc_id sets among units in the same canonical "
                "artifact. It measures evidence reuse, not prose duplication."
            ),
            "weekly_day_near_duplicate_proxy": {
                "threshold": threshold,
                "method": (
                    "Maximum of title token-set Sørensen-Dice similarity and body "
                    "Sørensen-Dice similarity over deterministic "
                    f"{_LEXICAL_SHINGLE_SIZE}-token lexical shingles."
                ),
                "limitation": (
                    "Candidate generator only: lexical overlap is neither a semantic "
                    "duplicate judgment nor evidence that two ideas are equivalent."
                ),
                "window_mapping": (
                    "A day idea is compared only when its full period lies inside the "
                    "weekly idea period in the same database and scope."
                ),
            },
            "series_quality_signals": {
                "title_frame_repetition": (
                    "Compares the normalized leading frame of adjacent canonical titles "
                    "within each artifact kind and granularity. English inflection is "
                    "lightly normalized; dense-script titles use their leading characters."
                ),
                "opening_repetition": (
                    "Compares the first five Latin-script tokens or eight dense-script "
                    "characters of adjacent canonical summaries."
                ),
                "boilerplate": (
                    "Reports five-token Latin-script or eight-character dense-script "
                    "phrases shared by units from at least two canonical pass outputs "
                    "of the same artifact kind and granularity."
                ),
                "summary_overlap": (
                    "Reports the maximum lexical shingle overlap between each artifact "
                    "summary and one of its own units."
                ),
                "generic_source_annotations": (
                    "Reports evidence reasons made only from a small generic source-action "
                    "vocabulary, plus exact generic Chinese forms. Reasons with numbers are "
                    "not classified as generic."
                ),
                "interpretation": (
                    "These are review signals, not publication gates. Candidate limits "
                    "bound report size and do not turn a proxy into a quality judgment."
                ),
            },
        },
        "groups": [evaluation.report for evaluation in evaluations],
        "aggregate": _aggregate_report(
            databases_total=len(resolved_paths), groups=evaluations
        ),
    }


def render_summary(report: dict[str, Any], *, output_path: Path | None) -> str:
    aggregate = report["aggregate"]
    artifact_counts = aggregate["artifact_counts"]
    trend = aggregate["trend_support"]
    ideas = aggregate["idea_support"]
    series = aggregate["series_quality"]
    lines = [
        "Artifact quality audit",
        (
            f"Databases: {aggregate['databases_total']} | "
            f"scopes: {aggregate['groups_total']} | "
            f"canonical outputs: {aggregate['canonical_pass_outputs']}"
        ),
        (
            "Canonical status: "
            f"{aggregate['row_diagnostics'].get('canonical_succeeded_outputs', 0)} "
            "succeeded | "
            f"{aggregate['row_diagnostics'].get('canonical_suppressed_outputs', 0)} "
            "suppressed | "
            f"{aggregate['row_diagnostics'].get('non_terminal_filtered', 0)} "
            "ineligible filtered"
        ),
        (
            f"Trends: {artifact_counts.get('trend_payloads', 0)} payloads / "
            f"{trend['units_total']} clusters | multi-source "
            f"{trend['multi_source_ratio']:.1%} | single-source "
            f"{trend['single_source_ratio']:.1%}"
        ),
        (
            f"Ideas: {artifact_counts.get('idea_payloads', 0)} payloads / "
            f"{ideas['units_total']} ideas | multi-source "
            f"{ideas['multi_source_ratio']:.1%} | single-source "
            f"{ideas['single_source_ratio']:.1%}"
        ),
        (
            "Weekly/day lexical near-duplicate candidates: "
            f"{aggregate['weekly_day_near_duplicate_candidates_total']} / "
            f"{aggregate['weekly_day_near_duplicate_pairs_compared']} compared"
        ),
        (
            "Series repetition: title frames "
            f"{series['title_frame_repeated_pairs']} / "
            f"{series['title_frame_adjacent_pairs_compared']} adjacent | openings "
            f"{series['opening_repeated_pairs']} / "
            f"{series['opening_adjacent_pairs_compared']} adjacent | shared-phrase units "
            f"{series['boilerplate_units_with_shared_phrases']} / "
            f"{series['boilerplate_units_total']}"
        ),
        (
            "Source annotations: generic "
            f"{series['generic_source_annotations']} / "
            f"{series['source_annotations_total']}"
        ),
    ]
    if output_path is not None:
        lines.append(f"JSON: {output_path.expanduser().resolve()}")
    return "\n".join(lines) + "\n"


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Measure structural evidence and series-level writing quality in canonical "
            "Recoleta Trend and Idea pass outputs without model calls."
        )
    )
    parser.add_argument(
        "--db",
        action="append",
        required=True,
        type=Path,
        help="Recoleta SQLite database. Repeat to aggregate multiple databases.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional JSON report path. Without it, the full report is printed.",
    )
    parser.add_argument(
        "--near-duplicate-threshold",
        type=float,
        default=_DEFAULT_NEAR_DUPLICATE_THRESHOLD,
        help="Lexical weekly/day Idea candidate threshold in [0, 1].",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    try:
        report = evaluate_databases(
            db_paths=args.db,
            near_duplicate_threshold=args.near_duplicate_threshold,
        )
    except ValueError as exc:
        parser.error(str(exc))
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    output_path: Path | None = args.output
    if output_path is None:
        print(serialized, end="")
        return 0
    resolved_output = output_path.expanduser().resolve()
    resolved_output.parent.mkdir(parents=True, exist_ok=True)
    resolved_output.write_text(serialized, encoding="utf-8")
    print(render_summary(report, output_path=resolved_output), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
