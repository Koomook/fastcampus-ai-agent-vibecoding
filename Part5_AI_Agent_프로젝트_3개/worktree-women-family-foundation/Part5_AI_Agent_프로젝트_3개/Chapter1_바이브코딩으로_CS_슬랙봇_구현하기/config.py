"""
Configuration settings for Slack Claude Bot.
Loads environment variables from .env file.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Slack credentials
    SLACK_BOT_TOKEN: str
    SLACK_SIGNING_SECRET: str

    # Optional: For future phases
    ANTHROPIC_API_KEY: str = ""
    NOTION_API_KEY: str = ""
    NOTION_DATABASE_ID: str = ""

    # Notion MCP (Phase 3)
    NOTION_TOKEN: str = ""  # Notion integration token for MCP server

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


# Global settings instance
settings = Settings()
