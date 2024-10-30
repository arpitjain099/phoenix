"""Associations for users and projects.

This is used to create permissions for users on projects.
"""
import datetime
from enum import Enum

import pydantic
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


class Role(str, Enum):
    """Role for user project associations."""

    # Currently user but we plan to have `manager` and `viewer` roles
    user = "user"


class UserProjectAssociationCreate(pydantic.BaseModel):
    """User project association create."""

    role: Role = Role.user


class UserProjectAssociationResponse(pydantic.BaseModel):
    """User project association response."""

    model_config = pydantic.ConfigDict(from_attributes=True)
    user_id: int
    project_id: int
    role: Role
    created_at: datetime.datetime


def create_user_project_association(
    session: orm.Session,
    project_id: int,
    user_id: int,
    user_project_association: UserProjectAssociationCreate,
) -> UserProjectAssociationResponse:
    """Create a user project association."""
    association = UserProjectAssociations(
        **user_project_association.dict(), project_id=project_id, user_id=user_id
    )
    session.add(association)
    session.commit()
    session.refresh(association)
    return UserProjectAssociationResponse.model_validate(association)
