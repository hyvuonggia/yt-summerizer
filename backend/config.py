"""
Configuration settings for the YouTube Video Summarizer backend.

Loads environment variables and provides typed settings for the application.
"""

import os
from typing import List
from dotenv import load_dotenv

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
    print(f"⚠️  Configuration warning: {e}")
    print("   Some features may not work without proper configuration.")