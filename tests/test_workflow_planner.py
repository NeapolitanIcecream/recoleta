from __future__ import annotations

import json
from datetime import UTC, date, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from recoleta.cli import workflow_planner as workflow_planner_module
from recoleta.cli.workflow_models import STEP_TRANSLATE
from recoleta.cli.workflow_planner import (
    WorkflowPlanningOptions,
    plan_workflow_execution,
)
from recoleta.cli.workflow_runner import GranularityPlanRequest, build_granularity_plan
from recoleta.workflow_freshness import (
    build_trend_ideas_freshness,
    build_trend_synthesis_freshness,
)


class _Policy:
    recursive_lower_levels = True
    delivery_mode = "all"
    translation = "none"
    translate_include = ["items", "trends", "ideas"]
    site_build = False
    on_translate_failure = "partial_success"


class _Settings:
    analyze_limit = 8
    triage_enabled = False
    topics: list[str] = []
    min_relevance_score = 0.0
    llm_model = "gpt-test"
    analyze_llm_model: str | None = None
    trends_llm_model: str | None = None
    ideas_llm_model: str | None = None
    translation_llm_model: str | None = None
    llm_output_language = "English"
    workflows = SimpleNamespace()
    sources = SimpleNamespace(arxiv=SimpleNamespace(enabled=False))
    arxiv_pool = SimpleNamespace(enabled=False)

    def workflow_policy_for_granularity(self, _granularity: str) -> _Policy:
        return _Policy()

    def localization_target_codes(self) -> list[str]:
        return []

    def safe_fingerprint(self) -> str:
        return "fp-test"


class _TranslationPolicy(_Policy):
    translation = "auto"
    translate_include = ["trends", "ideas"]


class _TranslationLocalization:
    source_language_code = "en"
    site_default_language_code = "en"
    targets = [SimpleNamespace(code="zh-cn", llm_label="Chinese")]


class _TranslationSettings(_Settings):
    localization = _TranslationLocalization()

    def workflow_policy_for_granularity(self, _granularity: str) -> _Policy:
        return _TranslationPolicy()

    def localization_target_codes(self) -> list[str]:
        return ["zh-cn"]


class _TriageSettings(_Settings):
    triage_enabled = True
    topics = ["software agents"]


