"""Instance Models."""
from typing import Optional

from sqlalchemy import ForeignKey, orm

from phiphi import platform_db
from phiphi.api import base_models


class InstanceBase(platform_db.Base):
    """Instance Model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    description: orm.Mapped[str]
    environment_slug: orm.Mapped[str] = orm.mapped_column(
        ForeignKey("environments.slug"), default="main"
    )
    pi_deleted_after_days: orm.Mapped[int]
    delete_after_days: orm.Mapped[int]
    expected_usage: orm.Mapped[Optional[str]]


class Instance(InstanceBase, base_models.TimestampModel):
    """Instance model that can inherit from multiple models."""

    __tablename__ = "instances"
