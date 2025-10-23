"""Configuration management for Playwright MCP Client."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for Playwright MCP Client."""

    anthropic_api_key: str
    playwright_server_path: str
    playwright_server_args: str
    output_dir: Path = Path("./output")

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "Config":
        """Load configuration from environment variables.

        Args:
            env_file: Path to .env file. If None, searches for .env in current directory.

        Returns:
            Config instance with loaded values.

        Raises:
            ValueError: If required environment variables are missing.
        """
        # Load .env file if it exists
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()

        # Get required environment variables
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        server_path = os.getenv("PLAYWRIGHT_MCP_SERVER_PATH", "npx")
        server_args = os.getenv("PLAYWRIGHT_MCP_SERVER_ARGS", "@playwright/mcp@latest")

        return cls(
            anthropic_api_key=api_key,
            playwright_server_path=server_path,
            playwright_server_args=server_args,
        )

    def ensure_output_dir(self) -> None:
        """Ensure output directory exists."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
