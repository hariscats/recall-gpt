"""
Configuration settings for the AI Learning Assistant application.
"""
import os
from enum import Enum
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseModel, Field, model_validator, field_validator, AnyHttpUrl

# Load environment variables
load_dotenv()

class AppEnvironment(str, Enum):
    """Application environment types."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

class AppSettings(BaseModel):
    """Application configuration settings."""

    # Azure OpenAI Configuration
    azure_openai_api_key: str = Field(default="dev_key", description="Azure OpenAI API key")
    azure_openai_endpoint: str = Field(default="https://example.com", description="Azure OpenAI endpoint URL")
    azure_openai_chat_deployment_name: str = Field(default="dev_deployment", description="Azure OpenAI chat deployment name")
    azure_ai_agent_id: str = Field(default="dev_agent", description="Azure AI Agent ID for Learning Assistant")
    
    # Database Configuration
    database_url: str = Field(default="sqlite:///./test.db", description="Database connection URL")
    
    # Application Settings
    app_env: AppEnvironment = Field(
        default=AppEnvironment.DEVELOPMENT,
        description="Application environment"
    )
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    enable_telemetry: bool = Field(default=False, description="Enable OpenTelemetry")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "",
        "case_sensitive": False,
        "env_nested_delimiter": "__",
    }

def get_settings() -> AppSettings:
    """
    Get application settings with default values for development.
    
    Returns:
        AppSettings: Application settings with defaults.
    """
    try:
        # Simply use defaults for development
        return AppSettings()
    except Exception as e:
        raise ValueError(f"Error loading application settings: {str(e)}")

# Create a global instance of settings
settings = get_settings()