class _ReadOnlyPlannerRepo:
    def __init__(
        self,
        *,
        missing_days: set[date] | None = None,
        missing_trend_windows: set[tuple[str, date]] | None = None,
        missing_idea_windows: set[tuple[str, date]] | None = None,
        untouched_task_sets: set[str] | None = None,
        source_hashes: dict[tuple[str, date], str] | None = None,
        stored_source_hashes: dict[tuple[str, date], str] | None = None,
    ) -> None:
        self.missing_days = set(missing_days or set())
        self.missing_trend_windows = set(missing_trend_windows or set())
        self.missing_idea_windows = set(missing_idea_windows or set())
        self.untouched_task_sets = set(untouched_task_sets or set())
        self.source_hashes = dict(source_hashes or {})
        self.stored_source_hashes = dict(stored_source_hashes or self.source_hashes)
        self.write_calls: list[str] = []

    def list_items_for_llm_analysis(self, **kwargs: Any) -> list[Any]:
        start = kwargs["period_start"].date()
        if start in self.missing_days:
            return [SimpleNamespace(id=1)]
        return []

    def list_items_for_publish(self, **_kwargs: Any) -> list[Any]:
        return []

    def get_latest_pass_output(self, **kwargs: Any) -> Any | None:
        granularity = kwargs["granularity"]
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        if granularity == "day" and period_start.date() in self.missing_days:
            return None
        pass_kind = kwargs["pass_kind"]
        status = kwargs.get("status")
        if pass_kind == "trend_synthesis":
            if granularity in self.untouched_task_sets:
                return None
            if (granularity, period_start.date()) in self.missing_trend_windows:
                return None
            freshness = build_trend_synthesis_freshness(
                settings=_Settings(),
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                repository=_StoredSourceRowsRepo(self),
            )
            return SimpleNamespace(
                id=_stable_pass_output_id(granularity, period_start, pass_kind),
                status=status,
                diagnostics_json=json.dumps({"workflow_freshness": freshness}),
                input_refs_json="[]",
            )
        if pass_kind == "trend_ideas":
            if granularity in self.untouched_task_sets:
                return None
            if (granularity, period_start.date()) in self.missing_idea_windows:
                return None
            upstream_id = _stable_pass_output_id(
                granularity, period_start, "trend_synthesis"
            )
            freshness = build_trend_ideas_freshness(
                settings=_Settings(),
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
                upstream_pass_output_id=upstream_id,
            )
            return SimpleNamespace(
                id=_stable_pass_output_id(granularity, period_start, pass_kind),
                status=status,
                diagnostics_json=json.dumps({"workflow_freshness": freshness}),
                input_refs_json=json.dumps(
                    [
                        {
                            "ref_kind": "pass_output",
                            "pass_kind": "trend_synthesis",
                            "pass_output_id": upstream_id,
                        }
                    ]
                ),
            )
        return None

    def list_documents(self, **kwargs: Any) -> list[Any]:
        doc_type = str(kwargs["doc_type"])
        granularity = kwargs["granularity"]
        period_start = kwargs["period_start"]
        if granularity == "day" and period_start.date() in self.missing_days:
            return []
        if doc_type in {"trend", "idea"} and granularity in self.untouched_task_sets:
            return []
        if doc_type == "trend" and (granularity, period_start.date()) in self.missing_trend_windows:
            return []
        if doc_type == "idea" and (granularity, period_start.date()) in self.missing_idea_windows:
            return []
        return [SimpleNamespace(id=1)]

    def list_document_chunks_in_period(self, **kwargs: Any) -> list[Any]:
        granularity = kwargs["granularity"]
        period_start = kwargs["period_start"]
        doc_type = str(kwargs["doc_type"])
        if granularity == "day" and period_start.date() in self.missing_days:
            return []
        if doc_type in {"trend", "idea"} and granularity in self.untouched_task_sets:
            return []
        if doc_type == "trend" and (granularity, period_start.date()) in self.missing_trend_windows:
            return []
        if doc_type == "idea" and (granularity, period_start.date()) in self.missing_idea_windows:
            return []
        return [SimpleNamespace(id=1)]

    def list_document_chunk_index_rows_in_period(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self._source_rows(
            doc_type=str(kwargs["doc_type"]),
            granularity=kwargs.get("granularity"),
            period_start=kwargs["period_start"],
            period_end=kwargs["period_end"],
            kind=str(kwargs["kind"]),
            stored=False,
        )

    def _source_rows(
        self,
        *,
        doc_type: str,
        granularity: str | None,
        period_start: datetime,
        period_end: datetime,
        kind: str,
        stored: bool,
    ) -> list[dict[str, Any]]:
        source_granularity = granularity or "item"
        if (
            source_granularity == "item"
            and period_start.date() in self.missing_days
        ):
            return []
        hash_map = self.stored_source_hashes if stored else self.source_hashes
        text_hash = hash_map.get(
            (source_granularity, period_start.date()),
            f"{source_granularity}-{period_start.date().isoformat()}-{kind}",
        )
        return [
            {
                "chunk_id": _stable_doc_id(source_granularity, period_start, kind),
                "doc_id": _stable_doc_id(source_granularity, period_start, "doc"),
                "doc_type": doc_type,
                "granularity": granularity,
                "chunk_index": {"summary": 0, "content": 1, "meta": 99}[kind],
                "kind": kind,
                "text_hash": text_hash,
                "event_start_ts": period_start,
                "event_end_ts": period_end,
            }
        ]

    def create_run(self, *_args: Any, **_kwargs: Any) -> None:
        self.write_calls.append("create_run")
        raise AssertionError("planner must not create run rows")

    def create_pass_output(self, *_args: Any, **_kwargs: Any) -> None:
        self.write_calls.append("create_pass_output")
        raise AssertionError("planner must not create pass outputs")

    def record_metric(self, *_args: Any, **_kwargs: Any) -> None:
        self.write_calls.append("record_metric")
        raise AssertionError("planner must not record metrics")


class _StoredSourceRowsRepo:
    def __init__(self, parent: _ReadOnlyPlannerRepo) -> None:
        self.parent = parent

    def list_document_chunk_index_rows_in_period(self, **kwargs: Any) -> list[dict[str, Any]]:
        return self.parent._source_rows(
            doc_type=str(kwargs["doc_type"]),
            granularity=kwargs.get("granularity"),
            period_start=kwargs["period_start"],
            period_end=kwargs["period_end"],
            kind=str(kwargs["kind"]),
            stored=True,
        )


class _NoCurrentAnalysisCandidatesRepo(_ReadOnlyPlannerRepo):
    def list_items_for_llm_analysis(self, **_kwargs: Any) -> list[Any]:
        return []


class _AnalyzeCandidatesRepo(_ReadOnlyPlannerRepo):
    def list_items_for_llm_analysis(self, **_kwargs: Any) -> list[Any]:
        return [SimpleNamespace(id=1)]


class _AnalyzeBudgetReceiptRepo(_AnalyzeCandidatesRepo):
    def __init__(self, *, selected_total: int) -> None:
        super().__init__()
        self.selected_total = selected_total
        self.receipt_requests: list[dict[str, Any]] = []

    def get_latest_workflow_step_receipt(self, **kwargs: Any) -> Any | None:
        self.receipt_requests.append(dict(kwargs))
        if kwargs["step_id"] != "analyze":
            return None
        if kwargs["granularity"] != "day":
            return None
        if str(kwargs.get("config_fingerprint") or "") != "fp-test":
            return None
        if self.selected_total < int(kwargs.get("min_selected_total") or 0):
            return None
        return SimpleNamespace(
            id=1,
            run_id="run-analyze-budget",
            requested_limit=self.selected_total,
            selected_total=self.selected_total,
            processed_total=self.selected_total,
            failed_total=0,
        )

    def count_items_for_llm_analysis_by_state(self, **_kwargs: Any) -> dict[str, int]:
        return {"triaged": 3, "retryable_failed": 1}


class _TranslationPlannerRepo(_ReadOnlyPlannerRepo):
    def __init__(
        self,
        *,
        existing_hashes: dict[tuple[str, int, str], str],
        missing_days: set[date] | None = None,
        missing_trend_windows: set[tuple[str, date]] | None = None,
        missing_idea_windows: set[tuple[str, date]] | None = None,
        untouched_task_sets: set[str] | None = None,
        source_hashes: dict[tuple[str, date], str] | None = None,
        stored_source_hashes: dict[tuple[str, date], str] | None = None,
    ) -> None:
        super().__init__(
            missing_days=missing_days,
            missing_trend_windows=missing_trend_windows,
            missing_idea_windows=missing_idea_windows,
            untouched_task_sets=untouched_task_sets,
            source_hashes=source_hashes,
            stored_source_hashes=stored_source_hashes,
        )
        self.existing_hashes = existing_hashes

    def get_localized_output(
        self,
        *,
        source_kind: str,
        source_record_id: int,
        language_code: str,
    ) -> Any | None:
        source_hash = self.existing_hashes.get(
            (source_kind, source_record_id, language_code)
        )
        return SimpleNamespace(source_hash=source_hash) if source_hash else None


class _MixedStatusIdeasRepo(_ReadOnlyPlannerRepo):
    def get_latest_pass_output(self, **kwargs: Any) -> Any | None:
        if kwargs["pass_kind"] != "trend_ideas":
            return super().get_latest_pass_output(**kwargs)
        status = kwargs.get("status")
        period_start = kwargs["period_start"]
        period_end = kwargs["period_end"]
        granularity = kwargs["granularity"]
        upstream_id = _stable_pass_output_id(
            granularity,
            period_start,
            "trend_synthesis",
        )
        if status == "succeeded":
            return self._ideas_row(
                status=status,
                row_id=upstream_id + 10,
                upstream_id=upstream_id - 1,
                created_at=datetime(2026, 3, 16, 2, tzinfo=UTC),
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
            )
        if status == "suppressed":
            return self._ideas_row(
                status=status,
                row_id=upstream_id + 11,
                upstream_id=upstream_id,
                created_at=datetime(2026, 3, 16, 3, tzinfo=UTC),
                granularity=granularity,
                period_start=period_start,
                period_end=period_end,
            )
        return None

    def _ideas_row(
        self,
        *,
        status: str,
        row_id: int,
        upstream_id: int,
        created_at: datetime,
        granularity: str,
        period_start: datetime,
        period_end: datetime,
    ) -> Any:
        freshness = build_trend_ideas_freshness(
            settings=_Settings(),
            granularity=granularity,
            period_start=period_start,
            period_end=period_end,
            upstream_pass_output_id=upstream_id,
        )
        return SimpleNamespace(
            id=row_id,
            status=status,
            created_at=created_at,
            diagnostics_json=json.dumps({"workflow_freshness": freshness}),
            input_refs_json=json.dumps(
                [
                    {
                        "ref_kind": "pass_output",
                        "pass_kind": "trend_synthesis",
                        "pass_output_id": upstream_id,
                    }
                ]
            ),
        )


class _DocumentOnlyLowerLevelRepo(_ReadOnlyPlannerRepo):
    def get_latest_pass_output(self, **kwargs: Any) -> Any | None:
        if (
            kwargs["granularity"] == "day"
            and kwargs["pass_kind"] in {"trend_synthesis", "trend_ideas"}
        ):
            return None
        return super().get_latest_pass_output(**kwargs)

    def list_documents(self, **kwargs: Any) -> list[Any]:
        if kwargs["granularity"] == "day" and kwargs["doc_type"] in {"trend", "idea"}:
            return (
                [SimpleNamespace(id=1)]
                if kwargs["doc_type"] == "trend"
                and kwargs["period_start"].date() == date(2026, 3, 16)
                else []
            )
        return super().list_documents(**kwargs)


def test_planner_skips_complete_day_level_work_for_week() -> None:
    plan = _week_plan()
    decisions = plan_workflow_execution(
        plan=plan,
        repository=_ReadOnlyPlannerRepo(),
        settings=_Settings(),
    )

    daily_expensive = [
        decision
        for decision in decisions
        if decision.granularity == "day"
        and decision.step_id in {"analyze", "trends:day", "ideas:day"}
    ]

    assert len(daily_expensive) == 21
    assert {decision.action for decision in daily_expensive} == {"skip"}
    assert {decision.reason for decision in daily_expensive} <= {
        "existing_lower_level_task_set",
        "no_candidate_items",
    }
    assert all(decision.authority for decision in decisions)


def test_week_planner_backfills_day_task_set_only_when_untouched() -> None:
    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_ReadOnlyPlannerRepo(untouched_task_sets={"day"}),
        settings=_Settings(),
    )

    day_generation = [
        decision
        for decision in decisions
        if decision.granularity == "day"
        and decision.step_id in {"trends:day", "ideas:day"}
    ]
    ingest_decision = _decision_for(decisions, "ingest", date(2026, 3, 16))
    analyze_decision = _decision_for(decisions, "analyze", date(2026, 3, 16))

    assert len(day_generation) == 14
    assert {decision.action for decision in day_generation} == {"run"}
    assert {decision.reason for decision in day_generation} == {
        "missing_lower_level_task_set"
    }
    assert ingest_decision.action == "skip"
    assert ingest_decision.reason == "downstream_complete"
    assert analyze_decision.action == "skip"
    assert analyze_decision.reason == "no_candidate_items"


