"""
AI Marketing Content Engine — Configuration

All application settings loaded from environment variables via pydantic-settings.
"""

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # ── Application ──────────────────────────────────────────────
    app_name: str = "AI Marketing Content Engine"
    app_env: str = "development"
    debug: bool = True

    # ── Database ─────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://marketing:marketing_secret_2024@postgres:5432/marketing_engine"

    # ── Backend ──────────────────────────────────────────────────
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ── LLM Provider ────────────────────────────────────────────
    llm_provider: str = "openai"  # openai | anthropic | gemini

    # OpenAI
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o"

    # Anthropic
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"

    # Google Gemini
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash"

    # LLM Generation Settings
    llm_max_retries: int = 2
    llm_timeout: int = 120
    llm_temperature: float = 0.7

    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string or JSON list."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [origin.strip() for origin in v.split(",")]
        return v

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


# Singleton settings instance
settings = Settings()
