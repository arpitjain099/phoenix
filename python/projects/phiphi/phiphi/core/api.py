"""Core api functionality."""
from typing import Annotated

import fastapi
from sqlalchemy.orm import Session

from phiphi.core import config, db
from phiphi.users import crud as user_crud
from phiphi.users import schemas as user_schemas

SessionDep = Annotated[Session, fastapi.Depends(db.get_session)]

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


def get_current_user(email: EmailHeaderDep, session: SessionDep) -> user_schemas.User:
    """Get the current user."""
    if not email:
        raise USER_NOT_FOUND

    user = user_crud.get_user_by_email(session, email)
    if user is None:
        raise USER_NOT_FOUND

    return user


CurrentUser = Annotated[user_schemas.User, fastapi.Depends(get_current_user)]