def test_week_planner_does_not_backfill_missing_day_after_task_set_ran() -> None:
    missing_day = date(2026, 3, 18)
    plan = _week_plan()
    decisions = plan_workflow_execution(
        plan=plan,
        repository=_ReadOnlyPlannerRepo(missing_days={missing_day}),
        settings=_Settings(),
    )

    missing_day_decisions = [
        decision
        for decision in decisions
        if decision.granularity == "day"
        and decision.period_start == datetime(2026, 3, 18, tzinfo=UTC)
        and decision.step_id in {"analyze", "trends:day", "ideas:day"}
    ]
    other_day_expensive = [
        decision
        for decision in decisions
        if decision.granularity == "day"
        and decision.period_start != datetime(2026, 3, 18, tzinfo=UTC)
        and decision.step_id in {"analyze", "trends:day", "ideas:day"}
    ]

    assert _decision_for(decisions, "ingest", missing_day).action == "run"
    assert _decision_for(decisions, "analyze", missing_day).action == "run"
    assert {
        decision.action
        for decision in missing_day_decisions
        if decision.step_id in {"trends:day", "ideas:day"}
    } == {"skip"}
    assert {
        decision.reason
        for decision in missing_day_decisions
        if decision.step_id in {"trends:day", "ideas:day"}
    } == {"existing_lower_level_task_set"}
    assert {decision.action for decision in other_day_expensive} == {"skip"}


