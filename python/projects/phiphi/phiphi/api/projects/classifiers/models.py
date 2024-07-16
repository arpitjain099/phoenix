"""Models for classifiers tables."""
from typing import Optional

from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models


class ClassifiersBase(platform_db.Base):
    """Classifiers model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    project_id: orm.Mapped[int]
    classifier_name: orm.Mapped[str]
    classifier_type: orm.Mapped[str]
    classifier_params: orm.Mapped[Optional[str]] = orm.mapped_column(base_models.JSONEncodedValue)
    deleted: orm.Mapped[bool]


class Classifiers(ClassifiersBase):
    """Classifiers tables."""

    __tablename__ = "classifiers"
