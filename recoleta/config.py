from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
from typing import Any

from platformdirs import user_data_dir
from pydantic import BaseModel, Field, SecretStr, field_validator, model_validator
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
import yaml

from recoleta.llm_connection import LLMConnectionConfig
from recoleta.types import DEFAULT_TOPIC_STREAM


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
_ENV_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def _normalize_identifier(value: Any, *, field_name: str) -> str:
    raw = str(value or "").strip().lower()
    normalized = "".join(
        ch if (ch.isalnum() or ch in {"-", "_"}) else "-" for ch in raw
    )
    while "--" in normalized:
        normalized = normalized.replace("--", "-")
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("-_")
    if not normalized:
        raise ValueError(f"{field_name} must contain at least one letter or digit")
    if len(normalized) > 64:
        raise ValueError(f"{field_name} must be <= 64 characters")
    return normalized


def _normalize_topic_stream_token(value: str) -> str:
    lowered = str(value or "").strip().lower()
    normalized = "".join(ch if ch.isalnum() else "_" for ch in lowered)
    while "__" in normalized:
        normalized = normalized.replace("__", "_")
    normalized = normalized.strip("_")
    return normalized or "stream"


def _normalize_optional_env_name(value: Any, *, field_name: str) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    if not normalized:
        return None
    if "\n" in normalized or "\r" in normalized:
        raise ValueError(f"{field_name} must be a single-line value")
    if len(normalized) > 128:
        raise ValueError(f"{field_name} must be <= 128 characters")
    if _ENV_NAME_RE.fullmatch(normalized) is None:
        raise ValueError(f"{field_name} must be a valid environment variable name")
    return normalized


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


def _load_secret_from_env(env_name: str | None) -> SecretStr | None:
    if env_name is None:
        return None
    raw = os.getenv(env_name, "").strip()
    if not raw:
        return None
    return SecretStr(raw)


@dataclass(frozen=True, slots=True)
class TopicStreamRuntime:
    name: str
    topics: list[str]
    allow_tags: list[str]
    deny_tags: list[str]
    publish_targets: list[str]
    markdown_output_dir: Path
    obsidian_base_folder: str
    min_relevance_score: float
    max_deliveries_per_day: int
    telegram_bot_token: SecretStr | None
    telegram_chat_id: SecretStr | None
    explicit: bool