def test_week_planner_skips_existing_lower_level_outputs_when_sources_changed() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_ReadOnlyPlannerRepo(
            source_hashes={("item", source_day): "source-hash-new"},
            stored_source_hashes={("item", source_day): "source-hash-old"},
        ),
        settings=_Settings(),
    )

    trend_decision = _decision_for(decisions, "trends:day", source_day)
    ideas_decision = _decision_for(decisions, "ideas:day", source_day)

    assert trend_decision.action == "skip"
    assert trend_decision.reason == "existing_lower_level_task_set"
    assert ideas_decision.action == "skip"
    assert ideas_decision.reason == "existing_lower_level_task_set"


def test_week_planner_skips_lower_level_task_set_when_artifact_exists() -> None:
    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_DocumentOnlyLowerLevelRepo(),
        settings=_Settings(),
    )

    day_generation = [
        decision
        for decision in decisions
        if decision.granularity == "day"
        and decision.step_id in {"trends:day", "ideas:day"}
    ]

    assert day_generation
    assert {decision.action for decision in day_generation} == {"skip"}
    assert {decision.reason for decision in day_generation} == {
        "existing_lower_level_task_set"
    }


def test_week_planner_skips_missing_lower_level_idea_after_task_set_ran() -> None:
    source_day = date(2026, 3, 18)

    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_ReadOnlyPlannerRepo(
            missing_idea_windows={("day", source_day)},
        ),
        settings=_Settings(),
    )

    trend_decision = _decision_for(decisions, "trends:day", source_day)
    ideas_decision = _decision_for(decisions, "ideas:day", source_day)
    ingest_decision = _decision_for(decisions, "ingest", source_day)
    analyze_decision = _decision_for(decisions, "analyze", source_day)
    publish_decision = _decision_for(decisions, "publish", source_day)

    assert trend_decision.action == "skip"
    assert trend_decision.reason == "existing_lower_level_task_set"
    assert ideas_decision.action == "skip"
    assert ideas_decision.reason == "existing_lower_level_task_set"
    assert ingest_decision.action == "skip"
    assert ingest_decision.reason == "downstream_complete"
    assert analyze_decision.action == "skip"
    assert analyze_decision.reason == "no_candidate_items"
    assert publish_decision.action == "skip"
    assert publish_decision.reason == "no_publish_candidates"


@pytest.mark.parametrize(
    ("settings_field", "workflow_model", "step_id"),
    [
        (None, "gpt-override", "trends:day"),
        ("trends_llm_model", None, "trends:day"),
        ("ideas_llm_model", None, "ideas:day"),
    ],
)
def test_week_planner_reruns_document_only_outputs_for_model_change(
    settings_field: str | None,
    workflow_model: str | None,
    step_id: str,
) -> None:
    source_day = date(2026, 3, 16)
    settings = _Settings()
    if settings_field is not None:
        setattr(settings, settings_field, "gpt-stage-override")
    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_DocumentOnlyLowerLevelRepo(),
        settings=settings,
        options=WorkflowPlanningOptions(llm_model=workflow_model),
    )

    decision = _decision_for(decisions, step_id, source_day)
    assert decision.action == "run"


def test_week_planner_treats_suppressed_lower_level_ideas_as_existing() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_MixedStatusIdeasRepo(),
        settings=_Settings(),
    )

    decision = _decision_for(decisions, "ideas:day", source_day)
    assert decision.action == "skip"
    assert decision.reason == "existing_lower_level_task_set"


def test_planner_runs_analyze_when_planned_ingest_may_create_candidates() -> None:
    missing_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_NoCurrentAnalysisCandidatesRepo(missing_days={missing_day}),
        settings=_Settings(),
    )

    ingest_decision = _decision_for(decisions, "ingest", missing_day)
    analyze_decision = _decision_for(decisions, "analyze", missing_day)
    trend_decision = _decision_for(decisions, "trends:day", missing_day)

    assert ingest_decision.action == "run"
    assert trend_decision.action == "run"
    assert analyze_decision.action == "run"
    assert analyze_decision.reason == "upstream_ingest_planned"


def test_planner_skips_analyze_when_budget_was_satisfied_with_backlog() -> None:
    source_day = date(2026, 3, 16)
    settings = _TriageSettings()
    repo = _AnalyzeBudgetReceiptRepo(selected_total=settings.analyze_limit)

    decisions = plan_workflow_execution(
        plan=_day_analyze_only_plan(settings=settings),
        repository=repo,
        settings=settings,
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)

    assert analyze_decision.action == "skip"
    assert analyze_decision.reason == "analyze_budget_satisfied"
    assert analyze_decision.estimated_llm_calls == 0
    assert analyze_decision.metadata == {
        "analyze_budget": {
            "configured_limit": 8,
            "receipt_run_id": "run-analyze-budget",
            "receipt_selected_total": 8,
            "receipt_requested_limit": 8,
            "receipt_processed_total": 8,
            "receipt_failed_total": 0,
        },
        "candidate_backlog": {
            "present": True,
            "total": 4,
            "by_state": {"retryable_failed": 1, "triaged": 3},
        },
    }


