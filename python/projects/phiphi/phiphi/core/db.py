"""Database."""
import logging
from typing import Generator

from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from phiphi.core import config

logger = logging.getLogger(__name__)

SCHEMA = "platform"


class Base(DeclarativeBase):
    """Base model.

    This will create all models in the schema `platform`.
    """

    metadata = MetaData(schema=SCHEMA)


engine = create_engine(str(config.settings.SQLALCHEMY_DATABASE_URI))


def get_session() -> Generator[Session, None, None]:
    """Get the session."""
    with Session(engine) as session:
        yield session
