"""Models for classifiers and classifier versions tables."""
import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models
from phiphi.api.projects.job_runs import models as job_run_models
from phiphi.api.projects.job_runs import schemas as job_run_schemas


class ClassifierVersionsBase(platform_db.Base):
    """Classifier versions table."""

    __abstract__ = True

    __tablename__ = "classifier_versions"

    version_id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    classifier_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("classifiers.id"))
    classes: orm.Mapped[str] = orm.mapped_column(base_models.JSONEncodedValue)
    params: orm.Mapped[Optional[str]] = orm.mapped_column(base_models.JSONEncodedValue)


class ClassifierVersions(ClassifierVersionsBase, base_models.TimestampModel):
    """Classifier versions table."""

    __tablename__ = "classifier_versions"


class ClassifiersBase(platform_db.Base):
    """Classifiers model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    project_id: orm.Mapped[int]
    name: orm.Mapped[str]
    type: orm.Mapped[str]
    archived_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(nullable=True)


job_run_foreign_type_query = (
    "or_("
    f"JobRuns.foreign_job_type=='{job_run_schemas.ForeignJobType.classify.value}',"
    f"JobRuns.foreign_job_type=='{job_run_schemas.ForeignJobType.classify_tabulate.value}'"
    ")"
)


class Classifiers(ClassifiersBase, base_models.TimestampModel):
    """Classifiers table."""

    __tablename__ = "classifiers"

    # Relationship to ClassifierVersions
    classifier_versions = orm.relationship(
        "ClassifierVersions",
        cascade="all, delete-orphan",
        order_by="ClassifierVersions.version_id.desc()",  # Ensures ordered by desc version_id
        lazy="dynamic",
    )

    intermediatory_classes = orm.relationship(
        "IntermediatoryClasses",
        cascade="all, delete-orphan",
        order_by="IntermediatoryClasses.id",
        lazy="dynamic",
    )

    # Relationship to get all related JobRuns, ordered by id descending
    job_runs = orm.relationship(
        "JobRuns",
        order_by="desc(JobRuns.id)",
        primaryjoin=(
            f"and_({job_run_foreign_type_query}, foreign(JobRuns.foreign_id)==Classifiers.id)"
        ),
        lazy="dynamic",
    )

    @property
    def latest_version(self) -> ClassifierVersions:
        """Get the latest version of the classifier."""
        latest_version: ClassifierVersions = self.classifier_versions.first()
        return latest_version

    def all_versions(self) -> list[ClassifierVersions]:
        """Get all versions of the classifier."""
        latest_versions: list[ClassifierVersions] = self.classifier_versions.all()
        return latest_versions

    @property
    def latest_job_run(self) -> job_run_models.JobRuns | None:
        """Property to get the most recent JobRun."""
        latest_run: job_run_models.JobRuns | None = self.job_runs.first()

        if latest_run is None:
            return None

        return latest_run


class IntermediatoryClassesBase(platform_db.Base):
    """Intermediatory classes table base.

    The intermediatory classes table stores the "live" table, on which all edits and additions to
    the classes are applied to.

    When a new version of the classifier is created, the classes are copied from this table to the
    classifier_versions table.
    """

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    classifier_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("classifiers.id"))
    name: orm.Mapped[str]
    description: orm.Mapped[str]


class IntermediatoryClasses(IntermediatoryClassesBase, base_models.TimestampModel):
    """Intermediatory classes table."""

    __tablename__ = "intermediatory_classes"

    __table_args__ = (
        sa.UniqueConstraint("classifier_id", "name", name="uq_classifier_classname"),
        sa.Index("ix_classifier_classname", "classifier_id", "name"),
    )
