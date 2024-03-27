"""Base models.

This module contains the base models that are used by other
models in the application.

Usage:
    The models in this module are not meant to be used directly.
    Instead, they are meant to be inherited by other models.

    ```python
    class MyModel(MyBaseModel, base_models.TimestampModel):
        pass
    ```

    The above example shows how to inherit from the TimestampModel.
    Using base models in this way allows for easy reuse of common fields.
"""
import datetime

from sqlalchemy import orm

from phiphi import platform_db


class TimestampModel(platform_db.Base):
    """Time stamp columns to be used as a base."""

    __abstract__ = True

    created_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        # When we want to test the created_at we have to use the lambda
        # https://github.com/spulec/freezegun/issues/306
        default=lambda: datetime.datetime.now()
    )
    updated_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        default=lambda: datetime.datetime.now(), onupdate=lambda: datetime.datetime.now()
    )