def test_planner_runs_analyze_when_budget_increases_above_receipt() -> None:
    source_day = date(2026, 3, 16)
    settings = _TriageSettings()
    settings.analyze_limit = 10

    decisions = plan_workflow_execution(
        plan=_day_analyze_only_plan(settings=settings),
        repository=_AnalyzeBudgetReceiptRepo(selected_total=8),
        settings=settings,
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)

    assert analyze_decision.action == "run"
    assert analyze_decision.reason == "candidate_items"


def test_planner_ignores_analyze_budget_receipt_for_workflow_model_override() -> None:
    source_day = date(2026, 3, 16)
    settings = _TriageSettings()
    repo = _AnalyzeBudgetReceiptRepo(selected_total=settings.analyze_limit)

    decisions = plan_workflow_execution(
        plan=_day_analyze_only_plan(settings=settings),
        repository=repo,
        settings=settings,
        options=WorkflowPlanningOptions(llm_model="gpt-override"),
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)
    assert analyze_decision.action == "run"
    assert analyze_decision.reason == "candidate_items"
    assert repo.receipt_requests
    assert repo.receipt_requests[0]["config_fingerprint"] != "fp-test"


def test_week_planner_trusts_day_analyze_budget_receipts() -> None:
    settings = _TriageSettings()

    decisions = plan_workflow_execution(
        plan=_week_analyze_only_plan(settings=settings),
        repository=_AnalyzeBudgetReceiptRepo(selected_total=settings.analyze_limit),
        settings=settings,
    )

    day_analyze_decisions = [
        decision
        for decision in decisions
        if decision.step_id == "analyze" and decision.granularity == "day"
    ]

    assert len(day_analyze_decisions) == 7
    assert {decision.action for decision in day_analyze_decisions} == {"skip"}
    assert {decision.reason for decision in day_analyze_decisions} == {
        "analyze_budget_satisfied"
    }


def test_planner_reruns_trends_and_ideas_when_analyze_is_planned() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_AnalyzeCandidatesRepo(),
        settings=_Settings(),
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)
    trend_decision = _decision_for(decisions, "trends:day", source_day)
    ideas_decision = _decision_for(decisions, "ideas:day", source_day)

    assert analyze_decision.action == "run"
    assert analyze_decision.reason == "candidate_items"
    assert trend_decision.action == "run"
    assert trend_decision.reason == "upstream_analyze_planned"
    assert ideas_decision.action == "run"
    assert ideas_decision.reason == "upstream_trend_planned"


def test_planner_runs_publish_when_analyze_is_planned() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_AnalyzeCandidatesRepo(),
        settings=_Settings(),
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)
    publish_decision = _decision_for(decisions, "publish", source_day)

    assert analyze_decision.action == "run"
    assert publish_decision.action == "run"
    assert publish_decision.reason == "upstream_analyze_planned"


def test_generation_force_does_not_force_analyze_without_reprocess_path() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_plan_without_ingest(),
        repository=_ReadOnlyPlannerRepo(),
        settings=_Settings(),
        options=WorkflowPlanningOptions(generation_force=True),
    )

    analyze_decision = _decision_for(decisions, "analyze", source_day)
    trend_decision = _decision_for(decisions, "trends:day", source_day)
    ideas_decision = _decision_for(decisions, "ideas:day", source_day)

    assert analyze_decision.action == "skip"
    assert analyze_decision.reason == "no_candidate_items"
    assert trend_decision.action == "force"
    assert ideas_decision.action == "force"


def test_generation_force_overrides_existing_lower_level_task_sets() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_ReadOnlyPlannerRepo(),
        settings=_Settings(),
        options=WorkflowPlanningOptions(generation_force=True),
    )

    trend_decision = _decision_for(decisions, "trends:day", source_day)
    ideas_decision = _decision_for(decisions, "ideas:day", source_day)

    assert trend_decision.action == "force"
    assert trend_decision.reason == "generation_force"
    assert ideas_decision.action == "force"
    assert ideas_decision.reason == "generation_force"


def test_month_planner_does_not_rerun_existing_week_when_day_is_generated() -> None:
    source_day = date(2026, 3, 18)
    source_week = date(2026, 3, 16)
    source_month = date(2026, 3, 1)

    decisions = plan_workflow_execution(
        plan=_month_plan(),
        repository=_ReadOnlyPlannerRepo(untouched_task_sets={"day"}),
        settings=_Settings(),
    )

    day_trend = _decision_for(decisions, "trends:day", source_day)
    week_trend = _decision_for(decisions, "trends:week", source_week)
    week_ideas = _decision_for(decisions, "ideas:week", source_week)
    month_trend = _decision_for(decisions, "trends:month", source_month)
    month_ideas = _decision_for(decisions, "ideas:month", source_month)

    assert day_trend.action == "run"
    assert day_trend.reason == "missing_lower_level_task_set"
    assert week_trend.action == "skip"
    assert week_trend.reason == "existing_lower_level_task_set"
    assert week_ideas.action == "skip"
    assert week_ideas.reason == "existing_lower_level_task_set"
    assert month_trend.action == "skip"
    assert month_ideas.action == "skip"


