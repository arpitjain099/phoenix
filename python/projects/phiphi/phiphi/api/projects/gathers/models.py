"""Gather Models."""
import datetime
from typing import Optional

from phiphi import platform_db
from phiphi.api import base_models
from sqlalchemy import orm


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

    apify_facebook_post_gather = orm.relationship(
        "ApifyFacebookPostGather", back_populates="gather", uselist=False
    )
