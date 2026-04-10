from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from platformdirs import user_data_dir
from pydantic import (
    BaseModel,
    Field,
    SecretStr,
    ValidationInfo,
    field_validator,
    model_validator,
)
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
import yaml

from recoleta.llm_connection import LLMConnectionConfig


def _parse_json_or_yaml(value: str) -> Any:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Value must not be empty")
    try:
        return json.loads(stripped)
    except Exception:
        loaded = yaml.safe_load(stripped)
        return loaded


def _parse_str_list(value: str) -> list[str]:
    stripped = value.strip()
    if not stripped:
        return []

    loaded: Any | None = None
    try:
        loaded = json.loads(stripped)
    except Exception:
        try:
            loaded = yaml.safe_load(stripped)
        except Exception:
            loaded = None

    if isinstance(loaded, list):
        return [str(item).strip() for item in loaded if str(item).strip()]
    if isinstance(loaded, str):
        stripped = loaded.strip()

    if "," in stripped:
        return [part.strip() for part in stripped.split(",") if part.strip()]
    return [stripped]


def _default_markdown_output_dir() -> Path:
    return (Path(user_data_dir("recoleta")) / "outputs").expanduser().resolve()


def _default_lancedb_dir() -> Path:
    return (Path(user_data_dir("recoleta")) / "lancedb").expanduser().resolve()


_ALLOWED_PUBLISH_TARGETS = {"markdown", "obsidian", "telegram"}
_ALLOWED_ARXIV_ENRICH_METHODS = {"pdf_text", "latex_source", "html_document"}
_ALLOWED_ARXIV_ENRICH_FAILURE_MODES = {"fallback", "strict"}
_ALLOWED_TRENDS_EMBEDDING_FAILURE_MODES = {"continue", "fail_fast", "threshold"}
_ALLOWED_WORKFLOW_DELIVERY_MODES = {"all", "local_only", "none"}
_ALLOWED_WORKFLOW_TRANSLATION_MODES = {"auto", "off"}
_ALLOWED_WORKFLOW_TRANSLATE_INCLUDE = {"items", "trends", "ideas"}
_ALLOWED_WORKFLOW_TRANSLATE_FAILURE = {"fail", "partial_success", "skip"}
_ALLOWED_DAEMON_WEEKDAYS = {"mon", "tue", "wed", "thu", "fri", "sat", "sun"}
_UNSUPPORTED_TOPIC_STREAM_FILE_KEYS = ("TOPIC_STREAMS", "topic_streams")
_UNSUPPORTED_TOPIC_STREAM_ENV_KEYS = ("TOPIC_STREAMS",)
_DEPRECATED_SCHEDULER_INTERVAL_KEYS = (
    "INGEST_INTERVAL_MINUTES",
    "ANALYZE_INTERVAL_MINUTES",
    "PUBLISH_INTERVAL_MINUTES",
)
_ENV_FILE_ASSIGNMENT_RE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=")
_LANGUAGE_CODE_RE = re.compile(r"^[A-Za-z]{2,3}(?:-[A-Za-z0-9]{2,8})*$")


def _normalize_publish_targets(values: list[str], *, field_name: str) -> list[str]:
    normalized: list[str] = []
    for raw in values:
        if not isinstance(raw, str):
            continue
        token = raw.strip().lower()
        if not token:
            continue
        normalized.append(token)
    normalized = list(dict.fromkeys(normalized))
    if not normalized:
        raise ValueError(
            f"{field_name} must include at least one target: markdown, obsidian, telegram"
        )
    unknown = sorted(
        {token for token in normalized if token not in _ALLOWED_PUBLISH_TARGETS}
    )
    if unknown:
        raise ValueError(
            f"Unsupported {field_name} value(s): "
            + ", ".join(unknown)
            + " (allowed: markdown, obsidian, telegram)"
        )
    return normalized


def _normalize_workflow_translate_include(
    values: list[str],
    *,
    field_name: str,
) -> list[str]:
    normalized: list[str] = []
    for raw in values:
        if not isinstance(raw, str):
            continue
        token = raw.strip().lower()
        if not token:
            continue
        normalized.append(token)
    normalized = list(dict.fromkeys(normalized))
    if not normalized:
        raise ValueError(
            f"{field_name} must include at least one value: items, trends, ideas"
        )
    unknown = sorted(
        {
            token
            for token in normalized
            if token not in _ALLOWED_WORKFLOW_TRANSLATE_INCLUDE
        }
    )
    if unknown:
        raise ValueError(
            f"Unsupported {field_name} value(s): "
            + ", ".join(unknown)
            + " (allowed: items, trends, ideas)"
        )
    return normalized


def _legacy_scheduler_interval_message(keys: list[str]) -> str:
    normalized = list(
        dict.fromkeys(str(key).strip() for key in keys if str(key).strip())
    )
    rendered = ", ".join(f"`{key}`" for key in normalized)
    return (
        "CLI v2 removed legacy scheduler interval settings: "
        f"{rendered}. Use `WORKFLOWS`/`DAEMON` (`workflows`/`daemon` in YAML) "
        "for workflow scheduling, or an external scheduler plus `recoleta stage ...` "
        "if you need ingest/analyze/publish-only runs."
    )


def _unsupported_config_format_message(keys: list[str]) -> str:
    normalized = list(
        dict.fromkeys(str(key).strip() for key in keys if str(key).strip())
    )
    rendered = ", ".join(f"`{key}`" for key in normalized)
    verb = "is" if len(normalized) == 1 else "are"
    return f"Unsupported config format: {rendered} {verb} no longer supported."


def _normalize_env_key(key: str) -> str:
    return str(key or "").strip().upper()


def _configured_env_files(settings_cls: type[BaseSettings]) -> list[Path]:
    env_file = settings_cls.model_config.get("env_file")
    if env_file is None:
        return []
    if isinstance(env_file, (str, Path)):
        candidates = [env_file]
    else:
        candidates = list(env_file)
    env_paths: list[Path] = []
    for candidate in candidates:
        raw = str(candidate or "").strip()
        if raw:
            env_paths.append(Path(raw).expanduser().resolve())
    return env_paths


def _scan_env_file_for_keys(path: Path, *, keys: tuple[str, ...]) -> list[str]:
    if not path.exists() or not path.is_file():
        return []
    normalized_keys = {_normalize_env_key(key) for key in keys}
    found: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = _ENV_FILE_ASSIGNMENT_RE.match(line)
        if match is None:
            continue
        key = match.group(1)
        if _normalize_env_key(key) in normalized_keys:
            found.append(key)
    return found


def _reject_unsupported_topic_stream_environment(
    settings_cls: type[BaseSettings],
) -> None:
    normalized_keys = {
        _normalize_env_key(key) for key in _UNSUPPORTED_TOPIC_STREAM_ENV_KEYS
    }
    found = [key for key in os.environ if _normalize_env_key(key) in normalized_keys]
    for env_path in _configured_env_files(settings_cls):
        found.extend(
            _scan_env_file_for_keys(
                env_path,
                keys=_UNSUPPORTED_TOPIC_STREAM_ENV_KEYS,
            )
        )
    if found:
        raise ValueError(_unsupported_config_format_message(found))