def test_month_planner_reruns_target_when_direct_week_source_is_generated() -> None:
    source_week = date(2026, 3, 16)
    source_month = date(2026, 3, 1)

    decisions = plan_workflow_execution(
        plan=_month_plan(),
        repository=_ReadOnlyPlannerRepo(untouched_task_sets={"week"}),
        settings=_Settings(),
    )

    week_trend = _decision_for(decisions, "trends:week", source_week)
    month_trend = _decision_for(decisions, "trends:month", source_month)
    month_ideas = _decision_for(decisions, "ideas:month", source_month)

    assert week_trend.action == "run"
    assert week_trend.reason == "missing_lower_level_task_set"
    assert month_trend.action == "run"
    assert month_trend.reason == "upstream_trend_planned"
    assert month_ideas.action == "run"
    assert month_ideas.reason == "upstream_trend_planned"


def test_planner_is_read_only() -> None:
    repository = _ReadOnlyPlannerRepo()

    _ = plan_workflow_execution(
        plan=_week_plan(),
        repository=repository,
        settings=_Settings(),
    )

    assert repository.write_calls == []


def test_planner_reports_translation_candidates_by_source_bucket(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trend_candidate = SimpleNamespace(
        source_kind="trend_synthesis",
        source_record_id=11,
        payload={"title": "fresh trend"},
        granularity="day",
    )
    idea_candidate = SimpleNamespace(
        source_kind="trend_ideas",
        source_record_id=12,
        payload={"title": "new ideas"},
        granularity="day",
    )

    def _fake_candidates(**kwargs: Any) -> list[Any]:
        assert kwargs["source_language_code"] == "en"
        assert kwargs["granularity"] == "day"
        assert kwargs["include"] == ["trends", "ideas"]
        return [trend_candidate, idea_candidate]

    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        _fake_candidates,
    )
    repo = _TranslationPlannerRepo(
        existing_hashes={
            (
                "trend_synthesis",
                11,
                "zh-cn",
            ): workflow_planner_module._translation_payload_hash(trend_candidate)
        }
    )

    decisions = plan_workflow_execution(
        plan=_day_translation_plan(),
        repository=repo,
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            translate_include=["trends", "ideas"],
            translate_granularities=["day"],
        ),
    )

    decision = _translation_decision(decisions)
    assert decision.action == "run"
    assert decision.reason == "translation_candidates"
    assert decision.estimated_llm_calls == 1
    by_source = _translation_summary_by_bucket(decision)
    assert by_source["trend_synthesis.day"]["skip"] == 1
    assert by_source["trend_synthesis.day"]["run"] == 0
    assert by_source["trend_ideas.day"]["skip"] == 0
    assert by_source["trend_ideas.day"]["run"] == 1


def test_planner_skips_translation_when_localized_outputs_are_fresh(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    trend_candidate = SimpleNamespace(
        source_kind="trend_synthesis",
        source_record_id=11,
        payload={"title": "fresh trend"},
        granularity="day",
    )

    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        lambda **_kwargs: [trend_candidate],
    )
    repo = _TranslationPlannerRepo(
        existing_hashes={
            (
                "trend_synthesis",
                11,
                "zh-cn",
            ): workflow_planner_module._translation_payload_hash(trend_candidate)
        }
    )

    decisions = plan_workflow_execution(
        plan=_day_translation_plan(),
        repository=repo,
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            translate_include=["trends", "ideas"],
            translate_granularities=["day"],
        ),
    )

    decision = _translation_decision(decisions)
    assert decision.action == "skip"
    assert decision.reason == "localized_outputs_fresh"
    assert decision.estimated_llm_calls == 0
    by_source = _translation_summary_by_bucket(decision)
    assert by_source["trend_synthesis.day"]["skip"] == 1
    assert by_source["trend_synthesis.day"]["run"] == 0


def test_planner_runs_translation_when_week_outputs_are_planned(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        lambda **_kwargs: [],
    )

    decisions = plan_workflow_execution(
        plan=_week_translation_plan(),
        repository=_TranslationPlannerRepo(
            missing_trend_windows={("week", date(2026, 3, 16))},
            existing_hashes={},
        ),
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            translate_include=["trends", "ideas"],
            translate_granularities=["week"],
        ),
    )

    assert _decision_for(decisions, "trends:week", date(2026, 3, 16)).action == "run"
    decision = _translation_decision(decisions)
    assert decision.action == "run"
    assert decision.reason == "upstream_generation_planned"


def test_planner_reruns_translation_when_workflow_model_changes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    candidate = SimpleNamespace(
        source_kind="trend_synthesis",
        source_record_id=11,
        payload={"title": "fresh trend"},
        granularity="day",
    )
    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        lambda **_kwargs: [candidate],
    )
    repo = _TranslationPlannerRepo(
        existing_hashes={
            (
                "trend_synthesis",
                11,
                "zh-cn",
            ): workflow_planner_module._translation_payload_hash(candidate)
        }
    )

    decisions = plan_workflow_execution(
        plan=_day_translation_plan(),
        repository=repo,
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            llm_model="gpt-translation-override",
            translate_include=["trends"],
            translate_granularities=["day"],
        ),
    )

    decision = _translation_decision(decisions)
    assert decision.action == "run"
    assert decision.reason == "translation_candidates"
    assert decision.estimated_llm_calls == 1


def test_trend_planner_reruns_trend_and_ideas_when_source_hash_changes() -> None:
    source_day = date(2026, 3, 16)
    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_ReadOnlyPlannerRepo(
            source_hashes={("item", source_day): "source-hash-new"},
            stored_source_hashes={("item", source_day): "source-hash-old"},
        ),
        settings=_Settings(),
    )

    decision = _decision_for(decisions, "trends:day", source_day)
    assert decision.action == "run"
    assert decision.reason == "stale_freshness"

    ideas_decision = _decision_for(decisions, "ideas:day", source_day)
    assert ideas_decision.action == "run"
    assert ideas_decision.reason == "upstream_trend_planned"


