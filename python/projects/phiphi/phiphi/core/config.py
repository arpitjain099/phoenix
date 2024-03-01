"""Configuration of phiphi application."""
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings of the app taken from environment variables."""

    # DB ENVIRONMENT
    SQLALCHEMY_DATABASE_URI: str


# Be aware that environment variables will overwrite the variables in the settings
if os.environ.get("SETTINGS_ENV_FILE"):
    settings = Settings(_env_file=os.environ.get("SETTINGS_ENV_FILE"))  # type: ignore [call-arg]
else:
    settings = Settings()  # type: ignore [call-arg]
