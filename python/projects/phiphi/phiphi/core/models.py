"""General models."""
import datetime

from sqlalchemy import orm

from phiphi.core import db


class TimestampModel(db.Base):
    """Generalised TimestampModel."""

    __abstract__ = True

    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(default=datetime.datetime.now)
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
