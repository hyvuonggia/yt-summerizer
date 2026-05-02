"""
Configuration settings for the YouTube Video Summarizer backend.

Loads environment variables and provides typed settings for the application.
"""

import os
import logging
from typing import List
from dotenv import load_dotenv

# Configure logging for config module
config_logger = logging.getLogger("backend.config")

# Load .env file if it exists.
# override=True ensures .env values always take precedence over shell env vars.
load_dotenv(override=True)


def _get_env(key: str, default: str) -> str:
    """Get environment variable with fallback."""
    return os.getenv(key, default)


def _get_env_int(key: str, default: str) -> int:
    """Get environment variable as integer with fallback."""
    return int(os.getenv(key, default))


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Environment
        self.environment: str = _get_env("ENVIRONMENT", "development")
        
        # API Configuration
        self.api_host: str = _get_env("API_HOST", "0.0.0.0")
        self.api_port: int = _get_env_int("API_PORT", "8000")
        
        # CORS Configuration
        cors_str = _get_env("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
        self.cors_origins: List[str] = [o.strip() for o in cors_str.split(",") if o.strip()]
        
        # LLM Configuration (OpenRouter)
        self.openrouter_api_key: str = _get_env("OPENROUTER_API_KEY", "")
        # Fall back to default when env var is present but empty (e.g. OPENROUTER_BASE_URL=)
        self.openrouter_base_url: str = _get_env("OPENROUTER_BASE_URL", "") or "https://openrouter.ai/api/v1"
        self.llm_provider: str = _get_env("LLM_PROVIDER", "openrouter")
        self.llm_model: str = _get_env("LLM_MODEL", "deepseek/deepseek-v3.2")
        
        # Token Limits
        self.max_input_tokens: int = _get_env_int("MAX_INPUT_TOKENS", "120000")  # DeepSeek v3.2 has 128K context
        self.max_output_tokens: int = _get_env_int("MAX_OUTPUT_TOKENS", "500")
        
        # YouTube API Configuration
        self.youtube_timeout: int = _get_env_int("YOUTUBE_TIMEOUT", "30")
        self.youtube_max_retries: int = _get_env_int("YOUTUBE_MAX_RETRIES", "3")
        
        # Logging
        self.log_level: str = _get_env("LOG_LEVEL", "INFO")
        
        # Database Configuration (Sprint P3.2 - MySQL)
        self.db_host: str = _get_env("DB_HOST", "localhost")
        self.db_port: int = _get_env_int("DB_PORT", "3306")
        self.db_user: str = _get_env("DB_USER", "yt_summerizer")
        self.db_password: str = _get_env("DB_PASSWORD", "")
        self.db_name: str = _get_env("DB_NAME", "yt_summerizer")
    
    @property
    def database_url(self) -> str:
        """Get the async database URL for SQLAlchemy."""
        from urllib.parse import quote_plus
        password = quote_plus(self.db_password) if self.db_password else ""
        user = quote_plus(self.db_user) if self.db_user else ""
        return f"mysql+aiomysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def sync_database_url(self) -> str:
        """Get the sync database URL for SQLAlchemy (for migrations)."""
        from urllib.parse import quote_plus
        password = quote_plus(self.db_password) if self.db_password else ""
        user = quote_plus(self.db_user) if self.db_user else ""
        return f"mysql+pymysql://{user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"


# Global settings instance
settings = Settings()


def validate_settings():
    """Validate critical settings and raise errors if missing."""
    errors = []
    
    if not settings.openrouter_api_key:
        errors.append("OPENROUTER_API_KEY is required in environment variables")
    
    if not settings.llm_model:
        errors.append("LLM_MODEL is required in environment variables")
    
    if errors:
        raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    return True


# Validate on import (optional - can be called explicitly)
try:
    validate_settings()
except ValueError as e:
    config_logger.warning(f"Configuration warning: {e}")
    config_logger.warning("Some features may not work without proper configuration.")