class TopicStreamConfig(BaseModel):
    name: str
    topics: list[str] = Field(default_factory=list)
    allow_tags: list[str] | None = None
    deny_tags: list[str] | None = None
    publish_targets: list[str] | None = None
    markdown_output_dir: Path | None = None
    obsidian_base_folder: str | None = None
    min_relevance_score: float | None = None
    max_deliveries_per_day: int | None = None
    telegram_bot_token_env: str | None = None
    telegram_chat_id_env: str | None = None

    @field_validator("name", mode="before")
    @classmethod
    def _normalize_name(cls, value: Any) -> str:
        return _normalize_identifier(value, field_name="topic_streams.name")

    @field_validator(
        "topics",
        "allow_tags",
        "deny_tags",
        mode="before",
    )
    @classmethod
    def _parse_string_list_fields(cls, value: Any, info: Any) -> Any:
        if value is None:
            return [] if info.field_name == "topics" else None
        if isinstance(value, str):
            return _parse_str_list(value)
        if isinstance(value, (list, tuple)):
            return [str(item).strip() for item in value if str(item).strip()]
        return value

    @field_validator("publish_targets", mode="before")
    @classmethod
    def _parse_publish_targets(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            return _parse_str_list(value)
        return value

    @field_validator("markdown_output_dir", mode="before")
    @classmethod
    def _normalize_markdown_output_dir(cls, value: str | Path | None) -> Path | None:
        if value is None:
            return None
        return Path(value).expanduser().resolve()

    @field_validator("obsidian_base_folder", mode="before")
    @classmethod
    def _normalize_obsidian_base_folder(cls, value: Any) -> str | None:
        if value is None:
            return None
        normalized = str(value).strip().strip("/")
        return normalized or None

    @field_validator(
        "telegram_bot_token_env",
        "telegram_chat_id_env",
        mode="before",
    )
    @classmethod
    def _normalize_env_names(cls, value: Any, info: Any) -> str | None:
        return _normalize_optional_env_name(
            value, field_name=f"topic_streams.{info.field_name}"
        )

    @model_validator(mode="after")
    def _validate_topic_stream(self) -> "TopicStreamConfig":
        if not self.topics:
            raise ValueError("topic_streams.topics must include at least one topic")
        if self.publish_targets is not None:
            self.publish_targets = _normalize_publish_targets(
                self.publish_targets,
                field_name="topic_streams.publish_targets",
            )
        if (self.telegram_bot_token_env is None) != (self.telegram_chat_id_env is None):
            raise ValueError(
                "topic_streams.telegram_bot_token_env and topic_streams.telegram_chat_id_env must be set together"
            )
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
        "TOPIC_STREAMS": "topic_streams",
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
        "ANALYZE_CONTENT_MAX_CHARS": "analyze_content_max_chars",
        "INGEST_INTERVAL_MINUTES": "ingest_interval_minutes",
        "ANALYZE_INTERVAL_MINUTES": "analyze_interval_minutes",
        "PUBLISH_INTERVAL_MINUTES": "publish_interval_minutes",
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
    }
    _FORBIDDEN_TOP_LEVEL_KEYS = {
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "RECOLETA_LLM_API_KEY",
        "telegram_bot_token",
        "telegram_chat_id",
        "llm_api_key",
    }

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

        if not config_path.exists():
            raise ValueError(f"RECOLETA_CONFIG_PATH does not exist: {config_path}")
        if not config_path.is_file():
            raise ValueError(f"RECOLETA_CONFIG_PATH must be a file: {config_path}")

        suffix = config_path.suffix.lower()
        if suffix in {".yaml", ".yml"}:
            loaded = yaml.safe_load(config_path.read_text(encoding="utf-8"))
        elif suffix == ".json":
            loaded = json.loads(config_path.read_text(encoding="utf-8"))
        else:
            raise ValueError(
                f"Unsupported config file type: {config_path.suffix} (expected .yaml/.yml/.json)"
            )

        if loaded is None:
            return {}
        if not isinstance(loaded, dict):
            raise ValueError(
                "Config file must contain a mapping/object at the top level"
            )

        for key in loaded:
            if key in self._FORBIDDEN_TOP_LEVEL_KEYS:
                raise ValueError(
                    f"Secrets must come from environment variables only: {key}"
                )

        mapped: dict[str, Any] = {}
        for key, value in loaded.items():
            if not isinstance(key, str):
                raise ValueError("Config file keys must be strings")
            mapped_key = self._KEY_MAP.get(key, key)
            if mapped_key in {"telegram_bot_token", "telegram_chat_id"}:
                raise ValueError(
                    f"Secrets must come from environment variables only: {key}"
                )
            mapped[mapped_key] = value
        return mapped

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
    llm_api_key: SecretStr | None = Field(
        default=None, validation_alias="RECOLETA_LLM_API_KEY"
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
    topic_streams: list[TopicStreamConfig] = Field(
        default_factory=list, validation_alias="TOPIC_STREAMS"
    )
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
    analyze_content_max_chars: int = Field(
        default=32_768, ge=0, validation_alias="ANALYZE_CONTENT_MAX_CHARS"
    )

    ingest_interval_minutes: int = Field(
        default=60, validation_alias="INGEST_INTERVAL_MINUTES"
    )
    analyze_interval_minutes: int = Field(
        default=120, validation_alias="ANALYZE_INTERVAL_MINUTES"
    )
    publish_interval_minutes: int = Field(
        default=120, validation_alias="PUBLISH_INTERVAL_MINUTES"
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
        default=8000, ge=1, validation_alias="TRENDS_OVERVIEW_PACK_MAX_CHARS"
    )
    trends_item_overview_top_k: int = Field(
        default=20, ge=0, validation_alias="TRENDS_ITEM_OVERVIEW_TOP_K"
    )
    trends_item_overview_item_max_chars: int = Field(
        default=500, ge=1, validation_alias="TRENDS_ITEM_OVERVIEW_ITEM_MAX_CHARS"
    )
    trends_rep_min_per_cluster: int = Field(
        default=2, ge=1, validation_alias="TRENDS_REP_MIN_PER_CLUSTER"
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

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
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

    @field_validator("topic_streams", mode="before")
    @classmethod
    def _parse_topic_streams_from_env_string(cls, value: Any) -> Any:
        if value is None:
            return []
        if isinstance(value, str):
            loaded = _parse_json_or_yaml(value)
            if not isinstance(loaded, list):
                raise ValueError("TOPIC_STREAMS must be a JSON/YAML list")
            return loaded
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

    @model_validator(mode="after")
    def _validate_topic_streams(self) -> "Settings":
        if self.topic_streams and self.topics:
            raise ValueError("TOPICS cannot be used together with TOPIC_STREAMS")
        if not self.topic_streams:
            return self
        names = [stream.name for stream in self.topic_streams]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            raise ValueError(
                "TOPIC_STREAMS names must be unique: " + ", ".join(duplicates)
            )
        token_names: dict[str, set[str]] = {}
        for stream in self.topic_streams:
            token = _normalize_topic_stream_token(stream.name)
            token_names.setdefault(token, set()).add(stream.name)
        colliding_names = sorted(
            {name for names in token_names.values() if len(names) > 1 for name in names}
        )
        if colliding_names:
            raise ValueError(
                "TOPIC_STREAMS names collide after downstream normalization: "
                + ", ".join(colliding_names)
            )
        return self

    def topic_stream_runtimes(self) -> list[TopicStreamRuntime]:
        if not self.topic_streams:
            return [
                TopicStreamRuntime(
                    name=DEFAULT_TOPIC_STREAM,
                    topics=list(self.topics),
                    allow_tags=list(self.allow_tags),
                    deny_tags=list(self.deny_tags),
                    publish_targets=list(self.publish_targets),
                    markdown_output_dir=self.markdown_output_dir,
                    obsidian_base_folder=self.obsidian_base_folder,
                    min_relevance_score=float(self.min_relevance_score),
                    max_deliveries_per_day=int(self.max_deliveries_per_day),
                    telegram_bot_token=self.telegram_bot_token,
                    telegram_chat_id=self.telegram_chat_id,
                    explicit=False,
                )
            ]

        runtimes: list[TopicStreamRuntime] = []
        streams_root = self.markdown_output_dir / "Streams"
        obsidian_streams_root = f"{self.obsidian_base_folder}/Streams"
        for stream in self.topic_streams:
            publish_targets = (
                list(stream.publish_targets)
                if stream.publish_targets is not None
                else list(self.publish_targets)
            )
            runtimes.append(
                TopicStreamRuntime(
                    name=stream.name,
                    topics=list(stream.topics),
                    allow_tags=(
                        list(stream.allow_tags)
                        if stream.allow_tags is not None
                        else list(self.allow_tags)
                    ),
                    deny_tags=(
                        list(stream.deny_tags)
                        if stream.deny_tags is not None
                        else list(self.deny_tags)
                    ),
                    publish_targets=publish_targets,
                    markdown_output_dir=(
                        stream.markdown_output_dir
                        if stream.markdown_output_dir is not None
                        else (streams_root / stream.name)
                    ),
                    obsidian_base_folder=(
                        stream.obsidian_base_folder
                        if stream.obsidian_base_folder is not None
                        else f"{obsidian_streams_root}/{stream.name}"
                    ),
                    min_relevance_score=float(
                        self.min_relevance_score
                        if stream.min_relevance_score is None
                        else stream.min_relevance_score
                    ),
                    max_deliveries_per_day=int(
                        self.max_deliveries_per_day
                        if stream.max_deliveries_per_day is None
                        else stream.max_deliveries_per_day
                    ),
                    telegram_bot_token=(
                        _load_secret_from_env(stream.telegram_bot_token_env)
                        if stream.telegram_bot_token_env is not None
                        else self.telegram_bot_token
                    ),
                    telegram_chat_id=(
                        _load_secret_from_env(stream.telegram_chat_id_env)
                        if stream.telegram_chat_id_env is not None
                        else self.telegram_chat_id
                    ),
                    explicit=True,
                )
            )
        return runtimes

    def safe_fingerprint(self) -> str:
        payload = self.model_dump(mode="json")
        payload["llm_api_key"] = "***"
        payload["telegram_bot_token"] = "***"
        payload["telegram_chat_id"] = "***"
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