def test_trend_planner_treats_workflow_model_override_as_stale_freshness() -> None:
    source_day = date(2026, 3, 16)
    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_ReadOnlyPlannerRepo(),
        settings=_Settings(),
        options=WorkflowPlanningOptions(llm_model="gpt-override"),
    )

    decision = _decision_for(decisions, "trends:day", source_day)
    assert decision.action == "run"
    assert decision.reason == "stale_freshness"


@pytest.mark.parametrize(
    ("workflow_name", "lower_granularity", "source_date"),
    [
        ("week", "day", date(2026, 3, 16)),
        ("month", "week", date(2026, 3, 16)),
    ],
)
def test_recursive_planner_reruns_lower_level_outputs_when_workflow_model_changes(
    workflow_name: str,
    lower_granularity: str,
    source_date: date,
) -> None:
    plan = _week_plan() if workflow_name == "week" else _month_plan()
    decisions = plan_workflow_execution(
        plan=plan,
        repository=_ReadOnlyPlannerRepo(),
        settings=_Settings(),
        options=WorkflowPlanningOptions(llm_model="gpt-override"),
    )

    trend_decision = _decision_for(
        decisions,
        f"trends:{lower_granularity}",
        source_date,
    )
    ideas_decision = _decision_for(
        decisions,
        f"ideas:{lower_granularity}",
        source_date,
    )

    assert trend_decision.action == "run"
    assert trend_decision.reason == "stale_freshness"
    assert ideas_decision.action == "run"


@pytest.mark.parametrize(
    ("settings_field", "step_id"),
    [
        ("trends_llm_model", "trends:day"),
        ("ideas_llm_model", "ideas:day"),
    ],
)
def test_week_planner_reruns_lower_level_output_when_stage_model_changes(
    settings_field: str,
    step_id: str,
) -> None:
    settings = _Settings()
    setattr(settings, settings_field, "gpt-stage-override")

    decisions = plan_workflow_execution(
        plan=_week_plan(),
        repository=_ReadOnlyPlannerRepo(),
        settings=settings,
    )

    decision = _decision_for(decisions, step_id, date(2026, 3, 16))
    assert decision.action == "run"


class _FreshnessSettings:
    def __init__(
        self,
        *,
        llm_model: str = "test/global",
        analyze_llm_model: str | None = None,
        trends_llm_model: str | None = None,
        ideas_llm_model: str | None = None,
        translation_llm_model: str | None = None,
    ) -> None:
        self.llm_model = llm_model
        self.analyze_llm_model = analyze_llm_model
        self.trends_llm_model = trends_llm_model
        self.ideas_llm_model = ideas_llm_model
        self.translation_llm_model = translation_llm_model
        self.llm_output_language = "English"

    def safe_model_dump(self) -> dict[str, object]:
        return {
            "llm_model": self.llm_model,
            "analyze_llm_model": self.analyze_llm_model,
            "trends_llm_model": self.trends_llm_model,
            "ideas_llm_model": self.ideas_llm_model,
            "translation_llm_model": self.translation_llm_model,
            "llm_output_language": self.llm_output_language,
            "topics": ["agents"],
        }

    def safe_fingerprint(self) -> str:
        return "full-config-fingerprint"


def test_trend_freshness_ignores_unrelated_stage_specific_models() -> None:
    period_start = datetime(2026, 3, 16, tzinfo=UTC)
    period_end = datetime(2026, 3, 17, tzinfo=UTC)
    base = build_trend_synthesis_freshness(
        settings=_FreshnessSettings(
            trends_llm_model="test/trends-stage",
            translation_llm_model="test/translation-a",
        ),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
    )
    unrelated_translation_change = build_trend_synthesis_freshness(
        settings=_FreshnessSettings(
            trends_llm_model="test/trends-stage",
            translation_llm_model="test/translation-b",
        ),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
    )
    effective_trends_change = build_trend_synthesis_freshness(
        settings=_FreshnessSettings(trends_llm_model="test/trends-next"),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
    )

    assert base["key"] == unrelated_translation_change["key"]
    assert base["key"] != effective_trends_change["key"]
    assert base["components"]["llm_model"] == "test/trends-stage"
    assert effective_trends_change["components"]["llm_model"] == "test/trends-next"


def test_ideas_freshness_ignores_unrelated_stage_specific_models() -> None:
    period_start = datetime(2026, 3, 16, tzinfo=UTC)
    period_end = datetime(2026, 3, 17, tzinfo=UTC)
    base = build_trend_ideas_freshness(
        settings=_FreshnessSettings(
            ideas_llm_model="test/ideas-stage",
            analyze_llm_model="test/analyze-a",
        ),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        upstream_pass_output_id=42,
    )
    unrelated_analyze_change = build_trend_ideas_freshness(
        settings=_FreshnessSettings(
            ideas_llm_model="test/ideas-stage",
            analyze_llm_model="test/analyze-b",
        ),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        upstream_pass_output_id=42,
    )
    effective_ideas_change = build_trend_ideas_freshness(
        settings=_FreshnessSettings(ideas_llm_model="test/ideas-next"),
        granularity="day",
        period_start=period_start,
        period_end=period_end,
        upstream_pass_output_id=42,
    )

    assert base["key"] == unrelated_analyze_change["key"]
    assert base["key"] != effective_ideas_change["key"]
    assert base["components"]["llm_model"] == "test/ideas-stage"
    assert effective_ideas_change["components"]["llm_model"] == "test/ideas-next"


