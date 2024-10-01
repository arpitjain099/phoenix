"""Models for classifiers and classifier versions tables."""
import datetime
from typing import Dict, Optional

import sqlalchemy as sa
from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models


class ClassifiersBase(platform_db.Base):
    """Classifiers model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    project_id: orm.Mapped[int]
    name: orm.Mapped[str]
    type: orm.Mapped[str]
    archived_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(nullable=True)


class Classifiers(ClassifiersBase, base_models.TimestampModel):
    """Classifiers table."""

    __tablename__ = "classifiers"

    # Relationship to ClassifierVersions
    classifier_versions: orm.Mapped[list["ClassifierVersions"]] = orm.relationship(
        back_populates="classifier",
        cascade="all, delete-orphan",
        order_by="ClassifierVersions.version_id.desc()",  # Ensures ordered by desc version_id
        lazy="dynamic",
    )

    @property
    def latest_version(self) -> "ClassifierVersions":
        """Get the latest version of the classifier."""
        return self.classifier_versions.first()

    def get_all_versions(self) -> list["ClassifierVersions"]:
        """Get all versions of the classifier."""
        return self.classifier_versions.all()


class ClassifierVersionsBase(platform_db.Base):
    """Classifier versions table."""

    __abstract__ = True

    __tablename__ = "classifier_versions"

    version_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    classifier_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("classifiers.id"))
    classes_dict: orm.Mapped[Dict[str, str]] = orm.mapped_column(base_models.JSONEncodedValue)
    params: orm.Mapped[Optional[str]] = orm.mapped_column(base_models.JSONEncodedValue)


class ClassifierVersions(ClassifierVersionsBase, base_models.TimestampModel):
    """Classifier versions table."""

    __tablename__ = "classifier_versions"

    # Relationship back to Classifiers
    classifier: orm.Mapped[Classifiers] = orm.relationship(
        "Classifiers", back_populates="classifier_versions"
    )
