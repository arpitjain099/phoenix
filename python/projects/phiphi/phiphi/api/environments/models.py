"""Environment Models."""

from phiphi import platform_db
from phiphi.api import base_models
from sqlalchemy import orm


class EnvironmentBase(platform_db.Base):
    """Environment Model."""

    __abstract__ = True

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    name: orm.Mapped[str]
    description: orm.Mapped[str]
    unique_id: orm.Mapped[str]


class Environment(EnvironmentBase, base_models.TimestampModel):
    """Environment model that can inherit from multiple models."""

    __tablename__ = "environments"
