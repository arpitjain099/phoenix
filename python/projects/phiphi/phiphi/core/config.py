"""Configuration of phiphi application."""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings of the app taken from environment variables."""

    # DB ENVIRONMENT
    SQLALCHEMY_DATABASE_URI: str


if os.environ.get("SETTINGS_ENV_FILE"):
    settings = Settings(_env_file=os.environ.get("SETTINGS_ENV_FILE"))  # type: ignore [call-arg]
else:
    settings = Settings()  # type: ignore [call-arg]
