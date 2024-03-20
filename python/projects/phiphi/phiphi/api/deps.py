"""Api Dependencies."""
from typing import Annotated, Callable

import fastapi
from sqlalchemy.orm import Session

from phiphi import config, platform_db
from phiphi.users import crud as user_crud
from phiphi.users import schemas as user_schemas

SessionDep = Annotated[Session, fastapi.Depends(platform_db.get_session)]

USER_NOT_FOUND = fastapi.HTTPException(
    status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
    detail="Cannot authenticate.",
)

# Using auto_error=False as we want to handle the error ourselves
# so we can use multiple authentication methods such as cookies and headers
email_header_scheme = fastapi.security.APIKeyHeader(
    name=config.settings.HEADER_AUTH_NAME, auto_error=False
)

EmailHeaderDep = Annotated[str, fastapi.Depends(email_header_scheme)]


# Using a noop function for the email_cookie_scheme so that if COOKIE_AUTH_NAME is None there are
# no errors.
def noop() -> None:
    """No operation."""
    return None


email_cookie_scheme: Callable[[], None] | fastapi.security.APIKeyCookie = noop

if config.settings.USE_COOKIE_AUTH and config.settings.COOKIE_AUTH_NAME:
    email_cookie_scheme = fastapi.security.APIKeyCookie(
        name=config.settings.COOKIE_AUTH_NAME, auto_error=False
    )

EmailCookieDep = Annotated[str, fastapi.Depends(email_cookie_scheme)]


def get_current_user(
    email: EmailHeaderDep,
    session: SessionDep,
    email_cookie: EmailCookieDep,
    request: fastapi.Request,
) -> user_schemas.User:
    """Get the current user."""
    # Header takes precedence over cookie
    if email is None and config.settings.USE_COOKIE_AUTH:
        email = email_cookie

    if not email:
        raise USER_NOT_FOUND

    user = user_crud.get_user_by_email(session, email)
    if user is None:
        raise USER_NOT_FOUND

    return user


CurrentUser = Annotated[user_schemas.User, fastapi.Depends(get_current_user)]
