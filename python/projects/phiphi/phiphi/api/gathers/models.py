"""Gather Models."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_models
from sqlalchemy import ForeignKey, orm


class GatherBase(platform_db.Base):
    """Gather model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    description: orm.Mapped[str]
    mark_to_delete: orm.Mapped[Optional[bool]]
    last_run_at: orm.Mapped[Optional[datetime.datetime]]
    gather_type: orm.Mapped[str]
    instance_id: orm.Mapped[int]


class Gather(GatherBase, base_models.TimestampModel):
    """Gather model that can inherit from multiple models."""

    __tablename__ = "gathers"
    __mapper_args__ = {
        "polymorphic_identity": "gather",
        "polymorphic_on": "gather_type",
    }

    apify_gather = orm.relationship("ApifyGather", back_populates="gather", uselist=False)


class ApifyGather(Gather):
    """Apify Gather model."""

    __tablename__ = "apify_gathers"
    __mapper_args__ = {
        "polymorphic_identity": "apify_gathers",
        # "inherit_condition": (id == Gather.id)
    }

    id: orm.Mapped[int] = orm.mapped_column(ForeignKey("gathers.id"), primary_key=True)
    source: orm.Mapped[Optional[str]]
    platform: orm.Mapped[Optional[str]]
    data_type: orm.Mapped[Optional[str]]
    start_date: orm.Mapped[Optional[datetime.datetime]]
    end_date: orm.Mapped[Optional[datetime.datetime]]
    limit_messages: orm.Mapped[int]
    limit_replies: orm.Mapped[int]
    nested_replies: orm.Mapped[bool]
    input_data: orm.Mapped[str]
    input_type: orm.Mapped[str]

    gather = orm.relationship("Gather", back_populates="apify_gather")
