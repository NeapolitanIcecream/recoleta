from __future__ import annotations

import json
from pathlib import Path
import sqlite3

from scripts import eval_artifact_quality as quality


def _create_db(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        create table runs (
            id text primary key,
            scope text
        );
        create table pass_outputs (
            id integer primary key,
            run_id text not null,
            pass_kind text not null,
            status text not null,
            granularity text,
            period_start text,
            period_end text,
            schema_version integer not null default 1,
            payload_json text not null,
            created_at text not null
        );
        """
    )
    connection.execute("insert into runs(id, scope) values ('run-1', 'radar-a')")
    return connection


def _insert_output(
    connection: sqlite3.Connection,
    *,
    row_id: int,
    pass_kind: str,
    granularity: str,
    period_start: str,
    period_end: str,
    payload: object,
    status: str = "succeeded",
) -> None:
    payload_json = payload if isinstance(payload, str) else json.dumps(payload)
    connection.execute(
        """
        insert into pass_outputs(
            id, run_id, pass_kind, status, granularity, period_start,
            period_end, payload_json, created_at
        ) values (?, 'run-1', ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            row_id,
            pass_kind,
            status,
            granularity,
            period_start,
            period_end,
            payload_json,
            f"2026-04-20T00:00:{row_id:02d}+00:00",
        ),
    )


def _ref(doc_id: int, chunk_index: int) -> dict[str, int]:
    return {"doc_id": doc_id, "chunk_index": chunk_index}


