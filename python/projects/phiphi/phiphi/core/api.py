"""Core api functionality."""
from typing import Annotated

import fastapi
from sqlalchemy.orm import Session

from phiphi.core import db

SessionDep = Annotated[Session, fastapi.Depends(db.get_session)]
