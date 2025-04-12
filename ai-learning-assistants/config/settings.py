"""
Application settings module.

Loads configuration from environment variables and provides
validated settings for the application.
"""

import os
from typing import Optional

from pydantic import validator, AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App configuration
    app_env: str = "development"
    log_level: str = "INFO"
    enable_telemetry: bool = False
    
    # Azure OpenAI Service configuration
    azure_openai_api_key: str
    azure_openai_endpoint: AnyHttpUrl
    azure_openai_chat_deployment_name: str
    
    # Database configuration (for future implementation)
    db_host: Optional[str] = None
    db_port: Optional[int] = None
    db_name: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    
    @validator("app_env")
    def validate_app_env(cls, v):
        """Validate app environment."""
        allowed = ["development", "testing", "production"]
        if v.lower() not in allowed:
            raise ValueError(f"app_env must be one of: {', '.join(allowed)}")
        return v.lower()
    
    @validator("log_level")
    def validate_log_level(cls, v):
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"log_level must be one of: {', '.join(allowed)}")
        return v.upper()
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Load settings from environment variables
settings = Settings()