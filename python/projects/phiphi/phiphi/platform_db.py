"""Database."""
import logging
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from phiphi import config

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    """Base model."""


engine = create_engine(str(config.settings.SQLALCHEMY_DATABASE_URI))


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Get the session."""
    with Session(engine) as session:
        yield session
