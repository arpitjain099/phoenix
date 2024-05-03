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
    project_id: orm.Mapped[int]
    source: orm.Mapped[Optional[str]]
    platform: orm.Mapped[Optional[str]]
    data_type: orm.Mapped[Optional[str]]
    deleted_at: orm.Mapped[Optional[datetime.datetime]]
    child_type: orm.Mapped[Optional[str]]


class Gather(GatherBase, base_models.TimestampModel):
    """Gather model that can inherit from multiple models."""

    __tablename__ = "gathers"
    __mapper_args__ = {
        "polymorphic_identity": "gather",
        "polymorphic_on": "child_type",
    }

    apify_gather = orm.relationship("ApifyGather", back_populates="gather", uselist=False)


class ApifyGather(Gather):
    """Apify Gather model."""

    __tablename__ = "apify_gathers"
    __mapper_args__ = {
        "polymorphic_identity": "apify_facebook_posts",
    }

    id: orm.Mapped[int] = orm.mapped_column(ForeignKey("gathers.id"), primary_key=True)
    limit_posts_per_account: orm.Mapped[int]
    limit_replies: orm.Mapped[int]
    nested_replies: orm.Mapped[bool]
    input: orm.Mapped[str] = orm.mapped_column(base_models.JSONEncodedValue)

    gather = orm.relationship("Gather", back_populates="apify_gather")
