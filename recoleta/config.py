from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic.fields import FieldInfo
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict
import yaml


class _ConfigFileSettingsSource(PydanticBaseSettingsSource):
    _KEY_MAP: dict[str, str] = {
        "OBSIDIAN_VAULT_PATH": "obsidian_vault_path",
        "RECOLETA_DB_PATH": "recoleta_db_path",
        "LLM_MODEL": "llm_model",
        "SOURCES": "sources",
        "TOPICS": "topics",
        "MIN_RELEVANCE_SCORE": "min_relevance_score",
        "MAX_DELIVERIES_PER_DAY": "max_deliveries_per_day",
        "TITLE_DEDUP_THRESHOLD": "title_dedup_threshold",
        "TITLE_DEDUP_MAX_CANDIDATES": "title_dedup_max_candidates",
        "INGEST_INTERVAL_MINUTES": "ingest_interval_minutes",
        "ANALYZE_INTERVAL_MINUTES": "analyze_interval_minutes",
        "PUBLISH_INTERVAL_MINUTES": "publish_interval_minutes",
        "ARTIFACTS_DIR": "artifacts_dir",
        "OBSIDIAN_BASE_FOLDER": "obsidian_base_folder",
        "LOG_LEVEL": "log_level",
        "LOG_JSON": "log_json",
        "WRITE_DEBUG_ARTIFACTS": "write_debug_artifacts",
    }
    _FORBIDDEN_TOP_LEVEL_KEYS = {
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "telegram_bot_token",
        "telegram_chat_id",
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
            raise ValueError(f"Unsupported config file type: {config_path.suffix} (expected .yaml/.yml/.json)")

        if loaded is None:
            return {}
        if not isinstance(loaded, dict):
            raise ValueError("Config file must contain a mapping/object at the top level")

        for key in loaded:
            if key in self._FORBIDDEN_TOP_LEVEL_KEYS:
                raise ValueError(f"Secrets must come from environment variables only: {key}")

        mapped: dict[str, Any] = {}
        for key, value in loaded.items():
            if not isinstance(key, str):
                raise ValueError("Config file keys must be strings")
            mapped_key = self._KEY_MAP.get(key, key)
            if mapped_key in {"telegram_bot_token", "telegram_chat_id"}:
                raise ValueError(f"Secrets must come from environment variables only: {key}")
            mapped[mapped_key] = value
        return mapped

    def get_field_value(self, field: FieldInfo, field_name: str) -> tuple[Any, str, bool]:  # noqa: ARG002
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
            field_value, field_key, value_is_complex = self.get_field_value(field, field_name)
            field_value = self.prepare_field_value(field_name, field, field_value, value_is_complex)
            if field_value is not None:
                collected[field_key] = field_value
        return collected


class ArxivSourceConfig(BaseModel):
    queries: list[str] = Field(default_factory=list)
    max_results_per_run: int = 50


class HNSourceConfig(BaseModel):
    rss_urls: list[str] = Field(default_factory=lambda: ["https://news.ycombinator.com/rss"])


class HFDailySourceConfig(BaseModel):
    enabled: bool = False


class OpenReviewSourceConfig(BaseModel):
    venues: list[str] = Field(default_factory=list)


class RSSSourceConfig(BaseModel):
    feeds: list[str] = Field(default_factory=list)


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
        extra="ignore",
        case_sensitive=False,
        validate_by_alias=True,
        validate_by_name=True,
    )

    config_path: Path | None = Field(default=None, validation_alias="RECOLETA_CONFIG_PATH")
    obsidian_vault_path: Path = Field(validation_alias="OBSIDIAN_VAULT_PATH")
    recoleta_db_path: Path = Field(validation_alias="RECOLETA_DB_PATH")
    telegram_bot_token: SecretStr = Field(validation_alias="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: SecretStr = Field(validation_alias="TELEGRAM_CHAT_ID")
    llm_model: str = Field(validation_alias="LLM_MODEL")

    sources: SourcesConfig = Field(default_factory=SourcesConfig, validation_alias="SOURCES")
    topics: list[str] = Field(default_factory=list, validation_alias="TOPICS")
    min_relevance_score: float = Field(default=0.6, validation_alias="MIN_RELEVANCE_SCORE")
    max_deliveries_per_day: int = Field(default=10, validation_alias="MAX_DELIVERIES_PER_DAY")
    title_dedup_threshold: float = Field(default=92.0, validation_alias="TITLE_DEDUP_THRESHOLD")
    title_dedup_max_candidates: int = Field(
        default=500,
        ge=0,
        validation_alias="TITLE_DEDUP_MAX_CANDIDATES",
    )

    ingest_interval_minutes: int = Field(default=60, validation_alias="INGEST_INTERVAL_MINUTES")
    analyze_interval_minutes: int = Field(default=120, validation_alias="ANALYZE_INTERVAL_MINUTES")
    publish_interval_minutes: int = Field(default=120, validation_alias="PUBLISH_INTERVAL_MINUTES")

    artifacts_dir: Path | None = Field(default=None, validation_alias="ARTIFACTS_DIR")
    obsidian_base_folder: str = Field(default="Recoleta", validation_alias="OBSIDIAN_BASE_FOLDER")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    log_json: bool = Field(default=False, validation_alias="LOG_JSON")
    write_debug_artifacts: bool = Field(default=False, validation_alias="WRITE_DEBUG_ARTIFACTS")

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

    @field_validator("obsidian_vault_path", mode="before")
    @classmethod
    def _normalize_vault_path(cls, value: str | Path) -> Path:
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

    @field_validator("config_path", mode="before")
    @classmethod
    def _normalize_optional_config_path(cls, value: str | Path | None) -> Path | None:
        if value is None:
            return None
        return Path(value).expanduser().resolve()

    def safe_fingerprint(self) -> str:
        payload = self.model_dump(mode="json")
        payload["telegram_bot_token"] = "***"
        payload["telegram_chat_id"] = "***"
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