def _normalize_language_code(value: Any, *, field_name: str) -> str:
    normalized = str(value or "").strip()
    if not normalized:
        raise ValueError(f"{field_name} must not be empty")
    if "\n" in normalized or "\r" in normalized:
        raise ValueError(f"{field_name} must be a single-line value")
    if len(normalized) > 32:
        raise ValueError(f"{field_name} must be <= 32 characters")
    if _LANGUAGE_CODE_RE.fullmatch(normalized) is None:
        raise ValueError(f"{field_name} must be a valid language code")
    return normalized


class LocalizationTargetConfig(BaseModel):
    code: str
    llm_label: str

    @field_validator("code", mode="before")
    @classmethod
    def _normalize_code(cls, value: Any) -> str:
        return _normalize_language_code(value, field_name="localization.targets.code")

    @field_validator("llm_label", mode="before")
    @classmethod
    def _normalize_llm_label(cls, value: Any) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            raise ValueError("localization.targets.llm_label must not be empty")
        if "\n" in normalized or "\r" in normalized:
            raise ValueError(
                "localization.targets.llm_label must be a single-line value"
            )
        if len(normalized) > 64:
            raise ValueError("localization.targets.llm_label must be <= 64 characters")
        return normalized


class LocalizationConfig(BaseModel):
    source_language_code: str
    targets: list[LocalizationTargetConfig] = Field(default_factory=list)
    site_default_language_code: str
    legacy_backfill_source_language_code: str | None = None

    @field_validator(
        "source_language_code",
        "site_default_language_code",
        "legacy_backfill_source_language_code",
        mode="before",
    )
    @classmethod
    def _normalize_language_codes(cls, value: Any, info: Any) -> str | None:
        if value is None:
            return None
        return _normalize_language_code(
            value, field_name=f"localization.{info.field_name}"
        )

    @model_validator(mode="after")
    def _validate_localization(self) -> "LocalizationConfig":
        target_codes = [target.code for target in self.targets]
        duplicates = sorted(
            {code for code in target_codes if target_codes.count(code) > 1}
        )
        if duplicates:
            raise ValueError(
                "localization.targets codes must be unique: " + ", ".join(duplicates)
            )
        if self.source_language_code in set(target_codes):
            raise ValueError(
                "localization.targets.code must not duplicate source_language_code"
            )
        known_codes = {self.source_language_code, *target_codes}
        if self.site_default_language_code not in known_codes:
            raise ValueError(
                "localization.site_default_language_code must match source_language_code or one target code"
            )
        return self


