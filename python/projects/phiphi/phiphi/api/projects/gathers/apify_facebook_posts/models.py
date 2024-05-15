"""Apify facebook posts gather model."""
from typing import Optional

from phiphi.api import base_models
from phiphi.api.projects.gathers import models as gather_models
from sqlalchemy import ForeignKey, orm


class ApifyFacebookPostGather(gather_models.Gather):
    """Apify Gather model."""

    __tablename__ = "apify_facebook_post_gathers"
    __mapper_args__ = {
        "polymorphic_identity": "apify_facebook_posts",
    }

    id: orm.Mapped[int] = orm.mapped_column(ForeignKey("gathers.id"), primary_key=True)
    limit_posts_per_account: orm.Mapped[int]
    account_url_list: orm.Mapped[str] = orm.mapped_column(base_models.JSONEncodedValue)
    only_posts_older_than: orm.Mapped[Optional[str]]
    only_posts_newer_than: orm.Mapped[Optional[str]]
