"""Configuration of phiphi application."""
import logging
import os

import pydantic
from pydantic import networks
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings
from typing_extensions import Annotated

logger = logging.getLogger(__name__)

# Validate sqlite URLs: sqlite://, sqlite+aiosqlite://
SqliteDsn = Annotated[
    MultiHostUrl,
    networks.UrlConstraints(
        host_required=False,
        allowed_schemes=[
            "sqlite",
            # Async
            "sqlite+aiosqlite",
        ],
    ),
]


class Settings(BaseSettings):
    """Settings of the app taken from environment variables."""

    TITLE: str = "phiphi"
    VERSION: str = "v0.0.1"

    # DB ENVIRONMENT
    SQLALCHEMY_DATABASE_URI: SqliteDsn | pydantic.PostgresDsn
    TESTING_SQLALCHEMY_DATABASE_URI: SqliteDsn | pydantic.PostgresDsn

    # Seed data
    FIRST_ADMIN_USER_EMAIL: pydantic.EmailStr = "admin@admin.com"
    FIRST_ADMIN_USER_DISPLAY_NAME: str = "admin"

    # Authorization
    # This is the header that will be used to get the user email
    # x-auth-request-email is the one set for oauth2-proxy
    HEADER_AUTH_NAME: str = "x-auth-request-email"


if os.environ.get("SETTINGS_ENV_FILE"):
    logger.warning(
        f"Using settings file: {os.environ.get('SETTINGS_ENV_FILE')}."
        " Be aware that environment variables will take priority over variables defined in the"
        " settings file."
        " IE. `export TITLE='title_env'` will override the TITLE='title_file' variable in the"
        " settings file."
    )
    settings = Settings(_env_file=os.environ.get("SETTINGS_ENV_FILE"))  # type: ignore [call-arg]
else:
    settings = Settings()  # type: ignore [call-arg]
