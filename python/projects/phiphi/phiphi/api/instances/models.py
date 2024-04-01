"""Instance Models."""
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_models
from sqlalchemy import orm


class InstanceBase(platform_db.Base):
    """Instance Model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(index=True, unique=True)
    description: orm.Mapped[Optional[str]]
    environment_key: orm.Mapped[Optional[str]]
    pi_deleted_after: orm.Mapped[Optional[int]]
    deleted_after: orm.Mapped[Optional[int]]
    expected_usage: orm.Mapped[Optional[str]]


class Instance(InstanceBase, base_models.TimestampModel):
    """Instance model that can inherit from multiple models."""

    __tablename__ = "instances"
