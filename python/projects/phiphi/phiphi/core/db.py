"""Database."""
import logging
from typing import Generator

from sqlalchemy import DDL, MetaData, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session

from phiphi.core import config

logger = logging.getLogger(__name__)

SCHEMA = "platform"


class Base(DeclarativeBase):
    """Base model.

    This will create all models in the schema `platform`.
    """

    metadata = MetaData(schema=SCHEMA)


# This is needed so that create_all will also create the schema
event.listen(Base.metadata, "before_create", DDL("CREATE SCHEMA IF NOT EXISTS " + SCHEMA))


engine = create_engine(str(config.settings.SQLALCHEMY_DATABASE_URI))


def get_session() -> Generator[Session, None, None]:
    """Get the session."""
    with Session(engine) as session:
        yield session
