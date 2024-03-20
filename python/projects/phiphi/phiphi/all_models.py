"""All models of the application.

This module is used to import all models of the application to be used in the
Alembic migrations and testing.
"""
from phiphi.core import db
from phiphi.users import models  # noqa: F401

Base = db.Base
base_metadata = Base.metadata
