"""Manual post authors ORModels."""
import sqlalchemy as sa
from sqlalchemy import orm

from phiphi import platform_db
from phiphi.api import base_models


class IntermediatoryClassifiedPostAuthorsBase(platform_db.Base):
    """Intermediatory classified post authors table.

    The intermediatory table stores the "live" table, on which all edits and additions to
    the list of classified authors are made.

    When a new version of the classifier is created, the table is copied to the
    "classified_authors" attribute in the `params` of the classifier_versions table. Pipeline
    classifiers then use the versioned params to classify data.
    """

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    classifier_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("classifiers.id"))
    class_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("intermediatory_classes.id"))
    # This the author id from the project db
    phoenix_platform_message_author_id: orm.Mapped[str] = orm.mapped_column(
        sa.String, nullable=False
    )


class IntermediatoryClassifiedPostAuthors(
    IntermediatoryClassifiedPostAuthorsBase, base_models.TimestampModel
):
    """Intermediatory classified authors table."""

    __tablename__ = "intermediatory_classified_post_authors"

    __table_args__ = (
        sa.UniqueConstraint(
            "classifier_id",
            "class_id",
            "phoenix_platform_message_author_id",
            name="uq_intermediatory_classified_authors",
        ),
        sa.Index("ix_intermediatory_classified_authors", "classifier_id", "class_id"),
        # We are adding an index on class_id to speed
        sa.Index("ix_intermediatory_classified_authors_class", "class_id"),
        # We are adding an index on phoenix_platform_message_author_id as we are going to do a join
        # on this id from the project data
        sa.Index(
            "ix_intermediatory_classified_authors_phoenix_id", "phoenix_platform_message_author_id"
        ),
    )