def test_ideas_planner_prefers_newer_suppressed_output_over_older_success() -> None:
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_plan(),
        repository=_MixedStatusIdeasRepo(),
        settings=_Settings(),
    )

    decision = _decision_for(decisions, "ideas:day", source_day)
    assert decision.action == "skip"
    assert decision.reason == "suppressed_ideas"
    assert decision.estimated_llm_calls == 0


def test_translation_planner_sees_ideas_rerun_from_changed_trend_source(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        lambda **_kwargs: [],
    )
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_translation_plan(),
        repository=_TranslationPlannerRepo(
            existing_hashes={},
            source_hashes={("item", source_day): "source-hash-new"},
            stored_source_hashes={("item", source_day): "source-hash-old"},
        ),
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            translate_include=["ideas"],
            translate_granularities=["day"],
        ),
    )

    assert _decision_for(decisions, "trends:day", source_day).action == "run"
    assert _decision_for(decisions, "ideas:day", source_day).action == "run"
    decision = _translation_decision(decisions)
    assert decision.action == "run"
    assert decision.reason == "upstream_generation_planned"


def test_translation_planner_sees_analyze_run_for_item_translation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        workflow_planner_module,
        "_translation_candidates_for_plan",
        lambda **_kwargs: [],
    )
    source_day = date(2026, 3, 16)

    decisions = plan_workflow_execution(
        plan=_day_translation_plan(),
        repository=_TranslationPlannerRepo(
            existing_hashes={},
            missing_days={source_day},
        ),
        settings=_TranslationSettings(),
        options=WorkflowPlanningOptions(
            translate_include=["items"],
            translate_granularities=["day"],
        ),
    )

    assert _decision_for(decisions, "analyze", source_day).action == "run"
    decision = _translation_decision(decisions)
    assert decision.action == "run"
    assert decision.reason == "upstream_generation_planned"


def test_translation_planner_candidate_loader_is_read_only(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_requests: list[Any] = []

    def _fake_incremental_candidates(request: Any) -> list[Any]:
        captured_requests.append(request)
        return []

    monkeypatch.setattr(
        "recoleta.translation._candidate_incremental_candidates",
        _fake_incremental_candidates,
    )

    assert (
        workflow_planner_module._translation_candidates_for_plan(
            repository=SimpleNamespace(),
            granularity="day",
            include=["ideas"],
            source_language_code="en",
            period_start=datetime(2026, 3, 16, tzinfo=UTC),
            period_end=datetime(2026, 3, 17, tzinfo=UTC),
            all_history=False,
        )
        == []
    )

    assert captured_requests
    assert captured_requests[0].materialize_missing_idea_projections is False


def _week_plan():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="week",
            command="run week",
            anchor_date="2026-03-16",
            settings=_Settings(),
            include_steps=[],
            skip_steps=[],
        )
    )


def _week_translation_plan():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="week",
            command="run week",
            anchor_date="2026-03-16",
            settings=_TranslationSettings(),
            include_steps=[],
            skip_steps=[],
        )
    )


def _month_plan():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="month",
            command="run month",
            anchor_date="2026-03-16",
            settings=_Settings(),
            include_steps=[],
            skip_steps=[],
        )
    )


def _day_plan():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="day",
            command="run day",
            anchor_date="2026-03-16",
            settings=_Settings(),
            include_steps=[],
            skip_steps=[],
        )
    )


def _day_plan_without_ingest():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="day",
            command="run day",
            anchor_date="2026-03-16",
            settings=_Settings(),
            include_steps=[],
            skip_steps=["ingest"],
        )
    )


def _day_analyze_only_plan(*, settings):
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="day",
            command="run day",
            anchor_date="2026-03-16",
            settings=settings,
            include_steps=[],
            skip_steps=["ingest", "publish", "trends:day", "ideas:day"],
        )
    )


def _week_analyze_only_plan(*, settings):
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="week",
            command="run week",
            anchor_date="2026-03-16",
            settings=settings,
            include_steps=[],
            skip_steps=[
                "ingest",
                "publish",
                "trends:day",
                "ideas:day",
                "trends:week",
                "ideas:week",
            ],
        )
    )


def _day_translation_plan():
    return build_granularity_plan(
        request=GranularityPlanRequest(
            workflow_name="day",
            command="run day",
            anchor_date="2026-03-16",
            settings=_TranslationSettings(),
            include_steps=[],
            skip_steps=[],
        )
    )


def _translation_decision(decisions):
    return next(decision for decision in decisions if decision.step_id == STEP_TRANSLATE)


def _translation_summary_by_bucket(decision):
    assert decision.metadata is not None
    translation = decision.metadata["translation"]
    return {entry["source_bucket"]: entry for entry in translation["by_source"]}


def _decision_for(decisions, step_id, anchor_date):
    return next(
        decision
        for decision in decisions
        if decision.step_id == step_id and decision.anchor_date == anchor_date
    )


def _stable_pass_output_id(
    granularity: str,
    period_start: datetime,
    pass_kind: str,
) -> int:
    offset = {"day": 0, "week": 100, "month": 200}[granularity]
    kind_offset = {"trend_synthesis": 1, "trend_ideas": 2}[pass_kind]
    return offset + period_start.toordinal() * 10 + kind_offset


def _stable_doc_id(
    granularity: str,
    period_start: datetime,
    kind: str,
) -> int:
    granularity_offset = {"item": 0, "day": 100, "week": 200, "month": 300}[
        granularity
    ]
    kind_offset = {"doc": 0, "summary": 1, "content": 2, "meta": 3}[kind]
    return granularity_offset + period_start.toordinal() * 10 + kind_offset
