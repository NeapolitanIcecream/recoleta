from __future__ import annotations

import hashlib
import json
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ArxivSourceConfig(BaseModel):
    queries: list[str] = Field(default_factory=list)
    max_results_per_run: int = 50


class HNSourceConfig(BaseModel):
    rss_urls: list[str] = Field(default_factory=lambda: ["https://news.ycombinator.com/rss"])


class HFDailySourceConfig(BaseModel):
    enabled: bool = True


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
    )

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

    def safe_fingerprint(self) -> str:
        payload = self.model_dump(mode="json")
        payload["telegram_bot_token"] = "***"
        payload["telegram_chat_id"] = "***"
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()
