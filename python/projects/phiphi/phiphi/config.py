"""Configuration of phiphi application."""
import logging
import os
from typing import Any, Optional

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


def parse_cors(v: Any) -> list[str] | str:
    """Parse cors origins into a list or str.

    Taken from:
    https://github.com/tiangolo/full-stack-fastapi-template/blob/master/backend/app/core/config.py#L18C1-L23C24
    """
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    """Settings of the app taken from environment variables."""

    TITLE: str = "phiphi"
    VERSION: str = "v0.0.1"

    # Cors
    # From https://github.com/tiangolo/full-stack-fastapi-template/blob/master/backend/app/core/config.py#L45
    CORS_ORIGINS: Annotated[list[pydantic.AnyUrl] | str, pydantic.BeforeValidator(parse_cors)] = []

    # DB ENVIRONMENT
    SQLALCHEMY_DATABASE_URI: SqliteDsn | pydantic.PostgresDsn
    TESTING_SQLALCHEMY_DATABASE_URI: SqliteDsn | pydantic.PostgresDsn

    # Seed data
    FIRST_ADMIN_USER_EMAIL: pydantic.EmailStr = "admin@admin.com"
    FIRST_ADMIN_USER_DISPLAY_NAME: str = "admin"
    FIRST_ENVIRONMENT_SLUG: str = "main"
    FIRST_ENVIRONMENT_NAME: str = "Main environment"
    FIRST_ENVIRONMENT_DESCRIPTION: str = "Main default environment of phoenix"

    # Authorization
    # This is the header that will be used to get the user email
    # x-auth-request-email is the one set for oauth2-proxy
    HEADER_AUTH_NAME: str = "x-auth-request-email"
    # For Development Use Only!!
    # For cookie AUTH to be active both USE_COOKIE_AUTH and COOKIE_AUTH_NAME must be set
    USE_COOKIE_AUTH: bool = False
    # Name of the cookie that holds the email of the user
    COOKIE_AUTH_NAME: Optional[str] = None


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
