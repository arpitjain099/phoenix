"""General models."""
import datetime

from sqlalchemy import orm

from phiphi.core import db


class TimestampModel(db.Base):
    """Generalised TimestampModel."""

    __abstract__ = True

    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        # When we want to test the created_at we have to use the lambda
        # https://github.com/spulec/freezegun/issues/306
        default=lambda: datetime.datetime.now()
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now()
    )
