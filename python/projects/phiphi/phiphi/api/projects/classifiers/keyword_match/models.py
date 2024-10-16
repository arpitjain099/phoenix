"""Keyword Match models."""
import sqlalchemy as sa
from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models


class IntermediatoryClassToKeywordConfigBase(platform_db.Base):
    """Intermediatory class to keyword config table base.

    The intermediatory table stores the "live" table, on which all edits and additions to
    the list of class_to_keyword_configs are made.

    When a new version of the classifier is created, the table is copied to the
    "class_to_keyword_configs" attribute in the `params` of the classifier_versions table. Pipeline
    classifiers then use the versioned params to classify data.
    """

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    classifier_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("classifiers.id"))
    class_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("intermediatory_classes.id"))
    # It is important for the unique constraint to work correctly that the musts and nots are not
    # NULL.
    musts: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False)
    # We are using a default value of "" for nots to ensure that the unique constraint works
    nots: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=False, default="")


class IntermediatoryClassToKeywordConfig(
    IntermediatoryClassToKeywordConfigBase, base_models.TimestampModel
):
    """Intermediatory class to keyword config table."""

    __tablename__ = "intermediatory_class_to_keyword_configs"

    __table_args__ = (
        # For clarification, the unique constraint will treat NULLs as the different values so that
        # two rows with the same musts and NULL nots are not considered duplicates.
        sa.UniqueConstraint(
            "classifier_id",
            "class_id",
            "musts",
            "nots",
            name="uq_intermediatory_class_to_keyword_configs",
        ),
        sa.Index("ix_intermediatory_class_to_keyword_configs", "classifier_id", "class_id"),
    )
