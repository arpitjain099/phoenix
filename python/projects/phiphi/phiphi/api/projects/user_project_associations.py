"""Associations for users and projects.

This is used to create permissions for users on projects.
"""
from sqlalchemy import ForeignKey, Index, orm

from phiphi import platform_db
from phiphi.api import base_models


class UserProjectAssociationsBase(platform_db.Base):
    """UserProjectAssociation base model."""

    __abstract__ = True

    user_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("users.id"), primary_key=True)
    project_id: orm.Mapped[int] = orm.mapped_column(ForeignKey("projects.id"), primary_key=True)
    role: orm.Mapped[str]


class UserProjectAssociations(UserProjectAssociationsBase, base_models.TimestampModel):
    """UserProjectAssociation model."""

    __tablename__ = "user_project_associations"

    __table_args__ = (Index("idx_user_id_project_id_role", "user_id", "project_id", "role"),)

    user = orm.relationship("User")
    project = orm.relationship("Project")