class WorkflowPolicyConfig(BaseModel):
    recursive_lower_levels: bool = True
    delivery_mode: str = "all"
    translation: str = "auto"
    translate_include: list[str] = Field(
        default_factory=lambda: ["items", "trends", "ideas"]
    )
    site_build: bool = True
    on_translate_failure: str = "partial_success"

    @field_validator("delivery_mode", mode="before")
    @classmethod
    def _normalize_delivery_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower() or "all"
        if normalized not in _ALLOWED_WORKFLOW_DELIVERY_MODES:
            raise ValueError(
                "workflows.granularities.*.delivery_mode must be one of: all, local_only, none"
            )
        return normalized

    @field_validator("translation", mode="before")
    @classmethod
    def _normalize_translation_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower() or "auto"
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATION_MODES:
            raise ValueError(
                "workflows.granularities.*.translation must be one of: auto, off"
            )
        return normalized

    @field_validator("translate_include", mode="before")
    @classmethod
    def _parse_translate_include(cls, value: Any) -> Any:
        if value is None:
            return ["items", "trends", "ideas"]
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("on_translate_failure", mode="before")
    @classmethod
    def _normalize_translate_failure_policy(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower() or "partial_success"
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATE_FAILURE:
            raise ValueError(
                "workflows.granularities.*.on_translate_failure must be one of: fail, partial_success, skip"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_translate_include(self) -> "WorkflowPolicyConfig":
        self.translate_include = _normalize_workflow_translate_include(
            self.translate_include,
            field_name="workflows.granularities.*.translate_include",
        )
        return self


class WorkflowPolicyOverrideConfig(BaseModel):
    recursive_lower_levels: bool | None = None
    delivery_mode: str | None = None
    translation: str | None = None
    translate_include: list[str] | None = None
    site_build: bool | None = None
    on_translate_failure: str | None = None

    @field_validator("delivery_mode", mode="before")
    @classmethod
    def _normalize_delivery_mode(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value or "").strip().lower()
        if not normalized:
            return None
        if normalized not in _ALLOWED_WORKFLOW_DELIVERY_MODES:
            raise ValueError(
                "workflows.granularities.*.delivery_mode must be one of: all, local_only, none"
            )
        return normalized

    @field_validator("translation", mode="before")
    @classmethod
    def _normalize_translation_mode(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value or "").strip().lower()
        if not normalized:
            return None
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATION_MODES:
            raise ValueError(
                "workflows.granularities.*.translation must be one of: auto, off"
            )
        return normalized

    @field_validator("translate_include", mode="before")
    @classmethod
    def _parse_translate_include(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("on_translate_failure", mode="before")
    @classmethod
    def _normalize_translate_failure_policy(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value or "").strip().lower()
        if not normalized:
            return None
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATE_FAILURE:
            raise ValueError(
                "workflows.granularities.*.on_translate_failure must be one of: fail, partial_success, skip"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_translate_include(self) -> "WorkflowPolicyOverrideConfig":
        if self.translate_include is not None:
            self.translate_include = _normalize_workflow_translate_include(
                self.translate_include,
                field_name="workflows.granularities.*.translate_include",
            )
        return self

    def resolved(self, *, default: WorkflowPolicyConfig) -> WorkflowPolicyConfig:
        return WorkflowPolicyConfig(
            recursive_lower_levels=(
                default.recursive_lower_levels
                if self.recursive_lower_levels is None
                else self.recursive_lower_levels
            ),
            delivery_mode=default.delivery_mode
            if self.delivery_mode is None
            else self.delivery_mode,
            translation=default.translation
            if self.translation is None
            else self.translation,
            translate_include=(
                list(default.translate_include)
                if self.translate_include is None
                else list(self.translate_include)
            ),
            site_build=default.site_build
            if self.site_build is None
            else self.site_build,
            on_translate_failure=(
                default.on_translate_failure
                if self.on_translate_failure is None
                else self.on_translate_failure
            ),
        )


class GranularityWorkflowConfig(BaseModel):
    default: WorkflowPolicyConfig = Field(default_factory=WorkflowPolicyConfig)
    day: WorkflowPolicyOverrideConfig = Field(
        default_factory=WorkflowPolicyOverrideConfig
    )
    week: WorkflowPolicyOverrideConfig = Field(
        default_factory=WorkflowPolicyOverrideConfig
    )
    month: WorkflowPolicyOverrideConfig = Field(
        default_factory=WorkflowPolicyOverrideConfig
    )


class DeployWorkflowConfig(BaseModel):
    translation: str = "auto"
    translate_include: list[str] = Field(
        default_factory=lambda: ["items", "trends", "ideas"]
    )
    site_build: bool = True
    on_translate_failure: str = "partial_success"

    @field_validator("translation", mode="before")
    @classmethod
    def _normalize_translation_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower() or "auto"
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATION_MODES:
            raise ValueError("workflows.deploy.translation must be one of: auto, off")
        return normalized

    @field_validator("translate_include", mode="before")
    @classmethod
    def _parse_translate_include(cls, value: Any) -> Any:
        if value is None:
            return ["items", "trends", "ideas"]
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("on_translate_failure", mode="before")
    @classmethod
    def _normalize_translate_failure_policy(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower() or "partial_success"
        if normalized not in _ALLOWED_WORKFLOW_TRANSLATE_FAILURE:
            raise ValueError(
                "workflows.deploy.on_translate_failure must be one of: fail, partial_success, skip"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_translate_include(self) -> "DeployWorkflowConfig":
        self.translate_include = _normalize_workflow_translate_include(
            self.translate_include,
            field_name="workflows.deploy.translate_include",
        )
        return self


class WorkflowsConfig(BaseModel):
    granularities: GranularityWorkflowConfig = Field(
        default_factory=GranularityWorkflowConfig
    )
    deploy: DeployWorkflowConfig = Field(default_factory=DeployWorkflowConfig)

    def policy_for_granularity(self, granularity: str) -> WorkflowPolicyConfig:
        normalized = str(granularity or "").strip().lower()
        if normalized not in {"day", "week", "month"}:
            raise ValueError("workflow granularity must be one of: day, week, month")
        overrides = getattr(self.granularities, normalized)
        return overrides.resolved(default=self.granularities.default)


class DaemonScheduleConfig(BaseModel):
    workflow: str
    interval_minutes: int | None = Field(default=None, ge=1)
    weekday: str | None = None
    hour_utc: int | None = Field(default=None, ge=0, le=23)
    minute_utc: int | None = Field(default=None, ge=0, le=59)

    @field_validator("workflow", mode="before")
    @classmethod
    def _normalize_workflow(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in {"day", "week", "month", "deploy", "now"}:
            raise ValueError(
                "daemon.schedules.workflow must be one of: now, day, week, month, deploy"
            )
        return normalized

    @field_validator("weekday", mode="before")
    @classmethod
    def _normalize_weekday(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value or "").strip().lower()
        if not normalized:
            return None
        if normalized not in _ALLOWED_DAEMON_WEEKDAYS:
            raise ValueError(
                "daemon.schedules.weekday must be one of: mon, tue, wed, thu, fri, sat, sun"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_schedule_shape(self) -> "DaemonScheduleConfig":
        has_interval = self.interval_minutes is not None
        has_weekly = (
            self.weekday is not None
            or self.hour_utc is not None
            or self.minute_utc is not None
        )
        if has_interval and has_weekly:
            raise ValueError(
                "daemon.schedules entries must use either interval_minutes or weekday/hour_utc/minute_utc"
            )
        if has_interval:
            return self
        if self.weekday is None or self.hour_utc is None or self.minute_utc is None:
            raise ValueError(
                "daemon.schedules weekly entries require weekday, hour_utc, and minute_utc"
            )
        return self


class DaemonConfig(BaseModel):
    schedules: list[DaemonScheduleConfig] = Field(default_factory=list)


class EmailConfig(BaseModel):
    public_site_url: str
    from_email: str
    from_name: str | None = "Recoleta"
    to: list[str]
    granularity: str
    language_code: str | None = None
    max_clusters: int = Field(default=3, ge=1)
    max_evidence_per_cluster: int = Field(default=2, ge=1)
    subject_prefix: str | None = "[Recoleta]"

    @field_validator("to", mode="before")
    @classmethod
    def _parse_to(cls, value: Any) -> Any:
        if value is None:
            return value
        if isinstance(value, str):
            return _parse_str_list(value)
        return value

    @field_validator(
        "public_site_url",
        "from_email",
        "from_name",
        "language_code",
        "subject_prefix",
        mode="before",
    )
    @classmethod
    def _normalize_single_line_fields(cls, value: Any, info: ValidationInfo) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        if not normalized:
            return None
        if "\n" in normalized or "\r" in normalized:
            raise ValueError(f"{info.field_name} must be a single-line value")
        if info.field_name == "public_site_url":
            return normalized.rstrip("/")
        return normalized

    @field_validator("to", mode="after")
    @classmethod
    def _normalize_recipients(cls, value: list[Any]) -> list[str]:
        recipients: list[str] = []
        seen: set[str] = set()
        for item in list(value or []):
            normalized = str(item).strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            recipients.append(normalized)
        if not recipients:
            raise ValueError("EMAIL.to must contain at least one recipient")
        return recipients

    @field_validator("granularity", mode="before")
    @classmethod
    def _normalize_granularity(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if normalized not in {"day", "week", "month"}:
            raise ValueError("EMAIL.granularity must be one of: day, week, month")
        return normalized

    @model_validator(mode="after")
    def _validate_required_fields(self) -> "EmailConfig":
        if not self.public_site_url:
            raise ValueError("EMAIL.public_site_url is required")
        if not self.from_email:
            raise ValueError("EMAIL.from_email is required")
        return self


class _ConfigFileSettingsSource(PydanticBaseSettingsSource):
    _KEY_MAP: dict[str, str] = {
        "OBSIDIAN_VAULT_PATH": "obsidian_vault_path",
        "RECOLETA_DB_PATH": "recoleta_db_path",
        "LLM_MODEL": "llm_model",
        "LLM_OUTPUT_LANGUAGE": "llm_output_language",
        "RECOLETA_LLM_BASE_URL": "llm_base_url",
        "SOURCES": "sources",
        "TOPICS": "topics",
        "ALLOW_TAGS": "allow_tags",
        "DENY_TAGS": "deny_tags",
        "MIN_RELEVANCE_SCORE": "min_relevance_score",
        "MAX_DELIVERIES_PER_DAY": "max_deliveries_per_day",
        "TITLE_DEDUP_THRESHOLD": "title_dedup_threshold",
        "TITLE_DEDUP_MAX_CANDIDATES": "title_dedup_max_candidates",
        "TRIAGE_ENABLED": "triage_enabled",
        "TRIAGE_MODE": "triage_mode",
        "TRIAGE_EMBEDDING_MODEL": "triage_embedding_model",
        "TRIAGE_EMBEDDING_DIMENSIONS": "triage_embedding_dimensions",
        "TRIAGE_EMBEDDING_BATCH_MAX_INPUTS": "triage_embedding_batch_max_inputs",
        "TRIAGE_EMBEDDING_BATCH_MAX_CHARS": "triage_embedding_batch_max_chars",
        "TRIAGE_QUERY_MODE": "triage_query_mode",
        "TRIAGE_CANDIDATE_FACTOR": "triage_candidate_factor",
        "TRIAGE_MAX_CANDIDATES": "triage_max_candidates",
        "TRIAGE_ITEM_TEXT_MAX_CHARS": "triage_item_text_max_chars",
        "TRIAGE_MIN_SIMILARITY": "triage_min_similarity",
        "TRIAGE_EXPLORATION_RATE": "triage_exploration_rate",
        "TRIAGE_RECENCY_FLOOR": "triage_recency_floor",
        "ANALYZE_LIMIT": "analyze_limit",
        "ANALYZE_MAX_CONCURRENCY": "analyze_max_concurrency",
        "ANALYZE_WRITE_BATCH_SIZE": "analyze_write_batch_size",
        "ANALYZE_CONTENT_MAX_CHARS": "analyze_content_max_chars",
        "ARTIFACTS_DIR": "artifacts_dir",
        "OBSIDIAN_BASE_FOLDER": "obsidian_base_folder",
        "PUBLISH_TARGETS": "publish_targets",
        "MARKDOWN_OUTPUT_DIR": "markdown_output_dir",
        "LOG_LEVEL": "log_level",
        "LOG_JSON": "log_json",
        "WRITE_DEBUG_ARTIFACTS": "write_debug_artifacts",
        "RAG_LANCEDB_DIR": "rag_lancedb_dir",
        "TRENDS_EMBEDDING_MODEL": "trends_embedding_model",
        "TRENDS_EMBEDDING_DIMENSIONS": "trends_embedding_dimensions",
        "TRENDS_EMBEDDING_BATCH_MAX_INPUTS": "trends_embedding_batch_max_inputs",
        "TRENDS_EMBEDDING_BATCH_MAX_CHARS": "trends_embedding_batch_max_chars",
        "TRENDS_EMBEDDING_FAILURE_MODE": "trends_embedding_failure_mode",
        "TRENDS_EMBEDDING_MAX_ERRORS": "trends_embedding_max_errors",
        "TRENDS_SELF_SIMILAR_ENABLED": "trends_self_similar_enabled",
        "TRENDS_RANKING_N": "trends_ranking_n",
        "TRENDS_OVERVIEW_PACK_MAX_CHARS": "trends_overview_pack_max_chars",
        "TRENDS_ITEM_OVERVIEW_TOP_K": "trends_item_overview_top_k",
        "TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS": "trends_item_overview_item_max_chars",
        "TRENDS_REP_MIN_PER_CLUSTER": "trends_rep_min_per_cluster",
        "TRENDS_PEER_HISTORY_ENABLED": "trends_peer_history_enabled",
        "TRENDS_PEER_HISTORY_WINDOW_COUNT": "trends_peer_history_window_count",
        "TRENDS_PEER_HISTORY_MAX_CHARS": "trends_peer_history_max_chars",
        "TRENDS_EVOLUTION_MAX_SIGNALS": "trends_evolution_max_signals",
        "LOCALIZATION": "localization",
        "WORKFLOWS": "workflows",
        "DAEMON": "daemon",
        "EMAIL": "email",
    }
    _FORBIDDEN_TOP_LEVEL_KEYS = {
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "RECOLETA_LLM_API_KEY",
        "RECOLETA_RESEND_API_KEY",
        "telegram_bot_token",
        "telegram_chat_id",
        "llm_api_key",
        "resend_api_key",
    }
    _UNSUPPORTED_TOP_LEVEL_KEYS = set(_UNSUPPORTED_TOPIC_STREAM_FILE_KEYS)

    def __init__(self, settings_cls: type[BaseSettings]) -> None:
        super().__init__(settings_cls)
        self._data: dict[str, Any] | None = None

    def _resolve_config_path(self) -> Path | None:
        candidate = None
        try:
            state = self.current_state or {}
            candidate = state.get("config_path") or state.get("RECOLETA_CONFIG_PATH")
        except Exception:
            candidate = None
        if candidate is None:
            raw_path = os.getenv("RECOLETA_CONFIG_PATH", "").strip()
            if not raw_path:
                return None
            candidate = raw_path
        return Path(str(candidate)).expanduser().resolve()

    def _load_config_file(self) -> dict[str, Any]:
        config_path = self._resolve_config_path()
        if config_path is None:
            return {}
        self._validate_config_path(config_path)
        loaded = self._read_config_file(config_path)
        normalized = self._normalize_loaded_config(loaded)
        self._reject_disallowed_config_keys(normalized)
        return self._map_config_keys(normalized)

    @staticmethod
    def _validate_config_path(config_path: Path) -> None:
        if not config_path.exists():
            raise ValueError(f"RECOLETA_CONFIG_PATH does not exist: {config_path}")
        if not config_path.is_file():
            raise ValueError(f"RECOLETA_CONFIG_PATH must be a file: {config_path}")

    @staticmethod
    def _read_config_file(config_path: Path) -> Any:
        suffix = config_path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            return yaml.safe_load(config_path.read_text(encoding="utf-8"))
        if suffix == ".json":
            return json.loads(config_path.read_text(encoding="utf-8"))
        raise ValueError(
            f"Unsupported config file type: {config_path.suffix} (expected .yaml/.yml/.json)"
        )

    @staticmethod
    def _normalize_loaded_config(loaded: Any) -> dict[str, Any]:
        if loaded is None:
            return {}
        if not isinstance(loaded, dict):
            raise ValueError(
                "Config file must contain a mapping/object at the top level"
            )
        return loaded

    def _reject_disallowed_config_keys(self, loaded: dict[str, Any]) -> None:
        deprecated_scheduler_keys = self._collect_deprecated_scheduler_keys(loaded)
        if deprecated_scheduler_keys:
            raise ValueError(
                _legacy_scheduler_interval_message(deprecated_scheduler_keys)
            )
        unsupported_keys = self._collect_unsupported_top_level_keys(loaded)
        if unsupported_keys:
            raise ValueError(_unsupported_config_format_message(unsupported_keys))
        self._reject_forbidden_top_level_keys(loaded)

    @staticmethod
    def _collect_deprecated_scheduler_keys(loaded: dict[str, Any]) -> list[str]:
        return [
            key
            for key in loaded
            if isinstance(key, str)
            and key.upper() in _DEPRECATED_SCHEDULER_INTERVAL_KEYS
        ]

    def _collect_unsupported_top_level_keys(self, loaded: dict[str, Any]) -> list[str]:
        return [
            key
            for key in loaded
            if isinstance(key, str) and key in self._UNSUPPORTED_TOP_LEVEL_KEYS
        ]

    def _reject_forbidden_top_level_keys(self, loaded: dict[str, Any]) -> None:
        for key in loaded:
            if key in self._FORBIDDEN_TOP_LEVEL_KEYS:
                raise ValueError(
                    f"Secrets must come from environment variables only: {key}"
                )

    def _map_config_keys(self, loaded: dict[str, Any]) -> dict[str, Any]:
        mapped: dict[str, Any] = {}
        for key, value in loaded.items():
            if not isinstance(key, str):
                raise ValueError("Config file keys must be strings")
            mapped_key = self._KEY_MAP.get(key, key)
            self._reject_mapped_secret_key(raw_key=key, mapped_key=mapped_key)
            mapped[mapped_key] = value
        return mapped

    @staticmethod
    def _reject_mapped_secret_key(*, raw_key: str, mapped_key: str) -> None:
        if mapped_key in {"telegram_bot_token", "telegram_chat_id", "resend_api_key"}:
            raise ValueError(
                f"Secrets must come from environment variables only: {raw_key}"
            )

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> tuple[Any, str, bool]:  # noqa: ARG002
        if self._data is None:
            self._data = self._load_config_file()
        return self._data.get(field_name), field_name, False

    def prepare_field_value(  # noqa: PLR6301
        self,
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,  # noqa: ARG002
    ) -> Any:
        return value

    def __call__(self) -> dict[str, Any]:
        if self._data is None:
            self._data = self._load_config_file()
        collected: dict[str, Any] = {}
        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                collected[field_key] = field_value
        return collected


class ArxivSourceConfig(BaseModel):
    enabled: bool = False
    queries: list[str] = Field(default_factory=list)
    max_results_per_run: int = 50
    max_total_per_run: int | None = Field(default=None, ge=1, le=2000)
    enrich_method: str = Field(default="html_document")
    enrich_failure_mode: str = Field(default="fallback")
    html_document_max_concurrency: int = Field(default=4, ge=1, le=32)
    html_document_enable_parallel: bool = True
    html_document_skip_cleanup_when_complete: bool = True
    html_document_use_batched_db_writes: bool = True
    html_document_requests_per_second: float = Field(default=2.0, gt=0.0, le=20.0)
    html_document_log_sample_rate: float = Field(default=0.05, ge=0.0, le=1.0)

    @field_validator("enrich_method", mode="before")
    @classmethod
    def _normalize_enrich_method(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if not normalized:
            return "html_document"
        if normalized not in _ALLOWED_ARXIV_ENRICH_METHODS:
            raise ValueError(
                "SOURCES.arxiv.enrich_method must be one of: pdf_text, latex_source, html_document"
            )
        return normalized

    @field_validator("enrich_failure_mode", mode="before")
    @classmethod
    def _normalize_enrich_failure_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if not normalized:
            return "fallback"
        if normalized not in _ALLOWED_ARXIV_ENRICH_FAILURE_MODES:
            raise ValueError(
                "SOURCES.arxiv.enrich_failure_mode must be one of: fallback, strict"
            )
        return normalized

    @model_validator(mode="after")
    def _validate_enabled_requires_queries(self) -> "ArxivSourceConfig":
        fields_set = set(getattr(self, "model_fields_set", set()) or set())
        configured_without_enable = bool(fields_set - {"enabled"}) and not bool(
            self.enabled
        )
        if configured_without_enable:
            raise ValueError(
                "SOURCES.arxiv is configured but disabled; set SOURCES.arxiv.enabled=true (or remove the arxiv block)."
            )
        if self.enabled and not [q for q in self.queries if str(q).strip()]:
            raise ValueError(
                "SOURCES.arxiv.queries is required when SOURCES.arxiv.enabled=true"
            )
        self.queries = [str(q).strip() for q in self.queries if str(q).strip()]
        return self


class HNSourceConfig(BaseModel):
    enabled: bool = False
    rss_urls: list[str] = Field(
        default_factory=lambda: ["https://news.ycombinator.com/rss"]
    )
    max_items_per_feed: int = Field(default=50, ge=1, le=500)
    max_total_per_run: int | None = Field(default=None, ge=1, le=2000)

    @model_validator(mode="after")
    def _validate_enabled_requires_urls(self) -> "HNSourceConfig":
        fields_set = set(getattr(self, "model_fields_set", set()) or set())
        configured_without_enable = bool(fields_set - {"enabled"}) and not bool(
            self.enabled
        )
        if configured_without_enable:
            raise ValueError(
                "SOURCES.hn is configured but disabled; set SOURCES.hn.enabled=true (or remove the hn block)."
            )
        if self.enabled and not [u for u in self.rss_urls if str(u).strip()]:
            raise ValueError(
                "SOURCES.hn.rss_urls must be non-empty when SOURCES.hn.enabled=true"
            )
        self.rss_urls = [str(u).strip() for u in self.rss_urls if str(u).strip()]
        return self


class HFDailySourceConfig(BaseModel):
    enabled: bool = False
    max_items_per_run: int = Field(default=50, ge=1, le=500)

    @model_validator(mode="after")
    def _validate_enabled_flag(self) -> "HFDailySourceConfig":
        fields_set = set(getattr(self, "model_fields_set", set()) or set())
        configured_without_enable = bool(fields_set - {"enabled"}) and not bool(
            self.enabled
        )
        if configured_without_enable:
            raise ValueError(
                "SOURCES.hf_daily is configured but disabled; set SOURCES.hf_daily.enabled=true (or remove the hf_daily block)."
            )
        return self


class OpenReviewSourceConfig(BaseModel):
    enabled: bool = False
    venues: list[str] = Field(default_factory=list)
    max_results_per_venue: int = Field(default=50, ge=1, le=500)
    max_total_per_run: int | None = Field(default=None, ge=1, le=2000)

    @model_validator(mode="after")
    def _validate_enabled_requires_venues(self) -> "OpenReviewSourceConfig":
        fields_set = set(getattr(self, "model_fields_set", set()) or set())
        configured_without_enable = bool(fields_set - {"enabled"}) and not bool(
            self.enabled
        )
        if configured_without_enable:
            raise ValueError(
                "SOURCES.openreview is configured but disabled; set SOURCES.openreview.enabled=true (or remove the openreview block)."
            )
        if self.enabled and not [v for v in self.venues if str(v).strip()]:
            raise ValueError(
                "SOURCES.openreview.venues is required when SOURCES.openreview.enabled=true"
            )
        self.venues = [str(v).strip() for v in self.venues if str(v).strip()]
        return self


class RSSSourceConfig(BaseModel):
    enabled: bool = False
    feeds: list[str] = Field(default_factory=list)
    max_items_per_feed: int = Field(default=50, ge=1, le=500)
    max_total_per_run: int | None = Field(default=None, ge=1, le=2000)

    @model_validator(mode="after")
    def _validate_enabled_requires_feeds(self) -> "RSSSourceConfig":
        fields_set = set(getattr(self, "model_fields_set", set()) or set())
        configured_without_enable = bool(fields_set - {"enabled"}) and not bool(
            self.enabled
        )
        if configured_without_enable:
            raise ValueError(
                "SOURCES.rss is configured but disabled; set SOURCES.rss.enabled=true (or remove the rss block)."
            )
        if self.enabled and not [f for f in self.feeds if str(f).strip()]:
            raise ValueError(
                "SOURCES.rss.feeds is required when SOURCES.rss.enabled=true"
            )
        self.feeds = [str(f).strip() for f in self.feeds if str(f).strip()]
        return self


class SourcesConfig(BaseModel):
    arxiv: ArxivSourceConfig = Field(default_factory=ArxivSourceConfig)
    hn: HNSourceConfig = Field(default_factory=HNSourceConfig)
    hf_daily: HFDailySourceConfig = Field(default_factory=HFDailySourceConfig)
    openreview: OpenReviewSourceConfig = Field(default_factory=OpenReviewSourceConfig)
    rss: RSSSourceConfig = Field(default_factory=RSSSourceConfig)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        enable_decoding=False,
        extra="ignore",
        case_sensitive=False,
        validate_by_alias=True,
        validate_by_name=True,
    )

    config_path: Path | None = Field(
        default=None, validation_alias="RECOLETA_CONFIG_PATH"
    )
    recoleta_db_path: Path = Field(validation_alias="RECOLETA_DB_PATH")
    llm_model: str = Field(validation_alias="LLM_MODEL")
    llm_output_language: str | None = Field(
        default=None, validation_alias="LLM_OUTPUT_LANGUAGE"
    )
    localization: LocalizationConfig | None = Field(
        default=None, validation_alias="LOCALIZATION"
    )
    workflows: WorkflowsConfig = Field(
        default_factory=WorkflowsConfig, validation_alias="WORKFLOWS"
    )
    daemon: DaemonConfig = Field(
        default_factory=DaemonConfig, validation_alias="DAEMON"
    )
    email: EmailConfig | None = Field(default=None, validation_alias="EMAIL")
    legacy_ingest_interval_minutes: int | None = Field(
        default=None,
        validation_alias="INGEST_INTERVAL_MINUTES",
        exclude=True,
        repr=False,
    )
    legacy_analyze_interval_minutes: int | None = Field(
        default=None,
        validation_alias="ANALYZE_INTERVAL_MINUTES",
        exclude=True,
        repr=False,
    )
    legacy_publish_interval_minutes: int | None = Field(
        default=None,
        validation_alias="PUBLISH_INTERVAL_MINUTES",
        exclude=True,
        repr=False,
    )
    llm_api_key: SecretStr | None = Field(
        default=None, validation_alias="RECOLETA_LLM_API_KEY"
    )
    resend_api_key: SecretStr | None = Field(
        default=None, validation_alias="RECOLETA_RESEND_API_KEY"
    )
    llm_base_url: str | None = Field(
        default=None, validation_alias="RECOLETA_LLM_BASE_URL"
    )

    obsidian_vault_path: Path | None = Field(
        default=None, validation_alias="OBSIDIAN_VAULT_PATH"
    )
    telegram_bot_token: SecretStr | None = Field(
        default=None, validation_alias="TELEGRAM_BOT_TOKEN"
    )
    telegram_chat_id: SecretStr | None = Field(
        default=None, validation_alias="TELEGRAM_CHAT_ID"
    )

    sources: SourcesConfig = Field(
        default_factory=SourcesConfig, validation_alias="SOURCES"
    )
    topics: list[str] = Field(default_factory=list, validation_alias="TOPICS")
    allow_tags: list[str] = Field(default_factory=list, validation_alias="ALLOW_TAGS")
    deny_tags: list[str] = Field(default_factory=list, validation_alias="DENY_TAGS")
    min_relevance_score: float = Field(
        default=0.6, validation_alias="MIN_RELEVANCE_SCORE"
    )
    max_deliveries_per_day: int = Field(
        default=10, validation_alias="MAX_DELIVERIES_PER_DAY"
    )
    title_dedup_threshold: float = Field(
        default=92.0, validation_alias="TITLE_DEDUP_THRESHOLD"
    )
    title_dedup_max_candidates: int = Field(
        default=500,
        ge=0,
        validation_alias="TITLE_DEDUP_MAX_CANDIDATES",
    )

    triage_enabled: bool = Field(default=False, validation_alias="TRIAGE_ENABLED")
    triage_mode: str = Field(default="prioritize", validation_alias="TRIAGE_MODE")
    triage_embedding_model: str = Field(
        default="text-embedding-3-small", validation_alias="TRIAGE_EMBEDDING_MODEL"
    )
    triage_embedding_dimensions: int | None = Field(
        default=None, validation_alias="TRIAGE_EMBEDDING_DIMENSIONS"
    )
    triage_embedding_batch_max_inputs: int = Field(
        default=64,
        ge=1,
        validation_alias="TRIAGE_EMBEDDING_BATCH_MAX_INPUTS",
    )
    triage_embedding_batch_max_chars: int = Field(
        default=40_000,
        ge=1,
        validation_alias="TRIAGE_EMBEDDING_BATCH_MAX_CHARS",
    )
    triage_query_mode: str = Field(
        default="joined", validation_alias="TRIAGE_QUERY_MODE"
    )
    triage_candidate_factor: int = Field(
        default=5, ge=1, validation_alias="TRIAGE_CANDIDATE_FACTOR"
    )
    triage_max_candidates: int = Field(
        default=500, ge=1, validation_alias="TRIAGE_MAX_CANDIDATES"
    )
    triage_item_text_max_chars: int = Field(
        default=1200, ge=1, validation_alias="TRIAGE_ITEM_TEXT_MAX_CHARS"
    )
    triage_min_similarity: float = Field(
        default=0.0, ge=0.0, le=1.0, validation_alias="TRIAGE_MIN_SIMILARITY"
    )
    triage_exploration_rate: float = Field(
        default=0.05,
        ge=0.0,
        le=1.0,
        validation_alias="TRIAGE_EXPLORATION_RATE",
    )
    triage_recency_floor: int = Field(
        default=5, ge=0, validation_alias="TRIAGE_RECENCY_FLOOR"
    )
    analyze_limit: int = Field(default=100, ge=1, validation_alias="ANALYZE_LIMIT")
    analyze_max_concurrency: int = Field(
        default=4,
        ge=1,
        le=32,
        validation_alias="ANALYZE_MAX_CONCURRENCY",
    )
    analyze_write_batch_size: int = Field(
        default=32,
        ge=1,
        le=256,
        validation_alias="ANALYZE_WRITE_BATCH_SIZE",
    )
    analyze_content_max_chars: int = Field(
        default=32_768, ge=0, validation_alias="ANALYZE_CONTENT_MAX_CHARS"
    )

    artifacts_dir: Path | None = Field(default=None, validation_alias="ARTIFACTS_DIR")
    obsidian_base_folder: str = Field(
        default="Recoleta", validation_alias="OBSIDIAN_BASE_FOLDER"
    )
    publish_targets: list[str] = Field(
        default_factory=lambda: ["markdown"], validation_alias="PUBLISH_TARGETS"
    )
    markdown_output_dir: Path = Field(
        default_factory=_default_markdown_output_dir,
        validation_alias="MARKDOWN_OUTPUT_DIR",
    )
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_json: bool = Field(default=False, validation_alias="LOG_JSON")
    write_debug_artifacts: bool = Field(
        default=False, validation_alias="WRITE_DEBUG_ARTIFACTS"
    )

    rag_lancedb_dir: Path = Field(
        default_factory=_default_lancedb_dir, validation_alias="RAG_LANCEDB_DIR"
    )
    trends_embedding_model: str = Field(
        default="text-embedding-3-small", validation_alias="TRENDS_EMBEDDING_MODEL"
    )
    trends_embedding_dimensions: int | None = Field(
        default=None, validation_alias="TRENDS_EMBEDDING_DIMENSIONS"
    )
    trends_embedding_batch_max_inputs: int = Field(
        default=64, ge=1, validation_alias="TRENDS_EMBEDDING_BATCH_MAX_INPUTS"
    )
    trends_embedding_batch_max_chars: int = Field(
        default=40_000, ge=1, validation_alias="TRENDS_EMBEDDING_BATCH_MAX_CHARS"
    )
    trends_embedding_failure_mode: str = Field(
        default="continue", validation_alias="TRENDS_EMBEDDING_FAILURE_MODE"
    )
    trends_embedding_max_errors: int = Field(
        default=0, ge=0, validation_alias="TRENDS_EMBEDDING_MAX_ERRORS"
    )
    trends_self_similar_enabled: bool = Field(
        default=False, validation_alias="TRENDS_SELF_SIMILAR_ENABLED"
    )
    trends_ranking_n: int = Field(default=10, ge=1, validation_alias="TRENDS_RANKING_N")
    trends_overview_pack_max_chars: int = Field(
        default=16000, ge=1, validation_alias="TRENDS_OVERVIEW_PACK_MAX_CHARS"
    )
    trends_item_overview_top_k: int = Field(
        default=28, ge=0, validation_alias="TRENDS_ITEM_OVERVIEW_TOP_K"
    )
    trends_item_overview_item_max_chars: int = Field(
        default=800, ge=1, validation_alias="TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS"
    )
    trends_rep_min_per_cluster: int = Field(
        default=2, ge=1, validation_alias="TRENDS_REP_MIN_PER_CLUSTER"
    )
    trends_peer_history_enabled: bool = Field(
        default=True, validation_alias="TRENDS_PEER_HISTORY_ENABLED"
    )
    trends_peer_history_window_count: int = Field(
        default=3, ge=0, validation_alias="TRENDS_PEER_HISTORY_WINDOW_COUNT"
    )
    trends_peer_history_max_chars: int = Field(
        default=12000, ge=1, validation_alias="TRENDS_PEER_HISTORY_MAX_CHARS"
    )
    trends_evolution_max_signals: int = Field(
        default=5, ge=1, validation_alias="TRENDS_EVOLUTION_MAX_SIGNALS"
    )

    @model_validator(mode="after")
    def _validate_debug_artifacts_require_artifacts_dir(self) -> "Settings":
        if self.write_debug_artifacts and self.artifacts_dir is None:
            raise ValueError(
                "ARTIFACTS_DIR is required when WRITE_DEBUG_ARTIFACTS=true"
            )
        return self

    @model_validator(mode="after")
    def _validate_trends_embedding_failure_policy(self) -> "Settings":
        mode = (
            str(self.trends_embedding_failure_mode or "").strip().lower() or "continue"
        )
        if mode not in _ALLOWED_TRENDS_EMBEDDING_FAILURE_MODES:
            raise ValueError(
                "TRENDS_EMBEDDING_FAILURE_MODE must be one of: continue, fail_fast, threshold"
            )
        self.trends_embedding_failure_mode = mode
        if mode == "threshold" and int(self.trends_embedding_max_errors or 0) <= 0:
            raise ValueError(
                "TRENDS_EMBEDDING_MAX_ERRORS must be > 0 when TRENDS_EMBEDDING_FAILURE_MODE=threshold"
            )
        return self

    @model_validator(mode="after")
    def _validate_localization_requires_llm_output_language(self) -> "Settings":
        if self.localization is not None and self.localization.targets:
            if not str(self.llm_output_language or "").strip():
                raise ValueError(
                    "LLM_OUTPUT_LANGUAGE is required when LOCALIZATION.targets are configured"
                )
        return self

    @model_validator(mode="after")
    def _reject_legacy_scheduler_intervals(self) -> "Settings":
        deprecated_keys: list[str] = []
        if self.legacy_ingest_interval_minutes is not None:
            deprecated_keys.append("INGEST_INTERVAL_MINUTES")
        if self.legacy_analyze_interval_minutes is not None:
            deprecated_keys.append("ANALYZE_INTERVAL_MINUTES")
        if self.legacy_publish_interval_minutes is not None:
            deprecated_keys.append("PUBLISH_INTERVAL_MINUTES")
        if deprecated_keys:
            raise ValueError(_legacy_scheduler_interval_message(deprecated_keys))
        return self

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        _reject_unsupported_topic_stream_environment(settings_cls)
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            _ConfigFileSettingsSource(settings_cls),
            file_secret_settings,
        )

    @field_validator("sources", mode="before")
    @classmethod
    def _parse_sources_from_env_string(cls, value: Any) -> Any:
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, dict):
                raise ValueError("SOURCES must be a JSON/YAML object")
            return loaded
        return value

    @field_validator("localization", mode="before")
    @classmethod
    def _parse_localization_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, dict):
                raise ValueError("LOCALIZATION must be a JSON/YAML object")
            return loaded
        return value

    @field_validator("workflows", mode="before")
    @classmethod
    def _parse_workflows_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, dict):
                raise ValueError("WORKFLOWS must be a JSON/YAML object")
            return loaded
        return value

    @field_validator("daemon", mode="before")
    @classmethod
    def _parse_daemon_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, dict):
                raise ValueError("DAEMON must be a JSON/YAML object")
            return loaded
        return value

    @field_validator("email", mode="before")
    @classmethod
    def _parse_email_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, dict):
                raise ValueError("EMAIL must be a JSON/YAML object")
            return loaded
        return value

    @field_validator(
        "legacy_ingest_interval_minutes",
        "legacy_analyze_interval_minutes",
        "legacy_publish_interval_minutes",
        mode="before",
    )
    @classmethod
    def _normalize_legacy_scheduler_interval(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            value = stripped
        return int(value)

    @field_validator("publish_targets", mode="before")
    @classmethod
    def _parse_publish_targets_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            return _parse_str_list(value)
        return value

    @field_validator("llm_output_language", mode="before")
    @classmethod
    def _normalize_llm_output_language(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        if not normalized:
            return None
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("LLM_OUTPUT_LANGUAGE must be a single-line value")
        if len(normalized) > 64:
            raise ValueError("LLM_OUTPUT_LANGUAGE must be <= 64 characters")
        return normalized

    @field_validator("llm_api_key", mode="before")
    @classmethod
    def _normalize_llm_api_key(cls, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, SecretStr):
            normalized = value.get_secret_value().strip()
        else:
            normalized = str(value).strip()
        if not normalized:
            return None
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("RECOLETA_LLM_API_KEY must be a single-line value")
        if len(normalized) > 4096:
            raise ValueError("RECOLETA_LLM_API_KEY must be <= 4096 characters")
        return normalized

    @field_validator("resend_api_key", mode="before")
    @classmethod
    def _normalize_resend_api_key(cls, value: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, SecretStr):
            normalized = value.get_secret_value().strip()
        else:
            normalized = str(value).strip()
        if not normalized:
            return None
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("RECOLETA_RESEND_API_KEY must be a single-line value")
        if len(normalized) > 4096:
            raise ValueError("RECOLETA_RESEND_API_KEY must be <= 4096 characters")
        return normalized

    @field_validator("llm_base_url", mode="before")
    @classmethod
    def _normalize_llm_base_url(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip()
        if not normalized:
            return None
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("RECOLETA_LLM_BASE_URL must be a single-line value")
        if len(normalized) > 2048:
            raise ValueError("RECOLETA_LLM_BASE_URL must be <= 2048 characters")
        return normalized

    @field_validator("topics", mode="before")
    @classmethod
    def _parse_topics_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("allow_tags", mode="before")
    @classmethod
    def _parse_allow_tags_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("deny_tags", mode="before")
    @classmethod
    def _parse_deny_tags_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("triage_mode", mode="before")
    @classmethod
    def _normalize_triage_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if not normalized:
            return "prioritize"
        if normalized not in {"prioritize", "filter"}:
            raise ValueError("TRIAGE_MODE must be one of: prioritize, filter")
        return normalized

    @field_validator("triage_query_mode", mode="before")
    @classmethod
    def _normalize_triage_query_mode(cls, value: Any) -> str:
        normalized = str(value or "").strip().lower()
        if not normalized:
            return "joined"
        if normalized not in {"joined", "max_per_topic"}:
            raise ValueError("TRIAGE_QUERY_MODE must be one of: joined, max_per_topic")
        return normalized

    @field_validator("triage_embedding_model", mode="before")
    @classmethod
    def _normalize_triage_embedding_model(cls, value: Any) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            return "text-embedding-3-small"
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("TRIAGE_EMBEDDING_MODEL must be a single-line value")
        if len(normalized) > 128:
            raise ValueError("TRIAGE_EMBEDDING_MODEL must be <= 128 characters")
        return normalized

    @field_validator("triage_embedding_dimensions", mode="before")
    @classmethod
    def _normalize_triage_embedding_dimensions(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("TRIAGE_EMBEDDING_DIMENSIONS must be an integer") from exc
        if parsed <= 0:
            raise ValueError("TRIAGE_EMBEDDING_DIMENSIONS must be a positive integer")
        return parsed

    @field_validator("triage_embedding_batch_max_inputs", mode="before")
    @classmethod
    def _normalize_triage_embedding_batch_max_inputs(cls, value: Any) -> int:
        if value is None:
            return 64
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return 64
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                "TRIAGE_EMBEDDING_BATCH_MAX_INPUTS must be an integer"
            ) from exc
        if parsed <= 0:
            raise ValueError(
                "TRIAGE_EMBEDDING_BATCH_MAX_INPUTS must be a positive integer"
            )
        return parsed

    @field_validator("triage_embedding_batch_max_chars", mode="before")
    @classmethod
    def _normalize_triage_embedding_batch_max_chars(cls, value: Any) -> int:
        if value is None:
            return 40_000
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return 40_000
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                "TRIAGE_EMBEDDING_BATCH_MAX_CHARS must be an integer"
            ) from exc
        if parsed <= 0:
            raise ValueError(
                "TRIAGE_EMBEDDING_BATCH_MAX_CHARS must be a positive integer"
            )
        return parsed

    @field_validator("obsidian_vault_path", mode="before")
    @classmethod
    def _normalize_vault_path(cls, value: str | Path | None) -> Path | None:
        if value is None:
            return None
        path = Path(value).expanduser().resolve()
        if not path.is_absolute():
            raise ValueError("OBSIDIAN_VAULT_PATH must be an absolute path")
        return path

    @field_validator("recoleta_db_path", mode="before")
    @classmethod
    def _normalize_db_path(cls, value: str | Path) -> Path:
        return Path(value).expanduser().resolve()

    @field_validator("artifacts_dir", mode="before")
    @classmethod
    def _normalize_optional_path(cls, value: str | Path | None) -> Path | None:
        if value is None:
            return None
        return Path(value).expanduser().resolve()

    @field_validator("rag_lancedb_dir", mode="before")
    @classmethod
    def _normalize_lancedb_dir(cls, value: str | Path | None) -> Path:
        if value is None:
            return _default_lancedb_dir()
        return Path(value).expanduser().resolve()

    @field_validator("trends_embedding_model", mode="before")
    @classmethod
    def _normalize_trends_embedding_model(cls, value: Any) -> str:
        normalized = str(value or "").strip()
        if not normalized:
            return "text-embedding-3-small"
        if "\n" in normalized or "\r" in normalized:
            raise ValueError("TRENDS_EMBEDDING_MODEL must be a single-line value")
        if len(normalized) > 128:
            raise ValueError("TRENDS_EMBEDDING_MODEL must be <= 128 characters")
        return normalized

    @field_validator("trends_embedding_dimensions", mode="before")
    @classmethod
    def _normalize_trends_embedding_dimensions(cls, value: Any) -> int | None:
        if value is None:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return None
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError("TRENDS_EMBEDDING_DIMENSIONS must be an integer") from exc
        if parsed <= 0:
            raise ValueError("TRENDS_EMBEDDING_DIMENSIONS must be a positive integer")
        return parsed

    @field_validator("trends_embedding_batch_max_inputs", mode="before")
    @classmethod
    def _normalize_trends_embedding_batch_max_inputs(cls, value: Any) -> int:
        if value is None:
            return 64
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return 64
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                "TRENDS_EMBEDDING_BATCH_MAX_INPUTS must be an integer"
            ) from exc
        if parsed <= 0:
            raise ValueError(
                "TRENDS_EMBEDDING_BATCH_MAX_INPUTS must be a positive integer"
            )
        return parsed

    @field_validator("trends_embedding_batch_max_chars", mode="before")
    @classmethod
    def _normalize_trends_embedding_batch_max_chars(cls, value: Any) -> int:
        if value is None:
            return 40_000
        if isinstance(value, str):
            stripped = value.strip()
            if not stripped:
                return 40_000
            value = stripped
        try:
            parsed = int(value)
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                "TRENDS_EMBEDDING_BATCH_MAX_CHARS must be an integer"
            ) from exc
        if parsed <= 0:
            raise ValueError(
                "TRENDS_EMBEDDING_BATCH_MAX_CHARS must be a positive integer"
            )
        return parsed

    @field_validator("markdown_output_dir", mode="before")
    @classmethod
    def _normalize_markdown_output_dir(cls, value: str | Path | None) -> Path:
        if value is None:
            return _default_markdown_output_dir()
        return Path(value).expanduser().resolve()

    @field_validator("config_path", mode="before")
    @classmethod
    def _normalize_optional_config_path(cls, value: str | Path | None) -> Path | None:
        if value is None:
            return None
        return Path(value).expanduser().resolve()

    @model_validator(mode="after")
    def _validate_publish_targets(self) -> "Settings":
        self.publish_targets = _normalize_publish_targets(
            self.publish_targets,
            field_name="PUBLISH_TARGETS",
        )
        return self

    def workflow_policy_for_granularity(self, granularity: str) -> WorkflowPolicyConfig:
        return self.workflows.policy_for_granularity(granularity)

    def localization_target_codes(self) -> list[str]:
        if self.localization is None:
            return []
        return [target.code for target in self.localization.targets]

    def safe_model_dump(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        payload["llm_api_key"] = "***"
        payload["telegram_bot_token"] = "***"
        payload["telegram_chat_id"] = "***"
        payload["resend_api_key"] = "***"
        return payload

    def safe_fingerprint(self) -> str:
        payload = self.safe_model_dump()
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def llm_connection_config(self) -> LLMConnectionConfig:
        return LLMConnectionConfig(
            api_key=(
                self.llm_api_key.get_secret_value()
                if self.llm_api_key is not None
                else None
            ),
            base_url=self.llm_base_url,
        )
