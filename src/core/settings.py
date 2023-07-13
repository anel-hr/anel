import os
from pathlib import Path

from pydantic_settings import BaseSettings

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent


class Settings(BaseSettings):
    """Base settings object to inherit from."""

    class Config:
        env_file = os.path.join(PROJECT_ROOT_DIR, ".env")
        env_file_encoding = "utf-8"


class AppSettings(Settings):
    """Application settings."""

    app_name: str = "Anel"
    host: str = "0.0.0.0"
    port: int = 8080

    log_level = "INFO"
    app_secret_key: str


settings = AppSettings()
