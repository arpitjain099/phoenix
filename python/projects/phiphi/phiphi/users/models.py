"""User Models."""
from typing import Optional

from sqlalchemy import orm

from phiphi.core import db, models


class UserBase(db.Base):
    """User model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(index=True)
    display_name: orm.Mapped[Optional[str]]


class User(UserBase, models.TimestampModel):
    """User model that can inherit from multiple models."""

    __tablename__ = "users"
