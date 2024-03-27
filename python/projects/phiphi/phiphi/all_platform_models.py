"""All models of the application.

This module is used to import all models of the application to be used in the
Alembic migrations and testing.
"""
from phiphi import platform_db
from phiphi.api.users import models  # noqa: F401

Base = platform_db.Base
base_metadata = Base.metadata