def test_evaluate_databases_measures_support_without_counting_chunks_as_sources(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "quality.db"
    connection = _create_db(db_path)
    _insert_output(
        connection,
        row_id=1,
        pass_kind="trend_synthesis",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={"clusters": [{"title": "superseded", "evidence_refs": []}]},
    )
    _insert_output(
        connection,
        row_id=2,
        pass_kind="trend_synthesis",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={
            "clusters": [
                {
                    "title": "Execution evidence",
                    "content_md": "Two papers support this cluster.",
                    "evidence_refs": [_ref(10, 0), _ref(10, 1), _ref(20, 0)],
                },
                {
                    "title": "Runtime controls",
                    "content_md": "The same two papers support this cluster.",
                    "evidence_refs": [_ref(10, 0), _ref(20, 0)],
                },
            ]
        },
    )
    _insert_output(
        connection,
        row_id=3,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={
            "ideas": [
                {
                    "title": "Executable acceptance record",
                    "content_md": "Build an executable acceptance record for every edit.",
                    "evidence_refs": [_ref(30, 0), _ref(30, 1)],
                }
            ]
        },
    )
    _insert_output(
        connection,
        row_id=4,
        pass_kind="trend_ideas",
        granularity="week",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-13T00:00:00+00:00",
        payload={
            "ideas": [
                {
                    "title": "Executable acceptance record",
                    "content_md": "Build an executable acceptance record for every edit.",
                    "evidence_refs": [_ref(30, 0)],
                }
            ]
        },
    )
    _insert_output(
        connection,
        row_id=5,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-07T00:00:00+00:00",
        period_end="2026-04-08T00:00:00+00:00",
        payload={"ideas": []},
        status="failed",
    )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(
        db_paths=[db_path], near_duplicate_threshold=0.8
    )

    group = report["groups"][0]
    assert group["scope"] == "radar-a"
    assert group["artifact_counts"] == {
        "idea_payloads": 2,
        "trend_payloads": 1,
        "valid_idea_payloads": 2,
        "valid_trend_payloads": 1,
    }
    assert group["row_diagnostics"]["non_succeeded_filtered"] == 1
    assert group["row_diagnostics"]["superseded_succeeded_outputs"] == 1

    first_cluster = group["trend_units"][0]
    assert first_cluster["distinct_doc_ids"] == [10, 20]
    assert first_cluster["distinct_doc_support_count"] == 2
    assert first_cluster["same_doc_multi_chunk_doc_ids"] == [10]
    assert first_cluster["same_doc_multi_chunk_extra_refs"] == 1
    assert group["trend_support"]["multi_source_units"] == 2
    assert group["trend_support"]["single_source_units"] == 0
    assert group["repeated_support_sets"][0]["distinct_doc_ids"] == [10, 20]

    assert group["idea_support"]["single_source_units"] == 2
    assert group["idea_support"]["multi_source_units"] == 0
    assert group["weekly_day_near_duplicate_pairs_compared"] == 1
    candidates = group["weekly_day_near_duplicate_candidates"]
    assert len(candidates) == 1
    assert candidates[0]["score"] == 1.0
    assert candidates[0]["day_period_start"].startswith("2026-04-06")


def test_evaluate_databases_survives_bad_payloads_and_reads_legacy_trend_refs(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "legacy.db"
    connection = _create_db(db_path)
    _insert_output(
        connection,
        row_id=1,
        pass_kind="trend_synthesis",
        granularity="week",
        period_start="2026-03-02T00:00:00+00:00",
        period_end="2026-03-09T00:00:00+00:00",
        payload={
            "clusters": [
                {
                    "name": "Legacy cluster",
                    "description": "Old payload shape.",
                    "representative_chunks": [
                        {"doc_id": 41, "chunk_index": 0},
                        {"doc_id": 42, "chunk_index": 0},
                    ],
                },
                "not-an-object",
            ]
        },
    )
    _insert_output(
        connection,
        row_id=2,
        pass_kind="trend_ideas",
        granularity="week",
        period_start="2026-03-02T00:00:00+00:00",
        period_end="2026-03-09T00:00:00+00:00",
        payload="{bad json",
    )
    _insert_output(
        connection,
        row_id=3,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-03-03T00:00:00+00:00",
        period_end="2026-03-04T00:00:00+00:00",
        payload={"summary_md": "Old payload without ideas."},
    )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(db_paths=[db_path])

    group = report["groups"][0]
    assert group["artifact_counts"]["trend_payloads"] == 1
    assert group["artifact_counts"]["idea_payloads"] == 2
    assert group["artifact_counts"]["valid_idea_payloads"] == 1
    assert group["trend_units"][0]["distinct_doc_ids"] == [41, 42]
    assert group["row_diagnostics"]["malformed_payloads"] == 1
    assert group["row_diagnostics"]["missing_units_list"] == 1
    assert group["row_diagnostics"]["skipped_non_object_units"] == 1
    assert group["row_diagnostics"]["legacy_ref_fields_used"] == 1


def test_newer_suppressed_output_replaces_older_succeeded_artifact(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "suppressed.db"
    connection = _create_db(db_path)
    _insert_output(
        connection,
        row_id=1,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={
            "ideas": [
                {
                    "title": "Stale idea",
                    "evidence_refs": [_ref(10, 0), _ref(20, 0)],
                }
            ]
        },
    )
    _insert_output(
        connection,
        row_id=2,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={"ideas": []},
        status="suppressed",
    )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(db_paths=[db_path])

    group = report["groups"][0]
    assert group["artifact_counts"]["idea_payloads"] == 1
    assert group["artifact_counts"]["valid_idea_payloads"] == 1
    assert group["idea_support"]["units_total"] == 0
    assert group["row_diagnostics"]["terminal_pass_outputs"] == 2
    assert group["row_diagnostics"]["succeeded_pass_outputs"] == 1
    assert group["row_diagnostics"]["suppressed_pass_outputs"] == 1
    assert group["row_diagnostics"]["canonical_suppressed_outputs"] == 1
    assert group["row_diagnostics"]["superseded_terminal_outputs"] == 1
    assert group["row_diagnostics"]["superseded_succeeded_outputs"] == 1


def test_newer_failed_output_does_not_replace_older_succeeded_artifact(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "failed.db"
    connection = _create_db(db_path)
    _insert_output(
        connection,
        row_id=1,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={
            "ideas": [
                {
                    "title": "Last successful idea",
                    "evidence_refs": [_ref(10, 0), _ref(20, 0)],
                }
            ]
        },
    )
    _insert_output(
        connection,
        row_id=2,
        pass_kind="trend_ideas",
        granularity="day",
        period_start="2026-04-06T00:00:00+00:00",
        period_end="2026-04-07T00:00:00+00:00",
        payload={"ideas": []},
        status="failed",
    )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(db_paths=[db_path])

    group = report["groups"][0]
    assert group["idea_units"][0]["title"] == "Last successful idea"
    assert group["row_diagnostics"]["canonical_succeeded_outputs"] == 1
    assert group["row_diagnostics"]["non_terminal_filtered"] == 1


def test_evaluate_databases_reports_series_level_writing_repetition(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "series-quality.db"
    connection = _create_db(db_path)
    periods = [
        ("2026-04-06T00:00:00+00:00", "2026-04-07T00:00:00+00:00"),
        ("2026-04-07T00:00:00+00:00", "2026-04-08T00:00:00+00:00"),
        ("2026-04-08T00:00:00+00:00", "2026-04-09T00:00:00+00:00"),
    ]
    payloads = [
        {
            "title": "Code agents tighten release gates",
            "overview_md": "Teams using coding agents now require traceable release evidence before rollout.",
            "clusters": [
                {
                    "title": "Release evidence",
                    "content_md": "Teams using coding agents now require traceable release evidence before rollout.",
                    "evidence_refs": [
                        {"doc_id": 10, "chunk_index": 0, "reason": "Shows the point."}
                    ],
                }
            ],
        },
        {
            "title": "Coding agents enter deployment checks",
            "overview_md": "Teams using coding agents now face stricter deployment checks.",
            "clusters": [
                {
                    "title": "Deployment checks",
                    "content_md": "Teams using coding agents now require traceable release evidence before deployment.",
                    "evidence_refs": [
                        {
                            "doc_id": 20,
                            "chunk_index": 0,
                            "reason": "Shows a 23% gain on SWE-bench.",
                        }
                    ],
                }
            ],
        },
        {
            "title": "Runtime controls become auditable",
            "overview_md": "Audit records link tool calls to policy decisions.",
            "clusters": [
                {
                    "title": "Policy records",
                    "content_md": "Signed records preserve each tool decision for review.",
                    "evidence_refs": [],
                }
            ],
        },
    ]
    for row_id, ((period_start, period_end), payload) in enumerate(
        zip(periods, payloads, strict=True), start=1
    ):
        _insert_output(
            connection,
            row_id=row_id,
            pass_kind="trend_synthesis",
            granularity="day",
            period_start=period_start,
            period_end=period_end,
            payload=payload,
        )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(db_paths=[db_path])

    assert report["schema_version"] == 2
    series = report["groups"][0]["series_quality"]
    assert series["title_frame_repetition"]["adjacent_pairs_compared"] == 2
    assert series["title_frame_repetition"]["repeated_pairs"] == 1
    assert series["title_frame_repetition"]["candidates"][0]["frame"] == "cod agent"
    assert series["opening_repetition"]["repeated_pairs"] == 1
    assert series["boilerplate"]["units_with_shared_phrases"] == 2
    assert any(
        candidate["phrase"] == "teams using coding agents now"
        for candidate in series["boilerplate"]["candidates"]
    )
    assert series["summary_overlap"]["artifacts_compared"] == 3
    assert series["summary_overlap"]["candidates"][0]["score"] == 1.0
    assert series["generic_source_annotations"]["annotations_total"] == 2
    assert series["generic_source_annotations"]["generic_annotations"] == 1
    assert report["aggregate"]["series_quality"]["title_frame_repeated_pairs"] == 1


def test_evaluate_databases_treats_japanese_and_korean_as_dense_script(
    tmp_path: Path,
) -> None:
    db_path = tmp_path / "dense-script-quality.db"
    connection = _create_db(db_path)
    cases = [
        (
            "day",
            "2026-04-06T00:00:00+00:00",
            "2026-04-07T00:00:00+00:00",
            "エージェント評価を監査する",
            "評価結果を継続して記録する。",
            "評価結果を記録中",
        ),
        (
            "day",
            "2026-04-07T00:00:00+00:00",
            "2026-04-08T00:00:00+00:00",
            "エージェント評価を記録する",
            "評価結果を継続して比較する。",
            "評価結果を記録中",
        ),
        (
            "week",
            "2026-04-06T00:00:00+00:00",
            "2026-04-13T00:00:00+00:00",
            "에이전트 평가를 기록한다",
            "평가 결과를 지속해서 기록한다.",
            "평가결과를기록함",
        ),
        (
            "week",
            "2026-04-13T00:00:00+00:00",
            "2026-04-20T00:00:00+00:00",
            "에이전트 평가를 비교한다",
            "평가 결과를 지속해서 비교한다.",
            "평가결과를기록함",
        ),
    ]
    for row_id, (
        granularity,
        period_start,
        period_end,
        title,
        overview,
        content,
    ) in enumerate(cases, start=1):
        _insert_output(
            connection,
            row_id=row_id,
            pass_kind="trend_synthesis",
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            payload={
                "title": title,
                "overview_md": overview,
                "clusters": [
                    {
                        "title": title,
                        "content_md": content,
                        "evidence_refs": [],
                    }
                ],
            },
        )
    connection.commit()
    connection.close()

    report = quality.evaluate_databases(db_paths=[db_path])

    series = report["groups"][0]["series_quality"]
    title_frames = {
        candidate["granularity"]: candidate["frame"]
        for candidate in series["title_frame_repetition"]["candidates"]
    }
    openings = {
        candidate["granularity"]: candidate["opening_ngram"]
        for candidate in series["opening_repetition"]["candidates"]
    }
    phrases = {
        candidate["granularity"]: candidate["phrase"]
        for candidate in series["boilerplate"]["candidates"]
    }

    assert title_frames == {"day": "エージェン", "week": "에이전트평"}
    assert openings == {"day": "評価結果を継続し", "week": "평가결과를지속해"}
    assert phrases == {"day": "評価結果を記録中", "week": "평가결과를기록함"}
    assert all(" " not in value for value in [*title_frames.values(), *openings.values(), *phrases.values()])


def test_main_writes_json_report_and_prints_readable_summary(
    tmp_path: Path, capsys
) -> None:
    db_path = tmp_path / "empty.db"
    connection = _create_db(db_path)
    connection.commit()
    connection.close()
    output_path = tmp_path / "report.json"

    exit_code = quality.main(
        ["--db", str(db_path), "--output", str(output_path)]
    )

    assert exit_code == 0
    saved = json.loads(output_path.read_text(encoding="utf-8"))
    assert saved["aggregate"]["canonical_pass_outputs"] == 0
    stdout = capsys.readouterr().out
    assert "Artifact quality audit" in stdout
    assert "Series repetition:" in stdout
    assert str(output_path.resolve()) in stdout
